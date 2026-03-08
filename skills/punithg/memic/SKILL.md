---
name: memic-sdk
version: 0.3.0
description: 这是一个用于AI代理的上下文工程平台。用户可以上传文档，使用语义化及结构化查询进行搜索，并将相关的上下文信息插入到大型语言模型（LLM）的提示中。该平台支持“检索-聚合-生成”（RAG）技术、文本转SQL功能、混合搜索模式、元数据过滤机制以及多租户隔离功能。通过使用这一技术，可以将Memic集成到任何需要从文档和数据库中获取具体上下文信息的AI代理、协作式工具或应用程序中。
homepage: https://app.memic.ai
metadata:
  openclaw:
    emoji: "🧠"
    primaryEnv: MEMIC_API_KEY
    requires:
      env:
        - MEMIC_API_KEY
      bins:
        - pip
---
# Memic — 上下文工程 SDK

## Memic 是什么？

Memic 是一个用于管理上下文工程的平台。它无需将原始文档直接放入大型语言模型（LLM）的上下文窗口中（这种方式成本高昂、速度慢且容易超出令牌限制），而是负责处理整个流程——包括文档的导入、分割、嵌入以及向量化存储，并提供一个统一的搜索 API，仅返回相关的信息。Memic 还支持将文本转换为 SQL 语句以查询结构化数据库，因此一个 API 就可以同时处理文档和数据库的查询。

**它解决的问题**：AI 代理和 LLM 应用程序需要来自真实数据的可靠上下文信息。如果没有 Memic，您就需要自己构建和维护文件分割、嵌入、向量存储以及查询路由的基础设施。而 Memic 作为一项服务，可以完成所有这些工作——只需上传文件，通过一次 API 调用即可进行搜索，并获得带有来源信息的排名结果。

**主要功能**：
- **文档搜索（RAG）**：支持上传 PDF、DOCX、PPTX、TXT 等格式的文档，对其进行分割、嵌入并建立索引。搜索结果会包含文件名、页码和相关性评分。
- **数据库搜索（Text2SQL）**：可以连接 PostgreSQL/MySQL 数据库，通过自然语言查询获取由 SQL 生成的结果。
- **混合搜索**：一个 API 可以自动将查询路由到正确的来源（文档或数据库，或同时查询两者）。
- **多租户隔离**：每个 API 密钥都针对特定的组织/项目/环境进行配置，确保数据不会在租户之间泄露。
- **元数据过滤**：支持按参考 ID、页码范围、类别和文档类型进行过滤。

您的 API 密钥会自动解析上下文信息（组织、项目、环境），因此在 API 调用中无需手动指定这些信息。

**即将推出的功能**：
- **MCP 服务器**：实现模型上下文协议的原生集成，使 AI 代理（如 OpenClaw、Claude Code 等）可以直接使用 Memic 作为工具。
- **上下文压缩**：支持上传原始的代理会话日志或 MEMORY.md 文件，Memic 会对其进行总结、压缩并建立索引，以便代理无需重新加载整个会话历史即可获取所需上下文。
- **批量上下文注入**：支持一次性上传整个知识库（如会话 JSONL 数据、聊天记录、维基导出文件），Memic 会自动进行分割和索引，实现即时搜索。

**何时使用此技能**：在设置 Memic SDK、上传文档、搜索上下文、构建 RAG 流程、连接数据库以使用 Text2SQL、调试集成问题，或通过使用定向搜索替代原始上下文来降低 LLM 的令牌使用成本时。

## 快速入门

```bash
pip install memic
export MEMIC_API_KEY=mk_your_key_here
```

```python
from memic import Memic

client = Memic()  # API key auto-resolves org/project/environment

# Upload a document
file = client.upload_file("/path/to/doc.pdf")

# Search — returns only the relevant chunks, not the whole document
results = client.search(query="What are the key findings?", top_k=5)
for r in results:
    print(f"[{r.score:.2f}] {r.file_name} p{r.page_number}: {r.content[:100]}")
```

## 首先：了解使用场景

**向开发者提出两个问题：**

