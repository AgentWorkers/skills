---
name: nate-jones-second-brain
description: 使用 Supabase (pgvector) 和 OpenRouter 构建并运行一个个人知识管理系统。该系统包含五个结构化的表格：想法（inbox log）、人员信息（people）、项目（projects）、创意（ideas）以及管理员管理（admin）。系统具备基于人工智能的分类功能、基于置信度的信息路由机制，并支持跨所有类别的语义搜索。它可以捕获来自任何来源的想法，通过大型语言模型（LLM）对这些想法进行分类，将它们路由到相应的表格中；对于分类结果置信度较低的信息，系统会将其拒绝；同时，所有操作都会被记录下来（通过 Receipt 表格）。该系统的核心组件包括 Supabase（负责持久化的数据存储架构）和 OpenRouter（作为人工智能的接口），这两者共同为个人知识管理系统提供了强大的基础支持。作者：Jonathan • natebjones.com
metadata: {"openclaw": {"requires": {"env": ["SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY", "OPENROUTER_API_KEY"]}, "homepage": "https://natebjones.com"}}
---
# Nate Jones 的“第二大脑”（Nate Jones’ Second Brain）

当信息量庞大时，上下文就成了稀缺的资源。这项技能的核心就是“上下文架构”（Context Architecture）——一个持久且可搜索的知识层，它将你的智能助手（agent）转变为一个个人知识管理者。

**两个核心工具：**

- **Supabase**：你的数据库，功能远不止于此。它结合了 PostgreSQL 和 pgvector 技术，能够以结构化数据的形式存储你的想法、联系人、项目、创意和任务，并使用向量嵌入（vector embeddings）进行存储。内置了 REST API。数据属于你，基础设施也由你控制。模型可能会更新或替换，但你的上下文信息会一直保留下来。一旦你使用了 Supabase，你就为后续的所有功能打下了基础；而“第二大脑”（Second Brain）仅仅是个开始而已。
- **OpenRouter**：你的 AI 接口。只需一个 API 密钥，就可以访问所有的模型。通过更改字符串，你可以轻松切换不同的分类和路由规则。这个设计具有很强的前瞻性（future-proof）。

其他所有功能——比如如何捕获信息、如何检索信息、以及如何在此基础上构建更多应用——都属于应用层（application layer）的范畴。这项技能主要关注的是基础架构的构建。

> 如果相关表格还不存在，请参阅 `{baseDir}/references/setup.md`。

## 核心组件

以下是系统背后的运作原理。理解这些组件有助于你正确地使用系统。

| 组件 | 功能 | 实现方式 |
|-------|-------------|----------------|
| **Drop Box** | 一个无障碍的信息捕获点 | 所有信息首先都会被保存到 `thoughts` 表中 |
| **Sorter** | AI 分类与路由 | AI 对信息类型进行分类，然后将其路由到相应的结构化表格中 |
| **Form** | 一致的数据格式规范 | 每个表格都有明确的字段结构 |
| **Filing Cabinet** | 按类别分类的信息存储库 | `people`、`projects`、`ideas`、`admin` 表格 |
| **Bouncer** | 信息筛选机制 | 如果信息的置信度（confidence）低于 0.6，则不进行路由，而是保留在 `thoughts` 表中 |
| **Receipt** | 日志记录 | `thoughts` 表会记录信息的来源和去向 |
| **Tap on the Shoulder** | 主动信息推送 | 每日汇总查询（由应用层处理） |
| **Fix Button** | 人工修正功能 | 根据用户请求在表格间移动记录 |

完整的概念框架请参阅：`{baseDir}/references/concepts.md`

## 五个核心表格

| 表格 | 功能 | 关键字段 |
|-------|------|------------|
| `thoughts` | 信息存储与审计记录 | 包含内容、向量嵌入、元数据（类型、主题、联系人、置信度、路由目标） |
| `people` | 人际关系管理 | 包含姓名、上下文信息、跟进事项、标签、向量嵌入 |
| `projects` | 项目跟踪 | 包含项目名称、状态、下一步行动、备注、标签、向量嵌入 |
| `ideas` | 创意记录 | 包含创意标题、摘要、详细内容、主题、向量嵌入 |
| `admin` | 任务管理 | 包含任务名称、截止日期、状态、备注、向量嵌入 |

每个表格都支持基于自身字段的语义搜索（使用 `match_*` 函数）。跨表格搜索则通过 `search_all` 实现。

## 路由规则

当信息被分类后，会根据以下规则进行路由：

| 信息类型 | 路由目标 | 处理方式 |
|------|-------|--------|
| `person_note` | `people` | 创建新联系人记录或更新现有联系人信息 |
| `task` | `admin` | 插入新任务（状态为“待处理”） |
| `idea` | `ideas` | 插入新创意 |
| `observation` | 保留原处 | 仅保留在 `thoughts` 表中 |
| `reference` | 保留原处 | 仅保留在 `thoughts` 表中 |

如果信息的置信度低于 0.6，就不予路由，而是保留在 `thoughts` 表中，并通知用户。

## 快速入门

### 捕获信息（完整流程）

