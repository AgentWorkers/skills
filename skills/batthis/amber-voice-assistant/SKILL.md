---
name: amber-voice-assistant
description: "OpenClaw 最全面的电话功能：具备生产环境所需的低延迟 AI 通话能力（包括来电和去电），支持多语言处理，提供实时监控界面，并实现智能辅助决策（brain-in-the-loop）。"
homepage: https://github.com/batthis/amber-openclaw-voice-agent
metadata: {"openclaw":{"emoji":"☎️","requires":{"env":["TWILIO_ACCOUNT_SID","TWILIO_AUTH_TOKEN","TWILIO_CALLER_ID","OPENAI_API_KEY","OPENAI_PROJECT_ID","OPENAI_WEBHOOK_SECRET","PUBLIC_BASE_URL"],"optionalEnv":["OPENCLAW_GATEWAY_URL","OPENCLAW_GATEWAY_TOKEN","BRIDGE_API_TOKEN","TWILIO_WEBHOOK_STRICT","VOICE_PROVIDER","VOICE_WEBHOOK_SECRET"],"anyBins":["node","ical-query"]},"primaryEnv":"OPENAI_API_KEY"}}
---
# Amber — 具有电话功能的语音助手

## 概述

Amber 是 OpenClaw 的一个语音子助手，它通过一个适用于生产环境的 Twilio + OpenAI Realtime SIP 桥接（`runtime/`）和通话记录仪表板（`dashboard/`）为你的 OpenClaw 部署添加电话功能。Amber 并不是一个独立的语音助手；它作为你 OpenClaw 实例的扩展运行，在通话过程中将复杂的决策（如日历查询、联系人解析、审批工作流）通过 `ask_openclaw` 工具委托给 OpenClaw 处理。

Amber 负责处理来电筛选、拨出电话、预约预订、实时查询 OpenClaw 的知识库内容以及完整通话历史的可视化展示。

### 包含的内容

- **运行时桥接**（`runtime/`）：一个完整的 Node.js 服务器，用于将 Twilio 电话呼叫连接到 OpenAI Realtime，并在 OpenClaw 中实现智能处理。
- **通话记录仪表板**（`dashboard/`）：一个实时 Web UI，显示通话历史、通话记录、捕获的消息、通话摘要以及带有搜索和过滤功能的跟进跟踪。
- **设置与验证脚本**：预检工具、环境变量模板、快速启动脚本。
- **架构文档与故障排除**：通话流程图、常见故障处理指南。
- **安全防护措施**：针对拨出电话的审批流程、支付升级、同意权限的设置。

## 为什么选择 Amber 而不是其他语音助手

大多数在 ClawHub 上的语音助手都是通过托管服务（如 Bland AI、VAPI、Pamela）来路由电话呼叫的。Amber 采用了不同的方式：你拥有整个技术栈，且在整个通话过程中 OpenClaw 的智能处理能力始终处于活跃状态。

**Amber 的优势：**

- **实时通话仪表板**：提供实时 Web UI，显示完整的通话记录、捕获的消息、跟进跟踪以及搜索/过滤功能。ClawHub 上没有其他语音助手具备这些功能。
- **OpenClaw 智能处理**：`ask_openclaw` 工具在通话过程中将复杂的决策（如日历查询、联系人解析、审批工作流）委托给你的 OpenClaw 实例处理，而不会挂断通话。
- **统一处理来电和拨出电话**：使用相同的配置和同一个助手处理所有来电和拨出电话。
- **多语言自动检测**：Amber 可以自动检测来电者的语言，并使用 OpenAI Realtime 以相应的语言进行响应。支持阿拉伯语、西班牙语、法语等多种语言，无需额外配置。
- **自然的对话体验**：通过语音活动检测（VAD）和语言填充词，确保对话流畅进行，避免在查询或处理过程中出现沉默。
- **可更换的通话服务提供商**：默认使用 Twilio，也可以通过 `VOICE_PROVIDER` 更换为 Telnyx 或其他支持的通话服务提供商。无需修改任何代码。
- **生产环境的安全加固**：具备 Webhook 签名验证、身份验证控制端点、防止注入攻击的防护措施；如果在生产环境中缺少密钥，系统会发出警报。
- **完整的通话历史记录**：每次通话都会被记录下来，包括通话记录、摘要、意图和来电者信息。仪表板会自动显示未处理的跟进事项。
- **完全可配置**：助手名称、操作员信息、组织名称、日历集成等都可以通过环境变量进行设置。只需执行 `npm install`、配置 `.env`、`npm start` 即可启动。

