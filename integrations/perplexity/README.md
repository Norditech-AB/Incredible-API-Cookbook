# Perplexity AI Integration Guide

Complete guide to integrating Perplexity AI with Incredible API for intelligent web search, research automation, and real-time information gathering.

## 🔍 **Perplexity AI Integration Overview**

The Perplexity AI integration allows your agents to:
- **🌐 Search the Web**: Access real-time information from across the internet
- **📊 Research Topics**: Conduct comprehensive research on any subject
- **📈 Market Analysis**: Gather current market data and trends
- **📰 News Monitoring**: Stay updated with latest developments
- **🎯 Fact Checking**: Verify information with current sources

## 🔐 **Authentication Setup**

Perplexity AI uses API key authentication for secure access.

### 1. **API Key Configuration**

<div class="code-tabs" data-section="perplexity-auth">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python">import requests

def connect_perplexity(api_key):
    """Connect Perplexity AI integration"""
    url = "https://api.incredible.one/v1/integrations/perplexity/connect"
    
    data = {
        "user_id": "your_user_id",
        "api_key": api_key
    }
    
    response = requests.post(url, json=data, headers={
        "Authorization": "Bearer YOUR_INCREDIBLE_API_KEY"
    })
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Perplexity AI connected successfully!")
        return result
    else:
        print(f"❌ Connection failed: {response.text}")
        return None

# Usage
perplexity_api_key = "pplx-your-api-key-here"
connect_perplexity(perplexity_api_key)</code></pre>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">const axios = require('axios');

async function connectPerplexity(apiKey) {
    // Connect Perplexity AI integration
    const url = "https://api.incredible.one/v1/integrations/perplexity/connect";
    
    const data = {
        user_id: "your_user_id",
        api_key: apiKey
    };
    
    try {
        const response = await axios.post(url, data, {
            headers: {
                "Authorization": "Bearer YOUR_INCREDIBLE_API_KEY"
            }
        });
        
        console.log("✅ Perplexity AI connected successfully!");
        return response.data;
    } catch (error) {
        console.log("❌ Connection failed:", error.response?.data);
        return null;
    }
}

// Usage
const perplexityApiKey = "pplx-your-api-key-here";
await connectPerplexity(perplexityApiKey);</code></pre>
  </div>
</div>

### 2. **Environment Setup**

```bash
# Add to your .env file
PERPLEXITY_API_KEY=pplx-your-api-key-here
INCREDIBLE_API_KEY=your-incredible-api-key
USER_ID=your-user-id
```

## 🛠️ **Available Features**

### 🔍 **Web Search & Research**

<div class="code-tabs" data-section="perplexity-search">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python">def search_perplexity(query, focus=None):
    """Search using Perplexity AI"""
    url = "https://api.incredible.one/v1/integrations/perplexity/execute"
    
    data = {
        "user_id": "your_user_id",
        "feature_name": "PerplexityAISearch",
        "inputs": {
            "query": query,
            "focus": focus  # Optional: 'academic', 'writing', 'wolfram', 'youtube', 'reddit'
        }
    }
    
    response = requests.post(url, json=data, headers={
        "Authorization": "Bearer YOUR_API_KEY"
    })
    
    if response.status_code == 200:
        result = response.json()
        answer = result['result']['answer']
        sources = result['result'].get('sources', [])
        
        print(f"Answer: {answer}")
        print(f"Sources: {len(sources)} references")
        return {
            'answer': answer,
            'sources': sources,
            'query': query
        }
    else:
        print(f"Search failed: {response.text}")
        return None

# Usage examples
# General web search
result = search_perplexity("What are the latest AI trends in 2024?")

# Academic focus
academic_result = search_perplexity(
    "Machine learning applications in healthcare", 
    focus="academic"
)

# Reddit discussions
social_result = search_perplexity(
    "Best programming languages for beginners reddit",
    focus="reddit"
)

# Financial research
finance_result = search_perplexity("Tesla stock performance Q4 2024 earnings")</code></pre>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">async function searchPerplexity(query, focus = null) {
    // Search using Perplexity AI
    const url = "https://api.incredible.one/v1/integrations/perplexity/execute";
    
    const data = {
        user_id: "your_user_id",
        feature_name: "PerplexityAISearch",
        inputs: {
            query: query,
            focus: focus  // Optional: 'academic', 'writing', 'wolfram', 'youtube', 'reddit'
        }
    };
    
    try {
        const response = await axios.post(url, data, {
            headers: {
                "Authorization": "Bearer YOUR_API_KEY"
            }
        });
        
        const answer = response.data.result.answer;
        const sources = response.data.result.sources || [];
        
        console.log(`Answer: ${answer}`);
        console.log(`Sources: ${sources.length} references`);
        
        return {
            answer: answer,
            sources: sources,
            query: query
        };
    } catch (error) {
        console.log("Search failed:", error.response?.data);
        return null;
    }
}

