#!/usr/bin/env python3
"""
🌟 Incredible API - Hello World!
=================================

This is the simplest possible example of using the Incredible API.
Even if you've never written code before, you can understand this!

What this example does:
• Sends a simple question to our AI
• Gets a response back
• Shows you both the question and answer

It's like having a conversation with a really smart assistant!
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def hello_incredible():
    """
    The simplest possible function to talk to Incredible AI.
    
    Think of this like sending a text message to a really smart friend
    who knows everything and can help you with anything!
    """
    
    print("🌟 Welcome to Incredible API - Hello World!")
    print("=" * 50)
    
    # Step 1: Get your API key (like showing your ID card)
    api_key = os.getenv('INCREDIBLE_API_KEY')
    if not api_key:
        print("❌ Oops! You need to set your INCREDIBLE_API_KEY first.")
        print("💡 Check the README.md for setup instructions!")
        return
    
    # Step 2: Prepare what you want to ask the AI
    question = "Hello! What can you help me with?"
    
    print(f"👤 You asked: {question}")
    print("🤔 Thinking...")
    
    # Step 3: Set up the request (like addressing an envelope)
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Step 4: Package your question
    data = {
        "model": "small-1",           # Which AI brain to use
        "messages": [
            {
                "role": "user",       # You are the user
                "content": question   # This is what you're asking
            }
        ]
    }
    
    try:
        # Step 5: Send your question to the AI (like sending a message)
        response = requests.post(
            'https://api.incredible.one/v1/chat-completion',
            headers=headers,
            json=data,
            timeout=30
        )
        
        # Step 6: Check if everything went well
        if response.status_code == 200:
            # Success! The AI responded
            result = response.json()
            
            # Extract the AI's response (dig into the nested response)
            ai_response = result['result']['response'][0]['content']
            
            print(f"🤖 AI replied: {ai_response}")
            print("\n✅ Success! You just had your first conversation with Incredible AI!")
            
        else:
            print(f"❌ Something went wrong. Error code: {response.status_code}")
            print(f"Error message: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        print("💡 Check your internet connection!")


def what_just_happened():
    """
    Let's explain what just happened in simple terms!
    """
    print("\n" + "=" * 50)
    print("🤔 WHAT JUST HAPPENED?")
    print("=" * 50)
    
    print("""
Think of the Incredible API like having a conversation with the smartest
person in the world, but through the internet:

1. 📝 You wrote a question: "Hello! What can you help me with?"

2. 📦 Your computer packaged that question with your API key
   (like putting your name on a letter)

3. 🚀 It sent the package to our AI servers in the cloud

4. 🧠 Our AI (called 'small-1') read your question and thought about it

5. 💬 The AI wrote back a helpful response

6. 📬 Your computer received the response and showed it to you

The whole thing happened in just a few seconds!
""")


def why_does_this_matter():
    """
    Why is this simple example actually amazing?
    """
    print("\n" + "=" * 50)
    print("🚀 WHY DOES THIS MATTER?")
    print("=" * 50)
    
    print("""
This simple "Hello World" example is the foundation for incredible things:

🤖 **Instant AI Assistant**: You now have access to a super-smart AI that can:
   • Answer any question
   • Help with work tasks
   • Write content for you
   • Solve problems
   • And much more!

🔗 **Building Blocks**: This same basic pattern can:
   • Send emails automatically
   • Research topics online
   • Organize your calendar  
   • Create reports
   • Build entire applications

💡 **No AI Expertise Needed**: You don't need to:
   • Train your own AI models
   • Manage complex servers
   • Worry about AI infrastructure
   • Be a machine learning expert

🎯 **What's Next**: Try changing the question in this file to:
   • "What's the weather like?" 
   • "Write me a short poem"
   • "Help me plan my day"
   • "Explain quantum physics simply"

The possibilities are endless!
""")


if __name__ == "__main__":
    # Run the hello world example
    hello_incredible()
    
    # Explain what happened
    what_just_happened()
    
    # Show why it matters
    why_does_this_matter()
    
    print("\n🎉 Ready to explore more? Check out the other tutorial files!")
    print("Next up: Try running 1_basic_chat.py for more examples!")
