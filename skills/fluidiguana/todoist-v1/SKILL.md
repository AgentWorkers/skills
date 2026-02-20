---
name: todoist
description: 管理 Todoist 任务：列出、创建、完成、更新以及整理任务和项目。
---
# Todoist

API v1 的地址为 `https://api.todoist.com/api/v1/`，使用 Bearer Token 进行身份验证。

## 身份验证

Token 存储在环境变量 `TODOIST_TOKEN` 中。你可以在 shell 或 OpenClaw 的配置文件中设置该变量：

```bash
export TODOIST_TOKEN=your-token-here
```

你可以在以下链接获取 Token：https://app.todoist.com/app/settings/integrations/developer

## 常用操作

### 列出任务

```bash
curl -s "https://api.todoist.com/api/v1/tasks" \
  -H "Authorization: Bearer $TODOIST_TOKEN" | python3 -m json.tool
```

按项目筛选任务：
```bash
curl -s "https://api.todoist.com/api/v1/tasks?project_id=PROJECT_ID" \
  -H "Authorization: Bearer $TODOIST_TOKEN"
```

### 获取单个任务

```bash
curl -s "https://api.todoist.com/api/v1/tasks/TASK_ID" \
  -H "Authorization: Bearer $TODOIST_TOKEN"
```

### 创建任务

```bash
curl -s -X POST "https://api.todoist.com/api/v1/tasks" \
  -H "Authorization: Bearer $TODOIST_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Task name", "project_id": "PROJECT_ID", "due_string": "tomorrow", "priority": 1}'
```

任务的优先级范围为 1（普通）到 4（紧急）；`due_string` 支持自然语言表达（例如：“明天”、“每周一”、“2月20日”）。

### 完成任务

```bash
curl -s -X POST "https://api.todoist.com/api/v1/tasks/TASK_ID/close" \
  -H "Authorization: Bearer $TODOIST_TOKEN"
```

### 更新任务

```bash
curl -s -X POST "https://api.todoist.com/api/v1/tasks/TASK_ID" \
  -H "Authorization: Bearer $TODOIST_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Updated name", "due_string": "next friday"}'
```

### 删除任务

```bash
curl -s -X DELETE "https://api.todoist.com/api/v1/tasks/TASK_ID" \
  -H "Authorization: Bearer $TODOIST_TOKEN"
```

### 列出项目

```bash
curl -s "https://api.todoist.com/api/v1/projects" \
  -H "Authorization: Bearer $TODOIST_TOKEN"
```

### 创建项目

```bash
curl -s -X POST "https://api.todoist.com/api/v1/projects" \
  -H "Authorization: Bearer $TODOIST_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Project Name"}'
```

### 列出任务所属的章节

```bash
curl -s "https://api.todoist.com/api/v1/sections?project_id=PROJECT_ID" \
  -H "Authorization: Bearer $TODOIST_TOKEN"
```

### 创建新章节

```bash
curl -s -X POST "https://api.todoist.com/api/v1/sections" \
  -H "Authorization: Bearer $TODOIST_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"project_id": "PROJECT_ID", "name": "Section Name", "order": 0}'
```

### 将任务移动到指定章节

```bash
curl -s -X POST "https://api.todoist.com/api/v1/tasks/TASK_ID" \
  -H "Authorization: Bearer $TODOIST_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"section_id": "SECTION_ID"}'
```

## 注意事项

- API v2 已被弃用（错误代码：410）；请使用 v1。
- Token 是个人专用的 API Token，而非 OAuth 令牌。
- 使用 “List projects” 和 “List sections” 功能来获取项目/章节的 ID。
- 建议优先完成任务，而非直接删除它们。