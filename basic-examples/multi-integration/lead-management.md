# Lead Management Agent

An intelligent agent that captures leads from multiple sources, enriches contact data, and manages follow-up communications automatically.

## 📋 **Workflow Overview**

```
📧 Gmail → 📊 Google Sheets → 📧 Gmail
  Capture     Enrich        Follow-up
```

**Apps Used:** Gmail + Google Sheets + Gmail (3 integrations total)

## 🎯 **What This Agent Does**

1. **📧 Capture**: Automatically detects and extracts leads from email communications
2. **📊 Enrich**: Stores lead data in structured sheets with enrichment and scoring
3. **📧 Follow-up**: Sends personalized follow-up emails based on lead score and activity

## 🛠 **Prerequisites**

- Incredible API access with function calling enabled
- Connected integrations:
  - Gmail (OAuth) - for both lead capture and follow-up
  - Google Sheets (OAuth) - for lead database management

## 📋 **Setup**

### Environment Configuration

```bash
# .env
INCREDIBLE_API_KEY=your_incredible_api_key
INCREDIBLE_BASE_URL=https://api.incredible.one
USER_ID=your_user_id

# Lead Management Settings
LEADS_SHEET_ID=your_google_sheet_id
SALES_TEAM_EMAIL=sales@company.com
COMPANY_NAME=Your Company Name

# Lead Scoring Parameters
MIN_LEAD_SCORE=60  # Minimum score for automatic follow-up
FOLLOW_UP_DELAY_HOURS=24  # Hours to wait before follow-up
```

## 💻 **Implementation**

