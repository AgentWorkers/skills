---
name: socialclaw-cli
description: 通过已安装的社交 CLI（Social CLI）安全地操作 Meta API 工作流。当用户需要身份验证、查询、发布内容、管理 Instagram 或 WhatsApp 账户、运行营销 API 动作、执行操作工作流，或通过终端命令启动代理/网关流程时，请使用此功能。该技能可将自然语言请求转换为明确的社交命令，并提供风险提示及故障排除支持。
---
# SocialClaw CLI

使用此工具将用户的意图转换为适用于 Meta API 操作的安全 `social` 命令。请确保 `social` 已经预先安装，先验证其可用性，然后再根据用户意图路由到相应的业务流程。

## 核心业务流程

1. 在会话中的第一个命令执行之前，验证环境是否满足要求。
2. 将用户意图解析为具体的操作类型（即属于哪个主要业务领域）。
3. 当系统状态未知时，先执行只读操作。
4. 在执行任何写操作之前，先提出具体的命令建议。
5. 对写操作实施风险控制，并请求用户确认。
6. 仅执行必要的最小命令序列。
7. 在遇到故障时，通过有针对性的诊断和重试机制来恢复系统状态。

### 验证环境

- 在 PowerShell 中运行 `scripts/check_social_cli.ps1`。
- 在 POSIX shell 中运行 `sh scripts/check_social_cli.sh`。
- 如果 `social-cli` 未安装或版本过旧：
  - 使用 `npm install -g @vishalgojha/social-cli` 进行安装或升级。
  - 重新运行验证脚本。

## 业务领域路由

仅加载所选业务领域的参考文件以及 `references/safety-and-risk.md` 文件。

- `auth`、`query`、`post`、`instagram`：`references/workflows-core.md`
- `marketing`、`whatsapp`：`references/workflows-marketing-whatsapp.md`
- `ops`、`agent`、`gateway`、`studio`：`references/workflows-ops-agent-gateway.md`
- 命令查找及备用方案：`references/command-map.md`
- 错误处理与恢复：`references/troubleshooting.md`

## 执行策略

- 优先使用可预测的 CLI 命令，而非复杂的文本描述。
- 当用户指定了客户端或工作空间时，确保命令的执行符合相应的配置要求。
- 绝不在输出中显示完整的令牌或敏感信息。
- 在证明没有风险之前，将所有写操作视为高风险操作。
- 当配置的可靠性较低时，先运行 `social doctor` 工具进行检测。

## 风险策略

请参考 `references/safety-and-risk.md` 文件中的分类标准和确认流程。

- 只读操作可以立即执行。
- 低风险和高风险的写操作需要用户的明确确认。
- 高风险操作必须包含费用支出或数据交付的警告信息，并提供相应的回滚命令。

## 输出规范

在响应操作结果时：

1. 显示操作的简要概述。
2. 显示可执行的命令内容。
3. 说明操作所依赖的环境信息（配置文件、账户 ID、页面 ID、地区、时间范围）。
4. 如果操作不是只读操作，请求用户确认。