---
name: amber-voice-assistant
title: "Amber — Phone-Capable Voice Agent"
description: "OpenClaw 最全面的电话通话功能：具备生产环境所需的各项能力，支持低延迟的 AI 通话（包括来电和去电）、多语言处理、实时监控界面（live dashboard），以及智能辅助决策系统（brain-in-the-loop）。"
homepage: https://github.com/batthis/amber-openclaw-voice-agent
metadata: {"openclaw":{"emoji":"☎️","requires":{"env":["TWILIO_ACCOUNT_SID","TWILIO_AUTH_TOKEN","TWILIO_CALLER_ID","OPENAI_API_KEY","OPENAI_PROJECT_ID","OPENAI_WEBHOOK_SECRET","PUBLIC_BASE_URL"],"optionalEnv":["OPENCLAW_GATEWAY_URL","OPENCLAW_GATEWAY_TOKEN","BRIDGE_API_TOKEN","TWILIO_WEBHOOK_STRICT","VOICE_PROVIDER","VOICE_WEBHOOK_SECRET"],"anyBins":["node","ical-query"]},"primaryEnv":"OPENAI_API_KEY"}}
---
# Amber — 具备电话功能的语音助手

## 概述

Amber 为任何基于 OpenClaw 的系统添加了电话功能，使其能够通过自然语言对话提供语音服务。它内置了一个 **适用于生产环境的 Twilio + OpenAI Realtime SIP 桥接器**（`runtime/`），支持处理来电筛选、拨出电话、预约预订以及实时查询 OpenClaw 中的信息。

**✨ 新功能：** 交互式设置向导（`npm run setup`）可实时验证凭据并生成有效的 `.env` 文件，无需手动配置！

## 功能演示

![设置向导演示](demo/demo.gif)

