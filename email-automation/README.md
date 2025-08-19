# Email Automation

**Automatically respond to Gmail inquiries and log interactions to Google Sheets.**

## What it does

1. **Monitors Gmail** for support/sales inquiries
2. **Sends auto-responses** based on email content
3. **Logs all interactions** to Google Sheets for tracking

## Quick Start

```bash
# 1. Clone and navigate
git clone [repo-url]
cd email-automation

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up configuration
cp env.example .env
# Edit .env with your credentials

# 4. Run the automation
python main.py
```

## Required Setup

### 1. Incredible API

- Get API key from [Incredible Dashboard](https://incredible.one)
- Connect Gmail integration (OAuth)
- Connect Google Sheets integration (OAuth)

### 2. Google Sheet Setup

- Create a new Google Sheet
- Copy the Sheet ID from the URL
- Sheet will auto-create "EmailLog" tab with headers

### 3. Environment Variables

```bash
INCREDIBLE_API_KEY=your_api_key
USER_ID=your_user_id
EMAIL_LOG_SHEET_ID=your_sheet_id
```

## How it works

The script searches for emails matching these patterns:

- `is:unread (subject:support OR subject:help)`
- `is:unread (subject:demo OR subject:pricing)`
- `is:unread to:support@company.com`

For each email found:

1. **Analyzes content** to determine response type
2. **Generates appropriate auto-response**:
   - Support inquiries → Support team response
   - Sales inquiries → Sales team response
   - General inquiries → General acknowledgment
3. **Sends response** to original sender
4. **Logs interaction** in Google Sheets

## Expected Output

```
🤖 Incredible API - Email Automation Example
==================================================
✅ Email automation initialized for user: user123
🔍 Searching emails: is:unread (subject:support OR subject:help)
📧 Found 2 emails

📧 Processing: Need help with login
📤 Sending email to: customer@example.com
✅ Email sent successfully
📊 Logging interaction to sheets
✅ Interaction logged to sheets

🎉 Email automation complete! Processed 2 emails.
✅ Successfully processed 2 emails
```

## Customization

Edit the auto-response templates in `generate_auto_response()` method:

- Support responses
- Sales responses
- General responses

## Troubleshooting

**"Missing required environment variables"**

- Check your `.env` file has all required variables

**"Error searching emails"**

- Verify Gmail OAuth is connected in Incredible dashboard
- Check your API key is valid

**"Error logging to sheets"**

- Verify Google Sheets OAuth is connected
- Check the Sheet ID is correct
- Ensure sheet is accessible to your account

## Next Steps

- Set up as a cron job for automated processing
- Add more sophisticated email categorization
- Implement email priority scoring
- Add Slack notifications for urgent emails