## `ask_openclaw` 工具的工作原理

Amber 不只是一个简单读取脚本的语音机器人；它可以在通话过程中咨询你的 OpenClaw 实例，以回答那些它本身无法回答的问题。

### 工作流程

```
Caller asks a question
        ↓
Amber (OpenAI Realtime) decides she needs more info
        ↓
Amber says "One moment, let me check on that for you"
        ↓
Amber calls the `ask_openclaw` tool with a short question
        ↓
Bridge sends the question to your OpenClaw gateway
  (via POST /v1/chat/completions on localhost)
        ↓
OpenClaw checks calendar, contacts, memory, etc.
        ↓
Response comes back → Amber speaks the answer to the caller
```

### 示例

> **来电者：**“Abe 周四有空吗？”
> **Amber：**“让我帮您确认一下……”
> *(Amber 调用 ask_openclaw：“Abe 周四晚上有空吗？”)*
> *(OpenClaw 查询日历后回复：“Abe 周四晚上有空。”)*
> **Amber：**“好的，周四晚上可以！需要我帮忙安排吗？”

### 配置

该桥接通过 `OPENCLAW_GATEWAY_URL`（默认为 `http://127.0.0.1:18789`）连接到你的 OpenClaw 网关，并使用 `OPENCLAW_GATEWAY_TOKEN` 进行身份验证。它以聊天消息的形式发送问题，其中包含：

- 提供通话上下文的系统提示（谁在呼叫、目的、最近的通话记录）
- 语音助手提出的问题作为用户输入

你的 OpenClaw 实例负责处理剩余的部分——包括日历查询、联系人解析、内存搜索或你配置的任何其他功能。

### Amber 何时会发挥作用？

- 当来电者提出的问题不在系统提示范围内时（例如日程安排、可用性、偏好设置）。
- 当来电者询问关于操作员的信息时。
- 在拨出电话时，Amber 需要在通话过程中验证详细信息。
- 任何需要你个人数据或上下文来回答的问题。

### 语言填充词

为了避免在等待 OpenClaw 回答时出现沉默，Amber 会自动说一些自然的语言填充词，例如“稍等，让我确认一下”。语音活动检测（VAD）经过调整，以防止在通话中断时切断与来电者的连接。

## 运行时环境变量

### 必需变量

| 变量 | 描述 |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | 你的 Twilio 账户 SID |
| `TWILIO_AUTH_TOKEN` | 你的 Twilio 认证令牌（用于 API 调用和可选的 Webhook 验证） |
| `TWILIO_CALLER_ID` | 你的 Twilio 电话号码（E.164 格式，例如 `+14165551234`） |
| `OPENAI_API_KEY` | 你的 OpenAI API 密钥 |
| `OPENAIPROJECT_ID` | 你的 OpenAI 项目 ID（用于实时 SIP） |
| `OPENAI_WEBHOOK_SECRET` | 你的 OpenAI Webhook 密钥（用于签名验证） |
| `PUBLIC_BASE_URL` | 你的桥接服务的公共 URL（例如 `https://your-domain.com`） |

