---
name: greek-email-processor
description: >
  **希腊会计系统的电子邮件处理功能**  
  该系统通过 IMAP 协议连接外部服务器，用于扫描财务文件、AADE 通知以及发票等重要文档，并将这些文件路由至本地的处理流程（pipelines）中。
version: 1.0.0
author: openclaw-greek-accounting
homepage: https://github.com/satoshistackalotto/openclaw-greek-accounting
tags: ["greek", "accounting", "email", "document-classification", "imap"]
metadata: {"openclaw": {"requires": {"bins": ["jq", "curl"], "env": ["OPENCLAW_DATA_DIR", "IMAP_HOST", "IMAP_USER", "IMAP_PASSWORD"]}, "optional_env": {"SMTP_HOST": "Email server for auto-responses (requires human approval before sending)", "SMTP_USER": "Email account for sending responses", "SMTP_PASSWORD": "Email account password (use app-specific passwords)", "GOOGLE_CLIENT_ID": "Gmail API OAuth client ID (alternative to IMAP for Gmail users)", "GOOGLE_CLIENT_SECRET": "Gmail API OAuth client secret", "MS_CLIENT_ID": "Microsoft Graph API client ID (alternative to IMAP for Outlook users)", "MS_CLIENT_SECRET": "Microsoft Graph API client secret", "GOOGLE_CALENDAR_ID": "Google Calendar ID for deadline event creation", "SLACK_WEBHOOK_URL": "Webhook URL for processing status notifications"}, "notes": "IMAP credentials are the only required credentials — works with any email provider. Gmail API and Microsoft Graph API are optional alternatives that provide richer features. SMTP, Calendar, and Slack integrations are optional notification channels. All auto-responses require human approval."}}
---
# 希腊语电子邮件处理系统

该功能可将 OpenClaw 转变为一个智能的希腊语商务电子邮件处理工具，能够自动检测、分类和处理来自希腊政府机构、银行及商业合作伙伴的财务文件和官方通信。

## 设置

```bash
# 1. Set data directory
export OPENCLAW_DATA_DIR="/data"

# 2. Configure email access (use a scoped service account with read-only access)
export IMAP_HOST="imap.your-provider.com" # e.g. imap.gmail.com, imap.outlook.com
export IMAP_USER="accounting@yourfirm.gr"
export IMAP_PASSWORD="app-specific-password"  # Use app passwords, not main password

# 3. Configure outbound email (optional — only needed for auto-responses)
export SMTP_HOST="smtp.your-provider.com" # e.g. smtp.gmail.com, smtp.outlook.com
export SMTP_USER="accounting@yourfirm.gr"
export SMTP_PASSWORD="app-specific-password"

# 4. Ensure dependencies are installed
which jq curl || sudo apt install jq curl

# 5. Create incoming directories
mkdir -p $OPENCLAW_DATA_DIR/incoming/{invoices,receipts,statements,government}
```

**安全提示：**
- 使用专用的应用程序密码（切勿使用您的主电子邮件密码）
- 为服务账户授予最低必要的权限（仅限 IMAP 的读取权限）
- SMTP 凭据是可选的——仅在启用自动回复功能时需要
- 所有自动回复在发送前均需经过人工审核

## 核心理念

- **优先支持希腊语**：原生支持希腊语电子邮件和文档
- **智能分类**：自动识别文档类型和优先级
- **合规性优先**：特别处理 AADE（希腊税务管理局）、EFKA（希腊财政委员会）及政府通信
- **了解商务语境**：理解希腊商务沟通模式
- **注重隐私**：安全处理电子邮件中的敏感财务信息

## 主要功能

### 1. 希腊语文档识别与分类
- **发票识别**：识别电子邮件附件中的希腊语发票（ΤΙΜθ΂θΓΙθ, ΑΠθΔΕΙξΗ）
- **政府通知**：识别 AADE、EFKA 及市政机构的通信
- **银行对账单**：处理来自希腊主要银行的对账单
- **税务文件**：检测与税务相关的电子邮件和表格
- **客户通信**：分类商务信函和付款请求
- **收据处理**：识别费用收据和商务文件

