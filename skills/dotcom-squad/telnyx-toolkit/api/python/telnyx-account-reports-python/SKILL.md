---
name: telnyx-account-reports-python
description: >-
  Generate and retrieve usage reports for billing, analytics, and
  reconciliation. This skill provides Python SDK examples.
metadata:
  author: telnyx
  product: account-reports
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户报告 - Python

## 安装

```bash
pip install telnyx
```

## 设置

```python
import os
from telnyx import Telnyx

client = Telnyx(
    api_key=os.environ.get("TELNYX_API_KEY"),  # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 获取所有 MDR 详细报告请求

检索已认证用户的所有 MDR 详细报告请求

`GET /legacy_reporting/batch_detail_records/messaging`

```python
messagings = client.legacy.reporting.batch_detail_records.messaging.list()
print(messagings.data)
```

## 创建新的 MDR 详细报告请求

使用指定的过滤器创建新的 MDR 详细报告请求

`POST /legacy_reporting/batch_detail_records/messaging` — 必需参数：`start_time`、`end_time`

```python
from datetime import datetime

messaging = client.legacy.reporting.batch_detail_records.messaging.create(
    end_time=datetime.fromisoformat("2024-02-12T23:59:59"),
    start_time=datetime.fromisoformat("2024-02-01T00:00:00"),
)
print(messaging.data)
```

## 获取特定的 MDR 详细报告请求

通过 ID 获取特定的 MDR 详细报告请求

`GET /legacy_reporting/batch_detail_records/messaging/{id}`

```python
messaging = client.legacy.reporting.batch_detail_records.messaging.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(messaging.data)
```

## 删除 MDR 详细报告请求

通过 ID 删除特定的 MDR 详细报告请求

`DELETE /legacy_reporting/batch_detail_records/messaging/{id}`

```python
messaging = client.legacy.reporting.batch_detail_records.messaging.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(messaging.data)
```

## 获取所有 CDR 报告请求

检索已认证用户的所有 CDR 报告请求

`GET /legacy_reporting/batch_detail_records/voice`

```python
voices = client.legacy.reporting.batch_detail_records.voice.list()
print(voices.data)
```

## 创建新的 CDR 报告请求

使用指定的过滤器创建新的 CDR 报告请求

`POST /legacy_reporting/batch_detail_records/voice` — 必需参数：`start_time`、`end_time`

```python
from datetime import datetime

voice = client.legacy.reporting.batch_detail_records.voice.create(
    end_time=datetime.fromisoformat("2024-02-12T23:59:59"),
    start_time=datetime.fromisoformat("2024-02-01T00:00:00"),
)
print(voice.data)
```

## 获取特定的 CDR 报告请求

通过 ID 获取特定的 CDR 报告请求

`GET /legacy_reporting/batch_detail_records/voice/{id}`

```python
voice = client.legacy.reporting.batch_detail_records.voice.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(voice.data)
```

## 删除 CDR 报告请求

通过 ID 删除特定的 CDR 报告请求

`DELETE /legacy_reporting/batch_detail_records/voice/{id}`

```python
voice = client.legacy.reporting.batch_detail_records.voice.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(voice.data)
```

## 获取可用的 CDR 报告字段

检索可用于 CDR 报告的所有可用字段

`GET /legacy_reporting/batch_detail_records/voice/fields`

```python
response = client.legacy.reporting.batch_detail_records.voice.retrieve_fields()
print(response.billing)
```

## 列出 MDR 使用报告

获取所有之前的 MDR 使用报告请求

`GET /legacy_reporting/usage_reports/messaging`

```python
page = client.legacy.reporting.usage_reports.messaging.list()
page = page.data[0]
print(page.id)
```

## 创建新的传统使用 V2 MDR 报告请求

使用指定的过滤器创建新的传统使用 V2 MDR 报告请求

`POST /legacy_reporting/usage_reports/messaging`

```python
messaging = client.legacy.reporting.usage_reports.messaging.create(
    aggregation_type=0,
)
print(messaging.data)
```

## 获取 MDR 使用报告

通过 ID 获取单个 MDR 使用报告

`GET /legacy_reporting/usage_reports/messaging/{id}`

```python
messaging = client.legacy.reporting.usage_reports.messaging.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(messaging.data)
```

## 删除 V2 传统使用 MDR 报告请求

通过 ID 删除特定的 V2 传统使用 MDR 报告请求

`DELETE /legacy_reporting/usage_reports/messaging/{id}`

```python
messaging = client.legacy.reporting.usage_reports.messaging.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(messaging.data)
```

## 列出电信数据使用报告

获取分页的电信数据使用报告列表

`GET /legacy_reporting/usage_reports/number_lookup`

```python
number_lookups = client.legacy.reporting.usage_reports.number_lookup.list()
print(number_lookups.data)
```

## 提交电信数据使用报告

提交新的电信数据使用报告

`POST /legacy_reporting/usage_reports/number_lookup`

```python
number_lookup = client.legacy.reporting.usage_reports.number_lookup.create()
print(number_lookup.data)
```

## 通过 ID 获取电信数据使用报告

通过 ID 获取特定的电信数据使用报告

`GET /legacy_reporting/usage_reports/number_lookup/{id}`

```python
number_lookup = client.legacy.reporting.usage_reports.number_lookup.retrieve(
    "id",
)
print(number_lookup.data)
```

## 删除电信数据使用报告

通过 ID 删除特定的电信数据使用报告

`DELETE /legacy_reporting/usage_reports/number_lookup/{id}`

```python
client.legacy.reporting.usage_reports.number_lookup.delete(
    "id",
)
```

## 获取语音转文本使用报告

生成并同步获取语音转文本使用报告

`GET /legacy_reporting/usage_reports/speech_to_text`

```python
response = client.legacy.reporting.usage_reports.retrieve_speech_to_text()
print(response.data)
```

## 列出 CDR 使用报告

获取所有之前的 CDR 使用报告请求

`GET /legacy_reporting/usage_reports/voice`

```python
page = client.legacy.reporting.usage_reports.voice.list()
page = page.data[0]
print(page.id)
```

## 创建新的传统使用 V2 CDR 报告请求

使用指定的过滤器创建新的传统使用 V2 CDR 报告请求

`POST /legacy_reporting/usage_reports/voice`

```python
from datetime import datetime