<div class="code-tabs" data-section="lead-management">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python">import os
import re
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class LeadManagement:
def **init**(self):
self.api_key = os.getenv('INCREDIBLE_API_KEY')
self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
self.user_id = os.getenv('USER_ID')
self.leads_sheet_id = os.getenv('LEADS_SHEET_ID')
self.sales_team_email = os.getenv('SALES_TEAM_EMAIL')
self.company_name = os.getenv('COMPANY_NAME', 'Your Company')

        self.min_lead_score = int(os.getenv('MIN_LEAD_SCORE', '60'))
        self.follow_up_delay = int(os.getenv('FOLLOW_UP_DELAY_HOURS', '24'))

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def scan_emails_for_leads(self, hours_back=24):
        """Scan recent emails for potential leads"""
        print(f"📧 Scanning emails for leads (last {hours_back} hours)...")

        # Define search queries for lead identification
        lead_queries = [
            "subject:(inquiry OR quote OR pricing OR demo OR interested)",
            "subject:(information OR consultation OR meeting OR partnership)",
            "\"interested in\" OR \"looking for\" OR \"need help with\"",
            "\"can you help\" OR \"get in touch\" OR \"contact us\"",
            "\"pricing\" OR \"quote\" OR \"proposal\" OR \"budget\""
        ]

        potential_leads = []

        for query in lead_queries:
            emails = self.search_gmail(f"{query} newer_than:{hours_back}h")
            for email in emails:
                if self.is_potential_lead(email):
                    potential_leads.append(email)

        # Remove duplicates
        unique_leads = {email['id']: email for email in potential_leads}.values()

        print(f"📨 Found {len(unique_leads)} potential leads")
        return list(unique_leads)

    def search_gmail(self, query):
        """Search Gmail using the Incredible API"""
        url = f"{self.base_url}/v1/integrations/gmail/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "gmail_search",
            "inputs": {
                "query": query,
                "max_results": 50
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get('result', {}).get('emails', [])
            else:
                print(f"❌ Gmail search failed: {response.text}")
                return []
        except Exception as e:
            print(f"❌ Gmail error: {e}")
            return []

    def is_potential_lead(self, email):
        """Determine if email represents a potential lead"""
        # Skip emails from known team domains or automated systems
        sender = email.get('sender', '').lower()
        subject = email.get('subject', '').lower()
        content = email.get('content', '').lower()

        # Skip if from internal team
        if any(domain in sender for domain in ['@gmail.com', '@yahoo.com'] if '@' + self.company_name.lower().replace(' ', '') in sender):
            return False

        # Skip automated emails
        automated_keywords = ['noreply', 'no-reply', 'automated', 'system', 'notification']
        if any(keyword in sender for keyword in automated_keywords):
            return False

        # Look for lead indicators
        lead_indicators = [
            'interested in', 'looking for', 'need help', 'can you help',
            'pricing', 'quote', 'demo', 'consultation', 'meeting',
            'partnership', 'collaboration', 'services', 'solutions'
        ]

        full_text = f"{subject} {content}".lower()
        return any(indicator in full_text for indicator in lead_indicators)

    def extract_lead_data(self, email):
        """Extract and structure lead data from email"""
        print(f"📋 Processing lead: {email.get('subject', 'No Subject')}")

        lead_data = {
            'email_id': email.get('id', ''),
            'name': self.extract_name(email),
            'email': self.extract_email(email),
            'company': self.extract_company(email),
            'subject': email.get('subject', ''),
            'message': email.get('content', '')[:500] + '...' if len(email.get('content', '')) > 500 else email.get('content', ''),
            'source': 'Email',
            'date_received': email.get('date', datetime.now().isoformat()),
            'lead_score': 0,
            'status': 'New',
            'next_action': '',
            'assigned_to': self.sales_team_email
        }

        # Calculate lead score
        lead_data['lead_score'] = self.calculate_lead_score(lead_data)

        # Determine next action
        lead_data['next_action'] = self.determine_next_action(lead_data)

        return lead_data

    def extract_name(self, email):
        """Extract contact name from email"""
        sender = email.get('sender', '')

        # Try to extract name from sender field
        if '<' in sender and '>' in sender:
            name_part = sender.split('<')[0].strip()
            if name_part and not '@' in name_part:
                return name_part

        # Fallback to email prefix
        email_address = self.extract_email(email)
        if email_address:
            return email_address.split('@')[0].replace('.', ' ').replace('_', ' ').title()

        return 'Unknown'

    def extract_email(self, email):
        """Extract email address from sender"""
        sender = email.get('sender', '')

        # Extract email from sender field
        if '<' in sender and '>' in sender:
            return sender.split('<')[1].split('>')[0]
        elif '@' in sender:
            return sender

        return 'unknown@unknown.com'

    def extract_company(self, email):
        """Extract company name from email or signature"""
        content = email.get('content', '')
        sender_email = self.extract_email(email)

        # Try to extract from email domain
        if '@' in sender_email:
            domain = sender_email.split('@')[1]
            if not any(common in domain for common in ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']):
                company = domain.split('.')[0].title()
                return company

        # Try to extract from signature or content
        company_patterns = [
            r'(?:from|at|with)\s+([A-Z][a-zA-Z\s&]+(?:Inc|LLC|Corp|Ltd|Company))',
            r'([A-Z][a-zA-Z\s&]+(?:Inc|LLC|Corp|Ltd|Company))',
            r'(?:working at|employed at)\s+([A-Z][a-zA-Z\s&]+)',
        ]

        for pattern in company_patterns:
            matches = re.findall(pattern, content)
            if matches:
                return matches[0].strip()

        return 'Unknown'

    def calculate_lead_score(self, lead_data):
        """Calculate lead score based on various factors"""
        score = 0

        content = f"{lead_data['subject']} {lead_data['message']}".lower()

        # High-value keywords
        high_value_keywords = {
            'enterprise': 20, 'corporate': 15, 'budget': 15,
            'urgent': 10, 'asap': 10, 'immediate': 10,
            'demo': 15, 'presentation': 10, 'meeting': 10,
            'pricing': 15, 'quote': 15, 'proposal': 20,
            'partnership': 25, 'collaboration': 20
        }

        for keyword, points in high_value_keywords.items():
            if keyword in content:
                score += points

        # Company indicators
        if lead_data['company'] != 'Unknown':
            score += 15

        # Professional email domain
        email_domain = lead_data['email'].split('@')[1] if '@' in lead_data['email'] else ''
        if email_domain and not any(common in email_domain for common in ['gmail.com', 'yahoo.com', 'hotmail.com']):
            score += 10

        # Message length (longer messages often indicate more serious inquiries)
        message_length = len(lead_data['message'])
        if message_length > 200:
            score += 10
        elif message_length > 100:
            score += 5

        # Cap score at 100
        return min(score, 100)

    def determine_next_action(self, lead_data):
        """Determine appropriate next action based on lead score and content"""
        score = lead_data['lead_score']
        content = f"{lead_data['subject']} {lead_data['message']}".lower()

        if score >= 80:
            return "High Priority - Call within 2 hours"
        elif score >= 60:
            return "Send personalized follow-up email"
        elif 'demo' in content or 'meeting' in content:
            return "Schedule demo or meeting"
        elif 'pricing' in content or 'quote' in content:
            return "Send pricing information"
        else:
            return "Send general information"

    def save_lead_to_sheets(self, lead_data):
        """Save lead data to Google Sheets"""
        print(f"📊 Saving lead to sheets: {lead_data['name']}")

        # Prepare row data
        row_data = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            lead_data['name'],
            lead_data['email'],
            lead_data['company'],
            lead_data['subject'],
            lead_data['message'],
            lead_data['source'],
            lead_data['date_received'],
            lead_data['lead_score'],
            lead_data['status'],
            lead_data['next_action'],
            lead_data['assigned_to'],
            lead_data['email_id']
        ]

        url = f"{self.base_url}/v1/integrations/google_sheets/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "sheets_append_data",
            "inputs": {
                "spreadsheet_id": self.leads_sheet_id,
                "range": "Leads!A:M",
                "values": [row_data]
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                print(f"✅ Lead saved: {lead_data['name']} (Score: {lead_data['lead_score']})")
                return True
            else:
                print(f"❌ Failed to save lead: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Sheets error: {e}")
            return False

    def generate_follow_up_email(self, lead_data):
        """Generate personalized follow-up email"""
        subject = f"Re: {lead_data['subject']}"

        # Personalize based on lead score and content
        if lead_data['lead_score'] >= 80:
            urgency = "I wanted to reach out personally"
            priority = "high-priority"
        elif lead_data['lead_score'] >= 60:
            urgency = "Thank you for your interest"
            priority = "important"
        else:
            urgency = "Thanks for reaching out"
            priority = "valued"

        content = lead_data['message'].lower()

        if 'demo' in content:
            solution_offer = "I'd be happy to schedule a personalized demo to show you exactly how we can help."
        elif 'pricing' in content or 'quote' in content:
            solution_offer = "I'll prepare a customized quote that fits your specific requirements."
        elif 'meeting' in content:
            solution_offer = "I'd love to schedule a meeting to discuss your needs in detail."
        else:
            solution_offer = "I'd be happy to discuss how we can help you achieve your goals."

        body = f"""Hello {lead_data['name']},

{urgency} in {self.company_name} and wanted to personally follow up on your inquiry.

I reviewed your message about "{lead_data['subject']}" and understand you're looking for solutions that can help with your needs.

{solution_offer}

Here's what I'd like to offer:

• A free consultation to understand your specific requirements
• Customized recommendations based on your industry and use case
• Access to our team of experts who can provide detailed guidance

Would you be available for a brief 15-minute call this week? I'm confident we can provide valuable insights for your {priority} project.

You can reply to this email or feel free to call me directly. I'm here to help!

Best regards,
{self.company_name} Sales Team
{self.sales_team_email}

P.S. Based on your inquiry, I think you'd be particularly interested in [specific feature/benefit]. I'd love to show you how it works in action.

---

This is a personal response to your inquiry. We appreciate your interest in {self.company_name}."""

        return subject, body

    def send_follow_up_email(self, lead_data):
        """Send follow-up email to lead"""
        if lead_data['lead_score'] < self.min_lead_score:
            print(f"⏸ Skipping follow-up for {lead_data['name']} (score: {lead_data['lead_score']} < {self.min_lead_score})")
            return False

        print(f"📧 Sending follow-up to: {lead_data['name']}")

        subject, body = self.generate_follow_up_email(lead_data)

        url = f"{self.base_url}/v1/integrations/gmail/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "GMAIL_SEND_EMAIL",
            "inputs": {
                "to": lead_data['email'],
                "subject": subject,
                "body": body,
                "cc": self.sales_team_email
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                print(f"✅ Follow-up sent to {lead_data['name']}")
                return True
            else:
                print(f"❌ Failed to send follow-up: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Email error: {e}")
            return False

    def notify_sales_team(self, high_value_leads):
        """Notify sales team about high-value leads"""
        if not high_value_leads:
            return

        print(f"🚨 Notifying sales team about {len(high_value_leads)} high-value leads")

        subject = f"🔥 High-Value Leads Alert - {datetime.now().strftime('%B %d, %Y')}"

        body = f"""🚨 **High-Value Leads Alert** 🚨

{len(high_value_leads)} high-priority leads have been captured and require immediate attention:

"""

        for i, lead in enumerate(high_value_leads, 1):
            body += f"""

**Lead #{i}: {lead['name']}**
• Company: {lead['company']}
• Email: {lead['email']}
• Score: {lead['lead_score']}/100
• Subject: {lead['subject']}
• Next Action: {lead['next_action']}
• Preview: {lead['message'][:100]}...

---

"""

        body += f"""

📊 **View Full Lead Dashboard**: [Google Sheets](https://docs.google.com/spreadsheets/d/{self.leads_sheet_id})

🎯 **Immediate Actions Required:**
• Review all leads with scores above 80
• Contact high-priority leads within 2 hours
• Follow up on demo/meeting requests

This alert was generated by the Incredible Lead Management Agent.
"""

        url = f"{self.base_url}/v1/integrations/gmail/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "GMAIL_SEND_EMAIL",
            "inputs": {
                "to": self.sales_team_email,
                "subject": subject,
                "body": body
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                print("✅ Sales team notified")
                return True
            else:
                print(f"❌ Failed to notify sales team: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Notification error: {e}")
            return False

    def run_lead_workflow(self, hours_back=24):
        """Execute complete lead management workflow"""
        print("🚀 Starting Lead Management Workflow")
        print(f"📊 Leads Sheet: {self.leads_sheet_id}")
        print(f"📧 Sales Team: {self.sales_team_email}")
        print(f"🎯 Min Score for Follow-up: {self.min_lead_score}")
        print()

        # Step 1: Scan for leads
        potential_leads = self.scan_emails_for_leads(hours_back)

        if not potential_leads:
            print("✅ No new leads found")
            return

        # Step 2: Process each lead
        processed_leads = []
        high_value_leads = []

        for email in potential_leads:
            lead_data = self.extract_lead_data(email)

            # Save to sheets
            if self.save_lead_to_sheets(lead_data):
                processed_leads.append(lead_data)

                # Track high-value leads
                if lead_data['lead_score'] >= 80:
                    high_value_leads.append(lead_data)

                # Send follow-up if score is high enough
                self.send_follow_up_email(lead_data)

        # Step 3: Notify sales team about high-value leads
        if high_value_leads:
            self.notify_sales_team(high_value_leads)

        # Step 4: Summary
        follow_ups_sent = len([l for l in processed_leads if l['lead_score'] >= self.min_lead_score])

        print(f"\n🎉 Lead Management Workflow Complete!")
        print(f"📧 Emails scanned: {len(potential_leads)}")
        print(f"📊 Leads processed: {len(processed_leads)}")
        print(f"🔥 High-value leads: {len(high_value_leads)}")
        print(f"📧 Follow-ups sent: {follow_ups_sent}")
        print(f"📊 View dashboard: https://docs.google.com/spreadsheets/d/{self.leads_sheet_id}")

# Usage Examples

if **name** == "**main**":
lead_manager = LeadManagement()

    # Run daily lead processing
    lead_manager.run_lead_workflow(hours_back=24)

    print("\n" + "="*50 + "\n")

    # Run weekly catch-up
    lead_manager.run_lead_workflow(hours_back=168)  # 7 days</code></pre>

  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">const axios = require("axios");
require("dotenv").config();

class LeadManagement {
constructor() {
this.apiKey = process.env.INCREDIBLE_API_KEY;
this.baseUrl = process.env.INCREDIBLE_BASE_URL || "https://api.incredible.one";
this.userId = process.env.USER_ID;
this.leadsSheetId = process.env.LEADS_SHEET_ID;
this.salesTeamEmail = process.env.SALES_TEAM_EMAIL;
this.companyName = process.env.COMPANY_NAME || 'Your Company';

    this.minLeadScore = parseInt(process.env.MIN_LEAD_SCORE || '60');
    this.followUpDelay = parseInt(process.env.FOLLOW_UP_DELAY_HOURS || '24');

    this.headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${this.apiKey}`,
    };

}

async scanEmailsForLeads(hoursBack = 24) {
console.log(`📧 Scanning emails for leads (last ${hoursBack} hours)...`);

    const leadQueries = [
      "subject:(inquiry OR quote OR pricing OR demo OR interested)",
      "subject:(information OR consultation OR meeting OR partnership)",
      '"interested in" OR "looking for" OR "need help with"',
      '"can you help" OR "get in touch" OR "contact us"',
      '"pricing" OR "quote" OR "proposal" OR "budget"'
    ];

    const potentialLeads = [];

    for (const query of leadQueries) {
      const emails = await this.searchGmail(`${query} newer_than:${hoursBack}h`);
      for (const email of emails) {
        if (this.isPotentialLead(email)) {
          potentialLeads.push(email);
        }
      }
    }

    // Remove duplicates
    const uniqueLeads = Array.from(
      new Map(potentialLeads.map(email => [email.id, email])).values()
    );

    console.log(`📨 Found ${uniqueLeads.length} potential leads`);
    return uniqueLeads;

}

async searchGmail(query) {
const url = `${this.baseUrl}/v1/integrations/gmail/execute`;

    const data = {
      user_id: this.userId,
      feature_name: "gmail_search",
      inputs: {
        query: query,
        max_results: 50
      }
    };

    try {
      const response = await axios.post(url, data, { headers: this.headers });
      if (response.status === 200) {
        return response.data.result?.emails || [];
      } else {
        console.log(`❌ Gmail search failed: ${response.data}`);
        return [];
      }
    } catch (error) {
      console.log(`❌ Gmail error: ${error.message}`);
      return [];
    }

}

isPotentialLead(email) {
const sender = (email.sender || '').toLowerCase();
const subject = (email.subject || '').toLowerCase();
const content = (email.content || '').toLowerCase();

    // Skip if from internal team
    const companyDomain = this.companyName.toLowerCase().replace(/\s+/g, '');
    if (sender.includes(`@${companyDomain}`)) {
      return false;
    }

    // Skip automated emails
    const automatedKeywords = ['noreply', 'no-reply', 'automated', 'system', 'notification'];
    if (automatedKeywords.some(keyword => sender.includes(keyword))) {
      return false;
    }

    // Look for lead indicators
    const leadIndicators = [
      'interested in', 'looking for', 'need help', 'can you help',
      'pricing', 'quote', 'demo', 'consultation', 'meeting',
      'partnership', 'collaboration', 'services', 'solutions'
    ];

    const fullText = `${subject} ${content}`.toLowerCase();
    return leadIndicators.some(indicator => fullText.includes(indicator));

}

extractLeadData(email) {
console.log(`📋 Processing lead: ${email.subject || 'No Subject'}`);

    const leadData = {
      email_id: email.id || '',
      name: this.extractName(email),
      email: this.extractEmail(email),
      company: this.extractCompany(email),
      subject: email.subject || '',
      message: (email.content || '').length > 500 ?
        (email.content || '').substring(0, 500) + '...' :
        (email.content || ''),
      source: 'Email',
      date_received: email.date || new Date().toISOString(),
      lead_score: 0,
      status: 'New',
      next_action: '',
      assigned_to: this.salesTeamEmail
    };

    // Calculate lead score
    leadData.lead_score = this.calculateLeadScore(leadData);

    // Determine next action
    leadData.next_action = this.determineNextAction(leadData);

    return leadData;

}

extractName(email) {
const sender = email.sender || '';

    // Try to extract name from sender field
    if (sender.includes('<') && sender.includes('>')) {
      const namePart = sender.split('<')[0].trim();
      if (namePart && !namePart.includes('@')) {
        return namePart;
      }
    }

    // Fallback to email prefix
    const emailAddress = this.extractEmail(email);
    if (emailAddress) {
      return emailAddress.split('@')[0]
        .replace(/\./g, ' ')
        .replace(/_/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase());
    }

    return 'Unknown';

}

extractEmail(email) {
const sender = email.sender || '';

    // Extract email from sender field
    if (sender.includes('<') && sender.includes('>')) {
      return sender.split('<')[1].split('>')[0];
    } else if (sender.includes('@')) {
      return sender;
    }

    return 'unknown@unknown.com';

}

extractCompany(email) {
const content = email.content || '';
const senderEmail = this.extractEmail(email);

    // Try to extract from email domain
    if (senderEmail.includes('@')) {
      const domain = senderEmail.split('@')[1];
      const commonDomains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com'];
      if (!commonDomains.some(common => domain.includes(common))) {
        const company = domain.split('.')[0];
        return company.charAt(0).toUpperCase() + company.slice(1);
      }
    }

    // Try to extract from signature or content
    const companyPatterns = [
      /(?:from|at|with)\s+([A-Z][a-zA-Z\s&]+(?:Inc|LLC|Corp|Ltd|Company))/g,
      /([A-Z][a-zA-Z\s&]+(?:Inc|LLC|Corp|Ltd|Company))/g,
      /(?:working at|employed at)\s+([A-Z][a-zA-Z\s&]+)/g,
    ];

    for (const pattern of companyPatterns) {
      const matches = Array.from(content.matchAll(pattern));
      if (matches.length > 0) {
        return matches[0][1].trim();
      }
    }

    return 'Unknown';

}

calculateLeadScore(leadData) {
let score = 0;

    const content = `${leadData.subject} ${leadData.message}`.toLowerCase();

    // High-value keywords
    const highValueKeywords = {
      'enterprise': 20, 'corporate': 15, 'budget': 15,
      'urgent': 10, 'asap': 10, 'immediate': 10,
      'demo': 15, 'presentation': 10, 'meeting': 10,
      'pricing': 15, 'quote': 15, 'proposal': 20,
      'partnership': 25, 'collaboration': 20
    };

    for (const [keyword, points] of Object.entries(highValueKeywords)) {
      if (content.includes(keyword)) {
        score += points;
      }
    }

    // Company indicators
    if (leadData.company !== 'Unknown') {
      score += 15;
    }

    // Professional email domain
    const emailDomain = leadData.email.includes('@') ? leadData.email.split('@')[1] : '';
    const commonDomains = ['gmail.com', 'yahoo.com', 'hotmail.com'];
    if (emailDomain && !commonDomains.some(common => emailDomain.includes(common))) {
      score += 10;
    }

    // Message length
    const messageLength = leadData.message.length;
    if (messageLength > 200) {
      score += 10;
    } else if (messageLength > 100) {
      score += 5;
    }

    // Cap score at 100
    return Math.min(score, 100);

}

determineNextAction(leadData) {
const score = leadData.lead_score;
const content = `${leadData.subject} ${leadData.message}`.toLowerCase();

    if (score >= 80) {
      return "High Priority - Call within 2 hours";
    } else if (score >= 60) {
      return "Send personalized follow-up email";
    } else if (content.includes('demo') || content.includes('meeting')) {
      return "Schedule demo or meeting";
    } else if (content.includes('pricing') || content.includes('quote')) {
      return "Send pricing information";
    } else {
      return "Send general information";
    }

}

async saveLeadToSheets(leadData) {
console.log(`📊 Saving lead to sheets: ${leadData.name}`);

    const rowData = [
      new Date().toLocaleString(),
      leadData.name,
      leadData.email,
      leadData.company,
      leadData.subject,
      leadData.message,
      leadData.source,
      leadData.date_received,
      leadData.lead_score,
      leadData.status,
      leadData.next_action,
      leadData.assigned_to,
      leadData.email_id
    ];

    const url = `${this.baseUrl}/v1/integrations/google_sheets/execute`;

    const data = {
      user_id: this.userId,
      feature_name: "sheets_append_data",
      inputs: {
        spreadsheet_id: this.leadsSheetId,
        range: "Leads!A:M",
        values: [rowData]
      }
    };

    try {
      const response = await axios.post(url, data, { headers: this.headers });
      if (response.status === 200) {
        console.log(`✅ Lead saved: ${leadData.name} (Score: ${leadData.lead_score})`);
        return true;
      } else {
        console.log(`❌ Failed to save lead: ${response.data}`);
        return false;
      }
    } catch (error) {
      console.log(`❌ Sheets error: ${error.message}`);
      return false;
    }

}

generateFollowUpEmail(leadData) {
const subject = `Re: ${leadData.subject}`;

    // Personalize based on lead score and content
    let urgency, priority;
    if (leadData.lead_score >= 80) {
      urgency = "I wanted to reach out personally";
      priority = "high-priority";
    } else if (leadData.lead_score >= 60) {
      urgency = "Thank you for your interest";
      priority = "important";
    } else {
      urgency = "Thanks for reaching out";
      priority = "valued";
    }

    const content = leadData.message.toLowerCase();

    let solutionOffer;
    if (content.includes('demo')) {
      solutionOffer = "I'd be happy to schedule a personalized demo to show you exactly how we can help.";
    } else if (content.includes('pricing') || content.includes('quote')) {
      solutionOffer = "I'll prepare a customized quote that fits your specific requirements.";
    } else if (content.includes('meeting')) {
      solutionOffer = "I'd love to schedule a meeting to discuss your needs in detail.";
    } else {
      solutionOffer = "I'd be happy to discuss how we can help you achieve your goals.";
    }

    const body = `Hello ${leadData.name},

${urgency} in ${this.companyName} and wanted to personally follow up on your inquiry.

I reviewed your message about "${leadData.subject}" and understand you're looking for solutions that can help with your needs.

${solutionOffer}

Here's what I'd like to offer:

• A free consultation to understand your specific requirements
• Customized recommendations based on your industry and use case
• Access to our team of experts who can provide detailed guidance

Would you be available for a brief 15-minute call this week? I'm confident we can provide valuable insights for your ${priority} project.

You can reply to this email or feel free to call me directly. I'm here to help!

Best regards,
${this.companyName} Sales Team
${this.salesTeamEmail}

P.S. Based on your inquiry, I think you'd be particularly interested in [specific feature/benefit]. I'd love to show you how it works in action.

---

This is a personal response to your inquiry. We appreciate your interest in ${this.companyName}.`;

    return { subject, body };

}

async sendFollowUpEmail(leadData) {
if (leadData.lead_score < this.minLeadScore) {
console.log(`⏸ Skipping follow-up for ${leadData.name} (score: ${leadData.lead_score} < ${this.minLeadScore})`);
return false;
}

    console.log(`📧 Sending follow-up to: ${leadData.name}`);

    const { subject, body } = this.generateFollowUpEmail(leadData);

    const url = `${this.baseUrl}/v1/integrations/gmail/execute`;

    const data = {
      user_id: this.userId,
      feature_name: "GMAIL_SEND_EMAIL",
      inputs: {
        to: leadData.email,
        subject: subject,
        body: body,
        cc: this.salesTeamEmail
      }
    };

    try {
      const response = await axios.post(url, data, { headers: this.headers });
      if (response.status === 200) {
        console.log(`✅ Follow-up sent to ${leadData.name}`);
        return true;
      } else {
        console.log(`❌ Failed to send follow-up: ${response.data}`);
        return false;
      }
    } catch (error) {
      console.log(`❌ Email error: ${error.message}`);
      return false;
    }

}

async notifySalesTeam(highValueLeads) {
if (highValueLeads.length === 0) {
return;
}

    console.log(`🚨 Notifying sales team about ${highValueLeads.length} high-value leads`);

    const subject = `🔥 High-Value Leads Alert - ${new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })}`;

    let body = `🚨 **High-Value Leads Alert** 🚨

${highValueLeads.length} high-priority leads have been captured and require immediate attention:

`;

    highValueLeads.forEach((lead, index) => {
      body += `

**Lead #${index + 1}: ${lead.name}**
• Company: ${lead.company}
• Email: ${lead.email}
• Score: ${lead.lead_score}/100
• Subject: ${lead.subject}
• Next Action: ${lead.next_action}
• Preview: ${lead.message.substring(0, 100)}...

---

`;
});

    body += `

📊 **View Full Lead Dashboard**: [Google Sheets](https://docs.google.com/spreadsheets/d/${this.leadsSheetId})

🎯 **Immediate Actions Required:**
• Review all leads with scores above 80
• Contact high-priority leads within 2 hours
• Follow up on demo/meeting requests

This alert was generated by the Incredible Lead Management Agent.
`;

    const url = `${this.baseUrl}/v1/integrations/gmail/execute`;

    const data = {
      user_id: this.userId,
      feature_name: "GMAIL_SEND_EMAIL",
      inputs: {
        to: this.salesTeamEmail,
        subject: subject,
        body: body
      }
    };

    try {
      const response = await axios.post(url, data, { headers: this.headers });
      if (response.status === 200) {
        console.log("✅ Sales team notified");
        return true;
      } else {
        console.log(`❌ Failed to notify sales team: ${response.data}`);
        return false;
      }
    } catch (error) {
      console.log(`❌ Notification error: ${error.message}`);
      return false;
    }

}

async runLeadWorkflow(hoursBack = 24) {
console.log("🚀 Starting Lead Management Workflow");
console.log(`📊 Leads Sheet: ${this.leadsSheetId}`);
console.log(`📧 Sales Team: ${this.salesTeamEmail}`);
console.log(`🎯 Min Score for Follow-up: ${this.minLeadScore}`);
console.log();

    // Step 1: Scan for leads
    const potentialLeads = await this.scanEmailsForLeads(hoursBack);

    if (potentialLeads.length === 0) {
      console.log("✅ No new leads found");
      return;
    }

    // Step 2: Process each lead
    const processedLeads = [];
    const highValueLeads = [];

    for (const email of potentialLeads) {
      const leadData = this.extractLeadData(email);

      // Save to sheets
      if (await this.saveLeadToSheets(leadData)) {
        processedLeads.push(leadData);

        // Track high-value leads
        if (leadData.lead_score >= 80) {
          highValueLeads.push(leadData);
        }

        // Send follow-up if score is high enough
        await this.sendFollowUpEmail(leadData);
      }
    }

    // Step 3: Notify sales team about high-value leads
    if (highValueLeads.length > 0) {
      await this.notifySalesTeam(highValueLeads);
    }

    // Step 4: Summary
    const followUpsSent = processedLeads.filter(l => l.lead_score >= this.minLeadScore).length;

    console.log(`\n🎉 Lead Management Workflow Complete!`);
    console.log(`📧 Emails scanned: ${potentialLeads.length}`);
    console.log(`📊 Leads processed: ${processedLeads.length}`);
    console.log(`🔥 High-value leads: ${highValueLeads.length}`);
    console.log(`📧 Follow-ups sent: ${followUpsSent}`);
    console.log(`📊 View dashboard: https://docs.google.com/spreadsheets/d/${this.leadsSheetId}`);

}
}

// Usage Examples
async function main() {
const leadManager = new LeadManagement();

// Run daily lead processing
await leadManager.runLeadWorkflow(24);

console.log("\n" + "=".repeat(50) + "\n");

// Run weekly catch-up
await leadManager.runLeadWorkflow(168); // 7 days
}

if (require.main === module) {
main().catch(console.error);
}

module.exports = LeadManagement;</code></pre>

  </div>
</div>

## 🎯 **Usage Examples**

### Daily Lead Processing

```bash
# Process leads from last 24 hours
python lead_management.py --hours 24
```

### Weekly Lead Review

```bash
# Catch up on the week's leads
node leadManagement.js --hours 168
```

### High-Priority Lead Focus

```bash
# Only process high-scoring leads
python lead_management.py --min-score 80 --immediate-follow-up
```

## 📊 **Expected Output**

```
🚀 Starting Lead Management Workflow
📊 Leads Sheet: 1BcD3FgHiJkLmNoPqRsTuVwXyZ
📧 Sales Team: sales@company.com
🎯 Min Score for Follow-up: 60

📧 Scanning emails for leads (last 24 hours)...
📨 Found 5 potential leads

📋 Processing lead: Interested in your services
📊 Saving lead to sheets: John Smith
✅ Lead saved: John Smith (Score: 75)
📧 Sending follow-up to: John Smith
✅ Follow-up sent to John Smith

📋 Processing lead: Quote request for enterprise solution
📊 Saving lead to sheets: Sarah Johnson
✅ Lead saved: Sarah Johnson (Score: 85)
📧 Sending follow-up to: Sarah Johnson
✅ Follow-up sent to Sarah Johnson

🚨 Notifying sales team about 1 high-value leads
✅ Sales team notified

🎉 Lead Management Workflow Complete!
📧 Emails scanned: 5
📊 Leads processed: 5
🔥 High-value leads: 1
📧 Follow-ups sent: 4
📊 View dashboard: https://docs.google.com/spreadsheets/d/1BcD3FgHiJkLmNoPqRsTuVwXyZ
```

---

_This lead management agent transforms email inquiries into organized sales opportunities with automated scoring, follow-up, and team notifications._
