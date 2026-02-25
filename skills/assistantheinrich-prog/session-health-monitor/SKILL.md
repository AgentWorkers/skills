---
name: session-health-monitor
description: OpenClaw代理的上下文窗口健康状况监控——通过Telegram发送阈值警告、生成预压缩快照以及实现内存轮换机制。
allowed-tools:
  - Bash
  - Read
  - Write
version: 1.1.0
author: heinrichclawdster
---
# 会话健康监控器

监控您的 OpenClaw 代理上下文窗口的健康状况，在使用率过高时通过 Telegram 发送警告，在数据压缩前保存关键信息，并保持内存目录的整洁。

## 概述

OpenClaw 代理会话具备以下四项功能：

1. **上下文使用率阈值警告** — 代理会在 Telegram 消息中添加使用率信息，并在可配置的阈值下发出警告。
2. **压缩检测** — 通过跟踪使用率的变化来推断上下文何时被压缩。
3. **压缩前快照** — 在关键信息和决策丢失之前，将其保存到每日内存文件中。
4. **内存轮换** — 归档旧的内存文件，以防止文件堆积。

## 快速设置（OpenClaw）

### 1. 添加共享技能引用

将以下内容添加到您的 `shared/INDEX.md` 文件中：

```markdown
| Context window health, compaction detection, pre-compaction snapshots | `skill-session-health.md` |
```

### 2. 创建共享技能文档

创建 `shared/skill-session-health.md` 文件：

```markdown
# Session Health Monitor

## Context Health Thresholds
| Level  | Condition                          | Action                        |
|--------|------------------------------------|-------------------------------|
| GREEN  | <50% used AND 0 compactions        | Normal operation              |
| YELLOW | >=50% used OR >=1 compaction       | Save key facts via snapshot   |
| RED    | >=75% used OR >=2 compactions      | Save facts NOW, session ending|

## Behavioral Rules
1. When context reaches YELLOW+, extract 3-5 key facts (decisions, files changed, blockers)
2. Run: `bash scripts/snapshot.sh "fact1" "fact2"`
3. Append footer to Telegram messages at YELLOW+: `X% Context Window | Nx compacted`
4. Do this BEFORE session ends or context gets compacted
5. After any detected compaction, immediately snapshot what you remember
```

### 3. 添加心跳检测步骤

将以下代码添加到代理的心跳循环中：

```markdown
**Context health check**: Run `session_status` → always append context % to Telegram messages
as footer: `📊 X% Context Window`. If Context >50% OR Compactions >=1, add:
"⚠️ consider /restart after current task." If Context >75% OR Compactions >=2, flag as urgent.
```

## 上下文健康阈值

| 状态        | 条件                                      | 操作                                      |
|------------|----------------------------------------|----------------------------------------|
| 绿色        | 使用率 < 50% 且未发生压缩                         | 正常运行                                      |
| 黄色        | 使用率 ≥ 50% 或发生 ≥ 1 次压缩                        | 考虑保存关键信息                         |
| 红色        | 使用率 ≥ 75% 或发生 ≥ 2 次压缩                        | 立即保存关键信息，结束会话                         |

## Telegram 消息尾部

代理会在每条发出的 Telegram 消息中添加一个尾部信息：

```
📊 42% Context Window                          # GREEN — no extra warning
📊 63% Context Window | 1x compacted           # YELLOW — consider restart
⚠️ 📊 81% Context Window | 2x compacted        # RED — urgent, save facts
```

这样用户无需手动检查，就能了解会话的健康状况。

## 压缩前快照协议

**当上下文使用率达到黄色或更高级别时，代理应执行以下操作：**

1. 从当前会话中提取 3-5 个关键信息（所做的决策、更改的文件、发现的障碍等）。
2. 使用 `scripts/snapshot.sh` 脚本将这些信息写入 `memory/YYYY-MM-DD.md` 文件中。
3. 包括任何未完成的工作或后续步骤。
4. 必须在会话结束或上下文被压缩之前完成这些操作。

**快照内容示例：**
```markdown
## Pre-Compaction Snapshot (14:32)
- Refactored auth module to use JWT instead of sessions (files: src/auth.ts, src/middleware.ts)
- Bug found in rate limiter: counter resets on deploy, not on TTL expiry
- Next: write tests for new auth flow, fix rate limiter reset logic
- Decision: using RS256 for JWT signing (user preference)
```

**触发条件：**
- 会话中首次使用率达到 50% 以上。
- 检测到压缩操作时。
- 结束长时间运行的会话时。
- 代理检测到上下文信息积累较多时。

## 脚本参考

### context-check.sh
独立的健康检查脚本，适用于心跳循环中。

```bash
bash scripts/context-check.sh                    # Human-readable output
bash scripts/context-check.sh --json              # Machine-readable JSON
echo '{"context_window":{"used_percentage":72}}' | bash scripts/context-check.sh
# Exit codes: 0=GREEN, 1=YELLOW, 2=RED
```

### snapshot.sh
将关键信息保存到每日内存文件中。

```bash
bash scripts/snapshot.sh "Fact one" "Fact two" "Fact three"
echo -e "Fact one\nFact two" | bash scripts/snapshot.sh -
```

### rotate.sh
归档旧的内存文件。

```bash
bash scripts/rotate.sh           # Archives files older than 3 days (default)
KEEP_DAYS=7 bash scripts/rotate.sh  # Keep 7 days instead
```

## 配置

所有配置均通过环境变量进行设置，部分参数具有默认值：

| 变量                | 默认值                                      | 说明                                      |
|------------------|--------------------------------------------------|----------------------------------------|
| `MEMORY_DIR`         | 自动检测（见下文）                              | 存储每日内存文件的目录                         |
| `KEEP_DAYS`          | `3`                                      | 归档前的保留天数                              |
| `HEALTH_GREEN_MAX`   | `50`                                      | 绿色状态的最低使用率阈值                         |
| `HEALTH_RED_MIN`     | `75`                                      | 红色状态的最低使用率阈值                         |
| `COMPACTION_DROP`    | `30`                                      | 表示压缩发生的使用率下降百分比                         |

**内存目录的自动检测顺序：**
1. `$MEMORY_DIR` 环境变量
2. `~/.openclaw/workspace/memory`（如果存在）
3. `~/.claude/memory`（备用路径）

## 故障排除

### jq 未安装
```bash
# macOS
brew install jq
# Linux
sudo apt-get install jq
```

### 重置压缩状态
```bash
rm /tmp/session-health-*.json
```

### 代理未添加尾部信息
1. 检查 `shared/INDEX.md` 中是否引用了 `skill-session-health.md`。
2. 确认心跳循环中包含了上下文健康检查步骤。
3. 验证代理是否能够使用 `session_status` 工具。