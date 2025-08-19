# Lead Management System

**Automatically capture leads from Gmail, score them, store in Google Sheets CRM, and send personalized follow-ups.**

## What it does

1. **Scans Gmail** for potential lead inquiries
2. **Extracts lead information** (name, company, email)
3. **Scores leads** based on content analysis (0-100)
4. **Stores in Google Sheets** CRM with full details
5. **Sends follow-ups** to qualified leads automatically

## Quick Start

```bash
# 1. Clone and navigate
git clone [repo-url]
cd lead-management

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up configuration
cp env.example .env
# Edit .env with your credentials

# 4. Create Google Sheet with headers
# See "Sheet Setup" section below

# 5. Run lead processing
python main.py
```

## Required Setup

### 1. Incredible API

- Get API key from [Incredible Dashboard](https://incredible.one)
- Connect Gmail integration (OAuth)
- Connect Google Sheets integration (OAuth)

### 2. Google Sheet Setup

Create a sheet with these column headers in row 1:

```
Date Captured | Name | Email | Company | Subject | Lead Score | Status | Next Action | Source | Email ID
```

### 3. Environment Variables

```bash
INCREDIBLE_API_KEY=your_api_key
USER_ID=your_user_id
LEADS_SHEET_ID=your_sheet_id
MIN_LEAD_SCORE=60
COMPANY_NAME=Your Company
```

## Lead Scoring System

The system automatically scores leads 0-100 based on:

**High-Value Keywords** (20-30 points each):

- `enterprise`, `budget`, `purchase`, `buy`
- `demo`, `pricing`, `quote`, `urgent`
- `partnership`, `collaboration`

**Quality Indicators** (5-15 points each):

- Professional email domain (not gmail/yahoo)
- Company name extracted
- Message length (longer = more serious)

**Score Ranges**:

- **80-100**: High priority - call within 2 hours
- **60-79**: Qualified - send personalized follow-up
- **40-59**: Add to nurture campaign
- **0-39**: Send general information

## How it works

### Email Detection

Searches for emails matching:

```
subject:(inquiry OR quote OR pricing OR demo OR interested)
subject:(partnership OR collaboration OR integration)
"looking for" OR "need help" OR "can you help"
"get started" OR "learn more" OR "tell me about"
```

### Lead Processing

For each potential lead:

1. **Extract** name, email, company from sender info
2. **Analyze** email content for keywords and intent
3. **Calculate** lead score using scoring algorithm
4. **Determine** next action based on score
5. **Save** to Google Sheets CRM
6. **Send** personalized follow-up if score ≥ threshold

### Follow-up Emails

Automatically generates personalized responses:

- **High-value leads**: Urgent, priority language
- **Demo requests**: Offer to schedule demo
- **Pricing inquiries**: Promise pricing info
- **General**: Professional acknowledgment

## Expected Output

```
🎯 Incredible API - Lead Management System
==================================================
✅ Lead Manager initialized
📊 Leads Sheet: 1BcD3FgHiJkLmNoPqRsTuVwXyZ
🎯 Min Lead Score: 60

🚀 Starting lead scanning (last 24 hours)
🔍 Searching for leads (last 24h): subject:(inquiry OR quote OR pricing OR demo OR interested)
📧 Found 3 emails

📋 Processing: John Smith from Acme Corp
   Score: 85/100
   Action: High Priority - Call within 2 hours
📊 Saving lead: John Smith (Score: 85)
✅ Lead saved to CRM
📧 Sending follow-up to: John Smith
✅ Follow-up sent to John Smith

🎉 Lead processing complete!
📊 Total leads processed: 3
🔥 High-value leads (80+): 1
📧 Follow-ups sent: 2
```

## Customization

### Adjust Lead Scoring

Edit `calculate_lead_score()` method:

```python
high_value_keywords = {
    'enterprise': 30,     # Adjust points
    'your_keyword': 25,   # Add new keywords
}
```

### Customize Follow-up Templates

Edit `generate_follow_up_email()` method to change:

- Email templates
- Call-to-action text
- Contact information
- Available meeting times

### Change Detection Queries

Edit `lead_queries` in `scan_for_leads()`:

```python
lead_queries = [
    'your custom query here',
    'subject:(your keywords)',
]
```

## Automation

### Run Hourly

```bash
# Add to crontab for hourly processing
0 * * * * cd /path/to/lead-management && python main.py

# Or every 4 hours
0 */4 * * * cd /path/to/lead-management && python main.py
```

### Monitor Performance

Check your Google Sheet to:

- Track lead volume trends
- Analyze lead sources
- Monitor conversion rates
- Review follow-up effectiveness

## Troubleshooting

**"No new leads found"**

- Check if Gmail has emails matching the search queries
- Verify your search timeframe (try `hours_back=48`)

**"Error saving lead"**

- Check Google Sheets OAuth connection
- Verify sheet ID is correct
- Ensure sheet has proper headers

**"Follow-up email failed"**

- Check Gmail OAuth connection
- Verify sender email permissions
- Review email content for spam triggers

## Next Steps

- **Integration**: Connect with Slack for real-time notifications
- **Analytics**: Add lead source tracking and conversion metrics
- **Nurturing**: Implement multi-touch email sequences
- **Scoring**: Add more sophisticated ML-based scoring
- **CRM**: Sync with existing CRM systems
