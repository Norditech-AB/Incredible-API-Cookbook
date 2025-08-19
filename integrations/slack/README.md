# Slack Integration Guide

Complete guide to integrating Slack with Incredible API for team communication, notifications, and workflow automation.

## 💬 **Slack Integration Overview**

The Slack integration allows your agents to:
- **📢 Send Messages**: Post messages to channels and direct messages
- **🔔 Create Notifications**: Send alerts and updates to teams
- **📊 Share Reports**: Distribute automated reports and dashboards
- **🤖 Bot Interactions**: Create interactive bots and commands
- **📋 Workflow Automation**: Trigger actions based on Slack events

## 🔐 **Authentication Setup**

Slack uses OAuth 2.0 with bot tokens for secure access to workspaces.

### 1. **OAuth Configuration**

<div class="code-tabs" data-section="slack-oauth">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python">import requests

def initiate_slack_oauth():
    """Start Slack OAuth flow"""
    url = "https://api.incredible.one/v1/integrations/slack/connect"
    
    data = {
        "user_id": "your_user_id",
        "callback_url": "https://your-app.com/oauth/slack"
    }
    
    response = requests.post(url, json=data, headers={
        "Authorization": "Bearer YOUR_API_KEY"
    })
    
    if response.status_code == 200:
        result = response.json()
        print(f"Visit: {result['redirect_url']}")
        return result['redirect_url']
    else:
        print("OAuth initiation failed")
        return None

# Usage
oauth_url = initiate_slack_oauth()
print(f"Complete OAuth at: {oauth_url}")</code></pre>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">const axios = require('axios');

async function initiateSlackOAuth() {
    // Start Slack OAuth flow
    const url = "https://api.incredible.one/v1/integrations/slack/connect";
    
    const data = {
        user_id: "your_user_id",
        callback_url: "https://your-app.com/oauth/slack"
    };
    
    try {
        const response = await axios.post(url, data, {
            headers: {
                "Authorization": "Bearer YOUR_API_KEY"
            }
        });
        
        console.log(`Visit: ${response.data.redirect_url}`);
        return response.data.redirect_url;
    } catch (error) {
        console.log("OAuth initiation failed:", error.response?.data);
        return null;
    }
}

// Usage
const oauthUrl = await initiateSlackOAuth();
console.log(`Complete OAuth at: ${oauthUrl}`);</code></pre>
  </div>
</div>

### 2. **Required Scopes**

The Slack integration requests these OAuth scopes:
- `chat:write` - Send messages to channels and DMs
- `channels:read` - Access public channel information
- `users:read` - Access user profile information
- `files:write` - Upload files and attachments

## 🛠️ **Available Features**

### 📢 **Send Messages**

<div class="code-tabs" data-section="slack-send">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python">def send_slack_message(channel, text, blocks=None):
    """Send message to Slack channel"""
    url = "https://api.incredible.one/v1/integrations/slack/execute"
    
    data = {
        "user_id": "your_user_id",
        "feature_name": "send_message",
        "inputs": {
            "channel": channel,
            "text": text,
            "blocks": blocks  # Optional rich formatting
        }
    }
    
    response = requests.post(url, json=data, headers={
        "Authorization": "Bearer YOUR_API_KEY"
    })
    
    if response.status_code == 200:
        result = response.json()
        print(f"Message sent: {result['result']['ts']}")
        return result['result']
    else:
        print(f"Send failed: {response.text}")
        return None

# Usage examples
# Simple text message
send_slack_message("#general", "Hello team! 👋")

# Direct message to user
send_slack_message("@john.doe", "Please review the latest report")

# Message with rich formatting
rich_message = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Daily Report* 📊\n• Sales: $15,000\n• Leads: 25\n• Support Tickets: 3"
        }
    }
]
send_slack_message("#sales", "Daily metrics are in!", rich_message)</code></pre>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">async function sendSlackMessage(channel, text, blocks = null) {
    // Send message to Slack channel
    const url = "https://api.incredible.one/v1/integrations/slack/execute";
    
    const data = {
        user_id: "your_user_id",
        feature_name: "send_message",
        inputs: {
            channel: channel,
            text: text,
            blocks: blocks  // Optional rich formatting
        }
    };
    
    try {
        const response = await axios.post(url, data, {
            headers: {
                "Authorization": "Bearer YOUR_API_KEY"
            }
        });
        
        console.log(`Message sent: ${response.data.result.ts}`);
        return response.data.result;
    } catch (error) {
        console.log("Send failed:", error.response?.data);
        return null;
    }
}

