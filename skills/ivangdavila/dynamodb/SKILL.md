---
name: DynamoDB
description: 设计 DynamoDB 表并编写高效的查询语句，同时避免常见的 NoSQL 搭配误区（即错误的使用方式或常见的问题）。
metadata: {"clawdbot":{"emoji":"⚡","requires":{"anyBins":["aws"]},"os":["linux","darwin","win32"]}}
---

## 关键设计要素

- **分区键（Partition Key）**：决定了数据的分布方式。高基数（high-cardinality）的分区键能够均匀地分散负载。
- **热点分区（Hot Partition）**：当某个分区键接收了所有请求时，应使用复合键（composite key）或添加随机后缀来避免这种情况。
- **排序键（Sort Key）**：允许在分区内部进行范围查询（range queries），设计时需考虑数据的访问模式。
- **键的不可更改性**：创建表后无法修改分区键，因此必须在创建表之前规划好所有的数据访问模式。

## 查询（Query）与扫描（Scan）的区别

- **查询（Query）**：使用分区键以及可选的排序键，通常效率更高。
- **扫描（Scan）**：会读取整个表，效率低且耗时，且不支持索引；除非确实需要，否则应避免使用扫描操作。
- 如果需要根据某个条件进行过滤，通常意味着当前的数据结构中缺少相应的GSI（Global Secondary Index），此时应添加索引以避免不必要的扫描。

## 全局二级索引（Global Secondary Indexes, GSI）

- **GSI**：使用不同的分区键或排序键，可以提供额外的数据访问方式。
- **GSI的数据一致性**：GSI的数据是一致性的，但写入操作会有一定的延迟。
- **GSI的容量消耗**：每个GSI都需要单独分配存储空间，并且需要单独付费。
- **稀疏索引（Sparse Index）**：只有包含特定属性的数据才会被存储在GSI中。

## 单表设计（Single-Table Design）

- 可以使用一个表来存储多种类型的实体数据，通过前缀来区分不同的实体类型，例如 `USER#123`、`ORDER#456`。
- **重载的排序键（Overloaded Sort Key）**：可以同时用于多种查询场景，例如 `METADATA`、`ORDER#2024-01-15`、`ITEM#abc`。
- **查询结果类型**：查询可能返回多种类型的数据，客户端可以通过 `begins_with` 等方法进行过滤。
- **注意**：这种设计并不总是最优选择，应根据实际的访问模式来决定数据结构。

## 分页（Pagination）

- 每次请求返回的结果大小上限为1MB，因此需要实现分页功能。
- 响应中的 `LastEvaluatedKey` 可用于获取更多数据，可以将其作为 `ExclusiveStartKey` 用于下一次请求。
- 在循环中不断请求直到 `LastEvaluatedKey` 不存在为止，这是一个常见的错误：不要以为一次请求就能获取所有数据。
- `Limit` 参数限制的是被评估的数据数量，而不是实际返回的数据数量，因此仍需要实现分页逻辑。

## 数据一致性（Consistency）

- 默认情况下，读取操作的数据最终是一致的，但可能会返回过时的数据。
- 如果需要强一致性（strong consistency），可以设置 `ConsistentRead` 选项，但代价是读取性能会降低一半。
- GSI的读取操作始终是一致的，但不支持强一致性。
- 对于需要原子性（atomicity）的操作，应使用 `TransactWriteItems`。

## 条件性写入（Conditional Writes）

- 使用 `ConditionExpression` 实现乐观锁（optimistic locking）；如果条件不满足，写入操作会失败。
- 为防止数据被覆盖，可以使用 `attribute_not_exists(pk)` 等条件进行验证。
- 在写入前需要检查数据版本，如果版本与预期不符，则需要重试。
- 如果写入操作失败，应使用新鲜的数据重试。

## 批量操作（Batch Operations）

- `BatchWriteItem` 操作不是原子的（non-atomic），部分操作可能成功，需要检查 `UnprocessedItems` 列表。
- 未处理的任务会按照指数级退避策略（exponential backoff）进行重试，这一机制内置于AWS SDK中。
- 每批最多只能写入25个数据项，总大小不超过16MB；如果数据量较大，需要分批处理。
- 批量操作中不允许进行条件性写入，应使用 `TransactWriteItems` 来保证操作的原子性。

## 事务（Transactions）

- `TransactWriteItems` 用于执行多个数据项的原子性写入操作，要么全部成功，要么全部失败。
- 每次事务最多只能写入100个数据项，总大小不超过4MB。
- `TransactGetItems` 用于执行多个数据项的读取操作，并提供数据的一致性保障（snapshot isolation）。
- 事务操作的成本是普通操作的2倍，仅在需要保证原子性时使用。

## 时间戳过期（TTL, Time-To-Live）

- 可以为时间戳属性设置TTL（Time-To-Live），DynamoDB会自动删除过期的数据。
- 删除操作是后台进行的，过期的数据可能会在一段时间后仍然存在于数据库中。
- TTL值以Unix时间戳秒为单位；如果毫秒级的时间值未设置正确，查询时会返回错误结果。
- 如果需要根据TTL条件进行过滤，可以使用 `attribute_exists(ttl) AND ttl > :now`。

## 容量管理（Capacity Management）

- **按需付费（On-Demand）**：根据每次请求的实际使用量付费，适合流量不可预测的情况。
- **预配置容量（Provisioned）**：可以预先设置RCU（Read Capacity Units）/WCU（Write Capacity Units）来控制吞吐量，成本更便宜，适用于流量可预测的场景。
- **自动扩展（Auto-Scaling）**：对于流量可预测的场景，可以预先配置容量，并设置最小/最大/目标值。
- 如果实际吞吐量超过预配置值，系统会进行限流（throttling），需要重新尝试。

## 其他限制（Other Limits）

- 单个数据项的最大大小为400KB；如果需要存储大型对象，应将其存储在S3中，并在DynamoDB中引用。
- 分区的吞吐量上限为3000 RCU/1000 WCU，这些资源会在各个分区之间均匀分配。
- 每次查询或扫描操作返回的数据大小上限为1MB，超过这个限制需要使用分页。
- 每个数据项的属性名称总长度不能超过64KB；避免使用过长的属性名称。