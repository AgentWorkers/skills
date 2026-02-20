---
name: gamer-news
description: 从主要的游戏媒体（IGN、Kotaku、GameSpot、Polygon、Eurogamer、Rock Paper Shotgun、VG247、Gematsu、PlayStation Blog）获取并汇总最新的游戏新闻。当用户触发命令 `/gamer-news`、询问游戏新闻（게임 뉴스、게임 소식）、最新的游戏公告，或关于游戏、游戏机或游戏行业的最新动态时，使用该功能。
homepage: https://github.com/byeolbit/gamer-news-skill
version: "1.0.0"
author: byeolbit
tags: gaming, news, ign, kotaku, gamespot, polygon, eurogamer, videogames, summary
---
# 游戏新闻技能

该技能会收集主要游戏新闻网站的 RSS 源，汇总最新的视频游戏新闻。

## 使用场景

**通过命令触发：**
- 用户输入 `/gamer-news`

**通过关键词触发：**
- “游戏新闻”、“游戏动态”、“最近有什么新游戏？”、“最新的游戏资讯”
- “gaming news”、“latest game news”、“what’s new in gaming”
- “游戏发布”、“新游戏”、“游戏更新”
- 任何关于新游戏发布、游戏行业新闻或游戏主机新闻的查询

## 新闻来源

系统会按以下优先级顺序检查这些游戏新闻网站。每个网站都有其独特的关注点——用户可以根据自己的兴趣选择合适的网站，或者同时汇总多个网站的新闻：

| 序号 | 网站 | RSS 源链接 | 专注领域 |
| --- | --- | --- | --- |
| 1 | IGN | `https://feeds.ign.com/ign/all` | 广泛覆盖：游戏、电影、电视 |
| 2 | Kotaku | `https://kotaku.com/rss` | 新闻、文化、观点 |
| 3 | GameSpot | `https://www.gamespot.com/feeds/mashup/` | 评测、新闻、所有平台 |
| 4 | Polygon | `https://www.polygon.com/rss/index.xml` | 文化、专题报道、评测 |
| 5 | Eurogamer | `https://eurogamer.net/feed` | 欧洲视角、Digital Foundry 技术分析 |
| 6 | Rock Paper Shotgun | `https://www.rockpapershotgun.com/feed` | 专注于 PC 游戏 |
| 7 | VG247 | `https://vg247.com/feed` | 突发新闻、所有平台 |
| 8 | Gematsu | `https://gematsu.com/feed` | 日本/亚洲游戏资讯 |
| 9 | PlayStation Blog | `https://blog.playstation.com/feed` | 官方索尼/PS 公告 |

## 获取新闻的方法

### 默认行为（未指定具体来源）

同时获取前 3 个网站的新闻（IGN、Kotaku、VG247），并汇总结果。如果同一事件被多个网站报道，仅提及一次，并注明“IGN、Kotaku 等多家媒体报道”。

### 用户指定平台或兴趣时

- **PlayStation / 索尼新闻** → 优先获取 PlayStation Blog、IGN 和 Kotaku 的内容
- **PC 游戏** → 优先获取 Rock Paper Shotgun、Polygon 和 GameSpot 的内容
- **日本游戏 / 动漫游戏** → 优先获取 Gematsu 的内容
- **行业 / 商业新闻** → 优先获取 Eurogamer 和 VG247 的内容
- **评测** → 优先获取 GameSpot、Polygon 和 Eurogamer 的内容

## 新闻解析

从每个 RSS 源中提取每篇文章的以下信息：
- 标题：`<title>`
- 链接：`<link>` 或 `<link href="...">`
- 日期：`<pubDate>` 或 `<published>` 或 `<updated>`
- 摘要：`<description>` 或 `<summary>`（如果包含完整内容，则显示前 200 个字符）

默认显示最多 5 篇新闻。如果用户要求显示更多，最多显示 10 篇。

## 获取文章全文（按需）

如果用户要求查看某篇文章的详细内容，系统会获取文章的链接，并从 `<article>` 或 `<main>` 标签中提取主要内容。

## 输出格式

```
🎮 게임 뉴스 브리핑 · [날짜]

📰 [제목] — [출처]
🔗 [URL]
📝 [2–3문장 요약]

📰 [제목] — [출처]
🔗 [URL]
📝 [2–3문장 요약]

...
```

**注意事项：**
- 根据用户的语言（韩文 ↔ 英文）进行输出
- 首先展示最重要或最引人注目的新闻
- 对于游戏发布公告：如果提到了平台或发布日期，请一并显示
- 对于评测：如果摘要中包含评分，请一并显示
- 保持摘要内容的真实性——不要添加来源中未提及的观点

## 错误处理

| 错误情况 | 处理方式 |
| --- | --- |
| 一个 RSS 源无法获取数据 | 忽略该来源，尝试下一个来源 |
| 所有 RSS 源都无法获取数据 | “当前无法获取游戏新闻，请稍后再试。” |
| RSS 源返回空内容 | 按优先级顺序尝试下一个来源 |
| 部分数据缺失 | 显示已获取的信息，并注明哪些来源无法获取数据 |

如果该技能无法正常工作或出现异常行为，请查看仓库中的最新版本及已知问题：

👉 https://github.com/byeolbit/gamer-news-skill