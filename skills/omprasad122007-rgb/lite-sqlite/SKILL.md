---
name: lite-sqlite
description: 这是一个专为 OpenClaw 代理设计的快速、轻量级的本地 SQLite 数据库，具有极低的 RAM 和存储占用率。适用于高效创建或管理用于存储代理数据的 SQLite 数据库的场景。非常适合用于本地数据持久化、快速代理数据存储、低内存环境下的数据库应用，以及代理的备忘录和缓存存储需求。
---
# Lite SQLite – 轻量级本地数据库

这款超轻量级的SQLite数据库管理工具专为OpenClaw代理设计，适用于内存占用较低（约2-5MB）且对存储空间要求不高的环境。

## 为什么选择SQLite？

✅ **无需设置**：无需服务器，无需配置，基于文件存储。
✅ **低内存需求**：典型使用情况下仅需2-5MB内存。
✅ **性能快速**：每秒可处理数百万条查询。
✅ **便携性**：仅依赖一个.db文件。
✅ **可靠性**：遵循ACID规范，具有防崩溃机制。
✅ **跨平台**：支持所有支持Python的平台。

## 核心特性

- **内存模式**：用于存储临时数据（速度更快！）
- **WAL模式**：支持并发访问。
- **连接池**：提高连接效率。
- **自动模式迁移**：自动处理数据库结构变化。
- **内置备份/恢复功能**：方便数据备份与恢复。
- **查询优化建议**：提供优化查询的提示。

## 快速入门

### 基本数据库操作

```python
from sqlite_connector import SQLiteDB

# Create database (auto-wal mode enabled)
db = SQLiteDB("agent_data.db")

# Create table
db.create_table("memos", {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "title": "TEXT NOT NULL",
    "content": "TEXT",
    "created_at": "TEXT DEFAULT CURRENT_TIMESTAMP",
    "tags": "TEXT"
})

# Insert data
db.insert("memos", [title="First memo", content="Hello world", tags="test"])

# Query data
results = db.query("SELECT * FROM memos WHERE tags = ?", ("test",))

# Update data
db.update("memos", "id = ?", [content="Updated content"], (1,))

# Delete data
db.delete("memos", "id = ?", (1,))

# Close connection
db.close()
```

### 内存数据库（速度最快）

```python
# Fastest mode - RAM only, no disk I/O
db = SQLiteDB(":memory:")

# Perfect for temporary operations
db.create_table("temp", {...})

# Data persists only during session
# Use for caching, computations, temporary storage
```

---

## 性能优化

### 关键配置设置

```python
import sqlite3

# WAL mode (Write-Ahead Logging) - 3-4x faster
conn = sqlite3.connect("agent_data.db")
conn.execute("PRAGMA journal_mode=WAL")

# Sync OFF (faster writes, crash-safe with proper shutdown)
conn.execute("PRAGMA synchronous=NORMAL")

# Memory optimization
conn.execute("PRAGMA cache_size=-64000")  # 64MB cache
conn.execute("PRAGMA page_size=4096")

# Temp store in RAM
conn.execute("PRAGMA temp_store=MEMORY")
```

### 查询优化

```python
# Use indexes for frequent queries
db.create_index("memos", "tags")
db.create_index("memos", "created_at")

# Use prepared statements (automatic in our wrapper)
db.query("SELECT * FROM memos WHERE id = ?", (id,))

# Batch inserts for large datasets
db.batch_insert("memos", rows_data)
```

---

## 预定义数据库模式

### 代理备忘录模式（内存存储）

```python
db.create_table("agent_memos", {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "agent_id": "TEXT NOT NULL",           # Which agent created it
    "key": "TEXT NOT NULL",               # Lookup key
    "value": "TEXT",                      # Stored value
    "priority": "INTEGER DEFAULT 0",       # For retrieval ordering
    "created_at": "TEXT DEFAULT CURRENT_TIMESTAMP",
    "expires_at": "TEXT"                  # Optional TTL
})

# Create indexes
db.create_index("agent_memos", "agent_id")
db.create_index("agent_memos", "key")
db.create_index("agent_memos", "expires_at")
```

### 会话日志模式

