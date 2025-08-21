# Function Calling (Tools) with Incredible API

**Master the power of function calling - give your AI superpowers to interact with the real world!**

✅ **All examples tested and working** - Ready to run out of the box!

Function calling (also known as "tools" in Claude terminology) allows AI to execute custom functions, access external APIs, perform calculations, and interact with systems. This transforms static AI responses into dynamic, actionable workflows.

## 🎯 What You'll Learn

Each example builds upon the previous one, teaching you progressively advanced function calling concepts:

1. **🧮 Simple Calculator** - Single function calling (like Anthropic's example)
2. **🛠️ Multiple Tools** - Weather, calculator, and time functions
3. **📊 JSON Extraction** - Using tools for structured data output
4. **🚀 Advanced Workflow** - Multi-step function calling with real applications
5. **📈 Stock Analysis** - Real-world example with Yahoo Finance API integration
6. **🐉 AI Dungeon Master** - **Most Interactive!** RPG adventure with user input, combat, and storytelling

## ⚡ Quick Start

```bash
# 1. Navigate to function calling examples
cd 02-function-calling

# 2. Install dependencies (if not already done)
pip3 install -r requirements.txt

# 3. Set up your API key
cp env.example .env
# Edit .env with your API key and user ID

# 4. Run the examples in order (each builds on the previous)
python3 1_simple_calculator.py      # ✅ Start here - basic function calling
python3 2_multiple_tools.py         # ✅ Then this - AI choosing between tools
python3 3_json_extraction.py        # ✅ Then this - structured data extraction
python3 4_advanced_workflow.py      # ✅ Then this - complex multi-step workflows
python3 5_stock_analysis.py         # 🎉 Fun example - real-world stock analysis
python3 6_ai_dungeon_master.py      # 🐉 ULTIMATE - Interactive RPG adventure!
```

## 🔧 How Function Calling Works

Based on [Anthropic's tool use documentation](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview#single-tool-example), here's the flow:

### 1. **Define Functions**

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

### 2. **AI Decides to Use Function**

```json
{
  "result": {
    "response": [
      { "role": "assistant", "content": "I'll calculate that for you." },
      {
        "type": "function_call",
        "function_call_id": "abc-123",
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

### 3. **Execute Function & Return Results**

```python
# Your code executes the function
result = calculate_sum(15, 25)  # Returns 40

# Send result back to AI in message history
function_result_message = {
    "type": "function_call_result",
    "function_call_id": "abc-123",
    "function_call_results": [result]
}
```

### 4. **AI Uses Results in Final Response**

```
🤖 AI: "The sum of 15 and 25 is 40."
```

## 📁 Example Files

### 🧮 **1_simple_calculator.py** - Your First Function Call

**What it does:** Implements a simple calculator that AI can use for math problems.

**Perfect for:** Understanding the basic function calling flow.

**Inspired by:** [Anthropic's single tool example](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview#single-tool-example)

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

---

### 🛠️ **2_multiple_tools.py** - Multiple Functions Available

**What it does:** Gives AI access to weather, calculator, and time functions.

**Perfect for:** Learning how AI chooses between multiple available tools.

```bash
python3 2_multiple_tools.py
```

**You'll see AI intelligently choose the right tool for each question:**

- Math questions → Calculator
- Time questions → Time function
- Weather questions → Weather function

---

### 📊 **3_json_extraction.py** - Structured Data Output

**What it does:** Uses function calling to extract structured JSON from unstructured text.

**Perfect for:** Data processing, form filling, and content analysis.

**Based on:** [Anthropic's JSON mode example](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview#json-mode)

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

---

### 🚀 **4_advanced_workflow.py** - Real-World Application

**What it does:** Combines multiple functions in a complex workflow (email + calendar + task management).

**Perfect for:** Understanding how to build practical AI assistants.

```bash
python3 4_advanced_workflow.py
```

**Example workflow:** AI schedules a meeting, sends confirmation email, and creates follow-up tasks.

---

### 📈 **5_stock_analysis.py** - AI-Powered Stock Analysis (Fun Real-World Example!)

**What it does:** Creates an intelligent stock analysis assistant using real Yahoo Finance data.

**Perfect for:** Seeing function calling in action with real-world financial APIs.

```bash
python3 5_stock_analysis.py
```

**🎯 Features:**

- **Real stock data** from Yahoo Finance API (same data professionals use)
- **AI analysis** of market trends, technical indicators, and investment opportunities
- **Technical indicators** like moving averages, RSI, support/resistance levels
- **Multi-stock comparison** side-by-side analysis
- **Investment recommendations** with risk assessment
- **Educational explanations** of financial concepts in simple terms

**You'll see AI analyze stocks like:**

```
📈 AI STOCK ANALYSIS REPORT
=============================================================
Based on the current data for Apple (AAPL):

💰 Current Price: $193.58 (+1.23%)
📊 Technical Indicators:
   • RSI: 45.2 (Neutral - room for growth)
   • 20-day SMA: $190.45 (Price above average - bullish signal)
   • Support Level: $185.20 | Resistance: $198.50

📈 Investment Analysis:
Apple shows solid fundamentals with a P/E ratio of 28.5 and strong market
position. The stock is currently in a neutral RSI zone, suggesting it's
neither overbought nor oversold...

⚠️ Risks: Market volatility, regulatory concerns
🚀 Opportunities: Strong ecosystem, services growth
=============================================================
```

**🌟 Why This Example is Special:**

- **Real-world integration** with financial APIs
- **Educational value** - teaches both AI and finance concepts
- **Practical application** - actually useful for investment research
- **Advanced function chaining** - AI automatically chooses which analysis tools to use
- **Professional-grade data** - same Yahoo Finance API used by trading platforms

**Required:** `pip install yfinance` (automatically included in requirements.txt)

---

### 🐉 **6_ai_dungeon_master.py** - Interactive RPG Adventure (ULTIMATE Function Calling Experience!)

**What it does:** Creates a fully interactive text-based RPG where you type commands and the AI Dungeon Master responds with immersive storytelling and real game mechanics.

**Perfect for:** The most engaging and fun way to learn function calling concepts through actual gameplay!

```bash
python3 6_ai_dungeon_master.py
```

**🎮 Interactive Features:**

- **🎭 Character Creation** - Choose your name and class (Warrior, Mage, Rogue)
- **🎲 Real RPG Mechanics** - Dice rolls, combat, leveling, experience points
- **💬 Dynamic Storytelling** - AI narrates your adventure based on your choices
- **⚔️ Turn-Based Combat** - Fight goblins, wolves, skeletons with strategic gameplay
- **🎒 Inventory System** - Find treasures, use potions, upgrade equipment
- **📈 Character Progression** - Level up, gain new abilities, increase health
- **🗺️ Exploration** - Multiple locations with unique encounters
- **💾 Save/Load System** - Continue your adventure across multiple sessions

**You'll experience gameplay like:**

```
🎯 TURN 15
------------------------------
👤 Your action: attack the goblin with my sword

🎲 AI Dungeon Master is using game mechanics...
⚡ DM Action: roll_dice
🎲 Rolling 1d20+2 for player attack...
🎯 Rolled: [18] = 20
✨ 🌟 CRITICAL SUCCESS! The dice gods smile upon you!

⚡ DM Action: combat_system
⚔️  COMBAT ENCOUNTER!
🐉 A wild Goblin Scout appears!
❤️  Enemy Health: 20

🔄 ROUND 1
👤 Your Health: 85/100
🐉 Goblin Scout Health: 20/20
⚔️  You deal 12 damage to Goblin Scout!
💥 Goblin Scout deals 3 damage to you!
🎉 Victory! Goblin Scout is defeated!
⭐ Gained 30 experience! (150 → 180 XP)
💰 Found 15 gold! (75 → 90 coins)
📦 Added Magic Ring to inventory!

============================================================
🎭 DUNGEON MASTER
============================================================
Excellent strike! Your blade finds its mark perfectly as the
goblin stumbles backward. With a final gurgle, it collapses,
leaving behind a glinting magic ring among the scattered
coins.

As you catch your breath, you notice three paths ahead:
🏰 North: Ancient stone doorway with mysterious runes
🌲 East: Dense forest path with bird songs
💀 South: Dark corridor echoing with distant howls

What do you choose, brave warrior?
============================================================

🎮 What do you want to do next?
👤 Your action: examine the magic ring and head north to the stone doorway
```

**🌟 Why This Is The ULTIMATE Learning Experience:**

- **🎯 Most Interactive** - You actually PLAY with function calling instead of just watching
- **🎲 Complex Function Chaining** - AI combines multiple functions for rich gameplay
- **📚 Educational Through Fun** - Learn advanced concepts while having an amazing time
- **🔄 Dynamic Responses** - Every choice creates different outcomes and stories
- **⚡ Real-Time Function Calling** - See functions execute as you play
- **🎮 Gamification** - Makes abstract programming concepts tangible and engaging

**🛠️ Function Calling Magic In Action:**

```python
# The AI automatically uses these functions based on your actions:
roll_dice()           # Combat rolls, skill checks, random events
manage_player_stats() # Health, experience, leveling up
manage_inventory()    # Treasures, potions, equipment
combat_system()       # Turn-based battles with strategy
generate_encounter()  # Random adventures and discoveries
save_game_state()     # Persistent progress across sessions
```

**💡 What You'll Learn:**

- How AI makes intelligent function choices based on context
- Complex multi-function workflows in real-time
- State management across multiple function calls
- Interactive user input processing with AI
- Dynamic storytelling with structured game mechanics
- Real-world application of function calling concepts

**🚀 Real-World Applications:**

- **Interactive Customer Service** - Engaging bots with personality
- **Educational Gamification** - Learning through interactive experiences
- **Training Simulations** - AI-guided skill development
- **Entertainment Applications** - Games and interactive stories
- **Personalized User Experiences** - Dynamic content based on user choices

**💬 Example Commands You Can Try:**

- `"look around"` - Explore your surroundings
- `"attack the monster"` - Engage in combat
- `"check my inventory"` - See your items and equipment
- `"drink health potion"` - Use items strategically
- `"cast a spell"` - Use your class abilities
- `"search for treasure"` - Look for loot and secrets
- `"save game"` - Save your progress
- `"go north/south/east/west"` - Navigate the world

This is function calling at its most engaging - you're not just learning code, you're living an adventure! 🎉

## 🛠️ Setup Details

### Prerequisites

- Python 3.8 or newer
- Incredible API account with API key
- Understanding of basic API calls (complete `01-getting-started` first)

### Environment Variables

Create a `.env` file with:

```bash
INCREDIBLE_API_KEY=your_api_key_here
USER_ID=your_user_id_here
```

### Dependencies

```
requests>=2.31.0
python-dotenv>=1.0.0
yfinance>=0.2.18        # For stock analysis example
```

Install with: `pip3 install -r requirements.txt`

**Note:** The `yfinance` library is required for the stock analysis example and provides access to Yahoo Finance data.

## 💡 Key Concepts

### **Tool Schema Definition**

Every function needs a clear schema so AI understands how to use it:

```python
{
    "name": "function_name",
    "description": "Clear description of what this function does",
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

### **Function Execution Flow**

1. **Define** your functions with `parameters` schema
2. **Send** user query + available functions to API
3. **Check** response for `type: "function_call"` items
4. **Execute** the requested function(s) locally
5. **Send** results back using `function_call_result` message type
6. **Get** final response with function results incorporated

### **Best Practices**

- ✅ **Clear descriptions** - AI needs to understand when to use each tool
- ✅ **Proper error handling** - Functions might fail or get invalid inputs
- ✅ **Type validation** - Validate inputs before executing functions
- ✅ **Meaningful names** - Use descriptive function and parameter names
- ✅ **Return useful data** - Functions should return actionable information

## 🔍 Troubleshooting

### "500 Internal Server Error with multiple tools"

- Ensure ALL function definitions use `"parameters"` (not `"input_schema"`)
- Mixed schema formats in the same request will cause API errors
- Check that each tool definition follows the exact same structure

### "Data parsing errors in extraction functions"

- Functions should handle raw text input (like "$899" or "around 500 people")
- Use regex to extract numeric values from descriptive text
- Make optional parameters truly optional with default values

### "AI isn't using my function"

- Check function description is clear and specific
- Ensure the user query actually needs that function
- Verify the schema matches your function parameters

### "Function execution failed"

- Add error handling in your function code
- Validate inputs before processing
- Return meaningful error messages

### "Unexpected function calls"

- Make function descriptions more specific
- Add conditions for when the function should be used
- Consider using fewer, more focused functions

## 🎉 What's Next?

After mastering function calling, you'll be ready to:

- **Build AI assistants** that can perform real actions
- **Integrate with external APIs** through functions
- **Create automated workflows** combining multiple tools
- **Process structured data** with AI-powered extraction
- **Build complex applications** where AI orchestrates multiple systems

## 🚀 Advanced Topics

- **Error handling and retries** in function calls
- **Streaming function calls** for real-time updates
- **Function call chaining** for complex workflows
- **Dynamic function generation** based on context
- **Function call monitoring** and logging

---

**Ready to give your AI superpowers?** Start with `python3 1_simple_calculator.py` and watch AI come alive! 🎊

_This section is inspired by [Anthropic's excellent tool use documentation](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) - adapted for the Incredible API._