### 可选变量

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `OPENCLAW_GATEWAY_URL` | `http://127.0.0.1:18789` | `ask_openclaw` 工具使用的 OpenClaw 网关 URL |
| `OPENCLAW_GATEWAY_TOKEN` | **空** | 用于身份验证的令牌 |
| `BRIDGE_API_TOKEN` | **空** | 如果设置此变量，则 `/call/outbound` 和 `/openclaw/ask` 端点需要 `Authorization: Bearer <token>`。如果没有设置，这些端点仅限本地访问。 |
| `VOICE_PROVIDER` | `twilio` | 通话服务提供商。当前支持 `twilio`（适用于生产环境），`telnyx`（仅作为示例，尚未实现）。更换提供商无需修改代码。 |
| `VOICE_WEBHOOK_SECRET` | **默认使用 `TWILIO_AUTH_TOKEN`** | 如果 `VOICE_PROVIDER` 不是 `twilio`，则需要此变量来进行 Webhook 验证。在生产环境中必须设置。 |
| `TWILIO_WEBHOOK_STRICT` | `true` | 如果设置为 `false`，在无效的 Twilio 签名时会记录警告，但仍然会处理请求（仅限开发环境）。默认值为 `true`。 |
| `ASSISTANT_NAME` | `Amber` | 你的语音助手名称 |
| `OPERATOR_NAME` | `your operator` | 语音助手所代表的操作员名称 |
| `OPERATOR_PHONE` | **空** | 操作员的电话号码（用于备用响应） |
| `OPERATOR_EMAIL` | **空** | 操作员的电子邮件（用于备用响应） |
| `ORG_NAME` | **空** | 组织名称（包含在问候语中） |
| `DEFAULT_CALENDAR` | **空** | 预约的默认日历名称（例如 `Abe`） |
| `OPENAI_VOICE` | `alloy` | OpenAI TTS 语音类型（`alloy`、`echo`、`fable`、`onyx`、`nova`、`shimmer`） |
| `GENZ_CALLER_NUMBERS` | **空** | 以逗号分隔的 E.164 格式电话号码列表，用于 Gen Z 人群的筛选 |
| `OUTBOUND_MAP_PATH` | `<cwd>/data/bridge-outbound-map.json` | 存储拨出电话元数据的路径 |

### 安全注意事项

- **`BRIDGE_API_TOKEN`**：保护 `/call/outbound` 和 `/openclaw/ask` 端点免受未经授权的访问。如果未设置此变量，这些端点仅接受来自本地的请求。**强烈建议** 在桥接服务可访问互联网的情况下使用。
- **`VOICE_PROVIDER`**：选择通话服务提供商。Amber 使用了一种分离的架构：通话服务提供商层（电话号码、PSTN 路由）与 AI 流程分离。生产环境默认使用 `twilio`。如果设置 `telnyx`，在 `runtime/src/providers/telnyx.ts` 中实现相应逻辑。未来可以添加其他提供商而无需修改核心代码。
- **`TWILIO_WEBHOOK_STRICT`**：默认值为 `true`——无效的 Twilio Webhook 签名会被拒绝。仅在开发环境中将 `TWILIO_WEBHOOK_STRICT` 设置为 `false`。在生产环境中不要禁用此设置。

## ⚠️ 生产环境安全检查清单

在将 Amber 推向公共互联网之前，请验证以下内容：

