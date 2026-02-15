---
name: swiftscholar-skill
description: 该功能集成了 SwiftScholar 的 HTTP API，用于搜索、提交和分析学术论文。当用户需要搜索文献、提交 PDF 文件或 URL 以供解析、检索分析结果、管理收藏夹，或以编程方式检查 SwiftScholar 账户的使用情况时，可以使用此功能。
---

# SwiftScholar 技能 (`swiftscholar-skill`)  

此技能使代理能够使用 **SwiftScholar HTTP API** 来搜索、提交、分析和管理学术论文。建议优先使用以 JSON 为主的 `/api/tools/*` 端点，而非已弃用的 `/api/mcp/tools/*` 端点。  

**基本信息：**  
- **基础 URL**: `https://www.swiftscholar.net`  
- **认证**: `Authorization: Bearer <API_KEY>`  
- **规范版本**: OpenAPI 3.1.0 (`SwiftScholar HTTP API 1.0.0`)  

> **注意**：切勿在自然语言响应中暴露 API 密钥，仅将其包含在实际的 HTTP 请求头中。  

---

## 1. 何时使用此技能  

在以下情况下使用 SwiftScholar API：  
- 用户希望：  
  - **搜索学术论文**（关键词搜索或语义/向量搜索）  
  - **提交论文 URL 或 PDF 文件**以进行解析  
  - **获取结构化的 Markdown 分析结果**或原始 Markdown 内容  
  - **管理/查看收藏夹和收藏文件夹**  
  - **查看解析配额、使用情况以及可用的分析模型**  

**典型触发短语示例：**  
- “文献搜索”，“关键词搜索论文”，“语义搜索论文”  
- “解析这篇论文的 PDF/URL”，“分析这篇论文”  
- “获取这篇论文的详细分析结果/Markdown”  
- “SwiftScholar 收藏夹/收藏文件夹”  
- “SwiftScholar 账户使用情况/配额/解析历史记录”  

---

## 2. 认证和调用规范  

### 2.1 认证  

- 所有 `/api/tools/*` 端点都使用 **Bearer 令牌**：  
  - 请求头：`Authorization: Bearer <SWIFTSCHOLAR_API_KEY>`  
- 代理不得在自然语言响应中泄露或推断 API 密钥。  

### 2.2 通用请求规范  

- **HTTP 方法**：所有工具端点均为 `POST`。  
- **Content-Type**：  
  - JSON 请求：`application/json`  
  - PDF 上传：`multipart/form-data`，并将文件作为二进制数据上传  
- **错误处理**：  
  - JSON 响应遵循 `ToolApiResponse` 结构：  
    - `ok: boolean`（始终存在）  
    - `data: object`（成功时存在）  
    - `error: string`（失败时可能存在）  
- **调用后**：  
  - 如果 `ok` 为 `false` 或存在 `error`，向用户简要说明失败原因，并建议下一步操作（例如调整参数、缩小搜索范围）。  

---

## 3. 核心功能及端点  

本节按功能分类，而非按 URL 分类，以帮助代理选择合适的工具。  
所有列出的端点均位于 `paths./api/tools/...` 下。  

### 3.1 论文标签和基本浏览  

1. **列出所有论文标签（含标签 ID 和使用次数）**  
   - 端点：`POST /api/tools/paper_tags_list`  
   - 请求体：`{}`（无参数）  
   - **用途**：  
     - 在推荐标签过滤器或构建复杂查询时，首先列出可用的标签及其 ID。  

2. **分页显示论文**  
   - 端点：`POST /api/tools/papers_paginate`  
   - 请求体字段（部分）：  
     - `page: integer >= 1`（默认值 1）  
     - `pageSize: integer 1–50`（默认值 10）  
     - `licenses: string[]`（可能包含 `'none'`）  
     - `publishedFrom: string (YYYY-MM-DD)`  
     - `publishedTo: string (YYYY-MM-DD)`  
   - **用途**：  
     - 按时间或许可类型浏览论文列表，作为搜索结果或用户库浏览的依据。  

### 3.2 搜索：关键词搜索 vs 向量（语义）搜索  

1. **关键词搜索（字面匹配）**  
   - 端点：`POST /api/tools/papers_search_keyword`  
   - 关键请求体字段：  
     - `query: string`（必填；搜索字符串）  
     - `page, pageSize`（与 `papers_paginate` 相同）  
     - `tags: string[]` / `tagNames: string[]`（标签过滤器）  
     - `tagMode: "and" | "or"`（默认值 `"or"`）  
     - `licenses, publishedFrom, publishedTo`（与上述相同）  
   - **使用说明**：  
     - 当用户提供明确的关键词、标题片段或短语时使用此方法。  
     - 说明这是 **字面匹配**，适用于精确查找。  

