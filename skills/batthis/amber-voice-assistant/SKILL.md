---
name: amber-voice-assistant
title: "Amber — Phone-Capable Voice Agent"
description: "OpenClaw 最出色的语音和电话通话功能：支持通过 Twilio 进行呼入和呼出通话，并利用 OpenAI 的实时语音技术实现语音交互。具备来电管理、去电管理、日历管理、客户关系管理（CRM）功能，以及支持多种语言的电话助手服务，同时提供通话记录。系统还配备了设置向导、实时监控面板以及智能升级机制。现在该功能也作为 Claude Desktop 的插件（MCP）提供——用户可以直接通过 Claude Desktop 进行通话、查询客户关系管理信息以及查看日历安排。"
homepage: https://github.com/batthis/amber-openclaw-voice-agent
metadata: {"openclaw":{"emoji":"☎️","requires":{"env":["TWILIO_ACCOUNT_SID","TWILIO_AUTH_TOKEN","TWILIO_CALLER_ID","OPENAI_API_KEY","OPENAI_PROJECT_ID","OPENAI_WEBHOOK_SECRET","PUBLIC_BASE_URL"],"optionalEnv":["OPENCLAW_GATEWAY_URL","OPENCLAW_GATEWAY_TOKEN","BRIDGE_API_TOKEN","TWILIO_WEBHOOK_STRICT","VOICE_PROVIDER","VOICE_WEBHOOK_SECRET"],"anyBins":["node","ical-query","bash"]},"primaryEnv":"OPENAI_API_KEY","install":[{"id":"runtime","kind":"node","cwd":"runtime","label":"Install Amber runtime (cd runtime && npm install && npm run build)"}]}}
---
# Amber — 具备电话功能的语音助手

## 概述

Amber 为任何基于 OpenClaw 的部署方案提供了一款具备电话功能的人工智能语音助手。它内置了一个 **适用于生产环境的 Twilio + OpenAI Realtime 桥接器**（`runtime/`），能够处理来电筛选、拨出电话、预约预订以及实时查询 OpenClaw 知识库——所有这些操作都通过自然语言对话完成。

**✨ v5.4.0 的新功能：** Amber 现在作为 **Claude Desktop MCP 插件** 提供，包含 9 个工具：可以通过 Claude Desktop 或 Claude Cowork 按名称拨出电话、查看通话记录、查询 CRM 联系人、管理日历以及控制通话筛选。此外还支持与 Apple Contacts 的集成，并加入了防止误拨电话的防护机制。

**✨ 其他功能：** 交互式设置向导 (`npm run setup`) 可实时验证凭据并生成可用的 `.env` 文件——无需手动配置！

## 功能演示

![设置向导演示](demo/demo.gif)

