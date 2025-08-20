# Incredible API Cookbook 🧪

**Learn to build AI agents with the Incredible API through hands-on, executable examples.**

Start with the fundamentals and master the chat completion API step by step!

## 🎯 **What is Incredible API?**

A powerful API for creating AI agents that can:

- **Chat completion** with advanced AI models (`small-1`, with `big-1`, `huge-1` coming soon)
- **Function calling** to extend AI capabilities with custom functions
- **Integrations** with popular services like Gmail, Google Sheets, Perplexity AI, and more
- **Streaming responses** for real-time interaction

## 🎓 **Start Here: Getting Started**

**New to Incredible API?** Begin with our step-by-step tutorial:

### 📚 **[Getting Started Guide](./01-getting-started/)**

**Master the Incredible API fundamentals with hands-on examples**

```bash
cd 01-getting-started && python 1_basic_chat.py
```

**Complete progressive tutorial covering:**

#### 🔰 **[1. Basic Chat](./01-getting-started/1_basic_chat.py)**

- Simple chat completion requests
- Multi-model support (`small-1`, with more coming)
- Multi-turn conversations
- Error handling and best practices

#### 🌊 **[2. Streaming Chat](./01-getting-started/2_streaming_chat.py)**

- Real-time response streaming
- Server-Sent Events (SSE) handling
- Comparison with non-streaming responses

#### ⚡ **[3. Function Calling](./01-getting-started/3_function_calling.py)**

- Extend AI with custom functions
- Weather API integration example
- Structured function responses

#### 🔌 **[4. Integrations](./01-getting-started/4_integrations.py)**

- Gmail integration for sending emails
- Perplexity AI for intelligent research
- Pre-built service connections

**Everything you need to start building with Incredible API!**

---

## 📋 **API Response Formats**

Understanding how to parse API responses is crucial for working with the Incredible API:

### **Non-Streaming Responses**

```json
{
  "result": {
    "response": [
      {
        "content": "AI response content here...",
        "role": "assistant"
      }
    ],
    "thinking": "AI reasoning process..."
  }
}
```

**To extract the response text:** Use `result.result.response[0].content`

### **Streaming Responses (Server-Sent Events)**

```
data: {"content": {"type": "thinking_chunk", "content": "reasoning..."}}
data: {"content": {"type": "content_chunk", "content": "response text"}}
data: {"content": "[DONE]"}
```

**To extract streaming text:** Use `chunk_data.content.content`

_See the tutorial examples for complete parsing implementations._

## 🚀 **Quick Start - 2 Minutes to Running**

### 1. **Clone and Setup**

```bash
git clone https://github.com/yourusername/incredible-api-cookbook.git
cd incredible-api-cookbook/01-getting-started
```

### 2. **Install Dependencies**

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. **Configure Your API Key**

```bash
# Copy the example environment file
cp env.example .env

# Edit .env with your Incredible API credentials
INCREDIBLE_API_KEY=your_api_key_here
USER_ID=your_user_id_here
```

### 4. **Run Your First Example**

```bash
python 1_basic_chat.py
```

**That's it!** You're now making API calls with Incredible API. Continue with the other examples to learn more advanced features.

## ⚙️ **Setup Requirements**

### Prerequisites

- **Python 3.8+** installed on your system
- **Incredible API Account**: Sign up at [https://incredible.one](https://incredible.one)

### Required Environment Variables

```bash
INCREDIBLE_API_KEY=your_api_key_here
USER_ID=your_user_id_here
```

**Get these from your Incredible API dashboard after signing up.**

### Optional Integrations (for advanced examples)

- **Gmail**: For email integration examples
- **Perplexity AI**: For research functionality
- **Weather API**: For function calling examples

_See the detailed [Getting Started README](./01-getting-started/README.md) for complete setup instructions._

## 📖 **Tutorial Structure**

The getting-started folder is organized for progressive learning:

```
01-getting-started/
├── 1_basic_chat.py           # Start here - Basic chat completion
├── 2_streaming_chat.py       # Real-time streaming responses
├── 3_function_calling.py     # Extend AI with custom functions
├── 4_integrations.py         # Connect to external services
├── requirements.txt          # Python dependencies
├── env.example              # Configuration template
├── README.md                # Detailed tutorial guide
└── Incredible_API_Postman_Collection.json  # API testing collection
```

**Learning Path:**

1. **Start** with `1_basic_chat.py` to understand the fundamentals
2. **Progress** through each numbered example in order
3. **Configure** your credentials once in `.env`
4. **Run** each script individually to see concepts in action

## 🤝 Contributing

We welcome contributions to improve this tutorial! Whether it's:

- **Tutorial improvements** - Making examples clearer or more comprehensive
- **Bug fixes** - Fixing issues in the example code
- **Additional examples** - Adding more learning scenarios
- **Documentation** - Better explanations and setup guides

Please read our [Contributing Guide](./CONTRIBUTING.md) to get started.

## 📖 Additional Resources

- [**Official API Documentation**](https://docs.incredible.one)
- [**Chat Completion API Reference**](https://docs.incredible.one/api-reference/chat)
- [**Integrations Reference**](https://docs.incredible.one/api-reference/integrations)
- [**Community Forum**](https://community.incredible.one)
- [**Support**](mailto:support@incredible.one)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

**Ready to master the Incredible API?** Start with the [getting-started tutorial](./01-getting-started/) and build your first AI agent in 2 minutes! 🚀
