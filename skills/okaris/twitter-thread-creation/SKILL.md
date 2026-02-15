---
name: twitter-thread-creation
description: |
  Twitter/X thread writing with hook tweets, thread structure, and engagement optimization.
  Covers tweet formatting, character limits, media attachments, and posting strategies.
  Use for: Twitter threads, X posts, tweet storms, Twitter content, social media writing.
  Triggers: twitter thread, tweet thread, x thread, twitter post, tweet writing,
  thread creation, tweet storm, twitter content, x post, twitter writing,
  twitter hook, tweet formatting, thread structure
allowed-tools: Bash(infsh *)
---

# 在 Twitter/X 上创建高互动性的主题帖

通过 [inference.sh](https://inference.sh) 命令行工具来创建高互动性的 Twitter/X 主题帖。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Post a tweet
infsh app run x/post-create --input '{
  "text": "I analyzed 1,000 landing pages.\n\n90% make the same 5 mistakes.\n\nHere are the fixes (with examples):\n\n🧵👇"
}'
```

## 字符限制

| 元素 | 限制 |
|---------|-------|
| 推文文本 | 280 个字符（免费账户），25,000 个字符（高级账户） |
| 主题帖长度 | 无限制（10-15 条推文为最佳） |
| 图片说明文字 | 1,000 个字符 |
| 引用推文 | 280 个字符 |
| 回复 | 280 个字符 |
| 显示名称 | 50 个字符 |

## 主题帖结构

### 主题帖的构成

```
Tweet 1 (Hook):     Bold claim + "thread 🧵"
Tweet 2:            Context / why this matters
Tweet 3-9:          One point per tweet (numbered)
Tweet 10:           Summary or biggest takeaway
Tweet 11:           CTA (follow, retweet, bookmark)
```

### 第一条推文：吸引读者的内容

这条推文可以独立存在于时间线上，也可以作为主题帖的开篇。无论哪种情况，它都必须能够独立吸引读者的注意力。

| 推文类型 | 模板 |
|-----------|----------|
| “我做了 X 并得到了结果” | “我分析了 1,000 个数据。以下是我的发现：” |
| “10 个 [主题] 的技巧” | “[好处]：” |
| “与众不同的观点” | “ unpopular opinion: [引人注目的观点]” |
| “故事开头” | “2019 年，我经历了 [重大事件]。以下是详细经过：” |
| “操作指南” | “如何 [达成目标]（分步说明）：” |
| “令人惊讶的事实” | “[看似错误的统计数据]。让我来解释一下：” |

```bash
# Post hook tweet
infsh app run x/post-create --input '{
  "text": "I spent 3 years building SaaS products.\n\nHere are 10 things I wish someone told me on day 1:\n\n🧵"
}'
```

### 后续推文（3-9 条）

| 规则 | 原因 |
|------|-----|
| 每条推文只包含一个观点 | 有助于清晰表达和便于转发 |
| 推文编号（1/、2/ 等） | 便于读者追踪进度 |
| 每条推文都应独立成篇 | 读者更愿意分享单条推文 |
| 首先提出核心观点 | 避免让读者迷失重点 |
| 使用换行符 | 使内容更易阅读 |
| 包含示例 | 从抽象到具体 |

```bash
# Content tweet with visual
infsh app run x/post-create --input '{
  "text": "3/ Your pricing page is the second most visited page on your site.\n\nBut most founders treat it as an afterthought.\n\nThe fix:\n→ Show 3 tiers (not 2, not 5)\n→ Highlight the middle one\n→ Annual toggle defaulted ON\n→ Feature comparison below"
}'
```

### 结尾推文

```bash
# CTA tweet
infsh app run x/post-create --input '{
  "text": "11/ That'\''s the full playbook.\n\nTL;DR:\n• Validate before building\n• Launch ugly, iterate fast\n• Pricing is positioning\n• Talk to users weekly\n\nIf this was useful:\n→ Retweet the first tweet\n→ Follow me @username for more\n→ Bookmark this thread"
}'
```

## 格式规则

### 推文格式

```
❌ Dense:
"If you want to grow on Twitter you need to post consistently and engage with your audience while also making sure your content provides value to your followers."

✅ Formatted:
"Want to grow on Twitter?

3 non-negotiable rules:

→ Post daily (consistency > quality)
→ Reply to 20 accounts bigger than you
→ Every tweet must teach OR entertain

