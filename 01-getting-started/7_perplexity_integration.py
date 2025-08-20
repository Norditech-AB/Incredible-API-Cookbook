#!/usr/bin/env python3
"""
Perplexity Integration - AI Research Assistant
==============================================

Learn how to use AI for intelligent research using Perplexity AI.
Perfect for building AI that can gather real-time information!

What you'll learn:
    - How to do AI-powered research
    - How to get current, accurate information
    - Building research assistants

Usage:
    python 7_perplexity_integration.py

Note: You'll need to connect Perplexity integration in your dashboard first.
"""

import os
import requests
from dotenv import load_dotenv

# Load your API key from .env file
load_dotenv()

def do_ai_research(question):
    """Use Perplexity AI to research a question."""
    
    api_key = os.getenv('INCREDIBLE_API_KEY')
    user_id = os.getenv('USER_ID')
    
    if not api_key or not user_id:
        print("❌ Missing API credentials! Check your .env file")
        return None
    
    print("🔍 AI Research in Progress")
    print("-" * 40)
    
    # Perplexity integration endpoint
    url = "https://api.incredible.one/v1/integrations/perplexity/execute"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    data = {
        "user_id": user_id,
        "feature_name": "PERPLEXITY_SEARCH",
        "inputs": {
            "query": question
        }
    }
    
    try:
        print(f"🔎 Researching: {question}")
        print("⏳ AI is searching the internet...")
        
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        research_answer = result.get('result', {}).get('answer', 'No answer found')
        sources = result.get('result', {}).get('sources', [])
        
        print("✅ Research complete!")
        print()
        print("📄 Research Results:")
        print("=" * 50)
        print(research_answer)
        print("=" * 50)
        
        if sources:
            print()
            print("🔗 Sources:")
            for i, source in enumerate(sources[:3], 1):  # Show first 3 sources
                print(f"   {i}. {source.get('title', 'Unknown')}")
                if source.get('url'):
                    print(f"      {source['url']}")
        
        return research_answer
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Research failed")
        print(f"🔍 Error: {e}")
        print()
        print("🔧 Troubleshooting:")
        print("   1. Make sure Perplexity integration is connected in your dashboard")
        print("   2. Check your internet connection")
        print("   3. Try a different research question")
        print("   4. Verify your Perplexity API key is valid")
        return None

def research_examples():
    """Show different types of research questions."""
    print("📚 Research Examples")
    print("-" * 40)
    
    # Example questions to demonstrate different research types
    example_questions = [
        "What are the latest developments in renewable energy 2024?",
        "How does ChatGPT work in simple terms?", 
        "What are the current stock market trends?",
        "Best practices for Python programming 2024"
    ]
    
    print("Here are some example research questions:")
    for i, question in enumerate(example_questions, 1):
        print(f"   {i}. {question}")
    
    print()
    
    # Let user pick or enter their own
    choice = input("Enter a number (1-4) or type your own question: ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(example_questions):
        question = example_questions[int(choice) - 1]
    elif choice:
        question = choice
    else:
        question = example_questions[0]  # Default
    
    print()
    return do_ai_research(question)

def show_perplexity_setup_help():
    """Show users how to set up Perplexity integration."""
    print("🔧 Perplexity Integration Setup")
    print("-" * 40)
    print()
    print("To use Perplexity research, you need to:")
    print()
    print("1. 🌐 Go to your Incredible API dashboard")
    print("   → https://incredible.one/dashboard")
    print()
    print("2. 🔌 Find the 'Integrations' section")
    print()
    print("3. 🔍 Click 'Connect Perplexity'")
    print()
    print("4. 🔑 Enter your Perplexity API key")
    print("   → Get one from https://www.perplexity.ai/settings/api")
    print()
    print("5. ✅ Save and come back to run this script")
    print()
    print("💡 Why Perplexity? It's an AI search engine that gives you")
    print("   accurate, up-to-date information with sources!")

def main():
    """Test Perplexity research integration."""
    print("🔍 Perplexity Integration - AI Research Assistant")
    print("=" * 60)
    print("Let's teach AI to do research!")
    print()
    
    # Try to do research
    result = research_examples()
    
    print()
    
    if result:
        print("🎊 Amazing! Your AI can now do research!")
        print()
        print("🚀 What you can build:")
        print("   📊 Market research bots")
        print("   📰 News summarization services") 
        print("   🎓 Study assistants that find information")
        print("   📈 Trend analysis tools")
        print("   🔬 Competitive intelligence systems")
        print("   📚 Content research for writing")
    else:
        print("⚠️  Perplexity integration not set up yet")
        print()
        show_perplexity_setup_help()
    
    print()
    print("🏁 Congratulations! Tutorial Complete!")
    print()
    print("You've now learned all the Incredible API fundamentals:")
    print("   ✅ 1. Basic chat completion")
    print("   ✅ 2. Multiple models")
    print("   ✅ 3. Conversations")
    print("   ✅ 4. Streaming responses") 
    print("   ✅ 5. Function calling")
    print("   ✅ 6. Gmail integration")
    print("   ✅ 7. Research integration")
    print()
    print("🚀 You're ready to build incredible AI applications!")

if __name__ == "__main__":
    main()
