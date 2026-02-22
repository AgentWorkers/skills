---
name: session-health-monitor
description: Claude Code会监控上下文窗口的状态（包括健康状况），并具备压缩检测功能。在压缩操作之前，系统会生成预压缩快照；同时，系统还支持内存旋转（memory rotation）机制，以确保应用程序的稳定运行。
allowed-tools:
  - Bash
  - Read
  - Write
version: 1.0.0
author: heinrichclawdster
---
# 会话健康监控器

监控您的 Claude Code 上下文窗口的健康状况，检测数据压缩情况，在数据丢失前保存关键信息，并保持内存目录的整洁。

## 概述

该工具具备四种独立运行的功能（无需依赖 OpenClaw）：

1. **状态栏显示**：在 Claude Code 的状态栏中以颜色编码的方式显示上下文窗口的使用情况。
2. **压缩检测**：通过跟踪使用量的变化来检测上下文数据是否被压缩。
3. **压缩前快照**：将关键信息和决策保存到每日内存文件中。
4. **内存轮换**：将旧的内存文件归档，以避免文件堆积。

## 快速设置

```bash
bash scripts/setup-statusline.sh
```

设置完成后，只需重启 Claude Code，状态栏就会显示相关信息。

对于快照和内存轮换功能，相应的脚本可以独立运行——您可以在代理循环中调用这些脚本，或者手动执行它们。

## 上下文健康阈值

| 状态等级 | 条件                                      | 操作                                      |
|--------|----------------------------------------|----------------------------------------|
| 绿色    | 使用率 < 50% 且无数据压缩                        | 正常运行                                      |
| 黄色    | 使用率 ≥ 50% 或数据压缩次数 ≥ 1                        | 考虑保存关键信息                         |
| 红色    | 使用率 ≥ 75% 或数据压缩次数 ≥ 2                        | 立即保存关键信息，并结束会话                        |

## 状态栏显示

状态栏会使用颜色编码来指示上下文窗口的使用情况：

```
42% Context | 0x compact     # GREEN — all good
63% Context | 1x compact     # YELLOW — getting warm
81% Context | 2x compact     # RED — save facts immediately
```

所使用的颜色遵循与 Claude Code 终端渲染兼容的 ANSI 规范。

## 压缩前快照机制

**当上下文使用率达到黄色或更高级别时，代理应执行以下操作：**

1. 从当前会话中提取 3-5 个关键信息（例如：做出的决策、更改的文件、遇到的问题等）。
2. 使用 `scripts/snapshot.sh` 脚本将这些信息写入 `memory/YYYY-MM-DD.md` 文件中。
3. 包括任何未完成的工作或下一步需要执行的操作。
4. 必须在会话结束或上下文数据被压缩之前完成这些操作。

**快照内容示例：**
```markdown
## Pre-Compaction Snapshot (14:32)
- Refactored auth module to use JWT instead of sessions (files: src/auth.ts, src/middleware.ts)
- Bug found in rate limiter: counter resets on deploy, not on TTL expiry
- Next: write tests for new auth flow, fix rate limiter reset logic
- Decision: using RS256 for JWT signing (user preference)
```

**触发条件：**
- 会话中首次出现使用率超过 50% 的情况。
- 检测到数据压缩时。
- 在结束长时间运行的会话之前。
- 代理检测到上下文数据量较大时。

## 脚本参考

### statusline.sh
从标准输入（stdin）读取 Claude Code 的状态栏 JSON 数据，并输出格式化后的上下文信息。

```bash
# Called automatically by Claude Code via settings.local.json
# Manual test:
echo '{"context_window":{"used_percentage":42},"session_id":"test-123"}' | bash scripts/statusline.sh
```

### setup-statusline.sh
一个用于安装状态栏功能的脚本，它会将状态栏脚本复制到 Claude Code 中并修改相关设置。

```bash
bash scripts/setup-statusline.sh
# Backs up settings.local.json before patching
# Requires: jq
```

### context-check.sh
一个独立的健康检查脚本，适用于心跳循环或持续集成（CI）流程。

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
将旧的内存文件归档。

```bash
bash scripts/rotate.sh           # Archives files older than 3 days (default)
KEEP_DAYS=7 bash scripts/rotate.sh  # Keep 7 days instead
```

## 消息提示

当上下文使用率达到黄色或更高级别时，代理应在发送的消息中添加提示信息：

```
---
63% Context Window | 1x compacted
```

这有助于用户了解会话运行时间过长，可能需要重新开始的情况。

## 配置

所有配置都通过环境变量进行设置，部分变量具有默认值：

| 变量                | 默认值                                      | 说明                                      |
|----------------------|--------------------------------------------------|----------------------------------------|
| `MEMORY_DIR`         | 自动检测（详见下文）                              | 日内存文件的保存路径                          |
| `KEEP_days`          | `3`                                      | 文件归档前的保留天数                          |
| `HEALTH_GREEN_MAX`   | `50`                                      | 绿色状态的最大使用率百分比                        |
| `HEALTH_RED_MIN`     | `75`                                      | 红色状态的最小使用率百分比                        |
| `COMPACTION_DROP`    | `30`                                      | 表示数据压缩的百分比阈值                        |

**内存目录的自动检测顺序：**
1. `$MEMORY_DIR` 环境变量。
2. `~/.openclaw/workspace/memory`（如果存在）。
3. `~/.claude/memory`（备用路径）。

## 故障排除

### jq 未安装
```bash
# macOS
brew install jq
# Linux
sudo apt-get install jq
```

### 状态栏未更新
1. 确保 `scripts/snapshot.sh` 脚本位于 `~/.claude/session-health-statusline.sh` 文件路径下。
2. 检查 `settings.local.json` 文件中是否包含 `statusLine` 键。
3. 重启 Claude Code。
4. 手动测试：`echo '{}' | bash ~/.claude/session-health-statusline.sh`。

### 重置压缩状态
```bash
rm /tmp/session-health-*.json
```

### 状态栏显示“Context Window”但无使用率百分比

首次运行时可能会出现这种情况——状态栏需要从 Claude Code 获取一个数据点才能显示使用率。下次更新时问题会得到解决。