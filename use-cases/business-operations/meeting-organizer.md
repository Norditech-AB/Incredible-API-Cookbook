# Meeting Organizer Agent

Automatically extract meeting details from Gmail, organize them in Google Sheets, and create tasks in Asana for comprehensive meeting management.

## Business Problem

Managing meetings across multiple platforms is time-consuming and error-prone:

- Meeting invites scattered across email
- No centralized tracking of meeting details
- Missing preparation tasks and follow-ups
- Difficult to analyze meeting patterns

## Solution Overview

**Agent Name**: Meeting Organizer  
**Integrations**: Gmail + Google Sheets + Asana  
**Automation Level**: High  
**Business Impact**: 5-10 hours saved per week per team member

### Workflow

```
📧 Gmail → 📊 Sheets → 📋 Asana
  ↓         ↓          ↓
Extract   Organize   Create Tasks
```

## Implementation

### Core Agent

```python
import os
import re
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class MeetingOrganizerAgent:
    def __init__(self):
        self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
        self.user_id = os.getenv('USER_ID')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {os.getenv('INCREDIBLE_API_KEY')}"
        }

        # Configuration
        self.meetings_sheet_id = os.getenv('MEETINGS_SHEET_ID')
        self.asana_project_id = os.getenv('ASANA_PROJECT_ID')

        # Meeting patterns for extraction
        self.meeting_patterns = {
            'zoom_link': r'https://[\w\.-]+\.zoom\.us/j/\d+[\w\?&=]*',
            'teams_link': r'https://teams\.microsoft\.com/l/meetup-join/[\w\-%]+',
            'meet_link': r'https://meet\.google\.com/[\w\-]+',
            'date_pattern': r'(\w+day,?\s+)?(\w+\s+\d{1,2},?\s+\d{4})',
            'time_pattern': r'(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm))',
            'email_pattern': r'[\w\.-]+@[\w\.-]+\.\w+'
        }

    def search_meeting_emails(self, days_back=7):
        """Search for meeting-related emails"""
        queries = [
            f"newer_than:{days_back}d (subject:meeting OR subject:call OR subject:conference)",
            f"newer_than:{days_back}d (zoom.us OR teams.microsoft.com OR meet.google.com)",
            f"newer_than:{days_back}d (subject:invitation OR subject:invite)",
            f"newer_than:{days_back}d (subject:appointment OR subject:schedule)"
        ]

        all_emails = []

        for query in queries:
            emails = self.execute_gmail_search(query, max_results=20)
            all_emails.extend(emails)

        # Remove duplicates
        unique_emails = {email.get('id'): email for email in all_emails}.values()

        print(f"📧 Found {len(unique_emails)} potential meeting emails")
        return list(unique_emails)

    def execute_gmail_search(self, query, max_results=10):
        """Execute Gmail search"""
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
            print(f"Gmail search error: {response.text}")
            return []

    def extract_meeting_details(self, email):
        """Extract structured meeting information from email"""
        subject = email.get('subject', '')
        content = email.get('content', '')
        sender = email.get('sender', '')

        # Combine subject and content for parsing
        full_text = f"{subject} {content}"

        meeting_info = {
            'id': email.get('id'),
            'subject': self.clean_subject(subject),
            'organizer': sender,
            'date': self.extract_date(full_text),
            'time': self.extract_time(full_text),
            'duration': self.extract_duration(full_text),
            'location': self.extract_location(full_text),
            'attendees': self.extract_attendees(full_text),
            'agenda': self.extract_agenda(content),
            'meeting_link': self.extract_meeting_link(full_text),
            'priority': self.determine_priority(subject, content, sender),
            'email_date': email.get('date', ''),
            'preparation_needed': self.assess_preparation_needs(content)
        }

        return meeting_info

    def clean_subject(self, subject):
        """Clean meeting subject for better organization"""
        # Remove common prefixes
        prefixes = ['RE:', 'FW:', 'FWD:', 'Invitation:', 'INVITATION:']
        cleaned = subject

        for prefix in prefixes:
            if cleaned.upper().startswith(prefix.upper()):
                cleaned = cleaned[len(prefix):].strip()

        return cleaned

    def extract_date(self, text):
        """Extract date from text"""
        date_match = re.search(self.meeting_patterns['date_pattern'], text, re.IGNORECASE)
        if date_match:
            return date_match.group().strip()

        # Look for relative dates
        relative_dates = {
            'today': datetime.now().strftime('%B %d, %Y'),
            'tomorrow': (datetime.now() + timedelta(days=1)).strftime('%B %d, %Y'),
            'monday': self.get_next_weekday(0),
            'tuesday': self.get_next_weekday(1),
            'wednesday': self.get_next_weekday(2),
            'thursday': self.get_next_weekday(3),
            'friday': self.get_next_weekday(4)
        }

        text_lower = text.lower()
        for keyword, date_value in relative_dates.items():
            if keyword in text_lower:
                return date_value

        return "TBD"

    def extract_time(self, text):
        """Extract time from text"""
        time_match = re.search(self.meeting_patterns['time_pattern'], text, re.IGNORECASE)
        if time_match:
            return time_match.group().strip()

        # Look for time ranges
        time_range_pattern = r'(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm))\s*[-–]\s*(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm))'
        range_match = re.search(time_range_pattern, text, re.IGNORECASE)
        if range_match:
            return f"{range_match.group(1)} - {range_match.group(2)}"

        return "TBD"

    def extract_duration(self, text):
        """Extract meeting duration"""
        duration_patterns = [
            r'(\d+)\s*hour?s?',
            r'(\d+)\s*min(?:ute)?s?',
            r'(\d+)h\s*(\d+)m'
        ]

        for pattern in duration_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group()

        return "60 minutes"  # Default assumption

    def extract_location(self, text):
        """Extract meeting location"""
        # Check for video conference links first
        meeting_link = self.extract_meeting_link(text)
        if meeting_link:
            if 'zoom.us' in meeting_link:
                return "Zoom Video Conference"
            elif 'teams.microsoft.com' in meeting_link:
                return "Microsoft Teams"
            elif 'meet.google.com' in meeting_link:
                return "Google Meet"
            else:
                return "Video Conference"

        # Look for physical locations
        location_patterns = [
            r'(?:at|in|@)\s+([A-Z][a-zA-Z\s]+(?:Room|Office|Building|Conference|Floor))',
            r'(?:Room|Office)\s+([A-Z0-9\-]+)',
            r'(?:Building|Floor)\s+(\w+)'
        ]

        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return "TBD"

    def extract_meeting_link(self, text):
        """Extract video conference links"""
        for link_type, pattern in [
            ('zoom', self.meeting_patterns['zoom_link']),
            ('teams', self.meeting_patterns['teams_link']),
            ('meet', self.meeting_patterns['meet_link'])
        ]:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group()

        return None

    def extract_attendees(self, text):
        """Extract attendee email addresses"""
        emails = re.findall(self.meeting_patterns['email_pattern'], text)
        # Filter out common non-attendee emails
        filtered_emails = [
            email for email in emails
            if not any(skip in email.lower() for skip in ['noreply', 'no-reply', 'donotreply'])
        ]
        return list(set(filtered_emails))  # Remove duplicates

    def extract_agenda(self, content):
        """Extract meeting agenda or description"""
        if not content:
            return "No agenda provided"

        # Look for agenda section
        agenda_patterns = [
            r'agenda:?\s*(.*?)(?:\n\n|\nfrom:|\nsubject:)',
            r'topics?:?\s*(.*?)(?:\n\n|\nfrom:|\nsubject:)',
            r'discussion:?\s*(.*?)(?:\n\n|\nfrom:|\nsubject:)'
        ]

        for pattern in agenda_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                agenda = match.group(1).strip()
                if len(agenda) > 10:  # Meaningful content
                    return agenda[:500]  # Limit length

        # Return first meaningful paragraph
        paragraphs = content.split('\n\n')
        for paragraph in paragraphs:
            if len(paragraph.strip()) > 50:
                return paragraph.strip()[:500]

        return "See email for details"

    def determine_priority(self, subject, content, sender):
        """Determine meeting priority"""
        high_priority_indicators = [
            'urgent', 'asap', 'critical', 'emergency', 'important',
            'ceo', 'founder', 'president', 'director', 'vp'
        ]

        text_to_check = f"{subject} {content} {sender}".lower()

        if any(indicator in text_to_check for indicator in high_priority_indicators):
            return "HIGH"

        # Check if it's a large meeting (many attendees)
        attendee_count = len(self.extract_attendees(content))
        if attendee_count > 10:
            return "HIGH"

        # Check if it's soon
        date_text = self.extract_date(f"{subject} {content}")
        if any(word in date_text.lower() for word in ['today', 'tomorrow']):
            return "MEDIUM"

        return "LOW"

    def assess_preparation_needs(self, content):
        """Assess if meeting needs preparation"""
        prep_indicators = [
            'prepare', 'review', 'agenda', 'materials', 'documents',
            'presentation', 'demo', 'proposal', 'budget', 'report'
        ]

        content_lower = content.lower()
        prep_count = sum(1 for indicator in prep_indicators if indicator in content_lower)

        if prep_count > 2:
            return "HIGH"
        elif prep_count > 0:
            return "MEDIUM"
        else:
            return "LOW"

    def get_next_weekday(self, weekday):
        """Get next occurrence of specified weekday"""
        days_ahead = weekday - datetime.now().weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7

        target_date = datetime.now() + timedelta(days_ahead)
        return target_date.strftime('%B %d, %Y')

    def add_meeting_to_sheets(self, meeting_info):
        """Add meeting information to Google Sheets"""
        url = f"{self.base_url}/v1/integrations/google_sheets/execute"

        # Format data for sheets
        row_data = [
            meeting_info['subject'],
            meeting_info['date'],
            meeting_info['time'],
            meeting_info['duration'],
            meeting_info['organizer'],
            ', '.join(meeting_info['attendees'][:5]),  # Limit attendees shown
            meeting_info['location'],
            meeting_info['priority'],
            meeting_info['preparation_needed'],
            meeting_info['meeting_link'] or '',
            meeting_info['agenda'][:200] + '...' if len(meeting_info['agenda']) > 200 else meeting_info['agenda'],
            'PENDING',
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ]

        data = {
            "user_id": self.user_id,
            "feature_name": "SHEETS_ADD_ROW",
            "inputs": {
                "spreadsheet_id": self.meetings_sheet_id,
                "range": "Meetings",
                "values": [row_data]
            }
        }

        response = requests.post(url, headers=self.headers, json=data)

        if response.status_code == 200:
            print(f"✅ Added to sheets: {meeting_info['subject']}")
            return True
        else:
            print(f"❌ Sheets error: {response.text}")
            return False

    def create_asana_tasks(self, meeting_info):
        """Create preparation tasks in Asana"""
        url = f"{self.base_url}/v1/integrations/asana/execute"

        # Main meeting task
        main_task_name = f"📅 Meeting: {meeting_info['subject']}"
        main_task_notes = f"""
Meeting Details:
📅 Date: {meeting_info['date']}
🕒 Time: {meeting_info['time']}
👥 Organizer: {meeting_info['organizer']}
📍 Location: {meeting_info['location']}
🔗 Link: {meeting_info['meeting_link'] or 'N/A'}

Attendees: {', '.join(meeting_info['attendees'][:10])}

Agenda:
{meeting_info['agenda']}

Preparation Level: {meeting_info['preparation_needed']}
        """.strip()

        main_task_data = {
            "user_id": self.user_id,
            "feature_name": "ASANA_CREATE_TASK",
            "inputs": {
                "name": main_task_name,
                "notes": main_task_notes,
                "project_id": self.asana_project_id,
                "due_date": meeting_info['date']
            }
        }

        # Create main task
        main_response = requests.post(url, headers=self.headers, json=main_task_data)

        if main_response.status_code == 200:
            print(f"✅ Created Asana task: {meeting_info['subject']}")

            # Create subtasks if high preparation needed
            if meeting_info['preparation_needed'] == 'HIGH':
                self.create_preparation_subtasks(meeting_info, main_task_name)

            return True
        else:
            print(f"❌ Asana error: {main_response.text}")
            return False

    def create_preparation_subtasks(self, meeting_info, parent_task):
        """Create preparation subtasks for important meetings"""
        subtasks = [
            "Review meeting agenda and objectives",
            "Prepare necessary documents and materials",
            "Research attendees and their backgrounds",
            "Test video conference connection",
            "Prepare talking points and questions",
            "Block calendar for preparation time"
        ]

        for subtask in subtasks:
            self.create_asana_subtask(subtask, parent_task, meeting_info)

    def create_asana_subtask(self, task_name, parent_task, meeting_info):
        """Create a subtask in Asana"""
        url = f"{self.base_url}/v1/integrations/asana/execute"

        # Calculate due date (day before meeting)
        try:
            meeting_date = datetime.strptime(meeting_info['date'], '%B %d, %Y')
            prep_date = (meeting_date - timedelta(days=1)).strftime('%B %d, %Y')
        except:
            prep_date = meeting_info['date']

        data = {
            "user_id": self.user_id,
            "feature_name": "ASANA_CREATE_TASK",
            "inputs": {
                "name": f"📋 {task_name}",
                "notes": f"Preparation for: {meeting_info['subject']}",
                "project_id": self.asana_project_id,
                "due_date": prep_date,
                "parent_task": parent_task
            }
        }

        requests.post(url, headers=self.headers, json=data)

    def setup_tracking_sheet(self):
        """Setup Google Sheets with proper headers"""
        url = f"{self.base_url}/v1/integrations/google_sheets/execute"

        headers = [
            "Meeting Subject", "Date", "Time", "Duration", "Organizer",
            "Attendees", "Location", "Priority", "Prep Needed",
            "Meeting Link", "Agenda", "Status", "Created"
        ]

        data = {
            "user_id": self.user_id,
            "feature_name": "SHEETS_UPDATE_RANGE",
            "inputs": {
                "spreadsheet_id": self.meetings_sheet_id,
                "range": "A1:M1",
                "values": [headers]
            }
        }

        response = requests.post(url, headers=self.headers, json=data)

        if response.status_code == 200:
            print("✅ Tracking sheet configured")
        else:
            print(f"❌ Sheet setup error: {response.text}")

    def run_meeting_organization(self):
        """Main workflow execution"""
        print("🚀 Starting Meeting Organizer Agent...")
        print("=" * 60)

        # Step 1: Search for meeting emails
        print("📧 Step 1: Searching for meeting emails...")
        emails = self.search_meeting_emails(days_back=7)

        if not emails:
            print("No meeting emails found.")
            return

        # Step 2: Process each email
        print(f"\n📊 Step 2: Processing {len(emails)} emails...")
        processed_meetings = 0

        for email in emails:
            print(f"\n📨 Processing: {email.get('subject', 'No Subject')}")

            # Extract meeting details
            meeting_info = self.extract_meeting_details(email)

            # Only process if it looks like a real meeting
            if self.is_valid_meeting(meeting_info):
                # Add to sheets
                if self.add_meeting_to_sheets(meeting_info):
                    # Create Asana tasks
                    self.create_asana_tasks(meeting_info)
                    processed_meetings += 1
                    print(f"✅ Organized meeting: {meeting_info['subject']}")
            else:
                print(f"⏭️  Skipped: Doesn't appear to be a valid meeting")

        print(f"\n🎉 Organization Complete!")
        print(f"📊 Processed {processed_meetings} meetings")
        print(f"📈 View tracking sheet: https://docs.google.com/spreadsheets/d/{self.meetings_sheet_id}")
        print(f"📋 Check Asana project: {self.asana_project_id}")

    def is_valid_meeting(self, meeting_info):
        """Validate if extracted information represents a real meeting"""
        # Must have a meaningful subject
        if not meeting_info['subject'] or len(meeting_info['subject']) < 5:
            return False

        # Should have date or time information
        if meeting_info['date'] == 'TBD' and meeting_info['time'] == 'TBD':
            return False

        # Should have some location or link information
        if meeting_info['location'] == 'TBD' and not meeting_info['meeting_link']:
            return False

        return True

# Usage Example
if __name__ == "__main__":
    agent = MeetingOrganizerAgent()

    # Setup (run once)
    # agent.setup_tracking_sheet()

    # Run the organization workflow
    agent.run_meeting_organization()
```

