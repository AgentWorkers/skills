---
name: n8n-kafka-workflows
description: n8n工作流自动化与Kafka集成专家教程。涵盖Kafka触发节点、生产者节点、事件驱动的工作流、错误处理、重试机制，以及无代码/低代码事件处理模式。适用于n8n Kafka、Kafka触发器、Kafka生产者、n8n工作流、事件驱动自动化、无代码Kafka解决方案及各种工作流模式。
---

# n8n Kafka 工作流技能

具备将 Apache Kafka 与 n8n 工作流自动化平台集成方面的专业知识，支持无代码/低代码事件驱动的处理方式。

## 我所掌握的知识

### n8n Kafka 节点

**Kafka 触发节点**（事件消费者）：
- 在新的 Kafka 消息到达时触发工作流
- 支持消费者组
- 支持自动提交或手动偏移量管理
- 可订阅多个主题
- 支持消息批量处理

**Kafka 生产节点**（事件生产者）：
- 将消息发送到 Kafka 主题
- 支持基于键的分区
- 支持消息头部信息
- 支持压缩格式（gzip、snappy、lz4）
- 支持批量发送

**配置**：
```json
{
  "credentials": {
    "kafkaApi": {
      "brokers": "localhost:9092",
      "clientId": "n8n-workflow",
      "ssl": false,
      "sasl": {
        "mechanism": "plain",
        "username": "{{$env.KAFKA_USER}}",
        "password": "{{$env.KAFKA_PASSWORD}}"
      }
    }
  }
}
```

## 何时使用此技能

当您需要以下帮助时，请启用此技能：
- n8n Kafka 的配置（“在 n8n 中配置 Kafka 触发器”）
- 工作流模式（“使用 n8n 进行事件驱动的自动化处理”）
- 错误处理（“重试失败的 Kafka 消息”）
- 集成模式（“使用 HTTP API 丰富 Kafka 消息”）
- 生产者配置（“从 n8n 向 Kafka 发送消息”）
- 消费者组（“并行处理 Kafka 消息”）

## 常见的工作流模式

### 模式 1：事件驱动处理

**用例**：使用 HTTP API 丰富 Kafka 消息

```
[Kafka Trigger] → [HTTP Request] → [Transform] → [Database]
     ↓
  orders topic
     ↓
  Get customer data
     ↓
  Merge order + customer
     ↓
  Save to PostgreSQL
```

**n8n 工作流**：
1. **Kafka 触发器**：
   - 主题：`orders`
   - 消费者组：`order-processor`
   - 偏移量：`latest`

2. **HTTP 请求**（数据丰富）：
   - URL：`https://api.example.com/customers/${json.customerId}`
   - 方法：GET
   - 头部信息：`Authorization: Bearer/${env.API_TOKEN}`

3. **设置节点**（数据转换）：
   ```javascript
   return {
     orderId: $json.order.id,
     customerId: $json.order.customerId,
     customerName: $json.customer.name,
     customerEmail: $json.customer.email,
     total: $json.order.total,
     timestamp: new Date().toISOString()
   };
   ```

4. **PostgreSQL**（数据存储）：
   - 操作：INSERT
   - 表：`enriched_orders`
   - 列：从设置节点映射而来

### 模式 2：扇出（发布到多个主题）

**用例**：单个事件触发多个下游工作流

```
[Kafka Trigger] → [Switch] → [Kafka Producer] (topic: high-value-orders)
     ↓                ↓
  orders topic        └─→ [Kafka Producer] (topic: all-orders)
                           └─→ [Kafka Producer] (topic: analytics)
```

**n8n 工作流**：
1. **Kafka 触发器**：消费 `orders` 主题
2. **Switch 节点**：根据 `total` 值进行路由
   - 路由 1：`total > 1000` → `high-value-orders` 主题
   - 路由 2：始终 → `all-orders` 主题
   - 路由 3：始终 → `analytics` 主题
3. **Kafka 生产者**（3 个实例）：分别向相应主题发送消息

### 模式 3：带死信队列（DLQ）的重试

**用例**：重试失败的消息，失败后发送到 DLQ

```
[Kafka Trigger] → [Try/Catch] → [Success] → [Kafka Producer] (topic: processed)
     ↓                ↓
  input topic     [Catch Error]
                       ↓
                  [Increment Retry Count]
                       ↓
                  [If Retry < 3]
                       ↓ Yes
                  [Kafka Producer] (topic: input-retry)
                       ↓ No
                  [Kafka Producer] (topic: dlq)
```

**n8n 工作流**：
1. **Kafka 触发器**：`input` 主题
2. **Try 节点**：发送 HTTP 请求（可能失败）
3. **Catch 节点**（错误处理）：
   - 从消息头部获取重试次数
   - 增加重试次数
   - 如果重试次数小于 3 次：发送到 `input-retry` 主题
   - 否则：发送到 `dlq` 主题

