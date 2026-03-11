---
name: serpshot
description: 使用 Serpshot 的 Google 搜索 API 进行网页搜索和图片搜索。当用户需要通过 Google 搜索信息、研究主题或获取搜索结果时，可以使用该 API。每次请求最多支持 100 个查询，支持多种地理位置和语言设置。
---
# 技能：Serpshot Google 搜索 API

使用 Serpshot API 执行 Google 搜索。

## 使用场景

- 用户请求进行搜索、查询或调研某主题
- 需要获取某个主题的网页搜索结果
- 需要获取图片搜索结果

## 工具

- `exec` - 用于运行 Python 代码以调用 Serpshot API

## 使用方法

### 基本搜索
```python
import requests
import json
import os

# Get API key - YOU MUST ASK USER FOR API KEY
api_key = os.environ.get("SERPSHOT_API_KEY", "YOUR_API_KEY")

url = "https://api.serpshot.com/api/search/google"

headers = {
    "X-API-Key": api_key,
    "Content-Type": "application/json"
}

payload = {
    "queries": ["your search query here"],
    "type": "search",  # or "image"
    "num": 10,  # results per page (1-100)
    "page": 1,
    "location": "US",  # US, CN, JP, GB, DE, etc.
    "lr": "en",  # language restriction
    "gl": "us"  # geolocation
}

response = requests.post(url, headers=headers, json=payload)
data = response.json()

# Parse results
for result in data.get("data", {}).get("results", []):
    print(f"{result['position']}. {result['title']}")
    print(f"   {result['link']}")
    print(f"   {result['snippet']}")
    print()
```

### 参数

| 参数 | 类型 | 是否必填 | 描述 |
|---------|--------|---------|-------------------|
| queries | 数组（字符串） | 是 | 搜索查询（最多 100 个） |
| type | 字符串 | 否 | 搜索类型（"search" 或 "image"，默认为 "search"） |
| num | 整数 | 否 | 每页显示的结果数量（1-100），默认为 10 |
| page | 整数 | 否 | 页码，默认为 1 |
| location | 字符串 | 否 | 国家代码（US、CN、JP、GB、DE 等），默认为 US |
| lr | 字符串 | 否 | 语言限制（en、zh-Hans 等），默认为 en |
| gl | 字符串 | 否 | 地理位置（us、cn 等），默认为 us |

### 响应格式
```json
{
  "code": 200,
  "msg": "Success",
  "data": {
    "results": [
      {
        "title": "Result Title",
        "link": "https://example.com",
        "snippet": "Result description...",
        "position": 1
      }
    ],
    "total_results": "About 12,300,000 results",
    "search_time": 0.45,
    "credits_used": 1
  }
}
```

## 示例任务

### 任务 1：搜索 AI 相关新闻
```
queries: ["AI news 2026"]
location: "US"
num: 5
```

### 任务 2：搜索中文结果
```
queries: ["人工智能 最新消息"]
location: "CN"
lr: "zh-Hans"
gl: "cn"
num: 10
```

### 任务 3：图片搜索
```
queries: ["cute cats"]
type: "image"
num: 10
```

## 重要说明

1. **需要 API 密钥**：在使用此功能之前，必须获取用户的 Serpshot API 密钥。
2. **费用**：每次搜索都会消耗信用点数（请查看 /api/credit/available-credits）。
3. **速率限制**：请联系 Serpshot 了解具体的速率限制规则。
4. **支持的位置**：包括 US、CN、JP、GB、DE、CA、FR、ID、MX、SG 等地区。

## 错误处理

常见的错误代码：
- 400：请求错误（参数无效）
- 401：API 密钥无效
- 402：信用点数不足
- 429：超出速率限制

请查看响应中的 `data["code"]` 和 `data["msg"]` 以获取详细信息。