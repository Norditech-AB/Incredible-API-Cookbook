# Python SDK Examples

Comprehensive Python utilities and examples for building robust applications with the Incredible API.

## Overview

This directory contains Python SDK examples, utilities, and best practices for working with the Incredible API. All examples are production-ready and include proper error handling, logging, and testing patterns.

## Structure

```
python/
├── incredible_sdk/          # Core SDK utilities
│   ├── __init__.py
│   ├── client.py           # Main API client
│   ├── integrations.py     # Integration helpers
│   ├── functions.py        # Function calling utilities
│   ├── exceptions.py       # Custom exceptions
│   └── utils.py           # Common utilities
├── examples/               # Complete example applications
│   ├── email_automation/   # Gmail automation examples
│   ├── data_processing/    # Data analysis and processing
│   ├── business_workflows/ # Complete business solutions
│   └── ai_agents/         # Advanced AI agent patterns
├── templates/             # Reusable templates
├── tests/                # Unit and integration tests
└── requirements.txt      # Dependencies
```

## Quick Start

### Installation

```bash
# Clone the cookbook and navigate to Python SDK
cd incredible-api-cookbook/sdk-examples/python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your credentials
```

### Basic Usage

```python
from incredible_sdk import IncredibleClient

# Initialize client
client = IncredibleClient(api_key="your_api_key")

# Create a simple agent
agent = client.create_agent(
    name="Email Summarizer",
    integrations=["gmail", "slack"],
    prompt="Summarize important emails and post to Slack"
)

# Execute the agent
result = agent.execute()
print(result)
```

## Core SDK Components

### 1. IncredibleClient

The main client for interacting with the Incredible API.

```python
from incredible_sdk import IncredibleClient, AgentConfig

client = IncredibleClient(
    api_key="your_api_key",
    base_url="https://api.incredible.one",
    timeout=30,
    retry_attempts=3
)

# Chat completion with function calling
response = client.chat_completion(
    messages=[{"role": "user", "content": "Analyze my emails"}],
    functions=[client.get_gmail_functions()],
    stream=False
)

# Integration management
integrations = client.list_integrations()
client.connect_integration("gmail", user_id="user123")
result = client.execute_integration("gmail", "SEARCH_EMAILS", {"query": "urgent"})
```

### 2. Integration Helpers

Simplified interfaces for common integrations.

```python
from incredible_sdk.integrations import GmailHelper, SheetsHelper, SlackHelper

# Gmail operations
gmail = GmailHelper(client, user_id="user123")
emails = gmail.search("is:unread", max_results=10)
gmail.send_email(to="user@example.com", subject="Hello", body="World")

# Google Sheets operations
sheets = SheetsHelper(client, user_id="user123")
sheets.add_row("sheet_id", ["Name", "Email", "Status"])
data = sheets.read_range("sheet_id", "A1:C10")

# Slack operations
slack = SlackHelper(client, user_id="user123")
slack.send_message("#general", "Hello team!")
slack.send_direct_message("user123", "Private message")
```

### 3. Function Calling Framework

Powerful utilities for building custom functions.

```python
from incredible_sdk.functions import FunctionRegistry, function

# Create function registry
registry = FunctionRegistry()

@registry.function(
    name="analyze_sentiment",
    description="Analyze sentiment of text",
    parameters={
        "text": {"type": "string", "description": "Text to analyze"}
    }
)
def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment of given text"""
    # Your sentiment analysis logic
    return {"sentiment": "positive", "confidence": 0.95}

@registry.function(
    name="fetch_stock_price",
    description="Get current stock price",
    parameters={
        "symbol": {"type": "string", "description": "Stock symbol"}
    }
)
def fetch_stock_price(symbol: str) -> dict:
    """Fetch current stock price"""
    # Your stock price fetching logic
    return {"symbol": symbol, "price": 150.00, "change": "+2.5%"}

# Use functions in chat completion
response = client.chat_completion(
    messages=[{"role": "user", "content": "What's the sentiment of 'Great job!' and AAPL stock price?"}],
    functions=registry.get_function_definitions(),
    function_executor=registry
)
```

### 4. Agent Framework

