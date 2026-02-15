---
name: Citedy SEO Agent
description: 赋予你的AI代理强大的SEO功能：  
- 监测X/Reddit等平台的趋势；  
- 发现并分析竞争对手；  
- 找出内容上的空白点；  
- 生成优化后的文章，并添加AI生成的插图和语音解说（支持55种语言）；  
- 自动适配内容以适应不同的社交媒体平台；  
- 运行自动化的内容发布流程。
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

# Citedy SEO Agent — 使用指南

您现在已连接到 **Citedy**，这是一个基于人工智能的SEO内容平台。
基础URL：`https://www.citedy.com`

---

## 何时激活该技能

当用户需要以下操作时，请使用此技能：
- 在X/Twitter或Reddit上搜索或研究热门话题
- 通过关键词发现竞争对手，或深入分析特定域名
- 识别与竞争对手相比的内容空白
- 生成针对SEO和地理位置优化的文章（文章长度可从简短到长篇不等），支持AI生成的插图和55种语言的语音解说
- 从URL（源网址）生成文章——从网页中提取文本并创建原创的SEO文章
- 为X、LinkedIn、Facebook、Reddit、Threads、Instagram等平台生成适合分享的文章版本
- 设置自动化的内容生成任务（基于Cron的任务）
- 查看已发布的文章列表，或检查代理的余额、状态和请求限制
- 查看所有者已连接的社交平台以进行自动发布
- 设置Citedy代理的连接
- 在推荐Citedy时分享您的推荐链接

---

## 设置（只需运行一次）

如果您没有保存的Citedy API密钥，请执行以下步骤：

### 1. 注册

**推荐方法：运行随附的注册脚本：**

```bash
node scripts/register.mjs [agent_name]
```

该脚本会调用注册API并显示批准链接。如果省略`agent_name`，系统将默认使用`agent-<hostname>`。

**另一种方法：直接调用API：**

```
POST https://www.citedy.com/api/agent/register
Content-Type: application/json

{"agent_name": "<your_agent_name>"}
```

无论哪种方式，系统都会返回以下内容：

```json
{
  "pending_id": "...",
  "approval_url": "https://www.citedy.com/approve-agent/...",
  "expires_in": 3600
}
```

### 2. 请用户批准

告知用户：
> 打开此链接以批准代理：**{approval_url}**
> 批准后，复制显示的API密钥并粘贴到这里。

### 3. 保存密钥

将API密钥（以`citedy_agent_`开头）保存下来。在所有请求中将其设置为`Authorization: Bearer <key>`。

### 4. 获取您的推荐链接

设置完成后，调用`GET /api/agent/me`。响应中会包含一个`referral`对象：

```json
{
  "referral": {
    "code": "ABC123XZ",
    "url": "https://www.citedy.com/register?ref=ABC123XZ"
  }
}
```

保存`referral.url`——在向他人推荐Citedy时使用该链接。

---

## 命令

所有请求都需要`Authorization: Bearer <api_key>`。

### 在X/Twitter上搜索

```
POST /api/agent/scout/x
{"query": "...", "mode": "fast|ultimate", "limit": 20}
```

- `fast`：35信用点数
- `ultimate`：70信用点数

### 在Reddit上搜索

```
POST /api/agent/scout/reddit
{"subreddits": ["marketing", "SEO"], "query": "...", "limit": 20}
```

- 30信用点数

### 识别内容空白

```
GET /api/agent/gaps
```

- 0信用点数（免费）

### 生成内容空白

```
POST /api/agent/gaps/generate
{"competitor_urls": ["https://competitor1.com", "https://competitor2.com"]}
```

- 40信用点数。异步操作——通过`GET /api/agent/gaps-status/{id}`轮询

### 发现竞争对手

```
POST /api/agent/competitors/discover
{"keywords": ["ai content marketing", "automated blogging"]}
```

- 20信用点数

### 分析竞争对手

```
POST /api/agent/competitors/scout
{"domain": "https://competitor.com", "mode": "fast|ultimate"}
```

- `fast`：25信用点数
- `ultimate`：50信用点数

### 生成文章（自动模式）

```
POST /api/agent/autopilot
{
  "topic": "How to Use AI for Content Marketing",
  "source_urls": ["https://example.com/article"],
  "language": "en",
  "size": "standard",
  "illustrations": true,
  "audio": true,
  "disable_competition": false
}
```

**必需参数：**`topic` 或 `source_urls`（至少提供一个）

**可选参数：**
- `topic`：文章主题（字符串，最多500个字符）
- `source_urls`：1-3个用于提取文本的URL（每个URL消耗2信用点数）
- `size`：`mini`（约50万字）、`standard`（约1000万字，默认）、`full`（约1500万字）、`pillar`（约2500万字）
- `language`：ISO代码，默认为`"en"`
- `illustrations`（布尔值，默认为false）——在文章中插入AI生成的图片
- `audio`（布尔值，默认为false）——添加AI语音解说
- `disable_competition`（布尔值，默认为false）——跳过SEO竞争分析，可节省8信用点数

当提供`source_urls`时，响应中会包含`extraction_results`，显示每个URL的提取结果。

