# Incredible API Cookbook 🧪

**Practical, executable examples for building AI agents with the Incredible API.**

Clone any folder and run immediately - no complex setup required!

## 🎯 **What is Incredible API?**

Create AI agents that integrate with **up to 3 applications** to automate complex workflows:

- **Email automation** with Gmail + Sheets + Slack
- **Lead management** with smart scoring and follow-ups
- **Research automation** using Perplexity AI + data storage
- **Financial dashboards** with real-time monitoring

## 🚀 **Executable Examples**

Each folder is a **complete, runnable project**:

### 📧 **[Email Automation](./email-automation/)**

**Auto-respond to Gmail inquiries and log to Google Sheets**

```bash
cd email-automation && python main.py
```

- Monitors Gmail for support/sales emails
- Sends intelligent auto-responses
- Logs all interactions to spreadsheet
- **Apps**: Gmail + Google Sheets

### 🎯 **[Lead Management](./lead-management/)**

**Capture leads from email, score them, and send follow-ups**

```bash
cd lead-management && python main.py
```

- Scans emails for potential leads
- Scores leads 0-100 based on content
- Stores in Google Sheets CRM
- Sends personalized follow-up emails
- **Apps**: Gmail + Google Sheets

### 🔍 **[Research Reporter](./research-reporter/)**

**AI-powered research with comprehensive reports**

```bash
cd research-reporter && python main.py "AI in Healthcare 2024"
```

- Multi-query research using Perplexity AI
- Analyzes findings for themes and opportunities
- Stores research data in Google Sheets
- Emails executive reports to stakeholders
- **Apps**: Perplexity + Google Sheets + Gmail

### 📅 **[Meeting Organizer](./meeting-organizer/)**

**Extract meetings from Gmail and create organized workflows**

```bash
cd meeting-organizer && python main.py
```

- Scans Gmail for meeting invitations
- Creates calendar events automatically
- Generates prep and follow-up tasks in Asana
- **Apps**: Gmail + Google Calendar + Asana

### 📊 **[Financial Dashboard](./financial-dashboard/)**

**Real-time financial intelligence and reporting**

```bash
cd financial-dashboard && python main.py
```

- Researches market data and trends
- Analyzes portfolio performance
- Creates automated dashboards
- Sends executive financial reports
- **Apps**: Perplexity + Google Sheets + Gmail

### ✍️ **[Content Generator](./content-generator/)**

**Research topics and create multi-format content**

```bash
cd content-generator && python main.py "AI trends"
```

- Researches trending topics
- Generates blog posts, social media content
- Stores content in Google Docs
- Distributes to team via email
- **Apps**: Perplexity + Google Docs + Gmail

## 🚀 **Quick Start - 2 Minutes to Running**

### 1. **Choose an Example**

Pick any folder that interests you:

```bash
git clone https://github.com/yourusername/incredible-api-cookbook.git
cd incredible-api-cookbook/email-automation  # or any other folder
```

### 2. **Install & Configure**

```bash
# Install Python dependencies
pip install -r requirements.txt

# Set up your credentials
cp env.example .env
# Edit .env with your API keys
```

### 3. **Run It**

```bash
python main.py
```

**That's it!** Each example is self-contained and ready to run.

## ⚙️ **Setup Requirements**

### Incredible API Account

1. **Sign up**: [https://incredible.one](https://incredible.one)
2. **Get API key** from dashboard
3. **Connect integrations** (Gmail, Google Sheets, Perplexity, etc.)

### Common Environment Variables

```bash
INCREDIBLE_API_KEY=your_api_key_here
USER_ID=your_user_id_here
```

Each example includes specific setup instructions in its README.

## 📖 **How Each Example Works**

Every folder follows the **Modal Labs pattern**:

```
email-automation/
├── main.py           # Complete working script
├── requirements.txt  # Python dependencies
├── env.example      # Configuration template
└── README.md        # Usage instructions
```

1. **Clone** the folder you want to try
2. **Install** dependencies with `pip install -r requirements.txt`
3. **Configure** your credentials in `.env`
4. **Run** with `python main.py`

## 🤝 Contributing

We welcome contributions! Whether it's:

- New use case examples
- Bug fixes or improvements
- Integration guides
- Documentation enhancements

Please read our [Contributing Guide](./CONTRIBUTING.md) to get started.

## 📖 Additional Resources

- [**Official API Documentation**](https://docs.incredible.one)
- [**Integration Reference**](https://docs.incredible.one/api-reference/integrations)
- [**Community Forum**](https://community.incredible.one)
- [**Support**](mailto:support@incredible.one)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

**Ready to automate your workflows?** Pick an example folder and start building in 2 minutes! 🚀
