# 任务管理代理技能（Task Management Agent Skill）

## 概述

该技能提供了一种基于 SQLite 数据库的任务管理功能，支持任务的持久化存储与操作。通过该技能，AI 代理能够创建、读取、更新、删除任务，并对任务进行状态跟踪和优先级管理。

## 功能特性

- **任务创建**：可以添加新任务，包括任务标题、描述、状态和优先级。
- **任务检索**：可以获取单个任务或列出所有任务。
- **任务过滤**：可以根据任务状态或优先级进行筛选。
- **任务更新**：可以修改任务的任何字段（标题、描述、状态、优先级）。
- **任务删除**：可以从数据库中删除任务。
- **持久化存储**：所有任务都存储在 SQLite 数据库中，并带有自动添加的时间戳。

## 使用方式

### 命令行接口

```bash
# Add task
python task_skill.py add "Task title" "Description" --status pending --priority high

# List all tasks
python task_skill.py list

# Filter by status
python task_skill.py list --status in_progress

# Filter by priority
python task_skill.py list --priority urgent

# Get task details
python task_skill.py get 1

# Update task
python task_skill.py update 1 --status completed --priority low

# Delete task
python task_skill.py delete 1
```

## 数据模型

### 任务字段

| 字段 | 类型 | 描述 | 是否必填 | 默认值 |
|-------|------|-------------|----------|---------|
| id     | INTEGER | 任务 ID（自动生成） | 是 | - |
| title   | TEXT | 任务标题 | 是 | "" |
| description | TEXT | 任务描述 | 否 | "" |
| status   | TEXT | 任务状态 | 是 | "pending" |
| priority | TEXT | 任务优先级 | 是 | "medium" |
| created_at | TIMESTAMP | 创建时间戳 | 是 | 当前时间 |
| updated_at | TIMESTAMP | 最后更新时间戳 | 是 | 当前时间 |

### 状态值

- `pending`：任务处于待处理状态，尚未开始。
- `in_progress`：任务正在处理中。
- `completed`：任务已完成。
- `blocked`：任务被阻塞，无法继续执行。

### 优先级值

- `low`：低优先级任务。
- `medium`：中等优先级任务（默认值）。
- `high`：高优先级任务。
- `urgent`：紧急任务，需要立即处理。

## 响应格式

所有代理方法返回一个包含 `success` 字段的字典：

### 成功创建任务
```python
{
    "success": True,
    "task_id": 1,
    "message": "Task created with ID: 1"
}
```

### 成功列出任务
```python
{
    "success": True,
    "tasks": [
        {
            "id": 1,
            "title": "Task title",
            "description": "Task description",
            "status": "pending",
            "priority": "medium",
            "created_at": "2026-02-11T10:30:00",
            "updated_at": "2026-02-11T10:30:00"
        }
    ],
    "count": 1
}
```

### 成功获取任务信息
```python
{
    "success": True,
    "task": {
        "id": 1,
        "title": "Task title",
        "description": "Task description",
        "status": "pending",
        "priority": "medium",
        "created_at": "2026-02-11T10:30:00",
        "updated_at": "2026-02-11T10:30:00"
    }
}
```

### 操作失败
```python
{
    "success": False,
    "message": "Task 1 not found"
}
```

## 数据库

- **数据库文件**：`tasks.db`（自动创建于当前目录）。
- **数据库类型**：SQLite3。
- **数据库约束**：状态和优先级值在数据库层面进行验证。
- **时间戳**：由数据库自动管理。

## 依赖项

无依赖项——仅使用 Python 的内置 `sqlite3` 模块。

## 使用场景

1. **任务跟踪**：记录个人或项目的任务状态和优先级。
2. **待办事项管理**：维护一个持久的待办事项列表。
3. **工作流自动化**：将任务管理集成到自动化工作流中。
4. **项目管理**：简单的项目任务跟踪。
5. **代理内存管理**：为 AI 代理提供持久化的任务存储空间。

## 注意事项

- 数据库连接在操作过程中保持持久化。
- 操作完成后务必调用 `agent.close()` 以正确关闭数据库连接。
- 使用上下文管理器模式实现自动清理：
  ```python
  with TaskAgent() as agent:
      agent.add_task("Task", "Description")
  ```
- 任务 ID 为从 1 开始的自动递增整数。
- 所有时间戳均采用 ISO 8601 格式。