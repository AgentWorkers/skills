---
name: remindme
description: "⏰ 为 OpenClaw 提供简单的 Telegram 提醒功能，完全不依赖任何第三方工具（如 cron）。"
tags: [cron, reminders, productivity, schedule, telegram, discord, slack, whatsapp, signal]
metadata:
  openclaw:
    summary: "**Remind Me v2:** Schedule reminders anywhere. Natural language, native cron, zero dependencies."
    emoji: "bell"
user-invocable: true
command-dispatch: prompt
---

# Remind Me v2

您可以使用自然语言在**任何渠道**上设置提醒。无需任何设置，也无需依赖任何外部服务。

## 使用方法

```
/remindme drink water in 10 minutes
/remindme standup tomorrow at 9am
/remindme call mom next monday at 6pm
/remindme in 2 hours turn off oven
/remindme check deployment in 30s
/remindme every day at 9am standup
/remindme every friday at 5pm week recap
/remindme drink water in 10 minutes on telegram
/remindme standup tomorrow at 9am on discord
/remindme list
/remindme cancel <jobId>
```

## 代理指令

当用户触发 `/remindme` 命令时，系统会解析用户的意图：

- **列出所有提醒** → 调用 `cron.list` 函数显示当前激活的提醒任务。
- **取消/删除 `<jobId>` 提醒** → 调用 `cron.remove` 函数并传入相应的 `jobId`。
- **其他所有操作** → 创建一个新的提醒（具体步骤见下文）。

---

### 第一步：解析输入（结构化处理流程）

从输入内容中提取三个关键信息：**提醒内容**、**提醒时间**以及**提醒频率**（一次性还是周期性）。

按照以下决策流程进行处理，直到找到匹配项：

#### 第一层：模式匹配（适用于所有模型）

从输入内容中查找以下模式，并从上到下进行匹配。第一个匹配到的模式将决定提醒时间：

**相对时间表达**：
- `in Ns`、`in N seconds`、`in N min`、`in N hr`、`in N days`、`in N weeks`：表示具体的时间长度（以秒、分钟、小时或天为单位）。
- `at <time>`：表示绝对的时间点（例如 `at 10:30`）。
- `tomorrow`、`next <day>`、`on <day>`：表示具体的日期（例如 `tomorrow`、`next Monday`、`on Friday`）。

