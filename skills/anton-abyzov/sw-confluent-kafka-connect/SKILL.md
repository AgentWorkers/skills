---
name: confluent-kafka-connect
description: Kafka Connect集成专家。精通源连接器（source connectors）和目标连接器（sink connectors）的配置与使用，包括JDBC、Elasticsearch、S3、Debezium CDC等数据源/目标系统的集成方案。负责开发与配置相关连接器，并提供关于数据管道（data pipelines）设计模式的指导。支持Kafka Connect的核心功能，包括源连接器（source connector）、目标连接器（sink connector）、JDBC连接器（JDBC connector）、Debezium、SMT（Single Message Transforms）等组件的部署与优化。
---

# Confluent Kafka Connect 技能

具备使用 Kafka Connect 构建数据管道的专家级知识，包括源连接器（Source Connectors）和目标连接器（Sink Connectors）。

## 我所掌握的知识

### 连接器类型

**源连接器**（外部系统 → Kafka）：
- JDBC Source：数据库 → Kafka
- Debezium：CDC（MySQL、PostgreSQL、MongoDB）→ Kafka
- S3 Source：AWS S3 文件 → Kafka
- File Source：本地文件 → Kafka

**目标连接器**（Kafka → 外部系统）：
- JDBC Sink：Kafka → 数据库
- Elasticsearch Sink：Kafka → Elasticsearch
- S3 Sink：Kafka → AWS S3
- HDFS Sink：Kafka → Hadoop HDFS

**单条消息转换（Single Message Transforms, SMTs）**：
- 字段操作：插入（Insert）、屏蔽（Mask）、替换（Replace）、时间戳转换（TimestampConverter）
- 路由（Routing）：正则表达式路由器（RegexRouter）、时间戳路由器（TimestampRouter）
- 过滤（Filtering）：过滤器（Filter）、谓词（Predicates）

## 何时使用此技能

在需要以下帮助时请启用我：
- 连接器配置（“配置 JDBC 连接器”）
- CDC 模式（“Debezium MySQL CDC”）
- 数据管道（“将数据库变更流式传输到 Kafka”）
- 单条消息转换（“屏蔽敏感字段”）
- 连接器故障排除（“连接器任务失败”）

## 常见模式

### 模式 1：JDBC Source（数据库 → Kafka）

**用例**：将数据库表变更流式传输到 Kafka

**配置**：
```json
{
  "name": "jdbc-source-users",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "tasks.max": "1",
    "connection.url": "jdbc:postgresql://localhost:5432/mydb",
    "connection.user": "postgres",
    "connection.password": "password",
    "mode": "incrementing",
    "incrementing.column.name": "id",
    "topic.prefix": "postgres-",
    "table.whitelist": "users,orders",
    "poll.interval.ms": "5000"
  }
}
```

**模式选项**：
- `incrementing`：通过自增 ID 追踪
- `timestamp`：通过时间戳列追踪
- `timestamp+incrementing`：两者结合（最可靠）

### 模式 2：Debezium CDC（MySQL → Kafka）

**用例**：捕获所有数据库变更（INSERT/UPDATE/DELETE）

**配置**：
```json
{
  "name": "debezium-mysql-cdc",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "tasks.max": "1",
    "database.hostname": "localhost",
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "password",
    "database.server.id": "1",
    "database.server.name": "mysql",
    "database.include.list": "mydb",
    "table.include.list": "mydb.users,mydb.orders",
    "schema.history.internal.kafka.bootstrap.servers": "localhost:9092",
    "schema.history.internal.kafka.topic": "schema-changes.mydb"
  }
}
```

**输出格式**（Debezium Envelope）：
```json
{
  "before": null,
  "after": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "source": {
    "version": "1.9.0",
    "connector": "mysql",
    "name": "mysql",
    "ts_ms": 1620000000000,
    "snapshot": "false",
    "db": "mydb",
    "table": "users",
    "server_id": 1,
    "gtid": null,
    "file": "mysql-bin.000001",
    "pos": 12345,
    "row": 0,
    "thread": null,
    "query": null
  },
  "op": "c",  // c=CREATE, u=UPDATE, d=DELETE, r=READ
  "ts_ms": 1620000000000
}
```

