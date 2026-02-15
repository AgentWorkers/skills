---
name: telnyx-account-javascript
description: >-
  Manage account balance, payments, invoices, webhooks, and view audit logs and
  detail records. This skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: account
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户 - JavaScript

## 安装

```bash
npm install telnyx
```

## 设置

```javascript
import Telnyx from 'telnyx';

const client = new Telnyx({
  apiKey: process.env['TELNYX_API_KEY'], // This is the default and can be omitted
});
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出审计日志

检索审计日志条目的列表。

`GET /audit_events`

```javascript
// Automatically fetches more pages as needed.
for await (const auditEventListResponse of client.auditEvents.list()) {
  console.log(auditEventListResponse.id);
}
```

## 获取用户余额详情

`GET /balance`

```javascript
const balance = await client.balance.retrieve();

console.log(balance.data);
```

## 搜索详细记录

在 Telnyx 平台上搜索任何详细记录。

`GET /detail_records`

```javascript
// Automatically fetches more pages as needed.
for await (const detailRecordListResponse of client.detailRecords.list()) {
  console.log(detailRecordListResponse);
}
```

## 列出发票

检索分页显示的发票列表。

`GET /invoices`

```javascript
// Automatically fetches more pages as needed.
for await (const invoiceListResponse of client.invoices.list()) {
  console.log(invoiceListResponse.file_id);
}
```

## 根据 ID 获取发票

根据唯一的标识符检索单张发票。

`GET /invoices/{id}`

```javascript
const invoice = await client.invoices.retrieve('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(invoice.data);
```

## 列出自动充值偏好设置

返回支付自动充值偏好设置。

`GET /payments/auto_recharge_prefs`

```javascript
const autoRechargePrefs = await client.payment.autoRechargePrefs.list();

console.log(autoRechargePrefs.data);
```

## 更新自动充值偏好设置

更新支付自动充值偏好设置。

`PATCH /payments/auto_recharge_prefs`

```javascript
const autoRechargePref = await client.payment.autoRechargePrefs.update();

console.log(autoRechargePref.data);
```

## 列出用户标签

列出所有用户标签。

`GET /user_tags`

```javascript
const userTags = await client.userTags.list();

console.log(userTags.data);
```

## 列出 Webhook 交付记录

列出已认证用户的 Webhook 交付记录。

`GET /webhook_deliveries`

```javascript
// Automatically fetches more pages as needed.
for await (const webhookDeliveryListResponse of client.webhookDeliveries.list()) {
  console.log(webhookDeliveryListResponse.id);
}
```

## 根据 ID 查找 Webhook 交付详情

提供 Webhook 交付的调试数据，如时间戳、交付状态和尝试次数。

`GET /webhook_deliveries/{id}`

```javascript
const webhookDelivery = await client.webhookDeliveries.retrieve(
  'C9C0797E-901D-4349-A33C-C2C8F31A92C2',
);

console.log(webhookDelivery.data);
```