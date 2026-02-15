---
name: telnyx-porting-out-ruby
description: >-
  Manage port-out requests when numbers are being ported away from Telnyx. List,
  view, and update port-out status. This skill provides Ruby SDK examples.
metadata:
  author: telnyx
  product: porting-out
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Porting Out - Ruby

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

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出 portout 请求

根据过滤器返回 portout 请求

`GET /portouts`

```ruby
page = client.portouts.list

puts(page)
```

## 获取 portout 请求

根据提供的 ID 返回 portout 请求

`GET /portouts/{id}`

```ruby
portout = client.portouts.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(portout)
```

## 查看 portout 请求的评论

返回 portout 请求的所有评论

`GET /portouts/{id}/comments`

```ruby
comments = client.portouts.comments.list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(comments)
```

## 为 portout 请求添加评论

为 portout 请求创建评论

`POST /portouts/{id}/comments`

```ruby
comment = client.portouts.comments.create("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(comment)
```

## 查看 portout 请求的辅助文档

列出 portout 请求的所有辅助文档

`GET /portouts/{id}/supporting_documents`

```ruby
supporting_documents = client.portouts.supporting_documents.list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(supporting_documents)
```

## 创建 portout 请求的辅助文档

为 portout 请求创建辅助文档列表

`POST /portouts/{id}/supporting_documents`

```ruby
supporting_document = client.portouts.supporting_documents.create("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(supporting_document)
```

## 更新状态

授权或拒绝 portout 请求

`PATCH /portouts/{id}/{status}` — 必需参数：`reason`

```ruby
response = client.portouts.update_status(
  :authorized,
  id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  reason: "I do not recognize this transaction"
)

puts(response)
```

## 列出所有 port-out 事件

返回所有 port-out 事件的列表

`GET /portouts/events`

```ruby
page = client.portouts.events.list

puts(page)
```

## 查看特定的 port-out 事件

显示特定的 port-out 事件

`GET /portouts/events/{id}`

```ruby
event = client.portouts.events.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(event)
```

## 重新发布 port-out 事件

重新发布特定的 port-out 事件

`POST /portouts/events/{id}/republish`

```ruby
result = client.portouts.events.republish("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(result)
```

## 查看特定订单的 port-out 拒绝代码

根据 port-out ID，列出适用于该订单的拒绝代码

`GET /portouts/rejections/{portout_id}`

```ruby
response = client.portouts.list_rejection_codes("329d6658-8f93-405d-862f-648776e8afd7")

puts(response)
```

## 查看 port-out 相关报告

列出关于 port-out 操作生成的报告

`GET /portouts/reports`

```ruby
page = client.portouts.reports.list

puts(page)
```

## 创建 port-out 相关报告

生成关于 port-out 操作的报告

`POST /portouts/reports`

```ruby
report = client.portouts.reports.create(params: {filters: {}}, report_type: :export_portouts_csv)

puts(report)
```

## 获取报告

检索特定生成的报告

`GET /portouts/reports/{id}`

```ruby
report = client.portouts.reports.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(report)
```