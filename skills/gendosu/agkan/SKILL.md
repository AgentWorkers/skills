---
name: agkan
description: >
  **使用说明：**  
  当使用 agkan CLI 工具管理任务时，可以执行以下操作：  
  - 创建新任务  
  - 列出所有任务  
  - 更新任务信息  
  - 管理任务的标签  
  - 建立任务之间的关联（例如，将任务分配给特定团队或负责人）  
  - 通过看板（kanban board）跟踪项目进度  
  agkan CLI 是一个用于自动化任务管理的命令行工具，支持与各种项目管理工具（如 Kanban 系统）集成，提供高效的任务处理功能。
---
# agkan

## 概述

`agkan` 是一个基于 SQLite 的命令行（CLI）任务管理工具，专为与 AI 代理协作而设计。它支持以下 7 种任务状态：`icebox` → `backlog` → `ready` → `in_progress` → `review` → `done` → `closed`。

---

## 快速参考

### 代理指南

```bash
# Display a comprehensive guide for AI agents (overview, commands, workflows)
agkan agent-guide
```

### 任务操作

```bash
# Create task
agkan task add "Title" "Body"
agkan task add "Title" --status ready --author "agent"
agkan task add "Subtask" --parent 1
agkan task add "Title" --file ./spec.md  # Read body from file
agkan task add "Title" --blocked-by 1,2  # Set tasks that block this task
agkan task add "Title" --blocks 3,4      # Set tasks that this task blocks
agkan task add "Title" --assignees "alice,bob"  # Set task assignees (comma-separated)

# List tasks
agkan task list                    # All tasks
agkan task list --status in_progress
agkan task list --tree             # Hierarchical view
agkan task list --root-only        # Root tasks only
agkan task list --tag 1,2          # Filter by tags
agkan task list --dep-tree         # Dependency (blocking) tree view
agkan task list --sort title       # Sort by field (id / title / status / created_at / updated_at), default: created_at
agkan task list --order asc        # Sort order (asc / desc), default: desc
agkan task list --assignees "alice,bob"  # Filter by assignees (comma-separated)
agkan task list --all              # Include all statuses (including done and closed)

# Get details
agkan task get <id>

# Search
agkan task find "keyword"
agkan task find "keyword" --all  # Include done/closed

# Update (positional argument form - backward compatible)
agkan task update <id> status in_progress

# Update (named option form - v1.6.0+)
agkan task update <id> --status in_progress
agkan task update <id> --title "New Title"
agkan task update <id> --body "New body text"
agkan task update <id> --author "agent"
agkan task update <id> --assignees "alice,bob"
agkan task update <id> --file ./spec.md  # Read body from file
agkan task update <id> --status done --title "Updated Title"  # Multiple options

# Count
agkan task count
agkan task count --status ready --quiet  # Output numbers only

# Update parent-child relationship
agkan task update-parent <id> <parent_id>
agkan task update-parent <id> null  # Remove parent

# Delete task
agkan task delete <id>
```

### 任务之间的依赖关系

```bash
# task1 blocks task2 (task2 cannot be started until task1 is complete)
agkan task block add <blocker-id> <blocked-id>
agkan task block remove <blocker-id> <blocked-id>
agkan task block list <id>
```

### 标签操作

```bash
# Tag management
agkan tag add "frontend"
agkan tag list
agkan tag delete <tag-id-or-name>
agkan tag rename <id-or-name> <new-name>

# Tag tasks
agkan tag attach <task-id> <tag-id-or-name>
agkan tag detach <task-id> <tag-id-or-name>
agkan tag show <task-id>
```

### 元数据操作

```bash
# Set metadata
agkan task meta set <task-id> <key> <value>

# Get metadata
agkan task meta get <task-id> <key>

# List metadata
agkan task meta list <task-id>

# Delete metadata
agkan task meta delete <task-id> <key>
```

#### 优先级

任务的优先级通过 `priority` 键进行管理：

```bash
agkan task meta set <task-id> priority <value>
```

| 值 | 含义 |
|-----|------|
| `critical` | 需要立即处理。属于阻塞性问题（会阻止其他任务的执行） |
| `high` | 应优先处理 |
| `medium` | 普通优先级（默认值） |
| `low` | 有时间时再处理 |

**设置优先级的时机：** 优先级在规划阶段（`agkan-planning-subtask`）设置，同时任务会从 `backlog` 转移到 `ready` 状态。选择要执行的任务的技能（例如 `agkan-run`）会读取该优先级值来决定接下来处理哪个任务。

---

## 标签优先级

在选择或标记任务时，请按照以下优先级顺序进行：

| 优先级 | 标签名称 |
|----------|----------|
| 1 | bug   | 错误修复 |
| 2 | security | 安全相关 |
| 3 | improvement | 代码优化 |
| 4 | test   | 测试相关 |
| 5 | performance | 性能优化 |
| 6 | refactor | 代码重构 |
| 7 | docs   | 文档编写 |

