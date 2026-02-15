---
name: telnyx-messaging-hosted-javascript
description: >-
  Set up hosted SMS numbers, toll-free verification, and RCS messaging. Use when
  migrating numbers or enabling rich messaging features. This skill provides
  JavaScript SDK examples.
metadata:
  author: telnyx
  product: messaging-hosted
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Messaging Hosted - JavaScript

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

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出托管号码的订单信息

`GET /messaging_hosted_number_orders`

```javascript
// Automatically fetches more pages as needed.
for await (const messagingHostedNumberOrder of client.messagingHostedNumberOrders.list()) {
  console.log(messagingHostedNumberOrder.id);
}
```

## 创建托管号码订单

`POST /messaging_hosted_number_orders`

```javascript
const messagingHostedNumberOrder = await client.messagingHostedNumberOrders.create();

console.log(messagingHostedNumberOrder.data);
```

## 获取托管号码订单信息

`GET /messaging_hosted_number_orders/{id}`

```javascript
const messagingHostedNumberOrder = await client.messagingHostedNumberOrders.retrieve('id');

console.log(messagingHostedNumberOrder.data);
```

## 删除托管号码订单

删除托管号码订单及其所有关联的电话号码。

`DELETE /messaging_hosted_number_orders/{id}`

```javascript
const messagingHostedNumberOrder = await client.messagingHostedNumberOrders.delete('id');

console.log(messagingHostedNumberOrder.data);
```

## 上传托管号码相关文档

`POST /messaging_hosted_number_orders/{id}/actions/file_upload`

```javascript
const response = await client.messagingHostedNumberOrders.actions.uploadFile('id');

console.log(response.data);
```

## 验证托管号码的验证码

验证发送到托管号码的验证码。

`POST /messaging_hosted_number_orders/{id}/validation_codes` — 必需参数：`verification_codes`

```javascript
const response = await client.messagingHostedNumberOrders.validateCodes('id', {
  verification_codes: [{ code: 'code', phone_number: 'phone_number' }],
});

console.log(response.data);
```

## 生成托管号码的验证码

为托管号码生成验证码。

`POST /messaging_hosted_number_orders/{id}/verification_codes` — 必需参数：`phone_numbers`, `verification_method`

```javascript
const response = await client.messagingHostedNumberOrders.createVerificationCodes('id', {
  phone_numbers: ['string'],
  verification_method: 'sms',
});

console.log(response.data);
```

## 检查托管号码的适用性

`POST /messaging_hosted_number_orders/eligibility_numbers_check` — 必需参数：`phone_numbers`

```javascript
const response = await client.messagingHostedNumberOrders.checkEligibility({
  phone_numbers: ['string'],
});

console.log(response.phone_numbers);
```

## 删除托管号码

`DELETE /messaging_hosted_numbers/{id}`

```javascript
const messagingHostedNumber = await client.messagingHostedNumbers.delete('id');

console.log(messagingHostedNumber.data);
```

## 发送 RCS 消息

`POST /messages/rcs` — 必需参数：`agent_id`, `to`, `messaging_profile_id`, `agent_message`

```javascript
const response = await client.messages.rcs.send({
  agent_id: 'Agent007',
  agent_message: {},
  messaging_profile_id: 'messaging_profile_id',
  to: '+13125551234',
});

console.log(response.data);
```

## 列出所有 RCS 代理

`GET /messaging/rcs/agents`

```javascript
// Automatically fetches more pages as needed.
for await (const rcsAgent of client.messaging.rcs.agents.list()) {
  console.log(rcsAgent.agent_id);
}
```

## 获取 RCS 代理信息

`GET /messaging/rcs/agents/{id}`

```javascript
const rcsAgentResponse = await client.messaging.rcs.agents.retrieve('id');

console.log(rcsAgentResponse.data);
```

## 修改 RCS 代理信息

`PATCH /messaging/rcs/agents/{id}`

```javascript
const rcsAgentResponse = await client.messaging.rcs.agents.update('id');

console.log(rcsAgentResponse.data);
```

## 检查 RCS 功能（批量）

`POST /messaging/rcs/bulk_capabilities` — 必需参数：`agent_id`, `phone_numbers`

```javascript
const response = await client.messaging.rcs.listBulkCapabilities({
  agent_id: 'TestAgent',
  phone_numbers: ['+13125551234'],
});

console.log(response.data);
```

## 查看 RCS 功能

`GET /messaging/rcs/capabilities/{agent_id}/{phone_number}`

```javascript
const response = await client.messaging.rcs.retrieveCapabilities('phone_number', {
  agent_id: 'agent_id',
});

console.log(response.data);
```

## 添加 RCS 测试号码

为 RCS 代理添加测试电话号码以供测试使用。

`PUT /messaging/rcs/test_number_invite/{id}/{phone_number}`

```javascript
const response = await client.messaging.rcs.inviteTestNumber('phone_number', { id: 'id' });

console.log(response.data);
```

## 生成 RCS 深链接

