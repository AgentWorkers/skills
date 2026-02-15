# Social Scheduler 技能

**一款专为 OpenClaw 机器人设计的免费开源社交媒体调度工具**

由 AI 开发，专为 AI 设计。因为每个机器人都应该能够无需支付 Postiz 的费用就能安排帖子发布。

## 🎯 功能介绍

**支持在多个社交媒体平台上安排帖子发布：**
- **Discord** - 通过 Webhook（最简单的方式！）
- **Reddit** - 通过 OAuth2 发布帖子和评论
- **Twitter/X** - 通过 OAuth 1.0a 发布推文并支持上传媒体文件 📸
- **Mastodon** - 通过访问令牌发布帖子并支持上传媒体文件 📸
- **Bluesky** - 通过 API 密钥在 Bluesky 平台上发布帖子 ⭐

**新功能：** 支持媒体文件上传！可以在多个平台上上传图片和视频。详情请参阅 MEDIA-GUIDE.md。

**新功能：** 支持发布多条推文（线程）！可以自动链接多条推文，适用于 Twitter、Mastodon 和 Bluesky。

## 🚀 快速入门

### 安装

```bash
cd skills/social-scheduler
npm install
```

### Discord 设置

1. 在您的 Discord 服务器中创建一个 Webhook：
   - 服务器设置 → 集成 → Webhook → 新建 Webhook
   - 复制 Webhook 的 URL

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
   - 创建一个新的应用（或使用现有的应用）
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

1. 在您的 Mastodon 实例上创建一个应用：
   - 登录到您的实例（例如 mastodon.social）
   - 转到设置 → 开发 → 新应用
   - 设置权限（至少需要 “write:statuses” 权限）
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

1. 在 Bluesky 应用中创建一个应用密码：
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

1. 在 Moltbook 上注册您的机器人：
   - 访问 https://www.moltbook.com/register
   - 以 AI 机器人的身份注册
   - 保存您的 API 密钥（以 `moltbook_sk_` 开头）
   - 通过 Twitter/X 验证您的机器人身份

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

**注意：** Moltbook 是专为 AI 机器人设计的社交网络。只有经过验证的 AI 机器人才能发布帖子。人类用户只能观看帖子。

### Reddit 设置

1. 创建一个 Reddit 应用：
   - 访问 https://www.reddit.com/prefs/apps
   - 点击 “创建新应用”
   - 选择 “脚本” 类型
   - 记下您的 client_id 和 client_secret

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

### 立即发布帖子
```bash
node scripts/post.js <platform> <config> <content>
```

### 安排帖子发布
```bash
node scripts/schedule.js add <platform> <config> <content> <time>
```
时间格式：ISO 8601 格式（例如 `2026-02-02T20:00:00`）

### 查看待发布队列
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

### 运行调度器守护进程
```bash
node scripts/schedule.js daemon
```

## 🧵 多条推文发布（新功能！）

支持在 Twitter、Mastodon 和 Bluesky 上发布相互关联的多条推文。

### 立即发布多条推文

**Twitter 多条推文：**
```bash
node scripts/thread.js twitter config.json \
  "This is tweet 1/3 of my thread 🧵" \
  "This is tweet 2/3. Each tweet replies to the previous one." \
  "This is tweet 3/3. Thread complete! ✨"
```

**Mastodon 多条推文：**
```bash
node scripts/thread.js mastodon config.json \
  "First post in this thread..." \
  "Second post building on the first..." \
  "Final post wrapping it up!"
```

**Bluesky 多条推文：**
```bash
node scripts/thread.js bluesky config.json \
  "Story time! 1/" \
  "2/" \
  "The end! 3/3"
```

### 安排多条推文发布

可以通过传递一个数组作为内容来安排多条推文的发布：

```bash
# Using JSON array for thread content
node scripts/schedule.js add twitter config.json \
  '["Tweet 1 of my scheduled thread","Tweet 2","Tweet 3"]' \
  "2026-02-03T10:00:00"
```

### 多条推文的特点

✅ **自动链接** - 每条推文都会回复前一条推文
✅ **速率限制** - 每条推文之间有 1 秒的延迟，以避免 API 限制
✅ **错误处理** - 发生错误时会停止并报告失败的推文
✅ **生成链接** - 为多条推文生成相应的链接
✅ **跨平台支持** - 支持 Twitter、Mastodon 和 Bluesky

### 多条推文的最佳实践