所有技能都会参考这个优先级表来处理任务。

---

## JSON 输出

当需要机器处理数据时，可以使用 `--json` 标志：

```bash
agkan task list --json
agkan task get 1 --json
agkan task count --json
agkan tag list --json

# Combine with jq
agkan task list --status ready --json | jq '.tasks[].id'
```

### JSON 输出格式

#### `agkan task list --json`  

```json
{
  "totalCount": 10,
  "filters": {
    "status": "ready | null",
    "author": "string | null",
    "tagIds": [1, 2],
    "rootOnly": false
  },
  "tasks": [
    {
      "id": 1,
      "title": "Task Title",
      "body": "Body | null",
      "author": "string | null",
      "status": "icebox | backlog | ready | in_progress | review | done | closed",
      "parent_id": "number | null",
      "created_at": "2026-01-01T00:00:00.000Z",
      "updated_at": "2026-01-01T00:00:00.000Z",
      "parent": "object | null",
      "tags": [{ "id": 1, "name": "bug" }],
      "metadata": [{ "key": "priority", "value": "high" }]
    }
  ]
}
```

#### `agkan task get <id> --json`  

```json
{
  "success": true,
  "task": {
    "id": 1,
    "title": "Task Title",
    "body": "Body | null",
    "author": "string | null",
    "status": "backlog | ready | in_progress | review | done | closed",
    "parent_id": "number | null",
    "created_at": "2026-01-01T00:00:00.000Z",
    "updated_at": "2026-01-01T00:00:00.000Z"
  },
  "parent": "object | null",
  "children": [],
  "blockedBy": [{ "id": 2, "title": "..." }],
  "blocking": [{ "id": 3, "title": "..." }],
  "tags": [{ "id": 1, "name": "bug" }],
  "attachments": []
}
```

#### `agkan task count --json`  

```json
{
  "counts": {
    "icebox": 0,
    "backlog": 0,
    "ready": 2,
    "in_progress": 1,
    "review": 0,
    "done": 8,
    "closed": 5
  },
  "total": 16
}
```

#### `agkan task find <keyword> --json`  

```json
{
  "keyword": "Search keyword",
  "excludeDoneClosed": true,
  "totalCount": 3,
  "tasks": [
    {
      "id": 1,
      "title": "Task Title",
      "body": "Body | null",
      "author": "string | null",
      "status": "ready",
      "parent_id": "number | null",
      "created_at": "2026-01-01T00:00:00.000Z",
      "updated_at": "2026-01-01T00:00:00.000Z",
      "parent": "object | null",
      "tags": [],
      "metadata": []
    }
  ]
}
```

#### `agkan task block list <id> --json`  

```json
{
  "task": {
    "id": 1,
    "title": "Task Title",
    "status": "ready"
  },
  "blockedBy": [{ "id": 2, "title": "...", "status": "in_progress" }],
  "blocking": [{ "id": 3, "title": "...", "status": "ready" }]
}
```

#### `agkan task meta list <id> --json`  

```json
{
  "success": true,
  "data": [
    { "key": "priority", "value": "high" }
  ]
}
```

#### `agkan tag list --json`  

```json
{
  "totalCount": 3,
  "tags": [
    {
      "id": 1,
      "name": "bug",
      "created_at": "2026-01-01T00:00:00.000Z",
      "taskCount": 2
    }
  ]
}
```

---

## 典型工作流程

### Icebox 审查（agkan-icebox）

`Icebox` 包含尚未准备好进行规划的创意和候选任务。定期审查这些任务，以决定是继续推进还是关闭它们。

**从 Icebox 转到 Backlog 的条件：**
- 任务的需求或背景信息已经足够明确，可以开始规划了。
- 外部阻碍因素已经解决。
- 任务的相关性发生了变化。

**从 Icebox 转到 Closed 的条件：**
- 任务不再需要处理。
- 同类任务已在后续阶段被创建。
- 任务被其他方法替代。

### 作为代理接收任务

```bash
# Check assigned tasks
agkan task list --status ready
agkan task get <id>

# Start work
agkan task update <id> status in_progress

# Complete
agkan task update <id> status done
```

### 任务结构化

```bash
# Create parent task
agkan task add "Feature Implementation" --status ready

# Add subtasks
agkan task add "Design" --parent 1 --status ready
agkan task add "Implementation" --parent 1 --status backlog
agkan task add "Testing" --parent 1 --status backlog

# Set dependencies (Design → Implementation → Testing)
agkan task block add 2 3
agkan task block add 3 4

# View overall structure
agkan task list --tree
```

---

## 配置

将 `.agkan.yml` 文件放在项目根目录下，以自定义数据库路径：

```yaml
path: ./.agkan/data.db
```

或者使用环境变量：`AGENT_KANBAN_DB_PATH=/custom/path/data.db`