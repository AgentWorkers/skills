---
name: brave-search
description: >
  Brave Search API集成支持管理式身份验证功能，允许用户通过Brave Search进行网页搜索、图片搜索、新闻搜索和视频搜索，同时注重保护用户隐私。  
  当用户需要使用Brave Search进行网页搜索、查找图片、获取新闻或搜索视频时，可利用此功能。  
  对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
compatibility: Requires network access and valid Maton API key
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
# Brave Search

您可以使用受管理的身份验证方式访问Brave Search API。该搜索引擎专注于保护用户隐私，支持网页搜索、图片搜索、新闻搜索和视频搜索。

## 快速入门

```bash
# Web search
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/brave-search/res/v1/web/search?q=python+programming&count=5')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/brave-search/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的Brave Search API端点路径。该网关会将请求代理到 `api.search.brave.com`，并自动插入您的API密钥。

## 身份验证

所有请求都必须在 `Authorization` 头部包含Maton API密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的Brave Search连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=brave-search&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'brave-search'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "1472d925-86d6-4cbb-8f2f-17e18f6bc0c7",
    "status": "ACTIVE",
    "creation_time": "2026-03-10T11:12:30.963141Z",
    "last_updated_time": "2026-03-10T11:13:55.282885Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "brave-search",
    "metadata": {},
    "method": "API_KEY"
  }
}
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

如果您有多个Brave Search连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/brave-search/res/v1/web/search?q=test')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '1472d925-86d6-4cbb-8f2f-17e18f6bc0c7')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API参考

### 网页搜索

```bash
GET /brave-search/res/v1/web/search?q={query}
```

**必填参数：**
- `q`（字符串）：搜索查询（1-400个字符，最多50个单词）

**可选参数：**
- `country`（字符串）：2位字母的国家代码（默认："US"）
- `search_lang`（字符串）：搜索语言代码（默认："en"）
- `ui_lang`（字符串）：符合RFC 9110标准的用户界面语言（默认："en-US"）
- `count`（整数）：每页显示的结果数量（1-20，默认：20）
- `offset`（整数）：页面偏移量（0-9，默认：0）
- `safesearch`（字符串）：过滤级别 - "off", "moderate", "strict"（默认："moderate"）
- `freshness`（字符串）：时间过滤条件 - "pd"（过去一天）、"pw"（过去一周）、"pm"（过去一个月）、"py"（过去一年）或日期范围
- `text_decorations`（布尔值）：是否包含高亮标记（默认：true）
- `result_filter`（字符串）：以逗号分隔的结果类型（讨论、常见问题解答、信息框、新闻、视频、网页）
- `extra_snippets`（布尔值）：是否获取最多5个替代摘录
- `summary`（布尔值）：是否启用摘要功能

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/brave-search/res/v1/web/search?q=machine+learning&count=10&freshness=pw')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "type": "search",
  "query": {
    "original": "machine learning",
    "show_strict_warning": false,
    "is_navigational": false,
    "country": "us",
    "more_results_available": true
  },
  "web": {
    "type": "search",
    "results": [
      {
        "title": "Machine Learning - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Machine_learning",
        "description": "Machine learning is a subset of artificial intelligence...",
        "language": "en",
        "family_friendly": true
      }
    ]
  },
  "discussions": {...},
  "faq": {...},
  "videos": {...}
}
```

### 图片搜索

```bash
GET /brave-search/res/v1/images/search?q={query}
```

**必填参数：**
- `q`（字符串）：搜索查询