### 模式 4：批量处理与聚合

**用例**：聚合 100 条消息，然后批量发送到 API

```
[Kafka Trigger] → [Aggregate] → [HTTP Request] → [Kafka Producer]
     ↓               ↓
  events topic   Buffer 100 msgs
                     ↓
                Send batch to API
                     ↓
                Publish results
```

**n8n 工作流**：
1. **Kafka 触发器**：启用批量处理（每批 100 条消息）
2. **Aggregate 节点**：将消息合并成数组
3. **HTTP 请求**：发送批量数据
4. **Kafka 生产者**：发送处理结果

### 模式 5：将数据库变更（CDC）流式传输到 Kafka

**用例**：将数据库的变更实时传输到 Kafka

```
[Cron Trigger] → [PostgreSQL] → [Compare] → [Kafka Producer]
     ↓               ↓              ↓
  Every 1 min    Get new rows   Find diffs
                                    ↓
                              Publish changes
```

**n8n 工作流**：
1. **Cron 任务**：每分钟执行一次
2. **PostgreSQL**：查询新增行（WHERE updated_at > last_run）
3. **Function 节点**：检测变更（INSERT/UPDATE/DELETE 操作）
4. **Kafka 生产者**：发送 CDC 事件

## 最佳实践

### 1. 使用消费者组进行并行处理

✅ **应该这样做**：
```
Workflow Instance 1:
  Consumer Group: order-processor
  Partition: 0, 1, 2

Workflow Instance 2:
  Consumer Group: order-processor
  Partition: 3, 4, 5
```

❌ **不应该这样做**：
```
// WRONG: No consumer group (all instances get all messages!)
Consumer Group: (empty)
```

### 2. 使用 Try/Catch 处理错误

✅ **应该这样做**：
```
[Kafka Trigger]
  ↓
[Try] → [HTTP Request] → [Success Handler]
  ↓
[Catch] → [Error Handler] → [Kafka DLQ]
```

❌ **不应该这样做**：
```
// WRONG: No error handling (workflow crashes on failure!)
[Kafka Trigger] → [HTTP Request] → [Database]
```

### 3. 使用环境变量存储凭据

✅ **应该这样做**：
```
Kafka Brokers: {{$env.KAFKA_BROKERS}}
SASL Username: {{$env.KAFKA_USER}}
SASL Password: {{$env.KAFKA_PASSWORD}}
```

❌ **不应该这样做**：
```
// WRONG: Hardcoded credentials in workflow!
Kafka Brokers: "localhost:9092"
SASL Username: "admin"
SASL Password: "admin-secret"
```

### 4. 设置明确的分区键

✅ **应该这样做**：
```
Kafka Producer:
  Topic: orders
  Key: {{$json.customerId}}  // Partition by customer
  Message: {{$json}}
```

❌ **不应该这样做**：
```
// WRONG: No key (random partitioning!)
Kafka Producer:
  Topic: orders
  Message: {{$json}}
```

### 5. 监控消费者延迟

**配置 Prometheus 指标导出**：
```
[Cron Trigger] → [Kafka Admin] → [Get Consumer Lag] → [Prometheus]
     ↓               ↓                   ↓
  Every 30s    List consumer groups   Calculate lag
                                           ↓
                                   Push to Pushgateway
```

## 错误处理策略

### 策略 1：指数级退避重试

```javascript
// Function Node (Calculate Backoff)
const retryCount = $json.headers?.['retry-count'] || 0;
const backoffMs = Math.min(1000 * Math.pow(2, retryCount), 60000); // Max 60 seconds

return {
  retryCount: retryCount + 1,
  backoffMs,
  nextRetryAt: new Date(Date.now() + backoffMs).toISOString()
};
```

**工作流**：
1. 尝试处理消息
2. 处理失败后：计算退避时间
3. 等待（使用 Wait 节点）
4. 重试（发送到 retry 主题）
5. 如果达到最大重试次数：发送到 DLQ

### 策略 2：断路器

```javascript
// Function Node (Check Failure Rate)
const failures = $json.metrics.failures || 0;
const total = $json.metrics.total || 1;
const failureRate = failures / total;

if (failureRate > 0.5) {
  // Circuit open (too many failures)
  return { circuitState: 'OPEN', skipProcessing: true };
}

return { circuitState: 'CLOSED', skipProcessing: false };
```

**工作流**：
1. 记录成功/失败的次数
2. 计算失败率
3. 如果失败率超过 50%：停止处理
4. 等待 30 秒
5. 尝试发送单个请求（部分恢复处理）
6. 如果成功：恢复处理

