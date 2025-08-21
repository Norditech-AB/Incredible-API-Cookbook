#!/usr/bin/env python3
"""
🚀 Advanced Workflow - Multi-Step Function Calling
================================================

Learn how to chain multiple function calls together to create
powerful, multi-step workflows. This is where AI function calling
really shines - orchestrating complex sequences of actions.

What this demonstrates:
• Multi-step workflows with function chaining
• Real-world business process automation
• Error handling in complex workflows
• State management across function calls

Real-world applications:
• Meeting scheduling with email confirmations
• Order processing with inventory checks
• Customer onboarding workflows
• Data pipeline orchestration
"""

import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Workflow Functions - These would integrate with real systems

def check_calendar_availability(date, time, duration_hours):
    """
    Check if a time slot is available in the calendar.
    In real implementation, this would integrate with Google Calendar, Outlook, etc.
    """
    # Simulated calendar check
    busy_slots = [
        {"date": "2024-01-15", "time": "14:00", "duration": 2},
        {"date": "2024-01-15", "time": "10:00", "duration": 1},
        {"date": "2024-01-16", "time": "09:00", "duration": 3}
    ]
    
    # Check if requested slot conflicts with busy slots
    for slot in busy_slots:
        if slot["date"] == date and slot["time"] == time:
            result = {"available": False, "reason": "Time slot already booked"}
            print(f"📅 Calendar check: {date} {time} - Not available (conflict)")
            return result
    
    result = {"available": True, "slot": f"{date} {time} for {duration_hours} hours"}
    print(f"📅 Calendar check: {date} {time} - Available ✅")
    return result

def create_calendar_event(title, date, time, duration_hours, attendees):
    """
    Create a calendar event.
    Real implementation would create actual calendar events.
    """
    event_id = f"event_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    event_data = {
        "event_id": event_id,
        "title": title,
        "date": date,
        "time": time,
        "duration_hours": duration_hours,
        "attendees": attendees.split(", ") if isinstance(attendees, str) else attendees,
        "status": "created"
    }
    
    print(f"📅 Created calendar event: {title} on {date} at {time}")
    print(f"   Event ID: {event_id}")
    print(f"   Attendees: {', '.join(event_data['attendees'])}")
    
    return event_data

def send_meeting_invitation(event_id, title, date, time, attendees, meeting_link=None):
    """
    Send meeting invitation emails to attendees.
    Real implementation would integrate with email services.
    """
    # Simulate sending emails
    attendee_list = attendees.split(", ") if isinstance(attendees, str) else attendees
    
    invitation_data = {
        "event_id": event_id,
        "emails_sent": len(attendee_list),
        "recipients": attendee_list,
        "subject": f"Meeting Invitation: {title}",
        "meeting_details": {
            "date": date,
            "time": time,
            "link": meeting_link or "https://meet.incredible.one/12345"
        }
    }
    
    print(f"📧 Sent {len(attendee_list)} meeting invitations")
    print(f"   Subject: Meeting Invitation: {title}")
    print(f"   Meeting link: {invitation_data['meeting_details']['link']}")
    
    return invitation_data

def create_follow_up_tasks(meeting_title, attendees, due_date):
    """
    Create follow-up tasks after meeting creation.
    Real implementation would integrate with task management systems.
    """
    attendee_list = attendees.split(", ") if isinstance(attendees, str) else attendees
    
    tasks = []
    for attendee in attendee_list:
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(tasks)}"
        task = {
            "task_id": task_id,
            "title": f"Prepare for: {meeting_title}",
            "assigned_to": attendee.strip(),
            "due_date": due_date,
            "status": "pending"
        }
        tasks.append(task)
    
    print(f"✅ Created {len(tasks)} follow-up tasks")
    for task in tasks:
        print(f"   Task: {task['title']} → {task['assigned_to']}")
    
    return {"tasks_created": len(tasks), "tasks": tasks}

def log_workflow_completion(workflow_id, steps_completed, total_time):
    """
    Log the completion of a workflow for monitoring and analytics.
    """
    log_entry = {
        "workflow_id": workflow_id,
        "completed_at": datetime.now().isoformat(),
        "steps_completed": steps_completed,
        "total_time_seconds": total_time,
        "status": "completed"
    }
    
    print(f"📊 Workflow completed: {workflow_id}")
    print(f"   Steps: {steps_completed}")
    print(f"   Total time: {total_time}s")
    
    return log_entry

