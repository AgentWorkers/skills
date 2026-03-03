---
name: tiktok-slideshow
description: 通过 ViralBaby API 创建 TikTok 图片轮播（在照片上叠加文字的幻灯片）。适用于以下场景：用户需要创建 TikTok 幻灯片或轮播；查找用于社交媒体内容的背景图片；将幻灯片内容发布或上传到 TikTok；编辑幻灯片中的文字；或管理用于内容创作的图片集。**禁止用于以下用途**：一般的 TikTok 账户管理、TikTok 分析或数据统计；视频编辑或视频制作（仅适用于图片幻灯片）；非 TikTok 社交媒体平台；以及任何与为 TikTok 创建视觉幻灯片内容无关的任务。
---
# ViralBaby API v1 — 用于创建TikTok幻灯片的工具

该API支持为TikTok创建带有文字叠加效果的图片轮播片：用户可以搜索图片、构建幻灯片、编辑文字，并将结果上传到TikTok的草稿中。

**基础URL：** `https://viralbaby.co`

**所有端点（除认证相关端点外）都需要提供以下授权信息：** `Authorization: Bearer $VB_KEY`

**所有索引均从1开始计算**（例如，图片索引、幻灯片索引等。第1张幻灯片即为第一个幻灯片。）

---

## 认证与API密钥

**重要提示：** 请按以下顺序检查环境变量：
1. **检查 `$VB_KEY`** — 如果已设置，则表示您已经拥有API密钥，可以直接使用API。
2. **检查 `$VB_PASSWORD`** — 如果已设置，则表示您保存了密码。请登录以获取新的API密钥。
3. **如果两者都未设置**，请注册为新用户（详见下方说明）。

### 注册（新用户）
```
POST /api/v1/auth
Body: { "email": "user@example.com", "password": "securepassword", "action": "signup" }
Response: { "key": "vb_live_abc123...", "keyId": "uuid", "userId": "user_...", "message": "Account created..." }
```

注册时，系统会自动生成一个安全的密码。请立即将API密钥和密码保存为环境变量，以确保它们在会话之间保持一致：
```bash
export VB_KEY="vb_live_..."
export VB_PASSWORD="the-generated-password"
```

### 登录（现有用户）
如果 `$VB_KEY` 未设置但 `$VB_PASSWORD` 已设置，请登录以获取新的API密钥：
```
POST /api/v1/auth
Body: { "email": "user@example.com", "password": "$VB_PASSWORD" }
Response: { "key": "vb_live_abc123...", "keyId": "uuid", "userId": "user_...", "message": "Logged in..." }
```
随后将新密钥保存为环境变量：`export VB_KEY="vb_live_..."`

API密钥仅显示一次，之后无法再次获取。在所有其他端点的请求中，务必使用 `Authorization: Bearer $VB_KEY` 进行授权。

---

## 用户偏好设置

系统会存储并检索用户的业务背景及内容风格设置。**在创建任何内容之前，请务必在每次会话开始时获取用户的偏好设置。**

### 获取偏好设置
```
GET /api/v1/preferences
Response: {
  "style": { "id": "uuid", "name": "Casual", "content": "8th grade reading level, lowercase, first-person POV..." } | null,
  "product_info": { "id": "uuid", "name": "My Business", "content": "We sell organic skincare products..." } | null
}
```

### 保存或更新偏好设置
```
PUT /api/v1/preferences
Body: { "type": "style", "name": "My Style", "content": "casual tone, 8th grade reading level..." }
Body: { "type": "product_info", "name": "My Business", "content": "we sell X to Y audience..." }
Response: { "id": "uuid", "type": "style", "name": "...", "content": "..." }
```

偏好设置类型包括：`style`（语音/语气/格式）或 `product_info`（业务/产品描述）。

**工作流程：**
1. **首次会话时：** 执行 `GET /api/v1preferences` 请求。如果两个偏好值均为 `null`，则向用户询问其业务描述和内容风格，并使用 `PUT` 请求保存这些信息。
2. **后续会话中：** 系统会自动获取用户的偏好设置，无需再次询问。
3. **用户可随时通过请求来更新偏好设置**（例如：“将我的风格更新为更专业的样式”）。

---

## 内容构思流程

