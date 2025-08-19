# Function Calling Examples

Learn how to leverage Incredible's powerful function calling capabilities to create intelligent agents that can execute custom functions and interact with external systems.

## 🎯 **What is Function Calling?**

Function calling allows your AI agents to:
- **🔧 Execute Custom Logic**: Run your own functions based on user requests
- **🌐 Connect External APIs**: Integrate with any REST API or service
- **📊 Process Data**: Perform calculations, transformations, and analysis
- **🤝 Multi-Step Workflows**: Chain multiple function calls together

## 📚 **Examples in This Section**

### 🛠️ **Basic Function Calling**
- **Simple Calculator**: Mathematical operations with AI decision-making
- **Weather API**: Real-time weather data integration
- **Database Queries**: Dynamic SQL query generation and execution

### 🔗 **Multi-Function Workflows**
- **E-commerce Helper**: Product lookup, price checking, and order processing
- **Travel Planner**: Flight search, hotel booking, and itinerary creation
- **Data Pipeline**: ETL operations with validation and error handling

### 🎨 **Advanced Patterns**
- **Conditional Logic**: Functions that decide which other functions to call
- **Error Recovery**: Robust error handling with automatic retries
- **State Management**: Maintaining context across multiple function calls

## 🚀 **Quick Start**

<div class="code-tabs" data-section="function-calling-quick-start">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python">import requests

def calculate_area(shape, **dimensions):
    """Calculate area of different shapes"""
    if shape == "rectangle":
        return dimensions["width"] * dimensions["height"]
    elif shape == "circle":
        import math
        return math.pi * (dimensions["radius"] ** 2)
    else:
        return "Unsupported shape"

# Define function for AI
calculate_function = {
    "name": "calculate_area",
    "description": "Calculate area of geometric shapes",
    "parameters": {
        "type": "object",
        "properties": {
            "shape": {"type": "string", "enum": ["rectangle", "circle"]},
            "width": {"type": "number"},
            "height": {"type": "number"},
            "radius": {"type": "number"}
        },
        "required": ["shape"]
    }
}

# Chat completion with function calling
response = requests.post("https://api.incredible.one/v1/chat-completion", 
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "model": "incredible-agent",
        "user_id": "your_user_id",
        "messages": [{"role": "user", "content": "Calculate area of a 5x3 rectangle"}],
        "functions": [calculate_function],
        "stream": False
    }
)</code></pre>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">const axios = require('axios');

function calculateArea(shape, dimensions) {
    if (shape === "rectangle") {
        return dimensions.width * dimensions.height;
    } else if (shape === "circle") {
        return Math.PI * (dimensions.radius ** 2);
    } else {
        return "Unsupported shape";
    }
}

// Define function for AI
const calculateFunction = {
    name: "calculate_area",
    description: "Calculate area of geometric shapes",
    parameters: {
        type: "object",
        properties: {
            shape: { type: "string", enum: ["rectangle", "circle"] },
            width: { type: "number" },
            height: { type: "number" },
            radius: { type: "number" }
        },
        required: ["shape"]
    }
};

// Chat completion with function calling
const response = await axios.post("https://api.incredible.one/v1/chat-completion", {
    model: "incredible-agent",
    user_id: "your_user_id",
    messages: [{ role: "user", content: "Calculate area of a 5x3 rectangle" }],
    functions: [calculateFunction],
    stream: false
}, {
    headers: { "Authorization": "Bearer YOUR_API_KEY" }
});</code></pre>
  </div>
</div>

## 📖 **Function Definition Schema**

All functions must follow the JSON Schema format:

```json
{
    "name": "function_name",
    "description": "Clear description of what the function does",
    "parameters": {
        "type": "object",
        "properties": {
            "param1": {
                "type": "string|number|boolean|array|object",
                "description": "Parameter description",
                "enum": ["optional", "allowed", "values"]
            }
        },
        "required": ["param1", "param2"]
    }
}
```

## 🎯 **Best Practices**

### 📝 **Function Design**
- **Clear Names**: Use descriptive, action-oriented function names
- **Focused Purpose**: Each function should do one thing well
- **Input Validation**: Always validate parameters before execution
- **Error Handling**: Return meaningful error messages

### 🔧 **Implementation Tips**
- **Idempotent Operations**: Functions should be safe to call multiple times
- **Timeout Handling**: Set appropriate timeouts for external API calls
- **Logging**: Log function calls for debugging and monitoring
- **Security**: Validate all inputs to prevent injection attacks

### 🚀 **Performance**
- **Caching**: Cache expensive operations when possible
- **Async Operations**: Use async/await for I/O bound operations
- **Rate Limiting**: Respect API rate limits in external integrations
- **Resource Management**: Clean up resources properly

## 🔗 **Related Topics**

- [📧 Gmail Integration](../../integrations/gmail/README.md) - Email automation functions
- [📊 Google Sheets](../../integrations/google-sheets/README.md) - Spreadsheet operations
- [🚨 Error Handling](../../advanced/error-handling/README.md) - Robust error management
- [⚡ Performance](../../advanced/performance/README.md) - Optimization techniques

---

*Master function calling to create powerful, intelligent agents that can interact with any system or API.*
