---
name: amber-voice-assistant
description: "适用于 OpenClaw 的具备电话通话功能的 AI 语音代理：已具备生产环境使用条件的 Twilio + OpenAI 实时 SIP 桥接方案（包括运行时支持），内置通话记录仪表板（dashboard/），设置指南，环境配置模板（env templates），验证脚本（validation scripts），安全防护机制（guardrail patterns），以及故障排除操作手册（troubleshooting runbooks）。"
homepage: https://github.com/batthis/amber-openclaw-voice-agent
metadata: {"openclaw":{"emoji":"☎️","requires":{"env":["TWILIO_ACCOUNT_SID","TWILIO_AUTH_TOKEN","TWILIO_CALLER_ID","OPENAI_API_KEY","OPENAI_PROJECT_ID","OPENAI_WEBHOOK_SECRET","PUBLIC_BASE_URL"],"anyBins":["node"]},"primaryEnv":"OPENAI_API_KEY"}}
---
# Amber — 具备电话功能的语音助手

## 概述

Amber 是 OpenClaw 的一个语音子助手，它通过一个适用于生产环境的 Twilio + OpenAI Realtime SIP 桥接（`runtime/`）和通话记录仪表板（`dashboard/`）为你的 OpenClaw 部署添加电话功能。Amber 并不是一个独立的语音助手，而是作为你 OpenClaw 实例的扩展运行，在通话过程中将复杂的决策（如日历查询、联系人查找、审批工作流）委托给 OpenClaw，通过 `ask_openclaw` 工具来完成。

Amber 负责处理来电筛选、拨出电话、预约预订、实时查询 OpenClaw 的知识库内容以及完整的通话历史记录可视化。

### 包含的内容

- **运行时桥接**（`runtime/`）：一个完整的 Node.js 服务器，用于将 Twilio 电话呼叫与 OpenAI Realtime 连接起来，并将 OpenClaw 的智能决策集成到呼叫流程中。
- **通话记录仪表板**（`dashboard/`）：一个实时 Web 用户界面，显示通话历史记录、通话记录文本、捕获的消息、通话摘要以及带有搜索和过滤功能的跟进跟踪。
- **设置与验证脚本**：预检查脚本、环境变量模板、快速启动工具。
- **架构文档与故障排除**：通话流程图、常见故障处理指南。
- **安全机制**：针对拨出电话的审批流程、支付升级、同意权限等安全规则。

## 选择 Amber 的原因

- **几分钟内即可启动语音助手**：只需执行 `npm install`、配置 `.env` 文件，然后运行 `npm start` 即可。
- **全面的来电筛选**：包括问候语、信息记录、与日历系统的集成预约功能。
- **结构化的拨出电话流程**：包括预订、咨询、跟进等环节。
- **`ask_openclaw` 工具**：在通话过程中，语音助手会向 OpenClaw 询问日历信息、联系人信息等。
- **通话记录仪表板**：可以浏览通话历史记录、阅读通话记录文本、跟踪跟进情况，并按来电者/号码/内容进行搜索。
- **自动语言检测**：Amber 能够检测来电者的语言，并在通话过程中自动切换语言（支持阿拉伯语、西班牙语、法语等多种语言）。
- **语音活动检测（VAD）优化**：通过 VAD 优化，确保对话自然流畅（在查询过程中不会出现沉默。
- **完全可配置**：助手名称、操作员信息、组织名称、日历设置、筛选方式等均可通过环境变量进行配置。
- **操作员安全机制**：包括审批、升级、支付处理等安全保障。

## `ask_openclaw` 工具的工作原理

Amber 不仅仅是一个读取脚本的语音机器人；它可以在通话过程中向 OpenClaw 询问信息，以解决自身无法处理的问题。

### 功能流程

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
> *(OpenClaw 查询日历后回复：“周四晚上有空。”)*
> **Amber：**“好的，周四晚上可以！需要我为您安排吗？”

### 配置

