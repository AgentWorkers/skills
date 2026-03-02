---
name: reminder
description: 使用 OpenClaw 的 cron 功能创建一次性提醒任务。用户可以通过 Discord 以自然语言的方式指定提醒时间和任务内容，任务完成后的结果也会通过 Discord 发送给用户。
metadata:
  {
    "openclaw": {
      "emoji": "⏰",
      "user-invocable": true,
      "requires": { "bins": ["openclaw"], "tools": ["session_status"] }
    }
  }
---
# 提醒技能

使用 OpenClaw 的 cron 功能创建一次性提醒任务。

## 使用方法

当用户输入“30 秒后提醒我 XXX”或“下午 3 点提醒我”时，系统会创建一个 cron 作业，在指定时间执行该任务并返回执行结果。

## 参数配置

### 固定参数

- `--session main`：使用主会话（main session）来继承 Discord 的上下文信息。
- `--system-event`：用于主会话的系统事件数据。
- `--channel discord`：指定的 Discord 频道。
- `--announce`：将执行结果直接发送到指定的 Discord 频道。
- `--delete-after-run`：任务执行完成后自动删除。

### 动态参数（从当前会话上下文中获取）

可以使用 `session_status` 工具获取当前会话的上下文信息：

- `--agent`：从 `deliveryContext.accountId` 中获取（例如：`machu`）。
- `--to`：从 `deliveryContext.to` 中获取（例如：`channel:1476104553148452958`）。

### 时间解析

支持以下相对时间格式：

- `30 seconds`（30 秒后）
- `1 minute`（1 分钟后）
- `30 minutes`（30 分钟后）
- `2 hours`（2 小时后）
- `1 day`（1 天后）

同时支持以下绝对时间格式：

- `3pm`（下午 3 点）
- `9am today`（今天上午 9 点）
- `12pm tomorrow`（明天中午 12 点）

解析后的时间格式需转换为 ISO 8601 格式，以便用于 cron 作业。

## 使用示例

用户输入：“30 秒后提醒我查看天气”。

### 任务内容的安全性处理

用户指定的任务内容在传递给 cron 之前必须进行安全处理：

1. **验证规则**：拒绝任何包含危险字符的输入。脚本会拒绝以下类型的输入：
   - 命令替换符：`$()`, ````, ``
   - Shell 运算符：`;`, `|`, `&`, `>`, `<`
   - 双引号：`"`（可能导致命令解析错误）
   - 新行符：`\n`（可能用于插入多条命令）
   - 危险的命令前缀：`sudo`, `rm`, `wget`, `curl`, `bash` 等

2. **安全处理脚本**：使用 `scripts/sanitize-message.sh` 脚本对输入内容进行验证。

3. **处理方式**：如果输入内容被拒绝，系统会告知用户任务包含无效字符，并要求用户重新输入，避免使用 `$()`, `;`, `|`, `&`, `>`, `<`, `"` 或其他危险命令。

## 确认回复

任务创建完成后，系统会向用户回复确认信息，例如：“好的，X 分钟后会提醒您执行 XXX”。

## 注意事项：

- 提醒时间必须在未来，不能是过去的时间。
- 任务内容应简洁明了。
- 如果任务执行时间超过 48 小时，建议用户使用日历功能。
- 为确保消息可靠地发送到 Discord，务必使用 `--session main` 和 `--system-event` 参数。
- 在创建任务之前，务必使用 `sanitize-message.sh` 脚本对任务内容进行安全验证。