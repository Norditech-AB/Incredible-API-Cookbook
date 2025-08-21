#!/usr/bin/env python3
"""
📈 Stock Analysis Assistant - AI-Powered Investment Analysis
===========================================================

A fun, real-world example that combines Yahoo Finance data with AI analysis
to create an intelligent stock analysis assistant using function calling.

What this demonstrates:
• Real-world API integration (Yahoo Finance via yfinance)
• Financial data analysis with AI interpretation
• Technical indicators calculation (moving averages, RSI, volatility)
• AI-powered investment recommendations
• Multi-stock portfolio comparison
• Practical function calling for financial analysis

Features:
• Get real-time stock prices and historical data
• Calculate technical indicators automatically
• AI analysis of market trends and patterns
• Investment recommendations with risk assessment
• Compare multiple stocks side-by-side
• Educational explanations of financial concepts

Real-world applications:
• Personal investment research assistant
• Portfolio analysis and optimization
• Market trend identification
• Educational tool for learning about stocks
• Automated financial reporting

Requirements: pip install yfinance
"""

import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# External library for Yahoo Finance data
try:
    import yfinance as yf
except ImportError:
    print("❌ Missing required library!")
    print("📦 Please install: pip install yfinance")
    print("💡 Then run this script again")
    exit(1)

# Load environment variables
load_dotenv()