// Usage examples
// Simple text message
await sendSlackMessage("#general", "Hello team! 👋");

// Direct message to user
await sendSlackMessage("@john.doe", "Please review the latest report");

// Message with rich formatting
const richMessage = [
    {
        type: "section",
        text: {
            type: "mrkdwn",
            text: "*Daily Report* 📊\n• Sales: $15,000\n• Leads: 25\n• Support Tickets: 3"
        }
    }
];
await sendSlackMessage("#sales", "Daily metrics are in!", richMessage);</code></pre>
  </div>
</div>

### 🔔 **Notification System**

<div class="code-tabs" data-section="slack-notifications">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python">class SlackNotifier:
    def __init__(self):
        self.base_url = "https://api.incredible.one"
        self.notification_channels = {
            "alerts": "#alerts",
            "sales": "#sales-team",
            "support": "#support",
            "dev": "#dev-team"
        }
    
    def send_alert(self, alert_type, message, priority="normal"):
        """Send categorized alerts to appropriate channels"""
        channel = self.notification_channels.get(alert_type, "#general")
        
        # Format message based on priority
        if priority == "high":
            formatted_message = f"🚨 *HIGH PRIORITY ALERT*\n{message}"
        elif priority == "medium":
            formatted_message = f"⚠️ *Alert*\n{message}"
        else:
            formatted_message = f"ℹ️ {message}"
        
        return send_slack_message(channel, formatted_message)
    
    def send_metrics_report(self, metrics, channel="#general"):
        """Send formatted metrics report"""
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📊 Performance Metrics"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Revenue:*\n${metrics.get('revenue', 0):,.2f}"
                    },
                    {
                        "type": "mrkdwn", 
                        "text": f"*New Leads:*\n{metrics.get('leads', 0)}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Support Tickets:*\n{metrics.get('tickets', 0)}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Conversion Rate:*\n{metrics.get('conversion', 0):.1f}%"
                    }
                ]
            }
        ]
        
        return send_slack_message(channel, "Daily metrics update", blocks)
    
    def send_system_notification(self, event_type, details):
        """Send system event notifications"""
        event_messages = {
            "deployment": f"🚀 New deployment: {details}",
            "error": f"❌ System error: {details}",
            "backup": f"💾 Backup completed: {details}",
            "maintenance": f"🔧 Maintenance scheduled: {details}"
        }
        
        message = event_messages.get(event_type, f"📢 System event: {details}")
        return self.send_alert("dev", message)

# Usage examples
notifier = SlackNotifier()

# Send high priority alert
notifier.send_alert("support", "Customer unable to login - investigating", "high")

# Send daily metrics
daily_metrics = {
    "revenue": 15750.50,
    "leads": 23,
    "tickets": 5,
    "conversion": 8.2
}
notifier.send_metrics_report(daily_metrics, "#management")

# Send system notification
notifier.send_system_notification("deployment", "v2.1.3 deployed successfully")</code></pre>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">class SlackNotifier {
    constructor() {
        this.baseUrl = "https://api.incredible.one";
        this.notificationChannels = {
            "alerts": "#alerts",
            "sales": "#sales-team",
            "support": "#support",
            "dev": "#dev-team"
        };
    }
    
    async sendAlert(alertType, message, priority = "normal") {
        // Send categorized alerts to appropriate channels
        const channel = this.notificationChannels[alertType] || "#general";
        
        let formattedMessage;
        if (priority === "high") {
            formattedMessage = `🚨 *HIGH PRIORITY ALERT*\n${message}`;
        } else if (priority === "medium") {
            formattedMessage = `⚠️ *Alert*\n${message}`;
        } else {
            formattedMessage = `ℹ️ ${message}`;
        }
        
        return await sendSlackMessage(channel, formattedMessage);
    }
    
    async sendMetricsReport(metrics, channel = "#general") {
        // Send formatted metrics report
        const blocks = [
            {
                type: "header",
                text: {
                    type: "plain_text",
                    text: "📊 Performance Metrics"
                }
            },
            {
                type: "section",
                fields: [
                    {
                        type: "mrkdwn",
                        text: `*Revenue:*\n$${(metrics.revenue || 0).toLocaleString()}`
                    },
                    {
                        type: "mrkdwn",
                        text: `*New Leads:*\n${metrics.leads || 0}`
                    },
                    {
                        type: "mrkdwn",
                        text: `*Support Tickets:*\n${metrics.tickets || 0}`
                    },
                    {
                        type: "mrkdwn",
                        text: `*Conversion Rate:*\n${(metrics.conversion || 0).toFixed(1)}%`
                    }
                ]
            }
        ];
        
        return await sendSlackMessage(channel, "Daily metrics update", blocks);
    }
    
    async sendSystemNotification(eventType, details) {
        // Send system event notifications
        const eventMessages = {
            "deployment": `🚀 New deployment: ${details}`,
            "error": `❌ System error: ${details}`,
            "backup": `💾 Backup completed: ${details}`,
            "maintenance": `🔧 Maintenance scheduled: ${details}`
        };
        
        const message = eventMessages[eventType] || `📢 System event: ${details}`;
        return await this.sendAlert("dev", message);
    }
}

