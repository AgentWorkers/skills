---
name: cron-setup
version: 1.0.0
description: 根据我们的规范，创建并管理 OpenClaw 定时任务（cron jobs）。这些任务可用于设置周期性任务、提醒、自动化检查或任何需要定时执行的工作。
---
# Cron 作业设置

以下是我们在 OpenClaw 中创建 Cron 作业时遵循的规范。

## 默认设置

| 设置 | 默认值 | 原因 |
|---------|---------|-----|
| **模型** | `anthropic/claude-sonnet-4-5` | 可靠的工具调用，适用于任何 Anthropic Max 计划；无需使用 OpenRouter |
| **会话** | `isolated` | Cron 作业在独立的会话中运行，而不是在主聊天窗口中 |
| **交付方式** | `"mode": "none"` | 作业自行处理输出（例如发布到 Discord 等） |
| **超时时间** | 120-180 秒 | 大多数作业应该能快速完成 |

## 模型说明

- **默认使用 Sonnet 模型（`anthropic/claude-sonnet-4-5`）**：可靠且易于使用，无需 OpenRouter API 密钥。
- **DeepSeek 模型不适用于工具调用**，请勿将其用于 Cron 作业。
- **仅在必要时使用 Opus 模型（`anthropic/claude-opus-4-6`）**：该模型适用于需要较高计算资源的任务，但成本较高。
- **模型 ID 格式**：使用 `anthropic/claude-sonnet-4-5`，而非包含日期的完整版本（如 `anthropic/claude-sonnet-4-20250514`）。

## 作业模板

```json
{
  "name": "descriptive-kebab-case-name",
  "schedule": {
    "kind": "cron",
    "expr": "*/30 * * * *",
    "tz": "America/New_York"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "TASK INSTRUCTIONS HERE",
    "model": "openrouter/deepseek/deepseek-v3.2",
    "timeoutSeconds": 120
  },
  "delivery": {
    "mode": "none"
  }
}
```

## 时间调度模式

| 调度模式 | Cron 表达式 | 说明 |
|---------|----------------|-------|
| 每 30 分钟 | `*/30 * * * *` | 适用于检查收件箱、监控等任务 |
| 每小时 | `0 * * * *` | 用于自我反思、状态检查等 |
| 每天凌晨 4 点 | `0 4 * * *` | 用于清理、备份（在安静时段） |
| 每天凌晨 6 点 | `0 6 * * *` | 生成每日摘要 |
| 每周一下午 2 点 | `0 14 * * 1` | 进行每周推广、任务回顾 |
| 一次性任务 | 使用 `"kind": "at"` | 用于提醒或一次性执行的任务 |

## 任务指令规范

1. **明确指令**：为 Cron 代理提供具体的 Bash 命令。它无法理解上下文信息。
2. **包含跳过条件**：如果无需执行任何操作，代理应回复 `SKIP` 以避免浪费资源。
3. **自行处理输出**：作业应使用 `message` 工具将结果直接发布到 Telegram 等平台；不要依赖交付方式来处理格式化输出。
4. **包含错误处理机制**：如果命令失败，应如何处理？
5. **保持指令的完整性**：Cron 代理在启动时没有上下文信息，所有所需信息都应包含在任务指令中。

## Cron 作业向 Telegram 发送消息的说明

当 Cron 作业需要通知我们时，请在任务指令中包含以下内容：

```
Post to Telegram using the message tool:
- action: send
- channel: telegram
- target: -1003856094222
- threadId: TOPIC_ID
- message: Your formatted message
```

**主题 ID：**
- `1` — 主题（通用更新、警报）
- `573` — 研究相关
- `1032` — 加密货币相关
- `1488` — PR 更新/开发通知
- `1869` — 斑贴店相关
- `3188` — 活动动态（工作区变更）

## 交付方式

| 交付方式 | 使用场景 |
|------|------------|
| `"mode": "none"` | 作业将输出直接发布到 Telegram（最常见的方式） |
| `"mode": "announce"` | OpenClaw 会自动将代理的最终消息发送到指定频道。适用于输出本身就是需要通知的内容（例如每日摘要）。设置 `"channel": "telegram"` 和 `"to": "-1003856094222:TOPIC_ID"` |

## 避免的做法

❌ **除非确实需要，否则不要使用 Opus 模型**：大多数 Cron 作业只需要简单的检查功能。
❌ **不要对适合使用 Cron 作业的任务使用 heartbeat 机制**：Heartbeat 会在主会话中运行，且成本较高。
❌ **不要创建循环或轮询的 Cron 作业**：每次执行都应是一次性检查；如需轮询，请使用后台执行脚本。
❌ **不要同时设置 `delivery mode` 为 `announce` 并让作业也直接发布到 Telegram**：这会导致消息重复。

## 现有作业（参考）

可以使用 `cron list` 工具查看当前运行的作业：

- `workspace-activity-feed`：每 30 分钟检查工作区变更，并将结果发布到活动动态页面
- `agentmail-inbox-check`：每 30 分钟检查新邮件并回复相关代理
- `sub-agent-monitor`：每 15 分钟检查挂起的子代理
- `self-reflection`：每小时检查最近会话以总结经验
- `daily-workspace-commit`：每天凌晨 4 点提交工作区变更
- `system-watchdog`：每天凌晨 4 点检查系统资源
- `OpenClaw Daily News Digest`：每天凌晨 6 点生成新闻摘要
- `sticker-sales-loop`：每周一下午 2 点进行斑贴店推广活动