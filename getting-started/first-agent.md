# Your First Agent

Build your first multi-integration AI agent that demonstrates the power of combining multiple services in a single automation workflow.

## What We'll Build

**Meeting Organizer Agent**: An agent that extracts meeting details from Gmail, organizes them in Google Sheets, and creates tasks in Asana.

**Skills Demonstrated**:

- Email parsing and extraction
- Spreadsheet automation
- Task management integration
- Multi-step workflows

## Prerequisites

1. Complete the [Quick Setup](./quick-setup.md)
2. Follow the [Authentication Guide](./authentication.md) to connect:
   - Gmail (OAuth)
   - Google Sheets (OAuth)
   - Asana (OAuth or API Key)

## Step 1: Define Your Agent Functions

First, let's define the functions our agent will use:

```python
# agent_functions.py
import re
from datetime import datetime

def extract_meeting_details(email_content):
    """Extract meeting information from email content"""
    meeting_details = {
        "subject": "",
        "date": "",
        "time": "",
        "attendees": [],
        "location": "",
        "agenda": ""
    }

    # Simple regex patterns for meeting extraction
    patterns = {
        "zoom_link": r"https://[\w\.-]+\.zoom\.us/j/\d+",
        "date": r"(\w+day,?\s+\w+\s+\d{1,2},?\s+\d{4})",
        "time": r"(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm))",
        "email": r"[\w\.-]+@[\w\.-]+\.\w+"
    }

    # Extract information using patterns
    for key, pattern in patterns.items():
        matches = re.findall(pattern, email_content)
        if matches:
            if key == "email":
                meeting_details["attendees"] = matches
            else:
                meeting_details[key] = matches[0] if matches else ""

    return meeting_details

def format_meeting_for_sheets(meeting_details):
    """Format meeting details for Google Sheets"""
    return [
        meeting_details.get("subject", ""),
        meeting_details.get("date", ""),
        meeting_details.get("time", ""),
        ", ".join(meeting_details.get("attendees", [])),
        meeting_details.get("location", ""),
        meeting_details.get("agenda", ""),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]

def create_asana_task_data(meeting_details):
    """Format meeting details for Asana task creation"""
    task_name = f"Meeting: {meeting_details.get('subject', 'Untitled Meeting')}"

    notes = f"""
Meeting Details:
📅 Date: {meeting_details.get('date', 'TBD')}
🕒 Time: {meeting_details.get('time', 'TBD')}
👥 Attendees: {', '.join(meeting_details.get('attendees', []))}
📍 Location: {meeting_details.get('location', 'TBD')}
📋 Agenda: {meeting_details.get('agenda', 'No agenda provided')}

Preparation Tasks:
□ Review meeting agenda
□ Prepare necessary documents
□ Test video call connection
□ Send reminder to attendees
    """.strip()

    return {
        "name": task_name,
        "notes": notes,
        "due_date": meeting_details.get("date", ""),
    }
```

## Step 2: Create the Main Agent

Now let's build the main agent that orchestrates all integrations:

