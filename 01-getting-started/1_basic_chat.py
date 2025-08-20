#!/usr/bin/env python3
"""
Basic Chat Completion - Your First API Call
===========================================

This is your first step with the Incredible API!
Learn how to send a simple message and get a response.

What you'll learn:
    - How to make your first API call
    - How to get a response from AI
    - How the API works

Usage:
    python 1_basic_chat.py
"""

import os
import requests
from dotenv import load_dotenv

# Load your API key from .env file
load_dotenv()

def get_ai_response(message):
    """Send a message to AI and get a response back."""
    
    # Your API credentials  
    api_key = os.getenv('INCREDIBLE_API_KEY')
    
    if not api_key:
        print("❌ Missing API key!")
        print("💡 Copy .env.example to .env and add your API key")
        return None
    
    # Where to send the request
    url = "https://api.incredible.one/v1/chat-completion"
    
    # Tell the API who you are
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # What to send to the AI
    data = {
        "model": "small-1",                    # Which AI model to use
        "stream": False,                       # Get full response at once
        "messages": [                          # Your conversation
            {
                "role": "user",                # You are the user
                "content": message             # Your message
            }
        ]
    }
    
    print("🚀 Sending your message to AI...")
    print(f"💬 You: {message}")
    
    try:
        # Send the request
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        # Get the response
        result = response.json()
        
        # Extract AI's reply (this handles the API response format)
        ai_reply = result['result']['response'][0]['content']
        
        print(f"🤖 AI: {ai_reply}")
        print("✅ Success! You've made your first API call!")
        
        return ai_reply
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Something went wrong: {e}")
        return None

def main():
    """Run the basic chat example."""
    print("🎉 Welcome to Incredible API!")
    print("=" * 50)
    print("Let's make your first API call...")
    print()
    
    # Send a simple message
    message = "Hello! Can you say hi back to me?"
    
    ai_response = get_ai_response(message)
    
    if ai_response:
        print()
        print("🎊 Congratulations!")
        print("You just had your first conversation with AI!")
        print()
        print("💡 Next step: Try 2_multiple_models.py to test different AI models")
    else:
        print()
        print("😔 Don't worry, let's fix this:")
        print("1. Check your internet connection")
        print("2. Make sure your API key is correct in .env file")
        print("3. Try again!")

if __name__ == "__main__":
    main()