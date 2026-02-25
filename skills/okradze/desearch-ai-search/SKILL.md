---
name: desearch-ai-search
description: 这款由人工智能驱动的搜索工具能够从多个来源（包括网页、X/Twitter、Reddit、Hacker News、YouTube、ArXiv和Wikipedia）聚合并汇总相关信息。当你需要从互联网和社交平台上获取综合性的答案或精选的链接时，可以使用它。
metadata: {"clawdbot":{"emoji":"🔎","homepage":"https://desearch.ai","requires":{"env":["DESEARCH_API_KEY"]}}}
---
# AI Search by Desearch

这是一个基于人工智能的多源搜索工具，能够从网页、Reddit、Hacker News、YouTube、ArXiv、Wikipedia和X/Twitter等平台聚合搜索结果，返回摘要形式的答案或精选的链接。

## 快速入门

1. 从 [https://console.desearch.ai](https://console.desearch.ai) 获取API密钥。
2. 设置环境变量：`export DESEARCH_API_KEY='your-key-here'`。

## 使用方法

```bash
# AI contextual search (summarized results from multiple sources)
desearch.py ai_search "What is Bittensor?" --tools web,reddit,youtube

# AI web link search (curated links from specific sources)
desearch.py ai_web "machine learning papers" --tools arxiv,web,wikipedia

# AI X/Twitter link search (curated post links)
desearch.py ai_x "crypto market trends" --count 20
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `ai_search` | 在多个来源中进行人工智能摘要搜索，返回带有上下文的聚合结果。 |
| `ai_web` | 人工智能精选链接搜索，返回来自选定来源的最相关链接。 |
| `ai_x` | 基于人工智能的X/Twitter搜索，返回与特定主题最相关的帖子链接。 |

## 选项

| 选项 | 描述 | 适用范围 |
|--------|-------------|------------|
| `--tools`, `-t` | 搜索来源：`web`, `hackernews`, `reddit`, `wikipedia`, `youtube`, `arxiv`, `twitter`（用逗号分隔） | 所有命令 |
| `--count`, `-n` | 结果数量（默认：10，最大：200） | 所有命令 |
| `--date-filter` | 时间筛选：`PAST_24_HOURS`, `PAST_2_days`, `PAST_WEEK`, `PAST_2_WEEKS`, `PAST_MONTH`, `PAST_2_MONTHS`, `PAST_YEAR`, `PAST_2_YEARS` | `ai_search` |

## 示例

### 使用AI进行主题研究并获取摘要
```bash
desearch.py ai_search "What are the latest developments in quantum computing?" --tools web,arxiv,reddit
```

### 查找学术论文
```bash
desearch.py ai_web "transformer architecture improvements 2026" --tools arxiv,web
```

### 从多个来源获取最新新闻
```bash
desearch.py ai_search "AI regulation news" --tools web,hackernews,reddit --date-filter PAST_WEEK
```

### 查找YouTube教程
```bash
desearch.py ai_web "learn rust programming" --tools youtube,web
```

### 查找与特定主题相关的X/Twitter链接
```bash
desearch.py ai_x "latest AI breakthroughs" --count 20
```

## 响应示例

### 示例（部分内容）
```json
{
  "tweets": [
    {
      "id": "2023465890369728573",
      "text": "Superposition allows qubits to encode multiple possibilities...",
      "url": "https://x.com/rukky_003/status/2023465890369728573",
      "created_at": "2026-02-16T18:33:57.000Z",
      "like_count": 5,
      "retweet_count": 0,
      "view_count": 155,
      "reply_count": 0,
      "quote_count": 2,
      "lang": "en",
      "is_retweet": false,
      "is_quote_tweet": true,
      "media": [],
      "user": {
        "id": "1316260427190472704",
        "username": "rukky_003",
        "name": "RuqoCrypto 🧠",
        "url": "https://x.com/rukky_003",
        "followers_count": 2424,
        "verified": false,
        "is_blue_verified": true
      }
    }
  ],
  "search": [
    {
      "title": "What Is Quantum Computing? | IBM",
      "link": "https://www.ibm.com/think/topics/quantum-computing",
      "snippet": "Quantum computers take advantage of quantum mechanics..."
    }
  ],
  "miner_link_scores": {
    "2023465890369728573": "HIGH",
    "https://www.ibm.com/think/topics/quantum-computing": "MEDIUM"
  },
  "completion": "Quantum computing uses qubits that leverage superposition and entanglement to compute in fundamentally different ways than classical computers..."
}
```

### 注意事项
- `miner_link_scores` 键表示Twitter结果的链接ID，网页结果的链接为完整URL。其值可以是 `"HIGH"`, `"MEDIUM"`, 或 `"LOW"`。
- `media` 总是一个数组；如果没有附带媒体内容，则为空数组 `[]`。
- `completion` 总是一个字符串；如果摘要生成失败，则为空字符串 `""`。

### 错误代码及含义

- **状态码 401**：未经授权（例如，API密钥缺失或无效）
```json
{
  "detail": "Invalid or missing API key"
}
```

- **状态码 402**：需要支付（例如，账户余额不足）
```json
{
  "detail": "Insufficient balance, please add funds to your account to continue using the service."
}
```

## 资源

- [API参考文档](https://desearch.ai/docs/api-reference/post-desearch-ai-search)
- [Desearch控制台](https://console.desearch.ai)