---
name: bkmrk
description: 专为开发者设计的书签管理工具：您可以浏览、搜索、分类和管理由 AI 分析后的资源库。您可以提交 URL、分配项目、触发深度分析，并执行分阶段的操作。
homepage: https://bkmrkapp.com
---
# BKMRK — 书签智能工具

您已连接到用户的 BKMRK 库。BKMRK 使用 Claude AI 对书签进行分析，并结合用户的编码项目来评估书签的相关性，同时提供实现建议。

**术语说明：** 流程状态分为 `new`（新）、`staged`（待处理）和 `done`（已完成）。在指代用户接下来需要处理的项时，请始终使用 “staged”（而非 “queue” 或 “queued”）。

## 分析内容类型

BKMRK 可对所有类型的源内容进行深度分析：

- **推文**：获取推文的完整文本及其中的所有链接。
- **X 文章**：通过 X API 提取文章的全部内容（而不仅仅是标题）。
- **讨论串**：从所有回复中重建讨论串的文本，并提取讨论串中每条推文中的链接（而不仅仅是第一条推文中的链接）。
- **YouTube 视频**：提取完整的视频字幕（自动生成或手动添加），无论视频长度如何都会进行完整分析。
- **博客文章/新闻报道**：通过 trafilatura 提取文章的全部内容，并进行完整分析。
- **GitHub 仓库**：获取 README 文件和仓库元数据。
- **任何 URL**：通过 API 提交后，系统会自动获取并分析这些内容。

所有内容都会被发送给 Claude 进行分析——无论是长篇文章、2 小时的播客转录内容，还是完整的 X 文章内容，都会进行针对具体项目的深度分析。

## 认证

所有请求都需要在请求头中包含用户的 BKMRK API 密钥：

```
X-API-Key: {BKMRK_API_KEY}
```

API 密钥可以在 [https://bkmrkapp.com/settings](https://bkmrkapp.com/settings) 的 “Your API Key” 部分找到。

## 功能介绍

### 浏览书签库

您可以使用过滤器浏览已分析的书签库。系统会显示书签的评分、状态、针对每个项目的分析结果以及可执行的操作提示。这些功能可用于分类、浏览和流程管理。

```
GET https://bkmrkapp.com/api/agent/library
X-API-Key: {BKMRK_API_KEY}
```

所有查询参数都是可选的：
- `status`：按卡片状态过滤：`new`（新）、`staged`（待处理）、`done`（已完成）、`trashed`（已删除）。
- `project_id`：按项目 UUID 过滤。
- `min_score`：最低相关性分数（例如 `7`）。
- `priority`：按优先级过滤：`high`（高）、`medium`（中）、`low`（低）。
- `source`：按来源过滤：`sync`（来自 X 书签）或 `agent`（通过 API 提交）。
- `limit`：最大返回结果数量（默认：50，最大：100）。
- `include_project_analyses`：是否包含针对每个项目的深度分析数据（默认：`true`）。

示例：
- 查找未处理的高价值书签：`?status=new&min_score=7`
- 查找特定项目的待处理书签：`?status=staged&project_id=<uuid>`
- 仅查看通过 API 提交的书签：`?source=agent`
- 查找需要清理的低优先级书签：`?priority=low&min_score=0`

### 搜索书签库

可以通过标题、说明、操作内容、作者和链接进行关键词搜索。此功能可用于查找特定内容。

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

所有字段都是可选的。搜索结果会按相关性分数排序。

### 管理书签状态

您可以更改书签在流程中的状态：从 `new`（新）变为 `staged`（待处理）或 `done`（已完成），或者将书签标记为已删除/恢复。

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

有效状态：`new`（新）、`staged`（待处理）、`done`（已完成）、`trashed`（已删除）。请使用准确的状态值（例如使用 `staged` 而不是 “stage”，`trashed` 而不是 “trash”）。您还可以为任何书签设置 `"channel": "channel-name"`。

### 管理项目

您可以列出、创建和更新书签所关联的编码项目。

**列出项目：**
```
GET https://bkmrkapp.com/api/projects
X-API-Key: {BKMRK_API_KEY}
```

系统会返回所有项目的 ID、名称、描述和技术栈等信息。这些信息可用于获取其他 API 调用的项目 UUID。

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

您可以触发对特定项目的书签进行深度重新分析。系统会使用 Claude Sonnet 进行详细分析。分析结果会立即返回（202），并在 1-2 分钟内显示在书签库中。

```
POST https://bkmrkapp.com/api/reanalyze
Content-Type: application/json
X-API-Key: {BKMRK_API_KEY}

{
  "bookmark_id": "<uuid>",
  "project_ids": ["<project-uuid>"]
}
```

系统会返回 `job_id`、`credits_used` 和 `credits_remaining`。每个项目使用 1 个分析信用点。免费用户每月可使用 25 个信用点，Pro 用户每月可使用 100 个信用点，Scale 用户每月可使用 500 个信用点。

### 了解项目概况

您可以查看用户的仪表板摘要，包括项目列表、订阅等级、统计数据以及书签数量等信息。

```
GET https://bkmrkapp.com/api/context
X-API-Key: {BKMRK_API_KEY}
```

系统会返回项目列表、订阅等级、总书签数量、按状态分类的书签数量以及同步历史记录。

### 提交 URL

您可以将任何 URL 提交到库中以进行 AI 分析。支持推文、YouTube 视频、GitHub 仓库、博客文章和任何网页。系统会在后台进行内容增强和分析。

```
POST https://bkmrkapp.com/api/agent/submit
Content-Type: application/json
X-API-Key: {BKMRK_API_KEY}

{
  "url": "https://example.com/interesting-article"
}
```

支持的 URL 类型：
- **推文链接**（如 `x.com/user/status/123`）：获取推文的完整数据、讨论串上下文及所有链接。
- **YouTube 链接**：提取视频的完整字幕以供分析。
- **其他任何 URL**：提取文章的全部内容、标题和图片。

您可以选择包含 `"project_ids": ["<uuid>"]` 以针对特定项目进行分析。分析结果会包含 `bookmark_id` 和 `job_id`，并在 1-2 分钟内显示。

免费用户每月可使用 5 个分析信用点，Pro 用户每月可使用 50 个信用点，Scale 用户每月可使用 200 个信用点。

### 创建账户（入门流程）

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
1. `GET /api/context` — 检查当前状态。
2. `GET /api/agent/library?status=new&min_score=7` — 查找高价值但未处理的书签。
3. `POST /api/status` — 将符合条件的书签标记为待处理状态，将无关内容删除。

### 深入分析项目
1. `GET /api/projects` — 获取项目 UUID。
2. `GET /api/agent/library?project_id=<uuid>` — 查看与该项目相关的内容。
3. `POST /api/reanalyze` — 对缺乏项目特定数据的书签进行深度分析。
4. `GET /api/agent/library?project_id=<uuid>` — 查看分析后的结果。

### 批量清理
1. `GET /api/agent/library?priority=low&min_score=0` — 查找低价值书签。
2. `POST /api/status` 并设置 `status="trashed"` — 删除这些书签。

### 提交并验证分析结果
1. `POST /api/agent/submit` 提交 URL 以进行分析。
2. 等待 1-2 分钟。
3. `POST /api/agent/query` 并传入 `{"q": "hostname"` 以验证分析是否已完成。

## 完整的 API 文档

如需查看完整的 API 端点文档、定价等级和功能信息，请参考：

```
GET https://bkmrkapp.com/agent.json
```