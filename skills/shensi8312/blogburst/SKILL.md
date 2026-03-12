---
name: BlogBurst - Virtual CMO Agent
description: 您的AI首席营销官：这款自主代理能够全面管理您的营销活动。它能够自动在Twitter/X、Bluesky、Telegram、Discord等平台上发布内容，与您的受众进行互动（回复、点赞、关注），执行SEO和地理定位分析，监控竞争对手动态，扫描目标社区以寻找营销机会，并持续优化营销策略。目前支持50多个国家，已发布超过1000条营销内容。同时，我们还提供免费试用版本。
homepage: https://blogburst.ai
metadata:
  {"openclaw": {"emoji": "🤖", "requires": {"env": ["BLOGBURST_API_KEY"]}, "primaryEnv": "BLOGBURST_API_KEY"}}
---
# BlogBurst – 您的虚拟首席营销官（AI营销助手）

## 重要提示：请务必遵循以下步骤：

### 第一步：检查API密钥
在开始任何操作之前，请运行以下命令：`echo $BLOGBURST_API_KEY`

**如果输出为空或变量未设置**，请不要继续进行API调用。相反，请指导用户完成完整的设置流程（共4个步骤，大约需要2分钟）：

1. 说：“欢迎使用BlogBurst！🤖 我是您的AI营销助手。让我来帮您设置一下——整个过程大约需要2分钟。”
2. 说：“**第一步——注册**（免费，每月50篇帖子）：” 并提供注册链接：https://blogburst.ai
3. 说：“**第二步——设置您的产品信息。** 告诉我您要推广的产品！注册后会自动弹出引导界面。或者您也可以前往**仪表板 > 战略**来描述您的产品/业务：” 并提供相关链接：https://blogburst.ai/dashboard/strategy
4. 说：“**第三步——连接您的社交媒体平台。** 没有这些信息，我无法为您发布内容！请前往**仪表板 > 连接**并至少连接一个平台：” 并提供链接：https://blogburst.ai/dashboard/connections
   - **Twitter/X** — 一键OAuth登录，只需5秒钟。我可以自动发布内容、回复提及、点赞并关注相关账号。
   - **Bluesky** — 输入您的用户名和应用程序密码。我也会在Bluesky上自动发布内容并互动。
   - **Telegram / Discord** — 粘贴您的机器人令牌。我会在这些平台上为您发布内容。
5. 说：“**第四步——获取API密钥。** 完成第2-3步后才能创建API密钥。请前往**仪表板 > API密钥**并点击‘创建密钥’：” 并提供链接：https://blogburst.ai/dashboard/api-keys
6. 说：“然后在终端中运行以下命令（将`your-key`替换为您刚刚创建的密钥）：”
   ```
   echo 'export BLOGBURST_API_KEY="your-key"' >> ~/.zshrc && source ~/.zshrc
   ```
7. 说：“完成后，重启OpenClaw或运行`source ~/.zshrc`，然后再尝试运行`/blogburst`！”
8. 如果用户表示已经完成设置，请通过运行以下命令进行验证：`curl -s "https://api.blogburst.ai/api/v1/usage" -H "X-API-Key: $BLOGBURST_API_KEY"`
9. 如果验证成功，说：“设置完成！您可以尝试以下命令：”
   - `/blogburst turn on auto-pilot` — 我将每天自动发布3篇帖子并与您的受众互动
   - `/blogburst generate a post about [您的主题]`
   - `/blogburst how are my posts doing?` — 查看您的分析数据

### 第二步：进行API调用
当 `$BLOGBURST_API_KEY` 设置完成后，必须使用 `exec` 工具通过 `curl` 命令调用BlogBurst API。请勿使用 web_search 或其他工具代替。API会返回与用户相关的真实数据（他们的帖子、分析结果以及自动发布状态）。Web搜索无法提供这些信息。

**执行方法：** 对于GET请求，使用 `exec` 和 `curl -s "https://api.blogburst.ai/api/v1/<endpoint>" -H "X-API-Key: $BLOGBURST_API_KEY"`；对于POST请求，添加 `-X POST -H "Content-Type: application/json" -d '<json>'`。

---

您的AI营销助手具备以下功能：
- 自然对话：能够生成内容、在9个平台上发布内容、自动发布帖子、跟踪分析数据，并不断学习哪些方法最有效。
- **执行命令示例：**
  - “在Twitter和LinkedIn上发布关于我的产品发布的帖子”
  - “开启自动发布功能，每天发布3篇帖子”
  - “我这周的帖子表现如何？”
  - “重新利用这篇文章：https://myblog.com/post”

