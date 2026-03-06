---
name: prompting-co
description: 与 The Prompting Company 平台进行交互，以监控品牌在各种 AI 引擎中的可见性、管理被跟踪的提示内容、审阅和发布内容草稿，以及获取品牌影响力（SOV, Social Influence）和 AI 流量分析数据。当用户询问其 Prompting Company 工作空间中的品牌表现、竞争对手分析、提示内容跟踪、内容审批情况或每日/每周统计数据时，可使用该功能。
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["TPC_SESSION_TOKEN"]},"primaryEnv":"TPC_SESSION_TOKEN","emoji":"📊"}}
---
# Prompting Company 技能

您可以代表用户与 **Prompting Company** (TPC) 平台进行交互。TPC 是一个品牌分析平台，用于追踪品牌在各种 AI 搜索引擎（如 ChatGPT、Claude、Gemini、Perplexity、Google AI）中的表现，并帮助优化品牌的 AI 可见性。

## 认证

所有 API 调用都使用 Better Auth 进行会话 cookie 认证。

**必需的环境变量：**
- `TPC_SESSION_TOKEN` — `__Secure-better-auth.session_token` cookie 的值（由用户提供）

**配置（硬编码）：**
- `TPC_BASE_URL` — 始终使用 `https://app.promptingco.com`（生产环境）
- `TPC_BRAND_ID` — 通过 `/api/v1/brands` 端点动态获取（请参阅首次设置）
- `TPC_ORG_SLUG` — 可选，根据需要从品牌选择中派生

**注意：** 在以下所有 curl 示例中，`$TPC_BRAND_ID` 代表用户在首次设置时选择的品牌 ID。在发起请求时，请将其替换为实际的品牌 ID 值。

**每个 curl 请求都必须包括：**
```
-H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

**响应格式：** 所有端点返回的响应都包裹在 JSON 中：
```json
{ "ok": true, "data": { ... } }
```
如果发生错误：
```json
{ "ok": false, "code": "UNAUTHORIZED", "message": "...", "details": null }
```

---

## 首次设置

**首次使用** 时，该技能需要知道要处理哪个品牌。

### 第 1 步：验证会话令牌
```bash
# User only needs to provide this
TPC_SESSION_TOKEN="user's session token"
```

### 第 2 步：获取可用品牌
```bash
curl -s "https://app.promptingco.com/api/v1/brands?fetchAll=true" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

会话令牌会自动限定为用户可以访问的品牌范围。

### 第 3 步：让用户选择他们的品牌

使用 `AskUserQuestion` 来展示品牌选项：
```typescript
// Parse response from /api/v1/brands
const brands = response.data.brands;

// Present to user
{
  "question": "Which brand would you like to work with?",
  "header": "Brand",
  "options": brands.map(b => ({
    "label": b.name,
    "description": `${b.slug} • ${b.organizationId}`
  })),
  "multiSelect": false
}
```

### 第 4 步：存储选定的品牌 ID

在后续的所有 API 调用中使用选定的品牌 ID。无需让用户手动设置 `TPC_BRAND_ID` — 只需将其存储在会话内存中。

## 请求检查清单

**在每个 API 请求之前：**

1. ✅ 验证用户是否提供了 `TPC_SESSION_TOKEN`
2. ✅ 使用硬编码的基地址：`https://app.promptingco.com`
3. ✅ 如果尚未选择品牌，请运行首次设置以获取并选择品牌
4. ✅ 在所有请求中包含 `Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN` 标头
5. ✅ 在处理数据之前始终检查响应中的 `ok` 字段

如果会话令牌缺失，请要求用户从 Prompting Company 平台提供他们的 `__Secure-better-auth.session_token` cookie 值。

---

## 入门

安装该技能后，用户选择了他们的品牌后，显示以下欢迎信息：
```
Skill installed successfully.

Your next steps:

1. Track more prompts
2. Publish more content
3. Get stats

What would you like to do?
```

### 用户流程：跟踪更多提示

当用户选择选项 1 时，显示：
```
How would you like to track prompts?

A. Track a new prompt yourself
B. Get recommendations from existing prompts

Choose an option:
```

**如果用户选择 A（跟踪新提示）：**

