---
name: surreal-sync
description: "**从 MongoDB、PostgreSQL、MySQL、Neo4j、Kafka 和 JSONL 到 SurrealDB 的数据迁移与同步**  
支持全量及增量式的 CDC（Change Data Capture）同步功能。  
属于 surreal-skills 系列的一部分。"
license: MIT
metadata:
  version: "1.0.2"
  author: "24601"
  parent_skill: "surrealdb"
  snapshot_date: "2026-02-19"
  upstream:
    repo: "surrealdb/surreal-sync"
    release: "v0.3.4"
    sha: "8166b2b041b1"
---
# Surreal-Sync – 数据迁移与同步工具

Surreal-Sync 是一个命令行（CLI）工具，用于将数据从多种数据库源迁移到 SurrealDB，并通过“变更数据捕获”（Change Data Capture, CDC）技术实现数据的完全同步或增量同步。

## 支持的数据库源

| 数据源 | 完整同步 | 增量同步 | 方法 |
|--------|-----------|----------------|--------|
| MongoDB | 是 | 是 | 基于变更流的同步机制 |
| MySQL | 是 | 是 | 基于触发器的 CDC 机制 + 序列检查点 |
| PostgreSQL（使用触发器） | 是 | 是 | 基于触发器的 CDC 机制 + 序列检查点 |
| PostgreSQL（使用 wal2json 插件） | 是 | 是 | 通过 wal2json 插件实现逻辑复制 |
| Neo4j | 是 | 是 | 基于时间戳的跟踪机制 |
| JSONL 文件 | 是 | 不支持 | 从 JSON 行格式批量导入数据 |
| Apache Kafka | 是 | 是 | 通过消费者订阅机制进行数据传输，并支持去重 |

## 快速入门

```bash
# Install surreal-sync (Rust binary)
cargo install surreal-sync

# Full sync from PostgreSQL (trigger-based)
surreal-sync from postgres trigger-full \
  --connection-string "postgresql://user:pass@localhost/mydb" \
  --surreal-endpoint "http://localhost:8000" \
  --surreal-username root \
  --surreal-password root \
  --to-namespace prod \
  --to-database main

# Incremental CDC from PostgreSQL (wal2json)
surreal-sync from postgres wal2json \
  --connection-string "postgresql://user:pass@localhost/mydb" \
  --surreal-endpoint "http://localhost:8000" \
  --surreal-username root \
  --surreal-password root \
  --to-namespace prod \
  --to-database main

# Full sync from MongoDB
surreal-sync from mongo full \
  --connection-string "mongodb://localhost:27017/mydb" \
  --surreal-endpoint "http://localhost:8000" \
  --surreal-username root \
  --surreal-password root \
  --to-namespace prod \
  --to-database main

# Batch import from JSONL
surreal-sync from jsonl import \
  --file data.jsonl \
  --surreal-endpoint "http://localhost:8000" \
  --surreal-username root \
  --surreal-password root \
  --to-namespace prod \
  --to-database main

# Consume from Kafka
surreal-sync from kafka consume \
  --bootstrap-servers "localhost:9092" \
  --topic my-events \
  --surreal-endpoint "http://localhost:8000" \
  --surreal-username root \
  --surreal-password root \
  --to-namespace prod \
  --to-database main
```

## CLI 使用模式

```
surreal-sync from <SOURCE> <COMMAND> \
  --connection-string [CONNECTION STRING] \
  --surreal-endpoint [SURREAL ENDPOINT] \
  --surreal-username [SURREAL USERNAME] \
  --surreal-password [SURREAL PASSWORD] \
  --to-namespace <NS> \
  --to-database <DB>
```

## 主要特性

- 自动推断数据库模式并创建 SurrealDB 表结构 |
- 将源数据库的主键映射为 SurrealDB 中的记录 ID |
- 提取数据之间的关系并生成图结构（graph） |
- 支持配置批量处理的大小和并行度 |
- 支持通过检查点实现同步的恢复功能 |
- 对 Kafka 消费者提供去重功能 |

## 完整文档

请参阅以下规则文件以获取详细使用指南：
- **[rules/surreal-sync.md](../../rules/surreal-sync.md)** – 包含源数据库配置、模式映射、CDC 设置、冲突解决方法以及生产环境部署的相关信息 |
- **[surrealdb/surreal-sync](https://github.com/surrealdb/surreal-sync)** – 上游代码仓库