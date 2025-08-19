# Authentication Guide

Learn how to connect your AI agents to real applications using various authentication methods.

## Overview

Incredible API supports multiple authentication schemes to connect with different services:

- **OAuth 2.0** - For services like Gmail, Google Sheets, LinkedIn
- **API Key** - For services like Perplexity, OpenAI
- **OAuth 1.0** - For services like Twitter (X)
- **Basic Auth** - For simple username/password authentication
- **Bearer Token** - For token-based authentication

## Authentication Flow

### 1. Check Available Integrations

First, let's see what integrations are available:

```python
import requests

def list_integrations():
    response = requests.get("https://api.incredible.one/v1/integrations")
    integrations = response.json()

    print("Available Integrations:")
    for integration in integrations:
        print(f"- {integration['name']} ({integration['id']})")
        print(f"  Auth Method: {integration['auth_method']}")
        print(f"  Features: {[f['name'] for f in integration['features']]}")
        print()

list_integrations()
```

### 2. Connect Integrations

#### OAuth 2.0 Example (Gmail)

OAuth requires a redirect flow for user authorization:

```python
import requests
import json

def connect_gmail(user_id, callback_url=None):
    url = "https://api.incredible.one/v1/integrations/gmail/connect"

    data = {
        "user_id": user_id,
        "callback_url": callback_url or "https://your-app.com/oauth/callback"
    }

    response = requests.post(url, json=data)
    result = response.json()

    if "redirect_url" in result:
        print("📧 Gmail Connection:")
        print(f"1. Visit this URL: {result['redirect_url']}")
        print(f"2. Authorize access to your Gmail")
        print(f"3. You'll be redirected back to your callback URL")
        return result['redirect_url']
    else:
        print(f"Error: {result}")

# Usage
redirect_url = connect_gmail("your_user_id")
```

#### API Key Example (Perplexity)

API key authentication is straightforward:

```python
def connect_perplexity(user_id, api_key):
    url = "https://api.incredible.one/v1/integrations/perplexity/connect"

    data = {
        "user_id": user_id,
        "api_key": api_key
    }

    response = requests.post(url, json=data)
    result = response.json()

    if result.get("success"):
        print("✅ Perplexity connected successfully!")
        return True
    else:
        print(f"❌ Connection failed: {result}")
        return False

# Usage
connect_perplexity("your_user_id", "pplx-your-api-key")
```

## Complete Authentication Examples

### Multi-Service Setup

Here's a complete example that connects multiple services:

```python
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

class IntegrationManager:
    def __init__(self):
        self.base_url = "https://api.incredible.one"
        self.user_id = "your_user_id"  # Replace with actual user ID

    def connect_api_key_service(self, service_id, api_key):
        """Connect services that use API key authentication"""
        url = f"{self.base_url}/v1/integrations/{service_id}/connect"

        data = {
            "user_id": self.user_id,
            "api_key": api_key
        }

        response = requests.post(url, json=data)
        result = response.json()

        if result.get("success"):
            print(f"✅ {service_id.title()} connected successfully!")
            return True
        else:
            print(f"❌ {service_id.title()} connection failed: {result}")
            return False

    def initiate_oauth(self, service_id, callback_url=None):
        """Initiate OAuth flow for services that require it"""
        url = f"{self.base_url}/v1/integrations/{service_id}/connect"

        data = {
            "user_id": self.user_id,
            "callback_url": callback_url or f"https://your-app.com/oauth/{service_id}"
        }

        response = requests.post(url, json=data)
        result = response.json()

        if "redirect_url" in result:
            print(f"🔗 {service_id.title()} OAuth Setup:")
            print(f"Visit: {result['redirect_url']}")
            print(f"Instructions: {result.get('instructions', 'Complete authorization')}")
            return result['redirect_url']
        else:
            print(f"❌ {service_id.title()} OAuth failed: {result}")
            return None

    def setup_complete_workspace(self):
        """Set up a complete workspace with multiple integrations"""
        print("🚀 Setting up your Incredible workspace...\n")

        # Connect API key services
        api_services = {
            "perplexity": os.getenv("PERPLEXITY_API_KEY"),
            # "openai": os.getenv("OPENAI_API_KEY"),  # If available
        }

        for service, api_key in api_services.items():
            if api_key:
                self.connect_api_key_service(service, api_key)
            else:
                print(f"⚠️  {service.title()} API key not found in environment")

        print()

        # Initiate OAuth for services that require it
        oauth_services = ["gmail", "google_sheets", "slack"]

        print("📋 OAuth Services Setup:")
        print("Complete these OAuth flows to finish setup:\n")

        for service in oauth_services:
            redirect_url = self.initiate_oauth(service)
            if redirect_url:
                print(f"• {service.title()}: {redirect_url}")
                print()

        print("💡 After completing OAuth flows, your workspace will be ready!")

# Usage
if __name__ == "__main__":
    manager = IntegrationManager()
    manager.setup_complete_workspace()
```

### Environment Variables Setup

Create a comprehensive `.env` file:

```bash
# .env

# Incredible API
INCREDIBLE_API_KEY=your_incredible_api_key
INCREDIBLE_BASE_URL=https://api.incredible.one
USER_ID=your_user_id

# API Key Services
PERPLEXITY_API_KEY=pplx-your-api-key
OPENAI_API_KEY=sk-your-openai-key

# OAuth Callback URLs (for production)
GMAIL_CALLBACK_URL=https://your-app.com/oauth/gmail
SLACK_CALLBACK_URL=https://your-app.com/oauth/slack
SHEETS_CALLBACK_URL=https://your-app.com/oauth/sheets

# Development
DEBUG=true
```

