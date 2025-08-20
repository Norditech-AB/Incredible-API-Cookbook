#!/usr/bin/env python3
"""
Streaming Chat Completion Example
================================

Learn how to handle streaming responses from the Incredible API.
Streaming is the default mode and provides real-time response generation.

Usage:
    python 2_streaming_chat.py

What you'll learn:
    - How streaming responses work
    - Processing Server-Sent Events (SSE)
    - Building real-time chat applications
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

def streaming_chat_example():
    """Demonstrate streaming chat completion."""
    print("📡 Streaming Chat Completion Example")
    print("=" * 40)
    
    # Configuration
    api_key = os.getenv('INCREDIBLE_API_KEY')
    base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
    
    if not api_key:
        print("❌ Error: INCREDIBLE_API_KEY not found in environment")
        return False
    
    # API endpoint
    url = f"{base_url}/v1/chat-completion"
    
    # Headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # Streaming request (stream=True is default)
    data = {
        "model": "small-1",
        "stream": True,  # Enable streaming
        "system": "You are a helpful assistant. Be concise but informative.",
        "messages": [
            {
                "role": "user",
                "content": "Explain how streaming responses work in APIs. Be detailed but clear."
            }
        ]
    }
    
    print("🚀 Sending streaming request...")
    print(f"📤 Question: {data['messages'][0]['content']}")
    print("\n💬 Streaming Response:")
    print("-" * 40)
    
    try:
        # Make streaming request
        response = requests.post(url, json=data, headers=headers, stream=True)
        response.raise_for_status()
        
        full_response = ""
        
        # Process Server-Sent Events
        for line in response.iter_lines(decode_unicode=True):
            if line.startswith('data: '):
                # Extract JSON data
                data_part = line[6:]  # Remove 'data: ' prefix
                
                try:
                    chunk_data = json.loads(data_part)
                    
                    # Handle the nested streaming format: {"content": {"type": "...", "content": "..."}}
                    if isinstance(chunk_data, dict) and 'content' in chunk_data:
                        inner_content = chunk_data['content']
                        
                        # Check for completion
                        if inner_content == '[DONE]':
                            break
                        
                        # Handle nested content object
                        if isinstance(inner_content, dict):
                            chunk_type = inner_content.get('type', '')
                            actual_content = inner_content.get('content', '')
                            
                            # For now, include all content types (including thinking)
                            # Later you can filter by: if chunk_type != 'thinking_chunk':
                            if actual_content and isinstance(actual_content, str):
                                print(actual_content, end='', flush=True)
                                full_response += actual_content
                        
                        # Handle simple string content
                        elif isinstance(inner_content, str):
                            print(inner_content, end='', flush=True)
                            full_response += inner_content
                    
                except json.JSONDecodeError:
                    # Skip invalid JSON lines
                    continue
        
        print("\n" + "-" * 40)
        print("✅ Streaming completed!")
        print(f"📊 Total characters received: {len(full_response)}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Streaming error: {e}")
        return False

def compare_streaming_vs_non_streaming():
    """Compare streaming vs non-streaming responses."""
    print("\n⚖️  Streaming vs Non-Streaming Comparison")
    print("=" * 50)
    
    # Configuration
    api_key = os.getenv('INCREDIBLE_API_KEY')
    base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
    
    url = f"{base_url}/v1/chat-completion"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    question = "Write a short poem about programming."
    
    base_data = {
        "model": "small-1",
        "system": "You are a creative assistant.",
        "messages": [{"role": "user", "content": question}]
    }
    
    # Test 1: Non-streaming
    print("📦 1. Non-Streaming Response:")
    print("-" * 30)
    
    import time
    start_time = time.time()
    
    non_streaming_data = {**base_data, "stream": False}
    
    try:
        response = requests.post(url, json=non_streaming_data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        non_streaming_response = parse_api_response(result)
        non_streaming_time = time.time() - start_time
        
        print(non_streaming_response)
        print(f"\n⏱️  Non-streaming time: {non_streaming_time:.2f}s")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Non-streaming error: {e}")
        return False
    
    # Test 2: Streaming
    print(f"\n📡 2. Streaming Response:")
    print("-" * 30)
    
    start_time = time.time()
    streaming_data = {**base_data, "stream": True}
    
    try:
        response = requests.post(url, json=streaming_data, headers=headers, stream=True)
        response.raise_for_status()
        
        streaming_response = ""
        first_chunk_time = None
        
        for line in response.iter_lines(decode_unicode=True):
            if line.startswith('data: '):
                data_part = line[6:]
                
                try:
                    chunk_data = json.loads(data_part)
                    
                    # Handle the nested streaming format: {"content": {"type": "...", "content": "..."}}
                    if isinstance(chunk_data, dict) and 'content' in chunk_data:
                        inner_content = chunk_data['content']
                        
                        # Check for completion
                        if inner_content == '[DONE]':
                            break
                        
                        # Handle nested content object
                        if isinstance(inner_content, dict):
                            chunk_type = inner_content.get('type', '')
                            actual_content = inner_content.get('content', '')
                            
                            # For comparison, include all content types
                            if actual_content and isinstance(actual_content, str):
                                if first_chunk_time is None:
                                    first_chunk_time = time.time() - start_time
                                
                                print(actual_content, end='', flush=True)
                                streaming_response += actual_content
                        
                        # Handle simple string content
                        elif isinstance(inner_content, str):
                            if first_chunk_time is None:
                                first_chunk_time = time.time() - start_time
                            print(inner_content, end='', flush=True)
                            streaming_response += inner_content
                    
                except json.JSONDecodeError:
                    continue
        
        total_streaming_time = time.time() - start_time
        
        print(f"\n\n⏱️  First chunk time: {first_chunk_time:.2f}s")
        print(f"⏱️  Total streaming time: {total_streaming_time:.2f}s")
        
        # Comparison
        print(f"\n📊 Comparison:")
        print(f"   Non-streaming: Wait {non_streaming_time:.2f}s, then get full response")
        print(f"   Streaming: First content in {first_chunk_time:.2f}s, complete in {total_streaming_time:.2f}s")
        print(f"\n💡 Streaming provides better user experience for longer responses!")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Streaming error: {e}")
        return False

def custom_system_prompt_example():
    """Example with custom system prompts."""
    print("\n🎭 Custom System Prompt Example")
    print("=" * 40)
    
    # Configuration
    api_key = os.getenv('INCREDIBLE_API_KEY')
    base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
    
    url = f"{base_url}/v1/chat-completion"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # Custom system prompts
    system_prompts = [
        {
            "name": "Pirate Assistant",
            "prompt": "You are a helpful pirate assistant. Always talk like a pirate and end responses with 'Arr!'",
            "question": "How do I install Python packages?"
        },
        {
            "name": "Technical Expert",
            "prompt": "You are a senior software engineer. Give detailed, technical explanations with code examples.",
            "question": "How do I install Python packages?"
        },
        {
            "name": "Beginner-Friendly",
            "prompt": "You are teaching programming to complete beginners. Use simple language and avoid jargon.",
            "question": "How do I install Python packages?"
        }
    ]
    
    for example in system_prompts:
        print(f"\n🎯 {example['name']}:")
        print(f"System: {example['prompt']}")
        print(f"Question: {example['question']}")
        print("Response:", end="")
        
        data = {
            "model": "small-1",
            "stream": False,
            "system": example['prompt'],
            "messages": [{"role": "user", "content": example['question']}]
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            assistant_response = parse_api_response(result)
            
            print(f" {assistant_response}\n")
            
        except requests.exceptions.RequestException as e:
            print(f" ❌ Error: {e}\n")
    
    print("✅ System prompt examples completed!")

def main():
    """Run all basic chat examples."""
    print("🚀 Incredible API - Basic Chat Completion")
    print("=" * 60)
    
    # Run examples
    success = streaming_chat_example()
    
    if success:
        compare_streaming_vs_non_streaming()
        custom_system_prompt_example()
    
    print(f"\n{'='*60}")
    print("🎓 What you learned:")
    print("   • How to make basic chat completion requests")
    print("   • Difference between streaming and non-streaming")
    print("   • How to use custom system prompts")
    print("   • How to handle API responses and errors")
    print("\n➡️  Next: Try 3_function_calling.py to learn about function calling!")

if __name__ == "__main__":
    main()
