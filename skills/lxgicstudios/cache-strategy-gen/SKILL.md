---
name: cache-strategy
description: 为您的 API 获取基于人工智能的缓存策略建议。在性能至关重要的情况下使用这些策略。
---

# 缓存策略

你知道应该对某些数据进行缓存，但不确定该缓存哪些内容、将缓存放在哪里以及缓存的有效期应该是多久。将这个工具应用于你的 API 路由，就能获得具体的缓存建议。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-cache-strategy ./src/api/
```

## 功能介绍

- 分析你的 API 端点
- 判断哪些数据应该被缓存
- 根据数据访问模式推荐合适的缓存时长（TTL 值）
- 建议使用哪种缓存方式（如 CDN、Redis 或内存）

## 使用示例

```bash
# Analyze API routes
npx ai-cache-strategy ./src/api/

# Analyze specific route file
npx ai-cache-strategy ./routes/products.ts

# Get Redis-specific recommendations
npx ai-cache-strategy ./src/api/ --layer redis
```

## 最佳实践

- **积极缓存静态数据**：配置相关数据、引用数据以及不经常变化的内容
- **谨慎处理用户数据**：个性化响应需要不同的缓存策略
- **正确地更新缓存**：过时的缓存反而比不使用缓存更糟糕
- **监控缓存命中率**：如果没有任何请求命中缓存，说明可能存在问题

## 适用场景

- API 响应时间过慢
- 数据库因重复查询而负担过重
- 需要扩展系统以降低负载
- 在开发新 API 时，希望提前规划缓存策略

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本无需支付费用、无需注册，也无需 API 密钥，直接可以使用这些工具。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-cache-strategy --help
```

## 工作原理

该工具会读取你的 API 路由文件，理解代码中的数据访问模式，并据此推荐合适的缓存策略。其背后的 AI 系统会综合考虑数据更新频率、个性化需求以及常见的访问模式等因素来做出决策。

## 许可证

采用 MIT 许可证，永久免费。你可以自由使用该工具。