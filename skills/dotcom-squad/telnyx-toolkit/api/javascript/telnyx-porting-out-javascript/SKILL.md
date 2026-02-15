---
name: telnyx-porting-out-javascript
description: >-
  Manage port-out requests when numbers are being ported away from Telnyx. List,
  view, and update port-out status. This skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: porting-out
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Porting Out - JavaScript

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

## 列出 portout 请求

根据筛选条件返回 portout 请求

`GET /portouts`

```javascript
// Automatically fetches more pages as needed.
for await (const portoutDetails of client.portouts.list()) {
  console.log(portoutDetails.id);
}
```

## 获取 portout 请求

根据提供的 ID 返回 portout 请求

`GET /portouts/{id}`

```javascript
const portout = await client.portouts.retrieve('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(portout.data);
```

## 查看 portout 请求的评论

返回 portout 请求的所有评论

`GET /portouts/{id}/comments`

```javascript
const comments = await client.portouts.comments.list('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(comments.data);
```

## 为 portout 请求添加评论

为 portout 请求创建评论

`POST /portouts/{id}/comments`

```javascript
const comment = await client.portouts.comments.create('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(comment.data);
```

## 查看 portout 请求的辅助文档

列出 portout 请求的所有辅助文档

`GET /portouts/{id}/supporting_documents`

```javascript
const supportingDocuments = await client.portouts.supportingDocuments.list(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(supportingDocuments.data);
```

## 为 portout 请求创建辅助文档列表

为 portout 请求创建辅助文档列表

`POST /portouts/{id}/supporting_documents`

```javascript
const supportingDocument = await client.portouts.supportingDocuments.create(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(supportingDocument.data);
```

## 更新状态

授权或拒绝 portout 请求

`PATCH /portouts/{id}/{status}` — 必需参数：`reason`

```javascript
const response = await client.portouts.updateStatus('authorized', {
  id: '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  reason: 'I do not recognize this transaction',
});

console.log(response.data);
```

## 列出所有 port-out 事件

返回所有 port-out 事件的列表

`GET /portouts/events`

```javascript
// Automatically fetches more pages as needed.
for await (const eventListResponse of client.portouts.events.list()) {
  console.log(eventListResponse);
}
```

## 查看特定的 port-out 事件

显示特定的 port-out 事件

`GET /portouts/events/{id}`

```javascript
const event = await client.portouts.events.retrieve('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(event.data);
```

## 重新发布 port-out 事件

重新发布特定的 port-out 事件

`POST /portouts/events/{id}/republish`

```javascript
await client.portouts.events.republish('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');
```

## 列出特定订单的 eligible port-out 拒绝代码

根据给定的 port-out ID，列出适用于该订单的拒绝代码

`GET /portouts/rejections/{portout_id}`

```javascript
const response = await client.portouts.listRejectionCodes('329d6658-8f93-405d-862f-648776e8afd7');

console.log(response.data);
```

## 查看 port-out 相关报告

列出关于 port-out 操作生成的报告

`GET /portouts/reports`

```javascript
// Automatically fetches more pages as needed.
for await (const portoutReport of client.portouts.reports.list()) {
  console.log(portoutReport.id);
}
```

## 创建 port-out 相关报告

生成关于 port-out 操作的报告

`POST /portouts/reports`

```javascript
const report = await client.portouts.reports.create({
  params: { filters: {} },
  report_type: 'export_portouts_csv',
});

console.log(report.data);
```

## 获取报告

检索生成的特定报告

`GET /portouts/reports/{id}`

```javascript
const report = await client.portouts.reports.retrieve('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(report.data);
```