```python
# meeting_organizer_agent.py
import os
import requests
import json
from dotenv import load_dotenv
from agent_functions import extract_meeting_details, format_meeting_for_sheets, create_asana_task_data

load_dotenv()

class MeetingOrganizerAgent:
    def __init__(self):
        self.api_key = os.getenv('INCREDIBLE_API_KEY')
        self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
        self.user_id = os.getenv('USER_ID')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def get_recent_emails(self, query="meeting OR call OR conference"):
        """Fetch recent emails that might contain meeting information"""

        # Define Gmail search function
        gmail_function = {
            "name": "gmail_search_emails",
            "description": "Search for emails in Gmail",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Gmail search query"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of emails to return"
                    }
                },
                "required": ["query"]
            }
        }

        # Create request
        data = {
            "model": "small-1",
            "messages": [
                {"role": "user", "content": f"Search for emails with query: {query}"}
            ],
            "stream": False,
            "functions": [gmail_function],
            "system": "You are a helpful assistant that can search Gmail for emails."
        }

        # Execute request
        response = requests.post(
            f"{self.base_url}/v1/chat-completion",
            headers=self.headers,
            json=data
        )

        if response.status_code == 200:
            return self.execute_gmail_search(response.json(), query)
        else:
            print(f"Error fetching emails: {response.text}")
            return []

    def execute_gmail_search(self, response_data, query):
        """Execute the Gmail search using the integrations API"""
        url = f"{self.base_url}/v1/integrations/gmail/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "GMAIL_SEARCH_EMAILS",
            "inputs": {
                "query": query,
                "max_results": 10
            }
        }

        response = requests.post(url, headers=self.headers, json=data)

        if response.status_code == 200:
            result = response.json()
            return result.get("result", {}).get("emails", [])
        else:
            print(f"Gmail search failed: {response.text}")
            return []

    def add_to_sheets(self, meeting_data):
        """Add meeting data to Google Sheets"""
        url = f"{self.base_url}/v1/integrations/google_sheets/execute"

        # Prepare data for sheets
        sheet_row = format_meeting_for_sheets(meeting_data)

        data = {
            "user_id": self.user_id,
            "feature_name": "SHEETS_ADD_ROW",
            "inputs": {
                "spreadsheet_id": os.getenv("MEETINGS_SHEET_ID"),
                "sheet_name": "Meetings",
                "values": [sheet_row]
            }
        }

        response = requests.post(url, headers=self.headers, json=data)

        if response.status_code == 200:
            print("✅ Meeting added to Google Sheets")
            return True
        else:
            print(f"❌ Failed to add to sheets: {response.text}")
            return False

    def create_asana_task(self, meeting_data):
        """Create a task in Asana for meeting preparation"""
        url = f"{self.base_url}/v1/integrations/asana/execute"

        task_data = create_asana_task_data(meeting_data)

        data = {
            "user_id": self.user_id,
            "feature_name": "ASANA_CREATE_TASK",
            "inputs": {
                "name": task_data["name"],
                "notes": task_data["notes"],
                "due_date": task_data["due_date"],
                "project_id": os.getenv("ASANA_PROJECT_ID")
            }
        }

        response = requests.post(url, headers=self.headers, json=data)

        if response.status_code == 200:
            print("✅ Task created in Asana")
            return True
        else:
            print(f"❌ Failed to create Asana task: {response.text}")
            return False

    def process_emails_for_meetings(self):
        """Main workflow: Process emails and organize meetings"""
        print("🔍 Searching for meeting-related emails...")

        # Step 1: Get recent emails
        emails = self.get_recent_emails()

        if not emails:
            print("No emails found")
            return

        print(f"📧 Found {len(emails)} emails to process")

        meetings_processed = 0

        # Step 2: Process each email
        for email in emails:
            print(f"\n📨 Processing: {email.get('subject', 'No Subject')}")

            # Extract meeting details
            meeting_details = extract_meeting_details(
                email.get('content', '') + ' ' + email.get('subject', '')
            )

            # Only process if we found meeting-like content
            if any([meeting_details.get('date'), meeting_details.get('time'),
                   'meeting' in email.get('subject', '').lower()]):

                # Step 3: Add to Google Sheets
                self.add_to_sheets(meeting_details)

                # Step 4: Create Asana task
                self.create_asana_task(meeting_details)

                meetings_processed += 1
                print(f"✅ Meeting organized: {meeting_details.get('subject', 'Untitled')}")

        print(f"\n🎉 Workflow complete! Processed {meetings_processed} meetings")

    def run_agent(self):
        """Run the complete meeting organizer workflow"""
        print("🚀 Starting Meeting Organizer Agent...")
        print("📋 This agent will:")
        print("  1. Search Gmail for meeting-related emails")
        print("  2. Extract meeting details from email content")
        print("  3. Add meeting info to Google Sheets")
        print("  4. Create preparation tasks in Asana")
        print()

        try:
            self.process_emails_for_meetings()
        except Exception as e:
            print(f"❌ Agent failed: {str(e)}")
            print("Check your integrations and API connections")

# Usage
if __name__ == "__main__":
    agent = MeetingOrganizerAgent()
    agent.run_agent()
```

## Step 3: Environment Configuration

Update your `.env` file with the necessary configuration:

```bash
# .env

# API Configuration
INCREDIBLE_API_KEY=your_api_key_here
INCREDIBLE_BASE_URL=https://api.incredible.one
USER_ID=your_user_id

# Google Sheets Configuration
MEETINGS_SHEET_ID=your_google_sheet_id

# Asana Configuration
ASANA_PROJECT_ID=your_asana_project_id

# Debug mode
DEBUG=true
```

## Step 4: Complete Agent Implementation

<div class="code-tabs" data-section="meeting-organizer-agent">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python"># meeting_organizer_agent.py

