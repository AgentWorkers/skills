---
name: telnyx-numbers-config-javascript
description: >-
  Configure phone number settings including caller ID, call forwarding,
  messaging enablement, and connection assignments. This skill provides
  JavaScript SDK examples.
metadata:
  author: telnyx
  product: numbers-config
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 数字信息配置 - JavaScript

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

以下所有示例均假设 `client` 已经按照上述方式初始化。

## 列出电话号码相关任务

`GET /phone_number_blocks/jobs`

```javascript
// Automatically fetches more pages as needed.
for await (const job of client.phoneNumberBlocks.jobs.list()) {
  console.log(job.id);
}
```

## 获取特定的电话号码相关任务

`GET /phone_number_blocks/jobs/{id}`

```javascript
const job = await client.phoneNumberBlocks.jobs.retrieve('id');

console.log(job.data);
```

## 删除与某个电话号码块关联的所有号码

创建一个新的后台任务，以删除与该电话号码块关联的所有号码。

`POST /phone_number_blocks/jobs/delete_phone_number_block` — 必需参数：`phone_number_block_id`

```javascript
const response = await client.phoneNumberBlocks.jobs.deletePhoneNumberBlock({
  phone_number_block_id: 'f3946371-7199-4261-9c3d-81a0d7935146',
});

console.log(response.data);
```

## 列出所有电话号码

`GET /phone_numbers`

```javascript
// Automatically fetches more pages as needed.
for await (const phoneNumberDetailed of client.phoneNumbers.list()) {
  console.log(phoneNumberDetailed.id);
}
```

## 获取某个电话号码的信息

`GET /phone_numbers/{id}`

```javascript
const phoneNumber = await client.phoneNumbers.retrieve('1293384261075731499');

console.log(phoneNumber.data);
```

## 更新某个电话号码的信息

`PATCH /phone_numbers/{id}`

```javascript
const phoneNumber = await client.phoneNumbers.update('1293384261075731499');

console.log(phoneNumber.data);
```

## 删除某个电话号码

`DELETE /phone_numbers/{id}`

```javascript
const phoneNumber = await client.phoneNumbers.delete('1293384261075731499');

console.log(phoneNumber.data);
```

## 更改电话号码的捆绑状态（将其添加到捆绑包中或从捆绑包中移除）

`PATCH /phone_numbers/{id}/actions/bundle_status_change` — 必需参数：`bundle_id`

```javascript
const response = await client.phoneNumbers.actions.changeBundleStatus('1293384261075731499', {
  bundle_id: '5194d8fc-87e6-4188-baa9-1c434bbe861b',
});

console.log(response.data);
```

## 为某个电话号码启用紧急呼叫功能

`POST /phone_numbers/{id}/actions/enable_emergency` — 必需参数：`emergency_enabled`, `emergency_address_id`

```javascript
const response = await client.phoneNumbers.actions.enableEmergency('1293384261075731499', {
  emergency_address_id: '53829456729313',
  emergency_enabled: true,
});

console.log(response.data);
```

## 获取带有语音设置的电话号码信息

`GET /phone_numbers/{id}/voice`

```javascript
const voice = await client.phoneNumbers.voice.retrieve('1293384261075731499');

console.log(voice.data);
```

## 更新带有语音设置的电话号码信息

`PATCH /phone_numbers/{id}/voice`

```javascript
const voice = await client.phoneNumbers.voice.update('1293384261075731499');

console.log(voice.data);
```

## 验证电话号码的所有权

验证提供的电话号码的所有权，并返回号码与其 ID 的对应关系，以及未在账户中找到的号码列表。

`POST /phone_numbers/actions/verify_ownership` — 必需参数：`phone_numbers`

```javascript
const response = await client.phoneNumbers.actions.verifyOwnership({
  phone_numbers: ['+15551234567'],
});

console.log(response.data);
```

## 列出 CSV 下载文件

`GET /phone_numbers/csv_downloads`

