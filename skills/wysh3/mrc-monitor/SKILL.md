---
name: mrc-monitor
description: 实时监控MRC食堂订单系统的令牌状态。系统会持续检查Firebase Firestore中的令牌信息，并在订单准备好时发送通知。用户可以通过发送命令（如“mrc 73”、“token 97”或“monitor 42”）来监控一个或多个食堂令牌。系统能够同时处理多个令牌，为每个令牌分别发送通知，并在所有令牌都准备好后自动退出。
---

# MRC食堂监控器

监控MRC食堂的订单令牌，并在令牌准备好取餐时发出通知。

## 快速入门

当用户发送包含食堂令牌的任何命令时：

1. 从消息中提取所有令牌编号。
2. 启动后台监控脚本。
3. 立即回复确认信息。

## 命令识别

用户可以使用不同的前缀来发送令牌：
- "mrc 73" 或 "mrc 73 97 42"
- "token 73" 或 "token 73 97"
- "monitor 73"
- "check 73"（仅执行一次性检查）

## 启动监控器

从用户消息中提取所有编号并启动后台监控：

```bash
python3 skills/mrc-monitor/scripts/monitor.py <platform> <channel_id> <token1> <token2> ...
```

参数说明：
- `platform`："telegram" 或 "discord"（通信平台）
- `channel_id`：当前频道标识符（平台前缀可选，例如 "telegram_123" 或 "123" 都可以）
- `token1`、`token2` 等：需要监控的令牌编号

示例：
```bash
python3 skills/mrc-monitor/scripts/monitor.py telegram telegram_6046286675 73 97 42
# or
python3 skills/mrc-monitor/scripts/monitor.py telegram 6046286675 73 97 42
```

## 后台执行

将监控器作为后台进程运行，以便代理能够立即响应：

```python
import subprocess

# channel_id can be with or without platform prefix (both work)
cmd = ['python3', 'skills/mrc-monitor/scripts/monitor.py',
       platform, channel_id] + [str(t) for t in tokens]
subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
```

## 代理响应

启动监控器后，立即回复确认信息：

```
✅ Monitoring tokens: 73, 97, 42
Checking every 15 seconds.
I'll notify you here when they're ready! 🍕
```

## 一次性检查

对于 "check 73" 命令，仅执行一次Firebase查询并返回状态信息，无需启动后台监控。

## 监控器行为

监控脚本：
- 每15秒查询一次Firebase Firestore。
- 检查每次查询中的所有被监控令牌。
- 当令牌的状态变为 "Ready" 时，发送 "🍕 订单X已准备好！" 的通知。
- 从监控列表中移除已通知的令牌。
- 所有令牌都通知完毕后自动退出。
- 优雅地处理错误并尝试重试。
- 将所有活动记录到 `skills/mrc-monitor/logs/monitor_YYYYMMDD_HHMMSS.log` 文件中。

## 错误处理

脚本自动处理以下情况：
- 网络超时（最多重试5次）
- HTTP错误（包括速率限制）
- 意外错误（连续失败5次后停止）
- 信号终止（SIGTERM、SIGINT）

遇到致命错误时，脚本会在退出前发送通知。

## Firebase详细信息

- **项目**：kanteen-mrc-blr-24cfa
- **集合**：orders
- **文档字段**：
  - `studentId`（字符串）："student-{token_number}"
  - `status`（字符串）："Preparing"、"Ready"、"Completed"