# Content Distribution Agent

Automate your content creation and distribution across multiple platforms with an intelligent agent that researches topics, creates content, and publishes strategically.

## 📋 **Workflow Overview**

```
🔍 Perplexity → 📄 Google Docs → 📧 Gmail
   Research       Create       Distribute
```

**Apps Used:** Perplexity + Google Docs + Gmail (3 apps total)

## 🎯 **What This Agent Does**

1. **🔍 Research**: Gathers comprehensive information on trending topics
2. **📄 Create**: Generates well-structured content in Google Docs
3. **📧 Distribute**: Sends content to stakeholders and publishing teams

## 🛠 **Prerequisites**

- Incredible API access with function calling enabled
- Connected integrations:
  - Perplexity (API key authentication)
  - Google Docs (OAuth)
  - Gmail (OAuth)

## 📋 **Setup**

### Environment Configuration

```bash
# .env
INCREDIBLE_API_KEY=your_incredible_api_key
INCREDIBLE_BASE_URL=https://api.incredible.one
USER_ID=your_user_id

# Content Settings
CONTENT_FOLDER_ID=your_google_drive_folder_id
CONTENT_TEAM_EMAILS=editor@company.com,marketing@company.com
PUBLICATION_SCHEDULE=daily  # daily, weekly, or custom

# Content Focus Areas
CONTENT_TOPICS=AI,technology,business,marketing
CONTENT_TYPES=blog_post,social_media,newsletter
TARGET_AUDIENCE=professionals,entrepreneurs,tech_enthusiasts
```

## 💻 **Implementation**

<div class="code-tabs" data-section="content-distribution">
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

