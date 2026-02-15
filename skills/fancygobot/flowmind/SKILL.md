---
name: flowmind
description: 使用 FlowMind 管理生产力——通过 REST API 实现目标、任务（包含子任务）、笔记、人员以及标签的管理。当用户需要创建、列出、更新或删除目标、任务、笔记、联系人或标签；管理重点/优先级；跟踪进度；或通过 FlowMind 整理工作空间时，可以使用该工具。
---

# FlowMind

[FlowMind](https://flowmind.life/) 是一个个性化的生产力工作空间，它将您的目标、任务、笔记和联系人整合在一个平台上。与传统的项目管理工具不同，FlowMind能够适应您的思维方式和工作习惯——将任务与更大的目标关联起来，根据精力水平和专注需求进行标记，并让您清晰地了解当前最重要的任务。除了任务管理之外，FlowMind还帮助您维护人脉关系、安排会议以及跟踪个人习惯——这些通常分散在不同应用程序中的功能。最棒的是，大多数功能都可以通过自然语言与人工智能交互来使用，因此您只需简单地说出需求，就能管理自己的工作流程。

## 设置

请在您的代理配置或环境中设置以下参数：
- `FLOWMIND_API_KEY`：来自 FlowMind 账户的Bearer 令牌（在“设置” → “API 密钥”中获取）
- 基本 URL：`https://flowmind.life/api/v1`

所有请求都需要使用 `Authorization: Bearer <FLOWMIND_API_KEY>` 和 `Content-Type: application/json`。

## 快速参考

### 目标
```
GET    /goals              — list (filter: status, category, pinned; sort: title, target_date, progress)
POST   /goals              — create (required: title)
GET    /goals/:id          — get
PATCH  /goals/:id          — update
DELETE /goals/:id          — delete
GET    /goals/:id/tasks    — list tasks for goal
```
字段：标题、描述、状态（活动/已完成/归档）、类别（工作/职业/健康/个人/学习/财务）、目标日期、进度（0-100）、是否固定显示

### 任务
```
GET    /tasks              — list (filter: status, priority, energy_level, goal_id, person_id, due_date_from/to, focused, focus_today)
POST   /tasks              — create (required: title)
GET    /tasks/:id          — get
PATCH  /tasks/:id          — update
DELETE /tasks/:id          — delete
GET    /tasks/:id/subtasks — list subtasks
POST   /tasks/:id/subtasks — create subtask
```
字段：标题、描述、状态（待办/进行中/已完成/归档）、优先级（低/中/高/紧急）、精力水平（低/中/高）、截止日期、计划时间、目标 ID、关联任务 ID、预计耗时、实际耗时、是否固定显示、是否专注、今日专注任务、专注顺序、图标

### 笔记
```
GET    /notes    — list (filter: category, task_id, pinned)
POST   /notes    — create (required: title)
GET    /notes/:id
PATCH  /notes/:id
DELETE /notes/:id
```
字段：标题、内容、类别、关联任务 ID、是否受保护、是否固定显示

### 人员信息
```
GET    /people             — list (filter: relationship_type, tag_id, search)
POST   /people             — create (required: name)
GET    /people/:id
PATCH  /people/:id
DELETE /people/:id
GET    /people/:id/tags    — list tags
POST   /people/:id/tags    — add tag (body: {tag_id})
DELETE /people/:id/tags/:tagId
```
字段：姓名、电子邮件、电话、公司、职位、关系类型（工作/同事/朋友/家人/导师/客户/其他）、备注、出生月份、出生日期、位置、最后一次联系时间

### 标签
```
GET    /tags    — list (sort: name, created_at)
POST   /tags    — create (required: name; optional: color)
GET    /tags/:id
PATCH  /tags/:id
DELETE /tags/:id
```

## 分页与排序
- `page`（默认值：1）、`limit`（默认值：20，最大值：100）
- `sort`：排序字段名称；`order=asc` 或 `order=desc`（升序/降序）

## 响应格式
```json
{ "data": [...], "meta": { "pagination": { "page": 1, "limit": 20, "total": 42, "totalPages": 3, "hasMore": true } } }
```

## 错误处理
错误会返回如下格式的响应：`{"error": {"code": "...", "message": "...", "details": [] }`。可能的错误代码包括：BAD_REQUEST、UNAUTHORIZED、NOT_FOUND、VALIDATION_ERROR、RATE_LIMITED。

## 常见工作流程

**每日专注任务**：`GET /tasks?focus_today=true` 可查看今日的专注任务列表。可以通过 `PATCH /tasks/:id { "focus_today": true }` 来切换专注任务。

**目标跟踪**：创建目标并通过 `goal_id` 关联任务；使用 `GET /goals/:id` 查看目标进度。

**会议准备**：`GET /people/:id` + `GET /tasks?person_id=:id` 可在会议前查看相关人员的任务信息。

有关完整的 API 详细信息，请参阅 [references/api.md](references/api.md)。