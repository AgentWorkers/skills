---
name: searxng
description: 使用自托管的 SearXNG 元搜索引擎在网络上进行搜索。该引擎无需 API 密钥即可聚合 Google、Brave、DuckDuckGo 等多个搜索引擎的结果。
homepage: https://docs.searxng.org
metadata: {"moltbot":{"emoji":"🔍","requires":{"bins":["python3"],"env":["SEARXNG_URL"]}}}
---

# SearXNG 网页搜索

通过您自己托管的 SearXNG 实例，提供尊重用户隐私的元搜索服务。

## 使用场景（触发语句）

当用户提出以下请求时，可以使用此功能：
- “在网页上搜索...”  
- “查找...” / “查询关于...的信息”  
- “...是什么？”（当需要获取当前信息时）  
- “进行研究...” / “搜索...”  
- “在 Google 上搜索...”（此时会重定向到尊重用户隐私的搜索平台）

## 快速入门

```bash
python3 ~/.clawdbot/skills/searxng/scripts/searxng_search.py "your query"
python3 ~/.clawdbot/skills/searxng/scripts/searxng_search.py "query" --count 10
python3 ~/.clawdbot/skills/searxng/scripts/searxng_search.py "query" --lang de
```

## 设置

设置 `SEARXNG_URL` 环境变量：
```bash
export SEARXNG_URL="http://your-searxng-host:8888"
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|---------|-------------|
| `-n`, `--count` | 5 | 返回的结果数量（1-20） |
| `-l`, `--lang` | auto | 语言代码（en, de, fr, es 等） |

## 输出结果

以 JSON 格式返回结果：
```json
{
  "query": "search terms",
  "count": 5,
  "results": [
    {"title": "...", "url": "...", "description": "...", "engines": ["google", "brave"], "score": 1.5}
  ]
}
```

## 注意事项

- 无需 API 密钥——SearXNG 会汇总来自上游搜索引擎的数据 |
- 结果中会包含来源搜索引擎的信息，以确保透明度 |
- 分数用于表示结果的相关性（分数越高，相关性越好） |
- 如需搜索新闻，可在查询中添加 “news”；或使用 `--lang` 参数获取特定地区的结果