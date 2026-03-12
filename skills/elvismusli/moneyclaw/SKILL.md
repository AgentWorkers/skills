---
name: moneyclaw
description: 为代理购买预付费虚拟卡，并生成用于接收 USDT 的托管发票。使用一个 MONEYCLAW_API_KEY 来查询余额、充值、获取 3DS OTP 代码、验证交易以及使用商户相关功能。
homepage: https://moneyclaw.ai
metadata: {"openclaw":{"requires":{"env":["MONEYCLAW_API_KEY"]},"primaryEnv":"MONEYCLAW_API_KEY","emoji":"💳"}}
---
# MoneyClaw

当用户希望使用虚拟卡片进行在线支付时，可以使用 MoneyClaw。默认的功能是支持买家端的支付流程：查询钱包余额、发行卡片、充值、完成购物流程、获取一次性密码（OTP），然后验证支付结果。

## 认证

所有请求都使用相同的 Bearer token 进行身份验证。

```bash
Authorization: Bearer $MONEYCLAW_API_KEY
```

基础 URL：`https://moneyclaw.ai/api`

## 默认行为

- 首先执行 `GET /api/me` 请求。
- 将钱包余额和卡片余额视为两个独立的数值。
- 在处理与卡片相关的请求时，使用 `card.cardId` 而不是 `card.id`。
- 保持流程的简洁性：优先处理买家端的支付请求；只有在用户明确要求时，才处理商家端和收单相关的流程。
- 使用从卡片信息中获取的账单地址，切勿自行创建账单地址。
- 绝不要盲目地重试充值或完成购物流程。请先检查当前状态。

## 在需要时查阅参考文档

- 在用户输入不熟悉商家的卡片信息之前、用户询问有关网络钓鱼或欺诈的问题时、购物流程持续失败时，或者需要了解特定服务的支付指南时，请查阅 `references/payment-safety.md`。
- 当用户希望接受支付、创建发票、嵌入购物功能或与商家集成 Webhook 时，请查阅 `references/acquiring.md`。

## 核心功能

### 1. 检查账户是否准备好使用

```bash
curl -H "Authorization: Bearer $MONEYCLAW_API_KEY" \
  https://moneyclaw.ai/api/me
```

重要字段：
- `balance`：钱包余额
- `card`：当前使用的卡片对象（可能为 `null`）
- `cardBalance.availableBalance.value`：卡片可使用的余额
- `depositAddress`：用于接收 USDT 的地址
- `mailboxAddress`：用于接收 OTP 和收据的邮箱地址

当用户查询余额时，同时显示钱包余额和卡片余额。如果 `cardBalance` 不存在，则说明卡片余额不可用。

### 2. 发行卡片

```bash
curl -X POST -H "Authorization: Bearer $MONEYCLAW_API_KEY" \
  https://moneyclaw.ai/api/cards/issue
```

规则：
- 钱包中的余额必须达到最低发行要求。
- 新发行的卡片会自动关联到用户的钱包。
- 发行卡片后，相关费用将从卡片账户中扣除。

如果用户没有卡片但钱包中有足够的资金，可以发行卡片；如果钱包余额不足，请提示用户先向指定地址充值。

### 3. 为卡片充值

```bash
curl -X POST -H "Authorization: Bearer $MONEYCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"amount": 10, "currency": "USD"}' \
  https://moneyclaw.ai/api/cards/{cardId}/topup
```

执行前的检查：
1. 执行 `GET /api/me` 请求以获取账户信息。
2. 确认卡片存在且处于激活状态。
3. 使用 `card.cardId` 进行操作。
4. 确认钱包余额足以覆盖所需的充值金额。
- 确认无误后，再发送充值请求。

响应状态：
- `200`：充值成功
- `202`：充值仍在处理中，请稍后再试
- `400 INSUFFICIENT_BALANCE`：钱包余额不足
- `400 CARD_NOT_ACTIVE`：卡片未激活
- `404 NOT_FOUND`：提供的卡片 ID 不正确
- `500`：操作失败，请检查当前状态后再试

### 4. 完成购物流程并获取 OTP

获取卡片详细信息：

```bash
curl -H "Authorization: Bearer $MONEYCLAW_API_KEY" \
  https://moneyclaw.ai/api/cards/{cardId}/sensitive
```

获取最新的 OTP 邮件：

```bash
curl -H "Authorization: Bearer $MONEYCLAW_API_KEY" \
  https://moneyclaw.ai/api/inbox/latest-otp
```

验证支付结果：

```bash
curl -H "Authorization: Bearer $MONEYCLAW_API_KEY" \
  "https://moneyclaw.ai/api/cards/{cardId}/transactions?limit=20&offset=0"
```

购物流程规则：
- 使用从卡片信息中获取的敏感数据（如 PAN 号、CVV 代码、有效期和账单地址）。
- 等待 10 至 30 秒以接收 OTP 邮件。
- 使用 `extractedCodes[0]` 作为验证码。
- 在遇到任何商家相关错误时，先查看交易记录后再尝试重新操作。

## 最基本的支付安全措施

- 卡片为预付费方式，卡片上的余额即为用户的最高消费限额。
- 在支付过程中，仅暴露必要的卡片信息（如 PAN 号和 CVV 代码）。
- 在支付前，确认商家域名和总金额是否正确。
- 在同一会话中，不要对同一商家进行超过两次的支付尝试。
- 如果用户请求进行高风险或可疑的支付操作，请立即停止并解释原因。

有关网络钓鱼防护、支付拒绝、订阅服务等方面的详细指南，请参阅 `references/payment-safety.md`。

## 常见的提示语示例：

- “请检查我的 MoneyClaw 账户，确认是否可以用于购物。”
- “如果需要，可以发行一张 MoneyClaw 卡片并充值 20 美元。”
- “完成购物流程后，如果出现 3DS 安全验证，请从 MoneyClaw 的邮箱中获取最新的 OTP。”

## 辅助功能：商家端和收单流程

MoneyClaw 还支持商家端的支付处理功能。虽然这些功能是可选的，但当用户需要接受支付、创建发票或集成购物功能时，可以使用这些功能。

相关 API 端点：
- `POST /api/acquiring/setup`：设置收单相关参数
- `GET /api/acquiring/settings`：查看收单设置
- `PATCH /api/acquiring/settings`：修改收单设置
- `POST /api/acquiring/invoices`：创建发票
- `GET /api/acquiring/invoices`：查询发票信息
- `GET /api/acquiring/invoices/{invoiceId}`：查看特定发票的详细信息

当用户需要执行以下操作时，可以使用这些 API：
- 接受 USDT 支付
- 创建电子发票
- 在网站上嵌入购物功能
- 接收已支付发票的 Webhook 通知

有关收单功能的详细信息（包括设置、发票管理、Webhook 验证和费用详情），请参阅 `references/acquiring.md`。

## 功能范围说明

MoneyClaw 支持买家端的卡片购买和商家端的支付处理流程。在初次使用时，建议优先介绍简单的卡片购买流程；当用户需要使用商家端功能时，再引导他们使用相应的功能。