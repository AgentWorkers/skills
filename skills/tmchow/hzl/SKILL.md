---
name: hzl
description: 用于代理协调的持久性任务账本。该系统能够规划多步骤的工作流程，在会话边界之间记录进度检查点，并通过项目池路由机制实现多个代理之间的协同工作。
metadata:
  { "openclaw": { "emoji": "🧾", "homepage": "https://github.com/tmchow/hzl", "requires": { "bins": ["hzl"] }, "install": [ { "id": "brew", "kind": "brew", "package": "hzl", "bins": ["hzl"], "label": "Install HZL (Homebrew)" }, { "id": "node", "kind": "node", "package": "hzl-cli", "bins": ["hzl"], "label": "Install HZL (npm)" } ] } }
---
# HZL：代理的持久性任务管理工具

HZL（https://hzl-tasks.com）是一个以本地使用为主的任务管理工具，代理可以通过它来：

- 将多步骤的工作分解为项目及任务；
- 设置检查点以保存工作进度，确保工作在会话结束时不会丢失；
- 通过项目池将任务分配给合适的代理；
- 在多个代理之间协调工作，处理任务的租用和依赖关系。

本技能将指导代理如何使用 `hzl` 命令行工具（CLI）。

## 何时使用 HZL

**OpenClaw 没有内置的任务跟踪功能。** 与 Claude Code（具有 TodoWrite 功能）或 Codex（具有 update_plan 功能）不同，OpenClaw 依赖内存和 markdown 文件来跟踪工作进度。HZL 可以填补这一空白。

**适合使用 HZL 的场景：**
- 需要按顺序执行的多步骤项目；
- 可能会持续到会话结束之后的工作，或者需要涉及多个代理的工作；
- 需要“从上次停止的地方继续执行”的工作；
- 需要将工作委托给其他代理，并在代理失败时能够恢复工作的情况。

**不适合使用 HZL 的场景：**
- 非常简单、可以立即完成的单步任务；
- 基于时间的提醒（请使用 OpenClaw 的 Cron 功能）；
- 长篇笔记或知识记录（请使用内存文件）。

**经验法则：** 如果你需要制定多步骤的计划，或者担心无法在当前会话内完成任务，请使用 HZL。

---

## ⚠️ 危险命令 — 请先阅读说明

| 命令 | 功能 |
|---------|--------|
| `hzl init --force` | **删除所有数据。** 会提示用户确认。 |
| `hzl init --force --yes` | **不经过确认就删除所有数据。** |
| `hzl task prune ... --yes` | **永久删除** 已完成/归档的任务和历史记录。 |

**除非用户明确要求删除数据，否则切勿运行这些命令。这些操作无法撤销。**

---

## 核心概念

- **项目（Project）**：任务的容器。在单代理环境中，使用一个共享项目；在多代理环境中，为每个代理角色使用一个项目（用于任务分配）。  
- **任务（Task）**：最高级别的工作单元。对于多步骤的任务，可以使用父任务来管理。  
- **子任务（Subtask）**：任务的细分部分（使用 `--parent <id>` 标记）。最多支持一级嵌套。`hzl task claim --next` 命令不会返回父任务。  
- **检查点（Checkpoint）**：用于会话恢复的进度快照。  
- **租用（Lease）**：一种有限时间的任务分配机制，有助于在多代理环境中检测任务是否卡住。  

---

## 项目设置

### 单代理环境

使用一个共享项目。所有请求和任务都会成为该项目的父任务。

```bash
hzl project list                    # Check first — only create if missing
hzl project create openclaw
```

所有操作都通过 `openclaw` 完成。`hzl task claim --next -P openclaw` 命令始终有效。

### 多代理环境（任务池分配）

为每个代理角色使用一个项目。分配给某个项目的任务可以被任何监控该项目的代理领取。当一个角色可能需要扩展到多个代理时，这种模式是合适的。

```bash
hzl project create research
hzl project create writing
hzl project create coding
hzl project create marketing
hzl project create coordination    # for cross-agent work
```

**任务池分配规则：** 在分配任务时不需要指定 `--agent` 参数；任何符合条件的代理都可以使用 `--next` 命令领取任务。

```bash
# Assigning work to the research pool (no --agent)
hzl task add "Research competitor pricing" -P research -s ready

# Kenji (or any researcher) claims it
hzl task claim --next -P research --agent kenji
```

只有当你希望特定代理执行任务时，才需要指定 `--agent` 参数；如果任何代理都可以执行任务，则使用 `--project` 参数。

---

## 会话开始（主要工作流程）

### 使用工作流命令（HZL v2+）