生成可用于与特定代理发起 RCS 对话的深链接。

`GET /messages/rcs_deeplinks/{agent_id}`

```javascript
const response = await client.messages.rcs.generateDeeplink('agent_id');

console.log(response.data);
```

## 列出验证请求

获取之前提交的免费电话验证请求列表。

`GET /messaging_tollfree/verification/requests`

```javascript
// Automatically fetches more pages as needed.
for await (const verificationRequestStatus of client.messagingTollfree.verification.requests.list({
  page: 1,
  page_size: 1,
})) {
  console.log(verificationRequestStatus.id);
}
```

## 提交验证请求

提交新的免费电话验证请求。

`POST /messaging_tollfree/verification/requests` — 必需参数：`businessName`, `corporateWebsite`, `businessAddr1`, `businessCity`, `businessState`, `businessZip`, `businessContactFirstName`, `businessContactLastName`, `businessContactEmail`, `businessContactPhone`, `messageVolume`, `phoneNumbers`, `useCase`, `useCaseSummary`, `productionMessageContent`, `optInWorkflow`, `optInWorkflowImageURLs`, `additionalInformation`, `isvReseller`

```javascript
const verificationRequestEgress = await client.messagingTollfree.verification.requests.create({
  additionalInformation: 'additionalInformation',
  businessAddr1: '600 Congress Avenue',
  businessCity: 'Austin',
  businessContactEmail: 'email@example.com',
  businessContactFirstName: 'John',
  businessContactLastName: 'Doe',
  businessContactPhone: '+18005550100',
  businessName: 'Telnyx LLC',
  businessState: 'Texas',
  businessZip: '78701',
  corporateWebsite: 'http://example.com',
  isvReseller: 'isvReseller',
  messageVolume: '100,000',
  optInWorkflow:
    "User signs into the Telnyx portal, enters a number and is prompted to select whether they want to use 2FA verification for security purposes. If they've opted in a confirmation message is sent out to the handset",
  optInWorkflowImageURLs: [
    { url: 'https://telnyx.com/sign-up' },
    { url: 'https://telnyx.com/company/data-privacy' },
  ],
  phoneNumbers: [{ phoneNumber: '+18773554398' }, { phoneNumber: '+18773554399' }],
  productionMessageContent: 'Your Telnyx OTP is XXXX',
  useCase: '2FA',
  useCaseSummary:
    'This is a use case where Telnyx sends out 2FA codes to portal users to verify their identity in order to sign into the portal',
});

console.log(verificationRequestEgress.id);
```

## 获取验证请求信息

通过 ID 获取单个验证请求的详细信息。

`GET /messaging_tollfree/verification/requests/{id}`

```javascript
const verificationRequestStatus = await client.messagingTollfree.verification.requests.retrieve(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(verificationRequestStatus.id);
```

## 更新验证请求

更新现有的免费电话验证请求。

`PATCH /messaging_tollfree/verification/requests/{id}` — 必需参数：`businessName`, `corporateWebsite`, `businessAddr1`, `businessCity`, `businessState`, `businessZip`, `businessContactFirstName`, `businessContactLastName`, `businessContactEmail`, `businessContactPhone`, `messageVolume`, `phoneNumbers`, `useCase`, `useCaseSummary`, `productionMessageContent`, `optInWorkflow`, `optInWorkflowImageURLs`, `additionalInformation`, `isvReseller`

```javascript
const verificationRequestEgress = await client.messagingTollfree.verification.requests.update(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  {
    additionalInformation: 'additionalInformation',
    businessAddr1: '600 Congress Avenue',
    businessCity: 'Austin',
    businessContactEmail: 'email@example.com',
    businessContactFirstName: 'John',
    businessContactLastName: 'Doe',
    businessContactPhone: '+18005550100',
    businessName: 'Telnyx LLC',
    businessState: 'Texas',
    businessZip: '78701',
    corporateWebsite: 'http://example.com',
    isvReseller: 'isvReseller',
    messageVolume: '100,000',
    optInWorkflow:
      "User signs into the Telnyx portal, enters a number and is prompted to select whether they want to use 2FA verification for security purposes. If they've opted in a confirmation message is sent out to the handset",
    optInWorkflowImageURLs: [
      { url: 'https://telnyx.com/sign-up' },
      { url: 'https://telnyx.com/company/data-privacy' },
    ],
    phoneNumbers: [{ phoneNumber: '+18773554398' }, { phoneNumber: '+18773554399' }],
    productionMessageContent: 'Your Telnyx OTP is XXXX',
    useCase: '2FA',
    useCaseSummary:
      'This is a use case where Telnyx sends out 2FA codes to portal users to verify their identity in order to sign into the portal',
  },
);

console.log(verificationRequestEgress.id);
```

## 删除验证请求

仅当验证请求处于“已拒绝”状态时，才能删除该请求。

`DELETE /messaging_tollfree/verification/requests/{id}`

```javascript
await client.messagingTollfree.verification.requests.delete('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');
```