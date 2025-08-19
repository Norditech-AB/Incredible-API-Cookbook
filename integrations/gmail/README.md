# Gmail Integration Guide

Complete guide to integrating Gmail with Incredible API for email automation, monitoring, and intelligent email processing.

## 📧 **Gmail Integration Overview**

The Gmail integration allows your agents to:
- **📨 Send Emails**: Compose and send emails programmatically
- **🔍 Search Emails**: Query emails with advanced search criteria
- **📬 Monitor Inbox**: Watch for new emails and process automatically
- **📋 Extract Data**: Parse email content for leads, receipts, and information
- **📊 Track Metrics**: Monitor email performance and engagement

## 🔐 **Authentication Setup**

Gmail uses OAuth 2.0 authentication for secure access to user email accounts.

### 1. **OAuth Configuration**

<div class="code-tabs" data-section="gmail-oauth">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python">import requests

def initiate_gmail_oauth():
    """Start Gmail OAuth flow"""
    url = "https://api.incredible.one/v1/integrations/gmail/connect"
    
    data = {
        "user_id": "your_user_id",
        "callback_url": "https://your-app.com/oauth/gmail"
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
oauth_url = initiate_gmail_oauth()
print(f"Complete OAuth at: {oauth_url}")</code></pre>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">const axios = require('axios');

async function initiateGmailOAuth() {
    // Start Gmail OAuth flow
    const url = "https://api.incredible.one/v1/integrations/gmail/connect";
    
    const data = {
        user_id: "your_user_id",
        callback_url: "https://your-app.com/oauth/gmail"
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
const oauthUrl = await initiateGmailOAuth();
console.log(`Complete OAuth at: ${oauthUrl}`);</code></pre>
  </div>
</div>

### 2. **Required Scopes**

The Gmail integration requests these OAuth scopes:
- `https://www.googleapis.com/auth/gmail.send` - Send emails
- `https://www.googleapis.com/auth/gmail.readonly` - Read emails
- `https://www.googleapis.com/auth/gmail.modify` - Modify labels and metadata

## 🛠️ **Available Features**

### 📨 **Send Email**

<div class="code-tabs" data-section="gmail-send">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python">def send_email(to, subject, body, cc=None, bcc=None):
    """Send email via Gmail"""
    url = "https://api.incredible.one/v1/integrations/gmail/execute"
    
    data = {
        "user_id": "your_user_id",
        "feature_name": "GMAIL_SEND_EMAIL",
        "inputs": {
            "to": to,
            "subject": subject,
            "body": body,
            "cc": cc,
            "bcc": bcc
        }
    }
    
    response = requests.post(url, json=data, headers={
        "Authorization": "Bearer YOUR_API_KEY"
    })
    
    if response.status_code == 200:
        result = response.json()
        print(f"Email sent: {result['result']['message_id']}")
        return result['result']
    else:
        print(f"Send failed: {response.text}")
        return None

# Usage examples
send_email(
    to="customer@example.com",
    subject="Welcome to our service",
    body="Thank you for signing up! Here's how to get started..."
)

send_email(
    to="team@company.com",
    subject="Weekly Report",
    body="Please find this week's metrics attached.",
    cc="manager@company.com"
)</code></pre>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">async function sendEmail(to, subject, body, cc = null, bcc = null) {
    // Send email via Gmail
    const url = "https://api.incredible.one/v1/integrations/gmail/execute";
    
    const data = {
        user_id: "your_user_id",
        feature_name: "GMAIL_SEND_EMAIL",
        inputs: {
            to: to,
            subject: subject,
            body: body,
            cc: cc,
            bcc: bcc
        }
    };
    
    try {
        const response = await axios.post(url, data, {
            headers: {
                "Authorization": "Bearer YOUR_API_KEY"
            }
        });
        
        console.log(`Email sent: ${response.data.result.message_id}`);
        return response.data.result;
    } catch (error) {
        console.log("Send failed:", error.response?.data);
        return null;
    }
}

// Usage examples
await sendEmail(
    "customer@example.com",
    "Welcome to our service",
    "Thank you for signing up! Here's how to get started..."
);

await sendEmail(
    "team@company.com",
    "Weekly Report", 
    "Please find this week's metrics attached.",
    "manager@company.com"
);</code></pre>
  </div>
</div>

### 🔍 **Search Emails**

<div class="code-tabs" data-section="gmail-search">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python">def search_emails(query, max_results=10):
    """Search emails with Gmail query syntax"""
    url = "https://api.incredible.one/v1/integrations/gmail/execute"
    
    data = {
        "user_id": "your_user_id",
        "feature_name": "gmail_search",
        "inputs": {
            "query": query,
            "max_results": max_results
        }
    }
    
    response = requests.post(url, json=data, headers={
        "Authorization": "Bearer YOUR_API_KEY"
    })
    
    if response.status_code == 200:
        result = response.json()
        emails = result['result']['emails']
        print(f"Found {len(emails)} emails")
        return emails
    else:
        print(f"Search failed: {response.text}")
        return []

# Usage examples
# Search for unread emails
unread_emails = search_emails("is:unread")

# Search for emails from specific sender
customer_emails = search_emails("from:customer@example.com")

# Search for emails with specific subject
support_emails = search_emails("subject:support OR subject:help")

# Search for recent emails
recent_emails = search_emails("newer_than:1d")

# Complex search query
urgent_emails = search_emails("is:unread (urgent OR priority OR asap) newer_than:6h")</code></pre>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">async function searchEmails(query, maxResults = 10) {
    // Search emails with Gmail query syntax
    const url = "https://api.incredible.one/v1/integrations/gmail/execute";
    
    const data = {
        user_id: "your_user_id",
        feature_name: "gmail_search",
        inputs: {
            query: query,
            max_results: maxResults
        }
    };
    
    try {
        const response = await axios.post(url, data, {
            headers: {
                "Authorization": "Bearer YOUR_API_KEY"
            }
        });
        
        const emails = response.data.result.emails;
        console.log(`Found ${emails.length} emails`);
        return emails;
    } catch (error) {
        console.log("Search failed:", error.response?.data);
        return [];
    }
}

// Usage examples
// Search for unread emails
const unreadEmails = await searchEmails("is:unread");

// Search for emails from specific sender
const customerEmails = await searchEmails("from:customer@example.com");

// Search for emails with specific subject
const supportEmails = await searchEmails("subject:support OR subject:help");

// Search for recent emails
const recentEmails = await searchEmails("newer_than:1d");

// Complex search query
const urgentEmails = await searchEmails("is:unread (urgent OR priority OR asap) newer_than:6h");</code></pre>
  </div>
</div>

## 📊 **Gmail Query Syntax**

Gmail supports powerful search operators:

### 📅 **Date & Time**
- `newer_than:2d` - Emails newer than 2 days
- `older_than:1w` - Emails older than 1 week
- `after:2024/1/1` - Emails after specific date
- `before:2024/12/31` - Emails before specific date

### 👤 **Sender & Recipient**
- `from:user@example.com` - From specific sender
- `to:me` - Sent to you
- `cc:manager@company.com` - CC'd to specific person
- `bcc:team@company.com` - BCC'd to specific person

### 📝 **Content**
- `subject:meeting` - Subject contains "meeting"
- `has:attachment` - Has attachments
- `filename:pdf` - Specific file type
- `"exact phrase"` - Exact phrase match

### 🏷️ **Labels & Status**
- `is:unread` - Unread emails
- `is:important` - Important emails
- `label:work` - Specific label
- `is:starred` - Starred emails

### 🔗 **Operators**
- `OR` - Either condition
- `AND` - Both conditions (default)
- `-` - Exclude (e.g., `-from:spam@example.com`)
- `()` - Group conditions

## 🎯 **Common Use Cases**

### 📈 **Lead Generation**

```python
# Find potential sales leads
lead_queries = [
    "subject:(inquiry OR quote OR pricing OR demo)",
    "subject:(interested OR information OR consultation)",
    "\"looking for\" OR \"need help\" OR \"can you help\""
]

for query in lead_queries:
    leads = search_emails(query + " newer_than:1d")
    for email in leads:
        process_potential_lead(email)
```

### 🎧 **Customer Support**

```python
# Monitor support emails
support_emails = search_emails("to:support@company.com is:unread")

for email in support_emails:
    create_support_ticket(email)
    send_auto_response(email)
```

### 📊 **Email Analytics**

```python
# Analyze email patterns
newsletter_opens = search_emails("from:newsletter@company.com has:opened")
unsubscribes = search_emails("subject:unsubscribe")

print(f"Newsletter engagement: {len(newsletter_opens)} opens")
print(f"Unsubscribe requests: {len(unsubscribes)}")
```

## 🔒 **Security & Best Practices**

### 🛡️ **OAuth Security**
- **Scope Limitation**: Only request necessary OAuth scopes
- **Token Storage**: Securely store and encrypt OAuth tokens
- **Token Refresh**: Handle token expiration gracefully
- **Revocation**: Provide users ability to revoke access

### 📧 **Email Handling**
- **Rate Limiting**: Respect Gmail API rate limits
- **Error Handling**: Handle API errors and retries appropriately
- **Privacy**: Protect sensitive email content and metadata
- **Compliance**: Follow email privacy regulations (GDPR, CAN-SPAM)

### 🔍 **Search Optimization**
- **Specific Queries**: Use specific search terms to reduce API calls
- **Pagination**: Handle large result sets with pagination
- **Caching**: Cache frequently accessed emails appropriately
- **Monitoring**: Monitor API usage and quota consumption

## 📈 **Advanced Features**

### 📬 **Email Monitoring**

Set up real-time email monitoring:

```python
def setup_email_monitoring():
    """Set up Gmail push notifications"""
    # Configure webhook for real-time email notifications
    # Process emails as they arrive for immediate responses
    pass
```

### 📨 **Template Management**

Create reusable email templates:

```python
email_templates = {
    "welcome": {
        "subject": "Welcome to {company_name}!",
        "body": "Hi {customer_name}, welcome to our platform..."
    },
    "follow_up": {
        "subject": "Following up on your inquiry",
        "body": "Hi {customer_name}, thank you for your interest..."
    }
}

def send_template_email(template_name, recipient, variables):
    template = email_templates[template_name]
    subject = template["subject"].format(**variables)
    body = template["body"].format(**variables)
    send_email(recipient, subject, body)
```

### 📊 **Email Analytics**

Track email performance:

```python
def analyze_email_performance():
    """Analyze sent email performance"""
    sent_emails = search_emails("in:sent newer_than:7d")
    
    metrics = {
        "total_sent": len(sent_emails),
        "replies_received": len(search_emails("is:unread newer_than:7d")),
        "bounce_rate": calculate_bounce_rate(sent_emails)
    }
    
    return metrics
```

---

*Master Gmail integration to create powerful email automation workflows that enhance communication, improve customer service, and drive business growth.*
