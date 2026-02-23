---
name: amber-voice-assistant
title: "Amber — Phone-Capable Voice Agent"
description: "这是为 OpenClaw 设计的最全面的电话功能。该功能已具备生产环境所需的各项条件，支持低延迟的人工智能通话（包括来电和去电）、多语言处理，以及实时监控界面（live dashboard）。此外，该系统还采用了“大脑在回路中”（brain-in-the-loop）的智能决策机制，以确保通话质量的优化。"
homepage: https://github.com/batthis/amber-openclaw-voice-agent
metadata: {"openclaw":{"emoji":"☎️","requires":{"env":["TWILIO_ACCOUNT_SID","TWILIO_AUTH_TOKEN","TWILIO_CALLER_ID","OPENAI_API_KEY","OPENAI_PROJECT_ID","OPENAI_WEBHOOK_SECRET","PUBLIC_BASE_URL"],"optionalEnv":["OPENCLAW_GATEWAY_URL","OPENCLAW_GATEWAY_TOKEN","BRIDGE_API_TOKEN","TWILIO_WEBHOOK_STRICT","VOICE_PROVIDER","VOICE_WEBHOOK_SECRET"],"anyBins":["node","ical-query","bash"]},"primaryEnv":"OPENAI_API_KEY"}}
---
# Amber — 具备电话功能的语音助手

## 概述

Amber 为任何基于 OpenClaw 的部署方案提供了一套具备电话功能的语音助手。它内置了一个 **适用于生产环境的 Twilio + OpenAI Realtime 通信桥梁**（`runtime/`），能够处理来电筛选、拨出电话、预约预订以及实时查询 OpenClaw 的知识库信息——所有这些操作都通过自然语言对话完成。

**✨ 新功能：** 交互式设置向导 (`npm run setup`) 可实时验证凭据，并自动生成可用的 `.env` 文件——无需手动配置！

## 功能演示

![设置向导演示](demo/demo.gif)

