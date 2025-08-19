# Email to Sheets Automation

A practical example of combining Gmail and Google Sheets to automatically log and track important emails.

## Use Case

Automatically track important emails in a Google Sheets spreadsheet for:

- Customer inquiries monitoring
- Support ticket logging
- Lead tracking
- Email analytics
- Team communication tracking

## Prerequisites

- Incredible API account and credentials
- Gmail integration connected (OAuth)
- Google Sheets integration connected (OAuth)
- A Google Sheets document with appropriate headers

## Setup

### 1. Create Your Tracking Spreadsheet

Create a Google Sheet with these columns:

```
| Date | Subject | Sender | Priority | Labels | Content Preview | Status |
```

### 2. Get Your Sheet ID

From your Google Sheets URL:

```
https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
```

## Implementation

### Python Version

```python
import os
import re
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class EmailToSheetsLogger:
    def __init__(self):
        self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
        self.user_id = os.getenv('USER_ID')
        self.sheet_id = os.getenv('EMAIL_TRACKING_SHEET_ID')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {os.getenv('INCREDIBLE_API_KEY')}"
        }

        # Define email filters
        self.filters = {
            "high_priority": [
                "is:important",
                "subject:urgent",
                "subject:asap",
                "from:ceo@",
                "from:support@"
            ],
            "customer_inquiries": [
                "subject:inquiry",
                "subject:question",
                "subject:help",
                "to:sales@",
                "to:support@"
            ],
            "leads": [
                "subject:demo",
                "subject:trial",
                "subject:pricing",
                "subject:partnership"
            ]
        }

    def search_emails(self, query, max_results=20):
        """Search Gmail with specified query"""
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

    def add_to_sheets(self, row_data):
        """Add a row to Google Sheets"""
        url = f"{self.base_url}/v1/integrations/google_sheets/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "SHEETS_ADD_ROW",
            "inputs": {
                "spreadsheet_id": self.sheet_id,
                "range": "Sheet1",  # or your sheet name
                "values": [row_data]
            }
        }

        response = requests.post(url, headers=self.headers, json=data)

        if response.status_code == 200:
            return True
        else:
            print(f"Error adding to sheets: {response.text}")
            return False

    def determine_priority(self, email):
        """Determine email priority based on content and sender"""
        subject = email.get('subject', '').lower()
        sender = email.get('sender', '').lower()
        content = email.get('content', '').lower()

        # High priority indicators
        high_priority_words = ['urgent', 'asap', 'emergency', 'critical', 'immediate']
        if any(word in subject + content for word in high_priority_words):
            return "HIGH"

        # VIP senders
        vip_domains = ['ceo@', 'founder@', 'president@']
        if any(domain in sender for domain in vip_domains):
            return "HIGH"

        # Medium priority
        medium_priority_words = ['important', 'meeting', 'deadline', 'review']
        if any(word in subject + content for word in medium_priority_words):
            return "MEDIUM"

        return "LOW"

    def extract_labels(self, email):
        """Extract or determine labels for the email"""
        labels = []

        subject = email.get('subject', '').lower()
        content = email.get('content', '').lower()

        # Business labels
        if any(word in subject + content for word in ['meeting', 'call', 'conference']):
            labels.append('meeting')

        if any(word in subject + content for word in ['invoice', 'payment', 'billing']):
            labels.append('financial')

        if any(word in subject + content for word in ['support', 'help', 'issue', 'problem']):
            labels.append('support')

        if any(word in subject + content for word in ['demo', 'trial', 'pricing']):
            labels.append('sales')

        return ', '.join(labels) if labels else 'general'

    def clean_content_preview(self, content, max_length=100):
        """Create a clean preview of email content"""
        if not content:
            return "No content"

        # Remove HTML tags
        clean_content = re.sub(r'<[^>]+>', '', content)

        # Remove extra whitespace
        clean_content = ' '.join(clean_content.split())

        # Truncate if too long
        if len(clean_content) > max_length:
            clean_content = clean_content[:max_length] + "..."

        return clean_content

    def format_email_for_sheets(self, email):
        """Format email data for Google Sheets row"""
        return [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Date
            email.get('subject', 'No Subject'),             # Subject
            email.get('sender', 'Unknown'),                 # Sender
            self.determine_priority(email),                 # Priority
            self.extract_labels(email),                     # Labels
            self.clean_content_preview(email.get('content', '')),  # Content Preview
            'NEW'                                           # Status
        ]

    def process_filter_category(self, category_name, queries):
        """Process emails for a specific filter category"""
        print(f"\n🔍 Processing {category_name} emails...")

        all_emails = []

        # Combine results from all queries in this category
        for query in queries:
            emails = self.search_emails(query, max_results=10)
            all_emails.extend(emails)

        # Remove duplicates based on email ID
        unique_emails = {email.get('id'): email for email in all_emails}.values()

        processed_count = 0

        for email in unique_emails:
            # Check if email was sent in last 24 hours (adjust as needed)
            try:
                email_date = datetime.fromisoformat(email.get('date', '').replace('Z', '+00:00'))
                hours_ago = (datetime.now(email_date.tzinfo) - email_date).total_seconds() / 3600

                if hours_ago > 24:  # Skip older emails
                    continue

            except:
                # If date parsing fails, process the email anyway
                pass

            # Format and add to sheets
            row_data = self.format_email_for_sheets(email)

            if self.add_to_sheets(row_data):
                print(f"✅ Logged: {email.get('subject', 'No Subject')}")
                processed_count += 1
            else:
                print(f"❌ Failed to log: {email.get('subject', 'No Subject')}")

        print(f"📊 Processed {processed_count} {category_name} emails")
        return processed_count

    def run_daily_sync(self):
        """Run the daily email to sheets synchronization"""
        print("🚀 Starting Email to Sheets Sync...")
        print(f"📊 Target Sheet: {self.sheet_id}")
        print(f"👤 User: {self.user_id}")
        print()

        total_processed = 0

        # Process each filter category
        for category_name, queries in self.filters.items():
            count = self.process_filter_category(category_name, queries)
            total_processed += count

        print(f"\n🎉 Sync Complete!")
        print(f"📧 Total emails processed: {total_processed}")
        print(f"📊 View your tracking sheet: https://docs.google.com/spreadsheets/d/{self.sheet_id}")

    def setup_sheet_headers(self):
        """Setup the initial headers in the Google Sheets"""
        headers = [
            "Date", "Subject", "Sender", "Priority",
            "Labels", "Content Preview", "Status"
        ]

        url = f"{self.base_url}/v1/integrations/google_sheets/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "SHEETS_UPDATE_RANGE",
            "inputs": {
                "spreadsheet_id": self.sheet_id,
                "range": "A1:G1",
                "values": [headers]
            }
        }

        response = requests.post(url, headers=self.headers, json=data)

        if response.status_code == 200:
            print("✅ Sheet headers configured")
        else:
            print(f"❌ Failed to setup headers: {response.text}")

    def get_sheet_stats(self):
        """Get statistics from the tracking sheet"""
        url = f"{self.base_url}/v1/integrations/google_sheets/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "SHEETS_READ_RANGE",
            "inputs": {
                "spreadsheet_id": self.sheet_id,
                "range": "A:G"  # Read all data
            }
        }

        response = requests.post(url, headers=self.headers, json=data)

        if response.status_code == 200:
            data = response.json().get("result", {}).get("values", [])

            if len(data) > 1:  # More than just headers
                print(f"📊 Total logged emails: {len(data) - 1}")

                # Count by priority
                priority_count = {}
                for row in data[1:]:  # Skip header
                    if len(row) > 3:
                        priority = row[3]
                        priority_count[priority] = priority_count.get(priority, 0) + 1

                print("📈 By Priority:")
                for priority, count in priority_count.items():
                    print(f"   {priority}: {count}")
            else:
                print("📊 No emails logged yet")
        else:
            print(f"❌ Failed to read sheet stats: {response.text}")

# Usage Examples
if __name__ == "__main__":
    logger = EmailToSheetsLogger()

    # Setup (run once)
    # logger.setup_sheet_headers()

    # Daily sync (run regularly)
    logger.run_daily_sync()

    # View statistics
    print("\n" + "="*50)
    logger.get_sheet_stats()
```

