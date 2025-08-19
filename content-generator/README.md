# Content Generator

**AI-powered content creation system that researches topics and generates blog posts, social media content, and newsletters.**

## What it does

1. **Researches topics** using Perplexity AI with multiple targeted queries
2. **Analyzes content opportunities** to identify angles and themes
3. **Generates multi-format content**: blog posts, social media, newsletters
4. **Creates Google Docs** with professional formatting
5. **Distributes to team** via email notifications

## Quick Start

```bash
# 1. Clone and navigate
git clone [repo-url]
cd content-generator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up configuration
cp env.example .env
# Edit .env with your credentials

# 4. Generate content for a topic
python main.py "AI trends"

# 5. Generate content for multiple topics
python main.py "Machine Learning" "Remote Work Tools" "FinTech Innovations"
```

## Required Setup

### 1. Incredible API
- Get API key from [Incredible Dashboard](https://incredible.one)
- Connect Perplexity AI integration (API key)
- Connect Google Docs integration (OAuth)
- Connect Gmail integration (OAuth)

### 2. Google Drive Setup
- Create a folder in Google Drive for content storage
- Copy the folder ID from the URL
- Share folder with your Google account used for OAuth

### 3. Environment Variables
```bash
INCREDIBLE_API_KEY=your_api_key
USER_ID=your_user_id
CONTENT_FOLDER_ID=your_drive_folder_id
CONTENT_TEAM_EMAILS=content@company.com,marketing@company.com
CONTENT_TYPES=blog_post,social_media,newsletter
```

## Content Research Strategy

For each topic, the system generates 5 comprehensive research queries:

1. **Latest trends and developments** - Current industry news and updates
2. **Expert opinions and thought leadership** - Insights from industry leaders
3. **Case studies and success stories** - Real-world examples and applications
4. **Challenges and solutions** - Problems faced and how they're being solved
5. **Future predictions and outlook** - Where the industry is heading

## Generated Content Types

### Blog Posts
Comprehensive articles including:
- Introduction and current landscape
- Key findings from research
- Major themes and trends
- Expert perspectives
- Conclusions and takeaways
- Call-to-action and sources

### Social Media Content
Platform-optimized content:
- **LinkedIn**: Professional posts with key insights
- **Twitter**: Thread format with bite-sized information  
- **Instagram**: Visual-friendly captions with hashtags
- **Newsletter snippets**: Email-ready summaries

### Newsletter Content
Complete newsletter sections:
- Subject line options
- Introduction and greeting
- Main content with research highlights
- Expert insights section
- Looking ahead predictions
- Resources and reading links

## Expected Output

```
✍️  Incredible API - Content Generator
==================================================
✅ Content Generator initialized
📁 Content Folder: 1BcD3FgHiJkLmNoPqRsTuVwXyZ
📧 Team Emails: 2

============================================================
✍️  CONTENT GENERATION: AI trends
============================================================

🚀 Starting content research on: AI trends
🔍 Researching: AI trends latest trends developments 2024
🔍 Researching: AI trends expert opinions thought leadership
🔍 Researching: AI trends case studies success stories examples
🔍 Researching: AI trends challenges problems solutions industry
🔍 Researching: AI trends future predictions outlook trends
📋 Research complete: 5 sources gathered

📊 Analyzing content opportunities...
🎯 Analysis complete:
   Content angles: 5
   Key themes: 3

📄 Creating Google Doc: AI trends - Blog Post
✅ Document created: https://docs.google.com/document/d/abc123/edit
📄 Creating Google Doc: AI trends - Social Media Content
✅ Document created: https://docs.google.com/document/d/def456/edit
📄 Creating Google Doc: AI trends - Newsletter Content
✅ Document created: https://docs.google.com/document/d/ghi789/edit

📧 Sending content distribution email...
✅ Distribution email sent to: content@company.com
✅ Distribution email sent to: marketing@company.com

🎉 Content generation complete for: AI trends
📊 Research sources: 5
📄 Documents created: 3
📧 Team members notified: 2

📁 Created Content:
  - AI trends - Blog Post: https://docs.google.com/document/d/abc123/edit
  - AI trends - Social Media Content: https://docs.google.com/document/d/def456/edit
  - AI trends - Newsletter Content: https://docs.google.com/document/d/ghi789/edit
```

## Content Analysis Features

### Opportunity Detection
Automatically identifies content angles:
- **Trend Analysis**: Latest developments and emerging patterns
- **Problem-Solution**: Challenges and how they're being addressed
- **Expert Insight**: Thought leadership and professional opinions
- **Innovation Focus**: New technologies and breakthrough developments

### Theme Extraction
Identifies key themes from research:
- Growth & Expansion trends
- Innovation & Technology developments
- Market disruption patterns
- Industry transformation insights

### Content Optimization
Each format is optimized for its intended use:
- **Blog posts**: SEO-friendly with proper structure and CTAs
- **Social media**: Platform-specific formatting and hashtags
- **Newsletters**: Email-optimized with clear sections and links

## Customization

### Modify Content Types
Edit your .env file:
```bash
# Choose which content formats to generate
CONTENT_TYPES=blog_post,social_media  # Skip newsletters
CONTENT_TYPES=blog_post              # Only blog posts
CONTENT_TYPES=social_media,newsletter # Skip blog posts
```

### Change Research Focus
Edit the research queries in `research_topic()`:
```python
research_queries = [
    f"{topic} your custom research angle",
    f"{topic} specific industry focus",
    f"{topic} your unique perspective"
]
```

### Customize Content Templates
Edit the generation methods:
- `generate_blog_post()` - Modify blog structure and tone
- `generate_social_media_content()` - Adjust platform formatting
- `generate_newsletter_content()` - Change newsletter style

### Adjust Target Audience
```bash
TARGET_AUDIENCE=executives     # For C-level content
TARGET_AUDIENCE=developers     # For technical content
TARGET_AUDIENCE=marketers      # For marketing-focused content
```

## Content Distribution

### Team Notifications
Automatically emails team with:
- Links to all generated documents
- Topic and creation timestamp
- Next steps for review and publication
- Content strategy notes

### Google Drive Organization
- All content stored in specified folder
- Consistent naming convention
- Easy access and collaboration
- Version control through Google Docs

## Automation Ideas

### Daily Content Generation
```bash
# Generate daily content on trending topics
0 9 * * * cd /path/to/content-generator && python main.py "Daily Tech News"
```

### Weekly Blog Posts
```bash
# Weekly industry analysis
0 9 * * 1 cd /path/to/content-generator && python main.py "Weekly Industry Roundup"
```

### Event-Triggered Content
- Generate content based on news alerts
- Create content for product launches
- Respond to industry developments
- Seasonal and holiday content

## Integration Enhancements

### Content Management Systems
- Sync with WordPress for direct publishing
- Integration with content calendars
- SEO optimization and metadata

### Social Media Scheduling
- Connect with Buffer or Hootsuite
- Automatic posting schedules
- Performance tracking integration

### Analytics and Optimization
- Track content performance metrics
- A/B testing for different formats
- Audience engagement analysis

## Troubleshooting

**"No research data collected"**
- Check Perplexity API connection
- Verify research queries are appropriate
- Try broader or more specific topics

**"Failed to create document"**
- Check Google Docs OAuth connection
- Verify folder ID is correct and accessible
- Ensure proper permissions for document creation

**"Distribution email failed"**
- Check Gmail OAuth connection
- Verify team email addresses
- Review email content length

## Advanced Features

### Content Quality Scoring
- Readability analysis
- SEO optimization scores
- Engagement prediction metrics
- Brand voice consistency checks

### Multi-Language Support
- Generate content in multiple languages
- Localized research and insights
- Cultural adaptation for different markets

### Content Series Generation
- Create connected content pieces
- Multi-part blog post series
- Themed content campaigns
- Educational content sequences

## Use Cases

- **Marketing Teams**: Regular blog posts and social media content
- **Content Agencies**: Scalable content production for multiple clients
- **Thought Leadership**: Industry analysis and expert commentary
- **Education**: Course materials and educational content
- **Product Marketing**: Feature announcements and educational content
- **News Organizations**: Daily analysis and trend reporting
