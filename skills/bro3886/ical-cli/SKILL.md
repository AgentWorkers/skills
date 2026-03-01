---
name: cal-cli
description: 使用 ical CLI 从终端管理 macOS 日历事件和日历。支持对事件和日历进行完整的创建（Create）、读取（Read）、更新（Update）和删除（Delete）操作（CRUD）。支持自然语言日期格式、重复规则、提醒功能、交互式界面，以及导入/导出（JSON/CSV/ICS）功能，并提供多种输出格式。适用于需要通过命令行与 Apple 日历进行交互、自动化日历工作流程或编写相关脚本的场景。
metadata:
  author: sidv
  version: "1.0"
compatibility: Requires macOS with Calendar.app. Requires Xcode Command Line Tools for building from source.
---
# ical — macOS 日历的命令行工具（CLI）

这是一个用 Go 语言编写的命令行工具，用于操作 macOS 的日历系统。它通过 cgo 和 EventKit 框架实现毫秒级的高速数据读取，程序运行时无需依赖任何外部库。

## 安装

```bash
go install github.com/BRO3886/ical/cmd/ical@latest
```

或者通过源代码编译安装：

```bash
git clone <repo-url> && cd ical
make build    # produces bin/ical
```

## 快速入门

```bash
# List all calendars (shows sources, colors, types)
ical calendars

# Create a new calendar
ical calendars create "Projects" --source iCloud --color "#FF6961"

# Show today's agenda
ical today

# List events this week
ical list --from today --to "end of week"

# Add an event with natural language dates
ical add "Team standup" --start "tomorrow at 9am" --end "tomorrow at 9:30am" --calendar Work --alert 15m

# Show event details (row number from last listing)
ical show 2

# Delete an event (--force skips confirmation prompt, required in scripts/agents)
ical delete 2 --force

# Search for events
ical search "meeting" --from "30 days ago" --to "next month"

# Export events to ICS
ical export --format ics --from today --to "in 30 days" --output-file events.ics
```

## 命令参考

### 事件创建、查看、更新和删除（CRUD）

| 命令        | 别名         | 功能                          |
| ------------ | --------------- | --------------------------- |
| `ical add`    | `create`, `new` | 创建新事件                   |
| `ical show`   | `get`, `info`   | 查看事件详细信息                |
| `ical update` | `edit`          | 更新事件属性                   |
| `ical delete` | `rm`, `remove`  | 删除事件                     |

### 事件列表查看

| 命令        | 别名        | 功能                          |
| -------------- | -------------- | ------------------------------ |
| `ical list`     | `ls`, `events` | 在指定日期范围内列出事件             |
| `ical today`    | —              | 显示今天的事件                   |
| `ical upcoming` | `next`, `soon` | 显示未来 N 天内的事件               |

### 搜索和导出事件

| 命令        | 别名        | 功能                          |
| -------------- | -------------- | ------------------------------ |
| `ical search` | `find`  | 根据标题、地点或备注搜索事件             |
| `ical export` | —       | 将事件导出为 JSON、CSV 或 ICS 格式           |
| `ical import` | —       | 从 JSON 或 CSV 文件导入事件             |

### 日历管理

| 命令                   | 别名           | 功能                          |
| ------------------------- | ----------------- | ------------------------------------ |
| `ical calendars`           | `icals`            | 列出所有日历                     |
| `ical calendars create`    | `add`, `new`      | 创建新日历                     |
| `ical calendars update`    | `edit`, `rename`  | 更新日历（重命名、更改颜色）             |
| `ical calendars delete`    | `rm`, `remove`    | 删除日历及其所有事件                 |

### 其他功能

| 命令                | 别名         | 功能                          |
| ---------------------- | ------- | -------------------------------------------------- |
| `ical skills install`   | —       | 为 Claude Code/Codex 安装 ical 功能插件       |
| `ical skills uninstall` | —       | 卸载 ical 功能插件                 |
| `ical skills status`    | —       | 显示插件安装状态                   |
| `ical version`          | —       | 显示程序版本和构建信息                 |
| `ical completion`       | —       | 为 bash/zsh/fish 提供命令补全功能           |

有关每个命令的完整参数说明，请参阅 [references/commands.md](references/commands.md)。

## 关键概念

### 行号

事件列表会显示行号（如 `#1`, `#2`, `#3` 等）。这些行号会被缓存到 `~/.ical-last-list` 文件中，以便在后续命令中引用：

```bash
ical list --from today --to "next week"   # Shows #1, #2, #3...
ical show 2                                # Show details for row #2
ical update 3 --title "New title"          # Update row #3
ical delete 1 --force                      # Delete row #1 (skip confirmation)
ical delete 1                              # Delete row #1 (prompts for confirmation)
```

每次执行 `list`, `today` 或 `upcoming` 命令时，行号会重置。如果未提供参数，`show`, `update` 和 `delete` 命令会启动交互式选择器来帮助用户输入事件信息。

### 事件 ID（适用于脚本和自动化脚本）

