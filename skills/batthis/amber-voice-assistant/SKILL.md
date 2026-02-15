---
name: amber-voice-assistant
description: 部署一个可用于生产环境的 OpenClaw 语音助手，该助手集成 Twilio 和 OpenAI Realtime 服务（需要 OPENAI_API_KEY）。该语音助手支持实时文本转语音（STT/TTS）功能，并能在通话过程中查询 OpenClaw 中存储的知识库。它同时支持来电（inbound_calls）和去电（outbound_calls）场景。该解决方案可用于设置来电/去电流程、以 OpenClaw 的方式查询知识或数据、实现安全防护机制（如审批流程或支付升级功能），以及快速完成语音助手的配置并将其发布到 ClawHub 平台供其他应用使用。
metadata: {"openclaw":{"emoji":"☎️","requires":{"env":["TWILIO_ACCOUNT_SID","TWILIO_AUTH_TOKEN","TWILIO_PHONE_NUMBER","OPENAI_API_KEY"],"anyBins":["node"]},"primaryEnv":"OPENAI_API_KEY"}}
---

# Amber 语音助手

## 概述

使用此技能，您可以将现有的语音通话设置转换为一个可共享、有文档记录的 OpenClaw 技能，供其他人安全地安装和运行。

## 个性化要求

在部署之前，用户必须完成以下个性化设置：
- 为助手设置名称、语音以及问候语；
- 获取自己的 Twilio 账号和密钥；
- 配置自己的 OpenClaw 网关/会话端点；
- 设置自己的通话安全策略（包括审批流程、升级机制和支付处理方式）。
**请勿使用其他服务提供商的示例配置值**。

## 5 分钟快速入门

1. 将 `references/env.example` 复制到您的 `.env` 文件中，并替换其中的占位符。
2. 导出所需的变量（`TWILIO_ACCOUNT_SID`、`TWILIO_AUTH_TOKEN`、`TWILIO_PHONE_NUMBER`、`OPENAI_API_KEY`）。
3. 运行快速设置脚本：`scripts/setup_quickstart.sh`。
4. 如果预测试通过，执行一次来电测试和一次去电测试。
5. 仅在这些测试通过后，才能投入生产环境使用。

## 安全默认设置

- 去电通话前必须获得明确批准。
- 如果请求支付或押金，应立即停止通话并升级至人工客服处理。
- 保持问候语简短明了。
- 当 `ask_openclaw` 功能响应缓慢或不可用时，启用超时机制并采用优雅的回退策略。

## 工作流程

1. **确认 V1 版本的功能范围**：
   - 仅包含稳定的功能：通话流程、中继行为、回退机制以及设置步骤。
   - 不包含与特定机器相关的敏感信息和私有路径。

2. **记录系统架构及限制**：
   - 阅读 `references/architecture.md`。
   - 确保功能描述符合实际情况（延迟可能有所不同；内存查找操作仅供参考）。

3. **运行发布检查清单**：
   - 阅读 `references/release-checklist.md`。
   - 验证配置参数、安全防护措施以及故障处理机制。

4. **运行运行时环境检查**：
   - 在目标服务器上运行 `scripts/validate_voice_env.sh` 脚本。
   - 在发布前修复任何环境配置问题。

5. **发布技能**：
   - 使用以下命令将技能发布到 ClawHub：
     `clawhub publish <skill-folder> --slug amber-voice-assistant --name "Amber Voice Assistant" --version 1.0.0 --tags latest --changelog "初始公开发布"`
   - （可选）在发布前运行本地技能验证工具。

6. **发布更新**：
   - 每次发布新的版本号（如 `1.0.1`、`1.1.0`、`2.0.0`）时，附带更新日志。
   - 确保 `latest` 版本始终处于推荐状态。

## 常见问题排查

- **“缺少环境变量”** → 重新检查 `.env` 文件中的值，并重新运行 `scripts/validate_voice_env.sh`。
- **“通话已连接但助手无响应”** → 检查 TTS 模型的配置及提供商的认证信息。
- **“ask_openclaw 超时”** → 验证网关 URL 和令牌的有效性，并适当增加超时时间。
- **“Webhook 无法访问”** → 检查隧道设置、域名以及 Twilio Webhook 的目标地址。

## 公开发布的注意事项

- **切勿公开任何敏感信息**：包括密钥、电话号码、Webhook URL、个人数据等。
- 为去电通话、支付操作和升级流程制定明确的安全规则。
- 如果对话质量或延迟调整仍在进行中，应将 V1 版本标记为测试版。

## 参考资源

- 系统架构与功能说明：`references/architecture.md`
- V1 版本发布检查清单：`references/release-checklist.md`
- 环境配置模板：`references/env.example`
- 快速设置脚本：`scripts/setup_quickstart.sh`
- 环境配置验证工具：`scripts/validate_voice_env.sh`