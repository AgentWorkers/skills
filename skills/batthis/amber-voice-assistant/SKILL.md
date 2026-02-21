---
name: amber-voice-assistant
description: "部署适用于 OpenClaw 的语音助手：包括一个可用于生产环境的 Twilio + OpenAI Realtime SIP 桥接方案（包括运行时组件），以及相应的设置指南、环境配置模板、验证脚本、安全防护机制和故障排除流程手册。"
metadata: {"openclaw":{"emoji":"☎️","requires":{"env":["TWILIO_ACCOUNT_SID","TWILIO_AUTH_TOKEN","TWILIO_PHONE_NUMBER","OPENAI_API_KEY"],"anyBins":["node"]},"primaryEnv":"OPENAI_API_KEY"}}
---
# Amber 语音助手

## 概述

Amber 语音助手为任何基于 OpenClaw 的部署方案提供语音交互功能。它内置了一个 **适用于生产环境的 Twilio + OpenAI Realtime SIP 桥接器**（位于 `runtime/` 目录下），该桥接器支持来电筛选、拨出电话、预约功能以及实时查询 OpenClaw 数据——所有这些操作均通过自然语言对话完成。

**✨ 新功能：** 交互式设置向导（`npm run setup`）可实时验证用户凭证，并自动生成有效的 `.env` 文件，无需手动配置！

## 功能演示

![设置向导演示](demo/demo.gif)

**[▶️ 在 asciinema.org 上观看交互式演示](https://asciinema.org/a/hWk2QxmuhOS9rWXy)**（可复制文本，支持调整播放速度）

*交互式向导会实时验证用户凭证，自动检测并配置 ngrok，几分钟内即可生成完整的 `.env` 文件。*

### 包含内容

- **运行时桥接器**（`runtime/`）：一个完整的 Node.js 服务器，用于将 Twilio 电话呼叫与 OpenAI Realtime 服务连接起来，并实现 OpenClaw 的智能响应。
- **设置与验证脚本**：用于预检查、环境变量模板及快速启动流程。
- **架构文档与故障排除指南**：包含呼叫流程图及常见故障处理方案。
- **安全机制**：针对拨出电话设置审批流程、支付处理规则及用户同意机制。

## 选择 Amber 的理由

- **快速部署语音助手**：只需执行 `npm install`、配置 `.env` 文件，然后运行 `npm start` 即可。
- **全面来电处理功能**：支持问候语、信息接收以及与日历系统的集成预约功能。
- **结构化的拨出电话流程**：包括预订、咨询、跟进等操作。
- **`ask_openclaw` 工具**：在通话过程中可查询日历、联系人信息及用户偏好设置。
- **语音交互优化**：通过语音填充语确保对话自然流畅（避免沉默环节）。
- **高度可配置**：助手名称、操作员信息、组织名称、日历设置、筛选规则等均可通过环境变量进行自定义。
- **操作员安全保障**：提供审批、升级及支付处理的机制。

## 个性化要求

在部署前，用户需要完成以下个性化设置：
- 为助手设置名称和问候语。
- 提供自己的 Twilio 账号及密码。
- 配置自己的 OpenAI 项目及相关 Webhook 密钥。
- 指定自己的 OpenClaw 服务端点。
- 自定义通话安全策略（包括审批流程、升级机制及支付处理规则）。
**请勿重复使用其他操作员的示例配置值。**

## 5 分钟快速入门

### 选项 A：交互式设置向导（推荐）✨

最简单的启动方式：
1. `cd runtime`
2. `npm run setup`
3. 按照向导提示操作：
   - 实时验证 Twilio 和 OpenAI 的凭证。
   - 自动检测并配置 ngrok（如可用）。
   - 生成有效的 `.env` 文件。
   （可选）安装依赖项并构建项目。
4. 配置 Twilio Webhook（向导会提供具体 URL）。
5. 启动服务器：`npm start`
6. 拨打自己的 Twilio 号码——语音助手会接听电话！

**优势：**
- 实时验证凭证（避免错误发生）。
- 无需手动编辑 `.env` 文件。
- 自动检测并配置 ngrok。
- 提供详细的步骤指导及实用链接。

### 选项 B：手动设置

1. `cd runtime && npm install`
2. 将 `../references/env.example` 复制到 `runtime/.env` 文件中，并填写相应值。
3. `npm run build && npm start`
4. 将 Twilio 语音 Webhook 指向 `https://<your-domain>/twilio/inbound`。
5. 拨打自己的 Twilio 号码——语音助手会接听电话！

### 选项 C：仅进行验证（适用于已有环境）

1. 将 `references/env.example` 复制到自己的 `.env` 文件中，并替换占位符。
2. 导出所需变量（`TWILIO_ACCOUNT_SID`、`TWILIO_AUTH_TOKEN`、`TWILIO_PHONE_NUMBER`、`OPENAI_API_KEY`）。
3. 运行快速设置脚本：`scripts/setup_quickstart.sh`。
4. 如果预检查通过，执行一次来电和一次拨出测试。
5. 确认无误后才能投入生产环境。

## 安全默认设置

- 拨出电话前必须获得明确批准。
- 如需收取费用或押金，系统会自动停止通话并转接给人工操作员。
- 保持问候语简短明了。
- 当 `ask_openclaw` 功能响应缓慢或不可用时，系统会自动退出并采取备用方案。

## 工作流程

1. **确认 V1 版本的功能范围**：
   - 仅包含稳定运行的功能：呼叫流程、桥接器行为、备用方案及设置步骤。
   - 避免包含与特定环境相关的敏感信息。

2. **文档化架构与限制**：
   - 阅读 `references/architecture.md` 文件。
   - 确保功能描述符合实际情况（延迟可能有所不同；数据查询为尽力而为）。

3. **执行发布前检查**：
   - 阅读 `references/release-checklist.md` 文件。
   - 验证配置参数、安全机制及故障处理流程。

4. **测试运行环境**：
   - 在目标服务器上运行 `scripts/validate_voice_env.sh` 脚本。
   - 在发布前修复任何环境或配置问题。

5. **发布技能**：
   - 使用 ClawHub 发布技能：
     `clawhub publish <skill-folder> --slug amber-voice-assistant --name "Amber Voice Assistant" --version 1.0.0 --tags latest --changelog "初始公开版本"`
   **可选**：发布前可运行本地验证工具。

6. **更新发布**：
   - 发布新的版本号（如 `1.0.1`、`1.1.0`、`2.0.0`）并附上更新日志。
   - 建议持续使用最新版本（`latest`）。

## 常见故障排除

- **“缺少环境变量”**：重新检查 `.env` 文件内容并重新运行 `scripts/validate_voice_env.sh`。
- **“电话接通但助手无响应”**：检查 TTS 模型配置及提供商认证信息。
- **`ask_openclaw` 超时**：检查网关 URL 和令牌设置，并适当延长超时时间。
- **Webhook 无法访问**：检查隧道/域名及 Twilio Webhook 的连接状态。

## 公开发布的注意事项

- 绝不要公开任何敏感信息（如密钥、电话号码、Webhook URL 或个人数据）。
- 明确规定拨出电话、支付处理及升级流程的安全规则。
- 如果对话质量或延迟仍在优化中，应将 V1 版本标记为测试版。

## 相关资源

- **运行时桥接器**：`runtime/`（完整源代码及使用说明）
- 架构与功能说明：`references/architecture.md`
- 发布前检查清单：`references/release-checklist.md`
- 环境变量模板：`references/env.example`
- 快速设置脚本：`scripts/setup_quickstart.sh`
- 配置验证工具：`scripts/validate_voice_env.sh`