---
name: timeplus-sql-guide
description: 编写并执行 Timeplus 流式 SQL 语句以实现实时数据分析。当用户需要创建数据流、运行流式查询、构建物化视图、导入数据、将数据发送到数据接收端、编写用户自定义函数（UDFs），或使用随机数据流进行数据模拟时，可以使用此技能。Timeplus 通过兼容 ClickHouse 的 HTTP 接口（端口 8123）执行 SQL 语句，该接口依赖于环境变量 TIMEPLUS_HOST、TIMEPLUS_USER 和 TIMEPLUS_PASSWORD。它支持完整的 Timeplus SQL 语法，包括窗口函数、JOIN 操作、公共表表达式（CTEs）、用户自定义函数（UDFs）、数据类型、聚合操作以及所有的数据定义语言（DDL）和数据操作语言（DML）语句。
license: Apache-2.0
compatibility: >
  Requires curl. Set environment variables: TIMEPLUS_HOST (hostname or IP of
  Timeplus server), TIMEPLUS_USER (username, default: 'default'),
  TIMEPLUS_PASSWORD (password). Port 8123 must be accessible. For streaming
  ingest, port 3218 must also be accessible.
metadata:
  author: timeplus-io
  version: "1.0"
  docs: https://docs.timeplus.com
  github: https://github.com/timeplus-io/proton
---
# Timeplus 流式 SQL 使用指南

您是 **Timeplus** 的专家——这是一个基于流式 SQL 引擎（Proton）构建的高性能实时流式分析平台。您需要编写正确且高效的 Timeplus SQL 语句，并通过兼容 ClickHouse 的 HTTP API 来执行这些语句。

## 快速参考

| 任务 | 参考文档 |
|------|-----------|
| 获取数据 | `references/INGESTION.md` |
| 转换数据 | `references/TRANSFORMATIONS.md` |
| 发送数据 | `references/SINKS.md` |
| 完整的 SQL 语法、数据类型和函数 | `references/SQL_REFERENCE.md` |
| 随机数据流（模拟数据） | `references/RANDOM_STREAMS.md` |
| Python 和 JavaScript 用户定义函数（UDFs） | `references/UDFS.md` |
| Python 表函数 | `references/Python_TABLE_FUNCTION.md` |

---

## 执行 SQL 语句

### 环境设置

始终使用以下环境变量——切勿将凭据硬编码：

```
- TIMEPLUS_HOST       # hostname or IP
- TIMEPLUS_USER       # username
- TIMEPLUS_PASSWORD   # password (can be empty)
```

### 通过 curl（端口 8123）执行 SQL 语句

端口 8123 是兼容 ClickHouse 的 HTTP 接口。使用它来执行所有 DDL 操作和历史查询（如 CREATE、DROP、INSERT、SELECT 等）。在执行查询时必须使用 `-u` 选项指定用户名和密码。

**注意**：如果 curl 没有返回任何内容，并不表示出现错误，而是表示查询没有返回任何记录。您可以通过检查 HTTP 状态码（200 OK 表示成功，4xx/5xx 表示失败）来确认查询的结果。

```bash
# Standard pattern — pipe SQL into curl
echo "YOUR SQL HERE" | curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

**健康检查：**
```bash
curl "http://${TIMEPLUS_HOST}:8123/"
# Returns: Ok.
```

**DDL 示例——创建数据流：**
```bash
echo "CREATE STREAM IF NOT EXISTS sensor_data (
  device_id string,
  temperature float32,
  ts datetime64(3, 'UTC') DEFAULT now64(3, 'UTC')
) SETTINGS logstore_retention_ms=86400000" | \
curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

**带有 JSON 输出的历史查询：**
```bash
echo "SELECT * FROM table(sensor_data) LIMIT 10" | \
curl "http://${TIMEPLUS_HOST}:8123/?default_format=JSONEachRow" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

**插入数据：**
```bash
echo "INSERT INTO sensor_data (device_id, temperature) VALUES ('dev-1', 23.5), ('dev-2', 18.2)" | \
curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

### 通过 REST API（端口 3218）进行流式数据导入**

用于将事件批次推送到数据流中：

```bash
curl -s -X POST "http://${TIMEPLUS_HOST}:3218/proton/v1/ingest/streams/sensor_data" \
  -H "Content-Type: application/json" \
  -d '{
    "columns": ["device_id", "temperature"],
    "data": [
      ["dev-1", 23.5],
      ["dev-2", 18.2],
      ["dev-3", 31.0]
    ]
  }'
```

### 输出格式

在 URL 后添加 `?default_format=<格式>` 参数来指定输出格式：

| 格式 | 适用场景 |
|--------|----------|
| `TabSeparated` | 默认格式，适合人类阅读 |
| `JSONEachRow` | 每行一个 JSON 对象 |
| `JSONCompact` | 压缩的 JSON 数组 |
| `CSV` | 逗号分隔的格式 |
| `Vertical` | 每行一个列，便于查看 |

---

## 核心概念

### 流式查询与历史查询的区别

