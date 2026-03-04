---
name: task-specialist
version: 1.2.2
author: OBODA0
homepage: https://github.com/OBODA0/task-specialist-skill
tags: ["task", "management", "sqlite", "workflow", "productivity", "project", "planning", "breakdown", "local", "cli"]
metadata: {"openclaw":{"emoji":"📋","requires":{"bins":["sqlite3","bash"]}}}
description: "这是一个功能强大的本地任务管理系统，基于 SQLite 数据库开发，旨在提升您的人工智能代理的项目执行效率。该系统非常适合处理简单任务以及复杂的多步骤项目，能够自动管理工作流程并追踪任务之间的依赖关系，同时无需依赖易出问题的内存系统。"
---
# Task-Specialist

**使用 SQLite 进行本地任务管理。** 支持离线操作，数据持久化存储，仅依赖 `sqlite3` 和 `bash`。

## 快速入门

```bash
# Install (creates DB only, no PATH changes)
bash install.sh

# Or install AND create easy CLI symlinks in ~/.local/bin
bash install.sh --symlink

# Create and work tasks
task create "Build auth module" --priority=8
task start 1
task-heartbeat 1          # keep-alive ping
task complete 1
```

## 代理原则

在使用 `task-specialist` 命令行工具时，请遵循以下原则以确保项目的高效、有序执行：
- **先分解任务**：始终使用 `task break` 将大型、多步骤的任务分解为更小、更逻辑清晰的子任务。
- **状态透明**：实时更新任务状态（`start`、`block`、`complete`），以便随时追踪任务进度。
- **依赖关系管理**：使用 `task depend` 将相互依赖的任务关联起来，避免执行顺序混乱。
- **记录进度**：通过 `--notes` 或 `task show` 输出来记录项目执行过程中的关键信息。

## 命令行参考

### 任务生命周期

```bash
task create "description" [--priority=N] [--parent=ID] [--project=NAME]  # → prints task ID
task edit    ID [--desc="new text"] [--priority=N] [--project=NAME]      # adjust task details
task start   ID                                          # pending → in_progress
task block   ID "reason"                                 # → blocked (reason in notes)
task complete ID                                         # → done + auto-unblocks dependents
task delete  ID [--force]                                # remove task (--force for parents)
```

**状态流转**：`pending` → `in_progress` → `blocked` → `done`

**优先级**：从 1（低）到 10（高）。默认值为 5。

**删除任务**：如果任务包含子任务，则拒绝删除操作；除非使用 `--force` 选项，否则会递归删除所有子任务及其依赖项。

### 查询任务信息

```bash
task list [--status=S] [--parent=ID] [--project=N] [--since=YYYY-MM-DD] [--search="regex"]
task export [--status=STATUS] [--project=NAME]                           # generates markdown table
task show ID                                                             # full details & deps
task stuck                                  # in_progress tasks inactive >30min
```

### 子任务分解

```bash
task break PARENT_ID "step 1" "step 2" "step 3"
```

创建与父任务关联的子任务，并自动处理依赖关系：步骤 2 依赖于步骤 1，步骤 3 依赖于步骤 2。

### 手动设置依赖关系

```bash
task depend TASK_ID DEPENDS_ON_ID
```

启动任务时，所有依赖任务必须已完成；否则命令会失败，并显示阻碍任务完成的障碍。

完成任务后，所有依赖关系都已满足的子任务会自动解除阻塞状态（从 `blocked` 变为 `pending`）。

### 心跳检测（Heartbeat）

```bash
task-heartbeat TASK_ID    # update last_updated timestamp
task-heartbeat            # report stalled tasks (no args)
```

**集成到长时间运行的脚本中**

```bash
while work_in_progress; do
  do_work
  task-heartbeat "$TASK_ID"
  sleep 300  # every 5 minutes
done
```

## 数据库架构

```sql
tasks: id, request_text, project, status, priority, parent_id,
       created_at, started_at, completed_at, last_updated, notes

dependencies: task_id, depends_on_task_id (composite PK)
```

## 环境配置

| 变量          | 默认值        | 用途                  |
|---------------|-------------|----------------------|
| `TASK_DB`       | `$PWD/.tasks.db`   | SQLite 数据库路径            |
|              |                |                      |
|              |                | 支持为不同项目/工作空间创建独立的任务列表，避免数据冲突 |

## 安全性措施

- 不使用 `eval()` 函数，不调用外部 API，也不进行加密操作。
- 仅使用 SQLite 和 Bash 进行数据处理，通过 VirusTotal 安全检测。
- 在执行任何 SQL 语句前，使用 `require_int()` 函数对所有任务 ID 进行整数验证。
- **状态白名单**：`task list --status` 命令仅接受 `pending`、`in_progress`、`blocked`、`done` 状态。
- **日期格式限制**：`--since` 参数必须符合 `YYYY-MM-DD` 格式。
- **文本输入处理**：使用单引号转义 (`sed "s/'/''/g"`) 来清理用户输入。
- **临时文件存储 SQL 语句**：将 SQL 语句写入临时文件，然后通过标准输入（stdin）传递给 `sqlite3`，以防止参数注入攻击。