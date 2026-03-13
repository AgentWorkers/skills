---
name: moneyclaw
description: 启用 OpenClaw 代理，使其能够使用预付费钱包和虚拟卡进行真实的在线购物，获取 OTP/3DS 代码，并在用户自主控制下验证支付结果。
homepage: https://moneyclaw.ai
metadata: {"openclaw":{"requires":{"env":["MONEYCLAW_API_KEY"]},"primaryEnv":"MONEYCLAW_API_KEY","emoji":"💳"}}
---
# MoneyClaw

MoneyClaw 为 OpenClaw 代理提供了真正的支付功能，支持用户自定义的自主决策权、预先设定的风险限制、OTP（一次性密码）/3DS（三重安全验证）支持以及可审计的支付流程。

**主要使用场景：** OpenClaw 代理在买家端的在线购物。

**次要使用场景：** 在用户明确要求的情况下，支持发票处理、托管支付链接以及商户/收单流程。

## 认证

所有请求均使用相同的 Bearer Token 进行身份验证。

```bash
Authorization: Bearer $MONEYCLAW_API_KEY
```

**基础 URL：** `https://moneyclaw.ai/api`

## 信任模型

MoneyClaw 的设计旨在确保代理的支付行为得到用户的明确授权：

- 使用预付费余额来控制风险范围；
- 为 OTP 和 3DS 验证流程设置专用的收件箱；
- 提供可查询的钱包和卡片交易记录以供用户核查支付活动；
- 允许用户自行决定代理应具备的自主决策权限。

## 自主决策模型

MoneyClaw 可以在两种模式下使用：基于审批的模式或预先授权的模式。

- 在基于审批的模式下，代理在执行支付操作前需要先获得用户的授权；
- 在预先授权的模式下，代理可以在用户配置的支付范围、余额和权限范围内执行支付操作。

## 安全限制

- 仅允许使用用户明确请求或预先授权的支付流程；
- 仅使用用户自己 MoneyClaw 账户返回的钱包、卡片和账单数据；
- 遵守商户、发卡机构、卡片网络以及验证流程的相关规定（包括 OTP 和 3DS 验证）；
- 严禁伪造账单信息、持卡人数据、地址、姓名、电话号码或验证信息；
- 如果交易失败、存在可疑行为或出现矛盾信息，请停止操作并检查交易状态后再尝试；
- 默认情况下优先使用预付费、风险可控的支付方式；
- 仅在用户明确要求时使用发票处理、商户支付链接或托管支付链接。

## 默认行为

- 首先执行 `GET /api/me` 请求；
- 将钱包余额和卡片余额视为独立的数据源；
- 在处理卡片相关操作时使用 `card.cardId`（而非 `card.id`）；
- 默认情况下使用买家端的支付流程；仅在用户明确要求时使用商户或收单流程；
- 使用来自用户 MoneyClaw 账户的账单地址，切勿自行创建虚假地址；
- 绝不要盲目尝试充值或完成支付操作，必须先读取当前的交易状态。

## 需要时查阅参考文档

- 在处理不熟悉的商户相关操作时，或在用户询问有关网络钓鱼或欺诈的问题时，应查阅 `references/payment-safety.md`；
- 当用户需要接受支付、创建发票或集成支付功能时，应查阅 `references/acquiring.md`。

## 核心功能

### 1. 检查账户状态

```bash
curl -H "Authorization: Bearer $MONEYCLAW_API_KEY" \
  https://moneyclaw.ai/api/me
```

重要字段包括：
- `balance`：钱包余额
- `card`：当前使用的卡片对象（或 `null`）
- `cardBalance.availableBalance.value`：卡片可用的余额
- `depositAddress`：用于发送 USDT 的地址
- `mailboxAddress`：用于接收 OTP 和收据的收件箱地址

当用户查询余额时，同时显示钱包余额和卡片余额；如果 `cardBalance` 信息缺失，则说明卡片余额不可用。

### 2. 发行卡片

