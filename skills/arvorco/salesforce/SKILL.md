---
name: salesforce
description: "通过 Salesforce CLI (`sf`) 查询和管理 Salesforce CRM 数据。可以执行 SOQL/SOSL 查询、查看对象结构、创建/更新/删除记录、批量导入/导出数据、运行 Apex 代码、部署元数据以及发起原始的 REST API 调用。"
homepage: https://developer.salesforce.com/tools/salesforcecli
metadata: {"clawdbot":{"emoji":"☁️","requires":{"bins":["sf"]},"install":[{"id":"npm","kind":"node","package":"@salesforce/cli","bins":["sf"],"label":"Install Salesforce CLI (npm)"}]}}
---

# Salesforce 技能

使用 Salesforce CLI（`sf`）与 Salesforce 组织进行交互。在使用 CLI 之前，必须先进行身份验证。始终添加 `--json` 选项以获得结构化的输出。

如果 `sf` 可执行文件不可用，可以通过 npm（`npm install -g @salesforce/cli`）进行安装，或从 https://developer.salesforce.com/tools/salesforcecli 下载。安装完成后，立即使用 `sf org login web` 进行身份验证，以连接到 Salesforce 组织。

## 身份验证和组织管理

### 登录（打开浏览器）
```bash
sf org login web --alias my-org
```

其他登录方法：
```bash
# JWT-based login (CI/automation)
sf org login jwt --client-id <consumer-key> --jwt-key-file server.key --username user@example.com --alias my-org

# Login with an existing access token
sf org login access-token --instance-url https://mycompany.my.salesforce.com

# Login via SFDX auth URL (from a file)
sf org login sfdx-url --sfdx-url-file authUrl.txt --alias my-org
```

### 管理组织
```bash
# List all authenticated orgs
sf org list --json

# Display info about the default org (access token, instance URL, username)
sf org display --json

# Display info about a specific org
sf org display --target-org my-org --json

# Display with SFDX auth URL (sensitive - contains refresh token)
sf org display --target-org my-org --verbose --json

# Open org in browser
sf org open
sf org open --target-org my-org

# Log out
sf org logout --target-org my-org
```

### 配置和别名
```bash
# Set default target org
sf config set target-org my-org

# List all config variables
sf config list

# Get a specific config value
sf config get target-org

# Set an alias
sf alias set prod=user@example.com

# List aliases
sf alias list
```

## 数据查询（SOQL）

通过默认 API 进行标准 SOQL 查询：
```bash
# Basic query
sf data query --query "SELECT Id, Name, Email FROM Contact LIMIT 10" --json

# WHERE clause
sf data query --query "SELECT Id, Name, Amount, StageName FROM Opportunity WHERE StageName = 'Closed Won'" --json

# Relationship queries (parent-to-child)
sf data query --query "SELECT Id, Name, (SELECT LastName, Email FROM Contacts) FROM Account LIMIT 5" --json

# Relationship queries (child-to-parent)
sf data query --query "SELECT Id, Name, Account.Name FROM Contact" --json

# LIKE for text search
sf data query --query "SELECT Id, Name FROM Account WHERE Name LIKE '%Acme%'" --json

# Date filtering
sf data query --query "SELECT Id, Name, CreatedDate FROM Lead WHERE CreatedDate = TODAY" --json

# ORDER BY + LIMIT
sf data query --query "SELECT Id, Name, Amount FROM Opportunity ORDER BY Amount DESC LIMIT 20" --json

# Include deleted/archived records
sf data query --query "SELECT Id, Name FROM Account" --all-rows --json

# Query from a file
sf data query --file query.soql --json

# Tooling API queries (metadata objects like ApexClass, ApexTrigger)
sf data query --query "SELECT Id, Name, Status FROM ApexClass" --use-tooling-api --json

# Output to CSV file
sf data query --query "SELECT Id, Name, Email FROM Contact" --result-format csv --output-file contacts.csv

# Target a specific org
sf data query --query "SELECT Id, Name FROM Account" --target-org my-org --json
```

对于返回超过 10,000 条记录的查询，请使用批量 API（Bulk API）：
```bash
sf data export bulk --query "SELECT Id, Name, Email FROM Contact" --output-file contacts.csv --result-format csv --wait 10
sf data export bulk --query "SELECT Id, Name FROM Account" --output-file accounts.json --result-format json --wait 10
```

