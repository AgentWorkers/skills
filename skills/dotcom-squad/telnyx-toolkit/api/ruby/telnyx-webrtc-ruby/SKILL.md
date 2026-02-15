---
name: telnyx-webrtc-ruby
description: >-
  Manage WebRTC credentials and mobile push notification settings. Use when
  building browser-based or mobile softphone applications. This skill provides
  Ruby SDK examples.
metadata:
  author: telnyx
  product: webrtc
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Webrtc - Ruby

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

## 列出移动推送凭据

`GET /mobile_push_credentials`

```ruby
page = client.mobile_push_credentials.list

puts(page)
```

## 创建新的移动推送凭据

`POST /mobile_push_credentials`

```ruby
push_credential_response = client.mobile_push_credentials.create(
  create_mobile_push_credential_request: {
    alias: "LucyIosCredential",
    certificate: "-----BEGIN CERTIFICATE----- MIIGVDCCBTKCAQEAsNlRJVZn9ZvXcECQm65czs... -----END CERTIFICATE-----",
    private_key: "-----BEGIN RSA PRIVATE KEY----- MIIEpQIBAAKCAQEAsNlRJVZn9ZvXcECQm65czs... -----END RSA PRIVATE KEY-----",
    type: :ios
  }
)

puts(push_credential_response)
```

## 获取移动推送凭据

根据给定的 `push_credential_id` 获取移动推送凭据

`GET /mobile_push_credentials/{push_credential_id}`

```ruby
push_credential_response = client.mobile_push_credentials.retrieve("0ccc7b76-4df3-4bca-a05a-3da1ecc389f0")

puts(push_credential_response)
```

## 删除移动推送凭据

根据给定的 `push_credential_id` 删除移动推送凭据

`DELETE /mobile_push_credentials/{push_credential_id}`

```ruby
result = client.mobile_push_credentials.delete("0ccc7b76-4df3-4bca-a05a-3da1ecc389f0")

puts(result)
```

## 列出所有凭据

列出所有的按需凭证。

`GET /telephony_credentials`

```ruby
page = client.telephony_credentials.list

puts(page)
```

## 创建凭据

创建一个新凭据。

`POST /telephony_credentials` — 必需参数：`connection_id`

```ruby
telephony_credential = client.telephony_credentials.create(connection_id: "1234567890")

puts(telephony_credential)
```

## 获取凭据详情

获取现有按需凭证的详细信息。

`GET /telephony_credentials/{id}`

```ruby
telephony_credential = client.telephony_credentials.retrieve("id")

puts(telephony_credential)
```

## 更新凭据

更新现有凭据。

`PATCH /telephony_credentials/{id}`

```ruby
telephony_credential = client.telephony_credentials.update("id")

puts(telephony_credential)
```

## 删除凭据

删除现有凭据。

`DELETE /telephony_credentials/{id}`

```ruby
telephony_credential = client.telephony_credentials.delete("id")

puts(telephony_credential)
```

## 创建访问令牌

为该凭据创建一个访问令牌（JWT）。

`POST /telephony_credentials/{id}/token`

```ruby
response = client.telephony_credentials.create_token("id")

puts(response)
```