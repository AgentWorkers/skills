---
name: x-api
description: 使用官方 API 和 OAuth 1.0a 在 X（Twitter）上发布内容。当您需要发推文、更新状态或发布内容时，可以使用此方法。该方法可以绕过基于 Cookie 的方法（如 bird CLI）所遇到的速率限制和机器人检测问题。
---

# x-api 🐦

使用官方API（OAuth 1.0a）在X平台上发布内容。

## 使用场景

- 发布推文：基于cookie的`bird tweet`方法会被机器人检测到并阻止；
- 为确保数据可靠性，需要使用官方API。

**阅读功能**（时间线、搜索、提及）建议使用`bird` CLI——它免费且适用于阅读操作。

## 设置

### 1. 获取API凭证

1. 访问 https://developer.x.com/en/portal/dashboard
2. 创建一个项目和应用程序
3. 将应用程序权限设置为“读取和写入”
4. 从“Keys and tokens”选项卡中获取以下凭证：
   - API Key（消费者密钥）
   - API Key Secret（消费者密钥）
   - Access Token（访问令牌）
   - Access Token Secret（访问令牌密钥）

### 2. 配置凭证

**选项A：环境变量**
```bash
export X_API_KEY="your-api-key"
export X_API_SECRET="your-api-secret"
export X_ACCESS_TOKEN="your-access-token"
export X_ACCESS_SECRET="your-access-token-secret"
```

**选项B：配置文件**（位于`~/.clawdbot/secrets/x-api.json`）

### 3. 安装依赖项
```bash
npm install -g twitter-api-v2
```

## 发布推文

```bash
x-post "Your tweet text here"
```

或使用完整路径：
```bash
node /path/to/skills/x-api/scripts/x-post.mjs "Your tweet text here"
```

支持多行推文：
```bash
x-post "Line one

Line two

Line three"
```

成功后，系统会返回推文的URL。

## 使用限制

- 免费 tier：每月1,500次发布（需要在X开发者门户中购买信用点数）；
- 基础 tier（每月100美元）：提供更高的使用限制。

## 阅读功能（使用bird）

如需阅读、搜索和监控内容，请使用`bird` CLI：
```bash
bird home                    # Timeline
bird mentions                # Mentions
bird search "query"          # Search
bird user-tweets @handle     # User's posts
bird read <tweet-url>        # Single tweet
```

## 故障排除

- **402：信用点数耗尽**：在X开发者门户的仪表板中补充信用点数；
- **401：未经授权**：重新生成访问令牌（请确保已设置“读取+写入”权限）；
- **未找到凭证**：请设置环境变量或创建配置文件（参见上述设置步骤）。