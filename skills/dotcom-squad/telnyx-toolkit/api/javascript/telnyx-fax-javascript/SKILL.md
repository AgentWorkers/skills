---
name: telnyx-fax-javascript
description: >-
  Send and receive faxes programmatically. Manage fax applications and media.
  This skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: fax
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 传真 - JavaScript

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

## 列出所有传真应用

此端点会在响应的 `data` 属性中返回您的所有传真应用列表。

`GET /fax_applications`

```javascript
// Automatically fetches more pages as needed.
for await (const faxApplication of client.faxApplications.list()) {
  console.log(faxApplication.id);
}
```

## 创建传真应用

根据请求中发送的参数创建一个新的传真应用。

`POST /fax_applications` — 必需参数：`application_name`、`webhook_event_url`

```javascript
const faxApplication = await client.faxApplications.create({
  application_name: 'fax-router',
  webhook_event_url: 'https://example.com',
});

console.log(faxApplication.data);
```

## 查询传真应用信息

在响应的 `data` 属性中返回现有传真应用的详细信息。

`GET /fax_applications/{id}`

```javascript
const faxApplication = await client.faxApplications.retrieve('1293384261075731499');

console.log(faxApplication.data);
```

## 更新传真应用

根据请求的参数更新现有传真应用的设置。

`PATCH /fax_applications/{id}` — 必需参数：`application_name`、`webhook_event_url`

```javascript
const faxApplication = await client.faxApplications.update('1293384261075731499', {
  application_name: 'fax-router',
  webhook_event_url: 'https://example.com',
});

console.log(faxApplication.data);
```

## 删除传真应用

永久删除一个传真应用。

`DELETE /fax_applications/{id}`

```javascript
const faxApplication = await client.faxApplications.delete('1293384261075731499');

console.log(faxApplication.data);
```

## 查看传真列表

`GET /faxes`

```javascript
// Automatically fetches more pages as needed.
for await (const fax of client.faxes.list()) {
  console.log(fax.id);
}
```

## 发送传真

发送传真。

`POST /faxes` — 必需参数：`connection_id`、`from`、`to`

```javascript
const fax = await client.faxes.create({
  connection_id: '234423',
  from: '+13125790015',
  to: '+13127367276',
});

console.log(fax.data);
```

## 查看传真详情

`GET /faxes/{id}`

```javascript
const fax = await client.faxes.retrieve('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(fax.data);
```

## 删除传真

`DELETE /faxes/{id}`

```javascript
await client.faxes.delete('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');
```

## 取消传真

取消处于以下状态之一的传出传真：`queued`、`media.processed`、`originated` 或 `sending`

`POST /faxes/{id}/actions/cancel`

```javascript
const response = await client.faxes.actions.cancel('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(response.data);
```

## 刷新传真信息

当传入的传真信息过期时，刷新其媒体链接。

`POST /faxes/{id}/actions/refresh`

```javascript
const response = await client.faxes.actions.refresh('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(response.data);
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `fax.delivered` | 传真已送达 |
| `fax.failed` | 传真发送失败 |
| `fax.media.processed` | 传真媒体文件已处理 |
| `fax.queued` | 传真已排队 |
| `fax.sendingstarted` | 传真发送开始 |