---
name: apple-calendar-manager
description: 通过 AppleScript 管理 Apple 日历事件：创建、编辑、删除和搜索日历事件。
---
# Apple 日历管理器

此技能允许 OpenClaw 通过 AppleScript 来管理 Apple 日历中的事件。

## 功能

-   向指定的日历中添加新事件，并支持智能日期解析（例如：“今天”、“明天”、“下周一”）。
-   （未来功能）编辑现有事件。
-   （未来功能）删除事件。
-   （未来功能）搜索事件。

## 系统要求

-   macOS 操作系统。
-   必须能够访问并授权使用 Apple 日历应用程序进行自动化操作。
-   所要添加的事件日历名称必须存在于用户的日历应用中。

## 使用方法

### 添加事件（支持智能日期解析）

使用 `add_event_smart.sh` 脚本来添加事件，该脚本支持相对日期或绝对日期的输入。

**参数：**
1.  `calendar_name`：日历的名称（例如：“Рабочий”（工作日），“Домашний”（家庭日历）。
2.  `event_summary`：事件的标题。
3.  `event_description`：（可选）事件的描述。
4.  `relative_start_date`：事件的开始时间（相对日期，例如：“today”（今天）、“tomorrow”（明天）、“day after tomorrow”（后天）、“понедельник”（周一）、“next monday”（下周一）；或绝对日期，例如：“2026-02-23”）。
5.  `start_time`：事件的开始时间（格式为 HH:MM，例如：“12:00”）。
6.  `relative_end_date`：事件的结束时间（与 `relative_start_date` 相同，也是相对日期）。
7.  `end_time`：事件的结束时间（格式为 HH:MM，例如：“15:00”）。

**示例：**
```
skills/apple-calendar-manager/add_event_smart.sh "Рабочий" "Чай с Настей" "Чай с Настей с 12 до 15" "tomorrow" "12:00" "tomorrow" "15:00"
```

### 添加事件（支持绝对日期解析）

如果您希望使用 `YYYYMMDDHHMMSS` 格式的绝对日期，可以直接使用 `add_event.scpt` 脚本。

**参数：**
1.  `calendar_name`：日历的名称。
2.  `event_summary`：事件的标题。
3.  `event_description`：事件的描述。
4.  `start_datetimeFormatted`：事件的开始日期和时间（格式为 `YYYYMMDDHHMMSS`）。
5.  `end_datetimeFormatted`：事件的结束日期和时间（格式为 `YYYYMMDDHHMMSS`）。

**示例：**
```
osascript skills/apple-calendar-manager/add_event.scpt "Рабочий" "Тест скилла Календарь" "Тестовое событие" "20260225140000" "20260225150000"
```

## 实现细节

-   通过 `osascript` 直接控制 Apple 日历应用程序。
- `parse_relative_date.sh` 脚本负责将相对日期字符串转换为 AppleScript 所需的绝对日期/时间格式。
- 需要确保 Apple Calendar.app 正在运行且可被访问。
- 仅适用于 macOS 操作系统。