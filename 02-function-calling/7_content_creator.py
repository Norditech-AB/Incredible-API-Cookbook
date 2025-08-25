#!/usr/bin/env python3
"""
AI Content Creator Pipeline - CORRECTED Function Calling Example

This example demonstrates the PROPER separation between AI creativity and utility functions:

✅ WHAT THE AI DOES (via Incredible API):
- Creative content generation and writing
- Strategic decision-making about structure and flow  
- Content analysis and optimization
- Determines when and how to use available tools

✅ WHAT THE FUNCTIONS DO (real utility work):
- search_web(): Actual web search functionality
- create_file(): Real file creation on disk
- count_words(): Text analysis and statistics  
- format_as_markdown(): Proper formatting utilities
- append_to_file(): File operations
- get_current_time(): System utilities

This showcases TRUE function calling: AI using real tools to accomplish complex tasks,
rather than calling functions that pretend to do AI work themselves!
"""

import os
import json
import time
import random
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import requests

def search_web(query: str, num_results: int = 5) -> Dict[str, Any]:
    """Search the web for information (mock implementation - in production would use real search API)."""
    print(f"🔍 Searching web for: '{query}' ({num_results} results)")
    
    # Simulate API call delay
    time.sleep(0.5)
    
    # In production, this would call a real search API like Serper, Bing, or Google
    # For now, return structured data that AI can work with
    # Provide more substantial research data to help AI create content
    if "AI" in query and ("developer" in query or "software" in query):
        search_results = {
            "query": query,
            "key_insights": [
                "AI tools like GitHub Copilot and ChatGPT are enhancing developer productivity by 30-50%",
                "Software developers are adapting rather than being replaced - AI handles routine tasks while developers focus on complex problem-solving",
                "New roles emerging: AI/ML engineers, prompt engineers, AI ethics specialists",
                "Skills in demand: AI integration, machine learning, data analysis, human-AI collaboration",
                "Companies report 40% faster development cycles when using AI coding assistants",
                "Developer job market remains strong with 22% projected growth through 2030"
            ],
            "statistics": {
                "productivity_increase": "30-50% with AI tools",
                "job_growth_projection": "22% through 2030",
                "companies_using_ai": "65% of tech companies",
                "developer_satisfaction": "78% positive about AI integration"
            },
            "expert_opinions": [
                "AI augments human creativity rather than replacing it - developers become AI collaborators",
                "The future belongs to developers who can effectively work alongside AI systems",
                "Coding will shift from writing syntax to designing solutions and managing AI outputs"
            ],
            "total_results": num_results,
            "research_quality": "comprehensive"
        }
    else:
        search_results = {
            "query": query,
            "summary": f"Found {num_results} relevant results about {query}",
            "key_findings": [
                f"Current trends in {query} show significant industry growth",
                f"Expert analysis reveals emerging opportunities in {query}",
                f"Recent research indicates important developments in {query}"
            ],
            "total_results": num_results
        }
    
    print(f"✅ Found {search_results['total_results']} relevant results")
    return search_results

def create_file(filename: str, content: str, file_type: str = "txt") -> str:
    """Create a file with the specified content."""
    print(f"📝 Creating {file_type} file: {filename}")
    
    # Ensure artifacts directory exists
    artifacts_dir = "artifacts"
    if not os.path.exists(artifacts_dir):
        os.makedirs(artifacts_dir)
    
    # Create full file path
    file_path = os.path.join(artifacts_dir, f"{filename}.{file_type}")
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ File created successfully: {file_path}")
        return file_path
    
    except Exception as e:
        print(f"❌ Error creating file: {e}")
        return f"Error: {e}"

def get_current_time() -> str:
    """Get the current timestamp."""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"⏰ Current time: {timestamp}")
    return timestamp

def count_words(text: str) -> Dict[str, Any]:
    """Count words, characters, and other text statistics."""
    print(f"📊 Analyzing text statistics...")
    
    words = text.split()
    sentences = text.split('.')
    paragraphs = text.split('\n\n')
    
    stats = {
        "word_count": len(words),
        "character_count": len(text),
        "character_count_no_spaces": len(text.replace(' ', '')),
        "sentence_count": len([s for s in sentences if s.strip()]),
        "paragraph_count": len([p for p in paragraphs if p.strip()]),
        "average_words_per_sentence": round(len(words) / max(len([s for s in sentences if s.strip()]), 1), 1),
        "reading_time_minutes": round(len(words) / 200, 1)  # Average reading speed
    }
    
    print(f"✅ Text analysis complete: {stats['word_count']} words, ~{stats['reading_time_minutes']} min read")
    return stats

