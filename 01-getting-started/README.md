# Getting Started with Incredible API

**Learn the fundamentals of the Incredible API chat completion endpoint through hands-on examples.**

Start here before diving into the advanced cookbook examples! This section covers all the core concepts you need to understand.

## 🎯 What You'll Learn

1. **Basic Chat Completion** - Simple requests and responses
2. **Streaming vs Non-Streaming** - Real-time vs batch responses
3. **Function Calling** - Extend AI with custom functions
4. **Integrations** - Use pre-built functions for popular services

## ⚡ Quick Start

```bash
# 1. Navigate to getting started
cd getting-started

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up configuration
cp env.example .env
# Edit .env with your API key and user ID

# 4. Run examples in order
python 1_basic_chat.py
python 2_streaming_chat.py
python 3_function_calling.py
python 4_integrations.py
```

## 📚 Progressive Learning Path

### 1️⃣ Basic Chat (`1_basic_chat.py`)

**Learn the fundamentals**

- Making your first API request
- Understanding request/response format
- Testing different models
- Using custom system prompts
- Multi-turn conversations

**Key Concepts:**

```python
{
    "model": "small-1",           # Which AI model to use
    "stream": False,                  # Non-streaming for simplicity
    "system": "You are a helpful...", # System prompt/personality
    "messages": [                     # Conversation history
        {"role": "user", "content": "Hello!"}
    ]
}
```

### 2️⃣ Streaming Chat (`2_streaming_chat.py`)

**Real-time responses**

- How streaming works (Server-Sent Events)
- Processing chunks as they arrive
- Building responsive chat interfaces
- Performance comparison

**Streaming Benefits:**

- ⚡ **Faster perceived response** - Content appears immediately
- 🎯 **Better UX** - Users see progress in real-time
- 📱 **Responsive apps** - No waiting for complete response

### 3️⃣ Function Calling (`3_function_calling.py`)

**Extend AI capabilities**

- Defining functions for the AI
- Parameter specifications
- Function execution workflow
- Error handling

**Function Definition:**

```python
{
    "name": "get_weather",
    "description": "Get weather for a city",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name"}
        },
        "required": ["city"]
    }
}
```

### 4️⃣ Integrations (`4_integrations.py`)

**Use pre-built services**

- Available integrations (Gmail, Sheets, etc.)
- Feature selection
- Multi-integration workflows
- Authentication requirements

**Integration Usage:**

```python
"integrations": [
    {
        "id": "gmail",
        "features": ["gmail_search", "GMAIL_SEND_EMAIL"]
    }
]
```

## 🔧 API Reference

### Chat Completion Endpoint

```
POST /v1/chat-completion
```

### Required Parameters

- `model` - AI model to use (`small-1` currently available, `tiny-1`, `big-1`, `huge-1` coming soon)
- `messages` - Array of conversation messages

### Optional Parameters

- `stream` - Enable streaming responses (default: `true`)
- `system` - System prompt (default: "You are a helpful assistant.")
- `functions` - Array of custom functions
- `integrations` - Array of integration configurations

### Response Formats

**Non-Streaming:**

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

**Streaming (Server-Sent Events):**

```
data: {"content": {"type": "thinking_chunk", "content": "reasoning..."}}
data: {"content": {"type": "content_chunk", "content": "response text"}}
data: {"content": "[DONE]"}
```

**To extract streaming text:** Use `chunk_data.content.content`  
**Note:** Can filter out `thinking_chunk` types for cleaner output.

## 🚀 Available Models

### Currently Available

| Model     | Provider   | Best For              |
| --------- | ---------- | --------------------- |
| `small-1` | Incredible | Fast, efficient tasks |

### Upcoming Models

| Model    | Provider   | Best For                  |
| -------- | ---------- | ------------------------- |
| `tiny-1` | Incredible | Ultra-fast, simple tasks  |
| `big-1`  | Incredible | Complex reasoning         |
| `huge-1` | Incredible | Advanced analysis & logic |

