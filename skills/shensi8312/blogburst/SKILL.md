---
name: BlogBurst - AI Social Media Agent
description: 自主AI营销代理：能够自然地进行聊天交流以生成内容，管理自动化流程，查看分析数据，并将内容发布到9个平台（Twitter/X、LinkedIn、Bluesky、Telegram、Discord、Reddit、TikTok、YouTube、Threads）。只需一个命令，即可实现整个社交媒体的自动化管理。
homepage: https://blogburst.ai
metadata:
  {"openclaw": {"emoji": "🚀", "requires": {"env": ["BLOGBURST_API_KEY"]}, "primaryEnv": "BLOGBURST_API_KEY"}}
---
# BlogBurst – 人工智能社交媒体营销代理

## 重要提示：请务必遵循以下步骤：

### 第一步：检查 API 密钥
在开始任何操作之前，请运行以下命令：`echo $BLOGBURST_API_KEY`

**如果输出为空或变量未设置**，请不要继续进行 API 调用。此时，应指导用户完成设置：
1. 说：“欢迎使用 BlogBurst！🚀 让我帮助您完成设置，整个过程只需 30 秒。”
2. 说：“首先，注册一个免费账户（每月可生成 50 条内容）：” 并提供注册链接：https://blogburst.ai
3. 说：“登录后，前往 **仪表板 > 设置 > API 密钥**，然后点击‘创建密钥’。”
4. 说：“接下来在终端中运行以下命令（将 `your-key` 替换为您刚刚创建的密钥）：”
   ```
   echo 'export BLOGBURST_API_KEY="your-key"' >> ~/.zshrc && source ~/.zshrc
   ```
5. 说：“完成后，重启 OpenClaw 或运行 `source ~/.zshrc`，然后再尝试运行 `/blogburst`！”
6. 如果用户表示已经完成设置，请通过运行以下命令进行验证：`curl -s "https://api.blogburst.ai/api/v1/usage" -H "X-API-Key: $BLOGBURST_API_KEY"`
7. 如果验证成功，说：“设置完成！现在可以尝试运行 `/blogburst generate a post about [topic]` 来生成关于 [topic] 的帖子。”

### 第二步：进行 API 调用
当 `$BLOGBURST_API_KEY` 已设置好后，必须使用 `exec` 工具通过 `curl` 命令调用 BlogBurst API。严禁使用其他工具替代。API 可返回与用户相关的实际数据（如用户的帖子、分析结果以及自动发布状态）。网络搜索无法提供这些信息。

**执行方法：** 对于 GET 请求，使用 `exec` 命令：`exec curl -s "https://api.blogburst.ai/api/v1/<endpoint>" -H "X-API-Key: $BLOGBURST_API_KEY"`；对于 POST 请求，添加 `-X POST -H "Content-Type: application/json" -d '<json>'`。

---

您的智能营销代理能够自然地与用户交流：它能够生成内容、发布到多个平台、自动执行每日发布任务、跟踪分析数据，并不断学习哪些方法最有效。

**用户可以使用以下命令来执行特定操作：**
- “在 Twitter 和 LinkedIn 上发布关于我的产品发布的帖子”
- “开启自动发布功能，每天发布 3 条帖子”
- “我的帖子这周的表现如何？”
- “重新利用这篇文章：https://myblog.com/post”