### 2. 电子邮件提供商集成
- **Gmail / Google Workspace**：通过 IMAP（使用专用应用程序密码）或可选的 Gmail API（设置 GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET）
- **Outlook / Exchange**：通过 IMAP 或可选的 Microsoft Graph API（设置 MS_CLIENT_ID, MS_CLIENT_SECRET）
- **任意 IMAP 提供商**：支持与任意电子邮件提供商的标准 IMAP 连接
- **IMAP/SMTP 提供商**：支持任何兼容 IMAP 的商务电子邮件服务
- **Yahoo Business**：支持 Yahoo 商务电子邮件
- **自定义 IMAP/POP3**：支持希腊语商务电子邮件提供商
- **多账户管理**：同时处理多个电子邮件账户
- **实时监控**：可配置时间间隔的持续收件箱监控

### 3. 希腊语处理
- **希腊语文本识别**：原生支持希腊语电子邮件内容分析
- **混合语言处理**：处理希腊语和英语的商务通信
- **希腊语日期格式**：识别希腊语日期格式（dd/MM/yyyy）
- **货币格式识别**：识别希腊语欧元格式（‚¬1.234,56）
- **地址解析**：识别希腊语地址格式
- **增值税号识别**：在电子邮件中识别希腊语增值税号（EL123456789）

### 4. 自动化处理流程
- **文档提取**：自动下载和处理附件
- **智能转发**：将电子邮件路由到相应的处理流程
- **客户通知**：以希腊语自动回复文档接收情况
- **优先级提升**：标记紧急邮件（如逾期付款、政府通知）
- **日历集成**（可选）：如果配置了 GOOGLE_CALENDAR_ID，可为付款截止日期创建日历事件
- **任务创建**：根据电子邮件内容生成会计任务

## 实施指南

### 电子邮件监控架构

#### IMAP 电子邮件集成
```yaml
IMAP_Configuration:
  imap_permissions:
    protocol: "IMAP for reading, SMTP for sending"
    security: "TLS/SSL required"
  
  monitoring_labels:
    - "INBOX"
    - "UNREAD"
    - "IMPORTANT"
    - custom_labels: ["Accounting", "Tax", "Invoices"]
  
  search_queries:
    invoices: "subject:(πžιμολςγιο OR invoice OR αποδειξη OR receipt)"
    tax_documents: "from:aade.gr OR from:efka.gov.gr OR subject:π πα"
    bank_statements: "from:alphabank.gr OR from:nbg.gr OR from:eurobank.gr OR from:piraeusbank.gr"
    client_payments: "subject:(πληρπ°μή OR payment OR οπ ειλή OR due)"
```

#### IMAP/SMTP 提供商集成
```yaml
Alternative_Provider_Notes:
  microsoft_graph_scopes:
    - "https://graph.microsoft.com/Mail.Read"
    - "https://graph.microsoft.com/Mail.Send"
    - "https://graph.microsoft.com/Mail.ReadWrite"
  
  folder_monitoring:
    - "Inbox"
    - "Accounting"
    - "Tax Documents" 
    - "Bank Statements"
  
  advanced_queries:
    greek_invoices: "subject:πžιμολςγιο OR attachmentNames:invoice"
    government_mail: "from:gov.gr OR from:aade.gr"
    banking: "from:bank OR from:πžράπεζα"
```

### 文档分类引擎

#### 希腊语文档类型
```yaml
Document_Classification:
  invoices:
    greek_keywords: ["πžιμολςγιο", "αποδειξη", "παρασπžαπžικς", "invoice"]
    file_patterns: ["*.pdf", "*.xml", "*.doc*"]
    confidence_thresholds:
      high: 0.95  # Clear invoice format
      medium: 0.80  # Probable invoice
      low: 0.60   # Possible invoice
    
  tax_documents:
    aade_keywords: ["π πα", "π ςροπš", "δήλπ°ση", "εκκαθαρισπžικς"]
    sender_patterns: ["*@aade.gr", "*@taxisnet.gr"]
    subject_patterns: ["*ΦΠΑ*", "*TAX*", "*ENFIA*"]
    
  bank_statements:
    greek_banks: ["Alpha Bank", "Εθνική Τράπεζα", "Eurobank", "Τράπεζα ΠειραιϽπš"]
    keywords: ["κίνηση λογαριασμού", "statement", "ανπžίγραπ ο", "υπςλοιπο"]
    formats: ["pdf", "csv", "xls", "xlsx"]
    
  receipts:
    keywords: ["αποδειξη", "παρασπžαπžικς", "πžιμολςγιο λιανικήπš", "receipt"]
    amount_patterns: ["‚¬\\d+[.,]\\d+", "\\d+[.,]\\d+\\s*‚¬", "\\d+[.,]\\d+\\s*EUR"]
    vat_patterns: ["ΦΠΑ \\d+%", "VAT \\d+%"]
    
  client_communications:
    payment_keywords: ["πληρπ°μή", "οπ ειλή", "λογαριασμςπš", "πžιμολςγηση"]
    request_keywords: ["παρακαλϽ", "αίπžημα", "π¡ρειάζομαι", "σπžείλπžε"]
    urgent_keywords: ["επείγον", "urgent", "άμεσα", "προθεσμία"]
```

