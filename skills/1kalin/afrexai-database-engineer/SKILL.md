# 数据库工程精通

> 深入掌握数据库设计、优化、迁移及操作系统管理。从数据库模式设计到生产环境监控——涵盖 PostgreSQL、MySQL、SQLite 及通用 SQL 设计模式。

## 第一阶段 — 数据库模式设计

### 设计概述

在编写任何 DDL 语句之前，请填写以下内容：
```yaml
project: ""
domain: ""
primary_use_case: "OLTP | OLAP | mixed"
expected_scale:
  rows_year_1: ""
  rows_year_3: ""
  concurrent_users: ""
  read_write_ratio: "80:20 | 50:50 | 20:80"
compliance: [] # GDPR, HIPAA, PCI-DSS, SOX
multi_tenancy: "none | schema-per-tenant | row-level | database-per-tenant"
```

### 规范化决策框架

| 规范化级别 | 规则 | 何时进行反规范化 |
|-------------|--------|-------------------|
| 第一范式（1NF） | 无重复字段，所有值都是原子的 | 始终遵循 |
| 第二范式（2NF） | 复合键上不存在部分依赖关系 | 始终遵循 |
| 第三范式（3NF） | 不存在传递依赖关系 | 适用于报告报表和读取密集型聚合操作 |
| 第四范式（BCNF） | 每个决定因素都是候选键 | 除非键关系复杂，否则很少需要 |

**反规范化的触发条件：**
- 需要跨 4 个表进行查询连接 |
- 索引查询的读取延迟超过 100 毫秒 |
- 缓存失效的复杂性高于反规范化的维护成本 |
- 报表查询会阻塞在线事务处理（OLTP）操作

### 命名规范
```
Tables:      snake_case, plural (users, order_items, payment_methods)
Columns:     snake_case, singular (first_name, created_at, is_active)
PKs:         id (bigint/uuid) or {table_singular}_id
FKs:         {referenced_table_singular}_id
Indexes:     idx_{table}_{columns}
Constraints: chk_{table}_{rule}, uq_{table}_{columns}, fk_{table}_{ref}
Enums:       Use VARCHAR + CHECK, not DB enums (easier to migrate)
Booleans:    is_, has_, can_ prefix (is_active, has_subscription)
Timestamps:  _at suffix (created_at, updated_at, deleted_at)
```

### 列类型决策树
```
Text < 255 chars, fixed set?     → VARCHAR(N) + CHECK
Text < 255 chars, variable?      → VARCHAR(255)
Text > 255 chars?                → TEXT
Whole numbers < 2B?              → INTEGER
Whole numbers > 2B?              → BIGINT
Money/financial?                 → NUMERIC(precision, scale) — NEVER float
True/false?                      → BOOLEAN
Date only?                       → DATE
Date + time?                     → TIMESTAMPTZ (always with timezone)
Unique identifier?               → UUID (distributed) or BIGSERIAL (single DB)
JSON/flexible schema?            → JSONB (Postgres) or JSON (MySQL)
Binary/file?                     → Store in object storage, reference by URL
IP address?                      → INET (Postgres) or VARCHAR(45)
Geospatial?                      → PostGIS geometry/geography types
```

### 基本表模板
```sql
CREATE TABLE {table_name} (
    id          BIGSERIAL PRIMARY KEY,
    -- domain columns here --
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by  BIGINT REFERENCES users(id),
    version     INTEGER NOT NULL DEFAULT 1,  -- optimistic locking
    
    -- soft delete (optional)
    deleted_at  TIMESTAMPTZ,
    
    -- multi-tenant (optional)  
    tenant_id   BIGINT NOT NULL REFERENCES tenants(id)
);

-- Updated_at trigger (PostgreSQL)
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    NEW.version = OLD.version + 1;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_{table_name}_updated
    BEFORE UPDATE ON {table_name}
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();
```

### 关系模式设计

