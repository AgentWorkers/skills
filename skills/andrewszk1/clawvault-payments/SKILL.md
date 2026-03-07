---
name: ClawVault Payments
description: 用于处理资金的人工智能代理的安全中间件。该中间件支持非托管式加密货币钱包以及具有消费限额、白名单和人工审批功能的虚拟Visa卡。
homepage: https://clawvault.cc
source: https://github.com/andrewszk/clawvault-mcp-server
metadata:
  openclaw:
    emoji: "🦞"
    primaryEnv: CLAWVAULT_API_KEY
    requires:
      env:
        - name: CLAWVAULT_API_KEY
          description: "Your ClawVault API key (format: cv_live_xxxxx). Get one at https://clawvault.cc/agents"
          required: true
---
# ClawVault 代理技能

您可以使用 ClawVault，这是一个专为 AI 代理设计的安全中间件。ClawVault 保护两种支出渠道：

1. **加密货币支付** – 在 Base 和 Solana 区块链上进行 USDC 转账；
2. **代理卡** – 可用于全球任何商家的虚拟 Visa 卡（适用于 SaaS、API、云服务等）。

这两种渠道都使用相同的规则引擎。每笔交易都会根据用户定义的规则进行验证：符合规则的交易会自动批准；不符合规则的交易需要通过 Telegram 或仪表板进行人工批准。

## 安全模型

- **非托管式**：您的私钥永远不会离开您的钱包；
- **规则驱动**：支出限额、白名单以及时间窗口都在链上得到强制执行；
- **人工审核**：任何不符合规则的交易都需要明确的人工批准；
- **审计追踪**：所有交易都会被记录并在仪表板上显示。

## API 基本 URL
```
https://api.clawvault.cc
```

## 认证

所有请求都必须在 `Authorization` 头部包含您的 API 密钥：
```
Authorization: Bearer ${CLAWVAULT_API_KEY}
```

您可以在以下链接获取 API 密钥：https://clawvault.cc/agents

---

# 加密货币支付（链上）

## 1. 请求进行加密货币支付

当您需要向区块链地址发送 USDC 时：

```http
POST /v1/payments
Content-Type: application/json

{
  "amount": "50.00",
  "token": "USDC",
  "recipient": "0x1234567890abcdef1234567890abcdef12345678",
  "chain": "base",
  "reason": "Payment for services rendered",
  "skill": "transfer"
}
```

### 响应（成功）
```json
{
  "success": true,
  "data": {
    "id": "pi_abc123",
    "status": "pending",
    "expiresAt": "2026-02-27T12:00:00Z"
  }
}
```

### 可能的状态：
- `auto_approved` – 交易立即执行（符合规则）；
- `pending` – 正在等待通过 Telegram 或仪表板进行人工批准；
- `denied` – 交易被拒绝；
- `expired` – 批准窗口已关闭（5 分钟后）。

---

## 2. 支付前检查（预测试）

在支付之前，请先检查交易是否可以自动批准或需要手动批准：

```http
POST /v1/rules/check
Content-Type: application/json

{
  "amount": "50.00",
  "token": "USDC",
  "recipient": "0x1234...",
  "chain": "base"
}
```

### 响应
```json
{
  "success": true,
  "data": {
    "allowed": true,
    "autoApprove": false,
    "reason": "Manual mode",
    "remainingBudget": { "daily": 450.00 },
    "remainingTx": { "daily": 46 }
  }
}
```

如果 `autoApprove: false`，则告知用户该交易需要他们的批准。

---

## 3. 查看钱包余额

查看您的钱包余额和当前的使用限额：

```http
GET /v1/vault
```

### 响应
```json
{
  "success": true,
  "data": {
    "chain": "base",
    "balances": [{ "token": "USDC", "balance": "150.00" }],
    "rules": {
      "mode": "manual",
      "perTxLimit": 500,
      "dailyTxMax": 20
    }
  }
}
```

---

# 代理卡（Visa 卡）

当您需要支付以下费用时，可以使用代理卡：
- SaaS 订阅服务（如 Vercel、Netlify 等）；
- API 服务（如 OpenAI、Anthropic、Twilio 等）；
- 云计算服务（如 AWS、GCP、Azure）；
- 任何接受 Visa 的商家。

## 4. 请求购买代理卡

```http
POST /v1/card/purchase
Content-Type: application/json

{
  "amount": 20.00,
  "currency": "USD",
  "merchant": "OpenAI API",
  "merchant_category": "api_services",
  "reason": "GPT-4 API credits for research task"
}
```

### 响应（批准）
```json
{
  "success": true,
  "data": {
    "id": "card_txn_abc123",
    "status": "approved",
    "card_credentials": {
      "number": "4242837419283847",
      "exp_month": 3,
      "exp_year": 2028,
      "cvc": "847"
    },
    "valid_for_seconds": 300
  }
}
```

### 响应（需要批准）
```json
{
  "success": true,
  "data": {
    "id": "card_txn_abc123",
    "status": "pending_approval",
    "reason": "Amount exceeds auto-approve threshold"
  }
}
```

**重要提示**：代理卡的凭证是临时且一次性的。请在商家结账时立即使用它们。切勿记录或存储卡凭证。

---

## 5. 查看卡余额

```http
GET /v1/card/balance
```