| # | 检查项 | 如果跳过可能带来的风险 |
|---|-------|-----------------|
| 1 | **设置 `BRIDGE_API_TOKEN`** | 确保 `/call/outbound` 和 `/openclaw/ask` 仅限本地访问。如果桥接服务可访问互联网且未设置此变量，任何人都可以触发拨出电话或查询你的 OpenClaw 实例。 |
| 2 | **设置 `VOICE_WEBHOOK_SECRET`**（或确保 `TWILIO_AUTH_TOKEN` 已设置） | 对于非 Twilio 服务提供商：如果在 `NODE_ENV=production` 时未设置此变量，桥接服务将无法启动并会抛出错误。对于 Twilio，会使用 `TWILIO_AUTH_TOKEN` 作为默认值。如果同时未设置 `BRIDGE_API_TOKEN`，则会接受伪造的请求。 |
| 3 | **不要禁用 `TWILIO_WEBHOOK_STRICT`** | 默认值为 `true`——无效的 Twilio Webhook 签名会被拒绝。仅在开发环境中将 `TWILIO_WEBHOOK_STRICT` 设置为 `false`。在生产环境中禁用此设置会导致伪造的 Twilio Webhook 请求被接受。 |
| 4 | **保护仪表板** | `dashboard/` 会暴露通话记录和来电者元数据。请在提供身份验证的情况下提供该服务，或仅允许本地访问。 |
| 5 | **不要提交 `dashboard/data/` 目录** | 运行时通话日志包含来电者名称和电话号码。这些信息在 Git 和发布的技能包中被排除——请保持这种设置。 |

## 外部依赖项

### `ical-query`（可选）
`ical-query` 是一个 macOS 的 Swift CLI 工具，通过 EventKit 读取 Apple 日历——它不是一个第三方包。在 `AGENT.md` 中提到，用于在通话处理过程中实时检查日历可用性。只有当你希望 Amber 在通话过程中查询本地 Apple 日历时才需要它。

- **来源：** 随 OpenClaw 一起提供的工具（`/usr/local/bin/ical-query`）——在 macOS 上由 OpenClaw 自动安装。
- **非必需：** 如果没有 `ical-query`，Amber 仍然可以正常工作；`AGENT.md` 中的日历检查指令也不会执行。
- **平台限制：** 仅适用于 macOS（需要 EventKit）。在 Linux/Windows 上不可用；如果在非 Apple 主机上部署，请忽略 `AGENT.md` 中的相关内容。

### `ical-query` 参数安全

`ical-query` 由 OpenClaw 助手调用（而不是由桥接服务直接调用）。为了防止通过恶意参数注入进行远程代码执行（RCE），`AGENT.md` 对参数进行了严格限制：

- **允许的子命令：** `today`、`tomorrow`、`week`、`range`、`calendars`——其他命令不允许。
- **`range` 日期参数：** 必须严格匹配 `YYYY-MM-DD` 格式——在使用日期作为参数之前，助手必须验证其格式。
- **不允许在参数中包含来电者的输入：** 来电者的自由格式语音、名称或任何用户输入都不能被插入到 `ical-query` 的参数中。
- 桥接服务运行时本身不会直接调用 `ical-query`——而是由 OpenClaw 自带的沙箱执行器处理。这一深度防御措施限制了助手的逻辑执行和工具的执行环境。

有关完整的参数安全规则，请参阅 `AGENT.md` 中的“日历”部分。

### `SUMMARY_JSON` 结构化输出

`AGENT.md` 指示 Amber 在通话结束时输出一个静默的 `SUMMARY_JSON` 标签。这并不是用于数据泄露的机制——它仅由 OpenClaw 自带的 SIP Webhook 处理器（`/openai/webhook`）消费，用于提取来电者名称、回拨号码和消息，以便存储在本地通话日志和可选的 OpenClaw 通知中。

- **处理者：** `runtime/src/index.ts` Webhook 处理器——在你的本地主机上运行。
- **存储位置：** 存储在 `runtime/data/` 目录中（仅限本地），并且可以通过 `ask_openclaw`（由你配置）转发到你的 OpenClaw 网关。
- **不会外部传输：** 任何第三方服务都不会接收此输出。桥接服务没有数据分析、遥测或外部数据转发功能。
- **数据范围：** 仅包含来电者提供的信息：名称、回拨号码和消息——不包括系统数据、凭据或环境变量。

## 通话记录数据和隐私

通话记录仪表板（`dashboard/`）将通话记录和来电者元数据存储在 `dashboard/data/` 目录中。此目录**不包括在发布的技能包和 Git 历史记录中**——它包含的是仅适用于你的部署环境的运行时生成的数据。

