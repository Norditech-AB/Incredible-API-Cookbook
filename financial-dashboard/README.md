# Financial Dashboard

**Automated financial intelligence system that researches market data, analyzes trends, and delivers executive reports.**

## What it does

1. **Researches market data** using Perplexity AI across multiple categories
2. **Analyzes trends** and sentiment from financial news and data
3. **Creates dashboards** in Google Sheets with automated updates
4. **Generates alerts** for significant market movements
5. **Emails reports** to executives and stakeholders

## Quick Start

```bash
# 1. Clone and navigate
git clone [repo-url]
cd financial-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up configuration
cp env.example .env
# Edit .env with your credentials

# 4. Run financial analysis
python main.py

# 5. Track specific stocks
python main.py --symbols AAPL,GOOGL,TSLA
```

## Required Setup

### 1. Incredible API
- Get API key from [Incredible Dashboard](https://incredible.one)
- Connect Perplexity AI integration (API key)
- Connect Google Sheets integration (OAuth)
- Connect Gmail integration (OAuth)

### 2. Google Sheet Setup
The script creates three sheets automatically:
- **Market_Summary**: High-level market sentiment and metrics
- **Detailed_Data**: Complete research data and sources
- **Alerts**: Significant market alerts and notifications

### 3. Environment Variables
```bash
INCREDIBLE_API_KEY=your_api_key
USER_ID=your_user_id
DASHBOARD_SHEET_ID=your_sheet_id
REPORT_RECIPIENTS=cfo@company.com,investor@company.com
COMPANY_SYMBOLS=AAPL,GOOGL,MSFT
MARKET_SECTORS=technology,finance,healthcare
```

## Research Categories

### Market Overview
- Stock market performance (NYSE, NASDAQ)
- Market volatility index (VIX)
- Economic indicators (GDP, inflation, unemployment)
- Federal Reserve policy and interest rates
- Market sentiment and investor confidence

### Company Performance
- Stock price performance and earnings
- Quarterly results and revenue growth
- Recent news and announcements
- Analyst recommendations

### Sector Analysis
- Industry trend analysis
- Sector performance comparisons
- Growth opportunities assessment
- Leading companies identification

## Expected Output

```
💰 Incredible API - Financial Dashboard
==================================================
✅ Financial Dashboard initialized
📊 Dashboard Sheet: 1BcD3FgHiJkLmNoPqRsTuVwXyZ
📈 Tracking: AAPL, GOOGL, MSFT

============================================================
💰 FINANCIAL DASHBOARD ANALYSIS
============================================================

📈 Researching market overview...
🔍 Researching: stock market performance today NYSE NASDAQ current
🔍 Researching: market volatility index VIX fear greed current levels
...
✅ Market overview research complete: 5 topics

🏢 Researching company performance: AAPL, GOOGL, MSFT
🔍 Researching: AAPL stock price performance earnings latest
...
✅ Company research complete: 9 analyses

🏭 Researching sector trends: technology, finance, healthcare
✅ Sector research complete: 9 analyses

📊 Analyzing financial data...
🎯 Analysis complete:
   Market Sentiment: BULLISH
   Key Insights: 4
   Alerts: 1

📊 Updating financial dashboard...
✅ Dashboard updated successfully
📝 Generating executive report...
📧 Sending financial report...
✅ Report sent to: cfo@company.com
✅ Report sent to: investor@company.com

🎉 Financial analysis complete!
📊 Data points analyzed: 23
📈 Market sentiment: BULLISH
🚨 Alerts generated: 1
📧 Reports sent: 2
📊 View dashboard: https://docs.google.com/spreadsheets/d/...
```

## Intelligence Analysis

### Sentiment Analysis
The system automatically determines market sentiment:
- **BULLISH**: More positive indicators than negative
- **BEARISH**: More negative indicators than positive  
- **MIXED**: Balanced or unclear sentiment

### Alert System
Automatic alerts for:
- **HIGH**: Market crashes, major volatility
- **MEDIUM**: Unusual movements, volatility spikes
- **LOW**: General market news and trends

### Key Insights
Extracts significant developments:
- Record highs/lows
- Breakthrough announcements
- Major milestones
- Earnings surprises

## Executive Reports

Generated reports include:

### Executive Summary
- Market sentiment assessment
- Key metrics and data points
- Alert summary

### Key Insights
- Top 5 significant developments
- Source attribution
- Impact analysis

### Market Alerts
- Priority-ranked alerts
- Detailed descriptions
- Recommended actions

### Strategic Recommendations
- Investment suggestions
- Risk management advice
- Portfolio adjustments
- Monitoring recommendations

### Market Overview
- Current market conditions
- Economic indicators
- Policy impacts

### Company Highlights
- Individual stock performance
- Earnings updates
- News and developments

## Customization

### Track Different Stocks
```bash
# Custom stock symbols
python main.py --symbols TSLA,AMZN,NFLX,META

# Or edit env file
COMPANY_SYMBOLS=your,custom,symbols
```

### Add Market Sectors
Edit env file:
```bash
MARKET_SECTORS=technology,healthcare,finance,energy,retail
```

### Modify Research Queries
Edit the research methods in main.py:
```python
market_queries = [
    "your custom market research query",
    "specific indicator you want to track"
]
```

### Customize Alert Thresholds
Edit `analyze_financial_data()` method:
```python
# Add custom alert conditions
if 'your_keyword' in data_text:
    analysis['alerts'].append({
        'level': 'HIGH',
        'message': 'Custom alert triggered'
    })
```

## Automation

### Daily Market Analysis
```bash
# Add to crontab for daily reports
0 9 * * * cd /path/to/financial-dashboard && python main.py
```

### Pre-Market Analysis
```bash
# Run before market open
30 8 * * 1-5 cd /path/to/financial-dashboard && python main.py
```

### After-Hours Analysis
```bash
# Run after market close
30 17 * * 1-5 cd /path/to/financial-dashboard && python main.py
```

## Integration Ideas

### Trading Platforms
- Connect with brokerage APIs
- Automated trade execution based on signals
- Portfolio rebalancing recommendations

### Risk Management
- VaR calculations
- Portfolio stress testing
- Correlation analysis

### Communication
- Slack notifications for urgent alerts
- SMS alerts for critical market events
- Teams integration for collaboration

## Troubleshooting

**"No financial data collected"**
- Check Perplexity API connection
- Verify research queries are working
- Try broader search terms

**"Error updating sheet"**
- Check Google Sheets OAuth connection
- Verify sheet ID is correct
- Ensure sheet permissions allow writing

**"Report email failed"**
- Check Gmail OAuth connection
- Verify recipient email addresses
- Check email content isn't too long

## Advanced Features

### Machine Learning Integration
- Sentiment scoring algorithms
- Trend prediction models
- Anomaly detection systems

### Real-Time Monitoring
- Live market data feeds
- Continuous analysis updates
- Instant alert notifications

### Portfolio Analytics
- Performance attribution
- Risk-adjusted returns
- Benchmark comparisons

## Use Cases

- **Investment Firms**: Daily market intelligence and portfolio monitoring
- **Corporate Finance**: Executive financial reporting and market analysis  
- **Wealth Management**: Client portfolio updates and market insights
- **Research Teams**: Comprehensive market research and trend analysis
- **Trading Desks**: Real-time market sentiment and alert systems
