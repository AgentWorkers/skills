---
name: accli
description: 此技能适用于在 macOS 上与 Apple Calendar 进行交互时使用。它可以用于列出日历、查看事件、创建/更新/删除日历事件，以及查询可用时间或忙碌状态。该技能会在用户发起如下请求时触发：查看我的日历、安排会议、查询我的日程安排、询问我明天是否有空，或其他与日历相关的操作。
---

# Apple Calendar CLI (accli)

## 安装

```bash
npm install -g @joargp/accli
```

**系统要求：** 仅支持 macOS（使用 JavaScript 进行自动化操作）

## 概述

accli 工具提供了通过命令行访问 macOS 的 Apple Calendar 的方式。它支持列出日历、查询事件、创建/更新/删除事件，以及检查多个日历中的可用时间。

## 快速参考

### 日期时间格式
- 有时间限制的事件：YYYY-MM-DDTHH:mm 或 YYYY-MM-DDTHH:mm:ss
- 全天事件：YYYY-MM-DD

### 全局选项
- --json  - 以 JSON 格式输出（推荐用于数据解析）
- --help  - 显示任意命令的帮助信息

## 命令

### 列出日历

```
accli calendars [--json]
```

列出所有可用的日历及其名称和唯一标识符（ID）。请先运行此命令以获取可用的日历及其 ID。

### 列出事件

```
accli events <calendarName> [options]
```

选项：
- --calendar-id <id>  - 日历的唯一标识符（推荐使用，而非日历名称）
- --from <datetime>  - 时间范围的开始时间（默认：当前时间）
- --to <datetime>  - 时间范围的结束时间（默认：当前时间后 7 天）
- --max <n>  - 返回的最大事件数量（默认：50 个）
- --query <q>  - 根据事件摘要/地点/描述进行不区分大小写的过滤
- --json  - 以 JSON 格式输出

示例：

```bash
# Events from Work calendar for this week
accli events Work --json

# Events in January
accli events Work --from 2025-01-01 --to 2025-01-31 --json

# Search for specific events
accli events Work --query "standup" --max 10 --json
```

### 获取单个事件

```
accli event <calendarName> <eventId> [--json]
```

根据事件 ID 获取其详细信息。

### 创建事件

```
accli create <calendarName> --summary <s> --start <datetime> --end <datetime> [options]
```

必选选项：
- --summary <s>  - 事件标题
- --start <datetime>  - 事件开始时间
- --end <datetime>  - 事件结束时间

可选选项：
- --location <l>  - 事件地点
- --description <d>  - 事件描述
- --all-day  - 创建全天事件
- --json  - 以 JSON 格式输出

示例：

```bash
# Create a timed meeting
accli create Work --summary "Team Standup" --start 2025-01-15T09:00 --end 2025-01-15T09:30 --json

# Create an all-day event
accli create Personal --summary "Vacation" --start 2025-07-01 --end 2025-07-05 --all-day --json

# Create with location and description
accli create Work --summary "Client Meeting" --start 2025-01-15T14:00 --end 2025-01-15T15:00 \
  --location "Conference Room A" --description "Q1 planning discussion" --json
```

### 更新事件

```
accli update <calendarName> <eventId> [options]
```

选项（均为可选选项，仅输入需要修改的内容）：
- --summary <s>  - 新事件标题
- --start <datetime>  - 新事件开始时间
- --end <datetime>  - 新事件结束时间
- --location <l>  - 新事件地点
- --description <d>  - 新事件描述
- --all-day  - 将事件转换为全天事件
- --no-all-day  - 将事件转换为有时间限制的事件
- --json  - 以 JSON 格式输出

示例：

```bash
accli update Work event-id-123 --summary "Updated Meeting Title" --start 2025-01-15T15:00 --end 2025-01-15T16:00 --json
```

### 删除事件

```
accli delete <calendarName> <eventId> [--json]
```

永久删除事件。执行前请用户确认。

### 检查可用时间

```
accli freebusy --calendar <name> --from <datetime> --to <datetime> [options]
```

选项：
- --calendar <name>  - 日历名称（可重复输入，用于多个日历）
- --calendar-id <id>  - 日历的唯一标识符（可重复输入）
- --from <datetime>  - 时间范围的开始时间（必选）
- --to <datetime>  - 时间范围的结束时间（必选）
- --json  - 以 JSON 格式输出

显示可用时间槽，排除已取消、被拒绝或处于“透明”状态的事件。

示例：

```bash
# Check availability across calendars
accli freebusy --calendar Work --calendar Personal --from 2025-01-15 --to 2025-01-16 --json

# Check specific hours
accli freebusy --calendar Work --from 2025-01-15T09:00 --to 2025-01-15T18:00 --json
```

### 配置

```bash
# Set default calendar (interactive)
accli config set-default

# Set default by name
accli config set-default --calendar Work

# Show current config
accli config show

# Clear default
accli config clear
```

如果未指定日历，accli 会自动使用默认日历。

## 工作流程指南

### 创建事件前
1. 列出所有日历，获取可用的日历名称和 ID。
2. 检查可用时间以选择合适的时间段。
3. 创建事件前请用户确认详细信息。

### 最佳实践
- 程序化解析数据时始终使用 --json 选项。
- 为确保准确性，建议使用 --calendar-id 而非日历名称。
- 查询事件时使用合理的日期范围。
- 删除事件前请用户确认。
- 一致使用 ISO 8601 日期时间格式。

### 常见用法

- 查找空闲时间并安排事件：
  ```bash
# 1. Check availability
accli freebusy --calendar Work --from 2025-01-15T09:00 --to 2025-01-15T18:00 --json

# 2. Create event in available slot
accli create Work --summary "Meeting" --start 2025-01-15T14:00 --end 2025-01-15T15:00 --json
```

- 查看今日日程：
  ```bash
accli events Work --from $(date +%Y-%m-%d) --to $(date -v+1d +%Y-%m-%d) --json
```