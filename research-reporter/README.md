# Research Reporter

**Automatically research topics using Perplexity AI, analyze findings, store in Google Sheets, and email comprehensive reports.**

## What it does

1. **Researches topics** using multiple targeted Perplexity AI queries
2. **Analyzes findings** to extract key themes, opportunities, and challenges
3. **Stores all data** in Google Sheets for future reference
4. **Generates reports** with executive summaries and recommendations
5. **Emails reports** to stakeholders automatically

## Quick Start

```bash
# 1. Clone and navigate
git clone [repo-url]
cd research-reporter

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up configuration
cp env.example .env
# Edit .env with your credentials

# 4. Run research on a topic
python main.py "AI in Healthcare 2024"

# 5. Research multiple topics
python main.py "FinTech trends" "Blockchain adoption" "Remote work tools"
```

## Required Setup

### 1. Incredible API

- Get API key from [Incredible Dashboard](https://incredible.one)
- Connect Perplexity AI integration (API key)
- Connect Google Sheets integration (OAuth)
- Connect Gmail integration (OAuth)

### 2. Google Sheet Setup

The script creates two sheets automatically:

- **Research_Data**: Raw research results and sources
- **Analysis**: Extracted insights and themes

### 3. Environment Variables

```bash
INCREDIBLE_API_KEY=your_api_key
USER_ID=your_user_id
RESEARCH_SHEET_ID=your_sheet_id
REPORT_RECIPIENTS=email1@company.com,email2@company.com
```

## Usage Examples

### Single Topic Research

```bash
python main.py "AI in Healthcare 2024"
```

### Multiple Topics

```bash
python main.py "Machine Learning trends" "Quantum computing" "Cybersecurity threats"
```

### Using Command Line Flags

```bash
python main.py --topics "Climate tech" --topics "Green energy" "Carbon capture"
```

## Research Strategy

For each topic, the system generates 5 comprehensive queries:

1. **Latest developments** - Current news and updates
2. **Market trends** - Industry analysis and growth
3. **Challenges & opportunities** - Barriers and potential
4. **Expert opinions** - Thought leader insights
5. **Case studies** - Real-world examples and success stories

## Expected Output

```
🔬 Incredible API - Research Reporter
==================================================
✅ Research Reporter initialized
📊 Research Sheet: 1BcD3FgHiJkLmNoPqRsTuVwXyZ
📧 Recipients: 2

============================================================
🔬 RESEARCH WORKFLOW: AI in Healthcare 2024
============================================================

🚀 Starting research on: AI in Healthcare 2024
🔍 Researching: AI in Healthcare 2024 latest developments 2024
✅ Research complete: 8 sources
🔍 Researching: AI in Healthcare 2024 market trends analysis current
✅ Research complete: 6 sources
...

📋 Completed research: 5/5 queries successful
📊 Analyzing research data...
🎯 Analysis complete:
   Themes: 3
   Opportunities: 4
   Challenges: 2

📊 Saving research to Google Sheets...
✅ Research data saved to Google Sheets
📝 Generating executive report...
📧 Sending research report...
✅ Report sent to: stakeholder1@company.com
✅ Report sent to: stakeholder2@company.com

🎉 Research workflow complete for: AI in Healthcare 2024
📊 Research queries: 5
📚 Total sources: 32
📧 Report recipients: 2
📈 View full data: https://docs.google.com/spreadsheets/d/...
```

## Report Structure

The generated report includes:

### Executive Summary

- Overview of research scope
- Key metrics (queries, sources)
- High-level findings

### Key Findings

- **Major Themes**: Trending topics and developments
- **Opportunities**: Market potential and growth areas
- **Challenges**: Barriers and risks to consider

### Detailed Research

- Complete findings from each query
- Source references and citations
- Comprehensive analysis

### Recommendations

- Strategic suggestions based on findings
- Next steps for stakeholders
- Areas for deeper investigation

## Customization

### Modify Research Queries

Edit the `research_topic()` method:

```python
research_queries = [
    f"{topic} your custom angle here",
    f"{topic} industry specific focus",
    # Add your domain-specific queries
]
```

### Adjust Analysis Logic

Edit `analyze_research_data()` to:

- Add domain-specific keyword detection
- Customize insight categorization
- Implement advanced sentiment analysis

### Customize Report Format

Edit `generate_executive_report()` to:

- Change report structure
- Add custom sections
- Modify formatting and style

## Automation

### Daily Market Research

```bash
# Add to crontab for daily research
0 9 * * * cd /path/to/research-reporter && python main.py "Daily market updates"
```

### Weekly Industry Reports

```bash
# Weekly comprehensive reports
0 9 * * 1 cd /path/to/research-reporter && python main.py "Industry weekly roundup" "Competitor analysis"
```

### Event-Triggered Research

Integrate with other systems to trigger research based on:

- News alerts
- Market movements
- Customer inquiries
- Competitive actions

## Data Management

### Google Sheets Structure

**Research_Data Sheet**:

- Timestamp, Topic, Query, Answer, Sources Count, Analysis

**Analysis Sheet**:

- Timestamp, Topic, Category, Insight, Source Query

### Export Options

- Download sheets as CSV for analysis
- Import into BI tools (Tableau, PowerBI)
- Sync with existing data warehouses

## Troubleshooting

**"No research data collected"**

- Check Perplexity API connection
- Verify API key is valid
- Try simpler, more general topics

**"Error updating sheet"**

- Check Google Sheets OAuth connection
- Verify sheet ID is correct
- Ensure sheet is accessible

**"Report email failed"**

- Check Gmail OAuth connection
- Verify recipient email addresses
- Review email content length

## Advanced Features

### Research Quality Scoring

- Source credibility assessment
- Information freshness validation
- Cross-reference verification

### Trend Analysis

- Historical data comparison
- Pattern recognition
- Predictive insights

### Custom Integrations

- Slack notifications for urgent findings
- CRM integration for sales intelligence
- Knowledge base updates for customer support

## Use Cases

- **Market Intelligence**: Competitive analysis and industry trends
- **Investment Research**: Due diligence and opportunity assessment
- **Product Development**: Technology trends and user needs
- **Content Creation**: Topic research and expert insights
- **Strategic Planning**: Industry analysis and future planning
