---
name: nag
description: 这是一个持续提醒系统，它会不断提醒您，直到您确认任务已完成。适用于设置重复性提醒、催促性任务，或任何需要跟进直至得到确认的任务。该系统支持每日重置、可配置的提醒窗口、紧急程度的提升，以及与自然语言匹配的确认机制。**请勿将其用于一次性提醒（请使用 cron）或需要立即行动的时效性警报（请使用带有 wakeMode 的 cron）**。
---
# Nag — 持续性提醒工具

Nag 是一个用于管理重复性提醒的工具。每个提醒都设有首次触发时间、提醒窗口，并且每天会自动重置。

## 使用场景

- 需要每天重复执行的习惯性任务（如补充营养、锻炼、练习）
- 被忽视或遗忘、需要持续跟进的任务
- 仅靠“提醒一次”无法确保完成的任务

## 不适合使用的情况

- 一次性提醒（例如“20分钟后提醒我”）——应使用 `schedule.kind: "at"` 的 cron 作业来处理
- 需要立即响应的紧急警报
- 无需用户确认的提醒（仅用于提供信息）

## 设置步骤

### 1. 状态文件（State File）

在工作区创建 `memory/nag-state.json` 文件：

```json
{
  "date": "2026-02-15",
  "reminders": {}
}
```

`date` 字段用于触发每日自动重置：当当前日期与存储的日期不同时，所有提醒都会被重置为未确认状态。

### 2. 提醒配置（Reminder Configuration）

在工作区根目录下创建 `nag-config.json` 文件：

```json
{
  "reminders": [
    {
      "id": "morning-supplements",
      "label": "morning supplements",
      "cronFirst": "0 8 * * *",
      "nagAfter": "09:00",
      "confirmPatterns": ["taken", "done", "took them", "did it", "yes"],
      "tone": "friendly but persistent, escalate to ALL CAPS drama after 3 nags",
      "messages": {
        "first": "Time for morning supplements!"
      }
    }
  ]
}
```

**字段说明：**

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `id` | 是 | 唯一标识符，用于状态文件中的键 |
| `label` | 是 | 用于显示的、人类可读的名称 |
| `cronFirst` | 是 | 初始提醒的 cron 表达式（用于创建 cron 作业） |
| `nagAfter` | 是 | 心跳提醒开始的时间（格式为 HH:MM，24 小时制） |
| `confirmPatterns` | 是 | 用于标记提醒已完成的语句数组（不区分大小写，支持子字符串匹配） |
| `tone` | 可选 | 用于生成提醒消息的语气。如果未设置，将使用中立友好的语气。模型会根据实际情况调整提醒内容 |
| `messages.first` | 可选 | cron 作业发送的初始提醒文本。如果未设置，将根据 `label` 和 `tone` 自动生成 |
| `messages.nag` | 可选 | 建议使用的提醒文本。如果未设置，将根据 `label`、`tone` 和 `nagCount` 生成 |
| `messages.escalate` | 可选 | 被忽略 3 次后的提醒文本。如果未设置，会根据语气增加紧迫感 |
| `days` | 可选 | 限制提醒触发日期的星期几数组（例如 `["星期一", "星期三", "星期五"]`）。如需每天触发，可省略此字段 |

更多示例请参见 [references/config-examples.md](references/config-examples.md)。

**消息生成规则：**  
当 `messages.nag` 或 `messages.escalate` 未设置时，系统会使用 `label` 和 `tone` 字段动态生成提醒内容。每次提醒的表述应有所不同，避免重复使用相同的文本。`nagCount` 用于表示提醒的紧急程度：0 表示普通，大于 3 表示紧急。

### 3. 配置 Cron 作业与心跳提醒机制

- 为每个提醒创建一个 cron 作业，使其在 `cronFirst` 时间点发送 `messages.first` 消息。
- 在 `HEARTBEAT.md` 文件中添加相应的提醒检查逻辑：

```
## Nag Check
Read nag-config.json and memory/nag-state.json.
For each reminder in nag-config.json:
- If date in state differs from today, reset all reminders (set confirmed: false, nagCount: 0).
- Skip if today's weekday isn't in the reminder's `days` array (if specified).
- If current time is after `nagAfter` and confirmed is false: send a nag message to the user.
  - Generate the message from the reminder's label and tone (or use messages.nag if provided).
  - If nagCount >= 3, escalate urgency (use messages.escalate if provided, otherwise generate with more intensity).
  - Increment nagCount in state.
- Do NOT nag before the nagAfter time.
```

### 4. 确认操作

当用户发送符合任何 `confirmPatterns` 的消息时，更新 `memory/nag-state.json` 文件：

```json
{
  "date": "2026-02-15",
  "reminders": {
    "morning-supplements": {
      "confirmed": true,
      "confirmedAt": "09:06",
      "nagCount": 1
    }
  }
}
```

通过检查用户消息中是否包含任何 `confirmPatterns` 中的子字符串（不区分大小写）来确认提醒是否已被处理。如果有多个提醒符合条件，系统会选择当前处于提醒窗口内的那个提醒进行确认。

## 添加新提醒

1. 在 `nag-config.json` 中添加新提醒的配置。
2. 为该提醒创建一个 cron 作业，设置 `cronFirst` 时间。
3. 心跳提醒机制会自动处理后续的所有操作。

## 删除提醒

1. 从 `nag-config.json` 中删除该提醒的配置。
2. 删除或禁用对应的 cron 作业。
3. （可选）从 `memory/nag-state.json` 中删除该提醒的记录。