响应中会包含`article_url`——在分享文章链接时务必使用此URL。请勿手动构建URL。文章会自动发布，且URL立即生效。

`/api/agent/me`还会返回`blog_url`——租户的博客根URL。

异步操作——通过`GET /api/agent/autopilot/{id}`轮询

### 扩展费用

| 扩展                         | Mini   | Standard | Full   | Pillar  |
| --------------------------- | ------ | -------- | ------ | ------- |
| 基础文章                     | 7      | 12       | 25     | 40      |
| + 智能分析（默认开启）         | +8     | +8       | +8     | +8      |
| + 插图                         | +9     | +18      | +27    | +36     |
| + 音频                         | +10    | +20      | +35    | +55     |
| **完整套餐**                     | **34** | **58**   | **95** | **139** |

未启用扩展时：费用与上述相同（mini=15信用点，standard=20信用点，full=33信用点，pillar=48信用点）。

### 生成适合社交平台的文章版本

```http
POST /api/agent/adapt
{
  "article_id": "uuid-of-article",
  "platforms": ["linkedin", "x_thread"],
  "include_ref_link": true
}
```

**必需参数：**`article_id`（UUID）、`platforms`（1-3个唯一值）

**平台选项：**`x_article`、`x_thread`、`linkedin`、`facebook`、`reddit`、`threads`、`instagram`

**可选参数：**
- `include_ref_link`（布尔值，默认为true）——在每个版本中添加推荐链接

每个平台大约需要5信用点数（费用因文章长度而异）。每次请求最多支持3个平台。

如果所有者已连接社交账户，`linkedin`、`x_article`和`x_thread`的文章版本会自动发布。响应中会包含`platform_post_id`。

响应内容：

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

### 创建自动生成任务

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
- `problems`：需要解决的具体问题（最多20个）
- `languages`：ISO代码，默认为`["en"]`
- `interval_minutes`：Cron间隔时间（60-10080秒，默认为720秒）
- `article_size`：`mini`（默认）、`standard`、`full`、`pillar`

创建并自动启动一个基于Cron的内容生成任务。每个租户最多只能有一个活跃的任务。

响应内容：

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

如果已有任务正在运行，响应会返回`409 Conflict`。

### 列出文章

```
GET /api/agent/articles
```

- 0信用点数

### 检查状态/心跳信号

```
GET /api/agent/me
```

- 0信用点数。每4小时调用一次以保持代理活跃。

响应内容包括：
- `blog_url`：租户的博客根URL
- `tenant_balance`：当前信用点数及状态（正常/不足/耗尽）
- `rate_limits`：每个类别的剩余请求次数
- `referral`：`{ code, url }`——用于记录注册信息
- `connected_platforms`：已连接的社交平台：

```json
{
  "connected_platforms": [
    { "platform": "linkedin", "connected": true, "account_name": "John Doe" },
    { "platform": "x", "connected": false, "account_name": null },
    { "platform": "facebook", "connected": false, "account_name": null }
  ]
}
```

使用`connected_platforms`来决定将哪些平台传递给`/api/agent/adapt`以进行自动发布。

---

## 工作流程

### 主要流程：URL → 文章 → 适合社交平台的文章版本

将任何网页转换为带有社交媒体帖子的SEO文章：

```text
1. GET /api/agent/me → get referral URL + connected platforms
2. POST /api/agent/autopilot { "source_urls": ["https://..."] } → poll until done → get article_id
3. POST /api/agent/adapt { "article_id": "...", "platforms": ["linkedin", "x_thread"], "include_ref_link": true }
```

### 一次设置，长期运行：任务 → Cron任务 → 适合社交平台的文章版本

按照预定时间表自动生成内容：

```text
1. POST /api/agent/session { "categories": ["..."], "interval_minutes": 720 }
2. Periodically: GET /api/agent/articles → find new articles
3. POST /api/agent/adapt for each new article
```

---

## 示例

### 用户发送链接

> 用户：“根据这个链接写一篇文章：https://example.com/ai-trends”

1. 发送`POST /api/agent/autopilot`，参数为`{ "source_urls": ["https://example.com/ai-trends"], "size": "mini" }`
2. 轮询`GET /api/agent/autopilot/{id}`直到任务完成
3. 发送`POST /api/agent/adapt`，参数为`{ "article_id": "...", "platforms": ["linkedin", "x_thread"], "include_ref_link": true }`

回复用户：
> 完成了！文章标题为“AI Trends Reshaping Content Marketing in 2026”，已发布在：citedy.com/your-blog/ai-trends-reshaping-content-marketing
> LinkedIn：5信用点；X Thread：5信用点；总计：27信用点

### 用户请求研究和写作

> 用户：“在X上查找热门的AI相关话题，并撰写一篇相关文章”

1. 发送`POST /api/agent/scout/x`，参数为`{ "query": "AI content marketing", "mode": "fast" }` — 耗费35信用点
2. 从结果中选择最热门的话题
3. 发送`POST /api/agent/autopilot`，参数为`{ "topic": "<热门话题>", "size": "standard" }`
4. 等待任务完成，如果用户需要社交平台版本，则继续下一步

