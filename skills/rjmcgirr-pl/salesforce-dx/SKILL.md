---
name: salesforce-dx
description: 使用 `sf` CLI 查询 Salesforce 数据并管理销售流程。该工具可用于执行各种操作，包括 SOQL 查询（从简单到复杂）、销售机会流程分析、预测报告生成、数据导出、数据库模式探索以及 CRM 数据操作。此外，它还适用于执行高管级的工作流程，例如按名称查找交易记录、获取联系人的电子邮件信息以联系潜在客户、准备销售流程评估报告，以及将 CRM 数据与其他工具进行交叉引用。`sf` CLI 可触发与 Salesforce、SOQL、销售流程、销售机会、预测数据、CRM 数据、交易查找、潜在客户信息或相关问题相关的操作。
---

# Salesforce DX — 数据与工作流

使用 `sf` CLI 查询数据并管理工作流。

## 先决条件

```bash
# Verify CLI and auth
sf --version
sf org list
```

如果没有列出任何组织，请进行身份验证：
```bash
sf org login web --alias my-org --set-default
```

## 架构探索

在查询之前，先了解可用的对象和字段：

```bash
# List all objects
sf sobject list --target-org my-org

# Describe object fields
sf sobject describe --sobject Opportunity --target-org my-org

# Quick field list (names only)
sf sobject describe --sobject Opportunity --target-org my-org | grep -E "^name:|^type:" 
```

## SOQL 查询

### 基本模式

```bash
# Simple query
sf data query -q "SELECT Id, Name, Amount FROM Opportunity LIMIT 10"

# With WHERE clause
sf data query -q "SELECT Id, Name FROM Opportunity WHERE StageName = 'Closed Won'"

# Date filtering
sf data query -q "SELECT Id, Name FROM Opportunity WHERE CloseDate = THIS_QUARTER"

# Export to CSV
sf data query -q "SELECT Id, Name, Amount FROM Opportunity" --result-format csv > opps.csv
```

### 关系

```bash
# Parent lookup (Account from Opportunity)
sf data query -q "SELECT Id, Name, Account.Name, Account.Industry FROM Opportunity"

# Child subquery (Opportunities from Account)
sf data query -q "SELECT Id, Name, (SELECT Id, Name, Amount FROM Opportunities) FROM Account LIMIT 5"
```

### 聚合操作

```bash
# COUNT
sf data query -q "SELECT COUNT(Id) total FROM Opportunity WHERE IsClosed = false"

# SUM and GROUP BY
sf data query -q "SELECT StageName, SUM(Amount) total FROM Opportunity GROUP BY StageName"

# Multiple aggregates
sf data query -q "SELECT StageName, COUNT(Id) cnt, SUM(Amount) total, AVG(Amount) avg FROM Opportunity GROUP BY StageName"
```

### 批量查询（大数据集）

```bash
# Use --bulk for >2000 records
sf data query -q "SELECT Id, Name, Amount FROM Opportunity" --bulk --wait 10
```

## 工作流管理

### 工作流快照

```bash
# Open pipeline by stage
sf data query -q "SELECT StageName, COUNT(Id) cnt, SUM(Amount) total FROM Opportunity WHERE IsClosed = false GROUP BY StageName ORDER BY StageName"

# Pipeline by owner
sf data query -q "SELECT Owner.Name, SUM(Amount) total FROM Opportunity WHERE IsClosed = false GROUP BY Owner.Name ORDER BY SUM(Amount) DESC"

# Pipeline by close month
sf data query -q "SELECT CALENDAR_MONTH(CloseDate) month, SUM(Amount) total FROM Opportunity WHERE IsClosed = false AND CloseDate = THIS_YEAR GROUP BY CALENDAR_MONTH(CloseDate) ORDER BY CALENDAR_MONTH(CloseDate)"
```

### 成败分析

```bash
# Win rate by stage
sf data query -q "SELECT StageName, COUNT(Id) FROM Opportunity WHERE IsClosed = true GROUP BY StageName"

# Closed won this quarter
sf data query -q "SELECT Id, Name, Amount, CloseDate FROM Opportunity WHERE StageName = 'Closed Won' AND CloseDate = THIS_QUARTER ORDER BY Amount DESC"

# Lost deals with reasons
sf data query -q "SELECT Id, Name, Amount, StageName, Loss_Reason__c FROM Opportunity WHERE StageName = 'Closed Lost' AND CloseDate = THIS_QUARTER"
```

### 预测查询

```bash
# Weighted pipeline (assumes Probability field)
sf data query -q "SELECT StageName, SUM(Amount) gross, SUM(ExpectedRevenue) weighted FROM Opportunity WHERE IsClosed = false GROUP BY StageName"

# Deals closing this month
sf data query -q "SELECT Id, Name, Amount, StageName, CloseDate FROM Opportunity WHERE CloseDate = THIS_MONTH AND IsClosed = false ORDER BY Amount DESC"

# Stale deals (no activity in 30 days)
sf data query -q "SELECT Id, Name, Amount, LastActivityDate FROM Opportunity WHERE IsClosed = false AND LastActivityDate < LAST_N_DAYS:30"
```

## 数据操作

### 创建记录

```bash
sf data create record -s Opportunity -v "Name='New Deal' StageName='Prospecting' CloseDate=2024-12-31 Amount=50000"
```

### 更新记录

```bash
# By ID
sf data update record -s Opportunity -i 006xx000001234 -v "StageName='Negotiation'"

# Bulk update via CSV
sf data upsert bulk -s Opportunity -f updates.csv -i Id --wait 10
```

### 导出/导入

```bash
# Export with relationships
sf data export tree -q "SELECT Id, Name, (SELECT Id, Subject FROM Tasks) FROM Account WHERE Industry = 'Technology'" -d ./export

# Import
sf data import tree -f ./export/Account.json
```

