---
name: telnyx-numbers-config-ruby
description: >-
  Configure phone number settings including caller ID, call forwarding,
  messaging enablement, and connection assignments. This skill provides Ruby SDK
  examples.
metadata:
  author: telnyx
  product: numbers-config
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 数字配置 - Ruby

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

## 列出电话号码块任务

`GET /phone_number_blocks/jobs`

```ruby
page = client.phone_number_blocks.jobs.list

puts(page)
```

## 获取电话号码块任务

`GET /phone_number_blocks/jobs/{id}`

```ruby
job = client.phone_number_blocks.jobs.retrieve("id")

puts(job)
```

## 删除与电话号码块关联的所有号码

创建一个新的后台任务，以删除与给定块关联的所有电话号码。

`POST /phone_number_blocks/jobs/delete_phone_number_block` — 必需参数：`phone_number_block_id`

```ruby
response = client.phone_number_blocks.jobs.delete_phone_number_block(
  phone_number_block_id: "f3946371-7199-4261-9c3d-81a0d7935146"
)

puts(response)
```

## 列出电话号码

`GET /phone_numbers`

```ruby
page = client.phone_numbers.list

puts(page)
```

## 获取电话号码

`GET /phone_numbers/{id}`

```ruby
phone_number = client.phone_numbers.retrieve("1293384261075731499")

puts(phone_number)
```

## 更新电话号码

`PATCH /phone_numbers/{id}`

```ruby
phone_number = client.phone_numbers.update("1293384261075731499")

puts(phone_number)
```

## 删除电话号码

`DELETE /phone_numbers/{id}`

```ruby
phone_number = client.phone_numbers.delete("1293384261075731499")

puts(phone_number)
```

## 更改电话号码的捆绑状态（将其添加到捆绑中或从捆绑中移除）

`PATCH /phone_numbers/{id}/actions/bundle_status_change` — 必需参数：`bundle_id`

```ruby
response = client.phone_numbers.actions.change_bundle_status(
  "1293384261075731499",
  bundle_id: "5194d8fc-87e6-4188-baa9-1c434bbe861b"
)

puts(response)
```

## 为电话号码启用紧急呼叫功能

`POST /phone_numbers/{id}/actions/enable_emergency` — 必需参数：`emergency_enabled`, `emergency_address_id`

```ruby
response = client.phone_numbers.actions.enable_emergency(
  "1293384261075731499",
  emergency_address_id: "53829456729313",
  emergency_enabled: true
)

puts(response)
```

## 获取带有语音设置的电话号码

`GET /phone_numbers/{id}/voice`

```ruby
voice = client.phone_numbers.voice.retrieve("1293384261075731499")

puts(voice)
```

## 更新带有语音设置的电话号码

`PATCH /phone_numbers/{id}/voice`

```ruby
voice = client.phone_numbers.voice.update("1293384261075731499")

puts(voice)
```

## 验证电话号码的所有权

验证提供的电话号码的所有权，并返回号码与其 ID 的映射关系，以及未在账户中找到的号码列表。

`POST /phone_numbers/actions/verify_ownership` — 必需参数：`phone_numbers`

```ruby
response = client.phone_numbers.actions.verify_ownership(phone_numbers: ["+15551234567"])

puts(response)
```

## 列出 CSV 下载内容

`GET /phone_numbers/csv_downloads`

```ruby
page = client.phone_numbers.csv_downloads.list

puts(page)
```

## 创建 CSV 下载文件

`POST /phone_numbers/csv_downloads`

```ruby
csv_download = client.phone_numbers.csv_downloads.create

puts(csv_download)
```

## 获取 CSV 下载文件

`GET /phone_numbers/csv_downloads/{id}`

```ruby
csv_download = client.phone_numbers.csv_downloads.retrieve("id")

puts(csv_download)
```

## 列出电话号码任务

`GET /phone_numbers/jobs`

```ruby
page = client.phone_numbers.jobs.list

puts(page)
```

## 获取电话号码任务

`GET /phone_numbers/jobs/{id}`

```ruby
job = client.phone_numbers.jobs.retrieve("id")

puts(job)
```

## 删除一批电话号码

创建一个新的后台任务，以删除一批电话号码。

`POST /phone_numbers/jobs/delete_phone_numbers` — 必需参数：`phone_numbers`

```ruby
response = client.phone_numbers.jobs.delete_batch(phone_numbers: ["+19705555098", "+19715555098", "32873127836"])

puts(response)
```

## 更新一批电话号码的紧急呼叫设置

创建一个新的后台任务，以更新一组电话号码的紧急呼叫设置。

`POST /phone_numbers/jobs/update_emergency_settings` — 必需参数：`emergency_enabled`, `phone_numbers`

```ruby
response = client.phone_numbers.jobs.update_emergency_settings_batch(
  emergency_enabled: true,
  phone_numbers: ["+19705555098", "+19715555098", "32873127836"]
)

puts(response)
```

## 更新一批电话号码

创建一个新的后台任务，以更新一批电话号码。

`POST /phone_numbers/jobs/update_phone_numbers` — 必需参数：`phone_numbers`

```ruby
response = client.phone_numbers.jobs.update_batch(phone_numbers: ["1583466971586889004", "+13127367254"])

puts(response)
```

## 获取一组电话号码的监管要求信息

`GET /phone_numbers/regulatory_requirements`

```ruby
phone_numbers_regulatory_requirement = client.phone_numbers_regulatory_requirements.retrieve

puts(phone_numbers_regulatory_requirement)
```

## 简化版电话号码列表

列出电话号码。此端点是 `/phone_numbers` 端点的简化版本，具有更高的性能和速率限制。

`GET /phone_numbers/slim`

```ruby
page = client.phone_numbers.slim_list

puts(page)
```

## 列出带有语音设置的电话号码

`GET /phone_numbers/voice`

```ruby
page = client.phone_numbers.voice.list

puts(page)
```

## 列出手机号码

`GET /v2/mobile_phone_numbers`

```ruby
page = client.mobile_phone_numbers.list

puts(page)
```

## 获取手机号码

`GET /v2/mobile_phone_numbers/{id}`

```ruby
mobile_phone_number = client.mobile_phone_numbers.retrieve("id")

puts(mobile_phone_number)
```

## 更新手机号码

`PATCH /v2/mobile_phone_numbers/{id}`

```ruby
mobile_phone_number = client.mobile_phone_numbers.update("id")

puts(mobile_phone_number)
```