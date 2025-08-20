#!/usr/bin/env python3
"""
Streaming Chat - See AI Respond in Real-Time
============================================

Learn how to get AI responses word-by-word as they're generated,
just like in ChatGPT where you see text appear gradually.

What you'll learn:
    - How to get real-time streaming responses
    - The difference between streaming and regular responses
    - How to handle streaming data

Usage:
    python 4_streaming_chat.py
"""

import os
import requests
from dotenv import load_dotenv
import json

# Load your API key from .env file
load_dotenv()

def get_regular_response(message):
    """Get a complete response all at once (non-streaming)."""
    
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
        "stream": False,  # No streaming - get full response
        "messages": [{"role": "user", "content": message}]
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

def get_streaming_response(message):
    """Get response word-by-word in real-time (streaming)."""
    
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
        "stream": True,  # Enable streaming!
        "messages": [{"role": "user", "content": message}]
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, stream=True)
        response.raise_for_status()
        
        full_response = ""
        
        # Read the response piece by piece
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                
                # Skip lines that don't have data
                if not line.startswith('data: '):
                    continue
                
                # Get the actual data
                data_content = line[6:]  # Remove 'data: ' prefix
                
                # Check if we're done
                if data_content.strip() == '[DONE]':
                    break
                
                try:
                    # Parse the JSON data
                    chunk_data = json.loads(data_content)
                    
                    # Extract the text content
                    if 'content' in chunk_data and isinstance(chunk_data['content'], dict):
                        if 'content' in chunk_data['content']:
                            chunk_text = chunk_data['content']['content']
                            if chunk_text:
                                print(chunk_text, end='', flush=True)
                                full_response += chunk_text
                
                except json.JSONDecodeError:
                    # Skip lines that aren't valid JSON
                    continue
        
        return full_response
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Compare streaming vs non-streaming responses."""
    print("🌊 Streaming vs Regular Responses")
    print("=" * 50)
    
    # The question we'll ask
    question = "Explain how computers work in simple terms, using about 50 words."
    
    print(f"💬 Question: {question}")
    print()
    
    # First: Get regular response
    print("📦 Regular response (all at once):")
    print("-" * 40)
    regular_response = get_regular_response(question)
    if regular_response:
        print(regular_response)
    print("-" * 40)
    
    print()
    print("⏱️  (Notice how the whole answer appeared instantly)")
    print()
    
    # Then: Get streaming response  
    print("🌊 Streaming response (word by word):")
    print("-" * 40)
    streaming_response = get_streaming_response(question)
    print()
    print("-" * 40)
    
    if streaming_response:
        print()
        print("🎉 Streaming complete!")
        print("✨ Notice how the text appeared gradually, like typing!")
        print()
        print("🔍 Why use streaming?")
        print("   - Users see responses immediately")
        print("   - Better user experience for long responses")
        print("   - Feels more interactive and alive")
    
    print()
    print("💡 Next step: Try 5_function_calling.py to extend AI with functions")

if __name__ == "__main__":
    main()