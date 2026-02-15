---
name: calctl
description: 通过 icalBuddy 和 AppleScript CLI 管理 Apple 日历事件
---

# calctl - Apple 日历命令行工具

使用 icalBuddy（用于快速读取日历数据）和 AppleScript（用于写入日历数据）从命令行管理 Apple 日历。

**安装要求：** `brew install ical-buddy`

## 命令

| 命令 | 描述 |
|---------|-------------|
| `calctl calendars` | 列出所有日历 |
| `calctl show [过滤条件]` | 显示事件（今日、明日、本周、YYYY-MM-DD） |
| `calctl add <标题>` | 创建新事件 |
| `calctl search <查询条件>` | 按标题搜索事件（最近 30 天内） |

## 示例

```bash
# List calendars
calctl calendars

# Show today's events
calctl show today

# Show this week's events
calctl show week

# Show events from specific calendar
calctl show week --calendar Work

# Show events on specific date
calctl show 2026-01-25

# Add an event
calctl add "Meeting with John" --date 2026-01-22 --time 14:00

# Add event to specific calendar
calctl add "Team Standup" --calendar Work --date 2026-01-22 --time 09:00 --end 09:30

# Add all-day event
calctl add "Holiday" --date 2026-01-25 --all-day

# Add event with notes
calctl add "Project Review" --date 2026-01-22 --time 15:00 --notes "Bring quarterly report"

# Search for events
calctl search "meeting"
```

## `add` 命令的选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `-c, --calendar <日历名称>` | 要向其中添加事件的日历 | Privat |
| `-d, --date <YYYY-MM-DD>` | 事件日期 | 今日 |
| `-t, --time <HH:MM>` | 开始时间 | 09:00 |
| `-e, --end <HH:MM>` | 结束时间 | 开始时间后 1 小时 |
| `-n, --notes <文本>` | 事件备注 | 无 |
| `--all-day` | 创建全天事件 | false |

## 可用的日历

本系统中常见的日历包括：
- Privat（个人日历）
- Work（工作日历）
- Familien Kalender
- rainbat solutions GmbH
- TimeTrack