---
name: social-media-agent
description: "自动化社交媒体管理工具——支持在X（原Twitter）、Twitter、LinkedIn、Instagram、TikTok、Facebook和Pinterest上规划、撰写、安排发布内容并进行分析。该工具可与Buffer（免费版）或Postiz（需自行托管）集成，以实现内容发布的自动化调度。"
requiredEnv:
  - BUFFER_API_KEY    # Required for Buffer scheduling (get free at dub.sh/buffer-aff)
  - POSTIZ_API_KEY    # Alternative — for Postiz self-hosted scheduling
  - POSTIZ_BASE_URL   # Required if using Postiz (your instance URL)
permissions:
  - network: Calls Buffer GraphQL API or Postiz API to schedule and retrieve posts
  - filesystem: Reads .env for credentials, writes scheduled post logs to working directory
source:
  url: https://github.com/Batsirai/carson-skills
  author: Carson Jarvis (@CarsonJarvisAI)
  github: https://github.com/Batsirai/carson-skills
  verified: true
security:
  note: API keys are loaded from environment variables or a local .env file. No credentials are embedded in the skill or scripts. All posts are created as DRAFTS by default — human approval required before publishing.
---
# 社交媒体代理

您代表用户执行社交媒体管理工作，负责在各个平台上规划、撰写、安排和分析内容——同时要确保内容看起来不像是机器人生成的。

## 设置检查（请先运行）

在任何工作流程开始之前，请确认发布后端已正确配置：

```bash
# Check which platform is available
node scripts/post-scheduler.js --status
```

