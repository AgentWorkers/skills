---
name: openclaw-youtube
description: "YouTube SERP Scout（适用于代理工具）：用于搜索排名靠前的视频、频道及热门趋势，以辅助内容研究及竞争对手监控。"
homepage: https://openclaw.ai
metadata: {"openclaw":{"emoji":"📺","requires":{"bins":["curl","python3"],"env":["AISA_API_KEY"]},"primaryEnv":"AISA_API_KEY"}}
---

# OpenClaw YouTube 📺

**专为自动化代理设计的YouTube搜索分析工具，由Aisa提供支持。**

只需一个API密钥，即可实现排名发现、内容研究、竞争对手跟踪等功能。

## 🔥 功能概述：

### 内容研究
```
"Find top-ranking videos about 'AI agents tutorial' to see what's working"
```

### 竞争对手跟踪
```
"Search for videos from competitor channels about 'machine learning'"
```

### 趋势分析
```
"What are the top YouTube videos about 'GPT-5' right now?"
```

### 主题分析
```
"Find popular videos on 'autonomous driving' to understand audience interest"
```

### 频道发现
```
"Search for channels creating content about 'crypto trading'"
```

## 快速入门
```bash
export AISA_API_KEY="your-key"
```

---

## 核心功能：

### 基本YouTube搜索
```bash
# Search for videos
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI+agents+tutorial" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### 带国家过滤器的搜索
```bash
# Search in specific country (US)
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=machine+learning&gl=us" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Search in Japan
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI&gl=jp&hl=ja" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### 带语言过滤器的搜索
```bash
# Search with interface language
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=python+tutorial&hl=en" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Chinese interface
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=编程教程&hl=zh-CN&gl=cn" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### 使用过滤令牌进行分页
```bash
# Use sp parameter for pagination or advanced filters
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI&sp=<filter_token>" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

---

## Python客户端
```bash
# Basic search
python3 {baseDir}/scripts/youtube_client.py search --query "AI agents tutorial"

# Search with country
python3 {baseDir}/scripts/youtube_client.py search --query "machine learning" --country us

# Search with language
python3 {baseDir}/scripts/youtube_client.py search --query "python tutorial" --lang en

# Full options
python3 {baseDir}/scripts/youtube_client.py search --query "GPT-5 news" --country us --lang en

# Competitor research
python3 {baseDir}/scripts/youtube_client.py search --query "OpenAI tutorial"

# Trend discovery
python3 {baseDir}/scripts/youtube_client.py search --query "AI trends 2025"
```

---

## 使用场景：

### 1. 内容差距分析
通过分析排名靠前的内容，发现策略中的不足之处：
```python
# Search for top videos in your niche
results = client.search("AI automation tutorial")
# Analyze titles, views, and channels to find opportunities
```

### 2. 竞争对手监控
跟踪竞争对手发布的视频内容：
```python
# Search for competitor brand + topic
results = client.search("OpenAI GPT tutorial")
# Monitor ranking changes over time
```

### 关键词研究
发现当前热门的主题：
```python
# Search broad topics to see what's popular
results = client.search("artificial intelligence 2025")
# Extract common keywords from top-ranking titles
```

### 目标受众研究
了解目标观众喜欢观看的内容：
```python
# Search in specific regions
results = client.search("coding tutorial", country="jp", lang="ja")
# Analyze regional content preferences
```

### SEO分析
分析视频在特定关键词下的排名情况：
```python
# Track ranking positions for target keywords
keywords = ["AI tutorial", "machine learning basics", "Python AI"]
for kw in keywords:
    results = client.search(kw)
    # Record top 10 videos and their channels
```

---

## API端点参考

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/youtube/search` | GET | 在YouTube上执行搜索查询 |

## 请求参数

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| engine | string | 是 | 必须为`youtube` |
| q | string | 是 | 搜索查询 |
| gl | string | 否 | 国家代码（例如：`us`、`jp`、`uk`、`cn`） |
| hl | string | 否 | 接口语言（例如：`en`、`ja`、`zh-CN`） |
| sp | string | 否 | 用于分页/过滤的YouTube过滤令牌 |

## 响应格式
```json
{
  "search_metadata": {
    "id": "search_id",
    "status": "Success",
    "created_at": "2025-01-15T12:00:00Z",
    "request_time_taken": 1.23,
    "total_time_taken": 1.45
  },
  "search_results": [
    {
      "video_id": "abc123xyz",
      "title": "Complete AI Agents Tutorial 2025",
      "link": "https://www.youtube.com/watch?v=abc123xyz",
      "channel_name": "AI Academy",
      "channel_link": "https://www.youtube.com/@aiacademy",
      "description": "Learn how to build AI agents from scratch...",
      "views": "125K views",
      "published_date": "2 weeks ago",
      "duration": "45:30",
      "thumbnail": "https://i.ytimg.com/vi/abc123xyz/hqdefault.jpg"
    }
  ]
}
```

---

## 国家代码（gl）

| 代码 | 国家 |
|------|---------|
| us | 美国 |
| uk | 英国 |
| jp | 日本 |
| cn | 中国 |
| de | 德国 |
| fr | 法国 |
| kr | 韩国 |
| in | 印度 |
| br | 巴西 |
| au | 澳大利亚 |

## 语言代码（hl）

| 代码 | 语言 |
|------|----------|
| en | 英语 |
| ja | 日语 |
| zh-CN | 简体中文 |
| zh-TW | 繁体中文 |
| ko | 韩语 |
| de | 德语 |
| fr | 法语 |
| es | 西班牙语 |
| pt | 葡萄牙语 |
| ru | 俄语 |

---

## 价格信息

| API | 费用 |
|-----|------|
| YouTube搜索 | 约0.002美元 |

每个响应结果中都会包含`usage.cost`和`usage.credits_remaining`字段。

---

## 开始使用：

1. 在[aisa.one](https://aisa.one)注册账号。
2. 获取您的API密钥。
3. 购买API信用额度（按需付费）。
4. 设置环境变量：`export AISA_API_KEY="your-key"`。

## 完整API参考

请访问[API参考文档](https://aisa.mintlify.app/api-reference/introduction)以获取完整的端点说明。