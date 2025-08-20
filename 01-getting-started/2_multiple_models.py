#!/usr/bin/env python3
"""
Multiple Models - Try Different AI Models
=========================================

Learn how to use different AI models available in Incredible API.
Each model has different capabilities and speeds.

What you'll learn:
    - How to choose different AI models
    - What models are available
    - How models respond differently

Usage:
    python 2_multiple_models.py
"""

import os
import requests
from dotenv import load_dotenv

# Load your API key from .env file
load_dotenv()

def test_model(model_name, question):
    """Test a specific AI model with a question."""
    
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
        "model": model_name,
        "stream": False,
        "messages": [{"role": "user", "content": question}]
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        ai_reply = result['result']['response'][0]['content']
        
        print(f"✅ {model_name}: {ai_reply}")
        return ai_reply
        
    except requests.exceptions.RequestException as e:
        print(f"❌ {model_name}: Not available yet ({e})")
        return None

def main():
    """Test different AI models."""
    print("🤖 Testing Different AI Models")
    print("=" * 50)
    print("Let's see how different AI models respond...")
    print()
    
    # Available models
    models = {
        "small-1": "✅ Available now - Fast and efficient",
        "tiny-1": "🔜 Coming soon - Ultra fast",
        "big-1": "🔜 Coming soon - More powerful", 
        "huge-1": "🔜 Coming soon - Most advanced"
    }
    
    # Show what models exist
    print("📋 Available Models:")
    for model, status in models.items():
        print(f"   {model}: {status}")
    print()
    
    # Test question
    question = "What's 5 + 3? Just give me the number."
    print(f"🧪 Testing with question: '{question}'")
    print()
    
    # Test each model
    for model_name in models.keys():
        test_model(model_name, question)
    
    print()
    print("🎉 Model testing complete!")
    print()
    print("💡 Next step: Try 3_conversation.py to learn about conversations")

if __name__ == "__main__":
    main()