- **一对多（One-to-Many）：**
```sql
-- Parent
CREATE TABLE departments (id BIGSERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL);
-- Child  
CREATE TABLE employees (
    id BIGSERIAL PRIMARY KEY,
    department_id BIGINT NOT NULL REFERENCES departments(id) ON DELETE RESTRICT,
    -- ON DELETE options: RESTRICT (safe default), CASCADE (children die), SET NULL
);
CREATE INDEX idx_employees_department_id ON employees(department_id);
```

- **多对多（Many-to-Many）：**
```sql
CREATE TABLE user_roles (
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id BIGINT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    granted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    granted_by BIGINT REFERENCES users(id),
    PRIMARY KEY (user_id, role_id)
);
```

- **自引用（层次结构）：**
```sql
CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    parent_id BIGINT REFERENCES categories(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    depth INTEGER NOT NULL DEFAULT 0,
    path TEXT NOT NULL DEFAULT ''  -- materialized path: '/1/5/12/'
);
CREATE INDEX idx_categories_parent ON categories(parent_id);
CREATE INDEX idx_categories_path ON categories(path text_pattern_ops);
```

- **多态性（尽可能避免，必要时使用）：**
```sql
-- Preferred: separate FKs
CREATE TABLE comments (
    id BIGSERIAL PRIMARY KEY,
    post_id BIGINT REFERENCES posts(id),
    ticket_id BIGINT REFERENCES tickets(id),
    body TEXT NOT NULL,
    CONSTRAINT chk_one_parent CHECK (
        (post_id IS NOT NULL)::int + (ticket_id IS NOT NULL)::int = 1
    )
);
```

---

## 第二阶段 — 索引策略

### 索引类型选择

| 索引类型 | 适用场景 | 示例 |
|---------|---------|--------|
| B 树（默认） | 等值查询、范围查询、排序查询、LIKE ‘prefix%’ | `CREATE INDEX idx_users_email ON users(email)` |
| 哈希索引（Hash） | 仅适用于等值查询，不支持范围查询 | `CREATE INDEX idx_sessions_token ON sessions USING hash(token)` |
| GIN 索引 | 适用于 JSONB 数据、全文搜索、数组和 tsvector 类型 | `CREATE INDEX idx_products_tags ON products USING gin(tags)` |
| GiST 索引 | 适用于地理空间数据、范围查询和最近邻查找 | `CREATE INDEX idx_locations_geom ON locations USING gist(geom)` |
| BRIN 索引 | 适用于具有自然排序顺序的大型表（如时间序列数据） | `CREATE INDEX idx_events_created ON events USING brin creado_at)` |
| 部分索引（Partial Index） | 适用于部分数据行的查询 | `CREATE INDEX idx_orders_pending ON orders creado_at WHERE status = 'pending'` |
| 覆盖索引（Covering Index） | 包含查询中需要的所有列，以减少表查找次数 | `CREATE INDEX idx_orders_user ON orders(user_id) INCLUDE (status, total)` |

### 索引设计规则：
1. **必须创建的索引：** 外键列、WHERE/JOIN/ORDER BY 子句中使用的列。
2. **无需创建的索引：** 单个低基数列（例如布尔值或只有 3 个值的列）——应将其组合成复合键。
3. **索引创建顺序：** 先创建选择性最高的列索引，然后按照从左到右的顺序创建其他索引。
4. **注意写操作的开销：** 每个索引都会增加 INSERT/UPDATE 操作的性能开销。如果一个数据表上有超过 8 个索引，建议重新评估索引策略。
5. **检查未使用的索引：** 定期（每月）检查数据库中未使用的索引，并删除那些很少被访问的索引。

### 查找未使用的索引（PostgreSQL）
```sql
SELECT schemaname, tablename, indexname, idx_scan, 
       pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE idx_scan = 0 AND indexrelid NOT IN (
    SELECT conindid FROM pg_constraint WHERE contype IN ('p', 'u')
)
ORDER BY pg_relation_size(indexrelid) DESC;
```

### 查找缺失的索引（PostgreSQL）
```sql
SELECT relname, seq_scan, seq_tup_read, 
       idx_scan, seq_tup_read / GREATEST(seq_scan, 1) as avg_tuples_per_scan
FROM pg_stat_user_tables
WHERE seq_scan > 100 AND seq_tup_read > 10000
ORDER BY seq_tup_read DESC;
-- High seq_scan + high seq_tup_read = missing index candidate
```