## 🔌 Available Integrations

| Integration     | ID                | Key Features                |
| --------------- | ----------------- | --------------------------- |
| Gmail           | `gmail`           | Email search, send, read    |
| Google Sheets   | `google_sheets`   | Create, update, read sheets |
| Perplexity AI   | `perplexity`      | Real-time research          |
| Asana           | `asana`           | Task and project management |
| Google Calendar | `google_calendar` | Event management            |
| Google Docs     | `google_docs`     | Document creation           |

## 💡 Best Practices

### System Prompts

```python
# ✅ Good - Specific and actionable
"You are a Python expert. Provide code examples and explain concepts clearly."

# ❌ Bad - Too vague
"You are helpful."
```

### Message Structure

```python
# ✅ Good - Clear roles and content
[
    {"role": "user", "content": "How do I install Python?"},
    {"role": "assistant", "content": "Here's how to install Python..."},
    {"role": "user", "content": "What about pip?"}
]
```

### Function Definitions

```python
# ✅ Good - Clear description and parameters
{
    "name": "calculate_tax",
    "description": "Calculate tax amount for a given income and rate",
    "parameters": {
        "type": "object",
        "properties": {
            "income": {"type": "number", "description": "Annual income"},
            "rate": {"type": "number", "description": "Tax rate as decimal (0.25 for 25%)"}
        },
        "required": ["income", "rate"]
    }
}
```

### Error Handling

```python
try:
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    result = response.json()

except requests.exceptions.RequestException as e:
    print(f"API Error: {e}")
    # Handle specific error cases
```

## 🎓 Learning Progression

1. **Start Here** → `getting-started/` (You are here!)
2. **Simple Examples** → Pick any cookbook folder
3. **Advanced Workflows** → Combine multiple integrations
4. **Custom Development** → Build your own applications

## 🔗 Integration Setup

Before using integrations in examples 4+, you'll need:

### 1. Get API Access

- Sign up at [Incredible Dashboard](https://incredible.one)
- Get your API key and User ID
- Add to `.env` file

### 2. Connect Integrations (OAuth)

For each integration you want to use:

- Gmail: Google OAuth for email access
- Google Sheets: Google OAuth for spreadsheet access
- Perplexity: API key for research capabilities
- Asana: OAuth for task management
- Others: Check individual integration requirements

### 3. Test Connection

Use the getting-started examples to verify:

- API credentials work
- Integrations are properly connected
- Functions execute successfully

## 🛠️ Troubleshooting

### Common Issues

**"Model not found"**

- Check model name spelling
- Verify model is available in your plan
- Try `small-1` as default

**"Integration not found"**

- Verify integration ID is correct
- Check if integration is connected in dashboard
- Ensure OAuth flow is completed

**"Authorization failed"**

- Check API key is correct and active
- Verify `Bearer ` prefix in Authorization header
- Ensure user_id matches your account

**"Functions not working"**

- Verify function definition syntax
- Check parameter types and requirements
- Test with simpler functions first

### Getting Help

1. **Check Examples** - Each file has detailed error handling
2. **Review API Docs** - Check the main API documentation
3. **Test Incrementally** - Start simple, add complexity gradually
4. **Verify Setup** - Ensure all credentials and integrations are configured

## ➡️ Next Steps

Once you've completed all getting-started examples:

### Simple Workflows

- **email-automation** - Automated email responses
- **lead-management** - Lead capture and follow-up
- **research-reporter** - AI-powered research reports

### Advanced Workflows

- **meeting-organizer** - Meeting extraction and calendar management
- **financial-dashboard** - Market analysis and reporting
- **content-generator** - Multi-format content creation

### Custom Development

- Combine multiple integrations
- Build custom functions
- Create specialized workflows for your use case

---

**Ready to build amazing AI-powered applications? Let's start with the basics! 🚀**
