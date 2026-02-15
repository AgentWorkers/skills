---
name: telnyx-porting-in-ruby
description: >-
  Port phone numbers into Telnyx. Check portability, create port orders, upload
  LOA documents, and track porting status. This skill provides Ruby SDK
  examples.
metadata:
  author: telnyx
  product: porting-in
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 的端口迁移功能（使用 Ruby 实现）

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

以下所有示例均假设 `client` 已经按照上述方式初始化。

## 列出所有端口迁移事件

返回所有端口迁移事件的列表。

`GET /porting/events`

```ruby
page = client.porting.events.list

puts(page)
```

## 显示特定端口迁移事件

显示特定的端口迁移事件。

`GET /porting/events/{id}`

```ruby
event = client.porting.events.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(event)
```

## 重新发布端口迁移事件

重新发布特定的端口迁移事件。

`POST /porting/events/{id}/republish`

```ruby
result = client.porting.events.republish("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(result)
```

## 预览 LOA 配置参数

预览生成的 LOA 模板，无需创建实际的 LOA 配置。

`POST /porting/loa_configuration_preview`

```ruby
response = client.porting.loa_configurations.preview_0(
  address: {city: "Austin", country_code: "US", state: "TX", street_address: "600 Congress Avenue", zip_code: "78701"},
  company_name: "Telnyx",
  contact: {email: "testing@client.com", phone_number: "+12003270001"},
  logo: {document_id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"},
  name: "My LOA Configuration"
)

puts(response)
```

## 列出 LOA 配置

列出所有的 LOA 配置。

`GET /porting/loa_configurations`

```ruby
page = client.porting.loa_configurations.list

puts(page)
```

## 创建 LOA 配置

创建一个新的 LOA 配置。

`POST /porting/loa_configurations`

```ruby
loa_configuration = client.porting.loa_configurations.create(
  address: {city: "Austin", country_code: "US", state: "TX", street_address: "600 Congress Avenue", zip_code: "78701"},
  company_name: "Telnyx",
  contact: {email: "testing@client.com", phone_number: "+12003270001"},
  logo: {document_id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"},
  name: "My LOA Configuration"
)

puts(loa_configuration)
```

## 获取 LOA 配置

获取特定的 LOA 配置。

`GET /porting/loa_configurations/{id}`

```ruby
loa_configuration = client.porting.loa_configurations.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(loa_configuration)
```

## 更新 LOA 配置

更新特定的 LOA 配置。

`PATCH /porting/loa_configurations/{id}`

```ruby
loa_configuration = client.porting.loa_configurations.update(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  address: {city: "Austin", country_code: "US", state: "TX", street_address: "600 Congress Avenue", zip_code: "78701"},
  company_name: "Telnyx",
  contact: {email: "testing@client.com", phone_number: "+12003270001"},
  logo: {document_id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"},
  name: "My LOA Configuration"
)

puts(loa_configuration)
```

## 删除 LOA 配置

删除特定的 LOA 配置。

`DELETE /porting/loa_configurations/{id}`

```ruby
result = client.porting.loa_configurations.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(result)
```

## 预览 LOA 配置

预览特定的 LOA 配置。

`GET /porting/loa_configurations/{id}/preview`

```ruby
response = client.porting.loa_configurations.preview_1("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(response)
```

## 列出所有端口迁移订单

返回所有端口迁移订单的列表。

`GET /porting_orders`

```ruby
page = client.porting_orders.list

puts(page)
```

## 创建端口迁移订单

创建一个新的端口迁移订单。

`POST /porting_orders` — 必需参数：`phone_numbers`

```ruby
porting_order = client.porting_orders.create(phone_numbers: ["+13035550000", "+13035550001", "+13035550002"])

puts(porting_order)
```

## 获取端口迁移订单详情

获取现有端口迁移订单的详细信息。

`GET /porting_orders/{id}`

```ruby
porting_order = client.porting_orders.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(porting_order)
```

## 修改端口迁移订单

修改现有端口迁移订单的详细信息。

`PATCH /porting_orders/{id}`

```ruby
porting_order = client.porting_orders.update("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(porting_order)
```

## 删除端口迁移订单

删除现有的端口迁移订单。

`DELETE /porting_orders/{id}`

```ruby
result = client.porting_orders.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(result)
```

## 异步激活端口迁移订单中的每个号码

异步激活端口迁移订单中的每个号码。

`POST /porting_orders/{id}/actions/activate`

```ruby
response = client.porting_orders.actions.activate("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(response)
```

## 取消端口迁移订单

