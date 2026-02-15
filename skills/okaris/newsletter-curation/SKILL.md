---
name: newsletter-curation
description: |
  Newsletter curation with content sourcing, editorial structure, and subscriber growth strategies.
  Covers issue formatting, link roundups, commentary style, and sending cadence.
  Use for: email newsletters, link roundups, weekly digests, curated content, creator newsletters.
  Triggers: newsletter, email newsletter, newsletter curation, weekly digest, link roundup,
  curated newsletter, newsletter writing, newsletter format, subscriber growth,
  newsletter strategy, content curation, newsletter template
allowed-tools: Bash(infsh *)
---

# 新闻通讯策划

通过 [inference.sh](https://inference.sh) 命令行工具来创建和策划高质量的新闻通讯。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Find content to curate
infsh app run tavily/search-assistant --input '{
  "query": "most important AI developments this week 2024"
}'

# Generate newsletter header
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:600px;height:200px;background:linear-gradient(135deg,#1e293b,#334155);display:flex;align-items:center;padding:40px;font-family:system-ui;color:white\"><div><h1 style=\"font-size:32px;margin:0;font-weight:800\">The Weekly Signal</h1><p style=\"font-size:16px;opacity:0.7;margin-top:8px\">Issue #47 — January 15, 2025</p></div></div>"
}'
```

## 新闻通讯的格式

### 1. 链接汇总

精选5-15个链接，并为每个链接附上1-3句话的评论。

```markdown
## This Week's Top Picks

### [Article Title](url)
One to three sentences explaining why this matters and what the
reader will get from it. Add your take — don't just describe.

### [Article Title](url)
Your commentary here. The value is your curation and perspective,
not just the link.
```

### 2. 深度分析 + 链接

一篇300-500字的深度分析文章 + 5-8个精选链接。

```markdown
## The Big Story

[300-500 word analysis of the week's most important topic]

## Also Worth Reading

- **[Title](url)** — One sentence commentary
- **[Title](url)** — One sentence commentary
...
```

### 3. 原创文章

一篇500-1000字的专题文章，需有明确的论点。

```markdown
## [Essay Title]

[Your original analysis, opinion, or insight]

## What I'm Reading

- [Title](url) — brief note
- [Title](url) — brief note
```

### 4. 问答 / 访谈

与专家或实践者的对话。

### 5. 数据/趋势

展示你所在领域的数据、图表和趋势分析。

## 通讯的结构

### 模板

```markdown
# [Newsletter Name] — Issue #[N]

## 👋 Hello

[2-3 sentences of personal intro — what's on your mind,
what this issue covers, why it matters right now]

## 🔥 The Big Story

[Featured content — your deepest analysis or most
important curated piece with commentary]

## 📚 Worth Reading

### [Title 1](url)
[2-3 sentence commentary with your take]

### [Title 2](url)
[2-3 sentence commentary]

### [Title 3](url)
[2-3 sentence commentary]

## 💡 Quick Hits

- [One-liner + link](url)
- [One-liner + link](url)
- [One-liner + link](url)

## 📊 Stat of the Week

[One compelling data point with context]

## 💬 From the Community

[Reader reply, question, or discussion point]

---

That's it for this week. If you found this useful, forward
it to a colleague who'd enjoy it.

[Your name]
```

## 内容来源

### 从哪里获取内容

```bash
# Industry news
infsh app run tavily/search-assistant --input '{
  "query": "[your niche] news this week latest developments"
}'

# Research and data
infsh app run exa/search --input '{
  "query": "[your niche] research report statistics 2024"
}'

# Trending discussions
infsh app run tavily/search-assistant --input '{
  "query": "site:reddit.com [your niche] discussion this week"
}'

# Academic/deep content
infsh app run exa/search --input '{
  "query": "[your niche] analysis deep dive opinion"
}'
```

### 来源类别

| 来源类型 | 示例 | 适合的内容类型 |
|------------|---------|----------|
| **新闻** | TechCrunch、The Verge、行业媒体 | 最新的行业动态 |
| **研究** | 论文、报告、调查 | 基于数据的见解 |
| **博客** | 工程博客、个人博客 | 实践者的观点 |
| **社交媒体** | Twitter帖子、LinkedIn文章 | 热门观点和讨论 |
| **工具** | 产品发布、更新 | 实用建议 |
| **社区** | Reddit、Hacker News、论坛 | 用户的真实反馈 |

### 内容筛选标准

对于每篇内容，需要考虑以下问题：

| 问题 | 如果不符合 → |
|---------|---------|
| 我会把这个内容单独发给同事吗？ | 不要包含这类内容 |
| 这个内容能提供实际帮助吗？ | 可以考虑不收录 |
| 来源是否可信？ | 寻找更可靠的来源 |
| 这个内容是否及时/相关？ | 可以留到以后再发，或者直接跳过 |
| 我能添加有价值的评论吗？ | 仅仅链接是不够的 |

## 撰写评论

### 什么是好的评论

```
❌ Just describing: "This article talks about React Server Components."
❌ Restating the headline: "React Server Components are here."

