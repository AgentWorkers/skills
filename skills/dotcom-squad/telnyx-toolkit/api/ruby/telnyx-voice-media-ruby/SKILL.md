---
name: telnyx-voice-media-ruby
description: >-
  Play audio files, use text-to-speech, and record calls. Use when building IVR
  systems, playing announcements, or recording conversations. This skill
  provides Ruby SDK examples.
metadata:
  author: telnyx
  product: voice-media
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Voice Media - Ruby

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

## 播放音频文件

在通话中播放音频文件。

`POST /calls/{call_control_id}/actions/playback_start`

```ruby
response = client.calls.actions.start_playback("call_control_id")

puts(response)
```

## 停止音频播放

停止通话中的音频播放。

`POST /calls/{call_control_id}/actions/playback_stop`

```ruby
response = client.calls.actions.stop_playback("call_control_id")

puts(response)
```

## 暂停录音

暂停通话的录音。

`POST /calls/{call_control_id}/actions/record_PAUSE`

```ruby
response = client.calls.actions.pause_recording("call_control_id")

puts(response)
```

## 恢复录音

恢复通话的录音。

`POST /calls/{call_control_id}/actions/record_resume`

```ruby
response = client.calls.actions.resume_recording("call_control_id")

puts(response)
```

## 开始录音

开始通话的录音。

`POST /calls/{call_control_id}/actions/record_start` — 必需参数：`format`, `channels`

```ruby
response = client.calls.actions.start_recording("call_control_id", channels: :single, format_: :wav)

puts(response)
```

## 停止录音

停止通话的录音。

`POST /calls/{call_control_id}/actions/record_stop`

```ruby
response = client.calls.actions.stop_recording("call_control_id")

puts(response)
```

## 将文本转换为语音并在通话中播放

将文本转换为语音并在通话中播放。

`POST /calls/{call_control_id}/actions/speak` — 必需参数：`payload`, `voice`

```ruby
response = client.calls.actions.speak("call_control_id", payload: "Say this on the call", voice: "female")

puts(response)
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL：
所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callPlaybackStarted` | 通话录音开始 |
| `callPlaybackEnded` | 通话录音结束 |
| `callSpeakEnded` | 通话语音播放结束 |
| `callRecordingSaved` | 通话录音保存 |
| `callRecordingError` | 通话录音出现错误 |
| `callRecordingTranscriptionSaved` | 通话录音转录文件保存 |
| `callSpeakStarted` | 通话语音播放开始 |
```