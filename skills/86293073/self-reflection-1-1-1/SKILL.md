---
name: self-reflection
description: 通过结构化的反思和总结，实现持续自我提升
version: 1.1.1
metadata: {"openclaw":{"emoji":"🪞","requires":{"bins":["jq","date"]}}}
---

# 🪞 自我反思

这是一种促进持续自我提升的技能。该工具通过定期触发的心跳检测机制，记录错误、经验教训以及随时间取得的进步。

## 快速入门

```bash
# Check if reflection is needed
self-reflection check

# Log a new reflection
self-reflection log "error-handling" "Forgot timeout on API call" "Always add timeout=30"

# Read recent lessons
self-reflection read

# View statistics
self-reflection stats
```

## 工作原理

```
Heartbeat (60m) → Agent reads HEARTBEAT.md → Runs self-reflection check
                                                      │
                                            ┌─────────┴─────────┐
                                            ▼                   ▼
                                           OK              ALERT
                                            │                   │
                                       Continue            Reflect
                                                               │
                                                     ┌─────────┴─────────┐
                                                     ▼                   ▼
                                                   read               log
                                              (past lessons)     (new insights)
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `check [--quiet]` | 检查是否需要进行自我反思（状态：OK 或 ALERT） |
| `log <tag> <miss> <fix>` | 记录新的反思内容 |
| `read [n]` | 读取最近 n 条反思记录（默认值：5） |
| `stats` | 显示反思记录的统计信息 |
| `reset` | 重置计时器 |

## 与 OpenClaw 的集成

在 `~/.openclaw/openclaw.json` 文件中启用心跳检测功能：

```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "60m",
        "activeHours": { "start": "08:00", "end": "22:00" }
      }
    }
  }
}
```

将 `HEARTBEAT.md` 文件添加到您的工作区中：

```markdown
## Self-Reflection Check (required)
Run `self-reflection check` at each heartbeat.
If ALERT: read past lessons, reflect, then log insights.
```

## 配置

创建 `~/.openclaw/self-reflection.json` 文件：

```json
{
  "threshold_minutes": 60,
  "memory_file": "~/workspace/memory/self-review.md",
  "state_file": "~/.openclaw/self-review-state.json",
  "max_entries_context": 5
}
```

## 作者

由 [hopyky](https://github.com/hopyky) 创建

## 许可证

MIT 许可证