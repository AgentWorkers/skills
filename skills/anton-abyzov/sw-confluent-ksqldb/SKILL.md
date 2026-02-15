---
name: confluent-ksqldb
description: ksqlDB流处理专家：支持在Kafka主题上执行类似SQL的查询操作，涵盖流处理与表格处理的概念、数据连接（JOIN）、聚合操作、窗口函数的应用、物化视图（Materialized Views）以及实时数据转换功能。适用于ksqlDB、ksql、流处理工具、Kafka SQL、实时分析场景，支持流式JOIN、表格式JOIN以及物化视图的创建与使用。
---

# Confluent ksqlDB 技能

具备 ksqlDB 的深入知识——Confluent 提供的基于事件流式的数据库，允许您使用类似 SQL 的查询语句在 Kafka 主题上构建实时应用程序。

## 我掌握的知识

### 核心概念

**流（Streams）**（无界、仅支持追加操作）：
- 表示不可变的事件序列
- 每一行都是一个新事件
- 无法更新或删除
- 例如：点击事件、传感器读数、交易记录

**表（Tables）**（可变、保存最新状态）：
- 表示当前状态
- 更新会覆盖之前的值（基于键进行覆盖）
- 实际上是对主题数据进行压缩存储
- 例如：用户资料、产品库存、账户余额

**主要区别**：
```sql
-- STREAM: Every event is independent
INSERT INTO clicks_stream (user_id, page, timestamp)
VALUES (1, 'homepage', CURRENT_TIMESTAMP());
-- Creates NEW row

-- TABLE: Latest value wins (by key)
INSERT INTO users_table (user_id, name, email)
VALUES (1, 'John', 'john@example.com');
-- UPDATES existing row with user_id=1
```

### 查询类型

**1. 流式查询（Streaming Queries）**（连续的、实时的）：
```sql
-- Filter events in real-time
SELECT user_id, page, timestamp
FROM clicks_stream
WHERE page = 'checkout'
EMIT CHANGES;

-- Transform on the fly
SELECT
  user_id,
  UPPER(page) AS page_upper,
  TIMESTAMPTOSTRING(timestamp, 'yyyy-MM-dd') AS date
FROM clicks_stream
EMIT CHANGES;
```

**2. 物化视图（Materialized Views）**（预计算的表格）：
```sql
-- Aggregate clicks per user (updates continuously)
CREATE TABLE user_click_counts AS
SELECT
  user_id,
  COUNT(*) AS click_count
FROM clicks_stream
GROUP BY user_id
EMIT CHANGES;

-- Query the table (instant results!)
SELECT * FROM user_click_counts WHERE user_id = 123;
```

**3. 拉取查询（Pull Queries）**（点对点的读取）：
```sql
-- Query current state (like traditional SQL)
SELECT * FROM users_table WHERE user_id = 123;

-- No EMIT CHANGES = pull query (returns once)
```

## 何时使用此技能

当您需要以下帮助时，请使用我：
- ksqlDB 语法（例如：“如何创建 ksqlDB 流？”）
- 流与表的概念（例如：“何时使用流而不是表？”）
- 连接操作（例如：“如何将流与表连接？”）
- 聚合操作（例如：“统计每个用户的事件数量”）
- 窗口操作（例如：“使用滚动窗口进行聚合”）
- 实时转换（例如：“过滤和丰富事件数据”）
- 物化视图（例如：“创建预计算的聚合结果”）

## 常见模式

### 模式 1：过滤事件

**用例**：提前过滤掉不相关的事件

```sql
-- Create filtered stream
CREATE STREAM important_clicks AS
SELECT *
FROM clicks_stream
WHERE page IN ('checkout', 'payment', 'confirmation')
EMIT CHANGES;
```

### 模式 2：丰富事件数据（流-表连接）

**用例**：为点击事件添加用户详细信息

```sql
-- Users table (current state)
CREATE TABLE users (
  user_id BIGINT PRIMARY KEY,
  name VARCHAR,
  email VARCHAR
) WITH (
  kafka_topic='users',
  value_format='AVRO'
);

-- Enrich clicks with user data
CREATE STREAM enriched_clicks AS
SELECT
  c.user_id,
  c.page,
  c.timestamp,
  u.name,
  u.email
FROM clicks_stream c
LEFT JOIN users u ON c.user_id = u.user_id
EMIT CHANGES;
```