---

## 第三阶段 — 查询优化

### EXPLAIN 解释

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;
```

**查询计划中的警示信号：**
| 问题 | 解决方案 |
|---------|---------|
| 在大型表上进行顺序扫描（Seq Scan） | 缺少相应的索引 | 添加相应的索引 |
| 外层循环嵌套（Nested Loop with large outer） | 使用哈希连接（Hash Join） |
| 排序操作性能低下 | 缺少 ORDER BY 子句所需的索引 | 添加相应的索引 |
| 哈希连接导致磁盘I/O操作过多 | 调整 work_mem 值或减少查询结果集的大小 |
| 图像堆扫描（Bitmap Heap Scan）效率低下 | 使用更具选择性的索引或部分索引 |
| 子查询（SubQuery）执行效率低下 | 优化子查询的编写方式 |

### 常见的查询优化技巧与解决方法：
- **在生产环境中避免使用 SELECT *：** 
```sql
-- Bad: fetches all columns, breaks covering indexes
SELECT * FROM orders WHERE user_id = 123;
-- Good: explicit columns
SELECT id, status, total, created_at FROM orders WHERE user_id = 123;
```

- **避免使用 N+1 查询结构：** 
```sql
-- Bad: 1 query for users + N queries for orders
SELECT id FROM users WHERE active = true;  -- returns 100 rows
SELECT * FROM orders WHERE user_id = ?;     -- called 100 times

-- Good: single JOIN or IN
SELECT u.id, o.id, o.total 
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.active = true;
```

- **避免在索引列上使用函数：** 
```sql
-- Bad: can't use index on created_at
WHERE EXTRACT(YEAR FROM created_at) = 2025
-- Good: range scan uses index
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01'

-- Bad: can't use index on email  
WHERE LOWER(email) = 'user@example.com'
-- Good: expression index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
```

- **避免使用 OR 条件导致索引失效：** 
```sql
-- Bad: often causes Seq Scan
WHERE status = 'pending' OR status = 'processing'
-- Good: IN uses index
WHERE status IN ('pending', 'processing')
```

- **使用 OFFSET 进行分页时：** 
```sql
-- Bad: OFFSET 10000 scans and discards 10000 rows
SELECT * FROM products ORDER BY id LIMIT 20 OFFSET 10000;
-- Good: keyset pagination
SELECT * FROM products WHERE id > :last_seen_id ORDER BY id LIMIT 20;
```

- **避免对大型表使用 COUNT(*)：** 
```sql
-- Bad: full table scan
SELECT COUNT(*) FROM events;
-- Good: approximate count (PostgreSQL)
SELECT reltuples::bigint FROM pg_class WHERE relname = 'events';
-- Or maintain a counter cache table
```

### 窗口函数参考
```sql
-- Running total
SELECT id, amount, SUM(amount) OVER (ORDER BY created_at) as running_total FROM payments;

-- Rank within group
SELECT *, RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) as dept_rank FROM employees;

-- Previous/next row
SELECT *, LAG(amount) OVER (ORDER BY created_at) as prev_amount,
          LEAD(amount) OVER (ORDER BY created_at) as next_amount FROM payments;

-- Moving average
SELECT *, AVG(amount) OVER (ORDER BY created_at ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as ma_7 FROM daily_sales;

-- Percent of total
SELECT *, amount / SUM(amount) OVER () * 100 as pct_of_total FROM line_items WHERE order_id = 1;
```

### 公共表表达式（CTE）的使用
```sql
-- Recursive: org chart traversal
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, 1 as depth FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, o.depth + 1
    FROM employees e JOIN org o ON e.manager_id = o.id
    WHERE o.depth < 10  -- safety limit
)
SELECT * FROM org ORDER BY depth, name;

