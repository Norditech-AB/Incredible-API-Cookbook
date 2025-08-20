#!/usr/bin/env python3
"""
Function Calling Example
=======================

Learn how to use function calling with the Incredible API.
Functions allow the AI to perform actions and get real data.

Usage:
    python 3_function_calling.py

What you'll learn:
    - How to define functions for the AI
    - Function calling workflow
    - Handling function results
"""

import os
import requests
import json
import math
from datetime import datetime
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

def get_current_time():
    """Get the current time."""
    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": "Local"
    }

def calculate_circle_area(radius):
    """Calculate the area of a circle given its radius."""
    if radius <= 0:
        return {"error": "Radius must be positive"}
    
    area = math.pi * radius ** 2
    return {
        "radius": radius,
        "area": round(area, 2),
        "formula": "π × radius²"
    }

def get_weather_info(city):
    """Mock weather function (in real apps, you'd call a weather API)."""
    # This is a mock function for demonstration
    mock_weather = {
        "new york": {"temp": "72°F", "condition": "Sunny", "humidity": "45%"},
        "london": {"temp": "15°C", "condition": "Cloudy", "humidity": "80%"},
        "tokyo": {"temp": "25°C", "condition": "Partly Cloudy", "humidity": "60%"},
        "paris": {"temp": "18°C", "condition": "Rainy", "humidity": "85%"}
    }
    
    city_lower = city.lower()
    if city_lower in mock_weather:
        return mock_weather[city_lower]
    else:
        return {"error": f"Weather data not available for {city}"}

def simple_function_calling_example():
    """Basic function calling example."""
    print("🛠️  Simple Function Calling Example")
    print("=" * 40)
    
    # Configuration
    api_key = os.getenv('INCREDIBLE_API_KEY')
    base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
    
    if not api_key:
        print("❌ Error: INCREDIBLE_API_KEY not found in environment")
        return False
    
    url = f"{base_url}/v1/chat-completion"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # Define functions in the format expected by the API
    functions = [
        {
            "name": "get_current_time",
            "description": "Get the current date and time",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "calculate_circle_area", 
            "description": "Calculate the area of a circle given its radius",
            "parameters": {
                "type": "object",
                "properties": {
                    "radius": {
                        "type": "number",
                        "description": "The radius of the circle"
                    }
                },
                "required": ["radius"]
            }
        }
    ]
    
    # Request that should trigger function calling
    data = {
        "model": "small-1",
        "stream": False,
        "system": "You are a helpful assistant with access to various tools. Use the available functions when needed to provide accurate information.",
        "functions": functions,
        "messages": [
            {
                "role": "user", 
                "content": "What time is it right now? Also, what's the area of a circle with radius 5?"
            }
        ]
    }
    
    print("🚀 Sending function calling request...")
    print(f"📤 Question: {data['messages'][0]['content']}")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        assistant_response = parse_api_response(result)
        
        print(f"\n💡 AI Response:")
        print("-" * 40)
        print(assistant_response)
        print("-" * 40)
        
        print("✅ Function calling example completed!")
        print("\n💡 Note: The AI should have called both functions and included their results in the response")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Function calling error: {e}")
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = e.response.json()
                print(f"Error details: {error_detail}")
            except:
                print(f"Response text: {e.response.text}")
        return False

def weather_function_example():
    """Example with a more practical function."""
    print("\n🌤️  Weather Function Example")
    print("=" * 40)
    
    # Configuration
    api_key = os.getenv('INCREDIBLE_API_KEY')
    base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
    
    url = f"{base_url}/v1/chat-completion"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # Define weather function
    weather_function = {
        "name": "get_weather_info",
        "description": "Get current weather information for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city to get weather for"
                }
            },
            "required": ["city"]
        }
    }
    
    # Request weather for multiple cities
    data = {
        "model": "small-1",
        "stream": False,
        "system": "You are a helpful weather assistant. Use the weather function to get current conditions and provide helpful advice.",
        "functions": [weather_function],
        "messages": [
            {
                "role": "user",
                "content": "What's the weather like in New York and London? Should I bring an umbrella?"
            }
        ]
    }
    
    print("🌍 Asking about weather in multiple cities...")
    print(f"📤 Question: {data['messages'][0]['content']}")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        assistant_response = parse_api_response(result)
        
        print(f"\n🌤️  Weather Response:")
        print("-" * 40)
        print(assistant_response)
        print("-" * 40)
        
        print("✅ Weather function example completed!")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Weather function error: {e}")
        return False

def advanced_function_example():
    """More complex function calling scenario."""
    print("\n🔬 Advanced Function Calling")
    print("=" * 40)
    
    # Configuration
    api_key = os.getenv('INCREDIBLE_API_KEY')
    base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
    
    url = f"{base_url}/v1/chat-completion"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # Multiple utility functions
    functions = [
        {
            "name": "get_current_time",
            "description": "Get the current date and time",
            "parameters": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "calculate_circle_area",
            "description": "Calculate the area of a circle given its radius",
            "parameters": {
                "type": "object",
                "properties": {"radius": {"type": "number", "description": "Circle radius"}},
                "required": ["radius"]
            }
        },
        {
            "name": "get_weather_info",
            "description": "Get weather information for a city",
            "parameters": {
                "type": "object", 
                "properties": {"city": {"type": "string", "description": "City name"}},
                "required": ["city"]
            }
        }
    ]
    
    # Complex request requiring multiple function calls
    data = {
        "model": "small-1",
        "stream": False,
        "system": "You are a multi-purpose assistant with access to various tools. Use functions when needed to provide accurate, real-time information.",
        "functions": functions,
        "messages": [
            {
                "role": "user",
                "content": "I'm planning a picnic in Paris tomorrow. Can you check the weather, tell me what time it is now, and calculate how much pizza I need if I want to cover a circular area with radius 10 meters?"
            }
        ]
    }
    
    print("🎯 Complex multi-function request...")
    print(f"📤 Scenario: {data['messages'][0]['content']}")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        assistant_response = parse_api_response(result)
        
        print(f"\n🎯 AI Planning Response:")
        print("-" * 40)
        print(assistant_response)
        print("-" * 40)
        
        print("✅ Advanced function calling completed!")
        print("💡 Notice how the AI coordinated multiple functions to answer your complex request")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Advanced function error: {e}")
        return False

def main():
    """Run all function calling examples."""
    print("🚀 Incredible API - Function Calling Examples")
    print("=" * 60)
    
    # Run examples progressively
    success = simple_function_calling_example()
    
    if success:
        weather_function_example()
        advanced_function_example()
    
    print(f"\n{'='*60}")
    print("🎓 Function Calling Complete!")
    print("\n💡 Key Concepts:")
    print("   • Functions extend AI capabilities with real data")
    print("   • Define functions with clear descriptions and parameters")  
    print("   • AI automatically decides when and how to use functions")
    print("   • Multiple functions can be called in a single request")
    print("\n🔧 Function Definition Tips:")
    print("   • Use descriptive names and descriptions")
    print("   • Specify parameter types and requirements clearly")
    print("   • Handle edge cases and errors gracefully")
    print("   • Keep functions focused on single responsibilities")
    print("\n➡️  Next: Try 4_integrations.py to use pre-built integrations!")

if __name__ == "__main__":
    main()
