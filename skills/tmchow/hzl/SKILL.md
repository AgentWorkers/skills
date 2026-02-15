---
name: hzl
description: OpenClaw的持久化任务数据库：用于协调子代理、管理检查点的进度，并在会话边界变化时保持数据的一致性。
metadata:
  { "openclaw": { "emoji": "🧾", "homepage": "https://github.com/tmchow/hzl", "requires": { "bins": ["hzl"] }, "install": [ { "id": "brew", "kind": "brew", "package": "hzl", "bins": ["hzl"], "label": "Install HZL (Homebrew)" }, { "id": "node", "kind": "node", "package": "hzl-cli", "bins": ["hzl"], "label": "Install HZL (npm)" } ] } }
---

# HZL：代理的持久任务跟踪工具

HZL（https://github.com/tmchow/hzl）是一个以本地存储为主的任务跟踪系统（基于数据库，可选择通过云同步进行备份），代理可以使用它来：

- 将多步骤的工作分解为项目和小任务
- 设置进度检查点（确保工作在会话结束后仍可保留）
- 协调子代理或多个编码工具的工作流程
- 生成可靠的状态报告（已完成的工作与剩余的工作）

本技能将教授代理如何使用 `hzl` 命令行界面（CLI）。

## 何时使用 HZL

**OpenClaw 没有内置的任务跟踪工具。** 与 Claude Code（具有 TodoWrite 功能）或 Codex（具有 update_plan 功能）不同，OpenClaw 依赖内存和 markdown 文件来跟踪工作。这使得 HZL 对 OpenClaw 来说尤为重要。

**对于任何非简单的任务跟踪，请默认使用 HZL：**
- 具有实际顺序依赖关系的多步骤项目
- 可能会跨越会话或涉及多个工具/代理的工作
- 需要委托给子代理的工作，并且在子代理崩溃时需要恢复工作
- 需要“从上次暂停的位置继续”的工作
- **任何希望跨会话持久保存的工作**
- **任何需要结构化管理（如任务嵌套、依赖关系、进度跟踪）的工作**
- **任何需要记录决策或责任归属的工作**

多会话或多代理的工作是使用 HZL 的常见场景，但这些并非使用 HZL 的必要条件。
对于单会话、单代理的工作，如果任务较为复杂，也可以使用 HZL。

**为什么 HZL 是 OpenClaw 的最佳选择：**

没有 HZL，OpenClaw 会在上下文中跟踪任务（这会占用大量内存，在数据压缩时导致数据丢失），或者通过 markdown 文件来跟踪任务（这需要手动管理，不支持任务嵌套或依赖关系，也没有可视化界面）。HZL 提供了以下功能：
- 持久化的存储，数据在会话结束后仍可保留
- 任务嵌套（父任务 + 子任务）和依赖关系
- 用于人类查看的 Web 仪表板（`hzl serve` 命令）
- 用于多代理协调的租约机制
- 进度检查点，便于恢复工作进度

**只有在以下情况下才无需使用 HZL：**
- 真正简单、一步即可完成的任务（会在当前会话内完成）
- 基于时间的提醒/警报（使用 OpenClaw Cron 功能）
- 长篇笔记或知识记录（使用专门的笔记系统）

**经验法则：** 如果你需要制定多步骤的计划，或者担心无法在当前会话内完成任务，就使用 HZL。

**示例：** “调查失败的测试并修复根本原因” → 应使用 HZL，因为这通常涉及多个子任务，即使你预计能在当前会话内完成。

**个人任务：** HZL 不是一个完善的个人待办事项管理工具，但它可以用于个人任务跟踪，也可以作为轻量级用户界面的后端。

## 核心概念

- **项目（Project）**：稳定的工作容器。对于 OpenClaw，使用一个 `openclaw` 项目即可——这样 `hzl task next` 的使用会更简单。创建项目前请先查看 `hzl project list`。
- **任务（Task）**：最高级别的工作项。对于多步骤的任务，它将成为一个父任务。
- **子任务（Subtask）**：任务的分解部分（格式为 `--parent <id>`）。最多支持一层嵌套。父任务是用于组织工作的容器——`hzl task next` 命令不会返回父任务。
- **检查点（Checkpoint）**：用于恢复进度的简短进度快照。
- **租约（Lease）**：有限期的任务分配机制（防止在多代理协作中出现任务孤立的情况）