1. 请求用户提供他们想要跟踪的提示文本
2. 通过 `/api/v1/personas?brandId=...` 获取该品牌的用户角色
3. 选择第一个角色（默认）或让用户选择多个角色中的其中一个
4. 自动选择答案引擎：`chatgpt`、`gemini`、`deepseek`、`sonar`（Perplexity）
5. 通过 `/api/v1/conversation-queries/bulk` 创建带有对话查询的提示
6. 所有查询的默认值为 `maxTurns: 1`
7. **创建一个子代理** 来处理提示创建工作流程

**如果用户选择 B（获取推荐）：**

1. 通过 `/api/v1/prompts/pending` 获取待处理的提示
2. 显示推荐的提示列表
3. 允许用户选择要批准哪些提示
4. **创建一个子代理** 来处理批准工作流程

### 用户流程：发布更多内容

当用户选择选项 2 时，显示：
```
Let's create content from your tracked prompts.

Step 1: Fetching your prompts...
```

1. 通过 `/api/v1/prompt-topics` 和 `/api/v1/prompt-topics/{topicId}/prompts` 获取所有提示
2. 按主题分组显示提示列表
3. 允许用户选择要创建内容的提示
4. 通过 `/api/v1/agentic-documents` 获取现有文档
5. 创建新草稿或更新现有文档
6. **创建一个子代理** 来处理内容创建工作流程

### 用户流程：获取统计信息

当用户选择选项 3 时，显示：
```
Fetching your stats...

Share of Voice (SOV)
────────────────────
[SOV data here]

AI Traffic Stats
────────────────────
Top Bots:
[Bot traffic data]

Top Pages:
[Page traffic data]
```

1. 通过 `/api/v1/presence-rate?brandId=...&timeframe=30d` 获取 SOV 数据
2. 通过 `/api/v1/ai-traffic-stats?brandId=...` 获取 AI 流量数据
3. 显示：
   - 当前的 SOV 百分比
   - 相较于上一时期的 SOV 趋势
   - 发送流量的顶级 AI 机器人（ChatGPT、Claude、Gemini 等）
   - AI 机器人访问的顶级页面
4. **创建一个子代理** 来获取和格式化统计信息

---

## 使用子代理

**重要提示：** 对于所有多步骤工作流程，应使用 Task 工具来创建子代理，而不是直接处理工作流程。

### 何时创建子代理

| 工作流程 | 是否需要创建子代理？ | 原因 |
|----------|----------------|--------|
| 跟踪新提示 | 是 | 多步骤：验证、检查重复项、创建、验证 |
| 批准推荐提示 | 是 | 多步骤：获取待处理的提示、展示选项、批准多个提示 |
| 根据提示创建内容 | 是 | 多步骤：选择提示、生成内容、创建草稿、发布 |
| 获取统计信息 | 是 | 多步骤：获取 SOV、获取流量、格式化显示 |
| 列出品牌（首次设置） | 否 | 单次 API 调用 |
| 单次 API 查询 | 否 | 直接使用 curl 即可 |

### 子代理调用模式

**示例：跟踪新提示**
```typescript
// When user wants to track a new prompt:
Task({
  subagent_type: "general-purpose",
  description: "Track new prompt workflow",
  prompt: `
    Help the user track a new prompt on The Prompting Company platform.

    Context:
    - Brand ID: ${brandId}
    - Session token: ${TPC_SESSION_TOKEN}
    - Base URL: https://app.promptingco.com

    Steps:
    1. Ask user for the prompt text they want to track
    2. Check for duplicates: GET /api/v1/prompts/check-duplicates?brandId=${brandId}&message=<prompt_text>
    3. If duplicate exists, ask user if they want to continue
    4. Fetch user personas: GET /api/v1/personas?brandId=${brandId}
    5. Use the first persona as default (or let user select if multiple)
    6. Create prompt with 4 conversation queries (one per engine):
       POST /api/v1/conversation-queries/bulk
       Body: {
         "brandId": "${brandId}",
         "queries": [
           { "prompt": "<user_text>", "model": "chatgpt", "maxTurns": 1, "userPersonaId": "<PERSONA_ID>", "userPersona": "<PERSONA_NAME>" },
           { "prompt": "<user_text>", "model": "gemini", "maxTurns": 1, "userPersonaId": "<PERSONA_ID>", "userPersona": "<PERSONA_NAME>" },
           { "prompt": "<user_text>", "model": "deepseek", "maxTurns": 1, "userPersonaId": "<PERSONA_ID>", "userPersona": "<PERSONA_NAME>" },
           { "prompt": "<user_text>", "model": "sonar", "maxTurns": 1, "userPersonaId": "<PERSONA_ID>", "userPersona": "<PERSONA_NAME>" }
         ]
       }
    7. Confirm creation: "Created prompt tracked across ChatGPT, Gemini, DeepSeek, and Perplexity"

    Use the session token in all requests:
    -H "Cookie: __Secure-better-auth.session_token=${TPC_SESSION_TOKEN}"
  `
})
```