```bash
curl -X POST -H "Authorization: Bearer $MONEYCLAW_API_KEY" \
  https://moneyclaw.ai/api/cards/issue
```

规则如下：
- 钱包余额必须达到最低发行要求；
- 新发行的卡片会自动关联到用户的钱包；
- 发行费用将从卡片账户中扣除。

如果用户没有卡片但钱包中有足够的资金，系统会自动发行卡片；如果钱包余额不足，系统会提示用户先充值。

### 3. 为卡片充值

```bash
curl -X POST -H "Authorization: Bearer $MONEYCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"amount": 10, "currency": "USD"}' \
  https://moneyclaw.ai/api/cards/{cardId}/topup
```

执行操作前的检查步骤：
1. 首先执行 `GET /api/me` 请求；
2. 确认卡片存在且处于激活状态；
3. 使用 `card.cardId` 进行操作；
4. 确认钱包余额足以覆盖所需的充值金额；
- 确认无误后才能发送充值请求。

响应状态码说明：
- `200`：充值成功
- `202`：充值仍在处理中，请稍后再试
- `400 INSUFFICIENT_BALANCE`：钱包余额不足
- `400 CARD_NOT_ACTIVE`：卡片未处于激活状态
- `404 NOT_FOUND`：卡片 ID 错误
- `500`：操作失败，请检查错误原因后再试

### 4. 完成授权后的支付流程并获取 OTP

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

验证支付过程中的实际操作情况：

```bash
curl -H "Authorization: Bearer $MONEYCLAW_API_KEY" \
  "https://moneyclaw.ai/api/cards/{cardId}/transactions?limit=20&offset=0"
```

支付规则：
- 使用从卡片响应中获取的敏感信息（如 PAN 号、CVV 代码、有效期和账单地址）；
- 等待 10 至 30 秒以接收 OTP 邮件；
- 使用 `extractedCodes[0]` 作为验证码；
- 在遇到任何商户错误时，先查看交易记录后再尝试支付。

## 支付执行规则

- 卡片采用预付费方式，实际可使用的支付金额受限于卡片余额；
- 在支付前确认商户域名和总金额是否正确；
- 未经用户确认或预先授权的情况下，同一商户的支付请求不得超过两次；
- 如果用户请求进行高风险或可疑的支付操作，必须立即停止并解释原因。

有关更详细的安全性、验证、订阅及重试指南，请参阅 `references/payment-safety.md`。

## 建议的提示语示例：

- “请检查我的 MoneyClaw 账户，确认是否可以用于购物。”
- “如果需要，可以为您发行一张 MoneyClaw 卡片并充值 20 美元。请在支付前确认，除非我明确表示此次支付是预先授权的。”
- “完成此次授权后的支付操作；如果出现 3DS 验证，请从 MoneyClaw 的收件箱中获取最新的 OTP 并验证最终的交易结果。”

## 辅助功能：商户和收单流程

MoneyClaw 还支持商户端的支付处理功能。虽然这些功能为次要选项，但在用户需要接受支付、创建发票或集成支付功能时可以使用。

相关 API 端点：
- `POST /api/acquiring/setup`：设置收单相关参数
- `GET /api/acquiring/settings`：查看收单设置
- `PATCH /api/acquiring/settings`：修改收单设置
- `POST /api/acquiring/invoices`：创建发票
- `GET /api/acquiring/invoices`：查询发票信息
- `GET /api/acquiring/invoices/{invoiceId}`：获取特定发票的详细信息

当用户需要执行以下操作时，请使用这些接口：
- 接受 USDT 支付
- 创建托管发票
- 在网站上集成支付功能
- 接收已支付发票的 Webhook 通知

有关收单功能的详细信息（包括设置、发票生命周期、Webhook 验证和费用详情），请参阅 `references/acquiring.md`。

## 功能范围说明

MoneyClaw 支持买家端的卡片购买和商户端的支付处理流程。初次使用时建议使用简单的卡片购买流程；当用户需要商户相关功能时，再切换到收单模式。