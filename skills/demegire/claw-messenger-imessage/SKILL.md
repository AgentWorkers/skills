# @emotion-machine/claw-messenger

这是一个用于 [OpenClaw](https://openclaw.ai) 的 iMessage、RCS 和 SMS 插件——无需使用手机或 Mac Mini。

| | |
|---|---|
| **开发者** | [Emotion Machine](https://emotionmachine.ai) |
| **官方网站** | [clawmessenger.com](https://clawmessenger.com) |
| **源代码** | [github.com/emotion-machine-org/claw-messenger](https://github.com/emotion-machine-org/claw-messenger) |
| **npm** | [@emotion-machine/claw-messenger](https://www.npmjs.com/package/@emotion-machine/claw-messenger) |
| **问题报告** | [GitHub 问题报告](https://github.com/emotion-machine-org/claw-messenger/issues) |
| **隐私政策** | [clawmessenger.com/privacy](https://clawmessenger.com/privacy) |
| **定价** | [clawmessenger.com/pricing](https://clawmessenger.com/pricing) |

## 工作原理

Claw Messenger 负责在您的 OpenClaw 代理与 iMessage/RCS/SMS 网络之间转发消息。该插件通过 WebSocket 连接到 Claw Messenger 中继服务器，并使用您的 API 密钥进行身份验证。中继服务器负责处理消息的传输和路由，然后实时将消息转发回您的代理。

```
OpenClaw Agent  ←→  Plugin (local)  ←→  Relay Server (WSS)  ←→  iMessage / RCS / SMS
```

## 所需凭证

此插件需要 **一个凭证**：Claw Messenger API 密钥。

| 属性 | 值 |
|----------|-------|
| **密钥格式** | `cm_live_{tag}_{secret}` |
| **获取途径** | [clawmessenger.com/dashboard](https://clawmessenger.com/dashboard) |
| **安全性要求** | **保密性极高**——请将其视为密码，切勿提交到版本控制系统中。 |
| **存储位置** | 本地存储在 `.openclaw.json` 文件的 `channels.claw-messenger.apiKey` 中 |
| **密钥更新** | 可以随时通过 [仪表板](https://clawmessenger.com/dashboard) 革新密钥 |
| **权限范围** | 仅授权使用您的账户发送和接收消息 |

无需其他凭证、环境变量或秘密信息。

## 配置文件路径

所有插件配置都存储在一个文件中：

**`.openclaw.json` → `channels.claw-messenger`

这是插件唯一读取或写入的文件。完整的配置规范在下面的 [配置参考](#configuration-reference) 中有详细说明，并在插件清单 (`openclaw.plugin.json` → `configSchema`) 中进行了声明。

## 外部连接

该插件仅建立以下一个外部连接：

| 属性 | 值 |
|----------|-------|
| **主机** | `claw-messenger.onrender.com` |
| **协议** | `wss://`（TLS 加密的 WebSocket） |
| **用途** | 作为 OpenClaw 与 iMessage/RCS/SMS 运营商网络之间的中继服务器 |
| **托管平台** | 由 Emotion Machine 在 [Render](https://render.com)（托管型云平台）上托管。`onrender.com` 子域名是 Render 服务的标准域名。 |
| **数据传输** | 该中继服务器仅作为无状态的桥梁使用——消息内容在传输过程中不会被存储，但会记录发送者、接收者和时间戳等元数据，用于跟踪和计费（详见 [隐私政策](https://clawmessenger.com/privacy)）。 |
| **自定义域名** | 如果您的组织需要自定义域名或自行托管，请联系 hello@emotionmachine.ai |

插件不建立其他外部连接。

## 插件清单概述

插件的 `openclaw.plugin.json` 清单声明了以下内容（此处重复以便透明展示）：

- **所需凭证：** `apiKey`（标记为 `sensitive: true`，占位符为 `cm_live_...`）
- **配置文件路径：** `.openclaw.json` → `channels.claw-messenger`
- **外部连接：** `wss://claw-messenger.onrender.com`（中继服务器）
- **配置规范：** `apiKey`（必填字符串），`serverUrl`（可选字符串），`preferredService`（可选枚举），`dmPolicy`（可选枚举），`allowFrom`（可选数组）

所有运行时使用的凭证和配置路径都在清单中明确声明。不存在未声明的秘密信息、环境变量或配置文件。

## 安装

该插件以 [`@emotion-machine/claw-messenger`](https://www.npmjs.com/package/@emotion-machine/claw-messenger) 的名称发布在 npm 上。安装前可以查看包的详细信息：

```bash
npm pack @emotion-machine/claw-messenger --dry-run
```

## 配置

安装完成后，将插件添加到您的 OpenClaw 配置文件（`.openclaw.json`）的 `channels` 部分：

```json5
{
  "channels": {
    "claw-messenger": {
      "enabled": true,
      "apiKey": "cm_live_XXXXXXXX_YYYYYYYYYYYYYY",  // required — your API key
      "serverUrl": "wss://claw-messenger.onrender.com",  // default relay server
      "preferredService": "iMessage",  // "iMessage" | "RCS" | "SMS"
      "dmPolicy": "pairing",           // "open" | "pairing" | "allowlist"
      "allowFrom": ["+15551234567"]    // only used with "allowlist" policy
    }
  }
}
```

### 配置参考

| 字段 | 是否必填 | 默认值 | 说明 |
|-------|----------|---------|-------------|
| `apiKey` | 是 | — | 您的 `cm_live_*` API 密钥，存储在 `.openclaw.json` 中。 |
| `serverUrl` | 否 | `wss://claw-messenger.onrender.com` | WebSocket 中继服务器地址。 |
| `preferredService` | 否 | `iMessage` | 默认的消息传递服务（`iMessage`、`RCS` 或 `SMS`）。 |
| `dmPolicy` | 否 | `pairing` | 收件人确认策略：`open`、`pairing` 或 `allowlist`。 |
| `allowFrom` | 否 | `[]` | 使用 `allowlist` 策略时允许接收消息的手机号码列表。 |

## 安全性与隐私

- 您的 `cm_live_*` API 密钥属于 **高度敏感的凭证**。请将 `.openclaw.json` 添加到 `.gitignore` 文件中，避免将其提交到版本控制系统中。 |
- 可以随时通过 [仪表板](https://clawmessenger.com/dashboard) 革新密钥。建议先使用测试密钥进行测试。 |
- 所有连接均使用 **TLS 加密的 WebSockets**（`wss://`）。消息内容不会存储在中继服务器上。 |
- 会记录消息的元数据（发送者、接收者和时间戳）以用于跟踪和计费（详见 [隐私政策](https://clawmessenger.com/privacy)）。 |
- 计费基于每月的消息发送量。详细信息请参阅 [定价页面](https://clawmessenger.com/pricing)。

## 功能

- **发送和接收** 文本消息及媒体文件（图片、视频、音频、文档）
- **iMessage 动作**（点赞、不喜欢、大笑、强调、提问）
- **群组聊天**——可向现有群组发送消息或创建新群组
- **输入提示**——显示消息的发送和接收状态
- **私信安全策略**——开放式确认、基于配对的确认方式或允许列表

## 代理工具

该插件提供了两个可供代理使用的工具：

| 工具 | 说明 |
|------|-------------|
| `claw_messenger_status` | 检查连接状态、服务器地址和默认消息服务 |
| `claw_messenger_switch_service` | 在运行时切换默认消息服务 |

## 命令行命令

| 命令 | 说明 |
|---------|-------------|
| `/cm-status` | 显示连接状态、服务器地址和默认消息服务 |
| `/cm-switch <service>` | 切换默认消息服务（`iMessage`、`RCS` 或 `SMS`）

## 开始使用

1. 在 [clawmessenger.com](https://clawmessenger.com) 注册账号。
2. 从 [仪表板](https://clawmessenger.com/dashboard) 创建 API 密钥。
3. 安装插件：`openclaw plugins install @emotion-machine/claw-messenger`
4. 使用您的 API 密钥配置插件（请确保 `.openclaw.json` 不被提交到版本控制系统中）。
5. 开始使用——您的代理现在可以发送和接收消息了。

## 技术支持

- **问题报告**：[github.com/emotion-machine-org/claw-messenger/issues](https://github.com/emotion-machine-org/claw-messenger/issues)
- **邮箱**：hello@emotionmachine.ai
- **文档**：[clawmessenger.com/docs](https://clawmessenger.com/docs)

## 许可证

本插件采用 **无许可证**（UNLICENSED）方式提供。