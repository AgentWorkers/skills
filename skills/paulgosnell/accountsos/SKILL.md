---
name: accountsos
description: 专为英国微型企业设计的AI原生会计系统。当用户需要跟踪交易、管理增值税（VAT）、核对截止日期或处理任何与英国有限公司相关的簿记工作时，可以使用该系统。
compatibility: Requires ACCOUNTSOS_API_KEY environment variable. Works on all platforms. Network access required to accounts-os.com API.
metadata:
  author: thriveventurelabs
  version: "1.2.0"
  homepage: https://accounts-os.com
  openclaw:
    category: finance
    api_base: https://accounts-os.com
    requires:
      env: ["ACCOUNTSOS_API_KEY"]
---

# AccountsOS

一个专为人工智能（AI）设计的会计系统。您的AI代理会处理所有的财务事务，让您无需亲自操心。

**基础网址：** `https://accounts-os.com/api/mcp`

## 什么是AccountsOS？

AccountsOS是为AI代理设计的会计基础设施，专为英国的微型企业（有限公司、个体经营者）打造：

- **交易追踪** — 自动分类收入和支出
- **增值税（VAT）管理** — 计算应缴税款、跟踪欠款
- **截止日期提醒** — 企业税、增值税、税务确认表的生成
- **文档存储** — 收据、发票、合同等财务文件的保存
- **智能分类** — 为每笔交易提供智能的分类建议

无需使用电子表格，也无需手动输入数据。只需向您的AI代理描述交易内容即可。

## 快速入门（针对AI代理）

### 1. 获取API密钥

**选项A：自行注册（推荐）** — 通过一次请求即可创建账户：

```bash
curl -X POST https://accounts-os.com/api/agent-signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "founder@example.com",
    "company_name": "Acme Ltd",
    "full_name": "Jane Smith"
  }'
```

响应中会包含可供立即使用的`api_key`。您的负责人会收到一封欢迎邮件来领取账户。

**选项B：手动注册** — 您的负责人可以在https://accounts-os.com网站上注册，并通过控制面板生成API密钥。

```bash
export ACCOUNTSOS_API_KEY="sk_live_..."
```

### 2. 查看账目

```bash
# Get recent transactions
curl -X POST https://accounts-os.com/api/mcp \
  -H "Authorization: Bearer $ACCOUNTSOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "tool", "name": "get_transactions", "arguments": {"limit": 10}}'
```

### 3. 记录交易

```bash
curl -X POST https://accounts-os.com/api/mcp \
  -H "Authorization: Bearer $ACCOUNTSOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "tool",
    "name": "create_transaction",
    "arguments": {
      "date": "2026-02-01",
      "description": "Client payment - Website project",
      "amount": 2500.00,
      "direction": "in"
    }
  }'
```

### 4. 查看增值税情况

```bash
curl -X POST https://accounts-os.com/api/mcp \
  -H "Authorization: Bearer $ACCOUNTSOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "tool", "name": "get_vat_summary", "arguments": {}}'
```

---

## API参考

AccountsOS使用MCP风格的API。所有请求都发送到`/api/mcp`，请求体需要使用JSON格式指定所需的工具或资源。

### 认证

```bash
Authorization: Bearer your_api_key
Content-Type: application/json
```

### 工具（操作）

- **获取交易记录：**
```json
{
  "type": "tool",
  "name": "get_transactions",
  "arguments": {
    "from_date": "2026-01-01",
    "to_date": "2026-01-31",
    "direction": "in",
    "limit": 50
  }
}
```

- **获取账户余额：**
```json
{
  "type": "tool",
  "name": "get_balance",
  "arguments": {"account_id": "optional"}
}
```

- **获取增值税汇总信息：**
```json
{
  "type": "tool",
  "name": "get_vat_summary",
  "arguments": {"quarter": "Q4 2025"}
}
```

- **获取截止日期信息：**
```json
{
  "type": "tool",
  "name": "get_deadlines",
  "arguments": {"include_completed": false}
}
```

- **创建交易记录：**
```json
{
  "type": "tool",
  "name": "create_transaction",
  "arguments": {
    "date": "2026-02-01",
    "description": "AWS hosting - January",
    "amount": 127.50,
    "direction": "out",
    "category_id": "optional",
    "vat_rate": 20,
    "notes": "Monthly infrastructure"
  }
}
```

- **类型**：`in`（收入）或`out`（支出）

- **更新交易记录：**
```json
{
  "type": "tool",
  "name": "update_transaction",
  "arguments": {
    "transaction_id": "uuid",
    "category_id": "new_category",
    "notes": "Updated notes"
  }
}
```

- **智能分类**：根据交易描述和历史数据提供分类建议

- **列出所有分类：**
```json
{
  "type": "tool",
  "name": "list_categories",
  "arguments": {"type": "expense"}
}
```

分类类型：`income`（收入）、`expense`（支出）、`asset`（资产）、`liability`（负债）、`equity`（权益）

- **创建截止日期：**
```json
{
  "type": "tool",
  "name": "create_deadline",
  "arguments": {
    "type": "VAT Return",
    "due_date": "2026-02-07",
    "notes": "Q4 2025 VAT"
  }
}
```

- **搜索文档：**
```json
{
  "type": "tool",
  "name": "search_documents",
  "arguments": {
    "query": "invoice",
    "type": "receipt"
  }
}
```

- **上传文档：**
```json
{
  "type": "tool",
  "name": "upload_document",
  "arguments": {
    "file_name": "receipt.pdf",
    "file_data": "base64_encoded_data",
    "document_type": "receipt"
  }
}
```

