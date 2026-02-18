---
name: youtube-search
description: 通过 AIsa 统一端点访问 YouTube 搜索 API。使用一个 AIsa API 密钥即可搜索 YouTube 视频、频道和播放列表，无需 Google API 密钥或 OAuth 认证。当用户需要搜索 YouTube 内容时，可以使用此功能。有关其他 AIsa 功能（如大语言模型、金融数据、Twitter、网络搜索），请参阅 aisa-core 技能文档。
compatibility: Requires network access and valid AIsa API key
metadata:
  author: aisa-one
  version: "1.0.1"
  openclaw:
    emoji: 🎬
    requires:
      env:
        - AISA_API_KEY
---
# 通过 AIsa 在 YouTube 上搜索

您可以通过 AIsa 的统一 API 在 YouTube 上搜索视频、频道和播放列表。无需使用 Google API 密钥或 OAuth 设置，只需使用您的 AIsa API 密钥即可。

## 快速入门

```bash
# Search for videos (using requests — recommended)
python <<'EOF'
import os, json, requests
results = requests.get(
    'https://api.aisa.one/apis/v1/youtube/search',
    headers={'Authorization': f'Bearer {os.environ["AISA_API_KEY"]}'},
    params={'engine': 'youtube', 'q': 'coding tutorial'}
).json()
print(json.dumps(results, indent=2))
EOF
```

## 基本 URL

```
https://api.aisa.one/apis/v1/youtube/search
```

所有 YouTube 搜索请求都通过这个单一的端点发送。AIsa 会处理与 YouTube 数据源的认证过程——您只需要提供您的 AIsa API 密钥。

## 认证

所有请求都必须在 `Authorization` 头部包含 AIsa API 密钥：

```
Authorization: Bearer $AISA_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `AISA_API_KEY`：

```bash
export AISA_API_KEY="YOUR_AISA_API_KEY"
```

### 获取您的 API 密钥

1. 在 [AIsa Marketplace](https://marketplace.aisa.one) 上登录或创建账户。
2. 进入您的仪表板。
3. 复制您的 API 密钥。

## API 参考

### YouTube 搜索

```bash
GET /apis/v1/youtube/search
```

#### 查询参数

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| `engine` | 字符串 | 是 | 必须设置为 `youtube` |
| `q` | 字符串 | 是 | 搜索查询（与 YouTube 搜索框的语法相同） |
| `sp` | 字符串 | 否 | 用于分页或高级过滤的 YouTube 过滤令牌 |
| `gl` | 字符串 | 否 | 用于获取本地化结果的国家代码（例如 `us`、`jp`、`gb`）。并非所有国家代码都受支持——请参见以下说明 |
| `hl` | 字符串 | 否 | 界面语言（例如 `en`、`zh`、`ja`） |

#### 示例：基本搜索

```bash
curl -s -X GET "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=machine+learning+tutorial" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

#### 示例：按国家和语言进行搜索

```bash
curl -s -X GET "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI+news&gl=us&hl=en" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

#### 使用 `sp` 令牌进行分页

```bash
# Use the sp token from a previous response to get the next page
curl -s -X GET "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=python+tutorial&sp=EgIQAQ%3D%3D" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

#### 响应

API 返回结构化的 YouTube 搜索结果，包括视频元数据、频道信息、缩略图和分页令牌。

**注意：** 响应结构可能因查询语言而异。英语查询通常会将结果返回在 `videos` 数组中；某些非英语查询可能会将结果返回在 `sections` 数组中。请务必检查这两种格式。

```json
{
  "search_metadata": {
    "status": "Success",
    "total_time_taken": 1.2
  },
  "search_parameters": {
    "engine": "youtube",
    "q": "machine learning tutorial"
  },
  "next_page_token": "CBQQABoCEgA%3D",
  "videos": [
    {
      "position_on_page": 1,
      "title": "Machine Learning Full Course for Beginners",
      "link": "https://www.youtube.com/watch?v=abc123xyz",
      "channel": {
        "name": "Tech Academy",
        "link": "https://www.youtube.com/channel/UCxyz123",
        "thumbnail": "https://yt3.ggpht.com/..."
      },
      "published_date": "2 months ago",
      "views": 1500000,
      "length": "3:45:20",
      "description": "Complete machine learning tutorial...",
      "thumbnail": {
        "static": "https://i.ytimg.com/vi/abc123xyz/hq720.jpg",
        "rich": "https://i.ytimg.com/an_webp/abc123xyz/mqdefault_6s.webp"
      }
    }
  ]
}
```

**替代响应格式（非英语查询）：**

某些查询会将结果返回在 `sections` 数组中，而不是扁平的 `videos` 数组中：

```json
{
  "sections": [
    {
      "title": "搜索结果",
      "videos": [
        {
          "title": "编程教程...",
          "link": "https://www.youtube.com/watch?v=...",
          ...
        }
      ]
    }
  ]
}
```

