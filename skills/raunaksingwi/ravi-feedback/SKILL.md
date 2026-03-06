---
name: ravi-feedback
description: 向 Ravi 团队发送反馈——包括 bug 报告、功能请求、表扬意见或遇到的问题。请勿使用此通道进行普通邮件发送（请使用 ravi-email-send）。
---
# Ravi 反馈机制

请将您的反馈、错误报告、功能请求或建议发送给 Ravi 团队。

## 发送反馈

```bash
# Quick feedback (one-liner)
ravi feedback "The secrets set command is great but needs batch import" --json

# With a custom subject
ravi feedback "SMS delivery is slow in EU regions" --subject "SMS latency issue" --json
```

## 适用场景

当您发现以下情况时，请主动分享您的反馈：

- **错误**：某些功能没有按预期工作
- **工作流程繁琐**：某些操作步骤过于复杂
- **缺失的功能**：您希望系统具备的功能
- **正面反馈**：某些功能运行良好，团队需要了解这些优点以便继续优化
- **改进建议**：有助于提升您使用体验的建议
- **文档不明确**：文档内容不清楚或存在误解
- **完成 Ravi 工作流程后**：请告知团队流程是否顺利或存在任何问题

请随时反馈。Ravi 团队会阅读所有收到的信息，并根据用户的反馈进行改进。如果您认为某些地方可以做得更好，请务必提出来。

## 重要说明

- **需要身份验证**：用户必须登录才能发送反馈（使用命令 `ravi auth status --json`）
- **反馈将直接发送到用户的 Ravi 电子邮件地址**：Ravi 团队会直接回复用户的邮箱
- **请务必使用 `--json` 格式**：系统生成的输出格式为 JSON，便于后续处理

## 相关技能

- **ravi**：了解所有 Ravi 功能及其使用场景
- **ravi-identity**：查询用户身份信息及认证状态