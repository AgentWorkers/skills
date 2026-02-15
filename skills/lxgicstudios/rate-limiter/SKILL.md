---
name: rate-limiter
description: 使用人工智能生成速率限制配置。在保护 API 免受滥用时可以使用这种方法。
---

# 速率限制生成器

描述您的速率限制需求。您可以获取适用于 express-rate-limit、基于 Redis 的限制器或自定义实现的配置文件，无需阅读任何文档即可快速保护您的 API。

**一个命令，零配置，立即生效。**

## 快速入门

```bash
npx ai-rate-limit "100 requests per minute per user"
```

## 功能概述

- 生成速率限制中间件及相关配置文件
- 支持内存存储、Redis 存储和数据库存储
- 为不同用户类型设置分层速率限制
- 支持基于 API 密钥和 IP 地址的访问限制
- 在响应中包含正确的速率限制头部信息

## 使用示例

```bash
# Simple IP-based limiting
npx ai-rate-limit "60 requests per minute per IP"

# User tier-based limits
npx ai-rate-limit "free users 100/hour, pro users 1000/hour"

# Redis-backed for distributed systems
npx ai-rate-limit "500 requests per minute" --store redis

# Endpoint-specific limits
npx ai-rate-limit "10 login attempts per 15 minutes"

# With sliding window
npx ai-rate-limit "1000/day sliding window" --algorithm sliding
```

## 最佳实践

- **先设置宽松的限制，再逐步收紧**：在阻止恶意请求的同时，避免影响正常用户
- **为不同端点设置不同的限制**：登录页面需要比数据读取端点更严格的限制
- **返回正确的头部信息**：X-RateLimit-Remaining 标头有助于客户端正确处理请求
- **在生产环境中使用 Redis**：内存中的限制无法在多台服务器之间共享

## 适用场景

- 新发布的 API 需要基本的安全保护
- 面临爬虫攻击或暴力破解尝试时
- 需要为特定高成本操作设置速率限制
- 实现分层的定价策略

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无支付门槛、无需注册，也不需要 API 密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 系统要求

无需安装，只需使用 `npx` 命令运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-rate-limit --help
```

## 工作原理

该工具会解析您提供的速率限制配置信息，提取所需的限制规则、时间窗口及策略，并生成相应的中间件配置文件。您还可以选择为所选存储方式配置后端存储系统。

## 许可证

采用 MIT 许可协议，永久免费使用。您可以随意使用该工具。