## 用于脚本编写的 JSON 输出

添加 `--json` 选项以获得结构化输出：

```bash
sf data query -q "SELECT Id, Name, Amount FROM Opportunity WHERE IsClosed = false" --json
```

使用 `jq` 进行解析：
```bash
sf data query -q "SELECT Id, Name FROM Opportunity LIMIT 5" --json | jq '.result.records[].Name'
```

## 常见日期字面量

| 字面量 | 含义 |
|---------|---------|
| TODAY   | 当前日期 |
| THIS_WEEK | 当前周   |
| THIS_MONTH | 当前月份 |
| THIS_QUARTER | 当前季度 |
| THIS_YEAR | 当前年份 |
| LAST_N_days:n | 过去 n 天 |
| NEXT_N_days:n | 下 n 天 |
| LAST_QUARTER | 上一个季度 |

## 故障排除

**“查询格式错误”** — 请检查字段的 API 名称（而非标签名）。使用 `sf sobject describe` 进行验证。

**“QUERY_TIMEOUT”** — 添加过滤器，使用 `--bulk` 选项，或设置 `LIMIT`。

**“无效字段”** — 该字段可能不存在于该对象中，或者您的权限不足。

**大量结果集** — 对于返回超过 2000 条记录的查询，请使用 `--bulk` 选项。

## 高管工作流

### 快速查找交易

通过名称或账户查找交易：
```bash
# By opportunity name (fuzzy)
sf data query -q "SELECT Id, Name, Amount, StageName, CloseDate, Owner.Name, Account.Name FROM Opportunity WHERE Name LIKE '%Acme%' ORDER BY Amount DESC"

# By account name
sf data query -q "SELECT Id, Name, Amount, StageName, CloseDate FROM Opportunity WHERE Account.Name LIKE '%Microsoft%' AND IsClosed = false"

# Recent deals I own
sf data query -q "SELECT Id, Name, Amount, StageName, CloseDate, Account.Name FROM Opportunity WHERE OwnerId = '<my-user-id>' AND IsClosed = false ORDER BY CloseDate"
```

### 获取联系人信息以进行外联

查找需要发送邮件的联系人：
```bash
# Contacts at an account
sf data query -q "SELECT Id, Name, Email, Phone, Title FROM Contact WHERE Account.Name LIKE '%Acme%'"

# Decision makers (by title)
sf data query -q "SELECT Name, Email, Title, Account.Name FROM Contact WHERE Title LIKE '%CEO%' OR Title LIKE '%VP%' OR Title LIKE '%Director%'"

# Contacts on a specific deal
sf data query -q "SELECT Contact.Name, Contact.Email, Contact.Title, Role FROM OpportunityContactRole WHERE Opportunity.Name LIKE '%Acme%'"
```

### 为工作流审查做准备

获取快速的高管总结：
```bash
# Top 10 deals closing this quarter
sf data query -q "SELECT Name, Account.Name, Amount, StageName, CloseDate, Owner.Name FROM Opportunity WHERE CloseDate = THIS_QUARTER AND IsClosed = false ORDER BY Amount DESC LIMIT 10"

# Deals by rep (for 1:1s)
sf data query -q "SELECT Owner.Name, COUNT(Id) deals, SUM(Amount) total FROM Opportunity WHERE IsClosed = false GROUP BY Owner.Name ORDER BY SUM(Amount) DESC"

# Deals needing attention (stale)
sf data query -q "SELECT Name, Amount, StageName, LastActivityDate, Owner.Name FROM Opportunity WHERE IsClosed = false AND LastActivityDate < LAST_N_DAYS:14 ORDER BY Amount DESC LIMIT 10"
```

### 客户信息分析

在通话或会议前：
```bash
# Account overview
sf data query -q "SELECT Id, Name, Industry, BillingCity, Website, OwnerId FROM Account WHERE Name LIKE '%Acme%'"

# All open deals with account
sf data query -q "SELECT Name, Amount, StageName, CloseDate FROM Opportunity WHERE Account.Name LIKE '%Acme%' AND IsClosed = false"

# Recent activities
sf data query -q "SELECT Subject, Status, ActivityDate FROM Task WHERE Account.Name LIKE '%Acme%' ORDER BY ActivityDate DESC LIMIT 5"
```

### 跨工具工作流

**Salesforce + 电子邮件（通过 gog/gmail）：**
1. 查找联系人邮箱：`sf data query -q "SELECT Email FROM Contact WHERE Account.Name LIKE '%Acme%'"`
2. 使用该邮箱地址通过您的邮件工具发送邮件

**Salesforce + 日历：**
1. 查找即将成交的交易：`sf data query -q "SELECT Name, Account.Name, CloseDate FROM Opportunity WHERE CloseDate = THIS_WEEK"`
2. 与日历进行交叉核对，确保安排了跟进任务

**通话后的快速 CRM 更新：**
```bash
# Log a task
sf data create record -s Task -v "Subject='Call with John' WhatId='<opportunity-id>' Status='Completed' ActivityDate=$(date +%Y-%m-%d)"

# Update opportunity stage
sf data update record -s Opportunity -i <opp-id> -v "StageName='Negotiation' NextStep='Send proposal'"
```

### 查找用户 ID

用于执行“我负责的交易”相关查询：
```bash
sf data query -q "SELECT Id, Name FROM User WHERE Email = 'your.email@company.com'"
```

请将此信息保存在本地配置文件中以供快速参考。

## 参考资料

- **[soql-patterns.md](references/soql-patterns.md)** — 高级 SOQL 模式（多态性、半连接、公式字段）
- **[pipeline-queries.md](references/pipeline-queries.md)** — 可直接使用的管道和预测查询模板