---
name: BlogBurst
description: AI内容创作与分发：帮助用户构思文章标题、生成博客文章，并为9个平台（Twitter、LinkedIn、Bluesky、Telegram、Discord、Reddit、TikTok、YouTube、Threads）生成优化后的内容。
homepage: https://blogburst.ai
metadata:
  {"openclaw": {"emoji": "📝", "requires": {"env": ["BLOGBURST_API_KEY"]}, "primaryEnv": "BLOGBURST_API_KEY"}}
---

# BlogBurst - 人工智能内容创作与分发工具

BlogBurst 可帮助您将创意转化为在 9 个社交媒体平台上发布的实际内容。典型的工作流程如下：

1. **头脑风暴**：通过 AI 聊天功能生成文章标题。
2. **生成**：根据选定的标题生成完整的博客文章。
3. **创建**：为 Twitter、LinkedIn、TikTok 等平台生成适配的内容。

您也可以通过提供文章的 URL 来重新利用现有内容。

## 设置

1. 在 [blogburst.ai](https://blogburst.ai) 注册账号。
2. 进入“控制面板”（Dashboard），然后选择“API 密钥”（API Keys）以生成 API 密钥。
3. 设置环境变量：
```bash
export BLOGBURST_API_KEY="your-key"
```

所有 API 请求都需要在请求头中添加以下字段：`X-API-Key: $BLOGBURST_API_KEY`

基础 URL：`https://api.blogburst.ai/api/v1`

---

## API 1：头脑风暴标题

与 AI 对话，以为您的内容想出一个吸引人的标题。

**端点**：`POST /chat/title`

**请求数据**：
```json
{
  "messages": [
    {"role": "user", "content": "I want to write about AI in healthcare"}
  ],
  "language": "en"
}
```

这是一个多轮对话过程。每次发送对话内容时都需要包含完整的对话历史记录：
```json
{
  "messages": [
    {"role": "user", "content": "I want to write about AI in healthcare"},
    {"role": "assistant", "content": "Great topic! What aspect interests you most?"},
    {"role": "user", "content": "AI helping doctors diagnose diseases faster"}
  ],
  "language": "en"
}
```

**响应数据**：
```json
{
  "success": true,
  "reply": "Here are some title ideas based on AI-assisted diagnosis...",
  "suggested_titles": [
    "How AI Detects What Doctors Miss in 5 Seconds",
    "Medical AI: From Assistant to Lifesaver",
    "When AI Becomes Your First Doctor"
  ],
  "usage": {"tokens_used": 350, "cost": 0.001, "model": "gemini-2.5-flash"}
}
```

**使用场景**：当用户需要帮助确定主题或标题时，或者输入类似“帮我想个标题”、“我该写些什么”之类的请求时。

---

## API 2：生成博客文章

根据给定的主题或标题生成完整的博客文章。

**端点**：`POST /blog/generate`

**请求数据**：
- `topic`（必填）：文章的主题或标题（5-500 个字符）
- `tone`：专业 | 休闲 | 诙谐 | 教育性 | 鼓舞人心（默认：专业）
- `language`：语言代码（例如：en, zh）（默认：en）
- `length`：简短（500-800 字）| 中等（1000-1500 字）| 长篇（2000-3000 字）（默认：中等）

**响应数据**：
```json
{
  "success": true,
  "title": "How AI Detects What Doctors Miss in 5 Seconds",
  "content": "Full markdown blog post content here...",
  "summary": "A concise summary of the article...",
  "keywords": ["AI", "healthcare", "diagnosis", "medical AI"],
  "usage": {"tokens_used": 2500, "cost": 0.005, "model": "gemini-2.5-flash"}
}
```

**使用场景**：当用户希望根据某个主题生成博客文章或长篇内容时。

---

## API 3：为多个平台生成适配内容

根据给定的主题为多个社交媒体平台生成适配的内容。这是主要的内容分发接口。

**端点**：`POST /blog/platforms`

**请求数据**：
- `topic`（必填）：文章的主题或标题（5-500 个字符）
- `platforms`（必填）：需要生成内容的平台列表（1-9 个平台，例如：twitter, linkedin, reddit, bluesky, telegram, discord, tiktok, youtube）
- `tone`：专业 | 休闲 | 诙谐 | 教育性 | 鼓舞人心（默认：专业）
- `language`：语言代码（默认：en）

**响应数据**：
```json
{
  "success": true,
  "topic": "How AI Detects What Doctors Miss in 5 Seconds",
  "twitter": {
    "thread": [
      "1/ AI can now detect diseases that doctors miss. Here's how it's saving lives...",
      "2/ A study found AI caught 95% of early-stage cancers, vs 85% for radiologists.",
      "3/ The key? AI analyzes millions of images. A doctor sees thousands in a lifetime."
    ]
  },
  "linkedin": {
    "post": "I've been researching AI in healthcare for 2 years.\n\nThe results are staggering...",
    "hashtags": ["#AIHealthcare", "#MedTech", "#DigitalHealth"]
  },
  "bluesky": {
    "posts": ["AI is quietly revolutionizing medical diagnosis. Here's what most people don't know..."]
  },
  "telegram": {
    "post": "**AI in Medical Diagnosis: The Silent Revolution**\n\nDoctors are getting a powerful new ally..."
  },
  "discord": {
    "post": "Hey everyone! Wanted to share something fascinating about AI in healthcare..."
  },
  "reddit": {
    "title": "How AI is detecting diseases doctors miss - a deep dive",
    "body": "I've been following AI in healthcare closely and wanted to share...",
    "suggestedSubreddits": ["r/artificial", "r/healthcare", "r/technology"]
  },
  "tiktok": {
    "hook": "Did you know AI can detect cancer faster than a doctor?",
    "script": "Here's something wild. AI systems can now...",
    "caption": "AI is changing medicine forever",
    "hashtags": ["#AI", "#Healthcare", "#MedTech", "#Science"]
  },
  "youtube": {
    "title": "How AI Detects What Doctors Miss",
    "description": "In this video, we explore how artificial intelligence...",
    "script": "What if I told you that an AI can spot a disease...",
    "tags": ["AI healthcare", "medical AI", "diagnosis"]
  },
  "usage": {"tokens_used": 3000, "cost": 0.006, "model": "gemini-2.5-flash"}
}
```

**使用场景**：当用户希望为多个平台创建社交媒体帖子或分发内容时，或者输入类似“为 Twitter 和 LinkedIn 生成相关内容”之类的请求时。

---

## API 4：重新利用现有内容

将现有的博客文章或文本转换为适用于特定平台的内容。

**端点**：`POST /repurpose`

**通过 URL 传递请求数据**：
```json
{
  "content": "https://myblog.com/my-article",
  "platforms": ["twitter", "linkedin", "bluesky"],
  "tone": "casual",
  "language": "en"
}
```

**通过文本传递请求数据**：
```json
{
  "content": "Your full article text here (minimum 50 characters)...",
  "platforms": ["twitter", "linkedin", "bluesky"],
  "tone": "casual",
  "language": "en"
}
```

**请求参数**：
- `content`（必填）：文章的 URL 或文本内容
- `platforms`（必填）：需要生成内容的平台列表（例如：twitter, linkedin, reddit, bluesky）
- `tone`：专业 | 休闲 | 诙谐 | 教育性 | 鼓舞人心
- `language`：语言代码（默认：en）

**响应数据**：返回的结果将与 API 3 的响应格式相同，但会针对每个平台进行个性化处理。

**使用场景**：当用户提供文章 URL 或直接提供文本内容，并希望将其适配到特定平台时。

---

## API 5：将内容发布到已连接的平台

将内容直接发布到用户已连接的社交媒体账户。

**重要提示**：在使用此 API 之前，用户必须先在 [blogburst.ai/dashboard/connections](https://blogburst.ai/dashboard/connections) 连接他们的社交媒体账户。如果没有连接任何账户，发布操作将失败。

### 检查已连接的账户

**端点**：`GET /publish/connected`

**响应数据**：
```json
{
  "platforms": [
    {
      "platform": "bluesky",
      "username": "@user.bsky.social",
      "connected_at": "2026-02-01T10:00:00Z",
      "capabilities": {"text": true, "images": true, "video": true}
    },
    {
      "platform": "telegram",
      "username": "MyChannel",
      "connected_at": "2026-02-01T10:00:00Z",
      "capabilities": {"text": true, "images": true, "video": true}
    }
  ]
}
```

**使用场景**：在发布内容之前，调用此接口查看用户已连接的平台。如果没有连接的账户，请提示用户先访问 [https://blogburst.ai/dashboard/connections] 连接账户。

### 发布内容

**端点**：`POST /publish`

**请求数据**：
- `platforms`（必填）：需要发布内容的平台 ID 列表
- `content`（必填）：要发布的内容文本
- `image_urls`（可选）：要附带的图片 URL 列表
- `video_url`（可选）：要附带的视频 URL
- `reddit_subreddit`（可选）：Reddit 帖子的子版块名称
- `reddit_title`（可选）：Reddit 帖子的标题

**响应数据**：
```json
{
  "total": 3,
  "successful": 2,
  "failed": 1,
  "results": [
    {"platform": "bluesky", "success": true, "post_url": "https://bsky.app/..."},
    {"platform": "telegram", "success": true, "post_url": "https://t.me/..."},
    {"platform": "discord", "success": false, "error": "Webhook expired"}
  ]
}
```

**使用场景**：在使用 API 3 或 API 4 生成内容后，当用户希望将这些内容发布到已连接的平台时。请务必先使用 `GET /publish/connected` 检查已连接的账户。

---

## 推荐的工作流程

为获得最佳效果，请按照以下步骤操作：

1. 询问用户希望创作的内容主题。
2. 调用 **API 1**（`/chat/title`）共同头脑风暴标题。
3. 选定标题后，调用 **API 3**（`/blog/platforms`）为选定的平台生成内容。
4. 将生成的内容按平台分类展示给用户。
5. 如果用户希望发布内容，请先调用 `GET /publish/connected` 检查已连接的账户。
6. 如果有连接的账户，再调用 **API 5**（`/publish`）为每个平台发布内容。
7. 如果没有连接的账户，请提示用户：“请先在 [https://blogburst.ai/dashboard/connections] 连接您的社交媒体账户”。

如果用户已有博客文章的 URL，可以直接使用 **API 4**（`/repurpose`）。

如果用户希望先生成完整的博客文章，可以在步骤 3 之前使用 **API 2**（`/blog/generate`）。

**关于发布**：每个平台都会收到针对其特性进行个性化处理的内容。例如，将 Twitter 的帖子内容发送到 Twitter，将 LinkedIn 的帖子内容发送到 LinkedIn 等。切勿将相同的原始内容发送到所有平台——请使用 API 3 为每个平台生成的适配后的内容。

## 支持的平台

| 平台 | ID | 是否支持生成内容 | 是否支持自动发布 | 备注 |
|----------|-----|------------------|----------------------|
| Twitter/X | twitter | 是 | 是 | 支持带有链接的推文（每条推文 280 个字符） |
| LinkedIn | linkedin | 是 | 即将支持 | 包含专业见解和标签 |
| Bluesky | bluesky | 是 | 是 | 支持简短且真实的帖子（300 个字符） |
| Telegram | telegram | 是 | 是 | 支持格式丰富的信息推送 |
| Discord | discord | 是 | 是 | 适合社区发布的公告 |
| Reddit | reddit | 是 | API 尚在开发中 | 支持讨论帖子和子版块推荐 |
| TikTok | tiktok | 是 | 是 | 支持包含链接、脚本、标题和标签的帖子 |
| YouTube | youtube | 是 | 是 | 支持标题、描述、脚本和标签 |
| Threads | threads | 是 | 即将支持 | 支持对话式帖子 |

## 相关链接

- 网站：https://blogburst.ai
- API 文档：https://api.blogburst.ai/docs
- 账户连接：https://blogburst.ai/dashboard/connections
- GitHub 仓库：https://github.com/shensi8312/blogburst-openclaw-skill