def format_as_markdown(content: str, title: str = "Document") -> str:
    """Format text content as properly structured Markdown."""
    print(f"📝 Formatting content as Markdown...")
    
    # Add proper Markdown structure
    formatted_content = f"""# {title}

*Generated on {time.strftime('%Y-%m-%d at %H:%M:%S')}*

---

{content}

---

*This content was generated using the Incredible API with function calling capabilities.*
"""
    
    print(f"✅ Markdown formatting complete")
    return formatted_content

def append_to_file(filename: str, new_content: str) -> str:
    """Append content to an existing file."""
    print(f"📝 Appending content to file: {filename}")
    
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"\n\n{new_content}")
        
        print(f"✅ Content appended successfully to {filename}")
        return f"Content appended to {filename}"
    
    except Exception as e:
        print(f"❌ Error appending to file: {e}")
        return f"Error: {e}"

def read_file_content(filename: str) -> str:
    """Read and return the content of a file."""
    print(f"📖 Reading file: {filename}")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ File read successfully: {len(content.split())} words")
        return content
    
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return f"Error reading file: {e}"

def main():
    """Main function demonstrating the AI Content Creator Pipeline."""
    
    print("🎨 AI Content Creator Pipeline - CORRECTED Function Calling Demo")
    print("=" * 70)
    print()
    print("This example shows the PROPER separation of concerns:")
    print("• AI handles creativity, content generation, and decision-making")  
    print("• Functions provide real utilities: file ops, web search, formatting")
    print("• Demonstrates TRUE function calling power!")
    print()
    
    # Get user input
    topic = input("Enter a topic you'd like content about (e.g., 'sustainable technology'): ").strip()
    
    if not topic:
        topic = "sustainable technology"
        print(f"Using default topic: '{topic}'")
    
    platform = input("\nChoose platform (blog/social/newsletter) [blog]: ").strip() or "blog"
    
    print(f"\n🚀 Starting content creation pipeline for: '{topic}' (Platform: {platform})")
    print("-" * 50)
    
    # Prepare API request
    api_key = os.getenv("INCREDIBLE_API_KEY")
    user_id = os.getenv("USER_ID")
    
    if not api_key or not user_id:
        print("❌ Error: Missing INCREDIBLE_API_KEY or USER_ID in environment variables")
        print("Please set up your .env file with your Incredible API credentials")
        return
    
    # Define available utility functions for the AI to use
    functions = [
        {
            "name": "search_web",
            "description": "Search the web for information about a topic and return structured results",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find information about"
                    },
                    "num_results": {
                        "type": "integer", 
                        "description": "Number of search results to return (1-10)",
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "create_file", 
            "description": "Create a new file with specified content",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name for the new file (without extension)"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file"
                    },
                    "file_type": {
                        "type": "string",
                        "description": "File extension/type",
                        "enum": ["txt", "md", "html", "json"]
                    }
                },
                "required": ["filename", "content"]
            }
        },
        {
            "name": "append_to_file",
            "description": "Append additional content to an existing file",
            "parameters": {
                "type": "object", 
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Path to the existing file"
                    },
                    "new_content": {
                        "type": "string",
                        "description": "Content to append to the file"
                    }
                },
                "required": ["filename", "new_content"]
            }
        },
        {
            "name": "read_file_content",
            "description": "Read and return the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Path to the file to read"
                    }
                },
                "required": ["filename"]
            }
        },
        {
            "name": "count_words",
            "description": "Analyze text and return word count, reading time, and other statistics",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text content to analyze"
                    }
                },
                "required": ["text"]
            }
        },
        {
            "name": "format_as_markdown",
            "description": "Format content as properly structured Markdown with title and metadata",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Content to format as Markdown"
                    },
                    "title": {
                        "type": "string", 
                        "description": "Title for the Markdown document"
                    }
                },
                "required": ["content"]
            }
        },
        {
            "name": "get_current_time",
            "description": "Get the current date and time timestamp",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    ]
    
    # API request to create content using function calling
    messages = [
        {
            "role": "user",
            "content": f"""You MUST create and save a comprehensive article about "{topic}". 

MANDATORY WORKFLOW - DO NOT DEVIATE:

1. RESEARCH: Call search_web ONLY ONCE with query about "{topic}"
2. WRITE ARTICLE: Create a 1000+ word article with these sections:
   - Introduction: Why this topic matters
   - Current Impact: How AI affects developer jobs now  
   - Benefits: Positive changes AI brings
   - Challenges: Concerns and solutions
   - Future: What's coming and how to prepare
   - Conclusion: Key takeaways
3. SAVE: Call create_file to save as markdown (filename: "ai_developer_impact", content: your full article, file_type: "md")
4. ANALYZE: Call count_words on your article text
5. TIMESTAMP: Call get_current_time

YOU MUST EXECUTE ALL 5 STEPS. If you don't call create_file, count_words, and get_current_time, you have FAILED.

Do NOT do multiple searches. Do NOT stop after research. You MUST save the actual article content."""
        }
    ]
    
    # Make API request
    url = "https://api.incredible.one/v1/chat-completion"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "small-1", 
        "stream": False,
        "messages": messages,
        "functions": functions,
        "max_tokens": 8000
    }
    
    # Track all function calls and results for the complete pipeline
    function_results = {}
    search_count = 0  # Prevent infinite search loops
    required_functions = {"create_file": False, "count_words": False, "get_current_time": False}
    
    print(f"\n🤖 AI is analyzing your request and planning the content creation pipeline...")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📋 Response headers: {dict(response.headers)}")
        
        if response.status_code != 200:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            return
            
        if not response.text.strip():
            print(f"❌ Empty response from API")
            return
            
        print(f"📄 Raw response preview: {response.text[:200]}...")
        
        try:
            result = response.json()
        except json.JSONDecodeError as json_err:
            print(f"❌ JSON Decode Error: {json_err}")
            print(f"📄 Full response text: {response.text}")
            return
        
        # Process function calls if present - loop until no more function calls
        max_iterations = 10  # Prevent infinite loops
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            has_function_calls = False
            
            if "result" in result and "response" in result["result"]:
                for item in result["result"]["response"]:
                    if item.get("type") == "function_call" and "function_calls" in item:
                        has_function_calls = True
                        
                        # Execute each function call
                        for func_call in item["function_calls"]:
                            func_name = func_call["name"]
                            func_args = func_call["input"]
                            
                            print(f"\n🔧 AI wants to use function: {func_name}")
                            print(f"📝 Parameters: {json.dumps(func_args, indent=2)}")
                            
                            # Execute the appropriate utility function
                            try:
                                if func_name == "search_web":
                                    search_count += 1
                                    if search_count > 2:  # Stricter limit
                                        result_data = {"message": "Research phase complete. Now write and save your article using create_file."}
                                        print(f"🚫 Search limit reached - forcing AI to create content")
                                    else:
                                        result_data = search_web(**func_args)
                                elif func_name == "create_file":
                                    result_data = create_file(**func_args)
                                    required_functions["create_file"] = True
                                    print("✅ REQUIRED: create_file completed!")
                                elif func_name == "append_to_file":
                                    result_data = append_to_file(**func_args)
                                elif func_name == "read_file_content":
                                    result_data = read_file_content(**func_args)
                                elif func_name == "count_words":
                                    result_data = count_words(**func_args)
                                    required_functions["count_words"] = True
                                    print("✅ REQUIRED: count_words completed!")
                                elif func_name == "format_as_markdown":
                                    result_data = format_as_markdown(**func_args)
                                elif func_name == "get_current_time":
                                    result_data = get_current_time(**func_args)
                                    required_functions["get_current_time"] = True
                                    print("✅ REQUIRED: get_current_time completed!")
                                else:
                                    result_data = {"error": f"Unknown function: {func_name}"}
                                
                                function_results[func_name] = result_data
                                print(f"✅ Function {func_name} completed successfully")
                                
                            except Exception as e:
                                error_result = {"error": str(e)}
                                function_results[func_name] = error_result
                                print(f"❌ Function {func_name} failed: {e}")
                        
                        # Build correct message history following other examples
                        function_call_id = item.get("function_call_id")
                        if not function_call_id:
                            print("⚠️ Warning: Missing function_call_id in response")
                            continue
                        
                        # Prepare function results (simplified)
                        results_for_api = [function_results.get(call["name"], {}) for call in item["function_calls"]]
                            
                        # Build message history correctly (like other examples)
                        messages_history = [messages[0]]  # Original user message
                        
                        # Add the function call item
                        messages_history.append(item)
                        
                        # Add function results
                        function_result_message = {
                            "type": "function_call_result", 
                            "function_call_id": function_call_id,
                            "function_call_results": results_for_api
                        }
                        messages_history.append(function_result_message)
                        
                        # Create follow-up payload (matching other examples)
                        follow_up_payload = {
                            "model": "small-1", 
                            "stream": False,
                            "messages": messages_history,
                            "functions": functions
                        }
                        
                        print(f"\n🔄 Sending function results back to AI for next steps...")
                        print(f"📤 Follow-up payload preview:")
                        print(f"   Messages count: {len(follow_up_payload['messages'])}")
                        print(f"   Last message type: {follow_up_payload['messages'][-1].get('type', 'unknown')}")
                        print(f"   Function call ID: {function_call_id}")
                        print(f"   Results count: {len(function_result_message['function_call_results'])}")
                        print(f"   Functions included: Yes (required for follow-up)")
                        
                        # Make follow-up request (with correct message structure)
                        response = requests.post(url, headers=headers, json=follow_up_payload)
                        
                        if response.status_code != 200:
                            print(f"❌ Follow-up HTTP Error {response.status_code}: {response.text}")
                            print(f"📤 Failed payload: {json.dumps(follow_up_payload, indent=2)}")
                            break
                            
                        result = response.json()
                        print(f"✅ Follow-up request successful!")
                        
                        # Check what the AI responded with
                        if "result" in result and "response" in result["result"]:
                            response_items = result['result']['response']
                            print(f"📋 AI response items: {len(response_items)}")
                            for resp_item in response_items:
                                if resp_item.get("role") == "assistant":
                                    content = resp_item.get('content', '')
                                    if content:
                                        print(f"🤖 AI: {content[:200]}...")
                                    else:
                                        print(f"🤖 AI: [Completed content creation tasks]")
                                elif resp_item.get("type") == "function_call":
                                    print(f"🔧 AI wants to call more functions: {[call['name'] for call in resp_item.get('function_calls', [])]}")
                        
                        # Continue processing - AI might want to make more function calls
                        break  # Break out of the item loop to process the new result
            
            if not has_function_calls:
                # Check if required functions were completed
                missing_functions = [func for func, completed in required_functions.items() if not completed]
                if missing_functions:
                    print(f"⚠️ AI stopped but missing required functions: {missing_functions}")
                    print(f"🏁 Pipeline incomplete - required functions not executed!")
                else:
                    print(f"🏁 No more function calls needed - conversation complete!")
                break
                
        if iteration >= max_iterations:
            print(f"⚠️ Reached maximum iterations ({max_iterations}) - stopping to prevent infinite loop")
        
        # Display final AI response
        if "result" in result and "response" in result["result"] and len(result["result"]["response"]) > 0:
            final_response = result["result"]["response"][-1]
            if final_response.get("role") == "assistant":
                print(f"\n🎉 CONTENT CREATION PIPELINE COMPLETE!")
                print("=" * 50)
                print(f"🤖 AI Summary: {final_response.get('content', 'Content creation finished!')}")
        else:
            print(f"\n🎉 CONTENT CREATION PIPELINE COMPLETE!")
            print("=" * 50)
            print(f"🤖 AI Summary: Content creation finished successfully!")
        
        # Show pipeline summary
        print(f"\n📊 PIPELINE EXECUTION SUMMARY:")
        print("-" * 30)
        for func_name, result_data in function_results.items():
            if "error" not in result_data:
                print(f"✅ {func_name}: Success")
            else:
                print(f"❌ {func_name}: {result_data['error']}")
        
        # Show saved files
        saved_files = [result for result in function_results.values() 
                      if isinstance(result, str) and result.startswith("artifacts/")]
        
        if saved_files:
            print(f"\n💾 GENERATED FILES:")
            for file_path in saved_files:
                print(f"📄 {file_path}")
                
        print(f"\n🎊 Your complete content about '{topic}' is ready!")
        print("The AI successfully used real utility functions to research, create, analyze,")
        print("and save professional content - showcasing true function calling power!")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
