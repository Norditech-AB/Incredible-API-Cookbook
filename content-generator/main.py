#!/usr/bin/env python3
"""
Content Generator with Incredible API
====================================

This example demonstrates how to:
1. Research trending topics using Perplexity AI
2. Generate multi-format content (blog posts, social media, newsletters)
3. Store content in Google Docs with proper formatting
4. Distribute content to team via email

Usage:
    python main.py "AI trends"
    python main.py "FinTech innovations" "Remote work tools"

Features:
    - AI-powered topic research
    - Multi-format content generation
    - Google Docs integration
    - Automated team distribution
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

class ContentGenerator:
    def __init__(self):
        """Initialize the content generator system."""
        self.api_key = os.getenv('INCREDIBLE_API_KEY')
        self.user_id = os.getenv('USER_ID')
        self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
        self.folder_id = os.getenv('CONTENT_FOLDER_ID')
        self.team_emails = os.getenv('CONTENT_TEAM_EMAILS', '').split(',')
        
        # Configuration
        self.content_types = os.getenv('CONTENT_TYPES', 'blog_post,social_media,newsletter').split(',')
        self.target_audience = os.getenv('TARGET_AUDIENCE', 'professionals')
        
        if not all([self.api_key, self.user_id, self.folder_id]):
            raise ValueError("Missing required environment variables. Check .env file.")
        
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        print(f"✅ Content Generator initialized")
        print(f"📁 Content Folder: {self.folder_id}")
        print(f"📧 Team Emails: {len([e for e in self.team_emails if e.strip()])}")

    def search_perplexity(self, query):
        """Execute Perplexity AI search for content research."""
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

    def research_topic(self, topic):
        """Conduct comprehensive research on a topic for content creation."""
        print(f"\n🚀 Starting content research on: {topic}")
        
        # Generate content-focused research queries
        research_queries = [
            f"{topic} latest trends developments 2024",
            f"{topic} expert opinions thought leadership",
            f"{topic} case studies success stories examples",
            f"{topic} challenges problems solutions industry",
            f"{topic} future predictions outlook trends"
        ]
        
        research_results = []
        
        for query in research_queries:
            result = self.search_perplexity(query)
            if result:
                research_results.append(result)
                time.sleep(1)  # Rate limiting
        
        print(f"📋 Research complete: {len(research_results)} sources gathered")
        return research_results

    def analyze_content_opportunities(self, research_results):
        """Analyze research to identify content opportunities and angles."""
        print("📊 Analyzing content opportunities...")
        
        content_angles = []
        key_themes = []
        trending_topics = []
        
        for result in research_results:
            content = result['answer'].lower()
            
            # Identify content angles
            if any(word in content for word in ['trend', 'emerging', 'new', 'latest']):
                content_angles.append({
                    'angle': 'Trend Analysis',
                    'description': result['answer'][:200] + '...',
                    'source': result['query']
                })
            
            if any(word in content for word in ['challenge', 'problem', 'issue', 'solution']):
                content_angles.append({
                    'angle': 'Problem-Solution',
                    'description': result['answer'][:200] + '...',
                    'source': result['query']
                })
            
            if any(word in content for word in ['expert', 'opinion', 'analysis', 'insight']):
                content_angles.append({
                    'angle': 'Expert Insight',
                    'description': result['answer'][:200] + '...',
                    'source': result['query']
                })
            
            # Extract key themes (simplified)
            if any(word in content for word in ['growth', 'increase', 'expand']):
                key_themes.append('Growth & Expansion')
            
            if any(word in content for word in ['innovation', 'technology', 'digital']):
                key_themes.append('Innovation & Technology')
        
        # Remove duplicates
        key_themes = list(set(key_themes))
        
        print(f"🎯 Analysis complete:")
        print(f"   Content angles: {len(content_angles)}")
        print(f"   Key themes: {len(key_themes)}")
        
        return {
            'content_angles': content_angles[:5],  # Top 5 angles
            'key_themes': key_themes,
            'trending_topics': trending_topics
        }

    def generate_blog_post(self, topic, research_data, analysis):
        """Generate a comprehensive blog post."""
        timestamp = datetime.now().strftime("%B %d, %Y")
        
        # Select best content angle
        primary_angle = analysis['content_angles'][0] if analysis['content_angles'] else None
        
        blog_content = f"""# {topic}: Latest Trends and Insights

