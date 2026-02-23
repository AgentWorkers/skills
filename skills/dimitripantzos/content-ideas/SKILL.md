---
name: content-ideas
description: 从多个来源生成内容创意。汇总来自 RSS 源、Reddit、Hacker News、X/Twitter 以及网络搜索的趋势信息。生成具有可操作性的内容创意，包括具体的切入点、写作角度和呈现格式。适用于需要内容灵感、趋势监测或制定内容计划时使用。
---
# 内容创意生成器

将趋势转化为可用的内容，从多个来源收集信息，按特定领域进行筛选，最终输出具有实际操作价值的创意。

## 工作原理

1. **收集数据**：从 RSS、Reddit、Hacker News、X（Twitter 的前身）以及网络搜索中获取信息。
2. **筛选内容**：确保内容符合你的领域和目标受众的需求。
3. **分析趋势**：当前哪些话题最热门？哪些角度尚未被关注？
4. **生成创意**：为每个创意提供具体的切入点和呈现格式。

## 快速入门

向你的智能助手请求：

> “生成本周的10个内容创意。我的领域是针对小型企业的AI自动化。”

智能助手应执行以下操作：
1. 检查已配置的数据来源（RSS订阅源、相关子版块等）。
2. 在你的领域内搜索热门话题。
3. 分析哪些内容获得了较高的互动量。
4. 生成包含具体切入点和呈现形式的创意。

## 配置信息

配置信息存储在 `content-ideas/config.json` 文件中：

```json
{
  "niche": "AI automation for small businesses",
  "audience": "non-technical founders, solopreneurs",
  "platforms": ["twitter", "linkedin", "blog"],
  
  "sources": {
    "rss": [
      "https://news.ycombinator.com/rss",
      "https://www.reddit.com/r/smallbusiness/.rss",
      "https://www.reddit.com/r/Entrepreneur/.rss"
    ],
    "subreddits": ["smallbusiness", "Entrepreneur", "SaaS", "artificial"],
    "twitter": {
      "accounts": ["@levelsio", "@marckohlbrugge", "@andrewchen"],
      "keywords": ["AI automation", "no-code", "solopreneur"]
    },
    "keywords": ["AI", "automation", "productivity", "small business", "startup"]
  },
  
  "filters": {
    "minEngagement": 100,
    "maxAgeDays": 7,
    "excludeKeywords": ["crypto", "NFT", "web3"]
  },
  
  "output": {
    "ideasPerRun": 10,
    "includeHooks": true,
    "includeFormats": true,
    "includeAngles": true
  }
}
```

## 输出格式

创意的输出格式如下（具体格式可根据实际需求调整）：

```markdown
## Content Ideas - 2026-02-22

### Idea 1: [Title]
**Source:** r/smallbusiness trending post
**Why it's hot:** 500+ upvotes, addresses common pain point
**Your angle:** [How to spin for your audience]
**Hook options:**
- "Most small business owners waste 10 hours/week on this..."
- "I automated X and saved $2000/month. Here's how."
- "Stop doing [thing] manually. This is 2026."
**Formats:** Twitter thread, LinkedIn post, blog tutorial
**Engagement prediction:** High (solves clear pain point)

### Idea 2: [Title]
...
```

## 数据源集成

### RSS订阅源（通过 `rss-reader` 技能）

- 任何子版块的 RSS 链接：
  - 新帖子：`https://www.reddit.com/r/{subreddit}/.rss`
  - 本周热门帖子：`https://www.reddit.com/r/{subreddit}/top/.rss?t=week`

### Hacker News
- 首页：`https://news.ycombinator.com/rss`
- 查看所有内容：`https://hnrss.org/show`
- 提问：`https://hnrss.org/ask`
- 按关键词搜索：`https://hnrss.org/newest?q=AI+automation`

### X/Twitter（通过 `bird` 或 `x-twitter` 技能）

- 搜索你所在领域的热门话题和高互动量的帖子。

### 网络搜索（通过 `web_search` 工具）

- 搜索相关领域的热门文章、新闻和讨论。

## 工作流程

### 每日创意生成（使用 Cron 任务）

设置每日定时任务来生成创意：

```
Schedule: 07:00 daily
Task: Generate 5 content ideas based on overnight trends. Save to content-ideas/daily/YYYY-MM-DD.md
```

### 每周内容计划

```
Schedule: Sunday 20:00
Task: Generate 15-20 content ideas for the week. Organize by platform and day. Save to content-ideas/weekly/YYYY-WW.md
```

### 按需研究

> “[领域] 目前有哪些热门话题？给我5个今天可以发布的创意。”

## 创意分类

### 应时性创意（当前热门话题）
- 突发新闻的应对策略
- 对热门帖子的独到见解
- “关于 X，大家可能忽略的要点”

### 持久性创意（始终适用）
- 教程
- 工具对比
- 入门指南
- 常见错误

### 个人分享（基于个人经验）
- 幕后故事
- 经验教训
- 案例研究
- 失败与成功案例

### 反传统观点（与众不同）
- 不流行的观点
- 破除误解
- “为什么我不这样做”

## 创意生成技巧

在生成创意时，可以使用以下公式来增加吸引力：

1. **问题引发关注**：“大多数 [目标受众] 在 [某件事] 上浪费了 [时间/金钱]…”
2. **好奇心引导**：“成功人士做的、但没人讨论的事情是……”
3. **社会证明**：“[某人] 如何在 [时间内] 从 [A] 变成了 [B]……”
4. **反传统观点**：“[普遍观点] 是错误的，原因如下……”
5. **操作指南**：“如何在 [时间内] 完成 [目标]（分步说明）”
6. **清单**：“[目标受众] 需要了解的 [主题] 相关的 [数量] 件事”
7. **故事分享**：“我 [做了某事]，结果如何……”

## 与品牌风格的一致性

在生成创意时，要确保内容符合品牌的整体风格和表达方式：

```
1. Load brand-voice/profile.json
2. Match hooks to tone (casual vs professional)
3. Filter ideas by audience match
4. Adapt language to vocabulary preferences
```

## 使用建议

1. **质量胜过数量**：5个高质量的创意比20个平庸的创意更有价值。
2. **跨平台应用**：同一个创意可以用于多个平台（如帖子、博客文章等）。
3. **时效性很重要**：热门话题通常只有24-48小时的窗口期。
4. **独特的视角**：不要仅仅报道趋势，要加入自己的见解。
5. **保存未采用的创意**：暂时不符合需求的创意未来可能会有用。
6. **跟踪效果**：哪些创意能引发受众的互动？