## 文本搜索（SOSL）

SOSL 可同时搜索多个对象：
```bash
# Search for text across objects
sf data search --query "FIND {John Smith} IN ALL FIELDS RETURNING Contact(Name, Email), Lead(Name, Email)" --json

# Search in name fields only
sf data search --query "FIND {Acme} IN NAME FIELDS RETURNING Account(Name, Industry), Contact(Name)" --json

# Search from a file
sf data search --file search.sosl --json

# Output to CSV
sf data search --query "FIND {test} RETURNING Contact(Name)" --result-format csv
```

## 单条记录操作

### 获取记录
```bash
# By record ID
sf data get record --sobject Contact --record-id 003XXXXXXXXXXXX --json

# By field match (WHERE-like)
sf data get record --sobject Account --where "Name=Acme" --json

# By multiple fields (values with spaces need single quotes)
sf data get record --sobject Account --where "Name='Universal Containers' Phone='(123) 456-7890'" --json
```

### 创建记录（先获得用户确认）
```bash
sf data create record --sobject Contact --values "FirstName='Jane' LastName='Doe' Email='jane@example.com'" --json

sf data create record --sobject Account --values "Name='New Company' Website=www.example.com Industry='Technology'" --json

# Tooling API object
sf data create record --sobject TraceFlag --use-tooling-api --values "DebugLevelId=7dl... LogType=CLASS_TRACING" --json
```

### 更新记录（先获得用户确认）
```bash
# By ID
sf data update record --sobject Contact --record-id 003XXXXXXXXXXXX --values "Email='updated@example.com'" --json

# By field match
sf data update record --sobject Account --where "Name='Old Acme'" --values "Name='New Acme'" --json

# Multiple fields
sf data update record --sobject Account --record-id 001XXXXXXXXXXXX --values "Name='Acme III' Website=www.example.com" --json
```

### 删除记录（需要用户明确确认）
```bash
# By ID
sf data delete record --sobject Account --record-id 001XXXXXXXXXXXX --json

# By field match
sf data delete record --sobject Account --where "Name=Acme" --json
```

## 批量数据操作（Bulk API 2.0）

对于大量数据集（数千到数百万条记录）：

### 批量导出
```bash
# Export to CSV
sf data export bulk --query "SELECT Id, Name, Email FROM Contact" --output-file contacts.csv --result-format csv --wait 10

# Export to JSON
sf data export bulk --query "SELECT Id, Name FROM Account" --output-file accounts.json --result-format json --wait 10

# Include soft-deleted records
sf data export bulk --query "SELECT Id, Name FROM Account" --output-file accounts.csv --result-format csv --all-rows --wait 10

# Resume a timed-out export
sf data export resume --job-id 750XXXXXXXXXXXX --json
```

### 批量导入
```bash
# Import from CSV
sf data import bulk --file accounts.csv --sobject Account --wait 10

# Resume a timed-out import
sf data import resume --job-id 750XXXXXXXXXXXX --json
```

### 批量插入/更新（Bulk Upsert）
```bash
sf data upsert bulk --file contacts.csv --sobject Contact --external-id Email --wait 10
```

### 批量删除
```bash
# Delete records listed in CSV (CSV must have an Id column)
sf data delete bulk --file records-to-delete.csv --sobject Contact --wait 10
```

### 树状数据导出/导入（针对关联记录）
```bash
# Export with relationships into JSON tree format
sf data export tree --query "SELECT Id, Name, (SELECT Name, Email FROM Contacts) FROM Account" --json

# Export with a plan file (for multiple objects)
sf data export tree --query "SELECT Id, Name FROM Account" --plan --output-dir export-data

# Import from tree JSON files
sf data import tree --files Account.json,Contact.json

# Import using a plan definition file
sf data import tree --plan Account-Contact-plan.json
```

## 模式检查
```bash
# Describe an object (fields, relationships, picklist values)
sf sobject describe --sobject Account --json

# Describe a custom object
sf sobject describe --sobject MyCustomObject__c --json

# Describe a Tooling API object
sf sobject describe --sobject ApexClass --use-tooling-api --json

# List all objects
sf sobject list --json

# List only custom objects
sf sobject list --sobject custom --json

# List only standard objects
sf sobject list --sobject standard --json
```