class ContentDistribution:
def **init**(self):
self.api_key = os.getenv('INCREDIBLE_API_KEY')
self.base_url = os.getenv('INCREDIBLE_BASE_URL', 'https://api.incredible.one')
self.user_id = os.getenv('USER_ID')
self.folder_id = os.getenv('CONTENT_FOLDER_ID')
self.team_emails = os.getenv('CONTENT_TEAM_EMAILS', '').split(',')

        self.content_topics = os.getenv('CONTENT_TOPICS', 'AI,technology').split(',')
        self.content_types = os.getenv('CONTENT_TYPES', 'blog_post,social_media').split(',')
        self.target_audience = os.getenv('TARGET_AUDIENCE', 'professionals').split(',')

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def research_trending_topics(self, focus_area="technology"):
        """Research trending topics and current developments"""
        print(f"🔍 Researching trending topics in {focus_area}...")

        research_queries = [
            f"trending {focus_area} topics 2024 latest developments",
            f"popular {focus_area} discussions social media today",
            f"{focus_area} industry news breaking developments",
            f"viral {focus_area} content ideas engagement trends",
            f"{focus_area} thought leadership trending discussions"
        ]

        research_results = []

        for query in research_queries:
            result = self.execute_perplexity_search(query)
            research_results.append({
                'query': query,
                'findings': result,
                'focus_area': focus_area,
                'timestamp': datetime.now().isoformat()
            })

        return research_results

    def execute_perplexity_search(self, query):
        """Execute Perplexity search for content research"""
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
                return f"Research failed: {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"

    def analyze_content_opportunities(self, research_results):
        """Analyze research to identify content opportunities"""
        print("📊 Analyzing content opportunities...")

        opportunities = []

        for result in research_results:
            findings = result['findings']

            # Extract potential content topics
            content_ideas = []

            # Look for trending keywords and topics
            trending_keywords = self.extract_trending_keywords(findings)

            # Generate content ideas based on findings
            if 'AI' in findings or 'artificial intelligence' in findings.lower():
                content_ideas.append({
                    'type': 'blog_post',
                    'title': f"The Future of AI in {result['focus_area'].title()}",
                    'angle': 'thought_leadership',
                    'keywords': trending_keywords,
                    'urgency': 'high'
                })

            if 'trend' in findings.lower() or 'popular' in findings.lower():
                content_ideas.append({
                    'type': 'social_media',
                    'title': f"5 {result['focus_area'].title()} Trends You Can't Ignore",
                    'angle': 'list_format',
                    'keywords': trending_keywords,
                    'urgency': 'medium'
                })

            if 'breakthrough' in findings.lower() or 'innovation' in findings.lower():
                content_ideas.append({
                    'type': 'newsletter',
                    'title': f"Innovation Spotlight: {result['focus_area'].title()} Breakthroughs",
                    'angle': 'news_analysis',
                    'keywords': trending_keywords,
                    'urgency': 'high'
                })

            for idea in content_ideas:
                idea['research_source'] = result['query']
                idea['supporting_data'] = findings[:200] + '...' if len(findings) > 200 else findings
                opportunities.append(idea)

        # Sort by urgency and potential impact
        opportunities.sort(key=lambda x: {'high': 3, 'medium': 2, 'low': 1}[x['urgency']], reverse=True)

        return opportunities[:5]  # Return top 5 opportunities

    def extract_trending_keywords(self, text):
        """Extract trending keywords from research text"""
        # Simple keyword extraction
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}

        words = text.lower().split()
        keywords = [word.strip('.,!?;:"()[]') for word in words
                   if len(word) > 3 and word.lower() not in common_words]

        # Return most frequent keywords
        from collections import Counter
        word_counts = Counter(keywords)
        return [word for word, count in word_counts.most_common(10)]

    def create_content_document(self, content_idea):
        """Create content document in Google Docs"""
        print(f"📄 Creating content: {content_idea['title']}")

        # Generate content outline and draft
        content_draft = self.generate_content_draft(content_idea)

        # Create Google Doc
        url = f"{self.base_url}/v1/integrations/google_docs/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "create_document",
            "inputs": {
                "title": content_idea['title'],
                "content": content_draft,
                "folder_id": self.folder_id
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                result = response.json()
                doc_id = result.get('result', {}).get('document_id')
                doc_url = f"https://docs.google.com/document/d/{doc_id}"
                print(f"✅ Document created: {doc_url}")
                return {
                    'doc_id': doc_id,
                    'doc_url': doc_url,
                    'title': content_idea['title'],
                    'type': content_idea['type']
                }
            else:
                print(f"❌ Document creation failed: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Document error: {e}")
            return None

    def generate_content_draft(self, content_idea):
        """Generate content draft based on idea and research"""
        timestamp = datetime.now().strftime("%B %d, %Y")

        if content_idea['type'] == 'blog_post':
            return f"""# {content_idea['title']}

_Published: {timestamp}_
_Keywords: {', '.join(content_idea.get('keywords', [])[:5])}_

## Introduction

{content_idea['supporting_data']}

## Key Points to Explore

1. **Current State Analysis**

   - Market overview and trends
   - Key players and developments
   - Challenges and opportunities

2. **Future Implications**

   - Predicted outcomes and impacts
   - Strategic considerations
   - Actionable insights

3. **Expert Perspectives**
   - Industry expert opinions
   - Case studies and examples
   - Best practices and recommendations

## Supporting Research

**Source**: {content_idea['research_source']}

**Key Findings**: {content_idea['supporting_data']}

## Next Steps

- [ ] Add detailed research and citations
- [ ] Include relevant statistics and data
- [ ] Add expert quotes and interviews
- [ ] Optimize for SEO with target keywords
- [ ] Create compelling visuals and graphics
- [ ] Review and edit for publication

---

_Draft created by Incredible Content Distribution Agent_
_Research conducted on {timestamp}_
"""

        elif content_idea['type'] == 'social_media':
            return f"""# {content_idea['title']} - Social Media Content

_Created: {timestamp}_

## Main Post Content

🚀 **{content_idea['title']}**

Based on the latest research, here are the key developments:

{content_idea['supporting_data'][:150]}...

What trends are you seeing in your industry? Share your thoughts! 👇

#{' #'.join(content_idea.get('keywords', [])[:3])}

## Alternative Versions

**LinkedIn Version:**
Professional take with industry insights and discussion prompts

**Twitter Version:**
Concise thread format with key statistics and engaging questions

**Instagram Version:**
Visual storytelling with infographic potential

## Engagement Strategy

- Best posting times: [Add optimal times for each platform]
- Target hashtags: #{' #'.join(content_idea.get('keywords', []))}
- Call-to-action: Encourage discussion and sharing
- Follow-up content: Plan series or continuation posts

## Performance Tracking

- [ ] Monitor engagement rates
- [ ] Track hashtag performance
- [ ] Analyze audience response
- [ ] Iterate based on feedback

---

_Generated by Incredible Content Distribution Agent_
"""

        else:  # newsletter
            return f"""# {content_idea['title']} - Newsletter

_Issue Date: {timestamp}_

## Subject Line Options

1. {content_idea['title']}
2. Breaking: Latest Developments in {content_idea.get('focus_area', 'Technology')}
3. Weekly Roundup: What's Trending Now

## Newsletter Content

**Hello [Subscriber Name],**

Hope you're having a great week! Here's what's capturing attention in {content_idea.get('focus_area', 'our industry')} right now:

### 🔥 Trending This Week

{content_idea['supporting_data']}

### 💡 Key Takeaways

- [Add 3-5 bullet points of key insights]
- [Include actionable advice]
- [Highlight important developments]

### 📚 Worth Reading

- [Curated list of relevant articles]
- [Industry reports and studies]
- [Expert opinions and analysis]

### 🚀 What's Next

Looking ahead, keep an eye on:

- [Upcoming developments]
- [Important dates and events]
- [Emerging trends to watch]

---

**Thank you for reading!**

Best regards,
[Your Name]

P.S. What topics would you like us to cover next? Reply and let us know!

---

_Unsubscribe | Update Preferences | Forward to a Friend_
_Generated by Incredible Content Distribution Agent_
"""

    def distribute_content(self, documents):
        """Distribute created content to stakeholders"""
        print("📧 Distributing content to stakeholders...")

        if not documents:
            print("❌ No documents to distribute")
            return

        # Prepare summary email
        summary = self.create_distribution_summary(documents)

        subject = f"New Content Ready for Review - {datetime.now().strftime('%B %d, %Y')}"

        for email in self.team_emails:
            if not email.strip():
                continue

            self.send_email(email.strip(), subject, summary)

    def create_distribution_summary(self, documents):
        """Create summary email for content distribution"""
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

        summary = f"""

📄 **Content Distribution Report**
📅 Generated: {timestamp}

## 🎯 New Content Created

"""

        for i, doc in enumerate(documents, 1):
            summary += f"""

### {i}. {doc['title']}

**Type**: {doc['type'].replace('\_', ' ').title()}
**Document**: [View in Google Docs]({doc['doc_url']})
**Status**: Ready for review

"""

        summary += f"""

## 📋 Next Steps

### Content Review Process

1. **Review & Edit**: Check each document for accuracy and style
2. **SEO Optimization**: Ensure keywords and metadata are optimized
3. **Visual Assets**: Add images, charts, or graphics as needed
4. **Publication Schedule**: Assign publication dates and platforms
5. **Promotion Plan**: Develop distribution and promotion strategy

### Distribution Checklist

- [ ] Content quality review completed
- [ ] SEO keywords optimized
- [ ] Visual assets added
- [ ] Publication schedule set
- [ ] Social media promotion planned
- [ ] Email newsletter integration
- [ ] Website/blog publication ready

## 📊 Content Portfolio Summary

**Total Documents**: {len(documents)}
**Content Types**: {', '.join(set(doc['type'].replace('\_', ' ').title() for doc in documents))}
**Ready for Publication**: {len(documents)}

## 🔗 Quick Access Links

"""

        for doc in documents:
            summary += f"- [{doc['title']}]({doc['doc_url']})\n"

        summary += """

---

🤖 **Generated by Incredible Content Distribution Agent**
_This content was researched, created, and organized automatically_

For questions or modifications, please review the documents and reply to this email.
"""

        return summary

    def send_email(self, recipient, subject, body):
        """Send email via Gmail integration"""
        url = f"{self.base_url}/v1/integrations/gmail/execute"

        data = {
            "user_id": self.user_id,
            "feature_name": "GMAIL_SEND_EMAIL",
            "inputs": {
                "to": recipient,
                "subject": subject,
                "body": body
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                print(f"✅ Content summary sent to {recipient}")
                return True
            else:
                print(f"❌ Failed to send to {recipient}: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Email error for {recipient}: {e}")
            return False

    def run_content_workflow(self, focus_areas=None):
        """Execute complete content creation and distribution workflow"""
        focus_areas = focus_areas or self.content_topics

        print("🚀 Starting Content Distribution Workflow")
        print(f"📁 Content Folder: {self.folder_id}")
        print(f"📧 Distribution List: {', '.join(self.team_emails)}")
        print(f"🎯 Focus Areas: {', '.join(focus_areas)}")
        print()

        all_research = []
        all_opportunities = []
        created_documents = []

        # Research each focus area
        for area in focus_areas:
            research_results = self.research_trending_topics(area)
            all_research.extend(research_results)

            # Analyze opportunities for this area
            opportunities = self.analyze_content_opportunities(research_results)
            all_opportunities.extend(opportunities)

        if not all_opportunities:
            print("❌ No content opportunities identified")
            return False

        print(f"💡 Identified {len(all_opportunities)} content opportunities")

        # Create content for top opportunities
        for opportunity in all_opportunities[:3]:  # Create top 3 pieces
            document = self.create_content_document(opportunity)
            if document:
                created_documents.append(document)

        # Distribute content
        if created_documents:
            self.distribute_content(created_documents)

        # Summary
        print(f"\n🎉 Content Workflow Complete!")
        print(f"🔍 Research queries executed: {len(all_research)}")
        print(f"💡 Content opportunities identified: {len(all_opportunities)}")
        print(f"📄 Documents created: {len(created_documents)}")
        print(f"📧 Distribution emails sent: {len([e for e in self.team_emails if e.strip()])}")

        if created_documents:
            print(f"\n📁 Created Content:")
            for doc in created_documents:
                print(f"  - {doc['title']}: {doc['doc_url']}")

        return True

# Usage Examples

if **name** == "**main**":
content_agent = ContentDistribution()

    # Run complete workflow for default topics
    content_agent.run_content_workflow()

    print("\n" + "="*50 + "\n")

    # Run workflow for specific focus areas
    content_agent.run_content_workflow(focus_areas=["AI", "marketing", "business"])

    print("\n" + "="*50 + "\n")

    # Research specific topic only
    research = content_agent.research_trending_topics("artificial intelligence")
    opportunities = content_agent.analyze_content_opportunities(research)
    print(f"🔍 Found {len(opportunities)} AI content opportunities")
    for opp in opportunities:
        print(f"  - {opp['title']} ({opp['type']})")</code></pre>

  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">const axios = require("axios");
require("dotenv").config();

class ContentDistribution {
constructor() {
this.apiKey = process.env.INCREDIBLE_API_KEY;
this.baseUrl = process.env.INCREDIBLE_BASE_URL || "https://api.incredible.one";
this.userId = process.env.USER_ID;
this.folderId = process.env.CONTENT_FOLDER_ID;
this.teamEmails = (process.env.CONTENT_TEAM_EMAILS || '').split(',');

    this.contentTopics = (process.env.CONTENT_TOPICS || 'AI,technology').split(',');
    this.contentTypes = (process.env.CONTENT_TYPES || 'blog_post,social_media').split(',');
    this.targetAudience = (process.env.TARGET_AUDIENCE || 'professionals').split(',');

    this.headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${this.apiKey}`,
    };

}

async researchTrendingTopics(focusArea = "technology") {
console.log(`🔍 Researching trending topics in ${focusArea}...`);

    const researchQueries = [
      `trending ${focusArea} topics 2024 latest developments`,
      `popular ${focusArea} discussions social media today`,
      `${focusArea} industry news breaking developments`,
      `viral ${focusArea} content ideas engagement trends`,
      `${focusArea} thought leadership trending discussions`
    ];

    const researchResults = [];

    for (const query of researchQueries) {
      const result = await this.executePerplexitySearch(query);
      researchResults.push({
        query: query,
        findings: result,
        focus_area: focusArea,
        timestamp: new Date().toISOString()
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
        return response.data.result?.answer || 'No results found';
      } else {
        return `Research failed: ${response.data}`;
      }
    } catch (error) {
      return `Error: ${error.message}`;
    }

}

analyzeContentOpportunities(researchResults) {
console.log("📊 Analyzing content opportunities...");

    const opportunities = [];

    for (const result of researchResults) {
      const findings = result.findings;
      const contentIdeas = [];

      const trendingKeywords = this.extractTrendingKeywords(findings);

      // Generate content ideas based on findings
      if (findings.includes('AI') || findings.toLowerCase().includes('artificial intelligence')) {
        contentIdeas.push({
          type: 'blog_post',
          title: `The Future of AI in ${result.focus_area.charAt(0).toUpperCase() + result.focus_area.slice(1)}`,
          angle: 'thought_leadership',
          keywords: trendingKeywords,
          urgency: 'high'
        });
      }

      if (findings.toLowerCase().includes('trend') || findings.toLowerCase().includes('popular')) {
        contentIdeas.push({
          type: 'social_media',
          title: `5 ${result.focus_area.charAt(0).toUpperCase() + result.focus_area.slice(1)} Trends You Can't Ignore`,
          angle: 'list_format',
          keywords: trendingKeywords,
          urgency: 'medium'
        });
      }

      if (findings.toLowerCase().includes('breakthrough') || findings.toLowerCase().includes('innovation')) {
        contentIdeas.push({
          type: 'newsletter',
          title: `Innovation Spotlight: ${result.focus_area.charAt(0).toUpperCase() + result.focus_area.slice(1)} Breakthroughs`,
          angle: 'news_analysis',
          keywords: trendingKeywords,
          urgency: 'high'
        });
      }

      for (const idea of contentIdeas) {
        idea.research_source = result.query;
        idea.supporting_data = findings.length > 200 ? findings.substring(0, 200) + '...' : findings;
        idea.focus_area = result.focus_area;
        opportunities.push(idea);
      }
    }

    // Sort by urgency and potential impact
    opportunities.sort((a, b) => {
      const urgencyMap = { high: 3, medium: 2, low: 1 };
      return urgencyMap[b.urgency] - urgencyMap[a.urgency];
    });

    return opportunities.slice(0, 5); // Return top 5 opportunities

}

