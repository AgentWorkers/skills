**主要技能说明（含前置内容、命令行界面（CLI）参考及SOQL模式）**

---

```yaml
---
name: salesforce
description: Manage Salesforce CRM - query records, create/update contacts, accounts, opportunities, leads, and cases. Use when the user asks about CRM data, sales pipeline, customer records, or Salesforce operations.
metadata: {"moltbot":{"emoji":"☁️","requires":{"bins":["sf"],"env":["SALESFORCE_ACCESS_TOKEN"]},"primaryEnv":"SALESFORCE_ACCESS_TOKEN","install":[{"id":"npm","kind":"node","package":"@salesforce/cli","bins":["sf"],"label":"Install Salesforce CLI (npm)"},{"id":"brew","kind":"brew","formula":"salesforce-cli","bins":["sf"],"label":"Install Salesforce CLI (brew)"}]}}
homepage: https://developer.salesforce.com/tools/salesforcecli
---
```

# Salesforce CRM 技能

使用官方的 Salesforce CLI (`sf`) 和 REST API 与 Salesforce CRM 进行交互。

## 先决条件

1. 通过 npm 或 Homebrew 安装了 Salesforce CLI (`sf`)。
2. 配置了身份验证方式：
    - `sf org login web`（OAuth 浏览器登录方式 - 推荐用于交互式操作）
    - `sf org login jwt`（JWT 登录方式 - 适用于无界面/自动化操作）
    - 设置 `SALESFORCE_ACCESS_TOKEN` 环境变量（直接使用访问令牌）

## 快速参考

### 身份验证与组织管理

```bash
# Login to org (opens browser)
sf org login web --alias myorg

# Login with JWT (headless)
sf org login jwt --client-id <consumer-key> --jwt-key-file <path-to-key> --username <user> --alias myorg

# List connected orgs
sf org list

# Set default org
sf config set target-org myorg

# Display org info
sf org display --target-org myorg
```

### 查询记录（SOQL）

```bash
# Query contacts
sf data query --query "SELECT Id, Name, Email, Phone FROM Contact LIMIT 10" --target-org myorg

# Query with WHERE clause
sf data query --query "SELECT Id, Name, Amount, StageName FROM Opportunity WHERE StageName = 'Prospecting'" --target-org myorg

# Query accounts by name
sf data query --query "SELECT Id, Name, Industry, Website FROM Account WHERE Name LIKE '%Acme%'" --target-org myorg

# Export to CSV
sf data query --query "SELECT Id, Name, Email FROM Contact" --result-format csv > contacts.csv

# Export to JSON
sf data query --query "SELECT Id, Name FROM Account" --result-format json
```

### 创建记录

```bash
# Create a Contact
sf data create record --sobject Contact --values "FirstName='John' LastName='Doe' Email='john.doe@example.com'" --target-org myorg

# Create an Account
sf data create record --sobject Account --values "Name='Acme Corp' Industry='Technology' Website='https://acme.com'" --target-org myorg

# Create an Opportunity
sf data create record --sobject Opportunity --values "Name='Big Deal' AccountId='001XXXXXXXXXXXXXXX' StageName='Prospecting' CloseDate='2025-06-30' Amount=50000" --target-org myorg

# Create a Lead
sf data create record --sobject Lead --values "FirstName='Jane' LastName='Smith' Company='NewCo' Email='jane@newco.com' Status='Open - Not Contacted'" --target-org myorg

# Create a Case
sf data create record --sobject Case --values "Subject='Support Request' Description='Customer needs help' Status='New' Priority='Medium'" --target-org myorg
```

### 更新记录

```bash
# Update a Contact
sf data update record --sobject Contact --record-id 003XXXXXXXXXXXXXXX --values "Phone='555-1234' Title='VP Sales'" --target-org myorg

# Update an Opportunity stage
sf data update record --sobject Opportunity --record-id 006XXXXXXXXXXXXXXX --values "StageName='Negotiation/Review' Amount=75000" --target-org myorg

# Update Account
sf data update record --sobject Account --record-id 001XXXXXXXXXXXXXXX --values "Description='Key strategic account'" --target-org myorg
```

