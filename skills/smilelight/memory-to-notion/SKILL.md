---
name: memory-to-notion
description: 将对话记录进行总结并归档到 Notion 中。当用户输入“总结对话记录”、“归档对话”、“保存对话记录”、“将对话记录同步到 Notion”、“将对话记录写入 Notion”、“回顾并记录我们讨论的内容”，或任何类似请求（如回顾、总结、归档或导出对话历史/聊天记录到 Notion）时，系统应自动触发相应的操作。
disable-model-invocation: true
user-invocable: true
---
# 将对话内容存储到 Notion 数据库中

该技能会检索用户的过往对话记录，分析其中有价值的内容，将这些内容分解为独立的记忆条目，并将它们作为记录写入 Notion 数据库的 “Memory Store” 中。

## 数据库的查找

该技能采用“零配置”方式：数据库的名称始终为“Memory Store”。

**查找数据库：**

```
POST /v1/search
{
  "query": "Memory Store"
}
```

在搜索结果中，找到标题为“Memory Store”的条目。提取以下信息：
- `data_source_id`：用于查询（`POST /v1/data_sources/{id}/query`）
- `database_id`：用于创建页面（`POST /v1/pages`，其中包含 `parent: {"database_id": "..."}`）

- **如果找到**：使用 `data_source_id` 进行查询，使用 `database_id` 创建页面。
- **如果没有找到**：询问用户：“在您的 Notion 工作区中未找到 ‘Memory Store’ 数据库。应该将其创建在哪个页面下？请提供 Notion 页面的 URL 或页面 ID。”
  然后创建数据库（详见下面的数据库创建步骤）。

### 数据库结构

| 属性        | 类型        | 描述                                             |
|-------------|-------------|---------------------------------------------------------|
| 标题         | 文本         | 一条简短的记忆摘要（可搜索）                                      |
| 类别         | 单选         | 事实 / 决策 / 偏好设置 / 上下文 / 规律 / 技能                           |
| 内容         | 富文本        | 详细的记忆内容                                         |
| 来源         | 单选         | Claude.ai / ClaudeCode / 手动输入 / OpenClaw / 其他                        |
| 状态         | 单选         | 活动中 / 已归档 / 矛盾                                        |
| 范围         | 单选         | 全局 / 项目                                           |
| 项目名称       | 文本         | 项目名称（当范围设置为“项目”时填写；全局时留空）                         |
| 失效时间       | 单选         | 永久有效 / 30 天 / 90 天 / 1 年                                    |
| 来源日期       | 日期         | 对话发生的时间                                         |

### 数据库创建

如果数据库不存在，则在用户指定的父页面下创建它。使用上述数据库结构，通过 Notion 的 `create-database` API 来创建数据库。

### 类别定义

- **事实**：客观事实——用户的身份、背景、技术栈、使用的工具、工作环境、组织结构
- **决策**：架构决策、技术选择、方法选择
- **偏好设置**：用户的编码风格、工具配置、交互习惯
- **上下文**：背景信息——项目背景、领域知识、观察结果
- **规律**：工作流程、重复出现的需求
- **技能**：掌握的技能和知识——命令、API、使用的技术

## 平台适配

该技能使用通用的 Notion REST API 格式进行操作。每个平台的人工智能系统应使用以下固定的映射方式将其转换为相应的工具功能。切勿自行猜测，必须严格遵循这些映射规则。

### Claude Code / Claude.ai（Notion MCP 工具）

