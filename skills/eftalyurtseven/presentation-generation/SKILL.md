---
name: presentation-generation
description: 使用 each::sense AI 生成专业的演示文稿和幻灯片集。通过 AI 驱动的幻灯片生成功能，您可以制作产品推介资料、商务演示文稿、培训材料、会议演讲等内容。
metadata:
  author: eachlabs
  version: "1.0"
---
# 演示文稿生成

使用 `each::sense` 功能可以生成专业的演示文稿和幻灯片集。该技能能够为商业演示、提案演示、教育内容等创建视觉效果出色的幻灯片。

## 特点

- **商业演示文稿**：适用于公司会议和报告的专业幻灯片
- **提案演示文稿**：具有清晰叙述结构的投资者演示文稿
- **销售演示文稿**：用于客户提案和演示的说服性幻灯片
- **教育幻灯片**：包含清晰视觉效果的教学和课程材料
- **培训材料**：用于新员工入职和技能提升的演示文稿
- **产品发布**：具有影响力的产品发布幻灯片
- **季度报告**：包含数据可视化的报告演示文稿
- **会议演讲**：适用于主题演讲和分会场的演示文稿

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10-slide business presentation about digital transformation strategy for enterprise companies. Include title slide, agenda, key challenges, solutions, case studies, implementation roadmap, and closing slide.",
    "mode": "max"
  }'
```

## 演示文稿类型及使用场景

| 类型 | 幻灯片数量 | 适用场景 |
|------|--------|----------|
| 提案演示文稿 | 10-15张 | 投资者会议、筹款活动 |
| 销售演示文稿 | 8-12张 | 客户提案、产品演示 |
| 商业演示文稿 | 10-20张 | 战略会议、高管简报 |
| 培训演示文稿 | 15-30张 | 新员工入职、技能培训 |
| 会议演讲 | 20-40张 | 主题演讲、技术会议 |
| 季度报告 | 10-15张 | 利益相关者更新、董事会会议 |
| 产品发布 | 10-15张 | 产品发布活动、营销活动 |

## 使用场景示例

### 1. 商业演示文稿（示例）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 12-slide business presentation on AI adoption in healthcare. Include: title slide, executive summary, current state of healthcare AI, key use cases (diagnosis, drug discovery, patient care), implementation challenges, ROI analysis, case study examples, future trends, recommendations, and conclusion with next steps. Professional corporate style with blue color scheme.",
    "mode": "max"
  }'
```

### 2. 投资者提案演示文稿（示例）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10-slide startup pitch deck for a fintech company that provides AI-powered expense management for small businesses. Include: cover slide with company name TechExpense, problem statement showing SMB pain points, solution overview, product demo screenshots, market size ($50B TAM), business model (SaaS subscription), traction (10K users, 40% MoM growth), competitive landscape, team slide, and ask slide ($5M Series A). Modern, clean design with fintech aesthetic.",
    "mode": "max"
  }'
```

### 3. 销售演示文稿（示例）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an 8-slide sales presentation for enterprise cloud security software. Include: title slide, client pain points (data breaches, compliance, complexity), our solution overview, key features (real-time monitoring, automated compliance, AI threat detection), customer success stories with metrics, pricing tiers, implementation timeline, and call-to-action slide. Professional but engaging style, use security-themed visuals.",
    "mode": "max"
  }'
```

### 4. 教育/讲座幻灯片（示例）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 15-slide educational presentation on Machine Learning fundamentals for university students. Include: title slide, learning objectives, what is ML (definition), types of ML (supervised, unsupervised, reinforcement), key algorithms overview, neural networks basics, real-world applications, hands-on exercise introduction, common pitfalls, best practices, resources for further learning, summary, and Q&A slide. Academic style with diagrams and visualizations.",
    "mode": "max"
  }'
```

### 5. 培训演示文稿（示例）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 20-slide employee onboarding training presentation for a tech company. Include: welcome slide, company history and mission, organizational structure, core values, team introductions section, key policies (remote work, PTO, benefits), tools and systems overview (Slack, Jira, GitHub), security and compliance training, first week checklist, 30-60-90 day goals, mentorship program, career development paths, FAQ section, key contacts, and closing slide with encouragement. Friendly, approachable design with company brand colors (teal and orange).",
    "mode": "max"
  }'
```

### 6. 产品发布幻灯片（示例）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 12-slide product launch presentation for a new AI-powered fitness app called FitGenius. Include: dramatic title slide, the fitness problem (lack of personalization), introducing FitGenius, key features (AI coach, adaptive workouts, nutrition tracking, progress analytics), how it works (3-step process), app screenshots showcase, early user testimonials, pricing plans, launch timeline, press and influencer strategy, and closing call-to-action. Energetic, modern design with gradient colors (purple to orange).",
    "mode": "max"
  }'
```

### 7. 季度报告演示文稿（示例）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10-slide Q4 2024 quarterly report presentation for a SaaS company. Include: title slide with company logo placeholder, executive summary with key metrics, revenue performance (show $12M ARR, 25% YoY growth), customer metrics (500 new customers, 95% retention), product updates shipped this quarter, team growth (20 new hires), challenges faced and lessons learned, Q1 2025 priorities and goals, financial outlook, and thank you slide. Data-driven with charts and graphs, professional corporate style.",
    "mode": "max"
  }'
```

