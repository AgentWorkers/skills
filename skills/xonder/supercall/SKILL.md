---
name: supercall
description: 使用 AI 驱动的电话功能，可以自定义通话角色和目标。该功能结合了 OpenAI Realtime API 和 Twilio 来实现超低延迟的语音通话。适用于需要打电话、确认预约、传递信息或让 AI 自动处理电话对话的场景。与标准的语音通话插件不同，通话对方无法访问网关代理，从而降低了被攻击的风险。
homepage: https://github.com/xonder/supercall
metadata:
  {
    "openclaw":
      {
        "emoji": "📞",
        "requires": { "plugins": ["supercall"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "plugin",
              "package": "@xonder/supercall",
              "label": "Install supercall plugin (npm)",
            },
          ],
      },
  }
---

# SuperCall

使用 OpenAI Realtime API 和 Twilio，通过自定义的角色和目标发起由 AI 驱动的电话呼叫。

## 特点

- **自定义角色通话**：为自动通话定义角色、目标和开场白。
- **全实时模式**：基于 GPT-4o 的语音对话，延迟小于 1 秒。
- **通话提供商**：支持 Twilio（全实时）以及用于测试的模拟提供商。
- **音频流媒体**：通过 WebSocket 进行双向音频传输，实现实时对话。
- **访问限制**：与标准 voice_call 插件不同，通话中的对方无法访问网关代理，从而降低了安全风险。

## 安装步骤

1. 将此技能复制到您的 OpenClaw 技能目录中。
2. **启用回调钩子**（用于处理通话完成事件）（必需）：

```json
{
  "hooks": {
    "enabled": true,
    "token": "your-secret-token"
  }
}
```

使用以下命令生成一个令牌：`openssl rand -hex 24`

3. 在您的 openclaw 配置文件中配置该插件：

```json
{
  "plugins": {
    "entries": {
      "supercall": {
        "enabled": true,
        "config": {
          "provider": "twilio",
          "fromNumber": "+15551234567",
          "twilio": {
            "accountSid": "your-account-sid",
            "authToken": "your-auth-token"
          },
          "streaming": {
            "openaiApiKey": "your-openai-key"
          },
          "tunnel": {
            "provider": "ngrok",
            "ngrokDomain": "your-domain.ngrok.app"
          }
        }
      }
    }
  }
}
```

**注意**：`hooks.token` 是处理通话完成事件所必需的。如果没有这个令牌，代理在通话结束后将不会收到通知。

## 工具：supercall

使用自定义角色发起电话呼叫：

```
supercall(
  action: "persona_call",
  to: "+1234567890",
  persona: "Personal assistant to the king",
  goal: "Confirm the callee's availabilities for dinner next week",
  openingLine: "Hey, this is Michael, Alex's Assistant..."
)
```

### 可用操作

- `persona_call`：以指定角色发起新通话。
- `get_status`：检查通话状态和通话记录。
- `end_call`：结束正在进行的通话。
- `list_calls`：列出所有正在进行的角色通话。

## 配置选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `provider` | 语音提供商（twilio/mock） | 必需 |
| `fromNumber` | 主叫方号码（E.164 格式） | 对于真实提供商是必需的 |
| `toNumber` | 收件人号码 | - |
| `streaming.openaiApiKey` | OpenAI API 密钥（用于实时通话） | 环境变量 `OPENAI_API_KEY` |
| `streaming.silenceDurationMs` | VAD（Voice Activity Detection）静默时长（毫秒） | 800 |
| `streaming.vadThreshold` | VAD 阈值（0-1，数值越大越不敏感） | 0.5 |
| `streaming.streamPath` | 媒体流的 WebSocket 路径 | `/voice/stream` |
| `tunnel-provider` | 用于 Webhook 的隧道服务（ngrok/tailscale-serve/tailscale-funnel） | 无 |

全实时功能需要 OpenAI API 密钥。

## 系统要求

- Node.js 20 及以上版本。
- 需要 Twilio 账户以支持全实时通话（包括媒体流传输）。
- 需要 ngrok 或 Tailscale 服务来设置 Webhook 隧道（在生产环境中使用）。
- 需要 OpenAI API 密钥以启用实时功能。

## 架构

这是一个完全独立的技能，不依赖于内置的 voice-call 插件。所有的电话呼叫逻辑都是自包含的。