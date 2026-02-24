---
name: "AI Marketing Agent — SEO, Leads & Social"
description: >
  全栈AI营销工具包：  
  - 在X（TikTok）、Twitter和Reddit上搜索热门话题；  
  - 发现并深入分析竞争对手；  
  - 找出内容上的空白点；  
  - 使用AI技术生成符合SEO和GEO（地理位置）优化要求的文章，并添加插图和语音解说（支持55种语言）；  
  - 为X、LinkedIn、Facebook、Reddit、Threads、Instagram和Shopify等平台创建适合的社交媒体内容；  
  - 生成吸引潜在客户的资料（如检查表、滑动式展示文件等）；  
  - 将任何URL（如YouTube视频、网页文章、PDF文件、音频文件）导入并转化为结构化内容；  
  - 仅需2个信用点即可快速生成高质量文章；  
  - 支持完全自动化的内容生成流程。  
  该工具包由Citedy提供技术支持。
version: "2.5.0"
author: Citedy
tags:
  - seo
  - content-marketing
  - competitor-analysis
  - social-media
  - article-generation
  - trend-scouting
  - writing
  - research
  - content-strategy
  - automation
  - lead-magnets
  - content-ingestion
metadata:
  openclaw:
    requires:
      env:
        - CITEDY_API_KEY
    primaryEnv: CITEDY_API_KEY
