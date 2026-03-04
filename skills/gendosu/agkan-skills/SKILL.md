---
name: agkan
description: >
  **使用说明：**  
  当使用 agkan CLI 工具管理任务时，可以执行以下操作：  
  - 创建任务  
  - 列出任务  
  - 更新任务信息  
  - 管理任务的标签  
  - 建立任务之间的关联（例如：依赖关系）  
  - 通过看板（kanban board）跟踪项目进度  
  agkan CLI 是一个用于自动化任务管理的命令行工具，提供了丰富的功能来帮助您高效地组织和执行项目任务。
---
# agkan

## 概述

`agkan` 是一个基于 SQLite 的命令行（CLI）任务管理工具，专为与 AI 代理协作而优化设计。

**任务状态共有 7 种：** `icebox` → `backlog` → `ready` → `in_progress` → `review` → `done` → `closed`

## 安装（必需）

如果尚未安装 `agkan`，请先运行以下命令：

```bash
npm install -g agkan
```

在继续之前，请确认 `agkan` 命令可用。

---

## 快速参考

### 任务操作

```bash
# Create a task
agkan task add "title" "body"
agkan task add "title" --status ready --author "agent"
agkan task add "subtask" --parent 1
agkan task add "title" --file ./spec.md  # Load body from file

# List tasks
agkan task list                    # All tasks
agkan task list --status in_progress
agkan task list --tree             # Hierarchical view
agkan task list --root-only        # Root tasks only
agkan task list --tag 1,2          # Filter by tag

# Show details
agkan task get <id>

# Search
agkan task find "keyword"
agkan task find "keyword" --all  # Include done/closed

# Update
agkan task update <id> status in_progress

# Count
agkan task count
agkan task count --status ready --quiet  # Output number only

# Update parent-child relationship
agkan task update-parent <id> <parent_id>
agkan task update-parent <id> null  # Remove parent
```

### 任务之间的依赖关系（阻塞关系）

```bash
# task1 blocks task2 (task2 cannot start until task1 is complete)
agkan task block add <blocker-id> <blocked-id>
agkan task block remove <blocker-id> <blocked-id>
agkan task block list <id>
```

### 标签操作

```bash
# Manage tags
agkan task tag add "frontend"
agkan task tag list
agkan task tag delete <tag-id>

# Attach tags to tasks
agkan task tag attach <task-id> <tag-id>
agkan task tag detach <task-id> <tag-id>
agkan task tag show <task-id>
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

任务的优先级通过 `priority` 键来管理：

```bash
agkan task meta set <task-id> priority <value>
```

| 值 | 含义 |
|-----|------|
| `critical` | 需要立即处理的问题（阻塞其他任务） |
| `high` | 需要优先处理的任务 |
| `medium` | 正常优先级（默认值） |
| `low` | 可在有空闲时间时处理 |

---

## JSON 输出

当需要机器处理数据时，请使用 `--json` 标志：

```bash
agkan task list --json
agkan task get 1 --json
agkan task count --json
agkan task tag list --json

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
      "title": "task title",
      "body": "body | null",
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
    "title": "task title",
    "body": "body | null",
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
  "keyword": "search term",
  "excludeDoneClosed": true,
  "totalCount": 3,
  "tasks": [
    {
      "id": 1,
      "title": "task title",
      "body": "body | null",
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
    "title": "task title",
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

#### `agkan task tag list --json`  

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

## 常见工作流程

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

### 构建任务结构

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

# Review the full structure
agkan task list --tree
```

---

## 配置

将 `.agkan.yml` 文件放置在项目根目录下以自定义数据库路径：

```yaml
path: ./.agkan/data.db
```

或者使用环境变量：`AGENT_KANBAN_DB_PATH=/custom/path/data.db`