---
name: telnyx-voice-ruby
description: >-
  Make and receive calls, transfer, bridge, and manage call lifecycle with Call
  Control. Includes application management and call events. This skill provides
  Ruby SDK examples.
metadata:
  author: telnyx
  product: voice
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Voice - Ruby

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

## 回答来电

回答传入的来电。

`POST /calls/{call_control_id}/actions/answer`

```ruby
response = client.calls.actions.answer("call_control_id")

puts(response)
```

## 桥接通话

将两个通话控制请求进行桥接。

`POST /calls/{call_control_id}/actions/bridge` — 必需参数：`call_control_id`

```ruby
response = client.calls.actions.bridge(
  "call_control_id",
  call_control_id_to_bridge_with: "v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg"
)

puts(response)
```

## 拨打电话

从指定的连接拨打一个号码或 SIP URI。

`POST /calls` — 必需参数：`connection_id`, `to`, `from`

```ruby
response = client.calls.dial(
  connection_id: "7267xxxxxxxxxxxxxx",
  from: "+18005550101",
  to: "+18005550100"
)

puts(response)
```

## 挂断通话

挂断通话。

`POST /calls/{call_control_id}/actions/hangup`

```ruby
response = client.calls.actions.hangup("call_control_id")

puts(response)
```

## 转接通话

将通话转接到新的目的地。

`POST /calls/{call_control_id}/actions/transfer` — 必需参数：`to`

```ruby
response = client.calls.actions.transfer("call_control_id", to: "+18005550100")

puts(response)
```

## 列出指定连接的所有活跃通话

列出指定连接的所有活跃通话。

`GET /connections/{connection_id}/active_calls`

```ruby
page = client.connections.list_active_calls("1293384261075731461")

puts(page)
```

## 列出通话控制应用程序

返回通话控制应用程序的列表。

`GET /call_control_applications`

```ruby
page = client.call_control_applications.list

puts(page)
```

## 创建通话控制应用程序

创建一个新的通话控制应用程序。

`POST /call_control_applications` — 必需参数：`application_name`, `webhook_event_url`

```ruby
call_control_application = client.call_control_applications.create(
  application_name: "call-router",
  webhook_event_url: "https://example.com"
)

puts(call_control_application)
```

## 获取通话控制应用程序的详细信息

获取现有通话控制应用程序的详细信息。

`GET /call_control_applications/{id}`

```ruby
call_control_application = client.call_control_applications.retrieve("id")

puts(call_control_application)
```

## 更新通话控制应用程序

更新现有通话控制应用程序的设置。

`PATCH /call_control_applications/{id}` — 必需参数：`application_name`, `webhook_event_url`

```ruby
call_control_application = client.call_control_applications.update(
  "id",
  application_name: "call-router",
  webhook_event_url: "https://example.com"
)

puts(call_control_application)
```

## 删除通话控制应用程序

删除通话控制应用程序。

`DELETE /call_control_applications/{id}`

```ruby
call_control_application = client.call_control_applications.delete("id")

puts(call_control_application)
```

## 列出通话事件

根据指定的过滤参数筛选通话事件。

`GET /call_events`

```ruby
page = client.call_events.list

puts(page)
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callAnswered` | 通话已接听 |
| `callStreamingStarted` | 通话流开始 |
| `callStreamingStopped` | 通话流停止 |
| `callStreamingFailed` | 通话流失败 |
| `callBridged` | 通话被桥接 |
| `callInitiated` | 通话开始 |
| `callHangup` | 通话挂断 |
| `callRecordingSaved` | 通话录音保存 |
| `callMachineDetectionEnded` | 机器检测结束 |
| `callMachineGreetingEnded` | 机器问候结束 |
| `callMachinePremiumDetectionEnded` | 机器高级检测结束 |
| `callMachinePremiumGreetingEnded` | 机器高级问候结束 |
```