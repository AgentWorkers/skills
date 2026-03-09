---
name: citedy-trend-scout
title: "Trend & Intent Scout"
description: 了解您的受众当前正在搜索的内容——在 X（Twitter）、Twitter 和 Reddit 上搜索热门话题，发现并深入分析竞争对手，找出内容上的空白点。将社交信号与 SEO 智能相结合。由 Citedy 提供支持。
version: "1.0.0"
author: Citedy
tags:
  - trend-scouting
  - seo
  - competitor-analysis
  - content-gaps
  - twitter
  - reddit
  - research
  - market-research
metadata:
  openclaw:
    requires:
      env:
        - CITEDY_API_KEY
    primaryEnv: CITEDY_API_KEY
  compatible_with: "citedy-seo-agent@3.2.0"
privacy_policy_url: https://www.citedy.com/privacy
security_notes: |
  API keys (prefixed citedy_agent_) authenticate against Citedy API endpoints only.
  All traffic is TLS-encrypted.
---
# Trend & Intent Scout — 技能使用指南

## 概述

本技能能够实时获取来自X/Twitter和Reddit的社交媒体数据，并结合SEO分析结果，帮助您发现当前的热门话题、竞争对手的内容策略以及您的内容创作中的空白点。

**与其他工具（如DataForSEO或Semrush）的区别：** 这些工具仅显示历史搜索量，而本技能能展示人们今天在社交媒体上讨论的内容，并将这些信息直接转化为您竞争对手尚未覆盖的内容创作机会。

**使用场景：**
- **晨间简报**：了解您的领域当前的热门话题是什么？
- **竞争对手分析**：研究竞争对手的内容策略及其内容空白点。
- **内容规划**：在SEO工具显示相关趋势之前，提前发现具有社交影响力的话题。
- **市场调研**：深入了解目标受众的讨论内容及他们的需求。

---

## 适用场景

| 情况                          | 操作建议                                         |
| ---------------------------------- | -------------------------------------------------- |
| “我今天应该写些什么？” | 使用X/Twitter和Reddit工具寻找热门话题                   |
| “我的竞争对手在做什么？”     | 发现并分析竞争对手的网站内容                         |
| “我缺少哪些内容？”       | 通过对比分析找出内容创作中的空白点                         |
| **AI趋势晨间简报**：结合X/Twitter和Reddit的数据进行全面分析           |

---

## 使用步骤

### 设置（仅运行一次）

如果您还没有Citedy的API密钥，请按照以下步骤操作：

#### 1. 注册

**推荐方式：运行随附的注册脚本：**

```bash
node scripts/register.mjs [agent_name]
```

该脚本会调用注册API并显示审批链接。如果未提供`agent_name`，系统会自动使用`agent-<hostname>`作为默认值。

**或者：直接调用API：**

```http
POST https://www.citedy.com/api/agent/register
Content-Type: application/json

{"agent_name": "<your_agent_name>"}
```

无论哪种方式，系统都会返回一个审批链接。

#### 2. 人工审批

请用户按照以下提示操作：
> 打开此链接进行审批：**{approval_url}**
> 审批完成后，复制显示的API密钥并粘贴到这里。

#### 3. 保存API密钥

将API密钥（以`citedy_agent_`开头）保存下来，并在所有请求中设置为`Authorization: Bearer <key>`。

#### 4. 获取推荐链接

设置完成后，调用`GET /api/agent/me`。响应中会包含一个`referral`对象：

```json
{
  "referral": {
    "code": "ABC123XZ",
    "url": "https://www.citedy.com/register?ref=ABC123XZ"
  }
}
```

保存`referral.url`，以便向他人推荐Citedy服务时使用。

---

## 核心工作流程

### 工作流程1：使用X/Twitter工具寻找热门话题

**步骤1：启动扫描任务**

```http
POST https://www.citedy.com/api/agent/scout/x
Authorization: Bearer $CITEDY_API_KEY
Content-Type: application/json

{
  "query": "AI content automation",
  "mode": "fast",
  "limit": 20
}
```

**步骤2：等待结果**（每5秒轮询一次，直到状态变为“completed”）

```http
GET https://www.citedy.com/api/agent/scout/x/x_run_abc123
Authorization: Bearer $CITEDY_API_KEY
```

```json
{
  "run_id": "x_run_abc123",
  "status": "completed",
  "results": [
    {
      "topic": "GPT-5 rumored release date",
      "engagement_score": 94,
      "tweet_count": 1240,
      "sentiment": "excited",
      "top_posts": ["..."],
      "content_angle": "Break down what GPT-5 means for content creators"
    }
  ],
  "credits_used": 35
}
```