## 手动设置步骤
1. 在 [blogburst.ai](https://blogburst.ai) 注册免费账户
2. 访问仪表板 > 设置 > API 密钥 > 创建密钥
3. 设置环境变量：
```bash
export BLOGBURST_API_KEY="your-key"
```

所有请求都需要使用以下参数：`X-API-Key: $BLOGBURST_API_KEY`
基础 URL：`https://api.blogburst.ai/api/v1`

---

## API 1：代理聊天（推荐使用——可完成所有操作）
您可以与您的智能营销代理进行对话。它能够生成内容、查看分析数据、管理自动发布功能、查看热门话题等——所有操作均通过自然语言对话完成。代理具备自动执行任务的能力。

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

**多轮对话流程**：每次发送对话时都需要提供完整的对话历史记录：
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

**用户可以使用的指令**（代理理解自然语言）：
- “为 Twitter/Bluesky/LinkedIn 等平台生成一篇帖子”
- “我所在领域目前的热门话题是什么？”
- “我的帖子这周的表现如何？”
- “开启自动发布功能” / “暂停自动发布功能”
- “你今天发布了什么内容？”
- “我关联了哪些平台？”
- “显示我的近期活动”

**使用场景**：这是主要的 API，适用于用户关于社交媒体内容、分析、自动化或营销方面的所有请求。所有操作均通过对话方式完成。

---

## API 2：快速生成多平台内容
可以一次性为多个平台生成优化后的内容。适用于无需对话的快速内容生成需求。

**端点**：`POST /blog/platforms`

**请求格式**：
```json
{
  "topic": "5 lessons from building my SaaS in public",
  "platforms": ["twitter", "linkedin", "bluesky"],
  "tone": "casual",
  "language": "en"
}
```

**参数**：
- `topic`（必填）：帖子的标题或主题（5-500 个字符）
- `platforms`（必填）：需要发布的平台数组（例如：twitter, linkedin, reddit, bluesky, threads, telegram, discord, tiktok, youtube）
- `tone`：风格（professional | casual | witty | educational | inspirational，默认为 professional）
- `language`：语言代码（默认为 en）

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

**使用场景**：当用户需要快速为多个平台生成内容时使用。

---

## API 3：重新利用现有内容
可以将博客文章或文本转换为适合特定平台发布的格式。

**端点**：`POST /repurpose`

**请求格式**：
```json
{
  "content": "https://myblog.com/my-article",
  "platforms": ["twitter", "linkedin", "bluesky"],
  "tone": "casual",
  "language": "en"
}
```

**参数**：
- `content`（必填）：文章的 URL 或文本内容（至少 50 个字符）
- `platforms`（必填）：需要发布的平台数组（例如：twitter, linkedin, reddit, bluesky, threads, telegram, discord, tiktok, youtube）
- `tone`：风格（professional | casual | witty | educational | inspirational）
- `language`：语言代码（默认为 en）

**响应格式**：与 API 2 相同

**使用场景**：当用户提供文章 URL 或文本时，可以使用该 API 将其转换为适合多个平台的格式。

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

**执行命令**：`POST /assistant/auto-pilot/run-now`

**使用场景**：当用户需要启动/停止自动发布功能、更改发布频率或查看自动发布状态时使用。

---

## API 5：获取热门话题
实时获取来自 Reddit、HackerNews、Google Trends 和 Product Hunt 的热门话题。数据每 4 小时更新一次。

**端点**：`GET /assistant/trending-topics?limit=10`

**使用场景**：当用户想了解当前的热门话题或写作主题时使用。

---

## API 6：创意标题生成
与 AI 对话以生成吸引人的标题。

**端点**：`POST /chat/title`

**请求格式**：
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

**请求格式**：
```json
{
  "topic": "I Replaced My Marketing Team with an AI Agent",
  "tone": "casual",
  "language": "en",
  "length": "medium"
}
```

**参数**：
- `topic`（必填）：帖子的标题或主题（5-500 个字符）
- `tone`：风格（professional | casual | witty | educational | inspirational）
- `language`：语言代码（默认为 en）
- `length`：文章长度（short: 500-800 字；medium: 1000-1500 字；long: 2000-3000 字）

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

## 推荐的工作流程：
- **快速内容生成**：用户请求“为 Twitter 和 LinkedIn 生成相关帖子” → 调用 API 2（`/blog/platforms`）
- **对话式交互**：用户请求“帮助我处理社交媒体相关事务”或其他复杂任务 → 调用 API 1（`/assistant/agent-chat-v2`）——代理将完成所有操作
- **重新利用现有内容**：用户提供文章 URL 或文本 → 调用 API 3（`/repurpose`）
- **完整的内容生成流程**：
  1. 使用 API 6（`/chat/title`）生成创意标题
  2. 使用 API 7（`/blog/generate`）撰写文章
  3. 使用 API 2（`/blog/platforms`）将文章发布到相应平台
- **自动化操作**：用户请求“自动发布内容”或“开启自动发布功能” → 调用 API 4（`/assistant/auto-pilot`）

## 支持的平台
| 平台 | ID | 是否支持自动发布 | 内容格式 |
|----------|-----|:---:|---------------|
| Twitter/X | twitter | 不支持自动发布 | 需手动发布，每条帖子长度限制为 280 个字符 |
| LinkedIn | linkedin | 即将支持自动发布 | 提供专业见解和标签 |
| Bluesky | bluesky | 支持自动发布 | 短篇真实风格的帖子（300 个字符） |
| Telegram | telegram | 支持自动发布 | 提供格式丰富的信息发布 |
| Discord | discord | 支持自动发布 | 适合社区发布的公告 |
| Reddit | reddit | 不支持自动发布 | 需手动发布，提供讨论帖子和子版块推荐 |
| TikTok | tiktok | 不支持自动发布 | 需手动发布，包含标题、描述、脚本和标签 |
| YouTube | youtube | 不支持自动发布 | 需手动发布，包含标题、描述和脚本 |

## 相关链接：
- 官网：https://blogburst.ai
- API 文档：https://api.blogburst.ai/docs
- GitHub 仓库：https://github.com/shensi8312/blogburst-openclaw-skill