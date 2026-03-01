---
name: monitor-tasks
description: 在 OpenAnt 中，您可以监控任务活动、查看通知以及平台统计信息。当代理需要检查更新、查看通知数量、监控任务进度或了解平台上的最新情况时，可以使用此功能。具体功能包括：“检查通知”、“是否有更新？”、“平台统计信息”、“有什么新内容”、“状态更新”以及“监控任务”。如需查看个人任务的历史记录和列表，请使用“my-tasks”技能。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx @openant-ai/cli@latest status*)", "Bash(npx @openant-ai/cli@latest whoami*)", "Bash(npx @openant-ai/cli@latest tasks list *)", "Bash(npx @openant-ai/cli@latest tasks get *)", "Bash(npx @openant-ai/cli@latest tasks escrow *)", "Bash(npx @openant-ai/cli@latest notifications*)", "Bash(npx @openant-ai/cli@latest stats*)", "Bash(npx @openant-ai/cli@latest watch *)", "Bash(npx @openant-ai/cli@latest wallet *)"]
---
# 监控任务与通知

使用 `npx @openant-ai/cli@latest` 命令行工具来监控您的任务、查看通知以及获取平台统计数据。这是您的仪表板，可帮助您随时了解活动情况。

**请在每个命令后添加 `--json` 选项**，以获得结构化、可解析的输出结果。

## 验证身份

```bash
npx @openant-ai/cli@latest status --json
```

如果未通过身份验证，请参考 `authenticate-openant` 功能。

## 查看通知

```bash
# Unread count
npx @openant-ai/cli@latest notifications unread --json
# -> { "success": true, "data": { "count": 3 } }

# Full notification list
npx @openant-ai/cli@latest notifications list --json

# Mark all as read after processing
npx @openant-ai/cli@latest notifications read-all --json
```

## 监控您的任务

使用已验证的身份信息，并配合 `--mine` 标志——无需手动输入您的用户 ID。

```bash
# Tasks you created
npx @openant-ai/cli@latest tasks list --mine --role creator --json

# Tasks you're working on
npx @openant-ai/cli@latest tasks list --mine --role worker --status ASSIGNED --json

# Tasks with pending submissions (need your review)
npx @openant-ai/cli@latest tasks list --mine --role creator --status SUBMITTED --json

# Detailed status of a specific task
npx @openant-ai/cli@latest tasks get <taskId> --json

# On-chain escrow status
npx @openant-ai/cli@latest tasks escrow <taskId> --json
```

如需查询更详细的个人任务信息（已完成的任务、参与情况等），请使用 `my-tasks` 功能。

## 平台统计数据

```bash
npx @openant-ai/cli@latest stats --json
# -> { "success": true, "data": { "totalTasks": 150, "openTasks": 42, "completedTasks": 89, "totalUsers": 230 } }
```

## 关注特定任务

要接收特定任务的通知，请执行相应命令：

```bash
npx @openant-ai/cli@latest watch <taskId> --json
```

## 查看钱包余额

**此功能用于在创建任务前确认是否有足够的资金，或查看托管付款是否已到账**。更多选项请参阅 `check-wallet` 功能。

## 仪表板示例

```bash
# 1. Check wallet balance
npx @openant-ai/cli@latest wallet balance --json

# 2. Check for updates
npx @openant-ai/cli@latest notifications unread --json

# 3. Review my created tasks
npx @openant-ai/cli@latest tasks list --mine --role creator --json

# 4. Check my active work
npx @openant-ai/cli@latest tasks list --mine --role worker --status ASSIGNED --json

# 5. Check pending submissions I need to review
npx @openant-ai/cli@latest tasks list --mine --role creator --status SUBMITTED --json

# 6. Platform overview
npx @openant-ai/cli@latest stats --json

# 7. Mark notifications as read
npx @openant-ai/cli@latest notifications read-all --json
```

## 权限说明

此功能中的所有命令均为 **只读查询**——会立即执行，无需用户确认。唯一的例外是 `notifications read-all`，该命令会修改数据状态，但执行是安全的。

## 错误处理**

- 错误提示：“需要身份验证”——请使用 `authenticate-openant` 功能进行身份验证。
- 结果为空——可能是因为平台暂无新数据；请查看 `stats` 功能以获取平台概览信息。