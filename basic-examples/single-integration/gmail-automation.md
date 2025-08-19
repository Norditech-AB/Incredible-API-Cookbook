# Gmail Automation Examples

Learn how to automate Gmail tasks using the Incredible API with simple, practical examples.

## Prerequisites

- Incredible API account and credentials
- Gmail integration connected (OAuth)
- Basic understanding of function calling

## Example 1: Email Alert System

Monitor your inbox and get notifications for important emails.

### Python Implementation

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GmailAlertSystem:
    def __init__(self):
        self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
        self.user_id = os.getenv('USER_ID')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {os.getenv('INCREDIBLE_API_KEY')}"
        }

    def search_emails(self, query, max_results=10):
        """Search for emails matching criteria"""
        url = f"{self.base_url}/v1/integrations/gmail/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "GMAIL_SEARCH_EMAILS",
            "inputs": {
                "query": query,
                "max_results": max_results
            }
        }

        response = requests.post(url, headers=self.headers, json=data)

        if response.status_code == 200:
            return response.json().get("result", {}).get("emails", [])
        else:
            print(f"Error searching emails: {response.text}")
            return []

    def check_urgent_emails(self):
        """Check for urgent emails and send alerts"""
        print("🔍 Checking for urgent emails...")

        # Search for urgent keywords
        urgent_queries = [
            "subject:URGENT",
            "subject:ASAP",
            "subject:Emergency",
            "is:important is:unread"
        ]

        all_urgent_emails = []

        for query in urgent_queries:
            emails = self.search_emails(query, max_results=5)
            all_urgent_emails.extend(emails)

        # Remove duplicates
        unique_emails = {email['id']: email for email in all_urgent_emails}.values()

        if unique_emails:
            print(f"⚠️  Found {len(unique_emails)} urgent emails!")
            for email in unique_emails:
                self.process_urgent_email(email)
        else:
            print("✅ No urgent emails found")

    def process_urgent_email(self, email):
        """Process an urgent email"""
        print(f"📧 URGENT: {email.get('subject', 'No Subject')}")
        print(f"   From: {email.get('sender', 'Unknown')}")
        print(f"   Received: {email.get('date', 'Unknown')}")
        print(f"   Preview: {email.get('snippet', 'No preview')[:100]}...")
        print()

        # Here you could:
        # - Send a push notification
        # - Forward to your phone
        # - Add to a priority list
        # - Create a task

    def daily_summary(self):
        """Generate a daily email summary"""
        print("📊 Generating daily email summary...")

        today_emails = self.search_emails("newer_than:1d", max_results=50)

        if not today_emails:
            print("No emails found for today")
            return

        # Categorize emails
        categories = {
            "urgent": [],
            "meetings": [],
            "newsletters": [],
            "work": [],
            "personal": []
        }

        for email in today_emails:
            subject = email.get('subject', '').lower()
            sender = email.get('sender', '').lower()

            if any(word in subject for word in ['urgent', 'asap', 'emergency']):
                categories["urgent"].append(email)
            elif any(word in subject for word in ['meeting', 'call', 'conference']):
                categories["meetings"].append(email)
            elif any(word in sender for word in ['newsletter', 'noreply', 'marketing']):
                categories["newsletters"].append(email)
            elif any(word in sender for word in ['work', 'company', 'team']):
                categories["work"].append(email)
            else:
                categories["personal"].append(email)

        # Print summary
        print(f"📧 Daily Email Summary ({len(today_emails)} total emails)")
        print("=" * 50)

        for category, emails in categories.items():
            if emails:
                print(f"{category.upper()}: {len(emails)} emails")
                for email in emails[:3]:  # Show first 3
                    print(f"  • {email.get('subject', 'No Subject')}")
                if len(emails) > 3:
                    print(f"  ... and {len(emails) - 3} more")
                print()

# Usage Examples
if __name__ == "__main__":
    alert_system = GmailAlertSystem()

    # Check for urgent emails
    alert_system.check_urgent_emails()

    print("\n" + "="*50 + "\n")

    # Generate daily summary
    alert_system.daily_summary()
```

### JavaScript Implementation

```javascript
// gmailAlertSystem.js
const axios = require("axios");
require("dotenv").config();

