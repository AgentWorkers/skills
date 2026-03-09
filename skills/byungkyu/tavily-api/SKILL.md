---
name: tavily
description: >
  **Tavily API集成与管理的API密钥认证**  
  支持基于AI的网页搜索、从URL中提取内容、爬取网站信息、分析网站结构以及执行研究任务。  
  当用户需要执行网页搜索、提取页面内容、爬取网站数据、发现新的URL地址或进行包含引用的深入研究时，可使用此功能。  
  对于其他第三方应用程序，请使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。  
  该功能需要网络连接以及有效的Maton API密钥。
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# Tavily

您可以使用托管的API密钥进行身份验证来访问Tavily API。该API支持人工智能驱动的网页搜索、从URL中提取内容、爬取网站信息、映射网站结构以及执行深入的研究任务。

## 快速入门

```bash
# Search the web
python <<'EOF'
import urllib.request, os, json
data = json.dumps({"query": "latest AI news", "max_results": 5}).encode()
req = urllib.request.Request('https://gateway.maton.ai/tavily/search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/tavily/{endpoint}
```

请将 `{endpoint}` 替换为相应的Tavily API端点（如 `search`、`extract`、`crawl`、`map` 或 `research`）。Tavily网关会将请求代理到 `api.tavily.com`，并自动插入您的API密钥。

## 身份验证

所有请求都必须在 `Authorization` 头中包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的Tavily API密钥连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=tavily&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'tavily', 'method': 'API_KEY'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

在浏览器中打开返回的 `url`，以输入您的Tavily API密钥。

