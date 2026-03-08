---
name: coffee-chat
description: >
  生成一份个性化的咖啡聊天脚本，用于网络交流。适用场景包括：
  - 用户希望为与在 LinkedIn 上认识的人的咖啡聊天做准备；
  - 在见面前需要收集有关专业联系人的信息；
  - 为网络会议创建聊天指南。
  触发词：**“coffee chat”**、**“networking prep”**、**“coffee chat prep”**、**“chat playbook”**、**“meeting prep”**。
  该技能包含以下步骤：
  1. 收集目标人物的姓名和 LinkedIn 链接；
  2. 调查其所在公司和所在行业的背景信息；
  3. 查找该公司的创始人或员工的背景资料；
  4. 根据收集到的信息，生成一份详细的咖啡聊天脚本。
---
# 咖啡聊天剧本生成器

该技能可帮助您通过收集目标人物的相关信息并生成个性化的聊天指南，为专业的咖啡聊天做好准备。

---

## 先决条件

在使用此技能之前，请完成以下设置。仅**Apify CLI**是进行X（Twitter）数据抓取所必需的——其他功能均为可选。

### 1. Apify CLI（用于X/Twitter数据抓取）

Apify CLI用于运行Twitter数据抓取任务。

**安装：**
```bash
npm install -g apify-cli
```

**身份验证：**
```bash
apify login
# Paste your Apify API token when prompted
# Get your token at: https://console.apify.com/account/integrations
```

**验证：**
```bash
apify info
# Should show your username and token
```

> 免费 tier 每月提供5美元的计算额度。抓取10条推文大约花费0.004美元，完全在免费范围内。

---

### 2. Notion集成（可选——用于将剧本保存到Notion）

**创建集成：**
1. 访问 https://www.notion.so/my-integrations
2. 点击 “新建集成”
3. 为其命名（例如：“咖啡聊天技能”）
4. 复制 **内部集成令牌**

**设置API密钥：**
```bash
export NOTION_API_KEY="secret_xxxxxxxxxxxxxxxxxxxx"
# Add to your shell profile to persist:
echo 'export NOTION_API_KEY="secret_xxxxxxxxxxxxxxxxxxxx"' >> ~/.zshrc
```

**将您的Notion页面分享给集成：**
1. 打开您希望保存剧本的Notion页面
2. 点击 “...” → “添加连接” → 选择您的集成
3. 从URL中复制页面ID：
   - URL: `https://notion.so/My-Page-abc123def456...`
   - 页面ID: `abc123def456...`（最后一个 `-` 之后的部分）

**在此技能的Notion推送部分更新 `NOTION_PAGE_ID`。**

---

### 3. 网页搜索与数据获取（用于公司背景调查）

该技能依赖于网页搜索和数据获取功能来调查目标人物的公司、行业背景等信息。您的AI代理需要具备这些工具的访问权限。

**如果使用OpenClaw或Claude Code：**
- 网页搜索和数据获取功能已内置——无需额外设置

**如果使用其他代理框架，请确保其具备以下权限：**
- **搜索API**（例如Brave Search、Serper、Tavily、You.com），用于查询公司新闻、融资信息、创始人背景
- **网页数据获取/抓取工具**，用于读取公司网站、LinkedIn个人资料、新闻文章等内容

> 如果没有这些工具，代理将仅依赖训练数据，可能导致信息过时。此时调研质量会显著下降。

---

### 4. 所需工具/变量一览

| 工具/变量 | 是否必需 | 说明 |
|-----------------|----------|-------------|
| 网页搜索API | 是（用于调研） | OpenClaw/Claude Code内置；否则需配置代理的搜索插件 |
| 网页数据获取 | 是（用于调研） | OpenClaw/Claude Code内置；否则需配置代理的数据获取工具 |
| `APIFY_API_TOKEN` | 用于X数据抓取 | 通过 `apify login` 自动设置 |
| `NOTION_API_KEY` | 可选 | 您的Notion集成令牌 |

---

## 设置（首次使用）

在使用此技能之前，请在 `memory/my-profile.md` 文件中创建您的个人资料文件：

