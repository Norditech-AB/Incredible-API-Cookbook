#!/usr/bin/env python3
"""
Email Automation with Incredible API
=====================================

This example demonstrates how to:
1. Monitor Gmail for specific emails
2. Automatically respond to inquiries
3. Log interactions to Google Sheets

Usage:
    python main.py

Requirements:
    - Incredible API key
    - Gmail OAuth setup
    - Google Sheets OAuth setup
"""

import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmailAutomation:
    def __init__(self):
        """Initialize the email automation system."""
        self.api_key = os.getenv('INCREDIBLE_API_KEY')
        self.user_id = os.getenv('USER_ID') 
        self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
        self.sheet_id = os.getenv('EMAIL_LOG_SHEET_ID')
        
        # Validation
        if not all([self.api_key, self.user_id, self.sheet_id]):
            raise ValueError("Missing required environment variables. Check .env file.")
        
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        print(f"✅ Email Automation initialized for user: {self.user_id}")

    def search_emails(self, query, max_results=10):
        """
        Search Gmail using Incredible API.
        
        Args:
            query (str): Gmail search query (e.g., "is:unread subject:support")
            max_results (int): Maximum number of emails to return
            
        Returns:
            list: List of matching emails
        """
        print(f"🔍 Searching emails: {query}")
        
        url = f"{self.base_url}/v1/integrations/gmail/execute"
        data = {
            "user_id": self.user_id,
            "feature_name": "gmail_search",
            "inputs": {
                "query": query,
                "max_results": max_results
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            emails = result.get('result', {}).get('emails', [])
            print(f"📧 Found {len(emails)} emails")
            return emails
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error searching emails: {e}")
            return []

    def send_email(self, to, subject, body):
        """
        Send email via Gmail.
        
        Args:
            to (str): Recipient email address
            subject (str): Email subject
            body (str): Email body content
            
        Returns:
            bool: True if sent successfully
        """
        print(f"📤 Sending email to: {to}")
        
        url = f"{self.base_url}/v1/integrations/gmail/execute"
        data = {
            "user_id": self.user_id,
            "feature_name": "GMAIL_SEND_EMAIL",
            "inputs": {
                "to": to,
                "subject": subject,
                "body": body
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get('success'):
                print(f"✅ Email sent successfully")
                return True
            else:
                print(f"❌ Failed to send email: {result}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error sending email: {e}")
            return False

    def log_to_sheets(self, email_data, action_taken):
        """
        Log email interaction to Google Sheets.
        
        Args:
            email_data (dict): Email information
            action_taken (str): Action that was performed
        """
        print(f"📊 Logging interaction to sheets")
        
        url = f"{self.base_url}/v1/integrations/google_sheets/execute"
        
        # Prepare log entry
        log_entry = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            email_data.get('sender', 'Unknown'),
            email_data.get('subject', 'No Subject'),
            action_taken,
            email_data.get('id', '')
        ]
        
        data = {
            "user_id": self.user_id,
            "feature_name": "sheets_append_data",
            "inputs": {
                "spreadsheet_id": self.sheet_id,
                "range": "EmailLog!A:E",
                "values": [log_entry]
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            print(f"✅ Interaction logged to sheets")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error logging to sheets: {e}")

    def generate_auto_response(self, original_email):
        """
        Generate appropriate auto-response based on email content.
        
        Args:
            original_email (dict): The original email data
            
        Returns:
            tuple: (subject, body) for the response
        """
        sender_name = original_email.get('sender', '').split('<')[0].strip()
        if not sender_name:
            sender_name = "there"
        
        original_subject = original_email.get('subject', '')
        content = original_email.get('content', '').lower()
        
        # Determine response type based on content
        if any(word in content for word in ['support', 'help', 'issue', 'problem']):
            subject = f"Re: {original_subject}"
            body = f"""Hi {sender_name},

Thank you for contacting our support team. We've received your inquiry and will respond within 24 hours.

For urgent issues, please call our support hotline at (555) 123-4567.

Best regards,
Support Team

---
This is an automated response. Your message is important to us and will be reviewed by our team."""

        elif any(word in content for word in ['demo', 'trial', 'pricing', 'sales']):
            subject = f"Re: {original_subject}"
            body = f"""Hi {sender_name},

Thank you for your interest in our product! We'd love to show you how we can help your business.

I'll connect you with our sales team who will reach out within 2 business hours to schedule a personalized demo.

In the meantime, feel free to explore our resources:
• Product Overview: https://company.com/product
• Case Studies: https://company.com/cases
• Pricing: https://company.com/pricing

Best regards,
Sales Team

---
This is an automated response. A member of our sales team will follow up personally."""

        else:
            subject = f"Re: {original_subject}"
            body = f"""Hi {sender_name},

Thank you for your email. We've received your message and will review it carefully.

We typically respond to inquiries within 1-2 business days. If your matter is urgent, please call us at (555) 123-4567.

Best regards,
Team

---
This is an automated acknowledgment. We'll follow up with a personal response soon."""

        return subject, body

    def process_support_emails(self):
        """
        Main workflow: Process support emails with auto-responses.
        """
        print("\n🚀 Starting email automation workflow...")
        
        # Search for unread emails that might need responses
        queries = [
            "is:unread (subject:support OR subject:help)",
            "is:unread (subject:demo OR subject:pricing OR subject:sales)",
            "is:unread to:support@company.com",
            "is:unread (inquiry OR question OR interested)"
        ]
        
        processed_count = 0
        
        for query in queries:
            emails = self.search_emails(query, max_results=5)
            
            for email in emails:
                try:
                    print(f"\n📧 Processing: {email.get('subject', 'No Subject')}")
                    
                    # Generate and send auto-response
                    subject, body = self.generate_auto_response(email)
                    sender = email.get('sender', '')
                    
                    # Extract sender email
                    if '<' in sender and '>' in sender:
                        sender_email = sender.split('<')[1].split('>')[0]
                    else:
                        sender_email = sender
                    
                    if sender_email and '@' in sender_email:
                        # Send auto-response
                        if self.send_email(sender_email, subject, body):
                            action = "Auto-response sent"
                        else:
                            action = "Failed to send auto-response"
                    else:
                        action = "Invalid sender email"
                    
                    # Log the interaction
                    self.log_to_sheets(email, action)
                    processed_count += 1
                    
                    # Be nice to the API
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"❌ Error processing email: {e}")
                    self.log_to_sheets(email, f"Error: {str(e)}")
        
        print(f"\n🎉 Email automation complete! Processed {processed_count} emails.")
        return processed_count

def main():
    """Main entry point for the email automation script."""
    print("🤖 Incredible API - Email Automation Example")
    print("=" * 50)
    
    try:
        # Initialize the automation system
        automation = EmailAutomation()
        
        # Run the email processing workflow
        processed = automation.process_support_emails()
        
        print(f"\n✅ Successfully processed {processed} emails")
        print("📊 Check your Google Sheet for logged interactions")
        print("📧 Auto-responses have been sent to inquiries")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Set up your .env file with all required variables")
        print("   2. Completed OAuth setup for Gmail and Google Sheets")
        print("   3. Valid Incredible API credentials")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