```python
db.create_table("session_logs", {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "session_id": "TEXT NOT NULL",
    "agent": "TEXT NOT NULL",
    "message": "TEXT",
    "metadata": "TEXT",                   # JSON
    "created_at": "TEXT DEFAULT CURRENT_TIMESTAMP"
})

db.create_index("session_logs", "session_id")
db.create_index("session_logs", "created_at")
```

### 缓存模式（基于TTL）

```python
db.create_table("cache", {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "key": "TEXT UNIQUE NOT NULL",
    "value": "BLOB",                      # Supports binary data
    "created_at": "TEXT DEFAULT CURRENT_TIMESTAMP",
    "expires_at": "TEXT NOT NULL"
})

# Auto-cleanup expired entries
db.query("DELETE FROM cache WHERE expires_at < ?", (datetime.now().isoformat(),))

db.create_index("cache", "key")
db.create_index("cache", "expires_at")
```

---

## 高级特性

### 连接池

```python
from sqlite_connector import ConnectionPool

# Pool of connections for concurrent access
pool = ConnectionPool("agent_data.db", max_connections=5)

# Get connection
conn = pool.get_connection()
# Use conn...
pool.release_connection(conn)
```

### 自动备份

```python
# Backup database
db.backup("agent_data_backup.db")

# Automatic daily backup
db.auto_backup("backups/", "daily")
```

### 模式迁移

```python
# Add column if not exists
db.add_column("memos", "updated_at", "TEXT DEFAULT CURRENT_TIMESTAMP")

# Migrate data
db.migrate("memos", {
    "old_column": "new_column"
})
```

---

## 性能基准测试

### 典型性能指标

| 操作        | 行数        | 内存模式耗时（秒） | 磁盘模式耗时（秒） |
|------------|------------|------------------|-------------------|
| 插入        | 10,000       | 0.05            | 0.3               |
| 查询（带索引）    | 10,000       | 0.001            | 0.01               |
| 查询（全扫描）    | 10,000       | 0.05            | 0.5               |
| 更新        | 1,000       | 0.01            | 0.1               |
| 删除        | 1,000       | 0.01            | 0.1               |

### 内存使用情况

- 基础内存：2-5MB
- 存储10万行数据时：约10-15MB
- 存储100万行数据时：约50-100MB
- 使用内存模式时：数据大小加上额外开销

---

## OpenClaw代理的最佳实践

### 1. 选择合适的数据库模式

```python
# Use :memory: for temporary operations
temp_db = SQLiteDB(":memory:")

# Use file DB for persistent storage
persist_db = SQLiteDB("agent_storage.db")
```

### 2. 正确使用索引

```python
# Always index columns used in WHERE clauses
db.create_index("table", "column_name")

# Index multiple columns for composite queries
db.create_index("table", "col1, col2")
```

### 3. 批量处理数据

```python
# Instead of individual inserts:
for row in rows:
    db.insert("table", row)  # Slow!

# Use batch insert:
db.batch_insert("table", rows)  # Fast!
```

### 4. 使用TTL机制管理过期数据

```python
# Auto-cleanup old data
db.cleanup_expired("cache", "expires_at")
db.cleanup_old("logs", "created_at", days=7)
```

### 5. 定期压缩数据库

```python
# Reclaim space after many deletes
db.vacuum()  # Should be run during downtime
```

---

## DuckDB替代方案（用于数据分析）

对于需要复杂分析（如数据聚合、大数据集连接操作）的场景，可以考虑使用DuckDB：

```python
import duckdb

conn = duckdb.connect(":memory:")

# Faster than SQLite for complex analytics
conn.execute("""
    SELECT COUNT(*) as rows,
           AVG(value) as avg_value
    FROM large_table
""").fetchall()
```

**DuckDB适用场景：**
- 大规模数据集（超过1亿行）的分析
- 复杂的数据聚合和连接操作
- 列式数据操作
- 统计分析

**SQLite适用场景：**
- 需要事务处理的操作
- 数据量较小到中等（少于1亿行）
- 单点查询和更新操作
- 通用数据存储需求

---

## 常见使用模式

### 1. 备忘录存储

