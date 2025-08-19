# Meeting Manager Agent

An intelligent agent that extracts meeting details from Gmail, schedules them in Google Calendar, and creates follow-up tasks in Asana.

## 📋 **Workflow Overview**

```
📧 Gmail → 📅 Google Calendar → 📋 Asana
  Extract      Schedule         Tasks
```

**Apps Used:** Gmail + Google Calendar + Asana (3 apps total)

## 🎯 **What This Agent Does**

1. **📧 Extract**: Scans Gmail for meeting-related emails using AI
2. **📅 Schedule**: Automatically creates calendar events with parsed details
3. **📋 Tasks**: Generates preparation and follow-up tasks in Asana

## 🛠 **Prerequisites**

- Incredible API access with function calling enabled
- Connected integrations:
  - Gmail (OAuth)
  - Google Calendar (OAuth)
  - Asana (API key or OAuth)

## 📋 **Setup**

### Environment Configuration

```bash
# .env
INCREDIBLE_API_KEY=your_incredible_api_key
INCREDIBLE_BASE_URL=https://api.incredible.one
USER_ID=your_user_id

# Integration Settings
ASANA_PROJECT_ID=your_asana_project_id
CALENDAR_ID=primary  # or specific calendar ID

# Notification Settings
NOTIFICATION_EMAIL=your-assistant@company.com
```

## 💻 **Implementation**

<div class="code-tabs" data-section="meeting-manager">
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