```sql
-- STREAMING: Continuous, never ends. Default behavior.
SELECT device_id, temperature FROM sensor_data;

-- HISTORICAL: Bounded, returns immediately. Use table().
SELECT device_id, temperature FROM table(sensor_data) LIMIT 100;

-- HISTORICAL + FUTURE: All past events + all future events
SELECT * FROM sensor_data WHERE _tp_time >= earliest_timestamp();
```

### `_tp_time` 列

每个数据流都有一个内置的 `_tp_time` 列，其数据类型为 `datetime64(3, 'UTC')`，用于存储事件时间。默认情况下，该列会使用数据导入的时间。您可以在创建数据流时通过 `SETTINGS event_time_column='your_column'` 来设置自定义的事件时间列。

### 数据流模式

| 模式 | 创建方式 | 行为 |
|------|-------------|----------|
| `append` | `CREATE STREAM`（默认模式） | 不可修改的日志记录，仅添加新行 |
| `versioned_kv` | `+SETTINGS mode='versioned_kv'` | 按主键存储最新值 |
| `changelog_kv` | `+SETTINGS mode='changelog_kv'` | 支持插入/更新/删除操作 |
| `mutable` | `CREATE MUTABLE STREAM` | 支持行级别的更新/删除操作（企业级功能） |

---

## 常见使用模式

### 模式 1：创建数据流 → 插入数据 → 执行查询
```bash
# 1. Create stream
echo "CREATE STREAM IF NOT EXISTS orders (
  order_id string,
  product string,
  amount float32,
  region string
)" | curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-

# 2. Insert data
echo "INSERT INTO orders VALUES ('o-1','Widget',19.99,'US'), ('o-2','Gadget',49.99,'EU')" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-

# 3. Query historical data
echo "SELECT region, sum(amount) FROM table(orders) GROUP BY region" | \
  curl "http://${TIMEPLUS_HOST}:8123/?default_format=JSONEachRow" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

### 模式 2：窗口聚合（流式处理）
```bash
echo "SELECT window_start, region, sum(amount) AS revenue
FROM tumble(orders, 1m)
GROUP BY window_start, region
EMIT AFTER WATERMARK AND DELAY 5s" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

### 模式 3：物化视图管道
```bash
echo "CREATE MATERIALIZED VIEW IF NOT EXISTS mv_revenue_by_region
INTO revenue_by_region AS
SELECT window_start, region, sum(amount) AS total
FROM tumble(orders, 5m)
GROUP BY window_start, region" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

### 模式 4：用于测试的随机数据流
```bash
echo "CREATE RANDOM STREAM IF NOT EXISTS mock_sensors (
  device_id string DEFAULT 'device-' || to_string(rand() % 10),
  temperature float32 DEFAULT 20 + (rand() % 30),
  status string DEFAULT ['ok','warn','error'][rand() % 3 + 1]
) SETTINGS eps=5" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

---

## 错误处理

常见错误及解决方法：

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| `Connection refused` | 主机或端口错误 | 确保 `TIMEPLUS_HOST` 设置正确，并且端口 8123 是开放的 |
| `Authentication failed` | 凭据错误 | 检查 `TIMEPLUS_USER` 和 `TIMEPLUS_PASSWORD` 是否正确 |
| `Stream already exists` | 数据流已存在 | 使用 `CREATE STREAM IF NOT EXISTS` 来避免重复创建 |
| `Unknown column` | 列名错误或数据流配置错误 | 使用 `DESCRIBE stream_name` 来查看数据流的结构 |
| `Streaming query timeout` | 在端口 8123 上执行流式查询 | 对于历史查询，请使用 `table()` 包装查询语句 |
| `Type mismatch` | 数据类型不匹配 | 使用显式类型转换：`cast(val, 'float32')` |

**查看数据流信息：**
```bash
echo "DESCRIBE sensor_data" | curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

**列出所有数据流：**
```bash
echo "SHOW STREAMS" | curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

**解释 SQL 语句：**
```bash
echo "EXPLAIN SELECT * FROM tumble(sensor_data, 1m) GROUP BY window_start" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

---

## 何时查阅参考文档

当用户需要更深入的信息时，请查阅相应的参考文档：

- 创建或修改数据流、外部数据源 → `references/INGESTION.md`
- 窗口函数、JOIN 操作、公共表表达式（CTEs）、物化视图、聚合操作 → `references/TRANSFORMATIONS.md`
- 数据输出方式、外部数据表、Kafka 输出、Webhook 配置 → `references/SINKS.md`
- 数据类型、完整函数目录、查询设置、所有 DDL 语句 → `references/SQL_REFERENCE.md`
- 数据模拟、随机数据生成 → `references/RANDOM_STREAMS.md`
- 编写 Python 用户定义函数（UDFs）、JavaScript 用户定义函数（UDFs）、远程用户定义函数（remote UDFs）、SQL Lambda 表达式 → `references/UDFS.md`
- Python 表函数 → `references/Python_TABLE_FUNCTION.md`