High-level abstraction for building AI agents.

```python
from incredible_sdk import Agent, AgentConfig

class EmailAnalysisAgent(Agent):
    def __init__(self, client, config):
        super().__init__(client, config)
        self.gmail = GmailHelper(client, config.user_id)
        self.sheets = SheetsHelper(client, config.user_id)

    def execute(self):
        # Get recent emails
        emails = self.gmail.search("newer_than:1d", max_results=20)

        # Analyze each email
        analysis_results = []
        for email in emails:
            analysis = self.analyze_email(email)
            analysis_results.append(analysis)

            # Log to sheets
            self.sheets.add_row(self.config.tracking_sheet_id, [
                email['subject'],
                email['sender'],
                analysis['priority'],
                analysis['sentiment'],
                analysis['category']
            ])

        return {
            "processed_emails": len(emails),
            "analysis_results": analysis_results,
            "summary": self.generate_summary(analysis_results)
        }

    def analyze_email(self, email):
        """Analyze individual email"""
        response = self.client.chat_completion(
            messages=[{
                "role": "user",
                "content": f"Analyze this email:\nSubject: {email['subject']}\nContent: {email['content']}"
            }],
            functions=[
                {
                    "name": "extract_email_metadata",
                    "description": "Extract metadata from email",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                            "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative"]},
                            "category": {"type": "string"},
                            "action_required": {"type": "boolean"}
                        }
                    }
                }
            ]
        )

        return self.extract_function_result(response)

# Usage
config = AgentConfig(
    user_id="user123",
    tracking_sheet_id="sheet123",
    notification_channel="#email-alerts"
)

agent = EmailAnalysisAgent(client, config)
result = agent.execute()
```

## Example Applications

### 1. Email Automation Suite

Complete email management and automation system.

```python
# examples/email_automation/email_suite.py
from incredible_sdk import IncredibleClient
from incredible_sdk.integrations import GmailHelper, SheetsHelper, SlackHelper
from incredible_sdk.utils import setup_logging

logger = setup_logging(__name__)

class EmailAutomationSuite:
    def __init__(self, client, user_id):
        self.client = client
        self.user_id = user_id
        self.gmail = GmailHelper(client, user_id)
        self.sheets = SheetsHelper(client, user_id)
        self.slack = SlackHelper(client, user_id)

    def auto_categorize_emails(self, days_back=7):
        """Automatically categorize and organize emails"""
        logger.info(f"Starting email categorization for last {days_back} days")

        # Get recent emails
        emails = self.gmail.search(f"newer_than:{days_back}d", max_results=100)
        logger.info(f"Found {len(emails)} emails to process")

        categories = {
            "urgent": [],
            "meetings": [],
            "newsletters": [],
            "support": [],
            "personal": []
        }

        for email in emails:
            category = self.categorize_email(email)
            categories[category].append(email)

            # Log to tracking sheet
            self.sheets.add_row("email_tracking", [
                email['subject'],
                email['sender'],
                category,
                email['date'],
                'auto-categorized'
            ])

        # Generate summary report
        summary = self.generate_category_report(categories)

        # Send summary to Slack
        self.slack.send_message("#email-reports", summary)

        return categories

    def categorize_email(self, email):
        """Use AI to categorize individual email"""
        prompt = f"""
        Categorize this email into one of these categories:
        - urgent: Important emails requiring immediate attention
        - meetings: Meeting invitations, calendar events
        - newsletters: Marketing emails, newsletters, announcements
        - support: Customer support, help requests
        - personal: Personal correspondence

        Email Subject: {email['subject']}
        Email Sender: {email['sender']}
        Email Preview: {email.get('snippet', '')[:200]}

        Return only the category name.
        """

        response = self.client.chat_completion(
            messages=[{"role": "user", "content": prompt}]
        )

        category = response['result']['response'][0]['content'].strip().lower()

        # Validate category
        valid_categories = ["urgent", "meetings", "newsletters", "support", "personal"]
        return category if category in valid_categories else "personal"

    def setup_auto_responses(self):
        """Setup intelligent auto-responses"""
        # Check for emails that need auto-responses
        unread_emails = self.gmail.search("is:unread", max_results=20)

        for email in unread_emails:
            if self.should_auto_respond(email):
                response_type = self.determine_response_type(email)
                response_content = self.generate_response(email, response_type)

                self.gmail.send_email(
                    to=email['sender'],
                    subject=f"Re: {email['subject']}",
                    body=response_content,
                    reply_to_message_id=email['id']
                )

                # Mark as handled
                self.gmail.mark_as_read(email['id'])
                logger.info(f"Auto-responded to email from {email['sender']}")

    def generate_daily_digest(self):
        """Generate and send daily email digest"""
        today_emails = self.gmail.search("newer_than:1d")

        digest = self.create_email_digest(today_emails)

        # Send via Slack and Email
        self.slack.send_message("#daily-digest", digest)
        self.gmail.send_email(
            to=os.getenv("DIGEST_RECIPIENT"),
            subject=f"Daily Email Digest - {datetime.now().strftime('%Y-%m-%d')}",
            body=digest
        )

        return digest

# Usage
if __name__ == "__main__":
    client = IncredibleClient(api_key=os.getenv("INCREDIBLE_API_KEY"))
    suite = EmailAutomationSuite(client, user_id="user123")

    # Run daily automation
    suite.auto_categorize_emails()
    suite.setup_auto_responses()
    suite.generate_daily_digest()
```