### JavaScript Version

```javascript
// emailToSheetsLogger.js
const axios = require("axios");
require("dotenv").config();

class EmailToSheetsLogger {
  constructor() {
    this.baseUrl =
      process.env.INCREDIBLE_BASE_URL || "https://api.incredible.one";
    this.userId = process.env.USER_ID;
    this.sheetId = process.env.EMAIL_TRACKING_SHEET_ID;
    this.headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${process.env.INCREDIBLE_API_KEY}`,
    };

    this.filters = {
      high_priority: [
        "is:important",
        "subject:urgent",
        "subject:asap",
        "from:ceo@",
        "from:support@",
      ],
      customer_inquiries: [
        "subject:inquiry",
        "subject:question",
        "subject:help",
        "to:sales@",
        "to:support@",
      ],
      leads: [
        "subject:demo",
        "subject:trial",
        "subject:pricing",
        "subject:partnership",
      ],
    };
  }

  async searchEmails(query, maxResults = 20) {
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

  async addToSheets(rowData) {
    try {
      const url = `${this.baseUrl}/v1/integrations/google_sheets/execute`;

      const data = {
        user_id: this.userId,
        feature_name: "SHEETS_ADD_ROW",
        inputs: {
          spreadsheet_id: this.sheetId,
          range: "Sheet1",
          values: [rowData],
        },
      };

      await axios.post(url, data, { headers: this.headers });
      return true;
    } catch (error) {
      console.error("Error adding to sheets:", error.response?.data);
      return false;
    }
  }

  determinePriority(email) {
    const subject = (email.subject || "").toLowerCase();
    const sender = (email.sender || "").toLowerCase();
    const content = (email.content || "").toLowerCase();

    const highPriorityWords = [
      "urgent",
      "asap",
      "emergency",
      "critical",
      "immediate",
    ];
    if (highPriorityWords.some((word) => (subject + content).includes(word))) {
      return "HIGH";
    }

    const vipDomains = ["ceo@", "founder@", "president@"];
    if (vipDomains.some((domain) => sender.includes(domain))) {
      return "HIGH";
    }

    const mediumPriorityWords = ["important", "meeting", "deadline", "review"];
    if (
      mediumPriorityWords.some((word) => (subject + content).includes(word))
    ) {
      return "MEDIUM";
    }

    return "LOW";
  }

  extractLabels(email) {
    const labels = [];
    const subject = (email.subject || "").toLowerCase();
    const content = (email.content || "").toLowerCase();

    if (
      ["meeting", "call", "conference"].some((word) =>
        (subject + content).includes(word)
      )
    ) {
      labels.push("meeting");
    }

    if (
      ["invoice", "payment", "billing"].some((word) =>
        (subject + content).includes(word)
      )
    ) {
      labels.push("financial");
    }

    if (
      ["support", "help", "issue", "problem"].some((word) =>
        (subject + content).includes(word)
      )
    ) {
      labels.push("support");
    }

    if (
      ["demo", "trial", "pricing"].some((word) =>
        (subject + content).includes(word)
      )
    ) {
      labels.push("sales");
    }

    return labels.length > 0 ? labels.join(", ") : "general";
  }

  cleanContentPreview(content, maxLength = 100) {
    if (!content) return "No content";

    // Remove HTML tags
    let cleanContent = content.replace(/<[^>]+>/g, "");

    // Remove extra whitespace
    cleanContent = cleanContent.replace(/\s+/g, " ").trim();

    // Truncate if too long
    if (cleanContent.length > maxLength) {
      cleanContent = cleanContent.substring(0, maxLength) + "...";
    }

    return cleanContent;
  }

  formatEmailForSheets(email) {
    return [
      new Date().toISOString().slice(0, 19).replace("T", " "),
      email.subject || "No Subject",
      email.sender || "Unknown",
      this.determinePriority(email),
      this.extractLabels(email),
      this.cleanContentPreview(email.content || ""),
      "NEW",
    ];
  }

  async processFilterCategory(categoryName, queries) {
    console.log(`\n🔍 Processing ${categoryName} emails...`);

    let allEmails = [];

    for (const query of queries) {
      const emails = await this.searchEmails(query, 10);
      allEmails = allEmails.concat(emails);
    }

    // Remove duplicates
    const uniqueEmails = Array.from(
      new Map(allEmails.map((email) => [email.id, email])).values()
    );

    let processedCount = 0;

    for (const email of uniqueEmails) {
      try {
        const emailDate = new Date(email.date);
        const hoursAgo = (Date.now() - emailDate.getTime()) / (1000 * 60 * 60);

        if (hoursAgo > 24) continue; // Skip older emails
      } catch (e) {
        // Continue processing if date parsing fails
      }

      const rowData = this.formatEmailForSheets(email);

      if (await this.addToSheets(rowData)) {
        console.log(`✅ Logged: ${email.subject || "No Subject"}`);
        processedCount++;
      } else {
        console.log(`❌ Failed to log: ${email.subject || "No Subject"}`);
      }
    }

    console.log(`📊 Processed ${processedCount} ${categoryName} emails`);
    return processedCount;
  }

  async runDailySync() {
    console.log("🚀 Starting Email to Sheets Sync...");
    console.log(`📊 Target Sheet: ${this.sheetId}`);
    console.log(`👤 User: ${this.userId}`);
    console.log();

    let totalProcessed = 0;

    for (const [categoryName, queries] of Object.entries(this.filters)) {
      const count = await this.processFilterCategory(categoryName, queries);
      totalProcessed += count;
    }

    console.log(`\n🎉 Sync Complete!`);
    console.log(`📧 Total emails processed: ${totalProcessed}`);
    console.log(
      `📊 View your tracking sheet: https://docs.google.com/spreadsheets/d/${this.sheetId}`
    );
  }

  async setupSheetHeaders() {
    const headers = [
      "Date",
      "Subject",
      "Sender",
      "Priority",
      "Labels",
      "Content Preview",
      "Status",
    ];

    try {
      const url = `${this.baseUrl}/v1/integrations/google_sheets/execute`;

      const data = {
        user_id: this.userId,
        feature_name: "SHEETS_UPDATE_RANGE",
        inputs: {
          spreadsheet_id: this.sheetId,
          range: "A1:G1",
          values: [headers],
        },
      };

      await axios.post(url, data, { headers: this.headers });
      console.log("✅ Sheet headers configured");
    } catch (error) {
      console.error("❌ Failed to setup headers:", error.response?.data);
    }
  }
}

