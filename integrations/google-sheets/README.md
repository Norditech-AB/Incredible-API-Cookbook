# Google Sheets Integration Guide

Complete guide to integrating Google Sheets with Incredible API for data management, automation, and intelligent spreadsheet operations.

## 📊 **Google Sheets Integration Overview**

The Google Sheets integration allows your agents to:
- **📝 Read Data**: Access and query spreadsheet data
- **✏️ Write Data**: Create, update, and append information
- **📋 Manage Sheets**: Create new sheets and manage structure
- **📊 Format Data**: Apply formatting and validation rules
- **🔗 Automate Workflows**: Connect spreadsheets to other systems

## 🔐 **Authentication Setup**

Google Sheets uses OAuth 2.0 authentication for secure access to user spreadsheets.

### 1. **OAuth Configuration**

<div class="code-tabs" data-section="sheets-oauth">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python">import requests

def initiate_sheets_oauth():
    """Start Google Sheets OAuth flow"""
    url = "https://api.incredible.one/v1/integrations/google_sheets/connect"
    
    data = {
        "user_id": "your_user_id",
        "callback_url": "https://your-app.com/oauth/sheets"
    }
    
    response = requests.post(url, json=data, headers={
        "Authorization": "Bearer YOUR_API_KEY"
    })
    
    if response.status_code == 200:
        result = response.json()
        print(f"Visit: {result['redirect_url']}")
        return result['redirect_url']
    else:
        print("OAuth initiation failed")
        return None

# Usage
oauth_url = initiate_sheets_oauth()
print(f"Complete OAuth at: {oauth_url}")</code></pre>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">const axios = require('axios');

async function initiateSheetsOAuth() {
    // Start Google Sheets OAuth flow
    const url = "https://api.incredible.one/v1/integrations/google_sheets/connect";
    
    const data = {
        user_id: "your_user_id",
        callback_url: "https://your-app.com/oauth/sheets"
    };
    
    try {
        const response = await axios.post(url, data, {
            headers: {
                "Authorization": "Bearer YOUR_API_KEY"
            }
        });
        
        console.log(`Visit: ${response.data.redirect_url}`);
        return response.data.redirect_url;
    } catch (error) {
        console.log("OAuth initiation failed:", error.response?.data);
        return null;
    }
}

// Usage
const oauthUrl = await initiateSheetsOAuth();
console.log(`Complete OAuth at: ${oauthUrl}`);</code></pre>
  </div>
</div>

### 2. **Required Scopes**

The Google Sheets integration requests these OAuth scopes:
- `https://www.googleapis.com/auth/spreadsheets` - Read and write spreadsheets
- `https://www.googleapis.com/auth/drive.file` - Access to created/opened files

## 🛠️ **Available Features**

### 📖 **Read Data**

<div class="code-tabs" data-section="sheets-read">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python">def read_sheet_data(spreadsheet_id, range_name):
    """Read data from Google Sheets"""
    url = "https://api.incredible.one/v1/integrations/google_sheets/execute"
    
    data = {
        "user_id": "your_user_id",
        "feature_name": "sheets_read_range",
        "inputs": {
            "spreadsheet_id": spreadsheet_id,
            "range": range_name
        }
    }
    
    response = requests.post(url, json=data, headers={
        "Authorization": "Bearer YOUR_API_KEY"
    })
    
    if response.status_code == 200:
        result = response.json()
        values = result['result']['values']
        print(f"Read {len(values)} rows")
        return values
    else:
        print(f"Read failed: {response.text}")
        return []

# Usage examples
# Read entire sheet
all_data = read_sheet_data("1BcD3FgHiJkLmNoPqRsTuVwXyZ", "Sheet1")

# Read specific range
header_row = read_sheet_data("1BcD3FgHiJkLmNoPqRsTuVwXyZ", "Sheet1!A1:E1")

# Read column data
customer_names = read_sheet_data("1BcD3FgHiJkLmNoPqRsTuVwXyZ", "Customers!A:A")