extractTrendingKeywords(text) {
const commonWords = new Set(['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should']);

    const words = text.toLowerCase().split(/\s+/);
    const keywords = words
      .map(word => word.replace(/[.,!?;:"()\[\]]/g, ''))
      .filter(word => word.length > 3 && !commonWords.has(word));

    // Count word frequency
    const wordCounts = {};
    keywords.forEach(word => {
      wordCounts[word] = (wordCounts[word] || 0) + 1;
    });

    // Return most frequent keywords
    return Object.keys(wordCounts)
      .sort((a, b) => wordCounts[b] - wordCounts[a])
      .slice(0, 10);

}

async createContentDocument(contentIdea) {
console.log(`📄 Creating content: ${contentIdea.title}`);

    const contentDraft = this.generateContentDraft(contentIdea);

    const url = `${this.baseUrl}/v1/integrations/google_docs/execute`;

    const data = {
      user_id: this.userId,
      feature_name: "create_document",
      inputs: {
        title: contentIdea.title,
        content: contentDraft,
        folder_id: this.folderId
      }
    };

    try {
      const response = await axios.post(url, data, { headers: this.headers });
      if (response.status === 200) {
        const docId = response.data.result?.document_id;
        const docUrl = `https://docs.google.com/document/d/${docId}`;
        console.log(`✅ Document created: ${docUrl}`);
        return {
          doc_id: docId,
          doc_url: docUrl,
          title: contentIdea.title,
          type: contentIdea.type
        };
      } else {
        console.log(`❌ Document creation failed: ${response.data}`);
        return null;
      }
    } catch (error) {
      console.log(`❌ Document error: ${error.message}`);
      return null;
    }

}

generateContentDraft(contentIdea) {
const timestamp = new Date().toLocaleDateString('en-US', {
year: 'numeric',
month: 'long',
day: 'numeric'
});

    if (contentIdea.type === 'blog_post') {
      return `# ${contentIdea.title}

_Published: ${timestamp}_
_Keywords: ${(contentIdea.keywords || []).slice(0, 5).join(', ')}_

## Introduction

${contentIdea.supporting_data}

## Key Points to Explore

1. **Current State Analysis**

   - Market overview and trends
   - Key players and developments
   - Challenges and opportunities

2. **Future Implications**

   - Predicted outcomes and impacts
   - Strategic considerations
   - Actionable insights

3. **Expert Perspectives**
   - Industry expert opinions
   - Case studies and examples
   - Best practices and recommendations

## Supporting Research

**Source**: ${contentIdea.research_source}

**Key Findings**: ${contentIdea.supporting_data}

## Next Steps

- [ ] Add detailed research and citations
- [ ] Include relevant statistics and data
- [ ] Add expert quotes and interviews
- [ ] Optimize for SEO with target keywords
- [ ] Create compelling visuals and graphics
- [ ] Review and edit for publication

---

_Draft created by Incredible Content Distribution Agent_
_Research conducted on ${timestamp}_
`;
    } else if (contentIdea.type === 'social_media') {
      return `# ${contentIdea.title} - Social Media Content

_Created: ${timestamp}_

## Main Post Content

🚀 **${contentIdea.title}**

Based on the latest research, here are the key developments:

${contentIdea.supporting_data.substring(0, 150)}...

What trends are you seeing in your industry? Share your thoughts! 👇

#${(contentIdea.keywords || []).slice(0, 3).join(' #')}

## Alternative Versions

**LinkedIn Version:**
Professional take with industry insights and discussion prompts

**Twitter Version:**
Concise thread format with key statistics and engaging questions

**Instagram Version:**
Visual storytelling with infographic potential

## Engagement Strategy

- Best posting times: [Add optimal times for each platform]
- Target hashtags: #${(contentIdea.keywords || []).join(' #')}
- Call-to-action: Encourage discussion and sharing
- Follow-up content: Plan series or continuation posts

## Performance Tracking

- [ ] Monitor engagement rates
- [ ] Track hashtag performance
- [ ] Analyze audience response
- [ ] Iterate based on feedback

---

_Generated by Incredible Content Distribution Agent_
`;
    } else { // newsletter
      return `# ${contentIdea.title} - Newsletter

_Issue Date: ${timestamp}_

## Subject Line Options

1. ${contentIdea.title}
2. Breaking: Latest Developments in ${(contentIdea.focus_area || 'Technology').charAt(0).toUpperCase() + (contentIdea.focus_area || 'Technology').slice(1)}
3. Weekly Roundup: What's Trending Now

## Newsletter Content

**Hello [Subscriber Name],**

Hope you're having a great week! Here's what's capturing attention in ${contentIdea.focus_area || 'our industry'} right now:

### 🔥 Trending This Week

${contentIdea.supporting_data}

### 💡 Key Takeaways

- [Add 3-5 bullet points of key insights]
- [Include actionable advice]
- [Highlight important developments]

### 📚 Worth Reading

- [Curated list of relevant articles]
- [Industry reports and studies]
- [Expert opinions and analysis]

### 🚀 What's Next

Looking ahead, keep an eye on:

- [Upcoming developments]
- [Important dates and events]
- [Emerging trends to watch]

---

**Thank you for reading!**

Best regards,
[Your Name]

P.S. What topics would you like us to cover next? Reply and let us know!

---

_Unsubscribe | Update Preferences | Forward to a Friend_
_Generated by Incredible Content Distribution Agent_
`;
}
}

async distributeContent(documents) {
console.log("📧 Distributing content to stakeholders...");

    if (!documents || documents.length === 0) {
      console.log("❌ No documents to distribute");
      return;
    }

    const summary = this.createDistributionSummary(documents);
    const subject = `New Content Ready for Review - ${new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })}`;

    for (const email of this.teamEmails) {
      if (!email.trim()) continue;
      await this.sendEmail(email.trim(), subject, summary);
    }

}

createDistributionSummary(documents) {
const timestamp = new Date().toLocaleDateString('en-US', {
year: 'numeric',
month: 'long',
day: 'numeric',
hour: 'numeric',
minute: '2-digit'
});

    let summary = `

📄 **Content Distribution Report**
📅 Generated: ${timestamp}

## 🎯 New Content Created

`;

    documents.forEach((doc, index) => {
      summary += `

### ${index + 1}. ${doc.title}

**Type**: ${doc.type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
**Document**: [View in Google Docs](${doc.doc_url})
**Status**: Ready for review

`;
});

    summary += `

## 📋 Next Steps

### Content Review Process

1. **Review & Edit**: Check each document for accuracy and style
2. **SEO Optimization**: Ensure keywords and metadata are optimized
3. **Visual Assets**: Add images, charts, or graphics as needed
4. **Publication Schedule**: Assign publication dates and platforms
5. **Promotion Plan**: Develop distribution and promotion strategy

### Distribution Checklist

- [ ] Content quality review completed
- [ ] SEO keywords optimized
- [ ] Visual assets added
- [ ] Publication schedule set
- [ ] Social media promotion planned
- [ ] Email newsletter integration
- [ ] Website/blog publication ready

## 📊 Content Portfolio Summary

**Total Documents**: ${documents.length}
**Content Types**: ${[...new Set(documents.map(doc => doc.type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())))].join(', ')}
**Ready for Publication**: ${documents.length}

## 🔗 Quick Access Links

`;

    documents.forEach(doc => {
      summary += `- [${doc.title}](${doc.doc_url})\n`;
    });

    summary += `

---

🤖 **Generated by Incredible Content Distribution Agent**
_This content was researched, created, and organized automatically_

For questions or modifications, please review the documents and reply to this email.
`;

    return summary;

}

async sendEmail(recipient, subject, body) {
const url = `${this.baseUrl}/v1/integrations/gmail/execute`;

    const data = {
      user_id: this.userId,
      feature_name: "GMAIL_SEND_EMAIL",
      inputs: {
        to: recipient,
        subject: subject,
        body: body
      }
    };

    try {
      const response = await axios.post(url, data, { headers: this.headers });
      if (response.status === 200) {
        console.log(`✅ Content summary sent to ${recipient}`);
        return true;
      } else {
        console.log(`❌ Failed to send to ${recipient}: ${response.data}`);
        return false;
      }
    } catch (error) {
      console.log(`❌ Email error for ${recipient}: ${error.message}`);
      return false;
    }

}

async runContentWorkflow(focusAreas = null) {
const areas = focusAreas || this.contentTopics;

    console.log("🚀 Starting Content Distribution Workflow");
    console.log(`📁 Content Folder: ${this.folderId}`);
    console.log(`📧 Distribution List: ${this.teamEmails.join(', ')}`);
    console.log(`🎯 Focus Areas: ${areas.join(', ')}`);
    console.log();

    const allResearch = [];
    const allOpportunities = [];
    const createdDocuments = [];

    // Research each focus area
    for (const area of areas) {
      const researchResults = await this.researchTrendingTopics(area);
      allResearch.push(...researchResults);

      const opportunities = this.analyzeContentOpportunities(researchResults);
      allOpportunities.push(...opportunities);
    }

    if (allOpportunities.length === 0) {
      console.log("❌ No content opportunities identified");
      return false;
    }

    console.log(`💡 Identified ${allOpportunities.length} content opportunities`);

    // Create content for top opportunities
    for (const opportunity of allOpportunities.slice(0, 3)) {
      const document = await this.createContentDocument(opportunity);
      if (document) {
        createdDocuments.push(document);
      }
    }

    // Distribute content
    if (createdDocuments.length > 0) {
      await this.distributeContent(createdDocuments);
    }

    // Summary
    console.log(`\n🎉 Content Workflow Complete!`);
    console.log(`🔍 Research queries executed: ${allResearch.length}`);
    console.log(`💡 Content opportunities identified: ${allOpportunities.length}`);
    console.log(`📄 Documents created: ${createdDocuments.length}`);
    console.log(`📧 Distribution emails sent: ${this.teamEmails.filter(e => e.trim()).length}`);

    if (createdDocuments.length > 0) {
      console.log(`\n📁 Created Content:`);
      createdDocuments.forEach(doc => {
        console.log(`  - ${doc.title}: ${doc.doc_url}`);
      });
    }

    return true;

}
}

// Usage Examples
async function main() {
const contentAgent = new ContentDistribution();

// Run complete workflow for default topics
await contentAgent.runContentWorkflow();

console.log("\n" + "=".repeat(50) + "\n");

// Run workflow for specific focus areas
await contentAgent.runContentWorkflow(["AI", "marketing", "business"]);

console.log("\n" + "=".repeat(50) + "\n");

// Research specific topic only
const research = await contentAgent.researchTrendingTopics("artificial intelligence");
const opportunities = contentAgent.analyzeContentOpportunities(research);
console.log(`🔍 Found ${opportunities.length} AI content opportunities`);
opportunities.forEach(opp => {
console.log(`  - ${opp.title} (${opp.type})`);
});
}

if (require.main === module) {
main().catch(console.error);
}

module.exports = ContentDistribution;</code></pre>

  </div>
</div>

## 🎯 **Usage Examples**

### Daily Content Creation

```bash
# Generate daily content for social media
python content_distribution.py --type social_media --focus technology
```

### Weekly Newsletter

```bash
# Create comprehensive weekly newsletter
node contentDistribution.js --type newsletter --research-depth extensive
```

### Blog Series Generation

```bash
# Generate multiple blog posts on trending topics
python content_distribution.py --type blog_post --count 3 --focus "AI,business"
```

## 📊 **Expected Output**

```
🚀 Starting Content Distribution Workflow
📁 Content Folder: 1BcD3FgHiJkLmNoPqRsTuVwXyZ
📧 Distribution List: editor@company.com, marketing@company.com
🎯 Focus Areas: AI, technology, business

🔍 Researching trending topics in AI...
🔍 Researching trending topics in technology...
🔍 Researching trending topics in business...

📊 Analyzing content opportunities...
💡 Identified 8 content opportunities

📄 Creating content: The Future of AI in Technology
✅ Document created: https://docs.google.com/document/d/doc_abc123

📄 Creating content: 5 Business Trends You Can't Ignore
✅ Document created: https://docs.google.com/document/d/doc_def456

📄 Creating content: Innovation Spotlight: AI Breakthroughs
✅ Document created: https://docs.google.com/document/d/doc_ghi789

📧 Distributing content to stakeholders...
✅ Content summary sent to editor@company.com
✅ Content summary sent to marketing@company.com

🎉 Content Workflow Complete!
🔍 Research queries executed: 15
💡 Content opportunities identified: 8
📄 Documents created: 3
📧 Distribution emails sent: 2

📁 Created Content:
  - The Future of AI in Technology: https://docs.google.com/document/d/doc_abc123
  - 5 Business Trends You Can't Ignore: https://docs.google.com/document/d/doc_def456
  - Innovation Spotlight: AI Breakthroughs: https://docs.google.com/document/d/doc_ghi789
```

## 🔧 **Customization Options**

### Content Types

- **📝 Blog Posts**: Long-form thought leadership content
- **📱 Social Media**: Platform-optimized posts and threads
- **📧 Newsletters**: Curated industry insights and updates
- **📊 Reports**: Data-driven analysis and whitepapers

### Research Sources

- **🔍 Trend Analysis**: Social media and search trend monitoring
- **📰 News Monitoring**: Breaking industry developments
- **🎯 Competitor Analysis**: Content gap identification
- **📈 Performance Data**: Content engagement analytics

### Distribution Channels

- **📧 Email Distribution**: Stakeholder and team notifications
- **💬 Slack Integration**: Real-time content alerts
- **📱 Mobile Notifications**: Urgent content opportunities
- **📊 Dashboard Updates**: Content pipeline tracking

## 🛡 **Best Practices**

1. **🔍 Research Quality**: Verify sources and validate trending topics
2. **✍️ Content Standards**: Maintain consistent voice and quality
3. **⏰ Timing**: Align creation with optimal publishing schedules
4. **📊 Performance**: Track engagement and iterate based on data

## 🚀 **Advanced Features**

### AI-Powered Optimization

- **🤖 Content Personalization**: Audience-specific content variations
- **📊 Performance Prediction**: ML-based engagement forecasting
- **🎯 SEO Optimization**: Automated keyword and metadata optimization

### Workflow Automation

- **📅 Scheduled Creation**: Automated content generation schedules
- **🔄 Continuous Research**: Real-time trend monitoring and alerting
- **📈 Analytics Integration**: Performance tracking and optimization

---

_This content distribution agent eliminates manual research and creation tasks, delivering high-quality, timely content that engages your audience and drives results._
