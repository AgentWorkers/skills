---
name: session-guard
description: "用于防止和恢复 OpenClaw 会话文件膨胀以及会话上下文丢失的问题。适用场景包括：  
(1) 诊断主会话上下文丢失或被截断的原因；  
(2) 设置隔离式心跳检测/监控机制以避免会话数据污染；  
(3) 检测 OpenClaw 是否重启，并自动恢复会话上下文；  
(4) 审查内置心跳检测机制是否导致会话文件膨胀；  
(5) 配置安全的压缩设置；  
(6) 处理与会话重置、上下文丢失、输出中断或心跳检测数据污染相关的问题。"
---
# 会话保护机制

本修复方案针对 OpenClaw 的设计缺陷进行了改进，该缺陷导致会话文件变得庞大、损坏，并引发会话重置，从而丢失所有代理上下文信息。

## 问题所在

OpenClaw 内置的 `heartbeat` 功能仅在主会话中运行。每次心跳请求都会被记录为会话历史数据，导致 `.jsonl` 文件持续膨胀。如果心跳请求每小时发生一次且持续超过两天，文件大小会迅速增长至 10–15MB，进而损坏文件头信息并触发自动会话重置，导致所有代理上下文信息被清除。

**次要问题**：当 `heartbeat` 返回 `HEARTBEAT_OK` 信号时，OpenClaw 会忽略该信号，但仍会尝试向消息传递平台发送空字符串，从而导致 `sendMessage` 出错（错误提示为“消息内容为空”）。这个问题无法从代理端进行修复。

## 快速检查

运行以下脚本以检测相关问题：

```bash
python3 skills/session-guard/scripts/audit.py
```

该脚本会列出配置中的问题（如心跳功能是否启用、会话压缩设置等）以及会话文件的大小。

## 修复方案：禁用内置的心跳功能

如果检查发现 `heartbeat.every` 的值非零（即心跳功能处于启用状态），请对配置文件进行修改：

```python
# Via gateway tool:
gateway(action="config.patch", raw=json.dumps({
    "agents": {
        "defaults": {
            "heartbeat": {"every": "0m"},
            "compaction": {"mode": "default"}
        }
    }
}), note="Disabled main-session heartbeat to prevent bloat")
```

## 修复方案：创建独立的 heartbeat 定时任务

用一个独立的定时任务来替代被禁用的内置心跳功能。该定时任务会读取 `HEARTBEAT.md` 文件，并通过 `message` 工具直接发送 Telegram 警报（独立会话数据不会自动发送到指定频道）。

```python
cron(action="add", job={
    "name": "Isolated Heartbeat",
    "schedule": {"kind": "every", "everyMs": 3600000},  # 1h
    "payload": {
        "kind": "agentTurn",
        "model": "anthropic-proxy-4/glm-4.7",  # cheap model
        "message": "Read HEARTBEAT.md and follow it. Send Telegram alerts via message tool for anything urgent. Do NOT reply HEARTBEAT_OK — isolated sessions must use message tool to notify.",
        "timeoutSeconds": 120
    },
    "sessionTarget": "isolated"
})
```

## 修复方案：检测会话重置事件

为了在会话重置时自动恢复上下文信息，需要执行以下步骤：

**步骤 1**：设置一个定时任务来监控会话状态（在成本最低的服务器模型上每 5 分钟执行一次）：

```python
cron(action="add", job={
    "name": "Session Wake Monitor",
    "schedule": {"kind": "every", "everyMs": 300000},  # 5min
    "payload": {
        "kind": "agentTurn",
        "model": "nvidia-nim/qwen/qwen2.5-7b-instruct",
        "message": """Check if main session has reset:
1. Run: bash skills/session-guard/scripts/check_session.sh
   Output: CURRENT_ID|STORED_ID. Exit 0=same, 1=new, 2=error.
2. If exit 1 (new session):
   a. Update ID: python3 skills/session-guard/scripts/update_session_id.py <CURRENT_ID>
   b. Notify main session via sessions_send to trigger hydration.
3. If exit 0: do nothing, reply DONE.""",
        "timeoutSeconds": 60
    },
    "sessionTarget": "isolated"
})
```

