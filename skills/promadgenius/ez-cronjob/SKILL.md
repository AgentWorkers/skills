---
name: ez-cronjob
description: 修复Clawdbot/Moltbot中常见的cron作业故障问题，包括消息传递问题、工具超时、时区错误以及模型回退问题。
author: Isaac Zarzuri
author-url: https://x.com/Yz7hmpm
version: 1.0.0
homepage: https://www.metacognitivo.com
repository: https://github.com/ProMadGenius/clawdbot-skills
metadata: {"agentskills":{"category":"troubleshooting","tags":["cron","scheduling","telegram","debugging","moltbot","clawdbot"]}}
---

# Cron 作业可靠性指南

本指南详细介绍了如何诊断和解决 Clawdbot/Moltbot 中的 Cron 作业问题。其中包含了通过实际生产环境调试过程中发现的常见故障模式及其解决方法。

## 适用场景

在以下情况下请参考本指南：
- 预定的消息未能送达
- Cron 作业显示“错误”状态
- 消息发送时间不正确（时区问题）
- 代理在使用 `cron` 工具时超时
- 备用模型无视指令并意外调用其他工具

## 快速参考

### 黄金法则

**为确保消息可靠送达，请务必同时使用以下参数：**

```bash
clawdbot cron add \
  --name "my-job" \
  --cron "0 9 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --message "[INSTRUCTION: DO NOT USE ANY TOOLS] Your prompt here" \
  --deliver --channel telegram --to "CHAT_ID" \
  --best-effort-deliver
```

### 参数说明

| 参数 | 作用 | 重要性说明 |
|------|---------|----------------|
| `--session isolated` | 创建独立会话 | 避免在繁忙的对话中丢失消息 |
| `--tz "TIMEZONE"` | 明确指定时区 | 避免时区设置导致的混乱 |
| `--deliver` | 将消息发送到指定频道 | 对于 Telegram/WhatsApp 是必需的 |
| `--best-effort-deliver` | 遇到发送错误时仍尝试发送 | 实现优雅的降级处理 |

---

## 问题 1：内部 `cron` 工具死锁

### 症状
- 代理在调用 `cron list` 或 `cron add` 时超时（通常超时时间为 10 秒）
- 显示错误信息：“工具执行超时”
- 网关日志显示响应时间超过 80 秒

### 原因
内部 `cron` 工具导致代理进程与网关之间出现死锁。

### 解决方案
**切勿直接使用 `cron` 工具**，应改用 `exec`（或 `bash`）命令：

```bash
# CORRECT - uses exec to bypass deadlock
exec: clawdbot cron list
exec: clawdbot cron add --name "reminder" --at "+5m" --message "Hello"

# INCORRECT - causes timeout
cron list        # DO NOT USE
cron add ...     # DO NOT USE
```

### 对于 AI 代理
如果当前是由 AI 代理执行此操作：当用户要求你管理 Cron 作业时，**务必使用 `exec/bash` 命令`clawdbot cron`来执行相关操作**，切勿直接调用 `cron` 工具。

---

## 问题 2：消息未送达

### 症状
- 作业状态显示为“已完成”，但消息始终未送达
- 在测试环境中可以正常工作，但在实际调度时却失败
- 消息发送存在间歇性错误

### 原因
使用 `--session main` 或 `--system-event` 会导致在主会话中有活跃对话时消息丢失。

### 解决方案
**始终使用 `--session isolated` 参数**：

```bash
# CORRECT - isolated session, guaranteed delivery
clawdbot cron add \
  --name "daily-standup" \
  --cron "0 9 * * 1-5" \
  --session isolated \
  --deliver --channel telegram --to "-100XXXXXXXXXX"

# INCORRECT - messages can be lost
clawdbot cron add \
  --name "daily-standup" \
  --session main \
  --system-event \
  ...
```

### 验证方法
创建作业后，请进行测试：

```bash
# Run the job immediately to verify delivery
clawdbot cron run <job-id>
```

---

## 问题 3：执行时间错误

### 症状
- 作业提前或延迟 4-5 小时执行
- 调度时间显示正确，但实际执行时间有误
- 有时能正常执行，有时会失败

### 原因
未明确指定时区，系统默认使用 UTC 时区。

### 解决方案
**务必明确指定时区**：

```bash
# CORRECT - explicit timezone
clawdbot cron add \
  --cron "0 9 * * 1-5" \
  --tz "America/New_York" \
  ...

# INCORRECT - defaults to UTC
clawdbot cron add \
  --cron "0 9 * * 1-5" \
  ...
```

### 常见时区代码

| 地区 | 时区代码 |
|--------|-------------|
| 美国东部 | `America/New_York` |
| 美国太平洋 | `America/Los_Angeles` |
| 英国 | `Europe/London` |
| 中欧 | `Europe/Berlin` |
| 印度 | `Asia/Kolkata` |
| 日本 | `Asia/Tokyo` |
| 澳大利亚东部 | `Australia/Sydney` |
| 巴西 | `America/Sao_Paulo` |
| 玻利维亚 | `America/La_Paz` |

---

## 问题 4：备用模型无视指令