# Define all workflow functions for AI
WORKFLOW_TOOLS = [
    {
        "name": "check_calendar_availability", 
        "description": "Check if a specific time slot is available in the calendar",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                "time": {"type": "string", "description": "Time in HH:MM format (24-hour)"},
                "duration_hours": {"type": "number", "description": "Meeting duration in hours"}
            },
            "required": ["date", "time", "duration_hours"]
        }
    },
    {
        "name": "create_calendar_event",
        "description": "Create a calendar event after confirming availability",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Meeting title"},
                "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                "time": {"type": "string", "description": "Time in HH:MM format"},
                "duration_hours": {"type": "number", "description": "Meeting duration in hours"},
                "attendees": {"type": "string", "description": "Comma-separated list of attendee names/emails"}
            },
            "required": ["title", "date", "time", "duration_hours", "attendees"]
        }
    },
    {
        "name": "send_meeting_invitation",
        "description": "Send email invitations to meeting attendees",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {"type": "string", "description": "Calendar event ID"},
                "title": {"type": "string", "description": "Meeting title"},
                "date": {"type": "string", "description": "Meeting date"},
                "time": {"type": "string", "description": "Meeting time"},
                "attendees": {"type": "string", "description": "Comma-separated attendees"},
                "meeting_link": {"type": "string", "description": "Optional video meeting link"}
            },
            "required": ["event_id", "title", "date", "time", "attendees"]
        }
    },
    {
        "name": "create_follow_up_tasks",
        "description": "Create follow-up tasks for meeting attendees",
        "parameters": {
            "type": "object",
            "properties": {
                "meeting_title": {"type": "string", "description": "Meeting title for task reference"},
                "attendees": {"type": "string", "description": "Comma-separated attendees"},
                "due_date": {"type": "string", "description": "Task due date in YYYY-MM-DD format"}
            },
            "required": ["meeting_title", "attendees", "due_date"]
        }
    },
    {
        "name": "log_workflow_completion",
        "description": "Log the completion of the entire workflow",
        "parameters": {
            "type": "object",
            "properties": {
                "workflow_id": {"type": "string", "description": "Unique workflow identifier"},
                "steps_completed": {"type": "number", "description": "Number of steps completed"},
                "total_time": {"type": "number", "description": "Total workflow time in seconds"}
            },
            "required": ["workflow_id", "steps_completed", "total_time"]
        }
    }
]

def execute_workflow_function(function_name, arguments):
    """
    Execute workflow functions with proper error handling.
    """
    try:
        if function_name == "check_calendar_availability":
            return check_calendar_availability(**arguments)
        elif function_name == "create_calendar_event":
            return create_calendar_event(**arguments)
        elif function_name == "send_meeting_invitation":
            return send_meeting_invitation(**arguments)
        elif function_name == "create_follow_up_tasks":
            return create_follow_up_tasks(**arguments)
        elif function_name == "log_workflow_completion":
            return log_workflow_completion(**arguments)
        else:
            return {"error": f"Unknown function: {function_name}"}
    except Exception as e:
        return {"error": f"Function execution failed: {str(e)}"}

def run_advanced_workflow(workflow_request):
    """
    Run a complex multi-step workflow using AI function calling.
    """
    print(f"🚀 Starting advanced workflow...")
    print(f"📋 Request: {workflow_request}")
    print("🤖 AI will orchestrate multiple function calls...")
    print()
    
    # Get API key
    api_key = os.getenv('INCREDIBLE_API_KEY')
    if not api_key:
        print("❌ Missing INCREDIBLE_API_KEY!")
        return
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Keep track of conversation history for multi-step workflow
    conversation_history = [{"role": "user", "content": workflow_request}]
    
    # System prompt to guide AI through the workflow
    system_prompt = """You are an AI assistant that orchestrates complex workflows using function calls.

For meeting scheduling workflows, follow these steps:
1. First, check calendar availability
2. If available, create the calendar event  
3. Send meeting invitations to attendees
4. Create follow-up tasks for attendees
5. Log the workflow completion

Always use the function results from previous steps in subsequent function calls. Be systematic and thorough."""
    
    step_count = 0
    max_steps = 10  # Prevent infinite loops
    start_time = datetime.now()
    
    while step_count < max_steps:
        step_count += 1
        print(f"🔄 Step {step_count}:")
        print("-" * 20)
        
        # Prepare the request with conversation history
        data = {
            "model": "small-1",
            "stream": False,
            "system": system_prompt,
            "messages": conversation_history,
            "functions": WORKFLOW_TOOLS
        }
        
        try:
            response = requests.post(
                'https://api.incredible.one/v1/chat-completion',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"❌ API Error: {response.status_code}")
                break
            
            result = response.json()
            response_items = result['result']['response']
            
            # Look for function calls in the response
            function_call_item = None
            assistant_message = None
            
            for item in response_items:
                if item.get('type') == 'function_call':
                    function_call_item = item
                elif item.get('role') == 'assistant':
                    assistant_message = item
            
            if function_call_item:
                # AI wants to call a function
                function_call_id = function_call_item['function_call_id']
                function_calls = function_call_item['function_calls']
                
                if len(function_calls) > 0:
                    function_call = function_calls[0]  # Get first function call
                    function_name = function_call['name']
                    function_input = function_call['input']
                    
                    print(f"🔧 AI calling: {function_name}")
                    print(f"📋 Arguments: {function_input}")
                    
                    # Execute the function
                    function_result = execute_workflow_function(function_name, function_input)
                    
                    # Add assistant message to history if it exists
                    if assistant_message:
                        conversation_history.append(assistant_message)
                    
                    # Add function call and result to conversation history
                    conversation_history.extend([
                        function_call_item,
                        {
                            "type": "function_call_result",
                            "function_call_id": function_call_id,
                            "function_call_results": [function_result]
                        }
                    ])
                    
                    # Check if workflow is complete
                    if function_name == "log_workflow_completion":
                        print("✅ Workflow completed!")
                        break
                
            else:
                # AI provided a direct response (workflow might be complete)
                if assistant_message:
                    ai_response = assistant_message['content']
                    print(f"🤖 AI: {ai_response}")
                    
                    # Add response to history
                    conversation_history.append(assistant_message)
                    
                    # Check if AI indicates workflow is complete
                    if "complete" in ai_response.lower() or "finished" in ai_response.lower():
                        print("✅ Workflow completed by AI response!")
                        break
                else:
                    print("❌ No function call or assistant response found")
                    break
        
        except Exception as e:
            print(f"❌ Error in step {step_count}: {e}")
            break
    
    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()
    
    print(f"\n📊 Workflow Summary:")
    print(f"   Total steps: {step_count}")
    print(f"   Total time: {total_time:.1f}s")
    print(f"   Status: {'Completed' if step_count < max_steps else 'Max steps reached'}")