**解析两种格式：**

```python
# Handle both response structures
videos = results.get('videos', [])
if not videos and 'sections' in results:
    for section in results['sections']:
        videos.extend(section.get('videos', []))
```

### 高级搜索技巧

YouTube 的 `q` 参数支持与 YouTube 搜索框相同的搜索语法：

| 搜索语法 | 描述 | 示例 |
|---------------|-------------|---------|
| 基本关键词 | 标准搜索 | `q=python tutorial` |
| 精确短语 | 使用引号进行精确匹配 | `q="machine learning basics"` |
| 频道过滤 | 在特定频道内搜索 | `q=channel:GoogleDevelopers python` |
| 时长提示 | 与关键词结合使用 | `q=python tutorial long` |

### 使用 `sp` 过滤令牌

`sp` 参数接受 YouTube 编码的过滤令牌。常见值如下：

| 过滤条件 | `sp` 值 | 描述 |
|--------|-----------|-------------|
| 仅视频 | `EgIQAQ%3D%3D` | 仅过滤视频结果 |
| 仅频道 | `EgIQAg%3D%3D` | 仅过滤频道结果 |
| 仅播放列表 | `EgIQAw%3D%3D` | 仅过滤播放列表结果 |
| 正在直播 | `EgJAAQ%3D%3D` | 当前正在直播的内容 |
| 本周上传 | `EgIIAw%3D%3D` | 本周上传的内容 |
| 本月上传 | `EgIIBA%3D%3D` | 本月上传的内容 |
| 短视频（<4 分钟） | `EgIYAQ%3D%3D` | 时长较短的视频 |
| 长视频（>20 分钟） | `EgIYAg%3D%3D` | 时长较长的视频 |

您还可以从之前的 API 响应中的 `next_page_token` 字段获取分页所需的令牌。

#### 分页

使用响应中的 `next_page_token` 来获取下一页的结果：

```python
# First page
results = requests.get(
    'https://api.aisa.one/apis/v1/youtube/search',
    headers=headers,
    params={'engine': 'youtube', 'q': 'python tutorial'}
).json()

# Get next page token
next_token = results.get('next_page_token')
if next_token:
    page2 = requests.get(
        'https://api.aisa.one/apis/v1/youtube/search',
        headers=headers,
        params={'engine': 'youtube', 'q': 'python tutorial', 'sp': next_token}
    ).json()
```

## 代码示例

### JavaScript

```javascript
const headers = {
  'Authorization': `Bearer ${process.env.AISA_API_KEY}`
};

// Basic YouTube search
const results = await fetch(
  'https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI+agents+tutorial',
  { headers }
).then(r => r.json());

console.log(results.videos);

// Search with filters
const filtered = await fetch(
  'https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=deep+learning&gl=us&hl=en&sp=EgIQAQ%3D%3D',
  { headers }
).then(r => r.json());
```

### Python

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["AISA_API_KEY"]}'}

# Basic YouTube search
results = requests.get(
    'https://api.aisa.one/apis/v1/youtube/search',
    headers=headers,
    params={'engine': 'youtube', 'q': 'AI agents tutorial'}
).json()

for video in results.get('videos', []):
    print(f"{video['title']} - {video.get('views', 'N/A')} views")

# Search with country and language
results_jp = requests.get(
    'https://api.aisa.one/apis/v1/youtube/search',
    headers=headers,
    params={'engine': 'youtube', 'q': 'プログラミング', 'gl': 'jp', 'hl': 'ja'}
).json()
```

### Python（使用 urllib，无需额外依赖）

> **注意：** 由于 `urllib` 的默认 User-Agent，可能会遇到 403 错误。建议使用 `requests` 库。如果必须使用 `urllib`，请务必设置自定义的 User-Agent 头部。

```python
import urllib.request, urllib.parse, os, json

def youtube_search(query, gl=None, hl=None, sp=None):
    """Search YouTube via AIsa API."""
    params = {'engine': 'youtube', 'q': query}
    if gl: params['gl'] = gl
    if hl: params['hl'] = hl
    if sp: params['sp'] = sp
    
    url = f'https://api.aisa.one/apis/v1/youtube/search?{urllib.parse.urlencode(params)}'
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {os.environ["AISA_API_KEY"]}')
    req.add_header('User-Agent', 'AIsa-Skill/1.0')
    return json.load(urllib.request.urlopen(req))

# Search
results = youtube_search('OpenClaw tutorial', gl='us', hl='en')

# Handle both response formats
videos = results.get('videos', [])
if not videos and 'sections' in results:
    for section in results['sections']:
        videos.extend(section.get('videos', []))

