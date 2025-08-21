#!/usr/bin/env python3
"""
🛠️ Multiple Tools - AI Chooses the Right Function
=================================================

Learn how AI intelligently chooses between multiple available functions
using the Incredible API's actual function calling format. This example 
gives AI access to math, weather, and time functions, then shows how it 
picks the right tool for each question.

What this demonstrates:
• Defining multiple functions for AI (with "parameters" schema)
• How AI chooses the right function from multiple options
• Handling different function signatures with proper response parsing
• Building a toolkit of useful functions with function_call_id tracking

Based on: Incredible API Documentation (agentic_model_api_docs.md)
Format: Uses "parameters" instead of "input_schema"
Response: Structured with function_call_id and function_call_results

Real-world applications:
• Virtual assistants with multiple capabilities
• Customer service bots with various tools
• Automated workflows with different actions
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function 1: Calculator
def calculate_operation(operation, a, b):
    """
    Perform basic math operations.
    """
    operations = {
        "add": a + b,
        "subtract": a - b, 
        "multiply": a * b,
        "divide": a / b if b != 0 else "Error: Division by zero"
    }
    
    result = operations.get(operation, "Error: Unknown operation")
    print(f"🧮 Math: {a} {operation} {b} = {result}")
    return result

# Function 2: Weather (Demo)
def get_weather_info(city):
    """
    Get weather information for a city (demo function).
    In real applications, this would call a weather API.
    """
    weather_database = {
        "new york": {"temp": "72°F", "condition": "Sunny", "humidity": "45%"},
        "london": {"temp": "60°F", "condition": "Cloudy", "humidity": "80%"},
        "tokyo": {"temp": "68°F", "condition": "Rainy", "humidity": "90%"},
        "paris": {"temp": "65°F", "condition": "Partly Cloudy", "humidity": "60%"},
        "sydney": {"temp": "75°F", "condition": "Clear", "humidity": "55%"}
    }
    
    city_lower = city.lower()
    if city_lower in weather_database:
        weather = weather_database[city_lower]
        result = f"{weather['condition']}, {weather['temp']}, Humidity: {weather['humidity']}"
        print(f"🌤️ Weather for {city}: {result}")
        return result
    else:
        result = f"Weather data not available for {city}"
        print(f"🌤️ {result}")
        return result

# Function 3: Current Time
def get_current_time(timezone="UTC"):
    """
    Get the current time in a specified timezone.
    Simplified example - real implementation would handle timezones properly.
    """
    current_time = datetime.now()
    
    # Simplified timezone handling for demo
    timezone_offsets = {
        "UTC": 0,
        "EST": -5, 
        "PST": -8,
        "JST": 9,
        "GMT": 0
    }
    
    if timezone in timezone_offsets:
        # This is a simplified demo - real timezone handling is more complex
        time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        result = f"{time_str} {timezone}"
        print(f"🕐 Current time ({timezone}): {result}")
        return result
    else:
        result = f"Timezone '{timezone}' not supported. Available: UTC, EST, PST, JST, GMT"
        print(f"🕐 {result}")
        return result

# Define all available tools for AI
AVAILABLE_TOOLS = [
    {
        "name": "calculate_operation",
        "description": "Perform basic math operations: add, subtract, multiply, divide",
        "parameters": {
            "type": "object", 
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The math operation to perform"
                },
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number", 
                    "description": "Second number"
                }
            },
            "required": ["operation", "a", "b"]
        }
    },
    {
        "name": "get_weather_info",
        "description": "Get current weather information for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Name of the city to get weather for"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_current_time",
        "description": "Get the current time in a specified timezone",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "enum": ["UTC", "EST", "PST", "JST", "GMT"],
                    "description": "Timezone to get time for (default: UTC)"
                }
            },
            "required": []
        }
    }
]


def test_multiple_tools(question):
    """
    Send a question to AI with multiple tools available.
    """
    print(f"👤 Question: {question}")
    print("🤔 AI choosing from available tools...")
    
    # Get API key
    api_key = os.getenv('INCREDIBLE_API_KEY')
    if not api_key:
        print("❌ Missing INCREDIBLE_API_KEY!")
        return
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Step 1: Send request with all available tools
    data = {
        "model": "small-1",
        "stream": False,
        "messages": [{"role": "user", "content": question}],
        "functions": AVAILABLE_TOOLS
    }
    
    try:
        response = requests.post(
            'https://api.incredible.one/v1/chat-completion',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return
        
        result = response.json()
        response_items = result['result']['response']
        
        # Look for function calls in the response
        function_call_item = None
        assistant_message = None
        
        for item in response_items:
            if item.get('type') == 'function_call':
                function_call_item = item
            elif item.get('role') == 'assistant':
                assistant_message = item
        
        if function_call_item:
            # Step 2: AI decided to use one of our functions!
            function_call_id = function_call_item['function_call_id']
            function_calls = function_call_item['function_calls']
            
            if len(function_calls) > 0:
                function_call = function_calls[0]  # Get first function call
                function_name = function_call['name']
                function_input = function_call['input']
                
                print(f"🔧 AI chose function: {function_name}")
                print(f"📋 Function arguments: {function_input}")
                
                # Step 3: Execute the chosen function
                if function_name == "calculate_operation":
                    function_result = calculate_operation(
                        function_input["operation"],
                        function_input["a"], 
                        function_input["b"]
                    )
                elif function_name == "get_weather_info":
                    function_result = get_weather_info(function_input["city"])
                elif function_name == "get_current_time":
                    timezone = function_input.get("timezone", "UTC")
                    function_result = get_current_time(timezone)
                else:
                    print(f"❌ Unknown function: {function_name}")
                    return
                
                # Step 4: Send function result back to AI and get final response
                messages_history = [
                    {"role": "user", "content": question}
                ]
                
                # Add assistant message if it exists
                if assistant_message:
                    messages_history.append(assistant_message)
                
                # Add function call and result
                messages_history.extend([
                    function_call_item,
                    {
                        "type": "function_call_result",
                        "function_call_id": function_call_id,
                        "function_call_results": [function_result]
                    }
                ])
                
                # Get AI's final response using the function result
                final_data = {
                    "model": "small-1",
                    "stream": False, 
                    "messages": messages_history,
                    "functions": AVAILABLE_TOOLS
                }
                
                final_response = requests.post(
                    'https://api.incredible.one/v1/chat-completion',
                    headers=headers,
                    json=final_data,
                    timeout=30
                )
                
                if final_response.status_code == 200:
                    final_result = final_response.json()
                    final_response_items = final_result['result']['response']
                    
                    # Find assistant response
                    for item in final_response_items:
                        if item.get('role') == 'assistant':
                            print(f"🤖 AI: {item['content']}")
                            break
                    
                    print("✅ Function calling completed successfully!")
                else:
                    print(f"❌ Final response error: {final_response.status_code}")
                    print(f"Response: {final_response.text}")
        else:
            # AI responded directly without using functions
            if assistant_message:
                print(f"🤖 AI (no function): {assistant_message['content']}")
            else:
                print("🤖 AI: No clear response found")
            print("ℹ️ AI didn't need any functions for this question")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def multiple_tools_demo():
    """
    Demonstrate AI choosing between multiple available functions.
    """
    print("🛠️ Multiple Tools - AI Function Selection Demo")
    print("=" * 55)
    print("AI has access to these functions:")
    print("  🧮 Calculator (add, subtract, multiply, divide)")
    print("  🌤️ Weather lookup")
    print("  🕐 Current time")
    print()
    
    # Test different types of questions
    test_questions = [
        "What is 24 multiplied by 7?",
        "What's the weather like in Tokyo?", 
        "What time is it in EST timezone?",
        "Can you subtract 15 from 100?",
        "How's the weather in Paris?",
        "What color is the ocean?"  # This shouldn't need any function
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📋 Test {i}:")
        print("-" * 20)
        test_multiple_tools(question)

def explain_smart_selection():
    """
    Explain how AI selects the right function.
    """
    print("\n" + "=" * 55)
    print("🧠 HOW DOES AI CHOOSE THE RIGHT FUNCTION?")
    print("=" * 55)
    
    print("""
AI uses several factors to select functions:

1. 📝 **Function Descriptions**: AI reads each function's description
   - "Perform math operations" → Math questions
   - "Get weather information" → Weather questions  
   - "Get current time" → Time questions

2. 🎯 **Question Analysis**: AI analyzes the user's intent
   - "multiply" → Math operation needed
   - "weather" → Weather lookup needed
   - "time" → Time function needed

3. 🔍 **Parameter Matching**: AI checks if it has the required data
   - Calculator needs: operation, a, b
   - Weather needs: city name
   - Time needs: timezone (optional)

4. 🤖 **Smart Decisions**: AI can choose to:
   - Use the perfect function for the task
   - Use no function if none are needed
   - Handle missing information gracefully

This makes AI assistants incredibly flexible - they use the right tool
for each situation automatically!
""")

if __name__ == "__main__":
    # Run the multiple tools demonstration
    multiple_tools_demo()
    
    # Explain how AI makes smart selections
    explain_smart_selection()
    
    print("\n🎉 Next Steps:")
    print("   • 3_json_extraction.py - Use functions for structured data output")  
    print("   • 4_advanced_workflow.py - Chain multiple function calls")
    print("\n💡 Try modifying the questions above to see how AI adapts!")