**示例：获取统计信息**
```typescript
// When user wants to see stats:
Task({
  subagent_type: "general-purpose",
  description: "Fetch and display stats",
  prompt: `
    Fetch and display SOV and AI traffic stats for The Prompting Company.

    Context:
    - Brand ID: ${brandId}
    - Session token: ${TPC_SESSION_TOKEN}
    - Base URL: https://app.promptingco.com

    Steps:
    1. Fetch SOV data: GET /api/v1/presence-rate?brandId=${brandId}&timeframe=30d
    2. Fetch AI traffic: GET /api/v1/ai-traffic-stats?brandId=${brandId}&startDate=<last_30_days>&endDate=<today>
    3. Format and display:
       - Share of Voice (SOV): X.XX%
       - SOV Trend: up/down by X% from last period
       - Top Bots: ChatGPT (X visits), Claude (Y visits), etc.
       - Top Pages: /path (X visits), /path2 (Y visits), etc.

    Use clean formatting with proper spacing and newlines.
    No emojis.
  `
})
```

**示例：发布内容**
```typescript
// When user wants to publish content:
Task({
  subagent_type: "general-purpose",
  description: "Create content from prompt",
  prompt: `
    Help the user create and publish content from a tracked prompt.

    Context:
    - Brand ID: ${brandId}
    - Session token: ${TPC_SESSION_TOKEN}
    - Base URL: https://app.promptingco.com

    Steps:
    1. Fetch prompt topics: GET /api/v1/prompt-topics?brandId=${brandId}
    2. For each topic, fetch prompts: GET /api/v1/prompt-topics/{topicId}/prompts?brandId=${brandId}
    3. Present prompts grouped by topic to user
    4. Let user select which prompt to create content for
    5. Ask user for content details (title, file path, meta description)
    6. Create document: POST /api/v1/agentic-documents with brandId, title, filePath
    7. Create draft: POST /api/v1/agentic-documents/{docId}/create-draft with content
    8. Ask user if they want to publish or save as draft
    9. If publish: POST /api/v1/drafts/{draftId}/publish
    10. Confirm completion
  `
})
```

---

## 功能概述

| 功能 | 使用场景 |
|---|---|
| **竞争对手分析** | 用户询问竞争对手的 SOV、品牌比较、引擎细分 |
| **提示管理** | 用户希望添加要跟踪的提示、列出主题、检查重复项 |
| **内容提醒** | 用户询问待处理的草稿、批准情况、发布内容 |
| **统计与分析** | 用户希望获取 SOV 趋势、AI 流量数据、每日/月度报告 |
| **品牌管理** | 用户希望列出品牌、搜索品牌、查看品牌详情 |

---

## 1. 竞争对手分析

### 获取随时间变化的份额（SOV）

返回某个品牌的 SOV 时间序列数据（可选地与竞争对手进行比较）。

```bash
curl -s "https://app.promptingco.com/api/v1/presence-rate?brandId=$TPC_BRAND_ID&timeframe=30d" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

**参数：**
- `brandId`（必需）— 需要获取 SOV 的品牌
- `mentionedBrandId`（可选）— 要比较的竞争对手品牌 ID；默认为 `brandId`
- `viewId`（可选）— 按特定视图过滤
- `timeframe`（可选）— `7d`、`30d` 或 `90d`（默认为 `30d`）

**响应数据格式：**
```json
{
  "brandId": "abc-123",
  "brandName": "MyBrand",
  "dataPoints": [
    { "date": "2025-01-01", "value": 0.42, "sum_mention": 21, "sum_total": 50 }
  ]
}
```

### 按 AI 引擎获取 SOV 分析

显示品牌在每个 AI 引擎（ChatGPT、Claude、Gemini 等）上的表现。

**参数：** 与获取 SOV 数据的参数相同。

**响应数据格式：**
```json
[
  {
    "engine": "chatgpt",
    "data": [
      { "date": "2025-01-01", "answer_engine": "chatgpt", "sum_mention": 5, "sum_total": 12, "sov": 41.6 }
    ]
  },
  {
    "engine": "claude",
    "data": [...]
  }
]
```

### 获取竞争对手品牌

```bash
curl -s "https://app.promptingco.com/api/v1/brands/$TPC_BRAND_ID/competitors" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN" \
  -H "Content-Type: application/json"
