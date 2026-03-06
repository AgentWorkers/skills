---
name: recall-from-notion
description: 从 Notion 的记忆存储中检索用户的记忆信息。在对话开始时主动触发该功能，因为了解用户的背景、偏好、过去的决策或项目背景有助于提供更准确的回应。此外，在用户说出“回忆一下”、“还记得吗”、“你对我了解多少”、“根据你对我的了解”或提及过去的背景信息时，也应触发该功能。
user-invocable: true
---
# 从 Notion 中检索信息

从 **Memory Store**（Notion 数据库）中读取用户的记忆内容，并将其作为当前对话的上下文使用。

## 数据库发现

此技能采用 **零配置** 的方式：数据库的名称始终为 **"Memory Store"`。

**步骤 1：定位数据库**

```
POST /v1/search
{
  "query": "Memory Store"
}
```

从搜索结果中找到标题为 "Memory Store" 的条目，其 `object` 为 "data_source"。
提取以下信息：
- `data_source_id` — 用于查询（`POST /v1/data_sources/{id}/query`）
- `database_id` — 用于参考

- **如果找到** -> 使用 `data_source_id` 进行后续的所有查询。
- **如果没有找到** -> 直接跳过检索过程。**不要提示用户创建数据库**。

## 平台适配

此技能使用通用的 Notion REST API 格式进行操作。
每个平台的 AI 需要根据以下 **固定映射** 将这些操作转换为该平台可用的工具。
**请勿猜测** — 请严格按照这些映射进行操作。

### Claude Code / Claude.ai（Notion MCP 工具）

| 操作 | SKILL.md 中的描述 | 使用的 MCP 工具 | 关键参数 |
|-----------|-------------------|--------------|----------------|
| 发现数据库 | `POST /v1/search` | `notion-search` | `query: "Memory Store", `content_search_mode: "workspace_search"` |
| 获取 data_source_id | -- | `notion-fetch` | 从 `<data-source url="collection://...">` 标签中提取数据库信息 |
| 结构化查询 | `POST /v1/data_sources/{id}/query` | **不可用** | 请使用第二种方法 |
| 在数据库中进行语义搜索 | `POST /v1/search` + data_source_url | `notion-search` | `data_source_url: "collection://<data_source_id>"` |
| 获取页面详情 | `GET /v1/pages/{id}` | `notion-fetch` | `id: "<page_id>"` |

**重要提示：**
- 发现数据库时必须使用 `content_search_mode: "workspace_search"`（默认的 `ai_search` 模式可能无法返回数据库信息）
- 在 MCP 平台上，**结构化查询**（方法 1）是不可用的。在这种情况下，只能使用 **语义搜索**。对于少于 500 条记忆记录，这种方法是可以接受的。
- **不要对同一个 `data_source_url` 同时调用多个 `notion-search` — MCP 会出错**。请依次执行搜索，或者将它们合并为一个查询。
- 语义搜索的结果不包含完整的属性。需要使用 `notion-fetch` 来获取每个记忆记录的类别、状态、范围等信息。
- 在一个响应中可以**并行执行多个 `notion-fetch` 调用**，以减少延迟。

### OpenClaw