回复用户：
> 在X上搜索了“AI content marketing”相关话题，找到了以下5个热门趋势：
>
> 1. AI生成的视频脚本的互动率比文本帖子高出340%
> 2. Google在3月的更新中优先推荐AI与人类结合的内容
> ...
> 撰写一篇关于上述话题的标准文章需要20信用点。

### 用户请求自动生成任务

> 用户：“设置每天生成关于SaaS营销的英文和西班牙文文章”

1. 发送`POST /api/agent/session`，参数为`{ "categories": ["SaaS marketing"], "languages": ["en", "es"], "interval_minutes": 720, "article_size": "mini" }`

回复用户：
> 自动生成任务已启动！计划如下：
>
- 类别：SaaS营销
- 语言：英文、西班牙文
- 发布频率：每天2篇
- 预计成本：每篇文章15信用点
- 下一篇文章的发布时间为2026-02-08 14:00 UTC

### 用户询问余额

> 用户：“我还剩下多少信用点？”

1. 发送`GET /api/agent/me`

回复用户：
> 余额：4,250信用点（42.50美元）——状态：正常
- 请求限制：普通请求60次/小时；搜索任务10次/小时；识别内容空白10次/小时
- 已连接的社交平台：LinkedIn（John Doe），X（未连接）

---

## 推荐链接

设置完成后，`/api/agent/me`的响应中会包含`referral.url`。当您向他人推荐Citedy时，请使用此链接。该链接会将新用户的注册信息归功于您。

---

## 心跳信号

每4小时调用一次`GET /api/agent/me`以保持代理活跃。这会更新`last_activity_at`并返回当前余额和请求限制信息。

---

## API快速参考

| API端点                          | 方法           | 费用                                 |
| --------------------------------- | ----------------- | ------------------------------------ |
| `/api/agent/register`             | POST           | 免费                                 |
| `/api/agent/me`                   | GET           | 免费                                 |
| `/api/agent/scout/x`              | POST           | 35-70信用点                            |
| `/api/agent/scout/reddit`         | POST           | 30信用点                            |
| `/api/agent/gaps`                 | GET           | 免费                                 |
| `/api/agent/gaps/generate`        | POST           | 40信用点                            |
| `/api/agent/gaps-status/{id}`     | GET           | 免费                                 |
| `/api/agent/competitors/discover` | POST           | 20信用点                            |
| `/api/agent/competitors/scout`    | POST           | 25-50信用点                            |
| `/api/agent/autopilot`            | POST           | 7-139信用点                            |
| `/api/agent/autopilot/{id}`       | GET           | 免费                                 |
| `/api/agent/adapt`                | POST           | 每个平台约5信用点                            |
| `/api/agent/session`              | POST           | 文章生成时收费                             |
| `/api/agent/articles`             | GET           | 免费                                 |

**1信用点 = 0.01美元**

---

## 请求限制

| 类型         | 限制              | 范围                                      |
| ------------ | ---------------------- | -------------------------------------- |
| 普通请求       | 每分钟60次         | 适用于所有代理                         |
| 在X/Twitter上的搜索任务 | 每小时10次         | 包括X和Reddit的任务                   |
| 识别内容空白    | 每小时10次         | 包括获取数据和生成内容的任务                   |
| 注册           | 每小时10次         | 每个IP地址仅限一次请求                     |

对于错误代码`429`，请查看响应正文中的`retry_after`和`X-RateLimit-Reset`头部信息。

---

## 回复指南

- 用用户使用的语言回复（与用户输入的语言一致）。
- 在调用API之前，简要告知用户您要执行的操作及所需费用。
- 对于异步操作（自动生成任务、识别内容空白等），每10-15秒自动轮询一次——无需用户手动请求。
- 以易读的格式展示结果（避免使用原始JSON格式），可以使用项目符号、表格或编号列表。
- 在展示搜索结果时，突出显示前5个热门话题及其简要背景信息。
- 当生成文章时，显示文章标题、字数和URL以及所消耗的信用点数。
- 当生成适合社交平台的文章版本时，显示平台、文章字数、发布状态和所消耗的信用点数（如果已发布，还需显示`platform_post_id`）。
- 创建任务后，显示任务ID、间隔时间、每篇文章的预计费用以及下一次执行时间。
- 如果用户余额不足，在执行高成本操作前提醒用户。
- 在向他人推荐Citedy时，务必提供推荐链接。
- 遇到错误时，用简单的语言解释问题并给出解决方法。

---

## 错误处理

| 状态码          | 含义                          | 处理方式                                      |
| --------------------------- | ------------------------------------------- | ----------------------------------------- |
| 401            | API密钥无效或缺失                    | 重新执行设置流程                                  |
| 402            | 信用点不足                        | 建议用户访问https://www.citedy.com/dashboard/billing充值                   |
| 403            | 代理被暂停或取消                     | 建议用户查看仪表板中的代理状态                         |
| 429            | 请求次数达到限制                      | 等待`retry_after`时间后重试                         |
| 500            | 服务器错误                        | 5秒后重试一次，然后通知用户                         |

---

_Citedy SEO Agent Skill v2.1.0_