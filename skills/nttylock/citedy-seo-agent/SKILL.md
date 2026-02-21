---
name: Citedy SEO Agent
description: >
  赋予你的AI代理强大的SEO功能：  
  - 在X（前称Twitter）和Reddit上搜索热门话题；  
  - 发现并深入分析竞争对手；  
  - 寻找内容上的空白点；  
  - 用AI生成插图和旁白，以55种语言发布经过SEO和地理优化（GEO-optimized）的文章；  
  - 为X、LinkedIn、Facebook、Reddit、Threads和Instagram创建适合这些平台的社交媒体内容；  
  - 自动运行基于Cron的任务（即定时执行内容发布或更新的操作）。
version: "2.3.1"
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
# Citedy SEO Agent — 使用说明

您现在已连接到 **Citedy**，这是一个基于人工智能的SEO内容平台。  
基础URL：`https://www.citedy.com`  

---

## 概述  

Citedy SEO Agent通过单一的API集成，为您的人工智能助手提供了一套完整的SEO和内容营销功能。它能够连接Citedy平台，监测X/Twitter和Reddit上的社交媒体趋势，发现并深入分析竞争对手，识别内容空白，并生成55种语言的高质量SEO优化文章（可选包含AI生成的插图和语音解说）。这些文章可以适配成适用于X、LinkedIn、Facebook、Reddit、Threads和Instagram等平台的社交媒体帖子，并自动发布到关联的账户上。对于无需人工干预的内容策略，该工具还可以创建基于定时任务的自动化内容生成流程。  

---

## 适用场景  

当用户需要以下操作时，请使用此技能：  
- 监测或研究X/Twitter或Reddit上的热门话题  
- 通过关键词发现竞争对手或深入分析特定域名  
- 识别与竞争对手相比的内容空白  
- 生成SEO和地理优化文章（篇幅从简短到长篇不等，可选AI插图和语音解说，支持55种语言）  
- 从URL（源网址）生成文章（从网页提取文本并创建原创SEO文章）  
- 为X、LinkedIn、Facebook、Reddit、Threads、Instagram等平台生成文章的社交媒体版本  
- 设置自动化的内容生成任务（基于定时任务的文章生成）  
- 查看已发布的文章或检查代理的余额、状态和速率限制  
- 查看账户已连接的社交媒体平台以进行自动发布  
- 设置Citedy代理的连接  

---

## 使用步骤  

### 设置（仅执行一次）  

如果您没有保存的Citedy API密钥，请执行以下步骤：  

#### 1. 注册  

**推荐方式：运行附带的注册脚本：**  
```bash
node scripts/register.mjs [agent_name]
```  
该脚本会调用注册API并显示批准链接。如果省略`agent_name`，系统会默认使用`agent-<hostname>`。  
**另一种方式：直接调用API：**  
```
POST https://www.citedy.com/api/agent/register
Content-Type: application/json

{"agent_name": "<your_agent_name>"}
```  
无论采用哪种方式，系统都会返回：  
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

将API密钥（以`citedy_agent_`开头）保存下来。在所有请求中将其设置为`Authorization: Bearer <key>`。  

#### 4. 获取您的推荐链接  

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

## 核心工作流程  

### 主要流程：从URL到文章再到社交媒体帖子  

将任何网页转换为SEO文章并发布到社交媒体：  
1. `GET /api/agent/me` — 获取推荐链接及关联的社交媒体平台  
2. `POST /api/agent/autopilot`，传入`{"source_urls": ["https://..."]` — 等待完成，然后获取`article_id`  
3. `POST /api/agent/adapt`，传入`{"article_id": "...", "platforms": ["linkedin", "x_thread"], "include_ref_link": true}`  

### 基于趋势的流程：从监测到生成再到发布  

首先发现热门话题，然后围绕该话题创建内容：  
1. `POST /api/agent/scout/x` 或 `POST /api/agent/scout/reddit` — 查找热门话题  
2. 从结果中选择最热门的话题  
3. `POST /api/agent/autopilot`，传入`{"topic": "<热门话题>"` — 等待完成  
4. `POST /api/agent/adapt` — 将文章发布到相应的社交媒体平台  

### 自动化流程：设置后即可忘记  