### 获取连接信息

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个Tavily连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({"query": "AI news"}).encode()
req = urllib.request.Request('https://gateway.maton.ai/tavily/search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最旧的）活动连接。

## API参考

### 搜索

执行人工智能驱动的网页搜索，并可选择生成答案。

**请求参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| query | 字符串 | 是 | 搜索查询字符串 |
| max_results | 整数 | 否 | 结果数量（0-20，默认5） |
| search_depth | 字符串 | 否 | 搜索深度：`basic`、`advanced`、`fast`、`ultra-fast`（默认：basic） |
| topic | 字符串 | 否 | 搜索主题：`general` 或 `news`（默认：general） |
| include_answer | 布尔值/字符串 | 否 | 是否包含答案：`true`、`false`、`basic`、`advanced` |
| include_raw_content | 布尔值/字符串 | 否 | 是否包含原始内容：`true`、`false`、`markdown`、`text` |
| include_images | 布尔值 | 否 | 是否包含图片结果 |
| include_domains | 数组 | 否 | 仅搜索这些域名（最多300个） |
| exclude_domains | 数组 | 否 | 排除这些域名（最多150个） |
| time_range | 字符串 | 否 | 时间范围：`day`、`week`、`month`、`year` |
| start_date | 字符串 | 否 | 按日期过滤（YYYY-MM-DD） |
| end_date | 字符串 | 否 | 按日期过滤（YYYY-MM-DD） |

**响应：**

```json
{
  "query": "What is artificial intelligence?",
  "answer": "Artificial intelligence (AI) is...",
  "results": [
    {
      "title": "What is AI?",
      "url": "https://example.com/ai",
      "content": "AI is a branch of computer science...",
      "score": 0.95
    }
  ],
  "response_time": 0.55
}
```

### 提取内容

从一个或多个URL中提取内容。

**请求参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| urls | 字符串/数组 | 是 | 需要提取内容的URL |
| query | 字符串 | 否 | 用于重新排序内容的用户意图 |
| chunks_per_source | 整数 | 否 | 每个来源的最大片段数量（1-5，默认3） |
| extract_depth | 字符串 | 否 | 提取深度：`basic` 或 `advanced`（默认：basic） |
| format | 字符串 | 否 | 输出格式：`markdown` 或 `text`（默认：markdown） |
| include_images | 布尔值 | 否 | 是否包含提取的图片 |
| timeout | 浮点数 | 否 | 最大等待时间（秒）（1-60） |

**响应：**

```json
{
  "results": [
    {
      "url": "https://example.com/article",
      "raw_content": "# Article Title\n\nContent in markdown...",
      "images": [],
      "favicon": "https://example.com/favicon.ico"
    }
  ],
  "failed_results": [],
  "response_time": 0.01
}
```

### 映射网站结构

发现网站的URL，但不提取内容。

**请求参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| url | 字符串 | 是 | 开始映射的根URL |
| instructions | 字符串 | 用于指导爬虫的自然语言指令 |
| max_depth | 整数 | 否 | 探索深度（1-5，默认1） |
| max_breadth | 整数 | 每页的链接数量（1-500，默认20） |
| limit | 整数 | 需要处理的链接总数（默认50） |
| select_paths | 数组 | 否 | 包含URL的正则表达式模式 |
| exclude_paths | 数组 | 排除URL的正则表达式模式 |
| allow_external | 布尔值 | 是否包含外部链接（默认为true） |
| timeout | 浮点数 | 最大等待时间（10-150秒） |

**响应：**

```json
{
  "base_url": "https://example.com",
  "results": [
    "https://example.com/about",
    "https://example.com/products",
    "https://example.com/contact"
  ],
  "response_time": 0.1
}
```

### 爬取网站

爬取网站并从发现的页面中提取内容。

**请求参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| url | 字符串 | 是 | 开始爬取的根URL |
| instructions | 字符串 | 用于指导爬虫的自然语言指令（费用加倍） |
| chunks_per_source | 整数 | 每个来源的最大片段数量（1-5，默认3） |
| max_depth | 整数 | 探索深度（1-5，默认1） |
| max_breadth | 整数 | 每页的链接数量（1-500，默认20） |
| limit | 整数 | 需要处理的链接总数（默认50） |
| select_paths | 数组 | 包含URL的正则表达式模式 |
| exclude_paths | 数组 | 排除URL的正则表达式模式 |
| allow_external | 布尔值 | 是否包含外部链接（默认为true） |
| extract_depth | 字符串 | 提取深度：`basic` 或 `advanced`（默认：basic） |
| format | 字符串 | 输出格式：`markdown` 或 `text`（默认：markdown） |
| timeout | 浮点数 | 最大等待时间（10-150秒） |

**响应：**

```json
{
  "base_url": "https://example.com",
  "results": [
    {
      "url": "https://example.com/about",
      "raw_content": "# About Us\n\nContent...",
      "favicon": "https://example.com/favicon.ico"
    }
  ],
  "response_time": 0.09
}
```

### 研究任务

执行异步研究任务，收集数据并合成结果。

#### 创建研究任务

**请求参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| input | 字符串 | 是 | 研究任务或问题 |
| model | 字符串 | 否 | `mini`、`pro` 或 `auto`（默认：auto） |
| stream | 布尔值 | 否 | 是否通过SSE流式传输结果（默认：false） |
| output_schema | 对象 | 否 | 结构化输出的JSON模式 |
| citation_format | 字符串 | 否 | 引用格式：`numbered`、`mla`、`apa`、`chicago` |

**响应：**

```json
{
  "request_id": "582a6eec-9a10-43ba-830f-d9a1aeb19f07",
  "status": "pending",
  "input": "What are the latest developments in AI safety?",
  "model": "mini",
  "created_at": "2026-03-08T11:36:12.674507+00:00",
  "response_time": 0.05
}
```

#### 获取研究任务结果

**响应（已完成）：**

```json
{
  "request_id": "582a6eec-9a10-43ba-830f-d9a1aeb19f07",
  "status": "completed",
  "content": "## AI Safety Developments\n\nResearch findings...",
  "sources": [
    {
      "title": "Source Title",
      "url": "https://example.com/source",
      "favicon": "https://example.com/favicon.ico"
    }
  ],
  "created_at": "2026-03-08T11:36:12.674507+00:00",
  "response_time": 45
}
```

**状态值：** `pending`、`in_progress`、`completed`、`failed`

## 代码示例

### JavaScript

```javascript
// Search with answer
const response = await fetch('https://gateway.maton.ai/tavily/search', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'latest AI news',
    max_results: 5,
    include_answer: true
  })
});
const data = await response.json();
```

### Python

```python
import os
import requests

# Search with answer
response = requests.post(
    'https://gateway.maton.ai/tavily/search',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'query': 'latest AI news',
        'max_results': 5,
        'include_answer': True
    }
)
data = response.json()
```

## 注意事项

- 当启用 `include_answer` 时，搜索端点会返回人工智能生成的答案。
- `map` 功能仅返回URL；`crawl` 功能会返回包含提取内容的URL。
- 在 `crawl` 或 `map` 请求中使用 `instructions` 参数会加倍费用。
- 研究任务是异步的，需要通过GET请求来检查状态。
- 研究模型有三种类型：`mini`（快速/高效）、`pro`（全面）。
- 重要提示：当将curl输出传递给 `jq` 或其他命令时，在某些shell环境中环境变量（如 `$MATON_API_KEY`）可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到Tavily连接或请求无效 |
| 401 | Maton API密钥无效或缺失 |
| 429 | 超过请求频率限制 |
| 432 | 超过计划使用限制 |
| 433 | 超过按使用量计费的限制 |
| 4xx/5xx | 来自Tavily API的传递错误 |

## 资源

- [Tavily API文档](https://docs.tavily.com)
- [搜索API参考](https://docs.tavily.com/documentation/api-reference/endpoint/search)
- [提取API参考](https://docs.tavily.com/documentation/api-reference/endpoint/extract)
- [爬取API参考](https://docs.tavily.com/documentation/api-reference/endpoint/crawl)
- [研究API参考](https://docs.tavily.com/documentation/api-reference/endpoint/research)
- [Tavily控制面板](https://app.tavily.com)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)