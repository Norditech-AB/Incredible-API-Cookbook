#!/usr/bin/env python3
"""
📊 JSON Extraction - Structured Data from Unstructured Text
===========================================================

Learn how to use function calling to extract structured JSON data
from unstructured text. This technique is incredibly powerful for:

• Data processing and normalization
• Form filling from natural language
• Content analysis and classification  
• Converting text to structured databases

Based on: Anthropic's JSON mode example
https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview#json-mode

Real-world applications:
• Resume parsing into database fields
• Customer inquiry categorization
• Product description standardization
• Contact information extraction
"""

import os
import json
import re
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def extract_person_info(name, city, occupation, age=None, email=None, phone=None):
    """
    Structure person information into a standardized format.
    
    This function acts as a "schema validator" that ensures
    we get consistent, structured data from unstructured input.
    """
    person_data = {
        "name": name,
        "age": int(age) if age else None,
        "city": city,
        "occupation": occupation,
        "contact": {}
    }
    
    if email:
        person_data["contact"]["email"] = email
    if phone:
        person_data["contact"]["phone"] = phone
    
    # Clean up empty contact section
    if not person_data["contact"]:
        del person_data["contact"]
    
    print(f"📊 Extracted person data: {json.dumps(person_data, indent=2)}")
    return person_data

def extract_business_info(company, industry, employees, location, revenue=None, founded=None):
    """
    Structure business information into a standardized format.
    """
    # Clean employee count - extract numbers from text like "around 500 people"
    employee_count = None
    if employees:
        numbers = re.findall(r'\d+', str(employees))
        if numbers:
            employee_count = int(numbers[0])
    
    business_data = {
        "company": company,
        "industry": industry,
        "employee_count": employee_count,
        "location": location,
        "financial": {}
    }
    
    if revenue:
        business_data["financial"]["revenue"] = revenue
    if founded:
        business_data["financial"]["founded_year"] = int(founded)
    
    # Clean up empty financial section
    if not business_data["financial"]:
        del business_data["financial"]
    
    print(f"🏢 Extracted business data: {json.dumps(business_data, indent=2)}")
    return business_data

def extract_product_info(name, category, price, description, rating=None, availability=None):
    """
    Structure product information into a standardized format.
    """
    # Clean price - remove currency symbols and extract numeric value
    clean_price = None
    if price:
        # Remove currency symbols and extract numbers (including decimals)
        price_match = re.search(r'[\d,]+\.?\d*', str(price).replace(',', ''))
        if price_match:
            clean_price = float(price_match.group())
    
    product_data = {
        "product_name": name,
        "category": category,
        "price": clean_price,
        "description": description,
        "metadata": {}
    }
    
    if rating:
        # Clean rating - extract numeric value from text like "4.5 stars"
        rating_match = re.search(r'(\d+\.?\d*)', str(rating))
        if rating_match:
            product_data["metadata"]["rating"] = float(rating_match.group(1))
    if availability:
        product_data["metadata"]["availability"] = availability
        
    # Clean up empty metadata section
    if not product_data["metadata"]:
        del product_data["metadata"]
    
    print(f"🛍️ Extracted product data: {json.dumps(product_data, indent=2)}")
    return product_data

# Define extraction tools for AI
EXTRACTION_TOOLS = [
    {
        "name": "extract_person_info",
        "description": "Extract and structure personal information from unstructured text",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Person's full name"
                },
                "age": {
                    "type": "string", 
                    "description": "Person's age (as string, will be converted)"
                },
                "city": {
                    "type": "string",
                    "description": "City where person lives"
                },
                "occupation": {
                    "type": "string",
                    "description": "Person's job or occupation"
                },
                "email": {
                    "type": "string",
                    "description": "Email address if provided"
                },
                "phone": {
                    "type": "string", 
                    "description": "Phone number if provided"
                }
            },
            "required": ["name", "city", "occupation"]
        }
    },
    {
        "name": "extract_business_info",
        "description": "Extract and structure business information from unstructured text",
        "parameters": {
            "type": "object",
            "properties": {
                "company": {
                    "type": "string",
                    "description": "Company name"
                },
                "industry": {
                    "type": "string",
                    "description": "Industry or business sector"
                },
                "employees": {
                    "type": "string",
                    "description": "Number of employees"
                },
                "location": {
                    "type": "string", 
                    "description": "Company location or headquarters"
                },
                "revenue": {
                    "type": "string",
                    "description": "Annual revenue if mentioned"
                },
                "founded": {
                    "type": "string",
                    "description": "Year company was founded"
                }
            },
            "required": ["company", "industry", "location"]
        }
    },
    {
        "name": "extract_product_info",
        "description": "Extract and structure product information from unstructured text",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Product name"
                },
                "category": {
                    "type": "string",
                    "description": "Product category or type"
                },
                "price": {
                    "type": "string",
                    "description": "Product price (as string, will be converted)"
                },
                "description": {
                    "type": "string",
                    "description": "Brief product description"
                },
                "rating": {
                    "type": "string",
                    "description": "Product rating if mentioned"
                },
                "availability": {
                    "type": "string",
                    "description": "Availability status if mentioned"
                }
            },
            "required": ["name", "category", "description"]
        }
    }
]

