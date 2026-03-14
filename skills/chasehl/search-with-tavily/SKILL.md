---
name: tavily-search
description: 使用 Tavily API 进行网络搜索——Tavily 是一个专为 AI 代理设计的强大搜索引擎。当您需要从互联网上查找当前信息、新闻、研究资料或任何需要最新网络数据的主题时，可以使用它。该 API 支持多种搜索模式，包括基本搜索、问答模式以及用于 RAG（Retrieval with Answer Generation，基于答案的检索）应用的语境检索功能。
metadata:
  openclaw:
    emoji: 🔍
    requires:
      env:
        - TAVILY_API_KEY
---
# Tavily 搜索

使用 Tavily API 进行网络搜索——专为 AI 代理和检索增强型生成（RAG）应用程序优化。

## 快速入门

### 先决条件

设置您的 Tavily API 密钥：
```bash
export TAVILY_API_KEY="tvly-your-api-key"
```

或者直接使用带有 API 密钥的 Python 客户端。

### 基本搜索

```python
from tavily import TavilyClient

client = TavilyClient(api_key="tvly-your-api-key")
response = client.search("Latest AI developments")

for result in response['results']:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Content: {result['content'][:200]}...")
```

### 问答搜索（获取直接答案）

```python
answer = client.qna_search(query="Who won the 2024 US Presidential Election?")
print(answer)
```

### 上下文搜索（适用于检索增强型生成应用程序）

```python
context = client.get_search_context(
    query="Climate change effects on agriculture",
    max_tokens=4000
)
# Use context directly in LLM prompts
```

## 搜索参数

### 常见参数

| 参数 | 类型 | 描述 | 默认值 |
|-----------|------|-------------|---------|
| `query` | 字符串 | 搜索查询（必填） | - |
| `search_depth` | 字符串 | "basic" 或 "comprehensive" | "basic" |
| `max_results` | 整数 | 结果数量（1-20） | 5 |
| `include_answer` | 布尔值 | 是否包含 AI 生成的答案 | False |
| `include_raw_content` | 布尔值 | 是否包含完整页面内容 | False |
| `include_images` | 布尔值 | 是否包含图片链接 | False |

### 高级参数

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `topic` | 字符串 | 搜索主题："general" 或 "news" |
| `time_range` | 字符串 | 时间筛选："day", "week", "month", "year" |
| `include_domains` | 列表 | 限制在特定域名内 |
| `exclude_domains` | 列表 | 排除特定域名 |
| `exact_match` | 布尔值 | 是否要求精确短语匹配 |

## 响应格式

### 标准搜索响应

```json
{
  "query": "search query",
  "results": [
    {
      "title": "Result Title",
      "url": "https://example.com/article",
      "content": "Snippet or full content...",
      "score": 0.95,
      "raw_content": "Full page content (if requested)..."
    }
  ],
  "answer": "AI-generated answer (if requested)",
  "images": ["image_url1", "image_url2"],
  "response_time": 1.23
}
```

## 错误处理

### 常见错误

```python
from tavily import TavilyClient
from tavily.exceptions import TavilyError, RateLimitError, InvalidAPIKeyError

client = TavilyClient(api_key="your-api-key")

try:
    response = client.search("query")
except InvalidAPIKeyError:
    print("Invalid API key. Check your TAVILY_API_KEY.")
except RateLimitError:
    print("Rate limit exceeded. Please wait before retrying.")
except TavilyError as e:
    print(f"Tavily error: {e}")
```

## 最佳实践

### 1. 对于检索增强型生成（RAG），使用上下文搜索

对于检索增强型生成（RAG）应用，使用 `get_search_context()` 而不是标准搜索：

```python
context = client.get_search_context(
    query=user_query,
    max_tokens=4000,  # Fit within your LLM's context window
    search_depth="comprehensive"
)

# Use in prompt
prompt = f"""Based on the following context:
{context}

Answer this question: {user_query}"""
```

### 2. 处理速率限制

Tavily 有速率限制。请实施指数退避策略：

```python
import time
from tavily.exceptions import RateLimitError

def search_with_retry(client, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.search(query)
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

### 3. 筛选结果

使用域名过滤器来提高结果质量：

```python
# Only search trusted news sources
response = client.search(
    query="breaking news",
    include_domains=["bbc.com", "reuters.com", "apnews.com"],
    time_range="day"  # Only recent news
)
```

### 4. 对于事实性问题，使用问答模式

对于事实性问题，使用问答模式以获取直接答案：

```python
# Good for: "Who won the 2024 election?"
answer = client.qna_search("Who won the 2024 US Presidential Election?")

# Good for: "What is the capital of France?"
answer = client.qna_search("Capital of France")
```

## 额外资源

- **Tavily 文档**：https://docs.tavily.com
- **Python SDK**：https://github.com/tavily-ai/tavily-python
- **JavaScript SDK**：https://github.com/tavily-ai/tavily-js
- **API 参考**：https://docs.tavily.com/documentation/api-reference

## 技能维护

此技能需要：
- 设置 `TAVILY_API_KEY` 环境变量
- 安装 `tavily-python` 包（`pip install tavily-python`）

如有问题或需要更新，请参考 Tavily 文档或 GitHub 仓库。