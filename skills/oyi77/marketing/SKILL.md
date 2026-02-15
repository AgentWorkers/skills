---
name: marketing
version: 1.0.0
description: "社交媒体自动化、内容调度、数据分析以及活动管理——将您的人工智能助手转变为一个强大的营销工具，能够处理跨平台的内容策略。"
author: openclaw
---

# 营销技能 📢

**将你的人工智能助手打造成一个战略性的营销伙伴。**

无需持续的人工干预，即可处理社交媒体、内容调度、数据分析以及跨平台的活动管理。

---

## 该技能的功能

✅ **内容创作** — 生成帖子、话题串、新闻通讯以及视觉内容描述
✅ **多平台管理** — Twitter/X、LinkedIn、Instagram、Facebook、新闻通讯
✅ **调度与自动化** — 规划内容日程、安排发布时间、保持内容一致性
✅ **数据分析** — 监控用户互动情况、追踪关键绩效指标（KPIs）、识别趋势
✅ **活动管理** — 规划营销活动、跟踪活动效果、进行A/B测试
✅ **保持品牌语言一致性** — 在所有内容中保持统一的语气和风格

---

## 快速入门

1. 在 `TOOLS.md` 中配置你的营销偏好设置：
```markdown
### Marketing
- Brand voice: [Professional/Casual/Witty/etc.]
- Primary platforms: [Twitter, LinkedIn, etc.]
- Posting frequency: [Daily/3x week/etc.]
- Target audience: [Description]
```

2. 设置你的内容日程：
```bash
./scripts/content-calendar.sh init
```

3. 开始创作内容吧！

---

## 内容策略框架

### 帖子的AIDA模型

| 阶段 | 目的 | 示例引语 |
|-------|---------|--------------|
| **吸引注意** | 阻止用户继续滚动页面 | “大多数营销人员将80%的预算浪费在了这个环节上...” |
| **激发兴趣** | 激发好奇心 | “这就是顶尖1%的营销人员与众不同的地方...” |
| **激发欲望** | 创造用户需求 | “想象一下，在30天内将你的互动次数提高一倍...” |
| **促使行动** | 鼓励用户采取行动 | “今天就试试这个：[可操作的技巧]” |

### 平台特定的最佳实践

**Twitter/X：**
- 最佳长度：100-280个字符
- 使用话题串发布长篇内容（5-15条推文）
- 引语要简洁明了
- 最多使用1-2个标签
- 最佳发布时间：当地时间上午9点、中午12点、下午5点

**LinkedIn：**
- 语气要专业且亲切
- 用一个引人注目的陈述或问题开头
- 使用换行符提高可读性
- 1300-2000个字符的效果最佳
- 包含相关标签（3-5个）

**Instagram：**
- 以视觉内容为主
- 为图片添加说明文字
- 标签策略：在第一条评论中添加20-30个标签
- 每条帖子都要包含明确的行动号召
- 轮播帖子的互动率最高

**新闻通讯：**
- 主题行：40-60个字符
- 预览文本很重要（前90个字符）
- 每封邮件中包含一个明确的行动号召
- 个人故事可以提高打开率
- 定期发送（同一天/同一时间）

---

## 内容日程管理

### 月度规划模板

```markdown
# [Month] Content Calendar

## Themes
- Week 1: [Theme]
- Week 2: [Theme]
- Week 3: [Theme]
- Week 4: [Theme]

## Key Dates
- [Date]: [Event/Holiday]

## Content Mix (per week)
- Educational: 3
- Promotional: 1
- Engagement: 2
- User-generated/Curated: 1

## Platform Schedule
| Day | Twitter | LinkedIn | Instagram | Newsletter |
|-----|---------|----------|-----------|------------|
| Mon | Thread  | Article  | Carousel  | -          |
| Tue | Tips    | -        | Story     | -          |
| Wed | Poll    | Post     | Reel      | Send       |
| Thu | Thread  | -        | Story     | -          |
| Fri | Fun     | Post     | Post      | -          |
```

### 内容批量处理工作流程

1. **创意日**（每月一次）——头脑风暴30多个内容创意
2. **创作日**（每周一次）——一次性完成下周的所有内容
3. **调度日**（每周一次）——将内容上传到调度工具
4. **互动日**（每天）——回复评论、与社区互动

---

## 数据分析与关键绩效指标（KPIs）

### 需要追踪的关键指标

| 指标 | 它告诉你的信息 | 目标增长 |
|--------|-------------------|---------------|
| 浏览量 | 内容覆盖范围 | 每月增长10% |
| 互动率 | 内容质量 | Twitter >3%，LinkedIn >5% |
| 点击率 | 行动号召的有效性 | >2% |
| 关注者增长 | 品牌影响力 | 每月增长5% |
| 转化率 | 商业效果 | 根据目标而定 |

### 周度数据分析模板

```markdown
# Week of [Date] - Analytics Report

## Summary
- Total impressions: [X]
- Total engagement: [X]
- New followers: [X]
- Top performing post: [Link]

## Platform Breakdown

### Twitter
- Impressions: [X]
- Engagement rate: [X]%
- Best day: [Day]
- Top tweet: [Content]

### LinkedIn
- Impressions: [X]
- Engagement rate: [X]%
- Comments: [X]
- Top post: [Content]

## Insights
- What worked: [Analysis]
- What didn't: [Analysis]
- Next week focus: [Adjustment]
```

---

## 活动管理

### 活动规划模板