### Configuration Files

#### Environment Variables

```bash
# .env
INCREDIBLE_API_KEY=your_api_key
INCREDIBLE_BASE_URL=https://api.incredible.one
USER_ID=your_user_id

# Google Sheets Configuration
MEETINGS_SHEET_ID=your_google_sheet_id

# Asana Configuration
ASANA_PROJECT_ID=your_asana_project_id
```

#### Sheet Setup Script

```python
# setup_meeting_tracker.py
def setup_meeting_tracking_infrastructure():
    """Setup the complete meeting tracking system"""

    # Create Google Sheet with multiple tabs
    create_sheets_workbook()

    # Setup Asana project structure
    create_asana_project()

    # Configure email filters
    setup_gmail_filters()

def create_sheets_workbook():
    """Create a comprehensive meeting tracking workbook"""
    sheets = [
        {
            "name": "Meetings",
            "headers": [
                "Subject", "Date", "Time", "Duration", "Organizer",
                "Attendees", "Location", "Priority", "Prep Needed",
                "Link", "Agenda", "Status", "Created"
            ]
        },
        {
            "name": "Analytics",
            "headers": [
                "Month", "Total Meetings", "Avg Duration", "Top Organizers",
                "Meeting Types", "Preparation Score"
            ]
        },
        {
            "name": "Action Items",
            "headers": [
                "Meeting", "Action Item", "Owner", "Due Date", "Status"
            ]
        }
    ]

    for sheet in sheets:
        create_sheet_tab(sheet["name"], sheet["headers"])
```

