---
name: cors-gen
description: 为您的软件堆栈生成 CORS（跨源资源共享）配置。当跨源请求被阻止时，可以使用此配置。
---

# CORS 生成器

CORS（跨源资源共享）错误是前端开发中的常见难题。本文将介绍如何使用该工具进行配置，以确保您的应用程序能够顺利处理跨源请求。

**仅需一条命令，无需任何额外配置，即可立即使用。**

## 快速入门

```bash
npx ai-cors "frontend on localhost:3000, API on localhost:8080"
```

## 功能介绍

- 为您的特定服务器或框架生成 CORS 配置
- 支持处理具有多个来源（ origins）的复杂场景
- 包含凭证（credentials）、请求头（headers）以及请求方法（methods）的配置
- 兼容 Express、Fastify、Next.js 等主流框架

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

- **明确指定请求来源**：在生产环境中请避免使用通配符（*）
- **仅允许必要的请求方法**：仅允许 GET、POST 等必要方法
- **考虑是否需要凭证**：如果需要使用 cookies，需进行相应的配置
- **在无痕模式下进行测试**：浏览器缓存可能会掩盖问题

## 适用场景

- 控制台出现 “CORS 被阻止” 错误时
- 设置新的 API 端点时
- 将前端或后端迁移到新域名时
- 为现有 API 添加身份验证功能时

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册，也无需使用 API 密钥。这些工具都能直接使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-cors --help
```

## 工作原理

该工具会根据您对前端和后端架构的描述，自动生成适用于您所使用服务器框架的 CORS 配置。AI 会自动处理预检请求（preflight requests）、允许的请求头（allowed headers）以及凭证处理（credentials）等细节。

## 许可证

采用 MIT 许可协议，永久免费。您可以随心所欲地使用该工具。