```markdown
# Campaign: [Name]

## Overview
- **Goal:** [Specific, measurable goal]
- **Timeline:** [Start] - [End]
- **Budget:** [Amount if applicable]
- **Success Metrics:** [KPIs]

## Target Audience
- Demographics: [Age, location, etc.]
- Pain points: [Problems we solve]
- Platforms: [Where they hang out]

## Content Assets
- [ ] Main announcement post
- [ ] Supporting content (X posts)
- [ ] Visuals/graphics
- [ ] Landing page copy
- [ ] Email sequence

## Schedule
| Date | Platform | Content | CTA |
|------|----------|---------|-----|
| [Date] | Twitter | [Content] | [Action] |

## Results (fill after)
- Reach: [X]
- Engagement: [X]
- Conversions: [X]
- ROI: [X]
- Learnings: [What we learned]
```

---

## 内容创作提示

### 用于Twitter话题串的提示
```
Create a Twitter thread on [TOPIC]:
- Hook that stops scrolling
- 5-10 tweets of value
- Each tweet stands alone but builds on previous
- End with CTA and recap
- Conversational but authoritative tone
```

### 用于LinkedIn帖子的提示
```
Write a LinkedIn post about [TOPIC]:
- Opening hook (1-2 lines)
- Personal story or observation
- Key insight or lesson
- Actionable takeaway
- Engagement question
- 1200-1500 characters
```

### 用于新闻通讯的提示
```
Draft newsletter on [TOPIC]:
- Compelling subject line (3 options)
- Personal opening
- Main value content
- One clear CTA
- PS line for bonus engagement
```

---

## 自动化工作流程

### 日常营销流程

```markdown
## Morning (30 min)
- [ ] Check overnight engagement
- [ ] Respond to comments/DMs
- [ ] Share 2-3 relevant posts from others
- [ ] Check trending topics for opportunities

## Afternoon (15 min)
- [ ] Post scheduled content (if not automated)
- [ ] Engage with 5 accounts in your niche
- [ ] Check analytics for unusual activity

## Weekly (1 hour)
- [ ] Review analytics dashboard
- [ ] Plan next week's content
- [ ] Batch create content
- [ ] Update content calendar
```

### 内容再利用矩阵

| 原始内容 | Twitter | LinkedIn | Instagram | 新闻通讯 |
|----------|---------|----------|-----------|------------|
| 博文 | 话题串 | 摘要帖 | 轮播图 | 精选内容 |
| 播客 | 引用推文 | 关键见解 | 音频片段 | 集锦 |
| 视频 | 视频片段 + 话题串 | 嵌入链接 | 视频集 | 背景故事 |

---

## 品牌语言指南

### 语言定义模板

```markdown
# Brand Voice

## We Are
- [Trait 1]: [Example]
- [Trait 2]: [Example]
- [Trait 3]: [Example]

## We Are Not
- [Anti-trait 1]: [Why to avoid]
- [Anti-trait 2]: [Why to avoid]

## Tone Spectrum
Formal ----[X]---- Casual
Serious ----[X]---- Playful
Reserved ----[X]---- Enthusiastic

## Sample Phrases
- Instead of "Click here" → "Dive in"
- Instead of "Buy now" → "Start your journey"
- Instead of "We're the best" → "Here's what we learned"

## Emoji Usage
- Frequency: [Sparingly/Moderate/Freely]
- Favorites: [List emojis that fit brand]
- Never use: [Emojis to avoid]
```

---

## 脚本

### content-calendar.sh
通过命令行管理你的内容日程。

```bash
# Initialize calendar
./scripts/content-calendar.sh init

# Add content
./scripts/content-calendar.sh add "2024-01-15" "twitter" "Thread on productivity"

# View week
./scripts/content-calendar.sh week

# View month
./scripts/content-calendar.sh month
```

### analytics-report.sh
生成每周的数据分析总结。

```bash
# Generate this week's report
./scripts/analytics-report.sh weekly

# Compare to last week
./scripts/analytics-report.sh compare
```

---

## 集成建议

### 与其他技能的集成

| 技能 | 集成方式 |
|-------|-------------|
| **数据分析师** | 深度数据分析、趋势可视化 |
| **销售** | 将营销活动与销售流程对齐 |
| **业务发展** | 为合作伙伴关系创建内容 |

### 常见工作流程

**会议内容转化：**
当你有会议记录时，提取可用于社交媒体的精彩观点。

**数据分析与策略制定：**
利用数据分析师的技能来可视化营销效果，并找出优化机会。

---

## 最佳实践

1. **一致性比完美更重要** — 定期发布比偶尔的完美更重要
2. **80/20内容法则** — 80%的内容质量，20%的推广工作
3. **互动优先，而非单向传播** — 社交媒体是一种互动方式
4. **全面测试** — 对引语、行动号召、发布时间等进行A/B测试
5 **批量创作** — 一次性完成一周的内容
6. **无节制地再利用内容** — 一个创意，多种形式
7. **关注真正重要的指标** — 选择3-5个关键绩效指标，忽略表面数据
8. **保持真实性** — 人们关注的是人，而不是品牌

---

## 故障排除

**互动率低？**
- 核对发布时间与用户活跃时间
- 检查引语是否能够吸引用户继续阅读
- 通过互动（互相回应）提高互动率

**发布内容不统一？**
- 每周批量创作内容
- 使用调度工具
- 建立内容库以备备用

**内容不符合品牌风格？**
- 查看品牌语言指南
- 创建一个包含优秀内容示例的文件
- 发布前检查内容是否符合品牌风格

---

## 许可证

**许可证：** MIT — 可自由使用、修改和分发。

---

*“营销不再取决于你制作的内容，而取决于你讲述的故事。” — Seth Godin*