```python
def save_memo(db, agent_id, key, value, ttl_hours=24):
    expires_at = (datetime.now() + timedelta(hours=ttl_hours)).isoformat()
    db.insert("agent_memos", {
        "agent_id": agent_id,
        "key": key,
        "value": json.dumps(value),
        "expires_at": expires_at
    })
```

### 2. 会话持久化

```python
def save_session(db, session_id, agent, message, metadata=None):
    db.insert("session_logs", {
        "session_id": session_id,
        "agent": agent,
        "message": message,
        "metadata": json.dumps(metadata) if metadata else None
    })
```

### 3. 缓存机制

```python
def cache_get(db, key):
    if expired_key := db.query_one(
        "SELECT value FROM cache WHERE key = ? AND expires_at > ?",
        (key, datetime.now().isoformat())
    ):
        return json.loads(expired_key)
    return None

def cache_set(db, key, value, ttl_seconds=3600):
    expires_at = (datetime.now() + timedelta(seconds=ttl_seconds)).isoformat()
    db.insert_or_replace("cache", {
        "key": key,
        "value": json.dumps(value),
        "expires_at": expires_at
    })
```

---

## 错误处理

```python
try:
    db.insert("metrics", {...})
except sqlite3.IntegrityError:
    # Duplicate key violation
    pass
except sqlite3.OperationalError:
    # Table doesn't exist or database locked
    pass
```

---

## 优化数据库大小的建议

### 减少存储空间

1. **选择合适的数据类型**：
   - 使用INTEGER代替TEXT存储数值型数据
   - 使用REAL代替TEXT存储浮点型数据
   - 使用CHECK约束进行数据验证。
2. **规范化数据结构**：
   - 将JSON数据存储为TEXT格式
   - 对于可变长度的字符串使用TEXT类型
   - 避免存储冗余数据。
3. **定期执行数据清理（Vacuum操作）**：```python
   db.vacuum()  # Reclaims space after deletes
   ```
4. **使用WAL模式代替日志模式**：```python
   conn.execute("PRAGMA journal_mode=WAL")
   ```

---

## 从其他数据库迁移数据

### 从JSON文件迁移

```python
# Load JSON into SQLite
import json

with open("data.json") as f:
    data = json.load(f)

db.create_table("json_data", {key: "TEXT" for key in data[0].keys()})
db.batch_insert("json_data", data)
```

### 从CSV文件迁移

```python
import pandas as pd

df = pd.read_csv("data.csv")
df.to_sql("csv_data", conn, if_exists="replace", index=False)
```

---

## 故障排除

### 数据库锁定问题

```python
# Use WAL mode for concurrent access
conn.execute("PRAGMA journal_mode=WAL")

# Or use connection pool
pool = ConnectionPool("db.db", timeout=5.0)
```

### 查询性能缓慢问题

```python
# Check query plan
plan = conn.execute("EXPLAIN QUERY PLAN SELECT * FROM ...").fetchall()

# Add indexes
db.create_index("table", "column")

# Use ANALYZE
conn.execute("ANALYZE")
```

### 数据库容量过大问题

```python
# Check size info
size_info = conn.execute("PRAGMA page_count, page_size").fetchone()
print(f"Size: {(page_count * page_size) / (1024*1024):.2f} MB")

# Vacuum to reclaim space
db.vacuum()
```

---

## 命令行工具

随附的`sqlite_cli.py`提供了命令行访问接口：

```bash
# Create database
python scripts/sqlite_cli.py create agent_data.db

# Add table
python scripts/sqlite_cli.py create-table agent_memos -c id:INTEGER:P -c title:TEXT -c content:TEXT

# Insert data
python scripts/sqlite_cli.py insert agent_memos '{"title": "Test", "content": "Hello"}'

# Query data
python scripts/sqlite_cli.py query "SELECT * FROM agent_memos"

# Optimize
python scripts/sqlite_cli.py optimize agent_data.db
```

---

## 参考资源

- **SQLite官方文档**：https://www.sqlite.org/docs.html
- **Python的sqlite3库**：https://docs.python.org/3/library/sqlite3.html
- **DuckDB**：https://duckdb.org/docs/
- **SQLite性能概述**：https://www.sqlite.org/optoverview.html