// Usage examples
const notifier = new SlackNotifier();

// Send high priority alert
await notifier.sendAlert("support", "Customer unable to login - investigating", "high");

// Send daily metrics
const dailyMetrics = {
    revenue: 15750.50,
    leads: 23,
    tickets: 5,
    conversion: 8.2
};
await notifier.sendMetricsReport(dailyMetrics, "#management");

// Send system notification
await notifier.sendSystemNotification("deployment", "v2.1.3 deployed successfully");</code></pre>
  </div>
</div>

## 💬 **Message Formatting**

### 📝 **Markdown Formatting**
Slack supports markdown-style formatting:
- `*bold text*` - **Bold text**
- `_italic text_` - *Italic text*
- `~strikethrough~` - ~~Strikethrough~~
- `` `code` `` - `Inline code`
- `> quoted text` - Quoted text

### 🎨 **Block Kit Formatting**
Use Slack's Block Kit for rich, interactive messages:

```python
def create_interactive_message():
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🎯 Action Required"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "New high-priority lead requires attention"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Review Lead"
                },
                "url": "https://crm.company.com/leads/123"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Lead Score: 95/100 • Source: Website • Urgency: High"
                }
            ]
        }
    ]
    
    send_slack_message("#sales", "New lead alert", blocks)
```

## 🎯 **Common Use Cases**

### 📊 **Automated Reporting**

```python
def send_daily_report():
    """Send automated daily business report"""
    # Gather metrics from various sources
    metrics = {
        "sales": get_daily_sales(),
        "leads": get_new_leads_count(),
        "support_tickets": get_open_tickets(),
        "website_traffic": get_traffic_stats()
    }
    
    # Create comprehensive report
    report_blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "📈 Daily Business Report"}
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Sales Performance:*\n• Revenue: ${metrics['sales']['revenue']:,.2f}\n• Orders: {metrics['sales']['orders']}\n• Avg Order: ${metrics['sales']['avg_order']:,.2f}"
            }
        },
        {
            "type": "section", 
            "text": {
                "type": "mrkdwn",
                "text": f"*Lead Generation:*\n• New Leads: {metrics['leads']['new']}\n• Qualified: {metrics['leads']['qualified']}\n• Conversion Rate: {metrics['leads']['conversion_rate']:.1f}%"
            }
        }
    ]
    
    send_slack_message("#management", "Daily report ready", report_blocks)

# Schedule to run daily
send_daily_report()
```

### 🚨 **Alert System**

