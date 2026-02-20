---
name: session-guard
description: "用于防止和恢复 OpenClaw 会话数据膨胀以及上下文丢失的问题。适用场景包括：  
(1) 诊断主会话上下文丢失或被截断的原因；  
(2) 设置独立的心跳检测/监控机制以避免会话数据污染；  
(3) 检测 OpenClaw 是否重启，并自动恢复会话上下文；  
(4) 审查内置的心跳检测机制是否导致会话文件膨胀；  
(5) 配置安全的压缩设置；  
(6) 处理与会话重置、上下文丢失、输出中断或心跳检测异常相关的问题。"
---
# 会话保护机制

该修复方案旨在解决 OpenClaw 中的架构问题：内置的“心跳”功能在主会话中运行，导致会话文件变得庞大、损坏，并引发会话重置，从而丢失所有代理上下文。

## 问题所在

OpenClaw 的内置“心跳”功能仅在主会话中执行。每次心跳操作都会被记录为对话历史，使得会话文件 `.jsonl` 的大小不断增大。如果连续两天以上每小时都执行一次心跳操作，文件大小可能会达到 10–15MB，导致文件头损坏并触发自动会话重置，从而无声地清除所有代理上下文。

**次要问题**：当心跳功能返回 `HEARTBEAT_OK` 时，OpenClaw 会忽略该值，但仍然会尝试向消息传递平台发送空字符串，从而导致 `sendMessage` 出错（错误提示为“消息内容为空”）。这个问题无法从代理端进行修复。

## 一次性安装（推荐）

通过一个命令自动应用所有保护措施：

```bash
python3 skills/session-guard/scripts/install.py
```

该命令会执行以下五个步骤：
1. **配置补丁**：禁用内置的心跳功能（配置为 `every: 0m`），并将压缩设置为 `default` 模式。
2. **独立的心跳任务**：设置每小时执行一次，从独立会话中读取 `HEARTBEAT.md` 文件。
3. **会话唤醒监控任务**：设置每 5 分钟执行一次，检测会话重置情况并触发数据恢复操作。
4. **会话大小监控任务**：设置每 15 分钟执行一次，如果会话大小超过 8MB 且会话处于空闲状态，则重启代理网关。
5. **初始化会话 ID**：存储当前的会话 ID，用于后续的唤醒检测。

**可选配置**：
```bash
python3 install.py --dry-run                        # preview all changes, no writes
python3 install.py --heartbeat-model anthropic-proxy-4/glm-4.7  # model for heartbeat cron
python3 install.py --monitor-model nvidia-nim/qwen/qwen2.5-7b-instruct  # model for monitors
python3 install.py --crit-mb 6                      # lower size threshold
python3 install.py --skip-crons                     # config patch only
python3 install.py --workspace /custom/path
```

该脚本会自动从 `~/.openclaw/openclaw.json` 文件中获取代理网关的 URL 和令牌信息。如果系统中已经存在相关的 Cron 任务，则会跳过这些任务（因为它们是重复执行的）。

---

## 快速审计

运行以下脚本可以检测存在的问题：

```bash
python3 skills/session-guard/scripts/audit.py
```

输出结果会列出配置中的问题（如心跳功能是否启用、压缩设置是否正确）以及会话文件的大小。

## 修复措施：禁用内置的心跳功能

如果审计结果显示 `heartbeat.every` 的值非零（即心跳功能处于启用状态），则需要对配置文件进行修改：

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

## 修复措施：创建独立的心跳任务

用一个独立的 Cron 任务来替代被禁用的内置心跳功能。该任务会从独立会话中读取 `HEARTBEAT.md` 文件，并通过 `message` 工具直接发送警报（独立会话的数据不会自动发送到消息通道）。

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

## 修复措施：会话唤醒检测

为了在 OpenClaw 重置会话时自动恢复上下文，需要执行以下操作：
**步骤 1**：设置会话唤醒监控任务（使用最便宜的模型，每 5 分钟执行一次）：

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

**步骤 2**：在 `HEARTBEAT.md` 文件中添加会话唤醒检测逻辑，以便每次心跳操作时都能检测到会话状态的变化：

```markdown
## Session Wake Detection (run first on every heartbeat)
1. bash memory/scripts/check_new_session.sh
2. If exit 1: hydrate context (read today's daily notes, search tiered memory), update ID
```

**步骤 3**：仅首次启动时初始化会话 ID：

```bash
# Get current session ID
ls -t ~/.openclaw/agents/main/sessions/*.jsonl | grep -v '\.reset\.' | head -1 | xargs basename | sed 's/\.jsonl//'
# Then store it:
python3 skills/session-guard/scripts/update_session_id.py <ID>
```

## 监控会话大小

检查当前会话文件的大小是否异常膨胀：

```bash
python3 skills/session-guard/scripts/audit.py --warn-mb 3
```

阈值设置：当文件大小达到 5MB 时发出警告，达到 10MB 时视为严重问题。在 `compaction: "default"` 的配置下，正常的活跃会话文件大小应保持在 2MB 以下。