# Convert to structured data
def parse_sheet_data(values):
    if not values:
        return []
    
    headers = values[0]
    rows = []
    for row in values[1:]:
        # Pad row if shorter than headers
        padded_row = row + [''] * (len(headers) - len(row))
        rows.append(dict(zip(headers, padded_row)))
    
    return rows

customers = parse_sheet_data(read_sheet_data("spreadsheet_id", "Customers!A:E"))</code></pre>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">async function readSheetData(spreadsheetId, rangeName) {
    // Read data from Google Sheets
    const url = "https://api.incredible.one/v1/integrations/google_sheets/execute";
    
    const data = {
        user_id: "your_user_id",
        feature_name: "sheets_read_range",
        inputs: {
            spreadsheet_id: spreadsheetId,
            range: rangeName
        }
    };
    
    try {
        const response = await axios.post(url, data, {
            headers: {
                "Authorization": "Bearer YOUR_API_KEY"
            }
        });
        
        const values = response.data.result.values;
        console.log(`Read ${values.length} rows`);
        return values;
    } catch (error) {
        console.log("Read failed:", error.response?.data);
        return [];
    }
}

// Usage examples
// Read entire sheet
const allData = await readSheetData("1BcD3FgHiJkLmNoPqRsTuVwXyZ", "Sheet1");

// Read specific range
const headerRow = await readSheetData("1BcD3FgHiJkLmNoPqRsTuVwXyZ", "Sheet1!A1:E1");

// Read column data
const customerNames = await readSheetData("1BcD3FgHiJkLmNoPqRsTuVwXyZ", "Customers!A:A");

// Convert to structured data
function parseSheetData(values) {
    if (!values || values.length === 0) {
        return [];
    }
    
    const headers = values[0];
    const rows = [];
    
    for (let i = 1; i < values.length; i++) {
        const row = values[i];
        // Pad row if shorter than headers
        const paddedRow = [...row, ...Array(headers.length - row.length).fill('')];
        const rowObject = {};
        headers.forEach((header, index) => {
            rowObject[header] = paddedRow[index];
        });
        rows.push(rowObject);
    }
    
    return rows;
}

const customers = parseSheetData(await readSheetData("spreadsheet_id", "Customers!A:E"));</code></pre>
  </div>
</div>

### ✏️ **Write & Update Data**

<div class="code-tabs" data-section="sheets-write">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python">def update_sheet_range(spreadsheet_id, range_name, values):
    """Update specific range in Google Sheets"""
    url = "https://api.incredible.one/v1/integrations/google_sheets/execute"
    
    data = {
        "user_id": "your_user_id",
        "feature_name": "sheets_update_range",
        "inputs": {
            "spreadsheet_id": spreadsheet_id,
            "range": range_name,
            "values": values
        }
    }
    
    response = requests.post(url, json=data, headers={
        "Authorization": "Bearer YOUR_API_KEY"
    })
    
    if response.status_code == 200:
        result = response.json()
        print(f"Updated {result['result']['updated_cells']} cells")
        return True
    else:
        print(f"Update failed: {response.text}")
        return False

def append_sheet_data(spreadsheet_id, range_name, values):
    """Append data to Google Sheets"""
    url = "https://api.incredible.one/v1/integrations/google_sheets/execute"
    
    data = {
        "user_id": "your_user_id",
        "feature_name": "sheets_append_data",
        "inputs": {
            "spreadsheet_id": spreadsheet_id,
            "range": range_name,
            "values": values
        }
    }
    
    response = requests.post(url, json=data, headers={
        "Authorization": "Bearer YOUR_API_KEY"
    })
    
    if response.status_code == 200:
        result = response.json()
        print(f"Appended {len(values)} rows")
        return True
    else:
        print(f"Append failed: {response.text}")
        return False

# Usage examples
# Update specific cells
update_sheet_range("spreadsheet_id", "A1:B2", [
    ["Name", "Email"],
    ["John Doe", "john@example.com"]
])

