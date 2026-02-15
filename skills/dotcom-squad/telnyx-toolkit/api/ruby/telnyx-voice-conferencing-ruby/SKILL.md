---
name: telnyx-voice-conferencing-ruby
description: >-
  Create and manage conference calls, queues, and multi-party sessions. Use when
  building call centers or conferencing applications. This skill provides Ruby
  SDK examples.
metadata:
  author: telnyx
  product: voice-conferencing
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 语音会议 - Ruby

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

## 将呼叫放入队列

将呼叫放入队列中。

`POST /calls/{call_control_id}/actions/enqueue` — 必需参数：`queue_name`

```ruby
response = client.calls.actions.enqueue("call_control_id", queue_name: "support")

puts(response)
```

## 从队列中移除呼叫

从队列中移除呼叫。

`POST /calls/{call_control_id}/actions/leave_queue`

```ruby
response = client.calls.actions.leave_queue("call_control_id")

puts(response)
```

## 列出会议

列出所有会议。

`GET /conferences`

```ruby
page = client.conferences.list

puts(page)
```

## 创建会议

使用 `call_control_id` 和会议名称从现有的通话中创建会议。

`POST /conferences` — 必需参数：`call_control_id`, `name`

```ruby
conference = client.conferences.create(
  call_control_id: "v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg",
  name: "Business"
)

puts(conference)
```

## 获取会议信息

获取现有会议的信息。

`GET /conferences/{id}`

```ruby
conference = client.conferences.retrieve("id")

puts(conference)
```

## 暂停会议参与者的发言

暂停会议中参与者的发言。

`POST /conferences/{id}/actions/hold`

```ruby
response = client.conferences.actions.hold("id")

puts(response)
```

## 加入会议

加入现有的通话以参与会议。

`POST /conferences/{id}/actions/join` — 必需参数：`call_control_id`

```ruby
response = client.conferences.actions.join(
  "id",
  call_control_id: "v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg"
)

puts(response)
```

## 退出会议

将通话从会议中移除并恢复到待机状态。

`POST /conferences/{id}/actions/leave` — 必需参数：`call_control_id`

```ruby
response = client.conferences.actions.leave("id", call_control_id: "c46e06d7-b78f-4b13-96b6-c576af9640ff")

puts(response)
```

## 静音会议参与者

静音会议中的参与者。

`POST /conferences/{id}/actions/mute`

```ruby
response = client.conferences.actions.mute("id")

puts(response)
```

## 向会议参与者播放音频

向会议中的所有或部分参与者播放音频。

`POST /conferences/{id}/actions/play`

```ruby
response = client.conferences.actions.play("id")

puts(response)
```

## 暂停会议录制

暂停会议录制。

`POST /conferences/{id}/actions/record_PAUSE`

```ruby
response = client.conferences.actions.record_pause("id")

puts(response)
```

## 恢复会议录制

恢复会议录制。

`POST /conferences/{id}/actions/record_resume`

```ruby
response = client.conferences.actions.record_resume("id")

puts(response)
```

## 开始会议录制

开始会议录制。

`POST /conferences/{id}/actions/record_start` — 必需参数：`format`

```ruby
response = client.conferences.actions.record_start("id", format_: :wav)

puts(response)
```

## 停止会议录制

停止会议录制。

`POST /conferences/{id}/actions/record_stop`

```ruby
response = client.conferences.actions.record_stop("id")

puts(response)
```

## 向会议参与者朗读文本

将文本转换为语音并播放给所有或部分参与者。

`POST /conferences/{id}/actions/speak` — 必需参数：`payload`, `voice`

```ruby
response = client.conferences.actions.speak("id", payload: "Say this to participants", voice: "female")

puts(response)
```

## 停止向会议参与者播放音频

停止向会议中的所有或部分参与者播放音频。

`POST /conferences/{id}/actions/stop`

```ruby
response = client.conferences.actions.stop("id")

puts(response)
```

## 恢复会议参与者的发言权限

恢复会议中参与者的发言权限。

`POST /conferences/{id}/actions/unhold` — 必需参数：`call_control_ids`

```ruby
response = client.conferences.actions.unhold(
  "id",
  call_control_ids: ["v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg"]
)

puts(response)
```

## 取消对会议参与者的静音状态

取消对会议中参与者的静音状态。

`POST /conferences/{id}/actions/unmute`

```ruby
response = client.conferences.actions.unmute("id")

puts(response)
```

## 更新会议参与者信息

更新会议参与者的角色。

`POST /conferences/{id}/actions/update` — 必需参数：`call_control_id`, `supervisor_role`

```ruby
action = client.conferences.actions.update(
  "id",
  call_control_id: "v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg",
  supervisor_role: :whisper
)

puts(action)
```

## 列出会议参与者

列出会议中的所有参与者。

`GET /conferences/{conference_id}/participants`

```ruby
page = client.conferences.list_participants("conference_id")

puts(page)
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL：
所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callEnqueued` | 呼叫被放入队列 |
| `callLeftQueue` | 呼叫离开队列 |
| `conferenceCreated` | 会议创建 |
| `conferenceEnded` | 会议结束 |
| `conferenceFloorChanged` | 会议主持人变更 |
| `conferenceParticipantJoined` | 会议参与者加入 |
| `conferenceParticipantLeft` | 会议参与者离开 |
| `conferenceParticipantPlaybackEnded` | 会议参与者停止发言 |
| `conferenceParticipantPlaybackStarted` | 会议参与者开始发言 |
| `conferenceParticipantSpeakEnded` | 会议参与者结束发言 |
| `conferenceParticipantSpeakStarted` | 会议参与者开始发言 |
| `conferencePlaybackEnded` | 会议播放结束 |
| `conferencePlaybackStarted` | 会议播放开始 |
| `conferenceRecordingSaved` | 会议录制保存 |
| `conferenceSpeakEnded` | 会议发言结束 |
| `conferenceSpeakStarted` | 会议发言开始 |
```
```