✅ Adding context: "React Server Components shipped last week, and this
   is the first production teardown I've seen. Key insight: they reduced
   initial JS bundle by 60%, but added complexity to the build pipeline."

✅ Giving your take: "I'm skeptical about the migration path here.
   Most teams I've talked to are waiting for better tooling."

✅ Connecting dots: "This pairs well with Vercel's announcement last
   month — the ecosystem is clearly converging on this pattern."
```

### 评论的撰写格式

```
[What happened] + [Why it matters to the reader] + [Your take or prediction]
```

## 发送频率

| 发送频率 | 适合的内容类型 | 开启率的影响 |
|-----------|---------|-----------------|
| **每周** | 大多数新闻通讯 | 开启率最高——规律性强，不会让人感到压力 |
| **每两周** | 深度分析文章、原创文章 | 如果内容足够丰富，效果较好 |
| **每天** | 以新闻为主的简短内容 | 需要养成习惯，但风险较高 |
| **每月** | 研究汇总 | 适合深度内容，但容易被人遗忘 |

**每周发送是最理想的选择。** 每周同一天、同一时间发送，有助于培养读者的阅读习惯。

| 发送时间 | 开启率 |
|-----|------------|
| 星期二 | 最高 |
| 星期四 | 第二高 |
| 星期三 | 第三高 |
| 星期一 | 较低（收件箱可能过于拥挤） |
| 星期五 | 较低（周末模式） |
| 周末 | 最低（但某些小众群体可能更关注） |

## 主题行

| 撰写公式 | 示例 |
|---------|---------|
| 期号 + 话题简介 | “#47：没人讨论的这个框架” |
| 期号 + 主题 | “本月改变我工作流程的5个工具” |
| 问题式标题 | “TypeScript要消亡了吗？” |
| 本周内容 + 类别 | “本周AI领域动态：GPT-5的传闻、开源项目的成功” |
| 直接提供价值 | “我希望早些时候就有这份SQL优化指南” |

**主题行长度控制在50个字符以内。** 手机端显示时通常会自动截断在35个字符左右。

## 增长策略

| 策略 | 实施方法 |
|----------|---------------|
| **交叉推广** | 与内容互补的新闻通讯合作 |
| **社交媒体分享** | 在Twitter/LinkedIn上分享关键内容，并附上订阅链接 |
| **推荐计划** | “推荐给3位朋友”或提供正式的推荐奖励 |
| **SEO优化** | 将新闻通讯存档为博客文章 |
| **吸引读者的内容** | “订阅即可获得[免费资源]” |
| **保持内容质量** | 最有效的增长策略：内容本身要有价值 |

```bash
# Create social teaser for newsletter
infsh app run x/post-create --input '{
  "text": "This week in The Weekly Signal:\n\n→ Why edge computing is eating the backend\n→ The database migration nobody talks about\n→ 5 tools I discovered this month\n\nJoin 2,000+ engineers: [link]\n\nIssue #47 drops tomorrow morning."
}'
```

## 重要的指标

| 指标 | 良好 | 优秀 | 指标不佳时的应对措施 |
|--------|------|-------|--------------|
| **开启率** | 30-40% | 40%以上 | 提高主题行的吸引力 |
| **点击率** | 3-5% | 5%以上 | 提升内容质量，优化邀请订阅的文案 |
| **退订率** | 每期低于0.5% | 低于0.2% | 检查内容质量和发送频率 |
| **回复率** | 有任何回复 | 定期回复读者 | 提出问题，鼓励互动 |
| **转发率** | 有任何转发 | — | 使内容值得分享 |
| **增长率** | 每月5-10% | 10%以上 | 增加分享渠道，推广推荐计划 |

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 没有固定的发送时间表 | 读者会忘记你的通讯 | 每周同一天、同一时间发送 |
| 链接没有评论 | 你的通讯就像一个书签，没有吸引力 | 为每篇文章添加你的评论 |
| 链接太多（超过15个） | 内容过于杂乱，没有亮点 | 每期最多精选5-10个链接 |
| 主题行过于通用 | 开启率低 | 提炼最精彩的内容，长度控制在50个字符以内 |
| 没有个人风格 | 读起来像RSS订阅源 | 添加引言段落，表达你的观点和个性 |
| 仅包含推广内容 | 读者会退订 | 内容中90%应具有价值，推广内容占比不超过10% |
| 内容质量不稳定 | 会损害读者的信任 | 如果内容质量差，可以选择跳过该期 |
| 没有鼓励互动的提示 | 单向的信息传递 | 提出问题，鼓励读者回复和分享 |
| 没有存档或SEO优化 | 缺少增长渠道 | 将通讯内容发布为网页形式 |

## 相关技能

```bash
npx skills add inferencesh/skills@email-design
npx skills add inferencesh/skills@content-repurposing
npx skills add inferencesh/skills@seo-content-brief
```

查看所有可用工具：`infsh app list`