| 操作            | SKILL.md 中的描述            | 使用的 MCP 工具            | 关键参数                                      |
|-----------------|-------------------|-------------------|-----------------------------------------|
| 查找数据库       | `POST /v1/search`         | `notion-search`         | `query: "Memory Store", `content_search_mode: "workspace_search"`         |
| 获取数据库 ID      |                    | `notion-fetch`         | 从 `<data-source url="collection://...">` 标签中提取 `data_source_id`         |
| 去重查询        | `POST /v1/data_sources/{id}/query`     | **不可用**           | 退而使用 `notion-search` 并提供 `data_source_url`                |
| 创建页面         | `POST /v1/pages`         | `notion-create-pages`         | `parent: { "data_source_id": "..." }`                         |
| 更新页面状态       | `PATCH /v1/pages/{id}`         | `notion-update-page`         | `command: "update_properties"`                         |
| 创建数据库       | `POST /v1/databases`         | `notion-create-database`         | 使用 SQL DDL 语法                         |
| 获取页面内容       | `GET /v1/pages/{id}`         | `notion-fetch`         | `id: "<page_id>"`                         |

**重要说明：**
- 查找数据库时必须使用 `content_search_mode: "workspace_search"`（默认的 `ai_search` 模式可能无法找到数据库）
- MCP 平台不支持结构化去重查询。请使用语义搜索作为替代方案：
  使用 `notion-search` 并提供 `data_source_url: "collection://<data_source_id>"` 以及相关关键词。
  然后使用 `notion-fetch` 获取每个结果以比较所有属性。
- `notion-create-database` 使用 SQL DDL 语法，而非 JSON 格式。详细信息请参见数据库创建部分。

### OpenClaw / 直接 API 访问

请严格按照工作流程中的步骤使用 Notion REST API。所有操作（包括结构化去重查询）都得到完全支持。

## 工作流程

### 第一步：查找数据库

找到“Memory Store”数据库。如果未找到，则创建它（详见上文）。

### 第二步：收集对话内容

根据当前使用的平台选择合适的策略：

**Claude.ai**（支持对话历史记录 API）：
- 使用 `recent_chats(n=20)` 获取最近的对话记录
- 使用 `after`/`before` 参数按时间范围筛选
- 使用 `conversation_search` 按关键词搜索
- 为了全面归档，可以分多轮获取对话记录

**Claude Code**（仅适用于当前会话）：
- 从当前对话中提取有价值的信息
- 当用户输入“总结记忆”等指令时触发该功能
- 查看当前会话中产生的事实、决策和偏好设置
- 无法访问过去的会话记录——仅处理当前会话的内容

### 第三步：检查现有记忆记录（去重与冲突检测）

在写入新记录之前，先查询数据库以检查是否存在重复或冲突的内容。
对于每个待存储的记忆条目，需要检查其标题和内容：

```
POST /v1/data_sources/{data_source_id}/query
{
  "filter": {
    "or": [
      { "property": "Title", "title": { "contains": "<keyword from new memory>" } },
      { "property": "Content", "rich_text": { "contains": "<keyword from new memory>" } }
    ]
  },
  "page_size": 10
}
```

> **MCP 平台（Claude Code / Claude.ai）**：不支持结构化查询。请使用 `notion-search` 并提供 `data_source_url: "collection://<data_source_id>"` 以及相关关键词进行搜索。然后使用 `notion-fetch` 获取每个结果以比较属性。

查询返回完整的页面信息。需要检查以下情况：
1. **重复记录**：相同的事实已存在——跳过该记录
2. **更新记录**：主题相同但内容发生变化——更新现有记录，并在需要时将其标记为“矛盾记录”
3. **冲突记录**：新信息与现有记录矛盾——创建新记录并标记为“活动记录”，同时将旧记录标记为“矛盾记录”

### 第四步：将对话内容分解为独立的记忆条目

每个对话可能会产生 0 到 N 条记忆条目。基本原则是“每条记录只包含一个事实”。

**分解规则**：
- 每条记忆记录应独立且具有明确的意义
- 不要存储整个对话的摘要——只提取其中的事实、决策和偏好设置
- 标题应为简洁明了的陈述句（可搜索）
- 内容应包含足够的细节，以便在没有原始对话的情况下也能被理解

**示例**：
关于“设置一个新的 Python 项目”的对话可能会生成以下记忆条目：
```
"User prefers uv over pip for Python dependency management"  -> Category: Preference
"Project OpenClaw uses FastAPI + PostgreSQL architecture"     -> Category: Decision
"User prefers Ruff for code formatting and linting"           -> Category: Preference
"User is a programmer"                                        -> Category: Fact
```

**不应存储的内容**：
- 可以轻松重新搜索的临时问答（例如“Python 的 GIL 是什么”）
- 无关的寒暄和闲聊
- 未产生实际结果的失败尝试
- 用户明确要求删除的信息

### 第五步：将记录写入数据库

在数据库中创建相应的页面。为每个记忆条目设置以下属性：

```json
{
  "Title": "One-line summary",
  "Category": "Fact|Decision|Preference|Context|Pattern|Skill",
  "Content": "Detailed memory content, sufficient for any AI platform to understand and use",
  "Source": "Claude.ai|ClaudeCode|OpenClaw|Manual|Other",
  "Status": "Active",
  "Scope": "Global|Project",
  "Project": "Project name (set when Scope=Project)",
  "Expiry": "Never|30d|90d|1y",
  "date:Source Date:start": "YYYY-MM-DD",
  "date:Source Date:is_datetime": 0
}
```

**范围划分指南**：
- **全局**：跨项目的通用信息——用户偏好设置、通用工具链、个人习惯、全局性决策
- **项目**：项目特定的信息——项目架构、专用配置、项目范围内的技术决策
- 如果不确定，默认设置为“全局”
- 项目字段应与用户的项目目录名称或仓库名称匹配（例如“OpenClaw”）

**失效时间设置指南**：
- **永久有效**：稳定不变的信息（如用户名称、使用的工具、项目架构）
- **1 年**：可能会过时（如工具版本、项目状态）
- **90 天**：有效期较短的信息（如当前任务、临时决策）
- **30 天**：非常短暂的信息（如本周待办事项、临时解决方案）

### 第六步：处理冲突

如果第三步发现冲突记录：
1. 将**旧记录**的状态设置为“矛盾记录”：
   ```
   PATCH /v1/pages/{old_page_id}
   { "properties": { "Status": { "select": { "name": "Contradicted" } } } }
   ```
2. 将**新记录**的状态设置为“活动记录”（默认值）
3. （可选）在新记录的内容中注明它替换了哪些旧记录：“(更新：之前记录为 XX)”

### 第七步：报告结果

写入记录后，向用户提供以下信息：
- 处理的对话记录数量
- 创建/更新/跳过的记忆条目数量
- 新创建的记忆条目的列表（包括标题和类别）
- 发现的冲突及其解决方式

**示例**：
```
Memory archival complete

