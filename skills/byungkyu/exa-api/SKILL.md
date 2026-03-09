---
name: exa
description: >
  Exa API 支持使用管理的 API 密钥进行身份验证。用户可以通过该 API 执行神经网络搜索、获取页面内容、查找相似页面、获取 AI 生成的答案以及运行异步研究任务。  
  当用户需要搜索网页、从 URL 中提取内容、查找相似网站、获取带有引用的研究结果或执行深度研究任务时，可以使用此技能。  
  对于其他第三方应用程序，请使用 `api-gateway` 技能（https://clawhub.ai/byungkyu/api-gateway）。  
  使用该技能需要网络连接以及有效的 Maton API 密钥。
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
# Exa

您可以使用管理的API密钥进行Exa API的访问。该API支持神经网络搜索、页面内容检索、相似页面查找、生成带引用的AI答案以及运行异步研究任务。

## 快速入门

```bash
# Search the web
python <<'EOF'
import urllib.request, os, json
data = json.dumps({"query": "latest AI research", "numResults": 5}).encode()
req = urllib.request.Request('https://gateway.maton.ai/exa/search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/exa/{endpoint}
```

请将 `{endpoint}` 替换为相应的Exa API端点（`search`、`contents`、`findSimilar`、`answer`、`research/v1`）。该网关会将请求代理到 `api.exa.ai` 并自动插入您的API密钥。

## 认证

所有请求都需要在 `Authorization` 头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 管理您的Exa API密钥连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=exa&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'exa', 'method': 'API_KEY'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

在浏览器中打开返回的 `url`，以输入您的Exa API密钥。

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

