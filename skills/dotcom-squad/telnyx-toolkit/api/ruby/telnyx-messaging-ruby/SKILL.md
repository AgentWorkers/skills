---
name: telnyx-messaging-ruby
description: >-
  Send and receive SMS/MMS messages, manage messaging-enabled phone numbers, and
  handle opt-outs. Use when building messaging applications, implementing 2FA,
  or sending notifications. This skill provides Ruby SDK examples.
metadata:
  author: telnyx
  product: messaging
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 |

# Telnyx 消息服务 - Ruby

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

## 发送消息

可以使用电话号码、字母数字发送者 ID、短代码或号码池来发送消息。

`POST /messages` — 必需参数：`to`

```ruby
response = client.messages.send_(to: "+18445550001")

puts(response)
```

## 获取消息

注意：此 API 端点仅能获取创建时间不超过 10 天的消息。

`GET /messages/{id}`

```ruby
message = client.messages.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(message)
```

## 取消已安排的消息

取消尚未发送的已安排消息。

`DELETE /messages/{id}`

```ruby
response = client.messages.cancel_scheduled("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(response)
```

## 发送 Whatsapp 消息

`POST /messages/whatsapp` — 必需参数：`from`, `to`, `whatsapp_message`

```ruby
response = client.messages.send_whatsapp(from: "+13125551234", to: "+13125551234", whatsapp_message: {})

puts(response)
```

## 发送群组 MMS 消息

`POST /messages/group_mms` — 必需参数：`from`, `to`

```ruby
response = client.messages.send_group_mms(from: "+13125551234", to: ["+18655551234", "+14155551234"])

puts(response)
```

## 发送长码消息

`POST /messages/long_code` — 必需参数：`from`, `to`

```ruby
response = client.messages.send_long_code(from: "+18445550001", to: "+13125550002")

puts(response)
```

## 使用号码池发送消息

`POST /messages/number_pool` — 必需参数：`to`, `messaging_profile_id`

```ruby
response = client.messages.send_number_pool(
  messaging_profile_id: "abc85f64-5717-4562-b3fc-2c9600000000",
  to: "+13125550002"
)

puts(response)
```

## 安排消息

可以使用电话号码、字母数字发送者 ID、短代码或号码池来安排消息的发送。

`POST /messages/schedule` — 必需参数：`to`

```ruby
response = client.messages.schedule(to: "+18445550001")

puts(response)
```

## 发送短代码消息

`POST /messages/short_code` — 必需参数：`from`, `to`

```ruby
response = client.messages.send_short_code(from: "+18445550001", to: "+18445550001")

puts(response)
```

## 查看退订信息

获取退订信息的列表。

`GET /messaging_optouts`

```ruby
page = client.messaging_optouts.list

puts(page)
```

## 获取带有消息功能的电话号码信息

`GET /phone_numbers/{id}/messaging`

```ruby
messaging = client.phone_numbers.messaging.retrieve("id")

puts(messaging)
```

## 更新电话号码的消息功能配置

`PATCH /phone_numbers/{id}/messaging`

```ruby
messaging = client.phone_numbers.messaging.update("id")

puts(messaging)
```

## 查看带有消息功能的电话号码列表

`GET /phone_numbers/messaging`

```ruby
page = client.phone_numbers.messaging.list

puts(page)
```

## 获取带有消息功能的手机号码信息

`GET /mobile_phone_numbers/{id}/messaging`

```ruby
messaging = client.mobile_phone_numbers.messaging.retrieve("id")

puts(messaging)
```

## 查看带有消息功能的手机号码列表

`GET /mobile_phone_numbers/messaging`

```ruby
page = client.mobile_phone_numbers.messaging.list

puts(page)
```

## 批量更新电话号码配置

`POST /messaging_numbers/bulk_updates` — 必需参数：`messaging_profile_id`, `numbers`

```ruby
messaging_numbers_bulk_update = client.messaging_numbers_bulk_updates.create(
  messaging_profile_id: "00000000-0000-0000-0000-000000000000",
  numbers: ["+18880000000", "+18880000001", "+18880000002"]
)

puts(messaging_numbers_bulk_update)
```

## 查看批量更新状态

`GET /messaging_numbers/bulk_updates/{order_id}`

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `deliveryUpdate` | 消息发送状态更新 |
| `inboundMessage` | 收到的消息 |
| `replacedLinkClick` | 被替换的链接被点击 |
```
```