在创建幻灯片之前，请务必思考以下要点：
1. **吸引注意力**：如何让观众停止滑动？可以使用引人注目的陈述、令人惊讶的事实、用户普遍面临的问题，或者指出用户当前做法中的错误。
2. **内容**：观众真正需要了解什么？请利用存储的 `product_info` 来确定内容方向。
3. **表达方式**：根据用户设置的 `style` 偏好来选择合适的语气和格式（如阅读难度、叙述视角、大小写格式等）。
4. **行动号召**：最后一张幻灯片应包含明确的行动号召（如“关注、保存、评论或访问网站”）。

如果用户的偏好设置已经保存，无需在每次会话中都要求用户重新输入这些信息。

---

## 图片搜索

### 使用Unsplash平台搜索图片
```
POST /api/v1/images/search
Body: { "query": "sunset beach", "per_page": 20, "page": 1, "color": "teal" }
Response: {
  "searchId": "uuid",
  "results": [{
    "index": 1,
    "id": "unsplash-id",
    "description": "A sunset over the ocean",
    "thumbnailUrl": "https://...",
    "url": "https://...",
    "photographer": "John Doe"
  }],
  "total": 500
}
```

请保存搜索结果对应的 `searchId` — 该ID用于后续操作（如创建图片集合和查看预览页面）。

**`color` 参数**（可选）：用于按图片的主色调过滤搜索结果。适用于深色背景幻灯片的推荐颜色：
- `teal`：营造忧郁、氛围感强的效果（适用于大多数主题）
- `black`：颜色非常深，适合营造戏剧性效果
- `blue`：冷色调，显得冷静、专业
- 如果不设置此参数，则会显示所有图片（无颜色过滤）

**图片选择方式：**
- **自动模式**（由AI自动选择，无需人工审核）：
  - 使用 `color` 参数根据内容风格筛选图片。
  - 根据图片描述判断其是否适合用作背景图片（例如，选择描述为风景、建筑、抽象艺术或氛围场景的图片；避免使用肖像、特写人像或文字过多的图片）。
  - 从搜索结果中随机选择8–12张图片（而非仅选择前几张）。
- **预览模式**（人工选择）：
  - 搜索完成后，分享预览页面的URL：`https://viralbaby.co/preview/search/{searchId}`。
  - 告诉用户：“这是搜索结果，请告诉我您想要使用的图片编号（例如‘1, 3, 5, 8’）”。
  - 等待用户确认后，使用这些编号来创建图片集合。

---

## 图片集合管理

### 列出所有图片集合
```
GET /api/v1/collections
Response: [{ "id": "uuid", "name": "Beach Vibes", "imageCount": 12, "coverImageUrl": "..." }]
```

### 创建空集合
```
POST /api/v1/collections
Body: { "name": "Beach Vibes", "description": "Sunset and ocean photos" }
Response: { "id": "uuid", "name": "Beach Vibes" }
```

### 从搜索结果中创建图片集合
```
POST /api/v1/collections/from-search
Body: { "name": "Beach Vibes", "searchId": "uuid", "imageIndices": [1, 4, 6, 8] }
Response: { "collection": { "id": "uuid", "name": "Beach Vibes" }, "stats": { "total": 4, "successful": 4, "failed": 0 } }
```
此操作会将选中的图片下载到永久存储空间。每次请求最多可下载30张图片。

### 获取集合详情
```
GET /api/v1/collections/{id}
Response: { "id": "uuid", "name": "...", "imageCount": 12, "images": [{ "id": "uuid", "url": "https://..." }] }
```

### 删除集合
```
DELETE /api/v1/collections/{id}
Response: { "success": true }
```

---

## 幻灯片制作

### 列出所有幻灯片
```
GET /api/v1/slideshows
GET /api/v1/slideshows?status=draft
Response: [{ "id": "uuid", "title": "...", "status": "draft", "slideCount": 5, "previewUrl": "https://viralbaby.co/preview/uuid" }]
```

### 创建幻灯片
每张幻灯片都包含背景图片和文字叠加层。每个幻灯片最多可包含30张图片。

图片来源有以下三种优先级：
1. `imageUrl`：图片的直接URL。
2. `searchId` + `imageIndex`：根据索引从之前的搜索结果中选取图片。
3. `collectionId`：从集合中随机选取图片。