```javascript
// meetingOrganizerAgent.js
const axios = require("axios");
require("dotenv").config();

class MeetingOrganizerAgent {
  constructor() {
    this.apiKey = process.env.INCREDIBLE_API_KEY;
    this.baseUrl =
      process.env.INCREDIBLE_BASE_URL || "https://api.incredible.one";
    this.userId = process.env.USER_ID;
    this.headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${this.apiKey}`,
    };
  }

  extractMeetingDetails(emailContent) {
    const meetingDetails = {
      subject: "",
      date: "",
      time: "",
      attendees: [],
      location: "",
      agenda: "",
    };

    // Extract information using regex
    const patterns = {
      zoom_link: /https:\/\/[\w\.-]+\.zoom\.us\/j\/\d+/g,
      date: /(\w+day,?\s+\w+\s+\d{1,2},?\s+\d{4})/g,
      time: /(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm))/g,
      email: /[\w\.-]+@[\w\.-]+\.\w+/g,
    };

    for (const [key, pattern] of Object.entries(patterns)) {
      const matches = emailContent.match(pattern);
      if (matches) {
        if (key === "email") {
          meetingDetails.attendees = matches;
        } else {
          meetingDetails[key] = matches[0] || "";
        }
      }
    }

    return meetingDetails;
  }

  async getRecentEmails(query = "meeting OR call OR conference") {
    try {
      const url = `${this.baseUrl}/v1/integrations/gmail/execute`;

      const data = {
        user_id: this.userId,
        feature_name: "GMAIL_SEARCH_EMAILS",
        inputs: {
          query: query,
          max_results: 10,
        },
      };

      const response = await axios.post(url, data, { headers: this.headers });
      return response.data.result?.emails || [];
    } catch (error) {
      console.error("❌ Failed to fetch emails:", error.response?.data);
      return [];
    }
  }

  async addToSheets(meetingData) {
    try {
      const url = `${this.baseUrl}/v1/integrations/google_sheets/execute`;

      const sheetRow = [
        meetingData.subject || "",
        meetingData.date || "",
        meetingData.time || "",
        meetingData.attendees?.join(", ") || "",
        meetingData.location || "",
        meetingData.agenda || "",
        new Date().toISOString(),
      ];

      const data = {
        user_id: this.userId,
        feature_name: "SHEETS_ADD_ROW",
        inputs: {
          spreadsheet_id: process.env.MEETINGS_SHEET_ID,
          sheet_name: "Meetings",
          values: [sheetRow],
        },
      };

      await axios.post(url, data, { headers: this.headers });
      console.log("✅ Meeting added to Google Sheets");
      return true;
    } catch (error) {
      console.error("❌ Failed to add to sheets:", error.response?.data);
      return false;
    }
  }

  async createAsanaTask(meetingData) {
    try {
      const url = `${this.baseUrl}/v1/integrations/asana/execute`;

      const taskName = `Meeting: ${meetingData.subject || "Untitled Meeting"}`;
      const notes = `
Meeting Details:
📅 Date: ${meetingData.date || "TBD"}
🕒 Time: ${meetingData.time || "TBD"}
👥 Attendees: ${meetingData.attendees?.join(", ") || "None"}
📍 Location: ${meetingData.location || "TBD"}
📋 Agenda: ${meetingData.agenda || "No agenda provided"}

Preparation Tasks:
□ Review meeting agenda
□ Prepare necessary documents
□ Test video call connection
□ Send reminder to attendees
            `.trim();

      const data = {
        user_id: this.userId,
        feature_name: "ASANA_CREATE_TASK",
        inputs: {
          name: taskName,
          notes: notes,
          due_date: meetingData.date,
          project_id: process.env.ASANA_PROJECT_ID,
        },
      };

      await axios.post(url, data, { headers: this.headers });
      console.log("✅ Task created in Asana");
      return true;
    } catch (error) {
      console.error("❌ Failed to create Asana task:", error.response?.data);
      return false;
    }
  }

  async processEmailsForMeetings() {
    console.log("🔍 Searching for meeting-related emails...");

    // Step 1: Get recent emails
    const emails = await this.getRecentEmails();

    if (emails.length === 0) {
      console.log("No emails found");
      return;
    }

    console.log(`📧 Found ${emails.length} emails to process`);

    let meetingsProcessed = 0;

    // Step 2: Process each email
    for (const email of emails) {
      console.log(`\n📨 Processing: ${email.subject || "No Subject"}`);

      // Extract meeting details
      const meetingDetails = this.extractMeetingDetails(
        (email.content || "") + " " + (email.subject || "")
      );

      // Only process if we found meeting-like content
      if (
        meetingDetails.date ||
        meetingDetails.time ||
        (email.subject || "").toLowerCase().includes("meeting")
      ) {
        // Step 3: Add to Google Sheets
        await this.addToSheets(meetingDetails);

        // Step 4: Create Asana task
        await this.createAsanaTask(meetingDetails);

        meetingsProcessed++;
        console.log(
          `✅ Meeting organized: ${meetingDetails.subject || "Untitled"}`
        );
      }
    }

    console.log(
      `\n🎉 Workflow complete! Processed ${meetingsProcessed} meetings`
    );
  }

  async runAgent() {
    console.log("🚀 Starting Meeting Organizer Agent...");
    console.log("📋 This agent will:");
    console.log("  1. Search Gmail for meeting-related emails");
    console.log("  2. Extract meeting details from email content");
    console.log("  3. Add meeting info to Google Sheets");
    console.log("  4. Create preparation tasks in Asana");
    console.log();

    try {
      await this.processEmailsForMeetings();
    } catch (error) {
      console.error("❌ Agent failed:", error.message);
      console.log("Check your integrations and API connections");
    }
  }
}