## 执行 Apex 代码
```bash
# Execute Apex from a file
sf apex run --file script.apex --json

# Run interactively (type code, press Ctrl+D to execute)
sf apex run

# Run Apex tests
sf apex run test --test-names MyTestClass --json

# Get test results
sf apex get test --test-run-id 707XXXXXXXXXXXX --json

# View Apex logs
sf apex list log --json
sf apex get log --log-id 07LXXXXXXXXXXXX
```

## REST API（高级用法）

执行任意经过身份验证的 REST API 调用：
```bash
# GET request
sf api request rest 'services/data/v62.0/limits' --json

# List API versions
sf api request rest '/services/data/' --json

# Create a record via REST
sf api request rest '/services/data/v62.0/sobjects/Account' --method POST --body '{"Name":"REST Account","Industry":"Technology"}' --json

# Update a record via REST (PATCH)
sf api request rest '/services/data/v62.0/sobjects/Account/001XXXXXXXXXXXX' --method PATCH --body '{"BillingCity":"San Francisco"}' --json

# GraphQL query
sf api request graphql --body '{"query":"{ uiapi { query { Account { edges { node { Name { value } } } } } } }"}' --json

# Custom headers
sf api request rest '/services/data/v62.0/limits' --header 'Accept: application/xml'

# Save response to file
sf api request rest '/services/data/v62.0/limits' --stream-to-file limits.json
```

## 元数据部署与检索
```bash
# Deploy metadata to an org
sf project deploy start --source-dir force-app --json

# Deploy specific metadata components
sf project deploy start --metadata ApexClass:MyClass --json

# Retrieve metadata from an org
sf project retrieve start --metadata ApexClass --json

# Check deploy status
sf project deploy report --job-id 0AfXXXXXXXXXXXX --json

# Generate a new Salesforce DX project
sf project generate --name my-project

# List metadata components in the org
sf project list ignored --json
```

## 日志诊断
```bash
# Run CLI diagnostics
sf doctor

# Check CLI version
sf version

# See what is new
sf whatsnew
```

## 常见 SOQL 模式
```sql
-- Count records
SELECT COUNT() FROM Contact WHERE AccountId = '001XXXXXXXXXXXX'

-- Aggregate query
SELECT StageName, COUNT(Id), SUM(Amount) FROM Opportunity GROUP BY StageName

-- Date literals
SELECT Id, Name FROM Lead WHERE CreatedDate = LAST_N_DAYS:30

-- Subquery (semi-join)
SELECT Id, Name FROM Account WHERE Id IN (SELECT AccountId FROM Contact WHERE Email LIKE '%@acme.com')

-- Polymorphic lookup
SELECT Id, Who.Name, Who.Type FROM Task WHERE Who.Type = 'Contact'

-- Multiple WHERE conditions
SELECT Id, Name, Amount FROM Opportunity WHERE Amount > 10000 AND StageName != 'Closed Lost' AND CloseDate = THIS_QUARTER
```

## 安全规范

- **始终使用 `--json` 选项** 以获得结构化、可解析的输出。
- **未经用户明确确认，切勿创建、更新或删除记录**。在执行操作前，请先说明操作内容并征求用户同意。
- **除非用户明确请求并确认具体记录，否则切勿删除记录**。
- **在用户未审核文件/查询内容并确认之前，切勿执行批量删除或批量导入操作**。
- 在查询中使用 `LIMIT` 限制返回的数据量。初始值设为 `LIMIT 10`，如需更多数据再增加限制。
- 对于超过 10,000 条记录的查询，请使用 `sf data export bulk` 而不是 `sf data query`。
- 当用户需要“查找”或“搜索”单个对象时，使用 SOQL 的 `WHERE ... LIKE '%term%'`。当需要在多个对象中搜索时，使用 `sf data search`。
- 如果用户拥有多个组织，请使用 `--target-org <alias>` 选项；如有疑问，请询问用户具体使用哪个组织。
- 如果身份验证失败或会话过期，请引导用户重新登录（使用 `sf org login web`）。
- Batch API 2.0 有一些 SOQL 限制（例如不支持 `COUNT()` 等聚合函数），此时请使用标准的 `sf data query`。
- 在描述对象（`sf sobject describe`）时，JSON 输出可能非常庞大。应为用户总结关键字段、必填字段及对象之间的关系，而不是直接输出原始数据。