# Research Reporter Agent

An intelligent agent that conducts web research, compiles findings in Google Sheets, and delivers summaries via email.

## 📋 **Workflow Overview**

```
🔍 Perplexity → 📊 Google Sheets → 📧 Gmail
  Research        Compile         Deliver
```

**Apps Used:** Perplexity + Google Sheets + Gmail (3 apps total)

## 🎯 **What This Agent Does**

1. **🔍 Research**: Uses Perplexity AI to research any topic with multiple queries
2. **📊 Compile**: Organizes findings in a structured Google Sheet
3. **📧 Deliver**: Sends a professional research summary via Gmail

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

# Integration IDs
PERPLEXITY_API_KEY=pplx-your-api-key
RESEARCH_SHEET_ID=your_google_sheet_id_for_research

# Email Settings
RECIPIENT_EMAIL=research-team@yourcompany.com
```

## 💻 **Implementation**

<div class="code-tabs" data-section="research-reporter">
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
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class ResearchReporter:
def **init**(self):
self.api_key = os.getenv('INCREDIBLE_API_KEY')
self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
self.user_id = os.getenv('USER_ID')
self.sheet_id = os.getenv('RESEARCH_SHEET_ID')
self.recipient_email = os.getenv('RECIPIENT_EMAIL')

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def research_topic(self, topic, research_queries):
        """Conduct comprehensive research using Perplexity AI"""
        print(f"🔍 Researching: {topic}")

        research_data = []

        for i, query in enumerate(research_queries, 1):
            print(f"   {i}. {query}")

            # Define Perplexity search function
            perplexity_function = {
                "name": "perplexity_search",
                "description": "Search the web using Perplexity AI",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "focus": {"type": "string", "description": "Research focus area"}
                    },
                    "required": ["query"]
                }
            }

            # Create chat completion request
            data = {
                "model": "incredible-agent",
                "user_id": self.user_id,
                "messages": [
                    {
                        "role": "user",
                        "content": f"Research this query thoroughly: {query}"
                    }
                ],
                "functions": [perplexity_function],
                "stream": False
            }

            try:
                response = requests.post(
                    f"{self.base_url}/v1/chat-completion",
                    headers=self.headers,
                    json=data
                )

                if response.status_code == 200:
                    result = response.json()

                    # Process function calling results
                    if 'result' in result and 'response' in result['result']:
                        for item in result['result']['response']:
                            if item['type'] == 'function_call':
                                # Execute the search
                                search_result = self.execute_perplexity_search(
                                    item['function_call']['arguments']['query']
                                )

                                research_data.append({
                                    'query': query,
                                    'findings': search_result,
                                    'timestamp': datetime.now().isoformat()
                                })

            except Exception as e:
                print(f"❌ Research error for '{query}': {e}")
                research_data.append({
                    'query': query,
                    'findings': f"Research failed: {str(e)}",
                    'timestamp': datetime.now().isoformat()
                })

        return research_data

    def execute_perplexity_search(self, query):
        """Execute Perplexity search integration"""
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
                return result.get('result', {}).get('answer', 'No results found')
            else:
                return f"Search failed: {response.text}"
        except Exception as e:
            return f"Search error: {str(e)}"

    def save_to_sheets(self, topic, research_data):
        """Save research findings to Google Sheets"""
        print(f"📊 Saving research to Google Sheets...")

        # Prepare data for sheets
        sheet_data = []

        # Add header if first entry
        sheet_data.append([
            "Timestamp",
            "Topic",
            "Query",
            "Findings",
            "Research Date"
        ])

        # Add research data
        for item in research_data:
            sheet_data.append([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                topic,
                item['query'],
                item['findings'][:500] + "..." if len(item['findings']) > 500 else item['findings'],
                item['timestamp']
            ])

        # Execute Google Sheets integration
        url = f"{self.base_url}/v1/integrations/google_sheets/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "sheets_append_data",
            "inputs": {
                "spreadsheet_id": self.sheet_id,
                "range": "Research!A:E",
                "values": sheet_data
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                print("✅ Research saved to Google Sheets")
                return True
            else:
                print(f"❌ Failed to save to sheets: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Sheets error: {e}")
            return False

    def compile_summary(self, topic, research_data):
        """Create a comprehensive research summary"""
        summary = f"""

📋 **Research Report: {topic}**
📅 Date: {datetime.now().strftime("%B %d, %Y")}
🔍 Queries Researched: {len(research_data)}

## 🎯 Key Findings:

"""

        for i, item in enumerate(research_data, 1):
            summary += f"""

### {i}. {item['query']}

{item['findings'][:300]}{'...' if len(item['findings']) > 300 else ''}

---

"""

        summary += f"""

## 📊 Research Data

Full detailed findings have been saved to:
[Google Sheet](https://docs.google.com/spreadsheets/d/{self.sheet_id})

## 🤖 Generated by Incredible Research Agent

This report was automatically generated using AI research and data compilation.
"""

        return summary

    def send_email_summary(self, topic, summary):
        """Send research summary via Gmail"""
        print(f"📧 Sending research summary...")

        email_subject = f"Research Report: {topic} - {datetime.now().strftime('%B %d, %Y')}"

        # Execute Gmail integration
        url = f"{self.base_url}/v1/integrations/gmail/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "GMAIL_SEND_EMAIL",
            "inputs": {
                "to": self.recipient_email,
                "subject": email_subject,
                "body": summary
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                print(f"✅ Research summary sent to {self.recipient_email}")
                return True
            else:
                print(f"❌ Failed to send email: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Email error: {e}")
            return False

    def run_research_workflow(self, topic, research_queries):
        """Execute the complete research workflow"""
        print(f"🚀 Starting Research Workflow for: {topic}")
        print(f"📊 Target Sheet: {self.sheet_id}")
        print(f"📧 Will send summary to: {self.recipient_email}")
        print()

        # Step 1: Conduct research
        research_data = self.research_topic(topic, research_queries)

        if not research_data:
            print("❌ No research data collected")
            return False

        # Step 2: Save to sheets
        if not self.save_to_sheets(topic, research_data):
            print("⚠️  Failed to save to sheets, but continuing...")

        # Step 3: Compile summary
        summary = self.compile_summary(topic, research_data)

        # Step 4: Send email
        email_sent = self.send_email_summary(topic, summary)

        print(f"\n🎉 Research Workflow Complete!")
        print(f"✅ Research conducted: {len(research_data)} queries")
        print(f"{'✅' if email_sent else '❌'} Email summary sent")
        print(f"📊 View full data: https://docs.google.com/spreadsheets/d/{self.sheet_id}")

        return True

# Usage Examples

if **name** == "**main**":
reporter = ResearchReporter()

    # Example 1: Technology Research
    reporter.run_research_workflow(
        topic="AI in Healthcare 2024",
        research_queries=[
            "latest AI applications in healthcare diagnosis 2024",
            "AI medical imaging breakthroughs 2024",
            "regulatory challenges for AI in healthcare",
            "AI healthcare startups funding 2024"
        ]
    )

    print("\n" + "="*50 + "\n")

    # Example 2: Market Research
    reporter.run_research_workflow(
        topic="Remote Work Tools Market",
        research_queries=[
            "top remote work collaboration tools 2024",
            "remote work productivity statistics",
            "enterprise remote work software trends"
        ]
    )</code></pre>

  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">const axios = require("axios");
require("dotenv").config();

class ResearchReporter {
constructor() {
this.apiKey = process.env.INCREDIBLE_API_KEY;
this.baseUrl = process.env.INCREDIBLE_BASE_URL || "https://api.incredible.one";
this.userId = process.env.USER_ID;
this.sheetId = process.env.RESEARCH_SHEET_ID;
this.recipientEmail = process.env.RECIPIENT_EMAIL;

    this.headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${this.apiKey}`,
    };

}