# Append new customer
append_sheet_data("spreadsheet_id", "Customers!A:C", [
    ["Jane Smith", "jane@example.com", "2024-01-15"]
])

# Bulk append multiple rows
new_leads = [
    ["Lead 1", "lead1@example.com", "High"],
    ["Lead 2", "lead2@example.com", "Medium"],
    ["Lead 3", "lead3@example.com", "Low"]
]
append_sheet_data("spreadsheet_id", "Leads!A:C", new_leads)</code></pre>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">async function updateSheetRange(spreadsheetId, rangeName, values) {
    // Update specific range in Google Sheets
    const url = "https://api.incredible.one/v1/integrations/google_sheets/execute";
    
    const data = {
        user_id: "your_user_id",
        feature_name: "sheets_update_range",
        inputs: {
            spreadsheet_id: spreadsheetId,
            range: rangeName,
            values: values
        }
    };
    
    try {
        const response = await axios.post(url, data, {
            headers: {
                "Authorization": "Bearer YOUR_API_KEY"
            }
        });
        
        console.log(`Updated ${response.data.result.updated_cells} cells`);
        return true;
    } catch (error) {
        console.log("Update failed:", error.response?.data);
        return false;
    }
}

async function appendSheetData(spreadsheetId, rangeName, values) {
    // Append data to Google Sheets
    const url = "https://api.incredible.one/v1/integrations/google_sheets/execute";
    
    const data = {
        user_id: "your_user_id",
        feature_name: "sheets_append_data",
        inputs: {
            spreadsheet_id: spreadsheetId,
            range: rangeName,
            values: values
        }
    };
    
    try {
        const response = await axios.post(url, data, {
            headers: {
                "Authorization": "Bearer YOUR_API_KEY"
            }
        });
        
        console.log(`Appended ${values.length} rows`);
        return true;
    } catch (error) {
        console.log("Append failed:", error.response?.data);
        return false;
    }
}

// Usage examples
// Update specific cells
await updateSheetRange("spreadsheet_id", "A1:B2", [
    ["Name", "Email"],
    ["John Doe", "john@example.com"]
]);

// Append new customer
await appendSheetData("spreadsheet_id", "Customers!A:C", [
    ["Jane Smith", "jane@example.com", "2024-01-15"]
]);

// Bulk append multiple rows
const newLeads = [
    ["Lead 1", "lead1@example.com", "High"],
    ["Lead 2", "lead2@example.com", "Medium"],
    ["Lead 3", "lead3@example.com", "Low"]
];
await appendSheetData("spreadsheet_id", "Leads!A:C", newLeads);</code></pre>
  </div>
</div>

### 📋 **Create & Manage Sheets**

<div class="code-tabs" data-section="sheets-manage">
  <div class="code-tabs-header">
    <button class="code-tab-button" data-language="python">Python</button>
    <button class="code-tab-button" data-language="javascript">JavaScript</button>
    <div class="code-tab-header-controls">
      <button class="copy-button">Copy</button>
    </div>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-python">def create_spreadsheet(title, sheet_names=None):
    """Create new Google Spreadsheet"""
    url = "https://api.incredible.one/v1/integrations/google_sheets/execute"
    
    data = {
        "user_id": "your_user_id",
        "feature_name": "create_spreadsheet",
        "inputs": {
            "title": title,
            "sheets": sheet_names or ["Sheet1"]
        }
    }
    
    response = requests.post(url, json=data, headers={
        "Authorization": "Bearer YOUR_API_KEY"
    })
    
    if response.status_code == 200:
        result = response.json()
        spreadsheet_id = result['result']['spreadsheet_id']
        print(f"Created spreadsheet: {spreadsheet_id}")
        return spreadsheet_id
    else:
        print(f"Creation failed: {response.text}")
        return None