### 删除记录

```bash
# Delete a record
sf data delete record --sobject Contact --record-id 003XXXXXXXXXXXXXXX --target-org myorg

# Bulk delete via query (careful!)
sf data delete bulk --sobject Lead --file leads-to-delete.csv --target-org myorg
```

### 批量操作

```bash
# Bulk insert from CSV
sf data import bulk --sobject Contact --file contacts.csv --target-org myorg

# Bulk update from CSV
sf data upsert bulk --sobject Account --file accounts.csv --external-id Id --target-org myorg

# Check bulk job status
sf data bulk status --job-id <job-id> --target-org myorg
```

### 数据库模式与元数据

```bash
# Describe an object (get fields)
sf sobject describe --sobject Account --target-org myorg

# List all objects
sf sobject list --target-org myorg

# Get field details
sf sobject describe --sobject Opportunity --target-org myorg | jq '.fields[] | {name, type, label}'
```

## 常用 SOQL 模式

### 管道报告（Pipeline Report）

```sql
SELECT StageName, COUNT(Id) NumDeals, SUM(Amount) TotalValue
FROM Opportunity
WHERE IsClosed = false
GROUP BY StageName
```

### 最近活动（Recent Activities）

```sql
SELECT Id, Subject, WhoId, WhatId, ActivityDate
FROM Task
WHERE OwnerId = '<user-id>'
AND ActivityDate >= LAST_N_DAYS:7
ORDER BY ActivityDate DESC
```

### 按账户划分的联系人（Contacts by Account）

```sql
SELECT Account.Name, Id, Name, Email, Title
FROM Contact
WHERE Account.Name = 'Acme Corp'
```

### 开启的案例（Open Cases）

```sql
SELECT Id, CaseNumber, Subject, Status, Priority, CreatedDate
FROM Case
WHERE IsClosed = false
ORDER BY Priority, CreatedDate
```

### 按状态划分的潜在客户（Leads by Status）

```sql
SELECT Status, COUNT(Id) Total
FROM Lead
WHERE IsConverted = false
GROUP BY Status
```

## REST API（备用方案）

对于 CLI 未支持的操作，可以使用 curl 和 REST API 来执行：

```bash
# Set variables
INSTANCE_URL="https://yourorg.salesforce.com"
ACCESS_TOKEN="$SALESFORCE_ACCESS_TOKEN"

# Query via REST
curl -s "$INSTANCE_URL/services/data/v59.0/query?q=SELECT+Id,Name+FROM+Account+LIMIT+5" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json"

# Create record via REST
curl -s "$INSTANCE_URL/services/data/v59.0/sobjects/Contact" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"FirstName":"Test","LastName":"User","Email":"test@example.com"}'
```

## 错误处理

- **INVALID_SESSION_ID**：令牌已过期。请使用 `sf org login web` 重新登录。
- **MALFORMED_QUERY**：SOQL 语法错误。字符串需要使用单引号括起来。
- **ENTITY_IS_DELETED**：记录已被删除。在更新前请先进行查询确认。
- **REQUIRED_FIELD MISSING**：检查对象模式中是否缺少必填字段。

## 提示

1. **使用别名**：登录时设置 `--alias` 参数，之后使用 `--target-org alias` 来指定目标组织。
2. **JSON 输出**：使用 `--json` 参数以获取 JSON 格式的输出结果，便于程序解析。
3. **模拟执行**：对批量操作使用 `--dry-run` 参数进行预览。
4. **字段名称**：使用 API 定义的字段名称（例如 `FirstName`），而非显示名称（例如 “First Name”）。
5. **日期格式**：日期使用 `YYYY-MM-DD`，日期时间使用 `YYYY-MM-DDThh:mm:ssZ`。

## 限制

- 批量操作有每日 API 使用量限制（具体限制因 Salesforce 版本而异）。
- 某些对象（如 ContentDocument）有特殊的处理要求。
- 复杂查询可能会超出 API 的性能限制。