```markdown
# My Profile

- **Name**: [Your Name]
- **Role**: [Your current role and company]
- **Background**: [Brief career background, e.g. Finance → VC → AI]
- **Location**: [City, Country]
- **LinkedIn**: [Your LinkedIn URL]
- **Interests**: [Topics you care about / want to discuss]
```

同时配置集成（可选）：
- **Notion**：设置 `NOTION_API_KEY` 环境变量，并更新下方Notion推送部分的 `NOTION_PAGE_ID`
- **Apify**：为LinkedIn数据抓取设置 `APIFY_API_TOKEN` 环境变量（免费 tier可用）

---

## 工作流程

### 第1步：收集信息

向用户询问以下信息：
1. **目标人物的姓名**（必需）
2. **目标的LinkedIn个人资料链接**（可选，但推荐）
3. **目标公司的名称**（用于调研）
4. **目标的X（Twitter）用户名**（可选，例如 `@elonmusk` 或仅输入 `elonmusk`）——用于抓取最新帖子
5. **聊天的背景信息**（可选——如何认识目标人物、聊天目的）

从 `memory/my-profile.md` 文件中加载您的个人资料以供参考。

### 第2步：调查目标公司的信息

针对每个目标人物，进行全面的 company 调查：

1. **通过网页搜索** 获取公司信息：
   - 融资动态
   - 产品/功能发布
   - 团队/创始人信息

2. **在X（Twitter）上搜索** 公司账号：
   - 最新帖子
   - 产品演示
   - 与社区的互动情况

3. **搜索相关新闻**：
   - 公司融资公告
   - 产品发布
   - 行业动态

### 第3步：调查目标人物的背景信息

1. 通过网页搜索找到目标的LinkedIn个人资料
2. （如果使用Apify）抓取LinkedIn上的帖子
3. （如果用户提供了X（Twitter）用户名）执行以下操作：

```bash
apify call apidojo/tweet-scraper --input '{
  "searchTerms": ["from:USERNAME"],
  "maxTweets": 10,
  "sort": "Latest"
}' --output-dataset --silent
```

将 `USERNAME` 替换为目标人物的X用户名（不包括 `@`）。

- 解析数据并提取：推文内容、发布日期、点赞数、转发数、回复数
- 如果 `APIFY_API_TOKEN` 未设置或抓取失败，切换到网页搜索以获取最新的X推文
- 如果未提供X用户名，则跳过此步骤

4. **收集背景信息**：
   - 之前的工作经历
   - 教育背景
   - 重要项目/成就
   - 最近的帖子/关注话题（来自LinkedIn和X）

### 第4步：生成完整的聊天剧本

遵循以下 **完整剧本模板**，包含所有部分：
- 目标人物简介
- 公司与行业调研（详细信息）
- 创始人背景分析（针对初创公司）
- 最新内容与帖子
- 个人资料对比
- 8个问题
- 4个讨论要点
- 沟通技巧
- 聊天前准备清单

### 第5步：保存并推送到Notion（可选）

1. **本地保存**：`memory/coffee-chat-{target-slug}-{YYYY-MM-DD}.md`
2. **推送到Notion**：如果已设置 `NOTION_API_KEY`，则将文件添加到您的Notion页面

---

## 完整剧本模板