- `dashboard/data/calls.json` 和 `dashboard/data/calls.js` 是在运行时生成的，并在 `.gitignore` 文件中列出。
- 发布的技能包仅包含 `dashboard/data/sample.*` 文件（已匿名处理，非真实数据），用于 UI 开发/演示目的。
- **建议：** 如果你的桥接服务可访问互联网，请设置 `BRIDGE_API_TOKEN` 并在提供身份验证的情况下提供仪表板服务，或仅允许本地访问。

## Webhook 架构

桥接服务提供了两个 Webhook 端点——请确保将每个服务指向正确的端点：

| 端点 | 来源 | 目的 | 签名验证 |
|----------|--------|---------|----------------------|
| `/twilio/inbound` | Twilio | 接收来电电话 → 生成 TwiML 以连接到 OpenAI SIP | 无（面向 Twilio） |
| `/twilio/status` | Twilio | 通话状态回调（已接听、已接通、已完成） | 无 |
| `/openai/webhook` | OpenAI Realtime | 来自 OpenAI 的 SIP 通话事件 | ✅ 使用 `openai-signature` 进行 HMAC-SHA256 签名验证 |
| `/call/outbound` | 你的应用/OpenClaw | 触发拨出电话 | 仅限本地访问 |

**常见的设置错误：** 如果将 Twilio 的语音 Webhook 指向 `/openai/webhook` 而不是 `/twilio/inbound`，通话将会失败，因为 Twilio 不会发送 `/openai-signature` 标头。

## 个性化设置

在部署之前，用户需要自定义以下内容：
- 助手名称/语音和问候语
- 自己的 Twilio 账户和电话号码
- 自己的 OpenAI 项目和 Webhook 密钥
- 自己的 OpenClaw 网关/会话端点
- 自己的通话安全策略（审批、升级、支付处理）

请不要使用其他操作员的示例配置。

## 5 分钟快速启动指南

### 选项 A：运行时桥接（推荐）

1. `cd runtime && npm install`
2. 将 `../references/env.example` 复制到 `runtime/.env` 并填写你的配置信息。
3. `npm run build && npm start`
4. 将你的 Twilio 语音 Webhook 指向 `https://<your-domain>/twilio/inbound`
5. 拨打你的 Twilio 电话号码——你的语音助手会接听！

### 选项 B：仅验证（现有设置）

1. 将 `references/env.example` 复制到你的 `.env` 文件并替换占位符。
2. 导出所需的变量（`TWILIO_ACCOUNT_SID`、`TWILIO_AUTH_TOKEN`、`TWILIO_CALLER_ID`、`OPENAI_API_KEY`、`OPENAIPROJECT_ID`、`OPENAI_WEBHOOK_SECRET`、`PUBLIC_BASE_URL`）。
3. 运行快速设置脚本：`scripts/setup_quickstart.sh`
4. 如果预检通过，运行一个来电测试和一个拨出电话测试。
5. 确认无误后，再投入生产环境使用。

## 安全默认设置

- 拨出电话前需要明确获得批准。
- 如果请求支付或押金，停止操作并转交给人工操作员处理。
- 保持问候语简短明了。
- 当 `ask_openclaw` 响应缓慢或不可用时，设置超时和优雅的备用方案。

## 工作流程

1. **确认 V1 的功能范围**
   - 仅包含稳定的行为：通话流程、桥接服务行为、备用方案和设置步骤。
   - 不包括特定于机器的密钥和私有路径。
2. **记录架构和限制**
   - 阅读 `references/architecture.md`。
   - 保证声明的内容现实可行（延迟可能会有所不同；内存查询仅供参考）。
3. **运行发布检查清单**
   - 阅读 `references/release-checklist.md`。
   - 验证配置参数、安全防护措施和故障处理方式。
4. **运行运行时假设的测试**
   - 在目标主机上运行 `scripts/validate_voice_env.sh`。
   - 在发布前修复缺失的环境变量或配置问题。
