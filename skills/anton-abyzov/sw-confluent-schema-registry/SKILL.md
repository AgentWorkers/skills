---
name: confluent-schema-registry
description: Avro、Protobuf 和 JSON Schema 的 Schema Registry 专家，专注于这些格式的 Schema 管理工作。涵盖 Schema 进化策略、兼容性模式、验证方法，以及在 Confluent Cloud 和自托管 Schema Registry 中管理 Schema 的最佳实践。支持 Schema Registry 的激活功能，以及 Avro、Protobuf 和 JSON Schema 的相关操作（包括 Schema 进化、兼容性模式设置和 Schema 验证等）。
---

# Confluent Schema Registry 技能

具备丰富的 Confluent Schema Registry 知识，能够有效管理 Kafka 生态系统中的 Avro、Protobuf 和 JSON Schema。

## 我所掌握的内容

### Schema 格式

**Avro**（最受欢迎）：
- 二进制序列化格式
- 支持 Schema 的演化
- 比 JSON 更小的消息大小
- 通过头部中的 Schema ID 自描述
- 适用于：高吞吐量应用、数据仓库

**Protobuf**（Google Protocol Buffers）：
- 二进制序列化
- 使用 `.proto` 文件实现强类型
- 语言无关（Java、Python、Go、C++ 等）
- 高效的编码方式
- 适用于：多语言环境、gRPC 集成

**JSON Schema**：
- 人类可读的文本格式
- 易于调试
- 被广泛支持
- 消息大小较大
- 适用于：开发、调试、REST API

### 兼容性模式

| 模式 | 生产者可以 | 消费者可以 | 使用场景 |
|------|-------------|-------------|----------|
| **BACKWARD** | 删除字段、添加可选字段 | 使用新 Schema 读取旧数据 | 最常见，对消费者安全 |
| **FORWARD** | 添加字段、删除可选字段 | 使用旧 Schema 读取新数据 | 对生产者安全 |
| **FULL** | 仅允许添加/删除可选字段 | 双向兼容 | 生产者和消费者可以独立升级 |
| **NONE** | 任何更改 | 必须协调升级 | 仅限开发环境，不适合生产环境 |
| **BACKWARD_TRANSITIVE** | 在所有版本间保持 backward 兼容性 | 可以读取任何旧数据 | 最严格的 backward 兼容性 |
| **FORWARD_TRANSITIVE** | 在所有版本间保持 forward 兼容性 | 可以读取任何新数据 | 最严格的 forward 兼容性 |
| **FULL_TRANSITIVE** | 在所有版本间保持双向兼容性 | 最严格的兼容性 |

**默认值**：`BACKWARD`（推荐用于生产环境）

### Schema 演化策略

**添加字段**：
```avro
// V1
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "long"},
    {"name": "name", "type": "string"}
  ]
}

// V2 - BACKWARD compatible (added optional field with default)
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "long"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": ["null", "string"], "default": null}
  ]
}
```

**删除字段**（保持 backward 兼容性）：
```avro
// V1
{"name": "address", "type": "string"}

// V2 - Remove field (old consumers will ignore it)
// Field removed from schema
```

**更改字段类型**（会破坏兼容性！）：
```avro
// ❌ BREAKING - Cannot change string to int
{"name": "age", "type": "string"} → {"name": "age", "type": "int"}

// ✅ SAFE - Use union types
{"name": "age", "type": ["string", "int"], "default": "unknown"}
```

## 何时使用此技能

当您需要以下帮助时，请激活我：
- Schema 演化策略（“如何演化我的 Avro Schema？”）
- 兼容性模式选择（“生产环境应使用哪种兼容性模式？”）
- Schema 验证（“验证我的 Avro Schema”）
- 最佳实践（“Schema Registry 的最佳实践”）
- Schema 注册（“将 Avro Schema 注册到 Schema Registry”）
- 调试 Schema 问题（“Schema 兼容性错误”）
- 格式比较（“Avro 与 Protobuf 与 JSON Schema 的比较”）

## 最佳实践

### 1. 始终使用兼容的演化策略

✅ **应该**：
- 添加带有默认值的可选字段
- 删除可选字段
- 使用联合类型（union types）以提高灵活性
- 首先在测试环境中测试 Schema 的变化

❌ **不应该**：
- 更改字段类型
- 删除必填字段
- 重命名字段（同时添加新字段并弃用旧字段）
- 在生产环境中使用 `NONE` 兼容性模式

### 2. Schema 命名规范

**分层命名空间**：
```
com.company.domain.EntityName
com.acme.ecommerce.Order
com.acme.ecommerce.OrderLineItem
```

**Kafka 主题命名**：
- `<topic-name>-value` - 用于记录值
- `<topic-name>-key` - 用于记录键
- 例如：`orders-value`、`orders-key`

### 3. Schema Registry 配置