No shortcuts."
```

### 列表符号的使用

| 符号 | 用途 |
|--------|---------|
| → | 表示步骤、动作或方向 |
| • | 用于列出项目 |
| — | 用于插入补充说明或引用 |
| ✅ | 表示正确做法或优点 |
| ❌ | 表示错误做法或缺点 |
| 1/ 2/ 3/ | 用于编号推文 |

### 换行策略

换行符有助于控制阅读节奏和强调重点内容。

## 主题帖中的媒体元素

### 何时添加图片

| 推文位置 | 图片类型 | 目的 |
|---------------|-----------|---------|
| 开篇推文 | 吸引眼球的图片 | 阻止用户继续滚动 |
| 关键内容 | 屏幕截图、示例 | 作为证据 |
| 总结推文 | 信息图 | 便于分享的总结内容 |

```bash
# Generate thread header image
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1200px;height:675px;background:linear-gradient(135deg,#0f172a,#1e293b);display:flex;align-items:center;justify-content:center;padding:60px;font-family:system-ui;color:white;text-align:center\"><div><h1 style=\"font-size:48px;font-weight:900;line-height:1.2;margin:0\">10 SaaS Pricing Mistakes<br>That Cost You Revenue</h1><p style=\"font-size:22px;opacity:0.5;margin-top:20px\">A thread 🧵</p></div></div>"
}'

# Generate screenshots for evidence
infsh app run infsh/agent-browser --input '{
  "url": "https://example.com/pricing",
  "action": "screenshot"
}'
```

### 图片规格

| 格式 | 尺寸 | 最大文件大小 |
|--------|-----------|----------|
| 单张图片 | 推荐尺寸为 1200 x 675（16:9） | 最大 5 MB |
| 两张图片 | 每张 700 x 800 | 每张 5 MB |
| 四张图片 | 每张 600 x 600 | 每张 5 MB |
| GIF 图片 | 最大尺寸为 1280 x 1080 | 最大 15 MB |

## 主题帖类型

### 教育类主题帖

```
1/ [Topic] explained simply:
2/ What is [concept]?
3/ Why it matters
4-8/ Key principles (numbered)
9/ Common mistakes
10/ Resources
11/ CTA
```

### 故事/经历分享

```
1/ [Dramatic opener]
2/ Background/context
3-7/ Chronological events
8/ The turning point
9/ The lesson
10/ How to apply it
11/ CTA
```

### 信息整理/列表展示

```
1/ [Number] [things] every [audience] needs:
2-10/ One item per tweet with brief explanation
11/ CTA
```

### 分析/解读

```
1/ I analyzed [thing]. Here's what I found:
2/ The setup (what I looked at)
3-8/ Finding 1, 2, 3... with evidence
9/ The biggest surprise
10/ Takeaways
11/ CTA
```

## 提高互动性的策略

| 行动 | 时间 | 原因 |
|--------|--------|-----|
| 发布开篇推文 | 在目标受众的活跃时段（早上 8-10 点或中午 12-1 点） | 最大化初始曝光率 |
| 通过回复串联主题帖 | 在发布开篇推文后立即回复 | 完成整个主题帖的内容 |
| 固定主题帖 | 发布后立即固定主题帖的位置 | 让访客能够看到你的最佳内容 |
| 与回复互动 | 在发布后的 60 分钟内 | 提高平台的算法排名 |
| 引用推文 | 第二天 | 提高再次曝光的机会 |
| 重新发布开篇推文 | 1-2 周后 | 吸引新粉丝 |

## 如何将其他内容转化为主题帖

```bash
# Research source material
infsh app run tavily/search-assistant --input '{
  "query": "latest statistics on remote work productivity 2024"
}'

# Generate visual for the thread
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1200px;height:675px;background:#0f172a;display:flex;align-items:center;padding:60px;font-family:system-ui;color:white\"><div><p style=\"font-size:20px;color:#38bdf8;text-transform:uppercase;letter-spacing:2px\">Data Deep Dive</p><h1 style=\"font-size:52px;font-weight:900;margin:12px 0;line-height:1.2\">Remote Work in 2024:<br>What the Data Actually Says</h1></div></div>"
}'
```

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 开篇推文缺乏吸引力 | 主题帖在第一条推文后就无人关注 | 使用引人注目的开头语句 |
| 推文过多（20 条以上） | 读者会在第 10-12 条推文后失去兴趣 | 最佳数量为 8-12 条 |
| 每条推文包含多个观点 | 造成混淆且不易转发 | 每条推文只包含一个观点 |
| 推文没有编号 | 读者难以跟随进度 | 必须编号（1/、2/、3/ 等） |
| 没有图片 | 有图片的主题帖互动性更高 | 在开篇和关键内容处添加图片 |
| 只发布主题帖（不发布独立推文） | 会错过非主题帖形式的读者 | 也要发布独立推文 |
| 结尾没有呼吁行动的提示 | 错过引导读者转发的机会 | 必须要求读者转发、关注或收藏 |
| 发布时间不当 | 活跃时段之外发布会导致互动率低 | 在目标受众的活跃时段发布 |
| 推文内容过于冗长 | 读者难以阅读 | 使用换行符、符号和简短句子 |

## 相关技能

```bash
npx skills add inferencesh/skills@linkedin-content
npx skills add inferencesh/skills@content-repurposing
npx skills add inferencesh/skills@social-media-carousel
```

查看所有可用工具：`infsh app list`