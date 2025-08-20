#!/usr/bin/env python3
"""
Basic Chat Completion Example
============================

This is the simplest example of using the Incredible API chat completion endpoint.
Learn the fundamentals before moving to advanced examples.

Usage:
    python 1_basic_chat.py

What you'll learn:
    - How to make basic chat completion requests
    - Handling API responses
    - Using different models
"""

import os
import requests
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

def basic_chat_example():
    """Simple chat completion example."""
    print("💬 Basic Chat Completion Example")
    print("=" * 40)
    
    # Configuration
    api_key = os.getenv('INCREDIBLE_API_KEY')
    base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
    
    if not api_key:
        print("❌ Error: INCREDIBLE_API_KEY not found in environment")
        print("💡 Copy .env.example to .env and add your API key")
        return False
    
    # API endpoint
    url = f"{base_url}/v1/chat-completion"
    
    # Headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # Chat completion request
    data = {
        "model": "small-1",              # Model to use
        "stream": False,                     # Non-streaming for simplicity
        "system": "You are a helpful AI assistant.",  # System prompt
        "messages": [                        # Conversation history
            {
                "role": "user",
                "content": "Hello! Can you explain what APIs are in simple terms?"
            }
        ]
    }
    
    print("🚀 Sending chat completion request...")
    print(f"📤 Request: {data['messages'][0]['content']}")
    
    try:
        # Make the API request
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        assistant_response = parse_api_response(result)
        
        print(f"\n💡 Response:")
        print("-" * 40)
        print(assistant_response)
        print("-" * 40)
        
        print("✅ Chat completion successful!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = e.response.json()
                print(f"Error details: {error_detail}")
            except:
                print(f"Response text: {e.response.text}")
        return False

def multiple_models_example():
    """Test different models available."""
    print("\n🔄 Testing Multiple Models")
    print("=" * 40)
    
    # Configuration
    api_key = os.getenv('INCREDIBLE_API_KEY')
    base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
    
    # Different models to test
    models_to_test = [
        "small-1",
        "big-1", 
        "huge-1",
        "tiny-1"
    ]
    
    # Simple question
    test_message = "What is 2+2? Just give me the number."
    
    for model in models_to_test:
        print(f"\n🤖 Testing model: {model}")
        
        url = f"{base_url}/v1/chat-completion"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        data = {
            "model": model,
            "stream": False,
            "messages": [{"role": "user", "content": test_message}]
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            assistant_response = parse_api_response(result)
            
            print(f"✅ {model}: {assistant_response.strip()}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ {model}: Failed - {e}")

def conversation_example():
    """Example with multi-turn conversation."""
    print("\n💬 Multi-turn Conversation Example")
    print("=" * 40)
    
    # Configuration
    api_key = os.getenv('INCREDIBLE_API_KEY')
    base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
    
    url = f"{base_url}/v1/chat-completion"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # Build a conversation
    conversation = [
        {"role": "user", "content": "What's the capital of France?"},
    ]
    
    # First request
    data = {
        "model": "small-1",
        "stream": False,
        "system": "You are a knowledgeable geography assistant.",
        "messages": conversation
    }
    
    print("👤 User: What's the capital of France?")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        first_response = parse_api_response(result)
        
        print(f"🤖 Assistant: {first_response}")
        
        # Add assistant response to conversation
        conversation.append({"role": "assistant", "content": first_response})
        
        # Follow-up question
        conversation.append({"role": "user", "content": "What's the population of that city?"})
        
        print(f"\n👤 User: What's the population of that city?")
        
        # Second request with full conversation history
        data["messages"] = conversation
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            second_response = parse_api_response(result)
            
            print(f"🤖 Assistant: {second_response}")
            
            print("\n✅ Multi-turn conversation completed!")
            return True
            
        except requests.exceptions.RequestException as second_error:
            print(f"❌ Follow-up question failed: {second_error}")
            return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Conversation error: {e}")
        return False

def main():
    """Run all basic chat examples."""
    print("🚀 Incredible API - Getting Started with Chat Completion")
    print("=" * 60)
    
    # Example 1: Basic chat
    success1 = basic_chat_example()
    
    # Example 2: Multiple models  
    if success1:
        multiple_models_example()
    
    # Example 3: Conversation
    if success1:
        conversation_example()
    
    print(f"\n{'='*60}")
    print("🎉 Basic Examples Complete!")
    print("\n💡 Next Steps:")
    print("   - Try 2_streaming_chat.py for streaming responses")
    print("   - Try 3_function_calling.py for function calling")
    print("   - Try 4_integrations.py for using integrations")
    print("   - Explore advanced examples in other folders")

if __name__ == "__main__":
    main()