**生产者（使用 Avro）**：
```javascript
const { Kafka } = require('kafkajs');
const { SchemaRegistry } = require('@kafkajs/confluent-schema-registry');

const registry = new SchemaRegistry({
  host: 'https://schema-registry:8081',
  auth: {
    username: 'SR_API_KEY',
    password: 'SR_API_SECRET'
  }
});

// Register schema
const schema = `
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "long"},
    {"name": "name", "type": "string"}
  ]
}
`;

const { id } = await registry.register({
  type: SchemaType.AVRO,
  schema
});

// Encode message with schema
const payload = await registry.encode(id, {
  id: 1,
  name: 'John Doe'
});

await producer.send({
  topic: 'users',
  messages: [{ value: payload }]
});
```

**消费者（使用 Avro）**：
```javascript
const consumer = kafka.consumer({ groupId: 'user-processor' });

await consumer.subscribe({ topic: 'users' });

await consumer.run({
  eachMessage: async ({ message }) => {
    // Decode message (schema ID is in header)
    const decodedMessage = await registry.decode(message.value);
    console.log(decodedMessage); // { id: 1, name: 'John Doe' }
  }
});
```

### 4. Schema 验证流程

**注册前**：
1. 验证 Schema 语法（Avro、JSON、.proto、JSON Schema）
2. 检查与现有版本的兼容性
3. 使用样本数据进行测试
4. 首先在开发/测试环境中注册
5. 验证通过后部署到生产环境

**CLI 验证**：
```bash
# Check compatibility (before registering)
curl -X POST http://localhost:8081/compatibility/subjects/users-value/versions/latest \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "{...}"}'

# Register schema
curl -X POST http://localhost:8081/subjects/users-value/versions \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "{...}"}'
```

## 常见问题及解决方案

### 问题 1：Schema 兼容性错误

**错误**：
```
Schema being registered is incompatible with an earlier schema
```

**根本原因**：违反了兼容性模式（例如，在 BACKWARD 模式下删除了必填字段）

**解决方案**：
1. 检查当前的兼容性模式：
   ```bash
   curl http://localhost:8081/config/users-value
   ```
2. 修复 Schema 以使其兼容，或更改模式（请谨慎操作！）
3. 在注册前进行验证：
   ```bash
   curl -X POST http://localhost:8081/compatibility/subjects/users-value/versions/latest \
     -d '{"schema": "{...}"}'
   ```

### 问题 2：找不到 Schema

**错误**：
```
Subject 'users-value' not found
```

**根本原因**：Schema 尚未注册，或主题命名错误

**解决方案**：
1. 列出所有主题：
   ```bash
   curl http://localhost:8081/subjects
   ```
2. 如果缺失则注册 Schema
3. 检查主题命名规范（`<topic>-key` 或 `<topic>-value`）

### 问题 3：消息反序列化失败

**错误**：
```
Unknown magic byte!
```

**根本原因**：消息未使用 Schema Registry 进行编码（缺少魔数字节和 Schema ID）

**解决方案**：
1. 确保生产者使用了 Schema Registry 编码器
2. 检查消息格式：[魔数字节（1）+ Schema ID（4）+ 数据负载]
3. 使用 `@kafkajs/confluent-schema-registry` 库

## Schema 演化决策树

```
Need to change schema?
├─ Adding new field?
│  ├─ Required field? → Add with default value (BACKWARD)
│  └─ Optional field? → Add with default null (BACKWARD)
│
├─ Removing field?
│  ├─ Required field? → ❌ BREAKING CHANGE (coordinate upgrade)
│  └─ Optional field? → ✅ BACKWARD compatible
│
├─ Changing field type?
│  ├─ Compatible types (e.g., int → long)? → Use union types
│  └─ Incompatible types? → ❌ BREAKING CHANGE (add new field, deprecate old)
│
└─ Renaming field?
   └─ ❌ BREAKING CHANGE → Add new field + mark old as deprecated
```

## Avro、Protobuf 与 JSON Schema 的比较

| 特性 | Avro | Protobuf | JSON Schema |
|---------|------|----------|-------------|
| **编码方式** | 二进制 | 二进制 | 文本（JSON） |
| **消息大小** | 较小（比 JSON 小 90%） | 较小（比 JSON 小 80%） | 较大（基准） |
| **人类可读性** | 不支持 | 不支持 | 支持 |
| **Schema 演化** | 非常出色 | 良好 | 一般 |
| **语言支持** | Java、Python、C++ | 支持 20 多种语言 | 支持多种语言 |
| **性能** | 非常快 | 非常快 | 较慢 |
| **调试难度** | 较难 | 较难 | 较容易 |
| **适用场景** | 数据仓库、ETL | 多语言环境、gRPC | REST API、开发 |

**建议**：
- **生产环境**：Avro（最佳平衡）
- **多语言团队**：Protobuf
- **开发/调试**：JSON Schema

## 参考资料

- Schema Registry REST API：https://docs.confluent.io/platform/current/schema-registry/develop/api.html
- Avro 规范：https://avro.apache.org/docs/current/spec.html
- Protobuf 文档：https://developers.google.com/protocol-buffers
- JSON Schema 规范：https://json-schema.org/

---

**当您需要 Schema 管理、演化策略或兼容性指导时，请调用我！**