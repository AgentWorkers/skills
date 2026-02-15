---
name: amber-voice-assistant
description: Amber Voice Assistant 是一个用于将低延迟、支持电话功能的语音子代理添加到 OpenClaw 的设置与操作技能包，该方案基于 Twilio 和 OpenAI Realtime 技术实现。该技能包包含安装指南、环境配置模板、验证脚本、安全防护机制以及针对入站/出站呼叫工作流程的故障排除指南。
metadata: {"openclaw":{"emoji":"☎️","requires":{"env":["TWILIO_ACCOUNT_SID","TWILIO_AUTH_TOKEN","TWILIO_PHONE_NUMBER","OPENAI_API_KEY"],"anyBins":["node"]},"primaryEnv":"OPENAI_API_KEY"}}
---
# Amber 语音助手

## 概述

Amber 语音助手是一个用于设置和操作的技能包，可帮助您将一个低延迟、支持电话通话的语音子代理添加到 OpenClaw 中。该技能包专注于实际部署过程，包括环境配置、验证、安全防护机制以及入站/出站呼叫工作流的故障排除。

## 选择 Amber 的理由

- 提供针对 Twilio 和 OpenAI 实时语音工作流的实用设置指南；
- 提供针对常见故障（如 Webhook 或隧道连接问题、无声通话等）的验证和故障排除方案；
- 专为实际工作流程设计，适用于预订、筛选、回电、支持等场景；
- 与 OpenClaw 连接的系统（日历、CRM 等工具）兼容；
- 提供操作员在处理审批、升级或支付时的安全防护机制。

## 个性化要求

在部署之前，用户需要自定义以下内容：
- 语音助手的名称和问候语；
- 自己的 Twilio 账号及密码；
- 自己的 OpenClaw 网关/会话端点；
- 自己的呼叫安全策略（包括审批流程、升级机制和支付处理方式）。

请勿使用其他操作员的示例配置值。

## 5 分钟快速入门

1. 将 `references/env.example` 文件复制到您的 `.env` 文件中，并替换其中的占位符。
2. 导出所需的变量（`TWILIO_ACCOUNT_SID`、`TWILIO_AUTH_TOKEN`、`TWILIO_PHONE_NUMBER`、`OPENAI_API_KEY`）。
3. 运行快速设置脚本：`scripts/setup_quickstart.sh`。
4. 如果预测试通过，执行一次入站和一次出站测试。
5. 仅在此之后才能投入生产环境使用。

## 安全默认设置

- 出站呼叫前需要明确获得操作员的批准；
- 如需支付或收取费用，应立即停止并升级给人工操作员处理；
- 保持问候语简短明了；
- 当 `ask_openclaw` 功能响应缓慢或不可用时，应设置超时机制并采取优雅的回退策略。

## 工作流程

1. **确认 V1 版本的功能范围**：
   - 仅包含稳定运行的功能，如呼叫流程、桥接逻辑、回退机制以及设置步骤；
   - 不包括与特定机器相关的敏感信息和私有路径。

2. **文档化系统架构和限制**：
   - 阅读 `references/architecture.md` 以了解系统架构；
   - 确保功能描述符合实际情况（延迟可能会有所变化，内存查找操作仅供参考）。

3. **运行发布检查清单**：
   - 阅读 `references/release-checklist.md` 以验证配置参数、安全防护机制以及故障处理流程。

4. **运行运行时验证**：
   - 在目标主机上运行 `scripts/validate_voice_env.sh` 脚本；
   - 在发布前修复任何环境配置问题。

5. **发布技能包**：
   - 使用以下命令将技能包发布到 ClawHub：
     `clawhub publish <skill-folder> --slug amber-voice-assistant --name "Amber Voice Assistant" --version 1.0.0 --tags latest --changelog "初始公开发布"`
   - 可选：在发布前运行本地验证工具。

6. **发布更新**：
   - 发布新的版本号（如 `1.0.1`、`1.1.0`、`2.0.0`）并附带变更日志；
   - 确保 `latest` 版本始终处于推荐状态。

## 常见故障排除方法

- **“缺少环境变量”**：重新检查 `.env` 文件中的配置值，并重新运行 `scripts/validate_voice_env.sh`。
- **“呼叫已连接但语音助手无响应”**：检查 TTS 模型的设置和提供商身份验证。
- **`ask_openclaw` 超时**：检查网关 URL 和令牌设置，并适当增加超时时间。
- **“Webhook 无法访问”**：验证隧道连接、域名以及 Twilio Webhook 的目标地址。

## 公开发布的注意事项

- 绝不要发布任何敏感信息（如密钥、电话号码、Webhook URL、凭据或个人数据）；
- 为出站呼叫、支付处理和升级流程制定明确的安全规则；
- 如果对话质量或延迟调整正在进行中，应将 V1 版本标记为测试版。

## 参考资源

- 系统架构和行为说明：`references/architecture.md`
- V1 版本发布检查清单：`references/release-checklist.md`
- 环境配置模板：`references/env.example`
- 快速设置脚本：`scripts/setup_quickstart.sh`
- 环境配置验证工具：`scripts/validate_voice_env.sh`