// Usage
async function main() {
  const logger = new EmailToSheetsLogger();

  // Setup (run once)
  // await logger.setupSheetHeaders();

  // Daily sync (run regularly)
  await logger.runDailySync();
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = EmailToSheetsLogger;
```

## Configuration

### Environment Variables

```bash
# .env
INCREDIBLE_API_KEY=your_api_key
INCREDIBLE_BASE_URL=https://api.incredible.one
USER_ID=your_user_id
EMAIL_TRACKING_SHEET_ID=your_google_sheet_id
```

### Customization Options

#### 1. Custom Filters

```python
# Add your own email filters
custom_filters = {
    "security_alerts": [
        "subject:security",
        "subject:alert",
        "from:security@"
    ],
    "invoices": [
        "subject:invoice",
        "subject:billing",
        "has:attachment filename:pdf"
    ]
}
```

#### 2. Advanced Priority Rules

```python
def advanced_priority_logic(email):
    # Customer tier-based priority
    sender = email.get('sender', '')

    if sender in ['enterprise@customer.com']:
        return "CRITICAL"

    # Time-sensitive content
    content = email.get('content', '').lower()
    if 'deadline tomorrow' in content:
        return "HIGH"

    return determine_priority(email)
```

#### 3. Smart Categorization

```python
def ai_categorize_email(email_content):
    """Use AI to categorize emails more accurately"""
    categorization_function = {
        "name": "categorize_email",
        "description": "Categorize email content into business categories",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {"type": "string"},
                "subject": {"type": "string"},
                "sender": {"type": "string"}
            }
        }
    }
    # Implement AI-powered categorization
