# Financial Dashboard Agent

Automate your financial data collection, analysis, and reporting with an intelligent agent that gathers data from multiple sources and delivers comprehensive insights.

## 📋 **Workflow Overview**

```
💰 Financial APIs → 📊 Google Sheets → 📧 Gmail
   Data Collection     Analysis       Reports
```

**Apps Used:** Perplexity (Financial Data) + Google Sheets + Gmail (3 apps total)

## 🎯 **What This Agent Does**

1. **💰 Collect**: Gathers financial data from multiple sources via web research
2. **📊 Analyze**: Processes and organizes data in structured spreadsheets
3. **📧 Report**: Delivers executive summaries and detailed reports via email

## 🛠 **Prerequisites**

- Incredible API access with function calling enabled
- Connected integrations:
  - Perplexity (API key authentication)
  - Google Sheets (OAuth)
  - Gmail (OAuth)

## 📋 **Setup**

### Environment Configuration

```bash
# .env
INCREDIBLE_API_KEY=your_incredible_api_key
INCREDIBLE_BASE_URL=https://api.incredible.one
USER_ID=your_user_id

# Financial Dashboard Settings
FINANCIAL_DASHBOARD_SHEET_ID=your_google_sheet_id
REPORT_RECIPIENTS=cfo@company.com,finance-team@company.com

# Research Parameters
COMPANY_SYMBOLS=AAPL,GOOGL,MSFT,TSLA  # Stock symbols to track
MARKET_SECTORS=technology,healthcare,finance
```

## 💻 **Implementation**