```markdown
# ☕ Coffee Chat Playbook: [Target Company/Name]

**Date:** [YYYY-MM-DD]
**Status:** Researched

---

## 📋 Target Profile Summary

### Basic Info
- **Target**: [Name] (Founder/CEO/PM at [Company])
- **LinkedIn**: [URL]
- **Location**: [City, Country]
- **Connection**: [How you met]

### Background
- [Previous career/experience]
- [Notable projects or achievements]
- [Education]

### Recent Posts / Topics
- [Topic 1 from LinkedIn/X]
- [Topic 2]
- [Topic 3]

---

## 🏢 Company & Industry Research

### Company Overview
- **Company Name**: [Name]
- **Founded**: [Year]
- **Location**: [HQ location]
- **Funding**: [Amount] ([Investors]) - [Date]
- **Team**: [Size/distribution if known]
- **X/Website**: [Links]

### Product
- [Product description]
- [Key features]
- [Target users]

### Industry Landscape
- **Market**: [Brief description of market]
- **Competitors**: [List key competitors]
- **Trends**: [Industry trends]
- **Challenges**: [Key challenges]
- **Opportunities**: [Opportunities]

### Investors (if applicable)
- **Investor 1**: [Background]
- **Investor 2**: [Background]

---

## 👥 Founder Deep Dive (for startups)

### [Founder 1 Name] ([Title])
- **Background**: [e.g., Documentary filmmaker, Ex-Google, etc.]
- **Work history**: [Notable companies/clients]
- **Notable achievements**: [e.g., Founded X, Award Y]
- **Philosophy/Interests**: [From posts]

### [Founder 2 Name] ([Title])
- [Same structure]

---

## 📱 Recent Content & Posts

### LinkedIn Posts
- [Post 1: topic and key message]
- [Post 2]
- [Post 3]

### X (Twitter) Posts — Last 10
> Scraped via apidojo/tweet-scraper. If X username not provided, use web search results.

| # | Date | Tweet | Likes | RT | Replies |
|---|------|-------|-------|----|---------|
| 1 | [YYYY-MM-DD] | [Full tweet text] | [n] | [n] | [n] |
| 2 | [YYYY-MM-DD] | [Full tweet text] | [n] | [n] | [n] |
| 3 | [YYYY-MM-DD] | [Full tweet text] | [n] | [n] | [n] |
| ... | | | | | |

**Key themes from X posts:**
- [Theme 1: what they talk about most]
- [Theme 2: opinions/stances]
- [Theme 3: recent interests or announcements]

**Engagement pattern**: [High/Medium/Low — what type of content gets most engagement]

---

## 🔍 Profile Comparison (You vs Target)

### Your Profile
- **Role**: [Load from memory/my-profile.md]
- **Background**: [Load from memory/my-profile.md]
- **Location**: [Load from memory/my-profile.md]

### Common Ground
- [Common industry or domain]
- [Similar career transition experience]
- [Shared interests]

### Conversation Starters (Based on Research)
1. "[Based on their product launch] I saw [product] launched - what was the inspiration?"
2. "[Based on their background] As someone who transitioned from [old career] to [new career], what surprised you most?"
3. "[Based on their philosophy] Your focus on [X] resonates with me because..."
4. "[Based on investors] How did you approach raising from [Investor]?"
5. "[Based on team] With your distributed team across [locations], how do you manage collaboration?"

---

## 💬 Questions to Ask (8 total)

### 👤 Personal (3)
1. [Question based on their background - e.g., "What prompted your transition from X to Y?"]
2. [Question based on their location/move - e.g., "What's it like building a US company from [location]?"]
3. [Question based on their interests - e.g., "I saw you worked on [project] - what was that experience like?"]

### 💼 Work-Related (3)
4. [Question about their product - e.g., "How is [Company] different from competitors?"]
5. [Question about challenges - e.g., "What's been the biggest challenge building [Company]?"]
6. [Question about team/culture - e.g., "How do you think about team building as a founder?"]

### 🌐 Industry (2)
7. [Question about industry trends - e.g., "Where do you see the industry heading in 2-3 years?"]
8. [Question about advice - e.g., "What advice would you give to someone in my role?"]

---

## 🗣️ Your Talking Points (4)

1. **Your background**: [Load from memory/my-profile.md]
2. **What you admire**: [Something specific from their profile/posts]
3. **Your work**: [Current role and what you're building]
4. **Curiosity**: [Something specific you want to learn from them]

---

## 🧭 Communication Principles & In-Chat Guide

### ☕ The COFFEE Framework (30-min structure)

Use this as your session blueprint. Every great coffee chat has a shape.

| Time | Phase | What to do |
|------|-------|------------|
| 0–5 min | **C — Connect** | Start human. Share who you are briefly. Ask about them first. |
| 5–10 min | **O — Offer Proof** + **F — Frame** | Optionally show a 60-sec artifact (1-pager, analysis, teardown) that proves you've done homework. Then frame the agenda: *"I have a few questions — happy to go wherever is useful for you too."* |
| 10–25 min | **F — Focused Questions** | Ask 2–3 non-Googleable questions. Listen 70%, talk 30%. Follow their thread. |
| 25–30 min | **E — End on Time** | Start wrapping at min 25. Don't let it run over. |
| Closing | **E — Extend Help** | Before you leave: *"Is there anything I can help with from my end?"* |

> **Litmus test for every question:** If the answer is fully on Google or their LinkedIn, don't ask it. Ask things only *they* can answer.

---

### The Golden Rule: 70/30

> **They talk 70%, you talk 30%.** Your job is to draw them out, not to impress them.

- Ask open-ended questions, then listen fully before responding
- Don't fill silence — let them think
- Put your phone away. Be fully present

---

### 🤝 Nonverbal Signals (Don't Overlook These)

| Signal | What to do |
|--------|-----------|
| Eye contact | Maintain natural eye contact — shows you're engaged |
| Nodding | Nod slowly to signal you're following and interested |
| Smile | Warm, genuine smiles — not forced |
| Body posture | Lean slightly forward, open body language, no crossed arms |
| Hands | Keep visible, use to emphasize points naturally |
| Phone | Face-down or away — checking it kills rapport instantly |

---

### 🎭 Identify Their Networker Persona

Read the room in the first 2-3 minutes. Adjust your style accordingly.

#### 🔵 Practicalist
> Fact-driven, problem-solver, sticks to the point, values time efficiency

**Signs**: Gets straight to business, asks direct questions, gives concise answers

**Your technique**:
- Be clear on your intention upfront ("I'm here to learn about X")
- Skip small talk, lead with substance
- Give them space to respond — don't ramble
- Use data and specifics, not vague observations

**Sample opener**: *"I wanted to connect because [specific reason]. I have a few focused questions — hope that works for you."*

---

#### 🟡 Conversationalist
> Personable, relationship-focused, loves stories, open to tangents

**Signs**: Asks personal questions, shares stories, warm and expressive

**Your technique**:
- Power on small talk — ask about their weekend, their city, their journey
- Match their warmth and storytelling style
- Pay close attention to body language — they're reading yours too
- Let conversations flow naturally, don't over-structure

**Sample opener**: *"I loved your post about [X] — it really resonated with me. How did that come about?"*

---

#### 🔴 Dominator
> Dominates the conversation, tends to be the one asking questions, high-status energy

**Signs**: Asks lots of questions, steers topics, rarely pauses for your input

**Your technique**:
- Listen to their questions — they reveal what they care about
- Be more assertive: when there's a natural pause, jump in with your question
- Use bridging phrases: *"That's a great point — it makes me curious about..."*
- Don't wait to be invited — politely redirect to your agenda

**Sample opener**: *"Before I forget — I actually had a specific question I was hoping to get your take on..."*

---

### 💬 Question Bank (70/30 Principle)

Design questions to keep them talking. Follow up on their answers before moving to the next question.

> **How to use this bank:**
> - Pick 2-3 **Core Questions** per section — these are your main agenda
> - Use **Follow-Up Questions** only if time allows and the topic naturally opens up
> - Use **Transition Phrases** to move between topics without abrupt cuts

---

#### 🔓 Warm-Up (first 5 min — build comfort)

**Core:**
- *"How's your week going? Anything exciting on your plate right now?"*
- *"How did you end up in [city/role]? Was it planned or did it just happen?"*

**Follow-up (if they open up):**
- *"What do you enjoy most about being based in [city]?"*
- *"Was there a specific moment that made you decide to make the move?"*

**Transition into background:** *"That's really interesting — I'd love to hear more about your path to where you are now..."*

---

#### 🧬 Background & Journey (understand their path)

**Core:**
- *"What drew you to [industry/role] originally?"*
- *"What's been the most unexpected part of your journey so far?"*
- *"If you could start all over again, would you change your career path in any way?"* *(UB)*

**Follow-up (if time allows):**
- *"If you could go back and tell your younger self one thing, what would it be?"*
- *"Was there a specific decision that really changed the trajectory of things?"*
- *"How long does it typically take for people to rise to more senior levels in this field?"* *(UB)*

**Transition into work:** *"It sounds like you've built a really intentional path. I'm curious how that shapes how you think about [Company] today..."*

---

#### 🏢 Work & Company (go deeper on what they do)

**Core:**
- *"What does a great day at work look like for you right now?"*
- *"What's the hardest problem [Company] is working through?"*
- *"What parts of your job do you find most challenging — and most enjoyable?"* *(UB)*

**Follow-up (if they go deep):**
- *"How has the team's approach evolved as you've scaled?"*
- *"What's something people on the outside misunderstand about what you're building?"*
- *"How would you describe the culture — what kind of person thrives here?"* *(UB)*
- *"Why do people typically leave this company or field?"* *(UB)*

**Transition into industry:** *"Given everything you're seeing up close at [Company], I'd love your take on where the broader space is going..."*

---

#### 🌐 Industry & Trends (show intellectual curiosity)

**Core:**
- *"Where do you think [industry] is heading in the next 2-3 years?"*
- *"What's a trend you're watching that most people aren't paying attention to yet?"*
- *"What are the biggest challenges facing this industry right now?"* *(MIT)*

**Follow-up (if time allows):**
- *"Who do you think is doing the most interesting work in this space right now?"*
- *"Is there a bet you're making that feels contrarian to the mainstream view?"*
- *"Is the field growing — are there good opportunities for newcomers?"* *(UB)*
- *"What developments on the horizon could affect opportunities in this space?"* *(UB)*

**Transition into closing:** *"This has been really eye-opening — before we wrap up, I wanted to make sure I ask..."*

---

#### 🤝 Relationship-Building & Closing (make it mutual)

**Core:**
- *"Is there anything I can help with from my end — introductions, resources, anything?"*
- *"Would it be okay to keep in touch? I'd love to follow your journey."*
- *"Are there any questions I should have asked but didn't?"* *(MIT — always ask this)*

**Follow-up:**
- *"Who else do you think I should be talking to in this space? Would it be okay to use your name?"* *(UB)*
- *"What resources — books, podcasts, communities — would you recommend I look into?"* *(MIT)*

---

#### ⚡ Persona-Specific Follow-Ups
- **Practicalist**: *"How do you measure success on that?"* / *"What's the ROI you're seeing?"*
- **Conversationalist**: *"Tell me more about that — how did it feel?"* / *"What was the moment you knew?"*
- **Dominator**: *"You mentioned [X] — I've been thinking about that a lot. Can I ask your take on [Y]?"*

---

#### 🏛️ Consulting / Finance / High-Prestige Firm (use when target works at MBB, Big 4, investment bank, etc.)

These questions are sharper and more direct — suited for time-pressed, high-status professionals who respect preparation.

**About their firm & culture:**
- *"What surprised you most about [Firm] that you only discovered after joining?"*
- *"How would you describe someone who truly excels here — what separates them from the rest?"*
- *"What do you see as [Firm]'s biggest opportunity and biggest challenge right now?"*
- *"How would you compare [Firm] to others you've worked with or considered?"*

**About their career path:**
- *"What underrated skill do you think accelerated your growth here?"*
- *"What surprised you most moving from individual contributor to managing others?"*
- *"Looking back, what do you wish you'd known before entering this field?"*

**Situational / behavioral (if they're senior and the vibe allows):**
- *"Tell me about a time you had to persuade someone to change their mind when the stakes were high — how did you approach it?"*
- *"Describe a moment when you had to make a call with limited information. What did you do?"*
- *"What's a professional risk you took that paid off — and one that didn't?"*

**About breaking in (if you're exploring the field):**
- *"How do most people at your level enter this field — what paths tend to work?"*
- *"Considering my background, how well do you think I'd fit into this type of role?"* *(UB)*
- *"What would you recommend I do in the next 6 months to be a stronger candidate?"*
- *"Are there specific companies or teams within the industry you'd suggest I look at?"*

> **Tone note for consulting/finance targets:** Be crisp. Lead with your agenda. They appreciate directness and hate meandering. Show you've done the homework — reference their work, their firm's recent deals or reports, their public writing.

---

### 🔍 Finding Common Ground (TLDR)

Before the chat, scan their LinkedIn/X for:
- **Shared experiences**: same industry, career pivot, city, university
- **Shared interests**: topics they post about repeatedly
- **Shared values**: how they talk about their work and people

Use these to open genuine threads — not forced flattery. One real connection beats five generic questions.

---

### ✨ Value-Added Mindset

Go in with a giving mentality, not just a taking one:
- Bring a relevant article, resource, or intro to offer
- Share a genuine observation about their work: *"I noticed [X] — have you considered [Y]?"*
- Follow up within 24hrs: summarize 1-2 things you learned and mention what you'll do next

---

## ⚠️ Communication Tips

- **Tone**: Warm, curious, show genuine interest in their journey
- **Attitude**: Be authentic, appreciate their unique background
- **Address**: First names
- **Time Zone**: [Check time zone difference if remote]

---

## ✅ Pre-Chat Checklist

- [ ] Review company website and product
- [ ] Check recent LinkedIn/X posts
- [ ] Prepare 30-sec self introduction
- [ ] Set up calendar invite (consider time zones)
- [ ] Have questions ready
- [ ] Have pen and paper for notes
```