2. **向量搜索（语义搜索）**  
   - 端点：`POST /api/tools/papers_search_vector`  
   - 关键请求体字段：  
     - `query: string`（必填；自然语言查询）  
     - `limit: integer 1–30`（默认值 10）  
     - 其他过滤器与 `papers_search_keyword` 相同  
   - **使用说明**：  
     - 当用户描述**模糊概念**、研究主题或问题时使用（例如：“LLM 在医学成像领域的最新进展”）。  
     - 说明这是 **语义搜索**，更适合“查找相关论文”，无需精确匹配标题。  

### 3.3 提交论文：URL / PDF / 批量 URL  

1. **通过 URL 提交论文**  
   - 端点：`POST /api/tools/paper_submit_url`  
   - 请求体字段：  
     - `url: string`（必填；论文来源页面或 PDF URL）  
     - `modelId: string`（可选；PDF 分析模型）  
     - `force: boolean`（强制重新解析）  
     - `favoriteFolderId: string | null`（收藏文件夹；`null` 表示根目录）  
     - `favoriteNote: string`（收藏备注）  
   - **使用说明**：  
     - 当用户提供论文页面 URL 或直接 PDF URL 并希望进行解析、分析或保存到收藏夹时使用。  
     - 提醒解析可能需要时间，并建议在需要时查看结果。  

2. **提交 PDF 文件**  
   - 有两种主要方式：  
     - **JSON API**：  
       - 端点：`POST /api/tools/paper_submit_pdf`  
       - JSON 请求体：  
         - `pdfUrl: string` 或 `pdfBase64: string`（必须提供其中一个）  
         - `fileName: string`（可选）  
         - 其他字段与 `paper_submit_url` 相同（`modelId`, `force`, `favoriteFolderId`, `favoriteNote`）  
     - **注意**：规范明确要求“提供 `pdfUrl` 或 `pdfBase64` 中的一个。  
     - **multipart 上传**：  
       - 使用相同的端点，但采用 `multipart/form-data`：  
         - `file: binary`（必填；PDF 文件内容）  
         - 可选字段：`modelId`, `force`, `favoriteFolderId`, `favoriteNote`  
   - **使用说明**：  
     - 当用户拥有本地 PDF 或远程 PDF URL 并希望对其进行解析时使用。  

3. **批量提交 URL**  
   - 端点：`POST /api/tools/papers_submit_urls`  
   - 请求体字段：  
     - `urls: string[] | string`（数组或换行符分隔的字符串）  
     - `modelId: string`（可选；应用于所有 URL）  
     - `notifyOnComplete: boolean`（默认值 false）  
     - `force: boolean`（默认值 false）  
     - `favoriteFolderId: string | null`  
     - `favoriteNote: string`  
   - **使用说明**：  
     - 当用户提供多个论文 URL 并希望批量解析、保存或同时进行这两种操作时使用。  

### 3.4 阅读和分析：Markdown 分析 / 原始 Markdown / PDF 链接  

1. **获取Markdown格式的论文分析结果**  
   - 端点：`POST /api/tools/paper_analysis_markdown`  
   - 请求体字段：  
     - `paperId: string`（必填）  
     - `language: "auto" | "zh" | "en" | "both"`（默认值 `"auto"`）  
     - `scope: "public" | "me" | "auto"`（默认值 `"public"`  
   - **使用说明**：  
     - 当用户需要**结构化、易读的分析结果**（摘要、结构、关键点）时使用。  
     - 根据用户偏好设置 `language`：  
       - 对于中文用户，建议使用 `"zh"` 或 `"both"`；  
       - 如果不确定，使用 `"auto"`。  

2. **获取论文的原始 Markdown 内容**  
   - 端点：`POST /api/tools/paper_markdown_raw`  
   - 请求体字段：  
     - `paperId: string`（必填）  
     - `maxChars: integer (500–120000)`（可选；限制字符数）  
   - **使用说明**：  
     - 当用户希望进行自定义处理、重新总结或提取公式/表格时使用。  
     - 对于非常长的论文，请设置合理的 `maxChars` 并告知用户内容是否被截断。  

3. **获取受保护的 PDF 下载链接**  
   - 端点：`POST /api/tools/paper_pdf_link`  
   - 请求体字段：  
     - `paperId: string`（必填）  
   - **使用说明**：  
     - 当用户希望下载或本地打开 PDF 时使用。  
     - 遵守版权和可见性规则；仅提供 API 授权的链接。  

---

### 3.5 收藏夹和收藏论文  

1. **列出收藏文件夹**  
   - 端点：`POST /api/tools/paper_favorite_folders`  
   - 请求体：`{}`  
   - **用途**：  
     - 获取文件夹 ID、父子关系及路径，帮助用户组织和定位保存位置。  

