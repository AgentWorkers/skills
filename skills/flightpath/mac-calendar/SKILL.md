---
name: mac-calendar
description: 通过 SSH 在用户的 Mac（MacBook 或 Mac Mini）上读取和管理 Apple Calendar。适用于用户需要查看日历事件、创建新事件或以任何方式管理 Apple Calendar 的情况。
---
# Mac 日历

通过 SSH 和 AppleScript 访问 Guy 的 Mac 上的 Apple 日历。

## 脚本

`scripts/calendar.sh <action> [args...]`

### 动作

- `list-calendars` — 列出所有可用的日历
- `events [days] [calendar]` — 列出即将发生的事件（默认：7 天，所有日历）
- `today` — 列出今天的事件
- `tomorrow` — 列出明天的事件
- `this-week` — 列出本周的事件
- `add-event <calendar> <title> <start-date> [end-date> [location> [notes]` — 创建新事件
- `search <query> [days]` — 按标题/备注搜索事件（默认：±30 天）

### 日期格式

- `YYYY-MM-DD` 用于全天事件
- `YYYY-MM-DD HH:MM` 用于定时事件（24 小时格式，中部时间）

### 示例

```bash
# List all calendars
bash scripts/calendar.sh list-calendars

# Check today's events
bash scripts/calendar.sh today

# See next 14 days
bash scripts/calendar.sh events 14

# Create a new event
bash scripts/calendar.sh add-event "Work" "Team Meeting" "2026-02-18 14:00" "2026-02-18 15:00" "Conference Room A"

# Search for doctor appointments
bash scripts/calendar.sh search "doctor"
```

## 目标 Mac

使用与其他 Mac 技能相同的目标选择方式：
- 默认：Mac Mini (`guym@doclib`)
- 可通过 `MAC_TARGET=macbook` 更改为 MacBook