### 8. 会议演讲幻灯片（示例）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 25-slide conference talk presentation titled Building Scalable Microservices: Lessons from 1 Million RPS. Include: title slide with speaker name placeholder, about me slide, agenda, the scaling journey story (monolith to microservices), architecture evolution diagrams, key technical decisions, database strategies, caching layers, message queues, monitoring and observability, failure stories and recovery, performance benchmarks, cost optimization, team structure, lessons learned (5 slides with one key insight each), what we would do differently, future roadmap, resources and references, Q&A slide, and contact/social media slide. Tech conference style, dark theme with code snippets.",
    "mode": "max"
  }'
```

### 9. 网络研讨会幻灯片（示例）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 15-slide webinar presentation on Email Marketing Best Practices for E-commerce in 2025. Include: title slide with webinar branding, host introduction, agenda with timing, why email still matters (stats), building your list ethically, segmentation strategies, personalization techniques, automation workflows (welcome, abandoned cart, win-back), subject line optimization, mobile-first design, A/B testing framework, deliverability tips, measuring success (KPIs), live Q&A slide, and special offer slide with CTA. Marketing-focused design, vibrant but professional.",
    "mode": "max"
  }'
```

### 10. 团队会议演示文稿（示例）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an 8-slide weekly team meeting presentation for an engineering team. Include: title slide with date placeholder, sprint progress (velocity chart, completed vs planned), blockers and dependencies, demo highlights (2 features shipped), upcoming priorities for next sprint, team announcements (new hire, PTO), metrics dashboard (bugs fixed, deployment frequency, incident count), and open discussion slide. Simple, functional design focused on clarity, light theme.",
    "mode": "max"
  }'
```

## 最佳实践

### 内容结构
- **以引人注目的开头开始**：用一个吸引人的开场白吸引观众
- **每张幻灯片一个主题**：保持幻灯片的专注性和易读性
- **视觉层次结构**：有效使用标题、子标题和项目符号
- **数据可视化**：使用图表和图形来展示复杂数据
- **统一的设计风格**：在整个演示文稿中保持视觉一致性

### 幻灯片设计
- **简洁的文字**：每个项目符号不超过6个单词，每张幻灯片最多3个项目符号
- **高对比度**：确保文字和背景之间的对比度足够高，便于阅读
- **适当的空白空间**：为内容留出足够的展示空间
- **统一的字体**：最多使用2-3种字体
- **高质量的图片**：使用相关的高分辨率图片

### 演示文稿类型
- **提案演示文稿**：重点介绍故事、问题解决方案以及明确的需求
- **销售演示文稿**：首先展示价值，再提供支持证据
- **培训材料**：逐步披露信息，并包含练习环节
- **会议演讲**：强调核心观点，使用易于记忆的视觉元素

## 演示文稿制作提示

在创建演示文稿时，请包含以下细节：
1. **幻灯片数量**：指定所需的幻灯片数量
2. **结构**：列出需要包含的章节和幻灯片
3. **目标受众**：谁将观看这份演示文稿？
4. **风格**：企业风格、现代风格、趣味风格、学术风格等
5. **颜色**：使用品牌颜色或自定义的颜色方案
6. **数据内容**：包含具体的数字、指标或统计数据
7. **视觉元素**：请求提供图表、图表或特定的图片

### 演示文稿制作提示示例结构

```
"Create a [number]-slide [type] presentation about [topic].
Include: [list of slides/sections].
Audience: [who will view it].
Style: [design preferences].
[Additional requirements like colors, data points, etc.]"
```

## 模式选择

**“您需要快速且低成本的解决方案，还是高质量的作品？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终演示文稿、面向客户的演示文稿、重要会议 | 较慢 | 最高质量 |
| `eco` | 快速草稿、内部会议、概念探索 | 较快 | 良好质量 |

## 多轮迭代

使用 `session_id` 来迭代和完善您的演示文稿：

```bash
# Initial presentation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10-slide pitch deck for a sustainable fashion marketplace",
    "session_id": "pitch-deck-project"
  }'

# Add more slides
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add 3 more slides: one for partnerships, one for sustainability metrics, and one for media coverage",
    "session_id": "pitch-deck-project"
  }'

# Refine specific slide
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Update the market size slide with more detailed TAM/SAM/SOM breakdown",
    "session_id": "pitch-deck-project"
  }'

# Change design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the design more minimalist with earth tones to match our sustainability brand",
    "session_id": "pitch-deck-project"
  }'
```

## 为不同受众生成多个版本

可以为不同的受众生成多个版本的演示文稿：

```bash
# Version for investors
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10-slide pitch deck for our AI analytics product - investor focused, emphasize market size, growth metrics, and funding ask",
    "mode": "eco"
  }'

# Version for enterprise clients
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10-slide sales deck for our AI analytics product - enterprise client focused, emphasize ROI, security, integration capabilities",
    "mode": "eco"
  }'

# Version for technical audience
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10-slide technical overview for our AI analytics product - developer focused, emphasize architecture, APIs, and technical capabilities",
    "mode": "eco"
  }'
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 账户余额不足 | 在 eachlabs.ai 充值 |
| 内容违规 | 使用被禁止的内容 | 调整提示以符合内容政策 |
| 超时 | 生成过程复杂 | 将客户端的超时时间设置为至少10分钟 |

## 相关技能

- `each-sense`：核心API文档
- `meta-ad-creative-generation`：元广告创意生成工具
- `product-photo-generation`：用于幻灯片的产品图片生成工具