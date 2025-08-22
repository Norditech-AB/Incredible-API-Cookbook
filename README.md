# Incredible API Cookbook 🧪

**Learn to build AI agents with the Incredible API through hands-on, executable examples.**

## 🎯 What is Incredible API?

A powerful API for creating AI agents with:

- **Chat completion** with advanced models (`small-1`, `big-1`, `huge-1` coming soon)
- **Function calling** to extend AI capabilities
- **Streaming responses** for real-time interaction
- **Integrations** with Gmail, Google Sheets, Perplexity AI, and more

## 🚀 Quick Start (2 Minutes)

```bash
# 1. Clone and navigate
git clone https://github.com/yourusername/incredible-api-cookbook.git
cd incredible-api-cookbook/01-getting-started

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up API key
cp env.example .env
# Edit .env with your credentials

# 4. Run first example
python 0_hello_world.py
```

**Get your API key:** [https://incredible.one](https://incredible.one)

## 📚 Learning Path

### **[Getting Started](./01-getting-started/)** - Master the Fundamentals

```bash
cd 01-getting-started
```

**Progressive tutorials:**

- **🌟 Hello World** - Perfect for complete beginners
- **🔰 Basic Chat** - Your first API call
- **🤖 Multiple Models** - Try different AI models
- **💬 Conversations** - Chat back and forth
- **🌊 Streaming** - Real-time responses
- **⚡ Functions** - Give AI special powers

### **[Function Calling](./02-function-calling/)** - Give AI Superpowers

```bash
cd 02-function-calling
```

**Transform AI from chatbot to action-taker:**

- **🧮 Calculator** - Basic function calling
- **🛠️ Multiple Tools** - AI chooses right function
- **📊 JSON Extraction** - Structured data output
- **🚀 Advanced Workflow** - Multi-step automation
- **📈 Stock Analysis** - Real-world example with Yahoo Finance
- **🐉 Dungeon Master** - Experience AI-powered storytelling with real game mechanics
- **🎨 Content Creator** - Complete content pipeline from research to publication

## 📋 API Response Format

### Regular Response

```json
{
  "result": {
    "response": [{ "content": "AI response here", "role": "assistant" }]
  }
}
```

### Streaming Response

```
data: {"content": {"type": "content_chunk", "content": "word"}}
data: {"content": "[DONE]"}
```

## ⚙️ Setup

**Prerequisites:**

- Python 3.8+
- Incredible API account

**Environment variables (.env):**

```bash
INCREDIBLE_API_KEY=your_api_key_here
USER_ID=your_user_id_here
```

## 📖 Resources

- [Official Docs](https://docs.incredible.one)
- [API Reference](https://docs.incredible.one/api-reference/chat)
- [Community Forum](https://community.incredible.one)
- [Support](mailto:support@incredible.one)

## 🤝 Contributing

We welcome improvements! See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

## 📄 License

MIT License - see [LICENSE](./LICENSE) for details.

---

**Ready to master the Incredible API?** Start with `python 0_hello_world.py` and build your first AI agent! 🚀