### 模式 3：JDBC Sink（Kafka → 数据库）

**用例**：将 Kafka 事件写入 PostgreSQL

**配置**：
```json
{
  "name": "jdbc-sink-enriched-orders",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "tasks.max": "3",
    "topics": "enriched-orders",
    "connection.url": "jdbc:postgresql://localhost:5432/analytics",
    "connection.user": "postgres",
    "connection.password": "password",
    "auto.create": "true",
    "auto.evolve": "true",
    "insert.mode": "upsert",
    "pk.mode": "record_value",
    "pk.fields": "order_id",
    "table.name.format": "orders_${topic}"
  }
}
```

**插入模式**：
- `insert`：仅追加（重复数据时失败）
- `update`：仅更新（需要主键）
- `upsert`：插入或更新（推荐）

### 模式 4：S3 Sink（Kafka → AWS S3）

**用例**：将 Kafka 主题数据归档到 S3

**配置**：
```json
{
  "name": "s3-sink-events",
  "config": {
    "connector.class": "io.confluent.connect.s3.S3SinkConnector",
    "tasks.max": "3",
    "topics": "user-events,order-events",
    "s3.region": "us-east-1",
    "s3.bucket.name": "my-kafka-archive",
    "s3.part.size": "5242880",
    "flush.size": "1000",
    "rotate.interval.ms": "60000",
    "rotate.schedule.interval.ms": "3600000",
    "timezone": "UTC",
    "format.class": "io.confluent.connect.s3.format.json.JsonFormat",
    "partitioner.class": "io.confluent.connect.storage.partitioner.TimeBasedPartitioner",
    "path.format": "'year'=YYYY/'month'=MM/'day'=dd/'hour'=HH",
    "locale": "US",
    "timestamp.extractor": "Record"
  }
}
```

**分区策略**（S3 文件夹结构）：
```
s3://my-kafka-archive/
  topics/user-events/year=2025/month=01/day=15/hour=10/
    user-events+0+0000000000.json
    user-events+0+0000001000.json
  topics/order-events/year=2025/month=01/day=15/hour=10/
    order-events+0+0000000000.json
```

### 模式 5：Elasticsearch Sink（Kafka → Elasticsearch）

**用例**：为搜索索引 Kafka 事件

**配置**：
```json
{
  "name": "elasticsearch-sink-logs",
  "config": {
    "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
    "tasks.max": "3",
    "topics": "application-logs",
    "connection.url": "http://localhost:9200",
    "connection.username": "elastic",
    "connection.password": "password",
    "key.ignore": "true",
    "schema.ignore": "true",
    "type.name": "_doc",
    "index.write.wait_for_active_shards": "1"
  }
}
```

## 单条消息转换（SMTs）

### 转换 1：屏蔽敏感字段

**用例**：在 Kafka 主题中隐藏电子邮件/电话号码

**配置**：
```json
{
  "transforms": "maskEmail",
  "transforms.maskEmail.type": "org.apache.kafka.connect.transforms.MaskField$Value",
  "transforms.maskEmail.fields": "email,phone"
}
```

**转换前**：
```json
{"id": 1, "name": "John", "email": "john@example.com", "phone": "555-1234"}
```

**转换后**：
```json
{"id": 1, "name": "John", "email": null, "phone": null}
```

### 转换 2：添加时间戳

**用例**：为所有消息添加处理时间戳

**配置**：
```json
{
  "transforms": "insertTimestamp",
  "transforms.insertTimestamp.type": "org.apache.kafka.connect.transforms.InsertField$Value",
  "transforms.insertTimestamp.timestamp.field": "processed_at"
}
```

### 转换 3：根据字段值路由

**用例**：将高价值订单路由到单独的主题

**配置**：
```json
{
  "transforms": "routeByValue",
  "transforms.routeByValue.type": "org.apache.kafka.connect.transforms.RegexRouter",
  "transforms.routeByValue.regex": "(.*)",
  "transforms.routeByValue.replacement": "$1-high-value",
  "transforms.routeByValue.predicate": "isHighValue",
  "predicates": "isHighValue",
  "predicates.isHighValue.type": "org.apache.kafka.connect.transforms.predicates.TopicNameMatches",
  "predicates.isHighValue.pattern": "orders"
}
```

