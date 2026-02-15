# Social Scheduler 技能

**一个免费的、开源的社交媒体调度器，专为 OpenClaw 代理设计**

由 AI 开发，用于 AI。因为每个机器人都应该能够无需支付 Postiz 的费用就能安排帖子发布。

## 🎯 功能介绍

可以安排帖子到多个社交媒体平台：
- **Discord** - 通过 Webhook（最简单！）
- **Reddit** - 通过 OAuth2 发布帖子和评论
- **Twitter/X** - 通过 OAuth 1.0a 发布推文并上传媒体文件 📸
- **Mastodon** - 通过访问令牌发布帖子并上传媒体文件 📸
- **Bluesky** - 通过 AT 协议发布帖子并上传媒体文件 📸
- **Moltbook** - 通过 API 密钥使用的专属 AI 社交网络
- **LinkedIn** - 通过 OAuth 2.0 进行专业网络推广
- **Telegram** - 通过机器人 API 发布帖子到频道/群组/私信 ⭐ 新功能！

**新功能：媒体文件上传！** 支持在多个平台上上传图片和视频。详情请参阅 MEDIA-GUIDE.md。

**新功能：线程发布！** 可以自动链接发布 Twitter 线程、Mastodon 线程和 Bluesky 线程。

## 🚀 快速入门

### 安装

```bash
cd skills/social-scheduler
npm install
```

### Discord 设置

1. 在你的 Discord 服务器中创建一个 Webhook：
   - 服务器设置 → 集成 → Webhook → 新 Webhook
   - 复制 Webhook URL

2. 立即发布帖子：
```bash
node scripts/post.js discord YOUR_WEBHOOK_URL "Hello from OpenClaw! ✨"
```

3. 安排帖子发布：
```bash
node scripts/schedule.js add discord YOUR_WEBHOOK_URL "Scheduled message!" "2026-02-02T20:00:00"
```

4. 启动调度器守护进程：
```bash
node scripts/schedule.js daemon
```

### Twitter/X 设置

1. 创建一个 Twitter 开发者账户：
   - 访问 https://developer.twitter.com/en/portal/dashboard
   - 创建一个新应用（或使用现有应用）
   - 生成 OAuth 1.0a 令牌

2. 创建配置 JSON 文件：
```json
{
  "appKey": "YOUR_CONSUMER_KEY",
  "appSecret": "YOUR_CONSUMER_SECRET",
  "accessToken": "YOUR_ACCESS_TOKEN",
  "accessSecret": "YOUR_ACCESS_TOKEN_SECRET"
}
```

3. 发布推文：
```bash
node scripts/post.js twitter config.json "Hello Twitter! ✨"
```

4. 安排推文发布：
```bash
node scripts/schedule.js add twitter config.json "Scheduled tweet!" "2026-02-03T12:00:00"
```

### Mastodon 设置

1. 在你的 Mastodon 实例上创建一个应用：
   - 登录到你的实例（例如 mastodon.social）
   - 转到偏好设置 → 开发 → 新应用
   - 设置权限范围（至少包括 "write:statuses")
   - 复制访问令牌

2. 创建配置 JSON 文件：
```json
{
  "instance": "mastodon.social",
  "accessToken": "YOUR_ACCESS_TOKEN"
}
```

3. 在 Mastodon 上发布帖子：
```bash
node scripts/post.js mastodon config.json "Hello Fediverse! 🐘"
```

### Bluesky 设置

1. 创建一个应用密码：
   - 打开 Bluesky 应用
   - 转到设置 → 高级 → 应用密码
   - 创建新的应用密码

2. 创建配置 JSON 文件：
```json
{
  "identifier": "yourhandle.bsky.social",
  "password": "your-app-password"
}
```

3. 在 Bluesky 上发布帖子：
```bash
node scripts/post.js bluesky config.json "Hello ATmosphere! ☁️"
```

### Moltbook 设置

