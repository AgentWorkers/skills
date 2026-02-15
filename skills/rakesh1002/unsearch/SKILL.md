---
name: unsearch
version: 1.0.0
description: 使用 UnSearch API 进行网络搜索、内容抓取以及深入研究。当用户需要实时网络搜索结果、从 URL 中提取内容、事实验证，或者为 AI 代理、RAG（Retrieval, Augmentation, and Generation）流程或 LLM（Large Language Model）应用程序进行多源研究时，可以使用该 API。
metadata: {"openclaw":{"emoji":"🔍","homepage":"https://unsearch.dev","primaryEnv":"UNSEARCH_API_KEY","requires":{"env":["UNSEARCH_API_KEY"]}}}
---

# UnSearch：网络搜索工具

UnSearch 是一个基于开源技术的 Web 搜索工具，可作为 Tavily 或 Exa 的替代方案，支持网络搜索、内容提取、事实验证以及深度研究等功能。

## 快速入门

1. **设置 API 密钥：**
   请将以下代码中的 ````bash
export UNSEARCH_API_KEY="uns_your_api_key"
```` 替换为你的 API 密钥：
   ```python
   UNSEARCH_API_KEY = "your_api_key_here"
   ```

2. 你可以在 [https://unsearch.dev](https://unsearch.dev) 免费获取一个 API 密钥（每月 5,000 次查询）。

## API 端点

**基础 URL：** `https://api.unsearch.dev/api/v1`

所有请求都需要添加以下头部信息：`X-API-Key: $UNSEARCH_API_KEY`

---

## 1. **网络搜索**  
支持网络搜索，并可选择是否提取页面内容。

### 关键参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|---------|-------------|
| `query` | 字符串 | 必填 | 搜索查询（1-500 个字符） |
| `engines` | 字符串数组 | ["google", "bing", "duckduckgo"] | 搜索引擎 |
| `max_results` | 整数 | 10 | 返回的结果数量（1-100） |
| `scrape_content` | 布尔值 | true | 提取完整页面内容 |
| `language` | 字符串 | "en" | ISO 639-1 语言代码 |

### 响应结果

---

## 2. **智能搜索（兼容 Tavily）**  
提供智能化的搜索功能，并可选择是否生成答案。

### 关键参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|---------|-------------|
| `query` | 字符串 | 必填 | 搜索查询 |
| `include_answer` | 布尔值/字符串 | 是否生成 AI 答案（`true`, `"basic"`, `"advanced"`, `"production"`） |
| `search_depth` | 字符串 | "basic", "advanced", "fast" | 搜索深度 |
| `max_results` | 整数 | 5 | 返回的结果数量（1-20） |
| `include_raw_content` | 布尔值 | 是否包含原始页面内容 |
| `include_domains` | 字符串数组 | null | 仅搜索指定域名 |
| `exclude_domains` | 字符串数组 | null | 排除指定域名 |

### 响应结果

---

## 3. **内容提取**  
从指定 URL 中提取内容。

### 响应结果

---

## 4. **深度研究**  
支持多源信息整合及 AI 合成分析。

### 深度级别

| 深度 | 数据来源 | 适用场景 |
|------|---------|----------|
| `quick` | 3-5 | 快速概览 |
| `standard` | 5-10 | 平衡性分析 |
| `deep` | 10-20 | 详细分析 |
| `comprehensive` | 20-30 | 专家级分析 |

### 响应结果

---

## 5. **事实验证**  
可对比多个来源验证信息真实性。

### 响应结果

验证结果类型：`true`, `false`, `partially_true`, `misleading`, `unverifiable`

---

## Python 示例

（示例代码请参见 [此处](```python
import httpx
import os

API_KEY = os.environ["UNSEARCH_API_KEY"]
BASE_URL = "https://api.unsearch.dev/api/v1"

async def search(query: str, scrape: bool = False):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/search",
            headers={"X-API-Key": API_KEY},
            json={
                "query": query,
                "max_results": 10,
                "scrape_content": scrape
            }
        )
        return response.json()

async def agent_search(query: str, include_answer: bool = True):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/agent/search",
            headers={"X-API-Key": API_KEY},
            json={
                "query": query,
                "include_answer": include_answer,
                "max_results": 5
            }
        )
        return response.json()

async def extract_urls(urls: list[str]):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/agent/extract",
            headers={"X-API-Key": API_KEY},
            json={"urls": urls}
        )
        return response.json()
```)）

## JavaScript 示例

（示例代码请参见 [此处](```javascript
const API_KEY = process.env.UNSEARCH_API_KEY;
const BASE_URL = "https://api.unsearch.dev/api/v1";

async function search(query, scrapeContent = false) {
  const response = await fetch(`${BASE_URL}/search`, {
    method: "POST",
    headers: {
      "X-API-Key": API_KEY,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      query,
      max_results: 10,
      scrape_content: scrapeContent
    })
  });
  return response.json();
}

async function agentSearch(query, includeAnswer = true) {
  const response = await fetch(`${BASE_URL}/agent/search`, {
    method: "POST",
    headers: {
      "X-API-Key": API_KEY,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      query,
      include_answer: includeAnswer,
      max_results: 5
    })
  });
  return response.json();
}
```)

---

## 使用限制

| 计划类型 | 每月查询次数 | 使用限制 |
|------|---------------|------------|
| 免费 | 5,000 | 每分钟 10 次 |
| 专业版 | 25,000 | 每分钟 60 次 |
| 高级版 | 100,000 | 每分钟 200 次 |
| 超级版 | 500,000 | 每分钟 1,000 次 |

响应中的使用限制相关信息：
- `X-RateLimit-Remaining`：剩余请求次数 |
- `X-RateLimit-Reset`：重置时间戳 |

---

## 隐私设置  
对于敏感查询，可启用“零数据保留”模式。

---

## 错误处理

| 错误代码 | 描述 |
|------|-------------|
| 401 | API 密钥无效 |
| 429 | 使用次数达到限制（请查看 `Retry-After` 头部信息） |
| 422 | 验证错误 |
| 500 | 服务器错误 |

---

## 额外资源

- **文档：** [https://docs.unsearch.dev](https://docs.unsearch.dev) |
- **API 参考：** [https://docs.unsearch.dev/api](https://docs.unsearch.dev/api) |
- **自托管：** [https://github.com/unsearch-org/unsearch](https://github.com/unsearch-org/unsearch) |
- **获取 API 密钥：** [https://unsearch.dev](https://unsearch.dev)