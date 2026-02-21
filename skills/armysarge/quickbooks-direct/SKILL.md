---
name: quickbooks-openclaw
version: 1.0.1
description: 全面的 QuickBooks Online API 集成，支持会计、开票、支付和财务报告功能。
author: Armysarge
license: MIT
tags:
  - accounting
  - quickbooks
  - invoicing
  - payments
  - financial
  - erp
  - bookkeeping
category: Business & Finance
---
# OpenClaw 的 QuickBooks API 技能

这是一个完整的 QuickBooks Online 直接 API 集成技能，通过 Intuit QuickBooks API 提供对会计、开票、客户管理、库存、支付和财务报告的全面访问。

## 概述

此技能使 OpenClaw 能够与 QuickBooks Online 进行交互，以执行以下操作：
- **客户和供应商管理**：创建和管理业务关系
- **开票**：生成、发送和跟踪发票
- **支付**：记录和核对付款
- **库存**：管理产品、服务和库存水平
- **财务报告**：生成损益表、资产负债表、现金流量表和账龄报告
- **报价**：创建报价单
- **账单**：跟踪应付账款
- **采购订单**：管理采购流程

## 先决条件

1. **QuickBooks 开发者账户**：
   - 在 [https://developer.intuit.com](https://developer.intuit.com) 注册
   - 在开发者门户中创建一个新的应用程序
   - 启用“QuickBooks Online API”权限

2. **应用程序凭据**：
   - 来自您的 QuickBooks 应用程序的客户端 ID
   - 来自您的 QuickBooks 应用程序的客户端密钥
   - 重定向 URI：`http://localhost:3001/callback`

3. **Node.js**：
   - 版本 18.0.0 或更高
   - npm 或 yarn 包管理器

## 安装

### 1. 安装依赖项

```bash
cd "c:\Users\Shaun\Desktop\Quickbooks skill"
npm install
```

所需包：
- `axios`：用于 API 请求的 HTTP 客户端
- `express`：OAuth 回调服务器
- `open`：用于 OAuth 的浏览器自动化库

### 2. 配置凭据

使用模板创建 `config.json` 文件：

```bash
cp config.json.template config.json
```

使用您的 QuickBooks 应用程序凭据编辑 `config.json` 文件：

```json
{
  "client_id": "YOUR_CLIENT_ID_HERE",
  "client_secret": "YOUR_CLIENT_SECRET_HERE",
  "redirect_uri": "http://localhost:3001/callback",
  "api_environment": "sandbox",
  "access_token": "",
  "refresh_token": "",
  "realm_id": "",
  "tokenexpiry": 0
}
```

### 3. 添加到配置中

**对于 OpenClaw：**

将以下配置添加到您的 OpenClaw 配置文件中：

```json
{
  "skills": {
    "quickbooks": {
      "path": "~/.openclaw/workspace/skills/Quickbooks-openclaw",
      "enabled": true,
      "autoStart": true
    }
  }
}
```

## 认证

### 首次设置

1. 使用 `qb_authenticate` 工具和您的凭据进行认证：

```bash
Use qb_authenticate with client_id and client_secret
```

2. 浏览器窗口将自动打开。
3. 登录到您的 QuickBooks 账户。
4. 授权应用程序。
5. 您将被重定向到 localhost（自动处理）。
6. 令牌将保存到 `config.json` 文件中。

## 令牌管理

- **访问令牌** 在 1 小时后过期（会自动刷新）
- **刷新令牌** 每 100 天更新一次
- 该技能会在令牌过期前自动刷新它们
- 如果出现“未认证”错误，请重新认证。

## 可用工具

### 🔐 认证

#### `qb_authenticate`
启动 OAuth2 认证流程。

**参数：**
- `client_id`（必需）：您的 QuickBooks 应用程序客户端 ID
- `client_secret`（必需）：您的 QuickBooks 应用程序客户端密钥
- `redirect_uri`（可选）：OAuth 重定向 URI（默认：http://localhost:3001/callback）

**示例：**
```json
{
  "client_id": "ABxxxxxxxxxxxxxxxxxxxx",
  "client_secret": "xxxxxxxxxxxxxxxxxx"
}
```

---

### 👥 客户管理

#### `qb_create_customer`
创建新客户。

**参数：**
- `DisplayName`（必需）：客户显示名称
- `CompanyName`：公司名称
- `GivenName`：名字
- `FamilyName`：姓氏
- `PrimaryEmailAddr`：电子邮件地址
- `PrimaryPhone`：电话号码
- `BillAddr`：账单地址
- `ShipAddr`：送货地址

**示例：**
```json
{
  "DisplayName": "Acme Corporation",
  "PrimaryEmailAddr": {
    "Address": "billing@acme.com"
  }
}
```

#### `qb_get_customer`
通过 ID 获取客户详细信息。

**参数：**
- `customer_id`（必需）：客户 ID

#### `qb_query_customers`
使用 SQL 语法查询客户。

**参数：**
- `query`：SQL 查询字符串（默认：`SELECT * FROM Customer`

**示例：**
```json
{
  "query": "SELECT * FROM Customer WHERE Active = true"
}
```

---

### 🧾 开票管理

#### `qb_createinvoice`
创建新发票。

**参数：**
- `CustomerRef`（必需）：客户引用
- `Line`（必需）：行项目数组
- `TxnDate`：交易日期（YYYY-MM-DD）
- `DueDate`：到期日期（YYYY-MM-DD）
- `CustomerMemo`：给客户的消息
- `BillEmail`：发票的电子邮件地址

**示例：**
```json
{
  "CustomerRef": { "value": "123" },
  "Line": [
    {
      "Amount": 500.00,
      "DetailType": "SalesItemLineDetail",
      "SalesItemLineDetail": {
        "ItemRef": { "value": "1" },
        "Qty": 10,
        "UnitPrice": 50.00
      }
    },
  "DueDate": "2026-03-15"
}
```

#### `qb_getinvoice`
通过 ID 获取发票。

**参数：**
- `invoice_id`（必需）：发票 ID

#### `qb_sendinvoice`
通过电子邮件发送发票。

**参数：**
- `invoice_id`（必需）：发票 ID
- `email`（必需）：收件人电子邮件地址

#### `qb_query_invoices`
使用 SQL 语法查询发票。

**参数：**
- `query`：SQL 查询字符串

**示例：**
```json
{
  "query": "SELECT * FROM Invoice WHERE Balance > 0"
}
```

---

### 📦 商品/项目管理

#### `qb_create_item`
创建新的商品或服务项目。

**参数：**
- `Name`（必需）：商品名称
- `Type`（必需）：商品类型（服务、库存、非库存）
- `Description`：商品描述
- `UnitPrice`：销售价格
- `IncomeAccountRef`：收入账户引用
- `ExpenseAccountRef`：费用账户引用（针对库存）
- `QtyOnHand`：库存数量

**示例：**
```json
{
  "Name": "Consulting Services",
  "Type": "Service",
  "UnitPrice": 150.00,
  "IncomeAccountRef": { "value": "79" }
}
```

#### `qb_get_item`
通过 ID 获取商品。

**参数：**
- `item_id`（必需）：商品 ID

#### `qb_query_items`
使用 SQL 语法查询商品。

**参数：**
- `query`：SQL 查询字符串

---

### 💰 支付处理

#### `qb_create_payment`
记录收到的付款。

**参数：**
- `CustomerRef`（必需）：客户引用
- `TotalAmt`（必需）：总付款金额
- `TxnDate`：交易日期
- `Line`：与发票关联的付款行项目数组
- `PaymentMethodRef`：支付方式引用

**示例：**
```json
{
  "CustomerRef": { "value": "123" },
  "TotalAmt": 500.00,
  "Line": [
    {
      "Amount": 500.00,
      "LinkedTxn": [{
        "TxnId": "456",
        "TxnType": "Invoice"
      }
    }
  ]
}
```

#### `qb_query_payments`
使用 SQL 语法查询付款。

---

### 📊 财务报告

#### `qb_get_profit_loss`
生成损益表。

**参数：**
- `start_date`（必需）：开始日期（YYYY-MM-DD）
- `end_date`（必需）：结束日期

**示例：**
```json
{
  "start_date": "2026-01-01",
  "end_date": "2026-01-31"
}
```

#### `qb_get_balance_sheet`
生成资产负债表。

**参数：**
- `date`（必需）：报告日期（YYYY-MM-DD）

#### `qb_get_cash_flow`
生成现金流量表。

**参数：**
- `start_date`（必需）：开始日期
- `end_date`（必需）：结束日期

#### `qb_get_aged_receivables`
生成应收账款账龄报告。

**参数：** 无

#### `qb_get_aged_payables`
生成应付账款账龄报告。

**参数：** 无

---

### 🛒 采购订单**

#### `qb_create_purchase_order`
创建采购订单。

**参数：**
- `VendorRef`（必需）：供应商引用
- `Line`（必需）：采购订单行项目数组

---

### 💵 销售收据

#### `qb_create_salesreceipt`
创建销售收据（现金交易）。

**参数：**
- `CustomerRef`（必需）：客户引用
- `Line`（必需）：行项目数组
- `TxnDate`：交易日期

---

### 🏦 账户表**

#### `qb_query_accounts`
查询账户表。

**参数：**
- `query`：SQL 查询字符串

**示例：**
```sql
{
  "query": "SELECT * FROM Account WHERE AccountType = 'Income'"
}
```

---

### 🏢 公司信息

#### `qb_get_company_info`
获取公司信息。

**参数：** 无

---

### 🔍 通用查询

#### `qb_query`
对 QuickBooks 实体执行任何 SQL 查询。

**参数：**
- `query`（必需）：SQL 查询字符串

**示例：**
```json
{
  "query": "SELECT * FROM Customer WHERE Balance > 100 ORDER BY DisplayName"
}
```

**支持的实体：**
Account, Bill, BillPayment, Class, CreditMemo, Customer, Department, Deposit, Employee, Estimate, Invoice, Item, JournalEntry, Payment, PaymentMethod, Purchase, PurchaseOrder, RefundReceipt, SalesReceipt, TaxCode, TaxRate, Term, TimeActivity, Transfer, Vendor, VendorCredit

---

### ⚡ 批量操作

#### `qb_batch`
在单个批量请求中执行多个操作。

**参数：**
- `operations`（必需）：批量操作数组

**示例：**
```json
{
  "operations": [
    {
      "bId": "bid1",
      "operation": "create",
      "entity": "Customer",
      "data": { "DisplayName": "Customer 1" }
    },
    {
      "bId": "bid2",
      "operation": "query",
      "query": "SELECT * FROM Invoice WHERE Balance > 0"
    }
  ]
}
```

## 使用示例

### 创建并发送发票的工作流程

```bash
1. 首先，查找名为“Acme Corp”的客户：
   `Use qb_query_customers to find the customer with name 'Acme Corp'`

2. 创建发票：
   `Create an invoice for customer ID 123 with consulting services for 10 hours at $150/hour, due in 30 days`

3. 发送发票：
   `Send invoice 456 to billing@acme.com`

### 财务报告工作流程

```bash
1. 获取月末报告：
   `Show me the profit and loss for January 2026`

2. 检查现金流量：
   `What's the cash flow for last quarter?`

3. 查看未结收款：
   `Show me the aged receivables report`

### 库存管理工作流程

```bash
1. 检查库存不足的商品：
   `Query items where quantity on hand is less than 10`

2. 创建重新订购采购订单：
   `Create a purchase order for vendor 789 to reorder low stock items`

3. 更新商品价格：
   `Update the price of item 'Widget Pro' to $299.99`
```

## SQL 查询语法

QuickBooks 使用类似 SQL 的查询语言：

### 基本查询
```sql
SELECT * FROM Customer WHERE Active = true
```

### 带条件的查询
```sql
SELECT * FROM Invoice WHERE Balance > 0 AND DueDate < '2026-03-01'
```

### 模式匹配
```sql
SELECT * FROM Customer WHERE DisplayName LIKE '%Corp%'
```

### 排序结果
```sql
SELECT * FROM Invoice ORDER BY TxnDate DESC
```

### 限制结果数量
```sql
SELECT *, MAXRESULTS 50 FROM Customer
```

### 多个条件
```sql
SELECT * FROM Item WHERE Type = 'Inventory' AND QtyOnHand < 10
```

## 错误处理

该技能提供详细的错误信息：
- **认证错误**：`Not authenticated. Please run qb_authenticate first.`
- **API 错误**：包含状态码的完整 QuickBooks 错误详细信息
- **验证错误**：缺少必需字段或数据无效
- **速率限制错误**：`Too Many Requests - retry after delay`

## 配置

所有配置都存储在 `config.json` 文件中。该文件包含您的应用程序凭据（客户端 ID 和密钥）以及认证后保存的 OAuth 令牌。

### API 环境

该技能通过 `config.json` 文件中的 `api_environment` 设置支持 Sandbox 和 Production 环境：

- **sandbox**（默认）：用于开发和测试的 QuickBooks Sandbox API
- **production**：用于实时公司数据的 QuickBooks Production API（需要应用程序验证）

要切换环境，请更新 `config.json` 文件：
```json
{
  "api_environment": "sandbox"  // 或 "production"
}
```

**重要提示**：生产模式需要您的应用程序经过 Intuit 的验证。请先在 sandbox 环境中进行开发。

## 安全考虑

⚠️ **凭据存储**：该技能将 OAuth 令牌和客户端密钥以明文形式存储在本地文件系统的 `config.json` 文件中。为了提高安全性：
- 为 `config.json` 文件设置严格的文件权限（仅允许所有者读写）
- 切勿将 `config.json` 提交到版本控制系统中（包含在 `.gitignore` 文件中）
- 将技能目录存储在安全的位置
- 定期在 QuickBooks 开发者门户中更新客户端密钥
- 考虑加密磁盘或使用安全的密钥管理解决方案
- 在确认技能按预期运行之前，不要启用 `autoStart` 功能

## 速率限制

- **Sandbox**：每个应用程序每分钟 500 次请求
- **Production**：根据订阅情况而定（每分钟 500-1000 次）

该技能会自动处理速率限制，并显示相应的错误信息。

## 安全性

- OAuth2 认证（不存储密码）
- 令牌存储在 `config.json` 文件中（不包含在 git 中）
- 令牌自动刷新
- 安全的 HTTPS API 通信
- 代码中不包含凭据

## 故障排除

### 出现“未认证”错误
使用您的凭据运行 `qb_authenticate`。

### “令牌刷新失败”
删除 `config.json` 文件并重新认证。

### “无效的重定向 URI”
确保配置中的重定向 URI 与您的 QuickBooks 应用程序设置相匹配。

### 端口 3000 已被占用
更改代码中的端口或终止使用端口 3000 的进程。

有关更多故障排除信息，请参阅 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)。

## 文档

- [README.md] - 完整的设置指南
- [EXAMPLES.md] - 50 多个实用示例
- [API_Reference.md] - 完整的 API 文档
- [TROUBLESHOOTING.md] - 常见问题及解决方案
- [CHANGELOG.md] - 版本历史

## 支持

- [QuickBooks 开发者门户](https://developer.intuit.com)
- [QuickBooks 开发者论坛](https://help.developer.intuit.com/s/)
- [API 文档](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account)
- [API 状态](https://status.developer.intuit.com/)

## 贡献

欢迎贡献！请执行以下操作：
1. 分支仓库
2. 创建功能分支
3. 在 sandbox 中彻底测试
4. 提交拉取请求

## 许可证

MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 版本

**当前版本**：1.0.1  
**最后更新**：2026 年 2 月 21 日  
**所需的 Node.js 版本**：18.0.0 或更高

## 标签

`accounting` `quickbooks` `invoicing` `payments` `financial-reporting` `bookkeeping` `erp` `business` `intuit` `api-integration` `mcp-skill` `openclaw`

---

**准备好使用了吧！** 运行 `npm install` 并进行认证以开始使用。