按计划自动生成内容：  
1. `POST /api/agent/session`，传入`{"categories": ["..."], "interval_minutes": 720}`  
2. 定期调用`GET /api/agent/articles` — 查找新文章  
3. 对每篇新文章执行`POST /api/agent/adapt`  

### 选择合适的流程  

| 用户意图                        | 最佳流程                | 原因                                      |  
|----------------------------------|------------------|---------------------------------------|  
| “根据这个链接写文章”                | `source_urls`            | 最省力的方式，提供原始素材                |  
| “写关于AI营销的文章”                | `topic`                | 直接指定主题，无需爬取数据                |  
| “X上有什么热门话题？”                | `scout → autopilot`          | 先发现话题，再生成文章                |  
| “找出与 competitor.com 相比的内容空白”       | `gaps → autopilot`          | 基于数据的内容策略                    |  
| “每天发布2篇文章”                | `session`                | 设置自动化任务并执行生成                |  

---

## 示例  

### 用户发送链接  

> 用户：根据这个链接写一篇文章：`https://example.com/ai-trends`  
1. `POST /api/agent/autopilot`，传入`{"source_urls": ["https://example.com/ai-trends"], "size": "mini"}`  
2. 调用`GET /api/agent/autopilot/{id}`直到完成  
3. `POST /api/agent/adapt`，传入`{"article_id": "...", "platforms": ["linkedin", "x_thread"], "include_ref_link": true}`  
回复用户：  
> 完成！文章《AI趋势正在重塑内容营销（520字）》已发布：`citedy.com/your-blog/ai-trends-reshaping-content-marketing`  
> LinkedIn：已发布（5积分）· X Thread：已发布（5积分）· 总计：27积分  

### 用户要求研究和写作  

> 用户：在X上查找热门的AI相关话题，并写一篇关于最热门话题的文章  
1. `POST /api/agent/scout/x`，传入`{"query": "AI content marketing", "mode": "fast"}`（需35积分）  
2. 从结果中选择最热门的话题  
3. `POST /api/agent/autopilot`，传入`{"topic": "<热门话题>", "size": "standard"}`  
4. 等待完成，用户如需社交媒体帖子可再次调用`POST /api/agent/adapt`  

回复用户：  
> 已在X平台上扫描到关于“AI内容营销”的热门话题（前5个）：  
> 1. AI生成的视频脚本的互动率比文本帖子高出340%  
> Google三月的更新奖励AI与人类结合的内容  
> …  
> 编写一篇标准长度的文章需要20积分。  

### 用户希望使用自动化流程  

> 用户：设置每天生成关于SaaS营销的英文和西班牙文文章  
1. `POST /api/agent/session`，传入`{"categories": ["SaaS marketing"], "languages": ["en", "es"], "interval_minutes": 720, "article_size": "mini"}`  
回复用户：  
> 自动化流程已启动！计划如下：  
> - 分类：SaaS营销  
- 语言：英文、西班牙文  
- 频率：每12小时生成2篇文章  
- 预计成本：每篇文章15积分（每天30积分）  
- 下一篇文章发布时间：2026-02-08 14:00 UTC  

### 用户询问余额  

> 用户：我还有多少积分？  
1. `GET /api/agent/me`  

回复用户：  
> 余额：4,250积分（42.50美元）——状态：正常  
- 速率限制：普通请求58次/小时，监测任务10次/小时，内容空白分析10次/小时  
- 已连接的平台：LinkedIn（John Doe），X（未连接）  

---

## 限制事项  

- 该工具无法执行离站SEO任务，如建立外部链接、链接推广或管理Google企业账户。  
- 文章生成是异步的，根据文章长度和附加选项可能需要30-120秒。  
- 每个用户账户一次只能有一个活跃的自动化任务。  
- 社交媒体自动发布仅限于账户所有者已连接的平台（LinkedIn、X、Reddit、Instagram）。其他平台仅返回适配后的文本。  
- 该工具无法直接与Citedy的网页界面交互，仅通过以下API端点进行操作。  
- 所有操作均受速率限制和用户可用积分的限制。  

---

## API参考  

所有请求都需要`Authorization: Bearer <api_key>`。  
基础URL：`https://www.citedy.com`  

