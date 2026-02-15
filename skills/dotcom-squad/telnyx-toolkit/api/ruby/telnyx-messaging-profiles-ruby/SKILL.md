---
name: telnyx-messaging-profiles-ruby
description: >-
  Create and manage messaging profiles with number pools, sticky sender, and
  geomatch features. Configure short codes for high-volume messaging. This skill
  provides Ruby SDK examples.
metadata:
  author: telnyx
  product: messaging-profiles
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 消息传递配置文件 - Ruby

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

## 列出消息传递配置文件

`GET /messaging_profiles`

```ruby
page = client.messaging_profiles.list

puts(page)
```

## 创建消息传递配置文件

`POST /messaging_profiles` — 必需参数：`name`、`whitelisted_destinations`

```ruby
messaging_profile = client.messaging_profiles.create(name: "My name", whitelisted_destinations: ["US"])

puts(messaging_profile)
```

## 获取消息传递配置文件

`GET /messagingprofiles/{id}`

```ruby
messaging_profile = client.messaging_profiles.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(messaging_profile)
```

## 更新消息传递配置文件

`PATCH /messagingprofiles/{id}`

```ruby
messaging_profile = client.messaging_profiles.update("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(messaging_profile)
```

## 删除消息传递配置文件

`DELETE /messagingprofiles/{id}`

```ruby
messaging_profile = client.messaging_profiles.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(messaging_profile)
```

## 列出与消息传递配置文件关联的电话号码

`GET /messagingprofiles/{id}/phone_numbers`

```ruby
page = client.messaging_profiles.list_phone_numbers("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(page)
```

## 列出与消息传递配置文件关联的短代码

`GET /messagingprofiles/{id}/short_codes`

```ruby
page = client.messaging_profiles.list_short_codes("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(page)
```

## 列出自动应答设置

`GET /messagingprofiles/{profile_id}/autoresp_configs`

```ruby
autoresp_configs = client.messaging_profiles.autoresp_configs.list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(autoresp_configs)
```

## 创建自动应答设置

`POST /messagingprofiles/{profile_id}/autoresp_configs` — 必需参数：`op`、`keywords`、`country_code`

```ruby
auto_resp_config_response = client.messaging_profiles.autoresp_configs.create(
  "profile_id",
  country_code: "US",
  keywords: ["keyword1", "keyword2"],
  op: :start
)

puts(auto_resp_config_response)
```

## 获取自动应答设置

`GET /messagingprofiles/{profile_id}/autoresp_configs/{autoresp_cfg_id}`

```ruby
auto_resp_config_response = client.messaging_profiles.autoresp_configs.retrieve(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  profile_id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
)

puts(auto_resp_config_response)
```

## 更新自动应答设置

`PUT /messagingprofiles/{profile_id}/autoresp_configs/{autoresp_cfg_id}` — 必需参数：`op`、`keywords`、`country_code`

```ruby
auto_resp_config_response = client.messaging_profiles.autoresp_configs.update(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  profile_id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  country_code: "US",
  keywords: ["keyword1", "keyword2"],
  op: :start
)

puts(auto_resp_config_response)
```

## 删除自动应答设置

`DELETE /messagingprofiles/{profile_id}/autoresp_configs/{autoresp_cfg_id}`

```ruby
autoresp_config = client.messaging_profiles.autoresp_configs.delete(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  profile_id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
)

puts(autoresp_config)
```

## 列出所有短代码

`GET /short_codes`

```ruby
page = client.short_codes.list

puts(page)
```

## 获取特定短代码的信息

`GET /short_codes/{id}`

```ruby
short_code = client.short_codes.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(short_code)
```

## 更新短代码的设置

`PATCH /short_codes/{id}` — 必需参数：`messaging_profile_id`

```ruby
short_code = client.short_codes.update(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  messaging_profile_id: "abc85f64-5717-4562-b3fc-2c9600000000"
)

puts(short_code)
```