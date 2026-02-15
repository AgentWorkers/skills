---
name: moltpho
description: 通过 Moltpho 在 Amazon 上自主购物：搜索产品、管理信用额度，并使用 mUSD 在 Base 主网上购买商品。
metadata: {"requires": {"http": true, "browser": true}}
---

# Moltpho 购物技能

使用基于 Base 主网上的 mUSD 代币，在 Amazon 上自主购物。

## 概述

Moltpho 是一个无头购物商城，它允许 AI 代理通过由 mUSD（Base 主网上的 ERC-20 代币）支持的信用系统来发现和购买 Amazon 产品。该技能支持以下功能：

- 代理注册和凭证管理
- 产品搜索和发现
- 自主且主动的购买行为
- 信用余额监控
- x402 支付协议的集成

## 启动流程

首次调用该技能时，必须检查是否存在有效的凭证，如需要则进行注册。

### 凭证位置

| 平台 | 路径 |
|----------|------|
| Linux/macOS | `~/.config/moltpho/credentials.json` |
| Windows | `%APPDATA%\moltpho\credentials.json` |
| 可覆盖 | `MOLTPHO_CREDENTIALS_PATH` 环境变量 |

### 注册流程

1. 在指定路径下检查凭证文件。
2. 如果凭证文件缺失，调用 `POST /v1/agents/register`，并提供以下信息：
   - `openclaw_instance_id`（如果有的话）
   - `agent_display_name`
   - `agent_description`
   - 注册时不需要填写 shipping profile
3. 以 `chmod 600` 权限保存凭证文件。
4. 自动打开浏览器，并显示提示：“正在您的浏览器中打开门户以完成设置...”。
5. 注册过程中不需要填写 shipping profile——在所有者通过门户添加 shipping profile 之前，订单将无法完成。

### 凭证文件格式

```json
{
  "agent_id": "uuid",
  "api_key_id": "moltpho_key_...",
  "api_key_secret": "moltpho_secret_...",
  "api_base_url": "https://api.moltpho.com",
  "wallet_address": "0xabc123..."
}
```

## 核心功能

### bootstrap()

初始化代理凭证并打开门户以供所有者完成设置。

```
1. Check if credentials file exists at platform-specific path
2. If exists and valid: load credentials, verify with GET /v1/agents/me
3. If missing or invalid:
   a. Call POST /v1/agents/register (no auth required)
   b. Receive: agent_id, api_key_id, api_key_secret, claim_url, wallet_address
   c. Write credentials file with chmod 600
   d. Display: "Opening portal in your browser to complete setup..."
   e. Open browser to claim_url (valid for 24 hours)
4. Return agent status (UNCLAIMED, CLAIMED, DEGRADED, SUSPENDED)
```

### collect_shipping_profile()

（可选）从所有者处收集配送信息。

```
Note: This is OPTIONAL. Owners can configure shipping via the portal instead.
      Orders will fail with INVALID_SHIPPING_PROFILE until a profile exists.

If collecting in conversation:
1. Request full name
2. Request address (street, city, state, ZIP)
3. Request email
4. Request phone
5. Validate: US addresses only (international not supported in v1)
6. Call POST /v1/shipping_profiles (upsert_shipping_profile)
7. Confirm profile saved

The POST endpoint upserts the default profile:
- If no profile exists, creates one
- If a profile exists, updates it
```

### update_shipping_profile()

更新代理的配送地址。

```
Parameters:
- full_name: Recipient full name
- address1: Street address
- address2: Apt/suite (optional)
- city: City
- state: State (2-letter code)
- postal_code: ZIP code
- email: Contact email
- phone: Contact phone

Process:
1. Validate all required fields
2. Validate US address (only US supported in v1)
3. Call POST /v1/shipping_profiles (upserts default profile)
4. Return updated profile

Use cases:
- "Update my shipping address"
- "Change my delivery address to..."
- First-time setup during bootstrap
```

### catalog_search(query, constraints)

通过 Moltpho 在 Amazon 上搜索产品。