*Published: {timestamp}*
*Reading Time: 5-7 minutes*

## Introduction

{topic} continues to evolve rapidly, presenting new opportunities and challenges for businesses and professionals alike. This comprehensive analysis explores the latest developments, expert insights, and future trends shaping this dynamic field.

## Current Landscape

Based on recent research and expert analysis, the {topic.lower()} sector is experiencing significant transformation:

"""
        
        # Add key insights from research
        for i, result in enumerate(research_data[:3], 1):
            blog_content += f"""
### {i}. Key Finding: {result['query'].replace(topic, '').strip()}

{result['answer'][:400]}{'...' if len(result['answer']) > 400 else ''}

"""
        
        # Add analysis section
        if analysis['key_themes']:
            blog_content += """
## Major Themes and Trends

Our analysis reveals several critical themes emerging in this space:

"""
            for theme in analysis['key_themes']:
                blog_content += f"- **{theme}**: Driving significant change across the industry\n"
        
        # Add expert perspectives
        blog_content += """

## Expert Perspectives

Industry leaders and analysts are highlighting several key considerations:

"""
        
        if primary_angle:
            blog_content += f"""
### {primary_angle['angle']}

{primary_angle['description']}

"""
        
        # Add conclusion and call to action
        blog_content += f"""
## Looking Ahead

As {topic.lower()} continues to evolve, staying informed about these trends will be crucial for success. Organizations that adapt quickly to these changes will be best positioned to capitalize on emerging opportunities.

## Key Takeaways

- Monitor emerging trends and their potential impact
- Engage with expert analysis and industry insights  
- Prepare for continued evolution in this space
- Consider how these developments affect your strategy

---

*Want to stay updated on {topic.lower()} trends? Subscribe to our newsletter for regular insights and analysis.*

**Sources:** Based on analysis of {len(research_data)} expert sources and industry reports.
"""
        
        return blog_content

    def generate_social_media_content(self, topic, research_data, analysis):
        """Generate social media posts for different platforms."""
        
        social_content = f"""# {topic} - Social Media Content

*Created: {datetime.now().strftime('%B %d, %Y')}*

## LinkedIn Post

🚀 **{topic} Update: What You Need to Know**

Latest research reveals exciting developments in {topic.lower()}:

"""
        
        # Add key points for LinkedIn
        for i, result in enumerate(research_data[:3], 1):
            key_point = result['answer'][:100] + '...' if len(result['answer']) > 100 else result['answer']
            social_content += f"• {key_point}\n"
        
        social_content += f"""
The implications for businesses are significant. Are you ready for these changes?

#Technology #Innovation #Business #Trends

---

## Twitter Thread

🧵 Thread: {topic} insights (1/5)

1/5 🔥 {topic} is heating up! Here's what industry experts are saying...

2/5 📊 Key trend: {analysis['key_themes'][0] if analysis['key_themes'] else 'Major industry shifts'}

3/5 💡 Expert insight: {research_data[0]['answer'][:100] if research_data else 'Significant developments ahead'}...

4/5 🎯 What this means: Organizations need to adapt quickly to stay competitive

5/5 🚀 Bottom line: {topic} will continue to evolve rapidly. Stay informed! 

What are your thoughts? 👇

---

## Instagram Caption

🌟 {topic} Spotlight 

The future is here, and it's exciting! Our latest research into {topic.lower()} reveals some incredible insights.

Key highlights:
✨ Innovation accelerating
✨ New opportunities emerging  
✨ Industry transformation underway

Swipe to see the data ➡️

#Innovation #Technology #Future #Business #Trends

---

## Newsletter Snippet

**This Week in {topic}**

Our research team analyzed the latest developments in {topic.lower()}. Here's what caught our attention:

