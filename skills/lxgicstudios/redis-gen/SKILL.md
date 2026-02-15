---
name: redis-gen
description: 生成 Redis 键模式和数据结构设计。在规划 Redis 架构时可以使用这些内容。
---

# Redis Gen

Redis是一款性能出色的数据库，但设计合适的键值存储模式却是一门艺术。这款工具可以帮助你通过合理的键命名、TTL（过期时间）设置以及数据结构来规划Redis的存储方案，从而避免在是否使用哈希（hash）或有序集合（sorted set）时陷入困惑。

**只需一条命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-redis-schema "user sessions with activity tracking"
```

## 功能介绍

- 为你的具体使用场景生成最优的键值存储模式
- 推荐合适的数据结构（字符串、哈希、集合、有序集合、列表）
- 提供缓存失效的TTL设置建议
- 提供常见操作的示例命令
- 说明内存使用的相关注意事项

## 使用示例

```bash
# Design session storage
npx ai-redis-schema "user sessions with last active timestamp"

# Rate limiting schema
npx ai-redis-schema "api rate limiting per user per endpoint"

# Leaderboard design
npx ai-redis-schema "game leaderboard with weekly and all-time scores"

# Real-time features
npx ai-redis-schema "online presence tracking for chat app"
```

## 最佳实践

- **为键值对添加命名空间**：使用冒号进行分隔，例如 `user:123:sessions`
- **设置TTL**：大多数Redis数据都应该设置过期时间，避免占用大量内存
- **考虑数据查询效率**：在生产环境中应避免使用复杂的数据结构
- **注意内存消耗**：哈希结构更节省内存，而字符串结构则不然

## 适用场景

- 新功能开发需要使用Redis缓存时
- 重构现有的Redis代码时（尤其是代码结构混乱的情况）
- 学习Redis并希望了解常用的设计模式时
- 需要为团队文档化Redis的存储方案时

## 作为LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多个免费开发者工具之一。完全免费，无需注册或支付API密钥，只需使用npx命令即可运行。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，直接使用npx命令即可运行。建议使用Node.js 18及以上版本。运行时需要设置`OPENAI_API_KEY`环境变量。

```bash
export OPENAI_API_KEY=sk-...
npx ai-redis-schema --help
```

## 工作原理

该工具会根据你的使用场景描述，结合Redis的最佳实践来设计合适的存储方案。它会考虑数据访问模式、内存效率以及常见的使用误区，并生成包含键值存储模式、数据类型及示例操作的完整文档。

## 许可证

采用MIT许可证，永久免费。你可以随意使用该工具。