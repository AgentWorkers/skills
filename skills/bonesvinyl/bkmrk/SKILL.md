---
name: bkmrk
description: 专为开发者设计的书签功能：您可以浏览、搜索、分类和管理由 AI 分析后的资源库。您可以提交 URL、分配项目、触发深入分析，并执行分阶段执行的操作。
homepage: https://bkmrkapp.com
---
# BKMRK — 书签智能管理工具

您已连接到用户的 BKMRK 库。BKMRK 利用 Claude AI 对书签进行分析，并将其与用户的编码项目进行对比，评估书签的相关性并生成实施建议。

**术语说明：** 流程状态分为 `new`（新）、`staged`（已准备）和 `done`（已完成）。在指代用户接下来需要处理的项目时，请始终使用 “staged” 而不是 “queue” 或 “queued”。

## 分析内容类型

BKMRK 可对所有类型的来源内容进行深度分析：

- **推文**：获取推文的完整文本及其中的所有 URL。
- **X 文章**：通过 X API 提取文章的全部内容（而不仅仅是标题）。
- **讨论帖**：从所有回复中重建讨论帖的文本，并提取帖子中每条推文中的所有 URL（而不仅仅是第一条推文）。
- **YouTube 视频**：提取完整的视频字幕（无论是自动生成的还是手动添加的），无论视频长度如何都会进行详细分析。
- **博客文章/新闻报道**：通过 trafilatura 提取文章的全部内容，并进行详细分析。
- **GitHub 仓库**：获取 README 文件和仓库元数据。
- **任何 URL**：通过 API 提交后，系统会自动获取并分析该 URL 的内容。

所有分析内容都会被发送给 Claude 进行处理——无论是长篇文章、2 小时的播客转录内容，还是完整的 X 文章内容，都会被进行针对具体项目的深度分析。

## 认证

所有请求都需要在请求头中包含用户的 BKMRK API 密钥：

```
X-API-Key: {BKMRK_API_KEY}
```

