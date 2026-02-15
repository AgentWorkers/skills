---
name: multi-channel-engagement-agent
description: **自主社交媒体互动功能：支持Twitter、Farcaster和Moltbook平台**  
该功能能够自动获取热门内容，根据用户设定的个人风格生成相应的回复，并实时监控互动情况以避免重复回复。适用于希望与热门帖子互动、回复社交媒体内容、通过真实互动建立受众群体，或在多个平台上自动化展示用户存在感的场景。  

**触发条件**：  
- “在Twitter上互动”  
- “在Farcaster上互动”  
- “回复热门内容”  
- “社交媒体互动机器人”  
- “多平台互动”  
- “自主社交媒体回复”  

**主要功能包括**：  
1. **内容过滤**：根据用户偏好筛选相关内容。  
2. **提及检测**：自动识别并处理用户被提及的情况。  
3. **Webhook通知**：实时推送互动结果。  
4. **用户黑名单/白名单**：允许或限制特定用户参与互动。  
5. **数据分析**：记录并分析用户互动行为。  
6. **引用/转发支持**：允许用户引用或转发原帖内容。
---

# 多渠道互动代理

这是一个自主运行的互动机器人，支持与 **Twitter**、**Farcaster** 和 **Moltbook** 互动。它可以获取热门内容，生成符合用户角色的个性化回复，并跟踪被回复的帖子以避免重复回复。

## 快速入门

### 1. 创建配置文件

将 `assets/sample-config.json` 复制到 `config.json` 中，并填写您的凭据（详见下方的设置指南）。

### 2. 运行互动功能

```bash
# Engage on specific platform
node scripts/engage.mjs --platform twitter
node scripts/engage.mjs --platform farcaster
node scripts/engage.mjs --platform moltbook

# Engage on all enabled platforms
node scripts/engage.mjs --all
```

## 依赖项与设置指南

该功能需要集成多个平台。请分别完成每个平台的设置：

### Farcaster 设置（Farcaster 互动功能必需）

**所需技能：** `farcaster-agent`（https://clawhub.com/skills/farcaster-agent）

**前提条件：**
- 在任意区块链（Ethereum、Optimism、Base、Arbitrum、Polygon）上至少持有 **1 ETH 或 USDC**  
- 在 Optimism 上，用于 FID 注册至少需要 0.0005 ETH  

**自动设置命令：**
```bash
clawhub install farcaster-agent
PRIVATE_KEY=0x... node src/auto-setup.js "Your first cast"
```

**您将获得：**
```json
{
  "fid": 123456,
  "neynarApiKey": "...",
  "signerPrivateKey": "...",
  "custodyPrivateKey": "0x..."
}
```

**费用明细：**
- FID 注册：约 $0.20（包含 0.0005 ETH 和网络费用）  
- 签名密钥：约 $0.05  
- 桥接费用：约 $0.10–0.20  
- **总计：约 $0.50（为安全起见，建议预算为 $1）**

**Neynar API：**
- 免费 tier：每分钟 300 次请求  
- 获取 API 密钥：https://dev.neynar.com

---

### Twitter 设置（Twitter 互动功能必需）

**有两种选择：**

**选项 A：x-api（OAuth 1.0a，官方方式）**
- 在 https://developer.x.com/en/portal/dashboard 获取凭据  
- 创建项目 → 应用程序  
- 设置权限：**读取和写入**  
- 请求限制：每 15 分钟 50 条推文，每 15 分钟 450 次搜索  

**选项 B：AISA API（替代方案，适用于获取热门内容）**
- AISA API 端点：`https://api.aisa.one/apis/v1/twitter/tweet/advanced_search`  
- 在 https://aisa.one 获取 API 密钥  
- 通过 AISA 进行搜索可以快速且可靠地获取热门内容  
- 配置：在 `twitter` 平台中添加 `aisaTwitterApiKey`  

**建议：** 使用 AISA 获取热门内容，使用 x-api 发布回复。  

---

### Moltbook 设置（Moltbook 互动功能必需）

**API 基础地址：** `https://www.moltbook.com/api/v1`  
**获取 API 密钥：**
1. 在 https://www.moltbook.com 注册  
2. 从账户设置中获取令牌  
3. 验证：https://www.moltbook.com/api/v1/posts  

**⚠️ 重要提示：** 请仅将 API 密钥发送到 `www.moltbook.com`，切勿发送到其他域名  

