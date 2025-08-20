#!/usr/bin/env python3
"""
Conversations - Chat Back and Forth with AI
===========================================

Learn how to have a real conversation with AI where it remembers
what you talked about before.

What you'll learn:
    - How to build conversations
    - How AI remembers previous messages
    - How to ask follow-up questions

Usage:
    python 3_conversation.py
"""

import os
import requests
from dotenv import load_dotenv

# Load your API key from .env file
load_dotenv()

def send_message(conversation_history):
    """Send a conversation to AI and get a response."""
    
    api_key = os.getenv('INCREDIBLE_API_KEY')
    if not api_key:
        print("❌ Missing API key! Check your .env file")
        return None
    
    url = "https://api.incredible.one/v1/chat-completion"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    data = {
        "model": "small-1",
        "stream": False,
        "messages": conversation_history  # Send entire conversation
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        ai_reply = result['result']['response'][0]['content']
        
        return ai_reply
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Have a conversation with AI."""
    print("💬 Having a Conversation with AI")
    print("=" * 50)
    print("Let's ask AI something, then ask a follow-up question...")
    print()
    
    # Start the conversation
    conversation = []
    
    # First question
    first_question = "What's the capital of France?"
    conversation.append({"role": "user", "content": first_question})
    
    print(f"👤 You: {first_question}")
    
    # Get AI's response
    ai_response = send_message(conversation)
    if not ai_response:
        print("❌ Failed to get response")
        return
    
    print(f"🤖 AI: {ai_response}")
    
    # Add AI's response to conversation so it remembers
    conversation.append({"role": "assistant", "content": ai_response})
    
    print()
    print("Now let's ask a follow-up question...")
    print("(AI should remember we were talking about France)")
    print()
    
    # Follow-up question (notice we don't mention France again!)
    follow_up = "What's the population of that city?"
    conversation.append({"role": "user", "content": follow_up})
    
    print(f"👤 You: {follow_up}")
    
    # Get AI's response to follow-up
    ai_response2 = send_message(conversation)
    if not ai_response2:
        print("❌ Failed to get response")
        return
    
    print(f"🤖 AI: {ai_response2}")
    
    print()
    print("🎉 Conversation complete!")
    print("✨ Notice how AI remembered we were talking about Paris!")
    print()
    print("🔍 How it works:")
    print("   - Each message gets added to the conversation history")
    print("   - AI sees the entire conversation every time")
    print("   - This is how it 'remembers' what you talked about")
    print()
    print("💡 Next step: Try 4_streaming_chat.py to see real-time responses")

if __name__ == "__main__":
    main()
