---
name: telnyx-messaging-javascript
description: >-
  Send and receive SMS/MMS messages, manage messaging-enabled phone numbers, and
  handle opt-outs. Use when building messaging applications, implementing 2FA,
  or sending notifications. This skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: messaging
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 消息服务 - JavaScript

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

## 发送消息

可以使用电话号码、字母数字发送者 ID、短代码或号码池来发送消息。

`POST /messages` — 必需参数：`to`

```javascript
const response = await client.messages.send({ to: '+18445550001' });

console.log(response.data);
```

## 查取消息

注意：此 API 端点仅能检索创建时间不超过 10 天的消息。

`GET /messages/{id}`

```javascript
const message = await client.messages.retrieve('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(message.data);
```

## 取消已安排的消息

取消尚未发送的已安排消息。

`DELETE /messages/{id}`

```javascript
const response = await client.messages.cancelScheduled('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(response.id);
```

## 发送 Whatsapp 消息

`POST /messages/whatsapp` — 必需参数：`from`, `to`, `whatsapp_message`

```javascript
const response = await client.messages.sendWhatsapp({
  from: '+13125551234',
  to: '+13125551234',
  whatsapp_message: {},
});

console.log(response.data);
```

## 发送群组 MMS 消息

`POST /messages/group_mms` — 必需参数：`from`, `to`

```javascript
const response = await client.messages.sendGroupMms({
  from: '+13125551234',
  to: ['+18655551234', '+14155551234'],
});

console.log(response.data);
```

## 发送长码消息

`POST /messages/long_code` — 必需参数：`from`, `to`

```javascript
const response = await client.messages.sendLongCode({ from: '+18445550001', to: '+13125550002' });

console.log(response.data);
```

## 使用号码池发送消息

`POST /messages/number_pool` — 必需参数：`to`, `messaging_profile_id`

```javascript
const response = await client.messages.sendNumberPool({
  messaging_profile_id: 'abc85f64-5717-4562-b3fc-2c9600000000',
  to: '+13125550002',
});

console.log(response.data);
```

## 安排消息

可以使用电话号码、字母数字发送者 ID、短代码或号码池来安排消息的发送。

`POST /messages/schedule` — 必需参数：`to`

```javascript
const response = await client.messages.schedule({ to: '+18445550001' });

console.log(response.data);
```

## 发送短代码消息

`POST /messages/short_code` — 必需参数：`from`, `to`

```javascript
const response = await client.messages.sendShortCode({ from: '+18445550001', to: '+18445550001' });

console.log(response.data);
```

## 获取用户退订信息

检索用户的退订信息。

`GET /messaging_optouts`

```javascript
// Automatically fetches more pages as needed.
for await (const messagingOptoutListResponse of client.messagingOptouts.list()) {
  console.log(messagingOptoutListResponse.messaging_profile_id);
}
```

## 获取带有消息功能的电话号码信息

`GET /phone_numbers/{id}/messaging`

```javascript
const messaging = await client.phoneNumbers.messaging.retrieve('id');

console.log(messaging.data);
```

## 更新电话号码的消息功能配置

`PATCH /phone_numbers/{id}/messaging`

```javascript
const messaging = await client.phoneNumbers.messaging.update('id');

console.log(messaging.data);
```

## 获取带有消息功能的电话号码列表

`GET /phone_numbers/messaging`

```javascript
// Automatically fetches more pages as needed.
for await (const phoneNumberWithMessagingSettings of client.phoneNumbers.messaging.list()) {
  console.log(phoneNumberWithMessagingSettings.id);
}
```

## 获取带有消息功能的手机号码信息

`GET /mobile_phone_numbers/{id}/messaging`

```javascript
const messaging = await client.mobilePhoneNumbers.messaging.retrieve('id');

console.log(messaging.data);
```

## 获取带有消息功能的手机号码列表

`GET /mobile_phone_numbers/messaging`

```javascript
// Automatically fetches more pages as needed.
for await (const messagingListResponse of client.mobilePhoneNumbers.messaging.list()) {
  console.log(messagingListResponse.id);
}
```

## 批量更新电话号码配置

`POST /messaging_numbers/bulk_updates` — 必需参数：`messaging_profile_id`, `numbers`

```javascript
const messagingNumbersBulkUpdate = await client.messagingNumbersBulkUpdates.create({
  messaging_profile_id: '00000000-0000-0000-0000-000000000000',
  numbers: ['+18880000000', '+18880000001', '+18880000002'],
});

console.log(messagingNumbersBulkUpdate.data);
```

## 获取批量更新状态

`GET /messaging_numbers/bulk_updates/{order_id}`

```javascript
const messagingNumbersBulkUpdate = await client.messagingNumbersBulkUpdates.retrieve('order_id');

console.log(messagingNumbersBulkUpdate.data);
```

---

## Webhook

以下 Webhook 事件会发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `deliveryUpdate` | 消息送达更新 |
| `inboundMessage` | 收到的消息 |
| `replacedLinkClick` | 替换链接点击事件 |