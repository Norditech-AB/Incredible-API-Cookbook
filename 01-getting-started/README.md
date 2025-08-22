# Getting Started with Incredible API

**Learn the fundamentals step-by-step with simple, easy-to-understand examples.**

## 🌟 Start Here: Hello World!

**Brand new to APIs?** Start with Hello World - designed for anyone:

```bash
python 0_hello_world.py
```

This teaches you:

- How APIs work (in plain English!)
- What happens when you call the API
- Why this simple example is amazing
- What incredible things you can build next

## 📚 Learning Path

Complete these tutorials in order:

1. **🌟 Hello World** - Your first API call (perfect for beginners!)
2. **🔰 Basic Chat** - Learn the fundamentals
3. **🤖 Multiple Models** - Try different AI models
4. **💬 Conversations** - Chat back and forth with AI
5. **🌊 Streaming** - See responses in real-time
6. **⚡ Functions** - Give AI special powers

## ⚡ Quick Start

```bash
# 1. Navigate to getting started
cd 01-getting-started

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up your API key
cp env.example .env
# Edit .env with your API key and user ID

# 4. Start with Hello World
python 0_hello_world.py

# 5. Continue in order
python 1_basic_chat.py
```

## 📁 Tutorial Files

### 🌟 **0_hello_world.py** - Hello World! (Start Here)

**Perfect for:** Complete beginners, non-technical users

```bash
python 0_hello_world.py
```

**You'll see:**

```
🌟 Welcome to Incredible API - Hello World!
👤 You asked: Hello! What can you help me with?
🤔 Thinking...
🤖 AI replied: Hello! I'm an AI assistant...

🤔 WHAT JUST HAPPENED?
Think of the Incredible API like having a conversation...
```

**Special because:** Uses everyday language, explains each step, perfect for sharing with non-technical team members.

### 🔰 **1_basic_chat.py** - Your First Technical API Call

Send a message to AI and get a response back.

```bash
python 1_basic_chat.py
```

### 🤖 **2_multiple_models.py** - Try Different AI Models

Test different AI models to see how they respond.

```bash
python 2_multiple_models.py
```

### 💬 **3_conversation.py** - Chat Back and Forth

Have real conversations where AI remembers previous messages.

```bash
python 3_conversation.py
```

**Example:**

```
👤 You: What's the capital of France?
🤖 AI: The capital of France is Paris.
👤 You: What's the population of that city?
🤖 AI: Paris has approximately 2.1 million people...
✨ AI remembered we were talking about Paris!
```

### 🌊 **4_streaming_chat.py** - Real-Time Responses

See AI respond word-by-word like ChatGPT.

```bash
python 4_streaming_chat.py
```

### ⚡ **5_function_calling.py** - Give AI Special Powers

Let AI call your custom functions for calculations and data.

```bash
python 5_function_calling.py
```

**Example:**

```
💬 You: What is 25 + 17?
🔧 AI wants to use function: add_numbers
🧮 Calculating: 25 + 17 = 42
🤖 AI: The answer is 42!
```

## 🛠️ Setup

**Prerequisites:**

- Python 3.8+
- Internet connection
- Incredible API account

**Environment (.env file):**

```bash
INCREDIBLE_API_KEY=your_api_key_here
USER_ID=your_user_id_here
```

**Dependencies:**

```
requests>=2.31.0
python-dotenv>=1.0.0
```

Install: `pip install -r requirements.txt`

## 🔧 Troubleshooting

**"Missing API key":**

- Create `.env` file
- Add `INCREDIBLE_API_KEY`
- Get key from [Incredible API dashboard](https://incredible.one)

**"Connection Error":**

- Check internet connection
- Verify API key is valid

## 🎉 Next Steps

After completing all tutorials:

- Build your own AI applications
- Create custom integrations
- Explore advanced features
- Check out other cookbook examples

**Ready to start?** Run `python 0_hello_world.py` 🚀
