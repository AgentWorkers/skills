---
name: tasktrove
description: 通过 Tasktrove API 管理待办事项。该 API 用于列出、创建、完成或更新任务。它可以响应各种与待办事项相关的请求，例如：“我的待办事项列表里有什么？”、“添加一个任务”、“将某项任务标记为已完成”以及“今天到期的任务有哪些？”。
---

# Tasktrove 待办事项管理

通过自托管的 [Tasktrove](https://tasktrove.io) 实例来管理任务。（[GitHub](https://github.com/dohsimpson/tasktrove)）

## 配置

设置以下环境变量：

```bash
export TASKTROVE_HOST="http://your-server:3333"
```

如果您的实例需要身份验证，请选择以下选项：
```bash
export TASKTROVE_TOKEN="your-api-token"
```

## 快速参考

### 使用 CLI 脚本

```bash
# List today's tasks
python3 scripts/tasks.py list --today

# List overdue tasks
python3 scripts/tasks.py list --overdue

# List this week's tasks
python3 scripts/tasks.py list --week

# Add a task
python3 scripts/tasks.py add "Task title" --due 2026-02-10 --priority 2

# Complete a task (use ID prefix from list output)
python3 scripts/tasks.py complete abc123

# Search tasks
python3 scripts/tasks.py search "keyword"
```

### 直接调用 API

#### 列出任务
```bash
curl -s "$TASKTROVE_HOST/api/v1/tasks"
```

#### 创建任务
```bash
# Note: API requires all fields including id, completed, labels, etc.
curl -X POST "$TASKTROVE_HOST/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "<uuid>",
    "title": "Task title",
    "priority": 4,
    "dueDate": "2026-02-06",
    "completed": false,
    "labels": [],
    "subtasks": [],
    "comments": [],
    "createdAt": "2026-02-06T12:00:00.000Z",
    "recurringMode": "dueDate"
  }'
```

#### 完成/更新任务
```bash
# Note: PATCH goes to collection endpoint with ID in body (not /tasks/{id})
curl -X PATCH "$TASKTROVE_HOST/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{"id": "<task-id>", "completed": true}'
```

#### 删除任务
```bash
curl -X DELETE "$TASKTROVE_HOST/api/v1/tasks/<task-id>"
```

## 任务结构

| 字段 | 类型 | 说明 |
|-------|------|-------|
| id | 字符串 | 创建任务时必须提供的 UUID |
| title | 字符串 | 必填 |
| description | 字符串 | 可选 |
| completed | 布尔值 | 默认值为 false |
| priority | 数字 | 优先级范围：1（最高）到 4（最低） |
| dueDate | 字符串 | 格式为 YYYY-MM-DD |
| projectId | 字符串 | 项目的 UUID |
| labels | 字符串数组 | 标签的 UUID 列表 |
| subtasks | 对象数组 | 嵌套的子任务 |
| recurring | 字符串 | 使用 RRULE 格式表示重复任务 |

## 优先级级别

- P1：紧急/关键
- P2：高优先级
- P3：中等优先级
- P4：低优先级（默认）

## 注意事项

- Tasktrove 的用户界面支持自然语言输入，但 API 需要结构化的 JSON 数据。
- 使用 `PATCH` 操作时，需要在请求体中包含任务的 ID。
- 使用 `POST` 方法创建或更新任务时，必须提供所有字段的信息。