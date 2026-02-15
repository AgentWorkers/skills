---
name: gcalcli-calendar
description: "通过 `gcalcli` 使用 Google 日历：默认情况下仅显示今日的日程安排；采用“范围优先”的查找方式（即先查找指定范围内的日程）；支持快速创建/删除日程并会进行验证；该工具经过优化，以减少调用次数并降低输出信息量。"
metadata: {"openclaw":{"emoji":"📅","requires":{"bins":["gcalcli"]}}}
---

# gcalcli-calendar

使用 `gcalcli` 可以以最少的工具调用次数和最少的输出来读取、搜索或管理 Google 日历。

## 规则

### CLI 标志的放置（非常重要）
- 全局标志（`--nocolor`, `--calendar`）必须放在子命令之前。
- 与子命令相关的标志必须放在子命令名称之后。
- 例如：`gcalcli --nocolor delete --iamaexpert "query" start end` — 而不是 `gcalcli --nocolor --iamaexpert delete ...`。
- 这适用于所有子命令的标志：`--iamaexpert`（删除）、`--noprompt`/`--allday`（添加）、`--use-legacy-import`（导入）等。

### 输出与语言
- 除非用户明确要求（例如 "show commands used", "/debug", "/commands"），否则不要打印 CLI 命令/标志/工具详细信息。
- 如果用户要求查看命令：按顺序打印所有执行的命令（包括重试情况），不要打印其他内容。
- 在一个回复中不要混合使用不同的语言。
- 保持简洁。除非找不到结果，否则不要提供额外的信息。

### 日期与格式
- 默认使用用户友好的日期格式。只有在用户明确要求时才使用 ISO 格式。
- 除非需要区分事件标题的歧义，否则不要对事件标题进行引用。

### 日历范围
- 信任 `gcalcli` 的配置（默认情况下会忽略某些日历）。除非用户请求 "across all calendars" 或结果明显错误，否则不要扩大搜索范围。

### 日程（默认仅显示今天）
- 如果用户仅请求 "agenda" 而没有指定日期，系统将仅显示今天的日程。
- 只有在用户明确要求时才会显示更长的时间范围（明天、接下来的 N 天或特定日期范围）。

### 工作日请求（无需手动计算）
- 如果用户仅指定 "on Monday/Tuesday/..." 而没有提供具体日期：
  1) 首先获取接下来 14 天的日程安排；
  2) 从工具输出中选择匹配的事件；
  3) 继续操作（如果有多个匹配项，则需要进一步确认）。

### 查找事件：优先使用确定性扫描（按事件含义匹配）
- 在取消、删除或编辑事件时：
  - 优先使用 "agenda" 功能而非 "search" 功能。
  - 使用有限的时间窗口，并根据事件含义进行匹配（语义匹配），而不是精确的文本匹配。
  - 默认的时间窗口设置：
    - 如果用户指定了具体日期：仅扫描该日期的事件。
    - 如果用户指定了工作日：扫描接下来 14 天的事件。
    - 如果用户只提供了事件含义（如 "train", "lecture" 等）而没有指定日期：首先扫描接下来 30 天的事件。
    - 如果仍然找不到事件：扩展搜索范围到 180 天，并在找不到结果时给出提示。

只有在以下情况下，才使用 `gcalcli` 的 "search" 功能：
  - 时间窗口太大，无法通过 "agenda" 功能完成扫描；
  - 用户明确要求进行搜索。

### 搜索（有限的时间范围）
- 默认搜索范围：接下来大约 180 天（除非用户另有指定）。
- 如果没有找到匹配项：显示 "在接下来的 ~6 个月内没有匹配项 (<from>-><to>)" 并提供扩展搜索的选项。
- 只有在找不到结果时才显示搜索范围。

### 工具效率
- 默认情况下使用 `--nocolor` 选项以减少格式化和不必要的输出。
- 只有在需要解析、去重或排序数据时才使用 `--tsv` 选项。

## 操作策略（优化对话速度）

此技能专为个人助理设计，用户期望快速、无障碍地管理日历。以下的确认策略是经过深思熟虑的用户体验设计——具体原因和安全措施请参阅 README.md。

### 明确的操作：立即执行
- 对于取消、删除或编辑操作，如果满足以下所有条件，则直接执行：
  - 用户明确请求了该操作（例如 "删除我的牙医预约"）。
  - 在指定的时间窗口内只有一个匹配的事件。
  - 匹配结果明确无误（在指定的日期或用户提供的日期和时间上）。

