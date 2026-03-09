---
name: hzl
description: 用于代理协调的持久性任务账本。该系统能够规划多步骤的工作流程，在会话边界之间记录进度检查点，并通过项目池路由机制实现多个代理之间的协作。
metadata:
  { "openclaw": { "emoji": "🧾", "homepage": "https://github.com/tmchow/hzl", "requires": { "bins": ["hzl"] }, "install": [ { "id": "brew", "kind": "brew", "package": "hzl", "bins": ["hzl"], "label": "Install HZL (Homebrew)" }, { "id": "node", "kind": "node", "package": "hzl-cli", "bins": ["hzl"], "label": "Install HZL (npm)" } ] } }
---
# HZL：代理的持久任务账本

HZL（https://hzl-tasks.com）是一个以本地使用为主的任务账本，代理可以通过它来：

- 将多步骤的工作分解为项目和小任务；
- 设置检查点以保存工作进度，确保工作在会话结束后仍可继续；
- 通过项目池将工作分配给合适的代理；
- 在多个代理之间协调工作，处理任务分配和依赖关系。

本技能将指导代理如何使用 `hzl` 命令行工具（CLI）。

## 何时使用 HZL

**OpenClaw 没有内置的任务跟踪功能。** 与 Claude Code（具有 TodoWrite 功能）或 Codex（具有 update_plan 功能）不同，OpenClaw 依赖内存和 markdown 文件来跟踪工作进度。HZL 可以填补这一空白。

**适合使用 HZL 的场景：**
- 需要按顺序执行的多步骤项目；
- 可能会持续到会话结束之后的工作，或者需要多个代理共同完成的工作；
- 需要“从上次中断的地方继续执行”的工作；
- 需要将工作委托给其他代理，并在代理失败时能够恢复工作流程的情况。

**不适合使用 HZL 的场景：**
- 需要立即完成的简单单步任务；
- 基于时间的提醒（请使用 OpenClaw 的 Cron 功能）；
- 长篇笔记或知识记录（请使用内存文件）。

**经验法则：** 如果你需要制定多步骤的计划，或者担心无法在当前会话内完成任务，请使用 HZL。

---

## ⚠️ 破坏性命令 — 请先阅读说明

| 命令            | 功能                |
|------------------|----------------------|
| `hzl init --force`     | **删除所有数据。** 会提示用户确认。     |
| `hzl init --force --yes`     | **不提示确认即可删除所有数据。**     |
| `hzl task prune ... --yes`   | **永久删除** 已完成/归档的任务和历史记录。 |

**除非用户明确要求删除数据，否则切勿运行这些命令。删除操作不可撤销。**

---

## 核心概念

- **项目（Project）**：任务的容器。在单代理环境中，使用一个共享项目；在多代理环境中，为每个代理角色使用一个项目（用于任务分配）。
- **任务（Task）**：最高级别的工作单元。对于多步骤的任务，可以使用父任务来管理。
- **子任务（Subtask）**：任务的细分部分（使用 `--parent <id>`）。最多支持一级嵌套。`hzl task claim --next` 命令不会返回父任务。
- **检查点（Checkpoint）**：用于在会话中断后恢复进度的快照。
- **租约（Lease）**：一种有限期的任务分配机制，有助于在多代理环境中检测任务卡顿情况。

---

## 项目设置

### 单代理环境

使用一个共享项目。所有请求和任务都会成为该项目的父任务。

```bash
hzl project list                    # Check first — only create if missing
hzl project create openclaw
```

所有操作都通过 `openclaw` 进行。`hzl task claim --next -P openclaw` 命令始终有效。

### 多代理环境（任务池分配）

为每个代理角色使用一个项目。分配给某个项目的任务可以被该池中的任何代理领取。当一个角色可能需要扩展到多个代理时，这种模式是合适的。

```bash
hzl project create research
hzl project create writing
hzl project create coding
hzl project create marketing
hzl project create coordination    # for cross-agent work
```

