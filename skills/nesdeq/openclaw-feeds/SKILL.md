---
name: openclaw-feeds
description: >
  RSS news aggregator. Fetches headlines from curated feeds across three categories: news, games,
  and finance. Use when the user asks about current news, headlines, what's happening, what's going
  on, or says "what's up in news", "what's up in finance", "what's up in games", or the German
  equivalents "was geht mit nachrichten", "was geht mit money", "was geht mit gaming". Also
  activates for requests like "give me a news rundown", "latest headlines", "market news",
  "gaming news", "tech news", "finance roundup", or "briefing". Returns structured JSON from
  public RSS feeds — no API keys, no web search needed.
license: MIT
compatibility: Requires Python 3, feedparser (pip install feedparser), and network access to fetch RSS feeds.
allowed-tools: Bash(python3:*)
metadata:
  author: nesdeq
  version: "3.1.1"
  tags: "rss, news, feeds, headlines, aggregator"
---

# 新闻聚合器（RSS News Aggregator）

该工具能够从三个类别的精选RSS源中获取所有最新的新闻条目：新闻（news）、游戏（games）和金融（finance）。支持并发获取数据，并以JSON格式输出结果。无需使用API密钥。

## 使用限制

在启用此功能时，严禁使用网络搜索工具（如WebFetch）、浏览器插件或其他任何URL获取工具。RSS源是唯一的数据来源。禁止通过外部搜索来补充、验证或扩展结果内容；同时也不允许获取文章的完整URL，因为输出中已经包含了文章的摘要。

## 分类规则

根据用户输入的消息来确定新闻条目的所属类别：
- "news", "headlines", "nachrichten", "tech news" → 分类为 `news`
- "finance", "markets", "money", "stocks", "economy" → 分类为 `finance`
- "games", "gaming" → 分类为 `games`

| 分类 | RSS源列表 | 来源网站 |
|----------|-------|---------|
| `news` | Ars Technica, Wired, TechCrunch, The Verge, NYT, Heise, Quanta, Aeon, Nautilus 等 |
| `games` | GameStar, GamesGlobal, PC Gamer, Polygon, Kotaku, IGN, Rock Paper Shotgun, GamesIndustry.biz |
| `finance` | Bloomberg, WSJ, FT, CNBC, MarketWatch, Seeking Alpha, The Economist, Forbes, CoinDesk, Fed, ECB |

RSS源的详细信息存储在 [scripts/lists.py](scripts/lists.py) 文件中。

## 使用方法

针对每个分类分别运行一次脚本。如果用户需要查看多个类别的内容，可以多次执行该脚本。

```bash
python3 scripts/feeds.py --category news
python3 scripts/feeds.py --category games
python3 scripts/feeds.py --category finance
```

## 输出格式

脚本会输出一个JSON数组，其中第一个元素为元数据，其余元素为具体的新闻条目：

```json
[
  {
    "title": "头条新闻",
    "url": "https://example.com/article.html",
    "source": "Ars Technica",
    "date": "2023-01-01",
    "summary": "最新的科技新闻报道..."
  },
  {
    "title": "游戏产业动态",
    "url": "https://example.com/games/article.html",
    "source": "GameStar",
    "date": "2023-01-02",
    "summary": "游戏行业的最新动态..."
  },
  // 其他新闻条目...
]
```

## 命令行参数（CLI）

可以通过以下参数来指定获取的新闻类别：
- `-c, --category`：`news`、`games` 或 `finance`（必选）

## 结果展示方式

解析输出数据后，应以结构化、简洁的方式展示结果：
1. **按主题分类**：将同类新闻归类到相应的标题下（例如：“科技与产业”、“科学”、“市场”、“加密货币”）。
2. **简洁明了**：每个条目仅显示标题、简短摘要和来源信息。
3. **提供链接**：使用Markdown格式的链接，方便用户查看原始文章。
4. **去重处理**：如果多个来源报道了同一条新闻，仅显示一次，并注明其来源。
5. **突出重要新闻**：如果某条新闻被多个来源同时报道，会特别标注出来。

**示例输出：**

```markdown
- **科技与产业**
  - 标题：人工智能的最新进展
    链接：https://example.com/tech/article.html
    来源：Ars Technica
    日期：2023-01-01
    摘要：人工智能领域的新突破...

- **游戏**
  - 标题：《游戏星》的最新评测
    链接：https://example.com/games/article.html
    来源：GameStar
    日期：2023-01-02
    摘要：《游戏星》对最新游戏的深度评测...

```

## 特殊情况处理：
- 如果某个RSS源请求失败或超时（超时时间为15秒），该源的信息将被忽略，其他来源仍会继续返回结果。
- 如果没有找到任何新闻条目，脚本会输出：`{"error": "未找到相关条目", "category": "news"}`。
- 有些新闻条目可能没有摘要，但仍然会显示标题、URL和来源信息。