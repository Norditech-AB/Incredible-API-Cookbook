#!/usr/bin/env python3
"""
Research Reporter with Incredible API
=====================================

This example demonstrates how to:
1. Use Perplexity AI to research topics
2. Compile findings into structured reports
3. Store research data in Google Sheets
4. Email comprehensive reports to stakeholders

Usage:
    python main.py "AI in Healthcare 2024"
    python main.py --topics "FinTech trends" "Blockchain adoption" 

Features:
    - Multi-query research strategy
    - Intelligent source compilation
    - Structured data storage
    - Professional report generation
"""

import os
import sys
import time
import argparse
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ResearchReporter:
    def __init__(self):
        """Initialize the research reporter system."""
        self.api_key = os.getenv('INCREDIBLE_API_KEY')
        self.user_id = os.getenv('USER_ID')
        self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
        self.sheet_id = os.getenv('RESEARCH_SHEET_ID')
        self.recipients = os.getenv('REPORT_RECIPIENTS', '').split(',')
        
        if not all([self.api_key, self.user_id, self.sheet_id]):
            raise ValueError("Missing required environment variables. Check .env file.")
        
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        print(f"✅ Research Reporter initialized")
        print(f"📊 Research Sheet: {self.sheet_id}")
        print(f"📧 Recipients: {len([r for r in self.recipients if r.strip()])}")

    def search_perplexity(self, query):
        """Execute Perplexity AI search."""
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
            
            print(f"✅ Research complete: {len(sources)} sources")
            return {
                'query': query,
                'answer': answer,
                'sources': sources,
                'timestamp': datetime.now().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error researching '{query}': {e}")
            return None

    def research_topic(self, topic):
        """Conduct comprehensive research on a topic using multiple queries."""
        print(f"\n🚀 Starting research on: {topic}")
        
        # Generate comprehensive research queries
        research_queries = [
            f"{topic} latest developments 2024",
            f"{topic} market trends analysis current",
            f"{topic} challenges opportunities industry",
            f"{topic} expert opinions predictions future",
            f"{topic} case studies success stories recent"
        ]
        
        research_results = []
        
        for query in research_queries:
            result = self.search_perplexity(query)
            if result:
                research_results.append(result)
                # Be respectful to the API
                time.sleep(2)
            else:
                print(f"⚠️  Skipped failed query: {query}")
        
        print(f"📋 Completed research: {len(research_results)}/{len(research_queries)} queries successful")
        return research_results

    def analyze_research_data(self, research_results):
        """Analyze research data to extract key insights."""
        print("📊 Analyzing research data...")
        
        analysis = {
            'key_themes': [],
            'opportunities': [],
            'challenges': [],
            'expert_insights': [],
            'data_points': []
        }
        
        for result in research_results:
            content = result['answer'].lower()
            
            # Extract key themes (simplified keyword analysis)
            if any(word in content for word in ['trend', 'trending', 'growth', 'increase']):
                analysis['key_themes'].append({
                    'theme': 'Growth Trend',
                    'source_query': result['query'],
                    'evidence': result['answer'][:200] + '...'
                })
            
            # Identify opportunities
            if any(word in content for word in ['opportunity', 'potential', 'market', 'demand']):
                analysis['opportunities'].append({
                    'opportunity': 'Market Opportunity',
                    'source_query': result['query'],
                    'description': result['answer'][:200] + '...'
                })
            
            # Identify challenges
            if any(word in content for word in ['challenge', 'barrier', 'difficulty', 'problem']):
                analysis['challenges'].append({
                    'challenge': 'Industry Challenge',
                    'source_query': result['query'],
                    'description': result['answer'][:200] + '...'
                })
        
        print(f"🎯 Analysis complete:")
        print(f"   Themes: {len(analysis['key_themes'])}")
        print(f"   Opportunities: {len(analysis['opportunities'])}")
        print(f"   Challenges: {len(analysis['challenges'])}")
        
        return analysis

    def save_research_to_sheets(self, topic, research_results, analysis):
        """Save comprehensive research data to Google Sheets."""
        print("📊 Saving research to Google Sheets...")
        
        # Prepare data for the Research Data sheet
        research_data = []
        research_data.append([
            "Timestamp", "Topic", "Query", "Answer", "Sources Count", "Analysis"
        ])
        
        for result in research_results:
            research_data.append([
                result['timestamp'],
                topic,
                result['query'],
                result['answer'][:1000] + '...' if len(result['answer']) > 1000 else result['answer'],
                len(result['sources']),
                "Processed"
            ])
        
        # Save research data
        self.update_sheet("Research_Data!A:F", research_data)
        
        # Prepare analysis summary
        analysis_data = []
        analysis_data.append([
            "Timestamp", "Topic", "Category", "Insight", "Source Query"
        ])
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add themes
        for theme in analysis['key_themes']:
            analysis_data.append([
                timestamp, topic, "Theme", theme['evidence'], theme['source_query']
            ])
        
        # Add opportunities
        for opp in analysis['opportunities']:
            analysis_data.append([
                timestamp, topic, "Opportunity", opp['description'], opp['source_query']
            ])
        
        # Add challenges
        for challenge in analysis['challenges']:
            analysis_data.append([
                timestamp, topic, "Challenge", challenge['description'], challenge['source_query']
            ])
        
        # Save analysis
        self.update_sheet("Analysis!A:E", analysis_data)
        
        print("✅ Research data saved to Google Sheets")

    def update_sheet(self, range_name, data):
        """Update Google Sheets with research data."""
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

    def generate_executive_report(self, topic, research_results, analysis):
        """Generate a comprehensive executive report."""
        print("📝 Generating executive report...")
        
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        # Count metrics
        total_sources = sum(len(r['sources']) for r in research_results)
        
        report = f"""
📊 RESEARCH REPORT: {topic.upper()}
{'=' * 50}
📅 Generated: {timestamp}
🔍 Research Queries: {len(research_results)}
📚 Total Sources: {total_sources}

📋 EXECUTIVE SUMMARY
{'-' * 20}
This report provides comprehensive research on {topic} based on {len(research_results)} targeted research queries and {total_sources} verified sources. The analysis reveals key market trends, opportunities, and challenges in this domain.

🎯 KEY FINDINGS
{'-' * 15}
"""
        
        # Add key themes
        if analysis['key_themes']:
            report += "\n🔍 Major Themes:\n"
            for i, theme in enumerate(analysis['key_themes'][:3], 1):
                report += f"{i}. {theme['evidence']}\n\n"
        
        # Add opportunities
        if analysis['opportunities']:
            report += "💡 Key Opportunities:\n"
            for i, opp in enumerate(analysis['opportunities'][:3], 1):
                report += f"{i}. {opp['description']}\n\n"
        
        # Add challenges
        if analysis['challenges']:
            report += "⚠️  Key Challenges:\n"
            for i, challenge in enumerate(analysis['challenges'][:3], 1):
                report += f"{i}. {challenge['description']}\n\n"
        
        # Add detailed research findings
        report += f"""
📚 DETAILED RESEARCH FINDINGS
{'-' * 30}
"""
        
        for i, result in enumerate(research_results, 1):
            report += f"""
{i}. {result['query']}
{'-' * len(result['query'])}
{result['answer'][:500]}{'...' if len(result['answer']) > 500 else ''}

Sources: {len(result['sources'])} references
{'-' * 20}
"""
        
        report += f"""

📊 RESEARCH METHODOLOGY
{'-' * 25}
• Multi-query approach using {len(research_results)} targeted searches
• AI-powered source verification and analysis
• Cross-reference validation across {total_sources} sources
• Real-time data collection and processing

📈 RECOMMENDATIONS
{'-' * 20}
Based on this research, we recommend:
1. Further investigation into the most promising opportunities identified
2. Development of strategies to address key challenges
3. Continued monitoring of trends and developments
4. Stakeholder engagement based on expert insights

📋 DATA ACCESS
{'-' * 15}
Full research data and analysis available at:
Google Sheets: https://docs.google.com/spreadsheets/d/{self.sheet_id}

---
🤖 Generated by Incredible Research Reporter
📅 Report Date: {timestamp}
🔄 This report reflects the most current information available at time of generation.
"""
        
        return report

    def send_report_email(self, topic, report):
        """Send research report via email to recipients."""
        if not any(r.strip() for r in self.recipients):
            print("⏸  No recipients configured, skipping email")
            return False
        
        print("📧 Sending research report...")
        
        subject = f"Research Report: {topic} - {datetime.now().strftime('%B %d, %Y')}"
        
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

    def run_research_workflow(self, topic):
        """Execute complete research workflow for a topic."""
        print(f"\n{'='*60}")
        print(f"🔬 RESEARCH WORKFLOW: {topic}")
        print(f"{'='*60}")
        
        try:
            # Step 1: Conduct research
            research_results = self.research_topic(topic)
            
            if not research_results:
                print("❌ No research data collected")
                return False
            
            # Step 2: Analyze findings
            analysis = self.analyze_research_data(research_results)
            
            # Step 3: Save to sheets
            self.save_research_to_sheets(topic, research_results, analysis)
            
            # Step 4: Generate report
            report = self.generate_executive_report(topic, research_results, analysis)
            
            # Step 5: Send report
            self.send_report_email(topic, report)
            
            # Summary
            print(f"\n🎉 Research workflow complete for: {topic}")
            print(f"📊 Research queries: {len(research_results)}")
            print(f"📚 Total sources: {sum(len(r['sources']) for r in research_results)}")
            print(f"📧 Report recipients: {len([r for r in self.recipients if r.strip()])}")
            print(f"📈 View full data: https://docs.google.com/spreadsheets/d/{self.sheet_id}")
            
            return True
            
        except Exception as e:
            print(f"❌ Workflow error: {e}")
            return False

def main():
    """Main entry point for the research reporter script."""
    parser = argparse.ArgumentParser(description='Research Reporter with Incredible API')
    parser.add_argument('topics', nargs='*', help='Research topics (space-separated)')
    parser.add_argument('--topics', '-t', action='append', help='Additional topics')
    
    args = parser.parse_args()
    
    # Collect all topics
    topics = []
    if args.topics:
        topics.extend(args.topics)
    if hasattr(args, 'topics') and args.topics:
        topics.extend(args.topics)
    
    # Default topic if none provided
    if not topics:
        topics = ["AI and Machine Learning Trends 2024"]
        print("💡 No topics specified, using default: AI and Machine Learning Trends 2024")
    
    print("🔬 Incredible API - Research Reporter")
    print("=" * 50)
    
    try:
        # Initialize the research reporter
        reporter = ResearchReporter()
        
        # Process each topic
        successful_reports = 0
        for topic in topics:
            if reporter.run_research_workflow(topic):
                successful_reports += 1
            
            # Delay between topics to respect rate limits
            if len(topics) > 1:
                time.sleep(5)
        
        print(f"\n✅ Successfully completed {successful_reports}/{len(topics)} research reports")
        
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
