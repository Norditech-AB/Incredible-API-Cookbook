# Business Intelligence Agent

An intelligent agent that aggregates business data from multiple sources, analyzes trends, and delivers actionable insights via automated reports.

## 📋 **Workflow Overview**

```
🔍 Perplexity → 📊 Google Sheets → 📧 Gmail
   Data Collection   Analysis      Reports
```

**Apps Used:** Perplexity + Google Sheets + Gmail (3 apps total)

## 🎯 **What This Agent Does**

1. **🔍 Collect**: Gathers business intelligence from multiple data sources
2. **📊 Analyze**: Processes data and identifies key trends and insights
3. **📧 Report**: Delivers executive dashboards and detailed analysis reports

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

# Business Intelligence Settings
BI_DASHBOARD_SHEET_ID=your_google_sheet_id
BI_REPORT_RECIPIENTS=ceo@company.com,coo@company.com,strategy@company.com

# Analysis Parameters
COMPANY_NAME=Your Company Name
INDUSTRY_SECTOR=technology  # or finance, healthcare, etc.
COMPETITOR_COMPANIES=Company A,Company B,Company C
```

## 💻 **Implementation**

<div class="code-tabs" data-section="business-intelligence">
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

class BusinessIntelligence:
def **init**(self):
self.api_key = os.getenv('INCREDIBLE_API_KEY')
self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
self.user_id = os.getenv('USER_ID')
self.dashboard_sheet_id = os.getenv('BI_DASHBOARD_SHEET_ID')
self.recipients = os.getenv('BI_REPORT_RECIPIENTS', '').split(',')

        self.company_name = os.getenv('COMPANY_NAME', 'Your Company')
        self.industry_sector = os.getenv('INDUSTRY_SECTOR', 'technology')
        self.competitors = os.getenv('COMPETITOR_COMPANIES', '').split(',')

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def collect_market_intelligence(self):
        """Collect market and industry intelligence"""
        print("🔍 Collecting market intelligence...")

        intelligence_queries = [
            f"{self.industry_sector} industry trends 2024 market analysis",
            f"{self.industry_sector} market size growth projections revenue",
            f"emerging technologies {self.industry_sector} industry disruption",
            f"{self.industry_sector} investment funding venture capital trends",
            f"regulatory changes {self.industry_sector} industry compliance"
        ]

        market_data = []

        for query in intelligence_queries:
            result = self.execute_perplexity_search(query)
            market_data.append({
                'category': 'market_intelligence',
                'query': query,
                'data': result,
                'timestamp': datetime.now().isoformat()
            })

        return market_data

    def collect_competitor_analysis(self):
        """Analyze competitor performance and strategies"""
        print("🏢 Analyzing competitor landscape...")

        competitor_data = []

        for competitor in self.competitors:
            if not competitor.strip():
                continue

            competitor_queries = [
                f"{competitor.strip()} company financial performance revenue 2024",
                f"{competitor.strip()} product launches new features strategy",
                f"{competitor.strip()} market share customer base growth",
                f"{competitor.strip()} funding investment valuation news",
                f"{competitor.strip()} partnerships acquisitions deals"
            ]

            for query in competitor_queries:
                result = self.execute_perplexity_search(query)
                competitor_data.append({
                    'category': 'competitor_analysis',
                    'company': competitor.strip(),
                    'query': query,
                    'data': result,
                    'timestamp': datetime.now().isoformat()
                })

        return competitor_data

    def collect_business_trends(self):
        """Research general business and economic trends"""
        print("📈 Researching business trends...")

        trend_queries = [
            "business strategy trends 2024 digital transformation",
            "economic indicators inflation interest rates business impact",
            "consumer behavior changes spending patterns 2024",
            "supply chain trends logistics disruption recovery",
            "workforce trends remote work productivity technology"
        ]

        trend_data = []

        for query in trend_queries:
            result = self.execute_perplexity_search(query)
            trend_data.append({
                'category': 'business_trends',
                'query': query,
                'data': result,
                'timestamp': datetime.now().isoformat()
            })

        return trend_data

    def execute_perplexity_search(self, query):
        """Execute Perplexity search for business intelligence"""
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

    def analyze_intelligence_data(self, all_data):
        """Analyze collected intelligence data for insights"""
        print("📊 Analyzing intelligence data...")

        analysis = {
            'market_insights': [],
            'competitive_threats': [],
            'opportunities': [],
            'risks': [],
            'strategic_recommendations': []
        }

        for item in all_data:
            data_text = item['data'].lower()

            # Market insights analysis
            if item['category'] == 'market_intelligence':
                if 'growth' in data_text or 'increase' in data_text:
                    analysis['market_insights'].append({
                        'type': 'growth_opportunity',
                        'description': item['data'][:200] + '...',
                        'source_query': item['query'],
                        'impact': 'positive'
                    })
                elif 'decline' in data_text or 'decrease' in data_text:
                    analysis['risks'].append({
                        'type': 'market_risk',
                        'description': item['data'][:200] + '...',
                        'source_query': item['query'],
                        'severity': 'medium'
                    })

            # Competitor analysis
            elif item['category'] == 'competitor_analysis':
                if 'funding' in data_text or 'investment' in data_text:
                    analysis['competitive_threats'].append({
                        'competitor': item.get('company', 'Unknown'),
                        'threat_type': 'funding_advantage',
                        'description': item['data'][:200] + '...',
                        'urgency': 'high'
                    })
                elif 'product launch' in data_text or 'new feature' in data_text:
                    analysis['competitive_threats'].append({
                        'competitor': item.get('company', 'Unknown'),
                        'threat_type': 'product_innovation',
                        'description': item['data'][:200] + '...',
                        'urgency': 'medium'
                    })

            # Business trends analysis
            elif item['category'] == 'business_trends':
                if 'opportunity' in data_text or 'emerging' in data_text:
                    analysis['opportunities'].append({
                        'type': 'market_opportunity',
                        'description': item['data'][:200] + '...',
                        'source_query': item['query'],
                        'potential': 'high'
                    })

        # Generate strategic recommendations
        analysis['strategic_recommendations'] = self.generate_recommendations(analysis)

        return analysis

    def generate_recommendations(self, analysis):
        """Generate strategic recommendations based on analysis"""
        recommendations = []

        if len(analysis['opportunities']) > 0:
            recommendations.append({
                'category': 'growth_strategy',
                'priority': 'high',
                'recommendation': f"Capitalize on {len(analysis['opportunities'])} identified market opportunities",
                'action_items': [
                    'Conduct detailed feasibility analysis',
                    'Develop go-to-market strategy',
                    'Allocate resources for opportunity pursuit'
                ]
            })

        if len(analysis['competitive_threats']) > 2:
            recommendations.append({
                'category': 'competitive_response',
                'priority': 'high',
                'recommendation': f"Address {len(analysis['competitive_threats'])} competitive threats",
                'action_items': [
                    'Enhance product differentiation',
                    'Accelerate innovation timeline',
                    'Strengthen customer relationships'
                ]
            })

        if len(analysis['risks']) > 0:
            recommendations.append({
                'category': 'risk_mitigation',
                'priority': 'medium',
                'recommendation': f"Mitigate {len(analysis['risks'])} identified market risks",
                'action_items': [
                    'Develop contingency plans',
                    'Diversify market exposure',
                    'Monitor risk indicators'
                ]
            })

        return recommendations

    def save_to_dashboard(self, analysis_data, raw_data):
        """Save analysis to Google Sheets dashboard"""
        print("📊 Updating BI dashboard...")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Market Insights Sheet
        insights_data = []
        insights_data.append(["Timestamp", "Type", "Description", "Impact", "Source"])

        for insight in analysis_data['market_insights']:
            insights_data.append([
                timestamp,
                insight['type'],
                insight['description'],
                insight['impact'],
                insight['source_query']
            ])

        # Competitive Threats Sheet
        threats_data = []
        threats_data.append(["Timestamp", "Competitor", "Threat Type", "Description", "Urgency"])

        for threat in analysis_data['competitive_threats']:
            threats_data.append([
                timestamp,
                threat['competitor'],
                threat['threat_type'],
                threat['description'],
                threat['urgency']
            ])

        # Opportunities Sheet
        opportunities_data = []
        opportunities_data.append(["Timestamp", "Type", "Description", "Potential", "Source"])

        for opp in analysis_data['opportunities']:
            opportunities_data.append([
                timestamp,
                opp['type'],
                opp['description'],
                opp['potential'],
                opp['source_query']
            ])

        # Update sheets
        self.update_sheet("Market_Insights!A:E", insights_data)
        self.update_sheet("Competitive_Threats!A:E", threats_data)
        self.update_sheet("Opportunities!A:E", opportunities_data)

    def update_sheet(self, range_name, data):
        """Update specific sheet range with data"""
        url = f"{self.base_url}/v1/integrations/google_sheets/execute"

        request_data = {
            "user_id": self.user_id,
            "feature_name": "sheets_update_range",
            "inputs": {
                "spreadsheet_id": self.dashboard_sheet_id,
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

    def generate_executive_report(self, analysis_data):
        """Generate executive summary report"""
        print("📝 Generating executive report...")

        timestamp = datetime.now().strftime("%B %d, %Y")

        # Calculate summary metrics
        total_insights = len(analysis_data['market_insights'])
        total_threats = len(analysis_data['competitive_threats'])
        total_opportunities = len(analysis_data['opportunities'])
        total_risks = len(analysis_data['risks'])

        high_priority_recommendations = [r for r in analysis_data['strategic_recommendations']
                                       if r['priority'] == 'high']

        report = f"""

📊 **Business Intelligence Report**
📅 Date: {timestamp}
🏢 Company: {self.company_name}
🏭 Industry: {self.industry_sector.title()}

## 🎯 Executive Summary

**Intelligence Overview:**
• Market Insights: {total_insights}
• Competitive Threats: {total_threats}
• Business Opportunities: {total_opportunities}
• Risk Factors: {total_risks}
• High-Priority Recommendations: {len(high_priority_recommendations)}

## 📈 Market Intelligence

"""

        # Add market insights
        for insight in analysis_data['market_insights'][:3]:
            report += f"• **{insight['type'].replace('_', ' ').title()}**: {insight['description']}\n"

        report += "\n## 🏢 Competitive Landscape\n\n"

        # Add competitive threats
        for threat in analysis_data['competitive_threats'][:3]:
            report += f"• **{threat['competitor']}** - {threat['threat_type'].replace('_', ' ').title()}: {threat['description']}\n"

        report += "\n## 💡 Business Opportunities\n\n"

        # Add opportunities
        for opp in analysis_data['opportunities'][:3]:
            report += f"• **{opp['type'].replace('_', ' ').title()}**: {opp['description']}\n"

        # Add strategic recommendations
        report += "\n## 🎯 Strategic Recommendations\n\n"

        for rec in high_priority_recommendations:
            report += f"### {rec['category'].replace('_', ' ').title()} ({rec['priority'].upper()} Priority)\n"
            report += f"{rec['recommendation']}\n\n"
            report += "**Action Items:**\n"
            for action in rec['action_items']:
                report += f"• {action}\n"
            report += "\n"

        report += f"""

## 📊 Detailed Analysis

For comprehensive data and visualizations, access the full dashboard:
[Business Intelligence Dashboard](https://docs.google.com/spreadsheets/d/{self.dashboard_sheet_id})

### 📋 Next Steps

1. **Immediate Actions** (Next 30 days)
   • Review high-priority recommendations
   • Assign ownership for action items
   • Develop detailed implementation plans

2. **Strategic Initiatives** (Next 90 days)
   • Execute opportunity assessment
   • Implement competitive response strategies
   • Monitor risk indicators and market changes

3. **Continuous Monitoring**
   • Weekly competitor intelligence updates
   • Monthly market trend analysis
   • Quarterly strategic review and adjustment

---

🤖 **Generated by Incredible Business Intelligence Agent**
_This report combines real-time market research with competitive analysis and strategic insights_
"""

        return report

    def send_intelligence_report(self, report):
        """Send intelligence report via email"""
        print("📧 Distributing intelligence report...")

        subject = f"Business Intelligence Report - {self.company_name} - {datetime.now().strftime('%B %d, %Y')}"

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
                    "body": report
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

    def run_bi_analysis(self):
        """Execute complete business intelligence workflow"""
        print("🚀 Starting Business Intelligence Analysis")
        print(f"🏢 Company: {self.company_name}")
        print(f"🏭 Industry: {self.industry_sector}")
        print(f"📊 Dashboard: {self.dashboard_sheet_id}")
        print(f"📧 Recipients: {', '.join([r for r in self.recipients if r.strip()])}")
        print()

        # Collect all intelligence data
        market_data = self.collect_market_intelligence()
        competitor_data = self.collect_competitor_analysis()
        trend_data = self.collect_business_trends()

        all_data = market_data + competitor_data + trend_data

        if not all_data:
            print("❌ No intelligence data collected")
            return False

        # Analyze the data
        analysis = self.analyze_intelligence_data(all_data)

        # Save to dashboard
        self.save_to_dashboard(analysis, all_data)

        # Generate and send report
        report = self.generate_executive_report(analysis)
        self.send_intelligence_report(report)

        # Summary
        print(f"\n🎉 Business Intelligence Analysis Complete!")
        print(f"🔍 Data points collected: {len(all_data)}")
        print(f"📈 Market insights: {len(analysis['market_insights'])}")
        print(f"🏢 Competitive threats: {len(analysis['competitive_threats'])}")
        print(f"💡 Opportunities identified: {len(analysis['opportunities'])}")
        print(f"🎯 Strategic recommendations: {len(analysis['strategic_recommendations'])}")
        print(f"📧 Reports distributed: {len([r for r in self.recipients if r.strip()])}")
        print(f"📊 Dashboard: https://docs.google.com/spreadsheets/d/{self.dashboard_sheet_id}")

        return True

# Usage Examples

if **name** == "**main**":
bi_agent = BusinessIntelligence()

    # Run complete BI analysis
    bi_agent.run_bi_analysis()</code></pre>

  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">const axios = require("axios");
require("dotenv").config();

class BusinessIntelligence {
constructor() {
this.apiKey = process.env.INCREDIBLE_API_KEY;
this.baseUrl = process.env.INCREDIBLE_BASE_URL || "https://api.incredible.one";
this.userId = process.env.USER_ID;
this.dashboardSheetId = process.env.BI_DASHBOARD_SHEET_ID;
this.recipients = (process.env.BI_REPORT_RECIPIENTS || '').split(',');

    this.companyName = process.env.COMPANY_NAME || 'Your Company';
    this.industrySector = process.env.INDUSTRY_SECTOR || 'technology';
    this.competitors = (process.env.COMPETITOR_COMPANIES || '').split(',');

    this.headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${this.apiKey}`,
    };

}

