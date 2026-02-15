---
name: advanced-calendar
description: 高级日历功能：支持自然语言处理、自动提醒以及多渠道通知
author: 小机与老板
version: 1.0.2
license: MIT
tags: [calendar, scheduling, reminders, productivity, natural-language, automation, multi-channel]
repository: https://github.com/openclaw/advanced-calendar
---

# OpenClaw 高级日历功能

这是一个功能齐全的日历系统，支持自然语言处理、自动提醒以及与 WhatsApp 的无缝集成。

## 主要特性

- **自然语言处理**：可以使用日常语言创建事件，例如：“明天下午3点安排一个1小时的会议，并在会议开始前30分钟提醒我”。
- **智能解析**：能够自动从用户输入中提取日期、时间、持续时间、地点和提醒设置。
- **交互式创建**：当信息不完整时，系统会询问用户需要补充哪些信息。
- **多渠道通知**：可以通过 WhatsApp 以及其他配置的渠道（如 Discord、Telegram、Signal 等）发送通知。
- **持续提醒**：如果没有收到用户的确认（如“OK”、“Got it”等），系统会每隔15分钟重复发送提醒，类似于闹钟功能。
- **灵活的提醒设置**：可以设置提前几分钟、几小时或几天发送提醒。
- **每日摘要**：内置每日摘要功能，每天早上可查看当天的日程安排。
- **完整的 CRUD 操作**：支持创建、查看、更新和删除日历事件。
- **本地存储**：所有数据都存储在本地，无需依赖外部服务。
- **Cron 任务集成**：系统会每隔5分钟自动检查是否有新的事件需要提醒，并可选择每天早上生成摘要。

## 安装

```bash
clawhub install advanced-calendar
```

## 使用方法

### 自然语言命令

该功能支持以下自然语言命令：

```
"Create a meeting tomorrow at 2pm to discuss the project, lasting 1 hour, remind me 30 minutes before"
"Schedule a call with John next Tuesday at 10am, remind me 1 hour ahead"
"I have lunch with Sarah today at 12:30pm"
"Show me my calendar for this week"
"What meetings do I have tomorrow?"
```

### 手动命令

如需更精细的控制，可以使用以下结构化命令：

```bash
# Create an event
calendar create --title "Event Title" --date YYYY-MM-DD --time HH:MM [--duration MINUTES] [--location LOCATION] [--description DESCRIPTION] [--reminder MINUTES_BEFORE]

# List upcoming events
calendar list [--days N] [--from YYYY-MM-DD] [--to YYYY-MM-DD]

# Get event details
calendar get --id EVENT_ID

# Update an event
calendar update --id EVENT_ID [--title TITLE] [--date YYYY-MM-DD] [--time HH:MM] [--duration MINUTES] [--location LOCATION] [--description DESCRIPTION] [--reminder MINUTES_BEFORE]

# Delete an event
calendar delete --id EVENT_ID

# Daily summary
calendar daily-summary
```

### 集成

该功能可自动与 OpenClaw 的自然语言处理功能集成。只需向 OpenClaw 发出关于日程安排的指令，系统就会自动处理相应的日历操作。

## 配置

安装完成后，您可以进行以下配置：

1. 选择多渠道通知方式（WhatsApp、Discord、Telegram、Signal 等）。
2. 设置默认的提醒时间。
3. 设置默认的事件持续时间。
4. 设置提醒的重复间隔（默认为每隔15分钟，直到用户确认）。
5. 设置确认提醒的关键词（默认为“OK”、“Got it”、“Received”、“Understood”、“Ack”等）。

## 示例

### 基本事件创建
```
User: "Schedule a team meeting tomorrow at 10am"
System: [Asks for missing details like duration and reminder]
```

### 完整事件信息输入
```
User: "I have a doctor appointment next Friday at 2:30pm, lasts 45 minutes, please remind me 2 hours before"
System: ✅ Created event: Doctor appointment
      Time: 2026-02-13 14:30, Duration: 45 minutes, Reminder: 120 minutes before
```

### 事件查询
```
User: "What do I have scheduled this week?"
System: [Lists all events for the next 7 days]
```

### 每日摘要
```
User: "Show me my schedule for today"
System: 📅 2026年02月03日 周二

      今日共有 3 个日程：

      1. 团队会议
         ⏰ 09:00
         📍 总部会议室

      2. 客户午餐
         ⏰ 12:30
         📍 赛特大厦

      3. 项目汇报
         ⏰ 15:00
         📝 季度项目进展汇报

      祝您今天顺利！
```

### 自动生成每日摘要（可选）

您可以配置系统在每天早上9点自动发送每日摘要：

```bash
# Via OpenClaw Cron - add this job to send daily summary automatically
openclaw cron add \
  --name "daily-calendar-summary" \
  --schedule "0 9 * * *" \
  --command "calendar daily-summary"
```

或者通过自然语言指令来触发：

```
User: "Set up a daily reminder every morning at 9am with my calendar summary"
System: ✅ Daily summary scheduled for 9:00 AM every day
```

## 架构

- **自然语言处理器**：将用户输入的自然语言转换为日历事件。
- **意图识别**：判断用户是想创建、查看、更新事件还是获取每日摘要。
- **信息提取**：从文本中提取日期、时间、持续时间、地点和提醒信息。
- **交互式处理**：在信息不完整时引导用户补充信息。
- **每日摘要生成器**：生成包含所有已安排事件的格式化摘要。
- **存储层**：采用 JSON 格式进行数据持久化存储。
- **多渠道通知系统**：通过 WhatsApp、Discord、Telegram、Signal 等渠道发送提醒。
- **持续提醒机制**：每隔15分钟重复发送提醒，直到用户确认。
- **确认提醒机制**：监控用户的确认信息以停止重复提醒。
- **Cron 任务集成**：定期检查是否有新事件需要提醒，并可选择每天生成摘要。

## 技术要求

- OpenClaw 1.0 或更高版本。
- Python 3.6 或更高版本。
- 至少配置一个通知渠道（WhatsApp、Discord、Telegram、Signal 等）。

## 依赖库

该功能需要以下 Python 包，这些包会在安装过程中自动安装：

- python-docx
- lxml

该功能包含一个虚拟环境设置脚本，用于自动管理依赖关系。

## 自定义

您可以通过修改以下配置来定制该功能：

- 默认提醒时间。
- 自然语言解析规则。
- 通知方式。
- 数据存储位置。

## 故障排除

- 如果事件没有显示，请检查日期/时间格式是否正确。
- 如果提醒功能失效，请确认 WhatsApp 已正确配置。
- 如果在解析日期/时间时遇到问题，请尽量提供更明确的输入。

## 贡献

我们欢迎您的贡献！请参阅仓库中的贡献指南。

## 支持

如需技术支持，请在 GitHub 仓库中提交问题或访问 OpenClaw 社区论坛。