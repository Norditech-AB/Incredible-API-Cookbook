# Meeting Organizer

**Automatically extract meetings from Gmail, create calendar events, and generate prep/follow-up tasks in Asana.**

## What it does

1. **Scans Gmail** for meeting invitations and requests
2. **Extracts details** using AI (date, time, location, attendees)
3. **Creates calendar events** automatically in Google Calendar
4. **Generates tasks** in Asana for meeting preparation and follow-up

## Quick Start

```bash
# 1. Clone and navigate
git clone [repo-url]
cd meeting-organizer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up configuration
cp env.example .env
# Edit .env with your credentials

# 4. Run meeting organization
python main.py
```

## Required Setup

### 1. Incredible API
- Get API key from [Incredible Dashboard](https://incredible.one)
- Connect Gmail integration (OAuth)
- Connect Google Calendar integration (OAuth)
- Connect Asana integration (OAuth)

### 2. Asana Project Setup
- Create a project in Asana for meeting tasks
- Copy the project ID from the URL (long number)
- Add to your .env file

### 3. Environment Variables
```bash
INCREDIBLE_API_KEY=your_api_key
USER_ID=your_user_id
ASANA_PROJECT_ID=your_project_id
CALENDAR_ID=primary
```

## How it works

### Email Detection
Searches for emails matching:
- `subject:(meeting OR call OR conference OR zoom)`
- `subject:(invite OR invitation OR calendar)`
- `"join the meeting" OR "zoom link" OR "teams meeting"`
- `"schedule" OR "let's meet" OR "can we meet"`

### AI-Powered Extraction
For each meeting email, extracts:
- **Meeting title** from subject line
- **Date & time** using pattern recognition
- **Location** (physical address or video link)
- **Attendees** from email content and sender
- **Duration** (defaults to 1 hour)

### Workflow Automation
1. **Calendar Event Creation**:
   - Adds event to Google Calendar
   - Includes all attendees and details
   - Sets proper timezone

2. **Task Generation**:
   - **Prep task**: Due on meeting date with checklist
   - **Follow-up task**: Due day after meeting

## Expected Output

```
📅 Incredible API - Meeting Organizer
==================================================
✅ Meeting Organizer initialized
📅 Calendar: primary
📋 Asana Project: 1234567890

🚀 Starting meeting scan (last 24 hours)
🔍 Searching for meetings (last 24h): subject:(meeting OR call OR conference)
📧 Found 2 emails

🔄 Processing: Team Standup - Monday 2PM

📋 Extracting meeting details from: Team Standup - Monday 2PM
   📅 Date: 2024-01-15
   ⏰ Time: 14:00
   📍 Location: https://zoom.us/j/123456789

📅 Creating calendar event: Team Standup - Monday 2PM
✅ Calendar event created: abc123def456

📋 Creating Asana tasks for: Team Standup - Monday 2PM
✅ Created 2 Asana tasks
   ✅ Meeting processing completed

🎉 Meeting processing complete!
📧 Emails processed: 2
✅ Meetings organized: 2
📅 View calendar: https://calendar.google.com
📋 View tasks: https://app.asana.com/0/1234567890
```

## Generated Tasks

### Preparation Task
Created with due date = meeting date:
```
Prepare for: [Meeting Title]

Meeting Preparation Checklist:
□ Review meeting agenda
□ Prepare presentation materials  
□ Check technology/equipment
□ Review attendee backgrounds
□ Prepare questions and discussion topics
□ Confirm meeting logistics
```

### Follow-up Task  
Created with due date = day after meeting:
```
Follow-up: [Meeting Title]

Meeting Follow-up Actions:
□ Send meeting notes to attendees
□ Complete action items assigned
□ Schedule follow-up meetings if needed
□ Update project status  
□ File meeting documentation
```

## Supported Meeting Patterns

### Date/Time Formats
- "Monday, January 15, 2024 at 2:30 PM"
- "1/15/2024 14:30"
- "January 15 at 2 PM"
- "Tomorrow at 10 AM"

### Location Detection
- **Video**: Zoom, Teams, Google Meet, WebEx links
- **Physical**: "Conference Room A", "Building 2, Room 101"
- **Default**: "TBD" if not found

### Meeting Types
- Team meetings and standups
- Client calls and presentations  
- Conference calls and video meetings
- One-on-one meetings
- Interview scheduling

## Customization

### Modify Search Queries
Edit `meeting_queries` in `scan_for_meetings()`:
```python
meeting_queries = [
    'subject:(your custom keywords)',
    '"your specific meeting patterns"'
]
```

### Adjust Task Templates
Edit `create_asana_tasks()` to customize:
- Task names and descriptions
- Checklist items
- Due date calculation
- Task assignments

### Change Date/Time Parsing
Edit `extract_date_time()` to:
- Add new date/time patterns
- Support different languages
- Handle timezone conversion
- Parse recurring meetings

## Automation

### Hourly Processing
```bash
# Add to crontab for automatic processing
0 * * * * cd /path/to/meeting-organizer && python main.py
```

### Integration with Email Rules
Set up Gmail filters to:
- Label meeting emails automatically
- Forward important meetings to specific addresses
- Mark VIP meeting invitations

## Troubleshooting

**"Could not extract meeting details"**
- Check if email contains date/time information
- Verify meeting keywords are present
- Try with clearer meeting invitation formats

**"Failed to create calendar event"**
- Check Google Calendar OAuth connection
- Verify calendar ID (usually "primary")
- Ensure calendar permissions allow event creation

**"Error creating Asana task"**
- Check Asana OAuth connection
- Verify project ID is correct and accessible
- Ensure you have task creation permissions

## Advanced Features

### Smart Conflict Detection
- Check calendar for existing events
- Suggest alternative times for conflicts
- Notify about back-to-back meetings

### Meeting Analytics
- Track meeting frequency and duration
- Analyze meeting patterns
- Generate productivity reports

### Integration Enhancements
- Slack notifications for urgent meetings
- Automatic meeting room booking
- Integration with video conferencing platforms

## Use Cases

- **Executive Assistants**: Automate calendar management
- **Team Leads**: Organize recurring team meetings  
- **Sales Teams**: Manage client call scheduling
- **Project Managers**: Track project meeting workflows
- **Remote Teams**: Streamline virtual meeting coordination
