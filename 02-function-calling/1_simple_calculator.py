#!/usr/bin/env python3
"""
🧮 Simple Calculator - Your First Function Call
==============================================

This is the simplest possible function calling example using the
Incredible API's actual function calling format. AI gets access to a 
calculator function and can perform math operations.

What this demonstrates:
• How to define a function AI can use (with "parameters" schema)
• The complete function calling flow with proper message types
• How AI decides when to use functions
• Processing function results with function_call_id tracking

Based on: Incredible API Documentation (agentic_model_api_docs.md)
Format: Uses "parameters" instead of "input_schema" 
Response: Structured with function_call_id and function_call_results
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def calculate_sum(a, b):
    """
    Add two numbers together.
    
    This is our simple function that AI can call.
    In real applications, this could be any function - 
    API calls, database queries, file operations, etc.
    """
    result = a + b
    print(f"🧮 Executing: calculate_sum({a}, {b}) = {result}")
    return result

# Define the function schema for AI
# This tells AI what the function does and how to use it
CALCULATOR_FUNCTION = {
    "name": "calculate_sum",
    "description": "Add two numbers together and return the sum",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {
                "type": "number", 
                "description": "First number to add"
            },
            "b": {
                "type": "number",
                "description": "Second number to add"
            }
        },
        "required": ["a", "b"]
    }
}

def simple_calculator_example():
    """
    Demonstrate basic function calling with a calculator.
    """
    print("🧮 Simple Calculator - Function Calling Demo")
    print("=" * 50)
    
    # Get API key
    api_key = os.getenv('INCREDIBLE_API_KEY')
    if not api_key:
        print("❌ Missing INCREDIBLE_API_KEY in .env file!")
        print("💡 Copy env.example to .env and add your API key")
        return
    
    # Test with a math question
    user_question = "What is 127 + 349?"
    print(f"👤 User: {user_question}")
    print("🤔 AI thinking about whether to use the calculator...")
    
    # Step 1: Send initial request with available tools
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    initial_data = {
        "model": "small-1",
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": user_question
            }
        ],
        "functions": [CALCULATOR_FUNCTION]  # Give AI access to our calculator
    }
    
    try:
        # Make the API call
        response = requests.post(
            'https://api.incredible.one/v1/chat-completion',
            headers=headers,
            json=initial_data,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
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
            # Step 2: AI decided to use our function!
            function_call_id = function_call_item['function_call_id']
            function_calls = function_call_item['function_calls']
            
            if len(function_calls) > 0:
                function_call = function_calls[0]  # Get first function call
                function_name = function_call['name']
                function_input = function_call['input']
                
                print(f"🔧 AI wants to use function: {function_name}")
                print(f"📋 Function arguments: {function_input}")
                
                # Step 3: Execute the function
                if function_name == "calculate_sum":
                    function_result = calculate_sum(
                        function_input['a'], 
                        function_input['b']
                    )
                else:
                    print(f"❌ Unknown function: {function_name}")
                    return
                
                # Step 4: Send function result back to AI
                messages_history = [
                    {"role": "user", "content": user_question}
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
                
                final_data = {
                    "model": "small-1", 
                    "stream": False,
                    "messages": messages_history,
                    "functions": [CALCULATOR_FUNCTION]
                }
                
                # Get AI's final response using the function result
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
                    
                    print("\n✅ Function calling completed successfully!")
                else:
                    print(f"❌ Error in final response: {final_response.status_code}")
                    print(f"Response: {final_response.text}")
            
        else:
            # AI didn't use the function (responded directly)
            if assistant_message:
                print(f"🤖 AI (direct response): {assistant_message['content']}")
            else:
                print("🤖 AI: No clear response found")
            print("ℹ️  AI chose not to use the calculator function")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
    except KeyError as e:
        print(f"❌ Response format error: {e}")
        print(f"Raw response: {response.text}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")

def what_just_happened():
    """
    Explain the function calling process in simple terms.
    """
    print("\n" + "=" * 50)
    print("🤔 WHAT JUST HAPPENED?")
    print("=" * 50)
    
    print("""
        Function calling follows this exact flow:

        1. 📋 **Define Function**: We created calculate_sum() and described it to AI
        - Used "parameters" schema (not "input_schema")
        - Told AI: "This function adds two numbers"
        - Specified: "It needs parameters 'a' and 'b'"

        2. 🧠 **AI Decision**: AI analyzed the question "What is 127 + 349?"
        - AI thought: "This is a math problem"
        - AI decided: "I should use the calculate_sum function"

        3. 🔧 **Function Call**: AI sent structured function call
        - Format: {"type": "function_call", "function_calls": [...]}
        - AI said: "Call calculate_sum with a=127, b=349"
        - We executed: calculate_sum(127, 349) = 476

        4. 💬 **Final Response**: AI used the result to answer naturally
        - We sent back: {"type": "function_call_result", "function_call_results": [476]}
        - AI responded: "The sum of 127 and 349 is 476"

        This is the foundation of AI assistants that can DO things, not just talk!
    """)

def why_this_matters():
    """
    Explain why function calling is powerful.
    """
    print("\n" + "=" * 50) 
    print("🚀 WHY DOES THIS MATTER?")
    print("=" * 50)
    
    print("""
        This simple calculator example shows the foundation for incredible things:

        🧮 **Beyond Calculations**: Replace calculate_sum() with:
        • send_email(to, subject, body)
        • get_weather(city) 
        • query_database(sql)
        • create_calendar_event(title, time)
        • process_image(image_path)

        🤖 **Smart AI Assistants**: AI can now:
        • Decide WHEN to use functions (not every message needs them)
        • Choose the RIGHT function from many options
        • Handle complex multi-step workflows
        • Provide accurate data instead of making things up

        🔗 **Real-World Applications**:
        • Customer service bots that can check orders
        • Virtual assistants that manage your calendar
        • Content generators that access live data
        • Automation tools that integrate multiple systems

        💡 **Key Insight**: Functions give AI access to the real world!
        Instead of just generating text, AI can now:
        - Read files
        - Call APIs  
        - Update databases
        - Send notifications
        - Process data
        - Control systems

        The simple pattern you just saw scales to build incredibly powerful applications!
    """)

if __name__ == "__main__":
    # Run the simple calculator demo
    simple_calculator_example()
    
    # Explain what happened
    what_just_happened()
    
    # Show why it matters
    why_this_matters()
    
    print("\n🎉 Ready for more? Try:")
    print("   • 2_multiple_tools.py - Give AI access to multiple functions")
    print("   • 3_json_extraction.py - Use functions for structured data")
    print("   • 4_advanced_workflow.py - Build complex AI workflows")