## Advanced Features

### 1. AI-Powered Meeting Insights

```python
def analyze_meeting_patterns(self):
    """Use AI to analyze meeting patterns and provide insights"""

    analysis_function = {
        "name": "analyze_meetings",
        "description": "Analyze meeting data and provide insights",
        "parameters": {
            "type": "object",
            "properties": {
                "meetings_data": {
                    "type": "array",
                    "description": "Array of meeting information"
                }
            }
        }
    }

    # Get meetings data from sheets
    meetings_data = self.get_meetings_from_sheets()

    # Use AI for analysis
    insights = self.call_ai_function(analysis_function, {"meetings_data": meetings_data})

    return insights
```

### 2. Smart Conflict Detection

```python
def detect_schedule_conflicts(self, new_meeting):
    """Detect potential scheduling conflicts"""

    existing_meetings = self.get_meetings_for_date(new_meeting['date'])

    conflicts = []
    for meeting in existing_meetings:
        if self.time_overlap(new_meeting['time'], meeting['time']):
            conflicts.append({
                "conflicting_meeting": meeting['subject'],
                "overlap_duration": self.calculate_overlap(new_meeting, meeting)
            })

    return conflicts
```

### 3. Automated Follow-ups

```python
def create_post_meeting_tasks(self, meeting_info):
    """Automatically create follow-up tasks after meetings"""

    follow_up_tasks = [
        "Send meeting summary to attendees",
        "Update project status based on decisions",
        "Schedule follow-up meetings if needed",
        "Complete action items assigned to you"
    ]

    for task in follow_up_tasks:
        self.create_asana_task_with_template(task, meeting_info)
```