---

## Notion推送（可选）

需要 `NOTION_API_KEY` 环境变量和目标页面ID。

```bash
# Set your Notion page ID here
NOTION_PAGE_ID="YOUR_NOTION_PAGE_ID"
NOTION_KEY="${NOTION_API_KEY}"

curl -s -X PATCH "https://api.notion.com/v1/blocks/${NOTION_PAGE_ID}/children" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": "☕ Coffee Chat Playbook: [Target]"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Date: [YYYY-MM-DD]"}}]}},
      {"object": "block", "type": "divider", "divider": {}},
      {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "📋 Target Profile Summary"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "[Basic info, background, recent topics]"}}]}},
      {"object": "block", "type": "divider", "divider": {}},
      {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🏢 Company & Industry Research"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "[Funding, location, team, product, industry landscape]"}}]}},
      {"object": "block", "type": "divider", "divider": {}},
      {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "👥 Founder Deep Dive"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "[Background, work history, achievements, philosophy]"}}]}},
      {"object": "block", "type": "divider", "divider": {}},
      {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "📱 Recent Content & Posts"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "[LinkedIn posts + X activity]"}}]}},
      {"object": "block", "type": "divider", "divider": {}},
      {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🔍 You vs Target"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "[Common ground and conversation starters]"}}]}},
      {"object": "block", "type": "divider", "divider": {}},
      {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "💬 Questions (8)"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "[8 questions: 3 personal, 3 work, 2 industry]"}}]}},
      {"object": "block", "type": "divider", "divider": {}},
      {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🗣️ Talking Points (4)"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "[4 talking points]"}}]}},
      {"object": "block", "type": "divider", "divider": {}},
      {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "⚠️ Tips & ✅ Checklist"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "[Communication tips and pre-chat checklist]"}}]}}
    ]
  }'
```

