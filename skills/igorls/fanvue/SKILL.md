---
name: Fanvue
description: 通过 OAuth 2.0 API，在 Fanvue 创作者平台上管理内容、聊天记录、订阅者以及收益。
---

# Fanvue API 技能

集成 Fanvue 创建者平台，以管理聊天记录、帖子、订阅者、收益数据以及媒体内容。

## 先决条件

### 1. 创建 OAuth 应用程序

1. 访问 [Fanvue 开发者门户](https://fanvue.com/developers/apps)
2. 创建一个新的 OAuth 应用程序
3. 记下您的 **客户端 ID** 和 **客户端密钥**
4. 配置您的 **重定向 URI**（例如：`https://your-app.com/callback`）

### 2. 环境变量

设置以下环境变量：

```bash
FANVUE_CLIENT_ID=your_client_id
FANVUE_CLIENT_SECRET=your_client_secret
FANVUE_REDIRECT_URI=https://your-app.com/callback
```

---

## 认证

Fanvue 使用 **OAuth 2.0 with PKCE**（代码交换证明密钥）。所有 API 请求都需要：

- **授权头**：`Bearer <access_token>`
- **API 版本头**：`X-Fanvue-API-Version: 2025-06-26`

### OAuth 权限范围

根据您的需求请求以下权限范围：

| 权限范围 | 访问权限 |
|-------|--------|
| `openid` | OpenID Connect 认证 |
| `offline_access` | 刷新令牌支持 |
| `offline` | 离线访问 |
| `read:self` | 读取已认证用户信息 |
| `read:chat` | 读取聊天记录 |
| `write:chat` | 发送消息、更新聊天内容 |
| `read:post` | 读取帖子 |
| `write:post` | 创建帖子 |
| `read:creator` | 读取订阅者/关注者信息 |
| `read:media` | 读取媒体内容 |
| `write:tracking_links` | 管理活动链接 |
| `read:insights` | 读取收益/分析数据（仅限创建者账户） |
| `read:subscribers` | 读取订阅者列表（仅限创建者账户） |

> **注意**：某些端点（如订阅者、收益数据）需要 **创建者账户**，并且可能需要文档中未列出的额外权限范围。

### 快速认证流程

```typescript
import { randomBytes, createHash } from 'crypto';

// 1. Generate PKCE parameters
const codeVerifier = randomBytes(32).toString('base64url');
const codeChallenge = createHash('sha256')
  .update(codeVerifier)
  .digest('base64url');

// 2. Build authorization URL
const authUrl = new URL('https://auth.fanvue.com/oauth2/auth');
authUrl.searchParams.set('client_id', process.env.FANVUE_CLIENT_ID);
authUrl.searchParams.set('redirect_uri', process.env.FANVUE_REDIRECT_URI);
authUrl.searchParams.set('response_type', 'code');
authUrl.searchParams.set('scope', 'openid offline_access read:self read:chat write:chat read:post');
authUrl.searchParams.set('state', randomBytes(32).toString('hex'));
authUrl.searchParams.set('code_challenge', codeChallenge);
authUrl.searchParams.set('code_challenge_method', 'S256');

// Redirect user to: authUrl.toString()
```

```typescript
// 3. Exchange authorization code for tokens
const tokenResponse = await fetch('https://auth.fanvue.com/oauth2/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    client_id: process.env.FANVUE_CLIENT_ID,
    client_secret: process.env.FANVUE_CLIENT_SECRET,
    code: authorizationCode,
    redirect_uri: process.env.FANVUE_REDIRECT_URI,
    code_verifier: codeVerifier,
  }),
});

const tokens = await tokenResponse.json();
// tokens.access_token, tokens.refresh_token
```

---

## API 基本 URL

所有 API 请求的地址为：`https://api.fanvue.com`

### 标准请求头

```typescript
const headers = {
  'Authorization': `Bearer ${accessToken}`,
  'X-Fanvue-API-Version': '2025-06-26',
  'Content-Type': 'application/json',
};
```

---

## 代理自动化

这些工作流程专为自动化 Fanvue 创建者账户的 AI 代理设计。

### 访问图片（使用签名 URL）

基本的 `/media` 端点仅返回元数据。要获取可查看的图片 URL，请使用 `variants` 查询参数：

```typescript
// Step 1: List all media
const list = await fetch('https://api.fanvue.com/media', { headers });
const { data } = await list.json();

// Step 2: Get signed URLs for a specific media item
const media = await fetch(
  `https://api.fanvue.com/media/${uuid}?variants=main,thumbnail,blurred`, 
  { headers }
);
const { variants } = await media.json();

// variants = [
//   { variantType: 'main', url: 'https://media.fanvue.com/private/...' },
//   { variantType: 'thumbnail', url: '...' },
//   { variantType: 'blurred', url: '...' }
// ]
```

**图片类型：**
- `main` - 全分辨率原图
- `thumbnail` - 优化后的预览图（较小尺寸）
- `blurred` - 用于预告的模糊版本

### 创建包含媒体的帖子

```typescript
// Step 1: Have existing media UUIDs from vault
const mediaIds = ['media-uuid-1', 'media-uuid-2'];