```
Parameters:
- query: Search terms (string)
- constraints: Optional filters
  - max_price: Maximum price in USD
  - category: Product category keyword
  - min_rating: Minimum star rating (1-5)

Process:
1. Call GET /v1/catalog/search?query={query}&limit=20
2. Apply local constraints if provided
3. Present results with:
   - Product title and brand
   - Moltpho price (final price, includes 10% markup)
   - Availability status
   - Rating if available
4. If cache expired, results include "prices may have changed" warning

Rate limit: 60 requests/minute
```

### purchase(item, qty)

通过 x402 支付流程执行购买操作。

```
Parameters:
- item: ASIN or product identifier
- qty: Quantity (default 1)

Process:
1. BUDGET CHECK: Call GET /v1/balance to verify available credit
   - available_credit = balance - active_reservations
   - Check against per_order_cap if set
   - Check against daily_cap if set

2. CREATE QUOTE: Call POST /v1/quotes
   - Include: asin, quantity, shipping_profile_id
   - Returns: quote_id, total_due_usd, expires_at (10 min TTL)
   - Creates soft reservation against balance
   - May fail with INVALID_SHIPPING_PROFILE if no profile set

3. INITIATE ORDER: Call POST /v1/orders with quote_id
   - First call returns 402 Payment Required with PAYMENT-REQUIRED header

4. SIGN PAYMENT: Call POST /v1/wallets/x402/sign
   - Include: payment_required blob, idempotency_key
   - Returns: payment_signature for x402 header

5. COMPLETE ORDER: Retry POST /v1/orders with PAYMENT-SIGNATURE header
   - On success: returns order_id, status (PAID/PLACED)
   - Soft reservation converted to actual spend

Auto-retry on quote expiry:
- If quote expires during flow, automatically retry up to 3 times
- Only retry if new price is within 5% of original quote
- Fail after 3 retries or if price changed >5%

Rate limits:
- Quotes: 20/minute
- Orders: 5/minute
- Signing: 10/minute
```

### proactive_monitoring()

监控对话中的购买需求信号，并在适当的时候采取行动。

```
This function runs passively during conversation to detect purchase opportunities.

NEED SIGNALS (explicit):
- "I need", "we're out of", "buy", "order", "replace"
- "running low on", "almost out of"
- Direct product mentions with urgency

NEED SIGNALS (implicit):
- Repeated complaints about missing items
- Critical item shortages mentioned
- Context suggesting immediate need

CONFIDENCE SCORING:
- 1.0: Explicit purchase request ("buy me X")
- 0.8: Strong implied need ("we're completely out of toilet paper")
- 0.5: Weak implied convenience (do NOT buy)
- 0.0: Unknown/unclear

BUDGET SIGNAL HANDLING:
- Phrases like "money is tight", "on a budget", "can't afford"
- Reduce confidence by 0.3-0.5
- Proceed cautiously if still above threshold

PROACTIVE PURCHASE ALLOWED IF ALL TRUE:
- Owner has enabled proactive purchasing (default ON)
- Confidence >= 0.8 (threshold)
- Item matches low-risk categories:
  - Household essentials
  - Office supplies
  - Cables/adapters
  - Basic kitchen items
  - Toiletries
- Price <= min(per_order_cap, $75)
- Item keywords not in denied categories
- Item not in system blocklist
- Shipping profile exists

LOGGING:
Every purchase logs:
- "why we bought" (decision reason)
- Signals detected
- Confidence tier (HIGH/MEDIUM/LOW)
- Budget impact
```

### budget_check()

在任何购买操作之前，验证是否有足够的信用。

```
Process:
1. Call GET /v1/balance
2. Response includes:
   - available_credit_cents: Spendable amount
   - staged_refunds: Pending refunds (shown with asterisk)
   - target_limit: Owner's configured credit limit
3. Compare against:
   - Quote total
   - per_order_cap (if set)
   - daily_cap (if set, track daily spending)
4. Return: can_purchase (bool), available_amount, reason_if_blocked
```

### create_support_ticket(type, description, order_id)

创建支持工单，用于处理退货、包裹丢失等问题。