该桥接通过 `OPENCLAW/GateWAY_URL`（默认为 `http://127.0.0.1:18789`）与你的 OpenClaw 网关连接，并使用 `OPENCLAW/GateWAY_TOKEN` 进行身份验证。它以聊天消息的形式发送问题，其中包含：
- 提供通话上下文的系统提示（谁在呼叫、呼叫目的、最近的通话记录文本）。
- 语音助手提出的问题作为用户输入的消息。

你的 OpenClaw 实例负责处理后续任务，如日历查询、联系人查找、内存搜索等。

### Amber 何时会发挥作用？

- 当来电者询问系统提示中未包含的信息时（如日程安排、可用性、偏好设置）。
- 当来电者询问关于操作员的信息时。
- 在拨出电话过程中需要验证详细信息时。
- 当问题需要你的个人数据或系统上下文来回答时。

### 语音填充语

为了避免在等待 OpenClaw 回答时出现沉默，Amber 会自动说一些自然的填充语（例如“请稍等，我马上为您确认”）。VAD（语音活动检测）系统经过优化，以避免在通话中断时切断通话。

## Webhook 架构

该桥接提供了两个 Webhook 端点，请确保将每个服务连接到正确的端点：

| 端点 | 来源 | 用途 | 签名验证 |
|----------|--------|---------|----------------------|
| `/twilio/inbound` | Twilio | 接收来电 → 生成 TwiML 以连接到 OpenAI SIP | 无（仅针对 Twilio） |
| `/twilio/status` | Twilio | 通话状态回调（已接听、已挂断、已完成） | 无 |
| `/openai/webhook` | OpenAI Realtime | 来自 OpenAI 的 SIP 通话事件 | ✅ 使用 `openai-signature`（HMAC-SHA256）进行签名验证 |
| `/call/outbound` | 你的应用/OpenClaw | 触发拨出电话 | 仅限内部使用（localhost） |

**常见设置错误**：如果将 Twilio 的语音 Webhook 指向 `/openai/webhook` 而不是 `/twilio/inbound`，会导致调用失败，因为 Twilio 无法发送该端点所需的 `openai-signature` 头部信息。

## 个性化设置要求

在部署之前，用户需要完成以下个性化设置：
- 助手名称/语音和问候语文本。
- 自己的 Twilio 账号和密钥。
- 自己的 OpenAI 项目及其 Webhook 密钥。
- 自己的 OpenClaw 网关/会话端点。
- 自己的通话安全策略（包括审批、升级、支付处理规则）。

## 5 分钟快速启动指南

### 选项 A：运行时桥接（推荐）

1. `cd runtime && npm install`
2. 将 `../references/env.example` 复制到 `runtime/.env` 文件中，并填写你的配置值。
3. `npm run build && npm start`
4. 将你的 Twilio 语音 Webhook 指向 `https://<your-domain>/twilio/inbound`
5. 拨打你的 Twilio 账号——你的语音助手就会接听电话！

### 选项 B：仅进行验证（适用于已有设置）

1. 将 `references/env.example` 复制到你的 `.env` 文件中，并替换其中的占位符。
2. 导出所需的变量（`TWILIO_ACCOUNT_SID`、`TWILIO_AUTH_TOKEN`、`TWILIO_CALLER_ID`、`OPENAI_API_KEY`、`OPENAI_Project_ID`、`OPENAI_WEBHOOK_SECRET`、`PUBLIC_BASE_URL`）。
3. 运行快速设置脚本：`scripts/setup_quickstart.sh`
4. 如果预检查通过，执行一个来电测试和一个拨出电话测试。
5. 确认无误后，再投入生产环境使用。

## 安全默认设置

- 拨出电话前需要明确获得操作员的批准。
- 如果请求支付或预付款，应停止通话并转接给人工操作员。
- 保持问候语简短明了。
- 当 `ask_openclaw` 响应缓慢或不可用时，设置超时机制和优雅的回退策略。

## 工作流程

1. **确认 V1 版本的功能范围**：
   - 仅包含稳定的功能：通话流程、桥接行为、回退策略和设置步骤。
   - 不包括特定于机器的密钥和私有路径。

2. **记录架构和限制**：
   - 阅读 `references/architecture.md`。
   - 确保功能描述符合实际情况（延迟可能会有所变化；内存查询为尽力而为）。

