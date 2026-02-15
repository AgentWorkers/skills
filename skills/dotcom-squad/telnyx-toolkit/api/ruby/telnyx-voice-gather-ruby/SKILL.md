---
name: telnyx-voice-gather-ruby
description: >-
  Collect DTMF input and speech from callers using standard gather or AI-powered
  gather. Build interactive voice menus and AI voice assistants. This skill
  provides Ruby SDK examples.
metadata:
  author: telnyx
  product: voice-gather
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 语音采集 - Ruby

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

## 向 AI 助手添加消息

向 AI 助手发起的通话中添加消息。

`POST /calls/{call_control_id}/actions/ai_assistant_add_messages`

```ruby
response = client.calls.actions.add_ai_assistant_messages("call_control_id")

puts(response)
```

## 启动 AI 助手

在通话中启动 AI 助手。

`POST /calls/{call_control_id}/actions/ai_assistant_start`

```ruby
response = client.calls.actions.start_ai_assistant("call_control_id")

puts(response)
```

## 停止 AI 助手

在通话中停止 AI 助手。

`POST /calls/{call_control_id}/actions/ai_assistant_stop`

```ruby
response = client.calls.actions.stop_ai_assistant("call_control_id")

puts(response)
```

## 停止数据采集

停止当前的数据采集操作。

`POST /calls/{call_control_id}/actions/gather_stop`

```ruby
response = client.calls.actions.stop_gather("call_control_id")

puts(response)
```

## 使用 AI 进行数据采集

使用语音助手收集请求负载中定义的参数。

`POST /calls/{call_control_id}/actions/gather_using_ai` — 必需参数：`parameters`

```ruby
response = client.calls.actions.gather_using_ai(
  "call_control_id",
  parameters: {properties: "bar", required: "bar", type: "bar"}
)

puts(response)
```

## 使用音频进行数据采集

在通话中播放音频文件，直到收集到所需的 DTMF 信号以构建交互式菜单。

`POST /calls/{call_control_id}/actions/gather_using_audio`

```ruby
response = client.calls.actions.gather_using_audio("call_control_id")

puts(response)
```

## 使用语音合成进行数据采集

将文本转换为语音并在通话中播放，直到收集到所需的 DTMF 信号以构建交互式菜单。

`POST /calls/{call_control_id}/actions/gather_using_speak` — 必需参数：`voice`, `payload`

```ruby
response = client.calls.actions.gather_using_speak("call_control_id", payload: "say this on call", voice: "male")

puts(response)
```

## 数据采集

收集 DTMF 信号以构建交互式菜单。

`POST /calls/{call_control_id}/actions/gather`

```ruby
response = client.calls.actions.gather("call_control_id")

puts(response)
```

---

## Webhook

以下 webhook 事件会被发送到您配置的 webhook URL：
所有 webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 头部信息以供验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callGatherEnded` | 通话数据采集结束 |
| `CallAIGatherEnded` | 通话 AI 数据采集结束 |
| `CallAIGatherMessageHistoryUpdated` | 通话 AI 数据采集消息历史更新 |
| `CallAIGatherPartialResults` | 通话 AI 数据采集部分结果 |
| `CallConversationEnded` | 通话结束 |
| `callPlaybackStarted` | 通话播放开始 |
| `callPlaybackEnded` | 通话播放结束 |
| `callDtmfReceived` | 通话中接收到 DTMF 信号 |
```