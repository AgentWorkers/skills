---
name: redis
description: Redis数据库管理：键值操作、缓存、发布/订阅（pub/sub）以及数据结构相关命令。
metadata: {"clawdbot":{"emoji":"🔴","always":true,"requires":{"bins":["curl","jq"]}}}
---

# Redis 🔴

Redis 是一个基于内存的数据库管理系统。

## 安装

```bash
export REDIS_URL="redis://localhost:6379"
```

## 主要特性

- 支持键值操作
- 提供多种数据结构（列表、集合、哈希表）
- 支持发布/订阅（Pub/Sub）消息机制
- 具备缓存管理功能
- 支持时间戳（TTL）控制

## 使用示例

```
"Get key user:123"
"Set cache for 1 hour"
"Show all keys matching user:*"
"Flush cache"
```

## 命令集

```bash
redis-cli GET key
redis-cli SET key value EX 3600
redis-cli KEYS "pattern*"
```