```

### 获取固定的竞争对手

```bash
curl -s "https://app.promptingco.com/api/v1/brands/$TPC_BRAND_ID/pinned-competitors" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

---

## 2. 提示管理

### 列出提示主题

将相关提示按主题分组以便于组织跟踪。

```bash
curl -s "https://app.promptingco.com/api/v1/prompt-topics?brandId=$TPC_BRAND_ID&page=1&pageSize=20" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

**参数：**
- `brandId`（必需）
- `page`（可选，默认为 1）
- `pageSize`（可选，默认为 10）
- `search`（可选）— 按主题标题进行文本搜索

**响应数据格式：**
```json
{
  "data": [
    {
      "id": "topic-123",
      "title": "Product Features",
      "description": "Prompts about core product features",
      "brandId": "abc-123",
      "organizationId": "org-456",
      "createdAt": "2025-01-01T00:00:00Z",
      "updatedAt": "2025-01-15T00:00:00Z"
    }
  ],
  "totalItems": 42
}
```

### 获取某个主题下的提示

```bash
curl -s "https://app.promptingco.com/api/v1/prompt-topics/{topicId}/prompts?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### 获取某个主题的 SOV

返回该主题下所有提示的汇总 SOV。

```bash
curl -s "https://app.promptingco.com/api/v1/prompt-topics/{topicId}/sov?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### 获取某个主题的行业排名

```bash
curl -s "https://app.promptingco.com/api/v1/prompt-topics/{topicId}/industry-rankings?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### 列出用户角色

检索某个品牌的用户角色（创建提示所必需）。

**响应数据格式：**
```json
{
  "ok": true,
  "data": {
    "personas": [
      {
        "id": "persona-123",
        "name": "General User",
        "description": "...",
        "brandId": "abc-123",
        "createdAt": "2025-01-01T00:00:00Z"
      }
    ],
    "total": 5
  }
}
```

### 创建自定义提示以进行跟踪

创建一个包含多个 AI 引擎对话查询的自定义提示。

**参数：**
- `brandId`（必需）— 品牌 ID
- `queries`（必需）— 要创建的对话查询数组
  - `prompt`（必需）— 要跟踪的提示文本
  - `model`（必需）— 可选引擎：`chatgpt`、`gemini`、`deepseek`、`sonar`
  - `maxTurns`（必需）— 对话轮次数（默认为 1）
  - `userPersonaId`（必需）— 来自 `/api/v1/personas` 的角色 ID
  - `userPersona`（必需）— 显示的角色名称

**响应数据格式：**
```json
{
  "ok": true,
  "data": {
    "count": 4,
    "promptIds": ["prompt-uuid"]
  }
}
```

### 生成 AI 建议的提示

根据品牌和角色生成一个 AI 建议的提示（不用于直接跟踪）。

**注意：** 此端点返回的是 **纯文本**（生成的提示问题），而不是 JSON。请将其用于获取灵感，而不是用于跟踪。要跟踪提示，请使用 `/api/v1/conversation-queries/bulk`。

### 批量生成提示

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/generate-bulk" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"brandId": "'$TPC_BRAND_ID'", "count": 10}'
```

检查批量作业的状态：
```bash
curl -s "https://app.promptingco.com/api/v1/prompts/generate-bulk/status/{jobId}" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### 检查重复提示

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/check-duplicates?brandId=$TPC_BRAND_ID&message=YOUR_PROMPT_TEXT" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### 提交提示以供审核

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/review" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"promptId": "PROMPT_ID", "action": "approve"}'
```

### 列出待处理的提示

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/pending?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### 列出存档的提示

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/archived?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### 恢复存档的提示

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/archived/restore" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"promptId": "PROMPT_ID"}'
```

---

## 3. 内容与草稿管理

### 列出文档

