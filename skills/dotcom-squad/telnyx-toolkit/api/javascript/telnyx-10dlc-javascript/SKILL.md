---
name: telnyx-10dlc-javascript
description: >-
  Register brands and campaigns for 10DLC (10-digit long code) A2P messaging
  compliance in the US. Manage campaign assignments to phone numbers. This skill
  provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: 10dlc
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 |

# Telnyx 10Dlc - JavaScript

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

## 列出品牌

此端点用于列出与您的组织关联的所有品牌。

`GET /10dlc/brand`

```javascript
// Automatically fetches more pages as needed.
for await (const brandListResponse of client.messaging10dlc.brand.list()) {
  console.log(brandListResponse.identityStatus);
}
```

## 创建品牌

此端点用于创建新品牌。

`POST /10dlc/brand` — 必需参数：`entityType`, `displayName`, `country`, `email`, `vertical`

```javascript
const telnyxBrand = await client.messaging10dlc.brand.create({
  country: 'US',
  displayName: 'ABC Mobile',
  email: 'email',
  entityType: 'PRIVATE_PROFIT',
  vertical: 'TECHNOLOGY',
});

console.log(telnyxBrand.identityStatus);
```

## 获取品牌信息

通过 `brandId` 获取品牌详情。

`GET /10dlc/brand/{brandId}`

```javascript
const brand = await client.messaging10dlc.brand.retrieve('brandId');

console.log(brand);
```

## 更新品牌信息

通过 `brandId` 更新品牌属性。

`PUT /10dlc/brand/{brandId}` — 必需参数：`entityType`, `displayName`, `country`, `email`, `vertical`

```javascript
const telnyxBrand = await client.messaging10dlc.brand.update('brandId', {
  country: 'US',
  displayName: 'ABC Mobile',
  email: 'email',
  entityType: 'PRIVATE_PROFIT',
  vertical: 'TECHNOLOGY',
});

console.log(telnyxBrand.identityStatus);
```

## 删除品牌

删除品牌。

`DELETE /10dlc/brand/{brandId}`

```javascript
await client.messaging10dlc.brand.delete('brandId');
```

## 重新发送品牌 2FA 邮件

`POST /10dlc/brand/{brandId}/2faEmail`

```javascript
await client.messaging10dlc.brand.resend2faEmail('brandId');
```

## 获取品牌的外部审核记录

获取指定品牌的所有有效外部审核记录。

`GET /10dlc/brand/{brandId}/externalVetting`

```javascript
const externalVettings = await client.messaging10dlc.brand.externalVetting.list('brandId');

console.log(externalVettings);
```

## 请求品牌的外部审核

为品牌请求新的外部审核。

`POST /10dlc/brand/{brandId}/externalVetting` — 必需参数：`evpId`, `vettingClass`

```javascript
const response = await client.messaging10dlc.brand.externalVetting.order('brandId', {
  evpId: 'evpId',
  vettingClass: 'vettingClass',
});

console.log(response.createDate);
```

## 导入外部审核记录

此操作可用于从 TCR 认证的审核提供商导入外部审核记录。

`PUT /10dlc/brand/{brandId}/externalVetting` — 必需参数：`evpId`, `vettingId`

```javascript
const response = await client.messaging10dlc.brand.externalVetting.imports('brandId', {
  evpId: 'evpId',
  vettingId: 'vettingId',
});

console.log(response.createDate);
```

## 取消品牌审核

此操作允许您取消品牌审核。

`PUT /10dlc/brand/{brandId}/revet`

```javascript
const telnyxBrand = await client.messaging10dlc.brand.revet('brandId');

console.log(telnyxBrand.identityStatus);
```

## 通过品牌 ID 获取 SMS OTP 状态

通过品牌 ID 查询 SMS OTP（一次性密码）的状态，用于个人独资企业的品牌验证。

`GET /10dlc/brand/{brandId}/smsOtp`

```javascript
const response = await client.messaging10dlc.brand.retrieveSMSOtpStatus(
  '4b20019b-043a-78f8-0657-b3be3f4b4002',
);

console.log(response.brandId);
```

## 触发品牌 SMS OTP

触发或重新触发 SMS OTP（一次性密码），用于个人独资企业的品牌验证。

`POST /10dlc/brand/{brandId}/smsOtp` — 必需参数：`pinSms`, `successSms`

```javascript
const response = await client.messaging10dlc.brand.triggerSMSOtp(
  '4b20019b-043a-78f8-0657-b3be3f4b4002',
  { pinSms: 'Your PIN is @OTP_PIN@', successSms: 'Verification successful!' },
);

console.log(response.brandId);
```

## 验证品牌 SMS OTP

验证 SMS OTP（一次性密码），用于个人独资企业的品牌验证。

`PUT /10dlc/brand/{brandId}/smsOtp` — 必需参数：`otpPin`