5. **发布**
   - 将技能发布到 ClawHub（示例命令：`clawhub publish <skill-folder> --slug amber-voice-assistant --name "Amber Voice Assistant" --version 1.0.0 --tags latest --changelog "Initial public release"`。
   - 可选：在发布前运行本地技能验证工具/打包工具。
6. **发布更新**
   - 发布新的版本号（`1.0.1`、`1.1.0`、`2.0.0`）并附上变更日志。
   - 保持 `latest` 版本为最新版本。

## 通话记录仪表板

内置的仪表板提供了一个实时 Web UI，用于浏览通话历史记录。

### 设置

1. `cd dashboard`
2. （可选）根据 `contacts.example.json` 创建 `contacts.json` 文件以解析来电者名称。
3. 处理日志：`TWILIO_CALLER_ID=+1... node process_logs.js`
4. 提供服务：`node scripts/serve.js` → 打开 `http://localhost:8080`

### 功能

- 所有来电/拨出电话的时间线视图
- 每次通话的完整通话记录显示
- 捕获的消息提取（名称、回拨号码、消息）
- 由 AI 生成的通话摘要（意图、结果、下一步操作）
- 可以通过名称、号码、通话记录内容或通话 SID 进行搜索
- 支持根据名称、号码或通话记录内容进行筛选，并保留本地数据
- 新数据可用时自动刷新
- 可以根据方向、通话记录的可用性或捕获的消息进行筛选

### 环境变量

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `TWILIO_CALLER_ID` | **必需** | 你的 Twilio 电话号码，用于判断通话方向 |
| `ASSISTANT_NAME` | `Amber` | 通话记录中显示的语音助手名称 |
| `OPERATOR_NAME` | `the operator` | 通话摘要中使用的操作员名称 |
| `CONTACTS_FILE` | `./contacts.json` | 可选的电话号码到名称的映射文件 |
| `LOGS_DIR` | `../runtime/logs` | 包含通话日志文件的目录 |
| `OUTPUT_DIR` | `./data` | 处理后的 JSON 文件存储位置 |
| `BRIDGE_OUTBOUND_MAP` | `<LOGS_DIR>/bridge-outbound-map.json` | 存储拨出电话映射信息的路径 |

有关完整文档，请参阅 `dashboard/README.md`。

## 故障排除（常见问题）

- **“缺少环境变量”** → 重新检查 `.env` 文件中的值并重新运行 `scripts/validate_voice_env.sh`。
- **“通话连接成功但助手未响应”** → 检查 TTS 模型的设置和提供商的身份验证。
- **“ask_openclaw 超时”** → 检查网关 URL/令牌，并适当增加超时时间。
- **“Webhook 无法访问”** | 检查隧道/域名和 Twilio Webhook 目标。

## 公开发布时的安全注意事项

- **切勿公开密钥、令牌、电话号码、Webhook URL、凭据或个人数据。**
- 为拨出电话、支付和升级设置明确的安全规则。
- 如果对话质量或延迟仍在调整中，将 V1 版本标记为测试版。

## 支持与贡献

发现漏洞？有功能需求？想要贡献代码？

- **问题与功能请求：** [GitHub Issues](https://github.com/batthis/amber-openclaw-voice-agent/issues)
- **源代码：** [github.com/batthis/amber-openclaw-voice-agent](https://github.com/batthis/amber-openclaw-voice-agent)
- **欢迎提交 Pull 请求** — 分支仓库，进行修改并提交 PR。

## 资源

- **运行时桥接服务：`runtime/`（完整源代码和 README）**
- **通话记录仪表板：`dashboard/`（Web UI 和日志处理程序）**
- 架构和行为说明：`references/architecture.md`
- 发布检查清单：`references/release-checklist.md`
- 环境变量模板：`references/env.example`
- 快速设置脚本：`scripts/setup_quickstart.sh`
- 环境变量验证脚本：`scripts/validate_voice_env.sh`