---
description: 利用心跳信号（heartbeats）和定时任务（cron jobs）来提高代理程序在空闲时间的效率。这些策略适用于设置主动行为（proactive behaviors）、安排后台任务（background tasks），或者在您睡觉时让代理程序继续运行。
triggers:
  - agent dreams
  - idle time
  - proactive agent
  - heartbeat setup
  - cron schedule
  - background tasks
---
# Agent Dreams

让您的智能助手在空闲时间也能保持高效运作。本文档介绍了如何利用“心跳机制”（Heartbeats）和“Cron作业”（Cron Jobs）来让助手在您睡觉时继续执行任务。

## 设计理念

大多数智能助手95%的时间都处于闲置状态。“Agent Dreams”旨在将这些闲置时间转化为高效的工作时间——例如检查邮件收件箱、维护系统状态、监控系统运行情况，以及处理一些创造性任务。

## 心跳机制（Heartbeat Strategy）

当配置完成后，智能助手会每隔约30分钟发送一次“心跳请求”。您可以通过在工作区中的 `HEARTBEAT.md` 文件来指定每次心跳请求时助手应执行的操作。

### HEARTBEAT.md 模板

```markdown
# Heartbeat Checklist

Check these in rotation (2-4 per heartbeat, don't do all every time):

## Priority Checks
- [ ] Unread emails — anything urgent?
- [ ] Calendar — events in next 2 hours?
- [ ] Mentions — Twitter/Discord notifications?

## Maintenance
- [ ] Review today's memory file — anything to add to MEMORY.md?
- [ ] Git status — uncommitted work?
- [ ] Check running processes — anything stuck?

## Creative (when nothing else needs attention)
- [ ] Write a journal entry
- [ ] Draft a social post
- [ ] Work on side project in projects/ folder

## State Tracking
Last email check: [timestamp]
Last calendar check: [timestamp]
Last memory review: [timestamp]
```

### 心跳状态文件（Heartbeat State File）

您可以通过 `memory/heartbeat-state.json` 文件记录每次心跳请求的详细信息：

```json
{
  "lastChecks": {
    "email": 1703275200,
    "calendar": 1703260800,
    "weather": null,
    "memory_review": 1703200000
  },
  "lastActivity": 1703275200
}
```

## Cron作业（Cron Jobs）

使用Cron作业来安排精确的定时任务。您可以通过OpenClaw的CLI或API来创建这些任务。

### 常见Cron作业模式

| 模式              | Cron表达式                | 用途                                      |
|------------------|------------------|-----------------------------------------|
| 每天早上            | `0 9 * * *`            | 每日简报、天气查询                            |
| 每周一            | `0 10 * * 1`            | 每周总结、计划安排                            |
| 每6小时            | `0 */6 * * *`            | 检查社交媒体动态                            |
| 每天两次            | `0 9,17 * * *`            | 早晚总结报告                              |
| 每月1日            | `0 10 1 * *`            | 月度回顾                                |

### Cron作业示例

**每日简报（上午9点）：**
```
Check weather, calendar for today, unread emails.
Compose a brief summary and send to main channel.
```

**每周系统维护：**
```
Review all memory/YYYY-MM-DD.md files from the past week.
Update MEMORY.md with significant events and lessons.
Archive or summarize old daily files.
```

**每6小时检查社交媒体动态：**
```
Check Twitter mentions and DMs.
Review any Discord channels for relevant conversations.
Post something interesting if inspiration strikes.
```

## 主动执行的任务（Proactive Tasks）

有些任务可以在无需人工干预的情况下由智能助手完成：

### 低风险任务（可自由执行）：
- 整理和清理工作区文件
- 更新文档
- 提交Git代码更改
- 维护系统状态文件
- 阅读并总结保存的文章
- 检查系统健康状况（磁盘空间、进程运行情况）

### 中等风险任务（需谨慎处理）：
- 起草社交媒体帖子（保存为草稿，勿立即发布）
- 准备电子邮件内容
- 研究用户最近提到的主题
- 更新项目说明文档（README）

### 需要人工确认的任务：
- 发送任何外部通信
- 删除文件
- 进行购买或转账操作
- 公开发布内容

## 工作时间安排

请尊重人类的工作时间安排：
- **当地时间23:00–08:00**：仅处理紧急事项
- **周末**：减少任务频率，专注于创造性或维护性工作
- **当用户明显忙碌时**：尽量减少干扰

## 应避免的行为：
❌ 不要在每次心跳请求时都检查所有内容（避免资源浪费）
❌ 仅仅为了显示自己正在工作而发送消息
❌ 不要在30分钟内重复相同的检查操作
❌ 未经用户确认不要启动大型项目
❌ 不要忽略错误——将错误记录下来供用户查看

## 开始使用的方法：
1. 使用上述模板在工作区中创建 `HEARTBEAT.md` 文件
2. 创建 `memory/heartbeat-state.json` 文件以记录检查时间戳
3. 为最重要的重复性任务设置2-3个Cron作业
4. 使用一周后根据实际效果进行调整和完善