### 2. Business Intelligence Agent

Advanced data processing and analysis agent.

```python
# examples/business_workflows/bi_agent.py
from incredible_sdk import Agent, AgentConfig
from incredible_sdk.integrations import SheetsHelper, SlackHelper
from incredible_sdk.functions import FunctionRegistry
import pandas as pd
import numpy as np

class BusinessIntelligenceAgent(Agent):
    def __init__(self, client, config):
        super().__init__(client, config)
        self.sheets = SheetsHelper(client, config.user_id)
        self.slack = SlackHelper(client, config.user_id)
        self.function_registry = FunctionRegistry()
        self.setup_functions()

    def setup_functions(self):
        """Setup data analysis functions"""

        @self.function_registry.function(
            name="analyze_sales_data",
            description="Analyze sales performance data",
            parameters={
                "data": {"type": "array", "description": "Sales data array"},
                "period": {"type": "string", "description": "Analysis period"}
            }
        )
        def analyze_sales_data(data: list, period: str) -> dict:
            df = pd.DataFrame(data)

            analysis = {
                "total_revenue": df['revenue'].sum(),
                "avg_deal_size": df['revenue'].mean(),
                "conversion_rate": len(df[df['status'] == 'closed']) / len(df),
                "growth_rate": self.calculate_growth_rate(df, period),
                "top_performers": df.nlargest(5, 'revenue').to_dict('records'),
                "trends": self.identify_trends(df)
            }

            return analysis

        @self.function_registry.function(
            name="generate_insights",
            description="Generate business insights from data",
            parameters={
                "metrics": {"type": "object", "description": "Business metrics"},
                "context": {"type": "string", "description": "Business context"}
            }
        )
        def generate_insights(metrics: dict, context: str) -> dict:
            # Use AI to generate insights
            insights_prompt = f"""
            Analyze these business metrics and provide insights:

            Metrics: {metrics}
            Context: {context}

            Provide:
            1. Key insights (3-5 points)
            2. Recommendations (3-5 actions)
            3. Risk factors to monitor
            4. Opportunities to explore
            """

            response = self.client.chat_completion(
                messages=[{"role": "user", "content": insights_prompt}]
            )

            return {"insights": response['result']['response'][0]['content']}

    def execute(self):
        """Execute BI analysis workflow"""
        logger.info("Starting Business Intelligence analysis")

        # Collect data from multiple sources
        sales_data = self.collect_sales_data()
        marketing_data = self.collect_marketing_data()
        support_data = self.collect_support_data()

        # Perform analysis
        sales_analysis = self.analyze_sales_data(sales_data, "monthly")
        marketing_analysis = self.analyze_marketing_data(marketing_data)
        support_analysis = self.analyze_support_data(support_data)

        # Generate combined insights
        combined_metrics = {
            "sales": sales_analysis,
            "marketing": marketing_analysis,
            "support": support_analysis
        }

        business_insights = self.generate_insights(
            combined_metrics,
            "Monthly business performance review"
        )

        # Create comprehensive report
        report = self.create_bi_report(combined_metrics, business_insights)

        # Distribute report
        self.distribute_report(report)

        return {
            "status": "completed",
            "metrics": combined_metrics,
            "insights": business_insights,
            "report_url": report['url']
        }

    def collect_sales_data(self):
        """Collect sales data from CRM sheets"""
        sales_sheet_data = self.sheets.read_range(
            self.config.sales_sheet_id,
            "A1:Z1000"
        )

        # Convert to structured format
        headers = sales_sheet_data[0]
        data = []

        for row in sales_sheet_data[1:]:
            if len(row) >= len(headers):
                record = dict(zip(headers, row))
                data.append(record)

        return data

    def create_bi_report(self, metrics, insights):
        """Create comprehensive BI report"""
        # Create report in Google Sheets
        report_data = self.format_report_data(metrics, insights)

        # Create new sheet for this report
        report_sheet_id = self.sheets.create_sheet(
            f"BI_Report_{datetime.now().strftime('%Y%m%d')}"
        )

        # Add report data
        self.sheets.update_range(
            report_sheet_id,
            "A1:Z100",
            report_data
        )

        # Format the sheet
        self.sheets.format_report_sheet(report_sheet_id)

        return {
            "sheet_id": report_sheet_id,
            "url": f"https://docs.google.com/spreadsheets/d/{report_sheet_id}",
            "created_at": datetime.now().isoformat()
        }

    def distribute_report(self, report):
        """Distribute the BI report to stakeholders"""
        summary_message = f"""
        📊 **Monthly Business Intelligence Report**

        📈 **Key Highlights:**
        • Revenue: ${report['metrics']['sales']['total_revenue']:,.2f}
        • Growth: {report['metrics']['sales']['growth_rate']:.1%}
        • Conversion: {report['metrics']['sales']['conversion_rate']:.1%}

        🔗 **Full Report:** {report['url']}

        📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """

        # Send to Slack
        self.slack.send_message("#executive-reports", summary_message)

        # Email to stakeholders
        stakeholders = self.config.report_recipients
        for stakeholder in stakeholders:
            self.send_report_email(stakeholder, report, summary_message)

# Usage
config = AgentConfig(
    user_id="user123",
    sales_sheet_id="sales_data_sheet_id",
    marketing_sheet_id="marketing_data_sheet_id",
    support_sheet_id="support_data_sheet_id",
    report_recipients=["ceo@company.com", "cfo@company.com"]
)

bi_agent = BusinessIntelligenceAgent(client, config)
result = bi_agent.execute()
```