async researchTopic(topic, researchQueries) {
console.log(`🔍 Researching: ${topic}`);

    const researchData = [];

    for (let i = 0; i < researchQueries.length; i++) {
      const query = researchQueries[i];
      console.log(`   ${i + 1}. ${query}`);

      const perplexityFunction = {
        name: "perplexity_search",
        description: "Search the web using Perplexity AI",
        parameters: {
          type: "object",
          properties: {
            query: { type: "string", description: "Search query" },
            focus: { type: "string", description: "Research focus area" }
          },
          required: ["query"]
        }
      };

      const data = {
        model: "incredible-agent",
        user_id: this.userId,
        messages: [
          {
            role: "user",
            content: `Research this query thoroughly: ${query}`
          }
        ],
        functions: [perplexityFunction],
        stream: false
      };

      try {
        const response = await axios.post(
          `${this.baseUrl}/v1/chat-completion`,
          data,
          { headers: this.headers }
        );

        if (response.status === 200) {
          const result = response.data;

          if (result.result && result.result.response) {
            for (const item of result.result.response) {
              if (item.type === 'function_call') {
                const searchResult = await this.executePerplexitySearch(
                  item.function_call.arguments.query
                );

                researchData.push({
                  query: query,
                  findings: searchResult,
                  timestamp: new Date().toISOString()
                });
              }
            }
          }
        }
      } catch (error) {
        console.log(`❌ Research error for '${query}': ${error.message}`);
        researchData.push({
          query: query,
          findings: `Research failed: ${error.message}`,
          timestamp: new Date().toISOString()
        });
      }
    }

    return researchData;

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
        return response.data.result?.answer || 'No results found';
      } else {
        return `Search failed: ${response.data}`;
      }
    } catch (error) {
      return `Search error: ${error.message}`;
    }

}