**可选参数：**
- `country`（字符串）：2位字母的国家代码
- `search_lang`（字符串）：搜索语言代码
- `count`（整数）：每页显示的结果数量（1-20）
- `safesearch`（字符串）：过滤级别 - "off", "moderate", "strict"

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/brave-search/res/v1/images/search?q=sunset&count=5')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "type": "images",
  "results": [
    {
      "title": "Beautiful Sunset",
      "url": "https://example.com/sunset.jpg",
      "source": "https://example.com/gallery",
      "thumbnail": {
        "src": "https://imgs.search.brave.com/..."
      },
      "properties": {
        "width": 1920,
        "height": 1080,
        "format": "jpeg"
      }
    }
  ]
}
```

### 新闻搜索

```bash
GET /brave-search/res/v1/news/search?q={query}
```

**必填参数：**
- `q`（字符串）：搜索查询

**可选参数：**
- `country`（字符串）：2位字母的国家代码
- `search_lang`（字符串）：搜索语言代码
- `count`（整数）：每页显示的结果数量（1-20）
- `freshness`（字符串）：时间过滤条件 - "pd", "pw", "pm", "py"
- `safesearch`（字符串）：过滤级别

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/brave-search/res/v1/news/search?q=technology&count=5&freshness=pd')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "type": "news",
  "results": [
    {
      "title": "Latest Tech News",
      "url": "https://example.com/news/tech",
      "description": "Breaking technology news...",
      "age": "2 hours ago",
      "source": {
        "name": "Tech News",
        "url": "https://technews.com"
      },
      "thumbnail": {
        "src": "https://imgs.search.brave.com/..."
      }
    }
  ]
}
```

### 视频搜索

```bash
GET /brave-search/res/v1/videos/search?q={query}
```

**必填参数：**
- `q`（字符串）：搜索查询

**可选参数：**
- `country`（字符串）：2位字母的国家代码
- `search_lang`（字符串）：搜索语言代码
- `count`（整数）：每页显示的结果数量（1-20）
- `safesearch`（字符串）：过滤级别

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/brave-search/res/v1/videos/search?q=tutorial&count=5')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "type": "videos",
  "results": [
    {
      "title": "Python Tutorial for Beginners",
      "url": "https://www.youtube.com/watch?v=...",
      "description": "Learn Python programming...",
      "age": "1 year ago",
      "duration": "3:45:00",
      "thumbnail": {
        "src": "https://imgs.search.brave.com/..."
      },
      "meta_url": {
        "hostname": "www.youtube.com"
      }
    }
  ]
}
```

### 本地兴趣点

```bash
GET /brave-search/res/v1/local/pois?ids={poi_ids}
```

通过ID（从网页搜索结果中获取）获取本地兴趣点的详细信息。

**必填参数：**
- `ids`（字符串）：以逗号分隔的兴趣点ID

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/brave-search/res/v1/local/pois?ids=poi_123,poi_456')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "type": "local_pois",
  "results": [
    {
      "id": "poi_123",
      "name": "Coffee Shop",
      "address": "123 Main St",
      "phone": "+1-555-1234",
      "rating": 4.5,
      "reviews": 128
    }
  ]
}
```

### 兴趣点描述

```bash
GET /brave-search/res/v1/local/descriptions?ids={poi_ids}
```

获取本地兴趣点的详细描述。

**必填参数：**
- `ids`（字符串）：以逗号分隔的兴趣点ID

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/brave-search/res/v1/local/descriptions?ids=poi_123')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "type": "local_descriptions",
  "results": [
    {
      "id": "poi_123",
      "description": "A cozy coffee shop known for artisanal brews..."
    }
  ]
}
```

### 自动建议

> **注意：** 需要订阅自动建议服务。

```bash
GET /brave-search/res/v1/suggest/search?q={query}
```

在用户输入查询时获取搜索建议。

**必填参数：**
- `q`（字符串）：部分搜索查询

**可选参数：**
- `country`（字符串）：2位字母的国家代码
- `count`（整数）：返回的建议数量
- `rich`（布尔值）：是否启用增强元数据

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/brave-search/res/v1/suggest/search?q=how+to&count=5&rich=true')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "type": "suggest",
  "query": {
    "original": "how to"
  },
  "results": [
    {
      "query": "how to learn python",
      "is_entity": false
    },
    {
      "query": "how to code",
      "is_entity": false
    }
  ]
}
```

### 拼写检查

> **注意：** 需要订阅拼写检查服务。

```bash
GET /brave-search/res/v1/spellcheck/search?q={query}
```

检查拼写错误并获取修正建议。

