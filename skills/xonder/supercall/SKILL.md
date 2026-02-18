---
name: supercall
description: 使用 AI 驱动的电话功能，可以自定义通话角色和目标。该功能结合了 OpenAI Realtime API 和 Twilio，实现超低延迟的语音通话。同时支持 DTMF/IVR 导航——AI 可以通过发送按键音数字来导航自动电话菜单。适用于需要拨打电话、确认预约、传递信息、导航电话流程或让 AI 自主处理通话的场景。与标准的语音通话插件不同，通话对方无法访问网关代理，从而降低了被攻击的风险。
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

使用 OpenAI Realtime API 和 Twilio，通过自定义的角色和目标发起人工智能驱动的电话呼叫。

## 特点

- **角色驱动的呼叫**：为自动呼叫定义角色、目标和开场白。
- **全实时模式**：基于 GPT-4o 的语音对话，延迟小于 1 秒。
- **DTMF / IVR 导航**：AI 通过生成并注入音频流中的双音多频（DTMF）数字，自动导航电话菜单（例如：按 1 进入 X 功能、输入您的账户号码等）。
- **服务提供商**：支持 Twilio（全实时）和模拟服务提供商以供测试使用。
- **音频流媒体**：通过 WebSocket 实现双向音频传输，支持实时对话。
- **访问限制**：与标准 voice_call 插件不同，通话中的用户无法访问网关代理，从而降低了安全风险。

## 凭据

### 必需的凭证

