---
name: telnyx-voice-streaming-ruby
description: >-
  Stream call audio in real-time, fork media to external destinations, and
  transcribe speech live. Use for real-time analytics and AI integrations. This
  skill provides Ruby SDK examples.
metadata:
  author: telnyx
  product: voice-streaming
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 语音流媒体服务 - Ruby

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

## 启动分叉流媒体传输

`POST /calls/{call_control_id}/actions/fork_start`

```ruby
response = client.calls.actions.start_forking("call_control_id")

puts(response)
```

## 停止分叉流媒体传输

`POST /calls/{call_control_id}/actions/fork_stop`

```ruby
response = client.calls.actions.stop_forking("call_control_id")

puts(response)
```

## 启动流媒体传输

`POST /calls/{call_control_id}/actions/streaming_start`

**说明：** 媒体数据将实时传输到指定的 WebSocket 地址或 Dialogflow 连接。

```ruby
response = client.calls.actions.start_streaming("call_control_id")

puts(response)
```

## 停止流媒体传输

`POST /calls/{call_control_id}/actions/streaming_stop`

**说明：** 停止向指定的 WebSocket 地址传输媒体数据。

```ruby
response = client.calls.actions.stop_streaming("call_control_id")

puts(response)
```

## 启动实时转录

`POST /calls/{call_control_id}/actions/transcription_start`

**说明：** 开始对通话内容进行实时转录。

```ruby
response = client.calls.actions.start_transcription("call_control_id")

puts(response)
```

## 停止实时转录

`POST /calls/{call_control_id}/actions/transcription_stop`

**说明：** 停止对通话内容进行实时转录。

```ruby
response = client.calls.actions.stop_transcription("call_control_id")

puts(response)
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL：
所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头，用于验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callForkStarted` | 分叉流媒体传输开始 |
| `callForkStopped` | 分叉流媒体传输停止 |
| `callStreamingStarted` | 流媒体传输开始 |
| `callStreamingStopped` | 流媒体传输停止 |
| `callStreamingFailed` | 流媒体传输失败 |
| `transcription` | 转录开始 |
```
```