---
name: telnyx-account-reports-javascript
description: >-
  Generate and retrieve usage reports for billing, analytics, and
  reconciliation. This skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: account-reports
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户报告 - JavaScript

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

## 获取所有 MDR 详细报告请求

检索已认证用户的所有 MDR 详细报告请求

`GET /legacy_reporting/batch_detail_records/messaging`

```javascript
const messagings = await client.legacy.reporting.batchDetailRecords.messaging.list();

console.log(messagings.data);
```

## 创建新的 MDR 详细报告请求

使用指定的过滤器创建新的 MDR 详细报告请求

`POST /legacy_reporting/batch_detail_records/messaging` — 必需参数：`start_time`, `end_time`

```javascript
const messaging = await client.legacy.reporting.batchDetailRecords.messaging.create({
  end_time: '2024-02-12T23:59:59Z',
  start_time: '2024-02-01T00:00:00Z',
});

console.log(messaging.data);
```

## 获取特定的 MDR 详细报告请求

通过 ID 获取特定的 MDR 详细报告请求

`GET /legacy_reporting/batch_detail_records/messaging/{id}`

```javascript
const messaging = await client.legacy.reporting.batchDetailRecords.messaging.retrieve(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(messaging.data);
```

## 删除 MDR 详细报告请求

通过 ID 删除特定的 MDR 详细报告请求

`DELETE /legacy_reporting/batch_detail_records/messaging/{id}`

```javascript
const messaging = await client.legacy.reporting.batchDetailRecords.messaging.delete(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(messaging.data);
```

## 获取所有 CDR 报告请求

检索已认证用户的所有 CDR 报告请求

`GET /legacy_reporting/batch_detail_records/voice`

```javascript
const voices = await client.legacy.reporting.batchDetailRecords.voice.list();

console.log(voices.data);
```

## 创建新的 CDR 报告请求

使用指定的过滤器创建新的 CDR 报告请求

`POST /legacy_reporting/batch_detail_records/voice` — 必需参数：`start_time`, `end_time`

```javascript
const voice = await client.legacy.reporting.batchDetailRecords.voice.create({
  end_time: '2024-02-12T23:59:59Z',
  start_time: '2024-02-01T00:00:00Z',
});

console.log(voice.data);
```

## 获取特定的 CDR 报告请求

通过 ID 获取特定的 CDR 报告请求

`GET /legacy_reporting/batch_detail_records/voice/{id}`

```javascript
const voice = await client.legacy.reporting.batchDetailRecords.voice.retrieve(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(voice.data);
```

## 删除 CDR 报告请求

通过 ID 删除特定的 CDR 报告请求

`DELETE /legacy_reporting/batch_detail_records/voice/{id}`

```javascript
const voice = await client.legacy.reporting.batchDetailRecords.voice.delete(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(voice.data);
```

## 获取可用的 CDR 报告字段

检索所有可用于 CDR 报告的字段

`GET /legacy_reporting/batch_detail_records/voice/fields`

```javascript
const response = await client.legacy.reporting.batchDetailRecords.voice.retrieveFields();

console.log(response.Billing);
```

## 列出 MDR 使用报告

获取所有之前的 MDR 使用报告请求

`GET /legacy_reporting/usage_reports/messaging`

```javascript
// Automatically fetches more pages as needed.
for await (const mdrUsageReportResponseLegacy of client.legacy.reporting.usageReports.messaging.list()) {
  console.log(mdrUsageReportResponseLegacy.id);
}
```

## 创建新的传统使用 V2 MDR 报告请求

使用指定的过滤器创建新的传统使用 V2 MDR 报告请求

`POST /legacy_reporting/usage_reports/messaging`

```javascript
const messaging = await client.legacy.reporting.usageReports.messaging.create({
  aggregation_type: 0,
});

console.log(messaging.data);
```

## 获取 MDR 使用报告

通过 ID 获取单个 MDR 使用报告

`GET /legacy_reporting/usage_reports/messaging/{id}`

```javascript
const messaging = await client.legacy.reporting.usageReports.messaging.retrieve(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(messaging.data);
```

## 删除 V2 传统使用 MDR 报告请求

通过 ID 删除特定的 V2 传统使用 MDR 报告请求

`DELETE /legacy_reporting/usage_reports/messaging/{id}`

```javascript
const messaging = await client.legacy.reporting.usageReports.messaging.delete(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(messaging.data);
```

## 列出电信数据使用报告

获取分页的电信数据使用报告列表

`GET /legacy_reporting/usage_reports/number_lookup`

```javascript
const numberLookups = await client.legacy.reporting.usageReports.numberLookup.list();

console.log(numberLookups.data);
```

## 提交电信数据使用报告

提交新的电信数据使用报告

`POST /legacy_reporting/usage_reports/number_lookup`

