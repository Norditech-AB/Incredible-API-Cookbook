#!/usr/bin/env python3
"""
Integrations - Connect AI to Real Services
==========================================

Learn how to connect AI to real services like Gmail, Google Sheets,
and research tools. This is where AI becomes really powerful!

What you'll learn:
    - How to use pre-built integrations
    - How to send emails through AI
    - How to do research with AI

Usage:
    python 6_integrations.py

Note: You'll need to connect your Gmail and Perplexity integrations first.
"""

import os
import requests
from dotenv import load_dotenv

# Load your API key from .env file
load_dotenv()

def send_email_example():
    """Show how AI can send emails through Gmail."""
    
    api_key = os.getenv('INCREDIBLE_API_KEY')
    user_id = os.getenv('USER_ID')
    
    if not api_key or not user_id:
        print("❌ Missing API credentials! Check your .env file")
        return False
    
    print("📧 Testing Gmail Integration")
    print("-" * 30)
    
    url = "https://api.incredible.one/v1/integrations/gmail/execute"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # Send a test email
    data = {
        "user_id": user_id,
        "feature_name": "GMAIL_SEND_EMAIL",
        "inputs": {
            "to": "test@example.com",  # Change this to your email
            "subject": "Test from Incredible API!",
            "body": "Hello! This email was sent by AI through the Incredible API. Pretty cool, right?"
        }
    }
    
    try:
        print("📤 Sending test email...")
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        print("✅ Email sent successfully!")
        print(f"📧 Sent to: {data['inputs']['to']}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Email failed: {e}")
        print("💡 Make sure Gmail integration is connected in your dashboard")
        return False

def research_example():
    """Show how AI can do research using Perplexity."""
    
    api_key = os.getenv('INCREDIBLE_API_KEY')
    user_id = os.getenv('USER_ID')
    
    if not api_key or not user_id:
        print("❌ Missing API credentials! Check your .env file")
        return False
    
    print("🔍 Testing Perplexity Research")
    print("-" * 30)
    
    url = "https://api.incredible.one/v1/integrations/perplexity/execute"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # Do some research
    research_question = "What are the latest trends in artificial intelligence 2024?"
    
    data = {
        "user_id": user_id,
        "feature_name": "PERPLEXITY_SEARCH",
        "inputs": {
            "query": research_question
        }
    }
    
    try:
        print(f"🔎 Researching: {research_question}")
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        research_answer = result.get('result', {}).get('answer', 'No answer found')
        
        print("✅ Research complete!")
        print()
        print("📄 Research Results:")
        print("-" * 40)
        print(research_answer[:300] + "..." if len(research_answer) > 300 else research_answer)
        print("-" * 40)
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Research failed: {e}")
        print("💡 Make sure Perplexity integration is connected in your dashboard")
        return False

def main():
    """Test different integrations."""
    print("🔌 Integrations - Connect AI to the World")
    print("=" * 60)
    print("Let's connect AI to real services!")
    print()
    
    # Test Gmail integration
    email_success = send_email_example()
    print()
    
    # Test Perplexity research
    research_success = research_example()
    print()
    
    # Summary
    print("📊 Integration Test Results:")
    print(f"   📧 Gmail: {'✅ Working' if email_success else '❌ Failed'}")
    print(f"   🔍 Research: {'✅ Working' if research_success else '❌ Failed'}")
    print()
    
    if email_success or research_success:
        print("🎉 Great! Your integrations are working!")
        print()
        print("🚀 What you can build now:")
        print("   - AI assistants that send emails")
        print("   - Research bots that gather information")
        print("   - Automated workflows combining multiple services")
        print("   - Smart notifications and alerts")
    else:
        print("⚠️  No integrations working yet. Here's how to fix it:")
        print()
        print("🔧 Setup Steps:")
        print("   1. Go to your Incredible API dashboard")
        print("   2. Navigate to the Integrations section")
        print("   3. Connect Gmail (requires OAuth)")
        print("   4. Connect Perplexity (requires API key)")
        print("   5. Run this script again")
    
    print()
    print("🏁 Tutorial Complete!")
    print("You've learned all the Incredible API basics:")
    print("   ✅ Basic chat completion")
    print("   ✅ Multiple models")
    print("   ✅ Conversations") 
    print("   ✅ Streaming responses")
    print("   ✅ Function calling")
    print("   ✅ Service integrations")
    print()
    print("🚀 Ready to build something amazing!")

if __name__ == "__main__":
    main()