## ⚠️ 注意：这些命令具有破坏性——请先阅读说明

以下命令会 **永久删除 HZL 的数据**，且无法恢复：
| 命令 | 功能 |
|---------|--------|
| `hzl init --force` | **删除所有数据**。会提示确认。 |
| `hzl init --force --yes` | **不提示确认即可删除所有数据**。非常危险。 |
| `hzl task prune ... --yes` | **永久删除** 已完成/归档的任务及其事件历史记录。 |

**AI 代理：** 除非用户明确要求删除数据，否则** 绝不要运行这些命令。**

- `hzl init --force` 会删除整个事件数据库：所有项目、任务、检查点和历史记录
- `hzl task prune` 仅删除终端状态（已完成/归档）且超过指定时间的任务
- 无法撤销操作，且没有备份则无法恢复数据。

## 避免的错误做法：项目过度膨胀

使用一个 `openclaw` 项目。所有请求和计划应作为 **父任务** 来管理，而不是创建新的项目。

**错误的做法（会导致项目膨胀）：**
```bash
hzl project create "garage-sensors"
hzl project create "query-perf"
# Now you have to track which project to query
```

**正确的做法（单个项目，父任务）：**
```bash
# Check for existing project first
hzl project list

# Use single openclaw project
hzl task add "Install garage sensors" -P openclaw
# → Created task abc123

hzl task add "Wire sensor to hub" --parent abc123
hzl task add "Configure alerts" --parent abc123

# hzl task next --project openclaw always works
```

**为什么这很重要：**
- 项目会不断累积；你可能会拥有大量被放弃的一次性项目
- `hzl task next --project X` 需要明确知道要查询哪个项目
- 使用单个项目时，`hzl task next --project openclaw` 总是可行的

## 确定父任务的范围

HZL 支持一层嵌套（父任务 → 子任务）。父任务的范围应限定为可完成的结果。

**完成度的判断标准：** “我完成了[父任务]” 应该描述一个具体的成果。
- ✓ “安装了车库运动传感器”
- ✓ “修复了查询性能问题”
- ✗ “完成了家庭自动化系统”（这是一个开放性的任务，可能永远无法完成）
- ✗ “完成了后端工作”（如果前端功能尚未发布）

**根据问题的性质来划分任务范围，而不是技术层面。** 如果一个全栈功能（前端 + 后端 + 测试）一起发布，通常应视为一个父任务。

**在以下情况下将任务拆分为多个父任务：**
- 各部分可以独立交付（可以分别发布）
- 你正在解决的是相互关联的不同问题

**添加上下文信息：** 使用 `-d` 选项添加详细信息，使用 `-l` 选项添加参考文档：
```bash
hzl task add "Install garage sensors" -P openclaw \
  -d "Per linked spec. Mount sensors at 7ft height." \
  -l docs/sensor-spec.md,https://example.com/wiring-guide
```

**不要在描述中重复技术细节**——这会导致信息混乱。应使用参考文档来提供详细信息。

**如果没有文档**，请提供足够的细节以便其他代理能够完成任务：
```bash
hzl task add "Configure motion alerts" -P openclaw -d "$(cat <<'EOF'
Trigger alert when motion detected between 10pm-6am.
Use Home Assistant automation. Notify via Pushover.
EOF
)"
```
描述内容支持 markdown 格式（最多 16KB）。

## 核心工作流程

**设置：**
```bash
hzl project list                    # Always check first
hzl project create openclaw         # Only if needed
```

**添加新任务：**
```bash
hzl task add "Feature X" -P openclaw -s ready         # Ready to claim
hzl task add "Subtask A" --parent <id>                # Subtask
hzl task add "Subtask B" --parent <id> --depends-on <subtask-a-id>  # With dependency
```