**[▶️ 在 asciinema.org 上观看交互式演示](https://asciinema.org/a/l1nOHktunybwAheQ)**（可复制文本，可调节播放速度）

*交互式向导会实时验证凭据，检测 ngrok 的运行状态，并在几分钟内生成完整的 `.env` 文件。*

### 包含的内容

- **运行时通信桥梁** (`runtime/`)：一个完整的 Node.js 服务器，用于将 Twilio 电话呼叫与 OpenAI Realtime 服务连接起来，并实现 OpenClaw 的智能处理。
- **Amber 技能** (`amber-skills/`)：一系列模块化的通话中可用功能（日历查询、日志记录和消息转发），同时提供了自定义功能的开发规范。
- **通话日志仪表板** (`dashboard/`)：可以浏览通话记录、通话内容以及捕获的消息；包含 **手动同步按钮**，可按需拉取新通话记录。
- **设置与验证脚本**：用于预检查的脚本、环境配置模板以及快速启动工具。
- **架构文档与故障排除指南**：包含通话流程图和常见的故障处理方案。
- **安全机制**：针对拨出电话的审批流程、支付处理规则以及用户同意相关的限制。

## 🔌 Amber 技能——设计上具备高度可扩展性

Amber 配备了一个不断扩展的 **技能库**，这些技能可以直接集成到实时语音对话中。每个技能都暴露了一个结构化的函数，允许您在通话过程中调用它们，从而构建强大的语音工作流程，而无需修改通信桥梁的代码。

### 📅 日历功能

- 在通话过程中查询操作员的日程安排或预约新事件。
  - **可用性查询**：查询当天、明天、本周或任何特定日期的可用时间。
  - **事件创建**：直接通过电话对话在操作员的日历中预约事件。
  - **默认保护用户隐私**：仅告知来电者操作员是否忙碌；事件标题、名称和地点等信息不会被泄露。
  - 基于 `ical-query` 实现，完全本地处理，无网络延迟。

### 📬 日志记录与消息转发

- 允许来电者留言，留言会自动保存并转发给操作员。
  - 捕获来电者的留言内容、姓名以及可选的回拨号码。
  - 首先会保存到通话日志中（作为审计记录），然后通过操作员配置的消息渠道发送。
  - 发送前会先获得操作员的确认。
  - 发送目的地由操作员自行配置；来电者无法更改留言的发送路径。

### 自定义技能开发

Amber 的技能系统设计为可扩展的。每个技能都是一个独立的目录，包含 `SKILL.md`（元数据及函数规范）和 `handler.js` 文件。您可以：
- **根据自身需求定制内置技能**。
- **开发新的技能**：用于 CRM 查询、库存检查、自定义通知等功能，任何可以在通话中调用的功能。
- **通过 [ClawHub](https://clawhub.com) 与 OpenClaw 社区分享技能**。

更多示例和详细规范请参见 [`amber-skills/`](amber-skills/)。

> **注意：** 每个技能的 `handler.js` 文件都会根据其声明的权限进行审核。在开发或安装第三方技能时，请像处理普通 Node.js 模块一样仔细检查其源代码。

### 通话日志仪表板

```bash
cd dashboard && node scripts/serve.js   # → http://localhost:8787
```

- **⬇ 同步按钮**（绿色）：立即从 `runtime/logs/` 中拉取新通话记录并刷新仪表板。建议在通话结束后立即使用此按钮，无需等待后台同步。
- **↻ 刷新按钮**（蓝色）：从磁盘重新加载现有数据，不会重新处理日志。
- 后台同步脚本 (`node scripts/watch.js`) 在运行时每 30 秒自动同步一次数据。

## 选择 Amber 的理由

- **几分钟内即可部署语音助手**：只需执行 `npm install`、配置 `.env`，然后运行 `npm start`。
- 全面支持来电筛选功能：包括问候语、接收留言、日历集成以及预约预订。
- 支持结构化的拨出电话流程（如预约、咨询、跟进等）。
- **`ask_openclaw` 工具**：在通话过程中可以查询 OpenClaw 服务中的日历、联系人信息及用户偏好设置。
- 通过语音助手与 OpenClaw 服务进行交互，使对话更加自然（查询过程中不会出现沉默。
- 全面可配置：助手名称、操作员信息、组织名称、日历设置、筛选方式等均可通过环境变量进行配置。
- 提供操作员安全保障机制，包括审批流程、故障处理及支付处理。

## 个性化设置要求

在部署之前，用户需要完成以下个性化设置：
- 选择助手的名称和问候语内容。
- 提供自己的 Twilio 账号及相应的凭据。
- 提供自己的 OpenAI 项目信息及 Webhook 密钥。
- 指定自己的 OpenClaw 服务端点。
- 自定义通话安全策略（包括审批流程、故障处理及支付处理方式）。

请勿使用其他操作员的示例配置值。

## 5 分钟快速入门

### 选项 A：交互式设置向导（推荐）✨

最简单的入门方式：
1. `cd runtime`
2. `npm run setup`
3. 按照向导的提示操作：
   - 实时验证您的 Twilio 和 OpenAI 凭据。
   - 自动检测并配置 ngrok（如果可用）。
   - 生成可用的 `.env` 文件。
   - （可选）安装依赖项并构建项目。
4. 配置您的 Twilio Webhook（向导会提供具体的 URL）。
5. 启动服务器：`npm start`
6. 拨打您的 Twilio 账号——语音助手会立即响应！

**优势：**
- 实时验证凭据（避免在开始使用前出现错误）。
- 无需手动编辑 `.env` 文件。
- 自动检测并配置 ngrok。
- 提供详细的步骤指导及实用链接。

### 选项 B：手动设置

1. `cd runtime && npm install`
2. 将 `../references/env.example` 复制到 `runtime/.env` 中，并填写相应的值。
3. `npm run build && npm start`
4. 将您的 Twilio Webhook 配置为 `https://<your-domain>/twilio/inbound`
5. 拨打您的 Twilio 账号——语音助手会立即响应！

### 选项 C：仅进行验证（适用于已有设置的情况）

1. 将 `references/env.example` 复制到您的 `.env` 文件中，并替换其中的占位符。
2. 导出所需的变量（`TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_CALLER_ID`, `OPENAI_API_KEY`, `OPENAI_Project_ID`, `OPENAI_WEBHOOK_SECRET`, `PUBLIC_BASE_URL`）。
3. 运行快速设置脚本：`scripts/setup_quickstart.sh`
4. 如果预检查通过，执行一个来电测试和一个拨出电话测试。
5. 确认无误后才能投入生产环境使用。

## 安全默认设置

- 拨出电话前必须获得明确批准。
- 如果需要支付或收取费用，系统会自动停止通话并转接给人工操作员。
- 保持问候语简短明了。
- 当 `ask_openclaw` 功能响应缓慢或不可用时，系统会自动采取超时处理措施并切换到备用方案。

## 工作流程

1. **确认 V1 版本的功能范围**：
   - 仅包含稳定的功能：通话流程、通信桥梁的运行方式、备用方案以及设置步骤。
   - 不包括与特定系统相关的敏感信息和私有路径。
2. **文档化系统架构及限制**：
   - 阅读 `references/architecture.md`。
   - 确保功能描述符合实际情况（延迟可能有所不同；内存查询操作仅供参考）。
3. **执行发布前的检查**：
   - 阅读 `references/release-checklist.md`。
   - 验证配置参数、安全机制及故障处理方案。
4. **测试系统运行环境**：
   - 在目标服务器上运行 `scripts/validate_voice_env.sh`。
   - 在发布前修复任何环境配置问题。
5. **发布**：
   - 将代码发布到 ClawHub（示例命令：`clawhub publish <skill-folder> --slug amber-voice-assistant --name "Amber Voice Assistant" --version 1.0.0 --tags latest --changelog "Initial public release"`。
   - （可选）在发布前运行本地技能验证工具。
6. **更新发布**：
   - 发布新的版本号（如 `1.0.1`, `1.1.0`, `2.0.0`），并附上变更日志。
   - 确保 `latest` 版本始终保持可用状态。

## 常见故障排除方法

- **“缺少环境变量”**：重新检查 `.env` 文件中的值，并重新运行 `scripts/validate_voice_env.sh`。
- **“通话连接成功但助手无响应”**：检查 TTS 模型的配置及提供者的身份验证设置。
- **`ask_openclaw` 超时**：检查网关 URL 和令牌设置，并适当延长超时时间。
- **“Webhook 无法访问”**：检查隧道/域名及 Twilio Webhook 的连接情况。

## 公开发布的注意事项

- 绝不要发布包含敏感信息（如密钥、电话号码、Webhook URL、凭据或个人数据）。
- 为拨出电话、支付处理及故障处理制定明确的安全规则。
- 如果对话质量或延迟仍在调整中，应将 V1 版本标记为测试版本。

## 相关资源

- **运行时通信桥梁**：`runtime/`（完整源代码及使用说明）
- 架构与功能说明：`references/architecture.md`
- 发布前检查清单：`references/release-checklist.md`
- 环境配置模板：`references/env.example`
- 快速设置工具：`scripts/setup_quickstart.sh`
- 环境配置验证工具：`scripts/validate_voice_env.sh`