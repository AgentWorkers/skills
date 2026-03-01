---
name: voice-call
description: 通过 OpenClaw 的语音通话插件发起语音通话。
metadata:
  {
    "openclaw":
      {
        "emoji": "📞",
        "skillKey": "voice-call",
        "requires": { "config": ["plugins.entries.voice-call.enabled"] },
      },
  }
---
# 语音通话

使用语音通话插件来发起或查看通话（支持 Twilio、Telnyx、Plivo 或模拟通话）。

## 命令行接口 (CLI)

```bash
openclaw voicecall call --to "+15555550123" --message "Hello from OpenClaw"
openclaw voicecall status --call-id <id>
```

## 工具说明

使用 `voice_call` 命令来执行由代理发起的通话操作。

可用命令：

- `initiate_call` (message, to?, mode?)：发起新的通话
- `continue_call` (callId, message)：继续当前的通话
- `speak_to_user` (callId, message)：向通话中的用户发送语音消息
- `end_call` (callId)：结束通话
- `get_status` (callId)：获取通话状态

**注意：**

- 必须启用语音通话插件。
- 插件配置文件位于 `plugins.entries.voice-call.config` 中。
- Twilio 配置示例：`provider: "twilio"` + `twilio.accountSid/authToken` + `fromNumber`
- Telnyx 配置示例：`provider: "telnyx"` + `telnyx.apiKey/connectionId` + `fromNumber`
- Plivo 配置示例：`provider: "plivo"` + `plivo.authId/authToken` + `fromNumber`
- 开发环境备用方案：`provider: "mock"`（此时不使用真实网络连接，仅进行模拟操作）