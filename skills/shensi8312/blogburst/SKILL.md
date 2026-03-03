---
name: BlogBurst - AI Social Media Agent
description: >
  **自主AI营销代理**  
  能够自然地进行对话，生成内容，管理自动化营销流程，查看分析数据，并将内容发布到9个平台（Twitter/X、LinkedIn、Bluesky、Telegram、Discord、Reddit、TikTok、YouTube、Threads）。只需一个命令，即可实现整个社交媒体管理的自动化。
homepage: https://blogburst.ai
metadata:
  {"openclaw": {"emoji": "🚀", "requires": {"env": ["BLOGBURST_API_KEY"]}, "primaryEnv": "BLOGBURST_API_KEY"}}
---
# BlogBurst – 人工智能社交媒体营销助手

这是一个自主运行的AI营销工具，能够自然地与用户交流：生成内容、发布到多个平台、自动执行每日发布任务、跟踪分析数据，并不断学习哪些方法最有效。

**只需一句话，即可完成各种操作：**
- “在Twitter和LinkedIn上发布关于我的产品发布的信息”
- “开启自动发布功能，每天发布3条帖子”
- “我这周的帖子表现如何？”
- “重新利用这篇文章：https://myblog.com/post”

## 设置

1. 免费注册 [blogburst.ai](https://blogburst.ai)
2. 进入控制面板 > 设置 > API密钥 > 创建新的API密钥
3. 设置环境变量：
```bash
export BLOGBURST_API_KEY="your-key"
```

所有请求都需要使用以下参数：
`X-API-Key: $BLOGBURST_API_KEY`
基础URL：`https://api.blogburst.ai/api/v1`

---

## API 1：代理聊天（推荐使用——功能齐全）

与您的AI营销助手进行对话。它能够生成内容、查看分析数据、管理自动发布任务、查看热门话题等——所有操作都通过自然语言对话完成。助手具备相应的工具，并能自动执行相应操作。

**端点**：`POST /assistant/agent-chat-v2`

**请求格式**：
```json
{
  "messages": [
    {"role": "user", "content": "Generate a Twitter post about my product"}
  ],
  "language": "en"
}
```

**多轮对话**：每次发送时都需要提供完整的对话历史记录：
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

**响应格式**：
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

**用户可以使用的指令**（助手能理解自然语言）：
- “为Twitter/Bluesky/LinkedIn等所有平台生成一篇帖子”
- “我所在领域的热门话题是什么？”
- “我这周的帖子效果如何？”
- “开启自动发布功能” / “暂停自动发布”
- “你今天发布了什么内容？”
- “我关联了哪些平台？”
- “显示我的近期活动”

**使用场景**：这是主要的API接口，适用于任何关于社交媒体内容、分析、自动化或营销的请求。所有操作都通过对话形式完成。

---

## API 2：为多个平台生成内容（快速一次性生成）

一次性为多个平台生成优化后的内容。适用于无需对话的快速内容生成需求。

**端点**：`POST /blog/platforms`

**请求参数**：
- `topic`（必填）：主题或标题（5-500个字符）
- `platforms`（必填）：可选平台列表（例如：twitter, linkedin, reddit, bluesky, threads, telegram, discord, tiktok, youtube）
- `tone`：风格（专业 | 休闲 | 诙谐 | 教育性 | 鼓舞人心）（默认：专业）
- `language`：语言代码（默认：en）

**响应格式**：
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

**使用场景**：当用户需要快速为多个平台生成特定主题的内容时。

---

## API 3：重新利用现有内容

将博客文章或文本转换为适合特定平台发布的格式。

**端点**：`POST /repurpose`

**请求参数**：
- `content`（必填）：文章的URL或文本内容（至少50个字符）
- `platforms`（必填）：目标平台列表（例如：twitter, linkedin, reddit, bluesky, threads, telegram, discord, tiktok, youtube）
- `tone`：风格（专业 | 休闲 | 诙谐 | 教育性 | 鼓舞人心）
- `language`：语言代码（默认：en）

**响应格式**：与API 2相同

**使用场景**：当用户提供文章链接或文本时，可以使用该接口将其适配到不同的社交媒体平台上。

---

## API 4：自动发布管理

用于检查和配置自动发布功能。

**获取状态**：`GET /assistant/auto-pilot`

**响应格式**：
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

**配置自动发布**：`POST /assistant/auto-pilot`

**立即运行**：`POST /assistant/auto-pilot/run-now`

**使用场景**：用户需要启动或停止自动发布功能、调整发布频率或查看自动化状态时使用。

---

## API 5：热门话题

实时获取来自Reddit、HackerNews、Google Trends和Product Hunt的热门话题。更新频率为每4小时一次。

**端点**：`GET /assistant/trending-topics?limit=10`

**使用场景**：用户需要了解当前的热门话题或写作素材时使用。

---

## API 6：创意标题生成

与AI对话以生成吸引人的标题。

**端点**：`POST /chat/title`

**请求参数**：
```json
{
  "messages": [
    {"role": "user", "content": "I want to write about AI agents"}
  ],
  "language": "en"
}
```

**响应格式**：
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

**请求参数**：
- `topic`（必填）：主题或标题（5-500个字符）
- `tone`：风格（专业 | 休闲 | 诙谐 | 教育性 | 鼓舞人心）
- `language`：语言代码（默认：en）
- `length`：文章长度（短篇：500-800字 | 中篇：1000-1500字 | 长篇：2000-3000字）

**响应格式**：
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

## 推荐工作流程

### 快速内容生成
用户请求：**“为Twitter和LinkedIn生成关于X的文章”**
→ 调用 **API 2**（`/blog/platforms`）

### 对话式操作（最佳体验）
用户请求：**“帮我处理社交媒体相关事务”** 或任何复杂任务
→ 调用 **API 1**（`/assistant/agent-chat-v2`）——助手会完成所有操作

### 重新利用现有内容
用户提供文章链接或文本内容
→ 调用 **API 3**（`/repurpose`）

### 完整的内容生成流程
1. 使用 **API 6**（`/chat/title`）生成创意标题
2. 使用 **API 7**（`/blog/generate`）撰写文章
3. 使用 **API 2**（`/blog/platforms`）将文章发布到目标平台

### 自动化操作
用户请求：**“自动发布我的内容”** 或 **“开启自动发布功能”**
→ 调用 **API 4**（`/assistant/auto-pilot`）

## 支持的平台

| 平台 | ID | 是否支持自动发布 | 内容格式 |
|----------|-----|:---:|---------------|
| Twitter/X | twitter | 不支持 | 需手动发布，但支持特定格式（每条推文280个字符） |
| LinkedIn | linkedin | 即将支持 | 专业风格的内容 + 标签 |
| Bluesky | bluesky | 支持 | 简短且真实的帖子（300个字符） |
| Telegram | telegram | 支持 | 格式丰富的信息推送 |
| Discord | discord | 支持 | 适合社区的发布公告 |
| Reddit | reddit | 需手动发布 | 包含讨论帖子和子版块推荐 |
| TikTok | tiktok | 需手动发布 | 包含标题、描述、脚本和标签 |
| YouTube | youtube | 需手动发布 | 包含标题、描述和脚本 |

## 链接

- 官网：https://blogburst.ai
- API文档：https://api.blogburst.ai/docs
- GitHub仓库：https://github.com/shensi8312/blogburst-openclaw-skill