#### 智能内容分析
```yaml
Content_Analysis_Rules:
  priority_detection:
    high_priority:
      - government_communications: "Emails from AADE, EFKA, municipalities"
      - payment_due: "Overdue payment notices"
      - audit_requests: "Tax audit or compliance requests"
      - system_outages: "TAXIS, myDATA system announcements"
      
    medium_priority:
      - new_invoices: "Incoming invoices from suppliers"
      - bank_notifications: "Bank statement availability"
      - client_requests: "Client document requests"
      - deadline_reminders: "Tax or compliance deadline notices"
      
    low_priority:
      - newsletters: "Professional service newsletters"
      - marketing: "Software or service promotions"
      - routine_confirmations: "Standard transaction confirmations"
  
  automated_actions:
    high_priority_actions:
      - immediate_notification: "notification to assigned accountant"
      - create_calendar_event: "Add deadline to calendar"
      - create_task: "Generate action item in task management"
      - escalate_to_human: "Flag for immediate attention"
      
    medium_priority_actions:
      - extract_attachments: "Download and process documents"
      - forward_to_processing: "Send to document processing pipeline"
      - send_confirmation: "Automated receipt confirmation in Greek"
      - update_client_records: "Log communication in client file"
      
    low_priority_actions:
      - archive_appropriately: "File in correct folder"
      - update_newsletter_tracking: "Mark as read, file for reference"
```

### 希腊语处理引擎

#### 语言检测与解析
```yaml
Greek_Language_Support:
  text_processing:
    encoding: "UTF-8"
    character_sets: ["ISO-8859-7", "Windows-1253", "UTF-8"]
    
  date_recognition:
    greek_months: ["Ιανουάριοπš", "Φεβρουάριοπš", "Μάρπžιοπš", "Απρίλιοπš", "Μάιοπš", "Ιούνιοπš", "Ιούλιοπš", "Αύγουσπžοπš", "Σεππžέμβριοπš", "θκπžϽβριοπš", "Νοέμβριοπš", "Δεκέμβριοπš"]
    date_patterns: ["dd/MM/yyyy", "dd-MM-yyyy", "dd.MM.yyyy", "dd Μμμμ yyyy"]
    
  currency_recognition:
    euro_patterns: ["‚¬\\d+[.,]\\d+", "\\d+[.,]\\d+\\s*‚¬", "\\d+[.,]\\d+\\s*EUR", "\\d+[.,]\\d+\\s*ευρϽ"]
    greek_numerals: Support for Greek number formatting (1.234,56)
    
  vat_number_detection:
    greek_pattern: "EL\\d{9}"
    validation: "Check digit validation for Greek VAT numbers"
    
  address_parsing:
    greek_patterns: "Street number, area, postal code, city format"
    common_abbreviations: ["΀ºεπ°π .", "θδςπš", "Πλαπžεία", "Τ.Ρ."]
    
  business_terminology:
    accounting_terms: ["λογισπžήριο", "π οροπžεπ¡νικςπš", "ΦΠΑ", "ΕΝΦΙΑ", "ΕΦΡΑ"]
    legal_entities: ["Α.Ε.", "Ε.Π.Ε.", "θ.Ε.", "Ε.Ε.", "Ι.Ρ.Ε."]
```