API 密钥可在 [https://bkmrkapp.com/settings](https://bkmrkapp.com/settings) 的 “Your API Key” 部分获取。

## 功能介绍

### 浏览书签库

您可以使用过滤器浏览已分析的书签库。系统会显示书签的评分、状态、针对每个项目的分析结果以及可执行的操作提示。这些功能可用于分类、浏览和管理书签。

```
GET https://bkmrkapp.com/api/agent/library
X-API-Key: {BKMRK_API_KEY}
```

所有查询参数都是可选的：
- `bookmark_id`：通过 UUID 获取特定的书签（用于检查提交后的状态）。
- `status`：按书签状态过滤：`new`（新）、`staged`（已准备）、`done`（已完成）、`trashed`（已删除）。
- `project_id`：按项目 UUID 过滤书签。
- `min_score`：最低相关性分数（例如：`7`）。
- `priority`：按优先级过滤：`high`（高）、`medium`（中）、`low`（低）。
- `source`：按来源过滤：`sync`（来自 X 书签）或 `agent`（通过 API 提交）。
- `limit`：最大返回结果数量（默认：50，最大：100）。
- `include_project_analyses`：是否包含针对每个项目的详细分析数据（默认：`true`）。

示例：
- 查找未处理的高价值书签：`?status=new&min_score=7`
- 查找为特定项目准备的书签：`?status=staged&project_id=<uuid>`
- 仅显示通过 API 提交的书签：`?source=agent`
- 查找需要清理的低优先级书签：`?priority=low&min_score=0`

### 搜索书签库

可以通过标题、说明、操作内容、作者和 URL 进行关键词搜索。此功能可帮助您快速找到所需内容。

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

所有字段都是可选的。搜索结果会按照相关性分数排序显示。

### 管理书签状态

您可以调整书签在流程中的状态：从 `new`（新）变为 `staged`（已准备），或直接删除/恢复书签。

```
POST https://bkmrkapp.com/api/status
Content-Type: application/json
X-API-Key: {BKMRK_API_KEY}
```

单个书签的操作：
```json
{ "bookmark_id": "<uuid>", "status": "staged" }
```

批量更新书签状态：
```json
{ "items": [
    { "bookmark_id": "<uuid>", "status": "done" },
    { "bookmark_id": "<uuid>", "status": "trashed" }
] }
```

有效状态：`new`（新）、`staged`（已准备）、`done`（已完成）、`trashed`（已删除）（请使用准确的状态值，例如使用 “staged” 而不是 “stage”，“trashed” 而不是 “trash”）。您还可以为任何书签设置 “channel” 属性。

### 管理项目

您可以列出、创建和更新书签所关联的编码项目。

**列出项目：**
```
GET https://bkmrkapp.com/api/projects
X-API-Key: {BKMRK_API_KEY}
```

系统会返回所有项目的 ID、名称、描述和技术栈等信息。这些信息可用于后续的操作。

**创建项目：**
```
POST https://bkmrkapp.com/api/projects
Content-Type: application/json
X-API-Key: {BKMRK_API_KEY}

{
  "name": "My Project",
  "description": "What this project does",
  "tech_stack": ["React", "Node.js"],
  "focus_areas": ["performance", "auth"],
  "analysis_persona": "You are a senior React developer focused on performance optimization and server components.",
  "scoring_bias": "Prioritize: React Server Components, streaming SSR, bundle optimization. Deprioritize: Vue, Angular, jQuery."
}
```

可选的项目配置字段：
- `analysis_persona`：在分析书签时，向 Claude 的系统提示中注入的角色描述。这有助于使分析更具针对性。例如：“您是一位专注于 SwiftUI 模式、性能优化以及音乐应用中 Claude AI 集成的高级 iOS 开发者。”
- `scoring_bias`：指定该项目应重点关注或优先处理的主题。例如：“优先处理：SwiftUI、条形码扫描、黑胶音乐、AI 功能；优先级较低的主题：Web 框架、营销工具。”

**更新项目：**
```
PUT https://bkmrkapp.com/api/projects
Content-Type: application/json
X-API-Key: {BKMRK_API_KEY}

{
  "id": "<project-uuid>",
  "description": "Updated description",
  "tech_stack": ["React", "Next.js"],
  "analysis_persona": "You are a full-stack Next.js engineer...",
  "scoring_bias": "Prioritize: App Router, Server Actions, edge runtime."
}
```

### 深度分析

您可以触发对特定项目的书签进行重新分析。系统会使用 Claude Sonnet 进行深入分析。分析结果会立即返回（202 个指标），并在 1-2 分钟内显示在书签库中。

```
POST https://bkmrkapp.com/api/reanalyze
Content-Type: application/json
X-API-Key: {BKMRK_API_KEY}

{
  "bookmark_id": "<uuid>",
  "project_ids": ["<project-uuid>"]
}
```

系统会返回 `job_id`、`credits_used` 和 `credits_remaining`。每个项目的分析消耗 1 个信用点。免费用户每月可使用 25 个信用点，Pro 用户每月可使用 100 个信用点，Scale 用户每月可使用 500 个信用点。

### 了解项目概况

您可以查看用户的仪表板摘要，包括项目列表、订阅等级、统计数据和书签数量等信息。

```
GET https://bkmrkapp.com/api/context
X-API-Key: {BKMRK_API_KEY}
```

系统会返回项目列表、订阅等级、总书签数量、按状态分类的书签数量以及同步历史记录。

### 提交 URL

您可以将任何 URL 提交到库中进行 AI 分析。支持推文、YouTube 视频、GitHub 仓库、博客文章和任何网页。系统会在后台对这些内容进行丰富处理和分析。

```
POST https://bkmrkapp.com/api/agent/submit
Content-Type: application/json
X-API-Key: {BKMRK_API_KEY}

{
  "url": "https://example.com/interesting-article"
}
```

支持的 URL 类型：
- **推文 URL**（例如：`x.com/user/status/123`）：获取完整的推文数据、讨论帖上下文及其中的所有 URL。
- **YouTube URL**：提取完整的视频字幕用于分析。
- **其他 URL**：提取文章的全部内容、标题和图片。

您可以选择包含 `project_ids` 参数（例如：`["<uuid>"]`），以便针对特定项目进行分析。分析结果会包含 `bookmark_id` 和 `job_id`，并在 1-2 分钟内显示。

提交操作会计入您的每月书签使用量（Pro 用户每月 200 个信用点，Scale 用户每月 500 个信用点）。此功能需要付费订阅。

### 创建账户（入门流程）

如果用户尚未拥有 BKMRK 账户：

```
POST https://bkmrkapp.com/api/agent/onboard
Content-Type: application/json

{
  "email": "user@example.com",
  "consent": true
}
```

系统会立即生成一个 API 密钥。无需使用 OAuth 认证。

## 示例工作流程

### 日常任务管理
1. `GET /api/context` — 查看当前系统状态。
2. `GET /api/agent/library?status=new&min_score=7` — 查找未处理的高价值书签。
3. `POST /api/status` — 将符合条件的书签标记为 “已准备”，删除无关内容。

### 深入分析项目
1. `GET /api/projects` — 获取项目的 UUID。
2. `GET /api/agent/library?project_id=<uuid>` — 查看与该项目相关的内容。
3. `POST /api/reanalyze` — 对缺少项目特定信息的书签进行深度分析。
4. `GET /api/agent/library?project_id=<uuid>` — 查看分析后的结果。

### 批量清理
1. `GET /api/agent/library?priority=low&min_score=0` — 查找低价值书签。
2. `POST /api/status` 并设置 `status` 为 `trashed` — 删除这些书签。

### 提交和分析结果
1. `POST /api/agent/submit` 并提交一个 URL — 系统会返回 `bookmark_id`。
2. `GET /api/agent/library?bookmark_id=<uuid>` — 查看书签的状态：
   - 如果状态显示为 “processing”（处理中），请等待 30-60 秒后重试。
   - 如果 `items` 数组中包含结果，系统会向用户显示书签的评分、分析结果及后续操作建议。

## 完整的 API 文档

如需查看完整的 API 端点文档、定价等级和功能详情，请参阅：

```
GET https://bkmrkapp.com/agent.json
```