```javascript
// Automatically fetches more pages as needed.
for await (const csvDownload of client.phoneNumbers.csvDownloads.list()) {
  console.log(csvDownload.id);
}
```

## 创建 CSV 下载文件

`POST /phone_numbers/csv_downloads`

```javascript
const csvDownload = await client.phoneNumbers.csvDownloads.create();

console.log(csvDownload.data);
```

## 获取 CSV 下载文件

`GET /phone_numbers/csv_downloads/{id}`

```javascript
const csvDownload = await client.phoneNumbers.csvDownloads.retrieve('id');

console.log(csvDownload.data);
```

## 列出所有电话号码相关任务

`GET /phone_numbers/jobs`

```javascript
// Automatically fetches more pages as needed.
for await (const phoneNumbersJob of client.phoneNumbers.jobs.list()) {
  console.log(phoneNumbersJob.id);
}
```

## 获取特定的电话号码相关任务信息

`GET /phone_numbers/jobs/{id}`

```javascript
const job = await client.phoneNumbers.jobs.retrieve('id');

console.log(job.data);
```

## 删除一批电话号码

创建一个新的后台任务，以删除一批电话号码。

`POST /phone_numbers/jobs/delete_phone_numbers` — 必需参数：`phone_numbers`

```javascript
const response = await client.phoneNumbers.jobs.deleteBatch({
  phone_numbers: ['+19705555098', '+19715555098', '32873127836'],
});

console.log(response.data);
```

## 更新一批电话号码的紧急呼叫设置

创建一个新的后台任务，以更新一批电话号码的紧急呼叫设置。

`POST /phone_numbers/jobs/update_emergency_settings` — 必需参数：`emergency_enabled`, `phone_numbers`

```javascript
const response = await client.phoneNumbers.jobs.updateEmergencySettingsBatch({
  emergency_enabled: true,
  phone_numbers: ['+19705555098', '+19715555098', '32873127836'],
});

console.log(response.data);
```

## 更新一批电话号码的信息

创建一个新的后台任务，以更新一批电话号码的信息。

`POST /phone_numbers/jobs/update_phone_numbers` — 必需参数：`phone_numbers`

```javascript
const response = await client.phoneNumbers.jobs.updateBatch({
  phone_numbers: ['1583466971586889004', '+13127367254'],
});

console.log(response.data);
```

## 获取一组电话号码的监管要求信息

`GET /phone_numbers/regulatory_requirements`

```javascript
const phoneNumbersRegulatoryRequirement =
  await client.phoneNumbersRegulatoryRequirements.retrieve();

console.log(phoneNumbersRegulatoryRequirement.data);
```

## 简化版电话号码列表

提供性能更高、限制更少的电话号码列表接口。

`GET /phone_numbers/slim`

```javascript
// Automatically fetches more pages as needed.
for await (const phoneNumberSlimListResponse of client.phoneNumbers.slimList()) {
  console.log(phoneNumberSlimListResponse.id);
}
```

## 列出带有语音设置的电话号码

`GET /phone_numbers/voice`

```javascript
// Automatically fetches more pages as needed.
for await (const phoneNumberWithVoiceSettings of client.phoneNumbers.voice.list()) {
  console.log(phoneNumberWithVoiceSettings.id);
}
```

## 列出手机号码

`GET /v2/mobile_phone_numbers`

```javascript
// Automatically fetches more pages as needed.
for await (const mobilePhoneNumber of client.mobilePhoneNumbers.list()) {
  console.log(mobilePhoneNumber.id);
}
```

## 获取某个手机号码的信息

`GET /v2/mobile_phone_numbers/{id}`

```javascript
const mobilePhoneNumber = await client.mobilePhoneNumbers.retrieve('id');

console.log(mobilePhoneNumber.data);
```

## 更新某个手机号码的信息

`PATCH /v2/mobile_phone_numbers/{id}`

```javascript
const mobilePhoneNumber = await client.mobilePhoneNumbers.update('id');

console.log(mobilePhoneNumber.data);
```