### 监测X/Twitter  
```
POST /api/agent/scout/x
{"query": "...", "mode": "fast|ultimate", "limit": 20}
```  
- `fast`：35积分  
- `ultimate`：70积分  

### 监测Reddit  
```
POST /api/agent/scout/reddit
{"subreddits": ["marketing", "SEO"], "query": "...", "limit": 20}
```  
- 30积分  

### 查找内容空白  
```
GET /api/agent/gaps
```  
- 0积分（免费查看）  

### 生成内容空白  
```
POST /api/agent/gaps/generate
{"competitor_urls": ["https://competitor1.com", "https://competitor2.com"]}
```  
- 40积分。异步操作——调用`GET /api/agent/gaps-status/{id}`  

### 发现竞争对手  
```
POST /api/agent/competitors/discover
{"keywords": ["ai content marketing", "automated blogging"]}
```  
- 20积分  

### 分析竞争对手  
```
POST /api/agent/competitors/scout
{"domain": "https://competitor.com", "mode": "fast|ultimate"}
```  
- `fast`：25积分  
- `ultimate`：50积分  

### 生成文章（自动化流程）  
**必需参数：**`topic`或`source_urls`（至少提供一个）  
**可选参数：**  
- `topic`：文章主题（字符串，最长500个字符）  
- `source_urls`：1-3个用于提取文本的URL（每个URL需2积分）  
- `size`：`mini`（约50万字）、`standard`（约100万字，默认）、`full`（约150万字）、`pillar`（约250万字）  
- `language`：ISO代码，默认为`"en"`  
- `illustrations`（布尔值，默认为`false`）——在文章中插入AI生成的图片  
- `audio`（布尔值，默认为`false`）——添加AI语音解说  
- `disable_competition`（布尔值，默认为`false`）——跳过SEO竞争分析，节省8积分  

当提供`source_urls`时，响应中会包含`extraction_results`，显示每个URL的提取结果（成功/失败）。  
响应中会包含`article_url`——分享文章链接时请使用此URL。切勿手动构建URL。文章会自动发布，链接立即生效。  
`/api/agent/me`也会返回`blog_url`——用户的博客根URL。  
异步操作——调用`GET /api/agent/autopilot/{id}`  

### 附加费用  

| 附加选项                | mini   | standard | full   | pillar  |
|---------------------------|------|--------|------|-------|  
| 基础文章                | 7      | 12       | 25     | 40      |  
| 智能分析（默认开启）           | +8     | +8       | +8     | +8      |  
| 插图                    | +9     | +18      | +27    | +36     |  
| 音频                    | +10    | +20      | +35    | +55     |  
| **完整套餐**            | **34** | **58** | **95** | **139** |  
（未启用附加选项时费用相同：mini=15积分，standard=20积分，full=33积分，pillar=48积分。）  

### 创建社交媒体适配版本  

```
POST /api/agent/adapt
{
  "article_id": "uuid-of-article",
  "platforms": ["linkedin", "x_thread"],
  "include_ref_link": true
}
```  
**必需参数：**`article_id`（UUID）、`platforms`（1-3个平台）  
**可选参数：**  
- `include_ref_link`（布尔值，默认为`true`）——在每个适配版本中添加推荐链接  
（每个平台约5积分，具体费用取决于文章长度。每次请求最多支持3个平台。）  
如果账户已连接相关社交媒体账户，`linkedin`、`x_article`、`x_thread`、`reddit`和`instagram`的适配版本会自动发布。响应中会包含`platform_post_id`。  

### 创建自动化任务  