## Testing Framework

### Unit Tests

```python
# tests/test_client.py
import unittest
from unittest.mock import Mock, patch
from incredible_sdk import IncredibleClient

class TestIncredibleClient(unittest.TestCase):
    def setUp(self):
        self.client = IncredibleClient(api_key="test_key")

    @patch('incredible_sdk.client.requests.post')
    def test_chat_completion(self, mock_post):
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "response": [{"role": "assistant", "content": "Hello!"}]
            }
        }
        mock_post.return_value = mock_response

        # Test
        response = self.client.chat_completion(
            messages=[{"role": "user", "content": "Hi"}]
        )

        self.assertEqual(response['result']['response'][0]['content'], "Hello!")
        mock_post.assert_called_once()

    def test_function_registry(self):
        from incredible_sdk.functions import FunctionRegistry

        registry = FunctionRegistry()

        @registry.function(
            name="test_function",
            description="Test function",
            parameters={"input": {"type": "string"}}
        )
        def test_func(input: str) -> str:
            return f"Processed: {input}"

        functions = registry.get_function_definitions()
        self.assertEqual(len(functions), 1)
        self.assertEqual(functions[0]['name'], "test_function")

        result = registry.execute_function("test_function", {"input": "hello"})
        self.assertEqual(result, "Processed: hello")

if __name__ == "__main__":
    unittest.main()
```