### 问题 1：集成方式**
“您计划如何使用 Memic？”

1. **作为 AI 代理的上下文工具**：Memic 为 LLM 代理（如聊天机器人、代码助手等）提供 RAG（Retrieval, Aggregation, Generation）上下文。
2. **确定性搜索服务**：在您的应用程序中直接使用搜索 API（无需依赖 LLM）。

### 问题 2：数据来源**
“您将搜索哪种类型的数据？”

1. **非结构化数据（文档）**：PDF、Word 文档、文本文件 → 使用语义向量化搜索。
2. **结构化数据（数据库）**：PostgreSQL/MySQL → 通过自然语言查询转换为 SQL 语句。
3. **混合数据**：通过一个 API 同时查询文档和数据库。

## 先决条件**
- Python 3.8 或更高版本。
- 在 https://app.memic.ai 上注册一个 Memic 账户。
- 拥有一个 API 密钥（以 `mk_...` 开头）。

## 第一步：获取 API 密钥**

1. 访问 https://app.memic.ai → 仪表板 → API 密钥。
2. 点击“创建 API 密钥”。
3. 复制密钥。

**重要提示**：每个 API 密钥都针对特定的组织/项目/环境进行配置。SDK 会自动解析这些信息，因此您无需在 API 调用中手动指定这些信息。

## 第二步：安装和配置

```bash
pip install memic
```

```bash
# .env file
MEMIC_API_KEY=mk_your_api_key_here
```

## 第三步：验证设置

```python
from memic import Memic

client = Memic()

# Check what your API key resolves to
print(f"Org: {client.org_id}")
print(f"Project: {client.project_id}")
print(f"Environment: {client.environment_slug}")

# List projects in your org
projects = client.list_projects()
for p in projects:
    print(f"  - {p.name} ({p.id})")
```

### 如果未找到数据

**对于文档**：可以通过仪表板（https://app.memic.ai → 项目 → 上传）或 SDK（详见下方）进行上传。

**对于数据库**：访问 https://app.memic.ai → 连接器 → 添加连接器，然后输入您的 PostgreSQL/MySQL 连接详细信息。

## 核心 API 参考

### 上传文件

```python
# Upload and wait for processing to complete
file = client.upload_file(
    file_path="/path/to/document.pdf",
    reference_id="lesson_123",       # optional — for external system linking
    metadata={"category": "legal"},  # optional — custom key-value pairs
)
print(f"ID: {file.id}, Status: {file.status}")  # status = "ready" when done
```

支持的文件格式：PDF、DOCX、DOC、PPTX、XLSX、TXT、MD、HTML 等。

### 检查文件状态

```python
file = client.get_file_status(file_id="...")
print(f"Status: {file.status}")
print(f"Processing: {file.status.is_processing}")
print(f"Failed: {file.status.is_failed}")
print(f"Chunks: {file.total_chunks}")
```

### 搜索文档（语义搜索）

```python
results = client.search(
    query="What are the key findings?",
    top_k=10,
    min_score=0.7,
)

print(f"Found {results.total_results} results in {results.search_time_ms}ms")
for r in results:
    print(f"[{r.score:.2f}] {r.file_name} p{r.page_number}: {r.content[:150]}")
```

### 使用元数据过滤进行搜索

```python
from memic import MetadataFilters, PageRange

results = client.search(
    query="contract terms",
    top_k=5,
    filters=MetadataFilters(
        reference_id="contract_2024",              # filter by reference
        page_range=PageRange(gte=1, lte=20),       # pages 1-20 only
        category="legal",                          # by category
    )
)
```

**可用过滤条件**：
- `reference_id` / `reference_ids`：匹配文件引用 ID。
- `page_number` / `page_numbers`：精确匹配页码。
- `page_range`：指定页码范围（使用 `gte`/`lte`）。
- `category`：按类别过滤。
- `document_type`：按文档类型过滤。

### 按文件范围进行搜索

```python
# Search only within specific files
results = client.search(
    query="revenue figures",
    file_ids=["file-id-1", "file-id-2"],
    top_k=5,
)
```

