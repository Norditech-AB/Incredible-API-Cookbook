# Multi-Integration Examples

Learn how to combine multiple integrations to create powerful automation workflows with the Incredible API.

## Overview

Multi-integration workflows are where the Incredible API truly shines. By combining up to 3 integrations per agent, you can create sophisticated automation that spans multiple platforms and services.

## Featured Examples

### 🔗 Popular Integration Combinations

| Integration Set             | Use Case                             | Complexity |
| --------------------------- | ------------------------------------ | ---------- |
| Gmail + Sheets + Slack      | Email reporting & team notifications | ⭐⭐       |
| Gmail + Asana + Calendar    | Meeting management workflow          | ⭐⭐⭐     |
| Perplexity + Sheets + Gmail | Research & reporting automation      | ⭐⭐       |
| Slack + Sheets + Asana      | Team productivity dashboard          | ⭐⭐⭐     |

## Quick Start Examples

### 1. Email-to-Spreadsheet Logger

**Integrations**: Gmail + Google Sheets  
**Purpose**: Log important emails to a tracking spreadsheet

```python
def email_to_sheets_workflow():
    # 1. Search for important emails
    emails = search_gmail("is:important")

    # 2. Extract key information
    for email in emails:
        row_data = [email['subject'], email['sender'], email['date']]

        # 3. Add to spreadsheet
        add_to_sheets(spreadsheet_id, row_data)
```

[**View Full Example →**](./email-to-sheets.md)

### 2. Research & Report Generator

**Integrations**: Perplexity + Google Sheets + Gmail  
**Purpose**: Research topics and automatically generate reports

```python
def research_report_workflow(topic):
    # 1. Research the topic
    research_data = search_perplexity(topic)

    # 2. Organize in spreadsheet
    add_research_to_sheets(research_data)

    # 3. Generate and email report
    report = generate_report_from_sheets()
    send_email_report(report)
```

[**View Full Example →**](./research-reporter.md)

### 3. Meeting Management System

**Integrations**: Gmail + Google Calendar + Asana  
**Purpose**: Extract meetings from emails and create comprehensive management workflow

```python
def meeting_management_workflow():
    # 1. Find meeting emails
    meeting_emails = search_gmail("meeting OR call")

    # 2. Create calendar events
    for email in meeting_emails:
        meeting_details = extract_meeting_info(email)
        create_calendar_event(meeting_details)

        # 3. Create preparation tasks
        create_asana_tasks(meeting_details)
```

[**View Full Example →**](./meeting-manager.md)

## Advanced Patterns

### Data Flow Patterns

#### 1. Linear Flow

```
Service A → Process → Service B → Process → Service C
```

Example: Gmail → Extract → Sheets → Analyze → Slack

#### 2. Hub & Spoke

```
      Service A
         ↓
    Central Agent
       ↙    ↘
Service B  Service C
```

Example: Perplexity research feeds both Sheets and Email

#### 3. Conditional Branching

```
Service A → Decision Point
              ↙        ↘
         Service B   Service C
```

Example: Email analysis routes to either Slack or Asana based on content

### Error Handling Across Services

```python
class MultiServiceWorkflow:
    def __init__(self):
        self.failed_operations = []
        self.successful_operations = []

    def execute_with_fallback(self, operations):
        for operation in operations:
            try:
                result = operation.execute()
                self.successful_operations.append((operation, result))
            except Exception as e:
                self.failed_operations.append((operation, e))
                # Continue with remaining operations
                continue

        self.handle_failures()

    def handle_failures(self):
        if self.failed_operations:
            # Log failures
            # Attempt retry logic
            # Send notifications about failures
            pass
```

## Integration Compatibility Matrix

| Primary    | Secondary | Third    | Notes                        |
| ---------- | --------- | -------- | ---------------------------- |
| Gmail      | Sheets    | Slack    | Perfect for email reporting  |
| Gmail      | Asana     | Calendar | Great for meeting management |
| Perplexity | Sheets    | Gmail    | Ideal for research workflows |
| Slack      | Sheets    | Asana    | Team productivity tracking   |
| Gmail      | LinkedIn  | Twitter  | Content distribution         |

## Best Practices

### 1. Service Ordering

- **Start with data sources** (Gmail, Perplexity)
- **Process in the middle** (Sheets, custom functions)
- **End with notifications** (Slack, Email)

### 2. Error Recovery

```python
def resilient_multi_service_call():
    results = {}

    # Try each service independently
    for service_name, service_call in services.items():
        try:
            results[service_name] = service_call()
        except Exception as e:
            results[service_name] = None
            log_error(service_name, e)

    # Proceed with available data
    return process_partial_results(results)
```

### 3. Data Transformation