3. **运行发布检查列表**：
   - 阅读 `references/release-checklist.md`。
   - 验证配置参数、安全机制和故障处理流程。

4. **测试运行时环境**：
   - 在目标主机上运行 `scripts/validate_voice_env.sh`。
   - 在发布前修复任何缺失的环境变量或配置问题。

5. **发布**：
   - 将技能包发布到 ClawHub（示例命令：`clawhub publish <skill-folder> --slug amber-voice-assistant --name "Amber Voice Assistant" --version 1.0.0 --tags latest --changelog "Initial public release"`。
   - 可选：在发布前运行本地技能验证工具。

6. **发布更新**：
   - 发布新的半版本（如 `1.0.1`、`1.1.0`、`2.0.0`）并附上变更日志。
   - 保持 `latest` 版本作为推荐版本。

## 通话记录仪表板

内置的仪表板提供了一个实时 Web 用户界面，用于查看通话历史记录。

### 设置步骤

1. `cd dashboard`
2. （可选）根据 `contacts.example.json` 创建 `contacts.json` 文件以用于解析来电者名称。
3. 处理通话记录：`TWILIO_CALLER_ID=+1... node process_logs.js`
4. 运行服务器：`node scripts/serve.js` → 打开 `http://localhost:8080`

### 功能特点

- 所有来电/拨出电话的时间线视图。
- 每次通话的完整通话记录文本显示。
- 捕获的消息提取（包括来电者名称、回拨号码、消息内容）。
- 由 AI 生成的通话摘要（意图、结果、下一步操作）。
- 可按名称、号码、通话记录文本或通话 ID 进行搜索。
- 支持本地存储的跟进标记功能。
- 新数据可用时自动刷新。
- 可按通话方向、通话记录是否可用或捕获的消息进行过滤。

### 环境变量

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `TWILIO_CALLER_ID` | *(必填)* | 用于识别通话方向的 Twilio 账号 |
| `ASSISTANT_NAME` | `Amber` | 通话记录中显示的语音助手名称 |
| `OPERATOR_NAME` | `the operator` | 通话摘要中使用的操作员名称（例如：“消息已传递给...”） |
| `CONTACTS_FILE` | `./contacts.json` | 可选的电话号码到名称的映射文件 |
| `LOGS_DIR` | `../runtime/logs` | 存储通话记录文件的目录 |
| `OUTPUT_DIR` | `./data` | 处理后的 JSON 文件保存路径 |

详细文档请参阅 `dashboard/README.md`。

## 常见故障排除方法

- **“缺少环境变量”**：重新检查 `.env` 文件中的配置值，并重新运行 `scripts/validate_voice_env.sh`。
- **“通话连接成功但助手无响应”**：检查 TTS 模型的设置和提供商的身份验证。
- **“ask_openclaw 超时”**：检查网关 URL/令牌设置，并适当增加超时时间。
- **“Webhook 无法访问”**：检查隧道/域名和 Twilio Webhook 的目标地址。

## 公开发布的注意事项

- 绝不要发布任何密钥、令牌、电话号码、Webhook URL、凭证或个人数据。
- 为拨出电话、支付和升级设置明确的安全规则。
- 如果对话质量或延迟仍在调整中，将 V1 版本标记为测试版。

## 支持与贡献

发现漏洞？有功能需求？想要贡献代码？

- **问题与功能请求**：[GitHub 问题页面](https://github.com/batthis/amber-openclaw-voice-agent/issues)
- **源代码**：[github.com/batthis/amber-openclaw-voice-agent](https://github.com/batthis/amber-openclaw-voice-agent)
- **欢迎提交 Pull 请求**：克隆仓库，进行修改并提交 PR。

## 资源

- **运行时桥接**：`runtime/`（包含完整源代码和 README 文件）
- **通话记录仪表板**：`dashboard/`（Web 用户界面和日志处理脚本）
- 架构和行为说明：`references/architecture.md`
- 发布检查列表：`references/release-checklist.md`
- 环境变量模板：`references/env.example`
- 快速启动脚本：`scripts/setup_quickstart.sh`
- 环境配置验证工具：`scripts/validate_voice_env.sh`