```python
class BusinessAlertSystem:
    def __init__(self):
        self.thresholds = {
            "revenue_drop": 0.15,      # 15% revenue drop
            "lead_drop": 0.20,         # 20% lead drop
            "support_backlog": 50,     # 50+ open tickets
            "system_error_rate": 0.05  # 5% error rate
        }
    
    def check_revenue_alerts(self, current_revenue, previous_revenue):
        """Check for revenue alerts"""
        drop_percent = (previous_revenue - current_revenue) / previous_revenue
        
        if drop_percent > self.thresholds["revenue_drop"]:
            self.send_alert(
                "🚨 Revenue Alert",
                f"Revenue dropped {drop_percent:.1%} from yesterday\nCurrent: ${current_revenue:,.2f}\nPrevious: ${previous_revenue:,.2f}",
                "#management",
                "high"
            )
    
    def check_support_backlog(self, open_tickets):
        """Check support ticket backlog"""
        if open_tickets > self.thresholds["support_backlog"]:
            self.send_alert(
                "🎧 Support Backlog Alert", 
                f"{open_tickets} open support tickets\nConsider adding support capacity",
                "#support",
                "medium"
            )
    
    def send_alert(self, title, message, channel, priority):
        """Send formatted alert"""
        priority_icons = {"high": "🚨", "medium": "⚠️", "low": "ℹ️"}
        icon = priority_icons.get(priority, "📢")
        
        formatted_message = f"{icon} *{title}*\n{message}"
        send_slack_message(channel, formatted_message)

# Usage
alert_system = BusinessAlertSystem()
alert_system.check_revenue_alerts(45000, 52000)
alert_system.check_support_backlog(75)
```

### 🤖 **Team Collaboration**

```python
def coordinate_team_workflow(task_type, details):
    """Coordinate workflows between teams"""
    
    workflows = {
        "new_customer": {
            "sales": "🎉 New customer signed! Please update CRM and send welcome package",
            "support": "📞 New customer onboarded. Please prepare welcome call",
            "dev": "👤 New customer account created. Monitor for any setup issues"
        },
        "bug_report": {
            "dev": "🐛 New bug report received. Please investigate and assign priority",
            "support": "📝 Bug report logged. Please follow up with customer on timeline", 
            "management": "📊 New bug report impacts customer satisfaction metrics"
        },
        "feature_request": {
            "product": "💡 New feature request from customer. Please evaluate and prioritize",
            "dev": "🛠️ Feature request received. Technical feasibility assessment needed",
            "sales": "📈 Customer feature request may indicate market opportunity"
        }
    }
    
    team_channels = {
        "sales": "#sales-team",
        "support": "#support",
        "dev": "#dev-team", 
        "product": "#product",
        "management": "#management"
    }
    
    if task_type in workflows:
        for team, message in workflows[task_type].items():
            channel = team_channels.get(team, "#general")
            send_slack_message(channel, f"{message}\n\n*Details:* {details}")

# Usage
coordinate_team_workflow("new_customer", "Acme Corp - Enterprise plan - $50k ARR")
coordinate_team_workflow("bug_report", "Login issues affecting mobile users")
```

## 🔒 **Security & Best Practices**

### 🛡️ **Security Guidelines**
- **Token Management**: Securely store and rotate bot tokens
- **Channel Access**: Limit bot access to necessary channels only
- **Message Content**: Avoid sending sensitive data in messages
- **User Privacy**: Respect user privacy and workspace policies

### 📊 **Performance Optimization**
- **Rate Limiting**: Respect Slack's API rate limits (1 message per second)
- **Message Batching**: Combine multiple updates into single messages
- **Channel Strategy**: Use appropriate channels to avoid spam
- **Error Handling**: Handle API errors and retries gracefully

### 💬 **Communication Best Practices**
- **Clear Formatting**: Use consistent message formatting and structure
- **Actionable Content**: Include clear next steps and action items
- **Context**: Provide sufficient context for team members
- **Timing**: Send messages at appropriate times for team productivity

## 📈 **Advanced Features**

### 🔗 **Webhook Integration**

```python
def setup_slack_webhooks():
    """Set up incoming webhooks for external systems"""
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    
    def send_webhook_message(text, channel="#general"):
        payload = {
            "text": text,
            "channel": channel,
            "username": "Business Bot",
            "icon_emoji": ":robot_face:"
        }
        requests.post(webhook_url, json=payload)
    
    return send_webhook_message
```

### 📊 **Analytics & Tracking**

```python
def track_message_engagement():
    """Track message engagement and effectiveness"""
    # Monitor message responses
    # Track click-through rates on links
    # Measure team response times
    # Analyze communication patterns
    pass
```

### 🤖 **Interactive Bots**

```python
def create_interactive_bot():
    """Create interactive Slack bot with commands"""
    # Handle slash commands
    # Process interactive button clicks
    # Manage conversational flows
    # Provide contextual responses
    pass
```

---

*Transform team communication with intelligent Slack automation that keeps everyone informed, aligned, and productive.*