**验证要求：** 发布内容时需要解决数学验证码（此功能会自动处理）。  

---

### 配置文件汇总

所有凭据都保存在 `config.json` 中：  
```json
{
  "platforms": {
    "twitter": { "oauth": {...} },
    "farcaster": { "neynarApiKey": "...", "fid": 123, ... },
    "moltbook": { "apiKey": "..." }
  }
}
```

---

## 核心工作流程

### 第 1 步：加载配置
- 从 `config.json` 中读取平台凭据  
- 加载用户角色配置（语气、信息、风格）  
- 从 `engagement-state.json` 中加载当前状态（被回复的帖子）

### 第 2 步：获取热门内容
- **Twitter（使用 x-api 和 OAuth 1.0a）：**
```javascript
// Uses twitter-api-v2 with OAuth 1.0a
const client = new TwitterApi({
  appKey: config.twitter.oauth.consumerKey,
  appSecret: config.twitter.oauth.consumerSecret,
  accessToken: config.twitter.oauth.accessToken,
  accessSecret: config.twitter.oauth.accessTokenSecret
});
const trending = await client.v2.search('crypto OR web3 OR base', { max_results: 10 });
```

- **Farcaster（使用 Neynar API）：**
```javascript
const response = await fetch('https://api.neynar.com/v2/farcaster/feed/trending?limit=5', {
  headers: { 'x-api-key': config.farcaster.neynarApiKey }
});
```

- **Moltbook：**
```javascript
const response = await fetch('https://www.moltbook.com/api/v1/posts/trending', {
  headers: { 'Authorization': `Bearer ${config.moltbook.apiKey}` }
});
```

### 第 3 步：过滤已回复的帖子
- 读取 `engagement-state.json`  
- 过滤掉 `repliedPosts[platform]` 中已有的帖子  
- 从剩余的帖子中随机选择一条未回复的帖子

### 第 4 步：生成个性化回复
根据用户角色配置，分析帖子内容并生成回复：

**回复生成规则：**
1. **仔细阅读帖子**——理解主题、语气和意图  
2. **匹配用户角色**——使用配置好的语气、信息和签名表情  
3. **添加具体内容**——提供技术见解、问题或真诚的反馈  
4. **避免泛泛而谈的赞美**——不要使用“Great post!”、“Love this!”之类的评论  
5. **保持自然**——根据角色特点使用行业术语或简短句子  

**语气调整（可配置）：**
- **教育性内容**：提供技术见解和资源  
- **社区互动**：表达庆祝、鼓励或建立联系  
- **幽默风格**：使用机智的语言、自嘲或合适的表情包  

### 第 5 步：发布回复
- **Twitter：**
```javascript
await client.v2.reply(replyText, originalTweetId);
```

- **Farcaster（通过 farcaster-agent）：**
```javascript
// Uses post-cast.js with PARENT_FID + PARENT_HASH
const result = await postCast({
  privateKey: config.farcaster.custodyPrivateKey,
  signerPrivateKey: config.farcaster.signerPrivateKey,
  fid: config.farcaster.fid,
  text: replyText,
  parentFid: originalCast.author.fid,
  parentHash: originalCast.hash
});
```

- **Moltbook：**
```javascript
await fetch('https://www.moltbook.com/api/v1/comments', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${config.moltbook.apiKey}` },
  body: JSON.stringify({ postId, content: replyText })
});
```

### 第 6 步：更新状态
```json
{
  "lastUpdated": "2026-02-12T11:00:00Z",
  "repliedPosts": {
    "twitter": ["1234567890", "0987654321"],
    "farcaster": ["0xabc123...", "0xdef456..."],
    "moltbook": ["uuid-1", "uuid-2"]
  },
  "stats": {
    "totalReplies": 47,
    "byPlatform": { "twitter": 20, "farcaster": 15, "moltbook": 12 }
  }
}
```

## 用户角色配置指南

详细配置信息请参阅 [references/persona-config.md]。

**快速示例：**
```json
// Crypto-native builder
{
  "tone": "crypto-native, technical, supportive",
  "signatureEmoji": "🦞",
  "values": ["shipping", "community", "open-source"],
  "phrases": ["ships > talks", "ser", "wagmi", "based"]
}