如果你有完整的事件 ID（通常通过 `-o json` 格式输出），可以使用 `--id` 参数进行精确查找，避免不必要的匹配：

```bash
# Get event ID from JSON output
EVENT_ID=$(ical today -o json | jq -r '.[0].id')

# Use --id for reliable exact lookup
ical show --id "$EVENT_ID"
ical update --id "$EVENT_ID" --title "New title"
ical delete --id "$EVENT_ID" --force
```

> **脚本使用注意事项**：
> - `ical delete` 命令默认会提示用户确认操作。非交互式使用时必须使用 `--force`（或 `-f`）参数。该命令没有 `--confirm` 参数。
> - `ical update` 命令不需要用户确认，也不支持 `--force` 参数——直接使用需要修改的参数即可。
> `--id` 和参数之间的顺序是固定的，同时使用这两个参数会导致错误。

### 自然语言日期格式

日期参数（`--from`, `--to`, `--start`, `--end`, `--due`）支持自然语言输入：

```bash
ical list --from today --to "next friday"
ical add "Lunch" --start "tomorrow at noon" --end "tomorrow at 1pm"
ical search "standup" --from "2 weeks ago"
ical upcoming --days 14
```

支持的日期格式包括：`today`, `tomorrow`, `next monday`, `in 3 hours`, `eod`, `eow`, `this week`, `5pm`, `mar 15`, `2 days ago` 等。详细格式说明请参阅 [references/dates.md](references/dates.md)。

### 交互式界面

`add` 和 `update` 命令支持 `-i` 参数，可开启基于表单的交互式输入界面：

```bash
ical add -i        # Multi-page form: title, calendar, dates, location, recurrence
ical update 2 -i   # Pre-filled form with current event values
```

`show`, `update`, `delete` 命令在未提供参数时也会启动交互式选择器。

### 输出格式

所有读取事件的命令都支持 `-o` 或 `--output` 参数：

- **table**（默认）：带边框和颜色的表格格式
- **json**：机器可读的 JSON 格式（ISO 8601 日期格式）
- **plain**：纯文本格式，每行一个事件

系统会忽略 `NO_COLOR` 环境变量或 `--no-color` 参数的影响。

### 事件重复规则

事件可以设置重复规则：

```bash
# Daily standup
ical add "Standup" --start "tomorrow at 9am" --repeat daily

# Every 2 weeks on Mon and Wed
ical add "Team sync" --start "next monday at 10am" --repeat weekly --repeat-interval 2 --repeat-days mon,wed

# Monthly for 6 months
ical add "Review" --start "mar 1 at 2pm" --repeat monthly --repeat-count 6

# Yearly until a date
ical add "Anniversary" --start "jun 15" --repeat yearly --repeat-until "2030-06-15"
```

使用 `--repeat none` 可取消事件的重复设置；使用 `--span future` 可更新或删除当前事件及其未来的所有重复事件。

### 事件提醒

可以使用 `--alert` 参数为事件设置提醒：

```bash
ical add "Meeting" --start "tomorrow at 2pm" --alert 15m          # 15 minutes before
ical add "Flight" --start "mar 15 at 8am" --alert 1h --alert 1d   # 1 hour + 1 day before
```

支持的提醒时间单位包括：`m`（分钟）、`h`（小时）、`d`（天）。

## 常见使用场景

- **每日事件回顾**  
- **每周计划安排**  
- **使用 JSON 格式进行脚本自动化操作**

### 日历相关字段

- **日历字段**：`id`, `title`, `type`, `color`, `source`, `readOnly`
- **事件字段**：`id`, `title`, `start_date`, `end_date`, `calendar`, `calendar_id`, `location`, `notes`, `url`, `all_day`, `recurrence`, `alerts`

### 日历备份与恢复

```bash
# Export all events from the past year
ical export --from "12 months ago" --to "in 12 months" --format json --output-file backup.json

# Export as ICS for other calendar apps
ical export --from today --to "in 6 months" --format ics --output-file events.ics

# Import from backup
ical import backup.json --calendar "Restored"
```

## 公开 Go API

如需通过编程方式访问 macOS 日历，可以直接使用 [go-eventkit](https://github.com/BRO3886/go-eventkit)：

```go
import "github.com/BRO3886/go-eventkit/calendar"

client, _ := calendar.New()
events, _ := client.Events(from, to, calendar.WithCalendarName("Work"))
event, _ := client.CreateEvent(calendar.CreateEventInput{
    Title:        "Team Meeting",
    StartDate:    start,
    EndDate:      end,
    CalendarName: "Work",
})
```

详细 API 文档请参阅 [go-eventkit](https://github.com/BRO3886/go-eventkit)。

## 限制

- **仅支持 macOS**：需要通过 cgo 使用 EventKit 框架
- **不支持参与者管理**：参与者信息和组织者信息仅支持读取（苹果系统的限制）
- **订阅日历和生日日历不可编辑**：无法在这些日历上创建新事件
- **事件 ID 是日历级别的**：事件 ID 前面的 UUID 是日历 ID，而非特定事件的标识。建议使用行号或交互式界面来识别事件