---
name: telnyx-account-reports-ruby
description: >-
  Generate and retrieve usage reports for billing, analytics, and
  reconciliation. This skill provides Ruby SDK examples.
metadata:
  author: telnyx
  product: account-reports
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户报告 - Ruby

## 安装

```bash
gem install telnyx
```

## 设置

```ruby
require "telnyx"

client = Telnyx::Client.new(
  api_key: ENV["TELNYX_API_KEY"], # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 获取所有 MDR 详细报告请求

检索已认证用户的所有 MDR 详细报告请求

`GET /legacy_reporting/batch_detail_records/messaging`

```ruby
messagings = client.legacy.reporting.batch_detail_records.messaging.list

puts(messagings)
```

## 创建新的 MDR 详细报告请求

使用指定的过滤器创建新的 MDR 详细报告请求

`POST /legacy_reporting/batch_detail_records/messaging` — 必需参数：`start_time`, `end_time`

```ruby
messaging = client.legacy.reporting.batch_detail_records.messaging.create(
  end_time: "2024-02-12T23:59:59Z",
  start_time: "2024-02-01T00:00:00Z"
)

puts(messaging)
```

## 获取特定的 MDR 详细报告请求

通过 ID 获取特定的 MDR 详细报告请求

`GET /legacy_reporting/batch_detail_records/messaging/{id}`

```ruby
messaging = client.legacy.reporting.batch_detail_records.messaging.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(messaging)
```

## 删除 MDR 详细报告请求

通过 ID 删除特定的 MDR 详细报告请求

`DELETE /legacy_reporting/batch_detail_records/messaging/{id}`

```ruby
messaging = client.legacy.reporting.batch_detail_records.messaging.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(messaging)
```

## 获取所有 CDR 报告请求

检索已认证用户的所有 CDR 报告请求

`GET /legacy_reporting/batch_detail_records/voice`

```ruby
voices = client.legacy.reporting.batch_detail_records.voice.list

puts(voices)
```

## 创建新的 CDR 报告请求

使用指定的过滤器创建新的 CDR 报告请求

`POST /legacy_reporting/batch_detail_records/voice` — 必需参数：`start_time`, `end_time`

```ruby
voice = client.legacy.reporting.batch_detail_records.voice.create(
  end_time: "2024-02-12T23:59:59Z",
  start_time: "2024-02-01T00:00:00Z"
)

puts(voice)
```

## 获取特定的 CDR 报告请求

通过 ID 获取特定的 CDR 报告请求

`GET /legacy_reporting/batch_detail_records/voice/{id}`

```ruby
voice = client.legacy.reporting.batch_detail_records.voice.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(voice)
```

## 删除 CDR 报告请求

通过 ID 删除特定的 CDR 报告请求

`DELETE /legacy_reporting/batch_detail_records/voice/{id}`

```ruby
voice = client.legacy.reporting.batch_detail_records.voice.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(voice)
```

## 获取可用的 CDR 报告字段

检索所有可用于 CDR 报告的字段

`GET /legacy_reporting/batch_detail_records/voice/fields`

```ruby
response = client.legacy.reporting.batch_detail_records.voice.retrieve_fields

puts(response)
```

## 列出 MDR 使用报告

获取所有之前的 MDR 使用报告请求

`GET /legacy_reporting/usage_reports/messaging`

```ruby
page = client.legacy.reporting.usage_reports.messaging.list

puts(page)
```

## 创建新的传统使用 V2 MDR 报告请求

使用指定的过滤器创建新的传统使用 V2 MDR 报告请求

`POST /legacy_reporting/usage_reports/messaging`

```ruby
messaging = client.legacy.reporting.usage_reports.messaging.create(aggregation_type: 0)

puts(messaging)
```

## 获取 MDR 使用报告

通过 ID 获取单个 MDR 使用报告

`GET /legacy_reporting/usage_reports/messaging/{id}`

```ruby
messaging = client.legacy.reporting.usage_reports.messaging.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(messaging)
```

## 删除 V2 传统使用 MDR 报告请求

通过 ID 删除特定的 V2 传统使用 MDR 报告请求

`DELETE /legacy_reporting/usage_reports/messaging/{id}`

```ruby
messaging = client.legacy.reporting.usage_reports.messaging.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(messaging)
```

## 列出电信数据使用报告

获取分页的电信数据使用报告列表

`GET /legacy_reporting/usage_reports/number_lookup`

```ruby
number_lookups = client.legacy.reporting.usage_reports.number_lookup.list