**周期性提醒**：
- `every Nm/Nh/Nd`：表示“每隔 N 分钟/小时/天”重复。
- `every day at <time>`、`every weekday at <time>`、`every weekend at <time>`：表示“每天/每周几的 <时间>`。
- `every hour`：表示“每小时”重复。

**单位转换表**（用于 `everyMs` 和时间计算）：
| 单位 | 对应的毫秒数 |
|---|---|
| 1 second | 1000 |
| 1 minute | 60000 |
| 1 hour | 3600000 |
| 1 day | 86400000 |
| 1 week | 604800000 |

#### 第二层：俚语和简写表达

如果第一层匹配失败，检查以下常见表达：
- `in a bit`、`in a minute`、`shortly`：表示“大约 30 分钟后”。
- `in a while`：表示“1 小时后”。
- `later`、`later today`：表示“3 小时后”。
- `end of day`、`eod`：表示“今天下午 5 点”。
- `end of week`、`eow`：表示“周五下午 5 点”。
- `end of month`、`eom`：表示“本月最后一天下午 5 点”。
- `morning`、`afternoon`、`evening`、`tonight`：表示具体的时间点（例如 “上午 9 点”、“下午 2 点”、“晚上 6 点”）。
- `midnight`：表示“次日午夜”。
- `noon`：表示“中午 12 点”。

#### 第三层：事件相关表达（需要利用语言理解能力）

如果前两层都未匹配到有效信息，可能用户指的是某个特定事件或节日。根据用户的描述进行判断：
- **节日时间**：例如用户说“在 <节日> 之前/之后/当天”，需要确定节日的具体日期（例如圣诞节、情人节等）。
- **浮动日期的节日**：例如感恩节（美国）通常在十一月的第四个星期四，需要根据当年实际情况计算日期。

#### 第四层：消除歧义（如有必要，请用户确认）

如果经过前三层处理仍无法确定提醒时间，请询问用户具体时间。切勿自行猜测或设置默认时间。

### 第二步：计算提醒时间

- **时区规则**：始终使用用户的**本地时区**（系统默认时区），不要使用 UTC。如果用户指定了时区（例如 “at 9am EST”），则使用该时区。
- **一次性提醒**：使用包含用户本地时区偏移量的 ISO 8601 时间戳。
- **周期性提醒**：使用 Cron 表达式（例如 `every day at 9am` 表示“每天上午 9 点”）。
- **间隔性提醒**：使用 `everyMs` 参数设置提醒间隔（例如 `every 2 hours` 表示“每 2 小时”）。

### 第三步：确定提醒的展示渠道

提醒只有在用户能够看到的地方才能发挥作用。系统会按照以下优先级确定提醒的展示渠道：
1. 用户明确指定的渠道（如 Telegram、Discord、Slack、WhatsApp）。
2. 用户最近使用的渠道。
3. 用户在 `MEMORY.md` 文件中设置的优先提醒渠道。
4. 如果用户未配置任何外部渠道，则提示用户选择发送渠道。

### 第四步：调用 `cron.add` 函数

- **一次性提醒**：执行相应的代码块（```json
{
  "name": "Reminder: <short description>",
  "schedule": {
    "kind": "at",
    "at": "<ISO 8601 timestamp>"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "REMINDER: <the user's reminder message>. Deliver this reminder to the user now."
  },
  "delivery": {
    "mode": "announce",
    "channel": "<detected channel>",
    "to": "<detected target>",
    "bestEffort": true
  },
  "deleteAfterRun": true
}
```）。
- **周期性提醒**：执行相应的代码块（```json
{
  "name": "Recurring: <short description>",
  "schedule": {
    "kind": "cron",
    "expr": "<cron expression>",
    "tz": "<IANA timezone>"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "RECURRING REMINDER: <the user's reminder message>. Deliver this reminder to the user now."
  },
  "delivery": {
    "mode": "announce",
    "channel": "<detected channel>",
    "to": "<detected target>",
    "bestEffort": true
  }
}
```）。
- **固定间隔的周期性提醒**（例如“每 2 小时”）：执行相应的代码块（```json
{
  "name": "Recurring: <short description>",
  "schedule": {
    "kind": "every",
    "everyMs": <interval in milliseconds>
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "RECURRING REMINDER: <the user's reminder message>. Deliver this reminder to the user now."
  },
  "delivery": {
    "mode": "announce",
    "channel": "<detected channel>",
    "to": "<detected target>",
    "bestEffort": true
  }
}
```）。

### 第五步：向用户确认提醒信息

在成功设置提醒后，向用户发送确认信息（```
Reminder set!
"<reminder message>"
<friendly time description> (<ISO timestamp or cron expression>)
Will deliver to: <channel>
Job ID: <jobId> (use "/remindme cancel <jobId>" to remove)
```）。

---

## 注意事项：

1. **一次性提醒**必须设置 `deleteAfterRun: true`，周期性提醒则不需要。
2. **必须设置 `delivery.mode: "announce"`，否则用户无法收到提醒通知。
3. **必须设置 `sessionTarget: "isolated"`，以确保提醒在独立会话中执行。
4. **必须设置 `wakeMode: "now"`，以确保提醒在预定时间立即发送。
5. **必须设置 `delivery.bestEffort: true`，以防止提醒发送失败。
6. **不要使用 `act:wait` 或循环操作来延迟提醒发送（超过 1 分钟的延迟由 Cron 自动处理）。
7. **不要将提醒发送到本地主机/CLI/网页聊天界面**，因为用户可能不在这些地方；如果用户通过 CLI 使用服务，请询问发送渠道。
8. **始终使用用户的本地时区**，不要使用 UTC；如果 `MEMORY.md` 文件中有时区设置，请优先使用该设置。
9. **对于周期性提醒**，不要设置 `deleteAfterRun`。
10. **务必返回提醒的 `jobId`，以便用户日后取消提醒。
11. 如果用户指定了具体的发送渠道（如 Telegram、Discord 等），请覆盖系统自动检测的渠道设置。

## 常见问题解决方法：

- **提醒未发送？**：使用 `cron.list` 检查 Cron 服务是否在预定时间运行。
- **提醒发送到了错误的聊天界面？**：请使用正确的聊天界面 ID。
- **系统中积累了太多旧的提醒任务？**：请参考 `references/TEMPLATES.md` 中的清理脚本。
- **周期性提醒一直延迟？**：Cron 服务会采用指数级退避策略（首次失败后延迟 30 秒，之后逐渐增加）。

## 参考资料

更多模板和自动清理脚本的详细信息，请参阅 `references/TEMPLATES.md`。