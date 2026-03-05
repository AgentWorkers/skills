---
name: LinkedIn Content Creation Skill by Reepl
description: 使用 Reepl 管理您的 LinkedIn 账户：您可以创建帖子草稿、发布并安排发布时间、管理联系人和收藏夹、生成 AI 图片、创建轮播图、在 Twitter/X 上发布内容，以及维护您的语音资料。需要一个 Reepl 账户（reepl.io）。
homepage: https://reepl.io
metadata: {"openclaw":{"requires":{"env":["REEPL_MCP_KEY"]},"primaryEnv":"REEPL_MCP_KEY"}}
---
# 通过Reepl创建LinkedIn内容

通过Reepl的MCP集成，实现全面的LinkedIn内容管理。您可以用自己的真实声音撰写帖子、安排发布时间、管理草稿、生成AI图片、创建轮播图、发布到Twitter/X，以及浏览保存的内容库——所有这些都可以通过您的AI助手完成。

## 先决条件

1. **Reepl账户**——在[reepl.io](https://reepl.io)注册
2. **MCP连接**——通过OAuth连接您的账户（详见下面的设置指南）
3. **Gemini API密钥**（可选）——仅用于生成AI图片，可在[设置 > AI模型](https://app.reepl.io/settings/ai-models-api)获取链接

## 设置指南

```
# 1. Visit the OAuth page to connect your Reepl account
https://mcp.reepl.io/oauth/authorize

# 2. Log in with your Reepl credentials (Google or email)

# 3. Copy the API key shown after authorization

# 4. Configure the MCP server endpoint
https://mcp.reepl.io/mcp?key=YOUR_API_KEY
```

如果在任何步骤中遇到认证错误，请在上面的URL重新认证。

---

## 可用工具（共31个）

| 工具 | 功能 |
|------|---------|
| `create_draft` | 保存新的LinkedIn帖子草稿 |
| `get_drafts` | 列出并搜索您的草稿 |
| `update_draft` | 编辑现有的草稿 |
| `delete_draft` | 删除草稿 |
| `publish_to_linkedin` | 立即将帖子发布到LinkedIn |
| `schedule_post` | 将帖子安排在未来发布 |
| `update_scheduled_post` | 更改已安排帖子的时间、内容或设置 |
| `delete_scheduled_post` | 取消并删除已安排的帖子 |
| `publish_now` | 立即发布已安排的帖子 |
| `schedule_draft` | 安排现有草稿的发布时间 |
| `get_published_posts` | 查看您已发布的LinkedIn帖子 |
| `get Scheduled_posts` | 查看已安排的帖子队列 |
| `add_comment_to_post` | 为已发布的帖子添加评论 |
| `get_user_profile` | 获取您的Reepl账户信息 |
| `get_voice_profile` | 读取您的语音档案（写作风格模式） |
| `update_voice_profile` | 使用学习到的模式更新语音档案 |
| `get_contacts` | 浏览保存的LinkedIn联系人 |
| `get_lists` | 浏览您的联系人列表 |
| `get_list_contacts` | 获取特定列表中的联系人 |
| `add_contact_to_list` | 将联系人添加到列表中 |
| `get_collections` | 浏览您保存的帖子集合 |
| `get_saved_posts` | 从特定集合中读取帖子 |
| `get_templates` | 浏览您的帖子模板和创意 |
| `generate_image` | 为帖子生成AI图片（需要Gemini API密钥） |
| `generate_carousel_content` | 为轮播图生成AI幻灯片内容 |
| `list_carousel_drafts` | 列出保存的轮播图草稿 |
| `get_carousel_draft` | 获取特定的轮播图草稿 |
| `create_carousel_draft` | 保存新的轮播图草稿 |
| `update_carousel_draft` | 编辑现有的轮播图草稿 |
| `delete_carousel_draft` | 删除轮播图草稿 |
| `twitter_create_post` | 创建或安排Twitter/X帖子或帖子串 |

---

## 内容规则

所有LinkedIn内容必须为纯文本。切勿使用**粗体**、*斜体*或#标题等Markdown格式。LinkedIn不支持Markdown格式——这些格式会原样显示在动态中，看起来像是AI生成的。请使用换行符、间距和自然标点符号来组织内容。

LinkedIn帖子的长度限制为3000个字符。

---

## 工具参考

### 1. 创建草稿

保存一个帖子草稿，以便稍后编辑或发布。

```json
{
  "content": "Just wrapped up a deep dive into how AI is reshaping B2B sales.\n\nHere are 3 things I learned...",
  "title": "AI in B2B Sales",
  "mediaUrls": ["https://example.com/image.jpg"]
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `content` | 是 | 帖子文本（仅限纯文本） |
| `title` | 否 | 草稿的标题（用于组织） |
| `mediaUrls` | 否 | 要附加的图片URL数组 |

### 2. 获取草稿

列出并搜索您保存的草稿。

```json
{
  "search": "AI sales",
  "limit": 10
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `limit` | 否 | 返回的草稿数量（默认：20个） |
| `search` | 否 | 按关键词过滤草稿 |

### 3. 更新草稿

编辑现有草稿的内容、标题或图片。

```json
{
  "draft_id": "abc-123",
  "content": "Updated post content here...",
  "title": "New Title"
}
```

| 参数 | 必需 | 说明 |
| `draft_id` | 是 | 要更新的草稿ID |
| `content` | 否 | 更新后的帖子文本 |
| `title` | 否 | 更新后的标题 |
| `mediaUrls` | 否 | 更新后的图片URL（替换现有图片） |

### 4. 删除草稿

```json
{
  "draft_id": "abc-123"
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `draft_id` | 是 | 要删除的草稿ID |

---

### 5. 发布到LinkedIn

立即将帖子发布到LinkedIn。此操作不可撤销——在调用之前请务必获得用户的确认。

```json
{
  "content": "Excited to share that we just hit 10,000 users on Reepl!\n\nBuilding in public has been one of the best decisions we made.\n\nHere's what I'd tell founders who are hesitant to share their journey...",
  "visibility": "PUBLIC"
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `content` | 是 | 帖子文本（仅限纯文本，最多3000个字符） |
| `mediaUrls` | 否 | 要包含的图片URL数组 |
| `visibility` | 否 | `PUBLIC`（默认）或`CONNECTIONS` |

### 6. 安排帖子

将帖子安排在未来发布。时间以15分钟为间隔进行四舍五入。

```json
{
  "content": "Monday motivation: the best time to start was yesterday. The second best time is now.",
  "scheduledFor": "2026-02-17T08:00:00Z",
  "visibility": "PUBLIC"
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `content` | 是 | 帖子文本（仅限纯文本，最多3000个字符） |
| `scheduledFor` | 是 | ISO 8601时间戳（例如 `2026-02-17T08:00:00Z`） |
| `mediaUrls` | 否 | 图片URL数组 |
| `visibility` | 否 | `PUBLIC`（默认）或`CONNECTIONS` |

**安排帖子的建议：**
- 询问用户偏好的时间，而不是自行选择。
- 如果他们需要建议，可以推荐不同的时间段：清晨（7-8 AM）、午餐时间（12-1 PM）或傍晚（5-6 PM）。
- 避免同时安排所有帖子的发布时间——分散时间以提高互动率。

### 7. 更新已安排的帖子

更改已安排帖子的时间、内容、可见性或图片。

```json
{
  "post_id": "post-456",
  "scheduledFor": "2026-02-18T12:30:00Z",
  "content": "Updated content for the scheduled post..."
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `post_id` | 是 | 已安排帖子的ID |
| `scheduledFor` | 否 | 新的ISO 8601时间戳 |
| `content` | 否 | 更新后的帖子文本 |
| `visibility` | 否 | 更新后的可见性 |
| `mediaUrls` | 否 | 更新后的图片URL（替换现有图片） |

### 8. 取消并删除已安排的帖子

取消并删除已安排的帖子。仅适用于状态为`scheduled`、`failed`或`pending_approval`的帖子。已发布的帖子无法通过此方式删除。

```json
{
  "post_id": "post-456"
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `post_id` | 是 | 要删除的已安排帖子的ID |

### 9. 立即发布

通过将已安排的帖子重新安排为现在的时间，立即发布它。帖子将在几分钟内被调度器处理。仅适用于已安排的帖子。

```json
{
  "post_id": "post-456"
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `post_id` | 是 | 要立即发布的已安排帖子的ID |

### 10. 安排草稿

安排现有草稿在LinkedIn上发布。会获取草稿内容并创建一个新的已安排帖子。原始草稿仍保持为草稿状态。

```json
{
  "draft_id": "abc-123",
  "scheduledFor": "2026-02-17T08:00:00Z"
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `draft_id` | 是 | 要安排的草稿ID（使用`get_drafts`查找ID） |
| `scheduledFor` | 是 | 发布的时间戳（ISO 8601格式） |

---

### 11. 查看已发布的帖子

查看用户已发布的LinkedIn帖子。支持关键词搜索和分页。

```json
{
  "limit": 10,
  "search": "AI"
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `limit` | 否 | 返回的帖子数量（默认：20个） |
| `search` | 否 | 按关键词过滤帖子（不区分大小写） |
| `nextToken` | 否 | 分页的游标——使用上次响应中的`nextToken` |

### 12. 查看已安排的帖子

查看当前正在安排发布的帖子。支持状态过滤、关键词搜索和分页。

```json
{
  "limit": 10,
  "status": "scheduled"
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `limit` | 否 | 返回的帖子数量（默认：20个） |
| `status` | 否 | 按状态过滤：`scheduled`（默认）、`failed`、`pending_approval`、`changes_requested` |
| `search` | 否 | 按关键词过滤帖子（不区分大小写） |
| `nextToken` | 否 | 分页的游标——使用上次响应中的`nextToken` |

### 13. 为帖子添加评论

为已发布的LinkedIn帖子添加评论。某些帖子类型（转发帖子、受限帖子）可能不允许添加评论——这是LinkedIn的限制。

```json
{
  "post_id": "post-456",
  "comment_text": "Great insights! This resonates with what I've seen in enterprise sales."
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `post_id` | 是 | 已发布帖子的`postId`（来自`get_published_posts`） |
| `comment_text` | 是 | 评论文本（仅限纯文本，最多1250个字符）

---

### 14. 获取用户资料

返回用户的姓名、电子邮件和LinkedIn链接。无需参数。

### 15. 获取语音档案

读取用户的语音档案——从他们发布的帖子中学习到的写作风格模式。无需参数。

返回：
- `userInstructions` —— 用户设定的指导原则（避免/强调的主题、品牌关键词、自定义规则、写作样本）
- `generatedProfile` —— LLM学习到的模式（语气维度、词汇偏好、结构模式、反模式）
- `allowAutoUpdate` —— 是否允许自动更新语音档案 |
- `isActive` —— 语音档案是否处于活动状态

**在生成内容之前，请务必阅读语音档案。**这是确保帖子听起来像用户本人而非AI的关键。

### 16. 更新语音档案

在分析用户的帖子后，使用新学习到的模式更新语音档案。

```json
{
  "generatedProfile": {
    "schema_version": "1.0",
    "tone": { "primary": "conversational-authoritative" },
    "vocabulary": { "signature_phrases": ["here's the thing", "let me break this down"] },
    "structure": { "hook_patterns": [{ "type": "bold-statement" }, { "type": "question" }] },
    "anti_patterns": { "never_do": ["use corporate jargon", "start with 'I'm excited to announce'"] }
  }
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `allowAutoUpdate` | 否 | 仅在用户明确请求时更改 |
| `isActive` | 否 | 切换语音档案的开关 |
| `userInstructions` | 否 | 用户控制的指导原则——仅在用户明确要求时修改 |
| `generatedProfile` | 否 | 从分析帖子中学习到的模式 |

**重要提示：**在更新`generatedProfile`之前，请务必检查`allowAutoUpdate`是否设置为`true`。如果用户已锁定他们的档案，请勿进行更新。

---

### 17. 查看联系人

浏览保存的LinkedIn联系人及其资料。支持分页。

```json
{
  "search": "product manager",
  "limit": 20
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `limit` | 否 | 联系人数量（默认：20个） |
| `search` | 否 | 按名称、标题或关键词过滤 |
| `nextToken` | 否 | 分页的游标——使用上次响应中的`nextToken` |

### 18. 查看联系人列表

浏览用户的联系人列表（精选的联系人群组）。

```json
{
  "search": "leads",
  "limit": 10
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `search` | 否 | 按名称过滤列表 |
| `limit` | 否 | 列表数量（默认：20个） |

### 19. 获取列表中的联系人

获取特定联系人列表中的所有联系人。使用`get_lists`查找列表ID。

```json
{
  "list_id": "list-123",
  "limit": 20
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `list_id` | 是 | 从其中获取联系人的列表ID |
| `limit` | 否 | 联系人数量（默认：20个） |
| `nextToken` | 否 | 分页的游标——使用上次响应中的`nextToken` |

### 20. 将联系人添加到列表

将现有联系人添加到联系人列表中。使用`get_contacts`查找联系人ID，然后使用`get_lists`查找列表ID。

```json
{
  "profile_id": "profile-abc",
  "list_id": "list-123"
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `profile_id` | 是 | 要添加的联系人`profileID` |
| `list_id` | 是 | 要添加联系人的列表ID |

---

### 21. 查看收藏的帖子集合

浏览保存的帖子集合（标记的LinkedIn帖子群组）。

```json
{
  "search": "inspiration",
  "limit": 10
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `search` | 否 | 按名称过滤集合 |
| `limit` | 否 | 集合数量（默认：20个） |

### 22. 获取保存的帖子

从特定集合中读取帖子。首先使用`get_collections`查找集合ID。

```json
{
  "collectionID": "col-789",
  "search": "storytelling",
  "limit": 10
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `collectionID` | 是 | 要从中获取帖子的集合ID |
| `limit` | 否 | 帖子数量（默认：20个） |
| `search` | 否 | 按关键词过滤帖子 |

### 23. 获取模板

浏览用户库中保存的帖子模板和创意。

```json
{
  "search": "product launch",
  "limit": 10
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `limit` | 否 | 模板数量（默认：20个） |
| `search` | 否 | 按关键词过滤 |

### 24. 生成图片

使用Google Gemini为LinkedIn帖子生成AI图片。用户需要在[Reepl设置](https://app.reepl.io/settings/ai-models-api)中链接他们的Gemini API密钥。

```json
{
  "style": "infographic",
  "postContent": "3 ways AI is changing B2B sales in 2026..."
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `style` | 是 | 图片风格（见下表） |
| `postContent` | 否 | 用于提供上下文的帖子内容 |
| `customPrompt` | 如果风格设置为`custom` | 您自己的图片提示 |

**可用风格：**

| 风格 | 输出 |
|-------|--------|
| `infographic` | 专业的数据可视化和图表 |
| `minimal-illustration` | 简洁的线描插图 |
| `bold-text` | 字体设计和引用卡片 |
| `screenshot-social-proof` | 模拟截图 |
| `comic-storyboard` | 漫画风格的面板 |
| `realistic-portrait` | 真实风格的肖像 |
| `diagram-flowchart` | 图表和流程图 |
| `custom` | 您自己的提示（需要`customPrompt`） |

**在发布之前，请务必向用户展示生成的图片以获取批准。**在调用`publish_to_linkedin`或`schedule_post`时，将返回的URL作为`mediaUrls`传递。**

---

### 25. 生成轮播图内容

为LinkedIn轮播图生成AI幻灯片内容。支持纯文本主题、YouTube URL和文章URL。返回幻灯片的标题和正文文本，以便传递给`create_carousel_draft`。

注意：API会自动添加一个引导幻灯片和一个CTA幻灯片，因此实际的幻灯片数量将是`number_of_slides + 2`。

```json
{
  "topic": "remote work productivity tips",
  "number_of_slides": 5
}
```

```json
{
  "url": "https://youtube.com/watch?v=...",
  "number_of_slides": 6
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `topic` | 否 | 轮播图的主题或主题（适用于纯文本主题） |
| `url` | 否 | 用于提取内容的YouTube或文章URL |
| `number_of_slides` | 否 | 要生成的幻灯片数量（1-10张，默认：5张） |

### 26. 列出轮播图草稿

列出用户保存在Reepl中的轮播图草稿。

```json
{
  "search": "productivity",
  "limit": 10
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `search` | 否 | 按标题过滤草稿 |
| `limit` | 否 | 返回的草稿数量（默认：20个） |

### 27. 获取轮播图草稿

通过ID获取单个轮播图草稿，包括所有幻灯片内容、主题和样式。

```json
{
  "draft_id": "carousel-abc"
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `draft_id` | 是 | 草稿ID（使用`list_carousel_drafts`查找ID） |

### 28. 创建轮播图草稿

在Reepl中保存新的轮播图草稿。可以使用`generate_carousel_content`提供的幻灯片内容，或者自行编写。如果未指定主题或颜色，将应用您保存的品牌样式。

```json
{
  "title": "5 Remote Work Tips",
  "slides": [
    { "headline": "Stop working from the couch", "body": "Your brain associates spaces with activities. Create a dedicated workspace." },
    { "headline": "Time-block your deep work", "body": "90-minute focus blocks beat 8 hours of fragmented attention every time." }
  ],
  "theme": "3"
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `title` | 是 | 该轮播图草稿的标题 |
| `slides` | 是 | 幻灯片数组，每个幻灯片包含`headline`（必需）和可选的`body` |
| `theme` | 否 | 主题预设ID（`'1'`至`'22'`）。不设置则使用品牌默认样式 |
| `title_font_size` | 是 | 幻灯片标题的字体大小：`lg`、`md`（默认）或`sm` |
| `body_font_size` | 是 | 幻灯片正文的字体大小：`lg`、`md`（默认）或`sm` |

### 29. 更新轮播图草稿

更新现有的轮播图草稿。只需提供您想要更改的字段——未指定的字段保持不变。注意：提供`slides`会替换轮播图中的所有幻灯片。

```json
{
  "draft_id": "carousel-abc",
  "title": "Updated Title",
  "slides": [
    { "headline": "New headline", "body": "New body text" }
  ]
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `draft_id` | 是 | 要更新的草稿ID |
| `title` | 否 | 新标题 |
| `slides` | 否 | 替换幻灯片（替换所有现有幻灯片） |
| `theme` | 否 | 新的主题预设ID（`'1'`至`'22'`） |
| `title_font_size` | 是 | `lg`、`md`或`sm` |
| `body_font_size` | 是 | `lg`、`md`或`sm` |

### 30. 删除轮播图草稿

永久删除轮播图草稿。此操作不可撤销。

```json
{
  "draft_id": "carousel-abc"
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `draft_id` | 是 | 要删除的轮播图草稿的ID |

---

### 31. 在Twitter/X上创建帖子

创建或安排Twitter/X帖子或帖子串。需要在Reepl设置 > 集成中连接Twitter账户，并且拥有有效的高级订阅。

对于单条推文，传递一个包含多个项目的数组。对于帖子串，按顺序传递多个项目。

```json
{
  "threadTweets": [
    { "index": 0, "text": "I spent 6 months studying how top creators grow on LinkedIn. Here's what actually works (thread):" },
    { "index": 1, "text": "1/ Consistency beats virality. Posting 3x/week for 6 months outperforms a single viral post every time." },
    { "index": 2, "text": "2/ Comments matter more than posts. Thoughtful replies on big accounts drive more followers than original posts." }
  ],
  "scheduledFor": "2026-03-15T14:00:00Z"
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `threadTweets` | 是 | 推文对象数组，每个对象包含`index`（基于0的位置）和`text`（每条推文最多280个字符） |
| `scheduledFor` | 否 | ISO 8601时间戳。如果省略，则帖子将保存为草稿（状态：pending） |
| `linkedPostId` | 否 | 该帖子串所转发的LinkedIn帖子的`postId` |

---

## 常见用法模式

### 模式1：用用户的声音撰写帖子

```
1. get_voice_profile          -- read their writing style
2. Ask user for topic          -- what do they want to write about?
3. Write draft (plain text!)   -- match their tone, hooks, vocabulary
4. Show draft, get feedback    -- iterate until they're happy
5. create_draft OR publish     -- save or go live
```

### 模式2：安排一周的内容

```
1. get_voice_profile           -- read writing style
2. get_templates               -- browse content ideas
3. get_saved_posts             -- browse inspiration from collections
4. Write 3-5 posts             -- vary topics, hooks, formats
5. schedule_post (x5)          -- spread across Mon-Fri at varied times
```

### 模式3：重新利用保存的内容

```
1. get_collections             -- find the right collection
2. get_saved_posts             -- browse posts in it
3. Pick a post, rewrite it     -- new angle, user's voice
4. create_draft or publish     -- save or go live
```

### 模式4：使用AI生成的图片发布帖子

```
1. Write the post content first
2. generate_image              -- use post content as context
3. Show the image to user      -- get approval
4. publish_to_linkedin         -- pass image URL in mediaUrls
```

### 模式5：分析并更新语音档案

```
1. get_published_posts         -- fetch recent posts (limit: 20)
2. Analyze patterns            -- tone, hooks, vocabulary, structure
3. get_voice_profile           -- check if allowAutoUpdate is true
4. update_voice_profile        -- save learned patterns to generatedProfile
```

### 模式6：创建LinkedIn轮播图

```
1. Read carousel_guidelines prompt  -- understand content and styling rules
2. generate_carousel_content        -- provide topic or URL
3. Review slides with user          -- adjust if needed
4. create_carousel_draft            -- save with brand kit styling
5. Share the deep link              -- user fine-tunes in Reepl editor
6. update_carousel_draft            -- apply any requested edits
```

### 模式7：在Twitter/X上转发帖子

```
1. Write or retrieve the LinkedIn post content
2. Adapt for Twitter format           -- split into 280-char chunks for threads
3. twitter_create_post                -- schedule or save as draft
4. Pass linkedPostId if cross-posting -- links the Twitter thread to the LinkedIn post
```

### 模式8：安排草稿

```
1. get_drafts                  -- find the draft to publish
2. Ask user for preferred time -- or suggest morning/lunch/evening slots
3. schedule_draft              -- pass draft_id and scheduledFor
```

---

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Session expired or invalid` | OAuth令牌过期 | 在https://mcp.reepl.io/oauth/authorize重新认证 |
| `Content exceeds 3000 character limit` | 帖子太长 | 缩短内容 |
| `draft_id is required` | 缺少草稿ID | 先调用`get_drafts`查找ID |
| `collectionID is required` | 缺少集合ID | 先调用`get_collections`查找ID |
| `GEMINI_NOTLinked` | 未链接Gemini API密钥 | 用户必须在https://app.reepl.io/settings/ai-models-api中链接密钥 |
| `Rate limit exceeded` | 请求过多 | 稍等片刻后重试 |
| Resource not found` | ID无效 | 草稿/帖子/集合可能已被删除 |
| `Couldn't comment on this post` | 无法评论此帖子 | 这是LinkedIn的限制，不是错误——尝试其他帖子 |

---

## 最佳实践

1. **始终先阅读语音档案。**在撰写任何内容之前，调用`get_voice_profile`以了解用户的写作风格。帖子应该听起来像用户本人，而不是AI生成的。
2. **仅使用纯文本。**帖子内容中不得使用Markdown格式。不要使用**粗体**、*斜体*或#标题。LinkedIn会原样显示这些格式。
3. **发布前请确认。**在调用`publish_to_linkedin`、`schedule_post`或`publish_now`之前，务必展示最终内容并获得用户的明确确认。这些操作会影响用户的真实LinkedIn档案。
4. **合理安排发布时间。**不要每次都安排在早上9点发布。询问用户，或者建议不同的时间段，如清晨、午餐时间和傍晚。
5. **不要伪造数据。**不要编造参与度指标、分析数据或帖子性能数字。仅报告API返回的信息。
6. **尊重语音档案的锁定设置。**如果`allowAutoUpdate`设置为`false`，请勿修改`generatedProfile`。用户可能是有意锁定了他们的语音档案。
7. **利用现有资源。**在从头开始写作之前，先查看模板和保存的帖子以获取灵感。用户之所以保存这些内容是有原因的。
8. **在创建轮播图之前阅读指南。**在生成或保存轮播图内容之前，调用`carousel_guidelines`提示以了解内容规则和幻灯片结构。

---

## 参考资料

- [Reepl](https://reepl.io) —— 基于AI的LinkedIn内容管理平台
- [Reepl帮助中心](https://help.reepl.io) —— 文档和指南
- [MCP设置指南](https://mcp.reepl.io) —— 将您的Reepl账户连接到Claude
- [Reepl Chrome扩展程序](https://chromewebstore.google.com/detail/reepl/geomampobbapgnflneaofdplfomdkejn) —— 用于LinkedIn的AI写作助手