### 不明确的操作：始终先询问用户
- 如果有多个匹配项或匹配结果不确定：
  - 提出一个简短的询问问题，列出所有可能的选项（1-3 行），然后等待用户的选择。

### 创建事件：必须进行跨日历的重叠检查
- 在创建事件时：
  - 必须在所有未被忽略的日历中检查事件是否与其他事件有重叠（即使新事件被创建在特定的日历中）。
  - 如果存在重叠事件：
    - 在创建前请求用户确认。
  - 如果没有重叠：
    - 立即创建事件。

### 选择正确的创建方法
- **`add`** — 用于一次性事件。支持 `--allday`、`--reminder`、`--noprompt` 选项。不支持重复事件或显示事件是否可用（`TRANSP:TRANSPARENT`）。
- **通过 stdin 进行导入** — 仅在需要设置事件重复规则（`RRULE`）或显示事件是否可用（`TRANSP:TRANSPARENT`）时使用。通过 stdin 传递 ICS 格式的数据；切勿创建临时的 .ics 文件（执行沙箱环境中的工作目录可能不可靠）。
- **`quick`** — 除非用户明确要求使用自然语言输入来创建事件，否则不要使用此选项。此方法的准确性较低。

### 删除操作必须经过验证
- 使用 `--iamaexpert` 选项进行非交互式删除（该选项位于 `delete` 子命令之后）。这是 `gcalcli` 内置的非交互式/脚本化删除功能。
- 删除后必须在相同的时间窗口内通过 "agenda" 功能再次验证事件是否存在。
- 如果验证结果显示事件仍然存在，可以使用 `--refresh` 选项尝试重新删除。
- 除非验证确认事件已被删除，否则不要声称操作成功。

## 标准命令

### 日程（确定性列表）
- 显示今天的日程：`gcalcli --nocolor agenda today tomorrow`
- 显示接下来 14 天的工作日日程：`gcalcli --nocolor agenda today +14d`
- 显示接下来 30 天的事件（按事件含义匹配）：`gcalcli --nocolor agenda today +30d`
- 自定义时间范围：`gcalcli --nocolor agenda <start> <end>`

### 搜索（备用/明确请求）
- 默认搜索范围：接下来大约 6 个月内的事件：`gcalcli --nocolor search "<query>" today +180d`
- 自定义时间范围：`gcalcli --nocolor search "<query>" <start> <end>`

### 创建事件 — `add`（一次性事件）
- 创建事件前的重叠检查（跨日历）：
  - `gcalcli --nocolor agenda <start> <end>` — 重要：此处不要使用 `--calendar` 选项；必须检查所有未被忽略的日历中的事件重叠情况。
- 定时事件：
  - `gcalcli --nocolor --calendar "<Cal>" add --noprompt --title "<Title>" --when "<Start>" --duration <minutes>`
- 全天事件：
  - `gcalcli --nocolor --calendar "<Cal>" add --noprompt --allday --title "<Title>" --when "<Date>"`
- 带有提醒的事件：
  - `--reminder "20160 popup"` — 在事件发生前 14 天提醒
  - `--reminder "10080 popup"` — 在事件发生前 7 天提醒
  - `--reminder "0 popup"` — 在事件发生时提醒
  - 时间单位后缀：`w`（周）、`d`（天）、`h`（小时）、`m`（分钟）。如果没有后缀，则表示分钟。
  - 提醒方式：`popup`（默认）、`email`、`sms`。

### 创建事件 — 通过 stdin 进行导入（重复事件/显示事件是否可用）
- 仅在 `add` 功能无法满足需求时使用（例如重复事件或需要显示事件是否可用）。
- 通过 stdin 直接传递 ICS 数据；切勿创建临时文件。
```
echo 'BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
DTSTART;VALUE=DATE:20260308
SUMMARY:Event Title
RRULE:FREQ=YEARLY
TRANSP:TRANSPARENT
END:VEVENT
END:VCALENDAR' | gcalcli import --calendar "<Cal>"
```
- `DTSTART;VALUE=DATE:YYYYMMDD` 用于全天事件；`DTSTART:YYYYMMDDTHHmmSS` 用于定时事件。
- `RRULE:FREQ=YEARLY` — 每年重复一次。
- `TRANSP:TRANSPARENT` — 表示事件可用；`TRANSP:OPAQUE` — 表示事件不可用（默认值）。
- 每次导入操作对应一个事件（一个 VEVENT 块）。如果需要多个事件，请分别进行导入。
- 可使用 `--reminder "TIME"` 选项设置提醒时间。
- 所有与导入相关的选项（`--use-legacy-import`、`--verbose` 等）必须放在 `import` 之后。