// Usage
if (require.main === module) {
  const agent = new MeetingOrganizerAgent();
  agent.runAgent();
}

module.exports = MeetingOrganizerAgent;
```

## Step 5: Run Your Agent

### Python

```bash
python meeting_organizer_agent.py
```

### JavaScript

```bash
node meetingOrganizerAgent.js
```

## Expected Output

```
🚀 Starting Meeting Organizer Agent...
📋 This agent will:
  1. Search Gmail for meeting-related emails
  2. Extract meeting details from email content
  3. Add meeting info to Google Sheets
  4. Create preparation tasks in Asana

🔍 Searching for meeting-related emails...
📧 Found 3 emails to process

📨 Processing: Weekly Team Standup
✅ Meeting added to Google Sheets
✅ Task created in Asana
✅ Meeting organized: Weekly Team Standup

📨 Processing: Client Discovery Call
✅ Meeting added to Google Sheets
✅ Task created in Asana
✅ Meeting organized: Client Discovery Call

🎉 Workflow complete! Processed 2 meetings
```

## Customization Ideas

### 1. Enhanced Email Parsing

```python
def advanced_meeting_extraction(email_content):
    # Use AI for better extraction
    extraction_function = {
        "name": "extract_meeting_info",
        "description": "Extract structured meeting information from email text",
        "parameters": {
            "type": "object",
            "properties": {
                "email_text": {"type": "string"}
            }
        }
    }
    # Implement AI-powered extraction
```

### 2. Smart Scheduling

```python
def check_calendar_conflicts(meeting_date, meeting_time):
    # Check Google Calendar for conflicts
    # Suggest alternative times
    # Send notifications about conflicts
    pass
```

### 3. Automated Follow-ups

```python
def setup_meeting_reminders(meeting_details):
    # Create calendar events
    # Set up email reminders
    # Schedule preparation tasks
    pass
```

## Troubleshooting

### Common Issues

1. **Gmail Search Not Working**

   - Verify OAuth connection
   - Check search query syntax
   - Ensure proper permissions

2. **Sheets Access Denied**

   - Verify spreadsheet ID
   - Check sharing permissions
   - Confirm OAuth scopes

3. **Asana Task Creation Failed**
   - Verify project ID
   - Check API key permissions
   - Confirm workspace access

### Debug Mode

Add debug logging to troubleshoot issues:

```python
import logging

logging.basicConfig(level=logging.DEBUG)

def debug_integrations():
    # Test each integration separately
    test_gmail_connection()
    test_sheets_access()
    test_asana_connection()
```

## Next Steps

🎉 Congratulations! You've built your first multi-integration AI agent. Here's what to explore next:

1. **[Multi-Integration Examples](../basic-examples/multi-integration/)** - More complex workflows
2. **[Real-World Use Cases](../use-cases/)** - Industry-specific examples
3. **[Advanced Patterns](../advanced/)** - Error handling, optimization, and best practices

Your agent demonstrates the core concepts of the Incredible API:

- ✅ Function calling for custom logic
- ✅ Multi-integration workflows
- ✅ Data extraction and transformation
- ✅ Cross-platform automation

Ready to build something even more powerful? Check out our [advanced use cases](../use-cases/) for inspiration!