取消端口迁移订单。

`POST /porting_orders/{id}/actions/cancel`

```ruby
response = client.porting_orders.actions.cancel("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(response)
```

## 提交端口迁移订单

确认并提交端口迁移订单。

`POST /porting_orders/{id}/actions/confirm`

```ruby
response = client.porting_orders.actions.confirm("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(response)
```

## 共享端口迁移订单

为端口迁移订单创建共享令牌。

`POST /porting_orders/{id}/actions/share`

```ruby
response = client.porting_orders.actions.share("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(response)
```

## 列出所有端口迁移激活任务

返回所有端口迁移激活任务的列表。

`GET /porting/orders/{id}/activation_jobs`

```ruby
page = client.porting_orders.activation_jobs.list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(page)
```

## 获取端口迁移激活任务详情

获取特定的端口迁移激活任务的详细信息。

`GET /porting/orders/{id}/activation_jobs/{activationJobId}`

```ruby
activation_job = client.porting_orders.activation_jobs.retrieve(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
)

puts(activation_job)
```

## 更新端口迁移激活任务

更新端口迁移激活任务的激活时间。

`PATCH /porting/orders/{id}/activation_jobs/{activationJobId}`

```ruby
activation_job = client.porting_orders.activation_jobs.update(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
)

puts(activation_job)
```

## 列出所有附加文档

返回端口迁移订单的所有附加文档的列表。

`GET /porting/orders/{id}/additional_documents`

```ruby
page = client.porting_orders.additional_documents.list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(page)
```

## 创建附加文档列表

为端口迁移订单创建附加文档的列表。

`POST /porting/orders/{id}/additional_documents`

```ruby
additional_document = client.porting_orders.additional_documents.create("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(additional_document)
```

## 删除附加文档

删除端口迁移订单中的附加文档。

`DELETE /porting/orders/{id}/additional_documents/{additional_document_id}`

```ruby
result = client.porting_orders.additional_documents.delete(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
)

puts(result)
```

## 列出允许的 FOC 日期

返回端口迁移订单允许的 FOC 日期列表。

`GET /porting/orders/{id}/allowed_foc_windows`

```ruby
response = client.porting_orders.retrieve_allowed_foc_windows("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(response)
```

## 列出端口迁移订单的所有评论

返回端口迁移订单的所有评论列表。

`GET /porting/orders/{id}/comments`

```ruby
page = client.porting_orders.comments.list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(page)
```

## 为端口迁移订单创建评论

为端口迁移订单创建新的评论。

`POST /porting/orders/{id}/comments`

```ruby
comment = client.porting_orders.comments.create("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(comment)
```

## 下载端口迁移订单的 LOA 模板

下载端口迁移订单的 LOA 模板。

`GET /porting/orders/{id}/loa_template`

```ruby
response = client.porting_orders.retrieve_loa_template("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(response)
```

## 列出端口迁移订单的需求

根据国家/号码类型，返回该订单的所有需求列表。

`GET /porting/orders/{id}/requirements`

```ruby
page = client.porting_orders.retrieve_requirements("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(page)
```

## 获取关联的 V1 子请求 ID 和端口请求 ID

获取与端口迁移订单关联的 V1 子请求 ID 和端口请求 ID。

`GET /porting/orders/{id}/sub_request`

```ruby
response = client.porting_orders.retrieve_sub_request("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(response)
```

## 获取验证代码

返回端口迁移订单的所有验证代码列表。

`GET /porting/orders/{id}/verification_codes`

```ruby
page = client.porting_orders.verification_codes.list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(page)
```

## 发送验证代码

为所有端口迁移号码发送验证代码。

`POST /porting/orders/{id}/verification_codes/send`

```ruby
result = client.porting_orders.verification_codes.send_("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(result)
```

## 验证一系列号码的验证代码

验证一系列号码的验证代码。

`POST /porting/orders/{id}/verification_codes/verify`

```ruby
response = client.porting_orders.verification_codes.verify("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(response)
```

## 列出端口迁移订单的操作需求

返回特定端口迁移订单的操作需求列表。

`GET /porting_orders/{porting_order_id}/action_requirements`

```ruby
page = client.porting_orders.action_requirements.list("porting_order_id")

puts(page)
```

## 启动操作需求

为特定端口迁移订单启动操作需求。

`POST /porting_orders/{porting_order_id}/action_requirements/{id}/initiate`

```ruby
response = client.porting_orders.action_requirements.initiate(
  "id",
  porting_order_id: "porting_order_id",
  params: {first_name: "John", last_name: "Doe"}
)

puts(response)
```