-- Data pipeline: clean → transform → aggregate
WITH cleaned AS (
    SELECT *, TRIM(LOWER(email)) as clean_email FROM raw_signups WHERE email IS NOT NULL
),
deduped AS (
    SELECT DISTINCT ON (clean_email) * FROM cleaned ORDER BY clean_email, created_at DESC
)
SELECT DATE_TRUNC('week', created_at) as week, COUNT(*) FROM deduped GROUP BY 1 ORDER BY 1;
```

---

## 第四阶段 — 数据库迁移

### 迁移安全规则：
1. **在生产环境中**，切勿直接重命名列或表。
2. **切勿在已有数据的表上添加 NOT NULL 约束，除非同时为该列设置 DEFAULT 值。**
3. **切勿删除应用程序代码仍在引用的列。**
4. **务必先在测试环境中使用生产数据的副本进行迁移测试。**
5. **务必制定回滚计划（包括数据回滚方案）。**
6. **在对生产环境进行任何模式更改之前，务必备份数据。**

### 安全的迁移方法：
- **添加新列：** 
```sql
-- Step 1: Add nullable column
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
-- Step 2: Backfill (in batches!)
UPDATE users SET phone = '' WHERE phone IS NULL AND id BETWEEN 1 AND 10000;
-- Step 3: Add NOT NULL after backfill
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;
ALTER TABLE users ALTER COLUMN phone SET DEFAULT '';
```

- **重命名列：** 
```sql
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(200);
-- Step 2: Dual-write in application code (write to both old + new)
-- Step 3: Backfill
UPDATE users SET full_name = name WHERE full_name IS NULL;
-- Step 4: Switch application to read from new column
-- Step 5: Drop old column (after confirming no reads)
ALTER TABLE users DROP COLUMN name;
```

- **在不锁定表的情况下添加索引（PostgreSQL）：** 
```sql
CREATE INDEX CONCURRENTLY idx_orders_customer ON orders(customer_id);
-- Takes longer but doesn't lock the table
```

- **批量导入大型表数据：** 
```sql
-- Don't: UPDATE millions of rows in one transaction
-- Do: batch it
DO $$
DECLARE
    batch_size INT := 5000;
    affected INT;
BEGIN
    LOOP
        UPDATE users SET normalized_email = LOWER(email)
        WHERE normalized_email IS NULL AND id IN (
            SELECT id FROM users WHERE normalized_email IS NULL LIMIT batch_size
        );
        GET DIAGNOSTICS affected = ROW_COUNT;
        RAISE NOTICE 'Updated % rows', affected;
        EXIT WHEN affected = 0;
        COMMIT;
    END LOOP;
END $$;
```

### 迁移文件模板
```sql
-- Migration: YYYYMMDDHHMMSS_description.sql
-- Author: [name]
-- Ticket: [JIRA/Linear ID]
-- Risk: low|medium|high
-- Rollback: see DOWN section
-- Estimated time: [for production data volume]
-- Requires: [prerequisite migrations]

-- ========== UP ==========
BEGIN;

-- [DDL/DML here]

COMMIT;

-- ========== DOWN ==========
-- BEGIN;
-- [Rollback DDL/DML here]
-- COMMIT;

-- ========== VERIFY ==========
-- [Queries to confirm migration succeeded]
-- SELECT COUNT(*) FROM ... WHERE ...;
```

---

## 第五阶段 — 性能监控

### 关键性能指标仪表盘
```yaml
health_metrics:
  connections:
    active: "SELECT count(*) FROM pg_stat_activity WHERE state = 'active'"
    idle: "SELECT count(*) FROM pg_stat_activity WHERE state = 'idle'"
    max: "SHOW max_connections"
    threshold: "active > 80% of max = ALERT"
    
  cache_hit_ratio:
    query: |
      SELECT ROUND(100.0 * sum(heap_blks_hit) / 
             NULLIF(sum(heap_blks_hit) + sum(heap_blks_read), 0), 2) as ratio
      FROM pg_statio_user_tables
    healthy: "> 99%"
    warning: "< 95%"
    critical: "< 90%"
    
  index_hit_ratio:
    query: |
      SELECT ROUND(100.0 * sum(idx_blks_hit) / 
             NULLIF(sum(idx_blks_hit) + sum(idx_blks_read), 0), 2) as ratio
      FROM pg_statio_user_indexes
    healthy: "> 99%"
    
  table_bloat:
    query: |
      SELECT relname, n_dead_tup, n_live_tup,
             ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup, 0), 2) as dead_pct
      FROM pg_stat_user_tables WHERE n_dead_tup > 10000
      ORDER BY n_dead_tup DESC LIMIT 10
    action: "VACUUM ANALYZE {table} when dead_pct > 20%"
    
  slow_queries:
    query: |
      SELECT query, calls, mean_exec_time, total_exec_time
      FROM pg_stat_statements
      ORDER BY mean_exec_time DESC LIMIT 20
    action: "Optimize top 5 by total_exec_time first"
    
  replication_lag:
    query: |
      SELECT EXTRACT(EPOCH FROM replay_lag) as lag_seconds
      FROM pg_stat_replication
    warning: "> 5 seconds"
    critical: "> 30 seconds"