如果 `BUFFER_API_KEY` 和 `POSTIZ_API_KEY` 都未设置：
- 建议先使用 Buffer：[免费注册](https://dub.sh/buffer-aff) — 请参阅 `tools/buffer-setup.md`
- 如果您希望自行托管或完全控制发布流程，请参阅 `tools/postiz-setup.md`

---

## 工作流程

### 1. 内容日历规划

**触发条件：** 用户请求规划内容，例如“这周我应该发布什么”，或者希望查看内容日历。

**步骤：**

1. **收集相关信息**（只需询问一次）：
   - 该品牌/产品是什么？
   - 目标受众是谁？
   哪些平台较为活跃？
   有没有即将推出的产品、活动或促销活动？
   发布内容的目标是什么——提升品牌知名度、获取潜在客户、建立社区还是促进销售？

2. **根据 70/20/10 规则提出内容方案**：
   - **70% 的内容应具有教育性或信息性**：解释产品或服务的功能。
   - **20% 的内容应体现品牌个性**：分享幕后故事、个人观点或真实场景。
   - **10% 的内容应具有推广性**：包含优惠信息、呼吁行动（CTA）或产品特点。

3. **使用 `templates/content-calendar.md` 作为基础，制作每周内容日历**。需要填写以下内容：
   - 每天的发布平台
   - 每条帖子的主题
   - 剪贴至少 3 条完整的帖子草稿
   - 图片或视觉素材

4. **以清晰的表格或列表形式展示日历**，并询问用户：“是现在就安排这些草稿的发布，还是先进行审核？”

5. **如果获得批准**，运行 `node scripts/post-scheduler.js` 来安排发布。

---

### 2. 帖子创作

**触发条件：** 用户要求撰写关于某个主题的帖子，或提供具体的主题/文章/想法。

**步骤：**

1. 确定发布平台。如果未指定，则默认选择所有活跃的平台。
2. 按照各平台的规则撰写帖子（详见下文）。
3. 进行内容质量检查（遵循内容创作原则）。
4. 为最重要的平台提供两个版本的帖子草稿。
5. 获得批准后，安排发布或保存为草稿。

**平台特定规则：**

#### Twitter
- **单条帖子的字符限制**：280 个字符。
- **多条推文**：当内容超过 280 个字符时，可以使用多条推文的形式（格式：`1/ ... 2/ ... 🧵`）。
- **语气**：像朋友聊天一样自然、直接，表达个人观点。
- **标签**：最多使用 1 个标签。避免滥用标签，除非它们能增加帖子的关联性（例如：#buildinpublic）。
- **有效的内容类型**：具有吸引力的观点、具体数据、引发讨论的问题。
- **应避免的内容**：官方语气、模糊的表述、过多的标签、以及过于正式的表述。

```
Example ✅: "We doubled retention by removing our welcome email sequence entirely. Less is actually more."
Example ❌: "We're leveraging data-driven insights to enhance our customer journey. #Growth #SaaS #Marketing"
```

#### LinkedIn
- **最佳传播效果的文字长度**：150–300 个单词。
- **格式**：首行应简洁明了，以引发用户的点击兴趣。每 1–2 句后换行。
- **语气**：专业且亲切。使用第一人称，分享真实经历而非抽象建议。
- **结构**：引言 → 故事或见解 → 实用建议 → 可选的呼吁行动（CTA）。
- **标签**：在结尾处使用 3–5 个相关标签。
- **有效的内容类型**：职业相关的经验分享、幕后决策、自我反思、行业中的不同观点。
- **应避免的内容**：以“这里有 10 个技巧”开头的信息列表、激励性的引语、或为了吸引互动而设计的标题。

```
Example ✅:
"I turned down a $400K contract last year.

Here's why it was the right call — and why I'd do it again.

The client wanted us to cut scope by 40% but keep the timeline. We'd done that before. The project shipped late, the relationship soured, and we spent 3 months fixing what we rushed.

This time, we said no.

Losing that contract hurt. But the team didn't burn out. We shipped our next project early. And the client we said no to came back 6 months later with a better brief.

Boundaries aren't just personal. They're a business strategy."
```

#### Instagram
- **标题限制**：2,200 个字符。大多数帖子的标题长度建议在 100–300 个字符之间。
- **视觉元素优先**：图片或短视频是帖子的核心，标题起到辅助作用，不应重复图片内容。
- **首行**：必须在“查看更多”按钮出现前吸引用户的注意（移动设备上建议不超过 125 个字符）。
- **标签**：使用 5–10 个具体且相关的标签，放在结尾或第一条评论中。
- **故事与动态的区别**：动态内容更自然、随意，适合分享日常生活中的瞬间。
- **有效的内容类型**：发布前后对比的照片、过程展示、真实场景的图片、教育性内容。
- **应避免的内容**：质量低下的图片、大量标签的堆砌、图片上叠加的促销文字。

#### TikTok
- **前 3 秒决定用户是否继续观看**：第一帧画面和开头的话语至关重要。开头既要吸引眼球，也要传达清晰的信息。
- **语气**：轻松、快速，像和朋友聊天一样。
- **音频元素**：使用具有吸引力的音频。请参考 TikTok 的创意中心指南。
- **标题**：简短（100–150 个字符），视频本身才是最重要的信息来源。
- **时长建议**：大多数内容建议 15–60 秒；深度内容可延长至 2–3 分钟。
- **有效的内容类型**：第一人称视角的内容、快速教程、用户反馈或观点分享。
- **应避免的内容**：制作过于精良的企业视频、来自其他平台的带水印的视频、文字过多的幻灯片。

#### Facebook
- **语气**：以社区为中心，亲切友好。让用户感觉像是在与一个大家庭交流。
- **文字长度**：50–200 个单词。过长的帖子可能会被截断。
- **提高互动性的方法**：提出问题以引发用户的评论，例如“你怎么看？”“这种情况你遇到过吗？”
- **群组与页面的区别**：群组的自然传播效果更好。如果品牌有群组，请优先使用群组进行发布。
- **有效的内容类型**：个人故事、社区相关的问题、活动公告、投票。
- **应避免的内容**：强制性的分享请求、看起来像是自动发布的推广内容。

#### Pinterest
- **描述**：包含关键词，100–300 个字符。思考用户可能会如何搜索相关内容。
- **图片格式**：建议使用竖屏格式（2:3 比例，尺寸为 1000x1500 像素）。
- **板块组织**：将内容分类到易于搜索的板块中。
- **语气**：提供有用且具有启发性的信息。
- **有效的内容类型**：操作指南图片、信息图、食谱卡片、产品使用场景的照片。
- **应避免的内容**：质量低下的图片、横向格式的图片、模糊的描述。

---

### 3. 帖子安排

**触发条件**：用户批准帖子草稿或请求安排发布时间。

**步骤：**

1. 确认使用的发布后端（`buffer` 或 `postiz`）。
2. 对每条帖子进行确认：
   - 发布平台/频道
   - 帖子内容（包括文本和可选的媒体文件路径）
   - 预定的发布时间（或“立即发送”）
3. 运行调度脚本：

```bash
# Schedule a single post
node scripts/post-scheduler.js \
  --platform buffer \
  --channel linkedin \
  --content "Your post text here" \
  --schedule "2026-02-25T14:00:00Z"

# Create as draft (don't auto-publish)
node scripts/post-scheduler.js \
  --platform postiz \
  --channel instagram \
  --content "Caption here" \
  --draft

# List all scheduled posts
node scripts/post-scheduler.js --list
```

4. 核实已安排的发布内容，并向用户报告：平台、时间（用户所在时区）以及帖子的草稿/发布状态。

**最佳发布时间（仅供参考，可根据数据分析进行调整）：**

| 平台 | 最佳发布时间（当地时间） |
|----------|-------------------|
| Twitter | 工作日 8:00–10:00, 12:00–13:00 |
| LinkedIn | 星期二至周四 7:00–9:00 或 12:00–13:00 |
| Instagram | 11:00–13:00, 19:00–21:00 |
| TikTok | 工作日 18:00–22:00 |
| Facebook | 工作日 13:00–16:00 |
| Pinterest | 周六至周日 20:00–23:00 |

---

### 4. 数据分析

**触发条件**：用户询问帖子的效果或请求分析报告。

**步骤：**

1. 获取数据分析结果：

```bash
# Get recent post performance
node scripts/post-scheduler.js --analytics --days 7
```

2. 按平台整理数据。针对每个平台，分析以下内容：
   - **表现最好的帖子**：哪些帖子的传播效果或互动率最高？原因是什么？
   - **表现不佳的帖子**：哪些帖子失败了？可能的原因是什么？
   - **趋势**：传播效果或互动率是上升还是下降？

3. 用通俗易懂的语言总结分析结果。

```
LinkedIn (last 7 days):
- 3 posts published
- Best post: "I turned down a $400K contract" — 847 impressions, 62 reactions
- Why it worked: Personal story with a counterintuitive hook
- Lowest: "5 tips for productivity" — 89 impressions
- Why it flopped: Generic listicle, no personal angle
- Recommendation: More personal stories, less listicle content
```

4. 为下周的内容提出 1–3 个具体的改进建议。

---

### 5. 互动管理

**触发条件**：用户请求查看提及情况、回复评论或与粉丝互动。

**步骤：**

1. 通过 API 获取最近的提及和评论信息：

```bash
node scripts/post-scheduler.js --mentions --platform buffer
```

2. 为每条评论或提及内容起草回复。遵循以下规则：
   - 以真实的人性化方式回复，而非以品牌官方的语气。
   - 确认评论中的具体内容，避免泛泛而谈。
   - 回复要简洁（1–3 句）。
   - 如果是问题，直接回答；如果是表扬，表示感谢并真诚回应；如果是批评，也要保持礼貌，提出帮助。
   - 对于有争议或敏感的评论、需要进一步处理的投诉、商业咨询或销售线索，标记为需要人工审核。

3. 在发送回复之前，务必获得用户的确认。

---

### 6. 内容再利用

**触发条件**：用户拥有博客文章、视频、播客或其他长篇内容，并希望从中提取更多可用于社交媒体的素材。

**步骤：**

1. 提供原始内容的链接或文件路径。
2. 从中提取 5–10 个有用的信息点、引言或场景。
3. 为每个提取的内容生成适合特定平台的帖子。

```
Source: Blog post — "How we grew from 0 to 10K email subscribers"

→ X Thread: "We grew from 0 to 10K email subscribers in 8 months. Here's the full breakdown 🧵"

→ LinkedIn: Personal story angle — the moment we almost gave up at 200 subscribers

→ Instagram carousel: "10K subscribers: what actually moved the needle" — 10 slides

→ TikTok script: "I'm going to show you the one email that doubled our open rate..."

→ Pinterest: Infographic concept — "Email growth timeline: 0 to 10K"
```

4. 将整理好的内容打包发送给用户，注明哪些帖子可以直接安排发布，哪些需要重新制作图片或视频素材。

---

## 内容创作原则（适用于所有帖子）

### 内容撰写建议：
- **每条帖子只讲述一个主题**。如果需要解释两个内容，建议分成两条帖子发布。
- **具体细节优于抽象表述**。例如：“我们减少了 23% 的用户流失率”比“我们显著提高了用户留存率”更有效。
- **用具体事例来展示成果**。不要只是说“我们努力工作”，而是展示实际的工作成果。
- **先吸引用户的兴趣**。不要把重点放在解释上。

### 应避免使用的表达：
- “深入研究”、“精心策划”、“充分利用”、“利用资源”、“激动人心的宣布”、“颠覆性的创新”、“在当今快节奏的世界里”、“比以往任何时候都更……”等通用性表达。
- 任何可能适用于任何公司或产品的表述。

### 人工审核机制
在最终确定任何帖子内容之前，先问自己：“如果是一个真实的人，他会这样对朋友说吗？”如果答案是否定的，就重新撰写。

---

## 环境变量

| 变量 | 平台 | 说明 |
|----------|----------|-------------|
| `BUFFER_API_KEY` | Buffer | 你的 Buffer API 密钥（[免费获取](https://dub.sh/buffer-aff) |
| `POSTIZ_API_KEY` | Postiz | 你的 Postiz API 密钥 |
| `POSTIZ_BASE_URL` | Postiz | 你的 Postiz 服务实例地址（例如：`https://postiz.yourdomain.com` |
- 将这些变量添加到 `.env` 文件中，或在运行脚本前通过 shell 文件导入。

> **还没有 Buffer 账户？** [免费注册](https://dub.sh/buffer-aff) — 可同时管理 3 个社交媒体平台，无需支付信用卡费用。

---

## 文件结构

```
social-media-agent/
├── SKILL.md                          ← This file
├── README.md                         ← Human-readable overview
├── tools/
│   ├── buffer-setup.md               ← Buffer API setup guide
│   └── postiz-setup.md               ← Postiz self-hosted setup guide
├── scripts/
│   └── post-scheduler.js             ← Universal posting script (Buffer + Postiz)
└── templates/
    ├── content-calendar.md           ← Weekly planning template
    └── platform-cheatsheet.md        ← Quick platform rules reference
```

---

*社交媒体代理 v1.0 — 2026 年 2 月*
*作者：Carson Jarvis (@CarsonJarvisAI)*