// Usage examples
// General web search
const result = await searchPerplexity("What are the latest AI trends in 2024?");

// Academic focus
const academicResult = await searchPerplexity(
    "Machine learning applications in healthcare", 
    "academic"
);

// Reddit discussions
const socialResult = await searchPerplexity(
    "Best programming languages for beginners reddit",
    "reddit"
);

// Financial research
const financeResult = await searchPerplexity("Tesla stock performance Q4 2024 earnings");</code></pre>
  </div>
</div>

### 📊 **Research Automation**

<div class="code-tabs" data-section="perplexity-research">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python">class PerplexityResearcher:
    def __init__(self):
        self.base_url = "https://api.incredible.one"
        
    def comprehensive_research(self, topic, aspects=None):
        """Conduct comprehensive research on a topic"""
        if aspects is None:
            aspects = ["overview", "current_trends", "challenges", "opportunities", "future_outlook"]
        
        research_results = {}
        
        for aspect in aspects:
            query = f"{topic} {aspect} 2024"
            result = search_perplexity(query)
            
            if result:
                research_results[aspect] = {
                    'content': result['answer'],
                    'sources': result['sources'],
                    'query': query
                }
                
                # Add delay to respect rate limits
                time.sleep(1)
        
        return research_results
    
    def competitive_analysis(self, company, competitors):
        """Analyze company against competitors"""
        analysis = {}
        
        # Research main company
        company_info = search_perplexity(f"{company} business model revenue strategy 2024")
        analysis[company] = company_info
        
        # Research competitors
        for competitor in competitors:
            competitor_info = search_perplexity(f"{competitor} vs {company} comparison market share")
            analysis[competitor] = competitor_info
            time.sleep(1)
        
        return analysis
    
    def market_trends_research(self, industry, timeframe="2024"):
        """Research market trends for specific industry"""
        trend_queries = [
            f"{industry} market trends {timeframe}",
            f"{industry} growth opportunities {timeframe}",
            f"{industry} challenges disruption {timeframe}",
            f"{industry} investment funding {timeframe}",
            f"{industry} regulatory changes {timeframe}"
        ]
        
        trends = {}
        for i, query in enumerate(trend_queries):
            result = search_perplexity(query)
            if result:
                trends[f"trend_{i+1}"] = result
            time.sleep(1)
        
        return trends

# Usage examples
researcher = PerplexityResearcher()

# Comprehensive topic research
ai_research = researcher.comprehensive_research("Artificial Intelligence in Healthcare")

# Competitive analysis
competitor_analysis = researcher.competitive_analysis(
    "OpenAI", 
    ["Anthropic", "Google AI", "Microsoft AI"]
)

