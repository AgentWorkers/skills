---
name: cors-gen
description: 为您的软件栈生成 CORS（跨源资源共享）配置。当跨源请求被阻止时，可以使用此配置来解决相关问题。
---

# CORS 生成器

CORS（跨源资源共享）错误是前端开发中的常见难题。本工具将帮助您配置 CORS 设置，确保您的应用程序能够顺利处理跨源请求。

**只需一条命令，无需任何额外配置，即可立即使用。**

## 快速入门

```bash
npx ai-cors "frontend on localhost:3000, API on localhost:8080"
```

## 功能介绍

- 为您的特定服务器或框架生成 CORS 配置
- 支持处理具有多个源地址的复杂场景
- 包含身份验证信息、请求头以及请求方法的相关配置
- 兼容 Express、Fastify、Next.js 等常用框架

## 使用示例

```bash
# Local development
npx ai-cors "frontend on localhost:3000, API on localhost:8080"

# Production setup
npx ai-cors "React app on vercel, Express API on Railway"

# Multiple origins
npx ai-cors "allow requests from app.example.com and admin.example.com"

# With credentials
npx ai-cors "frontend on vercel, API on heroku, needs cookies"
```

## 最佳实践

- **明确指定允许的源地址**：在生产环境中请避免使用通配符（*）
- **仅允许必要的请求方法**（如 GET、POST，而非所有方法）
- **考虑身份验证需求**：使用 cookies 时需进行相应的配置
- **在无痕模式下进行测试**：浏览器缓存可能会掩盖潜在问题

## 适用场景

- 控制台出现“CORS 被阻止”的错误时
- 新增 API 端点时
- 将前端或后端迁移到新域名时
- 为现有 API 添加身份验证功能时

## 作为 LXGIC 开发工具包的一部分

LXGIC Studios 提供了 110 多款免费开发工具，这款工具便是其中之一。免费版本完全无需支付费用、注册或使用 API 密钥，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本，并设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-cors --help
```

## 工作原理

该工具会根据您提供的前端和后端配置信息，自动生成适用于您所使用服务器框架的 CORS 配置。AI 技术会自动处理预检请求（preflight requests）、允许的请求头以及身份验证相关细节。

## 许可证

采用 MIT 许可协议，永久免费。您可以自由使用该工具。

**更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，直接使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-cors --help
```