#### 希腊语电子邮件模板
```yaml
Automated_Response_Templates:
  invoice_received:
    subject: "Επιβεβαίπ°ση παραλαβήπš πžιμολογίου - {invoice_number}"
    body: |
      Αγαπηπžέ/ή {sender_name},
      
      ΕπιβεβαιϽνουμε πžην παραλαβή πžου πžιμολογίου {invoice_number} 
      ημερομηνίαπš {invoice_date} συνολικήπš αξίαπš {total_amount}.
      
      Το πžιμολςγιο έπ¡ει προπ°θηθεί σπžο λογισπžήρις μαπš για επεξεργασία.
      Η πληρπ°μή θα πραγμαπžοποιηθεί ενπžςπš {payment_terms}.
      
      Με εκπžίμηση,
      {company_name}
      
  document_request:
    subject: "Αίπžημα για πρςσθεπžα έγγραπ α - {reference_number}"
    body: |
      Αγαπηπžέ/ή {client_name},
      
      Για πžην ολοκλήρπ°ση πžηπš λογισπžικήπš επεξεργασίαπš, π¡ρειαζςμασπžε 
      πžα ακςλουθα έγγραπ α:
      
      {required_documents}
      
      Παρακαλούμε σπžείλπžε πžα έγγραπ α πžο συνπžομςπžερο δυναπžς.
      
      Ευπ¡αρισπžούμε,
      {accountant_name}
      
  payment_reminder:
    subject: "Υπενθύμιση πληρπ°μήπš - {invoice_number}"
    body: |
      Αγαπηπžέ/ή {client_name},
      
      Σαπš υπενθυμίζουμε ςπžι πžο πžιμολςγιο {invoice_number} 
      αξίαπš {amount} είπ¡ε λήξει πžην {due_date}.
      
      Παρακαλούμε προβείπžε σπžην πληρπ°μή πžο συνπžομςπžερο δυναπžς.
      
      Για οποιαδήποπžε διευκρίνιση, επικοινπ°νήσπžε μαζί μαπš.
      
      Με εκπžίμηση,
      {company_name}
```

## 工作流程模板

### 每日电子邮件处理流程

#### 早上 8:00（希腊时间）扫描电子邮件
```bash
#!/bin/bash
# Morning email processing workflow

# Check all configured email accounts
openclaw email scan all-accounts --since "24 hours ago"

# Process government emails first (highest priority)
openclaw email process --filter "government" --priority high

# Process banking notifications
openclaw email process --filter "banking" --auto-download-statements

# Process client invoices and payments
openclaw email process --filter "invoices" --auto-extract-data

# Process client communications
openclaw email process --filter "client-communications" --auto-respond

# Generate morning email summary
openclaw email summary daily --include-urgent --include-actions-needed
```

#### 每 15 分钟持续监控
```bash
#!/bin/bash
# Real-time email monitoring

# Quick scan for urgent emails
openclaw email scan --filter "urgent" --real-time

# Process AADE/EFKA notifications immediately
openclaw email process --filter "government" --immediate-alert

# Handle client payment confirmations
openclaw email process --filter "payments" --update-accounting-system

# Auto-respond to routine requests
openclaw email auto-respond --filter "routine" --use-greek-templates
```

#### 下午 6:00（希腊时间）结束当天处理
```bash
#!/bin/bash
# End of day email processing

# Process any remaining unread emails
openclaw email process --filter "unread" --batch-process

# Generate daily email report
openclaw email report daily --include-statistics --include-pending

# Archive processed emails appropriately
openclaw email archive --processed-today --by-category

# Prepare tomorrow's email agenda
openclaw email agenda tomorrow --include-expected --include-deadlines
```

### 集成流程

#### AADE 电子邮件集成
```yaml
AADE_Email_Processing:
  sender_domains:
    - "@aade.gr"
    - "@taxisnet.gr"
    - "@mydata.aade.gr"
    
  automatic_actions:
    tax_deadline_changes:
      - extract_new_deadline: "Parse email content for deadline changes"
      - update_calendar: "Update compliance deadline tracker immediately"
      - alert_clients: "Notify affected clients of deadline changes"
      - log_compliance: "Record change in compliance tracking system"
      
    system_maintenance_notices:
      - extract_maintenance_window: "Parse maintenance dates and times"
      - alert_users: "Notify users of planned system outages"
      - reschedule_activities: "Move planned TAXIS submissions if needed"
      
    audit_notifications:
      - high_priority_alert: "Immediate notification to assigned accountant"
      - create_urgent_task: "Generate audit response task"
      - gather_documents: "Prepare standard audit documentation"
      - legal_consultation: "Flag for legal review if needed"
```