class MeetingManager:
def **init**(self):
self.api_key = os.getenv('INCREDIBLE_API_KEY')
self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
self.user_id = os.getenv('USER_ID')
self.asana_project_id = os.getenv('ASANA_PROJECT_ID')
self.calendar_id = os.getenv('CALENDAR_ID', 'primary')

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def scan_emails_for_meetings(self, hours_back=24):
        """Scan recent emails for meeting invitations and requests"""
        print(f"📧 Scanning emails from last {hours_back} hours...")

        # Gmail search queries for meeting-related emails
        meeting_queries = [
            "subject:(meeting OR call OR conference OR zoom)",
            "subject:(schedule OR appointment OR invite)",
            "\"let's meet\" OR \"meeting request\" OR \"calendar invite\"",
            "\"join the meeting\" OR \"zoom link\" OR \"teams meeting\""
        ]

        all_meetings = []

        for query in meeting_queries:
            meetings = self.search_gmail(f"{query} newer_than:{hours_back}h")
            all_meetings.extend(meetings)

        # Remove duplicates based on message ID
        unique_meetings = {email['id']: email for email in all_meetings}.values()

        print(f"📨 Found {len(unique_meetings)} potential meeting emails")
        return list(unique_meetings)

    def search_gmail(self, query):
        """Search Gmail using the Incredible API"""
        url = f"{self.base_url}/v1/integrations/gmail/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "gmail_search",
            "inputs": {
                "query": query,
                "max_results": 20
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

    def extract_meeting_details(self, email):
        """Extract meeting details from email content using AI"""
        content = f"""

Subject: {email.get('subject', '')}
From: {email.get('sender', '')}
Content: {email.get('content', '')}
"""

        # Use AI to extract meeting details
        extraction_function = {
            "name": "extract_meeting_info",
            "description": "Extract meeting details from email content",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Meeting title"},
                    "date": {"type": "string", "description": "Meeting date (YYYY-MM-DD)"},
                    "time": {"type": "string", "description": "Meeting time (HH:MM)"},
                    "duration": {"type": "integer", "description": "Duration in minutes"},
                    "attendees": {"type": "array", "items": {"type": "string"}},
                    "location": {"type": "string", "description": "Meeting location or link"},
                    "agenda": {"type": "string", "description": "Meeting agenda or purpose"}
                },
                "required": ["title"]
            }
        }

        data = {
            "model": "incredible-agent",
            "user_id": self.user_id,
            "messages": [
                {
                    "role": "user",
                    "content": f"Extract meeting details from this email: {content}"
                }
            ],
            "functions": [extraction_function],
            "stream": False
        }

        try:
            response = requests.post(
                f"{self.base_url}/v1/chat-completion",
                headers=self.headers,
                json=data
            )

            if response.status_code == 200:
                result = response.json()

                # Process AI response
                if 'result' in result and 'response' in result['result']:
                    for item in result['result']['response']:
                        if item['type'] == 'function_call':
                            return item['function_call']['arguments']

                # Fallback: manual extraction
                return self.manual_extract_details(email)

        except Exception as e:
            print(f"❌ AI extraction failed: {e}")
            return self.manual_extract_details(email)

    def manual_extract_details(self, email):
        """Fallback manual extraction of meeting details"""
        subject = email.get('subject', '')
        content = email.get('content', '')

        # Extract basic details using regex
        title = subject or "Meeting"

        # Simple date extraction
        date_patterns = [
            r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b',  # MM/DD/YYYY
            r'\b(\d{4})-(\d{1,2})-(\d{1,2})\b',  # YYYY-MM-DD
        ]

        date = None
        for pattern in date_patterns:
            match = re.search(pattern, content)
            if match:
                if len(match.groups()) == 3:
                    if '/' in pattern:
                        month, day, year = match.groups()
                        date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    else:
                        year, month, day = match.groups()
                        date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                break

        return {
            "title": title,
            "date": date or (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "time": "10:00",  # Default time
            "duration": 60,   # Default duration
            "attendees": [email.get('sender', '')],
            "location": "TBD",
            "agenda": content[:200] + "..." if len(content) > 200 else content
        }

    def create_calendar_event(self, meeting_details):
        """Create calendar event using Google Calendar integration"""
        print(f"📅 Creating calendar event: {meeting_details['title']}")

        # Prepare calendar event data
        start_datetime = f"{meeting_details['date']}T{meeting_details['time']}:00"
        end_time = datetime.fromisoformat(start_datetime) + timedelta(minutes=meeting_details.get('duration', 60))

        url = f"{self.base_url}/v1/integrations/google_calendar/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "create_event",
            "inputs": {
                "calendar_id": self.calendar_id,
                "summary": meeting_details['title'],
                "description": meeting_details.get('agenda', ''),
                "start": {
                    "dateTime": start_datetime,
                    "timeZone": "America/New_York"
                },
                "end": {
                    "dateTime": end_time.isoformat(),
                    "timeZone": "America/New_York"
                },
                "location": meeting_details.get('location', ''),
                "attendees": [{"email": email} for email in meeting_details.get('attendees', [])]
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                result = response.json()
                event_id = result.get('result', {}).get('id')
                print(f"✅ Calendar event created: {event_id}")
                return event_id
            else:
                print(f"❌ Calendar creation failed: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Calendar error: {e}")
            return None

    def create_asana_tasks(self, meeting_details, event_id=None):
        """Create preparation and follow-up tasks in Asana"""
        print(f"📋 Creating Asana tasks for: {meeting_details['title']}")

        tasks_created = []

        # Preparation task
        prep_task = {
            "name": f"Prepare for: {meeting_details['title']}",
            "notes": f"""

Meeting Preparation Checklist:

📅 Meeting: {meeting_details['title']}
🗓 Date: {meeting_details['date']} at {meeting_details['time']}
📍 Location: {meeting_details.get('location', 'TBD')}

Agenda:
{meeting_details.get('agenda', 'No agenda provided')}

Action Items:
□ Review agenda and prepare talking points
□ Gather necessary documents
□ Test technology (if virtual meeting)
□ Prepare questions and discussion topics
""",
"due_on": meeting_details['date'],
"projects": [self.asana_project_id]
}

        prep_task_id = self.create_asana_task(prep_task)
        if prep_task_id:
            tasks_created.append(prep_task_id)

        # Follow-up task (due day after meeting)
        follow_up_date = (datetime.strptime(meeting_details['date'], "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

        follow_up_task = {
            "name": f"Follow-up: {meeting_details['title']}",
            "notes": f"""

Meeting Follow-up Actions:

📅 Meeting: {meeting_details['title']}
🗓 Held on: {meeting_details['date']}

Action Items:
□ Send meeting notes to attendees
□ Follow up on action items
□ Schedule next meeting if needed
□ Update project status

{f'📅 Calendar Event: {event_id}' if event_id else ''}
""",
"due_on": follow_up_date,
"projects": [self.asana_project_id]
}

        follow_up_task_id = self.create_asana_task(follow_up_task)
        if follow_up_task_id:
            tasks_created.append(follow_up_task_id)

        print(f"✅ Created {len(tasks_created)} Asana tasks")
        return tasks_created

    def create_asana_task(self, task_data):
        """Create a single task in Asana"""
        url = f"{self.base_url}/v1/integrations/asana/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "create_task",
            "inputs": task_data
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get('result', {}).get('gid')
            else:
                print(f"❌ Asana task creation failed: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Asana error: {e}")
            return None

    def process_meeting(self, email):
        """Process a single meeting email through the complete workflow"""
        print(f"\n🔄 Processing: {email.get('subject', 'No Subject')}")

        # Step 1: Extract meeting details
        meeting_details = self.extract_meeting_details(email)

        if not meeting_details or not meeting_details.get('title'):
            print("❌ Could not extract meeting details")
            return False

        print(f"   📋 Title: {meeting_details['title']}")
        print(f"   📅 Date: {meeting_details.get('date', 'TBD')}")
        print(f"   ⏰ Time: {meeting_details.get('time', 'TBD')}")

        # Step 2: Create calendar event
        event_id = self.create_calendar_event(meeting_details)

        # Step 3: Create Asana tasks
        task_ids = self.create_asana_tasks(meeting_details, event_id)

        success = event_id is not None and len(task_ids) > 0
        print(f"   {'✅' if success else '❌'} Meeting processing {'completed' if success else 'failed'}")

        return success

    def run_meeting_workflow(self, hours_back=24):
        """Execute the complete meeting management workflow"""
        print("🚀 Starting Meeting Manager Workflow")
        print(f"📊 Project ID: {self.asana_project_id}")
        print(f"📅 Calendar: {self.calendar_id}")
        print()

        # Step 1: Scan for meeting emails
        emails = self.scan_emails_for_meetings(hours_back)

        if not emails:
            print("✅ No new meeting emails found")
            return

        # Step 2: Process each meeting
        successful_meetings = 0
        for email in emails:
            if self.process_meeting(email):
                successful_meetings += 1

        # Step 3: Summary
        print(f"\n🎉 Meeting Workflow Complete!")
        print(f"📧 Emails processed: {len(emails)}")
        print(f"✅ Meetings scheduled: {successful_meetings}")

        if successful_meetings > 0:
            print(f"📅 View calendar: https://calendar.google.com")
            print(f"📋 View tasks: https://app.asana.com/0/{self.asana_project_id}")

# Usage Examples

if **name** == "**main**":
manager = MeetingManager()

    # Run daily meeting processing
    manager.run_meeting_workflow(hours_back=24)

    print("\n" + "="*50 + "\n")

    # Run weekly catch-up (process last 7 days)
    manager.run_meeting_workflow(hours_back=168)  # 7 days * 24 hours</code></pre>

  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">const axios = require("axios");
require("dotenv").config();

class MeetingManager {
constructor() {
this.apiKey = process.env.INCREDIBLE_API_KEY;
this.baseUrl = process.env.INCREDIBLE_BASE_URL || "https://api.incredible.one";
this.userId = process.env.USER_ID;
this.asanaProjectId = process.env.ASANA_PROJECT_ID;
this.calendarId = process.env.CALENDAR_ID || "primary";

    this.headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${this.apiKey}`,
    };

}

async scanEmailsForMeetings(hoursBack = 24) {
console.log(`📧 Scanning emails from last ${hoursBack} hours...`);

    const meetingQueries = [
      "subject:(meeting OR call OR conference OR zoom)",
      "subject:(schedule OR appointment OR invite)",
      '"let\'s meet" OR "meeting request" OR "calendar invite"',
      '"join the meeting" OR "zoom link" OR "teams meeting"'
    ];

    const allMeetings = [];

    for (const query of meetingQueries) {
      const meetings = await this.searchGmail(`${query} newer_than:${hoursBack}h`);
      allMeetings.push(...meetings);
    }

    // Remove duplicates based on message ID
    const uniqueMeetings = Array.from(
      new Map(allMeetings.map(email => [email.id, email])).values()
    );

    console.log(`📨 Found ${uniqueMeetings.length} potential meeting emails`);
    return uniqueMeetings;

}

async searchGmail(query) {
const url = `${this.baseUrl}/v1/integrations/gmail/execute`;

    const data = {
      user_id: this.userId,
      feature_name: "gmail_search",
      inputs: {
        query: query,
        max_results: 20
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

async extractMeetingDetails(email) {
const content = `Subject: ${email.subject || ''}
From: ${email.sender || ''}
Content: ${email.content || ''}`;

    const extractionFunction = {
      name: "extract_meeting_info",
      description: "Extract meeting details from email content",
      parameters: {
        type: "object",
        properties: {
          title: { type: "string", description: "Meeting title" },
          date: { type: "string", description: "Meeting date (YYYY-MM-DD)" },
          time: { type: "string", description: "Meeting time (HH:MM)" },
          duration: { type: "integer", description: "Duration in minutes" },
          attendees: { type: "array", items: { type: "string" } },
          location: { type: "string", description: "Meeting location or link" },
          agenda: { type: "string", description: "Meeting agenda or purpose" }
        },
        required: ["title"]
      }
    };

    const data = {
      model: "incredible-agent",
      user_id: this.userId,
      messages: [
        {
          role: "user",
          content: `Extract meeting details from this email: ${content}`
        }
      ],
      functions: [extractionFunction],
      stream: false
    };

    try {
      const response = await axios.post(
        `${this.baseUrl}/v1/chat-completion`,
        data,
        { headers: this.headers }
      );

      if (response.status === 200) {
        const result = response.data;

        if (result.result && result.result.response) {
          for (const item of result.result.response) {
            if (item.type === 'function_call') {
              return item.function_call.arguments;
            }
          }
        }

        return this.manualExtractDetails(email);
      }
    } catch (error) {
      console.log(`❌ AI extraction failed: ${error.message}`);
      return this.manualExtractDetails(email);
    }

}

manualExtractDetails(email) {
const subject = email.subject || '';
const content = email.content || '';

    const title = subject || "Meeting";

    // Simple date extraction
    const datePatterns = [
      /\b(\d{1,2})\/(\d{1,2})\/(\d{4})\b/,  // MM/DD/YYYY
      /\b(\d{4})-(\d{1,2})-(\d{1,2})\b/,   // YYYY-MM-DD
    ];

    let date = null;
    for (const pattern of datePatterns) {
      const match = content.match(pattern);
      if (match) {
        if (pattern.source.includes('/')) {
          const [, month, day, year] = match;
          date = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
        } else {
          const [, year, month, day] = match;
          date = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
        }
        break;
      }
    }

    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);

    return {
      title: title,
      date: date || tomorrow.toISOString().split('T')[0],
      time: "10:00",
      duration: 60,
      attendees: [email.sender || ''],
      location: "TBD",
      agenda: content.length > 200 ? content.substring(0, 200) + "..." : content
    };

}

async createCalendarEvent(meetingDetails) {
console.log(`📅 Creating calendar event: ${meetingDetails.title}`);

    const startDateTime = `${meetingDetails.date}T${meetingDetails.time}:00`;
    const endTime = new Date(startDateTime);
    endTime.setMinutes(endTime.getMinutes() + (meetingDetails.duration || 60));

    const url = `${this.baseUrl}/v1/integrations/google_calendar/execute`;

    const data = {
      user_id: this.userId,
      feature_name: "create_event",
      inputs: {
        calendar_id: this.calendarId,
        summary: meetingDetails.title,
        description: meetingDetails.agenda || '',
        start: {
          dateTime: startDateTime,
          timeZone: "America/New_York"
        },
        end: {
          dateTime: endTime.toISOString(),
          timeZone: "America/New_York"
        },
        location: meetingDetails.location || '',
        attendees: (meetingDetails.attendees || []).map(email => ({ email }))
      }
    };

    try {
      const response = await axios.post(url, data, { headers: this.headers });
      if (response.status === 200) {
        const eventId = response.data.result?.id;
        console.log(`✅ Calendar event created: ${eventId}`);
        return eventId;
      } else {
        console.log(`❌ Calendar creation failed: ${response.data}`);
        return null;
      }
    } catch (error) {
      console.log(`❌ Calendar error: ${error.message}`);
      return null;
    }

}

async createAsanaTasks(meetingDetails, eventId = null) {
console.log(`📋 Creating Asana tasks for: ${meetingDetails.title}`);

    const tasksCreated = [];

    // Preparation task
    const prepTask = {
      name: `Prepare for: ${meetingDetails.title}`,
      notes: `

Meeting Preparation Checklist:

📅 Meeting: ${meetingDetails.title}
🗓 Date: ${meetingDetails.date} at ${meetingDetails.time}
📍 Location: ${meetingDetails.location || 'TBD'}

Agenda:
${meetingDetails.agenda || 'No agenda provided'}

Action Items:
□ Review agenda and prepare talking points
□ Gather necessary documents
□ Test technology (if virtual meeting)
□ Prepare questions and discussion topics
`,
due_on: meetingDetails.date,
projects: [this.asanaProjectId]
};

    const prepTaskId = await this.createAsanaTask(prepTask);
    if (prepTaskId) {
      tasksCreated.push(prepTaskId);
    }

    // Follow-up task
    const meetingDate = new Date(meetingDetails.date);
    meetingDate.setDate(meetingDate.getDate() + 1);
    const followUpDate = meetingDate.toISOString().split('T')[0];

    const followUpTask = {
      name: `Follow-up: ${meetingDetails.title}`,
      notes: `

Meeting Follow-up Actions:

📅 Meeting: ${meetingDetails.title}
🗓 Held on: ${meetingDetails.date}

Action Items:
□ Send meeting notes to attendees
□ Follow up on action items
□ Schedule next meeting if needed
□ Update project status

${eventId ? `📅 Calendar Event: ${eventId}` : ''}
`,
due_on: followUpDate,
projects: [this.asanaProjectId]
};

    const followUpTaskId = await this.createAsanaTask(followUpTask);
    if (followUpTaskId) {
      tasksCreated.push(followUpTaskId);
    }

    console.log(`✅ Created ${tasksCreated.length} Asana tasks`);
    return tasksCreated;

}

async createAsanaTask(taskData) {
const url = `${this.baseUrl}/v1/integrations/asana/execute`;

    const data = {
      user_id: this.userId,
      feature_name: "create_task",
      inputs: taskData
    };

    try {
      const response = await axios.post(url, data, { headers: this.headers });
      if (response.status === 200) {
        return response.data.result?.gid;
      } else {
        console.log(`❌ Asana task creation failed: ${response.data}`);
        return null;
      }
    } catch (error) {
      console.log(`❌ Asana error: ${error.message}`);
      return null;
    }

}

async processMeeting(email) {
console.log(`\n🔄 Processing: ${email.subject || 'No Subject'}`);

    // Step 1: Extract meeting details
    const meetingDetails = await this.extractMeetingDetails(email);

    if (!meetingDetails || !meetingDetails.title) {
      console.log("❌ Could not extract meeting details");
      return false;
    }

    console.log(`   📋 Title: ${meetingDetails.title}`);
    console.log(`   📅 Date: ${meetingDetails.date || 'TBD'}`);
    console.log(`   ⏰ Time: ${meetingDetails.time || 'TBD'}`);

    // Step 2: Create calendar event
    const eventId = await this.createCalendarEvent(meetingDetails);

    // Step 3: Create Asana tasks
    const taskIds = await this.createAsanaTasks(meetingDetails, eventId);

    const success = eventId !== null && taskIds.length > 0;
    console.log(`   ${success ? '✅' : '❌'} Meeting processing ${success ? 'completed' : 'failed'}`);

    return success;

}

async runMeetingWorkflow(hoursBack = 24) {
console.log("🚀 Starting Meeting Manager Workflow");
console.log(`📊 Project ID: ${this.asanaProjectId}`);
console.log(`📅 Calendar: ${this.calendarId}`);
console.log();

    // Step 1: Scan for meeting emails
    const emails = await this.scanEmailsForMeetings(hoursBack);

    if (emails.length === 0) {
      console.log("✅ No new meeting emails found");
      return;
    }

    // Step 2: Process each meeting
    let successfulMeetings = 0;
    for (const email of emails) {
      if (await this.processMeeting(email)) {
        successfulMeetings++;
      }
    }

    // Step 3: Summary
    console.log(`\n🎉 Meeting Workflow Complete!`);
    console.log(`📧 Emails processed: ${emails.length}`);
    console.log(`✅ Meetings scheduled: ${successfulMeetings}`);

    if (successfulMeetings > 0) {
      console.log(`📅 View calendar: https://calendar.google.com`);
      console.log(`📋 View tasks: https://app.asana.com/0/${this.asanaProjectId}`);
    }

}
}

// Usage Examples
async function main() {
const manager = new MeetingManager();

// Run daily meeting processing
await manager.runMeetingWorkflow(24);

console.log("\n" + "=".repeat(50) + "\n");

// Run weekly catch-up (process last 7 days)
await manager.runMeetingWorkflow(168); // 7 days \* 24 hours
}

if (require.main === module) {
main().catch(console.error);
}

module.exports = MeetingManager;</code></pre>

  </div>
</div>

## 🎯 **Usage Examples**

### Daily Automated Processing

```bash
# Run every morning to process yesterday's emails
python meeting_manager.py --hours 24
```

### Weekly Catch-up

```bash
# Process the entire week's emails
node meetingManager.js --hours 168
```

### Custom Time Range

```bash
# Process last 3 days
python meeting_manager.py --hours 72
```

## 📊 **Expected Output**

```
🚀 Starting Meeting Manager Workflow
📊 Project ID: 1234567890123456
📅 Calendar: primary

📧 Scanning emails from last 24 hours...
📨 Found 3 potential meeting emails

🔄 Processing: Weekly Team Standup
   📋 Title: Weekly Team Standup
   📅 Date: 2024-01-15
   ⏰ Time: 10:00
📅 Creating calendar event: Weekly Team Standup
✅ Calendar event created: event_abc123
📋 Creating Asana tasks for: Weekly Team Standup
✅ Created 2 Asana tasks
   ✅ Meeting processing completed

🔄 Processing: Client Discovery Call - ABC Corp
   📋 Title: Client Discovery Call - ABC Corp
   📅 Date: 2024-01-16
   ⏰ Time: 14:00
📅 Creating calendar event: Client Discovery Call - ABC Corp
✅ Calendar event created: event_def456
📋 Creating Asana tasks for: Client Discovery Call - ABC Corp
✅ Created 2 Asana tasks
   ✅ Meeting processing completed

🎉 Meeting Workflow Complete!
📧 Emails processed: 3
✅ Meetings scheduled: 2
📅 View calendar: https://calendar.google.com
📋 View tasks: https://app.asana.com/0/1234567890123456
```

## 🔧 **Customization Options**

### Meeting Types

- **👥 Team Meetings**: Regular standup and sync calls
- **🎯 Client Calls**: Customer discovery and project meetings
- **🔬 Interviews**: Candidate screening and hiring
- **📈 Reviews**: Performance and project review meetings

### Task Templates

- **📋 Preparation Tasks**: Customizable checklists for meeting prep
- **📝 Follow-up Tasks**: Automated post-meeting action items
- **📊 Recurring Meetings**: Templates for regular team meetings

### Calendar Integration

- **📅 Multiple Calendars**: Support for work, personal, team calendars
- **⏰ Smart Scheduling**: Conflict detection and suggestion
- **🔔 Notifications**: Automated reminders and updates

## 🛡 **Best Practices**

1. **📧 Email Filters**: Use specific keywords to identify meeting emails
2. **🕒 Regular Processing**: Run hourly or daily for timely scheduling
3. **📋 Task Organization**: Use project-specific Asana boards
4. **🔒 Permission Management**: Ensure proper calendar and task access

## 🚀 **Advanced Features**

### AI-Powered Scheduling

- **🤖 Smart Conflict Resolution**: Automatically suggest alternative times
- **📊 Meeting Analytics**: Track meeting frequency and patterns
- **🎯 Priority Assessment**: Prioritize meetings based on content analysis

### Integration Enhancements

- **💬 Slack Notifications**: Real-time updates to team channels
- **📱 Mobile Sync**: Push notifications to mobile devices
- **📈 Reporting**: Weekly/monthly meeting summaries

---

_This meeting manager eliminates the manual work of scheduling and task creation, ensuring no meeting gets missed and all follow-ups are tracked._
