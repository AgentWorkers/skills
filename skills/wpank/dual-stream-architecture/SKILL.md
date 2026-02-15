---
name: dual-stream-architecture
model: reasoning
description: 双流事件发布方案：结合 Kafka 的持久性特性与 Redis 的 Pub/Sub 功能，实现实时数据传输。适用于构建需要同时保证数据可靠传输和低延迟更新的事件驱动系统。该方案支持双流传输、事件发布、Kafka 数据存储、实时事件处理以及基于 Pub/Sub 的流式架构。
---

# 双流架构

对于同时需要数据持久性（Kafka）和实时性（Redis Pub/Sub）的系统，该架构能够将事件同时发布到这两个目标。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install dual-stream-architecture
```


---

## 使用场景

- 需要数据持久性和实时性的事件驱动系统
- 需要推送实时更新的 WebSocket/SSE 后端
- 需要在事件发生时立即显示在仪表板上的系统
- Kafka 消费者存在延迟，但用户期望立即收到更新的系统

---

## 核心模式

```go
type DualPublisher struct {
    kafka  *kafka.Writer
    redis  *redis.Client
    logger *slog.Logger
}

func (p *DualPublisher) Publish(ctx context.Context, event Event) error {
    // 1. Kafka: Critical path - must succeed
    payload, _ := json.Marshal(event)
    err := p.kafka.WriteMessages(ctx, kafka.Message{
        Key:   []byte(event.SourceID),
        Value: payload,
    })
    if err != nil {
        return fmt.Errorf("kafka publish failed: %w", err)
    }

    // 2. Redis: Best-effort - don't fail the operation
    p.publishToRedis(ctx, event)

    return nil
}

func (p *DualPublisher) publishToRedis(ctx context.Context, event Event) {
    // Lightweight payload (full event in Kafka)
    notification := map[string]interface{}{
        "id":        event.ID,
        "type":      event.Type,
        "source_id": event.SourceID,
    }

    payload, _ := json.Marshal(notification)
    channel := fmt.Sprintf("events:%s:%s", event.SourceType, event.SourceID)

    // Fire and forget - log errors but don't propagate
    if err := p.redis.Publish(ctx, channel, payload).Err(); err != nil {
        p.logger.Warn("redis publish failed", "error", err)
    }
}
```

---

## 架构设计

```
┌──────────────┐     ┌─────────────────┐     ┌──────────────┐
│   Ingester   │────▶│  DualPublisher  │────▶│    Kafka     │──▶ Event Processor
│              │     │                 │     │  (durable)   │
└──────────────┘     │                 │     └──────────────┘
                     │                 │     ┌──────────────┐
                     │                 │────▶│ Redis PubSub │──▶ WebSocket Gateway
                     │                 │     │ (real-time)  │
                     └─────────────────┘     └──────────────┘
```

---

## 通道命名规范

```
events:{source_type}:{source_id}

Examples:
- events:user:octocat      - Events for user octocat
- events:repo:owner/repo   - Events for a repository
- events:org:microsoft     - Events for an organization
```

---

## 批量发布

为了提高吞吐量：

```go
func (p *DualPublisher) PublishBatch(ctx context.Context, events []Event) error {
    // 1. Batch to Kafka
    messages := make([]kafka.Message, len(events))
    for i, event := range events {
        payload, _ := json.Marshal(event)
        messages[i] = kafka.Message{
            Key:   []byte(event.SourceID),
            Value: payload,
        }
    }

    if err := p.kafka.WriteMessages(ctx, messages...); err != nil {
        return fmt.Errorf("kafka batch failed: %w", err)
    }

    // 2. Redis: Pipeline for efficiency
    pipe := p.redis.Pipeline()
    for _, event := range events {
        channel := fmt.Sprintf("events:%s:%s", event.SourceType, event.SourceID)
        notification, _ := json.Marshal(map[string]interface{}{
            "id":   event.ID,
            "type": event.Type,
        })
        pipe.Publish(ctx, channel, notification)
    }
    
    if _, err := pipe.Exec(ctx); err != nil {
        p.logger.Warn("redis batch failed", "error", err)
    }

    return nil
}
```

---

## 决策树

| 需求 | 流类型 | 原因 |
|-------------|--------|-----|
| 确保事件不会丢失 | 仅使用 Kafka | 需要确认接收并复制数据 |
| 用户需要立即看到事件 | 仅使用 Redis | 数据在亚毫秒级别内送达 |
| 同时满足数据持久性和实时性需求 | 使用双流架构 |
| 数据量非常大（>10,000条/秒） | 使用 Kafka 进行批量处理，Redis 用于存储 | Redis 可能会成为性能瓶颈 |
| 每个通道有大量订阅者 | 使用 Redis 结合本地分发机制 | 避免对 Redis 造成过大压力 |

---

## 相关技能

- **元技能：** [ai/skills/meta/realtime-dashboard/](../../meta/realtime-dashboard/) — 完整的实时仪表板指南
- [websocket-hub-patterns](../websocket-hub-patterns/) — WebSocket 网关相关模式
- [backend/service-layer-architecture](../../backend/service-layer-architecture/) — 服务层架构设计

---

## 绝对不要做的事情

- **绝不要因为 Redis 的错误而停止服务** — Redis 采用尽力而为的传输方式，记录错误并继续运行。
- **绝不要将所有数据发送到 Redis** — 仅发送事件 ID，客户端通过 API 获取完整数据。
- **绝不要为每个事件创建单独的 Redis 通道** — 应使用基于数据源的通道管理机制。
- **绝不要对“不重要”的事件跳过 Kafka** — 所有事件都应发送到 Kafka 以备后续重放。
- **绝不要使用 Redis Pub/Sub 作为数据持久化手段** — Redis 的消息传输方式是一次性的（即发送后不再保留）。

---

## 边缘情况处理

| 情况 | 解决方案 |
|------|----------|
| Redis 停机 | 记录警告信息，继续仅使用 Kafka 发送事件 |
| 客户端在数据传输过程中连接中断 | 通过 API 查询最近的事件，然后重新订阅 |
| 通道数量非常多 | 使用通配符模式或聚合通道来管理数据 |
| Kafka 出现压力（Backpressure） | 在内存中缓存数据并设置超时机制，如果内存满则停止发送 |
| 需要事件重放 | 从 Kafka 的指定偏移量处重新读取数据，而不是从 Redis 中读取 |

---