---
name: redis-schema-gen
description: 生成 Redis 键模式和数据结构。在设计 Redis 架构时可以使用这些信息。
---

# Redis模式生成器

Redis具有很高的灵活性，但这同时也意味着你需要仔细设计键的命名规则和数据结构。请描述你的使用场景，以便获得合适的Redis模式。

**仅需一条命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-redis-schema "user sessions and rate limiting"
```

## 功能介绍

- 生成Redis键的命名规范
- 设计合适的数据结构（字符串、哈希表、集合等）
- 提供TTL（生存时间）设置建议
- 文档化数据的访问模式

## 使用示例

```bash
# Session storage
npx ai-redis-schema "user sessions and rate limiting"

# Caching layer
npx ai-redis-schema "cache API responses with invalidation"

# Leaderboard
npx ai-redis-schema "game leaderboard with real-time updates"
```

## 最佳实践

- **使用命名空间化的键**：采用“前缀：类型：ID”的格式
- **设置TTL**：Redis的存储空间是有限的
- **选择合适的数据类型**：使用哈希表存储对象，使用有序集合进行排名
- **规划数据的过期时间**：确定数据应保留多久

## 适用场景

- 将Redis集成到你的应用程序架构中
- 设计缓存策略
- 开发实时功能
- 学习Redis的相关模式

## 本工具属于LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多个免费开发工具之一。完全免费，无需注册或支付API密钥，即可直接使用这些工具。

**了解更多：**
- GitHub：https://github.com/LXGIC-Studios
- Twitter：https://x.com/lxgicstudios
- Substack：https://lxgicstudios.substack.com
- 官网：https://lxgicstudios.com

## 系统要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。运行时需要设置`OPENAI_API_KEY`环境变量。

```bash
npx ai-redis-schema --help
```

## 工作原理

该工具会根据你的使用场景描述，自动生成合适的Redis键命名规则和数据结构。AI会判断哪种Redis数据类型最适合特定的访问模式。

## 许可证

采用MIT许可证，永久免费。你可以自由使用该工具。

---

**由LXGIC Studios开发**

- GitHub：[github.com/lxgicstudios/redis-schema-gen](https://github.com/lxgicstudios/redis-schema-gen)
- Twitter：[@lxgicstudios](https://x.com/lxgicstudios)