# Market trends
fintech_trends = researcher.market_trends_research("Fintech")</code></pre>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">class PerplexityResearcher {
    constructor() {
        this.baseUrl = "https://api.incredible.one";
    }
    
    async comprehensiveResearch(topic, aspects = null) {
        // Conduct comprehensive research on a topic
        if (!aspects) {
            aspects = ["overview", "current_trends", "challenges", "opportunities", "future_outlook"];
        }
        
        const researchResults = {};
        
        for (const aspect of aspects) {
            const query = `${topic} ${aspect} 2024`;
            const result = await searchPerplexity(query);
            
            if (result) {
                researchResults[aspect] = {
                    content: result.answer,
                    sources: result.sources,
                    query: query
                };
                
                // Add delay to respect rate limits
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
        }
        
        return researchResults;
    }
    
    async competitiveAnalysis(company, competitors) {
        // Analyze company against competitors
        const analysis = {};
        
        // Research main company
        const companyInfo = await searchPerplexity(`${company} business model revenue strategy 2024`);
        analysis[company] = companyInfo;
        
        // Research competitors
        for (const competitor of competitors) {
            const competitorInfo = await searchPerplexity(`${competitor} vs ${company} comparison market share`);
            analysis[competitor] = competitorInfo;
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
        
        return analysis;
    }
    
    async marketTrendsResearch(industry, timeframe = "2024") {
        // Research market trends for specific industry
        const trendQueries = [
            `${industry} market trends ${timeframe}`,
            `${industry} growth opportunities ${timeframe}`,
            `${industry} challenges disruption ${timeframe}`,
            `${industry} investment funding ${timeframe}`,
            `${industry} regulatory changes ${timeframe}`
        ];
        
        const trends = {};
        for (let i = 0; i < trendQueries.length; i++) {
            const result = await searchPerplexity(trendQueries[i]);
            if (result) {
                trends[`trend_${i + 1}`] = result;
            }
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
        
        return trends;
    }
}

// Usage examples
const researcher = new PerplexityResearcher();

// Comprehensive topic research
const aiResearch = await researcher.comprehensiveResearch("Artificial Intelligence in Healthcare");

// Competitive analysis
const competitorAnalysis = await researcher.competitiveAnalysis(
    "OpenAI", 
    ["Anthropic", "Google AI", "Microsoft AI"]
);

// Market trends
const fintechTrends = await researcher.marketTrendsResearch("Fintech");</code></pre>
  </div>
</div>

## 🎯 **Search Focus Options**

Perplexity AI offers specialized search focuses for different types of information:

### 📚 **Academic Focus**
- **Best for**: Research papers, scholarly articles, academic insights
- **Usage**: `focus="academic"`
- **Example**: Scientific studies, research findings, academic analysis

### ✍️ **Writing Focus**  
- **Best for**: Content creation, writing assistance, style guides
- **Usage**: `focus="writing"`
- **Example**: Writing tips, grammar help, content structure

### 🧮 **Wolfram Focus**
- **Best for**: Mathematical calculations, data analysis, computational queries
- **Usage**: `focus="wolfram"`
- **Example**: Complex calculations, data visualization, statistical analysis

### 🎥 **YouTube Focus**
- **Best for**: Video content, tutorials, entertainment information
- **Usage**: `focus="youtube"`
- **Example**: How-to videos, product reviews, educational content

### 💬 **Reddit Focus**
- **Best for**: Community discussions, opinions, user experiences
- **Usage**: `focus="reddit"`
- **Example**: User reviews, community insights, discussion threads

## 🎯 **Common Use Cases**

### 📈 **Market Research**

```python
def market_intelligence_report(industry, competitors=None):
    """Generate comprehensive market intelligence report"""
    
    # Industry overview
    industry_overview = search_perplexity(f"{industry} market size growth trends 2024")
    
    # Key players
    key_players = search_perplexity(f"top companies {industry} market leaders 2024")
    
    # Recent developments
    recent_news = search_perplexity(f"{industry} latest news developments 2024")
    
    # Investment trends
    investment_trends = search_perplexity(f"{industry} investment funding trends venture capital 2024")
    
    # Compile report
    report = {
        "industry": industry,
        "overview": industry_overview,
        "key_players": key_players,
        "recent_developments": recent_news,
        "investment_trends": investment_trends,
        "generated_at": datetime.now().isoformat()
    }
    
    if competitors:
        report["competitive_analysis"] = {}
        for competitor in competitors:
            competitor_info = search_perplexity(f"{competitor} {industry} strategy performance 2024")
            report["competitive_analysis"][competitor] = competitor_info
    
    return report

# Generate market report
fintech_report = market_intelligence_report(
    "fintech", 
    ["Square", "Stripe", "PayPal", "Klarna"]
)
```

### 📰 **News Monitoring**

```python
class NewsMonitor:
    def __init__(self, topics):
        self.topics = topics
        self.last_check = datetime.now()
    
    def check_breaking_news(self):
        """Check for breaking news on monitored topics"""
        breaking_news = []
        
        for topic in self.topics:
            # Look for recent developments
            query = f"{topic} breaking news latest developments today"
            result = search_perplexity(query)
            
            if result and self.is_breaking_news(result['answer']):
                breaking_news.append({
                    'topic': topic,
                    'news': result['answer'],
                    'sources': result['sources'],
                    'timestamp': datetime.now()
                })
        
        return breaking_news
    
    def is_breaking_news(self, content):
        """Determine if content represents breaking news"""
        breaking_indicators = [
            'breaking', 'just announced', 'developing story',
            'urgent', 'latest update', 'just in'
        ]
        
        return any(indicator in content.lower() for indicator in breaking_indicators)
    
    def get_trending_topics(self, category="technology"):
        """Get currently trending topics"""
        query = f"trending {category} topics news today viral"
        result = search_perplexity(query, focus="reddit")
        
        return result

# Monitor news for specific topics
monitor = NewsMonitor(["AI", "Tesla", "Bitcoin", "Climate Change"])
breaking_news = monitor.check_breaking_news()
trending_tech = monitor.get_trending_topics("technology")
```

### 🔍 **Fact Checking & Verification**

```python
def verify_claim(claim, sources_required=3):
    """Verify a claim using multiple sources"""
    
    # Search for information about the claim
    verification_query = f"fact check verify: {claim}"
    result = search_perplexity(verification_query, focus="academic")
    
    if not result:
        return {"status": "error", "message": "Unable to search for verification"}
    
    # Analyze the response for verification indicators
    answer = result['answer'].lower()
    sources = result['sources']
    
    # Look for verification language
    if any(word in answer for word in ['true', 'correct', 'confirmed', 'verified']):
        status = "likely_true"
    elif any(word in answer for word in ['false', 'incorrect', 'debunked', 'misleading']):
        status = "likely_false"
    elif any(word in answer for word in ['unclear', 'disputed', 'mixed', 'partial']):
        status = "disputed"
    else:
        status = "inconclusive"
    
    return {
        "claim": claim,
        "status": status,
        "verification_info": result['answer'],
        "sources": sources,
        "source_count": len(sources),
        "sufficient_sources": len(sources) >= sources_required,
        "verified_at": datetime.now().isoformat()
    }

# Verify various claims
climate_claim = verify_claim("Global temperatures have increased by 1.1°C since pre-industrial times")
tech_claim = verify_claim("ChatGPT has over 100 million users")
business_claim = verify_claim("Tesla delivered 1.8 million vehicles in 2023")
```

## 🔒 **Security & Best Practices**

### 🛡️ **API Security**
- **Key Protection**: Store API keys securely and never expose in code
- **Rate Limiting**: Respect Perplexity's rate limits (varies by plan)
- **Error Handling**: Handle API errors and network issues gracefully
- **Usage Monitoring**: Track API usage to avoid exceeding quotas

### 📊 **Search Optimization**
- **Query Quality**: Use specific, well-formed search queries
- **Source Verification**: Always review sources for credibility
- **Content Freshness**: Consider recency requirements for time-sensitive topics
- **Result Validation**: Cross-reference important information

### 💡 **Best Practices**
- **Clear Queries**: Write clear, specific search queries for better results
- **Source Checking**: Review provided sources for reliability
- **Rate Limiting**: Add delays between requests to avoid hitting limits
- **Error Recovery**: Implement retry logic for failed requests

## 📈 **Advanced Features**

### 🔄 **Automated Research Workflows**

```python
def automated_research_pipeline(topic, output_format="markdown"):
    """Automated research pipeline with multiple phases"""
    
    pipeline_results = {}
    
    # Phase 1: Overview research
    overview = search_perplexity(f"{topic} comprehensive overview 2024")
    pipeline_results["overview"] = overview
    
    # Phase 2: Current state analysis
    current_state = search_perplexity(f"{topic} current state market analysis")
    pipeline_results["current_state"] = current_state
    
    # Phase 3: Future trends
    future_trends = search_perplexity(f"{topic} future trends predictions 2025")
    pipeline_results["future_trends"] = future_trends
    
    # Phase 4: Expert opinions
    expert_opinions = search_perplexity(f"{topic} expert opinions analysis", focus="academic")
    pipeline_results["expert_opinions"] = expert_opinions
    
    # Compile final report
    if output_format == "markdown":
        return compile_markdown_report(topic, pipeline_results)
    else:
        return pipeline_results

def compile_markdown_report(topic, results):
    """Compile research results into markdown report"""
    report = f"# Research Report: {topic}\n\n"
    
    for section, data in results.items():
        if data:
            report += f"## {section.replace('_', ' ').title()}\n\n"
            report += f"{data['answer']}\n\n"
            
            if data['sources']:
                report += "### Sources\n"
                for i, source in enumerate(data['sources'], 1):
                    report += f"{i}. {source}\n"
                report += "\n"
    
    return report
```

### 📊 **Analytics & Monitoring**

```python
def track_research_quality(results):
    """Track and analyze research quality metrics"""
    
    metrics = {
        "total_queries": len(results),
        "successful_queries": len([r for r in results if r is not None]),
        "total_sources": sum(len(r['sources']) for r in results if r),
        "average_sources_per_query": 0,
        "query_success_rate": 0
    }
    
    if metrics["successful_queries"] > 0:
        metrics["average_sources_per_query"] = metrics["total_sources"] / metrics["successful_queries"]
        metrics["query_success_rate"] = metrics["successful_queries"] / metrics["total_queries"]
    
    return metrics
```

---

*Harness the power of real-time web intelligence with Perplexity AI integration for comprehensive research, market analysis, and informed decision-making.*
