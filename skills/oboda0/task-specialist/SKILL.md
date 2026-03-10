---
name: task-specialist
version: 2.1.0
author: OBODA0
homepage: https://github.com/OBODA0/task-specialist-skill
tags: ["task", "management", "sqlite", "workflow", "productivity", "project", "planning", "breakdown", "local", "cli"]
metadata: {"openclaw":{"emoji":"📋","requires":{"bins":["sqlite3","bash"]}}}
description: "这是一个基于本地 SQLite 数据库的强大任务管理系统，专为提升您的人工智能代理的项目执行效率而设计。它非常适合处理简单任务以及复杂的多步骤项目，能够自动管理工作流程并跟踪任务之间的依赖关系，且无需依赖易出问题的内存系统。"
---
# Task-Specialist

**使用 SQLite 进行本地任务管理。** 支持离线操作、数据持久化，且除了 `sqlite3` 和 `bash` 之外不依赖任何其他外部库。

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
- **状态透明化**：实时更新任务状态（`start`、`block`、`complete`），以便随时追踪任务进度。
- **依赖管理**：使用 `task depend` 将相互依赖的任务关联起来，避免执行顺序错误。
- **记录进度**：通过 `--notes` 或 `task show` 输出来记录项目执行过程中的关键信息。
- **多代理集群队列**：如果在其他代理并行执行任务时，**切勿** 盲目从 `task list` 中选取任务（这可能导致严重的竞态条件）。**必须** 使用 `task claim --agent="<YourName>"` 来获取最高优先级、尚未完成的任务，并将该任务的标识符显示在全局看板中。
- **上下文传递**：在关闭当前任务之前，使用 `task note <Next_Task_ID> "你的具体上下文信息"` 将重要的 URL、文件路径或错误代码传递给下游代理。**注意**：切勿在任务备注中存储 API 密钥或敏感信息，应使用安全的本地环境变量。
- **验证检查点**：如果任务关联了 `--verify="cmd"`，执行 `task complete <ID>` 会自动打印出 Bash 子 shell 的检查点信息。**出于安全考虑（防止远程代码执行），这些检查点必须手动执行。**

## 集群编排器指南

如果你是负责管理复杂项目的**主要代理（编排器）**，`task-specialist` 可帮助你创建多个子代理来同时执行独立的工作任务：
1. **何时创建子代理**：在需要横向扩展任务时使用集群功能（例如：“为 10 个不同的文件编写单元测试”，或“同时部署 3 个独立的 Docker 容器”）。对于高度线性、顺序性强的任务，无需创建子代理。
2. **构建任务结构**：
   - 首先使用 `task create` 创建所有并行任务。
   - 创建一个最终整合任务（例如：“合并服务”），并通过 `task depend` 将其与其他子任务关联起来。这会自动阻塞最终任务，直到所有子代理完成。
   - 使用 `task edit <ID> --notes="..."` 将必要的上下文信息（URL、文件路径、git SHA 值）直接添加到任务中。