class GmailAlertSystem {
  constructor() {
    this.baseUrl =
      process.env.INCREDIBLE_BASE_URL || "https://api.incredible.one";
    this.userId = process.env.USER_ID;
    this.headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${process.env.INCREDIBLE_API_KEY}`,
    };
  }

  async searchEmails(query, maxResults = 10) {
    try {
      const url = `${this.baseUrl}/v1/integrations/gmail/execute`;

      const data = {
        user_id: this.userId,
        feature_name: "GMAIL_SEARCH_EMAILS",
        inputs: {
          query: query,
          max_results: maxResults,
        },
      };

      const response = await axios.post(url, data, { headers: this.headers });
      return response.data.result?.emails || [];
    } catch (error) {
      console.error("Error searching emails:", error.response?.data);
      return [];
    }
  }

  async checkUrgentEmails() {
    console.log("🔍 Checking for urgent emails...");

    const urgentQueries = [
      "subject:URGENT",
      "subject:ASAP",
      "subject:Emergency",
      "is:important is:unread",
    ];

    let allUrgentEmails = [];

    for (const query of urgentQueries) {
      const emails = await this.searchEmails(query, 5);
      allUrgentEmails = allUrgentEmails.concat(emails);
    }

    // Remove duplicates
    const uniqueEmails = Array.from(
      new Map(allUrgentEmails.map((email) => [email.id, email])).values()
    );

    if (uniqueEmails.length > 0) {
      console.log(`⚠️  Found ${uniqueEmails.length} urgent emails!`);
      uniqueEmails.forEach((email) => this.processUrgentEmail(email));
    } else {
      console.log("✅ No urgent emails found");
    }
  }

  processUrgentEmail(email) {
    console.log(`📧 URGENT: ${email.subject || "No Subject"}`);
    console.log(`   From: ${email.sender || "Unknown"}`);
    console.log(`   Received: ${email.date || "Unknown"}`);
    console.log(
      `   Preview: ${(email.snippet || "No preview").substring(0, 100)}...`
    );
    console.log();
  }

  async dailySummary() {
    console.log("📊 Generating daily email summary...");

    const todayEmails = await this.searchEmails("newer_than:1d", 50);

    if (todayEmails.length === 0) {
      console.log("No emails found for today");
      return;
    }

    // Categorize emails
    const categories = {
      urgent: [],
      meetings: [],
      newsletters: [],
      work: [],
      personal: [],
    };

    todayEmails.forEach((email) => {
      const subject = (email.subject || "").toLowerCase();
      const sender = (email.sender || "").toLowerCase();

      if (
        ["urgent", "asap", "emergency"].some((word) => subject.includes(word))
      ) {
        categories.urgent.push(email);
      } else if (
        ["meeting", "call", "conference"].some((word) => subject.includes(word))
      ) {
        categories.meetings.push(email);
      } else if (
        ["newsletter", "noreply", "marketing"].some((word) =>
          sender.includes(word)
        )
      ) {
        categories.newsletters.push(email);
      } else if (
        ["work", "company", "team"].some((word) => sender.includes(word))
      ) {
        categories.work.push(email);
      } else {
        categories.personal.push(email);
      }
    });

    // Print summary
    console.log(`📧 Daily Email Summary (${todayEmails.length} total emails)`);
    console.log("=".repeat(50));

    Object.entries(categories).forEach(([category, emails]) => {
      if (emails.length > 0) {
        console.log(`${category.toUpperCase()}: ${emails.length} emails`);
        emails.slice(0, 3).forEach((email) => {
          console.log(`  • ${email.subject || "No Subject"}`);
        });
        if (emails.length > 3) {
          console.log(`  ... and ${emails.length - 3} more`);
        }
        console.log();
      }
    });
  }
}

// Usage
async function main() {
  const alertSystem = new GmailAlertSystem();

  // Check for urgent emails
  await alertSystem.checkUrgentEmails();

  console.log("\n" + "=".repeat(50) + "\n");

  // Generate daily summary
  await alertSystem.dailySummary();
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = GmailAlertSystem;
```

## Example 2: Email Auto-Responder

Automatically respond to emails based on content and sender.

### Python Implementation

```python
import re
from datetime import datetime

class EmailAutoResponder:
    def __init__(self):
        self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
        self.user_id = os.getenv('USER_ID')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {os.getenv('INCREDIBLE_API_KEY')}"
        }

        # Response templates
        self.templates = {
            "out_of_office": """
Thank you for your email. I am currently out of the office and will respond to your message when I return.

For urgent matters, please contact [alternate contact].

Best regards,
[Your Name]
            """.strip(),

            "meeting_request": """
Thank you for the meeting request. I'll review my calendar and get back to you within 24 hours with my availability.

Best regards,
[Your Name]
            """.strip(),

            "general_inquiry": """
Thank you for reaching out. I've received your message and will respond within 2 business days.

Best regards,
[Your Name]
            """.strip()
        }

    def classify_email(self, email):
        """Classify email type for appropriate response"""
        subject = email.get('subject', '').lower()
        content = email.get('content', '').lower()

        # Meeting request keywords
        if any(word in subject + content for word in ['meeting', 'call', 'schedule', 'appointment']):
            return "meeting_request"

        # General inquiry
        if any(word in subject + content for word in ['question', 'inquiry', 'help', 'support']):
            return "general_inquiry"

        # Default
        return "general_inquiry"

    def should_auto_respond(self, email):
        """Determine if email should get auto-response"""
        sender = email.get('sender', '').lower()

        # Don't respond to automated emails
        automated_patterns = [
            'noreply', 'no-reply', 'donotreply', 'automated',
            'notification', 'newsletter', 'marketing'
        ]

        if any(pattern in sender for pattern in automated_patterns):
            return False

        # Don't respond to internal emails (customize domain)
        if '@yourdomain.com' in sender:
            return False

        return True

    def send_auto_response(self, original_email, template_type):
        """Send automatic response email"""
        url = f"{self.base_url}/v1/integrations/gmail/execute"

        template = self.templates.get(template_type, self.templates["general_inquiry"])

        data = {
            "user_id": self.user_id,
            "feature_name": "GMAIL_SEND_EMAIL",
            "inputs": {
                "to": original_email.get('sender'),
                "subject": f"Re: {original_email.get('subject', 'Your Email')}",
                "body": template,
                "reply_to_message_id": original_email.get('id')
            }
        }

        response = requests.post(url, headers=self.headers, json=data)

        if response.status_code == 200:
            print(f"✅ Auto-response sent to {original_email.get('sender')}")
            return True
        else:
            print(f"❌ Failed to send auto-response: {response.text}")
            return False

    def process_new_emails(self):
        """Process new emails for auto-responses"""
        print("🔍 Checking for new emails to auto-respond...")

        # Get unread emails from last 2 hours
        unread_emails = self.search_emails("is:unread newer_than:2h", max_results=20)

        responses_sent = 0

        for email in unread_emails:
            if self.should_auto_respond(email):
                email_type = self.classify_email(email)

                print(f"📧 Processing: {email.get('subject', 'No Subject')}")
                print(f"   Type: {email_type}")

                if self.send_auto_response(email, email_type):
                    responses_sent += 1

                    # Mark as read to avoid re-processing
                    self.mark_as_read(email.get('id'))

        print(f"🎉 Sent {responses_sent} auto-responses")

    def mark_as_read(self, email_id):
        """Mark email as read"""
        url = f"{self.base_url}/v1/integrations/gmail/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "GMAIL_MARK_READ",
            "inputs": {
                "email_id": email_id
            }
        }

        requests.post(url, headers=self.headers, json=data)

# Usage
if __name__ == "__main__":
    responder = EmailAutoResponder()
    responder.process_new_emails()
```

## Example 3: Email Analytics

Track and analyze your email patterns.

### Python Implementation

```python
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import json

class EmailAnalytics:
    def __init__(self):
        self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
        self.user_id = os.getenv('USER_ID')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {os.getenv('INCREDIBLE_API_KEY')}"
        }

    def get_email_stats(self, days=30):
        """Get comprehensive email statistics"""
        print(f"📊 Analyzing emails from the last {days} days...")

        # Get emails from specified period
        query = f"newer_than:{days}d"
        emails = self.search_emails(query, max_results=1000)

        if not emails:
            print("No emails found for analysis")
            return

        stats = self.analyze_emails(emails)
        self.print_stats(stats, days)

    def analyze_emails(self, emails):
        """Analyze email data and generate statistics"""
        stats = {
            "total_emails": len(emails),
            "by_day": defaultdict(int),
            "by_hour": defaultdict(int),
            "by_sender": Counter(),
            "by_domain": Counter(),
            "by_subject_keywords": Counter(),
            "response_times": [],
            "email_lengths": []
        }

        for email in emails:
            # Parse date
            date_str = email.get('date', '')
            try:
                email_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))

                # Day of week analysis
                day_name = email_date.strftime('%A')
                stats["by_day"][day_name] += 1

                # Hour analysis
                hour = email_date.hour
                stats["by_hour"][hour] += 1

            except:
                pass

            # Sender analysis
            sender = email.get('sender', '')
            if sender:
                stats["by_sender"][sender] += 1

                # Domain analysis
                if '@' in sender:
                    domain = sender.split('@')[1]
                    stats["by_domain"][domain] += 1

            # Subject keyword analysis
            subject = email.get('subject', '').lower()
            words = re.findall(r'\w+', subject)
            for word in words:
                if len(word) > 3:  # Only meaningful words
                    stats["by_subject_keywords"][word] += 1

            # Email length analysis
            content = email.get('content', '')
            if content:
                stats["email_lengths"].append(len(content))

        return stats

    def print_stats(self, stats, days):
        """Print formatted statistics"""
        print("=" * 60)
        print(f"📧 EMAIL ANALYTICS REPORT ({days} days)")
        print("=" * 60)

        print(f"\n📈 OVERVIEW")
        print(f"Total emails: {stats['total_emails']}")
        print(f"Average per day: {stats['total_emails'] / days:.1f}")

        if stats['email_lengths']:
            avg_length = sum(stats['email_lengths']) / len(stats['email_lengths'])
            print(f"Average email length: {avg_length:.0f} characters")

        print(f"\n📅 BY DAY OF WEEK")
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            count = stats['by_day'][day]
            bar = '█' * min(count // 5, 20)
            print(f"{day:10} {count:4d} {bar}")

        print(f"\n🕐 BY HOUR OF DAY")
        for hour in range(24):
            count = stats['by_hour'][hour]
            bar = '█' * min(count // 2, 30)
            print(f"{hour:2d}:00 {count:4d} {bar}")

        print(f"\n👤 TOP SENDERS")
        for sender, count in stats['by_sender'].most_common(10):
            print(f"{count:4d} {sender}")

        print(f"\n🌐 TOP DOMAINS")
        for domain, count in stats['by_domain'].most_common(10):
            print(f"{count:4d} {domain}")

        print(f"\n🔤 COMMON SUBJECT KEYWORDS")
        for keyword, count in stats['by_subject_keywords'].most_common(15):
            print(f"{count:4d} {keyword}")

        print("\n" + "=" * 60)

# Usage
if __name__ == "__main__":
    analytics = EmailAnalytics()
    analytics.get_email_stats(days=30)
```

## Best Practices

### 1. Rate Limiting

```python
import time

def rate_limited_requests(requests_list, delay=1):
    """Execute requests with rate limiting"""
    for request in requests_list:
        result = execute_request(request)
        time.sleep(delay)  # Respect API limits
        yield result
```

### 2. Error Handling

```python
def robust_gmail_operation(operation, max_retries=3):
    """Execute Gmail operations with retry logic"""
    for attempt in range(max_retries):
        try:
            return operation()
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(2 ** attempt)
            else:
                print(f"Operation failed after {max_retries} attempts: {e}")
                raise
```

### 3. Email Safety

```python
def validate_email_address(email):
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_email_content(content):
    """Sanitize email content for safety"""
    # Remove potentially harmful content
    # Escape HTML entities
    # Validate attachments
    return content
```

## Next Steps

- **[Multi-Integration Examples](../multi-integration/)** - Combine Gmail with other services
- **[Advanced Gmail Patterns](../../advanced/gmail-advanced.md)** - Complex email workflows
- **[Function Calling Examples](../function-calling/)** - Custom email processing functions

These examples demonstrate the foundation of Gmail automation with the Incredible API. You can extend these patterns to create sophisticated email management systems!
