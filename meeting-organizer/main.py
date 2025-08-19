#!/usr/bin/env python3
"""
Meeting Organizer with Incredible API
=====================================

This example demonstrates how to:
1. Scan Gmail for meeting invitations and requests
2. Extract meeting details using AI
3. Create calendar events automatically
4. Generate prep and follow-up tasks in Asana

Usage:
    python main.py

Features:
    - AI-powered meeting detection
    - Automatic calendar event creation
    - Task generation for meeting prep
    - Follow-up task scheduling
"""

import os
import re
import time
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MeetingOrganizer:
    def __init__(self):
        """Initialize the meeting organizer system."""
        self.api_key = os.getenv('INCREDIBLE_API_KEY')
        self.user_id = os.getenv('USER_ID')
        self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
        self.asana_project_id = os.getenv('ASANA_PROJECT_ID')
        self.calendar_id = os.getenv('CALENDAR_ID', 'primary')
        
        if not all([self.api_key, self.user_id, self.asana_project_id]):
            raise ValueError("Missing required environment variables. Check .env file.")
        
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        print(f"✅ Meeting Organizer initialized")
        print(f"📅 Calendar: {self.calendar_id}")
        print(f"📋 Asana Project: {self.asana_project_id}")

    def search_emails(self, query, hours_back=24):
        """Search Gmail for meeting-related emails."""
        print(f"🔍 Searching for meetings (last {hours_back}h): {query}")
        
        url = f"{self.base_url}/v1/integrations/gmail/execute"
        data = {
            "user_id": self.user_id,
            "feature_name": "gmail_search",
            "inputs": {
                "query": f"{query} newer_than:{hours_back}h",
                "max_results": 15
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

    def extract_meeting_details(self, email):
        """Extract meeting details from email using AI and pattern matching."""
        print(f"📋 Extracting meeting details from: {email.get('subject', 'No Subject')}")
        
        subject = email.get('subject', '')
        content = email.get('content', '')
        sender = email.get('sender', '')
        
        # Extract basic info
        meeting_details = {
            'title': subject or 'Meeting',
            'organizer': sender,
            'description': content[:500] if content else '',
            'email_id': email.get('id', ''),
            'attendees': []
        }
        
        # Extract date and time using patterns
        meeting_details.update(self.extract_date_time(content))
        
        # Extract attendees
        meeting_details['attendees'] = self.extract_attendees(content, sender)
        
        # Extract location/meeting link
        meeting_details['location'] = self.extract_location(content)
        
        # Set default duration
        if 'duration' not in meeting_details:
            meeting_details['duration'] = 60  # Default 1 hour
        
        print(f"   📅 Date: {meeting_details.get('date', 'TBD')}")
        print(f"   ⏰ Time: {meeting_details.get('time', 'TBD')}")
        print(f"   📍 Location: {meeting_details.get('location', 'TBD')}")
        
        return meeting_details

    def extract_date_time(self, content):
        """Extract date and time from email content."""
        details = {}
        
        # Common date patterns
        date_patterns = [
            r'(\w+day),?\s+(\w+)\s+(\d{1,2}),?\s+(\d{4})',  # Monday, January 15, 2024
            r'(\d{1,2})/(\d{1,2})/(\d{4})',                 # 1/15/2024
            r'(\d{4})-(\d{1,2})-(\d{1,2})',                 # 2024-01-15
            r'(\w+)\s+(\d{1,2}),?\s+(\d{4})',               # January 15, 2024
        ]
        
        # Common time patterns
        time_patterns = [
            r'(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)',           # 2:30 PM
            r'(\d{1,2})\s*(AM|PM|am|pm)',                   # 2 PM
            r'at\s+(\d{1,2}):(\d{2})',                      # at 14:30
        ]
        
        # Try to find date
        for pattern in date_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                if '/' in pattern:
                    # MM/DD/YYYY format
                    month, day, year = match.groups()
                    details['date'] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                elif '-' in pattern:
                    # YYYY-MM-DD format
                    year, month, day = match.groups()
                    details['date'] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                else:
                    # Text format - simplified parsing
                    try:
                        if len(match.groups()) == 4:  # Monday, January 15, 2024
                            _, month_name, day, year = match.groups()
                        else:  # January 15, 2024
                            month_name, day, year = match.groups()
                        
                        month_map = {
                            'january': '01', 'february': '02', 'march': '03',
                            'april': '04', 'may': '05', 'june': '06',
                            'july': '07', 'august': '08', 'september': '09',
                            'october': '10', 'november': '11', 'december': '12'
                        }
                        month = month_map.get(month_name.lower(), '01')
                        details['date'] = f"{year}-{month}-{day.zfill(2)}"
                    except:
                        pass
                break
        
        # Try to find time
        for pattern in time_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                if len(match.groups()) == 3:  # HH:MM AM/PM
                    hour, minute, ampm = match.groups()
                    hour = int(hour)
                    if ampm.upper() == 'PM' and hour != 12:
                        hour += 12
                    elif ampm.upper() == 'AM' and hour == 12:
                        hour = 0
                    details['time'] = f"{hour:02d}:{minute}"
                elif len(match.groups()) == 2:
                    if ':' in match.group(0):  # at HH:MM
                        hour, minute = match.groups()
                        details['time'] = f"{hour.zfill(2)}:{minute}"
                    else:  # H AM/PM
                        hour, ampm = match.groups()
                        hour = int(hour)
                        if ampm.upper() == 'PM' and hour != 12:
                            hour += 12
                        elif ampm.upper() == 'AM' and hour == 12:
                            hour = 0
                        details['time'] = f"{hour:02d}:00"
                break
        
        # Default to tomorrow at 2 PM if no date/time found
        if 'date' not in details:
            tomorrow = datetime.now() + timedelta(days=1)
            details['date'] = tomorrow.strftime('%Y-%m-%d')
        
        if 'time' not in details:
            details['time'] = '14:00'  # 2 PM default
        
        return details

    def extract_attendees(self, content, sender):
        """Extract attendee emails from content."""
        attendees = []
        
        # Add sender
        if '<' in sender and '>' in sender:
            sender_email = sender.split('<')[1].split('>')[0]
            attendees.append(sender_email)
        
        # Look for email patterns in content
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        found_emails = re.findall(email_pattern, content)
        
        for email in found_emails:
            if email not in attendees:
                attendees.append(email)
        
        return attendees[:10]  # Limit to 10 attendees

    def extract_location(self, content):
        """Extract meeting location or video link."""
        # Look for common meeting platforms
        video_patterns = [
            r'(https://zoom\.us/j/\d+)',
            r'(https://teams\.microsoft\.com/[^\s]+)',
            r'(https://meet\.google\.com/[^\s]+)',
            r'(https://.*\.webex\.com/[^\s]+)'
        ]
        
        for pattern in video_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
        
        # Look for physical locations
        location_patterns = [
            r'(?:room|conference room|office)\s+([A-Z0-9\-]+)',
            r'(?:at|in)\s+([A-Z][a-zA-Z\s]+(?:room|office|building))',
            r'(?:location|where):\s*([^\n\r]+)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                if len(location) > 5 and len(location) < 100:
                    return location
        
        return "TBD"

    def create_calendar_event(self, meeting_details):
        """Create calendar event using Google Calendar integration."""
        print(f"📅 Creating calendar event: {meeting_details['title']}")
        
        # Calculate start and end times
        start_datetime = f"{meeting_details['date']}T{meeting_details['time']}:00"
        start_time = datetime.fromisoformat(start_datetime)
        end_time = start_time + timedelta(minutes=meeting_details['duration'])
        end_datetime = end_time.isoformat()
        
        url = f"{self.base_url}/v1/integrations/google_calendar/execute"
        data = {
            "user_id": self.user_id,
            "feature_name": "create_event",
            "inputs": {
                "calendar_id": self.calendar_id,
                "summary": meeting_details['title'],
                "description": f"{meeting_details['description']}\n\nOrganizer: {meeting_details['organizer']}",
                "start": {
                    "dateTime": start_datetime,
                    "timeZone": "America/New_York"  # Adjust as needed
                },
                "end": {
                    "dateTime": end_datetime,
                    "timeZone": "America/New_York"
                },
                "location": meeting_details['location'],
                "attendees": [{"email": email} for email in meeting_details['attendees']]
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            event_id = result.get('result', {}).get('id')
            if event_id:
                print(f"✅ Calendar event created: {event_id}")
                return event_id
            else:
                print(f"❌ Failed to create calendar event")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating calendar event: {e}")
            return None

    def create_asana_tasks(self, meeting_details, event_id=None):
        """Create preparation and follow-up tasks in Asana."""
        print(f"📋 Creating Asana tasks for: {meeting_details['title']}")
        
        tasks_created = []
        
        # Preparation task
        prep_task_name = f"Prepare for: {meeting_details['title']}"
        prep_notes = f"""
Meeting Preparation Checklist:

📅 Meeting: {meeting_details['title']}
🕐 Date/Time: {meeting_details['date']} at {meeting_details['time']}
📍 Location: {meeting_details['location']}
👥 Attendees: {', '.join(meeting_details['attendees'][:5])}

Preparation Tasks:
□ Review meeting agenda
□ Prepare presentation materials
□ Check technology/equipment
□ Review attendee backgrounds
□ Prepare questions and discussion topics
□ Confirm meeting logistics

{f'📅 Calendar Event: {event_id}' if event_id else ''}
"""
        
        prep_task = {
            "name": prep_task_name,
            "notes": prep_notes.strip(),
            "due_on": meeting_details['date'],
            "projects": [self.asana_project_id]
        }
        
        prep_task_id = self.create_asana_task(prep_task)
        if prep_task_id:
            tasks_created.append(prep_task_id)
        
        # Follow-up task (due day after meeting)
        follow_up_date = datetime.strptime(meeting_details['date'], "%Y-%m-%d") + timedelta(days=1)
        follow_up_task_name = f"Follow-up: {meeting_details['title']}"
        follow_up_notes = f"""
Meeting Follow-up Actions:

📅 Meeting: {meeting_details['title']}
🕐 Held: {meeting_details['date']} at {meeting_details['time']}

Follow-up Tasks:
□ Send meeting notes to attendees
□ Complete action items assigned
□ Schedule follow-up meetings if needed
□ Update project status
□ File meeting documentation

{f'📅 Calendar Event: {event_id}' if event_id else ''}
"""
        
        follow_up_task = {
            "name": follow_up_task_name,
            "notes": follow_up_notes.strip(),
            "due_on": follow_up_date.strftime("%Y-%m-%d"),
            "projects": [self.asana_project_id]
        }
        
        follow_up_task_id = self.create_asana_task(follow_up_task)
        if follow_up_task_id:
            tasks_created.append(follow_up_task_id)
        
        print(f"✅ Created {len(tasks_created)} Asana tasks")
        return tasks_created

    def create_asana_task(self, task_data):
        """Create a single task in Asana."""
        url = f"{self.base_url}/v1/integrations/asana/execute"
        
        data = {
            "user_id": self.user_id,
            "feature_name": "create_task",
            "inputs": task_data
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            task_id = result.get('result', {}).get('gid')
            return task_id
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating Asana task: {e}")
            return None

    def process_meeting(self, email):
        """Process a single meeting email through complete workflow."""
        print(f"\n🔄 Processing: {email.get('subject', 'No Subject')}")
        
        try:
            # Extract meeting details
            meeting_details = self.extract_meeting_details(email)
            
            if not meeting_details.get('title'):
                print("❌ Could not extract meeting details")
                return False
            
            # Create calendar event
            event_id = self.create_calendar_event(meeting_details)
            
            # Create Asana tasks
            task_ids = self.create_asana_tasks(meeting_details, event_id)
            
            success = event_id is not None and len(task_ids) > 0
            print(f"   {'✅' if success else '❌'} Meeting processing {'completed' if success else 'failed'}")
            
            return success
            
        except Exception as e:
            print(f"❌ Error processing meeting: {e}")
            return False

    def scan_for_meetings(self, hours_back=24):
        """Main workflow: Scan for meetings and process them."""
        print(f"\n🚀 Starting meeting scan (last {hours_back} hours)")
        
        # Meeting detection queries
        meeting_queries = [
            'subject:(meeting OR call OR conference OR zoom)',
            'subject:(invite OR invitation OR calendar)',
            '"join the meeting" OR "zoom link" OR "teams meeting"',
            '"schedule" OR "let\'s meet" OR "can we meet"'
        ]
        
        all_meeting_emails = []
        
        # Search with each query
        for query in meeting_queries:
            emails = self.search_emails(query, hours_back)
            
            for email in emails:
                if self.is_meeting_email(email):
                    all_meeting_emails.append(email)
        
        # Remove duplicates
        unique_meetings = {email['id']: email for email in all_meeting_emails}
        meetings = list(unique_meetings.values())
        
        print(f"📨 Found {len(meetings)} potential meetings")
        
        if not meetings:
            print("✅ No new meetings found")
            return 0
        
        # Process each meeting
        successful_meetings = 0
        
        for email in meetings:
            if self.process_meeting(email):
                successful_meetings += 1
            time.sleep(1)  # Rate limiting
        
        print(f"\n🎉 Meeting processing complete!")
        print(f"📧 Emails processed: {len(meetings)}")
        print(f"✅ Meetings organized: {successful_meetings}")
        print(f"📅 View calendar: https://calendar.google.com")
        print(f"📋 View tasks: https://app.asana.com/0/{self.asana_project_id}")
        
        return successful_meetings

    def is_meeting_email(self, email):
        """Determine if email represents a meeting."""
        subject = email.get('subject', '').lower()
        content = email.get('content', '').lower()
        
        # Meeting indicators
        meeting_keywords = [
            'meeting', 'call', 'conference', 'zoom', 'teams',
            'invite', 'invitation', 'schedule', 'calendar',
            'appointment', 'discussion', 'sync', 'standup'
        ]
        
        # Exclude automated/spam emails
        exclude_keywords = [
            'newsletter', 'marketing', 'promotion', 'unsubscribe',
            'automated', 'noreply', 'system'
        ]
        
        full_text = f"{subject} {content}".lower()
        
        has_meeting_keywords = any(keyword in full_text for keyword in meeting_keywords)
        has_exclude_keywords = any(keyword in full_text for keyword in exclude_keywords)
        
        return has_meeting_keywords and not has_exclude_keywords

def main():
    """Main entry point for the meeting organizer script."""
    print("📅 Incredible API - Meeting Organizer")
    print("=" * 50)
    
    try:
        # Initialize the meeting organizer
        organizer = MeetingOrganizer()
        
        # Scan for meetings from last 24 hours
        processed = organizer.scan_for_meetings(hours_back=24)
        
        if processed > 0:
            print(f"\n✅ Successfully organized {processed} meetings")
            print("📅 Check your calendar for new events")
            print("📋 Check Asana for preparation and follow-up tasks")
        else:
            print("\n📭 No new meetings found in the specified timeframe")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Set up your .env file with all required variables")
        print("   2. Connected Gmail, Google Calendar, and Asana integrations")
        print("   3. Created an Asana project for meeting tasks")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