```javascript
await client.messaging10dlc.brand.verifySMSOtp('4b20019b-043a-78f8-0657-b3be3f4b4002', {
  otpPin: '123456',
});
```

## 通过 ID 获取品牌反馈

通过 ID 获取关于品牌的反馈信息。

`GET /10dlc/brand_feedback/{brandId}`

```javascript
const response = await client.messaging10dlc.brand.getFeedback('brandId');

console.log(response.brandId);
```

## 提交活动计划

在创建活动计划之前，请使用 [Qualify By Usecase 端点](https://developers.telnyx.com/api-reference/campaign/qualify-by-usecase) 确保您想要分配新活动计划的品牌符合要求...

`POST /10dlc/campaignBuilder` — 必需参数：`brandId`, `description`, `usecase`

```javascript
const telnyxCampaignCsp = await client.messaging10dlc.campaignBuilder.submit({
  brandId: 'brandId',
  description: 'description',
  usecase: 'usecase',
});

console.log(telnyxCampaignCsp.brandId);
```

## 根据用例验证品牌

此端点用于检查提供的品牌是否适合您所需的活动计划用例。

`GET /10dlc/campaignBuilder/brand/{brandId}/usecase/{usecase}`

```javascript
const response = await client.messaging10dlc.campaignBuilder.brand.qualifyByUsecase('usecase', {
  brandId: 'brandId',
});

console.log(response.annualFee);
```

## 列出活动计划

检索与指定 `brandId` 关联的所有活动计划。

`GET /10dlc/campaign`

```javascript
// Automatically fetches more pages as needed.
for await (const campaignListResponse of client.messaging10dlc.campaign.list({
  brandId: 'brandId',
})) {
  console.log(campaignListResponse.ageGated);
}
```

## 获取活动计划详情

通过 `campaignId` 获取活动计划详情。

`GET /10dlc/campaign/{campaignId}`

```javascript
const telnyxCampaignCsp = await client.messaging10dlc.campaign.retrieve('campaignId');

console.log(telnyxCampaignCsp.brandId);
```

## 更新活动计划

通过 `campaignId` 更新活动计划的属性。

`PUT /10dlc/campaign/{campaignId}`

```javascript
const telnyxCampaignCsp = await client.messaging10dlc.campaign.update('campaignId');

console.log(telnyxCampaignCsp.brandId);
```

## 关闭活动计划

终止活动计划。

`DELETE /10dlc/campaign/{campaignId}`

```javascript
const response = await client.messaging10dlc.campaign.deactivate('campaignId');

console.log(response.time);
```

## 为被拒绝的活动计划提交申诉

为状态为 TELNYX_FAILED 或 MNO_REJECTED 的活动计划提交申诉。

`POST /10dlc/campaign/{campaignId}/appeal` — 必需参数：`appeal_reason`

```javascript
const response = await client.messaging10dlc.campaign.submitAppeal(
  '5eb13888-32b7-4cab-95e6-d834dde21d64',
  {
    appeal_reason:
      'The website has been updated to include the required privacy policy and terms of service.',
  },
);

console.log(response.appealed_at);
```

## 获取活动计划的 MNO 元数据

获取每个活动计划对应的 MNO（移动网络运营商）元数据。

`GET /10dlc/campaign/{campaignId}/mnoMetadata`

```javascript
const response = await client.messaging10dlc.campaign.getMnoMetadata('campaignId');

console.log(response['10999']);
```

## 获取活动计划的操作状态

检索活动计划在 MNO（移动网络运营商）层面的操作状态。

`GET /10dlc/campaign/{campaignId}/operationStatus`

```javascript
const response = await client.messaging10dlc.campaign.getOperationStatus('campaignId');

console.log(response);
```

## 获取 OSR 活动计划属性

`GET /10dlc/campaign/{campaignId}/osr_attributes`

```javascript
const response = await client.messaging10dlc.campaign.osr.getAttributes('campaignId');

console.log(response);
```

## 获取共享状态

`GET /10dlc/campaign/{campaignId}/sharing`

```javascript
const response = await client.messaging10dlc.campaign.getSharingStatus('campaignId');

console.log(response.sharedByMe);
```

## 接受共享的活动计划

手动接受与 Telnyx 共享的活动计划。

`POST /10dlc/campaign/acceptSharing/{campaignId}`

```javascript
const response = await client.messaging10dlc.campaign.acceptSharing('C26F1KLZN');

console.log(response);
```

## 获取活动计划成本

`GET /10dlc/campaign/usecase_cost`

```javascript
const response = await client.messaging10dlc.campaign.usecase.getCost({ usecase: 'usecase' });

console.log(response.campaignUsecase);
```

## 列出共享的活动计划

分页方式获取您与 Telnyx 共享的所有活动计划。

`GET /10dlc/partner_campaigns`

```javascript
// Automatically fetches more pages as needed.
for await (const telnyxDownstreamCampaign of client.messaging10dlc.partnerCampaigns.list()) {
  console.log(telnyxDownstreamCampaign.tcrBrandId);
}
```

## 获取单个共享活动计划

通过 `campaignId` 获取活动计划详情。

`GET /10dlc/partner_campaigns/{campaignId}`

```javascript
const telnyxDownstreamCampaign = await client.messaging10dlc.partnerCampaigns.retrieve(
  'campaignId',
);

console.log(telnyxDownstreamCampaign.tcrBrandId);
```

## 更新单个共享活动计划

通过 `campaignId` 更新活动计划详情。

`PATCH /10dlc/partner_campaigns/{campaignId}`

```javascript
const telnyxDownstreamCampaign = await client.messaging10dlc.partnerCampaigns.update('campaignId');

console.log(telnyxDownstreamCampaign.tcrBrandId);
```

## 获取共享状态

`GET /10dlc/partnerCampaign/{campaignId}/sharing`

```javascript
const response = await client.messaging10dlc.partnerCampaigns.retrieveSharingStatus('campaignId');

console.log(response);
```

## 列出共享的活动计划

分页方式获取您与 Telnyx 共享的所有活动计划

此端点目前仅返回 Telnyx 已接受的活动计划。

`GET /10dlc/partnerCampaign/sharedByMe`

```javascript
// Automatically fetches more pages as needed.
for await (const partnerCampaignListSharedByMeResponse of client.messaging10dlc.partnerCampaigns.listSharedByMe()) {
  console.log(partnerCampaignListSharedByMeResponse.brandId);
}
```

## 列出电话号码活动计划

`GET /10dlc/phone_number_campaigns`

```javascript
// Automatically fetches more pages as needed.
for await (const phoneNumberCampaign of client.messaging10dlc.phoneNumberCampaigns.list()) {
  console.log(phoneNumberCampaign.campaignId);
}
```

## 创建新的电话号码活动计划

`POST /10dlc/phone_number_campaigns` — 必需参数：`phoneNumber`, `campaignId`

```javascript
const phoneNumberCampaign = await client.messaging10dlc.phoneNumberCampaigns.create({
  campaignId: '4b300178-131c-d902-d54e-72d90ba1620j',
  phoneNumber: '+18005550199',
});

console.log(phoneNumberCampaign.campaignId);
```

## 获取单个电话号码活动计划

通过 `phoneNumber` 获取特定的电话号码/活动计划关联信息。

`GET /10dlc/phone_number_campaigns/{phoneNumber}`

```javascript
const phoneNumberCampaign = await client.messaging10dlc.phoneNumberCampaigns.retrieve(
  'phoneNumber',
);

console.log(phoneNumberCampaign.campaignId);
```

## 创建新的电话号码活动计划

`PUT /10dlc/phone_number_campaigns/{phoneNumber}` — 必需参数：`phoneNumber`, `campaignId`

```javascript
const phoneNumberCampaign = await client.messaging10dlc.phoneNumberCampaigns.update('phoneNumber', {
  campaignId: '4b300178-131c-d902-d54e-72d90ba1620j',
  phoneNumber: '+18005550199',
});

console.log(phoneNumberCampaign.campaignId);
```

## 删除电话号码活动计划

此端点用于删除与指定 `phoneNumber` 关联的活动计划。

`DELETE /10dlc/phone_number_campaigns/{phoneNumber}`

```javascript
const phoneNumberCampaign = await client.messaging10dlc.phoneNumberCampaigns.delete('phoneNumber');

console.log(phoneNumberCampaign.campaignId);
```

## 将通信资料库（Messaging Profile）分配给活动计划

此端点允许您将所有与通信资料库关联的电话号码链接到活动计划。

`POST /10dlc/phoneNumberAssignmentByProfile` — 必需参数：`messagingProfileId`

```javascript
const response = await client.messaging10dlc.phoneNumberAssignmentByProfile.assign({
  messagingProfileId: '4001767e-ce0f-4cae-9d5f-0d5e636e7809',
});

console.log(response.messagingProfileId);
```

## 获取任务状态

检查将通信资料库中的所有电话号码分配给活动计划的任务状态。

`GET /10dlc/phoneNumberAssignmentByProfile/{taskId}`

```javascript
const response = await client.messaging10dlc.phoneNumberAssignmentByProfile.retrieveStatus(
  'taskId',
);

console.log(response.status);
```

## 获取电话号码状态

检查与指定 `taskId` 关联的个别电话号码/活动计划的分配状态。

`GET /10dlc/phoneNumberAssignmentByProfile/{taskId}/phoneNumbers`

```javascript
const response = await client.messaging10dlc.phoneNumberAssignmentByProfile.listPhoneNumberStatus(
  'taskId',
);

console.log(response.records);
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `campaignStatusUpdate` | 活动计划状态更新 |
```
```