**Twitter 多条推文：**
- 每条推文长度控制在 280 个字符以内
- 使用编号格式（例如 “1/10”, “2/10” 等）
- 在第一条推文中吸引读者的注意
- 最后一条推文应包含行动号召或总结

**Mastodon 多条推文：**
- 每条推文长度限制为 500 个字符
- 如有必要，可以使用内容警告功能
- 在第一条推文中标记相关主题

**Bluesky 多条推文：**
- 每条推文长度限制为 300 个字符
- 推文应简洁明了（3-5 条为宜）
- 使用表情符号增加视觉效果

### 多条推文示例

**📖 故事分享帖：**
```bash
node scripts/thread.js twitter config.json \
  "Let me tell you about the day everything changed... 🧵" \
  "It started like any other morning. Coffee, emails, the usual routine." \
  "But then I received a message that would change everything..." \
  "The rest is history. Thread end. ✨"
```

**📚 教程帖：**
```bash
node scripts/thread.js twitter config.json \
  "How to build your first AI agent in 5 steps 🤖 Thread:" \
  "Step 1: Choose your platform (OpenClaw, AutoGPT, etc.)" \
  "Step 2: Define your agent's purpose and personality" \
  "Step 3: Set up tools and integrations" \
  "Step 4: Test in a safe environment" \
  "Step 5: Deploy and iterate. You're live! 🚀"
```

**💡 提示帖：**
```bash
node scripts/thread.js twitter config.json \
  "10 productivity tips that actually work (from an AI) 🧵" \
  "1. Batch similar tasks together - context switching kills flow" \
  "2. Use the 2-minute rule - if it takes <2min, do it now" \
  "3. Block deep work time - no meetings, no interruptions" \
  "...and more tips..." \
  "10. Remember: done is better than perfect. Ship it! ✨"
```
该功能每 60 秒检查一次待发布队列，并在预定时间发布帖子。

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

**带媒体文件的推文：**
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

**设置帖子的可见性：**
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

**设置帖子的语言：**
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

**简单文本帖子：**
```javascript
"Hello Moltbook! 🤖"  // Auto-posts to /s/general
```

**对象形式的帖子：**
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

**在帖子下发表评论：**
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

**注意：** Moltbook 仅限 AI 机器人使用。如果没有指定，默认的子版块为 “general”。

### Discord

**基本消息：**
```javascript
{
  content: "Hello world!"
}
```

**富文本嵌入：**
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

**发布多条推文：**
```javascript
{
  content: "Reply in thread",
  threadId: "1234567890"
}
```

### Reddit

**纯文本帖子：**
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

**在现有帖子下发表评论：**
```javascript
{
  thingId: "t3_abc123",  // Full ID with prefix
  text: "My comment"
}
```

## 🔧 从 OpenClaw 机器人调用

您可以使用 `exec` 工具从您的机器人中调用此技能：

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

## 🛠️ 开发进度

**第 1 阶段 - 完成 ✅**
- ✅ 支持 Discord Webhook
- ✅ 支持 Reddit OAuth2
- ✅ 待发布队列管理
- ✅ 调度器守护进程
- ✅ 命令行界面（CLI）

**第 2 阶段 - 完成 ✅**
- ✅ 支持 Twitter/X 的 OAuth 1.0a 协议
- ✅ 支持 Mastodon（任何实例）
- ✅ 支持 Bluesky（AT 协议）
- ✅ 支持 Moltbook（API 密钥） ⭐ 已发布！

**第 3 阶段 - 即将推出**
- [ ] 支持媒体文件上传功能
- [ ] 支持多条推文发布（Twitter/Reddit）
- [ ] 支持 LinkedIn 集成

**第 4 阶段 - 未来计划**
- [ ] 支持 Telegram 机器人 API
- [ ] 开发 Web 界面
- [ ] 实现数据分析功能
- [ ] 支持批量帖子发布

## 🤝 贡献方式

这是一个开源社区项目。如果您要为新的平台添加支持，请：
1. 遵循现有的平台结构（参见 `platforms/discord.js`）
2. 添加相应的验证逻辑
3. 更新此 README 文件
4. 与 OpenClaw 社区分享您的贡献！

## 📝 许可证

MIT 许可证 - 永久免费。由 Ori 开发，充满对 OpenClaw 社区的热爱。

---

**有问题吗？** 请查看 PROJECT.md 文件以获取开发说明和架构详情。