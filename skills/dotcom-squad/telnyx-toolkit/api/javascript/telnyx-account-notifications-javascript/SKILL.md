---
name: telnyx-account-notifications-javascript
description: >-
  Configure notification channels and settings for account alerts and events.
  This skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: account-notifications
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户通知 - JavaScript

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

## 列出通知渠道

列出通知渠道。

`GET /notification_channels`

```javascript
// Automatically fetches more pages as needed.
for await (const notificationChannel of client.notificationChannels.list()) {
  console.log(notificationChannel.id);
}
```

## 创建通知渠道

创建一个新的通知渠道。

`POST /notification_channels`

```javascript
const notificationChannel = await client.notificationChannels.create();

console.log(notificationChannel.data);
```

## 获取通知渠道信息

获取指定通知渠道的信息。

`GET /notification_channels/{id}`

```javascript
const notificationChannel = await client.notificationChannels.retrieve(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(notificationChannel.data);
```

## 更新通知渠道信息

更新通知渠道的设置。

`PATCH /notification_channels/{id}`

```javascript
const notificationChannel = await client.notificationChannels.update(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(notificationChannel.data);
```

## 删除通知渠道

删除指定的通知渠道。

`DELETE /notification_channels/{id}`

```javascript
const notificationChannel = await client.notificationChannels.delete(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(notificationChannel.data);
```

## 列出所有通知事件条件

返回所有通知事件条件的列表。

`GET /notification_event_conditions`

```javascript
// Automatically fetches more pages as needed.
for await (const notificationEventConditionListResponse of client.notificationEventConditions.list()) {
  console.log(notificationEventConditionListResponse.id);
}
```

## 列出所有通知事件

返回所有通知事件的列表。

`GET /notification_events`

```javascript
// Automatically fetches more pages as needed.
for await (const notificationEventListResponse of client.notificationEvents.list()) {
  console.log(notificationEventListResponse.id);
}
```

## 列出所有通知配置文件

返回所有通知配置文件的列表。

`GET /notification_profiles`

```javascript
// Automatically fetches more pages as needed.
for await (const notificationProfile of client.notificationProfiles.list()) {
  console.log(notificationProfile.id);
}
```

## 创建通知配置文件

创建一个新的通知配置文件。

`POST /notification_profiles`

```javascript
const notificationProfile = await client.notificationProfiles.create();

console.log(notificationProfile.data);
```

## 获取通知配置文件信息

获取指定通知配置文件的信息。

`GET /notification_profiles/{id}`

```javascript
const notificationProfile = await client.notificationProfiles.retrieve(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(notificationProfile.data);
```

## 更新通知配置文件信息

更新通知配置文件的设置。

`PATCH /notification_profiles/{id}`

```javascript
const notificationProfile = await client.notificationProfiles.update(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(notificationProfile.data);
```

## 删除通知配置文件

删除指定的通知配置文件。

`DELETE /notification_profiles/{id}`

```javascript
const notificationProfile = await client.notificationProfiles.delete(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(notificationProfile.data);
```

## 列出通知设置

列出所有通知设置。

`GET /notification_settings`

```javascript
// Automatically fetches more pages as needed.
for await (const notificationSetting of client.notificationSettings.list()) {
  console.log(notificationSetting.id);
}
```

## 添加通知设置

添加一个新的通知设置。

`POST /notification_settings`

```javascript
const notificationSetting = await client.notificationSettings.create();

console.log(notificationSetting.data);
```

## 获取通知设置信息

获取指定通知设置的信息。

`GET /notification_settings/{id}`

```javascript
const notificationSetting = await client.notificationSettings.retrieve(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(notificationSetting.data);
```

## 删除通知设置

删除指定的通知设置。

`DELETE /notification_settings/{id}`

```javascript
const notificationSetting = await client.notificationSettings.delete(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(notificationSetting.data);
```