```

### 表大小分析
```sql
SELECT 
    relname as table,
    pg_size_pretty(pg_total_relation_size(relid)) as total_size,
    pg_size_pretty(pg_relation_size(relid)) as table_size,
    pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) as index_size,
    n_live_tup as row_count
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 20;
```

### 锁定情况监控
```sql
-- Find blocking queries
SELECT 
    blocked.pid as blocked_pid,
    blocked.query as blocked_query,
    blocking.pid as blocking_pid,
    blocking.query as blocking_query,
    NOW() - blocked.query_start as blocked_duration
FROM pg_stat_activity blocked
JOIN pg_locks bl ON bl.pid = blocked.pid
JOIN pg_locks kl ON kl.locktype = bl.locktype AND kl.relation = bl.relation AND kl.pid != bl.pid
JOIN pg_stat_activity blocking ON blocking.pid = kl.pid
WHERE NOT bl.granted;
```

---

## 第六阶段 — 备份与恢复

### 备份策略选择：

| 备份方法 | 数据恢复点（RPO） | 备份速度 | 适用场景 |
|---------|-------------|-----------|---------|
| pg_dump（逻辑备份） | 瞬间备份 | 适用于数据量较小的数据库（<50GB），适用于跨版本迁移 |
| pg_basebackup（物理备份） | 持续备份（使用 WAL） | 适用于大型数据库，适用于相同版本的数据库恢复 |
| WAL 归档（PITR） | 几秒钟内完成备份 | 适用于需要近乎零数据丢失风险的生产环境 |
| 备份副本提升（Replica Promotion） | 几秒钟内完成备份 | 适用于高可用性（HA）场景下的快速恢复 |

### 常用的备份命令
```bash
# Logical backup (compressed)
pg_dump -Fc -Z 9 -j 4 -d mydb -f backup_$(date +%Y%m%d_%H%M%S).dump

# Restore
pg_restore -d mydb -j 4 --clean --if-exists backup_20260216.dump

# Schema only
pg_dump -s -d mydb -f schema.sql

# Single table
pg_dump -t orders -d mydb -f orders_backup.dump

# Physical backup
pg_basebackup -D /backup/base -Ft -z -P -X stream
```

### 备份验证检查项：
- 备份操作是否顺利完成。
- 备份文件的大小是否在预期范围内。
- 是否能够成功恢复到测试数据库。
- 恢复后的表行数是否与生产环境一致。
- 应用程序是否能够连接到恢复后的数据库并执行查询。
- 是否对恢复后的数据进行了自动化测试。
- 是否验证了备份数据的加密效果。
- 是否已经将备份数据复制到了异地。

---

## 第七阶段 — 数据库安全

### 访问控制检查
```sql
-- Create application role (least privilege)
CREATE ROLE app_user LOGIN PASSWORD 'use-vault-not-plaintext';
GRANT CONNECT ON DATABASE mydb TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
-- NO: GRANT ALL, superuser, CREATE, DROP

-- Read-only role for analytics
CREATE ROLE analyst LOGIN PASSWORD 'use-vault';
GRANT CONNECT ON DATABASE mydb TO analyst;
GRANT USAGE ON SCHEMA public TO analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analyst;