#### 银行电子邮件集成
```yaml
Greek_Bank_Email_Processing:
  supported_banks:
    alpha_bank:
      domains: ["@alphabank.gr", "@alpha.gr"]
      statement_patterns: ["statement", "κίνηση λογαριασμού"]
      
    national_bank:
      domains: ["@nbg.gr", "@ethnikibank.gr"]
      statement_patterns: ["ανπžίγραπ ο κίνησηπš", "account statement"]
      
    eurobank:
      domains: ["@eurobank.gr"]
      statement_patterns: ["κίνηση λογαριασμού", "λογαριασμςπš κίνησηπš"]
      
    piraeus_bank:
      domains: ["@piraeusbank.gr", "@winbank.gr"]
      statement_patterns: ["statement", "κίνηση", "υπςλοιπο"]
      
  processing_workflow:
    statement_detection:
      - verify_sender: "Confirm email is from legitimate bank domain"
      - extract_attachments: "Download PDF/CSV statement files"
      - parse_account_info: "Extract account numbers and dates"
      - integrate_accounting: "Forward to bank reconciliation system"
      
    payment_confirmations:
      - match_transactions: "Match with pending payment records"
      - update_client_accounts: "Mark invoices as paid"
      - generate_receipts: "Create payment confirmation documents"
      
    fraud_detection:
      - verify_bank_signatures: "Check for legitimate bank formatting"
      - flag_suspicious: "Alert for unusual sender patterns"
      - security_validation: "Verify against known bank communication patterns"
```

## 高级功能

### 客户通信自动化

#### 智能自动回复系统
```yaml
Auto_Response_Logic:
  invoice_submissions:
    conditions:
      - "Email contains PDF attachment"
      - "Subject contains 'πžιμολςγιο' or 'invoice'"
      - "Sender is known client"
    actions:
      - send_confirmation: "Automated receipt confirmation in Greek"
      - extract_invoice_data: "Process invoice for accounting system"
      - create_payment_schedule: "Add to payment processing queue"
      
  document_requests:
    conditions:
      - "Email contains request for documents"
      - "Keywords: 'σπžείλπžε', 'π¡ρειάζομαι', 'παρακαλϽ'"
    actions:
      - acknowledge_request: "Confirm receipt of request"
      - generate_document_list: "List available documents"
      - schedule_follow_up: "Set reminder if documents not sent"
      
  payment_inquiries:
    conditions:
      - "Subject contains 'πληρπ°μή' or 'payment'"
      - "Client asking about payment status"
    actions:
      - check_payment_status: "Query accounting system"
      - send_status_update: "Provide current payment status"
      - attach_receipt: "Include payment confirmation if paid"
```

### 多账户管理

#### 账户配置
```yaml
Multi_Account_Setup:
  primary_business_account:
    email: "accounting@company.gr"
    protocol: "IMAP"
    processing_priority: "high"
    auto_responses: "enabled"
    
  client_communication_account:
    email: "info@company.gr"  
    protocol: "IMAP"
    processing_priority: "medium"
    auto_responses: "enabled"
    
  government_notifications_account:
    email: "compliance@company.gr"
    protocol: "IMAP"
    processing_priority: "critical"
    auto_responses: "disabled"
    
  bank_statements_account:
    email: "banking@company.gr"
    provider: "Yahoo"
    processing_priority: "high"
    auto_responses: "disabled"
    
Account_Synchronization:
  cross_account_deduplication: "Prevent duplicate processing"
  unified_reporting: "Single report covering all accounts"
  centralized_task_management: "Tasks from all accounts in one queue"
  global_contact_management: "Shared client database across accounts"
```

## 安全与隐私功能

### 数据保护
- **电子邮件加密**：支持加密电子邮件通信
- **安全附件处理**：病毒扫描和安全存储
- **访问控制**：基于角色的电子邮件处理功能访问权限
- **审计日志**：完整的电子邮件处理活动记录
- **GDPR 合规性**：符合欧洲隐私法规

### 希腊商务隐私
- **客户保密**：安全处理客户通信
- **银行安全**：特别保护银行对账单的处理
- **政府通信安全**：安全处理官方通信
- **文档保留**：遵守希腊法律关于电子邮件保留的规定
- **专业保密**：尊重会计师与客户之间的保密协议

## 性能优化