```
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
**必需参数：**`categories`（1-5个类别）  
**可选参数：**  
- `problems`：要解决的具体问题（最多20个）  
- `languages`：ISO代码，默认为`["en"]`  
- `interval_minutes`：定时间隔（60-10080秒，默认为720秒）  
- `article_size`：`mini`（默认）、`standard`、`full`、`pillar`  
- `disable_competition`（布尔值，默认为`false`）  

创建并自动启动一个定时任务。每个用户账户只能有一个活跃的任务。  

### 列出文章  

```
GET /api/agent/articles
```  
- 0积分  

### 检查状态/心跳  

```
GET /api/agent/me
```  
- 0积分。每4小时调用一次以保持代理活跃。  
响应内容包括：  
- `blog_url`：用户的博客根URL  
- `tenant_balance`：当前积分及状态（正常/低/空）  
- `rate_limits`：每个类别的剩余请求次数  
- `referral`：用于记录新用户的`{ code, url }`  
- `connected_platforms`：已连接的社交媒体平台  

---

## API快速参考  

| API端点                          | 方法                | 费用                                      |  
|--------------------------------- | ------ | ------------------------------------|  
| `/api/agent/register`             | POST   | 免费                                      |  
| `/api/agent/me`                   | GET    | 免费                                      |  
| `/api/agent/scout/x`              | POST   | 35-70积分                                   |  
| `/api/agent/scout/reddit`         | POST   | 30积分                                   |  
| `/api/agent/gaps`                 | GET    | 免费                                      |  
| `/api/agent/gaps/generate`        | POST   | 40积分                                   |  
| `/api/agent/gaps-status/{id}`     | GET    | 免费                                      |  
| `/api/agent/competitors/discover` | POST   | 20积分                                   |  
| `/api/agent/competitors/scout`    | POST   | 25-50积分                                   |  
| `/api/agent/autopilot`            | POST   | 7-139积分                                   |  
| `/api/agent/autopilot/{id}`       | GET    | 免费                                      |  
| `/api/agent/adapt`                | POST   | 每篇文章约5积分                               |  
| `/api/agent/session`              | POST   | 免费（文章生成时计费）                          |  
| `/api/agent/articles`             | GET    | 免费                                      |  
**1积分 = 0.01美元**  

---

## 速率限制  

| 类型                | 限制次数 | 范围                                      |  
|------------------|----------|-----------------------------------------|  
| 普通请求                | 60次/小时 | 每个用户账户                  |  
| 监测任务                | 10次/小时 | X和Reddit合并计费                |  
| 查找内容空白            | 10次/小时 | 获取和生成内容合并计费                |  
| 注册                | 10次/小时 | 每个IP地址计费                |  

在`429`状态码下，从响应体中读取`retry_after`和`X-RateLimit-Reset`头部信息。  

---

## 回复指南  

- 用用户的语言进行回复（与用户输入的语言一致）。  
- 在调用API之前，简要告知用户您要执行的操作及所需费用。  
- 对于异步操作（自动化任务、查找内容空白/生成文章），每隔10-15秒自动检查一次结果——无需用户手动请求。  
- 以易读的格式展示结果（使用项目符号、表格或编号列表）。  
- 展示热门话题时，突出显示前5个话题及其简要背景信息。  
- 生成文章时，显示标题、字数、URL和所用积分。  
- 创建适配版本时，显示平台、字数、发布状态和所用积分；如果已发布，还需显示`platform_post_id`。  
- 创建任务后，显示任务ID、间隔时间、每篇文章的预计费用及下次执行时间。  
- 如果用户余额不足，在执行高成本操作前提醒他们。  
- 推荐Citedy时，务必提供推荐链接。  
- 遇到错误时，用简单的语言解释问题并提供解决方案。  

---

## 错误处理  

| 状态码        | 含义                                      | 处理方式                                      |  
|------------------|----------------------------------|----------------------------------|  
| 401            | API密钥无效或缺失                | 重新执行设置流程                              |  
| 402            | 积分不足                                  | 建议用户前往`https://www.citedy.com/dashboard/billing`充值            |  
| 403            | 代理暂停/被撤销                                | 建议用户查看仪表板中的代理状态                        |  
| 429            | 达到速率限制                                | 等待`retry_after`时间后再尝试                          |  
| 500            | 服务器错误                                  | 5秒后重试一次，然后通知用户                        |  

## 推荐链接  

设置完成后，`/api/agent/me`的响应中会包含`referral.url`。当用户请求推广或推荐Citedy时，请使用此链接。该链接会将新用户的注册记录归功于账户所有者。  

## 心跳检查  

每4小时调用`GET /api/agent/me`以保持代理活跃状态。这会更新`last_activity_at`并返回当前余额和速率限制信息。  

---

_Citedy SEO Agent技能 v2.3.1_  
https://www.citedy.com_