# Getting Started with Incredible API

**Learn the fundamentals step-by-step with simple, easy-to-understand examples.**

Each file focuses on one concept so you can learn at your own pace!

## 🎯 What You'll Learn

We've split everything into 7 simple steps:

1. **🔰 Basic Chat** - Your first API call (super simple!)
2. **🤖 Multiple Models** - Try different AI models
3. **💬 Conversations** - Chat back and forth with AI
4. **🌊 Streaming** - See responses appear in real-time
5. **⚡ Functions** - Give AI special powers
6. **📧 Gmail** - Send emails with AI
7. **🔍 Research** - AI research assistant

## ⚡ Quick Start

```bash
# 1. Navigate to getting started
cd 01-getting-started

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up your API key
cp env.example .env
# Edit .env with your API key and user ID

# 4. Start with the first example
python 1_basic_chat.py
```

**That's it!** Continue with each numbered file in order.

## 📁 Tutorial Files

### 🔰 **1_basic_chat.py** - Your First API Call

**What it does:** Send a simple message to AI and get a response back.

**Perfect for:** Complete beginners who want to see the API work.

```bash
python 1_basic_chat.py
```

**You'll see:**

```
🎉 Welcome to Incredible API!
💬 You: Hello! Can you say hi back to me?
🚀 Sending your message to AI...
🤖 AI: Hello there! Nice to meet you! 👋
✅ Success! You've made your first API call!
```

---

### 🤖 **2_multiple_models.py** - Try Different AI Models

**What it does:** Test different AI models to see how they respond.

**Perfect for:** Learning about available models and their differences.

```bash
python 2_multiple_models.py
```

**You'll see:**

```
🤖 Testing Different AI Models
📋 Available Models:
   small-1: ✅ Available now - Fast and efficient
   tiny-1: 🔜 Coming soon - Ultra fast
   big-1: 🔜 Coming soon - More powerful
   huge-1: 🔜 Coming soon - Most advanced
```

---

### 💬 **3_conversation.py** - Chat Back and Forth

**What it does:** Have a real conversation where AI remembers what you talked about.

**Perfect for:** Understanding how conversations work.

```bash
python 3_conversation.py
```

**You'll see:**

```
👤 You: What's the capital of France?
🤖 AI: The capital of France is Paris.
👤 You: What's the population of that city?
🤖 AI: Paris has approximately 2.1 million people...
✨ Notice how AI remembered we were talking about Paris!
```

---

### 🌊 **4_streaming_chat.py** - Real-Time Responses

**What it does:** See AI respond word-by-word like ChatGPT.

**Perfect for:** Learning the difference between streaming and regular responses.

```bash
python 4_streaming_chat.py
```

**You'll see responses appear gradually, just like in ChatGPT!**

---

### ⚡ **5_function_calling.py** - Give AI Special Powers

**What it does:** Let AI call your custom functions to do calculations and get data.

**Perfect for:** Understanding how to extend AI capabilities.

```bash
python 5_function_calling.py
```

**You'll see:**

```
💬 You: What is 25 + 17?
🔧 AI wants to use function: add_numbers
🧮 Calculating: 25 + 17 = 42
🤖 AI: The answer is 42!
```

---

### 📧 **6_gmail_integration.py** - Send Emails with AI

**What it does:** Connect AI to Gmail so it can send emails automatically.

**Perfect for:** Building AI assistants that can communicate via email.

```bash
python 6_gmail_integration.py
```

**You'll see:**

```
📤 Sending email to: test@example.com
✅ Email sent successfully!
🎉 Your AI can now send emails!
```

---

### 🔍 **7_perplexity_integration.py** - AI Research Assistant

**What it does:** Use AI to do intelligent research on any topic.

**Perfect for:** Building AI that can gather real-time information.

```bash
python 7_perplexity_integration.py
```

**You'll see AI researching topics and providing detailed answers with sources!**

## 🛠️ Setup Details

### Prerequisites

- Python 3.8 or newer
- Internet connection
- Incredible API account

### Environment Variables

Create a `.env` file with:

```bash
INCREDIBLE_API_KEY=your_api_key_here
USER_ID=your_user_id_here
```

**Get these from your [Incredible API dashboard](https://incredible.one)**

### Dependencies

All examples use these Python packages:

```
requests>=2.31.0
python-dotenv>=1.0.0
```

Install with: `pip install -r requirements.txt`

## 🔧 Troubleshooting

### "Missing API key" Error

- Make sure `.env` file exists
- Check that `INCREDIBLE_API_KEY` is set correctly
- Get your API key from the Incredible API dashboard

### "Connection Error"

- Check your internet connection
- Verify API key is valid
- Try again in a few minutes

### Integration Errors (File 6)

- Gmail: Connect Gmail integration in your dashboard
- Perplexity: Add Perplexity API key in your dashboard

## 📚 API Response Formats

### Regular Responses

```json
{
  "result": {
    "response": [
      {
        "content": "AI response here...",
        "role": "assistant"
      }
    ]
  }
}
```

### Streaming Responses

```
data: {"content": {"type": "content_chunk", "content": "word"}}
data: {"content": {"type": "content_chunk", "content": " by"}}
data: {"content": {"type": "content_chunk", "content": " word"}}
data: {"content": "[DONE]"}
```

_The examples handle all response parsing for you!_

## 🎉 Next Steps

After completing all 6 tutorials, you'll be ready to:

- Build your own AI applications
- Create custom integrations
- Understand advanced API features
- Explore the other cookbook examples

**Congratulations on learning the Incredible API! 🚀**

## 💡 Tips for Success

1. **Go in order** - Each example builds on the previous one
2. **Read the comments** - They explain what each line does
3. **Experiment** - Try changing messages and see what happens
4. **Don't skip steps** - Each concept is important
5. **Have fun** - You're building with cutting-edge AI!

---

**Ready to start?** Run `python 1_basic_chat.py` and make your first API call! 🎊