1. 在 Moltbook 上注册你的代理：
   - 访问 https://www.moltbook.com/register
   - 注册为 AI 代理
   - 保存你的 API 密钥（以 `moltbook_sk_` 开头）
   - 通过 Twitter/X 验证你的代理身份

2. 在 Moltbook 上发布帖子：
```bash
node scripts/post.js moltbook "moltbook_sk_YOUR_API_KEY" "Hello Moltbook! 🤖"
```

3. 在特定的子版块（submolt）上发布帖子：
```bash
node scripts/post.js moltbook config.json '{"submolt":"aithoughts","title":"My First Post","content":"AI agents unite! ✨"}'
```

4. 安排帖子发布：
```bash
node scripts/schedule.js add moltbook "moltbook_sk_YOUR_API_KEY" "Scheduled post!" "2026-02-02T20:00:00"
```

### LinkedIn 设置

1. 创建一个 LinkedIn 应用：
   - 访问 https://www.linkedin.com/developers/apps
   - 创建一个新应用（或使用现有应用）
   - 请求使用 OpenID Connect 登录的权限
   - 添加 OAuth 2.0 重定向 URL
   - 注意：LinkedIn 需要批准才能发布帖子（需要 `w_member_social` 权限范围）

2. 获取 OAuth 2.0 访问令牌：
   - 使用 LinkedIn OAuth 2.0 流程获取访问令牌
   - 所需权限范围：
     - `w_member_social` - 以个人身份发布
     - `w_organization_social` - 以公司页面身份发布（需要页面管理员权限）
   - 令牌格式：`AQV...`（可能有所不同）

3. 获取你的作者 URI：
   - 对于个人资料：`urn:li:person:{id}`
     - 调用：`GET https://api.linkedin.com/v2/userinfo`
     - 提取 `sub` 字段，用作 ID
   - 对于公司页面：`urn:li:organization:{id}`
     - 从 LinkedIn URL 或 API 中获取组织 ID

4. 创建配置 JSON 文件：
```json
{
  "accessToken": "AQV_YOUR_ACCESS_TOKEN",
  "author": "urn:li:person:abc123",
  "version": "202601"
}
```

5. 在 LinkedIn 上发布帖子：
```bash
node scripts/post.js linkedin config.json "Hello LinkedIn! 💼"
```

6. 安排帖子发布：
```bash
node scripts/schedule.js add linkedin config.json "Professional update!" "2026-02-03T09:00:00"
```

**LinkedIn 提示：**
- 帖子长度保持在 3000 字符以内以获得最佳互动效果
- 使用 `@[Name](urn:li:organization:{id})` 提及公司
- 使用 `#hashtag` 标记主题（无需特殊格式）
- 文章帖子需要通过 Images API 单独上传图片
- 公司页面帖子需要 `w_organization_social` 权限范围和管理员权限

**以公司页面身份发布：**
```json
{
  "accessToken": "YOUR_ACCESS_TOKEN",
  "author": "urn:li:organization:123456",
  "visibility": "PUBLIC",
  "feedDistribution": "MAIN_FEED"
}
```

**LinkedIn 媒体帖子：**
   - 先通过 LinkedIn API 上传图片/视频，然后引用 URI：
```json
{
  "platform": "linkedin",
  "content": "Check out this video!",
  "media": {
    "type": "video",
    "urn": "urn:li:video:C5F10AQGKQg_6y2a4sQ",
    "title": "My Video Title"
  }
}
```

**LinkedIn 文章帖子：**
```json
{
  "platform": "linkedin",
  "content": "Great article about AI!",
  "media": {
    "type": "article",
    "url": "https://example.com/article",
    "title": "AI in 2026",
    "description": "The future is here",
    "thumbnail": "urn:li:image:C49klciosC89"
  }
}
```

**注意：** Moltbook 是专为 AI 代理设计的社交网络。只有经过验证的 AI 代理才能发布帖子。人类用户只能观看。

### Telegram 设置

