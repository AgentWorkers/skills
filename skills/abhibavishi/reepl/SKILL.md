---
name: LinkedIn Content Creation Skill by Reepl
description: 使用 Reepl 管理您的 LinkedIn 账户：您可以创建帖子草稿、发布和安排发布时间、管理联系人和收藏夹、生成 AI 图像以及维护您的语音资料。需要一个 Reepl 账户（网址：reepl.io）。
homepage: https://reepl.io
metadata: {"openclaw":{"requires":{"env":["REEPL_MCP_KEY"]},"primaryEnv":"REEPL_MCP_KEY"}}
---

# 通过Reepl创建LinkedIn内容

通过Reepl的MCP集成，实现全面的LinkedIn内容管理。您可以用自己的真实风格撰写帖子、安排发布时间、管理草稿、生成AI图片、浏览保存的内容库以及维护联系人信息——所有这些都可以通过您的AI助手完成。

## 先决条件

1. **Reepl账户**——在[reepl.io](https://reepl.io)注册
2. **MCP连接**——通过OAuth连接您的账户（详见下方设置指南）
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

如果在任何步骤中遇到认证错误，请重新在上面的URL进行认证。

---

## 可用工具（共18个）

| 工具 | 功能 |
|------|---------|
| `create_draft` | 保存新的LinkedIn帖子草稿 |
| `get_drafts` | 列出并搜索您的草稿 |
| `update_draft` | 编辑现有的草稿 |
| `delete_draft` | 删除草稿 |
| `publish_to_linkedin` | 立即将帖子发布到LinkedIn |
| `schedule_post` | 将帖子安排在未来发布 |
| `update_scheduled_post` | 更改已安排帖子的时间、内容或设置 |
| `get_published_posts` | 查看您已发布的LinkedIn帖子 |
| `get_scheduled_posts` | 查看已安排的帖子队列 |
| `get_user_profile` | 获取您的Reepl账户信息 |
| `get_voice_profile` | 读取您的语音风格档案 |
| `update_voice_profile` | 使用学习到的模式更新语音风格档案 |
| `get_contacts` | 浏览保存的LinkedIn联系人 |
| `get_lists` | 浏览您的联系人列表 |
| `get_collections` | 浏览您保存的帖子集合 |
| `get_saved_posts` | 从特定集合中读取帖子 |
| `get_templates` | 浏览您的帖子模板和创意 |
| `generate_image` | 为帖子生成AI图片（需要Gemini API密钥） |

---

## 内容规则

所有LinkedIn内容必须为纯文本。请勿使用**粗体**、*斜体*或#标题等Markdown格式。LinkedIn不支持Markdown格式——这些格式会原样显示在动态中，看起来像是AI生成的。请使用换行符、间距和自然标点符号来组织内容。

LinkedIn帖子的字符限制为3000个。

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
| `title` | 否 | 草稿的标题 |
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

立即将帖子发布到LinkedIn。此操作不可撤销——在调用之前务必获得用户的确认。

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

**安排发布时间的建议：**
- 询问用户偏好的时间，而不是自行选择。
- 如果用户需要建议，可以推荐不同的时间段：清晨（7-8 AM）、午餐时间（12-1 PM）或下午（5-6 PM）。
- 避免同时安排所有帖子的发布时间——分散发布时间以提高互动效果。

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

---

### 8. 查看已发布的帖子

查看用户已发布的LinkedIn帖子。

```json
{
  "limit": 10
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `limit` | 否 | 返回的帖子数量（默认：20个） |

### 9. 查看已安排的帖子

查看当前安排在未来发布的帖子。

```json
{
  "limit": 10
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `limit` | 否 | 返回的帖子数量（默认：20个） |

---

### 10. 获取用户信息

返回用户的姓名、电子邮件和LinkedIn URL。无需参数。

### 11. 获取语音风格档案

读取用户的语音风格档案——从他们发布的帖子中学习到的写作风格。无需参数。

返回：
- `userInstructions`——用户设定的指导原则（应避免/强调的主题、品牌关键词、自定义规则、写作示例）
- `generatedProfile`——通过LLM学习到的模式（语气维度、词汇偏好、结构模式、反模式）
- `allowAutoUpdate`——是否允许自动更新语音风格档案 |
- `isActive`——语音风格档案是否处于活动状态

**在生成内容之前，请务必阅读语音风格档案。**这是确保帖子听起来像用户本人而非AI的关键。

### 12. 更新语音风格档案

在分析用户的帖子后，使用新学习到的模式更新语音风格档案。

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
| `allowAutoUpdate` | 否 | 仅在用户明确要求时更改 |
| `isActive` | 否 | 切换语音风格档案的开关 |
| `userInstructions` | 否 | 用户控制的指导原则——仅在用户明确请求时修改 |
| `generatedProfile` | 否 | 通过分析帖子学习到的LLM模式 |

**重要提示：**在更新`generatedProfile`之前，请务必检查`allowAutoUpdate`是否设置为`true`。如果用户已锁定他们的风格档案，请勿进行更新。

---

### 13. 查看联系人

浏览保存的LinkedIn联系人及其资料。

```json
{
  "search": "product manager",
  "limit": 20
}
```

| 参数 | 必需 | 说明 |
|-----------|----------|-------------|
| `limit` | 否 | 联系人数量（默认：20个） |
| `search` | 否 | 按名称、标题或关键词过滤联系人 |

### 14. 查看联系人列表

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

---

### 15. 查看帖子集合

浏览用户保存的帖子集合（标记的LinkedIn帖子组）。

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

### 16. 获取保存的帖子

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
| `collectionID` | 是 | 要从中获取的集合ID |
| `limit` | 否 | 帖子数量（默认：20个） |
| `search` | 否 | 按关键词过滤帖子 |

### 17. 查看模板

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
| `catalogID` | 否 | 按特定目录过滤 |

---

### 18. 生成图片

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
| `postContent` | 否 | 用于生成图片的帖子内容 |
| `customPrompt` | 如果风格设置为`custom` | 用户自定义的图片提示 |

**可用风格：**

| 风格 | 输出 |
|-------|--------|
| `infographic` | 专业的数据可视化和图表 |
| `minimal-illustration` | 简洁的线条艺术插图 |
| `bold-text` | 字体设计和引用卡片 |
| `screenshot-social-proof` | 适用于社交媒体的截图 |
| `comic-storyboard` | 漫画风格的面板 |
| `realistic-portrait` | 真实风格的肖像 |
| `diagram-flowchart` | 图表和流程图 |
| `custom` | 用户自定义的提示（需要`customPrompt`） |

**在发布之前，请务必向用户展示生成的图片以获得批准。**在调用`publish_to_linkedin`或`schedule_post`时，将返回的URL作为`mediaUrls`传递。**

---

## 常见使用模式

### 模式1：用用户的声音撰写帖子

```
1. get_voice_profile          -- read their writing style
2. Ask user for topic          -- what do they want to write about?
3. Write draft (plain text!)   -- match their tone, hooks, vocabulary
4. Show draft, get feedback    -- iterate until they're happy
5. create_draft OR publish     -- save or go live
```

### 模式2：安排一周的内容发布计划

```
1. get_voice_profile           -- read writing style
2. get_templates               -- browse content ideas
3. get_saved_posts             -- browse inspiration from collections
4. Write 3-5 posts             -- vary topics, hooks, formats
5. schedule_post (x5)          -- spread across Mon-Fri at varied times
```

### 模式3：重新利用已保存的内容

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

### 模式5：分析并更新语音风格档案

```
1. get_published_posts         -- fetch recent posts (limit: 20)
2. Analyze patterns            -- tone, hooks, vocabulary, structure
3. get_voice_profile           -- check if allowAutoUpdate is true
4. update_voice_profile        -- save learned patterns to generatedProfile
```

---

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Session expired or invalid` | OAuth令牌过期 | 重新在https://mcp.reepl.io/oauth/authorize进行认证 |
| `Content exceeds 3000 character limit` | 帖子内容超过3000个字符 | 缩短内容长度 |
| `draft_id is required` | 缺少草稿ID | 先调用`get_drafts`查找ID |
| `collectionID is required` | 缺少集合ID | 先调用`get_collections`查找ID |
| `GEMINI_NOT_LINKED` | 未链接Gemini API密钥 | 用户需要在https://app.reepl.io/settings/ai-models-api中链接密钥 |
| `Rate limit exceeded` | 请求次数过多 | 稍等片刻后重试 |
| `Resource not found` | ID无效 | 草稿/帖子/集合可能已被删除 |

---

## 最佳实践

1. **始终先阅读语音风格档案。**在撰写任何内容之前，先调用`get_voice_profile`以了解用户的写作风格。帖子应该像用户本人一样，而不是像AI生成的。
2. **仅使用纯文本。**帖子内容中禁止使用Markdown格式（如**粗体**、*斜体*或#标题）。LinkedIn不会渲染Markdown格式。
3. **发布前务必确认。**在调用`publish_to_linkedin`或`schedule_post`之前，务必展示最终内容并获得用户的明确确认。这些操作会影响用户的真实LinkedIn个人资料。
4. **合理安排发布时间。**不要每次都选择上午9点发布。询问用户，或建议不同的时间段（如清晨、午餐时间或下午）。
5. **切勿伪造数据。**不要捏造参与度指标、分析数据或帖子表现数据。仅报告API返回的信息。
6. **尊重用户对语音风格档案的设置。**如果`allowAutoUpdate`设置为`false`，请勿修改`generatedProfile`。用户可能是有意锁定他们的风格档案的。
7. **利用现有资源。**在从头开始撰写之前，先查看模板和保存的帖子以获取灵感。用户之所以保存这些内容，是有原因的。

---

## 参考资料

- [Reepl](https://reepl.io)——基于AI的LinkedIn内容管理平台
- [Reepl帮助中心](https://help.reepl.io)——文档和指南
- [MCP设置指南](https://mcp.reepl.io)——将您的Reepl账户连接到Claude
- [Reepl Chrome扩展程序](https://chromewebstore.google.com/detail/reepl/geomampobbapgnflneaofdplfomdkejn)——专为LinkedIn设计的AI写作助手