### 混合搜索（文档 + 数据库）

当配置好了文档和数据库的连接器后，Memic 会自动将查询路由到相应的来源。

```python
results = client.search(query="Show me top customers by revenue")

# Check how the query was routed
if results.routing:
    print(f"Route: {results.routing.route}")        # "semantic", "structured", or "hybrid"
    print(f"Reason: {results.routing.reasoning}")

# Document results
if results.has_documents:
    for r in results.results.semantic:
        print(f"[Doc] {r.file_name}: {r.content[:100]}")

# Database results (Text2SQL)
if results.has_structured:
    print(f"SQL: {results.routing.sql_generated}")
    for row in results.results.structured.rows:
        print(f"[DB] {row}")
```

### 聊天（结合内置 LLM 的 RAG 功能）

```python
response = client._request(
    "POST", "/sdk/chat",
    json={"question": "What are the Q4 results?", "top_k": 5, "min_score": 0.5}
)
print(response["answer"])
print(f"Citations: {response['citations']}")
print(f"Model: {response['model']}")
```

## 集成方式

### 方式 A：作为 AI 代理的上下文工具

使用 Memic 为 LLM 代理提供所需的上下文信息：

```python
from memic import Memic
from openai import OpenAI  # or anthropic, etc.

memic = Memic()
llm = OpenAI()

def ask_with_context(question: str) -> str:
    # 1. Get relevant context from Memic
    results = memic.search(query=question, top_k=5, min_score=0.6)

    # 2. Format as LLM context
    context = "\n\n".join([
        f"[Source: {r.file_name}, Page {r.page_number}]\n{r.content}"
        for r in results
    ])

    # 3. Generate grounded response
    response = llm.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Answer based on this context:\n\n{context}"},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

answer = ask_with_context("What are the key contract terms?")
```

### 方式 B：优化 OpenClaw / AI 代理的上下文加载

通过使用定向搜索替代昂贵的原始上下文加载方式，从而降低令牌使用成本：

```python
from memic import Memic

memic = Memic()

# Instead of loading entire documents into context (thousands of tokens),
# search for just the relevant chunks (hundreds of tokens)
results = memic.search(query=user_question, top_k=3, min_score=0.7)

# Only inject what's relevant — typically 90%+ token savings vs raw context
context = "\n".join([r.content for r in results])
```

### 方式 C：确定性搜索 API

直接将 Memic 的搜索功能集成到应用程序中：

```python
from memic import Memic, MetadataFilters

memic = Memic()

def search_documents(query: str, category: str = None) -> dict:
    filters = MetadataFilters(category=category) if category else None

    results = memic.search(
        query=query,
        top_k=10,
        min_score=0.5,
        filters=filters,
    )

    return {
        "results": [
            {
                "title": r.file_name,
                "snippet": r.content[:300],
                "page": r.page_number,
                "score": r.score,
            }
            for r in results
        ],
        "total": results.total_results,
    }
```

## 调试

| 错误类型 | 解决方案 |
|---------|----------|
| `AuthenticationError` | 确保 `MEMIC_API_KEY` 已设置且有效。|
| `NotFoundError` | API 密钥可能配置错误（指向了错误的组织或项目）。|
| 没有找到结果 | 确保文件已上传且状态显示为“READY”。|
| 搜索结果相关性较低 | 降低 `min_score` 值或重新表述查询语句。|
| 上传失败（超时） | 大文件上传时间较长；增加 `poll_timeout` 值。|

### 异常处理

```python
from memic import MemicError, AuthenticationError, NotFoundError, APIError

try:
    results = client.search(query="test")
except AuthenticationError:
    print("Invalid or expired API key")
except NotFoundError:
    print("Resource not found")
except APIError as e:
    print(f"API error {e.status_code}: {e.message}")
except MemicError as e:
    print(f"SDK error: {e}")
```

## 资源

- **SDK**：`pip install memic` | https://pypi.org/project/memic/
- **仪表板**：https://app.memic.ai
- **GitHub**：https://github.com/memic-ai/memic-python