print(json.dumps(videos[:3], indent=2))
```

## 与其他 AIsa API 结合使用

AIsa 的一个主要优势是它提供了 **统一的 API 密钥**。您可以使用相同的 `AISA_API_KEY` 将 YouTube 搜索与其他 AIsa 功能结合使用：

### YouTube 搜索 + 大语言模型（LLM）摘要

```python
import os, requests, json

headers = {'Authorization': f'Bearer {os.environ["AISA_API_KEY"]}'}

# 1. Search YouTube
yt_results = requests.get(
    'https://api.aisa.one/apis/v1/youtube/search',
    headers=headers,
    params={'engine': 'youtube', 'q': 'latest AI developments 2026'}
).json()

# 2. Summarize with LLM (same API key!)
video_titles = [v['title'] for v in yt_results.get('videos', [])[:5]]
summary = requests.post(
    'https://api.aisa.one/v1/chat/completions',
    headers={**headers, 'Content-Type': 'application/json'},
    json={
        'model': 'qwen3-flash',
        'messages': [
            {'role': 'user', 'content': f'Summarize the trending AI topics based on these YouTube videos: {json.dumps(video_titles)}'}
        ]
    }
).json()

print(summary['choices'][0]['message']['content'])
```

### YouTube 搜索 + 网页搜索

```python
# Search both YouTube and the web for comprehensive research
yt_results = requests.get(
    'https://api.aisa.one/apis/v1/youtube/search',
    headers=headers,
    params={'engine': 'youtube', 'q': 'AI agent frameworks 2026'}
).json()

web_results = requests.get(
    'https://api.aisa.one/apis/v1/search/smart',
    headers=headers,
    params={'q': 'AI agent frameworks 2026'}
).json()
```

## 注意事项

- 所有请求均按使用次数计费，费用从您的 AIsa 帐户余额中扣除——无需单独管理 YouTube API 的使用量。
- `engine` 参数必须始终设置为 `youtube`。
- 视频链接的格式为 `https://www.youtube.com/watch?v={videoId}`。
- 频道链接的格式为 `https://www.youtube.com/channel/{channelId}`。
- 使用之前响应中的 `next_page_token` 作为分页参数。
- `gl`（国家代码）参数并不支持所有的 ISO 国家代码。已知不支持的国家代码包括 `cn`（中国）。如果遇到 “Unsupported value” 错误，请尝试省略 `gl` 或使用其他国家代码。
- 非英语查询可能会将结果返回在 `sections` 数组中，而不是扁平的 `videos` 数组中——请务必处理这两种格式。
- **重要提示：** Python 的 `urllib` 可能会因为默认的 User-Agent 而返回 403 错误。建议使用 `requests` 库，或添加自定义的 `User-Agent` 头部。
- **重要提示：** 使用 curl 命令时，请确保环境变量 `$AISA_API_KEY` 被正确设置。
- **重要提示：** 当将 curl 输出传递给 `jq` 时，请使用 `-s` 标志，并确保 API 密钥已设置。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 200 | 搜索成功 |
| 400 | 请求参数无效（缺少 `engine` 或 `q`） |
| 401 | 未经授权——AIsa API 密钥无效或缺失 |
| 429 | 日志限制 |
| 500 | 服务器内部错误 |

### 故障排除：API 密钥问题

1. 确保设置了 `AISA_API_KEY` 环境变量：

```bash
echo $AISA_API_KEY
```

2. 通过简单的测试验证 API 密钥是否有效：

```bash
python <<'EOF'
import os, json, requests
try:
    result = requests.get(
        'https://api.aisa.one/apis/v1/youtube/search',
        headers={'Authorization': f'Bearer {os.environ["AISA_API_KEY"]}'},
        params={'engine': 'youtube', 'q': 'test'}
    ).json()
    videos = result.get('videos', [])
    print(f"✅ API key is valid. Results: {len(videos)} videos found")
except Exception as e:
    print(f"❌ Error: {e}")
EOF
```

### 故障排除：没有结果

1. 确保您的查询内容不为空。
2. 尝试使用更宽泛的搜索词。
3. 如果使用了 `gl`，请确认所选的国家代码是否受支持——并非所有 ISO 代码都有效（例如 `cn` 不受支持）。可以尝试省略 `gl` 来测试。
4. 确保每个请求中都包含 `engine=youtube`。
5. 检查结果是否存储在 `sections` 数组中，而不是 `videos` 数组中（非英语查询通常会出现这种情况）。

## 资源

- [AIsa API 文档](https://docs.aisa.one)
- [AIsa 仪表板 / 商店](https://marketplace.aisa.one)
- [YouTube 搜索 API 参考](https://docs.aisa.one/reference/get_youtube-search)
- [AIsa 智能搜索 API](https://docs.aisa.one/reference/get_search-smart)
- [AIsa 聊天补全 API](https://docs.aisa.one/reference/createchatcompletion)
- [OpenClaw 技能](https://clawhub.ai)