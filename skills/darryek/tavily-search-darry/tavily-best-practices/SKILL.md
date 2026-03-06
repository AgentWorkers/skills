---
name: tavily-best-practices
description: "构建具备最佳实践的、可投入生产环境的 Tavily 集成方案。为使用编码辅助工具（如 Claude Code、Cursor 等）的开发者提供参考文档，帮助他们实现网页搜索、内容提取、爬虫功能以及研究工作，这些功能可应用于代理工作流程（agent workflows）、RAG（Retrieval, Augmentation, and Generation）系统或自主代理（autonomous agents）中。"
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

请参阅 **[references/sdk.md](references/sdk.md)** 以获取完整的 SDK 参考文档。

## 客户端初始化

```python
from tavily import TavilyClient

# 推荐使用环境变量 TAVILY_API_KEY
client = TavilyClient()

# 如果需要项目跟踪功能（适用于企业级使用），请指定项目 ID
client = TavilyClient(project_id="your-project-id")

# 异步客户端，用于并行执行多个查询
from tavily import AsyncTavilyClient
async_client = AsyncTavilyClient()
```

## 选择合适的方法

**针对自定义代理/工作流程:**

| 需求 | 方法 |
|------|--------|
| 网页搜索结果 | `search()` |
| 从特定 URL 提取内容 | `extract()` |
| 从整个网站提取内容 | `crawl()` |
| 从网站中发现 URL | `map()` |

**针对即开即用的研究功能:**

| 需求 | 方法 |
|------|--------|
| 使用 AI 进行端到端的研究 | `research()` |

## 快速参考

### `search()` - 网页搜索

```python
response = client.search(
    query="quantum computing breakthroughs",  # 请确保查询字符串长度不超过 400 个字符
    max_results=10,
    search_depth="advanced"
)
print(response)
```
关键参数：`query`、`max_results`、`search_depth`（可选值：ultra-fast、fast、basic、advanced）、`include_domains`、`exclude_domains`、`time_range`

请参阅 **[references/search.md](references/search.md)** 以获取完整的搜索功能参考文档。

### `extract()` - URL 内容提取

```python
# 单步提取内容
response = client.extract(
    urls=["https://docs.example.com"],
    extract_depth="advanced"
)
print(response)
```
关键参数：`urls`（最多 20 个 URL）、`extract_depth`、`query`、`chunks_per_source`（1-5）

请参阅 **[references/extract.md](references/extract.md)** 以获取完整的提取功能参考文档。

### `crawl()` - 全站内容提取

```python
response = client.crawl(
    url="https://docs.example.com",
    instructions="Find API documentation pages",  # 语义化搜索指令
    extract_depth="advanced"
)
print(response)
```
关键参数：`url`、`max_depth`、`max_breadth`、`limit`、`instructions`、`chunks_per_source`、`select_paths`、`exclude_paths`

请参阅 **[references/crawl.md](references/crawl.md)** 以获取完整的全站内容提取功能参考文档。

### `map()` - URL 发现

```python
response = client.map(
    url="https://docs.example.com")
print(response)
```

### `research()` - 基于 AI 的研究功能

```python
import time

# 进行多主题的综合研究
result = client.research(
    input="Analyze competitive landscape for X in SMB market",
    model="pro"  # 可选值："mini"（用于简化查询）或 "auto"（自动选择模型）
request_id = result["request_id"]

# 等待研究结果完成
while response["status"] not in ["completed", "failed"]:
    time.sleep(10)
    response = client.get_research(request_id)

print(response["content"])  # 研究报告内容
```
关键参数：`input`、`model`（可选值："mini"、"pro"、"auto"）、`stream`、`output_schema`、`citation_format`

请参阅 **[references/research.md](references/research.md)** 以获取完整的研究功能参考文档。

## 详细指南

有关所有参数、响应字段、使用模式和示例的详细信息，请参阅以下文档：

- **[references/sdk.md]**（Python 和 JavaScript SDK 参考文档）：包括异步操作模式和混合式检索（Hybrid RAG）功能
- **[references/search.md]**：查询优化、搜索深度设置、域名过滤、异步操作模式、后续过滤步骤
- **[references/extract.md]**：一步提取与两步提取的差异、查询/数据块的选择、高级提取模式
- **[references/crawl.md]**：爬取与 URL 发现的对比、语义化搜索指令、使用场景、先使用 `map()` 再使用 `extract()` 的操作流程
- **[references/research.md]**：最佳提示输入方式、模型选择、数据流处理、结构化输出格式
- **[references/integrations.md]**：与 LangChain、LlamaIndex、CrewAI、Vercel AI SDK 及其他框架的集成方式