Processed 8 conversations, generated 12 memories:
- New: 10
- Updated: 1 (user location updated from Beijing to Shenzhen)
- Skipped: 3 low-value conversations

New memories:
| Title | Category |
|-------|----------|
| User prefers uv for Python dependency management | Preference |
| Project OpenClaw uses FastAPI architecture | Decision |
```

## 重要注意事项

- **每条记录只包含一个事实**：切勿将整个对话的摘要放入一条记录中。
- **语言**：标题和内容应使用用户的主要语言（用户在对话中最常用的语言）编写。这样可以确保记忆记录能够被用户用自然使用的语言搜索和阅读。不要强制使用英语。
- **操作具有幂等性**：在写入记录前始终检查是否存在重复记录。重复执行操作不应导致重复条目。
- **来源信息的准确性**：根据当前使用的平台自动设置来源（Claude.ai → “Claude.ai”，Claude Code → “ClaudeCode”，OpenClaw → “OpenClaw”）。
- **保留详细信息**：在内容中保留代码片段、命令、配置值和 URL 的原始形式。
- **用户控制**：不要存储用户不希望看到的任何内容。如有疑问，请先询问用户。
- **跨平台兼容性**：编写的内容应能被任何人工智能平台理解和使用。

## 示例交互过程

**用户**：请求“总结记忆”

**Claude**：
1. 查找“Memory Store”数据库，获取 `data_source_id` 和 `database_id`
2. 查看当前会话记录（Claude Code）或最近的对话记录（Claude.ai）
3. 查询数据库以检查是否存在重复记录
4. 将对话内容分解为独立的记忆条目
5. 将这些条目写入数据库
6. 报告处理结果：“处理了 5 条对话记录，生成了 8 条新记录，更新了 1 条记录，跳过了 2 条记录。”