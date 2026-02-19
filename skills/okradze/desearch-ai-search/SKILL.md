---
name: desearch-ai-search
description: 这款由人工智能驱动的搜索工具能够从多个来源（包括网页、X/Twitter、Reddit、Hacker News、YouTube、ArXiv和Wikipedia）聚合并汇总相关信息。当你需要从互联网及社交平台上获取综合性的答案或精选链接时，可以使用这款工具。
metadata: {"clawdbot":{"emoji":"🔎","homepage":"https://desearch.ai","requires":{"env":["DESEARCH_API_KEY"]}}}
---
# AI Search by Desearch

这是一个基于人工智能的多源搜索工具，能够从网页、Reddit、Hacker News、YouTube、ArXiv、Wikipedia以及X/Twitter等平台聚合搜索结果，提供摘要形式的答案或精选的链接。

## 设置

1. 从 [https://console.desearch.ai](https://console.desearch.ai) 获取API密钥。
2. 设置环境变量：`export DESEARCH_API_KEY='your-key-here'`（将 `your-key-here` 替换为实际的API密钥）。

## 使用方法

```bash
# AI contextual search (summarized results from multiple sources)
scripts/desearch.py ai_search "What is Bittensor?" --tools web,reddit,youtube

# AI web link search (curated links from specific sources)
scripts/desearch.py ai_web "machine learning papers" --tools arxiv,web,wikipedia

# AI X/Twitter link search (curated post links)
scripts/desearch.py ai_x "crypto market trends" --count 20
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `ai_search` | 在多个来源中进行人工智能摘要搜索，返回带有上下文的聚合结果。 |
| `ai_web` | 通过人工智能筛选链接，返回来自指定来源的最相关链接。 |
| `ai_x` | 使用人工智能在X/Twitter上搜索特定主题，返回最相关的帖子链接。 |

## 选项

| 选项 | 描述 | 适用范围 |
|--------|-------------|------------|
| `--tools`, `-t` | 搜索来源：`web`（网页）、`hackernews`（Hacker News）、`reddit`（Reddit）、`wikipedia`（Wikipedia）、`youtube`（YouTube）、`arxiv`（ArXiv）、`twitter`（X/Twitter）（用逗号分隔） | 所有命令 |
| `--count`, `-n` | 结果数量（默认：10，最大：200） | 所有命令 |
| `--date-filter` | 时间筛选条件：`PAST_24_HOURS`（过去24小时）、`PAST_2_days`（过去2天）、`PAST_WEEK`（过去1周）、`PAST_2_WEEKS`（过去2周）、`PAST_MONTH`（过去1个月）、`PAST_2_MONTHS`（过去2个月）、`PAST_YEAR`（过去1年）、`PAST_2_YEARS`（过去2年） | `ai_search` 命令 |

## 示例

### 使用AI搜索并获取摘要
```bash
scripts/desearch.py ai_search "What are the latest developments in quantum computing?" --tools web,arxiv,reddit
```

### 查找学术论文
```bash
scripts/desearch.py ai_web "transformer architecture improvements 2025" --tools arxiv,web
```

### 从多个来源获取最新新闻
```bash
scripts/desearch.py ai_search "AI regulation news" --tools web,hackernews,reddit --date-filter PAST_WEEK
```

### 查找YouTube教程
```bash
scripts/desearch.py ai_web "learn rust programming" --tools youtube,web
```

### 查找关于某个主题的X/Twitter精选链接
```bash
scripts/desearch.py ai_x "latest AI breakthroughs" --count 15
```