**执行任务：**
```bash
hzl task next -P openclaw                # Next available task
hzl task next --parent <id>              # Next subtask of parent
hzl task next -P openclaw --claim        # Find and claim in one step
hzl task claim <id>                      # Claim specific task
hzl task checkpoint <id> "milestone X"   # Notable progress or before pausing
```

**更改任务状态：**
```bash
hzl task set-status <id> ready           # Make claimable (from backlog)
hzl task set-status <id> backlog         # Move back to planning
```
状态：`待办（Backlog）→ 准备中（Ready）→ 进行中（In Progress）→ 完成（Done）→ 被阻塞（Blocked）**

**任务被阻塞时：**
```bash
hzl task block <id> --comment "Waiting for API keys from DevOps"
hzl task unblock <id>                    # When resolved
```

**完成任务：**
```bash
hzl task comment <id> "Implemented X, tested Y"  # Optional: final notes
hzl task complete <id>

# After completing a subtask, check parent:
hzl task show <parent-id> --json         # Any subtasks left?
hzl task complete <parent-id>            # If all done, complete parent
```

**故障排除：**
| 错误 | 解决方法 |
|-------|-----|
| “无法领取任务（状态：待办）” | 使用 `hzl task set-status <id> ready` |
| “无法完成：状态为 X” | 首先领取任务：`hzl task claim <id>` |

---

## 扩展参考资料（根据需要查阅——首次阅读时可跳过）

```bash
# Setup
hzl init                                      # Initialize (safe, won't overwrite)
hzl init --reset-config                       # Reset config to default location
hzl status                                    # Database mode, paths, sync state
hzl doctor                                    # Health check for debugging

# Create with options
hzl task add "<title>" -P openclaw --priority 2 --tags backend,auth
hzl task add "<title>" -P openclaw --depends-on <other-id>
hzl task add "<title>" -P openclaw -s in_progress --assignee <name>  # Create and claim

# List and find
hzl task list -P openclaw --available        # Ready tasks with met dependencies
hzl task list --parent <id>                  # Subtasks of a parent
hzl task list --root                         # Top-level tasks only

# Dependencies
hzl task add-dep <task-id> <depends-on-id>
hzl validate                                 # Check for circular dependencies

# Web Dashboard
hzl serve                    # Start on port 3456 (network accessible)
hzl serve --host 127.0.0.1   # Restrict to localhost only
hzl serve --background       # Fork to background
hzl serve --status           # Check if running
hzl serve --stop             # Stop background server

# Multi-agent recovery
hzl task claim <id> --assignee <agent-id> --lease 30
hzl task stuck
hzl task steal <id> --if-expired --author <agent-id>
```

**提示：** 如果工具需要解析输出，建议使用 `--json` 格式。

## 作者跟踪

HZL 在两个层面上记录作者信息：

| 功能 | 记录的内容 | 设置方式 |
|---------|----------------|--------|
| **任务负责人（Assignee）** | 谁负责该任务 | 在 `claim` 或 `add` 命令中使用 `--assignee` 参数 |
| **操作执行者（Event Author）** | 谁执行了某个操作 | 在其他命令中使用 `--author` 参数 |

`--assignee` 参数在 `claim` 和 `add` 命令中用于设置任务的所有权。`--author` 参数在其他命令（如检查点、评论、阻塞等）中用于记录操作的执行者：

```bash
# Alice owns the task
hzl task claim 1 --assignee alice

# Bob adds a checkpoint (doesn't change ownership)
hzl task checkpoint 1 "Reviewed the code" --author bob

# Task is still assigned to Alice, but checkpoint was recorded by Bob
```

对于需要会话跟踪的 AI 代理，在 `claim` 命令中使用 `--agent-id` 参数：
```bash
hzl task claim 1 --assignee "Claude Code" --agent-id "session-abc123"
```

## 推荐的使用模式

### 启动一个多步骤项目

1) 使用单个 `openclaw` 项目（如果不存在则创建）。
2) 为该任务创建一个父任务。
3) 将任务分解为具有依赖关系的子任务。
4) 验证所有设置。

```bash
# Check if project exists first
hzl project list
# Create only if needed
hzl project create openclaw