## Testing Your Connections

### Connection Verification

```python
def test_integration(service_id, user_id):
    """Test if an integration is properly connected"""
    url = f"https://api.incredible.one/v1/integrations/{service_id}"

    response = requests.get(url)
    if response.status_code == 200:
        integration = response.json()
        print(f"✅ {integration['name']} integration available")

        # Test execution (example)
        test_url = f"https://api.incredible.one/v1/integrations/{service_id}/execute"
        test_data = {
            "user_id": user_id,
            "feature_name": integration['features'][0]['name'],
            "inputs": {}  # Add appropriate test inputs
        }

        # This would test the actual execution
        # test_response = requests.post(test_url, json=test_data)
        # return test_response.status_code == 200

        return True
    else:
        print(f"❌ {service_id} integration not available")
        return False

# Test all your connections
services_to_test = ["gmail", "perplexity", "slack"]
for service in services_to_test:
    test_integration(service, "your_user_id")
```

## JavaScript/Node.js Examples

### OAuth Setup (JavaScript)

```javascript
const axios = require("axios");
require("dotenv").config();

class IntegrationManager {
  constructor() {
    this.baseUrl =
      process.env.INCREDIBLE_BASE_URL || "https://api.incredible.one";
    this.userId = process.env.USER_ID;
  }

  async connectApiKeyService(serviceId, apiKey) {
    const url = `${this.baseUrl}/v1/integrations/${serviceId}/connect`;

    try {
      const response = await axios.post(url, {
        user_id: this.userId,
        api_key: apiKey,
      });

      if (response.data.success) {
        console.log(`✅ ${serviceId} connected successfully!`);
        return true;
      }
    } catch (error) {
      console.log(`❌ ${serviceId} connection failed:`, error.response?.data);
      return false;
    }
  }

  async initiateOAuth(serviceId, callbackUrl = null) {
    const url = `${this.baseUrl}/v1/integrations/${serviceId}/connect`;

    try {
      const response = await axios.post(url, {
        user_id: this.userId,
        callback_url: callbackUrl || `https://your-app.com/oauth/${serviceId}`,
      });

      if (response.data.redirect_url) {
        console.log(`🔗 ${serviceId} OAuth Setup:`);
        console.log(`Visit: ${response.data.redirect_url}`);
        return response.data.redirect_url;
      }
    } catch (error) {
      console.log(`❌ ${serviceId} OAuth failed:`, error.response?.data);
      return null;
    }
  }

  async setupWorkspace() {
    console.log("🚀 Setting up your Incredible workspace...\n");

    // Connect API key services
    if (process.env.PERPLEXITY_API_KEY) {
      await this.connectApiKeyService(
        "perplexity",
        process.env.PERPLEXITY_API_KEY
      );
    }

    // Initiate OAuth flows
    const oauthServices = ["gmail", "google_sheets", "slack"];

    console.log("\n📋 OAuth Services Setup:");
    for (const service of oauthServices) {
      const redirectUrl = await this.initiateOAuth(service);
      if (redirectUrl) {
        console.log(`• ${service}: ${redirectUrl}\n`);
      }
    }
  }
}

// Usage
const manager = new IntegrationManager();
manager.setupWorkspace();
```

## Best Practices

### 1. Secure Credential Storage

- Never commit API keys to version control
- Use environment variables or secure vaults
- Implement proper key rotation policies

### 2. Error Handling

```python
def safe_connect(service_id, credentials, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = connect_service(service_id, credentials)
            if result:
                return result
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff

    return None
```

### 3. OAuth Callback Handling

```python
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/oauth/<service>')
def oauth_callback(service):
    status = request.args.get('status')
    user_id = request.args.get('user_id')

    if status == 'success':
        print(f"✅ {service} connected for user {user_id}")
        return redirect('/dashboard?connected=' + service)
    else:
        print(f"❌ {service} connection failed")
        return redirect('/dashboard?error=' + service)
```

## Troubleshooting

### Common Issues

1. **OAuth Redirect Mismatch**

   - Ensure callback URLs match exactly
   - Check for trailing slashes
   - Verify HTTPS in production

2. **API Key Invalid**

   - Double-check the key format
   - Ensure proper permissions
   - Verify expiration dates

3. **Rate Limiting**
   - Implement exponential backoff
   - Respect API rate limits
   - Use proper error handling

### Debug Mode

```python
import logging

logging.basicConfig(level=logging.DEBUG)

def debug_connection(service_id):
    try:
        response = requests.get(f"https://api.incredible.one/v1/integrations/{service_id}")
        print(f"Service Details: {response.json()}")
    except Exception as e:
        print(f"Debug Error: {e}")
```

## Next Steps

Now that you have your integrations connected, you're ready to:

1. **[Build Your First Agent](./first-agent.md)** - Create a simple automation
2. **[Multi-Integration Examples](../basic-examples/multi-integration/)** - Combine multiple services
3. **[Real-World Use Cases](../use-cases/)** - Explore practical applications

Need help with a specific integration? Check our [integration-specific guides](../integrations/) for detailed examples!