OpenClaw 通过单独安装的 **"notion" 技能** 来访问 Notion
（[clawhub.ai/steipete/notion](https://clawhub.ai/steipete/notion)）。
在使用此功能之前，必须先安装该技能。

执行时，首先阅读 `notion` 技能的 SKILL.md 文件，以了解 Notion API 的访问模式（API 密钥设置、curl 命令、端点等）。然后按照这些模式执行操作。

- 此技能中描述的所有操作（搜索、查询、获取页面详情）都直接对应于 `notion` 技能的 REST API 模式。
- 所有操作（包括结构化查询，即方法 1）都得到完全支持。

**重要提示**：此技能（recall-from-notion）是一个依赖于 Notion 连接性的 **工作流技能**。它本身并不提供对 Notion 的直接访问功能——它依赖于平台的 Notion 集成（Claude Code/Claude.ai 上的 MCP 工具，OpenClaw 上的 `notion` 技能）。

## 何时触发

**在以下情况下始终触发：**
- 用户提及之前的对话或共享的上下文（例如：“我们之前讨论过这个”，“你知道我的设置”）
- 用户开始需要个人上下文的任务（编码、写作、规划、提供建议等）
- 用户询问自己的偏好、决策或项目细节
- 用户说“回忆一下”、“记住”或类似的话

**在以下情况下也可以触发：**
- 开始新的对话，且任务与特定领域相关（例如编码、架构、DevOps 等）
- 用户提到可能存储了相关上下文的项目名称、工具或技术
- 用户请求建议或意见，而过去的偏好信息可能对此有帮助

**在以下情况下跳过：**
- 仅涉及事实性的问答，且没有个人层面的内容（例如：“Python 的 GIL 是什么”）
- 用户明确表示希望重新开始或获取通用建议

## 检索策略

### 步骤 1：发现数据库

参见上面的 “数据库发现” 部分。如果未找到数据库，则直接跳过所有后续步骤。

### 步骤 2：分析对话主题

从用户的信息或对话上下文中提取：
1. **关键词**：具体的名词、技术、工具、项目名称
   - 例如：“Notion”、“Claude Code”、“orchestrator”、“Python”
2. **语义查询**：对用户意图的自然语言总结
   - 例如：“CI 配置偏好”、“Python 项目架构决策”
3. **当前项目**（如果在 Claude Code 中）：从工作目录中检测
   - 例如：“OpenClaw”、“skills”、“claude_world”

**搜索策略建议：**
- 相比多个包含关键词的搜索，优先使用 **一个精心构造的自然语言查询**。
  - 例如，“用户背景偏好和开发工具” 比三个单独的搜索更有效。
- 对于宽泛的查询（例如“你对我了解多少”、“我的基本信息”），一个通用的查询就足够了。
- 只有在第一次搜索明显遗漏了特定主题时，才进行第二次搜索。
- 在 MCP 平台上，对同一个 `data_source_url` 的多次搜索必须依次进行（参见重要提示）。

### 步骤 3：双路径检索

使用 **两种并行路径** 来最大化检索范围，然后合并结果。

**路径 1 — 结构化查询**（精确度高，返回完整属性）：

使用关键词过滤条件查询数据源的标题、内容和项目名称。

```
POST /v1/data_sources/{data_source_id}/query
{
  "filter": {
    "or": [
      { "property": "Title", "title": { "contains": "<keyword>" } },
      { "property": "Content", "rich_text": { "contains": "<keyword>" } },
      { "property": "Project", "rich_text": { "contains": "<keyword>" } }
    ]
  },
  "page_size": 50
}
```

对于多个关键词（例如：“Notion” 和 “MCP”）：

```json
{
  "filter": {
    "or": [
      { "property": "Title", "title": { "contains": "Notion" } },
      { "property": "Content", "rich_text": { "contains": "Notion" } },
      { "property": "Title", "title": { "contains": "MCP" } },
      { "property": "Content", "rich_text": { "contains": "MCP" } }
    ]
  }
}
```

> **MCP 平台（Claude Code / Claude.ai）**：路径 1 不可用（没有结构化查询工具）。
> 直接跳到路径 2。此时检索变为单路径的语义搜索。

**路径 2 — 语义搜索**（覆盖范围广，能捕捉到关键词未涵盖的内容）：

使用步骤 2 中的语义查询在 Memory Store 中进行搜索。

```
POST /v1/search
{
  "query": "<semantic query from Step 2>",
  "data_source_url": "collection://<data_source_id>"
}
```

这种方法可以捕捉到虽然不包含确切关键词但语义相关的记忆记录。
例如，搜索 “CI 配置” 可能会找到 “GitHub Actions 工作流偏好设置”，即使该记忆记录中不包含 “CI” 这个词。

> **为什么要使用双路径？**
> 结构化查询虽然精确，但只能匹配确切的关键词，可能会遗漏语义相关的记忆记录。
> 语义搜索虽然能理解意图，但返回的属性不完整（仅包含 ID/标题/高亮部分）。
> 结合这两种方法可以同时实现精确度和覆盖范围。

### 步骤 4：合并和丰富结果

1. **合并**：将两种路径的结果合并，并根据页面 ID 去重。
2. **丰富结果**：结构化查询的结果已经包含完整的属性。对于仅通过语义搜索找到的记忆记录，需要进一步获取它们的完整属性：
   ```
   GET /v1/pages/{page_id}
   ```
   （仅获取差异部分——跳过已经在结构化查询结果中的页面。）

> **MCP 平台**：由于只有路径 2 可用，因此所有结果都需要通过 `notion-fetch` 来丰富。
> 如果进行了多次搜索，**首先根据页面 ID 去重**，然后再获取唯一的结果。
> 可以并行执行多个 `notion-fetch` 调用来减少延迟。

### 步骤 5：过滤结果

对合并后的结果应用以下过滤条件：

**范围过滤（对 Claude Code 来说尤为重要）：**
- 始终包含：Scope = Global（全局范围）
- 包含：Scope = Project（如果项目名称与当前项目匹配）
- 排除：Scope = Other Projects（其他项目）
- 包含：no Scope set（视为全局范围）

**状态过滤：**
- **矛盾的信息**：始终跳过
- **已归档的信息**：除非用户明确要求，否则跳过

**过期过滤：**
- 30 天前的记录：Source Date + 30 天 < 今天 -> 跳过
- 90 天前的记录：Source Date + 90 天 < 今天 -> 跳过
- 1 年前的记录：Source Date + 1 年 < 今天 -> 跳过
- 从未过期的记录：始终包含

### 步骤 6：排序结果

**优先级评分：**
1. **双路径检索的记录**：同时被结构化查询和语义搜索找到的记录 -> 相关性最高
2. **主题相关性**：与用户当前的问题/任务直接相关
3. **类别权重**：偏好 > 事实 > 决策 > 模式 > 技能 > 上下文
4. **时效性**：来源日期较新的记录优先

**结果限制：** 最多返回 10-15 条记忆记录。

### 步骤 7：将结果作为上下文插入

将检索到的记忆记录按照类别分组，并以紧凑的形式显示：

```
Recalled context from Memory Store:

[Preferences]
- User prefers Ruff for code formatting and linting
- ...

[Facts]
- User is a programmer, primarily uses Python
- Notion workspace connected via MCP
- ...

[Decisions]
- Memory Store uses Notion Database as storage backend
- ...
```

规则：
- 按类别分组，每条记录保留 1-2 行
- 保留关键信息（ID、命令、URL）的原样
- 只显示有记录的类别
- 直接忽略无关的记忆记录

## 处理特殊情况

**没有找到结果**：如果没有找到记忆记录，则直接进行下一步，无需特别提示用户。

**结果过多（超过 15 条）**：严格排序，仅插入前 10-15 条。请注意还有更多记录可用。

**过时或错误的记忆记录**：标记出矛盾之处，并提供更新的建议。

**“你是怎么知道的？”**：解释这些信息来自 Memory Store，并提供查看或编辑的选项。

## 重要注意事项

- **静默插入**：除非用户明确要求，否则不要显示 “正在搜索 Memory Store...” 的提示。
- **使用用户的语言**：使用用户的主要语言构建搜索查询。记忆记录是以用户的语言存储的，因此使用相同的语言进行搜索可以获得更好的检索效果。
- **优先考虑相关性**：在有疑问时，可以选择不显示某些记录。
- **注意上下文范围**：在 Claude Code 中，根据当前项目自动调整搜索范围。
- **跨平台处理**：平等对待来自所有来源（Claude.ai、Claude Code、OpenClaw）的记忆记录。
- **只读操作**：此技能仅用于从数据库中读取数据，不会进行写入操作。