```bash
hzl workflow run start --agent <agent-id> --project <project> --json
```

这个命令可以同时处理租用期限到期的任务恢复和新任务的领取。如果返回了任务，就继续执行该任务；如果没有返回任务，说明队列为空。

### 不使用工作流命令（备用方案）

```bash
hzl task list -P <project> --available     # What's ready?
hzl task stuck                             # Any expired leases?

# If stuck tasks exist, read their state before claiming
hzl task show <stuck-id> --view standard --json
hzl task steal <stuck-id> --if-expired --agent <agent-id>
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

### 任务状态转换

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

## 委托和交接任务

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

在交接任务时，必须指定 `--agent` 和 `--project` 参数。省略 `--agent` 会导致任务被分配到任务池；此时需要 `--project` 来指定具体的代理。  

### 手动委托（备用方案）

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

HZL 默认支持跨项目依赖关系。使用 `hzl dep list --cross-project-only` 命令来查看跨项目的依赖关系。

---

## 设置检查点

在重要的里程碑或暂停之前设置检查点。一个好的检查点应该能够回答：“如果当前会话突然结束，其他代理能否从这里继续执行？”

**何时设置检查点：**
- 在执行可能失败的任何操作之前；
- 在创建子代理之前；
- 在完成有意义的工作单元之后；
- 在交接或暂停任务之前。

```bash
hzl task checkpoint <id> "Implemented login flow. Next: add token refresh." --progress 50
hzl task checkpoint <id> "Token refresh done. Testing complete." --progress 100
hzl task progress <id> 75          # Set progress without a checkpoint
```

---

## 回调处理

当任务状态变为 `done` 时，HZL 会将该任务的回调信息放入队列中。`drain` 命令用于处理这些回调。

```bash
hzl hook drain                     # Deliver all queued callbacks (run on a schedule)
hzl hook drain --dry-run           # Preview what would be delivered
```

配置信息位于 `~/.config/hzl/config.json` 文件中（如果文件不存在，请创建）：

```json
{
  "hooks": {
    "on_done": {
      "url": "<OPENCLAW_GATEWAY_URL>/events/inject",
      "headers": {
        "Authorization": "Bearer <YOUR_GATEWAY_TOKEN>"
      }
    }
  }
}
```

HZL 使用主机进程模型，没有内置的守护进程。在 OpenClaw 中，可以每 2 分钟运行一次 `hzl hook drain` 作为定时任务。如果没有调度器，回调信息会堆积在队列中但不会被执行。

---

## 多代理环境下的任务协调（使用租用机制）

```bash
# Claim with lease (prevents orphaned work)
hzl task claim <id> --agent <agent-id> --lease 30       # 30-minute lease

# Monitor for stuck tasks
hzl task stuck

# Recover an abandoned task
hzl task show <stuck-id> --view standard --json         # Read last checkpoint first
hzl task steal <stuck-id> --if-expired --agent <agent-id>
```

为每个代理指定唯一的 `--agent` 参数（例如 `henry`、`clara`、`kenji`），以便追踪任务的执行者。

---

## 任务和项目的规模设定

**完成度的判断标准：** “我完成了 [任务]” 应该描述一个具体的成果。
- ✓ “安装了车库运动传感器”  
- ✗ “完成了家庭自动化系统”（这是一个开放性的任务，实际上无法完成）

**何时将任务拆分为多个部分：** 当各个部分能够独立完成或解决不同的问题时。

**补充说明：**  
不要在任务描述中重复具体细节，应引用相关文档以避免信息混乱。

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

# Web dashboard
hzl serve                                     # Start on port 3456
hzl serve --host 127.0.0.1                    # Restrict to localhost
hzl serve --background                        # Fork to background
hzl serve --status / --stop

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

可以通过 `http://<your-box>:3456` 访问（通过 Tailscale 进行访问）。在 macOS 上，可以使用 `hzl serve --background` 命令。

---

## HZL 的局限性

- **不提供任务编排功能** — 不会自动创建代理或分配任务；
- **不自动分解任务** — 不会自动将任务拆分为更小的部分；
- **不支持智能调度** — 仅使用简单的优先级和 FIFO 排序规则。

这些功能属于任务管理之外的编排层。

---

## 其他注意事项

- 通过 `exec` 工具来运行 `hzl` 命令。
- 查阅 `TOOLS.md` 文件以获取你的身份信息、需要监控的项目以及与你的角色相关的命令。
- 为每个代理指定唯一的 `--agent` 参数，并使用租用机制来避免数据库中的冲突。
- `hzl workflow run` 命令需要 HZL v2.0 或更高版本；如果该版本不可用，请使用上述的手动方案。