def advanced_workflow_demo():
    """
    Demonstrate complex multi-step workflows.
    """
    print("🚀 Advanced Workflow - Multi-Step Function Calling")
    print("=" * 60)
    print("AI will orchestrate complex workflows using multiple functions...")
    print()
    
    # Example complex workflow request
    workflow_request = """
Please schedule a team meeting for next Monday (2024-01-15) at 2:00 PM for 2 hours.

Meeting details:
- Title: "Q1 Planning Session"
- Attendees: Sarah Johnson, Mike Chen, Lisa Wang
- Duration: 2 hours

Please follow the complete workflow:
1. Check if that time slot is available
2. Create the calendar event if available
3. Send meeting invitations to all attendees
4. Create follow-up preparation tasks due 1 day before the meeting
5. Log the workflow completion

Make sure to use the results from each step in the next step.
"""
    
    # Run the advanced workflow
    run_advanced_workflow(workflow_request)

def explain_advanced_workflows():
    """
    Explain the power of multi-step function calling workflows.
    """
    print("\n" + "=" * 60)
    print("🎯 WHY ARE ADVANCED WORKFLOWS GAME-CHANGING?")
    print("=" * 60)
    
    print("""
Advanced workflows with function calling enable true AI automation:

🔄 **Multi-Step Orchestration**:
   • AI manages complex sequences of actions
   • Each step uses results from previous steps
   • Automatic error handling and recovery
   • State management across multiple function calls

🤖 **Intelligent Decision Making**:
   • AI adapts the workflow based on function results
   • Handles edge cases and exceptions gracefully  
   • Optimizes the sequence of operations
   • Can retry or skip steps as needed

🏢 **Real-World Business Processes**:

   📅 **Meeting Management**:
      Check availability → Create event → Send invites → Create tasks → Log completion

   📦 **Order Processing**:
      Validate order → Check inventory → Process payment → Ship item → Send tracking

   👤 **Customer Onboarding**:
      Create account → Send welcome email → Schedule demo → Assign representative

   📊 **Data Pipelines**:
      Extract data → Transform format → Validate quality → Load to database → Generate report

🚀 **Key Benefits**:
   • Reduces manual work by 80%+
   • Ensures consistent process execution
   • Provides full audit trail of actions
   • Scales to handle thousands of workflows
   • Integrates with existing business systems

💡 **Advanced Patterns**:
   • Conditional workflows (if/then logic)
   • Parallel execution of independent steps
   • Rollback and retry mechanisms
   • Dynamic workflow generation based on context

This transforms AI from a chatbot into a true business automation platform!
""")

if __name__ == "__main__":
    # Run the advanced workflow demonstration
    advanced_workflow_demo()
    
    # Explain the power of advanced workflows
    explain_advanced_workflows()
    
    print("\n🎉 Congratulations! You've mastered function calling:")
    print("   ✅ Simple single function calls")
    print("   ✅ Multiple tool selection")
    print("   ✅ JSON data extraction")
    print("   ✅ Complex multi-step workflows")
    
    print("\n🚀 Next Steps:")
    print("   • Integrate with your real business systems")
    print("   • Build custom functions for your use case")
    print("   • Create industry-specific workflows")
    print("   • Explore parallel function execution")
    
    print("\n💡 You now have the foundation to build:")
    print("   • AI-powered customer service bots")
    print("   • Automated business process workflows")
    print("   • Intelligent data processing pipelines")
    print("   • Complex multi-system integrations")
