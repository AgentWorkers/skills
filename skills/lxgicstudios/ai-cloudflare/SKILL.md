---
name: cloudflare-gen
description: 生成 Cloudflare Workers 的配置文件及代码。适用于在边缘计算环境中进行开发时使用。
---

# Cloudflare Gen

Cloudflare Workers 是一个功能强大的工具，但其配置文件（`wrangler.toml`）的编写规范较为独特。这款工具能够根据用户提供的简单描述自动生成 Workers 的代码及配置文件，同时还会配置 Edge Functions、KV（Key-Value）存储以及 R2 数据存储服务。所有设置都会被正确地完成。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-cloudflare "API proxy with rate limiting"
```

## 功能介绍

- 生成 `wrangler.toml` 配置文件
- 生成 Workers 的 TypeScript/JavaScript 代码
- 设置 KV 命名空间及 R2 数据存储的绑定
- 配置正确的路由规则和中间件
- 处理环境变量及敏感信息（如密钥）

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

- **保持 Workers 代码简洁**：Edge 服务对代码大小有限制
- **使用 KV 进行数据读取**：KV 适合快速读取数据，但不适合写入操作
- **妥善处理错误**：Edge 服务中的错误较难调试，因此请确保错误信息明确易懂
- **在本地进行测试**：在部署前先使用 `wrangler` 工具进行开发测试

## 适用场景

- 在 Cloudflare 上构建无服务器（serverless）功能
- 需要边缘计算来处理对延迟敏感的应用场景
- 使用 Workers 配置 Cloudflare Pages
- 希望通过实际示例学习 Workers 的使用方法

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。所有工具均免费提供，无需注册或支付 API 密钥。只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
export OPENAI_API_KEY=sk-...
npx ai-cloudflare --help
```

## 工作原理

该工具会根据用户提供的描述生成 Workers 代码及 `wrangler.toml` 配置文件，并根据需要设置 KV、R2 或 Durable Objects 的数据存储绑定。生成的代码遵循 Cloudflare 的设计规范，同时能够处理常见的边缘计算场景。

## 许可证

采用 MIT 许可协议，永久免费。您可以自由使用该工具。

---

**由 LXGIC Studios 开发**

- GitHub: [github.com/lxgicstudios/ai-cloudflare](https://github.com/lxgicstudios/ai-cloudflare)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)