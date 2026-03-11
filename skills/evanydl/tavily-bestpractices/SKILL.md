---
name: tavily-best-practices
description: "构建具备最佳实践的、可投入生产的 Tavily 集成方案。为使用编码辅助工具（如 Claude Code、Cursor 等）的开发者提供参考文档，帮助他们实现网页搜索、内容提取、爬取以及研究等功能，这些功能可应用于代理工作流程（agent workflows）、RAG（Retrieval, Augmentation, Generation）系统或自主代理（autonomous agents）中。"
---
# Tavily

Tavily 是一个专为大型语言模型（LLMs）设计的搜索 API，它使 AI 应用程序能够访问实时的网络数据。

## 安装

**Python:**
```bash
pip install tavily-python
```

**JavaScript:**
```bash
npm install @tavily/core
```

有关完整的 SDK 参考信息，请参阅 **[references/sdk.md](references/sdk.md)**。

## 客户端初始化
```python
from tavily import TavilyClient

# Uses TAVILY_API_KEY env var (recommended)
client = TavilyClient()

#With project tracking (for usage organization)
client = TavilyClient(project_id="your-project-id")

# Async client for parallel queries
from tavily import AsyncTavilyClient
async_client = AsyncTavilyClient()
```

## 选择合适的方法

**对于自定义代理/工作流程:**

| 需求 | 方法 |
|------|--------|
| 网页搜索结果 | `search()` |
| 特定 URL 的内容 | `extract()` |
| 整个网站的内容 | `crawl()` |
| 从网站中发现 URL | `map()` |

**对于即用的研究功能:**

| 需求 | 方法 |
|------|--------|
| 基于 AI 的端到端研究 | `research()` |

## 快速参考

### `search()` - 网页搜索

```python
response = client.search(
    query="quantum computing breakthroughs",  # Keep under 400 chars
    max_results=10,
    search_depth="advanced"
)
print(response)
```
关键参数：`query`（查询字符串）、`max_results`（返回结果数量）、`search_depth`（搜索深度：超快/快速/基本/高级）、`include_domains`（包含的域名）、`exclude_domains`（排除的域名）、`time_range`（时间范围）

有关完整的搜索功能参考信息，请参阅 **[references/search.md](references/search.md)**。

### `extract()` - URL 内容提取

```python
# Simple one-step extraction
response = client.extract(
    urls=["https://docs.example.com"],
    extract_depth="advanced"
)
print(response)
```
关键参数：`urls`（最多 20 个 URL）、`extract_depth`（提取深度）、`query`（查询字符串）、`chunks_per_source`（每个来源的提取块数量，范围 1-5）

有关完整的提取功能参考信息，请参阅 **[references/extract.md](references/extract.md)**。

### `crawl()` - 全站内容提取

```python
response = client.crawl(
    url="https://docs.example.com",
    instructions="Find API documentation pages",  # Semantic focus
    extract_depth="advanced"
)
print(response)
```
关键参数：`url`（要爬取的 URL）、`max_depth`（最大爬取深度）、`max_breadth`（最大遍历宽度）、`limit`（限制条件）、`instructions`（爬取指令）、`chunks_per_source`（每个来源的提取块数量）、`select_paths`（需要提取的路径）、`exclude_paths`（需要排除的路径）

有关完整的爬取功能参考信息，请参阅 **[references/crawl.md](references/crawl.md)**。

### `map()` - URL 发现

```python
response = client.map(
    url="https://docs.example.com"
)
print(response)
```

### `research()` - 基于 AI 的研究功能

```python
import time

# For comprehensive multi-topic research
result = client.research(
    input="Analyze competitive landscape for X in SMB market",
    model="pro"  # or "mini" for focused queries, "auto" when unsure
)
request_id = result["request_id"]

# Poll until completed
response = client.get_research(request_id)
while response["status"] not in ["completed", "failed"]:
    time.sleep(10)
    response = client.get_research(request_id)

print(response["content"])  # The research report
```

关键参数：`input`（输入数据）、`model`（模型类型：“mini”/“pro”/“auto”）、`stream`（数据流类型）、`output_schema`（输出格式）、`citation_format`（引用格式）

有关完整的搜索功能参考信息，请参阅 **[references/research.md](references/research.md)**。

## 详细指南

有关所有参数、响应字段、使用模式和示例的详细信息，请参阅以下文档：

- **[references/sdk.md](references/sdk.md)** - Python 和 JavaScript SDK 参考文档，包含异步处理模式和混合式检索（RAG）功能。
- **[references/search.md](references/search.md)** - 查询优化、搜索深度设置、域名过滤、异步处理模式、后续过滤操作。
- **[references/extract.md](references/extract.md)** - 一步提取与两步提取的差异、查询字符串与提取块的使用方法、高级提取模式。
- **[references/crawl.md](references/crawl.md)** - 爬取与 URL 发现功能的区别、语义聚焦的设置方法、使用场景以及“先映射再提取”的处理流程。
- **[references/research.md](references/research.md)** - 提示生成的最佳实践、模型选择方法、数据流处理方式、结构化输出格式。
- **[references/integrations.md](references/integrations.md)** - 与 LangChain、LlamaIndex、CrewAI、Vercel AI SDK 等框架的集成方法。