## 列出所有关联的号码

返回与端口迁移订单关联的所有号码的列表。

`GET /porting_orders/{id}/associated_phone_numbers`

```ruby
page = client.porting_orders.associated_phone_numbers.list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(page)
```

## 创建关联的号码

为端口迁移订单创建新的关联号码。

`POST /porting_orders/{id}/associated_phone_numbers`

```ruby
associated_phone_number = client.porting_orders.associated_phone_numbers.create(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  action: :keep,
  phone_number_range: {}
)

puts(associated_phone_number)
```

## 删除关联的号码

从端口迁移订单中删除关联的号码。

`DELETE /porting/orders/{id}/associated_phone_numbers/{id}`

```ruby
associated_phone_number = client.porting_orders.associated_phone_numbers.delete(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  porting_order_id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
)

puts(associated_phone_number)
```

## 列出所有号码块

返回端口迁移订单中的所有号码块列表。

`GET /porting_orders/{id}/phone_number_blocks`

```ruby
page = client.porting_orders.phone_number_blocks.list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(page)
```

## 创建号码块

为端口迁移订单创建新的号码块。

`POST /porting_orders/{id}/phone_number_blocks`

```ruby
phone_number_block = client.porting_orders.phone_number_blocks.create(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  activation_ranges: [{end_at: "+4930244999910", start_at: "+4930244999901"}],
  phone_number_range: {end_at: "+4930244999910", start_at: "+4930244999901"}
)

puts(phone_number_block)
```

## 删除号码块

删除端口迁移订单中的号码块。

`DELETE /porting_orders/{id}/phone_number_blocks/{id}`

```ruby
phone_number_block = client.porting_orders.phone_number_blocks.delete(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  porting_order_id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
)

puts(phone_number_block)
```

## 列出所有号码扩展码

返回端口迁移订单中的所有号码扩展码列表。

`GET /porting_orders/{id}/phone_numberextensions`

```ruby
page = client.porting_orders.phone_number_extensions.list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(page)
```

## 创建号码扩展码

为端口迁移订单创建新的号码扩展码。

`POST /porting_orders/{id}/phone_number_extensions`

```ruby
phone_number_extension = client.porting_orders.phone_number_extensions.create(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  activation_ranges: [{end_at: 10, start_at: 1}],
  extension_range: {end_at: 10, start_at: 1},
  porting_phone_number_id: "f24151b6-3389-41d3-8747-7dd8c681e5e2"
)

puts(phone_number_extension)
```

## 删除号码扩展码

删除端口迁移订单中的号码扩展码。

`DELETE /porting_orders/{id}/phone_number_extensions/{id}`

```ruby
phone_number_extension = client.porting_orders.phone_number_extensions.delete(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  porting_order_id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
)

puts(phone_number_extension)
```

## 列出所有可能的异常类型

返回端口迁移订单的所有可能异常类型列表。

`GET /porting_orders/exception_types`

```ruby
response = client.porting_orders.retrieve_exception_types

puts(response)
```

## 列出所有号码配置

分页显示端口迁移订单的所有号码配置。

`GET /porting/orders/phone_number_configurations`

```ruby
page = client.porting_orders.phone_number_configurations.list

puts(page)
```

## 创建号码配置列表

创建号码配置的列表。

`POST /porting_orders/phone_number_configurations`

```ruby
phone_number_configuration = client.porting_orders.phone_number_configurations.create

puts(phone_number_configuration)
```

## 列出所有迁移中的号码

返回所有迁移中的号码列表。

`GET /porting/phone_numbers`

```ruby
page = client.porting_phone_numbers.list

puts(page)
```

## 列出与端口迁移相关的报告

列出关于端口迁移操作的报告。

`GET /porting/reports`

```ruby
page = client.porting.reports.list

puts(page)
```

## 创建与端口迁移相关的报告

生成关于端口迁移操作的报告。

`POST /porting/reports`

```ruby
report = client.porting.reports.create(params: {filters: {}}, report_type: :export_porting_orders_csv)

puts(report)
```

## 获取报告

获取特定生成的报告。

`GET /porting/reports/{id}`

```ruby
report = client.porting.reports.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(report)
```

## 列出英国的可用运营商

列出英国的可用运营商。

`GET /porting/uk_carriers`

```ruby
response = client.porting.list_uk_carriers

puts(response)
```

## 运行端口迁移检查

立即运行端口迁移检查并返回结果。

`POST /portability_checks`

```ruby
response = client.portability_checks.run

puts(response)
```
```