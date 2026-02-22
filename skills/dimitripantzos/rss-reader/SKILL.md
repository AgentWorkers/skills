---
name: rss-reader
description: 监控 RSS 和 Atom 源以进行内容研究。可以跟踪博客、新闻网站、时事通讯以及任何类型的 Feed 源。适用于监控竞争对手、追踪行业动态、寻找内容灵感或构建个人新闻聚合器。支持多个 Feed 源，并提供分类、过滤和摘要功能。
---
# RSS 阅读器

用于监控 RSS/Atom 源站，以获取内容灵感、跟踪竞争对手动态以及获取行业新闻。

## 快速入门

```bash
# Add a feed
node scripts/rss.js add "https://example.com/feed.xml" --category tech

# Check all feeds
node scripts/rss.js check

# Check specific category
node scripts/rss.js check --category tech

# List feeds
node scripts/rss.js list

# Remove a feed
node scripts/rss.js remove "https://example.com/feed.xml"
```

## 配置

源数据存储在 `rss-reader/feeds.json` 文件中：

```json
{
  "feeds": [
    {
      "url": "https://example.com/feed.xml",
      "name": "Example Blog",
      "category": "tech",
      "enabled": true,
      "lastChecked": "2026-02-22T00:00:00Z",
      "lastItemDate": "2026-02-21T12:00:00Z"
    }
  ],
  "settings": {
    "maxItemsPerFeed": 10,
    "maxAgeDays": 7,
    "summaryEnabled": true
  }
}
```

## 使用场景

### 内容研究
监控竞争对手的博客、行业出版物以及行业领军人物的内容：
```bash
# Add multiple feeds
node scripts/rss.js add "https://competitor.com/blog/feed" --category competitors
node scripts/rss.js add "https://techcrunch.com/feed" --category news
node scripts/rss.js add "https://news.ycombinator.com/rss" --category tech

# Get recent items as content ideas
node scripts/rss.js check --since 24h --format ideas
```

### 新闻通讯聚合
跟踪并整理各类新闻通讯：
```bash
node scripts/rss.js add "https://newsletter.com/feed" --category newsletters
```

### 关键词监控
根据关键词筛选信息：
```bash
node scripts/rss.js check --keywords "AI,agents,automation"
```

## 输出格式

### 默认格式（列表形式）
```
[tech] Example Blog - "New Post Title" (2h ago)
  https://example.com/post-1
[news] TechCrunch - "Breaking News" (4h ago)
  https://techcrunch.com/article-1
```

### 内容研究模式（仅显示相关内容）
```
## Content Ideas from RSS (Last 24h)

### Tech
- **"New Post Title"** - [Example Blog]
  Key points: Point 1, Point 2, Point 3
  Angle: How this relates to your niche

### News  
- **"Breaking News"** - [TechCrunch]
  Key points: Summary of the article
  Angle: Your take or response
```

### JSON 格式（适用于自动化）
```bash
node scripts/rss.js check --format json
```

## 按类别划分的热门源站

### 科技/人工智能
- `https://news.ycombinator.com/rss` - Hacker News
- `https://www.reddit.com/r/artificial/.rss` - r/artificial
- `https://www.reddit.com/r/LocalLLaMA/.rss` - r/LocalLLaMA
- `https://openai.com/blog/rss.xml` - OpenAI 博客

### 营销领域
- `https://www.reddit.com/r/Entrepreneur/.rss` - r/Entrepreneur
- `https://www.reddit.com/r/SaaS/.rss` - r/SaaS

### 新闻领域
- `https://techcrunch.com/feed/` - TechCrunch
- `https://www.theverge.com/rss/index.xml` - The Verge

## 定时任务集成

可以通过心跳信号（heartbeat）或 cron 作业来设置每日自动检查源站内容：

```
// In HEARTBEAT.md
- Check RSS feeds once daily, summarize new items worth reading
```

或者通过 cron 作业实现自动化检查：
```bash
clawdbot cron add --schedule "0 8 * * *" --task "Check RSS feeds and summarize: node /root/clawd/skills/rss-reader/scripts/rss.js check --since 24h --format ideas"
```

## 脚本

- `scripts/rss.js`：用于管理 RSS 源站的主要命令行工具
- `scripts/parse-feed.js`：用于解析 RSS 数据的脚本（使用 xml2js 库）

## 依赖库

```bash
npm install xml2js node-fetch
```

如果系统中缺少某些依赖库，脚本会提示用户进行安装。