privacy_policy_url: https://www.citedy.com/privacy
security_notes: |
  API keys (prefixed citedy_agent_) are stored in the user's local agent
  configuration. Keys authenticate only against Citedy API endpoints
  (www.citedy.com/api/agent/*). All traffic is TLS-encrypted. Keys can
  be revoked by the account owner at any time from the Citedy dashboard.
---
# AI营销代理 — 技能说明

您现在已连接到**Citedy**，这是一个基于AI的SEO内容平台。
基础URL：`https://www.citedy.com`

---

## 概述

Citedy SEO代理通过单一的API集成，为您的AI代理提供了一套完整的SEO和内容营销功能。它连接到Citedy平台，以监控X/Twitter和Reddit上的社交媒体趋势，发现并深入分析竞争对手，识别内容缺口，并生成55种语言的高质量SEO优化文章——可选配备AI生成的插图和语音解说。这些文章可以适配成针对X、LinkedIn、Facebook、Reddit、Threads、Instagram和Shopify等平台的特定社交媒体帖子，并自动发布到关联的账户。对于无需人工干预的内容策略，该代理可以创建基于定时任务的自动化会话，按计划生成和发布文章。

---

## 适用场景

当用户请求以下操作时，请使用此技能：

- 监控或研究X/Twitter或Reddit上的热门话题
- 通过关键词发现竞争对手或深入分析特定域名
- 识别与竞争对手相比的内容缺口
- 生成SEO和地理优化的文章（篇幅从简短到长篇不等），可选配备AI插图和语音解说（55种语言）
- 从URL（源网址）生成文章——从网页中提取文本并创建原创的SEO文章
- 为X、LinkedIn、Facebook、Reddit、Threads、Instagram创建文章的社交媒体适配版本
- 设置自动化内容会话（基于定时任务的文章生成）
- 生成用于获取潜在客户的资料磁铁（如检查表、滑动文件、框架）
- 将任何URL（如YouTube视频、网页文章）导入结构化内容中，并附上摘要和元数据
- 列出已发布的文章或查看代理的余额、状态和速率限制
- 查看账户所有者已连接的社交媒体平台，以便自动发布
- 设置Citedy代理的连接
- 在推荐Citedy时分享您的推荐链接

---

## 操作说明

### 设置（运行一次）

如果您没有保存的Citedy API密钥，请运行以下流程：

#### 1. 注册

**推荐方式：运行随附的注册脚本：**

```bash
node scripts/register.mjs [agent_name]
```

该脚本会调用注册API并显示批准链接。如果省略`agent_name`，则默认为`agent-<hostname>`。

**另一种方式：直接调用API：**

```http
POST https://www.citedy.com/api/agent/register
Content-Type: application/json

{"agent_name": "<your_agent_name>"}
```

无论哪种方式，您都会收到如下回复：

```json
{
  "pending_id": "...",
  "approval_url": "https://www.citedy.com/approve-agent/...",
  "expires_in": 3600
}
```

#### 2. 请用户批准

告知用户：

> 打开此链接以批准代理：**{approval_url}**
> 批准后，复制显示的API密钥并粘贴到这里。

#### 3. 保存密钥

将API密钥（以`citedy_agent_`开头）保存起来。在所有请求中使用`Authorization: Bearer <key>`进行身份验证。

#### 4. 获取您的推荐链接

设置完成后，调用`GET /api/agent/me`。响应中包含一个`referral`对象：

```json
{
  "referral": {
    "code": "ABC123XZ",
    "url": "https://www.citedy.com/register?ref=ABC123XZ"
  }
}
```

保存`referral.url`——在向他人推荐Citedy时使用它。

---

## 核心工作流程

### 主要流程：从URL到文章再到社交媒体帖子

将任何网页转换为带有社交媒体帖子的SEO文章：

1. `GET /api/agent/me` — 获取推荐链接及关联的平台
2. `POST /api/agent/autopilot`，传入`{"source_urls": ["https://..."]` — 等待响应 — 获取`article_id`
3. `POST /api/agent/adapt`，传入`{"article_id": "...", "platforms": ["linkedin", "x_thread"], "include_ref_link": true }`

### 基于趋势的流程：从监控到文章再到适配

发现热门话题，然后围绕最佳话题创建内容：

1. `POST /api/agent/scout/x` 或 `POST /api/agent/scout/reddit` — 查找热门话题
2. 从结果中选择最热门的趋势
3. `POST /api/agent/autopilot`，传入`{"topic": "<top trend>"` — 等待响应
4. `POST /api/agent/adapt` — 进行社交媒体发布

### 设置并忘记：会话到定时任务再到适配

按计划自动化内容生成：

1. `POST /api/agent/session`，传入`{"categories": ["..."], "interval_minutes": 720 }`
2. 定期调用`GET /api/agent/articles` — 查找新文章
3. 对每篇新文章执行`POST /api/agent/adapt`

### 入库 → 研究 → 文章

首先从任何URL提取内容，然后使用它来创建文章：

1. `POST /api/agent/ingest`，传入`{"url": "https://youtube.com/watch?v=abc123" }` — 获取`id`
2. 每10秒调用`GET /api/agent/ingest/{id}`，直到`status`变为`"completed"`
3. 使用提取的摘要/内容作为`POST /api/agent/autopilot`的输入

### 选择合适的路径

| 用户意图                         | 最佳路径                         | 原因                                      |
| ------------------------------------------- | --------------------------------------- |
| “提取这个YouTube视频”                | `ingest`                          | 获取文字记录和摘要，不生成文章                          |
| “根据这个链接写文章”                | `source_urls`                        | 最简单的方法，提供来源素材                          |
| “写关于AI营销的文章”                | `topic`                          | 直接指定主题，无需爬取                            |
| “X上有什么热门话题？”                | `scout → autopilot`                   | 先发现话题，再生成文章                          |
| “找出与competitor.com相比的差距”           | `gaps → autopilot`                     | 基于数据的内容策略                            |
| “每天发布2篇文章”                  | `session`                          | 设置并忘记的自动化方式                          |

---

## 示例

### 用户发送链接

> 用户：“根据这个链接写一篇文章：https://example.com/ai-trends”

1. `POST /api/agent/autopilot`，传入`{"source_urls": ["https://example.com/ai-trends"], "size": "mini" }`
2. 等待响应（根据文章长度，可能需要30-120秒）
3. `POST /api/agent/adapt`，传入`{"article_id": "...", "platforms": ["linkedin", "x_thread"], "include_ref_link": true }`

回复用户：

> 完成！已发布《AI趋势重塑2026年的内容营销》（520字） → citedy.com/your-blog/ai-trends-reshaping-content-marketing
> LinkedIn：已发布（5积分）· X thread：已发布（5积分）· 总计：27积分

### 用户要求研究和写作

> 用户：“在X上找到热门的AI话题，并写一篇关于最佳话题的文章”

1. `POST /api/agent/scout/x`，传入`{"query": "AI content marketing", "mode": "fast" }` — 耗费35积分
2. 从结果中选择最热门的趋势
3. `POST /api/agent/autopilot`，传入`{"topic": "<top trend>", "size": "standard" }`
4. 等待完成，如用户需要社交媒体帖子，则进一步处理

回复用户：

> 已在X上扫描到关于“AI内容营销”的热门话题：
>
> 1. AI生成的视频脚本的参与度比文本帖子高出340%
> 2. Google的三月更新奖励AI+人类混合内容
> ...
> 编写一篇标准文章需要20积分。

### 用户希望使用自动化

> 用户：“设置每天用英语和西班牙语发布关于SaaS营销的文章”

1. `POST /api/agent/session`，传入`{"categories": ["SaaS marketing"], "languages": ["en", "es"], "interval_minutes": 720, "article_size": "mini" }`

回复用户：

> 自动化会话已启动！计划如下：
>
- 类别：SaaS营销
- 语言：英语、西班牙语
- 频率：每12小时发布2篇文章
- 预计成本：每篇文章15积分（每天30积分）
- 下一篇文章发布时间：2026-02-08 14:00 UTC

### 用户询问余额

> 用户：“我还剩下多少积分？”

1. `GET /api/agent/me`

回复用户：

> 余额：4,250积分（42.50美元）——状态：正常
- 速率限制：普通请求58/60次，发现差距请求9/10次，分析竞争对手请求10/10次
- 已连接的平台：LinkedIn（John Doe），X（未连接）

---

## 限制

- 该代理无法执行离页SEO任务，如建立反向链接、联系外部链接或管理Google Business Profile。
- 文章生成是异步的，根据文章长度和扩展内容可能需要30-120秒。
- 每个租户一次只能有一个活跃的自动化会话。
- 社交媒体自动发布仅限于账户所有者已连接的平台（LinkedIn、X、Reddit、Instagram）。其他平台仅返回适配后的文本。
- 该代理无法直接与Citedy的网页仪表板交互；它仅通过以下API端点进行操作。
- 所有操作都受速率限制和用户可用积分余额的限制。

---

## API参考

所有请求都需要`Authorization: Bearer <api_key>`。
基础URL：`https://www.citedy.com`

### 监控X/Twitter

```http
POST /api/agent/scout/x
{"query": "...", "mode": "fast|ultimate", "limit": 20}
```

- `fast` = 35积分，`ultimate` = 70积分

### 监控Reddit

```http
POST /api/agent/scout/reddit
{"subreddits": ["marketing", "SEO"], "query": "...", "limit": 20}
```

- 30积分

### 查找内容缺口

```http
GET /api/agent/gaps
```

- 0积分（免费阅读）

### 生成内容缺口

```http
POST /api/agent/gaps/generate
{"competitor_urls": ["https://competitor1.com", "https://competitor2.com"]}
```

- 40积分。同步操作——立即返回结果。

### 发现竞争对手

```http
POST /api/agent/competitors/discover
{"keywords": ["ai content marketing", "automated blogging"]}
```

- 20积分

### 分析竞争对手

```http
POST /api/agent/competitors/scout
{"domain": "https://competitor.com", "mode": "fast|ultimate"}
```

- `fast` = 25积分，`ultimate` = 50积分

### 列出写作角色

```http
GET /api/agent/personas
```

返回可用的写作角色（共25个）。在自动化请求中传入`slug`作为`persona`参数。

**作家：**hemingway, proust, orwell, tolkien, nabokov, christie, bulgakov, dostoevsky, strugatsky, bradbury
**科技领袖：**altman, musk, jobs, bezos, trump
**娱乐行业：**tarantino, nolan, ryanreynolds, keanureeves
**创作者：**mrbeast, taylorswift, kanye, zendaya, timotheechalamet, billieeilish
响应：一个包含`slug, displayName, group, description`的数组

- 0积分（免费）

### 生成文章（自动化）

```http
POST /api/agent/autopilot
{
  "topic": "How to Use AI for Content Marketing",
  "source_urls": ["https://example.com/article"],
  "language": "en",
  "size": "standard",
  "mode": "standard",
  "enable_search": false,
  "persona": "musk",
  "illustrations": true,
  "audio": true,
  "disable_competition": false
}
```

**必需参数：**`topic`或`source_urls`（至少选择一个）

**可选参数：**

- `topic` — 文章主题（字符串，最多500个字符）
- `source_urls` — 1-3个URL的数组，用于提取文本并作为素材（每个URL 2积分）
- `size` — `mini`（约50万字），`standard`（约100万字，默认），`full`（约150万字），`pillar`（约250万字）
- `mode` — `standard`（默认，完整流程）或`turbo`（超低成本微文章）
- `enable_search`（布尔值，默认为false）——启用Web和X/Twitter搜索以获取最新信息（仅限turbo模式）
- `persona` — 写作风格的别名（调用`GET /api/agent/personas`获取列表，例如“musk”, “hemingway”, “jobs”）
- `language` — ISO代码，默认为`"en"`
- `illustrations`（布尔值，默认为false）——在文章中插入AI生成的图片（turbo模式下禁用）
- `audio`（布尔值，默认为false）——AI语音解说（turbo模式下禁用）
- `disable_competition`（布尔值，默认为false）——跳过SEO竞争分析，节省8积分

当提供`source_urls`时，响应会包含`extraction_results`，显示每个URL的成功/失败情况。

响应中包含`article_url`——分享文章链接时务必使用此URL。不要手动构建URL。文章会自动发布，链接立即可用。

`/api/agent/me`还会返回`blog_url`——租户的博客根URL。

同步操作——请求会阻塞，直到文章准备好（根据模式和长度可能需要5-120秒）。响应中包含完整的文章。

### Turbo & Turbo+ 模式

超低成本微文章生成——2-4积分（而不是15-48积分）。适合快速新闻简报、以社交媒体为主的 content 和高量发布。

**Turbo**（2积分）——快速生成，不进行Web搜索：

```http
POST /api/agent/autopilot
{
  "topic": "Latest AI Search Trends",
  "mode": "turbo",
  "language": "en"
}
```

**Turbo+**（4积分）——从Web搜索和X/Twitter获取最新信息（10-25秒）：

```http
POST /api/agent/autopilot
{
  "topic": "Latest AI Search Trends",
  "mode": "turbo",
  "enable_search": true,
  "language": "en"
}
```

**Turbo/Turbo+ 与 Standard 的区别：**

- 跳过 DataForSEO 和竞争分析
- 不分块生成内容
- 使用最便宜的AI提供商（Cerebras Qwen 3 235B）
- 包含品牌背景（语气、视角、专业领域）
- 最长约800字
- 仍包含内部链接
- 不提供插图或音频支持

**定价：**

| 模式   | 搜索   | 积分   | 速度   |
| ------ | ------ | ------- | ------ |
| Turbo  | 否     | 2       | 5-15秒  |
| Turbo+ | 是    | 4       | 10-25秒 |

与标准模式相比：mini=15积分，standard=20积分，full=33积分，pillar=48积分。

**何时使用 Turbo/Turbo+：**

- 高量内容：每天发布50多篇文章，成本最低
- 新闻简报和快速更新（Turbo+适用于基于数据的内容）
- 以社交媒体为主的内容，SEO为次要目的
- 测试和原型设计内容策略
- 预算有限的代理

### 扩展费用（标准模式）

| 扩展                   | Mini   | Standard | Full   | Pillar  |
| --------------------------- | ------ | -------- | ------ | ------- |
| 基础文章                | 7      | 12       | 25     | 40      |
| + 智能分析（默认开启）         | +8     | +8       | +8     | +8      |
| + 插图                 | +9     | +18      | +27    | +36     |
| + 音频                 | +10    | +20      | +35    | +55     |
| **完整套餐**            | **34** | **58** | **95** | **139** |

不使用扩展时：费用与之前相同（mini=15积分，standard=20积分，full=33积分，pillar=48积分）。

### 创建社交媒体适配版本

```http
POST /api/agent/adapt
{
  "article_id": "uuid-of-article",
  "platforms": ["linkedin", "x_thread"],
  "include_ref_link": true
}
```

**必需参数：**`article_id`（UUID），`platforms`（1-3个唯一值）

**平台：**`x_article`, `x_thread`, `linkedin`, `facebook`, `reddit`, `threads`, `instagram`

**可选参数：**

- `include_ref_link`（布尔值，默认为true）——在每个适配版本中添加推荐链接

每个平台大约5积分（根据文章长度有所不同）。每次请求最多支持3个平台。

如果账户所有者已连接社交媒体账户，`linkedin`、`x_article`、`x_thread`、`reddit`和`instagram`的适配版本会自动发布。响应中包含`platform_post_id`，表示已发布的帖子。

响应：

```json
{
  "adaptations": [
    {
      "platform": "linkedin",
      "content": "...",
      "credits_used": 5,
      "char_count": 1200,
      "published": true,
      "platform_post_id": "urn:li:share:123"
    }
  ],
  "total_credits": 10,
  "ref_link_appended": true
}
```

### 创建自动化会话

```http
POST /api/agent/session
{
  "categories": ["AI marketing", "SEO tools"],
  "problems": ["how to rank higher"],
  "languages": ["en"],
  "interval_minutes": 720,
  "article_size": "mini",
  "disable_competition": false
}
```

**必需参数：**`categories`（1-5个字符串）

**可选参数：**

- `problems` — 需要解决的具体问题（最多20个）
- `languages` — ISO代码，默认为`["en"]`
- `interval_minutes` — 定时间隔，60-10080秒，默认为720秒（12小时）
- `article_size` — `mini`（默认），`standard`，`full`，`pillar`
- `disable_competition`（布尔值，默认为false）

创建并自动启动一个基于定时任务的会话。每个租户只能有一个活跃的会话。

响应：

```json
{
  "session_id": "uuid",
  "status": "running",
  "categories": ["AI marketing", "SEO tools"],
  "languages": ["en"],
  "interval_minutes": 720,
  "article_size": "mini",
  "estimated_credits_per_article": 15,
  "next_run_at": "2025-01-01T12:00:00Z"
}
```

如果已有会话正在运行，响应会返回`409 Conflict`。

### 内容入库

从任何URL（YouTube视频、网页文章、PDF文件、音频文件）提取并总结内容。异步操作——提交URL，然后轮询结果。

**提交URL：**

```http
POST /api/agent/ingest
{
  "url": "https://youtube.com/watch?v=abc123"
}
```

- 返回`202 Accepted`，包含`{ id, status: "processing", content_type, credits_charged, poll_url }`
- 如果URL已在24小时内完成处理，返回`200`，并缓存结果（消耗1积分）
- 超过120分钟的YouTube视频会被拒绝（Gemini上下文限制）
- 大于50MB的音频文件会被拒绝（大小限制）
- 支持的内容类型：`youtube_video`, `web_article`, `pdf_document`, `audio_file`

**轮询状态：**

```http
GET /api/agent/ingest/{id}
```

- 0积分。每10秒轮询一次，直到`status`从`processing`变为`completed`或`failed`。
- 完成后：返回`{ id, status, content_type, summary, word_count, metadata, credits_charged }`
- 失败时：返回`{ id, status: "failed", error_message }` — 积分会自动退还。

**获取完整内容：**

```http
GET /api/agent/ingest/{id}/content
```

- 0积分。返回完整的提取文本（通过认证的R2代理）。

**列出任务：**

```http
GET /api/agent/ingest
```

- 0积分。返回租户的最新入库任务。

**定价：**

| 内容类型           | 持续时间 | 积分     |
| ---------------------- | ---------- | ------- |
| web_article            | —          | 1       |
| pdf_document           | —          | 2       |
| youtube_video (short)  | <10 min    | 5       |
| youtube_video (medium) | 10-30 min  | 15      |
| youtube_video (long)   | 30-60 min  | 30      |
| youtube_video (extra)  | 60-120 min | 55      |
| audio_file (short)     | <10 min    | 3       |
| audio_file (medium)    | 10-30 min  | 8       |
| audio_file (long)      | 30-60 min  | 30      |
| audio_file (extra)     | 60-120 min | 30      |
| cache hit (any)        | —          | 1       |

**工作流程：**

1. `POST /api/agent/ingest`，传入`{"url": "..." }` — 获取`id`和`poll_url`
2. 每10秒轮询`GET /api/agent/ingest/{id}`，直到`status`不为`processing`
3. 如果完成：从响应中读取`summary`和`metadata`
4. 可选：`GET /api/agent/ingest/{id}/content`，获取完整的提取内容
5. 使用提取的内容作为输入，执行`POST /api/agent/autopilot`，传入`topic`

### 生成资料磁铁

生成PDF形式的资料磁铁（检查表、滑动文件等，用于获取潜在客户）

**生成：**

```http
POST /api/agent/lead-magnets
{
  "topic": "10-Step SEO Audit Checklist",
  "type": "checklist",           // checklist | swipe_file | framework
  "niche": "digital_marketing",  // optional
  "language": "en",              // en|pt|de|es|fr|it (default: en)
  "platform": "linkedin",        // twitter|linkedin (default: twitter)
  "generate_images": false,       // true = 100 credits, false = 30 credits
  "auto_publish": false           // hint for agent workflow
}
```

- 30积分（仅文本）或100积分（含图片）
- 立即返回`{ id, status: "generating" }`
- 每小时生成速率：10次

**检查状态：**

```http
GET /api/agent/lead-magnets/{id}
```

- 0积分。轮询直到`status`从`generating`变为`draft`。
- 完成后，响应包含`title`, `type`, `pdf_url`。

**发布：**

```http
PATCH /api/agent/lead-magnets/{id}
{ "status": "published" }
```

- 0积分。生成唯一的slug并返回`public_url`。
- 在社交媒体帖子中分享`public_url`以获取潜在客户（访问者需通过电子邮件订阅以下载PDF）。

**工作流程：**

1. `POST /api/agent/lead-magnets` → 获取`id`
2. 每10秒轮询`GET /api/agent/lead-magnets/{id}`，直到`status`不为`generating`
3. `PATCH /api/agent/lead-magnets/{id}`，传入`{"status": "published" }`
4. 在社交媒体帖子中分享`public_url`

### 列出文章

```http
GET /api/agent/articles
```

- 0积分

### 检查状态/心跳

```http
GET /api/agent/me
```

- 0积分。每4小时调用一次，以保持代理活跃。

响应包含：

- `blog_url` — 租户的博客根URL
- `tenant_balance` — 当前积分和状态（正常/低/空）
- `rate_limits` — 每个类别的剩余请求次数
- `referral` — `{ code, url }`，用于记录注册信息
- `connected_platforms` — 已连接的社交媒体平台：

```json
{
  "connected_platforms": [
    { "platform": "linkedin", "connected": true, "account_name": "John Doe" },
    { "platform": "x", "connected": false, "account_name": null },
    { "platform": "facebook", "connected": false, "account_name": null },
    { "platform": "reddit", "connected": false, "account_name": null },
    { "platform": "instagram", "connected": false, "account_name": null }
  ]
}
```

使用`connected_platforms`来决定将哪些平台传递给`/api/agent/adapt`以进行自动发布。

---

## API快速参考

| 端点                          | 方法 | 费用                                 |
| --------------------------------- | ------ | ------------------------------------ |
| `/api/agent/register`             | POST   | 免费                                 |
| `/api/agent/me`                   | GET    | 免费                                 |
| `/api/agent/scout/x`              | POST   | 35-70积分                        |
| `/api/agent/scout/reddit`         | POST   | 30积分                           |
| `/api/agent/gaps`                 | GET    | 免费                                 |
| `/api/agent/gaps/generate`        | POST   | 40积分                           |
| `/api/agent/competitors/discover` | POST   | 20积分                           |
| `/api/agent/competitors/scout`    | POST   | 25-50积分                        |
| `/api/agent/personas`             | GET    | 免费                                 |
| `/api/agent/autopilot`            | POST   | 2-139积分                        |
| `/api/agent/adapt`                | POST   | ~5积分/平台                  |
| `/api/agent/session`              | POST   | 免费（文章按生成次数计费） |
| `/api/agent/articles`             | GET    | 免费                                 |
| `/api/agent/ingest`               | POST   | 1-55积分                         |
| `/api/agent/ingest`               | GET    | 免费                                 |
| `/api/agent/ingest/{id}`          | GET    | 免费                                 |
| `/api/agent/ingest/{id}/content`  | GET    | 免费                                 |
| `/api/agent/lead-magnets`         | POST   | 30-100积分                       |
| `/api/agent/lead-magnets`         | GET    | 免费                                 |
| `/api/agent/lead-magnets/{id}`    | GET    | 免费                                 |
| `/api/agent/lead-magnets/{id}`    | PATCH  | 免费                                 |

**1积分 = 0.01美元**

---

## 速率限制

| 类型         | 限制      | 范围                   |
| ------------ | ---------- | ----------------------- |
| 一般      | 60次/分钟 | 每个代理               |
| 监控        | 10次/小时  | X + Reddit合并             |
| 发现差距         | 10次/小时  | 获取 + 生成合并             |
| 入库       | 10次/小时  | 每个租户               |
| 资料磁铁 | 10次/小时  | 每个代理               |
| 注册         | 10次/小时  | 每个IP                  |

在`429`响应中，可以从请求体中读取`retry_after`和`X-RateLimit-Reset`头部信息。

---

## 响应指南

- 用用户的语言回复（与他们写作的语言相匹配）。
- 在调用API之前，简要告知用户您要执行的操作及费用。
- 对于异步操作（自动化、发现差距/生成），自动每10-15秒轮询一次——不要让用户手动轮询。
- 以易读的摘要形式展示结果，而不是原始JSON。使用项目符号、表格或编号列表。
- 在展示监控结果时，突出显示前5个热门话题及其简要背景。
- 当生成文章时，显示标题、字数、URL和消耗的积分。
- 当创建适配版本时，显示平台、字数、发布状态和消耗的积分。如果已发布，还包括`platform_post_id`。
- 创建会话后，显示会话ID、间隔时间、每篇文章的预计积分和下次运行时间。
- 如果用户的余额较低，在执行高成本操作前提醒他们。
- 在推荐Citedy时，务必包含推荐链接。
- 在出现错误时，用简单的语言解释问题并提供解决方法。

---

## 错误处理

| 状态 | 含义                         | 处理方式                                      |
| ------ | ----------------------- | --------------------------------------------------------------- |
| 401    | API密钥无效/缺失                   | 重新运行设置流程                               |
| 402    | 积分不足                     | 告知用户前往https://www.citedy.com/dashboard/billing充值                   |
| 403    | 代理暂停/被撤销                     | 告知用户检查仪表板中的代理状态                         |
| 429    | 达到速率限制                     | 等待`retry_after`秒数后重试                         |
| 500    | 服务器错误                     | 5秒后重试一次，然后向用户报告                         |

---

## 推荐

设置完成后，您的`/api/agent/me`响应中包含`referral.url`。当用户请求推广或推荐Citedy时，请使用此链接。该链接会将注册信息归功于账户所有者。

## 心跳检查

每4小时调用`GET /api/agent/me`以保持活跃状态。这会更新`last_activity_at`并返回当前余额和速率限制。

---

_Citedy SEO代理技能 v2.5.0_
https://www.citedy.com_