### 删除操作（需要验证）
- 使用 `--iamaexpert` 选项进行非交互式删除（该选项位于 `delete` 子命令之后）。这是 `gcalcli` 的内置非交互式删除功能。
- 删除后必须在相同的时间窗口内通过 "agenda" 功能再次验证事件是否存在。
- 如果验证结果显示事件仍然存在，可以使用 `--refresh` 选项尝试重新删除。
- 除非验证确认事件已被删除，否则不要声称操作成功。

### 其他常用命令

### 显示日程（确定性列表）
- 显示今天的日程：`gcalcli --nocolor agenda today tomorrow`
- 显示接下来 14 天的工作日日程：`gcalcli --nocolor agenda today +14d`
- 显示接下来 30 天的事件（按事件含义匹配）：`gcalcli --nocolor agenda today +30d`
- 自定义时间范围：`gcalcli --nocolor agenda <start> <end>`

### 搜索（备用/明确请求）
- 默认搜索范围：接下来大约 6 个月内的事件：`gcalcli --nocolor search "<query>" today +180d`
- 自定义时间范围：`gcalcli --nocolor search "<query>" <start> <end>`

### 创建事件 — `add`（一次性事件）
- 创建事件前的重叠检查（跨日历）：
  - `gcalcli --nocolor agenda <start> <end>` — 重要：此处不要使用 `--calendar` 选项；必须检查所有未被忽略的日历中的事件重叠情况。
- 定时事件：
  - `gcalcli --nocolor --calendar "<Cal>" add --noprompt --title "<Title>" --when "<Start>" --duration <minutes>`
- 全天事件：
  - `gcalcli --nocolor --calendar "<Cal>" add --noprompt --allday --title "<Title>" --when "<Date>"`
- 带有提醒的事件：
  - `--reminder "20160 popup"` — 在事件发生前 14 天提醒
  - `--reminder "10080 popup"` — 在事件发生前 7 天提醒
  - `--reminder "0 popup"` — 在事件发生时提醒
  - 时间单位后缀：`w`（周）、`d`（天）、`h`（小时）、`m`（分钟）。如果没有后缀，则表示分钟。
  - 提醒方式：`popup`（默认）、`email`、`sms`。

### 创建事件 — 通过 stdin 进行导入（重复事件/显示事件是否可用）
- 仅在 `add` 功能无法满足需求时使用（例如需要设置事件重复规则或显示事件是否可用）。
- 通过 stdin 直接传递 ICS 数据；切勿创建临时文件。
- 示例 ICS 数据格式：
  - `DTSTART;VALUE=DATE:YYYYMMDD` 用于全天事件；`DTSTART:YYYYMMDDTHHmmSS` 用于定时事件。
- `RRULE:FREQ=YEARLY` — 每年重复一次。
  - `DAILY`、`WEEKLY`、`MONTHLY` — 分别表示每天、每周、每月重复。
- `TRANSP:TRANSPARENT` — 表示事件可用；`TRANSP:OPAQUE` — 表示事件不可用（默认值）。
- 每次导入操作对应一个事件（一个 VEVENT 块）。如果需要多个事件，请分别进行导入。
- 可使用 `--reminder "TIME"` 选项设置提醒时间。
- 所有与导入相关的选项（`--use-legacy-import`、`--verbose` 等）必须放在 `import` 之后。

### 删除事件（需要验证）
- 通过 "agenda" 功能查找要删除的事件：
  - `gcalcli --nocolor agenda <dayStart> <dayEnd>`（指定日期）
  - `gcalcli --nocolor agenda today +14d`（工作日）
  - `gcalcli --nocolor agenda today +30d`（仅根据事件含义判断）
- 非交互式删除：
  - `gcalcli --nocolor delete --iamaexpert "<query>" <start> <end>`
- 验证结果：
  - `gcalcli --nocolor agenda <dayStart> <dayEnd>`
- 如果仍然存在重复事件，可以尝试再次删除：
  - `gcalcli --nocolor --refresh agenda <dayStart> <dayEnd>`