puts(number_lookups)
```

## 提交电信数据使用报告

提交新的电信数据使用报告

`POST /legacy_reporting/usage_reports/number_lookup`

```ruby
number_lookup = client.legacy.reporting.usage_reports.number_lookup.create

puts(number_lookup)
```

## 通过 ID 获取电信数据使用报告

通过 ID 获取特定的电信数据使用报告

`GET /legacy_reporting/usage_reports/number_lookup/{id}`

```ruby
number_lookup = client.legacy.reporting.usage_reports.number_lookup.retrieve("id")

puts(number_lookup)
```

## 删除电信数据使用报告

通过 ID 删除特定的电信数据使用报告

`DELETE /legacy_reporting/usage_reports/number_lookup/{id}`

```ruby
result = client.legacy.reporting.usage_reports.number_lookup.delete("id")

puts(result)
```

## 获取语音转文本使用报告

生成并同步获取语音转文本使用报告

`GET /legacy_reporting/usage_reports/speech_to_text`

```ruby
response = client.legacy.reporting.usage_reports.retrieve_speech_to_text

puts(response)
```

## 列出 CDR 使用报告

获取所有之前的 CDR 使用报告

`GET /legacy_reporting/usage_reports/voice`

```ruby
page = client.legacy.reporting.usage_reports.voice.list

puts(page)
```

## 创建新的传统使用 V2 CDR 报告请求

使用指定的过滤器创建新的传统使用 V2 CDR 报告请求

`POST /legacy_reporting/usage_reports/voice`

```ruby
voice = client.legacy.reporting.usage_reports.voice.create(
  end_time: "2024-02-01T00:00:00Z",
  start_time: "2024-02-01T00:00:00Z"
)

puts(voice)
```

## 获取 CDR 使用报告

通过 ID 获取单个 CDR 使用报告

`GET /legacy_reporting/usage_reports/voice/{id}`

```ruby
voice = client.legacy.reporting.usage_reports.voice.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(voice)
```

## 删除 V2 传统使用 CDR 报告请求

通过 ID 删除特定的 V2 传统使用 CDR 报告请求

`DELETE /legacy_reporting/usage_reports/voice/{id}`

```ruby
voice = client.legacy.reporting.usage_reports.voice.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(voice)
```

## 获取所有消息使用报告

获取所有消息使用报告

`GET /reports/mdr_usage_reports`

```ruby
page = client.reports.mdr_usage_reports.list

puts(page)
```

## 创建 MDR 使用报告

提交新的消息使用报告请求

`POST /reports/mdr_usage_reports`

```ruby
mdr_usage_report = client.reports.mdr_usage_reports.create(
  aggregation_type: :NO_AGGREGATION,
  end_date: "2020-07-01T00:00:00-06:00",
  start_date: "2020-07-01T00:00:00-06:00"
)

puts(mdr_usage_report)
```

## 获取消息使用报告

通过 ID 获取单个消息使用报告

`GET /reports/mdr_usage_reports/{id}`

```ruby
mdr_usage_report = client.reports.mdr_usage_reports.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(mdr_usage_report)
```

## 删除 MDR 使用报告

通过 ID 删除消息使用报告

`DELETE /reports/mdr_usage_reports/{id}`

```ruby
mdr_usage_report = client.reports.mdr_usage_reports.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(mdr_usage_report)
```

## 生成并获取 MDR 使用报告

同步生成并获取消息使用报告

`GET /reports/mdr_usage_reports/sync`

```ruby
response = client.reports.mdr_usage_reports.fetch_sync(aggregation_type: :PROFILE)

puts(response)
```

## 生成并获取 CDR 使用报告

同步生成并获取语音使用报告

`GET /reports/cdr_usage_reports/sync`

```ruby
response = client.reports.cdr_usage_reports.fetch_sync(
  aggregation_type: :NO_AGGREGATION,
  product_breakdown: :NO_BREAKDOWN
)

puts(response)
```

## 获取 Telnyx 产品使用数据（测试版）

按指定的维度获取 Telnyx 的使用数据

`GET /usage_reports`

```ruby
page = client.usage_reports.list(dimensions: ["string"], metrics: ["string"], product: "product")

puts(page)
```

## 获取使用报告查询选项（测试版）

获取用于查询使用情况的报告选项，包括可用的产品及其相应的指标和维度

`GET /usage_reports/options`

```ruby
response = client.usage_reports.get_options

puts(response)
```