# JavaScript/Node.js SDK Examples

Comprehensive JavaScript utilities and examples for building robust applications with the Incredible API.

## Overview

This directory contains JavaScript/Node.js SDK examples, utilities, and best practices for working with the Incredible API. All examples are production-ready and include proper error handling, logging, and testing patterns.

## Structure

```
javascript/
├── src/                    # Core SDK utilities
│   ├── incredible-sdk/     # Main SDK modules
│   │   ├── client.js       # Main API client
│   │   ├── integrations.js # Integration helpers
│   │   ├── functions.js    # Function calling utilities
│   │   ├── exceptions.js   # Custom exceptions
│   │   └── utils.js       # Common utilities
│   └── index.js           # Main export
├── examples/              # Complete example applications
│   ├── email-automation/  # Gmail automation examples
│   ├── data-processing/   # Data analysis and processing
│   ├── business-workflows/# Complete business solutions
│   └── ai-agents/        # Advanced AI agent patterns
├── templates/            # Reusable templates
├── tests/               # Unit and integration tests
├── package.json         # Dependencies and scripts
└── README.md           # This file
```

## Quick Start

### Installation

```bash
# Clone the cookbook and navigate to JavaScript SDK
cd incredible-api-cookbook/sdk-examples/javascript

# Install dependencies
npm install

# Set up environment
cp .env.example .env
# Edit .env with your credentials

# Run example
npm run example:basic
```

### Basic Usage

```javascript
const { IncredibleClient } = require('./src');

// Initialize client
const client = new IncredibleClient({
    apiKey: process.env.INCREDIBLE_API_KEY,
    baseUrl: 'https://api.incredible.one'
});

// Create a simple agent
async function main() {
    const response = await client.chatCompletion({
        messages: [{ role: 'user', content: 'Summarize my recent emails' }],
        functions: client.getGmailFunctions(),
        stream: false
    });
    
    console.log(response);
}

main().catch(console.error);
```

## Core SDK Components

### 1. IncredibleClient

The main client for interacting with the Incredible API.