def get_stock_data(symbol, period="1mo"):
    """
    Get comprehensive stock data from Yahoo Finance.
    """
    try:
        # Create ticker object
        ticker = yf.Ticker(symbol.upper())
        
        # Get basic info
        info = ticker.info
        
        # Get historical data
        hist = ticker.history(period=period)
        
        if hist.empty:
            return f"❌ No data found for symbol: {symbol}"
        
        # Calculate current metrics
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        change = current_price - prev_price
        change_pct = (change / prev_price) * 100
        
        # Calculate volatility (standard deviation of returns)
        returns = hist['Close'].pct_change().dropna()
        volatility = returns.std() * (252 ** 0.5) * 100  # Annualized volatility
        
        # Get volume info
        avg_volume = hist['Volume'].mean()
        current_volume = hist['Volume'].iloc[-1]
        
        stock_data = {
            "symbol": symbol.upper(),
            "company_name": info.get('longName', 'N/A'),
            "sector": info.get('sector', 'N/A'),
            "current_price": round(current_price, 2),
            "price_change": round(change, 2),
            "price_change_percent": round(change_pct, 2),
            "market_cap": info.get('marketCap', 'N/A'),
            "pe_ratio": info.get('trailingPE', 'N/A'),
            "52_week_high": round(hist['High'].max(), 2),
            "52_week_low": round(hist['Low'].min(), 2),
            "volatility_percent": round(volatility, 2),
            "average_volume": int(avg_volume),
            "current_volume": int(current_volume),
            "data_period": period,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        print(f"📊 Retrieved data for {stock_data['company_name']} ({symbol.upper()})")
        print(f"💰 Current Price: ${current_price:.2f} ({change_pct:+.2f}%)")
        
        return stock_data
        
    except Exception as e:
        error_msg = f"Error getting data for {symbol}: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

def calculate_technical_indicators(symbol, period="3mo"):
    """
    Calculate technical indicators for stock analysis.
    """
    try:
        ticker = yf.Ticker(symbol.upper())
        hist = ticker.history(period=period)
        
        if hist.empty:
            return f"❌ No data found for {symbol}"
        
        # Simple Moving Averages
        sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
        sma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
        
        # RSI (Relative Strength Index) - simplified calculation
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]
        
        # Support and Resistance levels (simplified)
        support = hist['Low'].rolling(window=20).min().iloc[-1]
        resistance = hist['High'].rolling(window=20).max().iloc[-1]
        
        # Current price for comparison
        current_price = hist['Close'].iloc[-1]
        
        indicators = {
            "symbol": symbol.upper(),
            "current_price": round(current_price, 2),
            "sma_20": round(sma_20, 2) if not pd.isna(sma_20) else None,
            "sma_50": round(sma_50, 2) if not pd.isna(sma_50) else None,
            "rsi": round(current_rsi, 2) if not pd.isna(current_rsi) else None,
            "support_level": round(support, 2),
            "resistance_level": round(resistance, 2),
            "analysis_period": period,
            "calculated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Add trend analysis
        if indicators["sma_20"] and indicators["sma_50"]:
            if indicators["sma_20"] > indicators["sma_50"]:
                trend = "Bullish (Short-term trending up)"
            else:
                trend = "Bearish (Short-term trending down)"
        else:
            trend = "Insufficient data for trend analysis"
        
        indicators["trend"] = trend
        
        print(f"📈 Technical indicators calculated for {symbol.upper()}")
        print(f"📊 RSI: {indicators['rsi']:.1f} | Trend: {trend}")
        
        return indicators
        
    except Exception as e:
        error_msg = f"Error calculating indicators for {symbol}: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

def compare_stocks(symbols):
    """
    Compare multiple stocks side by side.
    """
    try:
        if isinstance(symbols, str):
            symbols = [s.strip() for s in symbols.split(',')]
        
        comparisons = []
        
        for symbol in symbols:
            symbol = symbol.strip().upper()
            
            # Get basic stock data
            stock_data = get_stock_data(symbol, "1mo")
            
            if isinstance(stock_data, str):  # Error case
                continue
                
            # Create simplified comparison data
            comparison = {
                "symbol": symbol,
                "company": stock_data.get("company_name", "N/A"),
                "price": stock_data.get("current_price", 0),
                "change_percent": stock_data.get("price_change_percent", 0),
                "market_cap": stock_data.get("market_cap", "N/A"),
                "pe_ratio": stock_data.get("pe_ratio", "N/A"),
                "volatility": stock_data.get("volatility_percent", 0),
                "sector": stock_data.get("sector", "N/A")
            }
            
            comparisons.append(comparison)
        
        if not comparisons:
            return "❌ Could not retrieve data for any of the provided symbols"
        
        result = {
            "comparison_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "stocks_compared": len(comparisons),
            "stocks": comparisons
        }
        
        print(f"🔄 Compared {len(comparisons)} stocks successfully")
        return result
        
    except Exception as e:
        error_msg = f"Error comparing stocks: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

# Fix missing pandas import
import pandas as pd

# Define stock analysis tools for AI
STOCK_ANALYSIS_TOOLS = [
    {
        "name": "get_stock_data",
        "description": "Get comprehensive stock data including price, market cap, P/E ratio, volatility, and trading volume",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol (e.g., AAPL, GOOGL, TSLA)"
                },
                "period": {
                    "type": "string",
                    "enum": ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y"],
                    "description": "Time period for historical data (default: 1mo)"
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "calculate_technical_indicators",
        "description": "Calculate technical indicators including moving averages, RSI, support/resistance levels, and trend analysis",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol to analyze"
                },
                "period": {
                    "type": "string",
                    "enum": ["1mo", "3mo", "6mo", "1y", "2y"],
                    "description": "Time period for technical analysis (default: 3mo)"
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "compare_stocks",
        "description": "Compare multiple stocks side by side with key metrics and performance",
        "parameters": {
            "type": "object",
            "properties": {
                "symbols": {
                    "type": "string",
                    "description": "Comma-separated list of stock symbols to compare (e.g., 'AAPL,GOOGL,MSFT')"
                }
            },
            "required": ["symbols"]
        }
    }
]

def analyze_stock_with_ai(user_query):
    """
    Use AI to analyze stocks based on user query with function calling.
    """
    print(f"🤖 AI Stock Analyst analyzing: {user_query}")
    print("🔍 AI determining which analysis tools to use...")
    
    # Get API key
    api_key = os.getenv('INCREDIBLE_API_KEY')
    if not api_key:
        print("❌ Missing INCREDIBLE_API_KEY!")
        return
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # System prompt for stock analysis
    system_prompt = """You are an expert stock analyst and investment advisor. You have access to real-time stock data and technical analysis tools.

When analyzing stocks:
- Always get current stock data first
- Calculate technical indicators for deeper analysis
- Provide clear, educational explanations
- Give balanced investment perspectives (both risks and opportunities)
- Explain what the technical indicators mean in simple terms
- Compare multiple stocks when relevant
- Focus on helping users understand market dynamics

Be conversational but professional. Make complex financial concepts easy to understand."""
    
    # Step 1: Send initial request with stock analysis tools
    initial_data = {
        "model": "small-1",
        "stream": False,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_query}],
        "functions": STOCK_ANALYSIS_TOOLS
    }
    
    try:
        response = requests.post('https://api.incredible.one/v1/chat-completion', 
                               headers=headers, json=initial_data)
        response.raise_for_status()
        
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
            print("🔧 AI wants to use analysis tools...")
            
            function_call_id = function_call_item['function_call_id']
            function_calls = function_call_item['function_calls']
            
            # Execute the functions
            function_results = []
            for func_call in function_calls:
                function_name = func_call['name']
                function_input = func_call['input']
                
                print(f"⚡ Executing: {function_name} with {function_input}")
                
                # Call the appropriate function
                if function_name == "get_stock_data":
                    result = get_stock_data(**function_input)
                elif function_name == "calculate_technical_indicators":
                    result = calculate_technical_indicators(**function_input)
                elif function_name == "compare_stocks":
                    result = compare_stocks(**function_input)
                else:
                    result = f"Unknown function: {function_name}"
                
                function_results.append(result)
            
            # Prepare messages for second API call
            messages_history = [{"role": "user", "content": user_query}]
            
            if assistant_message:
                messages_history.append(assistant_message)
            
            messages_history.extend([
                function_call_item,
                {
                    "type": "function_call_result",
                    "function_call_id": function_call_id,
                    "function_call_results": function_results
                }
            ])
            
            # Step 2: Send results back to AI for analysis
            print("🤖 AI analyzing the stock data...")
            
            final_data = {
                "model": "small-1", 
                "stream": False,
                "system": system_prompt,
                "messages": messages_history,
                "functions": STOCK_ANALYSIS_TOOLS
            }
            
            final_response = requests.post('https://api.incredible.one/v1/chat-completion',
                                         headers=headers, json=final_data)
            final_response.raise_for_status()
            
            final_result = final_response.json()
            final_items = final_result['result']['response']
            
            # Extract the AI's analysis
            for item in final_items:
                if item.get('role') == 'assistant':
                    analysis = item['content']
                    print("\n" + "="*60)
                    print("📈 AI STOCK ANALYSIS REPORT")
                    print("="*60)
                    print(analysis)
                    print("="*60)
                    return analysis
        
        # If no function calls, just return the initial response
        elif assistant_message:
            print("\n" + "="*60)
            print("🤖 AI RESPONSE")
            print("="*60)
            print(assistant_message['content'])
            print("="*60)
            return assistant_message['content']
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def demo_stock_analysis():
    """
    Run a demo of the stock analysis assistant.
    """
    print("🎯 STOCK ANALYSIS ASSISTANT DEMO")
    print("="*50)
    
    # Example queries to demonstrate different capabilities
    example_queries = [
        "Analyze Apple (AAPL) stock and give me your investment opinion",
        "Compare Tesla (TSLA) vs Microsoft (MSFT) - which is a better buy right now?",
        "What do the technical indicators say about Google (GOOGL) stock trends?",
        "Should I invest in Amazon (AMZN)? What are the risks and opportunities?"
    ]
    
    print("🚀 Here are some example questions you can ask:")
    for i, query in enumerate(example_queries, 1):
        print(f"{i}. {query}")
    
    print("\n" + "="*50)
    print("📊 Running analysis for: Apple (AAPL)")
    print("="*50)
    
    # Run one example analysis
    analyze_stock_with_ai("Analyze Apple (AAPL) stock. Get the current price, technical indicators, and give me your investment analysis with both opportunities and risks.")