**步骤 2**：在 `HEARTBEAT.md` 文件中添加会话重置检测逻辑，以便每次心跳请求时都能检查会话状态：

```markdown
## Session Wake Detection (run first on every heartbeat)
1. bash memory/scripts/check_new_session.sh
2. If exit 1: hydrate context (read today's daily notes, search tiered memory), update ID
```

**步骤 3**：仅在首次启动时初始化会话 ID：

```bash
# Get current session ID
ls -t ~/.openclaw/agents/main/sessions/*.jsonl | grep -v '\.reset\.' | head -1 | xargs basename | sed 's/\.jsonl//'
# Then store it:
python3 skills/session-guard/scripts/update_session_id.py <ID>
```

## 监控会话文件大小

定期检查会话文件的大小：

```bash
python3 skills/session-guard/scripts/audit.py --warn-mb 3
```

阈值设置：5MB 时发出警告，10MB 时视为严重问题。在默认的压缩设置（`compaction: "default"`）下，正常运行的会话文件大小应保持在 2MB 以下。

## 恢复会话上下文

当检测到会话重置时，需要执行以下操作来恢复上下文信息：

```bash
python3 skills/session-guard/scripts/hydrate.py
```

具体操作包括加载并合并以下内容：
1. **每日记录**：来自 `memory/YYYY-MM-DD.md` 的过去两天内的数据
2. **重要节点信息**：通过树形搜索获取前三个关键节点的数据
3. **MEMORY.md**：长期存储的数据中的前 2000 个字符

最终生成的文件是一个结构化的 Markdown 总结，其中包含了关键上下文信息。用户可以阅读该文件，了解会话重置的情况以及已恢复的上下文内容。

**可选配置**：
```bash
python3 hydrate.py --days 3              # load 3 days of notes (default: 2)
python3 hydrate.py --memory-limit 5     # fetch 5 tiered memory results (default: 3)
python3 hydrate.py --workspace /path    # explicit workspace (default: auto-detect ~/clawd)
```

**完整的会话监控与恢复流程（用于会话状态监控定时任务）：**

```
1. bash skills/session-guard/scripts/check_session.sh
   → exit 0: same session, skip
   → exit 1: NEW SESSION — proceed with hydration

2. python3 skills/session-guard/scripts/hydrate.py > /tmp/hydration.txt
   cat /tmp/hydration.txt  # read and synthesize

3. python3 skills/session-guard/scripts/update_session_id.py <CURRENT_ID>

4. Notify user (via message tool in isolated sessions):
   "🔄 Session reset detected — context reloaded. [brief summary of key projects/state]"
```

## 脚本说明

| 脚本        | 功能                |
|------------|-------------------|
| `scripts/audit.py` | 检查配置文件及会话文件大小。参数：`--config`、`--sessions-dir`、`--warn-mb`、`--json` |
| `scripts/check_session.sh` | 检测会话 ID 是否发生变化。返回值：0 表示未变化，1 表示会话 ID 更新，2 表示检测到错误。参数：[state_file] [sessions_dir] |
| `scripts/update_session_id.py` | 保存新的会话 ID。参数：`<id>` [state_file] |
| `scripts/hydrate.py` | 从 `memory/YYYY-MM-DD.md`、分层存储的数据以及 `MEMORY.md` 中加载最新信息并生成总结报告。参数：`--days`、`--memory-limit`、`--workspace` |

**状态文件默认路径**：`~/clawd/memory/heartbeat-state.json`（键值为 `lastSessionId`）。可以通过环境变量 `GUARD_STATE_FILE` 或脚本参数进行自定义。

## OpenClaw 的已知缺陷（无法从代理端修复）：

1. `heartbeat.session` 配置仅支持 “main” 会话模式，不支持独立会话模式
2. 当 `HEARTBEAT_OK` 信号被忽略时，会向消息传递平台发送空字符串，导致 `sendMessage` 出错
3. 默认的压缩设置 `compaction.mode: "safeguard"` 对于长时间运行的代理来说过于保守，可能导致文件过大