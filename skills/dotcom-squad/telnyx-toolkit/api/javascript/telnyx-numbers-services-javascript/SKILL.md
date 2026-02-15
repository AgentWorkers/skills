---
name: telnyx-numbers-services-javascript
description: >-
  Configure voicemail, voice channels, and emergency (E911) services for your
  phone numbers. This skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: numbers-services
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 数字服务 - JavaScript

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

## 列出动态紧急地址

根据筛选条件返回动态紧急地址

`GET /dynamic_emergency_addresses`

```javascript
// Automatically fetches more pages as needed.
for await (const dynamicEmergencyAddress of client.dynamicEmergencyAddresses.list()) {
  console.log(dynamicEmergencyAddress.id);
}
```

## 创建动态紧急地址

创建一个动态紧急地址。

`POST /dynamic_emergency_addresses` — 必需参数：`house_number`、`street_name`、`locality`、`administrative_area`、`postal_code`、`country_code`

```javascript
const dynamicEmergencyAddress = await client.dynamicEmergencyAddresses.create({
  administrative_area: 'TX',
  country_code: 'US',
  house_number: '600',
  locality: 'Austin',
  postal_code: '78701',
  street_name: 'Congress',
});

console.log(dynamicEmergencyAddress.data);
```

## 获取动态紧急地址

根据提供的 ID 返回动态紧急地址

`GET /dynamic_emergency_addresses/{id}`

```javascript
const dynamicEmergencyAddress = await client.dynamicEmergencyAddresses.retrieve(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(dynamicEmergencyAddress.data);
```

## 删除动态紧急地址

根据提供的 ID 删除动态紧急地址

`DELETE /dynamic_emergency_addresses/{id}`

```javascript
const dynamicEmergencyAddress = await client.dynamicEmergencyAddresses.delete(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(dynamicEmergencyAddress.data);
```

## 列出动态紧急终端点

根据筛选条件返回动态紧急终端点

`GET /dynamic_emergency_endpoints`

```javascript
// Automatically fetches more pages as needed.
for await (const dynamicEmergencyEndpoint of client.dynamicEmergencyEndpoints.list()) {
  console.log(dynamicEmergencyEndpoint.dynamic_emergency_address_id);
}
```

## 创建动态紧急终端点

创建一个动态紧急终端点。

`POST /dynamic_emergency_endpoints` — 必需参数：`dynamic_emergency_address_id`、`callback_number`、`caller_name`

```javascript
const dynamicEmergencyEndpoint = await client.dynamicEmergencyEndpoints.create({
  callback_number: '+13125550000',
  caller_name: 'Jane Doe Desk Phone',
  dynamic_emergency_address_id: '0ccc7b54-4df3-4bca-a65a-3da1ecc777f0',
});

console.log(dynamicEmergencyEndpoint.data);
```

## 获取动态紧急终端点

根据提供的 ID 返回动态紧急终端点

`GET /dynamic_emergency_endpoints/{id}`

```javascript
const dynamicEmergencyEndpoint = await client.dynamicEmergencyEndpoints.retrieve(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(dynamicEmergencyEndpoint.data);
```

## 删除动态紧急终端点

根据提供的 ID 删除动态紧急终端点

`DELETE /dynamic_emergency_endpoints/{id}`

```javascript
const dynamicEmergencyEndpoint = await client.dynamicEmergencyEndpoints.delete(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(dynamicEmergencyEndpoint.data);
```

## 列出非美国地区的语音通道

列出您账户中的非美国地区语音通道。

`GET /channel_zones`

```javascript
// Automatically fetches more pages as needed.
for await (const channelZoneListResponse of client.channelZones.list()) {
  console.log(channelZoneListResponse.id);
}
```

## 更新非美国地区的语音通道

更新非美国地区的语音通道数量。

`PUT /channel_zones/{channel_zone_id}` — 必需参数：`channels`

```javascript
const channelZone = await client.channelZones.update('channel_zone_id', { channels: 0 });

console.log(channelZone.id);
```

## 列出美国地区的语音通道

列出您账户中的美国地区语音通道。

`GET /inbound_channels`

```javascript
const inboundChannels = await client.inboundChannels.list();

console.log(inboundChannels.data);
```

## 更新美国地区的语音通道

更新美国地区的语音通道数量。

`PATCH /inbound_channels` — 必需参数：`channels`

```javascript
const inboundChannel = await client.inboundChannels.update({ channels: 7 });

console.log(inboundChannel.data);
```

## 列出使用渠道计费的所有电话号码

按地区分组，检索所有使用渠道计费的电话号码。

`GET /list`

```javascript
const response = await client.list.retrieveAll();

console.log(response.data);
```

## 列出特定地区的使用渠道计费的电话号码

检索特定地区使用渠道计费的电话号码列表。

`GET /list/{channel_zone_id}`

```javascript
const response = await client.list.retrieveByZone('channel_zone_id');

console.log(response.data);
```

## 获取语音信箱

获取电话号码的语音信箱设置

`GET /phone_numbers/{phone_number_id}/voicemail`

```javascript
const voicemail = await client.phoneNumbers.voicemail.retrieve('123455678900');

console.log(voicemail.data);
```

## 创建语音信箱

为电话号码创建语音信箱设置

`POST /phone_numbers/{phone_number_id}/voicemail`

```javascript
const voicemail = await client.phoneNumbers.voicemail.create('123455678900');

console.log(voicemail.data);
```

## 更新语音信箱

更新电话号码的语音信箱设置

`PATCH /phone_numbers/{phone_number_id}/voicemail`

```javascript
const voicemail = await client.phoneNumbers.voicemail.update('123455678900');

console.log(voicemail.data);
```