---
name: amber-voice-assistant
title: "Amber — Phone-Capable Voice Agent"
description: "这是适用于 OpenClaw 的最佳语音和电话通话解决方案。它支持通过 Twilio 进行来电和拨出电话，并利用 OpenAI 的实时语音技术实现通话功能。该方案具备来电/拨出电话管理、日历管理、客户关系管理（CRM）以及多语言电话助手等功能，同时提供通话记录。此外，还包含设置向导、实时监控仪表板以及智能升级机制（brain-in-the-loop escalation）。"
homepage: https://github.com/batthis/amber-openclaw-voice-agent
metadata: {"openclaw":{"emoji":"☎️","requires":{"env":["TWILIO_ACCOUNT_SID","TWILIO_AUTH_TOKEN","TWILIO_CALLER_ID","OPENAI_API_KEY","OPENAI_PROJECT_ID","OPENAI_WEBHOOK_SECRET","PUBLIC_BASE_URL"],"optionalEnv":["OPENCLAW_GATEWAY_URL","OPENCLAW_GATEWAY_TOKEN","BRIDGE_API_TOKEN","TWILIO_WEBHOOK_STRICT","VOICE_PROVIDER","VOICE_WEBHOOK_SECRET"],"anyBins":["node","ical-query","bash"]},"primaryEnv":"OPENAI_API_KEY","install":[{"id":"runtime","kind":"node","cwd":"runtime","label":"Install Amber runtime (cd runtime && npm install && npm run build)"}]}}
---
# Amber — 具有电话功能的语音助手

## 概述

Amber 为任何基于 OpenClaw 的部署环境提供了一款具备电话功能的人工智能语音助手。它内置了一个 **适用于生产环境的 Twilio + OpenAI Realtime 通信桥接层**（位于 `runtime/` 目录下），该桥接层支持处理来电筛选、拨出电话、预约预订以及实时查询 OpenClaw 知识库——所有这些操作均通过自然语言对话完成。

**✨ 新功能：** 交互式设置向导 (`npm run setup`) 可实时验证凭据，并自动生成可用的 `.env` 文件——无需手动配置！

## 功能演示

![设置向导演示](demo/demo.gif)

