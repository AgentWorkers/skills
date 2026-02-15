---
name: telnyx-voice-advanced-ruby
description: >-
  Advanced call control features including DTMF sending, SIPREC recording, noise
  suppression, client state, and supervisor controls. This skill provides Ruby
  SDK examples.
metadata:
  author: telnyx
  product: voice-advanced
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Voice Advanced - Ruby

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

## 更新客户端状态

更新客户端状态

`PUT /calls/{call_control_id}/actions/client_state_update` — 必需参数：`client_state`

```ruby
response = client.calls.actions.update_client_state("call_control_id", client_state: "aGF2ZSBhIG5pY2UgZGF5ID1d")

puts(response)
```

## SIP 转接呼叫

在呼叫控制过程中发起 SIP 转接。

`POST /calls/{call_control_id}/actions/refer` — 必需参数：`sip_address`

```ruby
response = client.calls.actions.refer("call_control_id", sip_address: "sip:username@sip.non-telnyx-address.com")

puts(response)
```

## 发送 DTMF 音频

从当前通话线路发送 DTMF 音频。

`POST /calls/{call_control_id}/actions/send_dtmf` — 必需参数：`digits`

```ruby
response = client.calls.actions.send_dtmf("call_control_id", digits: "1www2WABCDw9")

puts(response)
```

## 启动 SIPREC 会话

启动在 SIPREC 连接器中配置的 SIPREC 会话。

`POST /calls/{call_control_id}/actions/siprec_start`

```ruby
response = client.calls.actions.start_siprec("call_control_id")

puts(response)
```

## 停止 SIPREC 会话

停止 SIPREC 会话。

`POST /calls/{call_control_id}/actions/siprec_stop`

```ruby
response = client.calls.actions.stop_siprec("call_control_id")

puts(response)
```

## 噪音抑制（测试版）

启动噪声抑制功能。

`POST /calls/{call_control_id}/actions/suppression_start`

```ruby
response = client.calls.actions.start_noise_suppression("call_control_id")

puts(response)
```

## 停止噪声抑制（测试版）

停止噪声抑制功能。

`POST /calls/{call_control_id}/actions/suppression_stop`

```ruby
response = client.calls.actions.stop_noise_suppression("call_control_id")

puts(response)
```

## 切换监督者角色

切换桥接呼叫的监督者角色。

`POST /calls/{call_control_id}/actions/switch_supervisor_role` — 必需参数：`role`

```ruby
response = client.calls.actions.switch_supervisor_role("call_control_id", role: :barge)

puts(response)
```

---

## Webhook

以下 Webhook 事件会发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 头部信息以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callReferStarted` | 转接呼叫开始 |
| `callReferCompleted` | 转接呼叫完成 |
| `callReferFailed` | 转接呼叫失败 |
| `callSiprecStarted` | SIPREC 会话开始 |
| `callSiprecStopped` | SIPREC 会话停止 |
| `callSiprecFailed` | SIPREC 会话失败 |
```
```