---

## 质量标准

1. **务必包含公司与行业调研**——包括融资情况、产品信息、竞争对手及行业趋势
2. **务必包含创始人背景分析**——针对初创公司，深入了解每位创始人的背景
3. **务必包含最新内容**——包括LinkedIn帖子和X平台上的动态
4. **务必对比个人资料**——找出您与目标人物之间的共同点
5. **生成8个具体问题**——3个关于个人经历、3个关于工作、2个关于行业的问题
6. **生成4个讨论要点**——展示您已做好充分准备
7. **务必进行本地保存**——将文件保存为 `memory/coffee-chat-{target-slug}-{YYYY-MM-DD}.md`
8. **推送到Notion**（如果已配置 `NOTION_API_KEY`）
9. **问题要具体**——根据目标人物的背景、帖子和公司动态来设计问题

---

## 已知限制

### LinkedIn数据抓取
- LinkedIn的数据抓取工具经常返回错误信息
- 在免费Apify tier下，LinkedIn个人资料抓取可能会失败
- **解决方法**：使用网页搜索获取公司/创始人信息，并在X平台上查看最新帖子

### 个人资料缓存
- 保存位置：`memory/my-profile.md`
- 如果缓存缺失，请在继续之前要求用户提供相关信息

### Notion
- 需要 `NOTION_API_KEY` 环境变量
- 在上述Notion推送部分设置您的页面ID
- Notion API版本：`2022-06-28`