**必填参数：**
- `q`（字符串）：需要检查拼写的文本
- `country`（字符串）：用于本地化修正的国家代码

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/brave-search/res/v1/spellcheck/search?q=helo+wrold&country=US')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "type": "spellcheck",
  "query": {
    "original": "helo wrold"
  },
  "results": [
    {
      "query": "hello world"
    }
  ]
}
```

### 摘要功能

> **注意：** 需要订阅摘要功能。

首先使用 `summary=1` 进行网页搜索以获取摘要密钥，然后使用该密钥获取摘要内容。

#### 获取摘要密钥

```bash
GET /brave-search/res/v1/web/search?q={query}&summary=1
```

#### 获取摘要内容

```bash
GET /brave-search/res/v1/summarizer/search?key={summarizer_key}
```

**可选参数：**
- `entity_info`（布尔值）：是否包含实体详情
- `inline_references`（布尔值）：是否包含引用标记

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json

# Step 1: Get summarizer key from web search
req = urllib.request.Request('https://gateway.maton.ai/brave-search/res/v1/web/search?q=what+is+python&summary=1')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
data = json.load(urllib.request.urlopen(req))
summarizer_key = data.get('summarizer', {}).get('key')

# Step 2: Fetch summary using the key
if summarizer_key:
    req = urllib.request.Request(f'https://gateway.maton.ai/brave-search/res/v1/summarizer/search?key={summarizer_key}')
    req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
    print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 其他摘要相关端点

```bash
GET /brave-search/res/v1/summarizer/summary?key={key}           # Summary only
GET /brave-search/res/v1/summarizer/title?key={key}             # Title only
GET /brave-search/res/v1/summarizer/enrichments?key={key}       # Enrichment data
GET /brave-search/res/v1/summarizer/followups?key={key}         # Follow-up suggestions
GET /brave-search/res/v1/summarizer/entity_info?key={key}       # Entity information
```

## 分页

使用 `count` 和 `offset` 进行分页：

```bash
# First page (results 1-10)
GET /brave-search/res/v1/web/search?q=test&count=10&offset=0

# Second page (results 11-20)
GET /brave-search/res/v1/web/search?q=test&count=10&offset=1
```

**注意：** `offset` 的范围是0-9，最多可获取200个结果（20个结果 × 10页）。

请检查响应中的 `query.more_results_available` 以确定是否还有更多结果。

## 位置相关头部信息

对于包含位置信息的搜索结果，需要包含以下位置头部信息：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/brave-search/res/v1/web/search?q=restaurants+near+me&count=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('x-loc-lat', '37.7749')
req.add_header('x-loc-long', '-122.4194')
req.add_header('x-loc-city', 'San Francisco')
req.add_header('x-loc-state', 'CA')
req.add_header('x-loc-country', 'US')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**可用的位置头部信息：**
- `x-loc-lat`：纬度（-90到90）
- `x-loc-long`：经度（-180到180）
- `x-loc-timezone`：IANA时区标识符
- `x-loc-city`：城市名称
- `x-loc-state`：州/省
- `x-loc-country`：2位字母的国家代码
- `x-loc-postal-code`：邮政编码

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/brave-search/res/v1/web/search?q=javascript&count=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.web.results);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/brave-search/res/v1/web/search',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'q': 'python programming', 'count': 10}
)
data = response.json()
for result in data.get('web', {}).get('results', []):
    print(f"{result['title']}: {result['url']}")
```

## 注意事项

- 每次请求最多返回20个结果。
- 最多10页结果（偏移量0-9）。
- 查询长度：1-400个字符，最多50个单词。
- Brave Search注重保护用户隐私，不会跟踪用户行为。
- 结果类型包括：网页、新闻、视频、讨论、常见问题解答、信息框。
- **重要提示：** 当将curl输出传递给 `jq` 或其他命令时，在某些shell环境中，环境变量 `$MATON_API_KEY` 可能无法正确显示。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到Brave Search连接 |
| 401 | Maton API密钥无效或缺失 |
| 404 | 未找到相应的订阅服务 |
| 422 | 订阅令牌无效 |
| 429 | 超过使用频率限制或配额 |
| 4xx/5xx | 来自Brave Search API的传递错误 |

### 故障排除：API密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证API密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称错误

1. 确保您的URL路径以 `brave-search` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/brave-search/res/v1/web/search?q=test`
- 错误的路径：`https://gateway.maton.ai/res/v1/web/search?q=test`

## 资源

- [Brave Search API文档](https://api-dashboard.search.brave.com/documentation)
- [Brave Search API控制台](https://api-dashboard.search.brave.com/)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)