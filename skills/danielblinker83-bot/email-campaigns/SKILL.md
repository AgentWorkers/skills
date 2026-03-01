---
name: email-campaigns
version: 1.0.0
description: 为任何企业编写高转化率的电子邮件营销活动——包括新闻通讯、重新参与（re-engagement）系列邮件、B2B冷启动（cold outreach）邮件、促销邮件以及自动化邮件发送策略（drip campaigns）。涵盖邮件主题行的编写技巧、用户细分策略（segmentation strategies）以及邮件发送的成功实践（deliverability best practices）。
tags: [email-marketing, newsletter, campaigns, copywriting, automation, b2b-outreach, drip-campaigns]
author: contentai-suite
license: MIT
---
# 电子邮件营销活动 —— 通用电子邮件营销系统

## 该技能的功能

该技能能够创建专业的电子邮件营销活动，确保邮件被打开、阅读，并引发用户的行动。适用于任何企业、任何规模的邮件列表，以及任何营销目标——从发送新闻通讯到开展B2B冷启动营销活动，再到重新吸引用户的活动。

## 使用方法

**输入格式：**
```
BUSINESS NAME: [Your brand]
NICHE: [Your industry]
EMAIL TYPE: [Newsletter / Promotional / Re-engagement / Cold outreach / Welcome sequence]
AUDIENCE SEGMENT: [Active subscribers / Cold leads / Past customers / B2B prospects]
GOAL: [Open rate / Clicks / Purchases / Replies / Appointments]
TONE: [Professional / Casual / Warm / Urgent / Story-based]
LIST SIZE: [Approximate — small <500 / medium 500-5K / large 5K+]
```

---

## 主题行公式

主题行对邮件的打开率有着至关重要的影响（高达80%）。请测试以下主题行生成公式：

```
Curiosity: "The [TOPIC] mistake you're probably making"
Personalization: "[First name], quick question about [TOPIC]"
Urgency: "Last chance: [OFFER] ends tonight"
Benefit: "How to [achieve result] without [pain point]"
Story: "I almost gave up on [thing]. Then this happened."
Number: "7 [TOPIC] tips I wish I knew earlier"
Question: "Are you making this [NICHE] mistake?"
Direct: "[Action] before [date/time]"
```

**主题行生成提示：**
```
Write 10 email subject lines for [BUSINESS NAME] for an email about [TOPIC].
Audience: [AUDIENCE SEGMENT]. Goal: [GOAL].
Mix: 3 curiosity, 2 benefit, 2 urgency, 2 question, 1 story.
Keep each under 50 characters for mobile. No clickbait — must match email content.
```

---

## 电子邮件类型与模板

### 1. 周报
```
SUBJECT: [Subject line formula]

Hi [First Name],

[OPENING — 1-2 sentences: a timely observation, personal note, or question]

[MAIN CONTENT SECTION]
This week I want to share [topic]:

[2-3 paragraphs of genuine value — insight, tip, or story]

[SECONDARY SECTION — optional]
Also this week: [brief mention of another useful resource or news]

[CTA]
[Single, clear action: read full article / book a call / reply with X]

[SIGN-OFF]
[Your name]
[Your title + company]

P.S. [One more insight or soft CTA — P.S. lines get high readership]
```

**新闻通讯提示：**
```
Write a weekly newsletter for [BUSINESS NAME] in [NICHE].
Topic: [MAIN TOPIC]
Opening: personal/relatable (2 sentences)
Main value: [3 paragraphs of insight or advice]
CTA: [desired action]
Tone: [TONE]. Max 400 words. P.S. line with soft CTA.
Subject line: [3 options using different formulas]
```

### 2. 重新吸引用户的活动（针对长期未活跃的订阅者）
```
EMAIL 1 — Subject: "We miss you, [First Name]"
[Acknowledge the time apart]
[Remind them of the value they signed up for]
[Give them a reason to re-engage — exclusive content or offer]
CTA: [Stay subscribed / Check this out]

EMAIL 2 (3 days later) — Subject: "Is this still useful for you?"
[Direct question — are they still interested?]
[What's changed/improved since they subscribed]
CTA: [Click if you want to stay / Unsubscribe if not]

EMAIL 3 (3 days later) — Subject: "Last email from us"
[Respect their time — this is the last one if they don't engage]
[One final compelling reason to stay]
CTA: [Keep me subscribed / Remove me from the list]
```