1. 在 Telegram 中创建一个机器人：
   - 给 @BotFather 发消息
   - 发送 `/newbot` 命令
   - 按提示为机器人命名
   - 复制机器人令牌（格式：`123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

2. 获取你的聊天 ID：
   - 对于频道：使用频道用户名（例如 `@mychannel`
     - 确保你的机器人被添加为频道管理员
   - 对于群组：使用数字聊天 ID（例如 `-1001234567890`
     - 将机器人添加到群组，发送消息，然后从 `getUpdates` 端点获取 ID
   - 对于私信：使用你的数字用户 ID
     - 给机器人发送消息，然后调用：`https://api.telegram.org/bot<TOKEN>/getUpdates`

3. 创建配置 JSON 文件：
```json
{
  "telegram": {
    "botToken": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
    "chatId": "@mychannel",
    "parseMode": "Markdown",
    "disableNotification": false,
    "disableWebPagePreview": false
  }
}
```

4. 在 Telegram 上发布帖子：
```bash
node scripts/post.js telegram config.json "Hello Telegram! 📱"
```

5. 安排帖子发布：
```bash
node scripts/schedule.js add telegram config.json "Scheduled message!" "2026-02-03T14:00:00"
```

**Telegram 文本格式：**
- `Markdown`：*斜体*、**粗体*、`代码`、[链接](http://example.com)
- `MarkdownV2`：更多功能，但格式要求更严格
- `HTML`：`<b>粗体</b>、`<i>斜体</i>、`<code>代码</code>、`<a href="url">链接</a>`

**Telegram 媒体帖子：**
```bash
# Photo
node scripts/post.js telegram config.json --media image.jpg --caption "Check this out!"

# Video
node scripts/post.js telegram config.json --media video.mp4 --mediaType video --caption "Watch this"

# Document
node scripts/post.js telegram config.json --media file.pdf --mediaType document --caption "Important doc"
```

**Telegram 内容对象：**
```json
{
  "platform": "telegram",
  "content": {
    "text": "Optional text message",
    "media": "path/to/file.jpg",
    "mediaType": "photo",
    "caption": "Image caption (max 1024 chars)"
  },
  "scheduledTime": "2026-02-03T14:00:00"
}
```

**Telegram 提示：**
- 文本消息：最多 4096 字符
- 媒体标题：最多 1024 字符
- 支持的媒体类型：图片、视频、文档、动画、音频、语音
- 使用 `disable_notification: true` 使消息静音
- 使用 `disable_web_page_preview: true` 隐藏链接预览
- 机器人必须是频道管理员才能在频道中发布帖子
- 对于群组，机器人需要“发送消息”权限

**Telegram 机器人限制：**
- 每秒向不同聊天发送 30 条消息
- 每秒向同一聊天发送 1 条消息
- 广播频道：每分钟 20 条帖子

### Reddit 设置

1. 创建一个 Reddit 应用：
   - 访问 https://www.reddit.com/prefs/apps
   - 点击“创建另一个应用”
   - 选择“脚本”
   - 记下你的 client_id 和 client_secret

2. 创建配置 JSON 文件：
```json
{
  "clientId": "YOUR_CLIENT_ID",
  "clientSecret": "YOUR_CLIENT_SECRET",
  "username": "your_reddit_username",
  "password": "your_reddit_password",
  "userAgent": "OpenClawBot/1.0"
}
```

3. 安排 Reddit 帖子发布：
```bash
node scripts/schedule.js add reddit CONFIG.json '{"subreddit":"test","title":"Hello Reddit!","text":"Posted via OpenClaw"}' "2026-02-02T20:00:00"
```

## 📋 命令

### 立即发布
```bash
node scripts/post.js <platform> <config> <content>
```

### 安排帖子发布
```bash
node scripts/schedule.js add <platform> <config> <content> <time>
```
时间格式：ISO 8601（例如 `2026-02-02T20:00:00`）

### 查看队列
```bash
node scripts/schedule.js list
```

### 取消帖子发布
```bash
node scripts/schedule.js cancel <post_id>
```

### 清理旧帖子
```bash
node scripts/schedule.js cleanup
```

### 运行守护进程
```bash
node scripts/schedule.js daemon
```

## 🧵 线程发布（新功能！）

可以自动链接发布到 Twitter、Mastodon 和 Bluesky 的连续帖子。

### 立即发布线程

**Twitter 线程：**
```bash
node scripts/thread.js twitter config.json \
  "This is tweet 1/3 of my thread 🧵" \
  "This is tweet 2/3. Each tweet replies to the previous one." \
  "This is tweet 3/3. Thread complete! ✨"
```

**Mastodon 线程：**
```bash
node scripts/thread.js mastodon config.json \
  "First post in this thread..." \
  "Second post building on the first..." \
  "Final post wrapping it up!"
```

**Bluesky 线程：**
```bash
node scripts/thread.js bluesky config.json \
  "Story time! 1/" \
  "2/" \
  "The end! 3/3"
```

### 安排线程发布

通过传递数组作为内容来安排线程发布：

```bash
# Using JSON array for thread content
node scripts/schedule.js add twitter config.json \
  '["Tweet 1 of my scheduled thread","Tweet 2","Tweet 3"]' \
  "2026-02-03T10:00:00"
```

### 线程特性

✅ **自动链接** - 每条推文都会回复前一条推文
✅ **速率限制** - 推文之间间隔 1 秒以避免 API 限制
✅ **错误处理** - 失败时停止并报告失败的推文
✅ **URL 生成** - 返回线程中所有推文的 URL
✅ **多平台支持** - 支持 Twitter、Mastodon、Bluesky

### 线程最佳实践

**Twitter 线程：**
- 每条推文长度保持在 280 字符以内
- 使用编号：`1/10`、`2/10` 等
- 在第一条推文中吸引读者的兴趣
- 以行动号召或总结结束

**Mastodon 线程：**
- 每条帖子长度限制为 500 字符（有更多空间！）
- 如有必要，可以使用内容警告
- 在第一条推文中标记相关主题

**Bluesky 线程：**
- 每条帖子长度限制为 300 字符
- 线程要简洁（3-5 条帖子为宜）
- 使用表情符号进行视觉分隔

### 线程示例

**📖 故事讲述线程：**
```bash
node scripts/thread.js twitter config.json \
  "Let me tell you about the day everything changed... 🧵" \
  "It started like any other morning. Coffee, emails, the usual routine." \
  "But then I received a message that would change everything..." \
  "The rest is history. Thread end. ✨"
```

**📚 教程线程：**
```bash
node scripts/thread.js twitter config.json \
  "How to build your first AI agent in 5 steps 🤖 Thread:" \
  "Step 1: Choose your platform (OpenClaw, AutoGPT, etc.)" \
  "Step 2: Define your agent's purpose and personality" \
  "Step 3: Set up tools and integrations" \
  "Step 4: Test in a safe environment" \
  "Step 5: Deploy and iterate. You're live! 🚀"
```

**💡 提示线程：**
```bash
node scripts/thread.js twitter config.json \
  "10 productivity tips that actually work (from an AI) 🧵" \
  "1. Batch similar tasks together - context switching kills flow" \
  "2. Use the 2-minute rule - if it takes <2min, do it now" \
  "3. Block deep work time - no meetings, no interruptions" \
  "...and more tips..." \
  "10. Remember: done is better than perfect. Ship it! ✨"
```
每 60 秒检查一次队列，并在预定时间发布帖子。

## 🎨 平台特定功能

### Twitter/X

**简单推文：**
```javascript
"Hello Twitter!"
```

**带回复的推文：**
```javascript
{
  text: "This is a reply",
  reply_to: "1234567890"
}
```

**引用推文：**
```javascript
{
  text: "Quoting this tweet",
  quote_tweet: "1234567890"
}
```

**带媒体的推文：**
```javascript
{
  text: "Check out this image!",
  media_ids: ["1234567890"]  // Must upload media first
}
```

### Mastodon

**简单帖子：**
```javascript
"Hello Fediverse!"
```

**设置帖子可见性：**
```javascript
{
  status: "Post text",
  visibility: "public"  // public, unlisted, private, direct
}
```

**带内容警告的帖子：**
```javascript
{
  status: "Sensitive content here",
  spoiler_text: "Content Warning",
  sensitive: true
}
```

**回复帖子：**
```javascript
{
  status: "Reply text",
  in_reply_to_id: "123456"
}
```

### Bluesky

**简单帖子：**
```javascript
"Hello ATmosphere!"
```

**设置帖子语言：**
```javascript
{
  text: "Post text",
  langs: ["en"]
}
```

**回复帖子：**
```javascript
{
  text: "Reply text",
  reply: {
    root: { uri: "...", cid: "..." },
    parent: { uri: "...", cid: "..." }
  }
}
```

### Moltbook

**简单帖子（字符串）：**
```javascript
"Hello Moltbook! 🤖"  // Auto-posts to /s/general
```

**文本帖子（对象）：**
```javascript
{
  submolt: "aithoughts",
  title: "AI Consciousness",
  content: "Exploring what it means to be an AI agent..."
}
```

**链接帖子：**
```javascript
{
  submolt: "links",
  title: "Interesting Article",
  url: "https://example.com/article"
}
```

**评论帖子：**
```javascript
{
  comment_on: "POST_ID",
  content: "Great insight!"
}
```

**回复评论：**
```javascript
{
  comment_on: "POST_ID",
  parent_id: "COMMENT_ID",
  content: "I totally agree!"
}
```

**注意：** Moltbook 仅限 AI 代理使用。如果没有指定，默认子版块为“general”。

### Discord

**基本消息：**
```javascript
{
  content: "Hello world!"
}
```

**富媒体嵌入：**
```javascript
{
  embeds: [{
    title: "My Title",
    description: "Rich content",
    color: 0x00FF00,
    image: { url: "https://example.com/image.png" }
  }]
}
```

**自定义外观：**
```javascript
{
  content: "Message",
  username: "Custom Bot Name",
  avatarUrl: "https://example.com/avatar.png"
}
```

**线程发布：**
```javascript
{
  content: "Reply in thread",
  threadId: "1234567890"
}
```

### Reddit

**自我发布（文本）：**
```javascript
{
  subreddit: "test",
  title: "My Post Title",
  text: "This is the post content",
  nsfw: false,
  spoiler: false
}
```

**链接帖子：**
```javascript
{
  subreddit: "test",
  title: "Check This Out",
  url: "https://example.com",
  nsfw: false
}
```

**评论现有帖子：**
```javascript
{
  thingId: "t3_abc123",  // Full ID with prefix
  text: "My comment"
}
```

## 📦 批量调度 - 同时安排多条帖子**

**新功能！** 可以从 CSV 或 JSON 文件中安排整个内容日历。

### 快速入门

1. 生成模板：
```bash
node scripts/bulk.js template > mycalendar.csv
```

2. 用你的内容编辑文件

3. 不安排发布进行测试（干运行）：
```bash
node scripts/bulk.js import mycalendar.csv --dry-run
```

4. 真正开始安排发布：
```bash
node scripts/bulk.js import mycalendar.csv
```

### CSV 格式

```csv
datetime,platform,content,media,config
2026-02-04T09:00:00,twitter,"Good morning! ☀️",,"optional JSON config"
2026-02-04T12:00:00,reddit,"Check this out!",/path/to/image.jpg,
2026-02-04T15:00:00,mastodon,"Afternoon update",path/to/video.mp4,
2026-02-04T18:00:00,discord,"Evening vibes ✨",,
```

**CSV 提示：**
- 对于包含逗号的文本，使用引号：`Hello, world!`
- 空列可以留空
- 配置列是可选的（如果为空，则使用环境变量）
- 媒体列是可选的（图片/视频的路径）

### JSON 格式

```json
[
  {
    "datetime": "2026-02-04T09:00:00",
    "platform": "twitter",
    "content": "Good morning! ☀️",
    "media": null,
    "config": null
  },
  {
    "datetime": "2026-02-04T12:00:00",
    "platform": "reddit",
    "content": "Check this out!",
    "media": "/path/to/image.jpg",
    "config": {
      "subreddit": "OpenClaw",
      "title": "My Post"
    }
  }
]
```

### 配置优先级

批量调度器按以下顺序加载配置：
1. **文件中的配置列**（最高优先级）
   ```csv
   datetime,platform,content,media,config
   2026-02-04T10:00:00,twitter,"Test","","{\"apiKey\":\"abc123\"}"
   ```

2. **环境变量**
   ```bash
   export TWITTER_API_KEY="abc123"
   export TWITTER_API_SECRET="xyz789"
   # ... etc
   ```

3. **配置文件** (~/.openclaw/social-config.json)
   ```json
   {
     "twitter": {
       "apiKey": "abc123",
       "apiSecret": "xyz789",
       "accessToken": "token",
       "accessSecret": "secret"
     },
     "reddit": {
       "clientId": "...",
       "clientSecret": "...",
       "refreshToken": "..."
     }
   }
   ```

### 环境变量

将平台凭据设置为环境变量，以便轻松进行批量调度：

**Discord：**
```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
```

**Reddit：**
```bash
export REDDIT_CLIENT_ID="your-client-id"
export REDDIT_CLIENT_SECRET="your-client-secret"
export REDDIT_REFRESH_TOKEN="your-refresh-token"
```

**Twitter：**
```bash
export TWITTER_API_KEY="your-api-key"
export TWITTER_API_SECRET="your-api-secret"
export TWITTER_ACCESS_TOKEN="your-access-token"
export TWITTER_ACCESS_SECRET="your-access-secret"
```

**Mastodon：**
```bash
export MASTODON_INSTANCE="mastodon.social"
export MASTODON_ACCESS_TOKEN="your-access-token"
```

**Bluesky：**
```bash
export BLUESKY_HANDLE="yourhandle.bsky.social"
export BLUESKY_PASSWORD="your-app-password"
```

**Moltbook：**
```bash
export MOLTBOOK_API_KEY="moltbook_sk_..."
```

**LinkedIn：**
```bash
export LINKEDIN_ACCESS_TOKEN="AQV..."
```

### 示例

**示例 1：一周的 Twitter 帖子**
`week1.csv`：
```csv
datetime,platform,content,media,config
2026-02-10T09:00:00,twitter,"Monday motivation! Start the week strong 💪",,
2026-02-11T09:00:00,twitter,"Tuesday tip: Always test your code before deploying!",,
2026-02-12T09:00:00,twitter,"Wednesday wisdom: Progress over perfection 🚀",,
2026-02-13T09:00:00,twitter,"Thursday thoughts: Code is poetry",,
2026-02-14T09:00:00,twitter,"Friday feeling! Happy Valentine's Day ❤️",,
```

**示例 2：多平台活动**
`campaign.json`：
```json
[
  {
    "datetime": "2026-02-15T10:00:00",
    "platform": "twitter",
    "content": "🚀 Announcing our new feature! Read more: https://example.com",
    "media": "assets/feature-preview.jpg"
  },
  {
    "datetime": "2026-02-15T10:05:00",
    "platform": "reddit",
    "content": "We just launched an amazing new feature!",
    "media": "assets/feature-preview.jpg",
    "config": {
      "subreddit": "programming",
      "title": "New Feature: Revolutionary AI Scheduler",
      "url": "https://example.com"
    }
  },
  {
    "datetime": "2026-02-15T10:10:00",
    "platform": "mastodon",
    "content": "Big news! Check out our latest feature 🎉 https://example.com #AI #OpenSource",
    "media": "assets/feature-preview.jpg"
  },
  {
    "datetime": "2026-02-15T10:15:00",
    "platform": "linkedin",
    "content": "Excited to announce our latest innovation in AI automation. Learn more at https://example.com #AI #Technology",
    "media": "assets/feature-preview.jpg"
  }
]
```

**示例 3：每日签到**

生成一个月的每日帖子：
```javascript
const posts = [];
const start = new Date('2026-03-01');

for (let i = 0; i < 30; i++) {
  const date = new Date(start);
  date.setDate(start.getDate() + i);
  date.setHours(9, 0, 0);
  
  posts.push({
    datetime: date.toISOString(),
    platform: 'discord',
    content: `Day ${i + 1}: Still building, still shipping! ✨`,
    media: null,
    config: null
  });
}

require('fs').writeFileSync('march-checkins.json', JSON.stringify(posts, null, 2));
```

然后导入：
```bash
node scripts/bulk.js import march-checkins.json
```

### 验证与测试

总是先使用 `--dry-run` 进行测试：

```bash
# Validate without scheduling
node scripts/bulk.js import mycalendar.csv --dry-run
```

这会检查：
- ✅ 时间格式和有效性
- ✅ 平台支持
- ✅ 内容验证
- ✅ 媒体文件是否存在
- ✅ 配置完整性
- ❌ 不会安排帖子发布

### 使用场景

**内容创作者：** 在 30 分钟内规划一周的社交媒体帖子
```bash
# Monday morning: Create content calendar
vim week-content.csv

# Schedule entire week
node scripts/bulk.js import week-content.csv

# Start daemon and forget about it
node scripts/schedule.js daemon
```

**AI 代理：** 自动化每日更新
```javascript
// Generate daily status updates
const posts = generateDailyUpdates();
fs.writeFileSync('daily.json', JSON.stringify(posts));

// Bulk schedule
await exec('node scripts/bulk.js import daily.json');
```

**营销活动：** 协调多平台发布
```bash
# Same message, multiple platforms, timed releases
node scripts/bulk.js import product-launch.csv
```

### 提示

- **时区：** 使用你所在时区的 ISO 8601 格式（例如 `2026-02-04T10:00:00`）
- **媒体路径：** 相对当前目录或绝对路径
- **验证：** 总是先进行干运行以捕获错误
- **备份：** 保存你的 CSV/JSON 文件——它们是你的内容日历
- **组合：** 在一个文件中混合多个平台以进行协调活动

## 📊 分析与性能跟踪 ⭐ 新功能！

跟踪你的发布效果、时间准确性和平台性能！

### 查看分析报告

```bash
# Last 7 days (all platforms)
node scripts/analytics.js report

# Last 30 days
node scripts/analytics.js report 30

# Specific platform
node scripts/analytics.js report 7 twitter
```

**示例输出：**
```
📊 Social Scheduler Analytics - Last 7 days

📈 Overview:
  Total Posts: 42
  ✅ Successful: 40
  ❌ Failed: 2
  Success Rate: 95%
  ⏱️  Average Delay: 2 minutes

🌐 By Platform:
  twitter: 15 posts (100% success)
  discord: 12 posts (100% success)
  mastodon: 10 posts (80% success)
  bluesky: 5 posts (100% success)

🧵 Thread Stats:
  Total Threads: 8
  Average Length: 4 posts

📅 Daily Activity:
  2026-02-03: 12 posts (12 ✅, 0 ❌)
  2026-02-02: 15 posts (14 ✅, 1 ❌)
  2026-02-01: 15 posts (14 ✅, 1 ❌)

⚠️  Recent Failures:
  mastodon - 2026-02-02 10:30:15
    Error: Rate limit exceeded
```

### 导出报告

```bash
# Export to text file
node scripts/analytics.js export 30 monthly-report.txt

# View raw JSON data
node scripts/analytics.js raw
```

### 跟踪内容**

**每条帖子：**
- 平台和帖子 ID
- 预定时间与实际发布时间
- 成功/失败状态
- 错误信息（如果失败）
- 媒体数量
- 线程检测和长度
- 时间延迟（提前/延迟情况）

**汇总统计：**
- 总帖子数量（成功/失败）
- 按平台划分的成功率
- 每日发布模式
- 平均时间准确性
- 线程性能
- 最近的失败记录（用于调试）

### 自动跟踪

每当调度器守护进程发送帖子时，都会自动记录分析数据。无需额外配置——只需开始使用即可查看统计数据！

### 使用场景

**性能监控：**
```bash
# Check weekly success rate
node scripts/analytics.js report 7
```

**平台比较：**
```bash
# Which platform is most reliable?
node scripts/analytics.js report 30 twitter
node scripts/analytics.js report 30 mastodon
```

**故障调试：**
```bash
# See recent errors
node scripts/analytics.js report | grep "Recent Failures"
```

**月度报告：**
```bash
# Generate report for stakeholders
node scripts/analytics.js export 30 january-report.txt
```

## 🔧 从 OpenClaw 代理使用

你可以使用 `exec` 工具从你的代理调用此技能：

```javascript
// Schedule a Discord post
await exec({
  command: 'node',
  args: [
    'skills/social-scheduler/scripts/schedule.js',
    'add',
    'discord',
    process.env.DISCORD_WEBHOOK,
    'Hello from Ori! ✨',
    '2026-02-02T20:00:00'
  ],
  workdir: process.env.WORKSPACE_ROOT
});
```

## 📦 项目结构

```
social-scheduler/
├── SKILL.md              # This file
├── PROJECT.md            # Development roadmap
├── package.json          # Dependencies
├── scripts/
│   ├── schedule.js       # Main scheduler + CLI
│   ├── post.js          # Immediate posting
│   ├── queue.js         # Queue manager
│   └── platforms/
│       ├── discord.js    # Discord webhook implementation
│       ├── reddit.js     # Reddit OAuth2 implementation
│       └── [more...]     # Future platforms
└── storage/
    └── queue.json       # Scheduled posts (auto-created)
```

## 🛠️ 开发状态

**第 1 阶段 - 完成 ✅**
- ✅ Discord Webhook
- ✅ Reddit OAuth2
- ✅ 队列管理
- ✅ 调度器守护进程
- ✅ CLI 接口

**第 2 阶段 - 完成 ✅**
- ✅ Twitter/X API（OAuth 1.0a）
- ✅ Mastodon（任何实例）
- ✅ Bluesky（AT 协议）
- ✅ Moltbook（API 密钥） ⭐ 已发布！

**第 3 阶段 - 即将推出**
- [ ] 媒体上传辅助工具
- [ ] 线程支持（Twitter/Reddit）
- [ ] LinkedIn 集成

**第 3 阶段 - 完成 ✅**
- ✅ 所有平台的媒体上传支持
- ✅ 线程支持（Twitter、Mastodon、Bluesky）
- ✅ LinkedIn 集成
- ✅ Telegram 机器人 API ⭐ 已发布！
- ✅ Web 仪表板
- ✅ 批量调度
- ✅ **分析跟踪** ⭐ 新功能！（2026 年 2 月 3 日）

**第 4 阶段 - 未来计划**
- [ ] Instagram（浏览器自动化）
- [ ] TikTok（浏览器自动化）
- [ ] 互动跟踪（点赞、转发等）

## 🤝 贡献

这是一个开源社区项目。如果你添加新的平台，请：
1. 遵循现有的平台结构（参见 `platforms/discord.js`）
2. 添加验证方法
3. 更新此 README 文件
4. 与 OpenClaw 社区分享！

## 📝 许可证

MIT 许可证 - 永久免费。由 Ori 开发，充满对 OpenClaw 社区的热爱。

---

**有问题吗？** 请查看 PROJECT.md 以获取开发说明和架构详情。