### 响应
```json
{
  "success": true,
  "data": {
    "balance": 450.00,
    "currency": "USD",
    "spent_today": 50.00,
    "spent_this_month": 350.00,
    "daily_limit": 500.00,
    "monthly_limit": 5000.00
  }
}
```

---

## 6. 检查卡的使用规则

在购买之前，请先检查是否允许进行该交易：

```http
POST /v1/card/check
Content-Type: application/json

{
  "amount": 20.00,
  "merchant_category": "api_services"
}
```

### 响应
```json
{
  "success": true,
  "data": {
    "allowed": true,
    "autoApprove": true,
    "reason": "Within limits, allowed category"
  }
}
```

---

# 常用端点

## 7. 查看支付/购买状态

```http
GET /v1/payments/{payment_id}
GET /v1/card/transactions/{transaction_id}
```

## 8. 列出最近的交易记录

```http
GET /v1/transactions?limit=10
GET /v1/card/transactions?limit=10
```

---

# 选择支付方式：加密货币还是代理卡

使用以下逻辑来决定使用哪种支付方式：

| 场景 | 使用方式 |
|----------|-----|
| 向区块链地址支付（0x...） | 加密货币（`/v1/payments`） |
| 支付 SaaS 订阅费用 | 代理卡（`/v1/card/purchase`） |
| 支付 API 服务费用 | 代理卡（`/v1/card/purchase`） |
| 支付云服务费用 | 代理卡（`/v1/card/purchase`） |
| 支付任何在线服务费用 | 代理卡（`/v1/card/purchase`） |
| 向他人的加密货币钱包转账 | 加密货币（`/v1/payments`） |
| DeFi、质押、代币交换 | 加密货币（`/v1/payments`） |

**经验法则**：如果是向区块链地址支付，使用加密货币；如果是向公司或服务支付，使用代理卡。

---

# 人工审批流程

当交易需要审批时：

1. 通过 Telegram 机器人或 ClawVault 仪表板通知用户；
2. 用户查看交易详情（金额、收款人、原因）；
3. 用户通过点击即可批准或拒绝；
4. 如果获得批准，交易将执行；如果被拒绝，交易将被取消；
5. 如果 5 分钟内没有操作，审批将自动失效。

**务必在需要审批时通知用户**：“此交易需要您的批准。请查看您的 Telegram 或 ClawVault 仪表板。”

---

# 常见场景

### 场景：用户请求支付 OpenAI API 服务费用
1. 调用 `/v1/card/check` 以确认是否允许；
2. 如果允许，调用 `/v1/card/purchase` 并设置商家为 “OpenAI API”；
3. 如果状态显示 “approved”，请立即使用代理卡进行支付；
4. 如果状态显示 “pending_approval”，请告知用户：“此购买需要您的批准。请查看 Telegram 或 ClawVault 仪表板。”

### 场景：用户请求向某个地址发送 USDC
1. 调用 `/v1/rules/check` 以确认交易是否可以自动批准；
2. 使用收款人地址调用 `/v1/payments`；
3. 如果状态显示 “pending”，请告知用户通过 Telegram 进行批准。

### 场景：购买代理卡被拒绝
告知用户：“购买请求被拒绝。原因：{reason}。请查看 ClawVault 仪表板以获取详细信息。”

### 场景：卡余额不足
告知用户：“卡余额不足。当前余额：${balance}。请先充值。”

---

# 错误处理

### 常见错误
| 代码 | 含义 | 处理方式 |
|------|---------|--------|
| `INVALID_KEY` | API 密钥无效 | 请检查您的 API 密钥 |
| `TIER_LIMIT_EXCEEDED` | 已达到月度使用限额 | 用户需要升级账户 |
| `INSUFFICIENT_BALANCE` | 资金不足 | 用户需要充值（使用加密货币）或为卡充值 |
| `RULE_VIOLATION` | 交易超出允许的参数范围 | 请查看 `reason` 字段 |
| `CARD_FROZEN` | 卡被冻结 | 用户需要在仪表板上解冻卡 |
| `MERCHANT_BLOCKED` | 该商家不允许使用代理卡 | 无法从该商家购买 |
| `CARD_NOT_ACTIVE` | 代理卡未激活 | 用户需要申请代理卡 |

### 错误响应格式
```json
{
  "success": false,
  "error": {
    "code": "RULE_VIOLATION",
    "message": "Exceeds per-transaction limit of $100"
  }
}
```

---

# 安全最佳实践

1. **切勿记录卡凭证** – 卡号和 CVC 码属于敏感信息；
2. **始终先进行验证** – 在进行交易前请使用 `/v1/rules/check` 或 `/v1/card/check`；
3. **向用户说明情况** – 如果需要审批，请告知他们在哪里进行审批；
4. **处理待审批的交易** – 不要假设交易会立即完成；
5. **立即使用卡凭证** – 卡凭证在 5 分钟后失效；
6. **提供交易链接** – 对于加密货币交易，提供链接 `https://basescan.org/tx/{txHash}`。

---

# 帮助支持

- 仪表板：https://clawvault.cc
- 文档：https://clawvault.cc/docs
- API 状态：https://api.clawvault.cc/health
- 源代码：https://github.com/andrewszk/clawvault-mcp-server