### 3. B2B冷启动营销活动
```
SUBJECT: [Specific, not generic — reference their company or role]

Hi [Name],

[OPENER — mention something specific about them: their content, their company, a mutual connection]

[BRIDGE — why you're reaching out and how it's relevant to them specifically]

[VALUE PROP — 1-2 sentences: what you do + the specific result for their type of business]

[SOCIAL PROOF — brief: "I've helped [type of company] achieve [result]"]

[SOFT CTA — make it easy to say yes]
Would it make sense to have a quick 15-minute call to see if there's a fit?

[SIGN-OFF]
[Name]
[Title + Company]

P.S. [Optional: relevant case study or resource link]
```

**B2B营销提示：**
```
Write a cold outreach email for [YOUR COMPANY] to [TARGET: job title at company type].
Problem you solve: [specific problem for them]
Your solution: [brief description]
Proof point: [result you've achieved for similar companies]
Tone: Direct, respectful, not salesy. Max 150 words.
Generate 3 subject line options.
```

### 4. 促销邮件
```
SUBJECT: [Benefit + urgency]

Hi [First Name],

[HOOK — start with a story or relatable situation, NOT "I'm excited to announce"]

[PROBLEM — the specific challenge your offer solves]

[OFFER INTRODUCTION — present it as the natural solution]

[WHAT'S INCLUDED — bullet points, keep it brief]

[SOCIAL PROOF — testimonial or result]

[URGENCY/SCARCITY — deadline, limited spots, or bonus]

[CTA BUTTON — clear, action-oriented]
[Button text: "Get instant access" / "Book my spot" / "Claim the offer"]

[OBJECTION HANDLING — 1-2 sentences addressing the main hesitation]

[REPEAT CTA]

[Sign-off]
```

### 5. 欢迎序列（新订阅者，共5封邮件）
```
Email 1 (Immediately): Deliver the promise — welcome + lead magnet/first value
Email 2 (Day 2): Your story — why you do what you do
Email 3 (Day 4): Your best free content — most valuable thing you've shared
Email 4 (Day 6): Social proof — a client result or your own transformation
Email 5 (Day 8): Soft offer — introduce your product/service naturally
```

---

## 分段策略

通过合理分段邮件列表，提升邮件内容的针对性：

| 分段 | 定义 | 内容重点 |
|---------|-----------|---------------|
| 活跃用户 | 近90天内打开过邮件 | 提供完整内容及促销信息 |
| 温和用户 | 91-180天内打开过邮件 | 发送旨在重新吸引用户的邮件 |
| 冷启动用户 | 180天以上未打开邮件 | 发送挽留用户的邮件 |
| 已购买用户 | 曾购买产品 | 提供升级购买或提升客户忠诚度的内容 |
| 潜在客户 | 注册但未购买产品 | 提供教育性内容，引导其完成购买流程 |
| VIP用户 | 高活跃度或高消费用户 | 提供专属优惠及个性化服务 |

---

## 电子邮件送达率检查清单

- [ ] 域名验证已完成（SPF、DKIM、DMARC）
- [ ] 邮件列表保持纯净——每季度清除无效地址 |
- [ ] 必须提供退订链接（法律要求） |
- [ ] 主题行中避免使用“免费”、“保证”、“!!!”、“立即行动”等可能触发垃圾邮件过滤的词汇 |
- [ ] 同时准备纯文本版本和HTML版本 |
- [] 在每次发送邮件前先给自己发送测试邮件 |
- [] 检查邮件在移动设备上的显示效果（移动设备上的打开率应超过60%） |
- [] 保持图片与文本的比例平衡（避免纯图片邮件）

---

## 行业性能基准

| 指标 | 低 | 平均 | 良好 | 优秀 |
|--------|-----|---------|------|-----------|
| 开启率 | <15% | 20-25% | 30-35% | 40%+ |
| 点击率 | <1% | 2-3% | 4-6% | 8%+ |
| 退订率 | >0.5% | 0.2-0.5% | <0.2% | <0.1% |

---

## 与ContentAI Suite的集成

该技能可无缝集成到 **[ContentAI Suite](https://contentai-suite.vercel.app)** 中——这是一个免费的多渠道营销平台，能够为任何企业快速生成专业营销内容。

→ **免费试用：** https://contentai-suite.vercel.app