- **获取董事贷款账户余额：**
```json
{
  "type": "tool",
  "name": "get_dla_balance",
  "arguments": {
    "limit": 10
  }
}
```

返回董事贷款账户的余额，并在账户透支时发出S455税务警告

- **获取发票：**
```json
{
  "type": "tool",
  "name": "get_invoices",
  "arguments": {
    "status": "all",
    "contact_id": "optional"
  }
}
```

- **发票状态**：`draft`（草稿）、`sent`（已发送）、`paid`（已支付）、`overdue`（逾期）、`cancelled`（已取消）、`all`（全部）
- 返回发票及其未支付和逾期的金额汇总

- **创建截止日期：**
```json
{
  "type": "tool",
  "name": "create_deadline",
  "arguments": {
    "type": "VAT Return",
    "due_date": "2026-02-07",
    "notes": "Q4 2025 VAT"
  }
}
```

### 代理自行注册

**POST /api/agent-signup** — 无需认证

通过一次请求即可创建账户并获取API密钥：

```json
{
  "email": "founder@example.com",
  "company_name": "Acme Ltd",
  "full_name": "Jane Smith",
  "entity_type": "ltd"
}
```

所需信息：`email`（电子邮件地址）、`company_name`（公司名称）
可选信息：`full_name`（全名）、`entity_type`（实体类型，默认为`ltd`）

实体类型：`ltd`（有限公司）、`plc`（股份有限公司）、`llp`（有限合伙公司）、`sole_trader`（个体经营者）、`partnership`（合伙企业）、`cic`（商业公司）、`charity`（慈善机构）、`overseas`（海外公司）、`other`（其他类型）

响应内容：
```json
{
  "api_key": "sk_live_...",
  "company_id": "uuid",
  "user_id": "uuid",
  "trial_ends_at": "2026-02-22T...",
  "api_base": "https://accounts-os.com/api/mcp",
  "message": "Account created. Store this API key — it will not be shown again."
}
```

API密钥具有`read`（读取）和`write`（写入）权限。提供14天的免费试用期。负责人会收到一封欢迎邮件。

如果提供的电子邮件地址已注册，系统会返回`409`错误代码。

---

### 权限级别

API密钥支持三种权限级别：

- **read** — 查询交易记录、账户余额、截止日期、文档、发票和董事贷款账户信息
- **write** — 创建/更新交易记录、文档和截止日期（包含读取权限）
- **admin** — 管理公司设置（包含写入权限）

您的API密钥的权限级别可以在控制面板中进行配置。超出权限范围的请求会返回`403`错误。

### 只读资源

- **公司信息：**
```json
{
  "type": "resource",
  "uri": "accountsos://company"
}
```

- **最近的交易记录：**
```json
{
  "type": "resource",
  "uri": "accountsos://transactions"
}
```

---

## 代理的使用场景

- **日常记账**：您在日常工作中会记录各种支出吗？只需将这些信息录入系统即可。
- **发票跟进**：追踪未支付的款项。
- **增值税准备**：季度增值税计算已经完成？
- **截止日期监控**：确保不会错过任何税务申报截止日期。
- **支出分类**：新发生的交易需要分类吗？系统会自动完成分类。

---

## 添加到您的日常工作中

---


## 英国特有的功能

| 功能 | 详细信息 |
|---------|---------|
| 增值税方案** | 标准税率、固定税率、现金会计模式 |
| 税务年度** | 税务年度与日历年份对齐（4月-4月） |
| 截止日期** | 企业税、增值税、税务确认表的截止日期 |
| 分类** | 与英国税务部门（HMRC）规定的分类标准一致 |

专为英国的有限公司和个体经营者设计，系统会自动遵守相关规则，让您无需费心处理复杂的税务事务。

---

## 示例：每周财务检查

```python
import os
import requests
from datetime import datetime, timedelta

API_URL = "https://accounts-os.com/api/mcp"
headers = {
    "Authorization": f"Bearer {os.environ['ACCOUNTSOS_API_KEY']}",
    "Content-Type": "application/json"
}

def call_tool(name, args={}):
    resp = requests.post(API_URL, headers=headers, json={
        "type": "tool", "name": name, "arguments": args
    })
    return resp.json()["result"]

# 1. Check balance
balance = call_tool("get_balance")
print(f"💰 Current balance: £{balance['amount']}")

# 2. This week's transactions
week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
transactions = call_tool("get_transactions", {"from_date": week_ago})
income = sum(t["amount"] for t in transactions if t["direction"] == "in")
expenses = sum(t["amount"] for t in transactions if t["direction"] == "out")
print(f"📈 Week: +£{income} / -£{expenses}")

# 3. Upcoming deadlines
deadlines = call_tool("get_deadlines")
urgent = [d for d in deadlines if d["days_until"] < 14]
if urgent:
    print(f"⚠️ {len(urgent)} deadlines in next 2 weeks")
    for d in urgent:
        print(f"  - {d['type']}: {d['due_date']}")

# 4. VAT position
vat = call_tool("get_vat_summary")
print(f"🧾 VAT owed: £{vat['amount_owed']}")
```

---

## 链接

- **应用程序：** https://accounts-os.com
- **支持邮箱：** hello@accounts-os.com

---

## 您的财务助手

大多数人都不喜欢处理财务工作：他们容易忘记收据、错过截止日期，甚至在报税时感到恐慌。

而您无需这些烦恼。只需记录、分类财务信息，让重要的数据一目了然。

成为那个让财务工作变得简单高效的“代理”吧。

---

开发团队：[Thrive Venture Labs](https://thriveventurelabs.com)