### 症状
- 主模型工作正常
- 备用模型激活时，代理会意外调用其他工具
- 代理在不应使用某些工具时仍尝试使用 `exec`、`read` 等命令

### 原因
某些备用模型（尤其是那些处理速度较快的模型）对系统指令的遵守程度不如主模型严格。

### 解决方案
**将指令直接嵌入到消息中**：

```bash
# CORRECT - instruction embedded in message
clawdbot cron add \
  --message "[INSTRUCTION: DO NOT USE ANY TOOLS. Respond with text only.] 
  
  Generate a motivational Monday message for the team."

# INCORRECT - relies only on system prompt
clawdbot cron add \
  --message "Generate a motivational Monday message for the team."
```

### 强健的消息模板示例

```text
[INSTRUCTION: DO NOT USE ANY TOOLS. Write your response directly.]

Your actual prompt here. Be specific about what you want.
```

---

## 问题 5：作业一直处于错误状态

### 症状
- 作业状态显示为“错误”
- 随后的作业也会失败
- 没有明确的错误提示信息

### 诊断方法

```bash
# Check job details
clawdbot cron show <job-id>

# Check recent logs
tail -100 /tmp/clawdbot/clawdbot-$(date +%Y-%m-%d).log | grep -i cron

# Check gateway errors
tail -50 ~/.clawdbot/logs/gateway.err.log
```

### 常见问题及解决方法

| 问题原因 | 解决方案 |
|-------|-----|
| 模型使用量超出限制 | 等待使用量恢复或切换模型 |
| 聊天 ID 无效 | 使用 `--to` 参数验证聊天 ID 的正确性 |
| 机器人被移出群组 | 将机器人重新添加到 Telegram 群组 |
| 网关未运行 | 重启 `clawdbot gateway` |

### 最终解决方案
如果以上方法均无效：

```bash
# Remove the problematic job
clawdbot cron rm <job-id>

# Restart gateway
clawdbot gateway restart

# Recreate with correct flags
clawdbot cron add ... (with all recommended flags)
```

---

## 调试命令

### 查看所有作业
```bash
clawdbot cron list
```

### 检查特定作业
```bash
clawdbot cron show <job-id>
```

### 立即测试作业
```bash
clawdbot cron run <job-id>
```

### 查看日志
```bash
# Today's logs filtered for cron
tail -200 /tmp/clawdbot/clawdbot-$(date +%Y-%m-%d).log | grep -i cron

# Gateway errors
tail -100 ~/.clawdbot/logs/gateway.err.log

# Watch logs in real-time
tail -f /tmp/clawdbot/clawdbot-$(date +%Y-%m-%d).log | grep --line-buffered cron
```

### 重启网关
```bash
clawdbot gateway restart
```

---

## 完整示例

### 每日例会提醒（周一至周五上午 9 点）
```bash
clawdbot cron add \
  --name "daily-standup-9am" \
  --cron "0 9 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --message "[INSTRUCTION: DO NOT USE ANY TOOLS. Write directly.]

Good morning team! Time for our daily standup.

Please share:
1. What did you accomplish yesterday?
2. What are you working on today?
3. Any blockers?

@alice @bob" \
  --deliver --channel telegram --to "-100XXXXXXXXXX" \
  --best-effort-deliver
```

### 即时提醒（20 分钟后）
```bash
clawdbot cron add \
  --name "quick-reminder" \
  --at "+20m" \
  --delete-after-run \
  --session isolated \
  --message "[INSTRUCTION: DO NOT USE ANY TOOLS.]

Reminder: Your meeting starts in 10 minutes!" \
  --deliver --channel telegram --to "-100XXXXXXXXXX" \
  --best-effort-deliver
```

### 周报（周五下午 5 点）
```bash
clawdbot cron add \
  --name "weekly-report-friday" \
  --cron "0 17 * * 5" \
  --tz "America/New_York" \
  --session isolated \
  --message "[INSTRUCTION: DO NOT USE ANY TOOLS.]

Happy Friday! Time to wrap up the week.

Please share your weekly highlights and any items carrying over to next week." \
  --deliver --channel telegram --to "-100XXXXXXXXXX" \
  --best-effort-deliver
```

---

## 新创建 Cron 作业前的检查清单

在创建任何 Cron 作业之前，请确保：
- 使用 `exec: clawdbot cron add`（而非直接使用 `cron` 工具）
- 设置 `--session isolated` 参数
- 明确指定时区（例如：`--tz "YOUR_TIMEZONE"`）
- 使用 `--deliver --channel CHANNEL --to "ID"` 来指定消息发送目标
- 选择 `--best-effort-deliver` 以应对发送失败的情况
- 消息开头应包含 `[INSTRUCTION: DO NOT USE ANY TOOLS]` 的提示
- 创建作业后使用 `clawdbot cron run <id>` 进行测试

---

## 相关资源
- [Clawdbot Cron 文档](https://docs.molt.bot/tools/cron)
- [时区数据库](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
- [Cron 表达式生成器](https://crontab.guru/)

---

*本技能由 Isaac Zarzuri 编写，基于他在 Clawdbot/Moltbot 的实际生产环境调试经验整理而成。*