**文字元素设置：**
- `text`（必填）：文本内容。
- `type`（必填）：`"title"`（字体较大、更显眼）或 `"subtitle"`（字体较小）。
- `fontSize`（可选）：字体大小（单位：px）。标题的默认大小为16px，副标题为14px。为在TikTok上获得更好的显示效果，建议标题使用18–20px的字体大小。
- 文本默认为白色，带有黑色边框。长文本会自动换行以适应幻灯片显示。
- 文本位置会自动调整：单个文字元素会垂直居中显示，标题和副标题的位置比例为40%/60%，以便清晰区分。

**幻灯片的宽高比支持：** `3:4`（默认值，最适合TikTok）、`1:1`、`9:16`、`4:5`。

### 获取幻灯片信息
```
GET /api/v1/slideshows/{id}
Response: { "id": "uuid", "title": "...", "slides": [...], "status": "draft", "previewUrl": "..." }
```

### 更新幻灯片
该接口用于编辑幻灯片内容：可以修改文字、重新排序图片、添加/删除幻灯片、更新标题等。

**编辑幻灯片的步骤：**
1. 执行 `GET /api/v1/slideshows/{id}` 请求，获取当前幻灯片的详细信息。
2. 根据需要修改 `slides` 数组（更改文字、重新排序图片、添加/删除幻灯片）。
3. 使用更新后的 `slides` 数组，执行 `PUT /api/v1/slideshows/{id}` 请求。

在编辑文字时，请保留原有的 `id` 和 `imageUrl`，仅修改需要修改的部分。

### 删除幻灯片
```
DELETE /api/v1/slideshows/{id}
Response: { "success": true }
```

### 服务器端生成幻灯片图片
系统会将幻灯片渲染为带有文字叠加层的JPEG图片，并返回S3格式的URL。

```
POST /api/v1/slideshows/{id}/render
Body: { "slideIndices": [1, 3] }   // optional (1-indexed), defaults to all slides
Response: { "renderedSlides": [{ "index": 1, "url": "https://s3.../rendered-slide.jpg" }] }
```

---

## 与TikTok的集成

### 连接TikTok账户
该API会生成一个一次性的OAuth授权链接。用户可以在任何浏览器中打开该链接，无需登录TikTok控制台。

**操作步骤：**
1. 将生成的 `authUrl` 提供给用户，让他们在浏览器中打开链接。
2. 用户完成TikTok的授权流程后，系统会显示成功页面。
**注意：** 此操作只需执行一次。

### 检查连接状态
```
GET /api/v1/tiktok/status
Response: { "connected": true, "tokenExpired": false, "user": { "display_name": "..." } }
// or
Response: { "connected": false, "message": "TikTok not connected..." }
```

### 将幻灯片上传到TikTok草稿
系统会先在服务器端生成所有幻灯片的图片文件，然后将其上传到用户的TikTok草稿中（不会立即发布）。用户需要打开TikTok应用来查看和发布这些幻灯片。

**上传时需要提供的信息：**
- `title`：TikTok帖子的简短标题。
- `description`：图片的描述性文字（最多4000个字符）。**建议编写详细的内容**——较长的描述在TikTok上效果更好。描述中应包含故事元素、背景信息、行动号召等。建议描述长度在500–2000个字符之间。
- `hashtags`：最多可添加5个标签（可带`#`前缀，也可不加）。系统会自动在描述中添加标签。

上传成功后，告知用户：“您的幻灯片已上传到TikTok草稿中。请打开TikTok应用进行查看和发布。”

---

## 完整的工作流程示例
以下是创建并上传幻灯片的完整步骤：