### 策略 3：幂等处理

```javascript
// Function Node (Deduplication)
const messageId = $json.headers?.['message-id'];
const cache = $('Redis').get(messageId);

if (cache) {
  // Already processed, skip
  return { skip: true, reason: 'duplicate' };
}

// Process and cache
await $('Redis').set(messageId, 'processed', { ttl: 3600 });
return { skip: false };
```

**工作流**：
1. 提取消息 ID
2. 检查 Redis 缓存
3. 如果消息已存在：跳过处理
4. 处理消息
5. 将消息 ID 存储到缓存中（缓存有效期为 1 小时）

## 性能优化

### 1. 批量处理

**在 Kafka 触发器中启用批量处理**：
```
Kafka Trigger:
  Batch Size: 100
  Batch Timeout: 5000ms  // Max wait 5 seconds
```

**处理批量数据**：
```javascript
// Function Node (Batch Transform)
const events = $input.all();
const transformed = events.map(event => ({
  id: event.json.id,
  timestamp: event.json.timestamp,
  processed: true
}));

return transformed;
```

### 2. 分批处理以实现并行处理

```
[Kafka Trigger] → [Split in Batches] → [HTTP Request] → [Aggregate]
     ↓                  ↓                     ↓
  1000 events      100 at a time       Parallel API calls
                                            ↓
                                      Combine results
```

### 3. 使用压缩技术

**Kafka 生产者**：
```
Compression: lz4  // Or gzip, snappy
Batch Size: 1000  // Larger batches = better compression
```

## 集成模式

### 模式 1：Kafka + HTTP API 丰富数据

```
[Kafka Trigger] → [HTTP Request] → [Transform] → [Kafka Producer]
     ↓                 ↓                ↓
  Raw events      Enrich from API   Combine data
                                         ↓
                                  Publish enriched
```

### 模式 2：Kafka + 数据库同步

```
[Kafka Trigger] → [PostgreSQL Upsert] → [Kafka Producer]
     ↓                   ↓                    ↓
  CDC events      Update database    Publish success/failure
```

### 模式 3：Kafka + 电子邮件通知

```
[Kafka Trigger] → [If Critical] → [Send Email] → [Kafka Producer]
     ↓                ↓                ↓
  Alerts        severity=critical  Notify admin
                                        ↓
                                   Publish alert sent
```

### 模式 4：Kafka + Slack 警报

```
[Kafka Trigger] → [Transform] → [Slack] → [Kafka Producer]
     ↓               ↓            ↓
  Errors        Format message  Send to #alerts
                                     ↓
                                Publish notification
```

## n8n 工作流的测试

### 手动测试

1. **使用样本数据测试**：
   - 右键点击节点 → “添加样本数据”
   - 执行工作流
   - 检查输出结果

2. **测试 Kafka 生产者**：
   ```bash
   # Consume test topic
   kcat -C -b localhost:9092 -t test-output -o beginning
   ```

3. **测试 Kafka 触发器**：
   ```bash
   # Produce test message
   echo '{"test": "data"}' | kcat -P -b localhost:9092 -t test-input
   ```

### 自动化测试

**使用 n8n CLI**：
```bash
# Execute workflow with input
n8n execute workflow --file workflow.json --input data.json

# Export workflow
n8n export:workflow --id=123 --output=workflow.json
```

## 常见问题及解决方案

### 问题 1：消费者延迟累积

**症状**：处理速度慢于消息到达速度

**解决方案**：
1. 增加消费者组规模（实现并行处理）
2. 启用批量处理（一次处理 100 条消息）
3. 优化 HTTP 请求（使用连接池）
4. 使用分批处理技术实现并行处理

### 问题 2：消息重复

**原因**：至少一次交付机制，没有去重功能

**解决方案**：添加幂等性检查：
```javascript
// Check if message already processed
const messageId = $json.headers?.['message-id'];
const exists = await $('Redis').exists(messageId);

if (exists) {
  return { skip: true };
}
```

### 问题 3：工作流执行超时

**原因**：HTTP 请求耗时过长

**解决方案**：使用异步处理模式：
```
[Kafka Trigger] → [Webhook] → [Wait for Webhook] → [Process Response]
     ↓               ↓
  Trigger job    Async callback
                     ↓
                 Continue workflow
```

## 参考资料

- n8n Kafka 触发器：https://docs.n8n.io/integrations/builtin/trigger-nodes/n8n-nodes-base.kafkatrigger/
- n8n Kafka 生产者：https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.kafka/
- n8n 最佳实践：https://docs.n8n.io/hosting/scaling/best-practices/
- 工作流示例：https://n8n.io/workflows

---

**当您需要 n8n Kafka 集成、工作流自动化或事件驱动的无代码解决方案时，请随时调用我！**