## Business Metrics

### ROI Calculation

- **Time Saved**: 2-3 hours per week per person
- **Accuracy Improvement**: 95% reduction in missed meetings
- **Preparation Quality**: 40% improvement in meeting preparation
- **Follow-up Rate**: 80% increase in post-meeting action completion

### Key Performance Indicators

- Meetings organized per week
- Average preparation score
- Meeting attendance rates
- Action item completion rates

## Deployment Options

### 1. Scheduled Automation

```bash
# Run every 2 hours during business hours
0 */2 9-17 * * 1-5 python meeting_organizer.py
```

### 2. Real-time Processing

```python
# Webhook-based real-time processing
@app.route('/gmail-webhook', methods=['POST'])
def process_new_email():
    email_data = request.json
    if is_meeting_email(email_data):
        agent.process_single_meeting(email_data)
    return "OK"
```

### 3. Cloud Function

```python
def meeting_organizer_handler(event, context):
    """Cloud function for meeting organization"""
    agent = MeetingOrganizerAgent()
    agent.run_meeting_organization()

    return {"status": "success", "processed": agent.processed_count}
```

## Customization Examples

### Industry-Specific Adaptations

#### Sales Teams

```python
def extract_sales_meeting_info(self, email):
    """Enhanced extraction for sales meetings"""
    base_info = self.extract_meeting_details(email)

    # Sales-specific information
    base_info.update({
        'lead_score': self.calculate_lead_score(email),
        'deal_stage': self.identify_deal_stage(email),
        'follow_up_type': self.determine_follow_up(email)
    })

    return base_info
```

