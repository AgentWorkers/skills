---
name: bkmrk
description: 专为开发者设计的书签功能：您可以浏览、搜索、分类和管理由 AI 分析后的资源库。提交 URL、分配项目、触发深度分析，并执行分阶段的操作。
homepage: https://bkmrkapp.com
---
# BKMRK — 书签智能管理工具

您已连接到用户的 BKMRK 库。BKMRK 利用 Claude AI 对书签进行分析，并根据用户的编码项目来评估书签的相关性，同时提供实现建议。

**术语说明：**  
流程状态分为 `new`（新建）、`staged`（待处理）和 `done`（已完成）。在指代用户接下来需要处理的项时，请始终使用 “staged”（而非 “queue” 或 “queued”）。  

## 认证  

所有请求都需要在请求头中包含用户的 BKMRK API 密钥：  
```
X-API-Key: {BKMRK_API_KEY}
```  

API 密钥可在 [https://bkmrkapp.com/settings](https://bkmrkapp.com/settings) 的 “Your API Key” 部分获取。  

## 功能介绍  

### 浏览书签库  

您可以使用过滤器浏览已分析的书签库。系统会显示书签的评分、状态、项目分析结果以及可执行的操作提示，便于您进行分类、查找和流程管理。  
```
GET https://bkmrkapp.com/api/agent/library
X-API-Key: {BKMRK_API_KEY}
```  

所有查询参数均为可选：  
- `status`：按书签状态过滤（`new`、`staged`、`done`、`trashed`）  
- `project_id`：按项目 UUID 过滤  
- `min_score`：最低相关性得分（例如 `7`）  
- `priority`：按优先级过滤（`high`、`medium`、`low`）  
- `source`：按来源过滤（`sync`：来自外部书签；`agent`：通过 API 提交）  
- `limit`：最大返回结果数量（默认：50，上限：100）  
- `include_project_analyses`：是否包含项目级别的详细分析数据（默认：`true`）  

示例：  
- 查找未处理的高价值书签：`?status=new&min_score=7`  
- 查找特定项目的待处理书签：`?status=staged&project_id=<uuid>`  
- 仅查看通过 API 提交的书签：`?source=agent`  
- 清理低优先级的书签：`?priority=low&min_score=0`  

### 搜索书签库  

支持在书签的标题、说明、操作内容、作者和 URL 中进行关键词搜索。  
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
所有字段均为可选，结果按相关性得分排序。  

### 管理书签状态  

您可以调整书签在流程中的状态（`new` → `staged` → `done`），或将其删除/恢复。  
```
POST https://bkmrkapp.com/api/status
Content-Type: application/json
X-API-Key: {BKMRK_API_KEY}
```  

**单个书签操作：**  
```json
{ "bookmark_id": "<uuid>", "status": "staged" }
```  
**批量更新：**  
```json
{ "items": [
    { "bookmark_id": "<uuid>", "status": "done" },
    { "bookmark_id": "<uuid>", "status": "trashed" }
] }
```  
有效状态：`new`、`staged`、`done`、`trashed`（请使用确切的状态值，例如使用 “staged” 而非 “stage”，“trashed” 而非 “trash”）。您还可以为任意书签设置 `"channel": "channel-name"`。  

### 管理项目  

您可以列出、创建或更新书签所关联的编码项目。  

**列出项目：**  
```
GET https://bkmrkapp.com/api/projects
X-API-Key: {BKMRK_API_KEY}
```  
系统会返回所有项目的 ID、名称、描述和技术栈信息，便于您获取项目 UUID 以进行其他操作。  

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

您可以针对特定项目触发书签的深度分析，使用 Claude Sonnet 进行全面分析。分析结果会立即返回（202），并在 1-2 分钟内显示在书签库中。  
```
POST https://bkmrkapp.com/api/reanalyze
Content-Type: application/json
X-API-Key: {BKMRK_API_KEY}

{
  "bookmark_id": "<uuid>",
  "project_ids": ["<project-uuid>"]
}
```  
系统会返回 `job_id`、`credits_used` 和 `credits_remaining`；每个项目消耗 1 个分析信用点。使用限制如下：免费用户每月 25 个信用点，Pro 用户每月 100 个信用点，Scale 用户每月 500 个信用点。  

### 了解项目详情  

您可以查看用户的仪表板摘要，包括项目列表、订阅等级、统计数据和书签数量等信息。  
```
GET https://bkmrkapp.com/api/context
X-API-Key: {BKMRK_API_KEY}
```  
系统会返回项目列表、订阅等级、总书签数、按状态分类的书签数量以及同步历史记录。  

### 提交 URL  

您可以将任何 URL 提交到库中以便进行 AI 分析。系统会在后台对其进行处理和分析。  
```
POST https://bkmrkapp.com/api/agent/submit
Content-Type: application/json
X-API-Key: {BKMRK_API_KEY}

{
  "url": "https://example.com/interesting-article"
}
```  
可选参数 `project_ids`：`["<uuid>"]` 可用于指定分析项目；系统会返回包含 `bookmark_id` 和 `job_id` 的分析结果（1-2 分钟内显示）。使用限制如下：免费用户每月 5 个信用点，Pro 用户每月 50 个信用点，Scale 用户每月 200 个信用点。  

### 创建账户（新用户注册）  

如果用户尚未拥有 BKMRK 账户：  
```
POST https://bkmrkapp.com/api/agent/onboard
Content-Type: application/json

{
  "email": "user@example.com",
  "consent": true
}
```  
系统会立即生成 API 密钥，无需 OAuth 验证。  

## 示例代理工作流程  

### 日常任务处理  
1. `GET /api/context` — 查看当前状态  
2. `GET /api/agent/library?status=new&min_score=7` — 查找未处理的高价值书签  
3. `POST /api/status` — 将符合条件的书签标记为待处理状态，删除无关内容  

### 深入分析项目  
1. `GET /api/projects` — 获取项目 UUID  
2. `GET /api/agent/library?project_id=<uuid>` — 查看与该项目相关的内容  
3. `POST /api/reanalyze` — 对缺少项目级分析数据的书签进行深度分析  
4. `GET /api/agent/library?project_id=<uuid>` — 查看分析后的结果  

### 批量清理  
1. `GET /api/agent/library?priority=low&min_score=0` — 查找低价值的书签  
2. `POST /api/status` 并设置 `status="trashed"` — 删除这些书签  

### 提交并验证分析结果  
1. `POST /api/agent/submit` 提交待分析的 URL  
2. 等待 1-2 分钟  
3. `POST /api/agent/query` 并传入 `{"q": "hostname"` 以验证分析是否已完成  

## 完整的 API 文档  

如需查看完整的 API 端点文档、定价等级和功能信息，请参阅：  
```
GET https://bkmrkapp.com/agent.json
```