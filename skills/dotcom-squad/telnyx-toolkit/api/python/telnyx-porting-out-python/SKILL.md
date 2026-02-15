---
name: telnyx-porting-out-python
description: >-
  Manage port-out requests when numbers are being ported away from Telnyx. List,
  view, and update port-out status. This skill provides Python SDK examples.
metadata:
  author: telnyx
  product: porting-out
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Porting Out - Python

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

以下所有示例均假设 `client` 已经按照上述方式初始化。

## 列出 portout 请求

根据过滤器返回 portout 请求

`GET /portouts`

```python
page = client.portouts.list()
page = page.data[0]
print(page.id)
```

## 获取 portout 请求

根据提供的 ID 返回 portout 请求

`GET /portouts/{id}`

```python
portout = client.portouts.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(portout.data)
```

## 获取 portout 请求的所有评论

返回 portout 请求的所有评论。

`GET /portouts/{id}/comments`

```python
comments = client.portouts.comments.list(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(comments.data)
```

## 为 portout 请求创建评论

为 portout 请求创建评论。

`POST /portouts/{id}/comments`

```python
comment = client.portouts.comments.create(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(comment.data)
```

## 获取 portout 请求的相关支持文档

列出 portout 请求的所有支持文档。

`GET /portouts/{id}/supporting_documents`

```python
supporting_documents = client.portouts.supporting_documents.list(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(supporting_documents.data)
```

## 创建 portout 请求的支持文档列表

创建 portout 请求的支持文档列表。

`POST /portouts/{id}/supporting_documents`

```python
supporting_document = client.portouts.supporting_documents.create(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(supporting_document.data)
```

## 更新状态

授权或拒绝 portout 请求

`PATCH /portouts/{id}/{status}` — 必需参数：`reason`

```python
response = client.portouts.update_status(
    status="authorized",
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    reason="I do not recognize this transaction",
)
print(response.data)
```

## 列出所有 port-out 事件

返回所有 port-out 事件的列表。

`GET /portouts/events`

```python
page = client.portouts.events.list()
page = page.data[0]
print(page)
```

## 显示 port-out 事件

显示特定的 port-out 事件。

`GET /portouts/events/{id}`

```python
event = client.portouts.events.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(event.data)
```

## 重新发布 port-out 事件

重新发布特定的 port-out 事件。

`POST /portouts/events/{id}/republish`

```python
client.portouts.events.republish(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
```

## 列出特定订单的 eligible port-out 拒绝代码

给定一个 port-out ID，列出适用于该 port-out 的拒绝代码

`GET /portouts/rejections/{portout_id}`

```python
response = client.portouts.list_rejection_codes(
    portout_id="329d6658-8f93-405d-862f-648776e8afd7",
)
print(response.data)
```

## 列出与 port-out 相关的报告

列出关于 port-out 操作生成的报告。

`GET /portouts/reports`

```python
page = client.portouts.reports.list()
page = page.data[0]
print(page.id)
```

## 创建与 port-out 相关的报告

生成关于 port-out 操作的报告。

`POST /portouts/reports`

```python
report = client.portouts.reports.create(
    params={
        "filters": {}
    },
    report_type="export_portouts_csv",
)
print(report.data)
```

## 获取报告

检索生成的特定报告。

`GET /portouts/reports/{id}`

```python
report = client.portouts.reports.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(report.data)
```