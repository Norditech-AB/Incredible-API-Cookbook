#!/usr/bin/env python3
"""
Function Calling - Give AI Special Powers
=========================================

Learn how to give AI special abilities by letting it call functions.
This lets AI do things like calculate math, get weather, or access databases.

What you'll learn:
    - How to create functions AI can use
    - How AI decides when to call functions
    - How to handle function results

Usage:
    python 5_function_calling.py
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load your API key from .env file
load_dotenv()

# Our special functions that AI can use
def add_numbers(a, b):
    """Add two numbers together."""
    result = a + b
    print(f"🧮 Calculating: {a} + {b} = {result}")
    return result

def get_current_weather(city):
    """Get the current weather for a city (demo function)."""
    # This is a demo - real function would call a weather API
    weather_data = {
        "New York": "Sunny, 72°F",
        "London": "Cloudy, 60°F", 
        "Tokyo": "Rainy, 68°F",
        "Paris": "Partly cloudy, 65°F"
    }
    
    weather = weather_data.get(city, f"Weather data not available for {city}")
    print(f"🌤️  Getting weather for {city}: {weather}")
    return weather

# Tell AI what functions are available
available_functions = [
    {
        "name": "add_numbers",
        "description": "Add two numbers together",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "get_current_weather", 
        "description": "Get the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    }
]

def call_ai_with_functions(message):
    """Send a message to AI that can use functions."""
    
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
        "messages": [{"role": "user", "content": message}],
        "functions": available_functions  # Give AI access to our functions
    }
    
    print(f"💬 You: {message}")
    print("🤔 AI is thinking...")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        
        # Check if AI wants to call a function
        ai_response = result['result']['response'][0]
        
        if 'function_call' in ai_response:
            # AI wants to call a function!
            function_call = ai_response['function_call']
            function_name = function_call['name']
            function_args = json.loads(function_call['arguments'])
            
            print(f"🔧 AI wants to use function: {function_name}")
            print(f"📋 With arguments: {function_args}")
            
            # Call the actual function
            if function_name == "add_numbers":
                function_result = add_numbers(function_args['a'], function_args['b'])
            elif function_name == "get_current_weather":
                function_result = get_current_weather(function_args['city'])
            else:
                function_result = "Unknown function"
            
            # Now ask AI to respond using the function result
            data["messages"].extend([
                {"role": "assistant", "content": None, "function_call": function_call},
                {"role": "function", "name": function_name, "content": str(function_result)}
            ])
            
            # Get AI's final response
            response = requests.post(url, json=data, headers=headers)
            result = response.json()
            final_response = result['result']['response'][0]['content']
            
            print(f"🤖 AI: {final_response}")
            return final_response
            
        else:
            # AI responded normally without using functions
            normal_response = ai_response['content']
            print(f"🤖 AI: {normal_response}")
            return normal_response
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Test function calling with different questions."""
    print("🔧 Function Calling - Give AI Special Powers")
    print("=" * 60)
    print("AI now has access to special functions!")
    print()
    
    # Test 1: Math calculation
    print("📊 Test 1: Math Question")
    print("-" * 30)
    call_ai_with_functions("What is 25 + 17?")
    
    print()
    
    # Test 2: Weather question  
    print("🌤️  Test 2: Weather Question")
    print("-" * 30)
    call_ai_with_functions("What's the weather like in New York?")
    
    print()
    
    # Test 3: Regular question (no function needed)
    print("💭 Test 3: Regular Question")
    print("-" * 30)
    call_ai_with_functions("What color is the sky?")
    
    print()
    print("🎉 Function calling tests complete!")
    print()
    print("🔍 What happened:")
    print("   - AI automatically chose when to use functions")
    print("   - Functions gave AI access to real calculations and data")
    print("   - AI used function results to give better answers")
    print()
    print("💡 Next step: Try 6_gmail_integration.py to send emails with AI")

if __name__ == "__main__":
    main()