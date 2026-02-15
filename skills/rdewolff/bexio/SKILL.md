---
name: bexio
description: Bexio Swiss Business Software API：用于管理联系人、报价/报价单、发票、订单以及商品/产品。适用于与Bexio CRM系统协同工作，包括创建或管理发票、报价单、销售订单、联系人信息，以及执行瑞士企业的日常管理任务。该API支持联系人及销售文档的查询、创建和编辑功能。
---

# Bexio

Bexio 是一款瑞士开发的商业软件 API，支持客户关系管理（CRM）、发票处理、报价生成、订单管理以及产品信息查询等功能。

## 设置

从 Bexio 获取个人访问令牌（Personal Access Token, PAT）：
1. 访问 https://office.bexio.com → 设置（Settings）→ 安全（Security）→ 个人访问令牌（Personal Access Tokens）
2. 创建一个具有所需权限范围的新的令牌。

将令牌保存在 `~/.clawdbot/clawdbot.json` 文件中：
```json
{
  "skills": {
    "entries": {
      "bexio": {
        "accessToken": "YOUR_ACCESS_TOKEN"
      }
    }
  }
}
```

或者通过环境变量设置：`BEXIO_ACCESS_TOKEN=xxx`

## 所需的权限范围（Required Scopes）：

- `contact_show`, `contact_edit` - 联系人信息（Contacts）
- `kb_offer_show`, `kb_offer_edit` - 报价/报价单（Quotes/Offers）
- `kbinvoice_show`, `kbinvoice_edit` - 发票（Invoices）
- `kb_order_show`, `kb_order_edit` - 订单（Orders）
- `article_show` - 产品信息（Articles/Products）

## 快速参考

### 联系人信息（Contacts）
```bash
{baseDir}/scripts/bexio.sh contacts list              # List all contacts
{baseDir}/scripts/bexio.sh contacts search "query"    # Search contacts
{baseDir}/scripts/bexio.sh contacts show <id>         # Get contact details
{baseDir}/scripts/bexio.sh contacts create --name "Company" --type company
{baseDir}/scripts/bexio.sh contacts edit <id> --email "new@email.com"
```

### 报价/报价单（Quotes/Offers）
```bash
{baseDir}/scripts/bexio.sh quotes list                # List quotes
{baseDir}/scripts/bexio.sh quotes search "query"      # Search quotes
{baseDir}/scripts/bexio.sh quotes show <id>           # Get quote details
{baseDir}/scripts/bexio.sh quotes create --contact <id> --title "Project Quote"
{baseDir}/scripts/bexio.sh quotes clone <id>          # Clone a quote
{baseDir}/scripts/bexio.sh quotes send <id> --email "client@email.com"
```

### 发票（Invoices）
```bash
{baseDir}/scripts/bexio.sh invoices list              # List invoices
{baseDir}/scripts/bexio.sh invoices search "query"    # Search invoices
{baseDir}/scripts/bexio.sh invoices show <id>         # Get invoice details
{baseDir}/scripts/bexio.sh invoices create --contact <id> --title "Invoice"
{baseDir}/scripts/bexio.sh invoices issue <id>        # Issue draft invoice
{baseDir}/scripts/bexio.sh invoices send <id> --email "client@email.com"
{baseDir}/scripts/bexio.sh invoices cancel <id>       # Cancel invoice
```

### 订单（Orders）
```bash
{baseDir}/scripts/bexio.sh orders list                # List orders
{baseDir}/scripts/bexio.sh orders search "query"      # Search orders
{baseDir}/scripts/bexio.sh orders show <id>           # Get order details
{baseDir}/scripts/bexio.sh orders create --contact <id> --title "Sales Order"
```

### 产品信息（Articles/Products）
```bash
{baseDir}/scripts/bexio.sh items list                 # List all items
{baseDir}/scripts/bexio.sh items search "query"       # Search items
{baseDir}/scripts/bexio.sh items show <id>            # Get item details
```

## 文档状态（Document Statuses）：

- **报价单（Quotes）**：草稿（draft）、待处理（pending）、已接受（accepted）、已拒绝（declined）
- **发票（Invoices）**：草稿（draft）、待处理（pending）、已支付（paid）、部分支付（partial）、已取消（canceled）
- **订单（Orders）**：草稿（draft）、待处理（pending）、已完成（done）

## 注意事项：

- **API 基址（API Base）**：`https://api.bexio.com`
- **认证方式（Auth）**：在请求头中传递 Bearer 令牌
- **请求速率限制（Rate Limit）**：约 1000 次请求/分钟（请查看 `X-RateLimit-*` 请求头）
- **分页（Pagination）**：使用 `?limit=X&offset=Y` 参数进行分页
- 在创建或编辑文档之前，请务必进行确认

## API 参考文档

有关端点的详细文档，请参阅 [references/api.md](references/api.md)。