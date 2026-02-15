---
name: supercall
description: 使用基于AI的电话通话功能，可以自定义通话角色和通话目标。该功能结合了OpenAI的实时API和Twilio技术，实现超低延迟的语音通话。适用于需要拨打电话、确认预约、传递信息或让AI自主处理电话对话的场景。与标准的语音通话插件不同，通话对方无法访问网关代理，从而降低了安全风险。
homepage: https://github.com/xonder/supercall
metadata:
  {
    "openclaw":
      {
        "emoji": "📞",
        "requires": { 
          "plugins": ["supercall"],
          "env": ["OPENAI_API_KEY", "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN"],
          "anyBins": ["ngrok", "tailscale"]
        },
        "primaryEnv": "OPENAI_API_KEY",
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@xonder/supercall",
              "label": "Install supercall plugin (npm)",
            },
          ],
      },
  }
---

# SuperCall

使用 OpenAI Realtime API 和 Twilio，通过自定义角色和目标发起人工智能驱动的电话呼叫。

## 特点

- **角色化呼叫**：为自动呼叫定义角色、目标和开场白。
- **全实时模式**：基于 GPT-4o 的语音对话，延迟小于 1 秒。
- **提供商**：支持 Twilio（全实时）和模拟提供商（用于测试）。
- **流媒体音频**：通过 WebSocket 进行双向音频传输，实现实时对话。
- **访问限制**：与标准 voice_call 插件不同，通话中的用户无法访问网关代理，从而降低了安全风险。

## 凭据

### 必需的凭证

| 凭据 | 来源 | 用途 |
|------------|--------|---------|
| `OPENAI_API_KEY` | [OpenAI](https://platform.openai.com/api-keys) | 用于启用实时语音功能（GPT-4o） |
| `TWILIO_ACCOUNT_SID` | [Twilio 控制台](https://console.twilio.com) | Twilio 账户标识符 |
| `TWILIO_AUTH_TOKEN` | [Twilio 控制台](https://console.twilio.com) | Twilio API 认证令牌 |

### 可选的凭证

| 凭据 | 来源 | 用途 |
|------------|--------|---------|
| `NGROK_AUTHTOKEN` | [ngrok](https://dashboard.ngrok.com) | 用于 ngrok 隧道认证（仅在使用 ngrok 作为隧道提供商时需要） |

凭证可以通过环境变量或在插件配置中设置（配置优先级更高）。

## 安装

1. 通过 npm 安装该插件，或将其复制到 OpenClaw 的扩展目录中。
2. **启用回调钩子**（必需）：

```json
{
  "hooks": {
    "enabled": true,
    "token": "your-secret-token"
  }
}
```

使用以下命令生成一个安全令牌：`openssl rand -hex 24`

> ⚠️ **安全提示**：`hooks.token` 是敏感信息，用于验证内部回调。请妥善保管，并在泄露后立即更换。

3. 在 openclaw 配置文件中配置该插件：

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

**重要提示**：`hooks.token` 是回调钩子所必需的。如果没有这个令牌，系统将无法在通话结束后通知代理。

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

- `persona_call`：使用指定角色发起新呼叫。
- `get_status`：查询呼叫状态和通话记录。
- `end_call`：结束当前通话。
- `list_calls`：列出所有正在进行的角色化呼叫。

## 配置选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `provider` | 语音提供商（例如：twilio/mock） | 必需 |
| `fromNumber` | 主叫号码（E.164 格式） | 对于真实提供商是必需的 |
| `toNumber` | 收件人号码 | - |
| `twilio.accountSid` | Twilio 账户 SID | 使用 `TWILIO_ACCOUNT_SID` 环境变量设置 |
| `twilio.authToken` | Twilio 认证令牌 | 使用 `TWILIO_AUTH_TOKEN` 环境变量设置 |
| `streaming.openaiApiKey` | OpenAI API 密钥（用于实时功能） | 使用 `OPENAI_API_KEY` 环境变量设置 |
| `streaming.silenceDurationMs` | VAD 静默时长（毫秒） | 800 |
| `streaming.vadThreshold` | VAD 阈值（0-1，数值越大越不敏感） | 0.5 |
| `streaming.streamPath` | 媒体流的 WebSocket 路径 | `/voice/stream` |
| `tunnel-provider` | 钩子服务器（ngrok/tailscale-serve/tailscale-funnel） | 无 |
| `tunnel.ngrokDomain` | ngrok 域名（生产环境推荐） | - |
| `tunnel.ngrokAuthToken` | ngrok 认证令牌 | 使用 `NGROK_AUTHTOKEN` 环境变量设置 |

**全实时功能** 需要 OpenAI API 密钥。

## 系统要求

- Node.js 20 及以上版本。
- 需要 Twilio 账户以支持实时通话（包括媒体流传输）。
- 需要 ngrok 或 Tailscale 作为 webhook 隧道服务（生产环境）。
- 需要 OpenAI API 密钥以使用实时功能。

## 架构

该插件是完全独立的，不依赖于内置的 voice-call 插件。所有语音呼叫逻辑均独立实现。

## 运行时行为与安全

该插件不仅提供指令执行功能，还会实际运行代码、创建进程、开启网络监听器并写入磁盘。以下是运行时的具体行为：

### 进程创建

当 `tunnel-provider` 设置为 `ngrok` 时，插件会通过 `child_process.spawn` 启动 `ngrok` 命令行工具；设置为 `tailscale-serve` 或 `tailscale-funnel` 时，则会启动 `tailscale` 命令行工具。这些进程会在插件运行期间持续存在，并在插件关闭时终止。如果 `tunnel-provider` 未设置（或直接提供了 `publicUrl`），则不会创建任何外部进程。

### 网络活动

- **本地 webhook 服务器**：插件会启动一个 HTTP 服务器（默认地址为 `0.0.0.0:3335`），用于接收 Twilio 的 webhook 回调和媒体流。
- **启动自测试**：插件在启动时会向自己的公共 webhook URL 发送一个带有 `x-supercall-self-test` 标头的 HTTP POST 请求以验证连接是否正常。如果 `publicUrl` 配置错误，该自测试请求可能会发送到错误的地址。请在启动前务必检查 `publicUrl` 或隧道配置。
- **外部 API 调用**：插件在通话期间会向 OpenAI Realtime API（WebSocket）和 Twilio REST API 发送请求。

### Webhook 验证

- **Twilio 呼叫**：使用 Twilio 的 X-Twilio-Signature 标头（HMAC-SHA1）进行验证。
- **自测试请求**：使用启动时生成的内部令牌（`x-supercall-self-test`）进行身份验证。
- **ngrok 免费 tier 的限制**：在免费 tier 的 ngrok 域名（如 `.ngrok-free.app`、`.ngrok.io`）下，由于 ngrok 的请求重写机制，URL 可能会发生变化，导致签名不匹配的情况会被记录但仍然会被允许通过。付费/自定义的 ngrok 域名（如 `.ngrok.app`）则会进行严格验证。此限制仅适用于免费 tier 域名，不影响 Tailscale 或直接使用的 `publicUrl` 配置。

### 数据存储

通话记录会保存在 `~/clawd/supercall-logs` 文件夹中。这些日志可能包含敏感的对话内容，请定期审查和清理。

### 最佳实践

- **保护凭证**：Twilio 和 OpenAI 的密钥可访问付费服务，请妥善保管。
- **验证公共 URL**：确保 `publicUrl` 或隧道配置指向正确的目标地址。
- **定期更换 `hooks.token`**，并在怀疑密钥被泄露时立即更换。
- **审查通话记录**：存储在磁盘中的记录可能包含敏感信息，请定期检查。