### 转换 4：展平嵌套 JSON

**用例**：为 JDBC 目标连接器展平嵌套结构

**配置**：
```json
{
  "transforms": "flatten",
  "transforms.flatten.type": "org.apache.kafka.connect.transforms.Flatten$Value",
  "transforms.flatten.delimiter": "_"
}
```

**转换前**：
```json
{
  "user": {
    "id": 1,
    "profile": {
      "name": "John",
      "email": "john@example.com"
    }
  }
}
```

**转换后**：
```json
{
  "user_id": 1,
  "user_profile_name": "John",
  "user_profile_email": "john@example.com"
}
```

## 最佳实践

### 1. 使用幂等连接器（Idempotent Connectors）

✅ **应该这样做**：
```json
// JDBC Sink with upsert mode
{
  "insert.mode": "upsert",
  "pk.mode": "record_value",
  "pk.fields": "id"
}
```

❌ **不应该这样做**：
```json
// WRONG: insert mode (duplicates on restart!)
{
  "insert.mode": "insert"
}
```

### 2. 监控连接器状态

```bash
# Check connector status
curl http://localhost:8083/connectors/jdbc-source-users/status

# Check task status
curl http://localhost:8083/connectors/jdbc-source-users/tasks/0/status
```

### 3. 使用模式注册表（Schema Registry）

✅ **应该这样做**：
```json
{
  "value.converter": "io.confluent.connect.avro.AvroConverter",
  "value.converter.schema.registry.url": "http://localhost:8081"
}
```

### 4. 配置错误处理

```json
{
  "errors.tolerance": "all",
  "errors.log.enable": "true",
  "errors.log.include.messages": "true",
  "errors.deadletterqueue.topic.name": "dlq-jdbc-sink",
  "errors.deadletterqueue.context.headers.enable": "true"
}
```

## 连接器管理

### 部署连接器

```bash
# Create connector via REST API
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d @jdbc-source.json

# Update connector
curl -X PUT http://localhost:8083/connectors/jdbc-source-users/config \
  -H "Content-Type: application/json" \
  -d @jdbc-source.json
```

### 监控连接器

```bash
# List all connectors
curl http://localhost:8083/connectors

# Get connector info
curl http://localhost:8083/connectors/jdbc-source-users

# Get connector status
curl http://localhost:8083/connectors/jdbc-source-users/status

# Get connector tasks
curl http://localhost:8083/connectors/jdbc-source-users/tasks
```

### 暂停/恢复连接器

```bash
# Pause connector
curl -X PUT http://localhost:8083/connectors/jdbc-source-users/pause

# Resume connector
curl -X PUT http://localhost:8083/connectors/jdbc-source-users/resume

# Restart connector
curl -X POST http://localhost:8083/connectors/jdbc-source-users/restart

# Restart task
curl -X POST http://localhost:8083/connectors/jdbc-source-users/tasks/0/restart
```

## 常见问题及解决方案

### 问题 1：连接器任务失败

**症状**：任务状态为 FAILED

**解决方案**：
1. 查看连接器日志：`docker logs connect-worker`
2. 验证配置：`curl http://localhost:8083/connector-plugins/<class>/config/validate`
3. 重启任务：`curl -X POST .../tasks/0/restart`

### 问题 2：模式不兼容

**错误**：检测到不兼容的模式

**解决方案**：启用自动模式演化：
```json
{
  "auto.create": "true",
  "auto.evolve": "true"
}
```

### 问题 3：JDBC 连接池耗尽

**错误**：无法获取 JDBC 连接

**解决方案**：增加连接池大小：
```json
{
  "connection.attempts": "3",
  "connection.backoff.ms": "10000"
}
```

## 参考资料

- Kafka Connect 文档：https://kafka.apache.org/documentation/#connect
- Confluent Hub：https://www.confluent.io/hub/
- Debezium 文档：https://debezium.io/documentation/
- 转换参考：https://kafka.apache.org/documentation/#connect_transforms

---

**当您需要 Kafka Connect、连接器、CDC 或数据管道方面的专业知识时，请随时调用我！**