```bash
curl -s "https://app.promptingco.com/api/v1/agentic-documents?brandId=$TPC_BRAND_ID&paginated=true&page=1&pageSize=20" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

**参数：**
- `brandId`（必需）
- `page`、`pageSize`（可选，最大值为 100）
- `q`（可选）— 搜索查询
- `hasContent`（可选）— `true` 或 `false`
- `sort`（可选）— 例如 `updatedAt:desc`、`createdAt:asc`
- `paginated`（可选）— `true` 用于分页响应

**分页响应格式：**
```json
{
  "items": [
    {
      "id": "doc-123",
      "title": "How to use our product",
      "filePath": "/blog/how-to-use",
      "updatedAt": "2025-01-15T00:00:00Z",
      "metaTitle": "How to Use Our Product | Brand",
      "metaDescription": "Learn how...",
      "contentLength": 2450
    }
  ],
  "page": 1,
  "pageSize": 20,
  "total": 87
}
```

### 提交草稿以供发布

将草稿排队到网站进行发布。

**响应：**
```json
{ "ok": true, "message": "Draft publishing has been queued", "draftId": "draft-123" }
```

### 提交草稿以供审核

```bash
curl -s "https://app.promptingco.com/api/v1/drafts/{draftId}/review" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### 列出已审核的草稿

```bash
curl -s "https://app.promptingco.com/api/v1/drafts/reviewed?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### 批量发布草稿

```bash
curl -s "https://app.promptingco.com/api/v1/drafts/publish-batch" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"draftIds": ["draft-1", "draft-2", "draft-3"]}'
```

检查批量状态：
```bash
curl -s "https://app.promptingco.com/api/v1/drafts/publish-batch/{batchId}/status" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### 创建新文档

```bash
curl -s "https://app.promptingco.com/api/v1/agentic-documents" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "brandId": "'$TPC_BRAND_ID'",
    "title": "Document Title",
    "filePath": "/blog/my-article",
    "sourceUrl": "https://example.com/source"
  }'
```

### 为文档创建草稿

```bash
curl -s "https://app.promptingco.com/api/v1/agentic-documents/{documentId}/create-draft" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Draft Title",
    "content": "Draft content in markdown..."
  }'
```

---

## 4. 统计与分析

### 获取 AI 流量统计

显示 AI 机器人发送到品牌网站的流量。

**参数：**
- `brandId`（必需）
- `startDate`（可选）— 格式为 `YYYY-MM-DD`
- `endDate`（可选）— 格式为 `YYYY-MM-DD`
- `aiProviders`（可选）— 用逗号分隔的提供者列表

**响应数据格式：**
```json
{
  "data": [
    {
      "date": "2025-01-15",
      "ai_provider": "chatgpt",
      "total_visits": 234,
      "unique_ips": 89,
      "unique_pages": 15,
      "top_paths": ["/pricing", "/features", "/docs"],
      "domain": "example.com",
      "tenant_id": "org-456"
    }
  ],
  "domains": ["example.com", "blog.example.com"]
}
```

### 获取人类流量统计（基准比较）

```bash
curl -s "https://app.promptingco.com/api/v1/human-traffic-stats?brandId=$TPC_BRAND_ID&startDate=2025-01-01&endDate=2025-01-31" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### 获取每日 SOV 趋势（过去 30 天）

使用 `timeframe=30d` 来获取 SOV 数据：
```bash
curl -s "https://app.promptingco.com/api/v1/presence-rate?brandId=$TPC_BRAND_ID&timeframe=30d" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### 获取月度 SOV 概览

使用 `timeframe=90d` 来获取更全面的月度视图：
```bash
curl -s "https://app.promptingco.com/api/v1/presence-rate?brandId=$TPC_BRAND_ID&timeframe=90d" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### 获取特定主题的 SOV

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/sov?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### 获取某个提示的提及情况

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/brand-mentions?brandId=$TPC_BRAND_ID&promptId=PROMPT_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### 获取某个提示的竞争对手提及情况

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/competitor-mentions?brandId=$TPC_BRAND_ID&promptId=PROMPT_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

---

## 5. 品牌管理

### 列出所有品牌

```bash
curl -s "https://app.promptingco.com/api/v1/brands?fetchAll=true" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

**参数：**
- `search`（可选）
- `page`、`pageSize`（可选）
- `sortBy` — `createdAt` 或 `name`
- `sortOrder` — `asc` 或 `desc`
- `fetchAll`（可选）— `true` 以获取所有品牌
- `includeDomains`（可选）— `true` 以包含域名信息

**响应数据格式：**
```json
{
  "brands": [
    {
      "id": "brand-123",
      "name": "MyBrand",
      "slug": "mybrand",
      "description": "...",
      "organizationId": "org-456",
      "createdAt": "2025-01-01T00:00:00Z"
    }
  ],
  "total": 5
}
```