voice = client.legacy.reporting.usage_reports.voice.create(
    end_time=datetime.fromisoformat("2024-02-01T00:00:00"),
    start_time=datetime.fromisoformat("2024-02-01T00:00:00"),
)
print(voice.data)
```

## 获取 CDR 使用报告

通过 ID 获取单个 CDR 使用报告

`GET /legacy_reporting/usage_reports/voice/{id}`

```python
voice = client.legacy.reporting.usage_reports.voice.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(voice.data)
```

## 删除 V2 传统使用 CDR 报告请求

通过 ID 删除特定的 V2 传统使用 CDR 报告请求

`DELETE /legacy_reporting/usage_reports/voice/{id}`

```python
voice = client.legacy.reporting.usage_reports.voice.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(voice.data)
```

## 获取所有消息使用报告

获取所有消息使用报告

`GET /reports/mdr_usage_reports`

```python
page = client.reports.mdr_usage_reports.list()
page = page.data[0]
print(page.id)
```

## 创建 MDR 使用报告

提交新的消息使用报告请求

`POST /reports/mdr_usage_reports`

```python
from datetime import datetime

mdr_usage_report = client.reports.mdr_usage_reports.create(
    aggregation_type="NO_AGGREGATION",
    end_date=datetime.fromisoformat("2020-07-01T00:00:00-06:00"),
    start_date=datetime.fromisoformat("2020-07-01T00:00:00-06:00"),
)
print(mdr_usage_report.data)
```

## 获取消息使用报告

通过 ID 获取单个消息使用报告

`GET /reports/mdr_usage_reports/{id}`

```python
mdr_usage_report = client.reports.mdr_usage_reports.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(mdr_usage_report.data)
```

## 删除 MDR 使用报告

通过 ID 删除消息使用报告

`DELETE /reports/mdr_usage_reports/{id}`

```python
mdr_usage_report = client.reports.mdr_usage_reports.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(mdr_usage_report.data)
```

## 生成并获取 MDR 使用报告

同步生成并获取消息使用报告

`GET /reports/mdr_usage_reports/sync`

```python
response = client.reports.mdr_usage_reports.fetch_sync(
    aggregation_type="PROFILE",
)
print(response.data)
```

## 生成并获取 CDR 使用报告

同步生成并获取语音使用报告

`GET /reports/cdr_usage_reports/sync`

```python
response = client.reports.cdr_usage_reports.fetch_sync(
    aggregation_type="NO_AGGREGATION",
    product_breakdown="NO_BREAKDOWN",
)
print(response.data)
```

## 获取 Telnyx 产品使用数据（测试版）

按指定维度获取 Telnyx 的使用数据

`GET /usage_reports`

```python
page = client.usage_reports.list(
    dimensions=["string"],
    metrics=["string"],
    product="product",
)
page = page.data[0]
print(page)
```

## 获取使用报告查询选项（测试版）

获取用于查询使用情况的报告选项，包括可用的产品及其相应的指标和维度

`GET /usage_reports/options`

```python
response = client.usage_reports.get_options()
print(response.data)
```