2. **列出收藏论文**  
   - 端点：`POST /api/tools/paper_favorites_list`  
   - 请求体字段：  
     - `page, pageSize`（分页；1–50）  
     - `folderId: string | null`（`null` 表示根目录；省略则表示所有文件夹）  
     - `includeDescendants: boolean`（默认值 false）  
     - `search: string`（在备注和标题中搜索）  
   - **用途**：  
     - 浏览用户的个人图书馆或按备注和标题筛选论文。  

3. **保存或更新收藏记录**  
   - 端点：`POST /api/tools/paper_favorite_save`  
   - 请求体字段：  
     - `paperId: string`（必填）  
     - `folderId: string | null`（目标文件夹；`null` 表示根目录；如果存在则重用现有文件夹）  
     - `note: string`（可选备注）  
   - **使用说明**：  
     - 在识别出重要论文后，建议将它们保存到合适的文件夹，并附上简短的描述性备注。  

### 3.6 分析模型和账户使用情况  

1. **列出可用的 PDF 分析模型**  
   - 端点：`POST /api/tools/paper_analysis_models`  
   - 请求体：`{}`  
   - **用途**：  
     - 显示当前计划下的可用模型（包括 `consumeUnits` 和每次解析的额外费用），帮助选择 `modelId`。  
     - 当用户关心成本或模型质量时使用；列出模型并提供推荐。  

2. **汇总账户配额和积分**  
   - 端点：`POST /api/tools/account_usage_summary`  
   - 请求体：`{}`  
   - **用途**：  
     - 汇总当前的解析配额和积分，让用户了解还可以解析多少篇论文。  

3. **列出解析历史记录**  
   - 端点：`POST /api/tools/parse_history_list`  
   - 请求体字段：  
     - `page, pageSize`（1–100）  
     - `chargeMode: string`（可选，例如 `FREE` 或 `BALANCE`）  
   - **用途**：  
     - 显示过去 30 天的解析使用记录（哪些论文被解析、何时被解析以及可能的费用）。  

## 4. 推荐的工作流程  

### 4.1 从研究问题到论文推荐（搜索工作流程）  

1. 用自然语言明确用户的研究问题或主题。  
2. 如果描述是概念性的或模糊的：  
   - 首先调用 **向量搜索** `/api/tools/papers_search_vector` 以聚焦概念相关性。  
3. 如果用户提供具体的关键词或标题片段：  
   - 使用 **关键词搜索** `/api/tools/papers_search_keyword`。  
4. 按相关性或最新时间排序结果：  
   - 显示论文标题、年份和主要贡献的简要描述，以及 `paperId` 以便后续操作。  
5. 对于选定的论文：  
   - 调用 `/api/tools/paper_analysis_markdown` 进行详细分析；或  
   - 调用 `/api/tools/paper_markdown_raw` 进行细粒度自定义处理。  

### 4.2 提交新论文并获取分析结果（提交 + 分析工作流程）  

1. 当用户提供论文 URL 或 PDF 时：  
   - 使用 `/api/tools/paper_submit_url`。  
   - 如果使用本地 PDF，使用 `/api/tools/paper_submit_pdf`。  
2. 如果用户指定了文件夹或备注：  
   - 在请求中包含 `favoriteFolderId` 和 `favoriteNote`。  
3. 等待解析完成（如果 API 是异步的，可参考历史记录或文档中的 ID）：  
   - 一旦获得 `paperId`，调用 `/api/tools/paper_analysis_markdown`。  
4. 概述分析结果，包括：  
   - 核心贡献、方法、数据集、结论以及它们与用户研究问题的关联。  

### 4.3 管理个人文献库（收藏工作流程）  

1. 当用户需要查看收藏夹结构时：  
   - 调用 `/api/tools/paper_favorite_folders` 列出所有文件夹。  
2. 按文件夹或搜索字符串查看收藏内容：  
   - 使用适当的 `folderId` 和 `search` 调用 `/api/tools/paper_favorites_list`。  
3. 当识别出重要的长期论文时：  
   - 调用 `/api/tools/paper_favorite_save` 创建或更新收藏记录。  
4. 在总结中：  
   - 建议按主题或项目组织文件夹，以便将来方便检索。  

---

## 5. 实用技巧  

- **优先使用 `/api/tools/*`：**  
  `/api/mcp/tools/*` 端点在 OpenAPI 规范中被标记为已弃用；新集成时应避免使用它们。  
- **验证参数：**  
  遵守 OpenAPI 的限制（分页限制、必填字段），以避免不必要的重试。  
- **后处理响应：**  
  每次调用后，将原始 JSON 转换为用户友好的输出：  
  - 简洁的论文列表（标题 + 年份 + 简短描述）；  
  - 清晰的要点总结（方法、结果、局限性）；  
  - 提供与用户问题相关的直接结论和建议（而不仅仅是原始数据）。