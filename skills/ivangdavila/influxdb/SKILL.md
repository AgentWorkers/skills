---
name: InfluxDB
description: 通过合理的模式设计和数据保留策略来存储和查询时间序列数据。
metadata: {"clawdbot":{"emoji":"📈","requires":{"anyBins":["influx","curl"]},"os":["linux","darwin","win32"]}}
---

## 版本差异

- InfluxDB 2.x 使用 Flux 查询语言，而 1.x 使用 InfluxQL；两者的语法完全不同。
- InfluxDB 2.x 支持“bucket”（数据桶）、“organization”（组织结构）和“token”（访问令牌）等概念；InfluxDB 1.x 则使用“database”（数据库）、“retention policy”（数据保留策略）和“user”（用户）等概念。
- 在复制查询语句之前，请务必确认所使用的版本，避免使用不兼容的命令。

## 标签（Tags）与字段（Fields）的区别（重要）

- 标签会被索引，而字段不会；因此可以基于标签进行过滤，也可以基于字段进行聚合操作。
- 标签的值必须是字符串类型；虽然数字也可以作为标签使用，但会浪费索引空间。
- 字段可以存储数字、字符串和布尔值；建议将指标数据存储在字段中。
- 选择错误的标签类型会严重影响查询性能，并且数据写入后无法更改。

## 高基数标签（High Cardinality Tags）的问题

- 如果标签的基数过高（即标签值的唯一组合数量过多），会导致查询性能严重下降。例如，将用户 ID 作为标签使用会引发性能灾难。
- 可以使用 `SHOW CARDINALITY`（InfluxDB 1.x）或 `influx bucket inspect`（InfluxDB 2.x）来检查标签的基数。
- 经验法则：每个指标类型对应的系列数量应少于 10 万个；超过这个数量可能会导致性能问题。

## 数据格式（Line Protocol）

- 数据格式为：`measurement,tag1=v1,tag2=v2,field1=1,field2="str,timestamp`。
- 标签中的等号（=`）两侧不能有空格，空格用于分隔标签和字段。
- 字符串字段需要使用引号，而标签值则不需要；例如：`field="text"` 和 `tag=text` 是不同的。
- 时间戳默认以纳秒为单位；需要明确指定精度以避免错误。

## 时间戳（Timestamps）

- 时间戳的默认精度为纳秒；如果发送数据时未指定精度，默认时间戳为 2000 年的数据。
- 写入数据时可以指定精度：`precision=s` 表示秒级精度，`precision=ms` 表示毫秒级精度。
- 如果时间戳缺失，系统会使用服务器时间；对于实时数据采集来说，这通常是可以接受的。
- 时间戳采用 UTC 格式；客户端的时间区设置不影响数据存储。

## 数据保留与降采样（Retention and Downsampling）

- 可以设置数据保留策略或数据桶的持续时间；超过保留期限的数据会自动删除。
- 原始数据会以 10 秒为间隔存储 7 天，之后会降采样为 1 分钟的间隔存储 30 天，再降采样为 1 小时的间隔存储 1 年。
- InfluxDB 2.x 使用专门的降采样任务来实现数据压缩；InfluxDB 1.x 则通过连续查询（Continuous Queries）来实现降采样功能。
- 如果不进行降采样，数据存储量会无限增长，查询速度也会变慢。

## Flux 查询模式（Flux Query Patterns, InfluxDB 2.x）

- 查询语句始终需要以 `from(bucket:)` 开头，然后是 `|> range(start:)`；范围指定是必需的。
- 使用 `|> filter(fn: (r) => r._measurement == "cpu")` 进行过滤。
- 使用 `|> aggregateWindow(every: 1h, fn: mean)` 进行基于时间的聚合操作。
- 可以使用 `|>` 管道运算符来链接多个转换操作；操作顺序对查询性能有影响。

## InfluxQL 查询模式（InfluxQL Patterns, InfluxDB 1.x）

- 示例查询语句：`SELECT mean("value") FROM "measurement" WHERE time > now() - 1h GROUP BY time(5m)`。
- 标识符需要使用双引号，字符串字面量需要使用单引号。
- 使用 `GROUP BY time()` 进行基于时间的聚合操作；大多数仪表盘都需要这个步骤。
- 可以使用 `FILL(none)` 来跳过空的时间间隔，或者使用 `FILL(previous)` 来填充缺失的数据。

## 数据模式设计（Schema Design）

- 每个指标类型对应一个表名（例如：cpu、memory、requests）。
- 使用标签来标识用于过滤或聚合的维度（如 host、region、service）。
- 使用字段来存储聚合后的数据（如 usage_percent、count、latency_ms）。
- 避免在指标名称中编码数据；例如：`cpu.host1` 是错误的写法，正确的写法是 `cpu` + `host=host1`。

## 数据写入性能（Write Performance）

- 批量写入数据会带来额外的 HTTP 开销；在生产环境中推荐使用 Telegraf 来处理数据采集，它支持批量处理、缓冲和重试机制。
- 如果可能的话，建议将数据写入本地主机；高吞吐量情况下网络延迟会影响写入速度。
- 客户端库支持异步写入，避免每次写入操作都阻塞程序。

## 查询性能（Query Performance）

- 查询时必须指定时间范围；不指定时间范围的查询会扫描所有数据。
- 应先根据标签进行过滤，再根据字段进行查询；标签查询会利用索引加速查询速度，而字段查询则需要扫描全部数据。
- 可以使用 `LIMIT` 或 `|> limit()` 来限制返回的结果数量；仪表盘通常不需要处理大量数据点。
- 使用 `GROUP BY` 或 `aggregateWindow` 来减少返回的数据量，提高查询效率。

## 常见错误

- “partial write: field type conflict”：同一个字段使用了不同的数据类型；需要在数据源处修复这个问题。
- “max-values-per-tag limit exceeded”：标签的基数过高；需要重新设计数据模式。
- “database not found”：InfluxDB 2.x 使用的是数据桶（buckets），而不是数据库（databases）；请检查 API 版本。
- 查询超时：可以缩小时间范围或使用更复杂的聚合操作来提高查询效率。