**任务池分配规则：** 任务分配时不需要指定 `--agent` 参数；任何符合条件的代理都可以使用 `--next` 命令领取任务。

```bash
# Assigning work to the research pool (no --agent)
hzl task add "Research competitor pricing" -P research -s ready

# Kenji (or any researcher) claims it
hzl task claim --next -P research --agent kenji
```

**代理任务分配：** 如果在创建任务时指定了 `--agent` 参数，只有指定的代理（或没有任务的代理）才能使用 `--next` 命令领取任务；没有代理分配的任务对所有代理都可见。

```bash
# Pre-route a task to a specific agent
hzl task add "Review Clara's PR" -P coding -s ready --agent kenji

# Kenji claims it (matches agent)
hzl task claim --next -P coding --agent kenji   # ✓ returns it

# Ada tries — skipped because it's assigned to kenji
hzl task claim --next -P coding --agent ada     # ✗ skips it
```

当需要将任务分配给特定代理时，在创建任务时使用 `--agent` 参数；如果任务可以由池中的任何代理领取，则省略该参数。

---

## 会话开始（主要工作流程）

### 使用工作流命令（HZL v2+）

```bash
hzl workflow run start --agent <agent-id> --project <project> --json
```

必须指定 `--project` 参数，代理需要根据自己被分配到的任务池来执行任务。可以使用 `--any-project` 来扫描所有项目（例如协调代理）。

这个命令可以同时处理租约过期后的任务恢复和新任务的领取。如果返回了任务，则开始执行；如果没有返回任务，则表示任务队列为空。此时会应用代理任务分配规则：分配给其他代理的任务将被跳过。

### 不使用工作流命令（备用方案）

```bash
hzl agent status                           # Who's active? What's running?
hzl task list -P <project> --available     # What's ready?
hzl task stuck                             # Any expired leases?
hzl task stuck --stale                     # Also check for stale tasks (no checkpoints)

# If stuck tasks exist, read their state before claiming
hzl task show <stuck-id> --view standard --json
hzl task steal <stuck-id> --if-expired --agent <agent-id> --lease 30
hzl task show <stuck-id> --view standard --json | jq '.checkpoints[-1]'

# Otherwise claim next available
hzl task claim --next -P <project> --agent <agent-id>
```

---

## 核心工作流程

### 添加任务

```bash
hzl task add "Feature X" -P openclaw -s ready              # Single-agent
hzl task add "Research topic Y" -P research -s ready        # Pool-routed (multi-agent)
hzl task add "Subtask A" --parent <id>                      # Subtask
hzl task add "Subtask B" --parent <id> --depends-on <a-id>  # With dependency
```

### 执行任务

```bash
hzl task claim <id>                          # Claim specific task
hzl task claim --next -P <project>           # Claim next available
hzl task checkpoint <id> "milestone X"       # Checkpoint progress
hzl task complete <id>                       # Finish
```

### 状态转换

```bash
hzl task set-status <id> ready               # Make claimable
hzl task set-status <id> backlog             # Move back to planning
hzl task block <id> --comment "reason"       # Block with reason
hzl task unblock <id>                        # Unblock
```

任务状态：`backlog` → `ready` → `in_progress` → `done`（或 `blocked`）

### 完成子任务

```bash
hzl task complete <subtask-id>
hzl task show <parent-id> --view summary --json   # Any subtasks remaining?
hzl task complete <parent-id>               # Complete parent if all done
```

---

## 委派和交接任务

### 使用工作流命令（HZL v2+）

```bash
# Hand off to another agent or pool — complete current, create follow-on atomically
hzl workflow run handoff \
  --from <task-id> \
  --title "<new task title>" \
  --project <pool>              # --agent if specific person; --project for pool

# Delegate a subtask — creates dependency edge by default
hzl workflow run delegate \
  --from <task-id> \
  --title "<delegated task>" \
  --project <pool> \
  --pause-parent                # Block parent until delegated task is done
```