### 模式 3：实时聚合

**用例**：统计每 5 分钟内每个用户的事件数量

```sql
CREATE TABLE user_clicks_per_5min AS
SELECT
  user_id,
  WINDOWSTART AS window_start,
  WINDOWEND AS window_end,
  COUNT(*) AS click_count
FROM clicks_stream
WINDOW TUMBLING (SIZE 5 MINUTES)
GROUP BY user_id
EMIT CHANGES;

-- Query current window
SELECT * FROM user_clicks_per_5min
WHERE user_id = 123
AND window_start >= NOW() - INTERVAL 5 MINUTES;
```

### 模式 4：检测异常

**用例**：当用户在 1 分钟内点击超过 100 次时发出警报

```sql
CREATE STREAM high_click_alerts AS
SELECT
  user_id,
  COUNT(*) AS click_count
FROM clicks_stream
WINDOW TUMBLING (SIZE 1 MINUTE)
GROUP BY user_id
HAVING COUNT(*) > 100
EMIT CHANGES;
```

### 模式 5：变更数据捕获（Change Data Capture, CDC）

**用例**：跟踪用户表中的数据变更

```sql
-- Create table from CDC topic (Debezium)
CREATE TABLE users_cdc (
  user_id BIGINT PRIMARY KEY,
  name VARCHAR,
  email VARCHAR,
  op VARCHAR  -- INSERT, UPDATE, DELETE
) WITH (
  kafka_topic='mysql.users.cdc',
  value_format='AVRO'
);

-- Stream of changes only
CREATE STREAM user_changes AS
SELECT * FROM users_cdc
WHERE op IN ('UPDATE', 'DELETE')
EMIT CHANGES;
```

## 连接类型

### 1. 流-流连接（Stream-Stream Join）

**用例**：在时间窗口内关联相关事件

**窗口类型**：
- `WITHIN 10 MINUTES`：事件必须在 10 分钟内发生
- `GRACE PERIOD 5 MINUTES`：允许延迟到达的事件在 5 分钟内被处理

### 2. 流-表连接（Stream-Table Join）

**用例**：用当前状态丰富事件数据

```sql
-- Add product details to order events
CREATE STREAM enriched_orders AS
SELECT
  o.order_id,
  o.product_id,
  p.product_name,
  p.price
FROM orders_stream o
LEFT JOIN products_table p ON o.product_id = p.product_id
EMIT CHANGES;
```

### 3. 表-表连接（Table-Table Join）

**用例**：合并两个表的数据（显示最新状态）

```sql
-- Join users with their current cart
CREATE TABLE user_with_cart AS
SELECT
  u.user_id,
  u.name,
  c.cart_total
FROM users u
LEFT JOIN shopping_carts c ON u.user_id = c.user_id
EMIT CHANGES;
```

## 窗口类型

### 滚动窗口（Tumbling Window，非重叠）

**用例**：按固定时间周期进行聚合

```sql
-- Count events every 5 minutes
SELECT
  user_id,
  COUNT(*) AS event_count
FROM events
WINDOW TUMBLING (SIZE 5 MINUTES)
GROUP BY user_id;

-- Windows: [0:00-0:05), [0:05-0:10), [0:10-0:15)
```

### 跳动窗口（Hopping Window，重叠）

**用例**：计算随时间变化的移动平均值

```sql
-- Count events in 10-minute windows, advancing every 5 minutes
SELECT
  user_id,
  COUNT(*) AS event_count
FROM events
WINDOW HOPPING (SIZE 10 MINUTES, ADVANCE BY 5 MINUTES)
GROUP BY user_id;

-- Windows: [0:00-0:10), [0:05-0:15), [0:10-0:20)
```

### 会话窗口（Session Window，基于事件）

**用例**：按用户会话对事件进行分组

```sql
-- Session ends after 30 minutes of inactivity
SELECT
  user_id,
  COUNT(*) AS session_events
FROM events
WINDOW SESSION (30 MINUTES)
GROUP BY user_id;
```

## 最佳实践

### 1. 使用合适的数据类型

✅ **应该**：
```sql
CREATE STREAM orders (
  order_id BIGINT,
  user_id BIGINT,
  total DECIMAL(10, 2),  -- Precise currency
  timestamp TIMESTAMP
);
```

