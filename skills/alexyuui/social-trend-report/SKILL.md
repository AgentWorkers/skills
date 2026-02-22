---
name: social-trend-report
description: 自动化社交媒体趋势监测及基于人工智能的周报生成工具。该工具从Reddit、Twitter/X和YouTube收集数据，生成结构化趋势报告，并提供可操作的内容洞察。适用于需要“监测趋势”、“生成周报”、“进行社交媒体分析”、“内容研究”、“趋势跟踪”或“竞争分析”的场景。支持配置特定行业的子版块、关键词及竞争对手相关数据。
---
# 社交趋势报告

通过监控 Reddit、Twitter/X 和 YouTube，为任何特定领域或行业生成每周趋势报告。

## 概述

该技能自动化了内容研究的工作流程：
1. **收集** 来自多个平台（Reddit、Twitter、YouTube）的数据
2. **分析** 趋势、用户情绪和互动模式
3. **生成** 一份结构化的报告，其中包含可操作的内容创意

## 设置

### 先决条件
- 用于获取 Twitter/X 数据的 `bird` CLI（安装命令：`npm i -g @anthropic/bird`）
  - 需要 Twitter 的认证 cookie：环境变量 `AUTH_TOKEN` 和 `CT0`
- 用于获取 Reddit 数据的 `web_fetch` 工具
- 用于搜索 YouTube 内容的 `web_search` 工具

### 配置

在工作区创建一个 `config.json` 文件以自定义监控目标：

```json
{
  "niche": "your industry/niche name",
  "reddit": {
    "subreddits": ["subreddit1", "subreddit2", "subreddit3"],
    "timeframe": "week",
    "limit": 10
  },
  "twitter": {
    "keywords": ["keyword1", "keyword2 phrase", "keyword3"],
    "lang": "en"
  },
  "youtube": {
    "search_queries": ["niche weekly update", "niche tutorial 2026"],
    "competitors": ["@competitor1", "@competitor2"]
  },
  "output": {
    "dir": "reports",
    "filename_pattern": "weekly-{date}.md",
    "discord_channel": null
  }
}
```

如果不存在 `config.json` 文件，该技能会提示您输入具体的领域和监控目标。

## 工作流程

### 第一步：数据收集

运行 `scripts/collect.sh` 或直接使用相应的工具：

**Reddit**（通过 `web_fetch`）：
```
URL pattern: https://www.reddit.com/r/{subreddit}/top/.json?t=week&limit=10
Extract: title, score, num_comments, selftext (first 200 chars)
```

**Twitter/X**（通过 `bird CLI`）：
```bash
bird search "{keyword}" --limit 20
```

**YouTube**（通过 `web_search`）：
```
Search: "{niche} {keyword} this week" + competitor channel names
```

### 第二步：人工智能分析

将收集到的数据提交给分析引擎，并使用以下分析指令：
> 分析以下社交媒体数据，针对 {niche} 领域：
> 识别：(1) 有数据支持的热门话题；(2) 常见的问题；
> (3) 带有建议格式的内容创意；(4) 竞争对手的动向；(5) 关键词趋势。
> 请提供具体且可操作的信息，并根据互动指标进行优先级排序。

### 第三步：报告输出

报告的结构如下：

```markdown
📊 {Niche} Trend Report ({date_range})

🔥 Trending Topics (3-5)
- Topic — Why it's hot + data (upvotes/views/engagement)

❓ Frequently Asked Questions (3-5)
- Common question → content opportunity

💡 Content Ideas (5)
- Idea title
  - Rationale + data backing
  - Suggested format (video/article/reel/thread)
  - Urgency: 🔴 time-sensitive / 🟡 this week / 🟢 evergreen

📈 Competitor Activity (2-3)
- What competitors published + performance

🌟 Keyword Trends
- High-engagement keywords this period
```

## 自动化

### 使用 OpenClaw 安排定期任务

通过 OpenClaw 的 cron 任务定期生成报告：

```bash
openclaw cron add \
  --name "Weekly Trend Report" \
  --schedule "0 10 * * 1" \
  --timezone "America/New_York" \
  --task "Read skills/social-trend-report/SKILL.md and generate this week's trend report using config.json. Save to reports/ and announce in Discord." \
  --model sonnet
```

### 热点警报模式

如需实时检测趋势，请在 `HEARTBEAT.md` 文件中添加相关配置：

```markdown
- Check if any monitored subreddit has a post with 500+ upvotes in last 24h
- If yes, generate a hotspot alert card and notify
```

## 提示
- **从小处开始**：先监控 2-3 个子版块，之后再逐步扩展
- **Reddit 数据格式**：在 Reddit URL 后添加 `.json` 以获取结构化数据。如果网络受到防火墙限制，请使用 `web_fetch`（而非 `curl`）
- **Twitter 的请求限制**：`bird search` 有请求次数限制，每次运行请控制在 4-6 次查询以内
- **优化搜索词**：根据分析结果不断调整搜索词
- **跨平台信号**：在 Reddit 和 Twitter 上同时热门的话题具有较高的可信度

## 示例领域

该技能适用于任何领域。以下是一些配置示例：
- **塔罗牌/占星术**：r/tarot, r/astrology, r/spirituality + “tarot reading”, “weekly horoscope”
- **SaaS/开发工具**：r/SaaS, r/startups, r/webdev + “developer tools”, “AI coding”
- **电子商务/直接面向消费者（DTC）**：r/ecommerce, r/shopify, r/dropship + “shopify store”, “DTC brand”
- **健身**：r/fitness, r/weightlifting, r/running + “workout routine”, “fitness tips”