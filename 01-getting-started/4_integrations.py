#!/usr/bin/env python3
"""
Integrations Example
===================

Learn how to use pre-built integrations with the Incredible API.
Integrations provide ready-to-use functions for popular services.

Usage:
    python 4_integrations.py

What you'll learn:
    - How to use integrations in chat completion
    - Available integration features
    - Combining integrations for powerful workflows
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def parse_api_response(result):
    """Helper function to parse API response in different formats."""
    
    if not isinstance(result, dict):
        return str(result)
    
    # Handle nested result format: {"result": {"response": [{"content": "text", "role": "assistant"}]}}
    if 'result' in result:
        inner_result = result['result']
        
        # Simple string result
        if isinstance(inner_result, str):
            return inner_result
        
        # Nested response format
        elif isinstance(inner_result, dict) and 'response' in inner_result:
            response_array = inner_result['response']
            if isinstance(response_array, list) and len(response_array) > 0:
                first_message = response_array[0]
                if isinstance(first_message, dict) and 'content' in first_message:
                    return first_message['content']
        
        return str(inner_result)
    
    # Handle direct response format: {"response": [{"content": "text", "role": "assistant"}]}
    elif 'response' in result:
        response_array = result['response']
        if isinstance(response_array, list) and len(response_array) > 0:
            first_message = response_array[0]
            if isinstance(first_message, dict) and 'content' in first_message:
                return first_message['content']
        
        return str(response_array)
    
    # Fallback: convert entire result to string
    return str(result)

def gmail_integration_example():
    """Example using Gmail integration."""
    print("📧 Gmail Integration Example")
    print("=" * 40)
    
    # Configuration
    api_key = os.getenv('INCREDIBLE_API_KEY')
    user_id = os.getenv('USER_ID')
    base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
    
    if not all([api_key, user_id]):
        print("❌ Error: INCREDIBLE_API_KEY and USER_ID required")
        print("💡 Add both to your .env file")
        return False
    
    url = f"{base_url}/v1/chat-completion"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # Use Gmail integration
    data = {
        "model": "small-1",
        "stream": False,
        "system": "You are a helpful email assistant. Use Gmail functions to help users manage their email.",
        "integrations": [
            {
                "id": "gmail",
                "features": ["gmail_search", "GMAIL_SEND_EMAIL"]  # Specify which features to enable
            }
        ],
        "messages": [
            {
                "role": "user",
                "content": f"Search my Gmail for any emails about 'meeting' from the last 3 days. My user_id is {user_id}"
            }
        ]
    }
    
    print("🔍 Asking AI to search Gmail for meetings...")
    print(f"📤 Request: Search for 'meeting' emails")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        assistant_response = parse_api_response(result)
        
        print(f"\n📧 Gmail Search Results:")
        print("-" * 40)
        print(assistant_response)
        print("-" * 40)
        
        print("✅ Gmail integration example completed!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Gmail integration error: {e}")
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = e.response.json()
                print(f"Error details: {error_detail}")
            except:
                print(f"Response text: {e.response.text}")
        return False

def perplexity_integration_example():
    """Example using Perplexity AI integration for research."""
    print("\n🔍 Perplexity AI Integration Example")
    print("=" * 40)
    
    # Configuration
    api_key = os.getenv('INCREDIBLE_API_KEY')
    user_id = os.getenv('USER_ID')
    base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
    
    url = f"{base_url}/v1/chat-completion"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # Use Perplexity integration
    data = {
        "model": "small-1",
        "stream": False,
        "system": "You are a research assistant with access to real-time information. Use Perplexity to get current, accurate data.",
        "integrations": [
            {
                "id": "perplexity",
                "features": ["PerplexityAISearch"]
            }
        ],
        "messages": [
            {
                "role": "user",
                "content": f"What are the latest developments in AI this week? Use Perplexity to research current news. My user_id is {user_id}"
            }
        ]
    }
    
    print("🔬 Asking AI to research latest AI developments...")
    print(f"📤 Request: Research current AI news")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        assistant_response = parse_api_response(result)
        
        print(f"\n🔍 Research Results:")
        print("-" * 40)
        print(assistant_response)
        print("-" * 40)
        
        print("✅ Perplexity integration example completed!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Perplexity integration error: {e}")
        return False

def multi_integration_example():
    """Example using multiple integrations together."""
    print("\n🎯 Multi-Integration Example")
    print("=" * 40)
    
    # Configuration
    api_key = os.getenv('INCREDIBLE_API_KEY')
    user_id = os.getenv('USER_ID')
    base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
    
    url = f"{base_url}/v1/chat-completion"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # Use multiple integrations
    data = {
        "model": "small-1",
        "stream": False,
        "system": "You are a comprehensive assistant with access to research and email capabilities. Coordinate between tools to complete complex tasks.",
        "integrations": [
            {
                "id": "perplexity",
                "features": ["PerplexityAISearch"]
            },
            {
                "id": "gmail", 
                "features": ["GMAIL_SEND_EMAIL"]
            }
        ],
        "messages": [
            {
                "role": "user",
                "content": f"Research the latest news about Tesla stock, then email me a summary at my Gmail. My user_id is {user_id}"
            }
        ]
    }
    
    print("🔗 Multi-integration workflow: Research + Email...")
    print(f"📤 Task: Research Tesla news and email summary")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        assistant_response = parse_api_response(result)
        
        print(f"\n🔗 Multi-Integration Result:")
        print("-" * 40)
        print(assistant_response)
        print("-" * 40)
        
        print("✅ Multi-integration example completed!")
        print("💡 The AI coordinated research and email to complete your complex request")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Multi-integration error: {e}")
        return False

def list_available_integrations():
    """Show available integrations and their features."""
    print("\n📋 Available Integrations")
    print("=" * 40)
    
    # Configuration
    api_key = os.getenv('INCREDIBLE_API_KEY')
    base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
    
    # This would typically come from an integrations list endpoint
    # For now, showing known integrations from the examples
    integrations = {
        "gmail": {
            "name": "Gmail",
            "description": "Email management and automation",
            "features": ["gmail_search", "GMAIL_SEND_EMAIL", "gmail_get_email"]
        },
        "google_sheets": {
            "name": "Google Sheets", 
            "description": "Spreadsheet creation and management",
            "features": ["sheets_create", "sheets_update_range", "sheets_read_range"]
        },
        "perplexity": {
            "name": "Perplexity AI",
            "description": "Real-time research and information",
            "features": ["PerplexityAISearch"]
        },
        "asana": {
            "name": "Asana",
            "description": "Task and project management", 
            "features": ["create_task", "update_task", "get_tasks"]
        },
        "google_calendar": {
            "name": "Google Calendar",
            "description": "Calendar and event management",
            "features": ["create_event", "update_event", "list_events"]
        },
        "google_docs": {
            "name": "Google Docs",
            "description": "Document creation and editing",
            "features": ["create_document", "update_document", "get_document"]
        }
    }
    
    print("🔌 Available Integrations:")
    print()
    
    for integration_id, info in integrations.items():
        print(f"📦 **{info['name']}** (`{integration_id}`)")
        print(f"   {info['description']}")
        print(f"   Features: {', '.join(info['features'])}")
        print()
    
    print("💡 Usage in chat completion:")
    print('''
    "integrations": [
        {
            "id": "gmail",
            "features": ["gmail_search", "GMAIL_SEND_EMAIL"]
        }
    ]
    ''')

def main():
    """Run all integration examples."""
    print("🚀 Incredible API - Integration Examples")
    print("=" * 60)
    
    # Show available integrations first
    list_available_integrations()
    
    # Run examples
    success = gmail_integration_example()
    
    if success:
        perplexity_integration_example()
        multi_integration_example()
    
    print(f"\n{'='*60}")
    print("🎓 Integration Examples Complete!")
    print("\n💡 Key Concepts:")
    print("   • Integrations provide pre-built functions for popular services")
    print("   • Specify integration ID and desired features")
    print("   • AI automatically uses integration functions as needed")
    print("   • Multiple integrations can work together")
    print("\n🔧 Integration Setup:")
    print("   • Each integration requires OAuth or API key setup")
    print("   • Configure integrations in Incredible dashboard")
    print("   • Provide user_id for user-specific operations")
    print("\n🔗 Integration Benefits:")
    print("   • No need to implement complex API calls")
    print("   • Built-in error handling and retries")
    print("   • Automatic authentication management")
    print("   • Ready-to-use functions for common tasks")
    print("\n➡️  Next: Try the advanced examples in other folders!")

if __name__ == "__main__":
    main()