def what_makes_this_special():
    """
    Explain why this stock analysis example is special.
    """
    print("\n" + "🌟 WHY THIS STOCK ANALYSIS ASSISTANT IS SPECIAL")
    print("="*60)
    
    print("""
💡 **Real-World Integration:**
   • Uses actual Yahoo Finance data - same data used by financial professionals
   • Live stock prices, market caps, trading volumes
   • Historical data for trend analysis

🧠 **AI-Powered Analysis:**
   • AI interprets complex financial data and explains it in simple terms
   • Provides balanced investment perspectives with risks and opportunities
   • Educational explanations of technical indicators

📊 **Advanced Technical Analysis:**
   • Moving averages (SMA 20, SMA 50) for trend identification
   • RSI (Relative Strength Index) for momentum analysis
   • Support and resistance levels for entry/exit points
   • Volatility analysis for risk assessment

⚡ **Function Calling Magic:**
   • AI automatically chooses which analysis tools to use based on your question
   • Chains multiple function calls together for comprehensive analysis
   • Combines real-time data with AI reasoning

🎯 **Practical Applications:**
   • Personal investment research assistant
   • Portfolio analysis and optimization  
   • Market trend identification
   • Educational tool for learning about stocks
   • Automated financial reporting

🔮 **What You Could Build Next:**
   • Automated portfolio rebalancing alerts
   • Daily market summary emails
   • Custom stock screening based on your criteria
   • Risk assessment for portfolio diversification
   • Integration with brokerage APIs for live trading

This demonstrates how AI + function calling + real-world APIs = powerful applications!
""")

if __name__ == "__main__":
    print("📈 Stock Analysis Assistant - AI-Powered Investment Analysis")
    print("="*65)
    
    # Check if required library is installed
    try:
        import yfinance
        print("✅ Yahoo Finance integration ready!")
    except ImportError:
        print("❌ Missing yfinance library!")
        print("📦 Install with: pip install yfinance")
        exit(1)
    
    # Run the demo
    demo_stock_analysis()
    
    # Show what makes it special
    what_makes_this_special()
    
    print("\n🎉 Try asking your own stock analysis questions!")
    print("💡 Example: 'Should I buy Tesla stock right now?'")
    print("💡 Example: 'Compare Apple vs Google stock performance'")
    print("💡 Example: 'What are the technical indicators saying about Bitcoin?'")