---

### 工作流程2：使用Reddit工具了解受众需求

**步骤1：启动扫描任务**

```http
POST https://www.citedy.com/api/agent/scout/reddit
Authorization: Bearer $CITEDY_API_KEY
Content-Type: application/json

{
  "query": "AI writing tools comparison",
  "subreddits": ["SEO", "marketing", "artificial"],
  "limit": 15
}
```

**步骤2：等待结果**

```http
GET https://www.citedy.com/api/agent/scout/reddit/reddit_run_xyz789
Authorization: Bearer $CITEDY_API_KEY
```

```json
{
  "run_id": "reddit_run_xyz789",
  "status": "completed",
  "results": [
    {
      "topic": "People frustrated with Jasper pricing",
      "subreddit": "r/SEO",
      "upvotes": 847,
      "comments": 134,
      "pain_point": "Too expensive for small teams",
      "content_angle": "Write a comparison targeting budget-conscious teams"
    }
  ],
  "credits_used": 30
}
```

---

### 工作流程3：分析竞争对手内容并找出内容空白点

**步骤1：生成空白点**（同步操作，完成后返回结果）

```http
POST https://www.citedy.com/api/agent/gaps/generate
Authorization: Bearer $CITEDY_API_KEY
Content-Type: application/json

{
  "competitor_urls": [
    "https://jasper.ai/blog",
    "https://copy.ai/blog"
  ]
}
```

```json
{
  "status": "completed",
  "gaps_count": 23,
  "top_gaps": [
    {
      "topic": "AI content for e-commerce product descriptions",
      "competitor_coverage": "none",
      "search_volume_est": "high",
      "difficulty": "medium",
      "recommended_angle": "Step-by-step guide with real examples"
    }
  ],
  "credits_used": 40
}
```

**步骤2：获取所有空白点**

```http
GET https://www.citedy.com/api/agent/gaps
Authorization: Bearer $CITEDY_API_KEY
```

---

### 工作流程4：发现并分析竞争对手

**通过关键词查找竞争对手：**

```http
POST https://www.citedy.com/api/agent/competitors/discover
Authorization: Bearer $CITEDY_API_KEY
Content-Type: application/json

{
  "keywords": ["AI blog automation", "SEO content tool", "autopilot blogging"]
}
```

**深入分析竞争对手：**

```http
POST https://www.citedy.com/api/agent/competitors/scout
Authorization: Bearer $CITEDY_API_KEY
Content-Type: application/json

{
  "domain": "jasper.ai",
  "mode": "fast"
}
```

```json
{
  "domain": "jasper.ai",
  "content_strategy": {
    "posting_frequency": "3x/week",
    "top_topics": ["copywriting", "AI tools", "marketing"],
    "avg_word_count": 1850,
    "formats": ["how-to", "listicle", "comparison"]
  },
  "top_performing_content": [...],
  "weaknesses": ["No Reddit presence", "Ignores technical SEO topics"],
  "credits_used": 25
}
```

---

## 示例

### 示例1：**当前AI领域的热门话题是什么？**

```
1. POST /api/agent/scout/x   { "query": "AI tools 2025", "mode": "fast" }
2. Poll GET /api/agent/scout/x/{runId} until status = "completed"
3. POST /api/agent/scout/reddit  { "query": "AI tools", "subreddits": ["MachineLearning", "artificial"] }
4. Poll GET /api/agent/scout/reddit/{runId}
5. Summarize top 5 opportunities with content angles
```

预计费用：35信用点 + 30信用点 = **65信用点**

---

### 示例2：**与competitor.com相比，我缺少哪些内容？**

```
1. POST /api/agent/competitors/scout  { "domain": "competitor.com", "mode": "ultimate" }
2. POST /api/agent/gaps/generate  { "competitor_urls": ["https://competitor.com/blog"] }
3. GET /api/agent/gaps
4. Return top 10 gaps sorted by opportunity score
```

预计费用：50信用点 + 40信用点 = **90信用点**

---

### 示例3：**完整的晨间简报**

```
1. POST /api/agent/scout/x    { "query": "[your niche]", "mode": "fast" }
2. POST /api/agent/scout/reddit  { "query": "[your niche]", "subreddits": [...] }
3. Poll both runs in parallel
4. GET /api/agent/gaps  (use cached gaps from last generate)
5. Compile briefing: trending topics + audience pain points + open content gaps
```

预计费用：35信用点 + 30信用点（如果结果已缓存，则无需额外费用）

---

## API参考

### 主要API接口