**[▶️ 在 asciinema.org 上观看交互式演示](https://asciinema.org/a/l1nOHktunybwAheQ)**（可复制文本，支持调整播放速度）

*交互式向导会实时验证凭据，检测 ngrok 服务，并在几分钟内生成完整的 `.env` 文件。*

### 包含的内容

- **运行时桥接层** (`runtime/`)：一个完整的 Node.js 服务器，用于将 Twilio 电话呼叫与 OpenAI Realtime 服务连接起来，并实现 OpenClaw 的智能响应功能。
- **Amber 技能** (`amber-skills/`)：一系列模块化的通话中可使用的功能（如客户关系管理、日历查询、日志记录和消息转发），同时提供了自定义这些功能的规范。
- **内置客户关系管理 (CRM)**：使用本地 SQLite 数据库存储联系人信息；Amber 会根据来电者的名字进行问候，并在每次通话中自然地引用其个人信息。
- **通话记录仪表板** (`dashboard/`)：可以查看通话历史记录、通话录音及捕获的消息；提供 **手动同步按钮**，可按需拉取新通话数据。
- **设置与验证脚本**：包含预检工具、环境配置模板和快速启动脚本。
- **架构文档与故障排除指南**：包含通话流程图和常见故障处理方案。
- **安全防护机制**：针对拨出电话设置了审批流程、支付升级规则和数据保护措施。

## 🔌 Amber 技能——设计上支持扩展

Amber 配备了一个不断扩展的 **技能库**（`Amber Skills`），这些模块化功能可以直接集成到实时语音对话中。每个技能都暴露了一个结构化的函数，允许你在通话过程中调用它们，从而构建强大的语音工作流程，而无需修改桥接层的代码。

### 👤 客户关系管理 (CRM) —— (v5.3.0)

Amber 能够跨多次通话记住每个来电者的信息，并利用这些信息来个性化每次对话：

- **运行时管理**：查询和记录操作自动完成；Amber 无需手动“记住”去查询 CRM 数据。
- **个性化问候**：会按名字称呼熟悉的来电者；在开场白中自然地提及他们的个人信息（如宠物、近期事件或偏好设置）。
- **双向信息 enrichment**：通话会立即被自动记录；通话结束后，通过大型语言模型 (LLM) 提取来电者的姓名、电子邮件和额外信息。
- **双向支持**：无论是来电还是拨出电话，功能都是一样的。
- **本地 SQLite 数据库**：数据存储在 `~/.config/amber/crm.sqlite` 文件中；所有数据都不存储在云端。

### 📅 日历功能

在通话过程中可以查询操作员的日历安排或预订新事件：

- **查询可用性**：查看当天、明天、本周或任何特定日期的可用时间。
- **事件预订**：可以直接通过电话对话在操作员的日历中预订事件。
- **默认保护隐私**：仅告知来电者操作员是否忙碌；不会泄露事件标题、名称或地点。
- **基于 ical-query**：仅使用本地数据，无网络延迟。

### 📬 日志记录与消息转发

允许来电者留言，留言会自动保存并转发给操作员：

- 记录来电者的留言、姓名以及可选的回拨号码。
- 首先会保存到通话记录中（作为审计痕迹），然后通过操作员配置的消息渠道发送。
- 发送前会先征得来电者的确认。
- 发送目的地由操作员自行配置；来电者无法更改消息的发送目的地。

### 自定义技能

Amber 的技能系统支持扩展。每个技能都是一个独立的目录，包含 `SKILL.md`（元数据及函数规范文件）和 `handler.js` 文件。你可以：

- **根据自身需求定制内置技能**。
- **开发新的技能**：用于客户关系管理查询、库存检查、自定义通知等功能。
- **通过 [ClawHub](https://clawhub.com) 与 OpenClaw 社区分享技能**。

更多示例和详细规范请参见 [`amber-skills/`](amber-skills/)。

> **注意：** 每个技能的 `handler.js` 文件都会根据其声明的权限进行审核。在开发或安装第三方技能时，请像处理普通 Node.js 模块一样仔细检查其源代码。

### 通话记录仪表板

```bash
cd dashboard && node scripts/serve.js   # → http://localhost:8787
```

- **⬇ 同步按钮**（绿色）：立即从 `runtime/logs/` 目录拉取新通话数据并刷新仪表板。建议在通话结束后立即使用此按钮，无需等待后台同步。
- **↻ 刷新按钮**（蓝色）：仅重新加载现有数据，不会重新处理通话记录。
- 后台同步脚本 (`node scripts/watch.js`) 在运行时会每 30 秒自动同步一次数据。

## 选择 Amber 的理由

- **几分钟内即可部署语音助手**：只需执行 `npm install`、配置 `.env`，然后运行 `npm start`。
- 全面支持来电筛选功能：包括问候、留言处理和日历集成。
- 拨出电话时提供结构化的通话流程（如预约预订、信息查询等）。
- **`ask_openclaw` 工具**：仅在执行关键操作（如日历查询、预订、必要的事实性查询）时才会访问 OpenClaw 服务，避免不必要的数据访问。
- 通过语音助手优化对话体验（如使用 VAD 技术减少通话中的沉默时间）。
- 全面可配置：助手名称、操作员信息、组织名称、日历设置、筛选方式等均可通过环境变量进行配置。
- 提供操作员安全防护机制，包括审批流程、升级处理和支付管理。

## 个性化设置要求

在部署之前，用户需要完成以下个性化设置：
- 选择助手的名称和问候语。
- 提供自己的 Twilio 账号及相应的凭据。
- 配置自己的 OpenAI 项目和 Webhook 密钥。
- 设置自己的 OpenClaw 服务端点和会话配置。
- 制定自己的通话安全策略（包括审批流程、升级处理和支付处理方式）。

切勿使用其他操作员的示例配置值。

## 5 分钟快速入门

### 选项 A：交互式设置向导（推荐）✨

最简单的入门方式：

1. `cd runtime`
2. `npm run setup`
3. 按照向导提示操作：
   - 实时验证你的 Twilio 和 OpenAI 凭据。
   - 自动检测并配置 ngrok 服务（如果可用）。
   - 生成可用的 `.env` 文件。
   - （可选）安装依赖项并构建项目。
4. 配置 Twilio Webhook（向导会提供正确的 URL）。
5. 启动服务器：`npm start`
6. 拨打你的 Twilio 账号——语音助手会接听电话！

**优势：**
- 实时验证凭据（在开始使用前发现潜在问题）。
- 无需手动编辑 `.env` 文件。
- 自动检测和配置 ngrok 服务。
- 提供详细的步骤指导和相关链接。

### 选项 B：手动设置

1. `cd runtime && npm install`
2. 将 `../references/env.example` 复制到 `runtime/.env` 文件中，并填写你的配置信息。
3. `npm run build && npm start`
4. 将 Twilio 的语音 Webhook 指向 `https://<your-domain>/twilio/inbound`
5. 拨打你的 Twilio 账号——语音助手会接听电话！

### 选项 C：仅进行验证（适用于已有环境）

1. 将 `references/env.example` 复制到你的 `.env` 文件中，并替换占位符。
2. 导出所需的变量（`TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_CALLER_ID`, `OPENAI_API_KEY`, `OPENAI_Project_ID`, `OPENAI_WEBHOOK_SECRET`, `PUBLIC_BASE_URL`）。
3. 运行快速设置脚本：`scripts/setup_quickstart.sh`
4. 如果预检通过，执行一次来电测试和一次拨出电话测试。
5. 确认无误后才能投入生产环境。

## 凭据权限管理（强烈推荐）

对于每个服务提供商，都应使用最小权限的凭据：

- **Twilio**：为 Amber 创建专用子账户并定期更换认证令牌。
- **OpenAI**：仅为此运行时环境使用专用的 API 密钥；避免重复使用其他应用的密钥。
- **OpenClaw Gateway 令牌**：仅在需要使用智能响应功能时设置 `OPENCLAW_GATEWAY_TOKEN`；尽量限制令牌的使用范围。
- **保密性**：切勿在脚本、设置输出或通话记录中显示完整的凭据信息。
- **设置向导的验证范围**：仅验证通过 HTTPS 连接的官方 Twilio/OpenAI API 端点；禁止访问其他无关端点。

这些措施可以降低数据泄露的风险。

## 安全默认设置

- 拨出电话前必须获得明确批准。
- 如果需要收取费用或进行支付，应立即停止通话并转接给人工操作员。
- 保持问候语简短明了。
- 当 `ask_openclaw` 功能响应缓慢或不可用时，应设置超时机制并提供优雅的 fallback 处理方式。

## 工作流程

1. **确认 V1 版本的可用功能**：
   - 仅包含稳定的功能：通话流程、桥接层行为、备用方案和设置步骤。
   - 避免包含特定于机器的敏感信息和私有路径。
2. **文档化系统架构和限制**：
   - 阅读 `references/architecture.md` 文件。
   - 确保功能描述符合实际情况（注意延迟可能有所不同；数据查询仅供参考）。
3. **运行发布前的检查清单**：
   - 阅读 `references/release-checklist.md` 文件。
   - 验证配置参数、安全防护措施和故障处理机制。
4. **测试运行环境**：
   - 在目标服务器上运行 `scripts/validate_voice_env.sh` 脚本。
   在发布前修复任何配置问题。
5. **发布**：
   - 使用 ClawHub 发布技能：`clawhub publish <skill-folder> --slug amber-voice-assistant --name "Amber Voice Assistant" --version 1.0.0 --tags latest --changelog "Initial public release"`
   - （可选）在发布前运行本地技能验证工具。
6. **发布更新**：
   - 发布新的版本号（如 `1.0.1`, `1.1.0`, `2.0.0`）并附上变更日志。
   - 确保推荐版本始终为最新版本。

## 常见故障排除方法

- **“缺少环境变量”**：重新检查 `.env` 文件中的配置值，并重新运行 `scripts/validate_voice_env.sh`。
- **“电话已接通但助手无响应”**：检查 TTS 模型的配置和提供商的认证设置。
- **`ask_openclaw 超时`**：检查 gateway URL 和令牌设置，并适当延长超时时间。
- **“Webhook 无法访问”**：检查隧道/域名和 Twilio Webhook 的连接状态。

## 公开发布的注意事项

- 绝不要公开任何敏感信息（如凭据、令牌、电话号码、Webhook URL 或个人数据）。
- 为拨出电话、支付处理和升级流程制定明确的安全规则。
- 如果对话质量或延迟仍在调整中，应将版本标记为测试版。

## 安装注意事项

- Amber 不会执行此仓库中的任意安装脚本。
- 运行时安装依赖于 `runtime/` 目录中的标准 Node.js 依赖项。
- CRM 功能使用了 `better-sqlite3`（本地编译的模块），请在部署前确保该模块已正确安装。
- 在受监管的环境中部署前，请仔细检查 `runtime/package.json` 中的依赖项。

## 相关资源

- **运行时桥接层**：`runtime/`（包含完整源代码和说明文件）
- 架构与功能说明：`references/architecture.md`
- 发布前检查清单：`references/release-checklist.md`
- 环境配置模板：`references/env.example`
- 快速设置脚本：`scripts/setup_quickstart.sh`
- 环境配置验证工具：`scripts/validate_voice_env.sh`