🔍 **Research Highlights:**
"""
        
        for result in research_data[:2]:
            social_content += f"• {result['answer'][:80]}...\n"
        
        social_content += f"""
📈 **Trend Watch:** {analysis['key_themes'][0] if analysis['key_themes'] else 'Continued growth expected'}

💡 **Expert Take:** Industry leaders predict significant changes ahead

*Full analysis available in our latest blog post*

---

*Generated by Incredible Content Generator*
"""
        
        return social_content

    def generate_newsletter_content(self, topic, research_data, analysis):
        """Generate newsletter content."""
        
        newsletter_content = f"""# Weekly Newsletter: {topic} Edition

*Issue Date: {datetime.now().strftime('%B %d, %Y')}*

## 📧 Subject Line Options
- "This Week in {topic}: Major Developments You Can't Miss"
- "{topic} Insights: Latest Trends and Expert Analysis"  
- "Weekly Roundup: {topic} News and Analysis"

## 📰 Newsletter Content

**Hello [First Name],**

Welcome to this week's {topic} newsletter! We've been tracking the latest developments and have some exciting insights to share.

### 🔥 What's Trending

This week's research reveals some fascinating developments in {topic.lower()}:

"""
        
        for i, result in enumerate(research_data[:3], 1):
            newsletter_content += f"""
**{i}. {result['query'].replace(topic, '').strip().title()}**
{result['answer'][:200]}{'...' if len(result['answer']) > 200 else ''}

"""
        
        newsletter_content += """
### 💡 Expert Insights

"""
        
        if analysis['content_angles']:
            newsletter_content += f"{analysis['content_angles'][0]['description']}\n\n"
        
        newsletter_content += f"""
### 📈 Looking Ahead

As we monitor {topic.lower()}, several trends are worth watching:

"""
        
        for theme in analysis['key_themes'][:3]:
            newsletter_content += f"• {theme}\n"
        
        newsletter_content += f"""

### 🔗 Resources & Reading