### Integration Tests

```python
# tests/test_integrations.py
import unittest
import os
from incredible_sdk import IncredibleClient
from incredible_sdk.integrations import GmailHelper

class TestGmailIntegration(unittest.TestCase):
    def setUp(self):
        self.client = IncredibleClient(api_key=os.getenv("TEST_API_KEY"))
        self.gmail = GmailHelper(self.client, user_id=os.getenv("TEST_USER_ID"))

    @unittest.skipIf(not os.getenv("RUN_INTEGRATION_TESTS"), "Integration tests disabled")
    def test_search_emails(self):
        emails = self.gmail.search("test", max_results=5)
        self.assertIsInstance(emails, list)
        self.assertLessEqual(len(emails), 5)

    @unittest.skipIf(not os.getenv("RUN_INTEGRATION_TESTS"), "Integration tests disabled")
    def test_send_email(self):
        result = self.gmail.send_email(
            to="test@example.com",
            subject="Test Email",
            body="This is a test email from the SDK"
        )
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
```

## Deployment

### Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Set environment variables
ENV PYTHONPATH=/app

# Run application
CMD ["python", "main.py"]
```

### Production Setup

```python
# production/app.py
from incredible_sdk import IncredibleClient
from incredible_sdk.utils import setup_logging, load_config
import schedule
import time

# Setup
logger = setup_logging(__name__, level="INFO")
config = load_config("production.yaml")
client = IncredibleClient(
    api_key=config.api_key,
    timeout=config.timeout,
    retry_attempts=config.retry_attempts
)

# Schedule jobs
schedule.every().hour.do(run_email_automation)
schedule.every().day.at("09:00").do(run_daily_reports)
schedule.every().monday.at("08:00").do(run_weekly_analysis)

def main():
    logger.info("Starting Incredible API automation service")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
```

## Best Practices

### 1. Error Handling

```python
from incredible_sdk.exceptions import (
    IncredibleAPIError,
    RateLimitError,
    AuthenticationError
)

try:
    result = client.chat_completion(messages=messages)
except RateLimitError as e:
    logger.warning(f"Rate limit hit, retrying in {e.retry_after} seconds")
    time.sleep(e.retry_after)
    result = client.chat_completion(messages=messages)
except AuthenticationError as e:
    logger.error(f"Authentication failed: {e}")
    # Handle auth refresh
except IncredibleAPIError as e:
    logger.error(f"API error: {e}")
    # Handle general API errors
```

### 2. Configuration Management

```python
# config/settings.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    api_key: str
    base_url: str = "https://api.incredible.one"
    user_id: str
    timeout: int = 30
    retry_attempts: int = 3

    # Integration settings
    gmail_user_id: str
    sheets_user_id: str
    slack_user_id: str

    # Monitoring
    log_level: str = "INFO"
    metrics_enabled: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
```

### 3. Monitoring and Metrics

```python
# monitoring/metrics.py
import time
from functools import wraps
from prometheus_client import Counter, Histogram, start_http_server

# Metrics
api_calls_total = Counter('incredible_api_calls_total', 'Total API calls', ['endpoint', 'status'])
api_call_duration = Histogram('incredible_api_call_duration_seconds', 'API call duration')

def monitor_api_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            api_calls_total.labels(endpoint=func.__name__, status='success').inc()
            return result
        except Exception as e:
            api_calls_total.labels(endpoint=func.__name__, status='error').inc()
            raise
        finally:
            duration = time.time() - start_time
            api_call_duration.observe(duration)

    return wrapper

# Start metrics server
start_http_server(8000)
```

## Next Steps

This Python SDK provides a solid foundation for building production-ready applications with the Incredible API. Key next steps:

1. **[Explore JavaScript SDK](../javascript/)** - If you need Node.js support
2. **[Advanced Patterns](../../advanced/)** - Learn architectural patterns
3. **[Production Deployment](../../advanced/deployment/)** - Scale your applications
4. **[Community Examples](https://github.com/incredible-api/community-examples)** - See what others are building

The Python SDK is designed to grow with your needs, from simple scripts to enterprise-scale applications.