### 高效处理
```yaml
Performance_Settings:
  email_scanning:
    interval: "5 minutes for critical accounts"
    batch_size: "50 emails per batch"
    concurrent_processing: "3 accounts simultaneously"
    
  attachment_processing:
    size_limits: "50MB per attachment"
    format_support: ["pdf", "doc", "docx", "xls", "xlsx", "csv", "xml"]
    ocr_enabled: "For scanned documents"
    
  response_times:
    urgent_emails: "<30 seconds"
    government_emails: "<1 minute" 
    routine_processing: "<5 minutes"
    
  caching:
    sender_recognition: "Cache known senders for faster processing"
    template_responses: "Pre-compiled response templates"
    document_patterns: "Cache document recognition patterns"
```

## 集成点

### OpenClaw 功能集成
```bash
# Integration with other Greek accounting skills
openclaw email process --forward-to greek-compliance-aade
openclaw email process --forward-to accounting-workflows
openclaw email process --forward-to cli-deadline-monitor

# Integration with document processing
openclaw email extract-attachments --process-with deepread-skill
openclaw email invoices --process-with greek-vat-calculator

# Integration with client management
openclaw email client-communications --update-client-records
openclaw email payments --update-accounting-ledger

# Update client records with email-derived data (requires client-data-management skill)
openclaw email client-communications --update-client-records
```

### 内部功能集成
```yaml
Companion_Skills:
  accounting-workflows: "Route extracted documents to processing pipeline"
  greek-document-ocr: "Send attachments for OCR processing"
  client-data-management: "Update client records from email content"
  greek-compliance-aade: "Forward AADE notifications for compliance tracking"
  greek-banking-integration: "Match email payment notifications with bank transactions"
```

> **注意**：该功能不与外部软件集成。它直接处理电子邮件，并将提取的数据通过本地文件系统路由到 OpenClaw 的其他相关功能。

## 使用示例

### 示例 1：发票处理
```bash
$ openclaw email process --filter "invoices" --account "accounting@company.gr"

📧 EMAIL PROCESSING RESULTS:

New Invoices Processed (3):
✅ SUPPLIER A AE - Invoice #2026-0156 - ‚¬1,250.00
   ├─ Status: VAT validated (24%)
   ├─ Due Date: March 15, 2026 (26 days)  
   ├─ Action: Forwarded to accounting system
   └─ Response: Greek confirmation sent to supplier

✅ ΠΡΡθΜΗΜΕΥΤΗΣ B ΕΠΕ - Τιμολςγιο #456 - ‚¬850.00
   ├─ Status: Greek invoice format recognized
   ├─ VAT Rate: 13% (services)
   ├─ Action: Added to payment queue
   └─ Response: "Επιβεβαίπ°ση παραλαβήπš" sent

⚠ï¸ VENDOR C - Invoice unclear format - ‚¬2,100.00
   ├─ Status: Manual review required
   ├─ Issue: VAT calculation uncertain
   ├─ Action: Flagged for accountant review
   └─ Response: Acknowledgment sent, review requested

Summary: 3 invoices processed, 2 automated, 1 manual review needed
```

### 示例 2：AADE 通知处理
```bash
$ openclaw email process --filter "government" --priority critical

ðŸÂ€ºï¸ GOVERNMENT EMAIL PROCESSING:

AADE Notification Processed (1):
🚨 CRITICAL: VAT Deadline Change Detected
   ├─ From: notifications@aade.gr
   ├─ Subject: "Αλλαγή προθεσμίαπš υποβολήπš δήλπ°σηπš ΦΠΑ"
   ├─ Change: March VAT deadline moved from 25th to 20th
   ├─ Impact: 5 days earlier than expected
   ├─ Actions Taken:
   ─š   ├─ Updated compliance deadline tracker ✅
   ─š   ├─ Notified affected clients ✅
   ─š   ├─ Rescheduled VAT preparation tasks ✅
   ─š   └─ Created urgent alert for accounting team ✅

EFKA System Notice (1):
„¹ï¸ Planned Maintenance Notification
   ├─ From: support@efka.gov.gr
   ├─ Maintenance Window: Feb 19, 02:00-06:00 EET
   ├─ Impact: Social security submissions unavailable
   ├─ Action: Rescheduled morning submissions to afternoon

Summary: Critical compliance changes processed and implemented
```