❌ **不应该**：
```sql
-- WRONG: Using DOUBLE for currency (precision loss!)
total DOUBLE
```

### 2. 始终指定键

✅ **应该**：
```sql
CREATE TABLE users (
  user_id BIGINT PRIMARY KEY,  -- Explicit key
  name VARCHAR
) WITH (kafka_topic='users');
```

❌ **不应该**：
```sql
-- WRONG: No key specified (can't join!)
CREATE TABLE users (
  user_id BIGINT,
  name VARCHAR
);
```

### 3. 使用窗口进行聚合

✅ **应该**：
```sql
-- Windowed aggregation (bounded memory)
SELECT COUNT(*) FROM events
WINDOW TUMBLING (SIZE 1 HOUR)
GROUP BY user_id;
```

❌ **不应该**：
```sql
-- WRONG: Non-windowed aggregation (unbounded memory!)
SELECT COUNT(*) FROM events GROUP BY user_id;
```

### 4. 设置保留策略

```sql
-- Limit table size (keep last 7 days)
CREATE TABLE user_stats (
  user_id BIGINT PRIMARY KEY,
  click_count BIGINT
) WITH (
  kafka_topic='user_stats',
  retention_ms=604800000  -- 7 days
);
```

## 性能优化

### 1. 分区对齐

**确保连接的流/表具有相同的分区键**：

```sql
-- GOOD: Both keyed by user_id (co-partitioned)
CREATE STREAM clicks (user_id BIGINT KEY, ...)
CREATE TABLE users (user_id BIGINT PRIMARY KEY, ...)

-- Join works efficiently (no repartitioning)
SELECT * FROM clicks c
JOIN users u ON c.user_id = u.user_id;
```

### 2. 使用物化视图

**预计算耗时的查询**：

```sql
-- BAD: Compute on every request
SELECT COUNT(*) FROM orders WHERE user_id = 123;

-- GOOD: Materialized table (instant lookup)
CREATE TABLE user_order_counts AS
SELECT user_id, COUNT(*) AS order_count
FROM orders GROUP BY user_id;

-- Query is now instant
SELECT order_count FROM user_order_counts WHERE user_id = 123;
```

### 3. 提前过滤数据

```sql
-- GOOD: Filter before join
CREATE STREAM important_events AS
SELECT * FROM events WHERE event_type = 'purchase';

SELECT * FROM important_events e
JOIN users u ON e.user_id = u.user_id;

-- BAD: Join first, filter later (processes all events!)
SELECT * FROM events e
JOIN users u ON e.user_id = u.user_id
WHERE e.event_type = 'purchase';
```

## 常见问题及解决方案

### 问题 1：查询超时

**错误**：查询超时

**根本原因**：在大型数据流上执行了非窗口化的聚合操作

**解决方案**：添加时间窗口：
```sql
-- WRONG
SELECT COUNT(*) FROM events GROUP BY user_id;

-- RIGHT
SELECT COUNT(*) FROM events
WINDOW TUMBLING (SIZE 1 HOUR)
GROUP BY user_id;
```

### 问题 2：分区不匹配

**错误**：无法连接流（分区键不同）

**解决方案**：重新划分数据流：
```sql
-- Repartition stream by user_id
CREATE STREAM clicks_by_user AS
SELECT * FROM clicks PARTITION BY user_id;

-- Now join works
SELECT * FROM clicks_by_user c
JOIN users u ON c.user_id = u.user_id;
```

### 问题 3：延迟到达的事件

**解决方案**：使用延迟处理期：
```sql
SELECT COUNT(*) FROM events
WINDOW TUMBLING (SIZE 5 MINUTES, GRACE PERIOD 1 MINUTE)
GROUP BY user_id;
-- Accepts events up to 1 minute late
```

## 参考资料

- ksqlDB 文档：https://docs.ksqldb.io/
- ksqlDB 教程：https://kafka-tutorials.confluent.io/
- 窗口操作指南：https://docs.ksqldb.io/en/latest/concepts/time-and-windows-in-ksqldb-queries/
- 连接类型说明：https://docs.ksqldb.io/en/latest/developer-guide/joins/

---

**当您需要流处理、实时分析或对 Kafka 数据进行类似 SQL 的查询时，请使用我！**