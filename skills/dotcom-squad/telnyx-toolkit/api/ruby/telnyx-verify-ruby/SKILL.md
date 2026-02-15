---
name: telnyx-verify-ruby
description: >-
  Look up phone number information (carrier, type, caller name) and verify users
  via SMS/voice OTP. Use for phone verification and data enrichment. This skill
  provides Ruby SDK examples.
metadata:
  author: telnyx
  product: verify
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Verify - Ruby

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

## 查找电话号码信息

返回有关提供的电话号码的信息。

`GET /number_lookup/{phone_number}`

```ruby
number_lookup = client.number_lookup.retrieve("+18665552368")

puts(number_lookup)
```

## 触发电话验证

`POST /verifications/call` — 必需参数：`phone_number`, `verify_profile_id`

```ruby
create_verification_response = client.verifications.trigger_call(
  phone_number: "+13035551234",
  verify_profile_id: "12ade33a-21c0-473b-b055-b3c836e1c292"
)

puts(create_verification_response)
```

## 触发闪现式电话验证

`POST /verifications/flashcall` — 必需参数：`phone_number`, `verify_profile_id`

```ruby
create_verification_response = client.verifications.trigger_flashcall(
  phone_number: "+13035551234",
  verify_profile_id: "12ade33a-21c0-473b-b055-b3c836e1c292"
)

puts(create_verification_response)
```

## 触发短信验证

`POST /verifications/sms` — 必需参数：`phone_number`, `verify_profile_id`

```ruby
create_verification_response = client.verifications.trigger_sms(
  phone_number: "+13035551234",
  verify_profile_id: "12ade33a-21c0-473b-b055-b3c836e1c292"
)

puts(create_verification_response)
```

## 获取验证结果

`GET /verifications/{verification_id}`

```ruby
verification = client.verifications.retrieve("12ade33a-21c0-473b-b055-b3c836e1c292")

puts(verification)
```

## 根据 ID 验证验证码

`POST /verifications/{verification_id}/actions/verify`

```ruby
verify_verification_code_response = client.verifications.actions.verify("12ade33a-21c0-473b-b055-b3c836e1c292")

puts(verify_verification_code_response)
```

## 按电话号码列出验证记录

`GET /verifications/by_phone_number/{phone_number}`

```ruby
by_phone_numbers = client.verifications.by_phone_number.list("+13035551234")

puts(by_phone_numbers)
```

## 根据电话号码验证验证码

`POST /verifications/by_phone_number/{phone_number}/actions/verify` — 必需参数：`code`, `verify_profile_id`

```ruby
verify_verification_code_response = client.verifications.by_phone_number.actions.verify(
  "+13035551234",
  code: "17686",
  verify_profile_id: "12ade33a-21c0-473b-b055-b3c836e1c292"
)

puts(verify_verification_code_response)
```

## 列出所有验证配置文件

获取分页显示的验证配置文件列表。

`GET /verify_profiles`

```ruby
page = client.verify_profiles.list

puts(page)
```

## 创建验证配置文件

创建一个新的验证配置文件，用于关联验证操作。

`POST /verify_profiles` — 必需参数：`name`

```ruby
verify_profile_data = client.verify_profiles.create(name: "Test Profile")

puts(verify_profile_data)
```

## 获取验证配置文件信息

获取单个验证配置文件的信息。

`GET /verify_profiles/{verify_profile_id}`

```ruby
verify_profile_data = client.verify_profiles.retrieve("12ade33a-21c0-473b-b055-b3c836e1c292")

puts(verify_profile_data)
```

## 更新验证配置文件

`PATCH /verify_profiles/{verify_profile_id}`

```ruby
verify_profile_data = client.verify_profiles.update("12ade33a-21c0-473b-b055-b3c836e1c292")

puts(verify_profile_data)
```

## 删除验证配置文件

`DELETE /verify_profiles/{verify_profile_id}`

```ruby
verify_profile_data = client.verify_profiles.delete("12ade33a-21c0-473b-b055-b3c836e1c292")

puts(verify_profile_data)
```

## 获取验证配置文件的消息模板

列出所有验证配置文件的消息模板。

`GET /verify_profiles/templates`

```ruby
response = client.verify_profiles.retrieve_templates

puts(response)
```

## 创建消息模板

创建一个新的验证配置文件消息模板。

`POST /verify_profiles/templates` — 必需参数：`text`

```ruby
message_template = client.verify_profiles.create_template(text: "Your {{app_name}} verification code is: {{code}}.")

puts(message_template)
```

## 更新消息模板

更新现有的验证配置文件消息模板。

`PATCH /verify_profiles/templates/{template_id}` — 必需参数：`text`

```ruby
message_template = client.verify_profiles.update_template(
  "12ade33a-21c0-473b-b055-b3c836e1c292",
  text: "Your {{app_name}} verification code is: {{code}}."
)

puts(message_template)
```