如果您有多个Exa连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({"query": "AI news"}).encode()
req = urllib.request.Request('https://gateway.maton.ai/exa/search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最旧的）活动连接。

## API参考

### 搜索

使用可选的内容提取功能进行神经网络搜索。

```bash
POST /exa/search
Content-Type: application/json

{
  "query": "latest AI research papers",
  "numResults": 10
}
```

**请求参数：**

| 参数 | 类型 | 是否必需 | 描述 |
|---------|-------|---------|-------------------|
| query    | string | 是     | 搜索查询字符串 |
| numResults | integer | 否      | 结果数量（最多100个，默认10个） |
| type     | string | 否      | 搜索类型：`neural`、`auto`（默认）、`keyword` |
| category | string | 否      | 过滤类别：`company`、`research paper`、`news`、`tweet`、`personal site`、`financial report`、`people` |
| includeDomains | array | 否      | 仅包含这些域名 |
| excludeDomains | array | 否      | 排除这些域名 |
| startPublishedDate | string | 否      | ISO 8601日期过滤器（之后） |
| endPublishedDate | string | 否      | ISO 8601日期过滤器（之前） |
| contents   | object | 否      | 内容提取选项（见下文） |

**内容提取选项：**

```json
{
  "contents": {
    "text": true,
    "highlights": true,
    "summary": true
  }
}
```

| 选项 | 类型 | 描述 |
|--------|-------|-------------------|
| text    | boolean/object | 提取完整页面文本 |
| highlights | boolean/object | 提取相关片段 |
| summary | boolean/object | 生成AI摘要 |

**响应：**

```json
{
  "requestId": "abc123",
  "resolvedSearchType": "neural",
  "results": [
    {
      "id": "https://example.com/article",
      "title": "Article Title",
      "url": "https://example.com/article",
      "publishedDate": "2024-01-15T00:00:00.000Z",
      "author": "Author Name",
      "text": "Full page content...",
      "highlights": ["Relevant snippet 1", "Relevant snippet 2"],
      "summary": "AI-generated summary..."
    }
  ],
  "costDollars": {
    "total": 0.005
  }
}
```

### 获取页面内容

检索特定URL的完整页面内容。

```bash
POST /exa/contents
Content-Type: application/json

{
  "ids": ["https://example.com/page1", "https://example.com/page2"],
  "text": true
}
```

**请求参数：**

| 参数 | 类型 | 是否必需 | 描述 |
|---------|-------|-------------------|
| ids     | array | 是     | 要获取内容的URL列表 |
| text    | boolean | 否      | 是否包含完整页面文本 |
| highlights | boolean/object | 是否包含相关片段 |
| summary | boolean/object | 是否生成AI摘要 |

**响应：**

```json
{
  "requestId": "abc123",
  "results": [
    {
      "id": "https://example.com/page1",
      "url": "https://example.com/page1",
      "title": "Page Title",
      "text": "Full page content..."
    }
  ]
}
```

### 查找相似页面

查找与给定URL相似的页面。

```bash
POST /exa/findSimilar
Content-Type: application/json

{
  "url": "https://example.com",
  "numResults": 10
}
```

**请求参数：**

| 参数 | 类型 | 是否必需 | 描述 |
|---------|-------|-------------------|
| url      | string | 是     | 要查找相似页面的URL |
| numResults | integer | 否      | 结果数量（最多100个，默认10个） |
| includeDomains | array | 否      | 仅包含这些域名 |
| excludeDomains | array | 否      | 排除这些域名 |
| contents   | object | 否      | 内容提取选项 |

**响应：**

```json
{
  "requestId": "abc123",
  "results": [
    {
      "id": "https://similar-site.com",
      "title": "Similar Site",
      "url": "https://similar-site.com",
      "score": 0.95
    }
  ],
  "costDollars": {
    "total": 0.005
  }
}
```

### 生成答案

生成带引用的AI答案。

```bash
POST /exa/answer
Content-Type: application/json

{
  "query": "What is machine learning?",
  "text": true
}
```

**请求参数：**

| 参数 | 类型 | 是否必需 | 描述 |
|---------|-------|-------------------|
| query    | string | 是     | 需要回答的问题 |
| text    | boolean | 否      | 是否在响应中包含源文本 |

**响应：**

```json
{
  "requestId": "abc123",
  "answer": "Machine learning is a subset of artificial intelligence...",
  "citations": [
    {
      "id": "https://example.com/ml-guide",
      "url": "https://example.com/ml-guide",
      "title": "Machine Learning Guide"
    }
  ]
}
```

### 运行研究任务

运行异步研究任务，探索网络、收集来源并生成带引用的综合结果。

#### 创建研究任务

```bash
POST /exa/research/v1
Content-Type: application/json

{
  "instructions": "What are the top AI companies and their main products?",
  "model": "exa-research"
}
```

**请求参数：**

| 参数 | 类型 | 是否必需 | 描述 |
|---------|-------|-------------------|
| instructions | string | 是     | 研究内容（最多4096个字符） |
| model    | string | 否      | 使用的模型：`exa-research-fast`、`exa-research`（默认）、`exa-research-pro` |
| outputSchema | object | 否      | 结构化输出的JSON模式 |

**响应：**

```json
{
  "researchId": "r_01abc123",
  "createdAt": 1772969504083,
  "model": "exa-research",
  "instructions": "What are the top AI companies...",
  "status": "running"
}
```

#### 获取研究任务结果

```bash
GET /exa/research/v1/{researchId}
```

**查询参数：**

| 参数 | 类型 | 描述 | -------------------|
| events    | string | 设置为 `true` 以包含事件日志 |
| stream    | string | 设置为 `true` 以进行SSE流式传输 |

**响应（已完成）：**

```json
{
  "researchId": "r_01abc123",
  "status": "completed",
  "createdAt": 1772969504083,
  "finishedAt": 1772969520000,
  "model": "exa-research",
  "instructions": "What are the top AI companies...",
  "output": {
    "content": "Based on my research, the top AI companies are..."
  },
  "costDollars": {
    "total": 0.15,
    "numSearches": 5,
    "numPages": 20,
    "reasoningTokens": 1500
  }
}
```

**状态值：** `pending`、`running`、`completed`、`canceled`、`failed`

#### 列出研究任务

```bash
GET /exa/research/v1?limit=10
```

**查询参数：**

| 参数 | 类型 | 描述 | -------------------|
| limit    | integer | 每页结果数量（1-50，默认10） |
| cursor   | string | 分页游标 |

**响应：**

```json
{
  "data": [
    {
      "researchId": "r_01abc123",
      "status": "completed",
      "model": "exa-research",
      "instructions": "What are the top AI companies..."
    }
  ],
  "hasMore": false,
  "nextCursor": null
}
```

## 代码示例

### JavaScript

```javascript
// Search with content extraction
const response = await fetch('https://gateway.maton.ai/exa/search', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'latest AI news',
    numResults: 5,
    contents: { text: true, highlights: true }
  })
});
const data = await response.json();
```

### Python

```python
import os
import requests

# Search with content extraction
response = requests.post(
    'https://gateway.maton.ai/exa/search',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'query': 'latest AI news',
        'numResults': 5,
        'contents': {'text': True, 'highlights': True}
    }
)
data = response.json()
```

## 注意事项

- 搜索类型：`neural`（语义搜索）、`auto`（混合搜索）、`keyword`（传统搜索）
- 每次搜索请求最多返回100个结果
- 内容提取（文本、高亮片段、摘要）会产生额外费用
- 如 `people` 和 `company` 等类别的过滤功能有限
- 时间戳采用ISO 8601格式
- 重要提示：在将curl输出传递给 `jq` 或其他命令时，某些shell环境中环境变量（如 `$MATON_API_KEY`）可能无法正确展开

## 错误处理

| 状态码 | 含义                         |
|--------|-----------------------------------------|
| 400     | 未找到Exa连接或请求无效                 |
| 401     | Maton API密钥无效或缺失                 |
| 429     | 请求频率限制                     |
| 4xx/5xx    | 来自Exa API的传递错误                   |

## 资源

- [Exa API文档](https://exa.ai/docs)
- [Exa API参考](https://exa.ai/docs/reference/search)
- [Exa控制面板](https://dashboard.exa.ai)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)