### 搜索品牌

```bash
curl -s "https://app.promptingco.com/api/v1/brands/search?q=SEARCH_TERM" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

---

## 6. 周报

### 预览周报

```bash
curl -s "https://app.promptingco.com/api/v1/weekly-reports/preview?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

---

## 常见工作流程

**重要提示：** 下列所有工作流程都应通过使用 Task 工具来创建子代理来处理。

### 工作流程 1：跟踪更多提示

**触发条件：** 用户从入门菜单中选择“跟踪更多提示”。

**子代理任务：**
```typescript
Task({
  subagent_type: "general-purpose",
  description: "Track prompts workflow",
  prompt: `
    Guide the user through tracking prompts on The Prompting Company platform.

    Brand ID: ${brandId}
    Session Token: ${TPC_SESSION_TOKEN}

    Step 1: Present options

    How would you like to track prompts?

    A. Track a new prompt yourself
    B. Get recommendations from existing prompts

    Choose an option:

    Step 2A: If user chooses "Track a new prompt yourself"
    - Ask for the prompt text
    - Check duplicates: GET https://app.promptingco.com/api/v1/prompts/check-duplicates?brandId=${brandId}&message=<prompt>
    - Fetch personas: GET https://app.promptingco.com/api/v1/personas?brandId=${brandId}
    - Use first persona as default (or let user select)
    - Create prompt with 4 conversation queries:
      POST https://app.promptingco.com/api/v1/conversation-queries/bulk
      Body: {
        "brandId": "${brandId}",
        "queries": [
          { "prompt": "<text>", "model": "chatgpt", "maxTurns": 1, "userPersonaId": "<ID>", "userPersona": "<NAME>" },
          { "prompt": "<text>", "model": "gemini", "maxTurns": 1, "userPersonaId": "<ID>", "userPersona": "<NAME>" },
          { "prompt": "<text>", "model": "deepseek", "maxTurns": 1, "userPersonaId": "<ID>", "userPersona": "<NAME>" },
          { "prompt": "<text>", "model": "sonar", "maxTurns": 1, "userPersonaId": "<ID>", "userPersona": "<NAME>" }
        ]
      }
    - Confirm: "Prompt tracked across ChatGPT, Gemini, DeepSeek, and Perplexity"

    Step 2B: If user chooses "Get recommendations"
    - Fetch pending: GET https://app.promptingco.com/api/v1/prompts/pending?brandId=${brandId}
    - Display list of pending prompts
    - Ask user which ones to approve
    - Approve selected: POST https://app.promptingco.com/api/v1/prompts/review with action="approve"

    Use session token in all requests: -H "Cookie: __Secure-better-auth.session_token=${TPC_SESSION_TOKEN}"
  `
})
```

### 工作流程 2：发布更多内容

**触发条件：** 用户从入门菜单中选择“发布更多内容”。

**子代理任务：**
```typescript
Task({
  subagent_type: "general-purpose",
  description: "Publish content workflow",
  prompt: `
    Guide the user through publishing content from tracked prompts.

    Brand ID: ${brandId}
    Session Token: ${TPC_SESSION_TOKEN}

    Step 1: Fetch prompts
    - GET https://app.promptingco.com/api/v1/prompt-topics?brandId=${brandId}
    - For each topic: GET https://app.promptingco.com/api/v1/prompt-topics/{topicId}/prompts?brandId=${brandId}

    Step 2: Display prompts grouped by topic

    Let's create content from your tracked prompts.

    Available prompts:

    Topic: [Topic Name]
    - [Prompt 1]
    - [Prompt 2]

    Which prompt would you like to create content for?

    Step 3: Create content
    - Ask for document details (title, file path)
    - Create document: POST https://app.promptingco.com/api/v1/agentic-documents
    - Ask for content (markdown format)
    - Create draft: POST https://app.promptingco.com/api/v1/agentic-documents/{docId}/create-draft

    Step 4: Publish
    - Ask if user wants to publish now or save as draft
    - If publish: POST https://app.promptingco.com/api/v1/drafts/{draftId}/publish
    - Confirm success

    Use session token in all requests: -H "Cookie: __Secure-better-auth.session_token=${TPC_SESSION_TOKEN}"
  `
})
```

### 工作流程 3：获取统计信息

**触发条件：** 用户从入门菜单中选择“获取统计信息”。

