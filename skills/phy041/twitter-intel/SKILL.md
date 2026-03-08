---
name: twitter-intel
description: 通过 GraphQL 实现的 Twitter 关键词搜索、监控及趋势分析
metadata: {"openclaw": {"emoji": "🔍", "os": ["darwin", "linux"], "requires": {"bins": ["python3"], "env": ["TWITTER_COOKIES_PATH"]}}}
---
# Twitter Intel — 关键词搜索与趋势监控工具

通过关键词在 Twitter 上进行搜索，收集高互动量的推文，分析趋势变化，并生成结构化的报告。该工具基于 `rnet_twitter.py` 和 GraphQL 搜索技术实现（无需浏览器自动化操作）。

---

## 架构

```
Phase 1: On-demand Search (user-triggered)
  User says "search OpenAI on twitter" -> search -> filter -> report

Phase 2: Keyword Monitoring (cron-driven)
  Config defines keywords -> scheduled search -> diff with last run -> alert on new high-engagement tweets

Phase 3: Trend Analysis (on-demand or weekly)
  Aggregate saved searches -> group by week -> detect topic shifts -> generate narrative
```

---

## 先决条件

```bash
# Install rnet (Rust HTTP client with TLS fingerprint emulation)
pip install "rnet>=3.0.0rc20" --pre

# Required files:
# 1. rnet_twitter.py — lightweight async Twitter GraphQL client
#    Get it: https://github.com/PHY041/rnet-twitter-client
# 2. twitter_cookies.json — your auth cookies
#    Format: [{"name": "auth_token", "value": "..."}, {"name": "ct0", "value": "..."}]
#    Get cookies: Chrome DevTools → Application → Cookies → x.com
#    Cookies expire ~2 weeks. Refresh when you get 403 errors.
```

请将 `TWITTER_COOKIES_PATH` 环境变量设置为你的 cookies 文件路径。

---

## 第一阶段：按需搜索

当用户输入 “search [关键词] on twitter” 或 “twitter intel [主题]” 或 “find tweets about [X]” 时：

### 第一步 — 运行搜索

```python
import asyncio, os
from rnet_twitter import RnetTwitterClient

async def search(query, count=200):
    client = RnetTwitterClient()
    cookies_path = os.environ.get("TWITTER_COOKIES_PATH", "twitter_cookies.json")
    client.load_cookies(cookies_path)
    tweets = await client.search_tweets(query, count=count, product="Top")
    return tweets
```

**搜索模式：**

| 模式 | `product=` | 使用场景 |
|------|-----------|----------|
| 高互动量 | `"Top"` | 查找有影响力的推文并进行内容分析 |
| 实时 | `"Latest"` | 监控热门讨论并实时跟踪 |

**常用的 Twitter 搜索操作符：**

| 操作符 | 例子 | 功能 |
|----------|---------|--------|
| `lang:en` | `OpenAI lang:en` | 仅显示英文内容 |
| `since:` / `until:` | `since:2026-01-24 until:2026-02-24` | 时间范围 |
| `-filter:replies` | `OpenAI -filter:replies` | 仅显示原始推文 |
| `min_faves:N` | `min_faves:50` | 最小点赞数（仅适用于实时搜索模式） |
| `from:` | `from:karpathy` | 指定作者 |
| `"exact"` | `"AI agent"` | 精确匹配短语 |

### 第二步 — 筛选与优化结果

在原始搜索结果的基础上，进一步筛选高质量推文：

```python
filtered = [
    t for t in tweets
    if keyword.lower() in t["text"].lower()
    and (t["favorite_count"] >= 10 or t["retweet_count"] >= 5)
    and not t["is_reply"]
]
```

---

## 第三步 — 生成报告

输出结构化的分析报告：

```
## Twitter Intel: [keyword]
**Period:** [date range] | **Tweets found:** N | **After filter:** N

### Top Tweets (by engagement)
1. @author (X likes, Y RTs, Z views) — date
   "tweet text..."
   [link]

### Key Themes
- Theme 1: [description] (N tweets)
- Theme 2: [description] (N tweets)

### Notable Authors
| Author | Followers | Tweets in set | Total engagement |
```

---

## 第二阶段：关键词监控（定时任务）

### 配置文件

```json
{
  "monitors": [
    {
      "id": "my-product-en",
      "query": "MyProduct lang:en -filter:replies",
      "product": "Top",
      "count": 100,
      "min_likes": 10,
      "alert_threshold": 100,
      "enabled": true
    }
  ]
}
```

### 状态文件

```json
{
  "my-product-en": {
    "last_run": "2026-02-24T12:00:00Z",
    "last_tweet_ids": ["id1", "id2"],
    "total_collected": 450
  }
}
```

### 定时任务工作流程：

1. 读取配置文件，遍历所有启用的监控任务。
2. 对于每个监控任务：
   - 运行 `search_tweets(query, count, product)` 进行搜索。
   - 根据 `min_likes` 筛选结果。
   - 与上次搜索的结果进行对比，仅保留新的推文。
   - 如果有新推文的点赞数达到 `alert_threshold`，立即发送警报。
   - 将所有新推文保存到每日文件 `{monitor_id}/YYYY-MM-DD.json` 中。
   - 更新状态文件。
3. 如果有新的重要推文，发送通知。

---

## 第三阶段：趋势分析

当用户输入 “analyze twitter trend for [关键词]” 或 “twitter trend report” 时：

1. 从 `{monitor_id}/` 目录下加载所有保存的每日文件。
2. 按周对推文进行分组。
3. 分析每周的数据：
   - 总推文数量及总互动量。
   - 点赞数最高的 5 条推文。
   - 主要话题（使用大型语言模型进行分类）。
   - 新出现的作者。
   - 情感倾向的变化。
4. 生成每周的趋势分析报告。

---

## 命令列表

| 用户指令 | 功能 |
|-----------|-----------|
| `/twitter-intel [关键词]` | 搜索、筛选并生成报告（显示前 200 条推文） |
| `/twitter-intel "[短语]" --latest` | 以实时模式进行搜索 |
| `monitor "[关键词]" on twitter` | 将该关键词添加到监控列表中 |
| `twitter intel status` | 显示所有正在运行的监控任务及上次执行结果 |
| `twitter trend report [关键词]` | 分析保存的数据并生成趋势报告 |
| `refresh twitter cookies` | 帮助用户更新 Twitter 的 cookies |

---

## 技术说明：

- **搜索功能需要使用 POST 请求**（GET 请求会返回 404 错误）——由 `rnet_twitter.py` 处理。
- **GraphQL 查询 ID 会动态更新**——如果搜索失败（返回 404 错误），则从 `https://abs.twimg.com/responsive-web/client-web/main.*.js` 重新获取查询 ID。
- **请求频率限制**：每 15 分钟内最多 300 次请求。每页显示 20 条推文，因此总共需要 10 次请求。定时任务每 4 小时执行一次是安全的。
- **Cookies 的有效期**：`auth_token` 大约在 2 周后失效。请监控是否出现 403 错误。