async saveToSheets(topic, researchData) {
console.log(`📊 Saving research to Google Sheets...`);

    const sheetData = [];

    // Add header
    sheetData.push([
      "Timestamp",
      "Topic",
      "Query",
      "Findings",
      "Research Date"
    ]);

    // Add research data
    for (const item of researchData) {
      sheetData.push([
        new Date().toLocaleString(),
        topic,
        item.query,
        item.findings.length > 500 ? item.findings.substring(0, 500) + "..." : item.findings,
        item.timestamp
      ]);
    }

    const url = `${this.baseUrl}/v1/integrations/google_sheets/execute`;

    const data = {
      user_id: this.userId,
      feature_name: "sheets_append_data",
      inputs: {
        spreadsheet_id: this.sheetId,
        range: "Research!A:E",
        values: sheetData
      }
    };

    try {
      const response = await axios.post(url, data, { headers: this.headers });
      if (response.status === 200) {
        console.log("✅ Research saved to Google Sheets");
        return true;
      } else {
        console.log(`❌ Failed to save to sheets: ${response.data}`);
        return false;
      }
    } catch (error) {
      console.log(`❌ Sheets error: ${error.message}`);
      return false;
    }

}

compileSummary(topic, researchData) {
const now = new Date();
let summary = `
📋 **Research Report: ${topic}**
📅 Date: ${now.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
🔍 Queries Researched: ${researchData.length}

## 🎯 Key Findings:

`;

    researchData.forEach((item, index) => {
      const truncatedFindings = item.findings.length > 300
        ? item.findings.substring(0, 300) + '...'
        : item.findings;

      summary += `

### ${index + 1}. ${item.query}

${truncatedFindings}

---

`;
});

    summary += `

## 📊 Research Data

Full detailed findings have been saved to:
[Google Sheet](https://docs.google.com/spreadsheets/d/${this.sheetId})

## 🤖 Generated by Incredible Research Agent

This report was automatically generated using AI research and data compilation.
`;

    return summary;

}

async sendEmailSummary(topic, summary) {
console.log(`📧 Sending research summary...`);

    const now = new Date();
    const emailSubject = `Research Report: ${topic} - ${now.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}`;

    const url = `${this.baseUrl}/v1/integrations/gmail/execute`;

    const data = {
      user_id: this.userId,
      feature_name: "GMAIL_SEND_EMAIL",
      inputs: {
        to: this.recipientEmail,
        subject: emailSubject,
        body: summary
      }
    };

    try {
      const response = await axios.post(url, data, { headers: this.headers });
      if (response.status === 200) {
        console.log(`✅ Research summary sent to ${this.recipientEmail}`);
        return true;
      } else {
        console.log(`❌ Failed to send email: ${response.data}`);
        return false;
      }
    } catch (error) {
      console.log(`❌ Email error: ${error.message}`);
      return false;
    }

}

