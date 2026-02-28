---
name: bkmrk
description: 专为开发者设计的书签功能：您可以浏览、搜索、分类和管理由 AI 分析后的资源库。提交 URL、分配任务、触发深度分析，并执行分阶段执行的操作。
homepage: https://bkmrkapp.com
---
# BKMRK — 书签智能管理系统

您已连接到用户的 BKMRK 库。BKMRK 使用 Claude AI 对书签进行分析，并根据用户的编码项目来评估书签的相关性，同时提供实现建议。

## 认证

所有请求都需要在请求头中包含用户的 BKMRK API 密钥：

```
X-API-Key: {BKMRK_API_KEY}
```

API 密钥可以在 [https://bkmrkapp.com/settings](https://bkmrkapp.com/settings) 的 “您的 API 密钥” 部分获取。

## 您可以执行的操作

### 浏览书签库

您可以使用过滤器来浏览已分析的书签库。系统会返回书签的评分、状态、项目分析结果以及可执行的操作提示，这些信息可用于分类、浏览和项目管理。

```
GET https://bkmrkapp.com/api/agent/library
X-API-Key: {BKMRK_API_KEY}
```

所有查询参数都是可选的：
- `status` — 按书签状态过滤：`new`（新建）、`staged`（待处理）、`done`（已完成）、`trashed`（已删除）
- `project_id` — 按项目 UUID 过滤
- `min_score` — 最低相关性评分（例如：`7`）
- `priority` — 按优先级过滤：`high`（高）、`medium`（中）、`low`（低）
- `source` — 按来源过滤：`sync`（来自其他书签源）或 `agent`（通过 API 提交）
- `limit` — 最大返回结果数量（默认：50，最大：100）
- `include_project_analyses` — 是否包含每个项目的详细分析数据（默认：`true`）

示例：
- 查找未处理的高价值书签：`?status=new&min_score=7`
- 查找特定项目的待处理书签：`?status=staged&project_id=<uuid>`
- 仅查看通过 API 提交的书签：`?source=agent`
- 查找需要清理的低优先级书签：`?priority=low&min_score=0`

### 在书签库中搜索

您可以按书签的标题、说明、操作内容、作者或 URL 进行关键词搜索。这有助于快速找到所需的内容。

```
POST https://bkmrkapp.com/api/agent/query
Content-Type: application/json
X-API-Key: {BKMRK_API_KEY}

{
  "q": "search terms",
  "project": "ProjectName",
  "priority": "high",
  "status": "new",
  "limit": 10
}
```

所有字段都是可选的。搜索结果会按照相关性评分进行排序。

### 管理书签状态

您可以更改书签的状态：从新建（new）变为待处理（staged），或从待处理变为已完成（done），也可以将书签删除或恢复。

```
POST https://bkmrkapp.com/api/status
Content-Type: application/json
X-API-Key: {BKMRK_API_KEY}
```

单个书签的操作：
```json
{ "bookmark_id": "<uuid>", "status": "staged" }
```

批量更新：
```json
{ "items": [
    { "bookmark_id": "<uuid>", "status": "done" },
    { "bookmark_id": "<uuid>", "status": "trashed" }
] }
```

有效状态：`new`、`staged`、`done`、`trashed`（请使用准确的状态值，例如使用 “staged” 而不是 “stage”，“trashed” 而不是 “trash”）。您还可以为任何书签设置 `"channel": "channel-name"`。

### 管理项目

您可以列出、创建和更新书签所关联的编码项目。

**列出项目：**
```
GET https://bkmrkapp.com/api/projects
X-API-Key: {BKMRK_API_KEY}
```

系统会返回所有项目的 ID、名称、描述和技术栈信息。您可以使用这些信息来获取项目的 UUID，以便进行其他操作。

**创建项目：**
```
POST https://bkmrkapp.com/api/projects
Content-Type: application/json
X-API-Key: {BKMRK_API_KEY}

{
  "name": "My Project",
  "description": "What this project does",
  "tech_stack": ["React", "Node.js"],
  "focus_areas": ["performance", "auth"]
}
```

**更新项目：**
```
PUT https://bkmrkapp.com/api/projects
Content-Type: application/json
X-API-Key: {BKMRK_API_KEY}

{
  "id": "<project-uuid>",
  "description": "Updated description",
  "tech_stack": ["React", "Next.js"]
}
```

### 深度分析

您可以触发对特定项目的书签进行深度分析。系统会使用 Claude Sonnet 进行详细分析，并立即返回分析结果（202）。分析结果将在 1-2 分钟内显示在书签库中。

```
POST https://bkmrkapp.com/api/reanalyze
Content-Type: application/json
X-API-Key: {BKMRK_API_KEY}

{
  "bookmark_id": "<uuid>",
  "project_ids": ["<project-uuid>"]
}
```

系统会返回 `job_id`、`credits_used` 和 `credits_remaining` 的信息。每个项目的分析费用为 1 个信用点。免费用户每月可使用 25 个信用点，Pro 用户每月可使用 100 个信用点，Scale 用户每月可使用 500 个信用点。

### 了解项目概况

您可以查看用户的仪表板摘要，包括项目列表、订阅层级、统计数据以及书签库的使用情况。

```
GET https://bkmrkapp.com/api/context
X-API-Key: {BKMRK_API_KEY}
```

系统会返回项目列表、订阅层级、总书签数量、按状态分类的书签数量以及同步历史记录。

### 提交 URL

您可以将任何 URL 提交到书签库进行 AI 分析。系统会在后台对这些 URL 进行丰富处理和分析。

```
POST https://bkmrkapp.com/api/agent/submit
Content-Type: application/json
X-API-Key: {BKMRK_API_KEY}

{
  "url": "https://example.com/interesting-article"
}
```

您可以选择包含 `["project_ids": ["<uuid>"]` 参数，以便针对特定项目进行分析。分析结果会包含 `bookmark_id` 和 `job_id`，并在 1-2 分钟内显示。

免费用户每月可使用 5 个信用点，Pro 用户每月可使用 50 个信用点，Scale 用户每月可使用 200 个信用点。

### 创建账户（新用户注册）

如果用户还没有 BKMRK 账户：

```
POST https://bkmrkapp.com/api/agent/onboard
Content-Type: application/json

{
  "email": "user@example.com",
  "consent": true
}
```

系统会立即生成一个 API 密钥。无需使用 OAuth 认证。

## 示例代理工作流程

### 日常任务处理
1. `GET /api/context` — 查看当前状态
2. `GET /api/agent/library?status=new&min_score=7` — 查找高价值但未处理的书签
3. `POST /api/status` — 将符合条件的书签标记为待处理状态，将无关的书签删除

### 深入分析项目
1. `GET /api/projects` — 获取项目的 UUID
2. `GET /api/agent/library?project_id=<uuid>` — 查看与该项目相关的内容
3. `POST /api/reanalyze` — 对缺少项目特定分析数据的书签进行深度分析
4. `GET /api/agent/library?project_id=<uuid>` — 查看分析后的结果

### 批量清理
1. `GET /api/agent/library?priority=low&min_score=0` — 查找低价值的书签
2. `POST /api/status` 并设置 `status="trashed"` — 删除这些书签

### 提交并验证分析结果
1. `POST /api/agent/submit` 并提交需要分析的 URL
2. 等待 1-2 分钟
3. `POST /api/agent/query` 并传入 `{"q": "hostname"` 以验证分析是否已完成

## 完整的 API 文档

有关所有端点的详细文档、定价层级和功能信息，请参阅：

```
GET https://bkmrkapp.com/agent.json
```