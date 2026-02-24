---
name: x-twitter-by-altf1be
description: "通过 API v2 将推文、帖子和媒体内容发布到 X/Twitter — 使用安全的 OAuth 1.0a 协议，无需依赖任何外部 npm 包。"
homepage: https://github.com/ALT-F1-OpenClaw/openclaw-skill-x-twitter
metadata:
  {"openclaw": {"emoji": "🐦", "requires": {"env": ["X_CONSUMER_KEY", "X_CONSUMER_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET"]}, "primaryEnv": "X_CONSUMER_KEY"}}
---
# 通过 @altf1be 使用 X/Twitter

您可以使用 X API v2 和安全的 OAuth 1.0a 签名机制，将推文、主题帖（threads）以及媒体内容发布到 X/Twitter 上。

## 设置

1. 从 [https://developer.x.com](https://developer.x.com) 获取 API 密钥。
2. 设置环境变量（或在 `{baseDir}` 目录下创建一个 `.env` 文件）：

```
X_CONSUMER_KEY=your-api-key
X_CONSUMER_SECRET=your-api-secret
X_ACCESS_TOKEN=your-access-token
X_ACCESS_TOKEN_SECRET=your-access-token-secret
```

3. 安装依赖项：`cd {baseDir} && npm install`

## 命令

```bash
# Verify connection
node {baseDir}/scripts/xpost.mjs verify

# Post a tweet
node {baseDir}/scripts/xpost.mjs tweet "Hello from OpenClaw! 🦞"

# Post with image
node {baseDir}/scripts/xpost.mjs tweet "Check this out!" --media ./screenshot.png

# Reply to a tweet
node {baseDir}/scripts/xpost.mjs tweet "Great point!" --reply 1234567890

# Post a thread (inline)
node {baseDir}/scripts/xpost.mjs thread "First tweet" "Second tweet" "Third tweet"

# Post a thread (from file, tweets separated by ---)
node {baseDir}/scripts/xpost.mjs thread --file ./thread.md
```

## 主题帖文件格式

创建一个文件，其中推文之间用 `---` 分隔：

```
🚀 Announcing something cool!
---
Here's why it matters...
---
Check it out: https://example.com
#OpenSource #AI
```

## 安全性

- 使用 OAuth 1.0a 用户上下文进行签名（写入操作时不允许仅限应用访问的认证方式）。
- 不会将任何凭证输出到标准输出（stdout）。
- API 调用使用纯 Node.js 的 `fetch` 函数以及内置的 `node:crypto` 模块（不使用第三方 HTTP 或 OAuth 库）。
- 依赖项极少：仅需要 `commander`（命令行接口框架）和 `dotenv`（用于加载环境变量）。

## 作者

Abdelkrim BOUJRAF — [ALT-F1 SRL](https://www.alt-f1.be)，布鲁塞尔 🇧🇪  
X 账号：[@altf1be](https://x.com/altf1be)