---
name: cloudflare-gen
description: 生成 Cloudflare Workers 的配置文件及代码。适用于在边缘计算环境中进行开发时使用。
---

# Cloudflare Gen

Cloudflare Workers功能强大，但其配置文件（`wrangler.toml`）的编写语法较为独特。这款工具能够根据用户提供的描述自动生成Worker代码及相应的配置文件，包括Edge函数、键值存储（KV storage）以及R2存储桶的配置。所有设置都会被正确地配置好。

**只需一个命令，无需任何额外的配置，即可立即使用。**

## 快速入门

```bash
npx ai-cloudflare "API proxy with rate limiting"
```

## 功能介绍

- 生成`wrangler.toml`配置文件
- 生成Worker函数的TypeScript/JavaScript代码
- 设置键值存储（KV）的命名空间及R2存储桶的绑定
- 配置正确的路由和中间件
- 处理环境变量及敏感信息（如API密钥）

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

- **保持Worker代码简洁**：Edge平台的资源有限，因此代码应尽可能简洁
- **优先使用键值存储（KV）进行数据读取**：KV存储在读取操作上性能较快，但在写入操作上速度较慢
- **妥善处理错误**：Edge平台的错误排查较为困难，因此应明确记录错误信息
- **在部署前进行本地测试**：使用`wrangler`工具进行开发测试

## 适用场景

- 在Cloudflare上构建无服务器（serverless）功能
- 需要利用Edge计算来处理对延迟敏感的应用场景
- 配置Cloudflare Pages并使用Worker函数
- 学习如何使用Cloudflare Workers，并希望获得可运行的示例代码

## 属于LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多个免费开发工具之一。完全免费，无需注册或支付API密钥。这些工具都能正常使用。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装任何软件，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。运行该工具需要设置`OPENAI_API_KEY`环境变量。

```bash
export OPENAI_API_KEY=sk-...
npx ai-cloudflare --help
```

## 工作原理

该工具会根据用户提供的描述生成Worker代码及`wrangler.toml`配置文件。同时，会根据需要配置键值存储（KV）、R2存储桶或持久化对象（Durable Objects）的绑定。生成的代码遵循Cloudflare的规范，并能够处理常见的Edge计算场景。

## 许可证

采用MIT许可证，永久免费。您可以自由使用该工具，无需遵守任何额外的限制。