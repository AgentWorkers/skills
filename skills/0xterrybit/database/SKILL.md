---
name: database
description: 数据库管理与查询：能够连接到 SQL 和 NoSQL 数据库，执行查询操作，并管理数据库架构（即数据表结构）。
metadata: {"clawdbot":{"emoji":"🗄️","always":true,"requires":{"bins":["curl","jq"]}}}
---

# 数据库 🗄️

数据库管理与查询功能。

## 支持的数据库

- PostgreSQL
- MySQL
- SQLite
- MongoDB
- Redis

## 主要功能

- 执行 SQL 查询
- 数据库模式管理
- 数据导出/导入
- 数据备份与恢复
- 性能监控

## 使用示例

```
"Show all tables in database"
"Run query: SELECT * FROM users LIMIT 10"
"Export table to CSV"
```

## 安全规则

1. 在执行 DELETE/DROP 操作前，请务必确认操作内容。
2. 对于没有 WHERE 子句的 SQL 查询，系统会发出警告。