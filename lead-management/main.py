#!/usr/bin/env python3
"""
Lead Management System with Incredible API
==========================================

This example demonstrates how to:
1. Scan Gmail for potential leads
2. Extract and score lead information
3. Store leads in Google Sheets CRM
4. Send personalized follow-up emails

Usage:
    python main.py

Features:
    - Automatic lead detection from emails
    - Lead scoring based on content analysis
    - CRM integration with Google Sheets
    - Automated follow-up sequences
"""

import os
import re
import time
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LeadManager:
    def __init__(self):
        """Initialize the lead management system."""
        self.api_key = os.getenv('INCREDIBLE_API_KEY')
        self.user_id = os.getenv('USER_ID')
        self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
        self.leads_sheet_id = os.getenv('LEADS_SHEET_ID')
        
        # Configuration
        self.min_lead_score = int(os.getenv('MIN_LEAD_SCORE', '60'))
        self.company_name = os.getenv('COMPANY_NAME', 'Your Company')
        
        if not all([self.api_key, self.user_id, self.leads_sheet_id]):
            raise ValueError("Missing required environment variables. Check .env file.")
        
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        print(f"✅ Lead Manager initialized")
        print(f"📊 Leads Sheet: {self.leads_sheet_id}")
        print(f"🎯 Min Lead Score: {self.min_lead_score}")

    def search_emails(self, query, hours_back=24):
        """Search Gmail for potential leads."""
        print(f"🔍 Searching for leads (last {hours_back}h): {query}")
        
        url = f"{self.base_url}/v1/integrations/gmail/execute"
        data = {
            "user_id": self.user_id,
            "feature_name": "gmail_search",
            "inputs": {
                "query": f"{query} newer_than:{hours_back}h",
                "max_results": 20
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            emails = result.get('result', {}).get('emails', [])
            return emails
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error searching emails: {e}")
            return []

    def extract_lead_data(self, email):
        """Extract and structure lead information from email."""
        # Basic extraction
        sender = email.get('sender', '')
        subject = email.get('subject', '')
        content = email.get('content', '')
        
        # Extract name
        if '<' in sender and '>' in sender:
            name = sender.split('<')[0].strip()
            email_addr = sender.split('<')[1].split('>')[0]
        else:
            name = 'Unknown'
            email_addr = sender
        
        # Extract company from email domain
        if '@' in email_addr:
            domain = email_addr.split('@')[1]
            company = domain.split('.')[0].title() if '.' in domain else 'Unknown'
        else:
            company = 'Unknown'
        
        # Create lead record
        lead = {
            'id': email.get('id', ''),
            'name': name or 'Unknown',
            'email': email_addr,
            'company': company,
            'subject': subject,
            'message': content[:500] if content else '',  # Truncate long messages
            'source': 'Email',
            'date_captured': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'New'
        }
        
        # Calculate lead score
        lead['lead_score'] = self.calculate_lead_score(lead)
        
        # Determine next action
        lead['next_action'] = self.determine_next_action(lead)
        
        return lead

    def calculate_lead_score(self, lead):
        """Calculate lead score based on various factors."""
        score = 0
        content = f"{lead['subject']} {lead['message']}".lower()
        
        # High-value keywords
        high_value_keywords = {
            'enterprise': 30, 'budget': 25, 'purchase': 25, 'buy': 20,
            'demo': 20, 'trial': 15, 'pricing': 15, 'quote': 20,
            'urgent': 15, 'asap': 15, 'meeting': 10, 'call': 10,
            'partnership': 25, 'collaboration': 20, 'integration': 15
        }
        
        for keyword, points in high_value_keywords.items():
            if keyword in content:
                score += points
        
        # Company indicators
        if lead['company'] != 'Unknown':
            score += 15
        
        # Professional email domain
        email_domain = lead['email'].split('@')[1] if '@' in lead['email'] else ''
        if email_domain and not any(common in email_domain for common in ['gmail.com', 'yahoo.com', 'hotmail.com']):
            score += 10
        
        # Message length (longer often = more serious)
        message_length = len(lead['message'])
        if message_length > 200:
            score += 10
        elif message_length > 100:
            score += 5
        
        return min(score, 100)  # Cap at 100

    def determine_next_action(self, lead):
        """Determine appropriate next action based on lead score and content."""
        score = lead['lead_score']
        content = f"{lead['subject']} {lead['message']}".lower()
        
        if score >= 80:
            return "High Priority - Call within 2 hours"
        elif score >= 60:
            if 'demo' in content:
                return "Schedule demo call"
            elif 'pricing' in content:
                return "Send pricing information"
            else:
                return "Send personalized follow-up email"
        elif score >= 40:
            return "Add to nurture campaign"
        else:
            return "Send general information"

    def save_lead_to_sheets(self, lead):
        """Save lead to Google Sheets CRM."""
        print(f"📊 Saving lead: {lead['name']} (Score: {lead['lead_score']})")
        
        url = f"{self.base_url}/v1/integrations/google_sheets/execute"
        
        # Prepare row data
        row_data = [
            lead['date_captured'],
            lead['name'],
            lead['email'],
            lead['company'],
            lead['subject'],
            lead['lead_score'],
            lead['status'],
            lead['next_action'],
            lead['source'],
            lead['id']
        ]
        
        data = {
            "user_id": self.user_id,
            "feature_name": "sheets_append_data",
            "inputs": {
                "spreadsheet_id": self.leads_sheet_id,
                "range": "Leads!A:J",
                "values": [row_data]
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            print(f"✅ Lead saved to CRM")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error saving lead: {e}")
            return False

    def send_follow_up_email(self, lead):
        """Send personalized follow-up email to qualified leads."""
        if lead['lead_score'] < self.min_lead_score:
            print(f"⏸  Skipping follow-up for {lead['name']} (score: {lead['lead_score']} < {self.min_lead_score})")
            return False
        
        print(f"📧 Sending follow-up to: {lead['name']}")
        
        # Generate personalized email
        subject, body = self.generate_follow_up_email(lead)
        
        url = f"{self.base_url}/v1/integrations/gmail/execute"
        data = {
            "user_id": self.user_id,
            "feature_name": "GMAIL_SEND_EMAIL",
            "inputs": {
                "to": lead['email'],
                "subject": subject,
                "body": body
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            print(f"✅ Follow-up sent to {lead['name']}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error sending follow-up: {e}")
            return False

    def generate_follow_up_email(self, lead):
        """Generate personalized follow-up email content."""
        subject = f"Re: {lead['subject']}"
        
        # Personalize based on lead score and content
        if lead['lead_score'] >= 80:
            urgency = "Thank you for your interest"
            priority = "high-priority"
        elif lead['lead_score'] >= 60:
            urgency = "Thanks for reaching out"
            priority = "valued"
        else:
            urgency = "Thank you for contacting us"
            priority = "important"
        
        content = lead['message'].lower()
        
        # Customize offer based on content
        if 'demo' in content:
            solution_offer = "I'd be happy to schedule a personalized demo to show you exactly how we can help."
        elif 'pricing' in content:
            solution_offer = "I'll send you detailed pricing information and can discuss options that fit your budget."
        elif 'integration' in content:
            solution_offer = "I'd love to discuss how our solution integrates with your existing systems."
        else:
            solution_offer = "I'd be happy to discuss how we can help you achieve your goals."
        
        body = f"""Hello {lead['name']},

{urgency} and for reaching out to {self.company_name}.

I reviewed your message about "{lead['subject']}" and understand you're looking for a solution. {solution_offer}

Based on your inquiry, I think you'd be particularly interested in:
• Our proven track record with companies like {lead['company']}
• Solutions that can be implemented quickly and efficiently
• Dedicated support throughout the process

Would you be available for a brief 15-minute call this week to discuss your specific needs? I have availability:
• Today after 2 PM
• Tomorrow morning 9-11 AM  
• Friday afternoon 1-4 PM

Feel free to reply with your preferred time, or you can book directly on my calendar: [calendar-link]

Looking forward to connecting!

Best regards,
[Your Name]
[Your Title]
{self.company_name}
[Phone] | [Email]

---
This is a personal response to your inquiry. We appreciate your interest in {self.company_name}."""
        
        return subject, body

    def scan_for_leads(self, hours_back=24):
        """Main workflow: Scan for new leads and process them."""
        print(f"\n🚀 Starting lead scanning (last {hours_back} hours)")
        
        # Lead detection queries
        lead_queries = [
            'subject:(inquiry OR quote OR pricing OR demo OR interested)',
            'subject:(partnership OR collaboration OR integration)',
            '"looking for" OR "need help" OR "can you help"',
            '"get started" OR "learn more" OR "tell me about"'
        ]
        
        all_potential_leads = []
        
        # Search with each query
        for query in lead_queries:
            emails = self.search_emails(query, hours_back)
            
            for email in emails:
                if self.is_potential_lead(email):
                    all_potential_leads.append(email)
        
        # Remove duplicates
        unique_leads = {email['id']: email for email in all_potential_leads}
        leads = list(unique_leads.values())
        
        print(f"📨 Found {len(leads)} potential leads")
        
        if not leads:
            print("✅ No new leads found")
            return 0
        
        # Process each lead
        processed_count = 0
        high_value_leads = []
        
        for email in leads:
            try:
                # Extract lead data
                lead = self.extract_lead_data(email)
                
                print(f"\n📋 Processing: {lead['name']} from {lead['company']}")
                print(f"   Score: {lead['lead_score']}/100")
                print(f"   Action: {lead['next_action']}")
                
                # Save to CRM
                if self.save_lead_to_sheets(lead):
                    processed_count += 1
                    
                    # Track high-value leads
                    if lead['lead_score'] >= 80:
                        high_value_leads.append(lead)
                    
                    # Send follow-up if qualified
                    if lead['lead_score'] >= self.min_lead_score:
                        self.send_follow_up_email(lead)
                        time.sleep(2)  # Rate limiting
                
            except Exception as e:
                print(f"❌ Error processing lead: {e}")
        
        print(f"\n🎉 Lead processing complete!")
        print(f"📊 Total leads processed: {processed_count}")
        print(f"🔥 High-value leads (80+): {len(high_value_leads)}")
        print(f"📧 Follow-ups sent: {len([l for l in leads if self.extract_lead_data(l)['lead_score'] >= self.min_lead_score])}")
        
        return processed_count

    def is_potential_lead(self, email):
        """Determine if email represents a potential lead."""
        sender = email.get('sender', '').lower()
        subject = email.get('subject', '').lower()
        content = email.get('content', '').lower()
        
        # Skip automated emails
        automated_keywords = ['noreply', 'no-reply', 'automated', 'system', 'notification']
        if any(keyword in sender for keyword in automated_keywords):
            return False
        
        # Look for lead indicators
        lead_indicators = [
            'inquiry', 'interested', 'demo', 'pricing', 'quote',
            'help', 'support', 'question', 'information',
            'partnership', 'collaboration', 'integration'
        ]
        
        full_text = f"{subject} {content}".lower()
        return any(indicator in full_text for indicator in lead_indicators)

def main():
    """Main entry point for the lead management script."""
    print("🎯 Incredible API - Lead Management System")
    print("=" * 50)
    
    try:
        # Initialize the lead manager
        manager = LeadManager()
        
        # Process leads from last 24 hours
        processed = manager.scan_for_leads(hours_back=24)
        
        if processed > 0:
            print(f"\n✅ Successfully processed {processed} leads")
            print("📊 Check your Google Sheet for the updated CRM")
            print("📧 Qualified leads have received follow-up emails")
        else:
            print("\n📭 No new leads found in the specified timeframe")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Set up your .env file with all required variables")
        print("   2. Created a Google Sheet for lead storage")
        print("   3. Completed OAuth setup for Gmail and Google Sheets")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
