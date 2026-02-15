---
name: postgres
description: PostgreSQL数据库管理：执行查询、管理数据库架构（schemas），并监控数据库性能。
metadata: {"clawdbot":{"emoji":"🐘","always":true,"requires":{"bins":["curl","jq"]}}}
---

# PostgreSQL 🐘

PostgreSQL 是一款开源的关系型数据库管理系统。

## 安装与配置

```bash
export DATABASE_URL="postgresql://user:pass@localhost:5432/dbname"
```

## 主要功能

- SQL 查询执行
- 数据库模式管理
- 索引优化
- 数据备份与恢复
- 性能监控
- 扩展功能管理

## 使用示例

```
"Show all tables"
"Run query: SELECT * FROM users"
"Create index on email column"
"Show slow queries"
```

## 命令行操作

```bash
psql "$DATABASE_URL" -c "SELECT * FROM users LIMIT 10"
```

## 安全使用规则

1. **在执行任何可能破坏数据库的操作之前，请务必确认操作的正确性。**
2. **在对数据库模式进行任何修改之前，请先进行数据备份。**