在交接任务时，必须指定 `--agent` 和 `--project` 参数。省略 `--agent` 会导致任务被分配到任务池；此时需要指定 `--project` 来指定任务池。

### 手动委托任务（备用方案）

```bash
hzl task add "<delegated title>" -P <pool> -s ready --depends-on <parent-id>
hzl task checkpoint <parent-id> "Delegated X to <pool> pool. Waiting on <task-id>."
hzl task block <parent-id> --comment "Waiting for <delegated-task-id>"
```

---

## 任务依赖关系

```bash
# Add dependency at creation
hzl task add "<title>" -P <project> --depends-on <other-id>

# Add dependency after creation
hzl task add-dep <task-id> <depends-on-id>

# Query dependencies
hzl dep list --agent <id> --blocking-only          # What's blocking me?
hzl dep list --from-agent <id> --blocking-only     # What's blocking work I created?
hzl dep list --project <p> --blocking-only         # What's blocking in a pool?
hzl dep list --cross-project-only                  # Cross-agent blockers

# Validate no cycles
hzl validate
```

HZL 默认支持跨项目依赖关系。可以使用 `hzl dep list --cross-project-only` 命令来查看跨项目的依赖关系。

---

## 设置检查点

在重要的里程碑或暂停操作之前设置检查点。一个好的检查点应该能够回答：“如果当前会话中断，其他代理能否从这里继续执行任务？”

**何时设置检查点：**
- 在执行可能失败的任何操作之前；
- 在创建子代理之前；
- 在完成有意义的工作单元之前；
- 在交接任务或暂停之前。

```bash
hzl task checkpoint <id> "Implemented login flow. Next: add token refresh." --progress 50
hzl task checkpoint <id> "Token refresh done. Testing complete." --progress 100
hzl task progress <id> 75          # Set progress without a checkpoint
```

---

## 生命周期钩子

HZL 会在任务状态发生重要变化时发送通知——目前仅支持 `on_done` 事件。其他生命周期事件（如任务卡顿、阻塞或进度变化）需要通过轮询来获取。这是有意设计的：只有当发生重要事件时，系统才会发送通知；其他情况则由代理和协调者手动轮询。

钩子的配置在安装过程中完成（详情请参阅文档）。作为代理，你需要了解以下操作细节：
- **只有 `on_done` 事件会触发通知。** 当任务完成时，HZL 会触发 Webhook。对于任务卡顿、状态过期或进度变化等情况，需要使用 `hzl task stuck --stale` 或 `hzl task list` 命令进行轮询。
- **通知不会立即发送。** `hzl hook drain` 命令会按照预设的 Cron 计划（通常每 2–5 分钟执行一次）来发送通知。你的任务完成信息会立即被记录，但通知会在下一次轮询时才发送到指定的网关。
- **通知中包含上下文信息。** 每条通知都会包含代理信息、项目信息和完整的事件详情。网关会负责根据代理进行消息路由——无论哪个代理完成了任务，通知都会发送到相同的地址。
- **如果通知发送失败，请使用 `hzl hook drain --json` 命令查看失败原因和错误详情。**

---

## 多代理环境下的任务协调（使用租约）

```bash
# Claim with lease (prevents orphaned work)
hzl task claim <id> --agent <agent-id> --lease 30       # 30-minute lease

# Fleet status: who's active, what they're working on, how long
hzl agent status                                        # All agents
hzl agent status --agent <name>                         # Single agent
hzl agent status --stats                                # Include task count breakdowns

# Agent activity history
hzl agent log <agent>                                   # Recent events for an agent

# Monitor for stuck tasks
hzl task stuck

# Monitor for stuck AND stale tasks (no checkpoints for 10+ min)
hzl task stuck --stale
hzl task stuck --stale --stale-threshold 15               # Custom threshold

# Recover an abandoned task (steal + set new lease atomically)
hzl task show <stuck-id> --view standard --json         # Read last checkpoint first
hzl task steal <stuck-id> --if-expired --agent <agent-id> --lease 30
```