**[▶️ 在 asciinema.org 上观看交互式演示](https://asciinema.org/a/l1nOHktunybwAheQ)**（可复制文本，可调节播放速度）

*交互式向导会实时验证凭据，检测 ngrok 的存在，并在几分钟内生成完整的 `.env` 文件。*

### 包含的内容

- **运行时桥接器** (`runtime/`) — 一个完整的 Node.js 服务器，用于将 Twilio 电话呼叫连接到 OpenAI Realtime，并在 OpenClaw 中实现智能处理。
- **Amber 技能** (`amber-skills/`) — 提供了模块化的通话中功能（如 CRM、日历管理、日志记录和消息转发），同时提供了自定义功能的规范。
- **内置 CRM** — 使用本地 SQLite 数据库存储联系人信息；Amber 会根据联系人姓名进行问候，并在每次通话中自然地引用其个人信息。
- **通话日志仪表板** (`dashboard/`) — 可查看通话记录、通话录音和捕获的消息；提供 **手动同步按钮**，可根据需要拉取新通话数据。
- **设置与验证脚本** — 包含预检功能、环境变量模板和快速启动工具。
- **架构文档与故障排除** — 提供通话流程图和常见故障处理指南。
- **安全防护机制** — 包括对外拨电话的审批流程、支付升级机制和隐私保护措施。

## 🔌 Amber 技能 — 可扩展的设计

Amber 配备了一个不断扩展的 **Amber 技能** 库——这些模块化功能可以直接插入到实时语音对话中。每个技能都暴露了一个结构化的函数，允许你在不修改桥接器代码的情况下构建强大的语音工作流程。

### 👤 CRM — 联系人管理 *(v5.3.0)*

Amber 能够跨多次通话记住每个来电者的信息，并利用这些信息来个性化每次对话。

- **运行时管理** — 自动执行查询和日志记录；Amber 无需手动“记住”要查询 CRM 的信息。
- **个性化问候** — 会按姓名问候已知来电者；在开场白中自然地提及个人相关信息（如宠物、近期事件、偏好设置）。
- **双重数据采集** — 自动记录通话内容；通话结束后会使用大型语言模型 (LLM) 提取来电者的姓名、电子邮件和 `context_notes`。
- **双向支持** — 对来电和去电均适用。
- **本地 SQLite 数据库** — 数据存储在 `~/.config/amber/crm.sqlite` 中；数据不会离开用户的设备。
- **依赖库要求** — 需要 `better-sqlite3`（原生构建库）。macOS 用户需执行 `sudo xcodebuild -license accept`；Linux 用户需安装 `build-essential` 和 `python3`。

### 📅 日历

可以在通话过程中查询操作员的日历安排或预订新事件。

- **查询可用性** — 可查看今天、明天、本周或任何特定日期的可用/忙碌时间。
- **事件创建** — 可直接通过电话对话在操作员的日历中预订预约。
- **默认隐私保护** — 仅告知来电者操作员是否忙碌；事件标题、名称和地点等信息不会被透露。
- **基于 ical-query** 实现 — 仅使用本地数据，无网络延迟。

### 📬 日志记录与消息转发

允许来电者留言，留言会自动保存并转发给操作员。

- 记录来电者的留言、姓名和可选的回拨号码。
- 首先会保存到通话日志中（作为审计痕迹），然后通过操作员配置的消息渠道发送。
- 发送前会先征得来电者的确认。
- 发送目的地由操作员自行配置；来电者无法更改留言的发送目的地。

### 自定义技能

Amber 的技能系统具有高度可扩展性。每个技能都是一个独立的目录，包含 `SKILL.md`（元数据 + 函数规范）和 `handler.js` 文件。你可以：
- **根据自身需求定制内置技能**
- **为特定场景开发新技能**（如 CRM 查询、库存检查、自定义通知等）
- **通过 [ClawHub](https://clawhub.com) 与 OpenClaw 社区分享技能**

更多示例和详细规范请参见 [`amber-skills/`](amber-skills/)。

> **注意：** 每个技能的 `handler.js` 文件都会根据其声明的权限进行审查。在构建或安装第三方技能时，请像处理普通 Node.js 模块一样审查其源代码。

### 通话日志仪表板

```bash
cd dashboard && node scripts/serve.js   # → http://localhost:8787
```

- **⬇ 同步按钮**（绿色）——立即从 `runtime/logs/` 中拉取新通话数据并刷新仪表板。建议在通话结束后立即使用此按钮，无需等待后台同步。
- **↻ 刷新按钮**（蓝色）——仅从磁盘重新加载现有数据，不会重新处理日志。
- 后台同步脚本 (`node scripts/watch.js`) 在运行时每 30 秒自动同步一次数据。

## 选择 Amber 的理由

- **几分钟内即可部署语音助手** — 只需执行 `npm install`、配置 `.env`，然后运行 `npm start`。
- 全面支持来电筛选功能：包括问候、留言记录和日历集成。
- 支持结构化的去电流程（如预约预订、咨询、跟进等）。
- **`ask_openclaw` 工具**（最小权限设计）——语音助手仅在需要查询日历信息或执行关键操作时才会访问 OpenClaw 网关，避免不必要的数据访问。
- 通过 VAD（Voice Activity Detection）优化对话流程，确保对话自然流畅（避免查询时的沉默环节）。
- 全面可配置：助手名称、操作员信息、组织名称、日历设置、筛选规则等均可通过环境变量进行调整。
- 提供操作员安全防护机制，包括审批流程、升级处理和支付管理功能。

## 个性化设置要求

在部署前，用户需要完成以下个性化设置：
- 选择助手名称/语音及问候语
- 提供自己的 Twilio 号码和账户凭据
- 配置自己的 OpenAI 项目和 Webhook 密钥
- 设置自己的 OpenClaw 网关/会话端点
- 定义自己的通话安全策略（包括审批流程、升级机制和支付处理方式）

切勿使用其他操作员的示例配置。

## 5 分钟快速入门

### 选项 A：交互式设置向导（推荐）✨

最简单的入门方式：

1. `cd runtime`
2. `npm run setup`
3. 按照向导提示操作：
   - 实时验证你的 Twilio 和 OpenAI 凭据
   - 自动检测并配置 ngrok（如果可用）
   - 生成可用的 `.env` 文件
   - （可选）安装依赖库并构建项目
4. 配置 Twilio Webhook（向导会显示具体的 URL）
5. 启动服务器：`npm start`
6. 拨打你的 Twilio 号码——语音助手会接听！

**优势：**
- 实时验证凭据（在开始使用前发现潜在问题）
- 无需手动编辑 `.env` 文件
- 自动检测并配置 ngrok
- 提供详细的逐步指导和相关链接

### 选项 B：手动设置

1. `cd runtime && npm install`
2. 将 `../references/env.example` 复制到 `runtime/.env` 中并填写你的配置信息。
3. `npm run build && npm start`
4. 将 Twilio 语音 Webhook 指向 `https://<your-domain>/twilio/inbound`
5. 拨打你的 Twilio 号码——语音助手会接听！

### 选项 C：仅进行验证（适用于已有设置）

1. 将 `references/env.example` 复制到你的 `.env` 文件中并替换占位符。
2. 导出所需变量（`TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_CALLER_ID`, `OPENAI_API_KEY`, `OPENAIPROJECT_ID`, `OPENAI_WEBHOOK_SECRET`, `PUBLIC_BASE_URL`）。
3. 运行快速设置脚本：`scripts/setup_quickstart.sh`
4. 如果预检通过，执行一次来电测试和一次去电测试。
5. 确认无误后才能投入生产环境。

## 凭据权限管理（建议采取更严格的措施）

对于所有服务提供商，都应使用最小权限的凭据：

- **Twilio：** 为 Amber 创建专用子账户并定期更换认证令牌。
- **OpenAI：** 仅为当前运行环境使用专用 API 密钥；避免重复使用其他应用的密钥。
- **OpenClaw 网关令牌：** 仅在需要使用智能处理功能时设置 `OPENCLAW_GATEWAY_TOKEN`；尽量减少令牌的使用范围。
- **保密措施**：切勿在脚本、设置输出或通话记录中显示完整凭据。
- **设置向导的验证范围**：仅验证通过 HTTPS 访问的官方 Twilio/OpenAI API 端点；禁止访问其他任意端点。

这些措施可以降低数据泄露的风险。

## 安全默认设置

- 对外拨电话必须获得明确授权。
- 如果需要支付或收取费用，应立即停止操作并联系人工操作员。
- 保持问候语简短明了。
- 当 `ask_openclaw` 功能响应缓慢或无法使用时，应设置超时机制并采取备用方案。

## 工作流程

1. **确认 V1 版本的可用功能**：
   - 仅包含稳定的功能：通话流程、桥接器行为、备用方案和设置步骤。
   - 避免包含机器特定的敏感信息和私有路径。
2. **文档化架构和限制**：
   - 阅读 `references/architecture.md`。
   - 保证声明的内容符合实际情况（延迟可能存在变化；数据查询为尽力而为）。
3. **运行发布检查清单**：
   - 阅读 `references/release-checklist.md`。
   - 验证配置参数、安全防护措施和故障处理机制。
4. **测试运行环境**：
   在目标服务器上运行 `scripts/validate_voice_env.sh`。
   在发布前修复任何配置问题。
5. **发布**：
   将技能包发布到 ClawHub（示例命令：`clawhub publish <skill-folder> --slug amber-voice-assistant --name "Amber Voice Assistant" --version 1.0.0 --tags latest --changelog "Initial public release"`。
   （可选）在发布前运行本地技能验证工具/打包工具。
6. **发布更新**：
   发布新的版本号（如 `1.0.1`, `1.1.0`, `2.0.0`），并附带变更日志。
   确保 `latest` 版本始终可用。

## 常见故障排除方法

- **“缺少环境变量”** → 重新检查 `.env` 文件中的配置值，并重新运行 `scripts/validate_voice_env.sh`。
- **“通话连接成功但助手无响应”** → 检查 TTS 模型设置和提供商的认证信息。
- **“ask_openclaw 超时”** → 检查网关 URL/令牌设置，并适当延长超时时间。
- **“Webhook 无法访问”** → 检查隧道/域名和 Twilio Webhook 的连接状态。

## 公开发布的注意事项

- 绝不要发布任何敏感信息（如密钥、电话号码、Webhook URL、凭据或个人数据）。
- 为对外拨电话、支付处理和升级流程制定明确的规则。
- 如果对话质量或延迟仍在调整中，应将版本标记为测试版。

## 安装注意事项

- Amber 不会执行来自此仓库的任意安装脚本。
- 运行时安装依赖项时使用 `runtime/` 目录中的标准 Node.js 依赖库。
- CRM 功能依赖于 `better-sqlite3`（原生模块），需在用户设备上本地编译。
- 在受监管的环境中部署前，请仔细检查 `runtime/package.json` 中的依赖项。

## 相关资源

- **运行时桥接器：`runtime/`（完整源代码及说明文件）
- 架构和行为说明：`references/architecture.md`
- 发布检查清单：`references/release-checklist.md`
- 环境变量模板：`references/env.example`
- 快速设置工具：`scripts/setup_quickstart.sh`
- 环境变量验证工具：`scripts/validate_voice_env.sh`