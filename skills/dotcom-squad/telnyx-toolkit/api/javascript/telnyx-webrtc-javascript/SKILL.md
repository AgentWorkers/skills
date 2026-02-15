---
name: telnyx-webrtc-javascript
description: >-
  Manage WebRTC credentials and mobile push notification settings. Use when
  building browser-based or mobile softphone applications. This skill provides
  JavaScript SDK examples.
metadata:
  author: telnyx
  product: webrtc
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Webrtc - JavaScript

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

## 列出移动推送凭据

`GET /mobile_push_credentials`

```javascript
// Automatically fetches more pages as needed.
for await (const pushCredential of client.mobilePushCredentials.list()) {
  console.log(pushCredential.id);
}
```

## 创建新的移动推送凭据

`POST /mobile_push_credentials`

```javascript
const pushCredentialResponse = await client.mobilePushCredentials.create({
  createMobilePushCredentialRequest: {
    alias: 'LucyIosCredential',
    certificate:
      '-----BEGIN CERTIFICATE----- MIIGVDCCBTKCAQEAsNlRJVZn9ZvXcECQm65czs... -----END CERTIFICATE-----',
    private_key:
      '-----BEGIN RSA PRIVATE KEY----- MIIEpQIBAAKCAQEAsNlRJVZn9ZvXcECQm65czs... -----END RSA PRIVATE KEY-----',
    type: 'ios',
  },
});

console.log(pushCredentialResponse.data);
```

## 获取移动推送凭据

根据给定的 `push_credential_id` 获取移动推送凭据

`GET /mobile_push_credentials/{push_credential_id}`

```javascript
const pushCredentialResponse = await client.mobilePushCredentials.retrieve(
  '0ccc7b76-4df3-4bca-a05a-3da1ecc389f0',
);

console.log(pushCredentialResponse.data);
```

## 删除移动推送凭据

根据给定的 `push_credential_id` 删除移动推送凭据

`DELETE /mobile_push_credentials/{push_credential_id}`

```javascript
await client.mobilePushCredentials.delete('0ccc7b76-4df3-4bca-a05a-3da1ecc389f0');
```

## 列出所有凭据

列出所有的按需生成的凭据。

`GET /telephony_credentials`

```javascript
// Automatically fetches more pages as needed.
for await (const telephonyCredential of client.telephonyCredentials.list()) {
  console.log(telephonyCredential.id);
}
```

## 创建凭据

创建一个新的凭据。

`POST /telephony_credentials` — 必需参数：`connection_id`

```javascript
const telephonyCredential = await client.telephonyCredentials.create({
  connection_id: '1234567890',
});

console.log(telephonyCredential.data);
```

## 获取凭据详情

获取现有按需生成凭据的详细信息。

`GET /telephony_credentials/{id}`

```javascript
const telephonyCredential = await client.telephonyCredentials.retrieve('id');

console.log(telephonyCredential.data);
```

## 更新凭据

更新现有的凭据。

`PATCH /telephony_credentials/{id}`

```javascript
const telephonyCredential = await client.telephonyCredentials.update('id');

console.log(telephonyCredential.data);
```

## 删除凭据

删除现有的凭据。

`DELETE /telephony_credentials/{id}`

```javascript
const telephonyCredential = await client.telephonyCredentials.delete('id');

console.log(telephonyCredential.data);
```

## 创建访问令牌

为该凭据创建一个访问令牌（JWT）。

`POST /telephony_credentials/{id}/token`

```javascript
const response = await client.telephonyCredentials.createToken('id');

console.log(response);
```