# Parent task for the initiative
hzl task add "Implement auth system" -P openclaw --priority 3
# → abc123

# Subtasks with sequencing
hzl task add "Clarify requirements + acceptance criteria" --parent abc123 --priority 5
hzl task add "Design API + data model" --parent abc123 --priority 4 --depends-on <reqs-id>
hzl task add "Implement endpoints" --parent abc123 --priority 3 --depends-on <design-id>
hzl task add "Write tests" --parent abc123 --priority 2 --depends-on <impl-id>
hzl task add "Docs + rollout plan" --parent abc123 --priority 1 --depends-on <tests-id>

hzl validate
```

### 从上一次会话中恢复

这是 OpenClaw 代理的核心用法——当你重新开始工作时，需要从上次会话的进度继续。

```bash
# 1. Check what's in progress or stuck
hzl task list -P openclaw --available     # What's ready to work?
hzl task stuck                            # Any expired leases from crashed sessions?

# 2. If there are stuck tasks, review their checkpoints before stealing
hzl task show <stuck-id> --json           # Read last checkpoint to understand state

# 3. Steal the expired task and continue
hzl task steal <stuck-id> --if-expired --author orchestrator

# 4. Read the last checkpoint to know exactly where to resume
hzl task show <stuck-id> --json | jq '.checkpoints[-1]'

# 5. Continue working, checkpoint your progress
hzl task checkpoint <stuck-id> "Resumed from previous session. Continuing from: <last checkpoint>"
```

**如果没有卡住的任务：** 只需使用 `hzl task next -P openclaw --claim` 命令来获取下一个可用的任务。

### 带有检查点的任务处理

在重要里程碑或暂停工作之前设置检查点。检查点应该简洁且易于操作：
- 你完成了什么
- 接下来该做什么（如果继续进行的话）

**AI 代理何时设置检查点：**
- 在执行可能失败的任何操作之前（如 API 调用、部署、安装）
- 在创建子代理之前（以防子代理崩溃）
- 在完成有意义的任务单元之后
- 在暂停或移交任务给其他代理之前

**经验法则：** 如果当前会话突然结束，其他代理能否从你的上一个检查点继续执行？如果不能，就立即设置检查点。

```bash
hzl task claim <id> --assignee orchestrator
# ...do work...
hzl task checkpoint <id> "Implemented login flow. Next: add token refresh." --progress 50
# ...more work...
hzl task checkpoint <id> "Added token refresh. Testing complete." --progress 100
hzl task complete <id>
```

你也可以在不设置检查点的情况下记录进度：
```bash
hzl task progress <id> 75
```

### 处理被阻塞的任务

当任务因外部依赖关系而卡住时，将其标记为阻塞状态：

```bash
hzl task claim <id> --assignee orchestrator
hzl task checkpoint <id> "Implemented login flow. Blocked: need API key for staging."
hzl task block <id> --comment "Blocked: waiting for staging API key from DevOps"

# Later, when unblocked:
hzl task unblock <id> --comment "Unblocked: received API key from DevOps"
hzl task checkpoint <id> "Got API key, resuming work"
hzl task complete <id>
```

**评论的最佳实践：** 提供关于操作背景的详细信息，而不仅仅是状态：
- 正确的示例：**“被阻塞：等待基础设施团队的 API 密钥”**
- 不正确的示例：**“等待 API 密钥”（缺少操作背景信息）**

被阻塞的任务会在仪表板（Blocked 列）中显示，并保留其负责人信息，但不会出现在 `--available` 列表中。

### 使用租约协调子代理

在委托任务时使用租约机制，以便能够检测到被放弃的任务并恢复工作。

```bash
hzl task add "Implement REST endpoints" -P myapp-auth --priority 3 --json
hzl task claim <id> --assignee subagent-claude-code --lease 30
```

**委托任务时提供明确指示：**
- 领取任务（并指定执行者 ID）
- 在执行过程中设置检查点
- 完成任务后更新状态

**监控任务进度：**
```bash
hzl task show <id> --json
hzl task stuck
hzl task steal <id> --if-expired --author orchestrator
```

### 使用子任务分解任务**

使用父任务/子任务的层次结构来组织复杂的工作：

```bash
# Create parent task
hzl task add "Implement vacation booking" -P portland-trip --priority 2
# → abc123