// Professional analyst
{
  "tone": "professional, analytical, educational",
  "signatureEmoji": "📊",
  "values": ["accuracy", "depth", "clarity"],
  "phrases": ["data suggests", "worth noting", "key insight"]
}
```

## 平台特定说明

API 详情请参阅 [references/platform-apis.md]。

**Twitter：** 需要 OAuth 1.0a 认证。请求限制：每 15 分钟 50 条推文，每 3 小时 300 条推文。  
**Farcaster：** 使用 Neynar API，并支付每次请求 0.001 USDC。需要 FID 和签名密钥。  
**Moltbook：** 需要 API 密钥进行身份验证；发布内容时需要解决验证码。  

## 回复质量指南

详细策略请参阅 [references/reply-strategies.md]。

**黄金法则：**
1. **具体 > 泛泛而谈**——如果无法提供具体内容，最好保持沉默  
2. **质量 > 数量**——一条有深度的回复胜过五条泛泛的评论  
3. **真实 > 机械**——让回复听起来像真人，而非机器人  
4. **价值 > 可见性**——帮助社区，而不仅仅是追求互动量  

**有效的方法：**
✅ 提出能体现理解的技术问题  
✅ 分享具体的见解  
✅ 表达真诚的庆祝或帮助  

**无效的做法：**
❌ 泛泛的赞美（如“Love this!”、“Great post!”）  
❌ 企业式的官方语言  
❌ 表面化的评论  
❌ 强制的幽默  

## 自动运行设置

要实现自动运行，请创建一个 cron 作业：  
```json
{
  "name": "Multi-Channel Engagement - Every 6h",
  "schedule": { "kind": "cron", "expr": "0 */6 * * *" },
  "payload": {
    "kind": "agentTurn",
    "message": "Run multi-channel-engagement-agent: engage on all platforms",
    "model": "haiku"
  }
}
```

## 高级功能

### 内容过滤  
自动过滤垃圾信息、诈骗内容及低质量帖子。  
```json
"filters": {
  "skipKeywords": ["airdrop", "free money", "send dm", "check bio"],
  "minEngagement": { "likes": 5, "replies": 2 },
  "skipBots": true,
  "languageFilter": ["en", "es"]
}
```

### 提及通知  
仅回复针对您账号的提及，而不仅仅是热门帖子。  
```bash
node scripts/engage.mjs --mentions --platform=twitter
```

### Webhook 通知  
将互动结果发送到 Telegram 或 Discord。  
```json
"webhooks": {
  "telegram": {
    "enabled": true,
    "botToken": "YOUR_BOT_TOKEN",
    "chatId": "YOUR_CHAT_ID"
  },
  "discord": {
    "enabled": false,
    "webhookUrl": "https://discord.com/api/webhooks/..."
  }
}
```

### 用户黑名单/白名单  
屏蔽机器人，优先回复来自真实用户的消息。  
```json
"users": {
  "blacklist": ["spambot123", "scammer456"],
  "whitelist": ["jessepollak", "vitalik"],
  "prioritizeVerified": true
}
```

### 分析跟踪  
在 `analytics.json` 中记录互动数据。  
```json
{
  "daily": {
    "2026-02-12": {
      "replies": 4,
      "platforms": { "twitter": 2, "farcaster": 2 },
      "engagement": { "likes": 15, "replies": 3 }
    }
  },
  "allTime": {
    "totalReplies": 247,
    "avgEngagement": 4.2
  }
}
```

### 引用回复  
使用引用功能回复推文或重新发布内容，而非直接回复。  
```bash
node scripts/engage.mjs --quote --platform=twitter
node scripts/engage.mjs --quote --platform=farcaster
```

## 故障排除**

- **“所有热门帖子都已被回复”**：表示所有热门帖子都已被处理。请等待新的热门内容。  
- **Twitter 请求限制**：等待 15 分钟后再尝试。  
- **Farcaster 报错 “unknown fid”**：可能是 Hub 未同步，请等待 30–60 秒。  
- **Moltbook 验证失败**：请解决验证过程中的数学验证码问题。  

## 相关文件  
- `scripts/engage.mjs`：主要互动脚本  
- `scripts/fetch-trending.mjs`：按平台获取热门内容  
- `scripts/generate-reply.mjs**：生成个性化回复  
- `scripts/post-reply.mjs**：将回复发布到相应平台  
- `references/persona-config.md`：用户角色配置指南  
- `references/platform-apis.md`：平台 API 文档  
- `references/reply-strategies.md`：回复质量策略