// Step 2: Create post
const response = await fetch('https://api.fanvue.com/posts', {
  method: 'POST',
  headers,
  body: JSON.stringify({
    text: 'Check out my new content! 🔥',
    mediaIds,
    audience: 'subscribers',  // or 'followers-and-subscribers'
    // Optional:
    price: null,              // Set for pay-per-view
    publishAt: null,          // Set for scheduled posts
  }),
});
```

**受众选项：**
| 值 | 可查看者 |
|-------|-------------|
| `subscribers` | 仅限付费订阅者 |
| `followers-and-subscribers` | 免费关注者和订阅者均可查看 |

### 发送包含媒体的消息

```typescript
// Get subscriber list for decision making
const subs = await fetch('https://api.fanvue.com/creators/list-subscribers', { headers });
const { data: subscribers } = await subs.json();

// Get top spenders for VIP targeting
const vips = await fetch('https://api.fanvue.com/insights/get-top-spenders', { headers });
const { data: topSpenders } = await vips.json();

// Send personalized message with media
await fetch('https://api.fanvue.com/chat-messages', {
  method: 'POST',
  headers,
  body: JSON.stringify({
    recipientUuid: subscribers[0].userUuid,
    content: 'Thanks for being a subscriber! Here\'s something special for you 💕',
    mediaIds: ['vault-media-uuid'],  // Attach media from vault
  }),
});

// Or send to multiple subscribers at once
await fetch('https://api.fanvue.com/chat-messages/mass', {
  method: 'POST',
  headers,
  body: JSON.stringify({
    recipientUuids: subscribers.map(s => s.userUuid),
    content: 'New exclusive content just dropped! 🎉',
    mediaIds: ['vault-media-uuid'],
  }),
});
```

### 代理决策上下文

为了实现有效的自动化，请收集以下上下文信息：

```typescript
interface AutomationContext {
  // Current media in vault
  media: {
    uuid: string;
    name: string;
    type: 'image' | 'video';
    description: string;  // AI-generated caption
    signedUrl: string;    // From variants query
  }[];
  
  // Audience data
  subscribers: {
    uuid: string;
    name: string;
    subscribedAt: string;
    tier: string;
  }[];
  
  // Engagement signals
  topSpenders: {
    uuid: string;
    totalSpent: number;
  }[];
  
  // Recent earnings for trend analysis
  earnings: {
    period: string;
    total: number;
    breakdown: { type: string; amount: number }[];
  };
}
```

---

## 核心操作

### 获取当前用户信息

```typescript
const response = await fetch('https://api.fanvue.com/users/me', { headers });
const user = await response.json();
```

### 列出聊天记录

```typescript
const response = await fetch('https://api.fanvue.com/chats', { headers });
const { data, pagination } = await response.json();
```

### 发送消息

```typescript
const response = await fetch('https://api.fanvue.com/chat-messages', {
  method: 'POST',
  headers,
  body: JSON.stringify({
    recipientUuid: 'user-uuid-here',
    content: 'Hello! Thanks for subscribing!',
  }),
});
```

### 创建帖子

```typescript
const response = await fetch('https://api.fanvue.com/posts', {
  method: 'POST',
  headers,
  body: JSON.stringify({
    content: 'New content available!',
    // Add media IDs, pricing, etc.
  }),
});
```

### 获取收益数据

```typescript
const response = await fetch('https://api.fanvue.com/insights/get-earnings', { headers });
const earnings = await response.json();
```

### 列出订阅者

```typescript
const response = await fetch('https://api.fanvue.com/creators/list-subscribers', { headers });
const { data } = await response.json();
```

---

## API 参考

请参阅 [api-reference.md](./api-reference.md) 以获取完整的端点文档。

---

## 令牌刷新

访问令牌会过期。使用刷新令牌来获取新的令牌：

```typescript
const response = await fetch('https://auth.fanvue.com/oauth2/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    grant_type: 'refresh_token',
    client_id: process.env.FANVUE_CLIENT_ID,
    client_secret: process.env.FANVUE_CLIENT_SECRET,
    refresh_token: currentRefreshToken,
  }),
});

const newTokens = await response.json();
```

---

## 错误处理

常见的 HTTP 状态码：

| 状态码 | 含义 |
|--------|---------|
| `200` | 成功 |
| `400` | 请求错误 - 请检查参数 |
| `401` | 未经授权 - 令牌过期或无效 |
| `403` | 禁止访问 - 缺少必要的权限范围 |
| `404` | 资源未找到 |
| `429` | 请求频率限制 - 请降低请求速率 |

---

## 资源

- [Fanvue API 文档](https://api.fanvue.com/docs)
- [OAuth 2.0 指南](https://api.fanvue.com/docs/authentication/quick-start)
- [开发者门户](https://fanvue.com/developers/apps)
- [Fanvue 应用启动包](https://github.com/fanvue/fanvue-app-starter)