async runResearchWorkflow(topic, researchQueries) {
console.log(`🚀 Starting Research Workflow for: ${topic}`);
console.log(`📊 Target Sheet: ${this.sheetId}`);
console.log(`📧 Will send summary to: ${this.recipientEmail}`);
console.log();

    // Step 1: Conduct research
    const researchData = await this.researchTopic(topic, researchQueries);

    if (researchData.length === 0) {
      console.log("❌ No research data collected");
      return false;
    }

    // Step 2: Save to sheets
    const sheetsSaved = await this.saveToSheets(topic, researchData);
    if (!sheetsSaved) {
      console.log("⚠️  Failed to save to sheets, but continuing...");
    }

    // Step 3: Compile summary
    const summary = this.compileSummary(topic, researchData);

    // Step 4: Send email
    const emailSent = await this.sendEmailSummary(topic, summary);

    console.log(`\n🎉 Research Workflow Complete!`);
    console.log(`✅ Research conducted: ${researchData.length} queries`);
    console.log(`${emailSent ? '✅' : '❌'} Email summary sent`);
    console.log(`📊 View full data: https://docs.google.com/spreadsheets/d/${this.sheetId}`);

    return true;

}
}

// Usage Examples
async function main() {
const reporter = new ResearchReporter();

// Example 1: Technology Research
await reporter.runResearchWorkflow(
"AI in Healthcare 2024",
[
"latest AI applications in healthcare diagnosis 2024",
"AI medical imaging breakthroughs 2024",
"regulatory challenges for AI in healthcare",
"AI healthcare startups funding 2024"
]
);

console.log("\n" + "=".repeat(50) + "\n");

// Example 2: Market Research
await reporter.runResearchWorkflow(
"Remote Work Tools Market",
[
"top remote work collaboration tools 2024",
"remote work productivity statistics",
"enterprise remote work software trends"
]
);
}

if (require.main === module) {
main().catch(console.error);
}

module.exports = ResearchReporter;</code></pre>

  </div>
</div>

## 🎯 **Usage Examples**

### Daily Market Research

```bash
# Monitor competitor activity
python research_reporter.py --topic "Competitor Analysis" --queries "Company X product updates, Company Y funding news"
```

### Technology Trends

```bash
# Stay updated on tech trends
node researchReporter.js --topic "AI Tools 2024" --queries "new AI productivity tools, AI automation trends"
```

## 📊 **Expected Output**

```
🚀 Starting Research Workflow for: AI in Healthcare 2024
📊 Target Sheet: 1BcD3FgHiJkLmNoPqRsTuVwXyZ
📧 Will send summary to: research-team@company.com

🔍 Researching: AI in Healthcare 2024
   1. latest AI applications in healthcare diagnosis 2024
   2. AI medical imaging breakthroughs 2024
   3. regulatory challenges for AI in healthcare
   4. AI healthcare startups funding 2024

📊 Saving research to Google Sheets...
✅ Research saved to Google Sheets

📧 Sending research summary...
✅ Research summary sent to research-team@company.com

🎉 Research Workflow Complete!
✅ Research conducted: 4 queries
✅ Email summary sent
📊 View full data: https://docs.google.com/spreadsheets/d/1BcD3FgHiJkLmNoPqRsTuVwXyZ
```

## 🔧 **Customization Options**

### Research Topics

- **🏥 Healthcare AI**: Latest medical AI developments
- **💰 FinTech**: Financial technology trends
- **🚀 Startups**: Emerging company analysis
- **🏭 Industry**: Sector-specific research

### Output Formats

- **📊 Detailed Sheets**: Full research data with citations
- **📧 Executive Summary**: Key points for leadership
- **📱 Slack Notifications**: Quick updates for teams

## 🛡 **Best Practices**

1. **📝 Query Design**: Use specific, focused research questions
2. **⏰ Scheduling**: Run daily/weekly for ongoing monitoring
3. **📊 Data Organization**: Use consistent sheet structures
4. **🔒 Access Control**: Secure API keys and sheet permissions

---

_This research agent automatically keeps your team informed with the latest information on any topic, compiled and delivered professionally._