-- Row-Level Security (multi-tenant)
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.tenant_id')::bigint);
```

### 防止 SQL 注入攻击
```
RULE 1: NEVER concatenate user input into SQL strings
RULE 2: Always use parameterized queries / prepared statements
RULE 3: Validate and whitelist table/column names if dynamic
RULE 4: Use ORMs for CRUD, raw SQL only for complex queries
RULE 5: Audit logs for unusual query patterns (UNION, DROP, --)
```

### 数据保护措施
```sql
-- Encrypt sensitive columns (application-level)
-- Store: pgp_sym_encrypt(data, key) 
-- Read: pgp_sym_decrypt(encrypted_col, key)

-- Audit trail table
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id BIGINT NOT NULL,
    action VARCHAR(10) NOT NULL, -- INSERT, UPDATE, DELETE
    old_data JSONB,
    new_data JSONB,
    changed_by BIGINT REFERENCES users(id),
    changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ip_address INET
);

-- Generic audit trigger
CREATE OR REPLACE FUNCTION audit_trigger() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, record_id, action, old_data, new_data, changed_by)
    VALUES (
        TG_TABLE_NAME,
        COALESCE(NEW.id, OLD.id),
        TG_OP,
        CASE WHEN TG_OP != 'INSERT' THEN to_jsonb(OLD) END,
        CASE WHEN TG_OP != 'DELETE' THEN to_jsonb(NEW) END,
        current_setting('app.user_id', true)::bigint
    );
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
```

---

## 第八阶段 — PostgreSQL 配置优化

### 根据服务器内存大小调整配置参数：

| 参数 | 小型服务器（4GB RAM） | 中型服务器（16GB RAM） | 大型服务器（64GB及以上） |
|---------|-----------------|-----------------|-------------------|
| shared_buffers | 1GB | 4GB | 16GB |
| effective_cache_size | 3GB | 12GB | 48GB |
| work_mem | 16MB | 64MB | 256MB |
| maintenance_work_mem | 256MB | 1GB | 2GB |
| max_connections | 100 | 200 | 300 |
| wal_buffers | 64MB | 128MB | 256MB |
| random_page_cost | 1.1（适用于 SSD） | 1.1（适用于 SSD） | 1.1（适用于 SSD） |
| effective_io_concurrency | 200（适用于 SSD） | 200（适用于 SSD） | 200（适用于 SSD） |
| max_parallel_workers_per_gather | 2 | 4 | 8 |

### 连接池管理（使用 PgBouncer）
```ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction          # transaction pooling (best for most apps)
max_client_conn = 1000           # accept up to 1000 app connections
default_pool_size = 25           # 25 actual DB connections per database
reserve_pool_size = 5            # extra connections for burst
reserve_pool_timeout = 3         # seconds before using reserve
server_idle_timeout = 300        # close idle server connections after 5 min
```

---

## 第九阶段 — 常见数据库优化技巧

- **软删除（Soft Delete）：** 
```sql
-- Add to table
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;
CREATE INDEX idx_users_active ON users(id) WHERE deleted_at IS NULL;

-- Application queries always filter
SELECT * FROM users WHERE deleted_at IS NULL AND ...;

-- Or use a view
CREATE VIEW active_users AS SELECT * FROM users WHERE deleted_at IS NULL;
```

- **乐观锁（Optimistic Locking）：** 
```sql
UPDATE products SET 
    price = 29.99, 
    version = version + 1, 
    updated_at = NOW()