- Full analysis: [Read our latest blog post](#)
- Industry report: [Download whitepaper](#)
- Expert interview: [Watch video](#)

---

**What's Next?**

Keep an eye on these developments as they'll likely impact the industry significantly. We'll continue monitoring and will update you with any major news.

**Questions or feedback?** Reply to this email - we read every response!

Best regards,
The Research Team

---

*Unsubscribe | Update Preferences | Forward to a Friend*
*Generated by Incredible Content Generator*
"""
        
        return newsletter_content

    def create_google_doc(self, title, content):
        """Create Google Doc with generated content."""
        print(f"📄 Creating Google Doc: {title}")
        
        url = f"{self.base_url}/v1/integrations/google_docs/execute"
        data = {
            "user_id": self.user_id,
            "feature_name": "create_document",
            "inputs": {
                "title": title,
                "content": content,
                "folder_id": self.folder_id
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            doc_url = result.get('result', {}).get('url', '')
            doc_id = result.get('result', {}).get('id', '')
            
            if doc_url:
                print(f"✅ Document created: {doc_url}")
                return {
                    'title': title,
                    'url': doc_url,
                    'id': doc_id
                }
            else:
                print(f"❌ Failed to create document")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating document: {e}")
            return None

    def send_content_distribution_email(self, topic, documents):
        """Send content distribution email to team."""
        if not any(e.strip() for e in self.team_emails):
            print("⏸  No team emails configured, skipping distribution")
            return False
        
        print("📧 Sending content distribution email...")
        
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        subject = f"New Content Ready: {topic} - {datetime.now().strftime('%B %d, %Y')}"
        
        body = f"""
📄 **Content Distribution Notification**
📅 Generated: {timestamp}

Hi Team,

New content has been generated for **{topic}** and is ready for your review and publication.

📋 **Generated Content:**
"""
        
        for doc in documents:
            body += f"\n• **{doc['title']}**\n  📎 Google Doc: {doc['url']}\n"
        
        body += f"""

🎯 **Next Steps:**
1. Review content for accuracy and brand voice
2. Make any necessary edits or adjustments
3. Schedule publication across appropriate channels
4. Track performance and engagement metrics

📊 **Content Strategy Notes:**
- Content is based on {topic} research and trending topics
- Optimized for professional audience engagement
- Includes multiple format options for cross-platform distribution

If you have any questions or need modifications, please let me know!

Best regards,
Content Generation Team

---
🤖 Generated by Incredible Content Generator
📅 Report Date: {timestamp}
"""
        
        for email in self.team_emails:
            if not email.strip():
                continue
                
            url = f"{self.base_url}/v1/integrations/gmail/execute"
            data = {
                "user_id": self.user_id,
                "feature_name": "GMAIL_SEND_EMAIL",
                "inputs": {
                    "to": email.strip(),
                    "subject": subject,
                    "body": body
                }
            }
            
            try:
                response = requests.post(url, json=data, headers=self.headers)
                response.raise_for_status()
                print(f"✅ Distribution email sent to: {email.strip()}")
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Failed to send to {email.strip()}: {e}")
        
        return True

    def run_content_workflow(self, topic):
        """Execute complete content generation workflow."""
        print(f"\n{'='*60}")
        print(f"✍️  CONTENT GENERATION: {topic}")
        print(f"{'='*60}")
        
        try:
            # Step 1: Research the topic
            research_results = self.research_topic(topic)
            
            if not research_results:
                print("❌ No research data collected")
                return False
            
            # Step 2: Analyze content opportunities
            analysis = self.analyze_content_opportunities(research_results)
            
            # Step 3: Generate content in multiple formats
            created_documents = []
            
            for content_type in self.content_types:
                if content_type.strip() == 'blog_post':
                    content = self.generate_blog_post(topic, research_results, analysis)
                    doc = self.create_google_doc(f"{topic} - Blog Post", content)
                    
                elif content_type.strip() == 'social_media':
                    content = self.generate_social_media_content(topic, research_results, analysis)
                    doc = self.create_google_doc(f"{topic} - Social Media Content", content)
                    
                elif content_type.strip() == 'newsletter':
                    content = self.generate_newsletter_content(topic, research_results, analysis)
                    doc = self.create_google_doc(f"{topic} - Newsletter Content", content)
                
                if doc:
                    created_documents.append(doc)
                
                time.sleep(1)  # Rate limiting
            
            # Step 4: Distribute to team
            if created_documents:
                self.send_content_distribution_email(topic, created_documents)
            
            # Summary
            print(f"\n🎉 Content generation complete for: {topic}")
            print(f"📊 Research sources: {len(research_results)}")
            print(f"📄 Documents created: {len(created_documents)}")
            print(f"📧 Team members notified: {len([e for e in self.team_emails if e.strip()])}")
            
            if created_documents:
                print(f"\n📁 Created Content:")
                for doc in created_documents:
                    print(f"  - {doc['title']}: {doc['url']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Content generation error: {e}")
            return False

def main():
    """Main entry point for the content generator script."""
    parser = argparse.ArgumentParser(description='Content Generator with Incredible API')
    parser.add_argument('topics', nargs='*', help='Content topics (space-separated)')
    
    args = parser.parse_args()
    
    # Use provided topics or default
    topics = args.topics if args.topics else ["AI and Machine Learning Trends"]
    
    if not topics:
        print("💡 Usage: python main.py 'Topic 1' 'Topic 2' ...")
        return 1
    
    print("✍️  Incredible API - Content Generator")
    print("=" * 50)
    
    try:
        # Initialize the content generator
        generator = ContentGenerator()
        
        # Process each topic
        successful_content = 0
        for topic in topics:
            if generator.run_content_workflow(topic):
                successful_content += 1
            
            # Delay between topics
            if len(topics) > 1:
                time.sleep(3)
        
        print(f"\n✅ Successfully generated content for {successful_content}/{len(topics)} topics")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Set up your .env file with all required variables")
        print("   2. Connected Perplexity AI integration")
        print("   3. Completed OAuth setup for Google Docs and Gmail")
        print("   4. Created Google Drive folder for content storage")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