# Create subtasks (project inherited automatically)
hzl task add "Research flights" --parent abc123
hzl task add "Book hotel" --parent abc123 --depends-on <flights-id>
hzl task add "Plan activities" --parent abc123

# View breakdown
hzl task show abc123

# Work through subtasks
hzl task next --parent abc123
```

**重要提示：** `hzl task next` 命令只会返回子任务（没有子任务的父任务）。父任务仅用于组织任务结构，不会作为“下一个可用任务”返回。

**完成子任务后：** 在完成每个子任务后，检查父任务是否还有剩余的工作：
```bash
hzl task complete <subtask-id>

# Check parent status
hzl task show abc123 --json         # Any subtasks left?
hzl task complete abc123            # If all done, complete parent
```

## Web 仪表板

HZL 内置了一个 Kanban 仪表板，用于监控任务状态。仪表板按列显示任务（待办 → 被阻塞 → 准备中 → 进行中 → 完成），并支持按日期和项目筛选。

### 设置仪表板（推荐给 OpenClaw 用户）

为了在设备上始终能够访问仪表板，请将其设置为 systemd 服务（仅限 Linux 系统）：

```bash
# Check if service already exists before overwriting
systemctl --user status hzl-web 2>/dev/null && echo "Service already exists — skip setup" && exit 0

# Create the systemd user directory if needed
mkdir -p ~/.config/systemd/user

# Generate and install the service file
hzl serve --print-systemd > ~/.config/systemd/user/hzl-web.service

# Enable and start
systemctl --user daemon-reload
systemctl --user enable --now hzl-web

# IMPORTANT: Enable lingering so the service runs even when logged out
loginctl enable-linger $USER

# Verify it's running
systemctl --user status hzl-web
```

仪表板的访问地址为 `http://<your-box>:3456`（可通过 Tailscale 访问）。

**如果需要使用不同的端口：**
```bash
hzl serve --port 8080 --print-systemd > ~/.config/systemd/user/hzl-web.service
```

**macOS 注意：** systemd 仅适用于 Linux。在 macOS 上，可以使用 `hzl serve --background` 命令或手动创建 launchd plist 文件。**

### 快速命令

```bash
hzl serve                    # Start in foreground (port 3456)
hzl serve --background       # Fork to background process
hzl serve --status           # Check if background server is running
hzl serve --stop             # Stop background server
hzl serve --host 127.0.0.1   # Restrict to localhost only
```

使用 `--background` 命令开启临时会话。使用 systemd 可以实现持续访问。

## 最佳实践

1. **始终使用 `--json` 格式** 以获取程序化输出
2. 在重要里程碑或暂停工作之前设置检查点
3. 在完成任务前查看相关评论
4. 对所有任务使用单个 `openclaw` 项目
5. 使用依赖关系来表示任务顺序，而不是优先级
6. 对于长时间运行的任务，使用租约机制以便及时发现卡住的任务
7. 在领取被阻塞的任务之前查看检查点

## HZL 的局限性

HZL 的设计有一些限制：
- **不支持任务编排** — 不会自动创建代理或分配任务
- **不支持任务自动分解** — 不会自动拆分任务
- **不支持智能调度** — 仅使用简单的优先级和 FIFO 排序机制

这些功能由任务编排层负责实现，而非任务跟踪层。

## OpenClaw 的特殊说明

- 通过 Exec 工具运行 `hzl ...` 命令。
- OpenClaw 技能启动时会检查主机上的 `requires.bins` 文件。如果启用了沙箱环境，该二进制文件也必须存在于沙箱容器内。可以通过 `agents.defaults.sandbox.docker.setupCommand` 命令进行安装（或使用自定义镜像）。
- 如果多个代理共享同一个 HZL 数据库，请使用不同的 `--assignee` ID（例如：`orchestrator`、`subagent-claude`、`subagent-gemini`），并通过租约机制避免冲突。