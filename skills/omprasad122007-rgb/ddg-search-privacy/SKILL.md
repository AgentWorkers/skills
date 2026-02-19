---
name: duckduckgo-search
version: 1.0.0
description: DuckDuckGo 是一款提供无隐私追踪功能的网页搜索引擎。当用户需要在网上搜索信息或进行基于网页的研究时，DuckDuckGo 可确保搜索过程不会被第三方追踪。它非常适合用于快速查找在线资料、验证事实以及发现相关网页的链接。
---
# DuckDuckGo 网页搜索

使用 DuckDuckGo API 进行私密网页搜索，实现无跟踪的信息检索。

## 核心特性

- 以隐私为中心的搜索（无跟踪）
- 即时答案支持
- 多种搜索模式（网页、图片、视频、新闻）
- 以 JSON 格式输出结果，便于解析
- 无需 API 密钥

## 快速入门

### 基本网页搜索

```python
import requests

def search_duckduckgo(query, max_results=10):
    """
    Perform DuckDuckGo search and return results.

    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 10)

    Returns:
        List of search results with title, url, description
    """
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 0
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Extract results
    results = []

    # Abstract (instant answer)
    if data.get("Abstract"):
        results.append({
            "type": "instant_answer",
            "title": "Instant Answer",
            "content": data["Abstract"],
            "source": data.get("AbstractSource", "DuckDuckGo")
        })

    # Related topics
    if data.get("RelatedTopics"):
        for topic in data["RelatedTopics"][:max_results]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append({
                    "type": "related",
                    "title": topic.get("FirstURL", "").split("/")[-1].replace("-", " ").title(),
                    "content": topic["Text"],
                    "url": topic.get("FirstURL", "")
                })

    return results[:max_results]
```

### 高级用法（HTML 抓取）

```python
from bs4 import BeautifulSoup
import requests

def search_with_results(query, max_results=10):
    """
    Perform DuckDuckGo search and scrape actual results.

    Args:
        query: Search query string
        max_results: Maximum number of results to return

    Returns:
        List of search results with title, url, snippet
    """
    url = "https://duckduckgo.com/html/"
    params = {"q": query}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.post(url, data=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for result in soup.find_all("a", class_="result__a", href=True)[:max_results]:
        results.append({
            "title": result.get_text(),
            "url": result["href"],
            "snippet": result.find_parent("div", class_="result__body").get_text().strip()
        })

    return results
```

## 搜索操作符

DuckDuckGo 支持以下标准搜索操作符：

| 操作符 | 例子 | 说明 |
|----------|---------|-------------|
| `""` | `"精确短语"` | 精确匹配短语 |
| `-` | `python -django` | 排除特定术语 |
| `site:` | `site:wikipedia.org history` | 在特定网站上搜索 |
| `filetype:` | `filetype:pdf report` | 指定文件类型 |
| `intitle:` | `intitle:openclaw` | 在标题中包含的关键词 |
| `inurl:` | `inurl:docs/` | 在 URL 中包含的关键词 |
| `OR` | `docker OR kubernetes` | 任一术语 |

## 搜索模式

### 网页搜索
默认模式，可在整个网页范围内进行搜索。

```python
search_with_results("machine learning tutorial")
```

### 图片搜索
```python
def search_images(query, max_results=10):
    url = "https://duckduckgo.com/i.js"
    params = {
        "q": query,
        "o": "json",
        "vqd": "",  # Will be populated
        "f": ",,,",
        "p": "1"
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []
    for result in data.get("results", [])[:max_results]:
        results.append({
            "title": result.get("title", ""),
            "url": result.get("image", ""),
            "thumbnail": result.get("thumbnail", ""),
            "source": result.get("source", "")
        })

    return results
```

### 新闻搜索
在查询中添加 `!news`：

```python
search_duckduckgo("artificial intelligence !news")
```

## 最佳实践

### 查询构建

**良好的查询示例：**
- `"DuckDuckGo API documentation 2024"`（具体且最新的内容）
- `site:github.com openclaw issues`（目标特定的网站）
- `python machine learning tutorial filetype:pdf`（指定资源类型）

**应避免的查询：**
- 模糊的单词（如 `"search"`、`"find"`）
- 过于复杂的操作符，可能导致结果混乱
- 包含多个不相关主题的查询

### 隐私注意事项

DuckDuckGo 的优势：
- ✅ 无个人数据跟踪
- ✅ 不存储搜索历史记录
- ✅ 不进行用户画像
- ✅ 不提供强制性的个性化搜索结果

### 性能提示

1. **使用 HTML 抓取获取实际结果**：虽然 JSON API 可提供即时答案，但返回的结果列表有限。
2. **适当延迟请求**：在多次请求时遵守速率限制。
3. **缓存结果**：存储常见的搜索内容，以避免重复调用 API。

## 错误处理

```python
def search_safely(query, retries=3):
    for attempt in range(retries):
        try:
            results = search_with_results(query)
            if results:
                return results
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff

    return []
```

## 输出格式

### Markdown 格式
```python
def format_results_markdown(results, query):
    output = f"# Search Results for: {query}\n\n"

    for i, result in enumerate(results, 1):
        output += f"## {i}. {result.get('title', 'Untitled')}\n\n"
        output += f"**URL:** {result.get('url', 'N/A')}\n\n"
        output += f"{result.get('snippet', result.get('content', 'N/A'))}\n\n"
        output += "---\n\n"

    return output
```

### JSON 格式
```python
import json

def format_results_json(results, query):
    return json.dumps({
        "query": query,
        "count": len(results),
        "results": results,
        "timestamp": datetime.now().isoformat()
    }, indent=2)
```

## 常见用法

### 查找文档
```python
search_duckduckgo(f'{library_name} documentation filetype:md')
```

### 最新信息
```python
search_duckduckgo(f'{topic} 2024 news')
```

### 故障排除
```python
search_duckduckgo(f'{error_message} {tool_name} stackoverflow')
```

### 技术对比
```python
search_duckduckgo('postgresql vs mysql performance 2024')
```

## 集成示例
```python
class DuckDuckGoSearcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def search(self, query, mode="web", max_results=10):
        """
        Unified search interface.

        Args:
            query: Search query
            mode: 'web', 'images', 'news'
            max_results: Maximum results

        Returns:
            Formatted results as list
        """
        if mode == "images":
            return self._search_images(query, max_results)
        elif mode == "news":
            return self._search_web(f"{query} !news", max_results)
        else:
            return self._search_web(query, max_results)

    def _search_web(self, query, max_results):
        # Implementation
        pass

    def _search_images(self, query, max_results):
        # Implementation
        pass
```

## 资源

### 官方文档
- DuckDuckGo API 文档：https://duckduckgo.com/api
- 即时答案 API：https://duckduckgo.com/params
- 搜索语法：https://help.duckduckgo.com/duckduckgo-help-pages/results/syntax/

### 参考资料
- 用于提取结果的 HTML 抓取技巧
- 速率限制的最佳实践
- 结果的解析与过滤方法