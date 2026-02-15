---
name: no-nonsense-tasks
description: 这是一款简洁实用的任务管理器，基于 SQLite 数据库进行开发。它支持跟踪任务的状态（待办、进行中、已完成），以及任务的描述和标签。适用于个人任务管理、待办事项处理、项目进度跟踪，或任何需要基于状态来组织任务的工作流程。该工具提供了添加、查看、筛选、更新、移动和删除任务的功能。
---

# 实用任务管理工具

这是一个基于 SQLite 的简单任务跟踪工具，没有多余的繁琐功能，只专注于任务的完成。

## 先决条件

- 必须安装 `sqlite3` 命令行工具。

## 快速入门

初始化数据库：

```bash
./scripts/init_db.sh
```

添加第一个任务：

```bash
./scripts/task_add.sh "Build task tracker skill" \
  --description "Create a SQLite-based task manager" \
  --tags "work,urgent" \
  --status todo
```

列出所有任务：

```bash
./scripts/task_list.sh
```

## 任务状态

任务会经历四种状态：

- **待办（backlog）** - 新的想法或未来的任务
- **待处理（todo）** - 已准备好开始执行
- **进行中（in-progress）** - 当前正在处理中
- **已完成（done）** - 已完成任务

## 命令

### 初始化数据库

```bash
./scripts/init_db.sh
```

默认数据库位置：`~/.no-nonsense/tasks.db`  
可以通过 `export NO_NONSENSE_TASKS_DB=/path/to/tasks.db` 来更改数据库路径。

### 添加任务

```bash
./scripts/task_add.sh <title> [options]
```

**选项：**
- `-d, --description TEXT` - 任务描述
- `-t, --tags TAGS` - 用逗号分隔的标签
- `-s, --status STATUS` - 任务状态（默认为待办）

**示例：**
```bash
./scripts/task_add.sh "Deploy to prod" --description "Deploy v2.0" --tags "deploy,critical" --status todo
```

### 列出任务

```bash
./scripts/task_list.sh [--status STATUS]
```

**示例：**
```bash
./scripts/task_list.sh              # All tasks
./scripts/task_list.sh --status todo
```

### 查看任务详情

```bash
./scripts/task_show.sh <task_id>
```

### 将任务状态切换

```bash
./scripts/task_move.sh <task_id> --status <STATUS>
```

**示例：**
```bash
./scripts/task_move.sh 7 --status in-progress
```

### 更新任务信息

```bash
./scripts/task_update.sh <task_id> [options]
```

**选项：**
- `--title TEXT` - 更新任务标题
- `-d, --description TEXT` - 更新任务描述
- `-t, --tags TAGS` - 更新任务标签（用逗号分隔）
- `-s, --status STATUS` - 更新任务状态

### 快速更新标签

```bash
./scripts/task_tag.sh <task_id> --tags <TAGS>
```

**示例：**
```bash
./scripts/task_tag.sh 8 --tags "urgent,bug,frontend"
```

### 按标签过滤任务

```bash
./scripts/task_filter.sh <tag>
```

### 删除任务

```bash
./scripts/task_delete.sh <task_id>
```

### 查看统计信息

```bash
./scripts/task_stats.sh
```

显示按状态分类的任务数量及总数。

## 使用技巧

**典型工作流程：**

1. 将新想法添加到待办列表：`task_add.sh "任务想法" --status backlog`
2. 当任务准备好时，将其状态切换到待处理：`task_move.sh <id> --status todo`
3. 开始执行任务：`task_move.sh <id> --status in-progress`
4. 完成任务：`task_move.sh <id> --status done`

**标签管理：**

- 使用标签对任务进行分类：`work`（工作）、`personal`（个人）、`urgent`（紧急）、`bug`（错误）、`feature`（功能）
- 组合标签：`urgent,work,api` 或 `personal,home,shopping`
- 按任意标签过滤任务：`task_filter.sh urgent`

**状态过滤：**

- 查看当前正在处理的任务：`task_list.sh --status in-progress`
- 规划当天任务：`task_list.sh --status todo`
- 查看已完成的任务：`task_list.sh --status done`