**子代理任务：**
```typescript
Task({
  subagent_type: "general-purpose",
  description: "Fetch and display stats",
  prompt: `
    Fetch and display SOV and AI traffic stats.

    Brand ID: ${brandId}
    Session Token: ${TPC_SESSION_TOKEN}

    Step 1: Fetch data
    - SOV: GET https://app.promptingco.com/api/v1/presence-rate?brandId=${brandId}&timeframe=30d
    - AI Traffic: GET https://app.promptingco.com/api/v1/ai-traffic-stats?brandId=${brandId}&startDate=<30_days_ago>&endDate=<today>

    Step 2: Format and display

    Fetching your stats...

    Share of Voice (SOV)
    ────────────────────────────────
    Current SOV: X.XX%
    Trend: [up/down] by X.XX% from last period

    Data points (last 30 days):
    - Date: SOV%

    AI Traffic Stats
    ────────────────────────────────
    Total AI visits: X,XXX

    Top Bots:
    1. ChatGPT: X visits
    2. Claude: X visits
    3. Gemini: X visits
    4. Perplexity: X visits

    Top Pages:
    1. /path: X visits
    2. /path2: X visits
    3. /path3: X visits

    Use clean formatting with proper spacing and newlines.
    No emojis.
    Use session token in all requests: -H "Cookie: __Secure-better-auth.session_token=${TPC_SESSION_TOKEN}"
  `
})
```

### 日报统计

**触发条件：** 用户请求“每日更新”或“每日统计”。

**创建子代理，执行以下操作：**
- 获取 SOV 趋势：`GET /api/v1/presence-rate?brandId=...&timeframe=7d`
- 获取 AI 流量：`GET /api/v1/ai-traffic-stats?brandId=...&startDate=YESTERDAY&endDate=TODAY`
- 获取每个引擎的细分数据：`GET /api/v1/brand-reach-per-engine?brandId=...&timeframe=7d`
- 总结：最新的 SOV 百分比、与上周相比的变化、顶级 AI 引擎、总 AI 访问量

### 竞争对手比较

**触发条件：** 用户请求与竞争对手进行比较。

**创建子代理，执行以下操作：**
1. 获取固定的竞争对手：`GET /api/v1/brands/{brandId}/pinned-competitors`
2. 获取自己的 SOV：`GET /api/v1/presence-rate?brandId=...&timeframe=30d`
3. 获取竞争对手的 SOV：`GET /api/v1/presence-rate?brandId=...&mentionedBrandId=COMPETITOR_ID&timeframe=30d`
4. 获取两个品牌的细分数据
5. 展示并列比较及趋势**

---

## 错误处理

### 响应结构

所有 API 响应都遵循以下格式：

**成功：**
```json
{ "ok": true, "data": { ... } }
```

**错误：**
```json
{
  "ok": false,
  "code": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": { ... } // optional
}
```

**在处理数据之前始终检查 `response.ok`。

### 错误代码

| 代码 | HTTP 状态 | 描述 | 操作 |
|------|-------------|-------------|--------|
| `UNAUTHORIZED` | 401 | 会话令牌过期或无效 | 请求用户从浏览器提供新的会话令牌 |
| `FORBIDDEN` | 403 | 用户无权访问此资源 | 检查用户是否有权限或品牌 ID 是否正确 |
| `BAD_REQUEST` | 400 | 缺少或无效的参数 | 在请求之前验证必需的参数 |
| `NOT_FOUND` | 404 | 资源不存在 | 验证 ID（brandId、promptId、documentId 等） |
| `VALIDATION_ERROR` | 400 | 参数验证失败 | 验证参数格式（日期、UUID、枚举值） |
| `RATE_LIMITED` | 429 | 请求过多 | 等待 2-3 秒后重试，并采用指数级退避策略 |
| `INTERNAL` | 500 | 服务器错误 | 2-3 秒后重试一次，然后向用户报告 |

### 请求前验证

**在发起任何 API 调用之前：**

1. **验证会话令牌是否存在：**
   ```bash
   if [ -z "$TPC_SESSION_TOKEN" ]; then
     echo "Error: Session token not provided. Please set TPC_SESSION_TOKEN."
     exit 1
   fi
   ```

2. **验证 UUID 参数：**
   - `brandId`、`promptId`、`documentId`、`topicId` 必须是有效的 UUID
   - 格式：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

3. **验证日期参数：**
   - 必须是 ISO 8601 格式：`YYYY-MM-DD`
   - `startDate` 必须在 `endDate` 之前
   - 例如：`2025-01-15`