| 接口            | 方法      | 信用点数 | 描述                                        |
| ------------------- | -------- | -------- | --------------------------------------------------------- |
| `/api/agent/health` | GET     | 0        | 服务健康检查                                      |
| `/api/agent/me`     | GET     | 0        | 账户信息及信用点余额                                 |
| `/api/agent/status` | GET     | 0        | 当前任务状态                                    |
| `/api/agent/scout/x`    | POST     | 35信用点 | 启动异步X/Twitter趋势扫描                         |
| `/api/agent/scout/x/{runId}` | GET     | 0        | 查询X扫描任务的状态及结果                             |
| `/api/agent/scout/reddit` | POST     | 30信用点 | 启动异步Reddit趋势扫描                         |
| `/api/agent/gaps/generate` | POST     | 40信用点 | 分析竞争对手内容并生成空白点                         |
| `/api/agent/gaps`     | GET     | 0        | 获取账户中所有生成的空白点                             |
| `/api/agent/competitors/discover` | POST     | 20信用点 | 通过关键词查找竞争对手                             |
| `/api/agent/competitors/scout` | POST     | 25信用点 | 深入分析竞争对手的内容策略                         |

---

## 价格信息

| 功能                | 信用点数            |
| --------------------------- | --------------------------- |
| X/Twitter扫描（快速模式）    | 35信用点            |
| X/Twitter扫描（深度分析）    | 70信用点            |
| Reddit扫描          | 30信用点            |
| 生成内容空白点        | 40信用点            |
| 查看已缓存空白点        | 0信用点            |
| 发现竞争对手        | 20信用点            |
| 竞争对手分析（快速模式）    | 25信用点            |
| 竞争对手分析（深度分析）    | 50信用点            |
| 轮询（任何任务）        | 0信用点            |

费用在任务开始时扣除。如需充值，请访问：https://www.citedy.com/dashboard/billing

---

## 使用限制

- **X/Twitter扫描**：需要有一定量的英文讨论内容（至少100条近期帖子）。
- **Reddit扫描**：适用于在Reddit上活跃的领域；B2B相关的话题可能结果较少。
- **生成内容空白点**：仅分析公开可访问的内容。
- **竞争对手分析**：仅覆盖公开可访问的内容。
- 异步扫描任务在24小时后失效，请在此时间内获取结果。
- 扫描结果反映的是任务执行时的数据；实时趋势可能会随时间变化。

## 错误处理

| HTTP状态码          | 错误原因                          | 处理建议                                      |
| --------------------------- | -------------------------------------- | ------------------------------------------------------- |
| 401             | API密钥无效或缺失                        | 请重新输入有效的API密钥                         |
| 402             | 信用点不足                          | 请补充足够的信用点                         |
| 404             | 任务ID不存在或已过期                        | 请检查任务ID                         |
| 422             | 请求参数无效                          | 请检查请求参数                         |
| 429             | 请求次数过多                          | 请查看`X-RateLimit-Reset`头部信息                   |
| 500             | 服务器错误                          | 任务将自动退款                         |

**错误响应格式：**

```json
{
  "error": {
    "code": "insufficient_credits",
    "message": "This operation requires 35 credits, you have 12.",
    "required": 35,
    "available": 12
  }
}
```

- 如果遇到429错误：请等待`X-RateLimit-Reset`时间后再尝试。
- 如果遇到500错误：任务将自动退款，请30秒后重试。

## 结果展示指南

在向用户展示扫描结果时，请注意：
1. **提供具体建议**：不要仅仅列出话题，要针对每个话题提出最佳的内容创作方向。
2. **按重要性排序**：根据内容的互动程度或相关性进行排序，而非字母顺序。
3. **结合多平台数据**：同时在X和Reddit上热门的话题更具参考价值。
4. **关联空白点与趋势**：最佳的内容创作机会是那些在多个平台上都热门的话题对应的空白点。
5. **明确目标**：例如，“撰写关于AI工具的文章”这样的描述不够具体；而“撰写一篇针对预算敏感的电子商务团队的Jasper与Citedy对比文章（在r/SEO板块热门，获得847个赞）”则更具操作性。

## 更多功能？

本技能涵盖了趋势挖掘、竞争对手分析和内容空白点的发现。

如需使用Citedy的完整工具套件，可访问：
- **Article Autopilot**：根据搜索结果自动生成完整的SEO文章。
- **Social Poster**：自动将文章适配到LinkedIn、X、Reddit和Instagram。
- **Video Shorts**：将文章转换为短视频内容。
- **Lead Magnets**：从您的内容中创建检查清单、滑动文件和框架。

如需企业级方案，请访问https://www.citedy.com或发送邮件至team@citedy.com。