```
0. Check credentials (in order):
   a. If $VB_KEY is set → skip to step 1
   b. If $VB_PASSWORD is set → POST /api/v1/auth { "email": "...", "password": "$VB_PASSWORD" } → export VB_KEY="vb_live_..."
   c. Otherwise → POST /api/v1/auth { "email": "...", "password": "<auto-generate>", "action": "signup" } → export VB_KEY="vb_live_..." && export VB_PASSWORD="..."

0b. Fetch preferences
   GET /api/v1/preferences
   → If style or product_info is null, ask user and save with PUT /api/v1/preferences
   → Use stored context for all content decisions going forward

1. Search for images
   POST /api/v1/images/search  { "query": "morning routine aesthetic" }
   → save searchId

2. Create a collection from search results
   POST /api/v1/collections/from-search  { "name": "Morning Routine", "searchId": "...", "imageIndices": [1, 3, 6, 9, 12] }
   → save collectionId

3. Create the slideshow (one slide per element in the array, up to 30 slides)
   POST /api/v1/slideshows  {
     "title": "5 Morning Routine Tips",
     "aspectRatio": "3:4",
     "slides": [
       { "collectionId": "...", "textElements": [{ "text": "Your morning routine is broken", "type": "title" }] },
       { "collectionId": "...", "textElements": [{ "text": "Tip #1: Wake up at the same time", "type": "title" }, { "text": "Consistency beats motivation", "type": "subtitle" }] },
       { "collectionId": "...", "textElements": [{ "text": "Tip #2: No phone for 30 min", "type": "title" }] },
       { "collectionId": "...", "textElements": [{ "text": "Tip #3: Move your body", "type": "title" }] },
       { "collectionId": "...", "textElements": [{ "text": "Follow for more tips", "type": "title" }] }
     ]
   }
   → save slideshowId, get previewUrl

4. (Optional) Edit slides
   GET /api/v1/slideshows/{id}  → get current slides
   Modify text/elements as needed, then:
   PUT /api/v1/slideshows/{id}  { "slides": [...updated slides...] }

5. Preview the slideshow
   Share previewUrl with the user so they can verify in their browser

6. Connect TikTok (first time only)
   GET /api/v1/tiktok/connect  → give authUrl to user to open in browser → complete OAuth
   GET /api/v1/tiktok/status   → verify connected: true

7. Upload to TikTok drafts
   POST /api/v1/tiktok/upload  { "slideshowId": "...", "title": "5 Morning Routine Tips", "description": "I used to wake up and immediately reach for my phone...\n\n(write a long, detailed caption — 500-2000+ chars)", "hashtags": ["morningroutine", "productivity"] }
   → Tell user to open TikTok app to review and publish from drafts
```

---

## 订费信息

**免费套餐：** 允许上传5次到TikTok。
**Pro套餐：** 一次性支付49美元，之后可无限次上传。

**唯一需要付费的端点为：** `POST /api/v1/tiktok/upload`。其他所有端点（搜索、图片集合管理、幻灯片制作等）均免费且无使用次数限制。

**查询计费状态：**
```
GET /api/v1/billing
Authorization: Bearer $VB_KEY
Response: {
  "plan": "free",
  "uploadCount": 3,
  "limit": 5,
  "upgradeUrl": "https://viralbaby.co/checkout?userId=user_xxx"
}
```

### 处理402错误（上传次数达到限制）
当免费上传次数用完时，`POST /api/v1/tiktok/upload` 会返回相应的错误信息：
```
HTTP 402
{
  "error": "Free upload limit reached. Upgrade to Pro for unlimited uploads.",
  "plan": "free",
  "uploadCount": 5,
  "limit": 5,
  "upgradeUrl": "https://viralbaby.co/checkout?userId=user_xxx"
}
```

收到402错误响应时，请告知用户他们已使用完免费上传次数，并提供升级链接（`upgradeUrl`），以便用户升级到Pro套餐。

**升级后：** 执行 `GET /api/v1/billing` 请求，即可查看计费详情。

---

## 反馈与错误处理

如果您在使用API时遇到问题，或者用户对ViralBaby有任何反馈，请按照以下方式报告：
```
POST /api/v1/feedback
Body: { "type": "error", "message": "POST /api/v1/tiktok/upload returned 500: Internal server error. Slideshow ID: abc123" }
Body: { "type": "feedback", "message": "User says: would love to be able to change font styles" }
```

- **类型**：`"error"` 表示API错误或故障；`"feedback"` 表示用户建议。
- **内容**：自由输入的文本。对于错误信息，请提供相关的端点、状态码、错误详情及任何相关ID；对于用户反馈，请直接引用用户的原话。

当API调用失败时（例如5xx错误或不应重复出现的4xx错误），系统会自动记录错误信息。请注意：401/402错误属于正常情况，无需特别报告。

---

## 错误响应格式
所有错误响应均遵循以下格式：
```json
{ "error": "Human-readable error message" }
```

**常见错误代码：**
- `400`：请求错误（参数缺失或无效）。
- `401`：API密钥无效或未设置。
- `402`：免费上传次数达到限制（此时会提供升级链接`upgradeUrl`）。
- `404`：资源未找到。
- `500`：服务器错误。