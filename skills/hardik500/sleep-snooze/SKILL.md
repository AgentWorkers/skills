---
name: sleep-snooze
version: 1.0.0
description: 在您的睡眠时间段内，您可以暂时关闭即将到来的通知；醒来后，系统会为您汇总当天的重要信息。该功能支持 Telegram、WhatsApp 以及 OpenClaw 所连接的任何其他消息服务。
user-invocable: true
metadata:
  openclaw:
    emoji: "🌙"
    homepage: https://github.com/Hardik500/sleep-snooze
    requires:
      bins:
        - node
    install:
      - kind: node
        package: better-sqlite3
        bins:
          - node
      - kind: node
        package: node-cron
        bins:
          - node
---
# 睡眠延迟通知系统

我们提供了一个睡眠延迟通知系统。当用户处于睡眠时间时，收到的消息会自动被放入队列中，而不会立即被发送。用户醒来后，系统会自动发送一份晨间摘要，汇总所有已排队的消息。

## 睡眠时间表

用户的睡眠时间表通过环境变量进行配置：
- `SLEEP_START` — 开始睡眠的时间（24小时格式，例如 `22:00`）
- `WAKE_TIME` — 发送摘要并恢复正常通知的时间（例如 `06:00`）
- `TIMEZONE` — IANA时区（例如 `Asia/Kolkata`、`America/New_York`、`Europe/London`）

## 斜杠命令

用户可以直接在聊天中使用以下斜杠命令：
- `/sleep` — 立即手动开启睡眠模式（覆盖时间表设置）
- `/wake` — 立即手动关闭睡眠模式并触发晨间摘要
- `/snooze-status` — 显示睡眠模式是否激活、队列中消息的数量以及摘要发送的时间
- `/snooze-setup` — 交互式配置睡眠开始时间、唤醒时间和时区
- `/snooze-history` — 显示过去7天的摘要汇总

## 睡眠期间的行为规则

**在向用户发送任何消息之前（包括主动通知、摘要、心跳信息、每周总结、股票提醒、备份确认或其他自动化报告）——请先检查用户的睡眠状态：**

```bash
node ~/.openclaw/skills/sleep-snooze/scripts/status.js
```

如果 `isSleeping` 的值为 `true`，则不要发送消息，而是将其放入队列中（详见下文）。这适用于来自他人的消息以及您即将主动发送的消息。

### 睡眠期间收到的消息

当用户在睡眠期间收到消息或通知时：
1. **不要** 发送推送通知或立即回复。
2. 调用 `node ~/.openclaw/skills/sleep-snooze/scripts/queue-message.js` 并将消息内容存储到本地队列中。
3. 无声地确认收到消息——除非消息被标记为紧急（详见下文），否则在睡眠期间不要向发送者回复。

### 睡眠期间生成的出站消息

当您（或任何代理）准备发送主动消息（如状态更新、摘要、报告、心跳信息等）时，请使用 `gate.js` 而不是直接发送。`gate.js` 会自动检查用户的睡眠状态并进行排队：

```bash
node ~/.openclaw/skills/sleep-snooze/scripts/gate.js \
  --provider <provider> \
  --sender-id <agent-id> \
  --sender-name "<Agent Name>" \
  --message "<full message text>"
```

**返回代码：**
- **0** — 用户正在睡眠中，消息已放入队列——不发送
- **2** — 用户正在睡眠中但消息紧急——前缀加上 `🚨` 发送
- **3** — 用户已醒来——正常发送

所有出站消息都应使用 `gate.js` 处理。它会根据当前时间与时间表进行比较，因此即使睡眠模式的定时任务未运行，也能正常工作。

## 紧急规则

某些消息会绕过延迟机制，无论是否处于睡眠时间都会立即被发送。以下情况下的消息被视为紧急：
- 发送者位于用户的 VIP 联系人列表中（存储在 `~/.openclaw/skills/sleep-snooze/data/vip-contacts.json` 中）
- 消息包含以下关键词（不区分大小写）：`urgent`、`emergency`、`critical`、`911`、`help me`
- 消息由发送系统明确标记为紧急

对于紧急消息：正常发送，并在通知前加上 `🚨 [紧急 - 在睡眠期间收到]`。

## 晨间摘要

每天在 `WAKE_TIME` 时，系统会自动执行以下操作：
1. 调用 `node ~/.openclaw/skills/sleep-snooze/scripts/digest.js` 生成并发送摘要。
2. 摘要按发送者分组显示消息，并附上每个对话的简要总结。
3. 发送完成后，清空消息队列。

**摘要格式（每个发送者发送一条消息）：**

```
🌅 Good morning! Here's what arrived while you slept:

📬 3 messages from Alex
  • "Hey are you free tomorrow?"
  • "Also wanted to share this article..."
  • "Never mind, talk later!"

📬 1 message from GitHub Notifications
  • PR #42 was merged into main

📬 2 messages from Server Monitor Bot
  • CPU spike at 03:14 — resolved
  • Disk usage at 78% — check when available

Reply to any sender's name to respond to their messages.
```

## 设置说明

当用户首次运行 `/snooze-setup` 时：
1. 询问用户的睡眠开始时间（例如：“您通常什么时候睡觉？”）
2. 询问用户的唤醒时间（例如：“您通常什么时候起床？”）
3. 询问用户的时区（可以建议使用 `date +%Z` 自动检测）
4. 运行 `node ~/.openclaw/skills/sleep-snooze/scripts/sleep-init.js` 以保存配置并注册定时任务
5. 向用户确认设置：“睡眠延迟通知已设置：🌙 晚上10:00 → ☀️ 上午6:00（IST）。我会在夜间将通知放入队列，并在早上6:00发送摘要。”

## 状态管理

睡眠模式的状态存储在 `~/.openclaw/skills/sleep-snooze/data/state.json` 中：
```json
{
  "sleepStart": "22:00",
  "wakeTime": "06:00",
  "timezone": "Asia/Kolkata",
  "manualOverride": false,
  "isSleeping": false,
  "lastDigestAt": "2025-01-15T06:00:00.000Z"
}
```

消息队列存储在 `~/.openclaw/skills/sleep-snooze/data/queue.db` 的 SQLite 数据库中。

## 重要说明

- 睡眠延迟通知系统同时适用于所有连接的通信工具（Telegram、WhatsApp、Discord、Slack、Signal）。
- 如果用户在睡眠期间询问“我错过了什么？”之类的问题，请检查队列大小并回复：“您有 X 条消息已排队。我将在 [WAKE_TIME] 发送摘要。”
- 如果用户在睡眠期间主动发送消息，说明他们已经醒来——暂时暂停睡眠模式30分钟。
- 请勿丢弃任何消息。如果发送失败，将在下一个摘要周期重新尝试发送。