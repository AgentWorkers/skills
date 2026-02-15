---
name: telnyx-numbers-compliance-ruby
description: >-
  Manage regulatory requirements, number bundles, supporting documents, and
  verified numbers for compliance. This skill provides Ruby SDK examples.
metadata:
  author: telnyx
  product: numbers-compliance
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 数字合规性 - Ruby

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

## 获取套餐信息

获取所有允许的套餐信息。

`GET /bundle_pricing/billing_bundles`

```ruby
page = client.bundle_pricing.billing_bundles.list

puts(page)
```

## 根据 ID 获取套餐

根据 ID 获取单个套餐。

`GET /bundle_pricing/billing_bundles/{bundle_id}`

```ruby
billing_bundle = client.bundle_pricing.billing_bundles.retrieve("8661948c-a386-4385-837f-af00f40f111a")

puts(billing_bundle)
```

## 获取用户套餐

获取分页显示的用户套餐列表。

`GET /bundle_pricing/user_bundles`

```ruby
page = client.bundle_pricing.user_bundles.list

puts(page)
```

## 创建用户套餐

为用户创建多个套餐。

`POST /bundle_pricing/user_bundles/bulk`

```ruby
user_bundle = client.bundle_pricing.user_bundles.create

puts(user_bundle)
```

## 获取未使用的用户套餐

返回所有未使用的用户套餐。

`GET /bundle_pricing/user_bundles/unused`

```ruby
response = client.bundle_pricing.user_bundles.list_unused

puts(response)
```

## 根据 ID 获取用户套餐

根据 ID 获取用户套餐。

`GET /bundle_pricing/user_bundles/{user_bundle_id}`

```ruby
user_bundle = client.bundle_pricing.user_bundles.retrieve("ca1d2263-d1f1-43ac-ba53-248e7a4bb26a")

puts(user_bundle)
```

## 取消激活用户套餐

根据 ID 取消激活用户套餐。

`DELETE /bundle_pricing/user_bundles/{user_bundle_id}`

```ruby
response = client.bundle_pricing.user_bundles.deactivate("ca1d2263-d1f1-43ac-ba53-248e7a4bb26a")

puts(response)
```

## 获取用户套餐资源

根据 ID 获取用户套餐的资源信息。

`GET /bundle_pricing/user_bundles/{user_bundle_id}/resources`

```ruby
response = client.bundle_pricing.user_bundles.list_resources("ca1d2263-d1f1-43ac-ba53-248e7a4bb26a")

puts(response)
```

## 列出所有文档链接

按创建时间降序列出所有文档链接。

`GET /document_links`

```ruby
page = client.document_links.list

puts(page)
```

## 列出所有文档

按创建时间降序列出所有文档。

`GET /documents`

```ruby
page = client.documents.list

puts(page)
```

## 上传文档

上传文档。<br /><br />上传的文件必须在 30 分钟内关联到某个服务，否则将被自动删除。

`POST /documents`

```ruby
response = client.documents.upload_json(document: {})

puts(response)
```

## 获取文档

获取文档信息。

`GET /documents/{id}`

```ruby
document = client.documents.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(document)
```

## 更新文档

更新文档内容。

`PATCH /documents/{id}`

```ruby
document = client.documents.update("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(document)
```

## 删除文档

删除文档。<br /><br />只有未关联到任何服务的文档才能被删除。

`DELETE /documents/{id}`

```ruby
document = client.documents.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(document)
```

## 下载文档

下载文档。

`GET /documents/{id}/download`

```ruby
response = client.documents.download("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(response)
```

## 生成文档的临时下载链接

生成一个临时预签名 URL，可以直接从存储后端下载文档（无需认证）。

`GET /documents/{id}/download_link`

```ruby
response = client.documents.generate_download_link("550e8400-e29b-41d4-a716-446655440000")

puts(response)
```

## 列出所有需求

支持过滤、排序和分页功能，列出所有需求。

`GET /requirements`

```ruby
page = client.requirements.list

puts(page)
```

## 获取需求记录

根据 ID 获取需求记录。

`GET /requirements/{id}`

```ruby
requirement = client.requirements.retrieve("a9dad8d5-fdbd-49d7-aa23-39bb08a5ebaa")

puts(requirement)
```

## 列出所有需求类型

按创建时间降序列出所有需求类型。

`GET /requirement_types`

```ruby
requirement_types = client.requirement_types.list

puts(requirement_types)
```

## 根据 ID 获取需求类型

根据 ID 获取需求类型。

`GET /requirement_types/{id}`

```ruby
requirement_type = client.requirement_types.retrieve("a38c217a-8019-48f8-bff6-0fdd9939075b")

puts(requirement_type)
```

## 获取监管要求

获取所有监管要求信息。

`GET /regulatory_requirements`

```ruby
regulatory_requirement = client.regulatory_requirements.retrieve

puts(regulatory_requirement)
```

## 列出需求组

列出所有需求组。

`GET /requirement_groups`

```ruby
requirement_groups = client.requirement_groups.list

puts(requirement_groups)
```

## 创建新的需求组

创建新的需求组。<br />必需参数：`country_code`、`phone_number_type`、`action`

```ruby
requirement_group = client.requirement_groups.create(action: :ordering, country_code: "US", phone_number_type: :local)

puts(requirement_group)
```

## 根据 ID 获取单个需求组

根据 ID 获取单个需求组。

`GET /requirement_groups/{id}`

```ruby
requirement_group = client.requirement_groups.retrieve("id")

puts(requirement_group)
```

## 更新需求组中的需求信息

更新需求组中的需求信息。

`PATCH /requirement_groups/{id}`

```ruby
requirement_group = client.requirement_groups.update("id")

puts(requirement_group)
```

## 根据 ID 删除需求组

根据 ID 删除需求组。

`DELETE /requirement_groups/{id}`

```ruby
requirement_group = client.requirement_groups.delete("id")

puts(requirement_group)
```

## 提交需求组以供审批

提交需求组以供审批。

`POST /requirement_groups/{id}/submit_for_approval`

```ruby
requirement_group = client.requirement_groups.submit_for_approval("id")

puts(requirement_group)
```

## 列出所有已验证的号码

获取已验证号码的分页列表。

`GET /verified_numbers`

```ruby
page = client.verified_numbers.list

puts(page)
```

## 请求电话号码验证

启动电话号码验证流程。

`POST /verified_numbers` — 必需参数：`phone_number`、`verification_method`

```ruby
verified_number = client.verified_numbers.create(phone_number: "+15551234567", verification_method: :sms)

puts(verified_number)
```

## 获取已验证的号码

获取已验证的号码信息。

`GET /verified_numbers/{phone_number}`

```ruby
verified_number_data_wrapper = client.verified_numbers.retrieve("+15551234567")

puts(verified_number_data_wrapper)
```

## 删除已验证的号码

删除已验证的号码。

`DELETE /verified_numbers/{phone_number}`

```ruby
verified_number_data_wrapper = client.verified_numbers.delete("+15551234567")

puts(verified_number_data_wrapper)
```

## 提交验证码

提交验证码。

`POST /verified_numbers/{phone_number}/actions/verify` — 必需参数：`verification_code`

```ruby
verified_number_data_wrapper = client.verified_numbers.actions.submit_verification_code("+15551234567", verification_code: "123456")

puts(verified_number_data_wrapper)
```