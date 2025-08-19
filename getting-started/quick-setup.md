# Quick Setup Guide

Get your first Incredible AI agent running in under 5 minutes!

## Prerequisites

- Incredible API account ([Sign up here](https://incredible.one))
- Python 3.8+ or Node.js 16+
- Basic familiarity with REST APIs

## Step 1: Get Your API Credentials

1. Sign up at [incredible.one](https://incredible.one)
2. Navigate to your dashboard
3. Go to Settings → API Keys
4. Generate a new API key
5. Copy and save it securely

## Step 2: Install Dependencies

### Python Setup

Create a new directory and set up your environment:

```bash
mkdir my-incredible-agent
cd my-incredible-agent

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install requests python-dotenv
```

### JavaScript Setup

```bash
mkdir my-incredible-agent
cd my-incredible-agent

# Initialize npm project
npm init -y

# Install required packages
npm install axios dotenv
```

## Step 3: Set Up Environment Variables

Create a `.env` file in your project directory:

```bash
# .env
INCREDIBLE_API_KEY=your_api_key_here
INCREDIBLE_BASE_URL=https://api.incredible.one
```

## Step 4: Your First Agent

Let's create a simple agent that searches the web using Perplexity AI.

### Python Example

Create `main.py`:

```python
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class IncredibleClient:
    def __init__(self):
        self.api_key = os.getenv('INCREDIBLE_API_KEY')
        self.base_url = os.getenv('INCREDIBLE_BASE_URL')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def create_search_agent(self, query):
        """Create an agent that searches the web using Perplexity"""

        # Define the search function
        search_function = {
            "name": "perplexity_search",
            "description": "Search the web using Perplexity AI",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }

        # Create the chat completion request
        data = {
            "model": "small-1",
            "messages": [
                {"role": "user", "content": f"Search for: {query}"}
            ],
            "stream": False,
            "functions": [search_function],
            "system": "You are a helpful research assistant. Use the perplexity_search function to find accurate, up-to-date information."
        }

        # Send request to Incredible API
        response = requests.post(
            f"{self.base_url}/v1/chat-completion",
            headers=self.headers,
            json=data
        )

        if response.status_code == 200:
            result = response.json()
            return self.handle_response(result)
        else:
            return f"Error: {response.status_code} - {response.text}"

    def handle_response(self, result):
        """Handle the API response and execute function calls"""
        print("🤖 AI Response:")

        for item in result["result"]["response"]:
            if item.get("role") == "assistant":
                print(f"Assistant: {item['content']}")
            elif item.get("type") == "function_call":
                print(f"🔍 Calling function: {item['function_calls'][0]['name']}")
                print(f"📋 Query: {item['function_calls'][0]['input']['query']}")

                # In a real implementation, you would call the Perplexity API here
                # For this example, we'll simulate the response
                mock_result = f"Search results for '{item['function_calls'][0]['input']['query']}' would appear here."

                print(f"✅ Search completed: {mock_result}")
                return mock_result

        return "Response completed"

# Usage example
if __name__ == "__main__":
    client = IncredibleClient()

    # Test the search agent
    query = "latest developments in artificial intelligence 2024"
    result = client.create_search_agent(query)
    print(f"\n🎉 Final result: {result}")
```

### JavaScript Example

Create `main.js`:

```javascript
const axios = require("axios");
require("dotenv").config();

class IncredibleClient {
  constructor() {
    this.apiKey = process.env.INCREDIBLE_API_KEY;
    this.baseUrl = process.env.INCREDIBLE_BASE_URL;
    this.headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${this.apiKey}`,
    };
  }

  async createSearchAgent(query) {
    // Define the search function
    const searchFunction = {
      name: "perplexity_search",
      description: "Search the web using Perplexity AI",
      parameters: {
        type: "object",
        properties: {
          query: {
            type: "string",
            description: "The search query",
          },
        },
        required: ["query"],
      },
    };

    // Create the chat completion request
    const data = {
      model: "small-1",
      messages: [{ role: "user", content: `Search for: ${query}` }],
      stream: false,
      functions: [searchFunction],
      system:
        "You are a helpful research assistant. Use the perplexity_search function to find accurate, up-to-date information.",
    };

    try {
      // Send request to Incredible API
      const response = await axios.post(
        `${this.baseUrl}/v1/chat-completion`,
        data,
        { headers: this.headers }
      );

      return this.handleResponse(response.data);
    } catch (error) {
      return `Error: ${error.response?.status} - ${
        error.response?.data || error.message
      }`;
    }
  }

  handleResponse(result) {
    console.log("🤖 AI Response:");

    for (const item of result.result.response) {
      if (item.role === "assistant") {
        console.log(`Assistant: ${item.content}`);
      } else if (item.type === "function_call") {
        console.log(`🔍 Calling function: ${item.function_calls[0].name}`);
        console.log(`📋 Query: ${item.function_calls[0].input.query}`);

        // In a real implementation, you would call the Perplexity API here
        // For this example, we'll simulate the response
        const mockResult = `Search results for '${item.function_calls[0].input.query}' would appear here.`;

        console.log(`✅ Search completed: ${mockResult}`);
        return mockResult;
      }
    }

    return "Response completed";
  }
}

// Usage example
async function main() {
  const client = new IncredibleClient();

  // Test the search agent
  const query = "latest developments in artificial intelligence 2024";
  const result = await client.createSearchAgent(query);
  console.log(`\n🎉 Final result: ${result}`);
}

main().catch(console.error);
```

## Step 5: Run Your Agent

### Python

```bash
python main.py
```

### JavaScript

```bash
node main.js
```

## Expected Output

You should see something like:

```
🤖 AI Response:
Assistant: I'll search for the latest developments in artificial intelligence for 2024.
🔍 Calling function: perplexity_search
📋 Query: latest developments in artificial intelligence 2024
✅ Search completed: Search results for 'latest developments in artificial intelligence 2024' would appear here.

🎉 Final result: Search results for 'latest developments in artificial intelligence 2024' would appear here.
```

## Next Steps

🎉 Congratulations! You've created your first Incredible AI agent. Here's what to explore next:

1. **[Authentication Guide](./authentication.md)** - Connect real integrations like Gmail, Slack, etc.
2. **[Multi-Integration Examples](../basic-examples/multi-integration/)** - Combine multiple apps
3. **[Real-World Use Cases](../use-cases/)** - Practical automation scenarios

## Common Issues

### API Key Not Working

- Double-check your API key in the dashboard
- Ensure `.env` file is in the correct directory
- Verify the environment variables are loaded correctly

### Connection Errors

- Check your internet connection
- Verify the base URL is correct
- Ensure you're using the latest API version

### Import Errors

- Make sure all dependencies are installed
- Check your Python/Node.js version compatibility

## Need Help?

- 📚 [Full Documentation](https://docs.incredible.one)
- 💬 [Community Forum](https://community.incredible.one)
- 📧 [Support](mailto:support@incredible.one)

Ready to build something more complex? Check out our [multi-integration examples](../basic-examples/multi-integration/) next!