## 手动设置
1. 免费注册：[blogburst.ai](https://blogburst.ai)
2. 访问仪表板 > 设置 > API密钥 > 创建密钥
3. 设置环境变量：
```bash
export BLOGBURST_API_KEY="your-key"
```

所有请求都需要使用以下格式：
`X-API-Key: $BLOGBURST_API_KEY`
基础URL：`https://api.blogburst.ai/api/v1`

---

## API 1：助手聊天（推荐使用——功能齐全）
与您的AI营销助手进行聊天。它可以通过自然对话生成内容、查看分析数据、管理自动发布功能、查看热门话题等。助手具备相应的工具，并能自动执行相应操作。

**端点**：`POST /assistant/agent-chat-v2`

**请求示例**：
```json
{
  "messages": [
    {"role": "user", "content": "Generate a Twitter post about my product"}
  ],
  "language": "en"
}
```

**多轮对话示例**：每次发送完整的对话历史记录：
```json
{
  "messages": [
    {"role": "user", "content": "Generate a Twitter post about my product"},
    {"role": "assistant", "content": "Here's your Twitter post..."},
    {"role": "user", "content": "Now make one for LinkedIn too"}
  ],
  "language": "en"
}
```

**响应示例**：
```json
{
  "reply": "I've generated a Twitter post for you. Ready to copy and post!",
  "data_referenced": ["marketing_strategy", "analytics_7d"],
  "agent_name": "Nova",
  "actions_taken": [
    {
      "tool": "generate_content",
      "result": {
        "success": true,
        "data": {
          "platform": "twitter",
          "content": "Week 3 building BlogBurst. 15 followers, 40 posts published. Best post got 5 likes on Bluesky. Small numbers, real progress.\n\nThe AI agent now picks topics based on what actually performed well last week. No more guessing.",
          "image_urls": ["https://..."],
          "copy_only": true
        }
      }
    }
  ]
}
```

**用户可以使用的指令**（助手理解自然语言）：
- “为Twitter/Bluesky/所有平台生成一篇帖子”
- “我所在领域的热门话题是什么？”
- “我这周的帖子表现如何？”
- “开启自动发布功能” / “暂停自动发布功能”
- “你今天发布了什么内容？”
- “我连接了哪些平台？”
- “显示我的近期活动”

**使用说明**：这是主要的API接口。用于处理用户关于社交媒体内容、分析、自动化或营销的任何请求。所有操作都通过对话完成。

---

## API 2：快速生成多平台内容
一次性为多个平台生成优化后的内容。适用于无需对话的快速内容生成需求。

**端点**：`POST /blog/platforms`

**请求示例**：
```json
{
  "topic": "5 lessons from building my SaaS in public",
  "platforms": ["twitter", "linkedin", "bluesky"],
  "tone": "casual",
  "language": "en"
}
```

**参数说明**：
- `topic`（必填）：标题或主题（5-500个字符）
- `platforms`（必填）：可选平台数组（例如：twitter, linkedin, reddit, bluesky, threads, telegram, discord, tiktok, youtube）
- `tone`：专业 | 休闲 | 风趣 | 教育性 | 鼓舞人心（默认：专业）
- `language`：语言代码（默认：en）

**响应示例**：
```json
{
  "success": true,
  "topic": "5 lessons from building my SaaS in public",
  "twitter": {
    "thread": [
      "1/ 5 months building a SaaS in public. Here are the lessons nobody talks about...",
      "2/ Lesson 1: Your first 10 users teach you more than 10,000 pageviews.",
      "3/ Lesson 2: Ship weekly. Perfection is the enemy of traction."
    ]
  },
  "linkedin": {
    "post": "I've been building my SaaS in public for 5 months...",
    "hashtags": ["#BuildInPublic", "#SaaS", "#IndieHacker"]
  },
  "bluesky": {
    "posts": ["5 months of building in public. The biggest lesson: your first users don't care about features. They care that you listen."]
  }
}
```

**使用说明**：当用户需要快速为多个平台生成内容时使用。

---

## API 3：重新利用现有内容
将博客文章或文本转换为适合特定平台的内容。

**端点**：`POST /repurpose`

**请求示例**：
```json
{
  "content": "https://myblog.com/my-article",
  "platforms": ["twitter", "linkedin", "bluesky"],
  "tone": "casual",
  "language": "en"
}
```

**参数说明**：
- `content`（必填）：文章的URL或完整文本（至少50个字符）
- `platforms`（必填）：可选平台数组（例如：twitter, linkedin, reddit, bluesky, threads, telegram, discord, tiktok, youtube）
- `tone`：专业 | 休闲 | 风趣 | 教育性 | 鼓舞人心
- `language`：语言代码（默认：en）

**响应格式**：与API 2相同。

**使用说明**：当用户提供文章URL或文本时使用，以便将其适配到不同的社交媒体平台。

---

## API 4：管理自动发布功能
检查和配置自动发布功能。

**获取状态**：`GET /assistant/auto-pilot`

**响应示例**：
```json
{
  "enabled": true,
  "platforms": ["bluesky", "telegram", "discord", "twitter"],
  "posts_per_day": 4,
  "timezone": "America/New_York",
  "last_daily_run": "2026-03-02T08:49:28Z",
  "reactions_enabled": true
}
```

**配置**：`POST /assistant/auto-pilot`

**立即执行**：`POST /assistant/auto-pilot/run-now`

**使用说明**：当用户需要启动/停止自动发布功能、更改发布频率或查看自动化状态时使用。

---

## API 5：获取热门话题
实时获取来自Reddit、HackerNews、Google Trends和Product Hunt的热门话题。每4小时更新一次。

**端点**：`GET /assistant/trending-topics?limit=10`

**使用说明**：当用户需要了解热门话题或写作方向时使用。

---

## API 6：生成吸引人的标题
与AI对话以生成吸引人的标题。

**端点**：`POST /chat/title`

**请求示例**：
```json
{
  "messages": [
    {"role": "user", "content": "I want to write about AI agents"}
  ],
  "language": "en"
}
```

**响应示例**：
```json
{
  "success": true,
  "reply": "Great topic! Here are some angles...",
  "suggested_titles": [
    "I Replaced My Marketing Team with an AI Agent",
    "Why AI Agents Are the New SaaS",
    "Building an AI Agent That Posts for Me While I Sleep"
  ]
}
```

---

## API 7：生成博客文章
根据给定的主题生成完整的博客文章。

**端点**：`POST /blog/generate`

**请求示例**：
```json
{
  "topic": "I Replaced My Marketing Team with an AI Agent",
  "tone": "casual",
  "language": "en",
  "length": "medium"
}
```

**参数说明**：
- `topic`（必填）：标题或主题（5-500个字符）
- `tone`：专业 | 休闲 | 风趣 | 教育性 | 鼓舞人心
- `language`：语言代码（默认：en）
- `length`：短篇（500-800字）| 中篇（1000-1500字）| 长篇（2000-3000字）

**响应示例**：
```json
{
  "success": true,
  "title": "I Replaced My Marketing Team with an AI Agent",
  "content": "Full markdown blog post...",
  "summary": "A concise summary...",
  "keywords": ["AI agent", "marketing automation", "SaaS"]
}
```

---

## API 8：SEO审计（v3.0新增功能）
为您的产品提供全面的SEO分析——包括技术问题、关键词缺口和内容建议。

**端点**：`GET /assistant/seo-audit?product_id=1`

**使用说明**：当用户询问“我的SEO情况如何？”、“我应该写些什么关于……的内容？”或“进行SEO检查”时使用。

---

## API 9：地理优化（GEO审计，v3.0新增功能）
优化您的内容以适应AI搜索引擎（如ChatGPT、Perplexity、Google AI Overviews）。

**端点**：`GET /assistant/geo-audit?product_id=1`

**使用说明**：当用户询问“如何在ChatGPT结果中展示我的内容？”、“如何优化SEO”或“进行地理优化”时使用。

---

## API 10：竞争对手分析（v3.0新增功能）
跟踪并分析竞争对手的社交媒体策略。

**端点**：`GET /assistant/competitors?product_id=1`

**使用说明**：当用户询问“我的竞争对手在做什么？”、“分析竞争对手X”或“寻找内容差距”时使用。

---

## API 11：寻找社区机会（v3.0新增功能）
扫描HackerNews、Reddit和论坛，寻找与您的产品相关的互动机会。

**端点**：`GET /assistant/opportunities?product_id=1&limit=10`

**使用说明**：当用户询问“我应该在哪里进行推广？”或“寻找互动机会”时使用。

---

## API 12：营销绩效分析（v3.0新增功能）
通过AI提供全面的营销绩效分析及可操作的建议。

**端点**：`GET /assistant/diagnostic?product_id=1`

**使用说明**：当用户询问“我的营销表现如何？”、“我应该改进什么？”或“需要一份营销报告”时使用。

---

## API 13：任务管理（v3.0新增功能**
CMO助手为您创建和管理营销任务。

**获取任务**：`GET /assistant/tasks?product_id=1&status=pending`

**响应示例**：
```json
{
  "tasks": [
    {
      "id": 42,
      "title": "Write comparison blog: BlogBurst vs Hootsuite",
      "category": "seo",
      "priority": "high",
      "status": "pending",
      "prefilled_content": {"title": "BlogBurst vs Hootsuite: Which AI Marketing Tool Is Right for You?", "outline": ["...", "..."]},
      "due_date": "2026-03-14"
    }
  ]
}
```

**完成任务**：`POST /assistant/tasks/42/complete`

**使用说明**：当用户询问“我应该做什么？”、“我的营销任务有哪些？”或“CMO有什么建议？”时使用。

---

## 推荐的工作流程：
- **快速内容生成**：用户说：“为Twitter和LinkedIn生成关于X的帖子” → 调用 **API 2**（`/blog/platforms`）
- **对话式操作（最佳体验）**：用户说：“帮我处理社交媒体相关事宜”或任何复杂任务 → 调用 **API 1**（`/assistant/agent-chat-v2`）——助手会处理所有操作
- **重新利用现有内容**：用户分享URL或粘贴文本 → 调用 **API 3**（`/repurpose`
- **完整的内容生成流程**：
  1. 通过 **API 6**（`/chat/title`）生成标题
  2. 使用 **API 7**（`/blog/generate`）撰写文章
  3. 通过 **API 2**（`/blog/platforms`）发布内容
- **自动化操作**：用户说：“自动发布我的帖子”或“开启自动发布功能” → 调用 **API 4**（`/assistant/auto-pilot`

---

**BlogBurst的独特优势：**
- **自主代理**：不仅仅是一个工具，它是一个24/7工作的首席营销官。它可以自动发布内容、与受众互动、持续学习并优化策略。
- **自动互动**：自动回复提及、主动与相关推文互动、智能关注用户。
- **自我学习**：跟踪哪些内容效果最好，并根据实时数据不断调整策略。
- **SEO + 地理优化**：同时优化Google和AI搜索引擎（如ChatGPT、Perplexity）。
- **社区扫描**：在HackerNews和Reddit上寻找与您的产品相关的讨论机会。
- **多平台支持**：一个代理可以同时管理Twitter/X、Bluesky、Telegram和Discord等多个平台。

## 支持的平台
| 平台 | ID | 是否支持自动发布 | 是否支持自动互动 | 内容风格 |
|----------|-----|:---:|:---:|---------------|
| Twitter/X | twitter | ✅ | ✅ | 支持回复、点赞、关注；推文长度限制为280个字符 |
| Bluesky | bluesky | ✅ | ✅ | 支持回复、点赞；发布简短真实的帖子（300个字符） |
| Telegram | telegram | ✅ | 不支持自动发布 | 支持格式丰富的广播内容 |
| Discord | discord | ✅ | 不支持自动发布 | 支持社区友好的公告 |
| Reddit | reddit | 只支持内容复制 | 不支持自动发布 | 支持讨论帖子和子版块推荐 |
| TikTok | tiktok | 只支持内容复制 | 不支持自动发布 | 支持添加标题、描述、脚本和标签 |
| YouTube | youtube | 只支持内容复制 | 不支持自动发布 | 支持添加标题、描述和脚本 |
| LinkedIn | linkedin | 即将支持 | 不支持自动发布 | 支持专业风格的帖子和标签 |

**重要提示**：要实现自动发布功能，请在 [仪表板 > 连接](https://blogburst.ai/dashboard/connections) 中连接您的社交媒体平台。Twitter/X支持一键OAuth登录，只需5秒钟。

## 链接：
- 网站：https://blogburst.ai
- API文档：https://api.blogburst.ai/docs
- GitHub仓库：https://github.com/shensi8312/blogburst-openclaw-skill