### 示例 3：客户通信自动化
```bash
$ openclaw email process --filter "client-communications" --auto-respond

👥 CLIENT COMMUNICATION PROCESSING:

Payment Status Inquiries (2):
📀¹ ΠΕ΀ºΑΤΗΣ A ΑΕ - Payment Status Request
   ├─ Query: "Πςπžε θα πληρπ°θεί πžο πžιμολςγις μαπš #789?"
   ├─ Status Check: Invoice paid Feb 15, 2026
   ├─ Response: Greek status update with payment confirmation
   └─ Attachment: Payment receipt included

📀¹ CLIENT B LTD - Overdue Payment Inquiry  
   ├─ Query: "Why is payment delayed for invoice #456?"
   ├─ Status Check: Payment scheduled for Feb 20, 2026
   ├─ Response: Explanation of payment schedule + apology
   └─ Follow-up: Added to priority payment list

Document Requests (1):
📀ž ΕΤΑΙΡΕΙΑ Γ ΕΠΕ - Additional Documentation  
   ├─ Request: "Χρειαζςμασπžε ανπžίγραπ ο π ορολογικήπš ενημερςπžηπžαπš"
   ├─ Document: Tax compliance certificate generated
   ├─ Response: Certificate attached with Greek cover letter
   └─ Archive: Request logged in client file

Summary: 3 client communications processed, all with automated responses
```

## OpenClaw 集成策略

### 实用的 OpenClaw 电子邮件处理流程
```bash
# File-based email processing — drop exported email files into incoming
openclaw email monitor-folder /data/incoming/ --greek-language
openclaw email process-attachments --extract-invoices --auto-classify
openclaw email generate-responses --templates-greek --auto-send false

# Email integration through file system
openclaw email scan-exports --source imap-archive --process-new
openclaw email parse-greek-documents --invoices --government --banking
```

### 基于文件的电子邮件工作流程（兼容 OpenClaw）
```yaml
Email_Processing_Workflow:
  # Step 1: Email Export (External to OpenClaw)
  email_export:
    method: "User exports emails/attachments to /data/incoming/"
    formats: [".eml", ".mbox", ".pst", ".msg", ".pdf", ".xlsx"]
    subfolders:
      invoices: "/data/incoming/invoices/"
      government: "/data/incoming/government/"
      statements: "/data/incoming/statements/"
      other: "/data/incoming/other/"
    
  # Step 2: OpenClaw Processing
  openclaw_processing:
    scan: "openclaw email scan-folder /data/incoming/"
    extract: "openclaw email extract-attachments --greek-docs"
    classify: "openclaw email classify-documents --business-types"
    
  # Step 3: Response Generation
  response_generation:
    templates: "openclaw email prepare-responses --greek-templates"
    review: "openclaw email review-drafts --manual-approval"
    output: "/data/processing/email-drafts/{YYYY-MM-DD}/{response-type}.txt"
```

### 适用于 OpenClaw 的电子邮件命令
```bash
# Document processing from incoming folder (after email export)
openclaw email extract-invoices --input-dir /data/incoming/invoices/
openclaw email process-statements --input-dir /data/incoming/statements/ --bank-format greek --auto-reconcile
openclaw email handle-government --input-dir /data/incoming/government/ --aade-notifications --priority urgent

# Greek language specific processing
openclaw email greek-classify --document-types --confidence-threshold 0.8
openclaw email greek-respond --template-library /data/system/templates/greek/
openclaw email greek-forward --accounting-system --include-metadata
```

### 与其他功能的集成
```bash
# Chain with other OpenClaw skills
openclaw email process-batch | openclaw accounting validate-invoices
openclaw email extract-data | openclaw greek-compliance calculate-vat
openclaw email government-alerts | openclaw deadline update-deadlines
```

一个成功的希腊语电子邮件处理系统应具备以下特点：
- ✅ 希腊语文档分类准确率超过 95%
- ✅ 紧急政府邮件的响应时间小于 30 秒
- ✅ 常规客户通信的自动化处理率超过 90%
- ✅ 无重要合规通知遗漏
- ✅ 所有电子邮件处理过程都有完整的审计记录
- ✅ 与所有主要的希腊语电子邮件提供商集成
- ✅ 所有通信均支持原生希腊语

请注意：该功能作为希腊语会计自动化的核心，确保不会遗漏任何重要的财务文件或政府通知，同时保持专业的希腊商务沟通标准。