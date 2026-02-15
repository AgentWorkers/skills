---
name: apple-calendar
description: macOS上的Apple Calendar.app集成：支持事件的CRUD（创建、读取、更新、删除）操作、搜索功能以及多日历管理。
metadata: {"clawdbot":{"emoji":"📅","os":["darwin"]}}
---

# Apple 日历

通过 AppleScript 与 Calendar.app 进行交互。脚本的运行路径为：`cd {baseDir}`

## 命令

| 命令 | 用法 |
|---------|-------|
| 列出日历 | `scripts/cal-list.sh` |
| 列出事件 | `scripts/cal-events.sh [天数] [日历名称]` |
| 读取事件信息 | `scripts/cal-read.sh <事件 UID> [日历名称]` |
| 创建事件 | `scripts/cal-create.sh <日历> <事件摘要> <开始时间> <结束时间> [地点] [描述] [全天] [重复频率]` |
| 更新事件 | `scripts/cal-update.sh <事件 UID> [--摘要 X] [--开始时间 X] [--结束时间 X] [--地点 X] [--描述 X]` |
| 删除事件 | `scripts/cal-delete.sh <事件 UID> [日历名称]` |
| 搜索事件 | `scripts/cal-search.sh <搜索条件> [天数] [日历名称]` |

## 日期格式

- 时间格式：`YYYY-MM-DD HH:MM`
- 全天事件：`YYYY-MM-DD`

## 重复频率

| 模式 | 描述 |
|---------|-------|
| 每日 10 次 | `FREQ=DAILY;COUNT=10` |
| 每周一/三/五 | `FREQ=WEEKLY;BYDAY=MO,WE,FR` |
| 每月 15 日 | `FREQ=MONTHLY;BYMONTHDAY=15` |

## 输出格式

- 搜索结果：`UID | 摘要 | 开始时间 | 结束时间 | 是否全天 | 地点 | 日历名称`
- 读取事件信息：包含事件的详细信息（摘要、URL、重复频率等）

## 注意事项：

- 只读日历（如生日、节假日日历）无法被修改。
- 日历名称区分大小写。
- 删除重复事件会删除该事件的所有重复记录。