```

## Automation & Scheduling

### 1. Cron Job Setup (Linux/Mac)

```bash
# Run every hour during business hours
0 9-17 * * 1-5 cd /path/to/your/script && python email_to_sheets_logger.py

# Run daily at 9 AM
0 9 * * * cd /path/to/your/script && python email_to_sheets_logger.py
```

### 2. Windows Task Scheduler

Create a batch file and schedule it:

```batch
@echo off
cd C:\path\to\your\script
python email_to_sheets_logger.py
```

### 3. Cloud Functions (AWS Lambda, Google Cloud Functions)

```python
def lambda_handler(event, context):
    logger = EmailToSheetsLogger()
    logger.run_daily_sync()

    return {
        'statusCode': 200,
        'body': 'Email sync completed'
    }
```

## Analytics & Reporting

### Generate Reports from Your Data

```python
def generate_weekly_email_report(sheet_id):
    """Generate analytics from tracked email data"""
    # Read data from sheets
    data = read_sheet_data(sheet_id)

    # Analyze patterns
    metrics = {
        "total_emails": len(data),
        "by_priority": count_by_priority(data),
        "by_sender": count_by_sender(data),
        "response_time": calculate_response_times(data),
        "trends": analyze_trends(data)
    }

    # Create report
    return generate_report(metrics)
```

## Best Practices

### 1. Deduplication

- Use email IDs to prevent duplicates
- Track processed emails in a separate sheet
- Implement date-based filtering

### 2. Error Handling

- Retry failed operations
- Log errors to a separate sheet
- Send alerts for critical failures

### 3. Performance

- Use batch operations when possible
- Implement rate limiting
- Process emails in chunks

### 4. Data Quality

- Validate email data before logging
- Sanitize content to prevent formatting issues
- Implement data cleanup routines

## Troubleshooting

### Common Issues

1. **Duplicate Entries**

   - Implement email ID tracking
   - Use date filters to avoid reprocessing

2. **Rate Limits**

   - Add delays between API calls
   - Implement exponential backoff

3. **Authentication Errors**
   - Refresh OAuth tokens
   - Verify integration connections

## Next Steps

This example demonstrates the foundation of multi-integration workflows. You can extend it by:

1. **Adding Slack Notifications** - Alert team when high-priority emails arrive
2. **Integrating with Asana** - Create tasks from support emails
3. **Adding Analytics** - Generate insights from email patterns

Ready to explore more complex workflows? Check out our [advanced multi-integration examples](./README.md)!
