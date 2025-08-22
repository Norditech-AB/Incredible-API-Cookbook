# Function Calling (Tools) with Incredible API

**Give your AI superpowers to interact with the real world!**

✅ **All examples tested and working**

Function calling allows AI to execute custom functions, access APIs, perform calculations, and interact with systems. Transform static AI responses into dynamic, actionable workflows.

## 🎯 What You'll Learn

Progressive examples teaching advanced function calling:

1. **🧮 Simple Calculator** - Single function calling
2. **🛠️ Multiple Tools** - Weather, calculator, and time functions
3. **📊 JSON Extraction** - Structured data output
4. **🚀 Advanced Workflow** - Multi-step function calling
5. **📈 Stock Analysis** - Real-world Yahoo Finance integration

## ⚡ Quick Start

```bash
# 1. Navigate to function calling
cd 02-function-calling

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Set up API key
cp env.example .env
# Edit .env with your credentials

# 4. Run examples in order
python3 1_simple_calculator.py
python3 2_multiple_tools.py
python3 3_json_extraction.py
python3 4_advanced_workflow.py
python3 5_stock_analysis.py
```

## 🔧 How It Works

Based on [Anthropic's tool use documentation](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview):

### 1. Define Functions

```python
def calculate_sum(a, b):
    """Add two numbers together."""
    return a + b

# Tell AI about this function
functions = [{
    "name": "calculate_sum",
    "description": "Add two numbers together",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {"type": "number", "description": "First number"},
            "b": {"type": "number", "description": "Second number"}
        },
        "required": ["a", "b"]
    }
}]
```

### 2. AI Uses Function

```json
{
  "result": {
    "response": [
      {
        "type": "function_call",
        "function_calls": [
          {
            "name": "calculate_sum",
            "input": { "a": 15, "b": 25 }
          }
        ]
      }
    ]
  }
}
```

### 3. Execute & Return Results

```python
result = calculate_sum(15, 25)  # Returns 40
# Send result back to AI
```

## 📁 Examples

### 🧮 **1_simple_calculator.py** - Your First Function Call

Basic calculator that AI can use for math.

```bash
python3 1_simple_calculator.py
```

**You'll see:**

```
👤 User: What is 127 + 349?
🔧 AI wants to use tool: calculate_sum
🧮 Executing: calculate_sum(127, 349) = 476
🤖 AI: The sum of 127 and 349 is 476.
```

### 🛠️ **2_multiple_tools.py** - Multiple Functions

AI chooses between weather, calculator, and time functions.

```bash
python3 2_multiple_tools.py
```

### 📊 **3_json_extraction.py** - Structured Data

Extract structured JSON from unstructured text.

```bash
python3 3_json_extraction.py
```

**Example:**

```
👤 Input: "John Smith, age 30, lives in New York, works as Engineer"
📊 JSON Output: {
  "name": "John Smith",
  "age": 30,
  "city": "New York",
  "occupation": "Engineer"
}
```

### 🚀 **4_advanced_workflow.py** - Complex Workflows

Multi-step workflows combining email, calendar, and task management.

```bash
python3 4_advanced_workflow.py
```

### 📈 **5_stock_analysis.py** - Real-World Financial AI

AI-powered stock analysis with Yahoo Finance data.

```bash
python3 5_stock_analysis.py
```

**Features:**

- Real stock data from Yahoo Finance
- AI analysis of market trends and indicators
- Technical indicators (RSI, moving averages)
- Investment recommendations with risk assessment

**Sample output:**

```
📈 AI STOCK ANALYSIS REPORT
=============================================================
Apple (AAPL): $193.58 (+1.23%)
📊 Technical Indicators:
   • RSI: 45.2 (Neutral)
   • 20-day SMA: $190.45 (Bullish signal)
   • Support: $185.20 | Resistance: $198.50

📈 Investment Analysis:
Strong fundamentals with P/E ratio of 28.5...
⚠️ Risks: Market volatility, regulatory concerns
🚀 Opportunities: Strong ecosystem, services growth
=============================================================
```

## 🛠️ Setup

**Prerequisites:**

- Python 3.8+
- Incredible API account

**Environment (.env):**

```bash
INCREDIBLE_API_KEY=your_api_key_here
USER_ID=your_user_id_here
```

**Dependencies:**

```
requests>=2.31.0
python-dotenv>=1.0.0
yfinance>=0.2.18        # For stock analysis
```

Install: `pip3 install -r requirements.txt`

## 💡 Key Concepts

**Function Schema:**

```python
{
    "name": "function_name",
    "description": "Clear description of what this does",
    "parameters": {
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "What this parameter is for"
            }
        },
        "required": ["param1"]
    }
}
```

**Execution Flow:**

1. Define functions with schema
2. Send query + available functions to API
3. Check for `function_call` in response
4. Execute functions locally
5. Send results back using `function_call_result`
6. Get final response with results

## 🔍 Troubleshooting

**"500 Internal Server Error":**

- Ensure ALL function definitions use `"parameters"` (not `"input_schema"`)
- Check schema consistency

**"AI isn't using my function":**

- Make function description clear and specific
- Verify schema matches function parameters

**"Function execution failed":**

- Add error handling in function code
- Validate inputs before processing

## 🎉 What's Next?

After mastering function calling:

- Build AI assistants that perform real actions
- Integrate with external APIs
- Create automated workflows
- Process structured data with AI
- Build complex applications where AI orchestrates systems

---

**Ready to give your AI superpowers?** Start with `python3 1_simple_calculator.py` 🎊
