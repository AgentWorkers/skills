---
name: mercury-payments
description: 通过 Mercury Bank API 支付发票。该 API 可用于通过 Mercury 发送自动清算house (ACH) 或电汇付款、创建收款人、查询交易记录以及管理支付流程。其功能包括：查找/创建收款人、执行付款（ACH 和国内电汇）、处理幂等性相关操作、格式化电汇用途信息，以及根据日期范围查询交易记录。
---
# Mercury Payments

通过 Mercury Bank API 支付发票。

## 前提条件
- 拥有具有写入权限的 Mercury API 令牌
- 请求头：`Authorization: Bearer <token>`
- 基本 URL：`https://api.mercury.com/api/v1`

## 账户查询
```bash
curl -s -H "Authorization: Bearer $TOKEN" "https://api.mercury.com/api/v1/accounts"
```
返回所有账户的信息，包括账户 ID、名称以及账户的最后四位数字。

## 支付流程

### 1. 获得明确批准
**未经明确批准，切勿付款。** 需提供以下信息：金额、收款人、发票编号、账户信息。

### 2. 检查收款人是否存在
```bash
curl -s -H "Authorization: Bearer $TOKEN" "https://api.mercury.com/api/v1/recipients" \
  | python3 -c "import sys,json; [print(r['name'],r['id']) for r in json.load(sys.stdin)]"
```

### 3. （如需）创建收款人账户
```bash
curl -s -X POST "https://api.mercury.com/api/v1/recipients" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vendor Name",
    "emails": ["vendor@example.com"],
    "defaultPaymentMethod": "ach",
    "electronicRoutingInfo": {
      "accountNumber": "...",
      "routingNumber": "...",
      "electronicAccountType": "businessChecking",
      "address": { "address1": "...", "city": "...", "region": "...", "postalCode": "...", "country": "US" }
    }
  }'
```

### 4. 发送付款

**ACH（自动清算 House）：**
```bash
curl -s -X POST "https://api.mercury.com/api/v1/account/{accountId}/transactions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "recipientId": "...",
    "amount": 500.00,
    "paymentMethod": "ach",
    "note": "INV-001 - Vendor - Jan 2025",
    "idempotencyKey": "vendor-inv001-jan2025"
  }'
```

**国内电汇：**
```bash
curl -s -X POST "https://api.mercury.com/api/v1/account/{accountId}/transactions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "recipientId": "...",
    "amount": 1000.00,
    "paymentMethod": "domesticWire",
    "purpose": {"simple": {"category": "vendor", "additionalInfo": "Invoice INV-001 Service Description"}},
    "note": "INV-001 - Vendor - Jan 2025",
    "idempotencyKey": "vendor-inv001-jan2025"
  }'
```

**电汇时必须提供付款用途。** 格式：`{"simple": {"category": "<类别>", "additionalInfo": "<备注>"}}`

支持的类别：`employee`（员工）、`landlord`（房东）、`vendor`（供应商）、`contractor`（承包商）、`subsidiary`（子公司）、`transferToMyExternalAccount`（转账至外部账户）、`familyMemberOrFriend`（家庭成员或朋友）、`forGoodsOrServices`（用于商品或服务）、`angelInvestment`（天使投资）、`savingsOrInvestments`（储蓄或投资）、`expenses`（开支）、`travel`（旅行）、`other`（其他）

### 5. 通知记账员和供应商
付款完成后，通过电子邮件通知记账员，并向供应商发送付款确认信息及发票副本。

## 查询交易记录
```bash
# Recent (~30 days default)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.mercury.com/api/v1/account/{accountId}/transactions?limit=500"

# Date range (required to go further back)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.mercury.com/api/v1/account/{accountId}/transactions?start=2025-01-01&end=2025-01-31&limit=500"
```
如果没有指定 `start`/`end` 参数，API 仅返回过去 30 天的交易记录。

## 重试机制
使用描述性键来确保操作的唯一性：`{vendor}-{invoice}-{period}`（例如：`acme-inv123-jan2025`）。这样可以避免重复付款。

## 支付检查清单
- [ ] 支付已获得明确批准
- [ ] 已下载发票 PDF 文件
- [ ] 收款人存在（或已创建）
- [ ] 付款金额、方式及备注正确
- [ ] 已通过电子邮件通知记账员并附上发票副本
- [ ] 已通过电子邮件通知供应商并附上发票副本