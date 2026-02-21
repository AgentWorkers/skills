---
name: SQL
slug: sql
version: 1.0.1
changelog: "Added SQL Server support, schema design patterns, query patterns (CTEs, window functions), operations guide (backup, monitoring, replication)"
homepage: https://clawic.com/skills/sql
description: 掌握使用 SQL 管理关系型数据库的技能。包括 PostgreSQL、MySQL、SQLite 和 SQL Server 的数据库架构设计、查询语句编写、性能优化以及数据库迁移等方面的知识。
metadata: {"clawdbot":{"emoji":"🗄️","requires":{"anyBins":["sqlite3","psql","mysql","sqlcmd"]},"os":["linux","darwin","win32"]}}
---
# SQL

从命令行层面掌握关系型数据库的用法。涵盖 SQLite、PostgreSQL、MySQL 和 SQL Server，提供经过实践验证的模式，用于数据库模式设计、查询、数据迁移和日常操作。

## 使用场景

适用于关系型数据库的各类工作，包括模式设计、查询编写、数据迁移、性能优化以及备份管理。支持 SQLite、PostgreSQL、MySQL 和 SQL Server。

## 快速参考

| 主题 | 文件名 |
|-------|------|
| 查询模式 | `patterns.md` |
| 模式设计 | `schemas.md` |
| 数据操作 | `operations.md` |

## 核心规则

### 1. 选择合适的数据库

| 使用场景 | 数据库 | 选择理由 |
|----------|----------|-----|
| 本地/嵌入式应用 | SQLite | 零配置，单文件存储 |
| 通用生产环境 | PostgreSQL | 支持最佳数据库标准，支持 JSONB 数据类型及扩展功能 |
| 旧系统/托管环境 | MySQL | 广泛的托管支持 |
| 企业级应用/.NET 环境 | SQL Server | 集成性强，适用于 Windows 环境 |

### 2. 始终使用参数化查询

```python
# ❌ NEVER
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# ✅ ALWAYS
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### 3. 为筛选条件添加索引

在大型表中，WHERE、JOIN ON 或 ORDER BY 子句中使用的任何列都需要添加索引。

### 4. 使用事务

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

### 5. 尽量使用 `EXISTS` 而不是 `IN`

```sql
-- ✅ Faster (stops at first match)
SELECT * FROM orders o WHERE EXISTS (
  SELECT 1 FROM users u WHERE u.id = o.user_id AND u.active
);
```

---

## 快速入门

### SQLite

```bash
sqlite3 mydb.sqlite                              # Create/open
sqlite3 mydb.sqlite "SELECT * FROM users;"       # Query
sqlite3 -header -csv mydb.sqlite "SELECT *..." > out.csv
sqlite3 mydb.sqlite "PRAGMA journal_mode=WAL;"   # Better concurrency
```

### PostgreSQL

```bash
psql -h localhost -U myuser -d mydb              # Connect
psql -c "SELECT NOW();" mydb                     # Query
psql -f migration.sql mydb                       # Run file
\dt  \d+ users  \di+                             # List tables/indexes
```

### MySQL

```bash
mysql -h localhost -u root -p mydb               # Connect
mysql -e "SELECT NOW();" mydb                    # Query
```

### SQL Server

```bash
sqlcmd -S localhost -U myuser -d mydb            # Connect
sqlcmd -Q "SELECT GETDATE()"                     # Query
sqlcmd -S localhost -d mydb -E                   # Windows auth
```

---

## 常见错误与陷阱

### 关于 NULL 的陷阱
- `NOT IN (子查询)`：如果子查询结果中包含 NULL，该操作会返回空结果集 → 应使用 `NOT EXISTS`  
- `NULL = NULL` 的结果仍为 NULL，而非 true → 应使用 `IS NULL`  
- `COUNT(column)` 会排除 NULL 值，而 `COUNT(*)` 会统计所有记录  

### 会降低索引效率的操作
- 对列进行函数操作（如 `WHERE YEAR(date) = 2024`）会导致全表扫描  
- 类型转换操作（如 `WHERE varchar_col = 123`）会忽略索引的加速效果  
- `LIKE '%term'` 无法利用索引加速查询 → 只有 `LIKE 'term%'` 才能利用索引  
- 复合索引（如 `(a, b)` 在仅基于 `b` 进行过滤时无法发挥作用  

### 关于连接操作的陷阱
- 使用 `LEFT JOIN` 时，如果右表没有指定过滤条件，实际操作会变成 `INNER JOIN`  
- 如果缺少连接条件，查询结果可能为笛卡尔积（即所有可能的组合）  
- 多个 `LEFT JOIN` 操作可能导致数据重复  

---

## 解释查询执行过程（EXPLAIN）

```sql
-- PostgreSQL
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 5;

-- SQLite
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 5;
```

**警告信号：**
- 在大型表上使用 `Seq Scan` 执行查询 → 需要为相关列添加索引  
- 过多的数据被过滤掉 → 索引未能有效覆盖查询条件  
- 实际查询结果与预估结果不符 → 需运行 `ANALYZE tablename;` 命令进行优化  

## 索引策略

```sql
-- Composite index (equality first, range last)
CREATE INDEX idx_orders ON orders(user_id, status);

-- Covering index (avoids table lookup)
CREATE INDEX idx_orders ON orders(user_id) INCLUDE (total);

-- Partial index (smaller, faster)
CREATE INDEX idx_pending ON orders(user_id) WHERE status = 'pending';
```

---

## 数据库之间的兼容性

| 特性 | PostgreSQL | MySQL | SQLite | SQL Server |
|---------|------------|-------|--------|------------|
| `LIMIT` 语句 | `LIMIT n` | `LIMIT n` | `LIMIT n` | `TOP n` |
| 插入/更新操作（UPsert） | `ON CONFLICT` | `ON DUPLICATE KEY` | `ON CONFLICT` | `MERGE` |
| 布尔值处理 | `true/false` | `1/0` | `1/0` | `1/0` |
| 字符串连接 | `||` | `CONCAT()` | `||` | `+` |

---

## 相关技能

如用户需要，可使用以下命令安装相关工具：
- `clawhub install prisma`：Node.js 数据库 ORM 工具  
- `clawhub install sqlite`：专门用于 SQLite 的工具集  
- `clawhub install analytics`：数据分析相关工具  

## 反馈建议：
- 如果内容有用，请使用 `clawhub star sql` 给予评分  
- 为了保持信息更新，请使用 `clawhub sync` 命令同步最新内容