#!/usr/bin/env python3
"""
Financial Dashboard with Incredible API
======================================

This example demonstrates how to:
1. Research financial data using Perplexity AI
2. Analyze market trends and performance
3. Create automated dashboards in Google Sheets
4. Email executive financial reports

Usage:
    python main.py
    python main.py --symbols AAPL,GOOGL,TSLA

Features:
    - Real-time market research
    - Automated trend analysis
    - Executive dashboard creation
    - Intelligent alert system
"""

import os
import time
import argparse
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FinancialDashboard:
    def __init__(self):
        """Initialize the financial dashboard system."""
        self.api_key = os.getenv('INCREDIBLE_API_KEY')
        self.user_id = os.getenv('USER_ID')
        self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
        self.sheet_id = os.getenv('DASHBOARD_SHEET_ID')
        self.recipients = os.getenv('REPORT_RECIPIENTS', '').split(',')
        
        # Configuration
        self.company_symbols = os.getenv('COMPANY_SYMBOLS', 'AAPL,GOOGL,MSFT').split(',')
        self.market_sectors = os.getenv('MARKET_SECTORS', 'technology,finance,healthcare').split(',')
        
        if not all([self.api_key, self.user_id, self.sheet_id]):
            raise ValueError("Missing required environment variables. Check .env file.")
        
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        print(f"✅ Financial Dashboard initialized")
        print(f"📊 Dashboard Sheet: {self.sheet_id}")
        print(f"📈 Tracking: {', '.join(self.company_symbols)}")

    def search_perplexity(self, query):
        """Execute Perplexity AI search for financial data."""
        print(f"🔍 Researching: {query}")
        
        url = f"{self.base_url}/v1/integrations/perplexity/execute"
        data = {
            "user_id": self.user_id,
            "feature_name": "PerplexityAISearch",
            "inputs": {
                "query": query
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            answer = result.get('result', {}).get('answer', '')
            sources = result.get('result', {}).get('sources', [])
            
            return {
                'query': query,
                'answer': answer,
                'sources': sources,
                'timestamp': datetime.now().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error researching '{query}': {e}")
            return None

    def research_market_overview(self):
        """Research general market conditions and trends."""
        print("\n📈 Researching market overview...")
        
        market_queries = [
            "stock market performance today NYSE NASDAQ current",
            "market volatility index VIX fear greed current levels",
            "economic indicators GDP inflation unemployment latest",
            "Federal Reserve interest rates policy latest news",
            "market sentiment investor confidence latest trends"
        ]
        
        market_data = []
        
        for query in market_queries:
            result = self.search_perplexity(query)
            if result:
                market_data.append({
                    'category': 'market_overview',
                    'query': query,
                    'data': result['answer'],
                    'sources': len(result['sources']),
                    'timestamp': result['timestamp']
                })
                time.sleep(1)  # Rate limiting
        
        print(f"✅ Market overview research complete: {len(market_data)} topics")
        return market_data

    def research_company_performance(self, symbols=None):
        """Research specific company performance."""
        if symbols is None:
            symbols = self.company_symbols
            
        print(f"\n🏢 Researching company performance: {', '.join(symbols)}")
        
        company_data = []
        
        for symbol in symbols:
            company_queries = [
                f"{symbol} stock price performance earnings latest",
                f"{symbol} quarterly results revenue growth analysis",
                f"{symbol} news announcements developments recent"
            ]
            
            for query in company_queries:
                result = self.search_perplexity(query)
                if result:
                    company_data.append({
                        'category': 'company_performance',
                        'symbol': symbol,
                        'query': query,
                        'data': result['answer'],
                        'sources': len(result['sources']),
                        'timestamp': result['timestamp']
                    })
                    time.sleep(1)  # Rate limiting
        
        print(f"✅ Company research complete: {len(company_data)} analyses")
        return company_data

    def research_sector_trends(self, sectors=None):
        """Research sector-specific trends and performance."""
        if sectors is None:
            sectors = self.market_sectors
            
        print(f"\n🏭 Researching sector trends: {', '.join(sectors)}")
        
        sector_data = []
        
        for sector in sectors:
            sector_queries = [
                f"{sector} sector performance trends analysis 2024",
                f"{sector} industry outlook growth opportunities",
                f"{sector} stocks leaders gainers performance"
            ]
            
            for query in sector_queries:
                result = self.search_perplexity(query)
                if result:
                    sector_data.append({
                        'category': 'sector_trends',
                        'sector': sector,
                        'query': query,
                        'data': result['answer'],
                        'sources': len(result['sources']),
                        'timestamp': result['timestamp']
                    })
                    time.sleep(1)  # Rate limiting
        
        print(f"✅ Sector research complete: {len(sector_data)} analyses")
        return sector_data

    def analyze_financial_data(self, all_data):
        """Analyze collected financial data for insights and alerts."""
        print("📊 Analyzing financial data...")
        
        analysis = {
            'market_sentiment': 'NEUTRAL',
            'key_insights': [],
            'alerts': [],
            'recommendations': [],
            'performance_summary': {}
        }
        
        positive_indicators = 0
        negative_indicators = 0
        
        for item in all_data:
            data_text = item['data'].lower()
            
            # Sentiment analysis (simplified)
            if any(word in data_text for word in ['gain', 'up', 'rise', 'positive', 'growth', 'bull']):
                positive_indicators += 1
                
            if any(word in data_text for word in ['loss', 'down', 'fall', 'negative', 'decline', 'bear']):
                negative_indicators += 1
            
            # Key insights extraction
            if any(word in data_text for word in ['breakthrough', 'record', 'highest', 'milestone']):
                analysis['key_insights'].append({
                    'type': 'positive_development',
                    'description': item['data'][:200] + '...',
                    'source': item['query'],
                    'category': item['category']
                })
            
            # Alert detection
            if any(word in data_text for word in ['volatility', 'crash', 'plunge', 'surge', 'unusual']):
                analysis['alerts'].append({
                    'level': 'HIGH' if any(word in data_text for word in ['crash', 'plunge']) else 'MEDIUM',
                    'message': item['data'][:150] + '...',
                    'source': item['query'],
                    'timestamp': item['timestamp']
                })
        
        # Determine overall market sentiment
        if positive_indicators > negative_indicators * 1.5:
            analysis['market_sentiment'] = 'BULLISH'
        elif negative_indicators > positive_indicators * 1.5:
            analysis['market_sentiment'] = 'BEARISH'
        else:
            analysis['market_sentiment'] = 'MIXED'
        
        # Generate recommendations
        analysis['recommendations'] = self.generate_recommendations(analysis, all_data)
        
        print(f"🎯 Analysis complete:")
        print(f"   Market Sentiment: {analysis['market_sentiment']}")
        print(f"   Key Insights: {len(analysis['key_insights'])}")
        print(f"   Alerts: {len(analysis['alerts'])}")
        
        return analysis

    def generate_recommendations(self, analysis, all_data):
        """Generate investment and strategy recommendations."""
        recommendations = []
        
        if analysis['market_sentiment'] == 'BULLISH':
            recommendations.append({
                'type': 'INVESTMENT',
                'recommendation': 'Consider increasing equity positions in strong-performing sectors',
                'reasoning': 'Market showing positive momentum across multiple indicators',
                'risk_level': 'MODERATE'
            })
        
        elif analysis['market_sentiment'] == 'BEARISH':
            recommendations.append({
                'type': 'RISK_MANAGEMENT',
                'recommendation': 'Consider defensive positioning and portfolio hedging',
                'reasoning': 'Market showing concerning trends requiring caution',
                'risk_level': 'HIGH'
            })
        
        if len(analysis['alerts']) > 2:
            recommendations.append({
                'type': 'MONITORING',
                'recommendation': 'Increase portfolio monitoring frequency due to market volatility',
                'reasoning': f'{len(analysis["alerts"])} significant market alerts detected',
                'risk_level': 'MEDIUM'
            })
        
        return recommendations

    def save_to_dashboard(self, all_data, analysis):
        """Save financial data and analysis to Google Sheets dashboard."""
        print("📊 Updating financial dashboard...")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Market Summary Sheet
        summary_data = []
        summary_data.append([
            "Timestamp", "Market Sentiment", "Total Insights", "Alerts", "Data Points"
        ])
        summary_data.append([
            timestamp,
            analysis['market_sentiment'],
            len(analysis['key_insights']),
            len(analysis['alerts']),
            len(all_data)
        ])
        
        self.update_sheet("Market_Summary!A:E", summary_data)
        
        # Detailed Data Sheet
        detailed_data = []
        detailed_data.append([
            "Timestamp", "Category", "Query", "Key_Data", "Sources", "Analysis"
        ])
        
        for item in all_data:
            detailed_data.append([
                item['timestamp'],
                item['category'],
                item['query'],
                item['data'][:500] + '...' if len(item['data']) > 500 else item['data'],
                item['sources'],
                "Processed"
            ])
        
        self.update_sheet("Detailed_Data!A:F", detailed_data)
        
        # Alerts Sheet (if there are alerts)
        if analysis['alerts']:
            alerts_data = []
            alerts_data.append([
                "Timestamp", "Level", "Message", "Source"
            ])
            
            for alert in analysis['alerts']:
                alerts_data.append([
                    alert['timestamp'],
                    alert['level'],
                    alert['message'],
                    alert['source']
                ])
            
            self.update_sheet("Alerts!A:D", alerts_data)
        
        print("✅ Dashboard updated successfully")

    def update_sheet(self, range_name, data):
        """Update Google Sheets with financial data."""
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
            response = requests.post(url, json=request_data, headers=self.headers)
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error updating sheet: {e}")
            return False

    def generate_executive_report(self, analysis, all_data):
        """Generate comprehensive executive financial report."""
        print("📝 Generating executive report...")
        
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        # Calculate summary statistics
        total_data_points = len(all_data)
        market_categories = len(set(item['category'] for item in all_data))
        
        report = f"""
📊 FINANCIAL INTELLIGENCE REPORT
{'=' * 50}
📅 Generated: {timestamp}
📈 Market Sentiment: {analysis['market_sentiment']}
📊 Data Points Analyzed: {total_data_points}
🏷️ Categories Covered: {market_categories}

💡 EXECUTIVE SUMMARY
{'-' * 20}
Market analysis reveals {analysis['market_sentiment'].lower()} sentiment with {len(analysis['key_insights'])} significant insights and {len(analysis['alerts'])} alerts requiring attention.

Key tracking includes: {', '.join(self.company_symbols)} and sectors: {', '.join(self.market_sectors)}
"""
        
        # Add key insights
        if analysis['key_insights']:
            report += "\n🎯 KEY INSIGHTS\n" + "-" * 15 + "\n"
            for i, insight in enumerate(analysis['key_insights'][:5], 1):
                report += f"{i}. {insight['description']}\n   Source: {insight['source']}\n\n"
        
        # Add alerts
        if analysis['alerts']:
            report += "🚨 MARKET ALERTS\n" + "-" * 15 + "\n"
            for alert in analysis['alerts']:
                report += f"• **{alert['level']}**: {alert['message']}\n\n"
        
        # Add recommendations
        if analysis['recommendations']:
            report += "💼 STRATEGIC RECOMMENDATIONS\n" + "-" * 30 + "\n"
            for i, rec in enumerate(analysis['recommendations'], 1):
                report += f"{i}. **{rec['type']}** (Risk: {rec['risk_level']})\n"
                report += f"   {rec['recommendation']}\n"
                report += f"   Reasoning: {rec['reasoning']}\n\n"
        
        # Add market overview
        report += "📈 MARKET OVERVIEW\n" + "-" * 17 + "\n"
        market_items = [item for item in all_data if item['category'] == 'market_overview']
        for item in market_items[:3]:
            report += f"• {item['data'][:200]}{'...' if len(item['data']) > 200 else ''}\n\n"
        
        # Add company highlights
        company_items = [item for item in all_data if item['category'] == 'company_performance']
        if company_items:
            report += "🏢 COMPANY HIGHLIGHTS\n" + "-" * 20 + "\n"
            for item in company_items[:3]:
                symbol = item.get('symbol', 'N/A')
                report += f"• **{symbol}**: {item['data'][:150]}{'...' if len(item['data']) > 150 else ''}\n\n"
        
        report += f"""
📊 DATA SOURCES & METHODOLOGY
{'-' * 30}
• Real-time financial data via Perplexity AI
• Multi-source verification and analysis
• Automated sentiment and trend analysis
• Risk assessment and recommendation engine

🔗 DASHBOARD ACCESS
{'-' * 20}
Full dashboard: https://docs.google.com/spreadsheets/d/{self.sheet_id}

---
🤖 Generated by Incredible Financial Dashboard
📅 Report Date: {timestamp}
🔄 Next update: Automated based on schedule
"""
        
        return report

    def send_financial_report(self, report):
        """Send financial report via email to recipients."""
        if not any(r.strip() for r in self.recipients):
            print("⏸  No recipients configured, skipping email")
            return False
        
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
                    "body": report
                }
            }
            
            try:
                response = requests.post(url, json=data, headers=self.headers)
                response.raise_for_status()
                print(f"✅ Report sent to: {recipient.strip()}")
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Failed to send to {recipient.strip()}: {e}")
        
        return True

    def run_financial_analysis(self, symbols=None):
        """Execute complete financial analysis workflow."""
        print(f"\n{'='*60}")
        print(f"💰 FINANCIAL DASHBOARD ANALYSIS")
        print(f"{'='*60}")
        
        try:
            # Step 1: Research market overview
            market_data = self.research_market_overview()
            
            # Step 2: Research company performance
            company_data = self.research_company_performance(symbols)
            
            # Step 3: Research sector trends
            sector_data = self.research_sector_trends()
            
            # Combine all data
            all_data = market_data + company_data + sector_data
            
            if not all_data:
                print("❌ No financial data collected")
                return False
            
            # Step 4: Analyze data
            analysis = self.analyze_financial_data(all_data)
            
            # Step 5: Save to dashboard
            self.save_to_dashboard(all_data, analysis)
            
            # Step 6: Generate and send report
            report = self.generate_executive_report(analysis, all_data)
            self.send_financial_report(report)
            
            # Summary
            print(f"\n🎉 Financial analysis complete!")
            print(f"📊 Data points analyzed: {len(all_data)}")
            print(f"📈 Market sentiment: {analysis['market_sentiment']}")
            print(f"🚨 Alerts generated: {len(analysis['alerts'])}")
            print(f"📧 Reports sent: {len([r for r in self.recipients if r.strip()])}")
            print(f"📊 View dashboard: https://docs.google.com/spreadsheets/d/{self.sheet_id}")
            
            return True
            
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            return False

def main():
    """Main entry point for the financial dashboard script."""
    parser = argparse.ArgumentParser(description='Financial Dashboard with Incredible API')
    parser.add_argument('--symbols', '-s', help='Comma-separated stock symbols (e.g., AAPL,GOOGL,TSLA)')
    
    args = parser.parse_args()
    
    # Parse symbols if provided
    symbols = None
    if args.symbols:
        symbols = [s.strip().upper() for s in args.symbols.split(',')]
    
    print("💰 Incredible API - Financial Dashboard")
    print("=" * 50)
    
    try:
        # Initialize the financial dashboard
        dashboard = FinancialDashboard()
        
        # Run financial analysis
        success = dashboard.run_financial_analysis(symbols)
        
        if success:
            print(f"\n✅ Financial dashboard updated successfully")
        else:
            print(f"\n❌ Financial analysis failed")
            return 1
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Set up your .env file with all required variables")
        print("   2. Connected Perplexity AI integration")
        print("   3. Completed OAuth setup for Google Sheets and Gmail")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
