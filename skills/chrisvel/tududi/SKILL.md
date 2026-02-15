---
name: tududi
description: 在 tududi（一个自托管的任务管理器）中，您可以管理任务、项目和笔记。它适用于创建待办事项列表、进行任务管理以及项目组织。
---

# tududi 任务管理

## 配置

使用环境变量（在 `openclaw.json` 的 `skills.entries.tududi.env` 下设置）：
- `TUDUDI_URL` - 基本 URL（例如：`http://localhost:3004`）
- `TUDUDI_API_TOKEN` - 从 tududi 设置 → API Tokens 中获取的 API 令牌

## 认证

所有 API 调用都需要在请求头中包含以下字段：
```
Authorization: Bearer $TUDUDI_API_TOKEN
```

## API 路由规范

- **复数名词**（如 `/tasks`、`/projects`、`/inbox`）用于 **GET** 操作（列出任务）
- **单数名词**（如 `/task`、`/project`）用于 **POST/PUT/DELETE** 操作（创建/更新/删除任务）
- 在更新/删除操作中使用 **UID**（而非数字 ID）作为标识

## 常见操作

### 列出任务
```bash
curl -s $TUDUDI_URL/api/v1/tasks \
  -H "Authorization: Bearer $TUDUDI_API_TOKEN"
```

### 创建任务
```bash
curl -s -X POST $TUDUDI_URL/api/v1/task \
  -H "Authorization: Bearer $TUDUDI_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Task title", "due_date": "2026-02-10", "priority": 2, "project_id": 1, "tags": [{"name": "bug"}]}'
```

优先级：1（较低）到 4（紧急）
标签：`[{"name": "tagname"}, ...]`

### 更新任务
```bash
curl -s -X PATCH $TUDUDI_URL/api/v1/task/{uid} \
  -H "Authorization: Bearer $TUDUDI_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": 1, "tags": [{"name": "bug"}]}'
```

状态：0=未开始，1=进行中，2=已完成，6=已归档
标签：`[{"name": "tagname"}, ...]`

### 删除任务
```bash
curl -s -X DELETE $TUDUDI_URL/api/v1/task/{uid} \
  -H "Authorization: Bearer $TUDUDI_API_TOKEN"
```

### 列出项目
```bash
curl -s $TUDUDI_URL/api/v1/projects \
  -H "Authorization: Bearer $TUDUDI_API_TOKEN"
```

### 创建项目
```bash
curl -s -X POST $TUDUDI_URL/api/v1/project \
  -H "Authorization: Bearer $TUDUDI_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Project name"}'
```

### 收件箱
```bash
# List inbox items
curl -s $TUDUDI_URL/api/v1/inbox \
  -H "Authorization: Bearer $TUDUDI_API_TOKEN"

# Delete inbox item (use UID)
curl -s -X DELETE $TUDUDI_URL/api/v1/inbox/{uid} \
  -H "Authorization: Bearer $TUDUDI_API_TOKEN"
```

### 标签
```bash
curl -s $TUDUDI_URL/api/v1/tags \
  -H "Authorization: Bearer $TUDUDI_API_TOKEN"
```

## 任务状态
- 未开始
- 进行中
- 已完成
- 已归档

## 过滤条件
- `$TUDUDI_URL/api/v1/tasks?filter=today` - 今日到期的任务
- `$TUDUDI_URL/api/v1/tasks?filter=upcoming` - 未来到期的任务
- `$TUDUDI_URL/api/v1/tasks?filter=someday` - 无到期时间的任务
- `$TUDUDI_URL/api/v1/tasks?project_id={id}` - 按项目筛选任务

## API 文档

Swagger UI 可在 `$TUDUDI_URLswagger` 查看（需要登录）