## 数据恢复：会话重置后的上下文恢复

当检测到会话重置时，需要执行数据恢复操作来重新加载上下文：

```bash
python3 skills/session-guard/scripts/hydrate.py
```

该操作会加载并合并以下内容：
1. **每日记录**：从 `memory/YYYY-MM-DD.md` 文件中读取过去两天的数据。
2. **分层存储的数据**：通过树形搜索方式获取最重要的 3 个节点的相关信息。
3. **MEMORY.md**：读取长期存储的数据（前 2000 个字符）。

最终生成的输出是一个结构化的 Markdown 总结文件。用户可以阅读该文件，了解会话重置的情况以及已恢复的上下文。

**可选配置**：
```bash
python3 hydrate.py --days 3              # load 3 days of notes (default: 2)
python3 hydrate.py --memory-limit 5     # fetch 5 tiered memory results (default: 3)
python3 hydrate.py --workspace /path    # explicit workspace (default: auto-detect ~/clawd)
```

**完整的会话唤醒检测及数据恢复流程（用于会话唤醒监控任务）：**

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

| 脚本        | 功能                        |
|------------|---------------------------|
| `scripts/audit.py`   | 审查配置文件和会话文件的大小。参数：`--config`、`--sessions-dir`、`--warn-mb`、`--json` |
| `scripts/check_session.sh` | 检测会话 ID 是否发生变化。返回值：0 表示未变化，1 表示会话 ID 新增，2 表示检测到错误。参数：[state_file] [sessions_dir] |
| `scripts/update_session_id.py` | 存储新的会话 ID。参数：`<id>` [state_file] |
| `scripts/hydrate.py`   | 从每日记录、分层存储的数据和 `MEMORY.md` 文件中提取信息并生成总结。参数：`--days`、`--memory-limit`、`--workspace` |
| `scripts(size_watcher.py` | 监控会话大小；如果会话大小超过阈值或处于空闲状态，则重启代理网关。参数：`--warn-mb`、`--crit-mb`、`--idle-minutes`、`--dry-run` |
| `scripts/install.py` | 一次性安装所有保护措施。参数：`--dry-run`、`--skip-crons`、`--heartbeat-model`、`--monitor-model`、`--workspace` |

配置文件的默认路径为 `~/clawd/memory/heartbeat-state.json`（键值为 `lastSessionId`）。可以通过环境变量 `GUARD_STATE_FILE` 或脚本参数来修改该路径。

## 主动恢复会话大小（使用 `size_watcher.py`）

当会话文件的大小接近阈值时，该脚本会主动重启代理网关，以防止文件损坏：

```bash
python3 skills/session-guard/scripts/size_watcher.py
python3 skills/session-guard/scripts/size_watcher.py --crit-mb 8 --idle-minutes 5
python3 skills/session-guard/scripts/size_watcher.py --dry-run  # check only
```

**工作原理**：
1. 找到最近被修改的活跃会话文件（即当前的主会话文件）。
2. 如果文件大小小于 `--warn-mb`（默认值 5MB），则输出 “OK”。
3. 如果文件大小在警告阈值和临界阈值之间（默认值 8MB），则输出警告信息，不采取任何行动。
4. 如果文件大小达到临界阈值且会话已空闲超过 `--idle-minutes`（默认值 5 分钟），则重启代理网关。
5. 重启后，会话唤醒监控任务会检测到新的会话状态，并触发 `hydrate.py` 脚本来恢复上下文。

**空闲状态检查**：只有当会话文件在指定的 `--idle-minutes` 时间内没有被写入新内容时，才会执行重启操作，以避免在对话进行过程中中断。

**将该脚本设置为 Cron 任务（每 15 分钟执行一次，使用最便宜的模型）：**

```python
cron(action="add", job={
    "name": "Session Size Watcher",
    "schedule": {"kind": "every", "everyMs": 900000},
    "payload": {
        "kind": "agentTurn",
        "model": "nvidia-nim/qwen/qwen2.5-7b-instruct",
        "message": """Run: python3 skills/session-guard/scripts/size_watcher.py --crit-mb 8 --idle-minutes 5
If RESTARTED: send Telegram alert via message tool: '🔄 Session size limit hit — gateway restarted. Hydration will follow.'
If RESTART_FAILED: send Telegram alert: '⚠️ Session bloat critical but restart failed. Check session-guard.log.'
If OK/WARN/SKIPPED: reply DONE.""",
        "timeoutSeconds": 60
    },
    "sessionTarget": "isolated"
})
```

所有操作都会记录到 `~/clawd/memory/session-guard.log` 文件中，以便后续审计。

## OpenClaw 的已知问题（无法从代理端解决）：
1. `heartbeat.session` 配置仅支持 “main” 会话模式，不支持独立会话模式。
2. 当 `HEARTBEAT_OK` 被忽略时，会向消息传递平台发送空字符串，导致 `sendMessage` 出错。
3. 默认的 `compaction.mode: "safeguard"` 对于长时间运行的代理来说过于保守，可能导致数据丢失。