```javascript
// src/incredible-sdk/client.js
const axios = require('axios');
const { IncredibleAPIError, RateLimitError, AuthenticationError } = require('./exceptions');

class IncredibleClient {
    constructor(options = {}) {
        this.apiKey = options.apiKey || process.env.INCREDIBLE_API_KEY;
        this.baseUrl = options.baseUrl || 'https://api.incredible.one';
        this.timeout = options.timeout || 30000;
        this.retryAttempts = options.retryAttempts || 3;
        
        this.axios = axios.create({
            baseURL: this.baseUrl,
            timeout: this.timeout,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`
            }
        });
        
        this.setupInterceptors();
    }
    
    setupInterceptors() {
        // Request interceptor for logging
        this.axios.interceptors.request.use(
            (config) => {
                console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
                return config;
            },
            (error) => Promise.reject(error)
        );
        
        // Response interceptor for error handling
        this.axios.interceptors.response.use(
            (response) => response,
            (error) => {
                if (error.response?.status === 429) {
                    throw new RateLimitError('Rate limit exceeded', error.response.headers['retry-after']);
                } else if (error.response?.status === 401) {
                    throw new AuthenticationError('Authentication failed');
                } else {
                    throw new IncredibleAPIError(`API error: ${error.message}`, error.response?.data);
                }
            }
        );
    }
    
    async chatCompletion(options) {
        const data = {
            model: options.model || 'small-1',
            messages: options.messages,
            stream: options.stream || false,
            functions: options.functions || [],
            system: options.system || 'You are a helpful assistant.'
        };
        
        try {
            const response = await this.axios.post('/v1/chat-completion', data);
            
            // Handle function calls if present
            if (options.functionExecutor && this.hasFunctionCalls(response.data)) {
                return await this.handleFunctionCalls(response.data, options);
            }
            
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    }
    
    async listIntegrations() {
        try {
            const response = await this.axios.get('/v1/integrations');
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    }
    
    async connectIntegration(integrationId, connectionData) {
        try {
            const response = await this.axios.post(
                `/v1/integrations/${integrationId}/connect`,
                connectionData
            );
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    }
    
    async executeIntegration(integrationId, featureName, inputs) {
        try {
            const response = await this.axios.post(
                `/v1/integrations/${integrationId}/execute`,
                {
                    user_id: inputs.userId || this.defaultUserId,
                    feature_name: featureName,
                    inputs: inputs
                }
            );
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    }
    
    hasFunctionCalls(responseData) {
        const responses = responseData.result?.response || [];
        return responses.some(item => item.type === 'function_call');
    }
    
    async handleFunctionCalls(responseData, options) {
        const responses = responseData.result.response;
        const updatedMessages = [...options.messages];
        
        for (const response of responses) {
            updatedMessages.push(response);
            
            if (response.type === 'function_call') {
                const results = [];
                
                for (const functionCall of response.function_calls) {
                    try {
                        const result = await options.functionExecutor.execute(
                            functionCall.name,
                            functionCall.input
                        );
                        results.push(result);
                    } catch (error) {
                        console.error(`Function execution error: ${error.message}`);
                        results.push({ error: error.message });
                    }
                }
                
                // Add function results to conversation
                updatedMessages.push({
                    type: 'function_call_result',
                    function_call_id: response.function_call_id,
                    function_call_results: results
                });
                
                // Continue conversation with results
                const continuationOptions = {
                    ...options,
                    messages: updatedMessages
                };
                
                return await this.chatCompletion(continuationOptions);
            }
        }
        
        return responseData;
    }
    
    getGmailFunctions() {
        return [
            {
                name: 'search_emails',
                description: 'Search for emails in Gmail',
                parameters: {
                    type: 'object',
                    properties: {
                        query: { type: 'string', description: 'Gmail search query' },
                        maxResults: { type: 'number', description: 'Maximum results to return' }
                    },
                    required: ['query']
                }
            },
            {
                name: 'send_email',
                description: 'Send an email via Gmail',
                parameters: {
                    type: 'object',
                    properties: {
                        to: { type: 'string', description: 'Recipient email address' },
                        subject: { type: 'string', description: 'Email subject' },
                        body: { type: 'string', description: 'Email body content' }
                    },
                    required: ['to', 'subject', 'body']
                }
            }
        ];
    }
    
    handleError(error) {
        if (error instanceof IncredibleAPIError) {
            return error;
        }
        
        return new IncredibleAPIError(`Unexpected error: ${error.message}`, error.response?.data);
    }
}

module.exports = IncredibleClient;
```

### 2. Integration Helpers

Simplified interfaces for common integrations.

```javascript
// src/incredible-sdk/integrations.js
class IntegrationHelper {
    constructor(client, userId) {
        this.client = client;
        this.userId = userId;
    }
}

class GmailHelper extends IntegrationHelper {
    async search(query, maxResults = 10) {
        return await this.client.executeIntegration('gmail', 'GMAIL_SEARCH_EMAILS', {
            userId: this.userId,
            query,
            max_results: maxResults
        });
    }
    
    async sendEmail(to, subject, body, options = {}) {
        return await this.client.executeIntegration('gmail', 'GMAIL_SEND_EMAIL', {
            userId: this.userId,
            to,
            subject,
            body,
            ...options
        });
    }
    
    async markAsRead(emailId) {
        return await this.client.executeIntegration('gmail', 'GMAIL_MARK_READ', {
            userId: this.userId,
            email_id: emailId
        });
    }
}

class SheetsHelper extends IntegrationHelper {
    async addRow(spreadsheetId, values, sheetName = 'Sheet1') {
        return await this.client.executeIntegration('google_sheets', 'SHEETS_ADD_ROW', {
            userId: this.userId,
            spreadsheet_id: spreadsheetId,
            range: sheetName,
            values: [values]
        });
    }
    
    async readRange(spreadsheetId, range) {
        return await this.client.executeIntegration('google_sheets', 'SHEETS_READ_RANGE', {
            userId: this.userId,
            spreadsheet_id: spreadsheetId,
            range
        });
    }
    
    async updateRange(spreadsheetId, range, values) {
        return await this.client.executeIntegration('google_sheets', 'SHEETS_UPDATE_RANGE', {
            userId: this.userId,
            spreadsheet_id: spreadsheetId,
            range,
            values
        });
    }
    
    async createSheet(name) {
        return await this.client.executeIntegration('google_sheets', 'SHEETS_CREATE', {
            userId: this.userId,
            name
        });
    }
}

class SlackHelper extends IntegrationHelper {
    async sendMessage(channel, text, options = {}) {
        return await this.client.executeIntegration('slack', 'SLACK_SEND_MESSAGE', {
            userId: this.userId,
            channel,
            text,
            ...options
        });
    }
    
    async sendDirectMessage(userId, text) {
        return await this.client.executeIntegration('slack', 'SLACK_SEND_DM', {
            userId: this.userId,
            target_user: userId,
            text
        });
    }
    
    async uploadFile(channel, filePath, title) {
        return await this.client.executeIntegration('slack', 'SLACK_UPLOAD_FILE', {
            userId: this.userId,
            channel,
            file_path: filePath,
            title
        });
    }
}

module.exports = {
    GmailHelper,
    SheetsHelper,
    SlackHelper
};
```

### 3. Function Registry

Powerful utilities for building custom functions.

```javascript
// src/incredible-sdk/functions.js
class FunctionRegistry {
    constructor() {
        this.functions = new Map();
    }
    
    register(name, description, parameters, handler) {
        this.functions.set(name, {
            definition: {
                name,
                description,
                parameters
            },
            handler
        });
        
        return this;
    }
    
    function(name, description, parameters) {
        return (target, propertyKey, descriptor) => {
            this.register(name, description, parameters, descriptor.value);
            return descriptor;
        };
    }
    
    getFunctionDefinitions() {
        return Array.from(this.functions.values()).map(f => f.definition);
    }
    
    async execute(functionName, inputs) {
        const func = this.functions.get(functionName);
        if (!func) {
            throw new Error(`Function ${functionName} not found`);
        }
        
        try {
            return await func.handler(inputs);
        } catch (error) {
            throw new Error(`Function execution failed: ${error.message}`);
        }
    }
}

// Helper function for easy registration
function createFunctionRegistry() {
    return new FunctionRegistry();
}

module.exports = {
    FunctionRegistry,
    createFunctionRegistry
};
```

### 4. Agent Framework

High-level abstraction for building AI agents.

```javascript
// src/incredible-sdk/agent.js
const { GmailHelper, SheetsHelper, SlackHelper } = require('./integrations');
const { FunctionRegistry } = require('./functions');

class Agent {
    constructor(client, config = {}) {
        this.client = client;
        this.config = config;
        this.userId = config.userId;
        
        // Initialize helpers
        this.gmail = new GmailHelper(client, this.userId);
        this.sheets = new SheetsHelper(client, this.userId);
        this.slack = new SlackHelper(client, this.userId);
        
        // Function registry
        this.functions = new FunctionRegistry();
        this.setupFunctions();
    }
    
    setupFunctions() {
        // Override in subclasses to add custom functions
    }
    
    async execute() {
        throw new Error('execute() method must be implemented by subclass');
    }
    
    async analyzeBatch(items, analysisPrompt, batchSize = 5) {
        const results = [];
        
        for (let i = 0; i < items.length; i += batchSize) {
            const batch = items.slice(i, i + batchSize);
            const batchResults = await Promise.all(
                batch.map(item => this.analyzeItem(item, analysisPrompt))
            );
            results.push(...batchResults);
            
            // Small delay to respect rate limits
            if (i + batchSize < items.length) {
                await this.delay(1000);
            }
        }
        
        return results;
    }
    
    async analyzeItem(item, prompt) {
        try {
            const response = await this.client.chatCompletion({
                messages: [{ role: 'user', content: `${prompt}\n\nItem: ${JSON.stringify(item)}` }],
                functions: this.functions.getFunctionDefinitions(),
                functionExecutor: this.functions
            });
            
            return this.extractAnalysisResult(response);
        } catch (error) {
            console.error(`Analysis failed for item: ${error.message}`);
            return { error: error.message, item };
        }
    }
    
    extractAnalysisResult(response) {
        const lastResponse = response.result.response[response.result.response.length - 1];
        
        if (lastResponse.role === 'assistant') {
            try {
                return JSON.parse(lastResponse.content);
            } catch {
                return { analysis: lastResponse.content };
            }
        }
        
        return { raw_response: response };
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    log(message, level = 'info') {
        const timestamp = new Date().toISOString();
        console.log(`[${timestamp}] [${level.toUpperCase()}] ${message}`);
    }
}

module.exports = Agent;
```

## Example Applications

### 1. Email Automation Suite

Complete email management and automation system.

```javascript
// examples/email-automation/email-suite.js
const Agent = require('../../src/incredible-sdk/agent');

class EmailAutomationSuite extends Agent {
    setupFunctions() {
        this.functions.register(
            'categorize_email',
            'Categorize email into business categories',
            {
                type: 'object',
                properties: {
                    subject: { type: 'string' },
                    sender: { type: 'string' },
                    content: { type: 'string' }
                }
            },
            this.categorizeEmail.bind(this)
        );
        
        this.functions.register(
            'extract_action_items',
            'Extract action items from email content',
            {
                type: 'object',
                properties: {
                    content: { type: 'string' }
                }
            },
            this.extractActionItems.bind(this)
        );
    }
    
    async execute() {
        this.log('Starting Email Automation Suite');
        
        try {
            // Get recent emails
            const emails = await this.gmail.search('newer_than:1d', 50);
            this.log(`Found ${emails.length} emails to process`);
            
            // Process emails in batches
            const processedEmails = await this.processBatchEmails(emails);
            
            // Generate summary report
            const summary = this.generateSummary(processedEmails);
            
            // Send daily digest
            await this.sendDailyDigest(summary);
            
            return {
                status: 'completed',
                processed: processedEmails.length,
                summary
            };
            
        } catch (error) {
            this.log(`Error in email automation: ${error.message}`, 'error');
            throw error;
        }
    }
    
    async processBatchEmails(emails) {
        const processed = [];
        
        for (const email of emails) {
            try {
                const analysis = await this.processEmail(email);
                processed.push(analysis);
                
                // Log to tracking sheet
                await this.logEmailToSheet(email, analysis);
                
                // Handle urgent emails
                if (analysis.priority === 'urgent') {
                    await this.handleUrgentEmail(email, analysis);
                }
                
            } catch (error) {
                this.log(`Failed to process email ${email.id}: ${error.message}`, 'error');
            }
        }
        
        return processed;
    }
    
    async processEmail(email) {
        const prompt = `
        Analyze this email and provide structured information:
        
        Subject: ${email.subject}
        From: ${email.sender}
        Content: ${email.content?.substring(0, 1000)}
        
        Return JSON with:
        - category: (urgent, meeting, newsletter, support, personal)
        - priority: (low, medium, high, urgent)
        - sentiment: (positive, neutral, negative)
        - action_required: (boolean)
        - summary: (brief summary)
        `;
        
        const response = await this.client.chatCompletion({
            messages: [{ role: 'user', content: prompt }],
            functions: this.functions.getFunctionDefinitions(),
            functionExecutor: this.functions
        });
        
        return this.extractAnalysisResult(response);
    }
    
    async categorizeEmail({ subject, sender, content }) {
        // Email categorization logic
        const text = `${subject} ${content}`.toLowerCase();
        
        if (text.includes('urgent') || text.includes('asap')) {
            return { category: 'urgent', confidence: 0.9 };
        }
        
        if (text.includes('meeting') || text.includes('call')) {
            return { category: 'meeting', confidence: 0.8 };
        }
        
        if (sender.includes('noreply') || sender.includes('newsletter')) {
            return { category: 'newsletter', confidence: 0.7 };
        }
        
        return { category: 'general', confidence: 0.5 };
    }
    
    async extractActionItems({ content }) {
        // Extract action items from email content
        const actionWords = ['todo', 'action', 'task', 'deadline', 'follow up'];
        const lines = content.split('\n');
        const actionItems = [];
        
        for (const line of lines) {
            if (actionWords.some(word => line.toLowerCase().includes(word))) {
                actionItems.push(line.trim());
            }
        }
        
        return { action_items: actionItems };
    }
    
    async logEmailToSheet(email, analysis) {
        if (!this.config.trackingSheetId) return;
        
        const row = [
            new Date().toISOString(),
            email.subject || 'No Subject',
            email.sender || 'Unknown',
            analysis.category || 'uncategorized',
            analysis.priority || 'low',
            analysis.sentiment || 'neutral',
            analysis.action_required || false,
            analysis.summary || 'No summary'
        ];
        
        await this.sheets.addRow(this.config.trackingSheetId, row);
    }
    
    async handleUrgentEmail(email, analysis) {
        const alertMessage = `
🚨 **Urgent Email Alert**

📧 **Subject:** ${email.subject}
👤 **From:** ${email.sender}
📅 **Received:** ${new Date(email.date).toLocaleString()}

📋 **Summary:** ${analysis.summary}

🔗 **Actions:** ${analysis.action_required ? 'Action Required' : 'No Action Needed'}
        `;
        
        // Send Slack alert
        if (this.config.urgentAlertsChannel) {
            await this.slack.sendMessage(this.config.urgentAlertsChannel, alertMessage);
        }
    }
    
    generateSummary(processedEmails) {
        const summary = {
            total: processedEmails.length,
            by_category: {},
            by_priority: {},
            action_required: 0
        };
        
        for (const email of processedEmails) {
            // Count by category
            const category = email.category || 'uncategorized';
            summary.by_category[category] = (summary.by_category[category] || 0) + 1;
            
            // Count by priority
            const priority = email.priority || 'low';
            summary.by_priority[priority] = (summary.by_priority[priority] || 0) + 1;
            
            // Count action required
            if (email.action_required) {
                summary.action_required++;
            }
        }
        
        return summary;
    }
    
    async sendDailyDigest(summary) {
        const digestMessage = `
📊 **Daily Email Digest - ${new Date().toLocaleDateString()}**

📈 **Statistics:**
• Total emails processed: ${summary.total}
• Emails requiring action: ${summary.action_required}

📁 **By Category:**
${Object.entries(summary.by_category)
    .map(([cat, count]) => `• ${cat}: ${count}`)
    .join('\n')}

⚡ **By Priority:**
${Object.entries(summary.by_priority)
    .map(([priority, count]) => `• ${priority}: ${count}`)
    .join('\n')}

📊 **View full report:** ${this.config.trackingSheetId ? 
    `https://docs.google.com/spreadsheets/d/${this.config.trackingSheetId}` : 
    'Not configured'}
        `;
        
        if (this.config.digestChannel) {
            await this.slack.sendMessage(this.config.digestChannel, digestMessage);
        }
    }
}

// Usage
async function main() {
    const { IncredibleClient } = require('../../src');
    
    const client = new IncredibleClient({
        apiKey: process.env.INCREDIBLE_API_KEY
    });
    
    const config = {
        userId: process.env.USER_ID,
        trackingSheetId: process.env.EMAIL_TRACKING_SHEET_ID,
        urgentAlertsChannel: '#urgent-alerts',
        digestChannel: '#daily-digest'
    };
    
    const emailSuite = new EmailAutomationSuite(client, config);
    const result = await emailSuite.execute();
    
    console.log('Email automation completed:', result);
}

if (require.main === module) {
    main().catch(console.error);
}

module.exports = EmailAutomationSuite;
```

### 2. Research Assistant Agent

AI-powered research and report generation.

```javascript
// examples/ai-agents/research-assistant.js
const Agent = require('../../src/incredible-sdk/agent');

class ResearchAssistantAgent extends Agent {
    setupFunctions() {
        this.functions.register(
            'web_search',
            'Search the web for information',
            {
                type: 'object',
                properties: {
                    query: { type: 'string', description: 'Search query' },
                    num_results: { type: 'number', description: 'Number of results to return' }
                }
            },
            this.webSearch.bind(this)
        );
        
        this.functions.register(
            'summarize_content',
            'Summarize content into key points',
            {
                type: 'object',
                properties: {
                    content: { type: 'string', description: 'Content to summarize' },
                    max_points: { type: 'number', description: 'Maximum key points' }
                }
            },
            this.summarizeContent.bind(this)
        );
    }
    
    async execute(researchTopic) {
        this.log(`Starting research on: ${researchTopic}`);
        
        try {
            // Step 1: Conduct initial research
            const initialResearch = await this.conductResearch(researchTopic);
            
            // Step 2: Analyze and synthesize findings
            const analysis = await this.analyzeFindings(initialResearch);
            
            // Step 3: Generate comprehensive report
            const report = await this.generateReport(researchTopic, analysis);
            
            // Step 4: Save to Google Sheets
            const reportUrl = await this.saveReport(researchTopic, report);
            
            // Step 5: Distribute findings
            await this.distributeReport(researchTopic, report, reportUrl);
            
            return {
                status: 'completed',
                topic: researchTopic,
                findings: analysis.key_findings,
                report_url: reportUrl
            };
            
        } catch (error) {
            this.log(`Research failed: ${error.message}`, 'error');
            throw error;
        }
    }
    
    async conductResearch(topic) {
        this.log('Conducting initial research');
        
        // Define research areas
        const researchAreas = [
            `${topic} overview definition`,
            `${topic} current trends 2024`,
            `${topic} market analysis`,
            `${topic} challenges problems`,
            `${topic} future predictions`
        ];
        
        const results = [];
        
        for (const area of researchAreas) {
            const searchResults = await this.webSearch({ query: area, num_results: 5 });
            results.push({
                area,
                results: searchResults
            });
            
            // Respect rate limits
            await this.delay(2000);
        }
        
        return results;
    }
    
    async webSearch({ query, num_results = 5 }) {
        // Use Perplexity integration for web search
        try {
            const response = await this.client.executeIntegration('perplexity', 'PerplexityAISearch', {
                userId: this.userId,
                query,
                max_results: num_results
            });
            
            return response.result || [];
        } catch (error) {
            this.log(`Web search failed for "${query}": ${error.message}`, 'error');
            return [];
        }
    }
    
    async analyzeFindings(research) {
        this.log('Analyzing research findings');
        
        const allContent = research
            .flatMap(area => area.results)
            .map(result => result.content || result.summary)
            .join('\n\n');
        
        const analysisPrompt = `
        Analyze this research content and provide a structured analysis:
        
        ${allContent.substring(0, 8000)} // Limit content length
        
        Provide a JSON response with:
        - key_findings: Array of 5-7 most important findings
        - themes: Major themes identified
        - insights: Key insights and implications
        - gaps: Information gaps that need more research
        - recommendations: 3-5 actionable recommendations
        `;
        
        const response = await this.client.chatCompletion({
            messages: [{ role: 'user', content: analysisPrompt }],
            functions: this.functions.getFunctionDefinitions(),
            functionExecutor: this.functions
        });
        
        return this.extractAnalysisResult(response);
    }
    
    async summarizeContent({ content, max_points = 5 }) {
        const prompt = `
        Summarize this content into ${max_points} key points:
        
        ${content}
        
        Return as a JSON array of strings, each being a concise key point.
        `;
        
        const response = await this.client.chatCompletion({
            messages: [{ role: 'user', content: prompt }]
        });
        
        const summary = this.extractAnalysisResult(response);
        return Array.isArray(summary) ? summary : [summary];
    }
    
    async generateReport(topic, analysis) {
        this.log('Generating comprehensive report');
        
        const reportPrompt = `
        Create a comprehensive research report on "${topic}" based on this analysis:
        
        ${JSON.stringify(analysis, null, 2)}
        
        The report should include:
        1. Executive Summary
        2. Key Findings
        3. Market Analysis
        4. Challenges and Opportunities
        5. Recommendations
        6. Conclusion
        
        Format as a professional business report.
        `;
        
        const response = await this.client.chatCompletion({
            messages: [{ role: 'user', content: reportPrompt }]
        });
        
        return response.result.response[0].content;
    }
    
    async saveReport(topic, report) {
        if (!this.config.reportsSheetId) {
            this.log('No reports sheet configured, skipping save');
            return null;
        }
        
        const timestamp = new Date().toISOString();
        const reportRow = [
            timestamp,
            topic,
            report.substring(0, 32000), // Sheets cell limit
            'Generated',
            this.userId
        ];
        
        await this.sheets.addRow(this.config.reportsSheetId, reportRow);
        
        return `https://docs.google.com/spreadsheets/d/${this.config.reportsSheetId}`;
    }
    
    async distributeReport(topic, report, reportUrl) {
        const summary = report.substring(0, 500) + '...';
        
        const message = `
📊 **Research Report Completed**

🔍 **Topic:** ${topic}
📅 **Date:** ${new Date().toLocaleDateString()}
📝 **Summary:** ${summary}

${reportUrl ? `📊 **Full Report:** ${reportUrl}` : ''}

🤖 Generated by Research Assistant Agent
        `;
        
        if (this.config.reportsChannel) {
            await this.slack.sendMessage(this.config.reportsChannel, message);
        }
        
        // Email to stakeholders if configured
        if (this.config.reportRecipients?.length > 0) {
            for (const recipient of this.config.reportRecipients) {
                await this.emailReport(recipient, topic, report);
            }
        }
    }
    
    async emailReport(recipient, topic, report) {
        const subject = `Research Report: ${topic}`;
        const body = `
Research Report: ${topic}
Generated: ${new Date().toLocaleDateString()}

${report}

---
Generated by Incredible API Research Assistant
        `;
        
        try {
            await this.gmail.sendEmail(recipient, subject, body);
            this.log(`Report emailed to ${recipient}`);
        } catch (error) {
            this.log(`Failed to email report to ${recipient}: ${error.message}`, 'error');
        }
    }
}

// Usage
async function main() {
    const { IncredibleClient } = require('../../src');
    
    const client = new IncredibleClient({
        apiKey: process.env.INCREDIBLE_API_KEY
    });
    
    const config = {
        userId: process.env.USER_ID,
        reportsSheetId: process.env.REPORTS_SHEET_ID,
        reportsChannel: '#research-reports',
        reportRecipients: ['team@company.com']
    };
    
    const researchAgent = new ResearchAssistantAgent(client, config);
    
    // Research a topic
    const topic = process.argv[2] || 'Artificial Intelligence in Healthcare';
    const result = await researchAgent.execute(topic);
    
    console.log('Research completed:', result);
}

if (require.main === module) {
    main().catch(console.error);
}

module.exports = ResearchAssistantAgent;
```

## Testing Framework

### Unit Tests

```javascript
// tests/client.test.js
const { IncredibleClient } = require('../src');
const nock = require('nock');

describe('IncredibleClient', () => {
    let client;
    
    beforeEach(() => {
        client = new IncredibleClient({
            apiKey: 'test-key',
            baseUrl: 'https://api.test.com'
        });
    });
    
    afterEach(() => {
        nock.cleanAll();
    });
    
    test('should make chat completion request', async () => {
        const mockResponse = {
            result: {
                response: [{ role: 'assistant', content: 'Hello!' }]
            }
        };
        
        nock('https://api.test.com')
            .post('/v1/chat-completion')
            .reply(200, mockResponse);
        
        const response = await client.chatCompletion({
            messages: [{ role: 'user', content: 'Hi' }]
        });
        
        expect(response).toEqual(mockResponse);
    });
    
    test('should handle rate limit errors', async () => {
        nock('https://api.test.com')
            .post('/v1/chat-completion')
            .reply(429, {}, { 'retry-after': '60' });
        
        await expect(client.chatCompletion({
            messages: [{ role: 'user', content: 'Hi' }]
        })).rejects.toThrow('Rate limit exceeded');
    });
});
```

### Integration Tests

```javascript
// tests/integration.test.js
const { IncredibleClient } = require('../src');
const { GmailHelper } = require('../src/incredible-sdk/integrations');

describe('Integration Tests', () => {
    let client;
    let gmail;
    
    beforeAll(() => {
        if (!process.env.TEST_API_KEY) {
            throw new Error('TEST_API_KEY environment variable required for integration tests');
        }
        
        client = new IncredibleClient({
            apiKey: process.env.TEST_API_KEY
        });
        
        gmail = new GmailHelper(client, process.env.TEST_USER_ID);
    });
    
    test('should list integrations', async () => {
        const integrations = await client.listIntegrations();
        expect(Array.isArray(integrations)).toBe(true);
        expect(integrations.length).toBeGreaterThan(0);
    }, 10000);
    
    test('should search emails', async () => {
        if (!process.env.RUN_INTEGRATION_TESTS) {
            return;
        }
        
        const emails = await gmail.search('test', 5);
        expect(Array.isArray(emails)).toBe(true);
        expect(emails.length).toBeLessThanOrEqual(5);
    }, 10000);
});
```

## Package Configuration

### package.json

```json
{
  "name": "incredible-api-sdk-js",
  "version": "1.0.0",
  "description": "JavaScript SDK for Incredible API",
  "main": "src/index.js",
  "scripts": {
    "test": "jest",
    "test:integration": "RUN_INTEGRATION_TESTS=true jest",
    "example:basic": "node examples/basic-usage.js",
    "example:email": "node examples/email-automation/email-suite.js",
    "example:research": "node examples/ai-agents/research-assistant.js",
    "lint": "eslint src/ examples/ tests/",
    "lint:fix": "eslint src/ examples/ tests/ --fix"
  },
  "dependencies": {
    "axios": "^1.6.0",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "nock": "^13.4.0",
    "eslint": "^8.55.0"
  },
  "keywords": ["api", "automation", "ai", "integrations"],
  "author": "Incredible API",
  "license": "MIT"
}
```

## Best Practices

### 1. Error Handling
```javascript
const { IncredibleAPIError, RateLimitError } = require('./src/incredible-sdk/exceptions');

async function robustApiCall(operation) {
    const maxRetries = 3;
    let attempt = 0;
    
    while (attempt < maxRetries) {
        try {
            return await operation();
        } catch (error) {
            if (error instanceof RateLimitError) {
                const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
                console.log(`Rate limited, retrying in ${delay}ms`);
                await new Promise(resolve => setTimeout(resolve, delay));
                attempt++;
            } else {
                throw error;
            }
        }
    }
    
    throw new Error(`Operation failed after ${maxRetries} attempts`);
}
```

### 2. Configuration Management
```javascript
// config/settings.js
const config = {
    api: {
        key: process.env.INCREDIBLE_API_KEY,
        baseUrl: process.env.INCREDIBLE_BASE_URL || 'https://api.incredible.one',
        timeout: parseInt(process.env.API_TIMEOUT) || 30000,
        retryAttempts: parseInt(process.env.RETRY_ATTEMPTS) || 3
    },
    integrations: {
        gmail: {
            userId: process.env.GMAIL_USER_ID
        },
        sheets: {
            userId: process.env.SHEETS_USER_ID
        },
        slack: {
            userId: process.env.SLACK_USER_ID
        }
    },
    logging: {
        level: process.env.LOG_LEVEL || 'info'
    }
};

module.exports = config;
```

### 3. Monitoring
```javascript
// monitoring/metrics.js
const EventEmitter = require('events');

class MetricsCollector extends EventEmitter {
    constructor() {
        super();
        this.metrics = {
            apiCalls: 0,
            errors: 0,
            totalDuration: 0
        };
    }
    
    recordApiCall(duration, success = true) {
        this.metrics.apiCalls++;
        this.metrics.totalDuration += duration;
        
        if (!success) {
            this.metrics.errors++;
        }
        
        this.emit('metric', {
            type: 'api_call',
            duration,
            success,
            timestamp: Date.now()
        });
    }
    
    getStats() {
        return {
            ...this.metrics,
            avgDuration: this.metrics.apiCalls > 0 ? 
                this.metrics.totalDuration / this.metrics.apiCalls : 0,
            errorRate: this.metrics.apiCalls > 0 ? 
                this.metrics.errors / this.metrics.apiCalls : 0
        };
    }
}

module.exports = new MetricsCollector();
```

## Deployment

### Production Setup

```javascript
// production/server.js
const express = require('express');
const { IncredibleClient } = require('../src');
const config = require('../config/settings');

const app = express();
const client = new IncredibleClient(config.api);

app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Webhook endpoint for email automation
app.post('/webhooks/email', async (req, res) => {
    try {
        const emailData = req.body;
        
        // Process email with automation suite
        const result = await processEmailWebhook(emailData);
        
        res.json({ success: true, result });
    } catch (error) {
        console.error('Webhook processing failed:', error);
        res.status(500).json({ error: error.message });
    }
});

// Start server
const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
```

## Next Steps

This JavaScript SDK provides comprehensive tools for building production applications with the Incredible API. Key next steps:

1. **[Explore Python SDK](../python/)** - If you need Python support
2. **[Advanced Patterns](../../advanced/)** - Learn architectural patterns  
3. **[Production Deployment](../../advanced/deployment/)** - Scale your applications
4. **[Community Examples](https://github.com/incredible-api/community-examples)** - See what others are building

The JavaScript SDK is designed for modern Node.js applications with async/await support, comprehensive error handling, and production-ready patterns.