def execute_extraction_function(function_name, arguments):
    """
    Execute the requested extraction function.
    """
    if function_name == "extract_person_info":
        return extract_person_info(**arguments)
    elif function_name == "extract_business_info":
        return extract_business_info(**arguments)
    elif function_name == "extract_product_info":
        return extract_product_info(**arguments)
    else:
        return f"Unknown extraction function: {function_name}"

def extract_structured_data(unstructured_text):
    """
    Extract structured JSON data from unstructured text using AI function calling.
    """
    print(f"📝 Input text: {unstructured_text}")
    print("🤖 AI analyzing text to determine extraction type...")
    
    # Get API key
    api_key = os.getenv('INCREDIBLE_API_KEY')
    if not api_key:
        print("❌ Missing INCREDIBLE_API_KEY!")
        return None
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Ask AI to extract structured data
    prompt = f"""
Please extract structured information from this text using the appropriate extraction function:

Text: {unstructured_text}

Choose the most appropriate extraction function based on the type of information in the text.
"""
    
    data = {
        "model": "small-1",
        "stream": False,
        "messages": [{"role": "user", "content": prompt}],
        "functions": EXTRACTION_TOOLS
    }
    
    try:
        response = requests.post(
            'https://api.incredible.one/v1/chat-completion',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            return None
        
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
            # AI chose an extraction function
            function_call_id = function_call_item['function_call_id']
            function_calls = function_call_item['function_calls']
            
            if len(function_calls) > 0:
                function_call = function_calls[0]  # Get first function call
                function_name = function_call['name']
                function_input = function_call['input']
                
                print(f"🔧 AI chose extraction: {function_name}")
                print(f"📋 Extracted fields: {list(function_input.keys())}")
                
                # Execute the extraction function
                structured_data = execute_extraction_function(function_name, function_input)
                
                print("✅ Extraction completed!")
                return structured_data
        else:
            # AI couldn't determine extraction type
            if assistant_message:
                print("❌ AI couldn't determine how to extract this data")
                print(f"🤖 AI response: {assistant_message['content']}")
            else:
                print("❌ No extraction function called or response found")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def json_extraction_demo():
    """
    Demonstrate JSON extraction with different types of unstructured data.
    """
    print("📊 JSON Extraction - Structured Data from Text")
    print("=" * 55)
    print("Converting unstructured text into structured JSON data...")
    print()
    
    # Test cases with different types of unstructured data
    test_cases = [
        {
            "type": "Person",
            "text": "Hi, I'm Sarah Johnson, I'm 28 years old and I work as a Software Engineer in San Francisco. You can reach me at sarah.j@email.com or call me at 555-0123."
        },
        {
            "type": "Business", 
            "text": "TechCorp is a leading software company based in Seattle. Founded in 2010, they specialize in cloud computing solutions and employ around 500 people. Last year they reported revenue of $50 million."
        },
        {
            "type": "Product",
            "text": "The UltraPhone Pro is a premium smartphone in the electronics category priced at $899. It features a stunning display and long battery life. Currently rated 4.5 stars and available for immediate shipping."
        },
        {
            "type": "Mixed",
            "text": "John Smith from New York works as a Marketing Manager. He's interested in our premium consulting services."
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['type']} Information")
        print("-" * 40)
        structured_data = extract_structured_data(test_case['text'])
        
        if structured_data:
            print(f"🎯 Successfully extracted {test_case['type'].lower()} data!")
        else:
            print("❌ Extraction failed")

def explain_json_extraction_power():
    """
    Explain why JSON extraction with function calling is powerful.
    """
    print("\n" + "=" * 55)
    print("🚀 WHY IS JSON EXTRACTION SO POWERFUL?")
    print("=" * 55)
    
    print("""
JSON extraction with function calling solves real business problems:

📋 **Data Normalization**:
   • Convert messy text into clean database records
   • Standardize formats across different data sources
   • Handle missing fields gracefully

🤖 **Intelligent Parsing**:
   • AI understands context and intent
   • Extracts relevant information automatically
   • Handles variations in how data is presented

🔧 **Real-World Applications**:

   📝 **Resume Processing**:
      Text: "John Doe, 5 years experience as Data Scientist at Google"
      JSON: {"name": "John Doe", "experience": 5, "role": "Data Scientist", "company": "Google"}

   📞 **Customer Support**:
      Text: "My order #12345 is delayed, contact me at jane@email.com"
      JSON: {"order_id": "12345", "issue": "delayed", "contact": "jane@email.com"}

   🛍️ **Product Cataloging**:
      Text: "Premium leather jacket, $299, available in black and brown"
      JSON: {"product": "Premium leather jacket", "price": 299, "colors": ["black", "brown"]}

💡 **Key Advantages**:
   • No training data required - uses AI's understanding
   • Flexible schemas that adapt to different content
   • Handles edge cases and missing information
   • Scales to any domain or data type

This transforms unstructured data into actionable, queryable information!
""")

if __name__ == "__main__":
    # Run the JSON extraction demonstration
    json_extraction_demo()
    
    # Explain the power of JSON extraction
    explain_json_extraction_power()
    
    print("\n🎉 Next Steps:")
    print("   • 4_advanced_workflow.py - Chain multiple function calls together")
    print("   • Modify the extraction schemas for your specific use case")
    print("   • Try with your own unstructured text data")
    
    print("\n💡 Pro Tip: Function calling for JSON extraction is perfect for:")
    print("   • Data migration projects") 
    print("   • Content management systems")
    print("   • Customer data processing")
    print("   • Document parsing workflows")
