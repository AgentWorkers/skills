---
name: macos-calendar
description: 通过 AppleScript 创建、列出和管理 macOS 日历事件。适用于用户需要添加提醒、安排事件、创建日历条目、设置截止日期或执行任何与 macOS 上的 Apple 日历相关的操作的情况。例如：请求“3 天后提醒我”、“添加到我的日历中”、“下周一下午 2 点安排会议”或“创建一个每周重复的事件”。仅适用于 macOS 系统。
license: MIT
compatibility: Requires macOS with Calendar.app. Uses osascript (AppleScript) and python3 for JSON parsing.
metadata:
  author: lucaperret
  version: "1.2.0"
  openclaw:
    os: macos
    emoji: "\U0001F4C5"
    homepage: https://github.com/lucaperret/agent-skills
    requires:
      bins:
        - osascript
        - python3
---
# macOS 日历

您可以通过 `$SKILL_DIR/scripts/calendar.sh` 脚本来管理 Apple 日历中的事件。所有日期处理都使用相对时间计算（`当前日期 + N * 天`），以避免因地区设置不同而产生的日期格式问题（例如法语/英语/德语系统中的日期格式差异）。

## 快速入门

### 列出日历

在创建事件之前，务必先列出所有可用的日历，以确定正确的日历名称：

```bash
"$SKILL_DIR/scripts/calendar.sh" list-calendars
```

### 创建事件

```bash
echo '<json>' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

**JSON 字段说明：**

| 字段 | 是否必填 | 默认值 | 说明 |
|---|---|---|---|
| `summary` | 是 | - | 事件标题 |
| `calendar` | 否 | 首选日历 | 从 `list-calendars` 函数中获取的日历名称 |
| `description` | 否 | "" | 事件备注 |
| `offset_days` | 否 | 0 | 从今天起的天数（0 表示今天，1 表示明天，7 表示下一周） |
| `iso_date` | 否 | - | 绝对日期格式（`YYYY-MM-DD`）（会覆盖 `offset_days` 的设置） |
| `hour` | 否 | 9 | 事件开始时间（0-23 小时） |
| `minute` | 否 | 0 | 事件开始分钟（0-59 分钟） |
| `duration_minutes` | 否 | 30 | 事件持续时间（分钟） |
| `alarm_minutes` | 否 | 0 | 事件提醒时间（分钟，0 表示不提醒） |
| `all_day` | 否 | false | 全天事件 |
| `recurrence` | 否 | - | iCal 的 RRULE 规则字符串。详情请参阅 [references/recurrence.md](references/recurrence.md) |

## 理解用户指令

将用户的自然语言指令转换为相应的 JSON 数据格式：

| 用户指令 | 对应的 JSON 数据 |
|---|---|
| “明天下午 2 点” | `offset_days: 1, hour: 14` |
| “3 天后” | `offset_days: 3` |
| “下周一上午 10 点” | 计算从今天到下周一的 `offset_days`，然后设置 `hour: 10` |
| “2026 年 2 月 25 日下午 3:30” | `iso_date: "2026-02-25", hour: 15, minute: 30` |
| “每周一至周五上午 9 点” | `hour: 9, recurrence: "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR"` |
| “提前 1 小时提醒我” | `alarm_minutes: 60` |
| “3 月 1 日全天事件” | `iso_date: "2026-03-01", all_day: true` |

对于 “下周一”、“下周五” 等时间表达式，请根据当前日期计算具体的 `offset_days` 值。如有需要，可以使用 `date` 命令来获取当前日期：

```bash
# Days until next Monday (1=Monday)
target=1; today=$(date +%u); echo $(( (target - today + 7) % 7 ))
```

## 示例指令及对应的脚本代码

以下是一些真实的用户指令及其对应的脚本代码：

**“2 天后提醒我去看牙医”**  
```bash
"$SKILL_DIR/scripts/calendar.sh" list-calendars
```  
然后执行：  
```bash
echo '{"calendar":"Personnel","summary":"Call dentist","offset_days":2,"hour":9,"duration_minutes":15,"alarm_minutes":30}' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

**“每周二下午 2 点安排团队会议，并设置 10 分钟的提醒”**  
```bash
echo '{"calendar":"Work","summary":"Team sync","hour":14,"duration_minutes":60,"recurrence":"FREQ=WEEKLY;BYDAY=TU","alarm_minutes":10}' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

**“将 7 月 15 日标记为假期”**  
```bash
echo '{"calendar":"Personnel","summary":"Vacances","iso_date":"2026-07-15","all_day":true}' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

**“我下周四下午 3:30 有医生预约，请提前 1 小时提醒我”**  
```bash
# First compute offset_days to next Thursday (4=Thursday)
target=4; today=$(date +%u); offset=$(( (target - today + 7) % 7 )); [ "$offset" -eq 0 ] && offset=7
```  
然后执行：  
```bash
echo "{\"calendar\":\"Personnel\",\"summary\":\"Doctor appointment\",\"offset_days\":$offset,\"hour\":15,\"minute\":30,\"duration_minutes\":60,\"alarm_minutes\":60}" | "$SKILL_DIR/scripts/calendar.sh" create-event
```

**“接下来 4 周内，每周一上午 9 点安排每日例会”**  
```bash
echo '{"calendar":"Work","summary":"Daily standup","hour":9,"duration_minutes":15,"recurrence":"FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;COUNT=20"}' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

**“每周五上午 11 点安排与经理的 1 对 1 会议”**  
```bash
echo '{"calendar":"Work","summary":"1-on-1 Manager","hour":11,"duration_minutes":30,"recurrence":"FREQ=WEEKLY;INTERVAL=2;BYDAY=FR","alarm_minutes":5}' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

## 重要规则：

1. **如果用户没有指定日历，请务必先列出所有日历**。标记为 `[read-only]` 的日历无法用于创建事件。
2. **在 AppleScript 中严禁使用硬编码的日期字符串**，请始终使用 `offset_days` 或 `iso_date` 来表示日期。
3. 如果用户使用多个个人日历，请务必确认正确的日历名称。
4. **切勿操作标记为 `[read-only]` 的日历**，否则脚本会报错。
5. **对于重复事件，请参考 [references/recurrence.md](references/recurrence.md) 了解 RRULE 规则的语法。
6. **所有数据必须通过标准输入（stdin）传递**，切勿作为命令行参数传递，以防数据泄露。
7. **脚本会对所有输入进行验证（类型转换、范围检查、格式验证）；无效的输入会触发错误提示。
8. **所有操作都会被记录到 `logs/calendar.log` 文件中，记录中包含时间戳、执行的命令、使用的日历以及事件摘要。**