```python
def standardize_data_between_services(data, from_service, to_service):
    """Transform data formats between different services"""
    transformers = {
        ('gmail', 'sheets'): transform_email_to_row,
        ('perplexity', 'gmail'): transform_search_to_email,
        ('sheets', 'slack'): transform_row_to_message
    }

    transformer = transformers.get((from_service, to_service))
    return transformer(data) if transformer else data
```

## Complete Examples

### 📊 Business Intelligence Workflow

Combine multiple data sources for comprehensive reporting.

```python
class BusinessIntelligenceAgent:
    def generate_weekly_report(self):
        # 1. Gather data from multiple sources
        email_metrics = self.get_email_metrics()
        project_updates = self.get_asana_updates()
        research_insights = self.get_perplexity_trends()

        # 2. Combine and analyze
        report_data = self.combine_data_sources(
            email_metrics, project_updates, research_insights
        )

        # 3. Generate report in Sheets
        report_url = self.create_sheets_report(report_data)

        # 4. Distribute via Slack and Email
        self.send_report_notifications(report_url)
```

[**View Full Implementation →**](./business-intelligence.md)

### 🎯 Lead Management System

Automate lead capture and follow-up across platforms.

```python
class LeadManagementAgent:
    def process_new_leads(self):
        # 1. Monitor multiple lead sources
        gmail_leads = self.scan_gmail_for_leads()
        linkedin_leads = self.check_linkedin_messages()

        # 2. Qualify and score leads
        qualified_leads = self.qualify_leads(gmail_leads + linkedin_leads)

        # 3. Log in CRM (Sheets)
        self.update_lead_database(qualified_leads)

        # 4. Schedule follow-ups (Asana)
        self.create_follow_up_tasks(qualified_leads)

        # 5. Notify sales team (Slack)
        self.alert_sales_team(qualified_leads)
```

[**View Full Implementation →**](./lead-management.md)

## Examples by Industry

### 📈 Sales & Marketing

- [Content Distribution Pipeline](./content-distribution.md)
- [Lead Scoring & Routing](./lead-scoring.md)
- [Social Media Automation](./social-media-automation.md)

### 💼 Operations & HR

- [Employee Onboarding Workflow](./employee-onboarding.md)
- [Expense Report Automation](./expense-automation.md)
- [Project Status Updates](./project-updates.md)

### 📊 Analytics & Reporting

- [Multi-Source Dashboards](./analytics-dashboard.md)
- [Automated Report Generation](./report-generation.md)
- [Performance Monitoring](./performance-monitoring.md)

## Testing Multi-Integration Workflows

### Unit Testing Individual Services

```python
def test_gmail_integration():
    # Test Gmail operations in isolation
    pass

def test_sheets_integration():
    # Test Sheets operations in isolation
    pass

def test_slack_integration():
    # Test Slack operations in isolation
    pass
```

### Integration Testing

```python
def test_gmail_to_sheets_flow():
    # Test data flow between Gmail and Sheets
    pass

def test_complete_workflow():
    # Test the entire multi-service workflow
    pass
```

### Mock Services for Development

```python
class MockGmailService:
    def search_emails(self, query):
        return [{"subject": "Test", "sender": "test@example.com"}]

class MockSheetsService:
    def add_row(self, data):
        return {"status": "success"}
```

## Troubleshooting

### Common Issues

1. **Service Rate Limits**

   - Implement delays between calls
   - Use bulk operations when available
   - Monitor rate limit headers

2. **Data Format Mismatches**

   - Implement data transformation layers
   - Validate data before service calls
   - Use consistent data schemas

3. **Authentication Failures**
   - Implement token refresh logic
   - Handle OAuth expiration gracefully
   - Monitor connection health

### Debug Tools

```python
class WorkflowDebugger:
    def __init__(self):
        self.operation_log = []

    def log_operation(self, service, operation, data, result):
        self.operation_log.append({
            "timestamp": datetime.now(),
            "service": service,
            "operation": operation,
            "input_data": data,
            "result": result
        })

    def export_debug_log(self):
        # Export log for analysis
        pass
```

## Next Steps

Ready to build your own multi-integration workflow? Here's how to proceed:

1. **[Choose Your Use Case](../../../use-cases/)** - Find industry-specific examples
2. **[Plan Your Architecture](../../advanced/architecture-patterns.md)** - Design robust workflows
3. **[Implement Error Handling](../../advanced/error-handling/)** - Build resilient systems
4. **[Monitor & Optimize](../../advanced/performance/)** - Ensure optimal performance

Multi-integration workflows unlock the true potential of automation. Start with simple 2-service combinations and gradually build more sophisticated 3-service workflows as you become comfortable with the patterns.
