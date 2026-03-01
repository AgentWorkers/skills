---
name: rem
description: 使用 `rem` CLI 从终端管理 macOS 的提醒事项。可以创建、列出、更新、完成、删除、搜索以及导出提醒事项列表。支持基于自然语言设置的到期日期、过滤功能，以及导入/导出操作，并支持多种输出格式。适用于需要通过命令行与 Apple Reminders 进行交互、自动化提醒任务流程或编写相关脚本的场景。
metadata:
  author: BRO3886
  version: "0.7.0"
compatibility: Requires macOS with Reminders.app. Requires Xcode Command Line Tools for building from source.
---
# rem — 用于 macOS Reminders 的命令行工具

这是一个用 Go 语言编写的命令行工具（CLI），用于操作 macOS 的 Reminders 应用程序。它通过 cgo 和 EventKit 框架以低于 200 毫秒的速度读取 Reminders 数据。该工具为单一的二进制文件，运行时无需依赖任何外部库。

## 安装

```bash
# macOS (recommended)
curl -fsSL https://rem.sidv.dev/install | bash

# Or via Go
go install github.com/BRO3886/rem/cmd/rem@latest
```

要将此工具安装到您的 AI 代理中，请执行以下命令：

```bash
# Claude Code or Codex
rem skills install

# OpenClaw
rem skills install --agent openclaw
```

## 快速入门

```bash
# See all lists with reminder counts
rem lists --count

# Add a reminder with natural language date
rem add "Buy groceries" --list Personal --due tomorrow --priority high

# List incomplete reminders in a list
rem list --list Work --incomplete

# Search across all reminders
rem search "meeting"

# Complete a reminder by short ID
rem complete abc12345

# View stats
rem stats
```

## 命令参考

### Reminders 的基本操作（CRUD）

| 命令 | 别名 | 描述 |
|---------|---------|-------------|
| `rem add` | `create`, `new` | 创建一个新的提醒 |
| `rem list` | `ls` | 使用过滤器列出提醒 |
| `rem show` | `get` | 显示单个提醒的详细信息 |
| `rem update` | `edit` | 更新提醒的属性 |
| `rem delete` | `rm`, `remove` | 删除一个提醒 |
| `rem complete` | `done` | 将提醒标记为已完成 |
| `rem uncomplete` | — | 将提醒标记为未完成 |
| `rem flag` | — | 为提醒添加标记 |
| `rem unflag` | — | 移除提醒的标记 |

### 列表管理

| 命令 | 别名 | 描述 |
|---------|---------|-------------|
| `rem lists` | — | 显示所有提醒列表 |
| `rem list-mgmt create` | `lm new` | 创建一个新的提醒列表 |
| `rem list-mgmt rename` | — | 重命名一个提醒列表 |
| `rem list-mgmt delete` | `lm rm` | 删除一个提醒列表 |

### 搜索与分析

| 命令 | 描述 |
|---------|-------------|
| `rem search <query>` | 根据标题和备注内容搜索提醒 |
| `rem stats` | 显示统计信息及每个列表的详细数据 |
| `rem overdue` | 显示过期的提醒 |
| `rem upcoming` | 显示未来 N 天内到期的提醒（默认值：7 天） |

### 导出/导入

| 命令 | 描述 |
|---------|-------------|
| `rem export` | 将提醒数据导出为 JSON 或 CSV 格式 |
| `rem import <file>` | 从 JSON 或 CSV 文件导入提醒数据 |

### 其他功能

| 命令 | 描述 |
|---------|-------------|
| `rem skills install` | 为 AI 代理安装 rem 工具 |
| `rem skills uninstall` | 从 AI 代理中卸载 rem 工具 |
| `rem skills status` | 显示工具的安装状态 |
| `rem interactive` / `rem i` | 进入交互式菜单模式 |
| `rem version` | 显示工具的版本信息 |
| `rem completion` | 为 bash/zsh/fish 环境生成命令补全功能 |

有关每个命令的完整参数说明，请参阅 [references/commands.md](references/commands.md)。

## 关键概念

### 简短 ID

Reminders 在系统中使用 UUID 格式进行标识（例如：`x-apple-reminder://AB12CD34-...`）。该工具会显示 UUID 的前 8 位字符作为简短 ID（例如：`AB12CD34`）。您可以在命令中指定自定义前缀；例如，`rem complete AB1` 会匹配名称中包含 “AB1” 的所有提醒。

### 自然语言日期格式

`--due` 参数支持以下自然语言日期格式：

```bash
rem add "Call dentist" --due tomorrow
rem add "Submit report" --due "next friday at 2pm"
rem add "Quick task" --due "in 30 minutes"
rem add "Wrap up" --due eod
```

支持的日期格式包括：`today`（今天）、`tomorrow`（明天）、`next monday`（下周一）、`in 3 hours`（3 小时后）、`eod`（当天结束）、`eow`（明天结束）、`5pm`（下午 5 点）、`2026-02-15`（2026 年 2 月 15 日）等。完整日期格式列表请参阅 [references/dates.md](references/dates.md)。

### 优先级设置

| 优先级 | 标记值 | AppleScript 对应值 |
|-------|-----------|-------------------|
| 高 | `--priority high` | 1（范围：1-4） |
| 中等 | `--priority medium` | 5 |
| 低 | `--priority low` | 9（范围：6-9） |
| 无 | `--priority none` | 0 |

### 输出格式

所有读取提醒的命令都支持 `-o` 或 `--output` 参数来指定输出格式：

- **table**（默认）：带边框的格式化表格 |
- **json**：机器可读的 JSON 格式 |
- **plain**：每行一个条目的纯文本格式

系统会自动识别 `NO_COLOR` 环境变量以禁用颜色显示。

### URL 存储

macOS Reminders 应用程序没有内置的 URL 字段。该工具会将 URL 信息存储在备注字段中，并以 `URL:` 作为前缀进行提取以便显示。

## 常见使用场景

- **每日回顾**：定期检查待办事项 |
- **批量操作**：使用 JSON 文件批量处理提醒 |
- **脚本化处理**：通过 JSON 数据进行自动化操作

## 公开 Go API

如需通过编程方式访问 Reminders 功能，可以直接使用 [`go-eventkit`](https://github.com/BRO3886/go-eventkit)：

```go
import "github.com/BRO3886/go-eventkit/reminders"

client, _ := reminders.New()
r, _ := client.CreateReminder(reminders.CreateReminderInput{
    Title:    "Buy milk",
    ListName: "Shopping",
    Priority: reminders.PriorityHigh,
})
items, _ := client.Reminders(reminders.WithCompleted(false))
```

有关 `go-eventkit` 的完整 API 文档，请参阅 [https://github.com/BRO3886/go-eventkit](https://github.com/BRO3886/go-eventkit)。

## 限制

- **仅支持 macOS**：需要 EventKit 框架和 `osascript` 功能 |
- **不支持标签、子任务或重复规则**：这些功能在 EventKit/AppleScript 中未实现 |
- 使用 `--flagged` 过滤器时性能较低（约 3-4 秒）：在这种情况下，工具会回退到使用 JXA（JavaScript for AppleScript）进行过滤 |
- 在某些 macOS 版本中，删除列表的操作可能会失败