**[▶️ 在 asciinema.org 上观看交互式演示](https://asciinema.org/a/l1nOHktunybwAheQ)**（可复制文本，可调节播放速度）

*交互式向导会实时验证凭据，自动检测 ngrok 并在几分钟内生成完整的 `.env` 文件。*

### 包含的内容

- **运行时桥接器**（`runtime/`）：一个完整的 Node.js 服务器，用于将 Twilio 电话呼叫与 OpenAI Realtime 服务连接起来。
- **通话记录仪表板**（`dashboard/`）：可以查看通话历史记录、通话内容及捕获的信息；提供 **手动同步按钮**，可按需拉取新通话数据。
- **设置与验证脚本**：包含预检功能、环境变量模板及快速启动工具。
- **架构文档与故障排除指南**：包含通话流程图及常见故障处理方案。
- **安全机制**：针对拨出电话设置审批流程、支付处理规则及用户同意权限。

### 通话记录仪表板

```bash
cd dashboard && node scripts/serve.js   # → http://localhost:8787
```

- **⬇ 同步按钮**（绿色）：立即从 `runtime/logs/` 中拉取新通话数据并刷新仪表板。建议在通话结束后立即使用该按钮，无需等待后台同步。
- **↻ 刷新按钮**（蓝色）：仅重新加载现有数据，不会重新处理通话记录。
- 后台同步脚本（`node scripts/watch.js`）在运行时每 30 秒自动同步一次数据。

## 选择 Amber 的理由

- **几分钟内即可部署语音助手**：只需执行 `npm install`、配置 `.env`，然后运行 `npm start` 即可。
- **全面的来电处理功能**：包括问候语、信息记录及日历集成。
- **结构化的拨出电话流程**：支持预约、咨询、回访等操作。
- **`ask_openclaw` 工具**：在通话过程中可查询日历、联系人信息及用户偏好设置。
- **语音交互优化**：通过 VAD（Voice Activity Detection）技术提升对话自然度，避免沉默片刻。
- **高度可配置**：助手名称、操作员信息、组织名称、日历设置等均可通过环境变量进行调整。
- **操作员安全保障**：提供审批、升级及支付处理机制。

## 个性化要求

在部署前，用户需要完成以下个性化设置：
- 为助手设置名称和问候语。
- 提供自己的 Twilio 账号及密钥。
- 配置自己的 OpenAI 项目及 Webhook 密钥。
- 设置自己的 OpenClaw 通道及会话端点。
- 定义自己的通话安全策略（包括审批流程、升级机制及支付处理规则）。

切勿重复使用其他操作员的示例配置。

## 5 分钟快速入门

### 选项 A：交互式设置向导（推荐）✨

最简单的使用方法：
1. `cd runtime`
2. `npm run setup`
3. 按照向导提示操作：
   - 实时验证 Twilio 和 OpenAI 的凭据。
   - 自动检测并配置 ngrok（如可用）。
   - 生成有效的 `.env` 文件。
   - （可选）安装依赖项并构建项目。
4. 配置 Twilio Webhook（向导会提供正确的 URL）。
5. 启动服务器：`npm start`
6. 拨打自己的 Twilio 账号——语音助手会接听电话！

**优势：**
- 实时验证凭据，避免错误。
- 无需手动编辑 `.env` 文件。
- 自动检测并配置 ngrok。
- 提供详细的步骤指导及实用链接。

### 选项 B：手动设置

1. `cd runtime && npm install`
2. 将 `../references/env.example` 复制到 `runtime/.env` 中并填写相关信息。
3. `npm run build && npm start`
4. 将 Twilio 语音 Webhook 指向 `https://<your-domain>/twilio/inbound`
5. 拨打自己的 Twilio 账号——语音助手会接听电话！

### 选项 C：仅进行验证（适用于已有环境）

1. 将 `references/env.example` 复制到自己的 `.env` 文件中并替换占位符。
2. 导出所需变量（`TWILIO_ACCOUNT_SID`、`TWILIO_AUTH_TOKEN`、`TWILIO_CALLER_ID`、`OPENAI_API_KEY`、`OPENAI_Project_ID`、`OPENAI_WEBHOOK_SECRET`、`PUBLIC_BASE_URL`）。
3. 运行快速设置脚本：`scripts/setup_quickstart.sh`
4. 如果预检通过，执行一次来电和一次拨出电话的测试。
5. 确认无误后才能投入生产环境。

## 安全默认设置

- 拨出电话前必须获得明确批准。
- 如需支付或收取费用，系统会自动停止通话并转接给人工操作员。
- 保持问候语简短明了。
- 当 `ask_openclaw` 功能响应缓慢或不可用时，系统会自动退出并采取备用方案。

## 工作流程

1. **确认 V1 版本的功能范围**：
   - 仅包含稳定运行的功能：通话流程、桥接器行为、备用方案及设置步骤。
   - 不包含特定于系统的敏感信息和私有路径。
2. **文档化系统架构与限制**：
   - 阅读 `references/architecture.md`。
   - 确保功能描述符合实际性能（注意延迟可能有所不同，部分操作可能基于最佳尝试进行）。
3. **执行发布前的检查**：
   - 阅读 `references/release-checklist.md`。
   - 验证环境变量配置及安全机制。
4. **测试系统运行环境**：
   - 在目标服务器上运行 `scripts/validate_voice_env.sh`。
   - 发布前修复任何环境或配置问题。
5. **发布技能**：
   - 使用 ClawHub 发布技能：  
     `clawhub publish <skill-folder> --slug amber-voice-assistant --name "Amber Voice Assistant" --version 1.0.0 --tags latest --changelog "Initial public release"`
   - （可选）发布前运行本地验证工具。
6. **更新发布**：
   - 发布新的版本号（如 `1.0.1`、`1.1.0`、`2.0.0`）并附上更新日志。
   - 始终保留最新版本的技能。

## 常见故障排除

- **“缺少环境变量”**：重新检查 `.env` 文件内容并重新运行 `scripts/validate_voice_env.sh`。
- **“电话连接成功但助手无响应”**：检查 TTS 模型配置及提供商认证。
- **`ask_openclaw` 超时**：检查通道 URL/令牌设置并适当延长超时时间。
- **Webhook 无法访问**：检查隧道/域名及 Twilio Webhook 的连接状态。

## 公开发布的注意事项

- 绝不要公开敏感信息（如密钥、电话号码、Webhook URL、个人数据）。
- 明确规定拨出电话、支付及升级处理的规则。
- 如果对话质量或延迟仍在调整中，应将 V1 版本标记为测试版。

## 相关资源

- **运行时桥接器**：`runtime/`（完整源代码及使用说明）
- 架构与功能说明：`references/architecture.md`
- 发布检查清单：`references/release-checklist.md`
- 环境变量模板：`references/env.example`
- 快速设置工具：`scripts/setup_quickstart.sh`
- 环境配置验证工具：`scripts/validate_voice_env.sh`