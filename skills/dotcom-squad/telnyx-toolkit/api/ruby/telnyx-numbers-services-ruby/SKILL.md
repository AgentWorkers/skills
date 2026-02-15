---
name: telnyx-numbers-services-ruby
description: >-
  Configure voicemail, voice channels, and emergency (E911) services for your
  phone numbers. This skill provides Ruby SDK examples.
metadata:
  author: telnyx
  product: numbers-services
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 数字服务 - Ruby

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

## 列出动态紧急地址

根据过滤器返回动态紧急地址

`GET /dynamic_emergency_addresses`

```ruby
page = client.dynamic_emergency_addresses.list

puts(page)
```

## 创建动态紧急地址

创建一个动态紧急地址。

`POST /dynamic_emergency_addresses` — 必需参数：`house_number`、`street_name`、`locality`、`administrative_area`、`postal_code`、`country_code`

```ruby
dynamic_emergency_address = client.dynamic_emergency_addresses.create(
  administrative_area: "TX",
  country_code: :US,
  house_number: "600",
  locality: "Austin",
  postal_code: "78701",
  street_name: "Congress"
)

puts(dynamic_emergency_address)
```

## 获取动态紧急地址

根据提供的 ID 返回动态紧急地址

`GET /dynamic_emergency_addresses/{id}`

```ruby
dynamic_emergency_address = client.dynamic_emergency_addresses.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(dynamic_emergency_address)
```

## 删除动态紧急地址

根据提供的 ID 删除动态紧急地址

`DELETE /dynamic_emergency_addresses/{id}`

```ruby
dynamic_emergency_address = client.dynamic_emergency_addresses.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(dynamic_emergency_address)
```

## 列出动态紧急终端点

根据过滤器返回动态紧急终端点

`GET /dynamic_emergency_endpoints`

```ruby
page = client.dynamic_emergency_endpoints.list

puts(page)
```

## 创建动态紧急终端点

创建一个动态紧急终端点。

`POST /dynamic_emergency_endpoints` — 必需参数：`dynamic_emergency_address_id`、`callback_number`、`caller_name`

```ruby
dynamic_emergency_endpoint = client.dynamic_emergency_endpoints.create(
  callback_number: "+13125550000",
  caller_name: "Jane Doe Desk Phone",
  dynamic_emergency_address_id: "0ccc7b54-4df3-4bca-a65a-3da1ecc777f0"
)

puts(dynamic_emergency_endpoint)
```

## 获取动态紧急终端点

根据提供的 ID 返回动态紧急终端点

`GET /dynamic_emergency_endpoints/{id}`

```ruby
dynamic_emergency_endpoint = client.dynamic_emergency_endpoints.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(dynamic_emergency_endpoint)
```

## 删除动态紧急终端点

根据提供的 ID 删除动态紧急终端点

`DELETE /dynamic_emergency_endpoints/{id}`

```ruby
dynamic_emergency_endpoint = client.dynamic_emergency_endpoints.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(dynamic_emergency_endpoint)
```

## 列出非美国地区的语音通道

列出您账户中的非美国地区语音通道。

`GET /channel_zones`

```ruby
page = client.channel_zones.list

puts(page)
```

## 更新非美国地区的语音通道

更新非美国地区的语音通道数量。

`PUT /channel_zones/{channel_zone_id}` — 必需参数：`channels`

```ruby
channel_zone = client.channel_zones.update("channel_zone_id", channels: 0)

puts(channel_zone)
```

## 列出美国地区的语音通道

列出您账户中的美国地区语音通道。

`GET /inbound_channels`

```ruby
inbound_channels = client.inbound_channels.list

puts(inbound_channels)
```

## 更新美国地区的语音通道

更新美国地区的语音通道数量。

`PATCH /inbound_channels` — 必需参数：`channels`

```ruby
inbound_channel = client.inbound_channels.update(channels: 7)

puts(inbound_channel)
```

## 列出使用通道计费的电话号码

检索按地区分组的所有使用通道计费的电话号码。

`GET /list`

```ruby
response = client.list.retrieve_all

puts(response)
```

## 列出特定地区的使用通道计费的电话号码

检索特定地区使用通道计费的电话号码列表。

`GET /list/{channel_zone_id}`

```ruby
response = client.list.retrieve_by_zone("channel_zone_id")

puts(response)
```

## 获取语音信箱

获取电话号码的语音信箱设置

`GET /phone_numbers/{phone_number_id}/voicemail`

```ruby
voicemail = client.phone_numbers.voicemail.retrieve("123455678900")

puts(voicemail)
```

## 创建语音信箱

为电话号码创建语音信箱设置

`POST /phone_numbers/{phone_number_id}/voicemail`

```ruby
voicemail = client.phone_numbers.voicemail.create("123455678900")

puts(voicemail)
```

## 更新语音信箱

更新电话号码的语音信箱设置

`PATCH /phone_numbers/{phone_number_id}/voicemail`

```ruby
voicemail = client.phone_numbers.voicemail.update("123455678900")

puts(voicemail)
```
```