WHERE id = 123 AND version = 5;  -- expected version
-- If 0 rows affected → concurrent modification → retry or error
```

- **事件源表设计（Event Sourcing Table）：** 
```sql
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    aggregate_type VARCHAR(50) NOT NULL,
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    metadata JSONB DEFAULT '{}',
    version INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (aggregate_id, version)
);
CREATE INDEX idx_events_aggregate ON events(aggregate_id, version);
CREATE INDEX idx_events_type ON events(event_type, created_at);
```

- **时间序列数据优化：** 
```sql
-- Partitioned by month
CREATE TABLE metrics (
    id BIGSERIAL,
    sensor_id INTEGER NOT NULL,
    value NUMERIC(12,4) NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (recorded_at);

CREATE TABLE metrics_2026_01 PARTITION OF metrics
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE metrics_2026_02 PARTITION OF metrics
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

-- Auto-create future partitions via cron or pg_partman
-- Use BRIN index for time-series
CREATE INDEX idx_metrics_time ON metrics USING brin(recorded_at);
```

- **全文搜索（PostgreSQL）：** 
```sql
-- Add search column
ALTER TABLE articles ADD COLUMN search_vector tsvector;
CREATE INDEX idx_articles_search ON articles USING gin(search_vector);

-- Populate
UPDATE articles SET search_vector = 
    setweight(to_tsvector('english', COALESCE(title, '')), 'A') ||
    setweight(to_tsvector('english', COALESCE(body, '')), 'B');

-- Search with ranking
SELECT id, title, ts_rank(search_vector, query) as rank
FROM articles, plainto_tsquery('english', 'database optimization') query
WHERE search_vector @@ query
ORDER BY rank DESC LIMIT 20;
```

- **JSONB 数据类型优化：** 
```sql
-- Store flexible attributes
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    attributes JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index specific JSON paths
CREATE INDEX idx_products_color ON products((attributes->>'color'));
-- Or GIN for any key lookups
CREATE INDEX idx_products_attrs ON products USING gin(attributes);

-- Query patterns
SELECT * FROM products WHERE attributes->>'color' = 'red';
SELECT * FROM products WHERE attributes @> '{"size": "large"}';
SELECT * FROM products WHERE attributes ? 'warranty';
```

---

## 第十阶段 — 日常运维流程

### 应急处理方案：
- **数据库负载过重：** 
```sql
-- 1. Find and kill long-running queries
SELECT pid, NOW() - query_start as duration, query 
FROM pg_stat_activity WHERE state = 'active' AND query_start < NOW() - INTERVAL '5 minutes'
ORDER BY duration DESC;

-- Kill a specific query
SELECT pg_cancel_backend(pid);    -- graceful
SELECT pg_terminate_backend(pid); -- force

-- 2. Check for lock contention (see Phase 5)

-- 3. Reduce max connections temporarily
-- In pgbouncer: pause database, reduce pool, resume

-- 4. Check if VACUUM is needed
SELECT relname, n_dead_tup, last_autovacuum FROM pg_stat_user_tables 
WHERE n_dead_tup > 100000 ORDER BY n_dead_tup DESC;
```

- **磁盘空间不足：** 
```bash
# 1. Check what's consuming space
du -sh /var/lib/postgresql/*/main/ 2>/dev/null || du -sh /var/lib/mysql/

# 2. Clean up WAL files (PostgreSQL) — CAREFUL
# Check replication slot status first
SELECT slot_name, active FROM pg_replication_slots;
# Drop inactive slots consuming WAL
SELECT pg_drop_replication_slot('unused_slot');

# 3. VACUUM FULL largest tables (locks table!)
VACUUM FULL large_table;

# 4. Remove old backups / logs
find /backups -name "*.dump" -mtime +7 -delete
```

### 周期性维护任务：
- **检查查询日志（耗时最长的前 10 条查询）** |
- **检查索引使用情况，删除未使用的索引，添加缺失的索引。**
- **验证备份是否成功并测试恢复功能。**
- **检查表空间使用情况，必要时执行 VACUUM 操作。**
- **监控连接数变化趋势。**
- **检查磁盘空间使用情况。**
- **检查数据复制延迟。**
- **更新表统计信息：执行 `ANALYZE` 命令。**

---

## 第十一阶段 — 数据库性能对比

| 特性 | PostgreSQL | MySQL（InnoDB） | SQLite |
|---------|-----------|----------------|--------|
| 适用场景 | 复杂查询、扩展功能 | Web 应用、读取密集型应用 | 嵌入式应用、开发环境、小型应用 |
| 最大数据量 | 实际上无限制 | 实际上无限制 | 最大 281 TB（实际使用中约 1 TB） |
| JSON 支持 | 支持 JSONB 数据类型（可索引，性能优异） | 支持 JSON 数据类型（索引功能有限） | 需通过 JSON1 扩展支持 |
| 全文搜索 | 内置支持（使用 tsvector） | 内置支持（FULLTEXT） | 需通过 FTS5 扩展支持 |
| 公共表表达式（CTE） | 完全支持 | 自 PostgreSQL 8.0 开始支持 | 自 PostgreSQL 3.25 开始支持 |
| 分区功能 | 支持声明式分区及范围/列表/哈希分区 | 支持范围/列表/哈希分区 | 不支持分区功能 |
| 行级安全性 | 支持 | 不支持（需使用视图） | 不支持 |
| 数据复制 | 支持流式复制和逻辑复制 | 支持二进制日志复制 | 不支持数据复制 |
| 连接模型 | 每个连接独立处理 | 每个连接使用单独的线程 | 每个连接在同一个进程内处理 |

---

## 综合评估评分（0-100 分）

| 评估维度 | 权重 | 0（较差） | 5（良好） | 10（优秀） |
|---------|--------|---------|---------|-----------------|
| 数据库模式设计 | 20% | 无规范化设计，无约束条件 | 符合第三范式（3NF），有外键约束，数据类型正确 | 采用最佳规范形式，所有约束条件都得到满足，定期进行性能审计 |
| 索引设计 | 15% | 仅为主键列创建索引 | 为外键列和常用查询创建索引 | 创建全面的索引，避免使用未使用的索引 |
| 查询性能 | 20% | 使用 SELECT * 或 N+1 类型的查询，未使用 EXPLAIN 分析 | 仅选择特定列进行查询，合理使用 JOIN 操作，优化查询计划 | 使用关键列进行分页，支持窗口函数，查询计划经过优化 |
| 迁移安全性 | 10% | 使用原始 DDL 语句进行迁移，无回滚机制 | 使用版本控制机制，数据迁移分批进行 | 无停机时间，支持批量数据导入 |
| 数据安全 | 15% | 普通用户具有访问权限，无数据审计机制 | 限制用户权限，使用参数化查询 | 支持细粒度访问控制（RLS），数据加密，定期进行安全审计 |
| 监控机制 | 10% | 无监控机制 | 仅提供基本连接/磁盘使用情况警报 | 提供全面的性能监控仪表盘，能够进行查询性能分析，具备主动优化能力 |
| 备份与恢复 | 10% | 无备份机制 | 每天自动备份数据 | 支持 PITR 技术，备份数据可快速恢复，数据备份复制到异地 |

**评分说明：**  
- 分数低于 40 分表示存在严重风险；  
- 40-60 分表示需要改进；  
- 60-80 分表示表现良好；  
- 80-90 分表示专业水平；  
- 90 分以上表示处于专家级别。  

---

## 常用命令说明：
- “为 [特定领域] 设计数据库模式” → 执行第一阶段的完整设计流程。  
- “优化这个 SQL 查询：[查询语句]” → 使用 EXPLAIN 分析工具进行优化并重写查询语句。  
- “为 [查询模式] 添加索引” → 选择合适的索引类型并创建索引。  
- “执行数据迁移操作：[具体变更内容]” → 安全地执行数据迁移并制定回滚计划。  
- “审计这个数据库” → 对数据库进行全面性能评估。  
- “配置数据库监控” → 设置第五阶段的监控指标。  
- “检查这个数据库模式” → 检查数据库的命名规范、数据类型、约束条件等。  
- “提供关于 PostgreSQL/MySQL/SQLite 的帮助” → 提供针对特定平台的指导。  
- “解决查询性能问题” → 使用 `pg_stat_statements` 分析工具诊断问题并优化查询。  
- “制定备份策略” → 根据第六阶段的指导原则制定备份策略。  
- “使这个表支持多租户访问” | 配置数据库以支持多租户访问模式。  
- “将这个表转换为支持分区结构” | 采用第九阶段的优化技巧进行数据分区。