```
Parameters:
- type: Ticket type - RETURN, LOST_PACKAGE, or OTHER
- description: Detailed description of the issue (1-2000 chars)
- order_id: Order ID (required for RETURN and LOST_PACKAGE)

Process:
1. Validate ticket type and description
2. If RETURN or LOST_PACKAGE, verify order_id is provided
3. Call POST /v1/support_tickets with { type, description, order_id }
4. Return ticket ID and status

Use cases:
- "I want to return this item" → type=RETURN, link to order
- "My package never arrived" → type=LOST_PACKAGE, link to order
- "I have a question about billing" → type=OTHER, no order needed

Note: Returns and lost packages require a support ticket.
      Automated refunds only happen for order cancellations.
```

### list_support_tickets()

列出代理的所有支持工单。

```
Process:
1. Call GET /v1/support_tickets
2. Display tickets with: type, status, order link, creation date
3. Status meanings:
   - OPEN: Submitted, awaiting support review
   - IN_PROGRESS: Being handled
   - WAITING_CUSTOMER: Support needs more info from you
   - RESOLVED: Issue resolved
   - CLOSED: Ticket closed
```

### logout()

删除本地凭证（代理信息在服务器端保留）。

```
Process:
1. Delete credentials file at platform-specific path
2. Display: "Credentials removed. Agent still exists on Moltpho servers."
3. To fully delete agent, owner must use portal

Note: This only removes LOCAL credentials. The agent account, wallet, and
      purchase history remain on Moltpho servers until owner deletes via portal.
```

## 浏览器门户的使用

该技能使用浏览器来执行需要所有者参与的操作。

### 何时打开浏览器

| 操作 | 方法 |
|--------|--------|
| 完成设置（领取链接） | 自动打开浏览器并显示提示 |
| 添加/管理支付卡 | 将所有者引导至门户 |
| 设置信用限额 | 将所有者引导至门户 |
| 配置配送 profile | 将所有者引导至门户 |
| 查看订单历史 | 将所有者引导至门户 |

### 浏览器使用指南

- 始终显示提示：“正在您的浏览器中打开门户...”。
- 绝不在聊天中请求卡号、密码或敏感凭证。
- 门户通过 Stripe Elements 处理所有 PCI 敏感操作。
- 所有者通过魔法链接（基于电子邮件）进行身份验证。

## API 认证

所有 API 请求（注册除外）都需要认证。

### 请求头

```
Authorization: Bearer <api_key_secret>
```

或者更推荐的方式：
```
X-Moltpho-Key-Id: <api_key_id>
X-Moltpho-Signature: <HMAC signature>
```

### 重试机制

对于会改变状态的请求，务必包含以下头部信息：
```
Idempotency-Key: <unique-key>
```

以下操作需要包含该头部信息：
- `POST /v1/quotes`
- `POST /v1/orders`
- `POST /v1/wallets/x402/sign`

## 错误处理

### 常见错误

| 代码 | 错误信息 | 处理方式 |
|------|-------|--------|
| 401 | 未经授权 | 重新启动流程或检查凭证 |
| 402 | 需要支付 | 使用 x402 签名重新尝试 |
| 409 | 价格变更 | 如果价格上涨超过 2%，重新报价 |
| 409 | 信用不足 | 通知用户并建议补充信用 |
| 409 | 报价过期 | 自动重试（最多 3 次）或重新报价 |
| 422 | 配送信息无效 | 提示所有者通过门户添加配送信息 |
| 422 | 代理被暂停 | 通知所有者并引导其通过门户处理 |
| 429 | 每次重试有次数限制 | 根据 `Retry-After` 头部信息等待 |
| 503 | 令牌暂停 | 系统暂停，请等待管理员处理 |

### 报价过期后的自动重试

当 x402 流程中的报价过期时：
1. 获取同一商品的新报价。
2. 比较新报价与原报价。
3. 如果价格变化在 5% 以内：继续使用新报价。
4. 如果价格变化超过 5%：以 “价格变更” 为由失败。
5. 最多尝试 3 次。

## 限制和约束

### 系统限制