| 凭据 | 来源 | 用途 |
|------------|--------|---------|
| `OPENAI_API_KEY` | [OpenAI](https://platform.openai.com/api-keys) | 用于激活实时语音 AI（GPT-4o） |
| `TWILIO_ACCOUNT_SID` | [Twilio 控制台](https://console.twilio.com) | Twilio 账户标识符 |
| `TWILIO_AUTH_TOKEN` | [Twilio 控制台](https://console.twilio.com) | Twilio API 认证令牌 |

### 可选的凭证

| 凭据 | 来源 | 用途 |
|------------|--------|---------|
| `NGROK_AUTHTOKEN` | [ngrok](https://dashboard.ngrok.com) | 用于 ngrok 隧道认证（仅在使用 ngrok 作为隧道提供商时需要） |

凭证可以通过环境变量或在插件配置中设置（配置优先级更高）。

## 安装

1. 通过 npm 安装该插件，或将其复制到 OpenClaw 的扩展目录中。

2. **启用回调钩子**（对于呼叫完成回调是必需的）：

```json
{
  "hooks": {
    "enabled": true,
    "token": "your-secret-token"
  }
}
```

使用以下命令生成一个安全令牌：`openssl rand -hex 24`

> ⚠️ **安全提示**：`hooks.token` 是敏感信息，用于验证内部回调。请妥善保管，并在泄露时立即更换。

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

**重要提示**：`hooks.token` 是呼叫完成回调所必需的。如果没有这个令牌，代理将无法收到呼叫结束的通知。

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

### 功能

- `persona_call` - 以指定角色发起新呼叫。
- `get_status` - 查查呼叫状态和通话记录。
- `end_call` - 结束正在进行的呼叫。
- `list_calls` - 列出所有正在进行的角色呼叫。

### DTMF / IVR 导航

在通话过程中，AI 会自动处理电话菜单（IVR 系统）。当听到如“按 1 进入销售服务”之类的提示时，它会使用内部的 `send_dtmf` 工具将双音多频数字发送到音频流中。这一过程完全自动化，无需额外配置或人工干预。

- **支持的字符**：`0-9`、`*`、`#`、`A-D`、`w`（表示 500 毫秒的暂停）。
- **示例序列**：`1`（按 1）、`1234567890#`（输入账户号码后按井号）、`1w123#`（先按 1，稍等再输入 123#）。
- **工作原理**：DTMF 数字按照 ITU 标准生成为双频信号，编码为 µ-law（8kHz 单声道格式），然后直接注入到 Twilio 媒体流中。无需任何外部依赖。

这意味着角色驱动的呼叫可以端到端地导航电话菜单——例如：“拨打药房电话，浏览菜单并查询我的处方状态。”

## 配置选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `provider` | 语音服务提供商（twilio/mock） | 必需 |
| `fromNumber` | 主叫方 ID（E.164 格式） | 对于真实服务提供商是必需的 |
| `toNumber` | 接收方号码 | - |
| `twilio.accountSid` | Twilio 账户 SID | 使用 `TWILIO_ACCOUNTSID` 环境变量设置 |
| `twilio.authToken` | Twilio 认证令牌 | 使用 `TWILIO_AUTH_TOKEN` 环境变量设置 |
| `streaming.openaiApiKey` | OpenAI API 密钥（用于实时功能） | 使用 `OPENAI_API_KEY` 环境变量设置 |
| `streaming.silenceDurationMs` | VAD 静默时长（以毫秒为单位） | 800 |
| `streaming.vadThreshold` | VAD 阈值（0-1，数值越大表示越不敏感） | 0.5 |
| `streaming.streamPath` | 媒体流的 WebSocket 路径 | `/voice/stream` |
| `tunnel-provider` | Webhook 的隧道服务（ngrok/tailscale-serve/tailscale-funnel） | 无 |
| `tunnel.ngrokDomain` | ngrok 域名（生产环境推荐使用） | - |
| `tunnel.ngrokAuthToken` | ngrok 认证令牌 | 使用 `NGROK_AUTHTOKEN` 环境变量设置 |

**全实时功能需要** OpenAI API 密钥。

## 系统要求

- Node.js 20 及以上版本。
- 需要 Twilio 账户以实现全实时通话（包括媒体流传输）。
- 需要 ngrok 或 Tailscale 服务来实现 Webhook 隧道（生产环境）。
- 需要 OpenAI API 密钥以使用实时功能。

## 架构

这是一个完全独立的技能模块，不依赖于内置的 voice-call 插件。所有的电话呼叫逻辑都是自包含的。

## 运行时行为与安全

该插件不仅提供指令执行功能，还会实际运行代码、创建进程、打开网络监听器，并将数据写入磁盘。以下是运行时的具体行为：

### 进程创建

当 `tunnel-provider` 设置为 `ngrok` 时，插件会通过 `child_process.spawn` 启动 `ngrok` 命令行工具。如果设置为 `tailscale-serve` 或 `tailscale-funnel`，则会启动 `tailscale` 命令行工具。这些进程会在插件运行期间持续存在，并在插件关闭时终止。如果 `tunnel-provider` 设置为 `none`（或直接提供了 `publicUrl`），则不会创建任何外部进程。

### 网络活动

- **本地 Webhook 服务器**：插件会启动一个 HTTP 服务器（默认地址为 `0.0.0.0:3335`），用于接收 Twilio 的 Webhook 回调和 WebSocket 媒体流。
- **启动自测试**：插件在启动时会向自身的公共 Webhook URL 发送一个带有 `x-supercall-self-test` 标头的 HTTP POST 请求以验证连接是否正常。如果 `publicUrl` 配置错误，自测试请求可能会发送到错误的地址。在启动前请务必检查 `publicUrl` 或隧道配置。
- **出站 API 调用**：插件在通话期间会向 OpenAI Realtime API（WebSocket）和 Twilio REST API 发送请求。

### Webhook 验证

- **Twilio 调用**：使用 Twilio 的 X-Twilio-Signature 标头（HMAC-SHA1）进行验证。
- **自测试请求**：使用启动时生成的内部令牌（`x-supercall-self-test`）进行认证。
- **ngrok 免费 tier 的限制**：在免费 tier 的 ngrok 域名（`.ngrok-free.app`、`.ngrok.io`）下，由于 ngrok 的请求重写机制，URL 可能会发生变化；即使签名不匹配，系统也会允许请求通过。对于付费/自定义的 ngrok 域名（`.ngrok.app`），则会进行严格验证。此限制仅适用于免费 tier 域名，不影响 Tailscale 或直接使用的 `publicUrl` 配置。

### 数据存储

通话记录会保存在 `~/clawd/supercall-logs` 文件夹中。这些日志可能包含敏感的对话内容，请定期审查并轮换日志。

### 最佳实践

- **保护凭证**：Twilio 和 OpenAI 的密钥可访问付费服务，请妥善保管。
- **验证公共 URL**：在启动前确保 `publicUrl` 或隧道配置指向正确的目标地址。
- **定期更换 `hooks.token`**，并在怀疑凭证被泄露时立即更换。
- **审查通话记录**：存储在磁盘上的通话记录可能包含敏感信息，请定期检查。