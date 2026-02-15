---
name: todozi
description: "Todozi Eisenhower Matrix API客户端 + LangChain工具：  
支持创建任务矩阵、任务、目标及笔记；实现任务列表的显示、搜索、更新功能；支持批量操作；支持Webhook触发。  
任务分类：待办（do）、已完成（done）、梦想中的任务（dream）、需委派（delegate）、需推迟（defer）、无需处理（dont）。"
---

# Todozi

## 快速入门

**作为SDK：**
```python
from skills.todozi.scripts.todozi import TodoziClient

client = TodoziClient(api_key="your_key")
matrices = await client.list_matrices()
task = await client.create_task("Build feature", priority="high")
await client.complete_item(task.id)
```

**作为LangChain工具：**
```python
from skills.todozi.scripts.todozi import TODOZI_TOOLS
# Add to agent tools list
```

## SDK概述

| 类别 | 功能 |
|-------|---------|
| `TodoziClient` | 异步API客户端 |
| `TodoziTask` | 任务数据类 |
| `TodoziMatrix` | 矩阵数据类 |
| `TodoziStats` | 统计数据类 |

### 环境配置
```bash
export TODOZI_API_KEY=your_key
export TODOZI_BASE=https://todozi.com/api  # optional, default provided
```

## 客户端方法

### 矩阵操作
```python
# List all matrices
matrices = await client.list_matrices()

# Create matrix
matrix = await client.create_matrix("Work", category="do")

# Get matrix
matrix = await client.get_matrix("matrix_id")

# Delete matrix
await client.delete_matrix("matrix_id")
```

### 任务/目标/备注
```python
# Create task
task = await client.create_task(
    title="Review PR",
    priority="high",
    due_date="2026-02-01",
    description="Check the new feature",
    tags=["pr", "review"],
)

# Create goal
goal = await client.create_goal("Ship v2", priority="high")

# Create note
note = await client.create_note("Remember to call Mom")

# Get item
item = await client.get_item("item_id")

# Update item
updated = await client.update_item("item_id", {"title": "New title", "priority": "low"})

# Complete item
await client.complete_item("item_id")

# Delete item
await client.delete_item("item_id")
```

### 列表操作
```python
# List tasks (with filters)
tasks = await client.list_tasks(status="todo", priority="high")

# List goals
goals = await client.list_goals()

# List notes
notes = await client.list_notes()

# List everything
all_items = await client.list_all()
```

### 搜索

**搜索条件：** 标题、描述、标签（不包含内容）

```python
results = await client.search(
    query="pr",
    type_="task",          # task, goal, or note
    status="pending",
    priority="high",
    category="do",
    tags=["review"],
    limit=10,
)
```

### 批量操作
```python
# Update multiple
await client.bulk_update([
    {"id": "id1", "title": "Updated"},
    {"id": "id2", "priority": "low"},
])

# Complete multiple
await client.bulk_complete(["id1", "id2"])

# Delete multiple
await client.bulk_delete(["id1", "id2"])
```

### Webhook（事件通知）
```python
# Create webhook
webhook = await client.create_webhook(
    url="https://yoururl.com/todozi",
    events=["item.created", "item.completed"],
)

# List webhooks
webhooks = await client.list_webhooks()

# Update webhook
await client.update_webhook(webhook_id, url, ["*"])

# Delete webhook
await client.delete_webhook(webhook_id)
```

### 系统管理
```python
# Stats
stats = await client.get_stats()

# Health check
health = await client.health_check()

# Validate API key
valid = await client.validate_api_key()

# Register (get API key)
keys = await client.register(webhook="https://url.com")
```

## LangChain工具

该技能提供了带有`@tool`标记的函数，用于与代理（agent）集成：

```python
from skills.todozi.scripts.todozi import TODOZI_TOOLS

# Available tools:
# - todozi_create_task(title, priority, due_date, description, thread_id, tags)
# - todozi_list_tasks(status, priority, thread_id, limit)
# - todozi_complete_task(task_id)
# - todozi_get_stats()
# - todozi_search(query, type_, status, priority, limit)
# - todozi_list_matrices()
```

## 分类

| 分类 | 描述 |
|----------|-------------|
| `do` | 立即执行（紧急且重要） |
| `delegate` | 委派他人处理（紧急但不重要） |
| `defer` | 延期处理（不紧急但重要） |
| `done` | 已完成任务的项目 |
| `dream` | 目标/梦想（不紧急且不重要） |
| `dont` | 不要做（两者都不符合） |

## 常用操作模式

- **自动创建默认矩阵：**  
  ```python
task = await client.create_task("My task")  # Creates "Default" matrix if needed
```

- **获取包含完成率的统计信息：**  
  ```python
stats = await client.get_stats()
rate = stats.completed_tasks / stats.total_tasks * 100 if stats.total_tasks > 0 else 0
```

- **使用多个条件进行搜索：**  
  ```python
results = await client.search("feature", type_="task", status="pending", priority="high")
```

- **完成多个任务：**  
  ```python
tasks = await client.list_tasks(status="todo")
ids = [t.id for t in tasks[:5]]
await client.bulk_complete(ids)
```