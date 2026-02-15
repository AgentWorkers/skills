---
name: TimescaleDB
description: 使用Hypertables存储和查询时间序列数据，支持数据压缩以及连续聚合操作。
metadata: {"clawdbot":{"emoji":"⏱️","requires":{"anyBins":["psql"]},"os":["linux","darwin","win32"]}}
---

## Hypertables

- 将表格转换为Hypertable：`SELECT create_hypertable('metrics', 'time')`
- 必须包含时间列（推荐使用TIMESTAMPTZ格式）——该列用作数据分块的键。
- 在插入数据之前执行转换操作——转换大型表格会消耗较多资源。
- 转换后的数据无法轻易恢复，因此请在转换前规划好数据结构。

## 数据分块（Chunking）

- 默认每个数据分块包含7天的数据——可根据数据量进行调整。
- 对于数据量较大的情况，可以使用`SELECT set_chunk_time_interval('metrics', INTERVAL '1 day')`来设置分块间隔。
- 每个数据分块的大小应占内存空间的25%左右：过小会导致额外的开销，过大则会导致查询速度变慢。
- 可以使用`SELECT * FROM chunks_detailed_size('metrics')`来查看各数据分块的大小。

## 时间分桶（Time Bucketing）

- `time_bucket('1 hour', time)`用于对时间戳进行分组——类似于`date_trunc`函数，但支持自定义的时间间隔。
- 在`GROUP BY`语句中可以使用`time_bucket('5 minutes', time)`来进行数据聚合。
- `time_bucket`函数还用于指定数据分块的起始时间，例如`time_bucket('1 day', time, '2024-01-01'::timestamptz)`。
- 该函数适用于非标准的时间间隔（如15分钟、4小时等）。

## 持续聚合（Continuous Aggregation）

- 持续聚合是一种自动更新的数据视图，用于预先计算复杂的聚合结果。
- 可以使用`CREATE MATERIALIZED VIEW hourly_stats WITH (timescaledb.continuous) AS SELECT ...`来创建这样的视图。
- 通过`SELECT add_continuous_aggregate_policy('hourly_stats', ...)`来为该视图设置更新策略。
- 查询时直接使用这些聚合视图，速度会比查询原始Hypertable快很多。

## 实时聚合（Real-Time Aggregation）

- 实时聚合会自动包含最新的数据，避免读取过时的数据。
- 使用`WITH (timescaledb.continuous, timescaledb.materialized_only = false)`来实现实时聚合功能。
- 这种方式结合了历史数据和实时数据，对查询性能的影响很小。
- 如果只需要批量处理数据，可以关闭实时聚合功能。

## 数据压缩（Compression）

- 可以压缩旧的数据分块以节省存储空间（通常可节省90%以上）：`ALTER TABLE metrics SET (timescaledb.compress)`。
- 使用`SELECT add_compression_policy('metrics', INTERVAL '7 days')`来设置压缩策略。
- 压缩后的数据分块仅支持读操作，无法更新或删除单个记录。
- 如果需要修改数据，可以使用`SELECT decompress_chunk('chunk_name')`来解压数据分块。

## 数据保留策略（Retention）

- 可以自动删除旧数据：`SELECT add_retention_policy('metrics', INTERVAL '90 days')`。
- 删除整个数据分块可以提高效率（无需逐行删除数据）。
- 数据保留操作由调度器自动执行，数据会在指定时间间隔后仍保留一段时间。
- 可以将数据压缩和保留策略结合使用（例如：每7天压缩数据，90天后删除）。

## 索引（Indexing）

- Hypertable中的时间列会自动被添加索引——避免创建多余的索引。
- 可以在需要过滤数据的列上添加索引：`CREATE INDEX ON metrics (device_id, time DESC)`。
- 使用复合索引（包含时间列）可以优化数据分块的读取效率。
- 对于很少被查询的列，可以省略索引的创建——因为索引会降低写入性能。

## 插入性能（Insert Performance）

- 批量插入数据效率较高；单行插入操作速度较慢。
- 可以使用`COPY`或`multi-value INSERT`语句进行数据插入：`INSERT INTO metrics VALUES (...), (...), ...`。
- 使用`timescaledb-parallel-copy`工具进行并行数据复制，可以提高I/O性能。
- 虽然可以支持乱序插入，但顺序插入效率更高。

## 查询模式（Query Patterns）

- 在`WHERE`子句中始终指定时间范围——这样可以避免查询不必要的数据分块。
- 使用`WHERE time > now() - INTERVAL '1 day'`可以跳过旧的数据分块。
- 使用`ORDER BY time DESC`和`LIMIT`来获取最新的数据（例如“最新的N条记录”），这样可以提高查询速度。
- 避免在大型表格上使用`SELECT *`语句——只获取需要的列。

## 分布式Hypertables（Distributed Hypertables）

- 分布式Hypertables支持横向扩展，数据会在多个节点之间分散存储。
- 需要分别创建访问节点和数据节点；访问节点负责处理查询请求。
- 分布式Hypertables的维护成本稍高，但适用于处理大量数据（单个节点可处理每秒数百万条记录）。
- 对于大多数工作负载来说，单个节点就已经足够了。