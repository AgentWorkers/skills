---
name: serpapi-mcp
description: 通过 `mcporter` 使用 SerpAPI 的 MCP 服务器来执行搜索。当用户要求使用 SerpAPI/SerpAPI MCP 进行网络搜索、希望在 Clawdbot 中集成 SerpAPI 功能，或者需要使用 `/serp` 命令时，可以使用此方法。
---

# serpapi-mcp

这是一个封装技能，它通过 `mcporter` CLI 调用 **SerpAPI 的 MCP 服务器**（Model Context Protocol）。

## 该技能的功能

- 通过 MCP（HTTP）从 OpenClaw 执行 SerpAPI 搜索。
- 将完整的 SerpAPI JSON 数据输出到标准输出（stdout）。
- 可选地将每次查询及其响应数据保存到 **Airtable** 中：
  - 原始 JSON 数据（完整的 SerpAPI 响应内容）
  - 结构化的摘要信息（包括前十个自然搜索结果、相关问题、视频、图片等）

## 使用方法

可以将此技能视为 `/serp` 命令的别名。

**语法：**
- `/serp <query>`
- `/serp <query> [engine] [num] [mode]`

**默认参数：**
- `engine=google_light`
- `num=5`
- `mode=compact`

**注意事项：**
- 如果需要使用 SerpAPI 的高级功能（如 “People also ask (PAA)”、视频内容、知识图谱等），请使用：
  - `engine=google`
  - `mode=complete`

**示例：**
- `/serp site:cnmv.es "educación financiera"`
- `/serp "AAPL stock" google 3 compact`
- `/serp "mortgage pay off vs invest" google 10 complete`

## 工作原理

**主脚本（将结果输出到标准输出）：**
- `skills/serpapi-mcp/scripts/serp.sh "<query>" [engine] [num] [mode]`

**调用的 MCP 服务端点：**
- `https://mcp.serpapi.com/$SERPAPI_API_KEY/mcp.search`

**可选的 Airtable 日志记录工具：**
- `skills/serpapi-mcp/scripts/airtable_log.mjs`

## 必需条件

### 1) MCP 客户端（`mcporter`）

此技能需要在主机上安装 **`mcporter`**。

**安装方法：**
- `npm install -g mcporter`

**验证方法：**
- `mcporter --help`

### 2) SerpAPI 密钥 + 故障转移机制**

您可以配置一个密钥或一个密钥池（按顺序尝试使用）：

- 单个密钥：
  - `SERPAPI_API_KEY`
- 密钥池（用逗号分隔）：
  - `SERPAPI_API_KEYS`

**推荐配置位置：**
- 仅在当前技能范围内配置：
  - `skills.entries.serpapi-mcp.env.SERPAPI_API_KEY`
  - `skills.entries.serpapi-mcp.env.SERPAPI_API_KEYS`
- 全局配置：
  - `envvars.SERPAPI_API_KEY`
  - `envvars.SERPAPI_API_KEYS`

**故障转移机制：**
- 在遇到常见的 **配额限制/身份验证错误**（如 429/401/403、”配额超出”或 “速率限制”）时，脚本会尝试使用下一个密钥。
- 对于其他错误（如请求格式错误），脚本会立即停止并返回错误信息。

## 可选功能：将搜索结果保存到 Airtable

### 启用/禁用日志记录

**启用日志记录：**
- `SERP_LOG_AIRTABLE=1`（或 `true`）

您可以在 Gateway 环境变量中全局配置此选项，或在每次运行脚本时临时设置。

### Airtable 配置（Gateway 环境变量）

请设置以下环境变量（切勿将敏感信息存储在仓库/工作区中）：
- `AIRTABLE_TOKEN`（Airtable 个人访问令牌）
- `AIRTABLE_BASE_ID`
- `AIRTABLE_TABLE`（表格名称或表格 ID）

### Airtable 的写入行为与兼容性

- Airtable 不会自动创建新的字段。
- 日志记录工具会检查表格结构：
  - 通过 Airtable 的 Metadata API 读取表格结构。
  - 仅写入表格中已存在的字段（按字段名称匹配）。
- 会尝试将数据转换为 Airtable 支持的数据类型（如复选框、数字、文本、日期等）。

### 推荐的 Airtable 表结构

字段名称必须与 Airtable 中的字段名称完全匹配：

- `Query` → 单行文本
- `Engine` → 单行文本
- `Num` → 数字
- `Mode` → 单行文本
- `Created` → 日期/时间
- `SerpApiSearchId` → 单行文本
- `SerpApiJsonEndpoint` → URL
- `GoogleUrl` → URL
- `ResultJson` → 长文本
- `ResultJsonTruncatedFlag` → 复选框
  - （兼容性说明：如果偏好使用 `ResultJsonTruncated`，日志记录工具也支持该字段名。）
- `SummaryJson` → 长文本
- `SummaryJsonTruncated` → 复选框
- `OrganicTop10Json` → 长文本
- `RelatedQuestionsTop10Json` → 长文本
- `ShortVideosTop10Json` → 长文本
- `VideosTop10Json` → 长文本
- `ImagesTop10Json` → 长文本
- `HasAiOverview` → 复选框
- `HasAnswerBox` → 复选框
- `HasKnowledgeGraph` → 复选框
- `OrganicCount` → 数字
- `RelatedQuestionsCount` → 数字
- `ShortVideosCount` → 数字
- `VideosCount` → 数字
- `ImagesCount` → 数字

### Airtable 的大小限制

Airtable 对每个单元格的大小有限制。日志记录工具会在必要时截断 JSON 字符串：
- `AIRTABLE_MAX_JSON_chars`（默认值：90000）
- `AIRTABLE_MAX_SUMMARY_CHARS`（默认值：90000）

## 输出结果

返回 SerpAPI 的 JSON 数据。根据所使用的引擎和 Google 的返回内容，响应数据可能包含以下字段：
- `organic_results`
- `short_videos` / `videos_results`
- `images_results`
- `related_questions`
- `knowledge_graph`
- `answer_box` / `ai_overview`
- 广告信息（`top_ads`、`bottom_ads` 等）