<div class="code-tabs" data-section="financial-dashboard">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python">import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class FinancialDashboard:
def **init**(self):
self.api_key = os.getenv('INCREDIBLE_API_KEY')
self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
self.user_id = os.getenv('USER_ID')
self.sheet_id = os.getenv('FINANCIAL_DASHBOARD_SHEET_ID')
self.recipients = os.getenv('REPORT_RECIPIENTS', '').split(',')

        self.company_symbols = os.getenv('COMPANY_SYMBOLS', 'AAPL,GOOGL').split(',')
        self.market_sectors = os.getenv('MARKET_SECTORS', 'technology,finance').split(',')

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def research_financial_data(self, data_type="market_overview"):
        """Research financial data using Perplexity AI"""
        print(f"💰 Researching {data_type}...")

        queries = {
            "market_overview": [
                "US stock market performance today major indices",
                "S&P 500 Nasdaq Dow Jones current status",
                "market volatility VIX fear greed index today"
            ],
            "company_analysis": [
                f"stock performance analysis {' '.join(self.company_symbols)} latest earnings",
                f"financial news {' '.join(self.company_symbols)} recent developments",
                f"analyst ratings price targets {' '.join(self.company_symbols)}"
            ],
            "sector_trends": [
                f"sector performance analysis {' '.join(self.market_sectors)} stocks",
                f"industry trends {' '.join(self.market_sectors)} market outlook",
                f"sector rotation investment flows {' '.join(self.market_sectors)}"
            ],
            "economic_indicators": [
                "Federal Reserve interest rates inflation data today",
                "economic indicators GDP unemployment consumer confidence",
                "currency exchange rates USD major pairs forex"
            ]
        }

        research_results = []

        for query in queries.get(data_type, []):
            result = self.execute_perplexity_search(query)
            research_results.append({
                'query': query,
                'data': result,
                'timestamp': datetime.now().isoformat(),
                'category': data_type
            })

        return research_results

    def execute_perplexity_search(self, query):
        """Execute Perplexity search for financial data"""
        url = f"{self.base_url}/v1/integrations/perplexity/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "PerplexityAISearch",
            "inputs": {
                "query": query
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get('result', {}).get('answer', 'No data available')
            else:
                return f"Research failed: {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"

    def process_financial_data(self, research_results):
        """Process and structure financial data for analysis"""
        print("📊 Processing financial data...")

        processed_data = {
            'market_summary': [],
            'key_metrics': [],
            'alerts': [],
            'recommendations': []
        }

        for result in research_results:
            # Extract key information from research
            data = result['data']
            category = result['category']

            # Simple keyword extraction for market movements
            if 'up' in data.lower() or 'gain' in data.lower() or 'rise' in data.lower():
                sentiment = 'POSITIVE'
            elif 'down' in data.lower() or 'fall' in data.lower() or 'decline' in data.lower():
                sentiment = 'NEGATIVE'
            else:
                sentiment = 'NEUTRAL'

            processed_item = {
                'category': category,
                'query': result['query'],
                'sentiment': sentiment,
                'summary': data[:200] + '...' if len(data) > 200 else data,
                'full_data': data,
                'timestamp': result['timestamp']
            }

            # Categorize based on content
            if category == 'market_overview':
                processed_data['market_summary'].append(processed_item)
            elif 'company' in category or any(symbol.lower() in data.lower() for symbol in self.company_symbols):
                processed_data['key_metrics'].append(processed_item)

            # Generate alerts for significant movements
            alert_keywords = ['surge', 'plunge', 'crash', 'rally', 'volatile', 'breaking']
            if any(keyword in data.lower() for keyword in alert_keywords):
                processed_data['alerts'].append({
                    'level': 'HIGH',
                    'message': processed_item['summary'],
                    'category': category,
                    'timestamp': result['timestamp']
                })

        return processed_data

    def save_to_dashboard(self, processed_data):
        """Save processed data to Google Sheets dashboard"""
        print("📊 Updating dashboard in Google Sheets...")

        # Prepare sheets data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Market Summary Sheet
        market_data = []
        market_data.append(["Timestamp", "Category", "Query", "Sentiment", "Summary"])

        for item in processed_data['market_summary']:
            market_data.append([
                timestamp,
                item['category'],
                item['query'],
                item['sentiment'],
                item['summary']
            ])

        # Key Metrics Sheet
        metrics_data = []
        metrics_data.append(["Timestamp", "Category", "Sentiment", "Summary", "Alert_Level"])

        for item in processed_data['key_metrics']:
            alert_level = "HIGH" if any(alert['message'] in item['summary'] for alert in processed_data['alerts']) else "NORMAL"
            metrics_data.append([
                timestamp,
                item['category'],
                item['sentiment'],
                item['summary'],
                alert_level
            ])

        # Update Market Summary Sheet
        self.update_sheet("Market_Summary!A:E", market_data)

        # Update Key Metrics Sheet
        self.update_sheet("Key_Metrics!A:E", metrics_data)

        # Update Alerts Sheet if there are alerts
        if processed_data['alerts']:
            alerts_data = []
            alerts_data.append(["Timestamp", "Level", "Category", "Message"])

            for alert in processed_data['alerts']:
                alerts_data.append([
                    timestamp,
                    alert['level'],
                    alert['category'],
                    alert['message']
                ])

            self.update_sheet("Alerts!A:D", alerts_data)

    def update_sheet(self, range_name, data):
        """Update specific sheet range with data"""
        url = f"{self.base_url}/v1/integrations/google_sheets/execute"

        request_data = {
            "user_id": self.user_id,
            "feature_name": "sheets_update_range",
            "inputs": {
                "spreadsheet_id": self.sheet_id,
                "range": range_name,
                "values": data
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=request_data)
            if response.status_code == 200:
                print(f"✅ Updated {range_name}")
                return True
            else:
                print(f"❌ Failed to update {range_name}: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Sheet update error: {e}")
            return False

    def generate_executive_summary(self, processed_data):
        """Generate executive summary report"""
        print("📝 Generating executive summary...")

        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

        # Count sentiments
        total_items = len(processed_data['market_summary']) + len(processed_data['key_metrics'])
        positive_count = sum(1 for item in processed_data['market_summary'] + processed_data['key_metrics']
                           if item['sentiment'] == 'POSITIVE')
        negative_count = sum(1 for item in processed_data['market_summary'] + processed_data['key_metrics']
                           if item['sentiment'] == 'NEGATIVE')

        market_sentiment = "BULLISH" if positive_count > negative_count else "BEARISH" if negative_count > positive_count else "MIXED"

        summary = f"""

📊 **Financial Dashboard Report**
📅 Generated: {timestamp}

## 🎯 Executive Summary

**Market Sentiment**: {market_sentiment}
**Data Points Analyzed**: {total_items}
**Positive Signals**: {positive_count}
**Negative Signals**: {negative_count}
**Active Alerts**: {len(processed_data['alerts'])}

## 📈 Market Overview

"""

        # Add market summary highlights
        for item in processed_data['market_summary'][:3]:  # Top 3 items
            summary += f"• **{item['sentiment']}**: {item['summary']}\n"

        summary += "\n## 🏢 Company Analysis\n\n"

        # Add key metrics highlights
        for item in processed_data['key_metrics'][:3]:  # Top 3 items
            summary += f"• **{item['sentiment']}**: {item['summary']}\n"

        # Add alerts if any
        if processed_data['alerts']:
            summary += "\n## 🚨 Important Alerts\n\n"
            for alert in processed_data['alerts']:
                summary += f"• **{alert['level']}**: {alert['message']}\n"

        summary += f"""

## 📊 Detailed Analysis

For comprehensive data and charts, view the full dashboard:
[Financial Dashboard](https://docs.google.com/spreadsheets/d/{self.sheet_id})

### 📋 Key Actions Recommended

• Monitor high-alert items closely
• Review portfolio allocation based on sector trends
• Consider market sentiment in upcoming decisions
• Schedule follow-up analysis if volatility increases

---

🤖 **Generated by Incredible Financial Dashboard Agent**
_This report combines real-time financial research with automated analysis_
"""

        return summary

    def send_financial_report(self, summary):
        """Send financial report via email"""
        print("📧 Sending financial report...")

        subject = f"Financial Dashboard Report - {datetime.now().strftime('%B %d, %Y')}"

        for recipient in self.recipients:
            if not recipient.strip():
                continue

            url = f"{self.base_url}/v1/integrations/gmail/execute"

            data = {
                "user_id": self.user_id,
                "feature_name": "GMAIL_SEND_EMAIL",
                "inputs": {
                    "to": recipient.strip(),
                    "subject": subject,
                    "body": summary
                }
            }

            try:
                response = requests.post(url, headers=self.headers, json=data)
                if response.status_code == 200:
                    print(f"✅ Report sent to {recipient.strip()}")
                else:
                    print(f"❌ Failed to send to {recipient.strip()}: {response.text}")
            except Exception as e:
                print(f"❌ Email error for {recipient.strip()}: {e}")

    def run_daily_analysis(self):
        """Execute complete daily financial analysis workflow"""
        print("🚀 Starting Daily Financial Analysis")
        print(f"📊 Dashboard Sheet: {self.sheet_id}")
        print(f"📧 Report Recipients: {', '.join(self.recipients)}")
        print(f"📈 Tracking: {', '.join(self.company_symbols)}")
        print()

        all_research = []

        # Research different categories
        categories = ["market_overview", "company_analysis", "sector_trends", "economic_indicators"]

        for category in categories:
            research_results = self.research_financial_data(category)
            all_research.extend(research_results)

        if not all_research:
            print("❌ No financial data collected")
            return False

        # Process the data
        processed_data = self.process_financial_data(all_research)

        # Update dashboard
        dashboard_updated = self.save_to_dashboard(processed_data)

        # Generate and send report
        summary = self.generate_executive_summary(processed_data)
        self.send_financial_report(summary)

        # Results summary
        print(f"\n🎉 Financial Analysis Complete!")
        print(f"📊 Data points collected: {len(all_research)}")
        print(f"🚨 Alerts generated: {len(processed_data['alerts'])}")
        print(f"{'✅' if dashboard_updated else '❌'} Dashboard updated")
        print(f"📧 Reports sent to {len([r for r in self.recipients if r.strip()])} recipients")
        print(f"📊 View dashboard: https://docs.google.com/spreadsheets/d/{self.sheet_id}")

        return True

# Usage Examples

if **name** == "**main**":
dashboard = FinancialDashboard()

    # Run complete daily analysis
    dashboard.run_daily_analysis()

    print("\n" + "="*50 + "\n")

    # Run specific category analysis
    results = dashboard.research_financial_data("market_overview")
    processed = dashboard.process_financial_data(results)
    summary = dashboard.generate_executive_summary(processed)
    print("📊 Market Overview Analysis:")
    print(summary)</code></pre>

  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">const axios = require("axios");
require("dotenv").config();

class FinancialDashboard {
constructor() {
this.apiKey = process.env.INCREDIBLE_API_KEY;
this.baseUrl = process.env.INCREDIBLE_BASE_URL || "https://api.incredible.one";
this.userId = process.env.USER_ID;
this.sheetId = process.env.FINANCIAL_DASHBOARD_SHEET_ID;
this.recipients = (process.env.REPORT_RECIPIENTS || '').split(',');

    this.companySymbols = (process.env.COMPANY_SYMBOLS || 'AAPL,GOOGL').split(',');
    this.marketSectors = (process.env.MARKET_SECTORS || 'technology,finance').split(',');

    this.headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${this.apiKey}`,
    };

}

async researchFinancialData(dataType = "market_overview") {
console.log(`💰 Researching ${dataType}...`);

    const queries = {
      market_overview: [
        "US stock market performance today major indices",
        "S&P 500 Nasdaq Dow Jones current status",
        "market volatility VIX fear greed index today"
      ],
      company_analysis: [
        `stock performance analysis ${this.companySymbols.join(' ')} latest earnings`,
        `financial news ${this.companySymbols.join(' ')} recent developments`,
        `analyst ratings price targets ${this.companySymbols.join(' ')}`
      ],
      sector_trends: [
        `sector performance analysis ${this.marketSectors.join(' ')} stocks`,
        `industry trends ${this.marketSectors.join(' ')} market outlook`,
        `sector rotation investment flows ${this.marketSectors.join(' ')}`
      ],
      economic_indicators: [
        "Federal Reserve interest rates inflation data today",
        "economic indicators GDP unemployment consumer confidence",
        "currency exchange rates USD major pairs forex"
      ]
    };

    const researchResults = [];

    for (const query of (queries[dataType] || [])) {
      const result = await this.executePerplexitySearch(query);
      researchResults.push({
        query: query,
        data: result,
        timestamp: new Date().toISOString(),
        category: dataType
      });
    }

    return researchResults;

}

async executePerplexitySearch(query) {
const url = `${this.baseUrl}/v1/integrations/perplexity/execute`;

    const data = {
      user_id: this.userId,
      feature_name: "PerplexityAISearch",
      inputs: {
        query: query
      }
    };

    try {
      const response = await axios.post(url, data, { headers: this.headers });
      if (response.status === 200) {
        return response.data.result?.answer || 'No data available';
      } else {
        return `Research failed: ${response.data}`;
      }
    } catch (error) {
      return `Error: ${error.message}`;
    }

}

processFinancialData(researchResults) {
console.log("📊 Processing financial data...");

    const processedData = {
      market_summary: [],
      key_metrics: [],
      alerts: [],
      recommendations: []
    };

    for (const result of researchResults) {
      const data = result.data;
      const category = result.category;

      // Simple sentiment analysis
      let sentiment = 'NEUTRAL';
      if (/\b(up|gain|rise|bull|positive|growth)\b/i.test(data)) {
        sentiment = 'POSITIVE';
      } else if (/\b(down|fall|decline|bear|negative|loss)\b/i.test(data)) {
        sentiment = 'NEGATIVE';
      }

      const processedItem = {
        category: category,
        query: result.query,
        sentiment: sentiment,
        summary: data.length > 200 ? data.substring(0, 200) + '...' : data,
        full_data: data,
        timestamp: result.timestamp
      };

      // Categorize data
      if (category === 'market_overview') {
        processedData.market_summary.push(processedItem);
      } else if (category.includes('company') || this.companySymbols.some(symbol =>
        data.toLowerCase().includes(symbol.toLowerCase()))) {
        processedData.key_metrics.push(processedItem);
      }

      // Generate alerts for significant movements
      const alertKeywords = ['surge', 'plunge', 'crash', 'rally', 'volatile', 'breaking'];
      if (alertKeywords.some(keyword => data.toLowerCase().includes(keyword))) {
        processedData.alerts.push({
          level: 'HIGH',
          message: processedItem.summary,
          category: category,
          timestamp: result.timestamp
        });
      }
    }

    return processedData;

}

async saveToDashboard(processedData) {
console.log("📊 Updating dashboard in Google Sheets...");

    const timestamp = new Date().toLocaleString();

    // Market Summary Sheet
    const marketData = [];
    marketData.push(["Timestamp", "Category", "Query", "Sentiment", "Summary"]);

    for (const item of processedData.market_summary) {
      marketData.push([
        timestamp,
        item.category,
        item.query,
        item.sentiment,
        item.summary
      ]);
    }

    // Key Metrics Sheet
    const metricsData = [];
    metricsData.push(["Timestamp", "Category", "Sentiment", "Summary", "Alert_Level"]);

    for (const item of processedData.key_metrics) {
      const alertLevel = processedData.alerts.some(alert =>
        alert.message.includes(item.summary)) ? "HIGH" : "NORMAL";
      metricsData.push([
        timestamp,
        item.category,
        item.sentiment,
        item.summary,
        alertLevel
      ]);
    }

    // Update sheets
    await this.updateSheet("Market_Summary!A:E", marketData);
    await this.updateSheet("Key_Metrics!A:E", metricsData);

    // Update Alerts Sheet if needed
    if (processedData.alerts.length > 0) {
      const alertsData = [];
      alertsData.push(["Timestamp", "Level", "Category", "Message"]);

      for (const alert of processedData.alerts) {
        alertsData.push([
          timestamp,
          alert.level,
          alert.category,
          alert.message
        ]);
      }

      await this.updateSheet("Alerts!A:D", alertsData);
    }

}

async updateSheet(rangeName, data) {
const url = `${this.baseUrl}/v1/integrations/google_sheets/execute`;

    const requestData = {
      user_id: this.userId,
      feature_name: "sheets_update_range",
      inputs: {
        spreadsheet_id: this.sheetId,
        range: rangeName,
        values: data
      }
    };

    try {
      const response = await axios.post(url, requestData, { headers: this.headers });
      if (response.status === 200) {
        console.log(`✅ Updated ${rangeName}`);
        return true;
      } else {
        console.log(`❌ Failed to update ${rangeName}: ${response.data}`);
        return false;
      }
    } catch (error) {
      console.log(`❌ Sheet update error: ${error.message}`);
      return false;
    }

}

generateExecutiveSummary(processedData) {
console.log("📝 Generating executive summary...");

    const timestamp = new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    });

    // Count sentiments
    const allItems = [...processedData.market_summary, ...processedData.key_metrics];
    const totalItems = allItems.length;
    const positiveCount = allItems.filter(item => item.sentiment === 'POSITIVE').length;
    const negativeCount = allItems.filter(item => item.sentiment === 'NEGATIVE').length;

    const marketSentiment = positiveCount > negativeCount ? "BULLISH" :
                           negativeCount > positiveCount ? "BEARISH" : "MIXED";

    let summary = `

📊 **Financial Dashboard Report**
📅 Generated: ${timestamp}

## 🎯 Executive Summary

**Market Sentiment**: ${marketSentiment}
**Data Points Analyzed**: ${totalItems}
**Positive Signals**: ${positiveCount}
**Negative Signals**: ${negativeCount}
**Active Alerts**: ${processedData.alerts.length}

## 📈 Market Overview

`;

    // Add market summary highlights
    for (const item of processedData.market_summary.slice(0, 3)) {
      summary += `• **${item.sentiment}**: ${item.summary}\n`;
    }

    summary += "\n## 🏢 Company Analysis\n\n";

    // Add key metrics highlights
    for (const item of processedData.key_metrics.slice(0, 3)) {
      summary += `• **${item.sentiment}**: ${item.summary}\n`;
    }

    // Add alerts if any
    if (processedData.alerts.length > 0) {
      summary += "\n## 🚨 Important Alerts\n\n";
      for (const alert of processedData.alerts) {
        summary += `• **${alert.level}**: ${alert.message}\n`;
      }
    }

    summary += `

## 📊 Detailed Analysis

For comprehensive data and charts, view the full dashboard:
[Financial Dashboard](https://docs.google.com/spreadsheets/d/${this.sheetId})

### 📋 Key Actions Recommended

• Monitor high-alert items closely
• Review portfolio allocation based on sector trends
• Consider market sentiment in upcoming decisions
• Schedule follow-up analysis if volatility increases

---

🤖 **Generated by Incredible Financial Dashboard Agent**
_This report combines real-time financial research with automated analysis_
`;

    return summary;

}

async sendFinancialReport(summary) {
console.log("📧 Sending financial report...");

    const subject = `Financial Dashboard Report - ${new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })}`;

    for (const recipient of this.recipients) {
      if (!recipient.trim()) continue;

      const url = `${this.baseUrl}/v1/integrations/gmail/execute`;

      const data = {
        user_id: this.userId,
        feature_name: "GMAIL_SEND_EMAIL",
        inputs: {
          to: recipient.trim(),
          subject: subject,
          body: summary
        }
      };

      try {
        const response = await axios.post(url, data, { headers: this.headers });
        if (response.status === 200) {
          console.log(`✅ Report sent to ${recipient.trim()}`);
        } else {
          console.log(`❌ Failed to send to ${recipient.trim()}: ${response.data}`);
        }
      } catch (error) {
        console.log(`❌ Email error for ${recipient.trim()}: ${error.message}`);
      }
    }

}

async runDailyAnalysis() {
console.log("🚀 Starting Daily Financial Analysis");
console.log(`📊 Dashboard Sheet: ${this.sheetId}`);
console.log(`📧 Report Recipients: ${this.recipients.join(', ')}`);
console.log(`📈 Tracking: ${this.companySymbols.join(', ')}`);
console.log();

    const allResearch = [];

    // Research different categories
    const categories = ["market_overview", "company_analysis", "sector_trends", "economic_indicators"];

    for (const category of categories) {
      const researchResults = await this.researchFinancialData(category);
      allResearch.push(...researchResults);
    }

    if (allResearch.length === 0) {
      console.log("❌ No financial data collected");
      return false;
    }

    // Process the data
    const processedData = this.processFinancialData(allResearch);

    // Update dashboard
    const dashboardUpdated = await this.saveToDashboard(processedData);

    // Generate and send report
    const summary = this.generateExecutiveSummary(processedData);
    await this.sendFinancialReport(summary);

    // Results summary
    console.log(`\n🎉 Financial Analysis Complete!`);
    console.log(`📊 Data points collected: ${allResearch.length}`);
    console.log(`🚨 Alerts generated: ${processedData.alerts.length}`);
    console.log(`${dashboardUpdated ? '✅' : '❌'} Dashboard updated`);
    console.log(`📧 Reports sent to ${this.recipients.filter(r => r.trim()).length} recipients`);
    console.log(`📊 View dashboard: https://docs.google.com/spreadsheets/d/${this.sheetId}`);

    return true;

}
}

// Usage Examples
async function main() {
const dashboard = new FinancialDashboard();

// Run complete daily analysis
await dashboard.runDailyAnalysis();

console.log("\n" + "=".repeat(50) + "\n");

// Run specific category analysis
const results = await dashboard.researchFinancialData("market_overview");
const processed = dashboard.processFinancialData(results);
const summary = dashboard.generateExecutiveSummary(processed);
console.log("📊 Market Overview Analysis:");
console.log(summary);
}

if (require.main === module) {
main().catch(console.error);
}

module.exports = FinancialDashboard;</code></pre>

  </div>
</div>

## 🎯 **Usage Examples**

### Daily Market Monitoring

```bash
# Run every morning before market open
python financial_dashboard.py --analysis daily
```

### Custom Research Focus

```bash
# Focus on specific sectors or companies
node financialDashboard.js --symbols "TSLA,NVDA,META" --sectors "technology,automotive"
```

### Executive Briefing

```bash
# Generate executive summary only
python financial_dashboard.py --report-only --recipients "ceo@company.com"
```

## 📊 **Expected Output**

```
🚀 Starting Daily Financial Analysis
📊 Dashboard Sheet: 1BcD3FgHiJkLmNoPqRsTuVwXyZ
📧 Report Recipients: cfo@company.com, finance-team@company.com
📈 Tracking: AAPL, GOOGL, MSFT, TSLA

💰 Researching market_overview...
💰 Researching company_analysis...
💰 Researching sector_trends...
💰 Researching economic_indicators...

📊 Processing financial data...
📊 Updating dashboard in Google Sheets...
✅ Updated Market_Summary!A:E
✅ Updated Key_Metrics!A:E
✅ Updated Alerts!A:D

📝 Generating executive summary...
📧 Sending financial report...
✅ Report sent to cfo@company.com
✅ Report sent to finance-team@company.com

🎉 Financial Analysis Complete!
📊 Data points collected: 12
🚨 Alerts generated: 2
✅ Dashboard updated
📧 Reports sent to 2 recipients
📊 View dashboard: https://docs.google.com/spreadsheets/d/1BcD3FgHiJkLmNoPqRsTuVwXyZ
```

## 🔧 **Customization Options**

### Research Focus Areas

- **📈 Market Indices**: S&P 500, NASDAQ, Dow Jones tracking
- **🏢 Company Portfolio**: Custom stock symbol monitoring
- **🏭 Sector Analysis**: Industry-specific trend analysis
- **🌍 Global Markets**: International market coverage

### Dashboard Layouts

- **📊 Executive View**: High-level summaries and alerts
- **📈 Detailed Analytics**: Comprehensive data tables
- **🚨 Risk Monitor**: Volatility and risk indicators
- **📱 Mobile Dashboard**: Simplified mobile-friendly view

### Alert System

- **🚨 Volatility Alerts**: Unusual market movements
- **📈 Performance Alerts**: Significant gains/losses
- **📰 News Alerts**: Breaking financial news
- **💰 Threshold Alerts**: Custom price/volume triggers

## 🛡 **Best Practices**

1. **⏰ Timing**: Run before market open and after close
2. **📊 Data Quality**: Validate research sources and accuracy
3. **🔒 Security**: Protect financial data and API access
4. **📱 Accessibility**: Ensure reports work on all devices

## 🚀 **Advanced Features**

### Predictive Analytics

- **🤖 AI Trend Analysis**: Pattern recognition in financial data
- **📊 Correlation Analysis**: Cross-market relationship tracking
- **📈 Performance Forecasting**: ML-based predictions

### Integration Enhancements

- **💬 Slack Alerts**: Real-time notifications to trading channels
- **📱 Mobile Push**: Critical alerts via mobile notifications
- **🔔 Calendar Integration**: Automated briefing schedule

---

_This financial dashboard keeps your team informed with real-time market insights, automated analysis, and actionable intelligence delivered when you need it._
