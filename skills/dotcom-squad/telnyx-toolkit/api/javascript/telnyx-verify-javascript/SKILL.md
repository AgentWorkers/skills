---
name: telnyx-verify-javascript
description: >-
  Look up phone number information (carrier, type, caller name) and verify users
  via SMS/voice OTP. Use for phone verification and data enrichment. This skill
  provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: verify
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Verify - JavaScript

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

## 查找电话号码信息

返回有关提供的电话号码的信息。

`GET /number_lookup/{phone_number}`

```javascript
const numberLookup = await client.numberLookup.retrieve('+18665552368');

console.log(numberLookup.data);
```

## 触发电话验证

`POST /verifications/call` — 必需参数：`phone_number`、`verify_profile_id`

```javascript
const createVerificationResponse = await client.verifications.triggerCall({
  phone_number: '+13035551234',
  verify_profile_id: '12ade33a-21c0-473b-b055-b3c836e1c292',
});

console.log(createVerificationResponse.data);
```

## 触发闪现式电话验证

`POST /verifications/flashcall` — 必需参数：`phone_number`、`verify_profile_id`

```javascript
const createVerificationResponse = await client.verifications.triggerFlashcall({
  phone_number: '+13035551234',
  verify_profile_id: '12ade33a-21c0-473b-b055-b3c836e1c292',
});

console.log(createVerificationResponse.data);
```

## 触发短信验证

`POST /verifications/sms` — 必需参数：`phone_number`、`verify_profile_id`

```javascript
const createVerificationResponse = await client.verifications.triggerSMS({
  phone_number: '+13035551234',
  verify_profile_id: '12ade33a-21c0-473b-b055-b3c836e1c292',
});

console.log(createVerificationResponse.data);
```

## 获取验证结果

`GET /verifications/{verification_id}`

```javascript
const verification = await client.verifications.retrieve('12ade33a-21c0-473b-b055-b3c836e1c292');

console.log(verification.data);
```

## 通过 ID 验证验证码

`POST /verifications/{verification_id}/actions/verify`

```javascript
const verifyVerificationCodeResponse = await client.verifications.actions.verify(
  '12ade33a-21c0-473b-b055-b3c836e1c292',
);

console.log(verifyVerificationCodeResponse.data);
```

## 按电话号码列出验证记录

`GET /verifications/by_phone_number/{phone_number}`

```javascript
const byPhoneNumbers = await client.verifications.byPhoneNumber.list('+13035551234');

console.log(byPhoneNumbers.data);
```

## 通过电话号码验证验证码

`POST /verifications/by_phone_number/{phone_number}/actions/verify` — 必需参数：`code`、`verify_profile_id`

```javascript
const verifyVerificationCodeResponse = await client.verifications.byPhoneNumber.actions.verify(
  '+13035551234',
  { code: '17686', verify_profile_id: '12ade33a-21c0-473b-b055-b3c836e1c292' },
);

console.log(verifyVerificationCodeResponse.data);
```

## 列出所有验证配置文件

获取分页显示的验证配置文件列表。

`GET /verify_profiles`

```javascript
// Automatically fetches more pages as needed.
for await (const verifyProfile of client.verifyProfiles.list()) {
  console.log(verifyProfile.id);
}
```

## 创建验证配置文件

创建一个新的验证配置文件，用于关联验证操作。

`POST /verify_profiles` — 必需参数：`name`

```javascript
const verifyProfileData = await client.verifyProfiles.create({ name: 'Test Profile' });

console.log(verifyProfileData.data);
```

## 获取验证配置文件信息

获取单个验证配置文件的信息。

`GET /verify_profiles/{verify_profile_id}`

```javascript
const verifyProfileData = await client.verifyProfiles.retrieve(
  '12ade33a-21c0-473b-b055-b3c836e1c292',
);

console.log(verifyProfileData.data);
```

## 更新验证配置文件

`PATCH /verify_profiles/{verify_profile_id}`

```javascript
const verifyProfileData = await client.verifyProfiles.update(
  '12ade33a-21c0-473b-b055-b3c836e1c292',
);

console.log(verifyProfileData.data);
```

## 删除验证配置文件

`DELETE /verify_profiles/{verify_profile_id}`

```javascript
const verifyProfileData = await client.verifyProfiles.delete(
  '12ade33a-21c0-473b-b055-b3c836e1c292',
);

console.log(verifyProfileData.data);
```

## 获取验证配置文件的消息模板

列出所有验证配置文件的消息模板。

`GET /verify_profiles/templates`

```javascript
const response = await client.verifyProfiles.retrieveTemplates();

console.log(response.data);
```

## 创建消息模板

创建一个新的验证配置文件消息模板。

`POST /verify_profiles/templates` — 必需参数：`text`

```javascript
const messageTemplate = await client.verifyProfiles.createTemplate({
  text: 'Your {{app_name}} verification code is: {{code}}.',
});

console.log(messageTemplate.data);
```

## 更新消息模板

更新现有的验证配置文件消息模板。

`PATCH /verify_profiles/templates/{template_id}` — 必需参数：`text`

```javascript
const messageTemplate = await client.verifyProfiles.updateTemplate(
  '12ade33a-21c0-473b-b055-b3c836e1c292',
  { text: 'Your {{app_name}} verification code is: {{code}}.' },
);

console.log(messageTemplate.data);
```