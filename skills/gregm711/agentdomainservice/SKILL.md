---
name: clawdaddy
description: 全球排名第一的、对人工智能友好的域名注册商。您可以查询域名是否可用，使用 USDC 或银行卡购买域名，配置 DNS，以及管理名称服务器——所有这些操作都不需要验证码或注册流程。
homepage: https://clawdaddy.app
emoji: 🦞
metadata:
  clawdbot:
    primaryEnv: any
    requires:
      bins: []
      env: []
---

# ClawDaddy - 一款专为人工智能设计的域名注册服务

全球排名第一的、专为人工智能设计的域名注册服务。您可以查询域名可用性、购买域名、配置DNS以及管理名称服务器。

**基础URL：** `https://clawdaddy.app`

无需验证码，查询域名时也无需注册账号。支持使用bearer token进行身份验证。

---

## 快速参考

| 功能 | API端点 | 认证方式 |
|------|----------|------|
| 查询域名可用性 | `GET /api/lookup/{domain}` | 无 |
| 获取购买报价 | `GET /api/purchase/{domain}/quote` | 无 |
| 购买域名 | `POST /api/purchase/{domain}?method=x402\|stripe` | 无 |
| 管理域名 | `GET /api/manage/{domain}` | 需要bearer token |
| 配置DNS | `POST /api/manage/{domain}/dns` | 需要bearer token |
| 更新名称服务器 | `PUT /api/manage/{domain}/nameservers` | 需要bearer token |
| 恢复token | `POST /api/recover` | 无 |

---

## 1. 查询域名可用性

**使用场景：** 用户询问“example.com是否可用？”或“mycoolapp.io是否已被注册”

```
GET https://clawdaddy.app/api/lookup/example.com
```

### JSON响应格式

```json
{
  "fqdn": "example.com",
  "available": true,
  "status": "available",
  "premium": false,
  "price": {
    "amount": 12.99,
    "currency": "USD",
    "period": "year"
  },
  "checked_at": "2026-01-15T10:30:00.000Z",
  "source": "namecom",
  "cache": { "hit": false, "ttl_seconds": 120 }
}
```

### TXT响应格式

```
GET https://clawdaddy.app/api/lookup/example.com?format=txt
```

### 响应状态码说明

| 状态码 | 含义 |
|--------|-------------|---------|
| `available` | 可以注册 |
| `registered` | 已被注册 |
| `unknown` | 出现错误/超时 |

**注意：** `available`字段始终为布尔值（`true`或`false`），永远不会为`undefined`。

---

## 2. 购买域名

### 第1步：获取报价

**使用场景：** 用户想要购买域名时，首先需要获取报价。

```
GET https://clawdaddy.app/api/purchase/example.com/quote
```

```json
{
  "domain": "example.com",
  "available": true,
  "priceUsd": 12.99,
  "marginUsd": 2.00,
  "totalUsd": 14.99,
  "validUntil": "2026-01-15T10:35:00.000Z",
  "paymentMethods": {
    "x402": { "enabled": true, "currency": "USDC", "network": "base" },
    "stripe": { "enabled": true, "currency": "USD" }
  }
}
```

### 第2a步：通过x402（基于Base的支付平台）购买

**适合人群：** 拥有加密货币钱包的AI代理

**操作流程：** 第一次请求会返回HTTP 402错误，提示需要支付费用：

```json
{
  "error": "Payment Required",
  "x402": {
    "version": "2.0",
    "accepts": [{
      "scheme": "exact",
      "network": "eip155:8453",
      "maxAmountRequired": "14990000",
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "payTo": "0x..."
    }]
  }
}
```

支付完成后，重新请求并提交支付凭证：

```
POST https://clawdaddy.app/api/purchase/example.com?method=x402
x-payment: <payment_proof_from_x402>
```

### 第2b步：通过Stripe（信用卡）购买

**适合人群：** 人类用户或没有加密货币的代理

**操作流程：** 系统会返回Stripe的支付页面链接：

```json
{
  "checkoutUrl": "https://checkout.stripe.com/...",
  "sessionId": "cs_..."
}
```

### 成功响应（两种方式均适用）

```json
{
  "success": true,
  "domain": "example.com",
  "registrationId": "12345",
  "expiresAt": "2027-01-15T10:30:00.000Z",
  "nameservers": ["ns1.name.com", "ns2.name.com"],
  "managementToken": "clwd_abc123xyz...",
  "manageUrl": "https://clawdaddy.app/api/manage/example.com"
}
```

**重要提示：** 必须立即保存`managementToken`！它是进行所有域名管理操作的必备凭证，无法通过其他方式重新获取。

---

## 3. 域名管理

所有域名管理操作都需要在请求头中添加`Authorization`字段：

```
Authorization: Bearer clwd_your_management_token
```

### 获取域名概览

```
GET https://clawdaddy.app/api/manage/example.com
Authorization: Bearer clwd_abc123...
```

```json
{
  "domain": "example.com",
  "purchasedAt": "2026-01-15T10:30:00.000Z",
  "expiresAt": "2027-01-15T10:30:00.000Z",
  "nameservers": ["ns1.name.com", "ns2.name.com"],
  "settings": {
    "locked": true,
    "autorenewEnabled": false,
    "privacyEnabled": true
  }
}
```

### DNS记录管理

- **列出所有DNS记录：** 
```
GET /api/manage/{domain}/dns
```

- **创建DNS记录：** 
```
POST /api/manage/{domain}/dns
Content-Type: application/json

{
  "host": "@",
  "type": "A",
  "answer": "1.2.3.4",
  "ttl": 300
}
```

