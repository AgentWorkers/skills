---
name: cloudflare-gen
description: 生成 Cloudflare Workers 的配置文件及相应代码。适用于在边缘计算环境中进行开发时使用。
---

# Cloudflare Gen

Cloudflare Workers 是一个功能强大的工具，但其配置文件（`wrangler.toml`）的格式相对独特。这款工具能够根据用户提供的 plain English 说明自动生成 Worker 代码及其配置文件，同时还能配置 Edge Functions、KV 存储以及 R2 数据存储服务。所有设置都会被正确地完成。

**只需一个命令，无需任何额外的配置，即可立即使用。**

## 快速入门

```bash
npx ai-cloudflare "API proxy with rate limiting"
```

## 功能概述

- 生成 `wrangler.toml` 配置文件
- 生成 TypeScript/JavaScript 语言的 Worker 代码
- 设置 KV（Key-Value）存储相关的命名空间和绑定
- 配置路由规则及中间件
- 处理环境变量和敏感信息（如密钥）

## 使用示例

```bash
# Simple Worker
npx ai-cloudflare "redirect based on country"

# API with storage
npx ai-cloudflare "REST API with KV storage for user preferences"

# Edge caching
npx ai-cloudflare "cache API responses at the edge for 1 hour"

# Auth middleware
npx ai-cloudflare "JWT validation middleware for API routes"
```

## 最佳实践

- **保持 Worker 代码简洁**：Edge 服务的资源有限，因此代码应尽可能简洁。
- **优先使用 KV 进行数据读取**：KV 适用于快速读取操作，但写入速度较慢。
- **妥善处理错误**：Edge 服务中的错误较难调试，因此务必明确地处理错误信息。
- **在本地进行测试**：在部署之前，先使用 `wrangler` 工具进行开发测试。

## 适用场景

- 在 Cloudflare 上构建无服务器（serverless）功能
- 需要利用 Edge 计算能力来处理对延迟敏感的应用场景
- 使用 Cloudflare Pages 并配置相关 Worker 功能
- 希望通过实际示例来学习如何使用 Cloudflare Workers

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。所有工具均免费提供，无需支付费用、注册账号或使用 API 密钥。这些工具都能正常使用。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
export OPENAI_API_KEY=sk-...
npx ai-cloudflare --help
```

## 工作原理

该工具会根据用户提供的描述自动生成 Worker 代码和 `wrangler.toml` 配置文件。如果需要，还会配置 KV、R2 或持久化对象（Durable Objects）的相关绑定。生成的代码遵循 Cloudflare 的设计规范，并能处理常见的边缘计算场景。

## 许可证

采用 MIT 许可协议，永久免费。您可以自由使用该工具，无需遵守任何额外的限制。