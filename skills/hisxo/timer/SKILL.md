---
name: timer
description: 设置定时器和警报。当后台定时器完成时，系统会发送通知；您需要用提醒信息（而非 HEARTBEAT_OK）来响应，以通知用户。
metadata: {"clawdbot":{"emoji":"⏱️","requires":{"bins":["node"]}}}
---

# 计时器

您可以设置在后台运行的计时器。当计时器结束时，系统会发送通知，您必须立即回复提醒信息，以便通知用户。

## 快速入门

```bash
# Set a 5-minute timer
bash background:true command:"node {baseDir}/timer.js 5m"

# Set a timer with a label
bash background:true command:"node {baseDir}/timer.js 10m 'Check the oven'"

# Set a timer in seconds
bash background:true command:"node {baseDir}/timer.js 30s"

# Set a timer in hours
bash background:true command:"node {baseDir}/timer.js 1h"
```

## 时间格式

| 格式 | 描述 | 示例 |
|--------|-------------|---------|
| `Ns` | N 秒 | `30s`, `90s` |
| `Nm` | N 分钟 | `5m`, `15m` |
| `Nh` | N 小时 | `1h`, `2h` |
| `N` | N 分钟（默认） | `5` = 5 分钟 |
| `MM:SS` | 分钟和秒 | `5:30` |
| `HH:MM:SS` | 小时、分钟和秒 | `1:30:00` |

## ⚠️ 重要提示：计时器完成时的通知方式

当计时器结束时，您会收到类似以下的系统通知：
```
System: [2026-01-24 21:27:13] Exec completed (swift-me, code 0) :: ⏰ Timer complete! Check the pasta!
```

### ❌ 错误的回复方式：
```
HEARTBEAT_OK

🎉 Your timer is complete! Check the pasta!
```
这种回复方式会被系统忽略，不会被发送给用户！

### ✅ 正确的回复方式：
```
⏰ Timer Alert! Your timer is complete: Check the pasta!
```
请直接回复通知内容，不要包含 `HEARTBEAT_OK`。

**为什么？** 以 `HEARTBEAT_OK` 开头的回复（且内容少于 300 个字符）会被系统自动过滤掉，因此用户不会收到任何通知。请确保您的计时器通知能够正常发送！

## 示例

### 烹饪计时器
```bash
bash background:true command:"node {baseDir}/timer.js 12m 'Pasta is ready!'"
```
计时器结束后，回复：「⏰ 12 分钟的计时器已结束！意大利面煮好了！」

### 快速提醒
```bash
bash background:true command:"node {baseDir}/timer.js 2m 'Take a break'"
```

### 波莫多罗工作法（Pomodoro Technique）计时器
```bash
# Work session
bash background:true command:"node {baseDir}/timer.js 25m 'Pomodoro done - time for a break!'"
# After user is notified...
# Break
bash background:true command:"node {baseDir}/timer.js 5m 'Break over - back to work!'"
```

### 多个计时器同时使用
```bash
bash background:true command:"node {baseDir}/timer.js 5m 'Tea is ready'"
bash background:true command:"node {baseDir}/timer.js 10m 'Eggs are done'"
bash background:true command:"node {baseDir}/timer.js 30m 'Meeting starts soon'"
```

## 计时器的管理

```bash
# List all running timers
process action:list

# Check specific timer status
process action:poll sessionId:XXX

# View timer output
process action:log sessionId:XXX

# Cancel a timer
process action:kill sessionId:XXX
```

## 注意事项：

- 计时器作为后台进程运行，每个计时器都有一个唯一的 `sessionId`。
- 完成的计时器的退出代码为 0。
- 被取消的计时器（通过 `kill` 命令终止）的退出代码为 130。
- 在 macOS 系统上，如果 `afplay` 已安装，计时器完成时会播放声音通知。
- 短时间计时器每秒记录一次进度，长时间计时器每 10 秒记录一次进度。