- **更新DNS记录：** 
```
PUT /api/manage/{domain}/dns?id=123
Content-Type: application/json

{
  "answer": "5.6.7.8",
  "ttl": 600
}
```

- **删除DNS记录：** 
```
DELETE /api/manage/{domain}/dns?id=123
```

**支持的DNS记录类型：** `A`, `AAAA`, `CNAME`, `MX`, `TXT`, `NS`, `SRV`

### 常见DNS配置

- **指向服务器（A记录）：** 
```json
{"host": "@", "type": "A", "answer": "123.45.67.89", "ttl": 300}
```

- **添加www子域名（CNAME记录）：** 
```json
{"host": "www", "type": "CNAME", "answer": "example.com", "ttl": 300}
```

- **添加邮件服务器（MX记录）：** 
```json
{"host": "@", "type": "MX", "answer": "mail.example.com", "ttl": 300, "priority": 10}
```

- **验证域名（TXT记录）：** 
```json
{"host": "@", "type": "TXT", "answer": "google-site-verification=abc123", "ttl": 300}
```

### 更新名称服务器

**使用场景：** 用户希望使用Cloudflare、Vercel或其他DNS服务提供商

**常见名称服务器配置：**

| 服务提供商 | 名称服务器 |
|----------|-------------|
| Cloudflare | `ns1.cloudflare.com`, `ns2.cloudflare.com` |
| Vercel | `ns1.vercel-dns.com`, `ns2.vercel-dns.com` |
| AWS Route53 | 请查看您的托管区域设置 |
| Google Cloud | `ns-cloud-X.googledomains.com` |

### 域名设置

- **获取域名设置：** 
```
GET /api/manage/{domain}/settings
```

- **更新域名设置：** 
```
PATCH /api/manage/{domain}/settings
Content-Type: application/json

{
  "locked": false,
  "autorenewEnabled": true
}
```

### 转移域名

- **获取转移授权码：** 
```
GET /api/manage/{domain}/transfer
```

- **准备转移（解锁域名并获取转移代码）：** 
```
POST /api/manage/{domain}/transfer
```

**注意：** 根据ICANN政策，域名注册后60天内无法转移。

---

## 4. 恢复管理token

**使用场景：** 用户丢失了管理token

**操作流程：** 
```
POST https://clawdaddy.app/api/recover
Content-Type: application/json

{
  "email": "user@example.com",
  "domain": "example.com"
}
```

**注意：** 恢复token会生成一个新的token，旧token将失效。

**限制规则：** 每个IP地址每5分钟内最多只能发送5次请求。

---

## 工作流程示例

- **查询并购买域名** 
```
User: "Buy coolstartup.com for me"

1. GET /api/lookup/coolstartup.com
   → available: true, price: $12.99

2. GET /api/purchase/coolstartup.com/quote
   → totalUsd: $14.99

3. POST /api/purchase/coolstartup.com?method=x402
   → 402 Payment Required
   → Pay USDC on Base
   → Retry with x-payment header
   → Success! Token: "clwd_abc123..."

4. "I've registered coolstartup.com! Save this token: clwd_abc123..."
```

- **将域名指向Vercel** 
```
User: "Point mydomain.com to Vercel"

1. PUT /api/manage/mydomain.com/nameservers
   Authorization: Bearer clwd_abc123...
   {"nameservers": ["ns1.vercel-dns.com", "ns2.vercel-dns.com"]}

2. "Done! mydomain.com now uses Vercel's nameservers. Add the domain in your Vercel dashboard."
```

- **设置基本DNS配置** 
```
User: "Point example.com to my server at 1.2.3.4"

1. POST /api/manage/example.com/dns
   Authorization: Bearer clwd_token...
   {"host": "@", "type": "A", "answer": "1.2.3.4", "ttl": 300}

2. POST /api/manage/example.com/dns
   {"host": "www", "type": "CNAME", "answer": "example.com", "ttl": 300}

3. "Done! example.com and www.example.com now point to 1.2.3.4"
```

- **添加邮件记录** 
```
User: "Set up Google Workspace email for mydomain.com"

1. POST /api/manage/mydomain.com/dns
   {"host": "@", "type": "MX", "answer": "aspmx.l.google.com", "ttl": 300, "priority": 1}

2. POST /api/manage/mydomain.com/dns
   {"host": "@", "type": "MX", "answer": "alt1.aspmx.l.google.com", "ttl": 300, "priority": 5}

3. POST /api/manage/mydomain.com/dns
   {"host": "@", "type": "TXT", "answer": "v=spf1 include:_spf.google.com ~all", "ttl": 300}

4. "Email records configured for Google Workspace!"
```

---

## 错误处理

所有错误都会以JSON格式返回：

```json
{
  "error": "Description of what went wrong",
  "details": "Additional context if available"
}
```

| 状态码 | 含义 |
|--------|---------|
| `400` | 请求无效 |
| `401` | 未经授权（token缺失或无效） |
| `402` | 需要支付（使用x402支付方式） |
| `404` | 域名未找到 |
| `500` | 服务器错误 |

---

## 重要提示：

- **查询和购买域名时无需注册账号**  
- **两种支付方式：** 代理用户可使用x402（基于Base的支付平台，支持USDC）；人类用户可使用Stripe  
- **务必保存管理token**——它是管理域名的唯一凭证  
- **管理操作需要使用bearer认证**——在请求头中添加`Authorization: Bearer clwd_...`  
- **响应格式为JSON**——查询域名时请使用`?format=json`参数  

---

## 来源

ClawDaddy：https://clawdaddy.app  
文档：https://clawdaddy.app/llms.txt