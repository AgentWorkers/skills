---
name: mayar-payment
description: Mayar.id 支付集成功能可用于通过 MCP（Mayar Integration Platform）生成发票、支付链接并追踪交易。适用于以下场景：  
(1) 为顾客创建支付发票/链接；  
(2) 跟踪支付状态和交易详情；  
(3) 生成适合在 WhatsApp 上发送的支付通知；  
(4) 支持印度尼西亚的支付方式（银行转账、电子钱包、QRIS）；  
(5) 管理订阅服务或会员资格；  
(6) 自动化电子商务、服务或数字产品的支付流程。
---

# Mayar 支付集成

通过 MCP（Model Context Protocol）集成 Mayar.id 支付平台，以实现印尼地区的支付处理功能。

## 先决条件

1. **Mayar.id 账户** - 在 https://mayar.id 注册账户。
2. **API 密钥** - 从 https://web.mayar.id/api-keys 生成 API 密钥。
3. **mcporter 已配置** - 必须在 Clawdbot 中设置 MCP。

## 设置

### 1. 存储 API 凭据

```bash
mkdir -p ~/.config/mayar
cat > ~/.config/mayar/credentials << EOF
MAYAR_API_TOKEN="your-jwt-token-here"
EOF
chmod 600 ~/.config/mayar/credentials
```

### 2. 配置 MCP 服务器

将以下内容添加到 `config/mcporter.json` 文件中：

```json
{
  "mcpServers": {
    "mayar": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.mayar.id/sse",
        "--header",
        "Authorization:YOUR_API_TOKEN_HERE"
      ]
    }
  }
}
```

请将 `YOUR_API_TOKEN_HERE` 替换为实际的 API 密钥。

### 3. 测试连接

```bash
mcporter list mayar
```

应显示 15 个及以上可用的支付工具。

## 核心工作流程

### 创建带有支付链接的发票

**最常见的使用场景：** 为客户生成支付链接。

```bash
mcporter call mayar.create_invoice \
  name="Customer Name" \
  email="email@example.com" \
  mobile="\"628xxx\"" \
  description="Order description" \
  redirectURL="https://yoursite.com/thanks" \
  expiredAt="2026-12-31T23:59:59+07:00" \
  items='[{"quantity":1,"rate":500000,"description":"Product A"}]'
```

**返回值：**
```json
{
  "id": "uuid",
  "transactionId": "uuid", 
  "link": "https://subdomain.myr.id/invoices/slug",
  "expiredAt": 1234567890
}
```

**关键字段：**
- `mobile` - 必须是一个字符串，格式为 `\"628xxx\"`。
- `expiredAt` - 采用 ISO 8601 格式，并包含时区信息。
- `items` - 一个数组，每个元素包含 `quantity`（数量）、`rate`（价格）和 `description`（描述）。
- `redirectURL` - 客户完成支付后跳转的网址。

### WhatsApp 集成模式

```javascript
// 1. Create invoice
const invoice = /* mcporter call mayar.create_invoice */;

// 2. Format message
const message = `
✅ *Order Confirmed!*

*Items:*
• Product Name
  Rp ${amount.toLocaleString('id-ID')}

*TOTAL: Rp ${total.toLocaleString('id-ID')}*

💳 *Pembayaran:*
${invoice.data.link}

⏰ Berlaku sampai: ${expiryDate}

Terima kasih! 🙏
`.trim();

// 3. Send via WhatsApp
message({
  action: 'send',
  channel: 'whatsapp',
  target: customerPhone,
  message: message
});
```

### 检查支付状态

```bash
# Get latest transactions (check if paid)
mcporter call mayar.get_latest_transactions page:1 pageSize:10

# Get unpaid invoices
mcporter call mayar.get_latest_unpaid_transactions page:1 pageSize:10
```

根据状态进行过滤：`\"created\"`（未支付）→ `\"paid\"`（已支付）。

### 其他操作

```bash
# Check account balance
mcporter call mayar.get_balance

# Get customer details
mcporter call mayar.get_customer_detail \
  customerName="Name" \
  customerEmail="email@example.com" \
  page:1 pageSize:10

# Filter by time period
mcporter call mayar.get_transactions_by_time_period \
  page:1 pageSize:10 \
  period:"this_month" \
  sortField:"createdAt" \
  sortOrder:"DESC"
```

## 常见模式

### 多商品发票

```javascript
items='[
  {"quantity":2,"rate":500000,"description":"Product A"},
  {"quantity":1,"rate":1000000,"description":"Product B"}
]'
// Total: 2M (2×500K + 1×1M)
```

### 订阅/定期支付

使用会员功能：

```bash
mcporter call mayar.get_membership_customer_by_specific_product \
  productName:"Premium Membership" \
  productLink:"your-product-link" \
  productId:"product-uuid" \
  page:1 pageSize:10 \
  memberStatus:"active"
```

### 支付确认流程

**选项 A：Webhook**（实时通知）**
- 在 Mayar 中注册 webhook URL。
- 实时接收支付通知。
- 适合生产环境。

**选项 B：轮询**（较简单）
- 每 30-60 秒轮询一次 `get_latest_transactions` 接口。
- 检查是否有新的支付记录。
- 适合 MVP 或测试环境。

## 故障排除

**支付链接显示 404 错误：**
- 链接格式：`https://your-subdomain.myr.id/invoices/slug`
- 确认控制面板中的子域名是否正确。
- 默认子域名可能是账户名称。

**手机号码无效：**
- 手机号码必须是一个字符串，格式为 `\"628xxx\"`（使用反引号）。
- 格式应为 `628xxxxxxxxxx`（不允许包含加号或空格）。

**发票过期：**
- 默认过期时间为 `expiredAt` 时间戳。
- 过期后客户无法进行支付。
- 如有需要，可以重新创建发票。

## 参考文档

- **API 详情：** 查看 [references/api-reference.md](references/api-reference.md)
- **集成示例：** 查看 [references/integration-examples.md](references/integration-examples.md)
- **MCP 工具参考：** 查看 [references/mcp-tools.md](references/mcp-tools.md)

## 生产环境检查清单

- [ ] 使用生产环境的 API 密钥（而非沙盒环境）。
- [ ] 设置用于接收支付通知的 webhook。
- [ ] 处理发票创建失败的情况。
- [ ] 存储发票 ID 以方便追踪。
- [ ] 处理支付到期事件。
- [ ] 集成客户数据库。
- [ ] 自动化处理收款/确认流程。

## 环境配置

**生产环境：**
- 控制面板：https://web.mayar.id
- API 基址：`https://api.mayar.id/hl/v1/`

**沙盒环境（测试）：**
- 控制面板：https://web.mayar.club
- API 基址：`https://api.mayar.club/hl/v1/`