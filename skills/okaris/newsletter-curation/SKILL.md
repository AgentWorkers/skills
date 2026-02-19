---
name: newsletter-curation
description: "**新闻通讯策划：内容来源、编辑结构与订阅者增长策略**  
本文档涵盖了新闻通讯的策划流程，包括内容来源管理、编辑框架的构建以及订阅者增长策略。具体内容包括：  
- 新闻通讯的排版规范；  
- 链接汇总的整理方法；  
- 评论文章的撰写风格；  
- 发送新闻通讯的频率安排。  
**适用场景**：  
- 电子邮件新闻通讯；  
- 链接汇总服务；  
- 周度内容摘要；  
- 由专业团队策划的内容推送服务；  
- 创作者专属新闻通讯。  
**相关术语/概念**：  
- 新闻通讯（Newsletter）  
- 内容策划（Content Curation）  
- 订阅者增长（Subscriber Growth）  
- 编辑结构（Editorial Structure）  
- 发送机制（Sending Mechanism）  
- 链接汇总（Link Roundup）  
- 摘要生成（Digest Generation）  
- 模板设计（Template Development）  
**触发条件**：  
- 新闻通讯发布（Newsletter Release）  
- 电子邮件通知（Email Notification）  
- 订阅者增长相关操作（Subscriber Growth Actions）  
- 周度内容更新（Weekly Content Update）  
- 链接更新（Link Update）  
- 新闻通讯撰写（Newsletter Writing）  
- 新闻通讯格式调整（Newsletter Format Adjustment）"
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

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以[手动安装并验证](https://dist.inference.sh/cli/checksums.txt)。

## 新闻通讯格式

### 1. 链接汇总

精选 5-15 个链接，每个链接附有 1-3 句的评论。

```markdown
## This Week's Top Picks

### [Article Title](url)
One to three sentences explaining why this matters and what the
reader will get from it. Add your take — don't just describe.

### [Article Title](url)
Your commentary here. The value is your curation and perspective,
not just the link.
```

### 深度分析 + 链接

一篇 300-500 字的深度分析文章 + 5-8 个精选链接。

```markdown
## The Big Story

[300-500 word analysis of the week's most important topic]

## Also Worth Reading

- **[Title](url)** — One sentence commentary
- **[Title](url)** — One sentence commentary
...
```

### 原创文章

一篇主题明确的文章（500-1,000 字）。

```markdown
## [Essay Title]

[Your original analysis, opinion, or insight]

## What I'm Reading

- [Title](url) — brief note
- [Title](url) — brief note
```

### 问答 / 访谈

与专家或实践者的对话。

### 数据 / 趋势

您所在领域的数字、图表和趋势分析。

## 通讯结构

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

### 哪里可以找到内容

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

| 来源类型 | 示例 | 适合类型 |
|------------|---------|----------|
| **新闻** | TechCrunch、The Verge、行业媒体 | 最新动态 |
| **研究** | 论文、报告、调查 | 数据支持的见解 |
| **博客** | 工程博客、个人博客 | 实践者的观点 |
| **社交媒体** | Twitter 帖子、LinkedIn 发文 | 热门观点、讨论 |
| **工具** | 产品发布、更新 | 实用推荐 |
| **社区** | Reddit、Hacker News、论坛 | 用户的真实反馈 |

### 策划质量筛选标准

对于每篇内容，需要考虑以下问题：

| 问题 | 如果不符合 → |
|---------|---------|
| 我会直接把这个内容发给同事吗？ | 不要包含 |
| 这篇文章能提供有用的信息吗？ | 可以考虑不收录 |
| 来源可信吗？ | 寻找更可靠的来源 |
| 这周的内容及时/相关吗？ | 可以留到以后再发或直接跳过 |
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

### 评论撰写公式

```
[What happened] + [Why it matters to the reader] + [Your take or prediction]
```

## 发送频率

| 发送频率 | 适合类型 | 开启率影响 |
|-----------|---------|-----------------|
| **每周** | 大多数新闻通讯 | 开启率最高——规律性强，不会让人感到压力 |
| **每两周** | 深度分析文章 | 如果内容丰富，效果较好 |
| **每天** | 以新闻为主的简短格式 | 需要养成习惯，但风险较大 |
| **每月** | 研究汇总 | 适合深度内容，但容易被人遗忘 |

**每周发送是最理想的选择。** 每周同一天、同一时间发送，有助于培养读者的阅读习惯。

| 发送日期 | 开启率 |
|-----|------------|
| 星期二 | 最高 |
| 星期四 | 第二高 |
| 星期三 | 第三高 |
| 星期一 | 较低（收件箱可能过满） |
| 星期五 | 较低（周末模式） |
| 周末 | 最低（但某些小众群体可能更感兴趣） |

## 主题行

| 撰写公式 | 示例 |
|---------|---------|
| 期号 + 亮点 | “#47：鲜为人知的框架” |
| 期号 + 主题 | “本月改变我工作流程的 5 个工具” |
| 问题 | “TypeScript 是否正在消亡？” |
| 本周主题 | “本周人工智能领域：GPT-5 的传闻、开源项目的成功” |
| 直接提供价值 | “我希望早些时候就能看到的 SQL 优化指南” |

**主题行长度控制在 50 个字符以内。** 手机屏幕上通常显示的字符数约为 35 个。

## 增长策略

| 策略 | 实施方法 |
|----------|---------------|
| **交叉推广** | 与内容互补的新闻通讯合作 |
| **社交媒体分享** | 在 Twitter/LinkedIn 上发布关键内容，并附上订阅链接 |
| **推荐计划** | “推荐给 3 位朋友” 或提供正式的推荐奖励 |
| **SEO 档案** | 将新闻通讯内容发布为博客文章 |
| **吸引读者的内容** | “订阅即可获得[免费资源]” |
| **保持内容质量** | 最有效的增长策略：内容本身要有价值 |

```bash
# Create social teaser for newsletter
infsh app run x/post-create --input '{
  "text": "This week in The Weekly Signal:\n\n→ Why edge computing is eating the backend\n→ The database migration nobody talks about\n→ 5 tools I discovered this month\n\nJoin 2,000+ engineers: [link]\n\nIssue #47 drops tomorrow morning."
}'
```

## 重要的指标

| 指标 | 达标情况 | 更佳表现 | 表现不佳时的应对措施 |
|--------|------|-------|--------------|
| **开启率** | 30-40% | 40%以上 | 提高主题行的吸引力 |
| **点击率** | 3-5% | 5%以上 | 提升内容策划质量，优化点击链接 |
| **退订率** | 每期低于 0.5% | 低于 0.2% | 检查内容质量和发送频率 |
| **回复率** | 有任何回复 | 定期回复读者 | 提出问题，鼓励互动 |
| **转发率** | 有任何转发 | — | 使内容值得分享 |
| **增长率** | 每月 5-10% | 10%以上 | 增加传播范围，推广推荐计划 |

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 没有固定的发送时间表 | 读者会忘记你的新闻通讯 | 每周同一天、同一时间发送 |
| 链接没有评论 | 这只是个书签，而不是有价值的新闻通讯 | 为每篇文章添加你的见解 |
| 链接过多（超过 15 个） | 内容过于杂乱，没有亮点 | 每期最多精选 5-10 个链接 |
| 主题行过于通用 | 开启率低 | 突出最佳内容，长度控制在 50 个字符以内 |
| 没有个人风格 | 读起来像 RSS 源 | 添加引言段落，表达个人观点和风格 |
| 仅包含宣传内容 | 读者会退订 | 内容中90%应具有价值，宣传内容占比不超过10% |
| 内容质量不稳定 | 读者会失去信任 | 如果内容质量差，可以选择跳过该期 |
| 没有互动引导 | 单向传播 | 提出问题，鼓励读者回复和转发 |
| 没有档案或 SEO 措施 | 缺少增长渠道 | 将新闻通讯内容发布为网页 |

## 相关技能

```bash
npx skills add inference-sh/skills@email-design
npx skills add inference-sh/skills@content-repurposing
npx skills add inference-sh/skills@seo-content-brief
```

查看所有可用工具：`infsh app list`