```bash
# 1. Embed
EMBEDDING=$(curl -s -X POST "https://openrouter.ai/api/v1/embeddings" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "openai/text-embedding-3-small", "input": "Sarah mentioned she is thinking about leaving her job to start consulting"}' \
  | jq -c '.data[0].embedding')

# 2. Classify (run in parallel with step 1)
METADATA=$(curl -s -X POST "https://openrouter.ai/api/v1/chat/completions" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-4o-mini", "response_format": {"type": "json_object"}, "messages": [{"role": "system", "content": "Extract metadata from the captured thought. Return JSON with: type (observation/task/idea/reference/person_note), topics (1-3 tags), people (array), action_items (array), dates_mentioned (array), confidence (0-1), suggested_route (people/projects/ideas/admin/null), extracted_fields (structured data for destination table)."}, {"role": "user", "content": "Sarah mentioned she is thinking about leaving her job to start consulting"}]}' \
  | jq -r '.choices[0].message.content')

# 3. Store in thoughts (the Receipt)
curl -s -X POST "$SUPABASE_URL/rest/v1/thoughts" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d "[{\"content\": \"Sarah mentioned she is thinking about leaving her job to start consulting\", \"embedding\": $EMBEDDING, \"metadata\": $METADATA}]"

# 4. Route based on classification (if confidence >= 0.6)
```

完整的捕获流程及路由逻辑请参阅：`{baseDir}/references/ingest.md`

### 单表语义搜索

```bash
QUERY_EMBEDDING=$(curl -s -X POST "https://openrouter.ai/api/v1/embeddings" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "openai/text-embedding-3-small", "input": "career changes"}' \
  | jq -c '.data[0].embedding')

curl -s -X POST "$SUPABASE_URL/rest/v1/rpc/match_thoughts" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"query_embedding\": $QUERY_EMBEDDING, \"match_threshold\": 0.5, \"match_count\": 10, \"filter\": {}}"
```

### 跨表搜索

```bash
curl -s -X POST "$SUPABASE_URL/rest/v1/rpc/search_all" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"query_embedding\": $QUERY_EMBEDDING, \"match_threshold\": 0.5, \"match_count\": 20}"
```

该操作会返回所有表格中的 `table_name`、`record_id`、`label`、`detail`、`similarity` 和 `created_at` 等信息。

### 列出活跃项目

```bash
curl -s "$SUPABASE_URL/rest/v1/projects?status=eq.active&select=name,next_action,notes&order=updated_at.desc" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY"
```

### 列出待处理任务

```bash
curl -s "$SUPABASE_URL/rest/v1/admin?status=eq.pending&select=name,due_date,notes&order=due_date.asc" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY"
```

## 数据捕获流程

当信息从任何来源传来时，会按照以下步骤处理：

1. 通过 OpenRouter 将文本转换为 1536 维的向量格式。
2. 使用 OpenRouter 的 LLM 对文本进行分类（确定类型、主题、相关联系人及推荐路由目标）。
3. 将信息记录到 `thoughts` 表中（无论是否进行路由处理，此步骤都会执行）。
4. 检查信息的置信度；如果置信度低于 0.6，则停止后续处理。
5. 根据信息类型将其路由到相应的结构化表格中。
6. 向用户确认信息已被捕获以及存储的位置。

完整的流程详情请参阅：`{baseDir}/references/ingest.md`

## 元数据结构

每条信息都会被赋予以下元数据：

| 字段 | 类型 | 值         |
|-------|------|------------|
| `type` | string | 类型（`observation`、`task`、`idea`、`reference`、`person_note`） |
| `topics` | string[] | 1-3 个主题标签（至少包含一个） |
| `people` | string[] | 被提及的人名（为空表示没有提及任何人） |
| `action_items` | string[] | 建议的后续行动（为空表示没有建议） |
| `dates_mentioned` | string[] | 提及的日期（格式为 YYYY-MM-DD，为空表示没有提及日期） |
| `source` | string | 信息来源（如 Slack、Signal、CLI 等） |
| `confidence` | float | LLM 的分类置信度（0-1，用于筛选） |
| `routed_to` | string | 信息存储的表格名称（未路由时为 null） |
| `routed_id` | string | 目标表格中的记录唯一标识符（未路由时为 null） |

## 参考资料

- **概念框架**：`{baseDir}/references/concepts.md`
- **首次设置指南**：`{baseDir}/references/setup.md`
- **数据库架构（SQL）**：`{baseDir}/references/schema.md`
- **数据捕获流程**：`{baseDir}/references/ingest.md`
- **信息检索功能**：`{baseDir}/references/retrieval.md`
- **OpenRouter API 使用说明**：`{baseDir}/references/openrouter.md`

## 环境变量

| 变量 | 所对应服务 |  
|----------|---------|  
| `SUPABASE_URL` | Supabase 项目的 REST API 地址 |  
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase 的认证密钥（全权限） |  
| `OPENROUTER_API_KEY` | OpenRouter 的 API 密钥 |  

## 安全注意事项

**为什么使用 `service_role` 密钥？** Supabase 提供两种密钥：`anon`（公共访问权限，遵循 RLS 规则）和 `service_role`（全权限，可绕过 RLS 规则）。我们选择使用 `service_role` 的原因如下：

- 这是一个专为个人使用的知识管理系统，而非多租户应用。
- 你的智能助手本身就是可信的服务器端组件。
- RLS（Role-Based Security）策略仅允许 `service_role` 访问权限，这是最严格的设置。
- 如果使用 `anon` 密钥，就需要放宽 RLS 规则以允许匿名访问用户的想法，但这会带来安全隐患。

**发送到 OpenRouter 的数据**：所有被捕获的文本（包括想法、人名和后续行动建议）都会被发送到 OpenRouter 进行嵌入和分类处理。这是系统设计的一部分——因为我们需要 AI 来理解这些信息的含义。除非你同意 OpenRouter 的数据处理政策，否则不要捕获敏感信息。

**密钥管理**：请妥善保管 `SUPABASE_SERVICE_ROLE_KEY` 和 `OPENROUTER_API_KEY`，切勿将它们公开存储在代码仓库中。定期更换这些密钥。在 OpenClaw 中，可以将它们存储在 `openclaw.json` 文件的 `skills.entries` 部分或作为环境变量。

---

由 Limited Edition Jonathan 开发 • natebjones.com 提供