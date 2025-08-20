#!/usr/bin/env python3
"""
Gmail Integration - Send Emails with AI
=======================================

Learn how to connect AI to Gmail so it can send emails for you.
This is perfect for building AI assistants that can communicate!

What you'll learn:
    - How to connect Gmail to your AI
    - How to send emails through the API
    - Real-world email automation

Usage:
    python 6_gmail_integration.py

Note: You'll need to connect Gmail integration in your dashboard first.
"""

import os
import requests
from dotenv import load_dotenv

# Load your API key from .env file
load_dotenv()

def send_simple_email():
    """Send a simple test email through Gmail."""
    
    api_key = os.getenv('INCREDIBLE_API_KEY')
    user_id = os.getenv('USER_ID')
    
    if not api_key or not user_id:
        print("❌ Missing API credentials! Check your .env file")
        return False
    
    print("📧 Sending Email Through Gmail")
    print("-" * 40)
    
    # Gmail integration endpoint
    url = "https://api.incredible.one/v1/integrations/gmail/execute"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # Email details
    recipient = input("📬 Enter email to send to (or press Enter for test@example.com): ").strip()
    if not recipient:
        recipient = "test@example.com"
    
    data = {
        "user_id": user_id,
        "feature_name": "GMAIL_SEND_EMAIL",
        "inputs": {
            "to": recipient,
            "subject": "Hello from Incredible API! 🚀",
            "body": """Hi there!

This email was sent by AI through the Incredible API. 

Pretty cool, right? This shows how AI can:
- Send personalized emails
- Automate communication
- Integrate with your favorite services

Best regards,
Your AI Assistant 🤖

---
Powered by Incredible API
"""
        }
    }
    
    try:
        print(f"📤 Sending email to: {recipient}")
        print("⏳ Please wait...")
        
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        
        print("✅ Email sent successfully!")
        print(f"📧 Recipient: {recipient}")
        print(f"📝 Subject: {data['inputs']['subject']}")
        print()
        print("🎉 Your AI can now send emails!")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Email failed to send")
        print(f"🔍 Error: {e}")
        print()
        print("🔧 Troubleshooting:")
        print("   1. Make sure Gmail integration is connected in your dashboard")
        print("   2. Check your internet connection") 
        print("   3. Verify your email address is valid")
        print("   4. Try again in a few minutes")
        return False

def show_gmail_setup_help():
    """Show users how to set up Gmail integration."""
    print("🔧 Gmail Integration Setup")
    print("-" * 40)
    print()
    print("To use Gmail integration, you need to:")
    print()
    print("1. 🌐 Go to your Incredible API dashboard")
    print("   → https://incredible.one/dashboard")
    print()
    print("2. 🔌 Find the 'Integrations' section")
    print()
    print("3. 📧 Click 'Connect Gmail'")
    print("   → This will open Google's permission page")
    print()
    print("4. ✅ Grant permissions to send emails")
    print("   → Google will ask for permission to send emails on your behalf")
    print()
    print("5. 🔄 Come back and run this script again")
    print()
    print("💡 Why OAuth? Gmail uses OAuth for security - this means Google")
    print("   confirms you really want to let the API send emails for you.")

def main():
    """Test Gmail integration."""
    print("📧 Gmail Integration - AI Email Assistant")
    print("=" * 60)
    print("Let's teach AI to send emails!")
    print()
    
    # Try to send an email
    success = send_simple_email()
    
    print()
    
    if success:
        print("🎊 Congratulations!")
        print("Your AI can now send emails! Here are some ideas:")
        print()
        print("🚀 What you can build:")
        print("   📬 AI customer service that sends responses")
        print("   📅 Meeting schedulers that send invites")
        print("   🔔 Notification systems that email updates")
        print("   📊 Report generators that email summaries")
        print("   💌 Personalized marketing campaigns")
    else:
        print("⚠️  Gmail integration not set up yet")
        print()
        show_gmail_setup_help()
    
    print()
    print("💡 Next step: Try 7_perplexity_integration.py to learn research!")

if __name__ == "__main__":
    main()
