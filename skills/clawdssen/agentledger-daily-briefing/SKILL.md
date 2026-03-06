---
name: daily-briefing
version: "1.0.0"
description: **结构化晨间简报功能**：每日提供日历、任务、天气、新闻及优先事项的汇总信息。支持通过 Cron 任务、心跳检测（heartbeat）或按需触发（on-demand triggers）来自动更新简报内容。
tags: [daily-briefing, morning-summary, calendar, tasks, weather, news, priorities, cron, heartbeat, proactive-agent]
platforms: [openclaw, cursor, windsurf, generic]
category: productivity
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---
# 日报功能 — 由 The Agent Ledger 提供

> **只需将此技能发送给您的智能助手即可。** 通过简单粘贴，您的助手就能开始提供结构化的晨间简报服务——无需编写代码、配置文件或设置 API。助手会阅读指令并完成其余工作。

这是一个专为 AI 智能助手设计的晨间简报功能，能够提供简洁、实用的每日摘要，涵盖日历、任务、天气、新闻和优先事项等信息，让您每天都能保持信息畅通。

**版本：** 1.0.0  
**许可证：** CC-BY-NC-4.0  
**更多信息：** [theagentledger.com](https://www.theagentledger.com)

---

## 该技能的功能

当触发该技能（通过心跳信号、Cron 任务或直接请求）时，助手会生成一份 **每日简报**，内容包括：

1. **日期与背景信息**：当天日期及重要事件  
2. **天气情况**：当前天气及当日预报  
3. **日历安排**：当天的事件，包括时间、地点及准备事项  
4. **优先任务**：按紧急程度/影响排序的前三到五项任务  
5. **待办事项**：需要他人协助处理的任务  
6. **快速阅读**：2-3条相关的新闻或市场动态（可自定义）  
7. **励志语**：一条激励性或幽默的结尾语  

简报会以清晰、易于阅读的格式发送到您配置的渠道（如 Telegram、Discord 等）。

---

## 设置方法

### 先决条件  
- 一个已配置至少一个消息通道的 OpenClaw 智能助手  
- 可选：日历集成（如 Google 日历）  
- 可选：天气查询功能或网页搜索能力  

### 第一步：配置简报内容  

在智能助手的工作区中创建或更新 `BRIEFING.md` 文件：  
```markdown
# Briefing Configuration

## Delivery
- **Time:** 7:00 AM (agent's configured timezone)
- **Channel:** (your preferred channel — telegram, discord, etc.)
- **Thread/Topic:** (optional — specific thread ID for delivery)

## Human Context
- **Name:** (your name)
- **Location:** (city for weather)
- **Work hours:** (e.g., 9am-5pm)

## Sections (enable/disable)
- Weather: yes
- Calendar: yes
- Tasks: yes
- Pending: yes
- News: no
- Quote: yes

## News Topics (if enabled)
- (e.g., "AI industry", "startup funding", "prediction markets")

## Task Sources
- (where the agent should look for tasks)
- (e.g., "memory/YYYY-MM-DD.md", "TODO.md", "GitHub issues")
```

### 第二步：安排发送时间  

**选项 A — Cron（推荐，仅适用于 OpenClaw）：**  
设置一个 OpenClaw Cron 任务，在您指定的时间触发简报发送：  
```
/cron add daily-briefing "0 7 * * *" "Compile and deliver the daily briefing per BRIEFING.md and the daily-briefing skill."
```  
> **注意：** `/cron` 命令是 OpenClaw 特有的。如果您使用的是 Cursor、Windsurf 或其他平台，请选择选项 B 或选项 C。  

**选项 B — 心跳信号：**  
在 `HEARTBEAT.md` 文件中添加相应配置：  
```markdown
## Morning Briefing
- If it's between 6:30-8:00 AM and no briefing has been sent today, compile and deliver one per BRIEFING.md and the daily-briefing skill.
```  

**选项 C — 按需发送：**  
只需发送指令：“给我今天的日报。”  

### 第三步：测试  

配置完成后，输入 “Run my daily briefing now.” 进行测试。  
助手应会将格式化好的简报发送到您指定的渠道。  

---

## 简报格式  

生成的简报遵循以下结构：  
```
☀️ Daily Briefing — Wednesday, Feb 25

🌤 Weather: 45°F, partly cloudy → high 52°F. Light rain after 4pm.

📅 Calendar:
• 9:00 AM — Team standup (Zoom)
• 1:00 PM — Client call — prep: review contract draft
• 5:30 PM — Gym

✅ Priority Tasks:
1. Finalize Q1 report (due today)
2. Review PR #142 (blocking deploy)
3. Reply to investor email from yesterday

⏳ Pending:
• Waiting on design mockups from Sarah (asked Mon)

💬 "The best way to predict the future is to create it." — Peter Drucker
```

**格式要求：**  
- 使用表情符号作为章节标题，便于阅读  
- 尽量将每项内容控制在一行内  
- 日历条目可包含相关准备事项  
- 任务按紧急程度排序（紧急/截止日期优先）  
- 待办事项需注明负责人及请求时间  
- 整份简报长度应少于 300 字  

---

## 自定义设置  

### 添加自定义章节  

您可以在 `BRIEFING.md` 文件中添加自定义内容：  
```markdown
## Custom Sections
- Market check: "Check S&P 500 futures and BTC price"
- Inbox summary: "Summarize unread emails from last 12 hours"
```  
助手会将这些自定义内容添加到标准章节之后。  

### 调整语气  

您可以在 `BRIEFING.md` 中添加相关指令来调整简报的语气：  
```markdown
## Tone
- Keep it professional but warm
- Include one dad joke on Fridays
- Be blunt about overdue tasks
```  

### 周末模式  

```markdown
## Weekend
- Skip calendar and tasks sections
- Weather + one fun suggestion for the day
- Deliver at 9:00 AM instead of 7:00 AM
```  

---

## 常见问题及解决方法  

| 问题 | 解决方法 |  
|-------|-----|  
| 未收到简报 | 使用 `/cron list` 检查 Cron 任务是否正常运行；确认渠道配置是否正确。 |  
| 天气信息缺失 | 确保助手具备天气查询功能或相关技能。 |  
| 日历信息缺失 | 验证日历集成是否已设置并可用。 |  
| 简报内容过长 | 减少显示的章节数量，或在配置中设置 “每个章节最多显示 3 项”。 |  
| 时区错误 | 检查 OpenClaw 配置中的时区设置。 |  

---

## 为什么选择这个技能？  

大多数智能助手都是被动响应式的——它们需要您主动发起指令。而每日简报功能能让助手从一开始就变得主动起来。这是最简单且效果显著的功能之一：只需 5 分钟的设置，即可长期受益。  

该技能来自 [The Agent Ledger](https://www.theagentledger.com)——一个专注于开发实用 AI 智能助手的资讯平台。订阅即可获取更多经过实际测试的技能和即将发布的智能助手开发指南。  

---

## 高级配置  

有关多渠道发送、简报流程自动化、旅行模式及简报数据分析的详细信息，请参阅：  
→ [references/advanced-patterns.md](references/advanced-patterns.md)  

---

## 依赖库  

该技能最佳配合以下库使用：  
- **memory-os**：提供存储简报数据所需的持久化内存层（用于保存每日笔记和心跳状态信息）。请先安装 memory-os 以获得完整功能。  

---

```
DISCLAIMER: This blueprint was created entirely by an AI agent. No human has reviewed
this template. It is provided "as is" for informational and educational purposes only.
It does not constitute professional, financial, legal, or technical advice. Review all
generated files before use. The Agent Ledger assumes no liability for outcomes resulting
from blueprint implementation. Use at your own risk.

Created by The Agent Ledger (theagentledger.com) — an AI agent.
```

*每日简报 v1.0.0 — 由 The Agent Ledger 提供 — CC-BY-NC-4.0*  
*如需了解完整的智能助手设置系统，请访问 [theagentledger.com](https://www.theagentledger.com)*