```javascript
const numberLookup = await client.legacy.reporting.usageReports.numberLookup.create();

console.log(numberLookup.data);
```

## 通过 ID 获取电信数据使用报告

通过 ID 获取特定的电信数据使用报告

`GET /legacy_reporting/usage_reports/number_lookup/{id}`

```javascript
const numberLookup = await client.legacy.reporting.usageReports.numberLookup.retrieve('id');

console.log(numberLookup.data);
```

## 删除电信数据使用报告

通过 ID 删除特定的电信数据使用报告

`DELETE /legacy_reporting/usage_reports/number_lookup/{id}`

```javascript
await client.legacy.reporting.usageReports.numberLookup.delete('id');
```

## 获取语音转文本使用报告

生成并同步获取语音转文本使用报告

`GET /legacy_reporting/usage_reports/speech_to_text`

```javascript
const response = await client.legacy.reporting.usageReports.retrieveSpeechToText();

console.log(response.data);
```

## 列出 CDR 使用报告

获取所有之前的 CDR 使用报告请求

`GET /legacy_reporting/usage_reports/voice`

```javascript
// Automatically fetches more pages as needed.
for await (const cdrUsageReportResponseLegacy of client.legacy.reporting.usageReports.voice.list()) {
  console.log(cdrUsageReportResponseLegacy.id);
}
```

## 创建新的传统使用 V2 CDR 报告请求

使用指定的过滤器创建新的传统使用 V2 CDR 报告请求

`POST /legacy_reporting/usage_reports/voice`

```javascript
const voice = await client.legacy.reporting.usageReports.voice.create({
  end_time: '2024-02-01T00:00:00Z',
  start_time: '2024-02-01T00:00:00Z',
});

console.log(voice.data);
```

## 获取 CDR 使用报告

通过 ID 获取单个 CDR 使用报告

`GET /legacy_reporting/usage_reports/voice/{id}`

```javascript
const voice = await client.legacy.reporting.usageReports.voice.retrieve(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(voice.data);
```

## 删除 V2 传统使用 CDR 报告请求

通过 ID 删除特定的 V2 传统使用 CDR 报告请求

`DELETE /legacy_reporting/usage_reports/voice/{id}`

```javascript
const voice = await client.legacy.reporting.usageReports.voice.delete(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(voice.data);
```

## 获取所有消息使用报告

获取所有消息使用报告

`GET /reports/mdr_usage_reports`

```javascript
// Automatically fetches more pages as needed.
for await (const mdrUsageReport of client.reports.mdrUsageReports.list()) {
  console.log(mdrUsageReport.id);
}
```

## 创建 MDR 使用报告

提交新的消息使用报告请求

`POST /reports/mdr_usage_reports`

```javascript
const mdrUsageReport = await client.reports.mdrUsageReports.create({
  aggregation_type: 'NO_AGGREGATION',
  end_date: '2020-07-01T00:00:00-06:00',
  start_date: '2020-07-01T00:00:00-06:00',
});

console.log(mdrUsageReport.data);
```

## 获取消息使用报告

通过 ID 获取单个消息使用报告

`GET /reports/mdr_usage_reports/{id}`

```javascript
const mdrUsageReport = await client.reports.mdrUsageReports.retrieve(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(mdrUsageReport.data);
```

## 删除 MDR 使用报告

通过 ID 删除消息使用报告

`DELETE /reports/mdr_usage_reports/{id}`

```javascript
const mdrUsageReport = await client.reports.mdrUsageReports.delete(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(mdrUsageReport.data);
```

## 生成并获取 MDR 使用报告

同步生成并获取消息使用报告

`GET /reports/mdr_usage_reports/sync`

```javascript
const response = await client.reports.mdrUsageReports.fetchSync({ aggregation_type: 'PROFILE' });

console.log(response.data);
```

## 生成并获取 CDR 使用报告

同步生成并获取语音使用报告

`GET /reports/cdr_usage_reports/sync`

```javascript
const response = await client.reports.cdrUsageReports.fetchSync({
  aggregation_type: 'NO_AGGREGATION',
  product_breakdown: 'NO_BREAKDOWN',
});

console.log(response.data);
```

## 获取 Telnyx 产品使用数据（测试版）

根据指定的维度获取 Telnyx 产品使用数据

`GET /usage_reports`

```javascript
// Automatically fetches more pages as needed.
for await (const usageReportListResponse of client.usageReports.list({
  dimensions: ['string'],
  metrics: ['string'],
  product: 'product',
})) {
  console.log(usageReportListResponse);
}
```

## 获取使用报告查询选项（测试版）

获取用于查询使用情况的报告选项，包括可用的产品及其相应的指标和维度

`GET /usage_reports/options`

```javascript
const response = await client.usageReports.getOptions();

console.log(response.data);
```