为每个代理指定唯一的 `--agent` 参数（例如 `henry`、`clara`、`kenji`），以便追踪任务的负责人。

---

## 任务和项目的规模设定

**任务完成度的判断标准：** “我完成了 [任务]” 应该描述一个具体的完成结果。
- ✓ “安装了车库运动传感器”（具体且可验证的任务）
- ✗ “完成了家庭自动化系统”（描述模糊，无法验证）

**何时将任务拆分为多个小任务：** 当任务的各个部分能够独立完成或解决不同的问题时。

**提供更多上下文信息：**
```bash
hzl task add "Install sensors" -P openclaw \
  -d "Mount at 7ft height per spec." \
  -l docs/sensor-spec.md,https://example.com/wiring-guide
```

不要在描述中重复任务的具体细节，建议参考官方文档以避免信息不一致。

---

## 扩展参考资料

```bash
# Setup
hzl init                                      # Initialize (safe, won't overwrite)
hzl status                                    # Database mode, paths, sync state
hzl doctor                                    # Health check

# List and find
hzl task list -P <project> --available        # Ready tasks with met dependencies
hzl task list --parent <id>                   # Subtasks of a parent
hzl task list --root                          # Top-level tasks only
hzl task list -P <project> --tags <csv>       # Filter by tags

# Create with options
hzl task add "<title>" -P <project> --priority 2 --tags backend,auth
hzl task add "<title>" -P <project> -s in_progress --agent <name>
hzl task add "<title>" -P <project> --stale-after 2h
hzl task update <id> --stale-after 30m
hzl task update <id> --clear-stale-after

# Agent fleet status
hzl agent status                              # Active/idle agents, current tasks, lease state
hzl agent status --agent <name>               # Single agent
hzl agent status --stats                      # With task count breakdowns
hzl agent log <agent>                         # Activity history for an agent

# Web dashboard
hzl serve                                     # Start on port 3456
hzl serve --host 127.0.0.1                    # Restrict to localhost
hzl serve --background                        # Fork to background
hzl serve --status / --stop

# Raw reporting surfaces
hzl events                                    # NDJSON event feed
hzl events --follow
hzl events --from 0 > events.jsonl
hzl stats --window 1h

# Authorship
hzl task claim <id> --agent alice
hzl task checkpoint <id> "note" --author bob  # Records who did the action
hzl task claim <id> --agent "Claude" --agent-id "session-abc123"

# Cloud sync (optional)
hzl init --sync-url libsql://<db>.turso.io --auth-token <token>
hzl sync
```

---

## Web 控制面板（始终开启，适用于 Linux）

```bash
hzl serve --print-systemd > ~/.config/systemd/user/hzl-web.service
systemctl --user daemon-reload
systemctl --user enable --now hzl-web
loginctl enable-linger $USER
```

可以通过 `http://<your-box>:3456` 访问（可通过 Tailscale 进行访问）。在 macOS 上，可以使用 `hzl serve --background` 命令启动控制面板。

---

## HZL 的局限性

- **不提供任务编排功能** — 不会自动创建代理或分配任务；
- **不自动分解任务** — 不会自动将任务拆分为更小的部分；
- **不支持智能调度** — 仅使用简单的优先级和 FIFO 排序规则。

这些功能属于任务编排层的职责范围，而非 HZL 的核心功能。

---

## 其他注意事项

- 请通过 `exec` 工具来运行 `hzl` 命令。
- 请查阅 `TOOLS.md` 文件，了解你的身份信息、需要监控的项目以及与你的角色相关的命令。
- 为每个代理指定唯一的 `--agent` 参数，并使用租约机制来避免数据库中的冲突。
- `hzl workflow run` 命令需要 HZL v2.0 或更高版本；如果该版本不可用，请使用上述的手动备用方案。