async collectMarketIntelligence() {
console.log("🔍 Collecting market intelligence...");

    const intelligenceQueries = [
      `${this.industrySector} industry trends 2024 market analysis`,
      `${this.industrySector} market size growth projections revenue`,
      `emerging technologies ${this.industrySector} industry disruption`,
      `${this.industrySector} investment funding venture capital trends`,
      `regulatory changes ${this.industrySector} industry compliance`
    ];

    const marketData = [];

    for (const query of intelligenceQueries) {
      const result = await this.executePerplexitySearch(query);
      marketData.push({
        category: 'market_intelligence',
        query: query,
        data: result,
        timestamp: new Date().toISOString()
      });
    }

    return marketData;

}

async collectCompetitorAnalysis() {
console.log("🏢 Analyzing competitor landscape...");

    const competitorData = [];

    for (const competitor of this.competitors) {
      if (!competitor.trim()) continue;

      const competitorQueries = [
        `${competitor.trim()} company financial performance revenue 2024`,
        `${competitor.trim()} product launches new features strategy`,
        `${competitor.trim()} market share customer base growth`,
        `${competitor.trim()} funding investment valuation news`,
        `${competitor.trim()} partnerships acquisitions deals`
      ];

      for (const query of competitorQueries) {
        const result = await this.executePerplexitySearch(query);
        competitorData.push({
          category: 'competitor_analysis',
          company: competitor.trim(),
          query: query,
          data: result,
          timestamp: new Date().toISOString()
        });
      }
    }

    return competitorData;

}