3. **启动子代理**：使用 OpenClaw 的 `sessions_spawn` 工具来启动子代理。设置 `mode: "run"` 以启动一次性执行的并行任务，并在 `task` 参数中传递相应的执行指令：
   ```json
   {
     "tool": "sessions_spawn",
     "runtime": "subagent",
     "mode": "run",
     "label": "worker-alpha",
     "task": "You are a Swarm Worker utilizing the `task-specialist` skill. The task payload DB is at $PWD/.tasks.db. (Read SKILL.md for CLI syntax if needed).\n1. Run `task claim --agent=\"worker-alpha\"` to atomically pop the queue.\n2. Read your target objective via `task show <ID>`.\n3. Execute the objective. Record vital context for me via `task note <ID> \"msg\"`.\n4. Run `task complete <ID>` and self-terminate."
   }
   ```

4. **监控集群状态**：当设置为 `mode: "run"` 的子代理正在异步执行时：
   - 定期运行 `task board` 命令查看 SQLite 看板中的任务进度。
   - 如果有代理超时，使用 `task stuck` 命令终止该代理（`subagents(action=\"kill\")`），并重新调度其任务。

## 子代理使用指南

作为新启动的**子代理**，你的唯一任务是执行队列中的待处理任务，同时避免与其他并行代理发生冲突：
1. **获取任务**：**切勿** 盲目从 `task list` 中选取任务。**必须** 使用 `task claim --agent="<YourName>"` 来获取任务。该命令会自动执行原子级的 SQL 锁，确保你不会与其他代理争夺相同的资源。
2. **读取任务上下文**：获取任务后（例如任务编号为 5），查看 `Notes:` 部分，其中可能包含来自编排器或其他子代理的详细信息。
3. **传递上下文**：完成任务后，判断是否需要将相关信息传递给下游代理。如果需要，使用 `task note <Next_Task_ID> \"你的上下文信息\"` 将这些信息添加到下游任务的备注中。
4. **完成任务并设置检查点**：执行 `task complete <ID>`。如果任务包含检查点验证脚本（Bash 子 shell），系统会提示你手动执行该脚本。**在任务通过测试之前，你必须修复代码中的问题才能完成任务并终止自身。**

## 命令行参考

### 任务生命周期

**状态流转**：`pending` → `in_progress` → `blocked` → `done`

**优先级**：从 1（低）到 10（高）。默认值为 5。
**删除任务**：如果任务有子任务，则拒绝删除请求；除非使用 `--force` 选项，否则删除操作会波及所有子任务及其依赖项。

### 查询与监控

```bash
task board                                                               # renders visual ASCII Kanban dashboard
task list [--status=S] [--parent=ID] [--project=N] [--format=chat] [--tag="T"] # tabular lists or github markdown
task export [--status=STATUS] [--project=NAME] [--json]                  # markdown table or raw JSON array hook
task show ID                                                             # full details, assignee, & deps
task stuck                                                               # in_progress tasks inactive >30min
```

### 子任务分解

```bash
task break PARENT_ID "step 1" "step 2" "step 3"
```

子任务会自动与父任务关联，并根据依赖关系进行顺序执行（例如：步骤 2 依赖于步骤 1，步骤 3 依赖于步骤 2）。

### 手动设置依赖关系

```bash
task depend TASK_ID DEPENDS_ON_ID
```

启动任务时，所有依赖任务必须已完成；否则系统会拒绝执行并列出阻碍任务完成的依赖项。

### 心跳检测

```bash
task-heartbeat TASK_ID    # update last_updated timestamp
task-heartbeat            # report stalled tasks (no args)
```

**集成到长期运行的脚本中**

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
       created_at, started_at, completed_at, last_updated, notes, verification_cmd, assignee

dependencies: task_id, depends_on_task_id (composite PK)
```

## 环境配置

| 变量 | 默认值 | 用途 |
|---|---|---|
| `TASK_DB` | `$PWD/.tasks.db` | SQLite 数据库的路径 |
| **注意**：数据库默认位于命令执行所在的当前工作目录下的隐藏文件 `.tasks.db` 中。该设置支持为不同项目/工作空间创建独立的任务列表，避免数据冲突。

## 安全性注意事项：
- 不使用 `eval()` 函数，不进行外部 API 调用，不使用加密技术。
- 仅使用 SQLite 和 Bash 进行任务处理，通过 VirusTotal 工具检测无安全风险。
- 对所有任务 ID 进行整数验证（使用 `require_int()` 函数）。
- **状态限制**：`task list --status` 仅接受 `pending`、`in_progress`、`blocked`、`done` 状态。
- **日期格式**：`--since` 参数必须符合 `YYYY-MM-DD` 格式。
- **文本输入处理**：使用单引号进行转义（`sed "s/'/''/g"`）。
- **临时文件存储**：SQL 语句会先写入临时文件，再通过标准输入（stdin）传递给 `sqlite3`，以防止参数注入攻击。