def add_sheet(spreadsheet_id, sheet_name):
    """Add new sheet to existing spreadsheet"""
    url = "https://api.incredible.one/v1/integrations/google_sheets/execute"
    
    data = {
        "user_id": "your_user_id",
        "feature_name": "add_sheet",
        "inputs": {
            "spreadsheet_id": spreadsheet_id,
            "sheet_name": sheet_name
        }
    }
    
    response = requests.post(url, json=data, headers={
        "Authorization": "Bearer YOUR_API_KEY"
    })
    
    return response.status_code == 200

# Usage examples
# Create new CRM spreadsheet
crm_id = create_spreadsheet("CRM Database", ["Customers", "Leads", "Deals"])

# Add monthly report sheet
add_sheet(crm_id, "January 2024")</code></pre>
  </div>
  
  <div class="code-tab-content">
    <pre><code class="language-javascript">async function createSpreadsheet(title, sheetNames = null) {
    // Create new Google Spreadsheet
    const url = "https://api.incredible.one/v1/integrations/google_sheets/execute";
    
    const data = {
        user_id: "your_user_id",
        feature_name: "create_spreadsheet",
        inputs: {
            title: title,
            sheets: sheetNames || ["Sheet1"]
        }
    };
    
    try {
        const response = await axios.post(url, data, {
            headers: {
                "Authorization": "Bearer YOUR_API_KEY"
            }
        });
        
        const spreadsheetId = response.data.result.spreadsheet_id;
        console.log(`Created spreadsheet: ${spreadsheetId}`);
        return spreadsheetId;
    } catch (error) {
        console.log("Creation failed:", error.response?.data);
        return null;
    }
}

async function addSheet(spreadsheetId, sheetName) {
    // Add new sheet to existing spreadsheet
    const url = "https://api.incredible.one/v1/integrations/google_sheets/execute";
    
    const data = {
        user_id: "your_user_id",
        feature_name: "add_sheet",
        inputs: {
            spreadsheet_id: spreadsheetId,
            sheet_name: sheetName
        }
    };
    
    try {
        const response = await axios.post(url, data, {
            headers: {
                "Authorization": "Bearer YOUR_API_KEY"
            }
        });
        
        return response.status === 200;
    } catch (error) {
        console.log("Add sheet failed:", error.response?.data);
        return false;
    }
}

// Usage examples
// Create new CRM spreadsheet
const crmId = await createSpreadsheet("CRM Database", ["Customers", "Leads", "Deals"]);

// Add monthly report sheet
await addSheet(crmId, "January 2024");</code></pre>
  </div>
</div>

## 📊 **Range Notation**

Google Sheets uses A1 notation for specifying ranges:

### 📍 **Basic Ranges**
- `A1` - Single cell
- `A1:C3` - Rectangle from A1 to C3
- `A:A` - Entire column A
- `1:1` - Entire row 1
- `A1:C` - From A1 to end of column C

### 📋 **Sheet References**
- `Sheet1!A1:C3` - Range on specific sheet
- `'My Sheet'!A1:C3` - Sheet name with spaces
- `Customers!A:E` - Entire range on Customers sheet

### 🔢 **Dynamic Ranges**
- `A1:A` - Column A starting from A1
- `A2:E` - Range starting from A2 to end of column E
- `2:2` - Entire row 2

## 🎯 **Common Use Cases**

### 📊 **CRM & Lead Tracking**

```python
class SheetsBasedCRM:
    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
    
    def add_lead(self, name, email, source, score):
        """Add new lead to CRM"""
        lead_data = [
            datetime.now().strftime("%Y-%m-%d"),
            name, email, source, score, "New"
        ]
        append_sheet_data(self.spreadsheet_id, "Leads!A:F", [lead_data])
    
    def update_lead_status(self, lead_email, new_status):
        """Update lead status"""
        leads = read_sheet_data(self.spreadsheet_id, "Leads!A:F")
        for i, lead in enumerate(leads[1:], 2):  # Skip header row
            if lead[2] == lead_email:  # Email column
                update_sheet_range(
                    self.spreadsheet_id, 
                    f"Leads!F{i}", 
                    [[new_status]]
                )
                break
    
    def get_leads_by_status(self, status):
        """Get all leads with specific status"""
        leads = read_sheet_data(self.spreadsheet_id, "Leads!A:F")
        return [lead for lead in leads[1:] if lead[5] == status]
```