4. **验证枚举参数：**
   - `timeframe`：只能是 `7d`、`30d` 或 `90d`
   - `sortBy`：只能是有效的列名
   - `sortOrder`：只能是 `asc` 或 `desc`
   - `action`：只能是 `approve` 或 `reject`

5. **验证分页参数：**
   - `page` 必须大于等于 1
   - `pageSize` 必须小于等于 100

### 错误恢复流程

#### 401 未授权（会话过期）

```bash
# When you receive 401 error:
# 1. Inform user their session has expired
# 2. Ask them to get a new session token:
#    - Go to https://app.promptingco.com
#    - Open browser DevTools (F12)
#    - Go to Application/Storage → Cookies
#    - Copy the value of "__Secure-better-auth.session_token"
# 3. Update TPC_SESSION_TOKEN and retry
```

#### 429 请求过多

```bash
# Implement exponential backoff:
retry_count=0
max_retries=3

while [ $retry_count -lt $max_retries ]; do
  response=$(curl -s ...)

  if echo "$response" | jq -e '.code == "RATE_LIMITED"' > /dev/null; then
    wait_time=$((2 ** retry_count))
    echo "Rate limited. Waiting ${wait_time}s before retry..."
    sleep $wait_time
    retry_count=$((retry_count + 1))
  else
    break
  fi
done
```

#### 404 未找到

```bash
# Common causes:
# 1. Brand ID doesn't exist → Re-run First-Time Setup to select valid brand
# 2. Prompt/Topic/Document deleted → Refresh list and ask user to select again
# 3. Typo in ID → Double-check UUID format
```

#### 500 服务器内部错误

```bash
# Retry once after short delay:
response=$(curl -s ...)

if echo "$response" | jq -e '.code == "INTERNAL"' > /dev/null; then
  echo "Server error. Retrying in 3 seconds..."
  sleep 3
  response=$(curl -s ...)

  if echo "$response" | jq -e '.code == "INTERNAL"' > /dev/null; then
    echo "Error: Server is experiencing issues. Please try again later."
    exit 1
  fi
fi
```

### 参数验证示例

**日期范围：**
```bash
# Validate dates before API call
if [[ ! "$start_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "Error: start_date must be YYYY-MM-DD format"
  exit 1
fi

# Ensure start is before end
if [[ "$start_date" > "$end_date" ]]; then
  echo "Error: start_date must be before end_date"
  exit 1
fi
```

**UUID：**
```bash
# Validate UUID format
uuid_pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
if [[ ! "$brand_id" =~ $uuid_pattern ]]; then
  echo "Error: Invalid brand ID format. Must be a UUID."
  exit 1
fi
```

### 向用户报告错误

在报告错误时，始终包括：

1. **出了什么问题：** 明确的错误信息
2. **发生原因：** 错误代码和服务器消息
3. **下一步该怎么做：** 可操作的修复步骤

**示例：**
```
❌ Error: Unable to fetch brand data

Reason: UNAUTHORIZED - Session token has expired

Action needed:
1. Go to https://app.promptingco.com
2. Open DevTools (F12) → Application → Cookies
3. Copy the "__Secure-better-auth.session_token" value
4. Update your TPC_SESSION_TOKEN and try again
```

---

## 提示

- **品牌选择：** 除非用户指定了另一个品牌名称，否则始终使用用户选择的品牌作为默认品牌。
- **SOV 显示：** 在显示 SOV 值时，将 `value` 乘以 100 以显示为百分比（例如 `0.42` 表示 `42%`）。
- **日期格式：** 日期始终使用 ISO 8601 格式：`YYYY-MM-DD`。
- **每个引擎的 SOV：** 每个引擎响应中的 `sov` 字段已经是 0-100 的百分比（无需转换）。
- **时间范围选项：**
  - `7d` — 周视图
  - `30d` — 月视图（默认）
  - `90d` — 季度视图
- **每日统计：** 当用户请求“每日统计”时，使用 `timeframe=7d` 并显示最新数据点及趋势。
- **月度统计：** 当用户请求“月度统计”时，使用 `timeframe=30d`。
- **响应解析：** 在访问 `response.data` 之前始终检查 `response.ok === true`。
- **错误消息：** 当发生错误时，向用户显示 API 响应中的 `message` 字段。
- **品牌上下文：** 如果用户提到了一个品牌名称，请通过 `/api/v1/brands/search` 来查找该品牌的 ID。