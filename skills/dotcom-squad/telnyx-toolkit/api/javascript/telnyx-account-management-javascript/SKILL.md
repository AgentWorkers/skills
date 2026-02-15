---
name: telnyx-account-management-javascript
description: >-
  Manage sub-accounts for reseller and enterprise scenarios. This skill provides
  JavaScript SDK examples.
metadata:
  author: telnyx
  product: account-management
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户管理 - JavaScript

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

## 列出当前用户管理的账户

列出当前用户管理的账户。

`GET /managed_accounts`

```javascript
// Automatically fetches more pages as needed.
for await (const managedAccountListResponse of client.managedAccounts.list()) {
  console.log(managedAccountListResponse.id);
}
```

## 创建一个新的受管理的账户

创建一个由已认证用户拥有的新受管理账户。

`POST /managed_accounts` — 必需参数：`business_name`

```javascript
const managedAccount = await client.managedAccounts.create({
  business_name: "Larry's Cat Food Inc",
});

console.log(managedAccount.data);
```

## 获取受管理的账户信息

获取单个受管理账户的详细信息。

`GET /managed_accounts/{id}`

```javascript
const managedAccount = await client.managedAccounts.retrieve('id');

console.log(managedAccount.data);
```

## 更新受管理的账户

更新单个受管理的账户。

`PATCH /managed_accounts/{id}`

```javascript
const managedAccount = await client.managedAccounts.update('id');

console.log(managedAccount.data);
```

## 禁用受管理的账户

禁用受管理的账户，使其无法使用 Telnyx 服务（包括发送或接收电话呼叫和短信）。

`POST /managedaccounts/{id}/actions/disable`

```javascript
const response = await client.managedAccounts.actions.disable('id');

console.log(response.data);
```

## 恢复受管理的账户

启用受管理的账户及其子用户使用 Telnyx 服务。

`POST /managed.accounts/{id}/actions/enable`

```javascript
const response = await client.managedAccounts.actions.enable('id');

console.log(response.data);
```

## 更新分配给特定受管理账户的全球出站通道数量

更新分配给特定受管理账户的全球出站通道数量。

`PATCH /managed_accounts/{id}/update_global_channel_limit`

```javascript
const response = await client.managedAccounts.updateGlobalChannelLimit('id');

console.log(response.data);
```

## 显示当前用户可用的全球出站通道信息

显示当前用户可用的全球出站通道信息。

`GET /managed_accounts/allocatable_global_outbound_channels`

```javascript
const response = await client.managedAccounts.getAllocatableGlobalOutboundChannels();

console.log(response.data);
```