### 📈 **Analytics & Reporting**

```python
def generate_monthly_report(spreadsheet_id):
    """Generate monthly performance report"""
    # Read sales data
    sales_data = read_sheet_data(spreadsheet_id, "Sales!A:E")
    
    # Calculate metrics
    total_sales = sum(float(row[3]) for row in sales_data[1:])
    avg_deal_size = total_sales / len(sales_data[1:])
    
    # Create report
    report_data = [
        ["Metric", "Value"],
        ["Total Sales", f"${total_sales:,.2f}"],
        ["Average Deal Size", f"${avg_deal_size:,.2f}"],
        ["Total Deals", len(sales_data[1:])],
        ["Report Generated", datetime.now().strftime("%Y-%m-%d %H:%M")]
    ]
    
    # Write to report sheet
    update_sheet_range(spreadsheet_id, "Report!A1:B5", report_data)
```

### 📋 **Inventory Management**

```python
class InventoryTracker:
    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
    
    def update_stock(self, product_id, quantity_change):
        """Update product stock levels"""
        inventory = read_sheet_data(self.spreadsheet_id, "Inventory!A:D")
        
        for i, item in enumerate(inventory[1:], 2):
            if item[0] == product_id:  # Product ID column
                current_stock = int(item[2])
                new_stock = current_stock + quantity_change
                
                update_sheet_range(
                    self.spreadsheet_id,
                    f"Inventory!C{i}",
                    [[new_stock]]
                )
                
                # Check for low stock alerts
                if new_stock < 10:
                    self.send_low_stock_alert(item[1], new_stock)
                break
    
    def send_low_stock_alert(self, product_name, stock_level):
        """Send alert for low stock"""
        print(f"🚨 Low stock alert: {product_name} ({stock_level} remaining)")
```

## 🔒 **Security & Best Practices**

### 🛡️ **Data Protection**
- **Access Control**: Use OAuth to limit access to specific spreadsheets
- **Input Validation**: Validate all data before writing to sheets
- **Error Handling**: Handle API errors and rate limits gracefully
- **Backup Strategy**: Regular backups of critical spreadsheet data

### 📊 **Performance Optimization**
- **Batch Operations**: Combine multiple updates into single API calls
- **Range Optimization**: Read/write specific ranges rather than entire sheets
- **Caching**: Cache frequently accessed data to reduce API calls
- **Pagination**: Handle large datasets with proper pagination

### 🔍 **Data Quality**
- **Validation Rules**: Implement data validation and formatting
- **Consistency**: Maintain consistent data formats and structures
- **Monitoring**: Monitor for data quality issues and anomalies
- **Documentation**: Document sheet structures and data meanings

## 📈 **Advanced Features**

### 📊 **Formula & Calculation Support**

```python
def add_calculated_columns(spreadsheet_id):
    """Add formulas for calculated fields"""
    formulas = [
        ["=SUM(B2:B100)"],          # Total
        ["=AVERAGE(B2:B100)"],      # Average
        ["=COUNT(B2:B100)"],        # Count
        ["=IF(B2>1000,\"High\",\"Low\")"]  # Conditional
    ]
    
    update_sheet_range(spreadsheet_id, "Summary!A1:A4", formulas)
```

### 📋 **Conditional Formatting**

```python
def apply_conditional_formatting(spreadsheet_id):
    """Apply conditional formatting rules"""
    # Color code cells based on values
    # Highlight important rows
    # Format dates and numbers consistently
    pass
```

### 🔗 **Data Validation**

```python
def setup_data_validation(spreadsheet_id):
    """Set up data validation rules"""
    # Dropdown lists for categories
    # Date range validation
    # Number format validation
    # Email format validation
    pass
```

---

*Master Google Sheets integration to create powerful data management workflows that organize, analyze, and automate your business processes.*