| 限制 | 值 |
|-------|-------|
| 单件商品最高价格 | 10,000 美元 |
| 报价有效期 | 10 分钟 |
| 价格容忍度 | 允许的价格上涨幅度为 2% |
| 自动重试的价格容忍度 | 5% |
| 每个代理的最大同时报价数量 | 5 个 |
| 主动购买的限额 | 每单最低限额为 75 美元 |

### 速率限制

| 端点 | 限制 |
|----------|-------|
| 商品搜索 | 每分钟 60 次 |
| 报价 | 每分钟 20 次 |
| 订单 | 每分钟 5 次 |
| 签名操作 | 每分钟 10 次 |

### 被禁止购买的商品（系统强制）

无论所有者设置如何，以下类别的商品均无法购买：
- 武器、枪支、弹药
- 受控物质、处方药
- 烟草、尼古丁产品
- 酒精
- 成人内容
- 危险材料

## 支付系统

### 信用模型

- 所有者设置目标信用限额（以美元计）。
- 每周自动充值将信用恢复到目标限额。
- 信用由 Base 主网上的 mUSD 代币支持。
- 价格比 Amazon 价格高出 10%（包含费用和手续费）。

### x402 支付流程

1. 调用 `POST /v1/orders`，响应中包含 `PAYMENT-REQUIRED` 头部信息。
2. 调用 `POST /v1/wallets/x402/sign`，并上传支付信息。
3. 钱包服务处理 EIP-3009 授权。
4. 重新发送订单，请求中包含 `PAYMENT-SIGNATURE` 头部信息。
5. 由 Base 主网上的系统完成结算。
6. 订单进入履行阶段。

### 退款

| 情况 | 退款方式 |
|----------|---------------|
| 采购失败 | 从 mUSD 余额中自动退款 |
| 订单取消（在 5 分钟内） | 从 mUSD 余额中自动退款 |
| 所有者降低信用限额 | 通过 Stripe 从卡中退款 |
| 包裹丢失/退货 | 需要创建支持工单（使用 `create_support_ticket`） |

## 代理状态

| 状态 | 含义 | 是否可以下单？ |
|-------|---------|------------|
| UNCLAIMED | 已注册，等待所有者领取 | 不能 |
| CLAIMED | 所有者已领取，功能正常 | 可以 |
| DEGRADED | 支付方式失败，使用剩余余额 | 可以（如果有余额） |
| SUSPENDED | 被管理员暂停，需要手动解决 | 不能 |

## 最佳实践

### 在进行任何购买之前

1. 调用 `budget_check()` 以验证可用信用。
2. 确认存在 shipping profile。
3. 检查商品是否在禁止购买的类别列表中。
4. 核实主动购买所需的信用阈值。

### 对话指南

- 在执行购买操作前，始终确认总价。
- 购买后报告订单状态和剩余信用。
- 如果检测到预算限制，告知用户相关限制。
- 绝不要强迫用户补充信用。

### 错误恢复

- 如果信用不足，建议通过门户补充信用。
- 如果配送信息无效，收集配送信息并调用 `upsert_shipping_profile()`，或引导用户通过门户处理。
- 如果代理被暂停，告知所有者需要通过门户解决问题。

## 快速参考

### 必需的 API 端点

| 端点 | 功能 |
|----------|---------|
| POST /v1/agents/register | 新代理注册 |
| GET /v1/agents/me | 当前代理状态 |
| GET /v1/balance | 可用信用 |
| GET /v1/catalog/search | 搜索产品 |
| POST /v1/quotes | 创建购买报价 |
| POST /v1/orders | 下单（使用 x402 支付） |
| POST /v1/wallets/x402/sign | 签署支付信息 |
| GET /v1/shipping_profiles | 查看配送信息 |
| POST /v1/shipping_profiles | 创建/更新配送信息 |
| POST /v1/support_tickets | 创建支持工单 |
| GET /v1/support_tickets | 查看支持工单列表 |

### 门户 URL

```
https://portal.moltpho.com
```

所有者操作：
- /claim/{token} - 领取代理所有权 |
- /agents - 管理代理 |
- /cards - 支付方式 |
- /orders - 订单历史 |
- /settings - 信用限额和偏好设置 |