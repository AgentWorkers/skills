# Mercury Payments 功能

## 概述
通过 Mercury 银行 API 支付发票，通知 Zeni（记账员）和供应商，并始终附上发票的 PDF 文件。

## 先决条件
- Mercury API 令牌（写入权限）：`$MERCURY_API_TOKEN` 或 `pass show <vault-path>`
- 身份验证：`Authorization: Bearer <token>`（基本身份验证也可使用：`token:` base64）
- 基本 URL：`https://api.mercury.com/api/v1`

## 账户
动态获取账户 ID（不要硬编码特定组织的 ID）：

```bash
curl -s -H "Authorization: Bearer $TOKEN" "https://api.mercury.com/api/v1/accounts"
```

默认支付账户应在支付时确认。

## 已知收款人
将收款人 ID 保存在您自己的安全记录中，或在运行时根据收款人名称进行查询。

## 支付流程

### 1. 获取明确授权
**未经授权操作员的明确批准，切勿汇款。** 需提供以下信息：金额、收款人、发票编号、账户信息。

### 2. 下载发票 PDF
找到发票对应的电子邮件地址，并将附件下载到 `/tmp/` 目录中。

### 3. 检查收款人是否存在
```bash
curl -s -H "Authorization: Bearer $TOKEN" "https://api.mercury.com/api/v1/recipients" | python3 -c "..."
```

### 4. （如需）创建收款人账户
```bash
curl -s -X POST "https://api.mercury.com/api/v1/recipients" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "...",
    "emails": ["..."],
    "defaultPaymentMethod": "ach",
    "electronicRoutingInfo": {
      "accountNumber": "...",
      "routingNumber": "...",
      "electronicAccountType": "businessChecking",
      "address": { "address1": "...", "city": "...", "region": "...", "postalCode": "...", "country": "US" }
    },
    "defaultAddress": { ... }
  }'
```

### 5. 发送支付
**ACH 支付：**
```bash
curl -s -X POST "https://api.mercury.com/api/v1/account/{accountId}/transactions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "recipientId": "...",
    "amount": 533.13,
    "paymentMethod": "ach",
    "note": "INV123 - Vendor - Period",
    "idempotencyKey": "unique-key-here"
  }'
```

**国内电汇支付：**
```bash
curl -s -X POST "https://api.mercury.com/api/v1/account/{accountId}/transactions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "recipientId": "...",
    "amount": 1080.00,
    "paymentMethod": "domesticWire",
    "purpose": {"simple": {"category": "vendor", "additionalInfo": "Invoice TRC37332 TRACE Data"}},
    "note": "INV-001 - Vendor - Jan 2026",
    "idempotencyKey": "unique-key-here"
  }'
```

**电汇时必须填写 “目的” 字段。** 格式：`{"simple": {"category": "<cat>", "additionalInfo": "<desc>"}}`
可选类别：`employee`（员工）、`landlord`（房东）、`vendor`（供应商）、`contractor`（承包商）、`subsidiary`（子公司）、`transferToMyExternalAccount`（转账至我的外部账户）、`familyMemberOrFriend`（家庭成员或朋友）、`forGoodsOrServices`（用于商品或服务）、`angelInvestment`（天使投资）、`savingsOrInvestments`（储蓄或投资）、`expenses`（费用）、`travel`（旅行）、`other`（其他）

### 6. 必须发送邮件给记账员
将邮件发送到记账员的收件箱（例如：`bookkeeping@example.com`），内容包括：
- 主题：`<供应商> 发票 <编号> — 已支付`
- 正文：支付金额、支付方式、预计交货日期
- **附上发票 PDF**

### 7. 必须发送邮件给供应商
如果可能，请在现有邮件线程中回复供应商，内容包括：
- 支付确认信息及金额
- **附上发票 PDF**
- 预计交货日期

## 内部转账（在 Mercury 账户之间进行）

```bash
curl -s -X POST "https://api.mercury.com/api/v1/transfer" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sourceAccountId": "YOUR_SOURCE_ACCOUNT_ID",
    "destinationAccountId": "YOUR_DESTINATION_ACCOUNT_ID",
    "amount": 465.00,
    "idempotencyKey": "unique-key-here"
  }'
```

必填字段：`sourceAccountId`（源账户 ID）、`destinationAccountId`（目标账户 ID）、`amount`（金额）、`idempotencyKey`（幂等性键）。
转账会立即完成。响应中包含 `creditTransaction`（贷方交易）和 `debitTransaction`（借方交易）信息。

## 查询交易记录
```bash
# Recent (default ~30 days)
curl -s -H "Authorization: Bearer $TOKEN" "https://api.mercury.com/api/v1/account/{id}/transactions?limit=500"

# Date range (goes further back)
curl -s -H "Authorization: Bearer $TOKEN" "https://api.mercury.com/api/v1/account/{id}/transactions?start=2025-12-01&end=2026-01-18&limit=500"
```
注意：如果没有指定日期参数，API 只能返回最近 30 天的交易记录。可以使用 `start`/`end` 参数查询更早的交易。

## 幂等性键
使用描述性键来标识交易：`{vendor}-{invoice}-{period}`（例如：`finra-trc37332-nov2025`）

## 检查清单
- [ ] 已获得授权操作员的明确批准
- [ ] 已下载发票 PDF
- [ ] 收款人存在（或已创建）
- [ ] 支付金额、支付方式及备注正确
- [ ] 已通过邮件将发票发送给 Zeni
- [ ] 已通过邮件将发票发送给供应商
- [ ] 支付记录已保存在每日日志文件中