async collectBusinessTrends() {
console.log("📈 Researching business trends...");

    const trendQueries = [
      "business strategy trends 2024 digital transformation",
      "economic indicators inflation interest rates business impact",
      "consumer behavior changes spending patterns 2024",
      "supply chain trends logistics disruption recovery",
      "workforce trends remote work productivity technology"
    ];

    const trendData = [];

    for (const query of trendQueries) {
      const result = await this.executePerplexitySearch(query);
      trendData.push({
        category: 'business_trends',
        query: query,
        data: result,
        timestamp: new Date().toISOString()
      });
    }

    return trendData;

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

analyzeIntelligenceData(allData) {
console.log("📊 Analyzing intelligence data...");

    const analysis = {
      market_insights: [],
      competitive_threats: [],
      opportunities: [],
      risks: [],
      strategic_recommendations: []
    };

    for (const item of allData) {
      const dataText = item.data.toLowerCase();

      // Market insights analysis
      if (item.category === 'market_intelligence') {
        if (dataText.includes('growth') || dataText.includes('increase')) {
          analysis.market_insights.push({
            type: 'growth_opportunity',
            description: item.data.substring(0, 200) + '...',
            source_query: item.query,
            impact: 'positive'
          });
        } else if (dataText.includes('decline') || dataText.includes('decrease')) {
          analysis.risks.push({
            type: 'market_risk',
            description: item.data.substring(0, 200) + '...',
            source_query: item.query,
            severity: 'medium'
          });
        }
      }

      // Competitor analysis
      else if (item.category === 'competitor_analysis') {
        if (dataText.includes('funding') || dataText.includes('investment')) {
          analysis.competitive_threats.push({
            competitor: item.company || 'Unknown',
            threat_type: 'funding_advantage',
            description: item.data.substring(0, 200) + '...',
            urgency: 'high'
          });
        } else if (dataText.includes('product launch') || dataText.includes('new feature')) {
          analysis.competitive_threats.push({
            competitor: item.company || 'Unknown',
            threat_type: 'product_innovation',
            description: item.data.substring(0, 200) + '...',
            urgency: 'medium'
          });
        }
      }

      // Business trends analysis
      else if (item.category === 'business_trends') {
        if (dataText.includes('opportunity') || dataText.includes('emerging')) {
          analysis.opportunities.push({
            type: 'market_opportunity',
            description: item.data.substring(0, 200) + '...',
            source_query: item.query,
            potential: 'high'
          });
        }
      }
    }

    // Generate strategic recommendations
    analysis.strategic_recommendations = this.generateRecommendations(analysis);

    return analysis;

}

generateRecommendations(analysis) {
const recommendations = [];

    if (analysis.opportunities.length > 0) {
      recommendations.push({
        category: 'growth_strategy',
        priority: 'high',
        recommendation: `Capitalize on ${analysis.opportunities.length} identified market opportunities`,
        action_items: [
          'Conduct detailed feasibility analysis',
          'Develop go-to-market strategy',
          'Allocate resources for opportunity pursuit'
        ]
      });
    }

    if (analysis.competitive_threats.length > 2) {
      recommendations.push({
        category: 'competitive_response',
        priority: 'high',
        recommendation: `Address ${analysis.competitive_threats.length} competitive threats`,
        action_items: [
          'Enhance product differentiation',
          'Accelerate innovation timeline',
          'Strengthen customer relationships'
        ]
      });
    }

    if (analysis.risks.length > 0) {
      recommendations.push({
        category: 'risk_mitigation',
        priority: 'medium',
        recommendation: `Mitigate ${analysis.risks.length} identified market risks`,
        action_items: [
          'Develop contingency plans',
          'Diversify market exposure',
          'Monitor risk indicators'
        ]
      });
    }

    return recommendations;

}

async saveToDashboard(analysisData, rawData) {
console.log("📊 Updating BI dashboard...");

    const timestamp = new Date().toLocaleString();

    // Market Insights Sheet
    const insightsData = [];
    insightsData.push(["Timestamp", "Type", "Description", "Impact", "Source"]);

    for (const insight of analysisData.market_insights) {
      insightsData.push([
        timestamp,
        insight.type,
        insight.description,
        insight.impact,
        insight.source_query
      ]);
    }

    // Competitive Threats Sheet
    const threatsData = [];
    threatsData.push(["Timestamp", "Competitor", "Threat Type", "Description", "Urgency"]);

    for (const threat of analysisData.competitive_threats) {
      threatsData.push([
        timestamp,
        threat.competitor,
        threat.threat_type,
        threat.description,
        threat.urgency
      ]);
    }

    // Opportunities Sheet
    const opportunitiesData = [];
    opportunitiesData.push(["Timestamp", "Type", "Description", "Potential", "Source"]);

    for (const opp of analysisData.opportunities) {
      opportunitiesData.push([
        timestamp,
        opp.type,
        opp.description,
        opp.potential,
        opp.source_query
      ]);
    }

    // Update sheets
    await this.updateSheet("Market_Insights!A:E", insightsData);
    await this.updateSheet("Competitive_Threats!A:E", threatsData);
    await this.updateSheet("Opportunities!A:E", opportunitiesData);

}

async updateSheet(rangeName, data) {
const url = `${this.baseUrl}/v1/integrations/google_sheets/execute`;

    const requestData = {
      user_id: this.userId,
      feature_name: "sheets_update_range",
      inputs: {
        spreadsheet_id: this.dashboardSheetId,
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

generateExecutiveReport(analysisData) {
console.log("📝 Generating executive report...");

    const timestamp = new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });

    const totalInsights = analysisData.market_insights.length;
    const totalThreats = analysisData.competitive_threats.length;
    const totalOpportunities = analysisData.opportunities.length;
    const totalRisks = analysisData.risks.length;

    const highPriorityRecommendations = analysisData.strategic_recommendations.filter(
      r => r.priority === 'high'
    );

    let report = `

📊 **Business Intelligence Report**
📅 Date: ${timestamp}
🏢 Company: ${this.companyName}
🏭 Industry: ${this.industrySector.charAt(0).toUpperCase() + this.industrySector.slice(1)}

## 🎯 Executive Summary

**Intelligence Overview:**
• Market Insights: ${totalInsights}
• Competitive Threats: ${totalThreats}
• Business Opportunities: ${totalOpportunities}
• Risk Factors: ${totalRisks}
• High-Priority Recommendations: ${highPriorityRecommendations.length}

## 📈 Market Intelligence

`;

    // Add market insights
    for (const insight of analysisData.market_insights.slice(0, 3)) {
      report += `• **${insight.type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}**: ${insight.description}\n`;
    }

    report += "\n## 🏢 Competitive Landscape\n\n";

    // Add competitive threats
    for (const threat of analysisData.competitive_threats.slice(0, 3)) {
      report += `• **${threat.competitor}** - ${threat.threat_type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}: ${threat.description}\n`;
    }

    report += "\n## 💡 Business Opportunities\n\n";

    // Add opportunities
    for (const opp of analysisData.opportunities.slice(0, 3)) {
      report += `• **${opp.type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}**: ${opp.description}\n`;
    }

    // Add strategic recommendations
    report += "\n## 🎯 Strategic Recommendations\n\n";

    for (const rec of highPriorityRecommendations) {
      report += `### ${rec.category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())} (${rec.priority.toUpperCase()} Priority)\n`;
      report += `${rec.recommendation}\n\n`;
      report += "**Action Items:**\n";
      for (const action of rec.action_items) {
        report += `• ${action}\n`;
      }
      report += "\n";
    }

    report += `

## 📊 Detailed Analysis

For comprehensive data and visualizations, access the full dashboard:
[Business Intelligence Dashboard](https://docs.google.com/spreadsheets/d/${this.dashboardSheetId})

### 📋 Next Steps

1. **Immediate Actions** (Next 30 days)
   • Review high-priority recommendations
   • Assign ownership for action items
   • Develop detailed implementation plans

2. **Strategic Initiatives** (Next 90 days)
   • Execute opportunity assessment
   • Implement competitive response strategies
   • Monitor risk indicators and market changes

3. **Continuous Monitoring**
   • Weekly competitor intelligence updates
   • Monthly market trend analysis
   • Quarterly strategic review and adjustment

---

🤖 **Generated by Incredible Business Intelligence Agent**
_This report combines real-time market research with competitive analysis and strategic insights_
`;

    return report;

}

async sendIntelligenceReport(report) {
console.log("📧 Distributing intelligence report...");

    const subject = `Business Intelligence Report - ${this.companyName} - ${new Date().toLocaleDateString('en-US', {
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
          body: report
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

async runBiAnalysis() {
console.log("🚀 Starting Business Intelligence Analysis");
console.log(`🏢 Company: ${this.companyName}`);
console.log(`🏭 Industry: ${this.industrySector}`);
console.log(`📊 Dashboard: ${this.dashboardSheetId}`);
console.log(`📧 Recipients: ${this.recipients.filter(r => r.trim()).join(', ')}`);
console.log();

    // Collect all intelligence data
    const marketData = await this.collectMarketIntelligence();
    const competitorData = await this.collectCompetitorAnalysis();
    const trendData = await this.collectBusinessTrends();

    const allData = [...marketData, ...competitorData, ...trendData];

    if (allData.length === 0) {
      console.log("❌ No intelligence data collected");
      return false;
    }

    // Analyze the data
    const analysis = this.analyzeIntelligenceData(allData);

    // Save to dashboard
    await this.saveToDashboard(analysis, allData);

    // Generate and send report
    const report = this.generateExecutiveReport(analysis);
    await this.sendIntelligenceReport(report);

    // Summary
    console.log(`\n🎉 Business Intelligence Analysis Complete!`);
    console.log(`🔍 Data points collected: ${allData.length}`);
    console.log(`📈 Market insights: ${analysis.market_insights.length}`);
    console.log(`🏢 Competitive threats: ${analysis.competitive_threats.length}`);
    console.log(`💡 Opportunities identified: ${analysis.opportunities.length}`);
    console.log(`🎯 Strategic recommendations: ${analysis.strategic_recommendations.length}`);
    console.log(`📧 Reports distributed: ${this.recipients.filter(r => r.trim()).length}`);
    console.log(`📊 Dashboard: https://docs.google.com/spreadsheets/d/${this.dashboardSheetId}`);

    return true;

}
}

// Usage Examples
async function main() {
const biAgent = new BusinessIntelligence();

// Run complete BI analysis
await biAgent.runBiAnalysis();
}

if (require.main === module) {
main().catch(console.error);
}

module.exports = BusinessIntelligence;</code></pre>

  </div>
</div>

## 🎯 **Usage Examples**

### Daily Intelligence Briefing

```bash
# Morning executive briefing
python business_intelligence.py --briefing daily
```

### Competitive Analysis Focus

```bash
# Deep dive on competitor activities
node businessIntelligence.js --focus competitors --depth comprehensive
```

### Market Opportunity Assessment

```bash
# Identify emerging market opportunities
python business_intelligence.py --focus opportunities --industry technology
```

## 📊 **Expected Output**

```
🚀 Starting Business Intelligence Analysis
🏢 Company: TechCorp Inc
🏭 Industry: technology
📊 Dashboard: 1BcD3FgHiJkLmNoPqRsTuVwXyZ
📧 Recipients: ceo@company.com, coo@company.com

🔍 Collecting market intelligence...
🏢 Analyzing competitor landscape...
📈 Researching business trends...

📊 Analyzing intelligence data...
📊 Updating BI dashboard...
✅ Updated Market_Insights!A:E
✅ Updated Competitive_Threats!A:E
✅ Updated Opportunities!A:E

📝 Generating executive report...
📧 Distributing intelligence report...
✅ Report sent to ceo@company.com
✅ Report sent to coo@company.com

🎉 Business Intelligence Analysis Complete!
🔍 Data points collected: 25
📈 Market insights: 4
🏢 Competitive threats: 6
💡 Opportunities identified: 3
🎯 Strategic recommendations: 3
📧 Reports distributed: 2
📊 Dashboard: https://docs.google.com/spreadsheets/d/1BcD3FgHiJkLmNoPqRsTuVwXyZ
```

---

_This business intelligence agent provides comprehensive market analysis, competitive insights, and strategic recommendations to drive informed decision-making._