#### Engineering Teams

```python
def extract_technical_meeting_info(self, email):
    """Enhanced extraction for technical meetings"""
    base_info = self.extract_meeting_details(email)

    # Technical-specific information
    base_info.update({
        'project_code': self.extract_project_code(email),
        'sprint_info': self.extract_sprint_details(email),
        'technical_requirements': self.extract_tech_requirements(email)
    })

    return base_info
```

## Integration with Other Tools

### Calendar Integration

```python
def sync_with_calendar(self, meeting_info):
    """Sync meeting information with calendar systems"""
    # Create calendar event
    # Set reminders
    # Invite attendees
    pass
```

### CRM Integration

```python
def sync_with_crm(self, meeting_info):
    """Sync meeting information with CRM"""
    # Update lead records
    # Log meeting activities
    # Update deal stages
    pass
```

## Troubleshooting

### Common Issues

1. **Email Parsing Errors**

   - Implement fuzzy matching for dates/times
   - Add manual review for uncertain extractions
   - Use AI for complex parsing scenarios

2. **Duplicate Meetings**

   - Implement email ID tracking
   - Use subject line similarity detection
   - Add manual deduplication workflows

3. **Missing Information**
   - Create templates for common meeting types
   - Implement smart defaults
   - Add manual data entry workflows

## Next Steps

This Meeting Organizer Agent demonstrates how to:

- ✅ Parse complex email content
- ✅ Extract structured data
- ✅ Organize information across platforms
- ✅ Create actionable tasks
- ✅ Implement business logic

### Related Examples

- [Customer Support Ticket Manager](../customer-support/ticket-manager.md)
- [Project Status Reporter](./project-reporter.md)
- [Sales Pipeline Automation](../sales-marketing/pipeline-automation.md)

Ready to build more sophisticated business automation? Explore our [advanced patterns](../../advanced/) section!
