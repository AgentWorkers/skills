---
name: event-store
model: standard
description: 为基于事件驱动的系统设计和实现事件存储机制。在构建事件驱动架构、实现事件持久化、数据投影（projection）、快照生成（snapshotting）或CQRS（Command-Query-Response-Signaling）模式时，可以使用该机制。
---

# 事件存储（Event Store）

本指南介绍了为基于事件驱动的应用程序设计事件存储的方法，涵盖事件模式（event schemas）、数据投影（projections）、快照生成（snapshotting）以及CQRS（Command-Query-Responsibility-Shadowing）框架的集成。

## 适用场景

- 设计事件驱动架构（event-driven infrastructure）
- 在不同的事件存储技术之间进行选择
- 实现自定义事件存储系统
- 从事件流中生成数据投影（build projections from event streams）
- 为提升聚合查询性能添加快照功能
- 将CQRS与事件驱动模型集成

## 核心概念

### 事件存储架构（Event Store Architecture）

```
┌─────────────────────────────────────────────────────┐
│                    Event Store                       │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Stream 1   │  │   Stream 2   │  │   Stream 3   │ │
│  │ (Aggregate)  │  │ (Aggregate)  │  │ (Aggregate)  │ │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤ │
│  │ Event 1     │  │ Event 1     │  │ Event 1     │ │
│  │ Event 2     │  │ Event 2     │  │ Event 2     │ │
│  │ Event 3     │  │ ...         │  │ Event 3     │ │
│  │ ...         │  │             │  │ Event 4     │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────┤
│  Global Position: 1 → 2 → 3 → 4 → 5 → 6 → ...     │
└─────────────────────────────────────────────────────┘
```

### 事件存储要求（Event Store Requirements）

| 要求                        | 描述                                      |
| --------------------------- | -------------------------------------- |
| **仅支持追加操作**                | 事件是不可变的，仅允许追加新的数据           |
| **支持排序**                    | 每个事件流以及全局范围内都支持排序             |
| **支持版本控制**                | 支持乐观并发控制（optimistic concurrency control）     |
| **提供实时通知**                | 支持实时事件通知功能                         |
| **保证操作幂等性**                | 确保重复写入操作不会导致数据损坏                   |

### 技术比较（Technology Comparison）

| 技术名称                     | 适用场景                                      | 限制因素                                      |
| --------------------------- | -------------------------------------- | ------------------------------------------------------ |
| **EventStoreDB**                | 专为事件驱动架构设计                         | 仅适用于单一用途                           |
| **PostgreSQL**                | 基于PostgreSQL的解决方案                         | 需手动实现相关功能                         |
| **Kafka**                    | 高吞吐量事件流处理工具                         | 不适合针对单个事件流的查询操作                         |
| **DynamoDB**                | 无服务器架构，原生支持AWS                         | 查询性能有限                               |

## 事件模式设计（Event Schema Design）

事件是数据存储的“真实来源”。合理的事件模式设计有助于确保系统的长期可扩展性。

### 事件结构（Event Structure）

```json
{
  "event_id": "uuid",
  "stream_id": "Order-abc123",
  "event_type": "OrderPlaced",
  "version": 1,
  "schema_version": 1,
  "data": {
    "customer_id": "cust-1",
    "total_cents": 5000
  },
  "metadata": {
    "correlation_id": "req-xyz",
    "causation_id": "evt-prev",
    "user_id": "user-1",
    "timestamp": "2025-01-15T10:30:00Z"
  },
  "global_position": 42
}
```

### 模式演化规则（Schema Evolution Rules）

1. **自由添加字段**                | 新字段总是可以安全地添加                         |
2. **禁止删除或重命名字段**                | 如需修改结构，应创建新的事件类型                   |
3. **为事件类型添加版本号**                | 当模式发生重大变更时，为事件类型添加版本号                 |
4. **读取时进行类型转换**                | 在反序列化过程中将旧版本的数据转换为当前格式           |

## PostgreSQL事件存储模式（PostgreSQL Event Store Schema）

```sql
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stream_id VARCHAR(255) NOT NULL,
    stream_type VARCHAR(255) NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    event_data JSONB NOT NULL,
    metadata JSONB DEFAULT '{}',
    version BIGINT NOT NULL,
    global_position BIGSERIAL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_stream_version UNIQUE (stream_id, version)
);

CREATE INDEX idx_events_stream ON events(stream_id, version);
CREATE INDEX idx_events_global ON events(global_position);
CREATE INDEX idx_events_type ON events(event_type);

CREATE TABLE snapshots (
    stream_id VARCHAR(255) PRIMARY KEY,
    stream_type VARCHAR(255) NOT NULL,
    snapshot_data JSONB NOT NULL,
    version BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE subscription_checkpoints (
    subscription_id VARCHAR(255) PRIMARY KEY,
    last_position BIGINT NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 事件存储实现（Event Store Implementation）

```python
@dataclass
class Event:
    stream_id: str
    event_type: str
    data: dict
    metadata: dict = field(default_factory=dict)
    event_id: UUID = field(default_factory=uuid4)
    version: int | None = None
    global_position: int | None = None

class EventStore:  # backed by PostgreSQL schema above
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def append(self, stream_id: str, stream_type: str,
                     events: list[Event],
                     expected_version: int | None = None) -> list[Event]:
        """Append events with optimistic concurrency control."""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                if expected_version is not None:
                    current = await conn.fetchval(
                        "SELECT MAX(version) FROM events "
                        "WHERE stream_id = $1", stream_id
                    ) or 0
                    if current != expected_version:
                        raise ConcurrencyError(
                            f"Expected {expected_version}, got {current}"
                        )

                start = await conn.fetchval(
                    "SELECT COALESCE(MAX(version), 0) + 1 "
                    "FROM events WHERE stream_id = $1", stream_id
                )
                for i, evt in enumerate(events):
                    evt.version = start + i
                    row = await conn.fetchrow(
                        "INSERT INTO events (id, stream_id, stream_type, "
                        "event_type, event_data, metadata, version) "
                        "VALUES ($1,$2,$3,$4,$5,$6,$7) "
                        "RETURNING global_position",
                        evt.event_id, stream_id, stream_type,
                        evt.event_type, json.dumps(evt.data),
                        json.dumps(evt.metadata), evt.version,
                    )
                    evt.global_position = row["global_position"]
                return events

    async def read_stream(self, stream_id: str,
                          from_version: int = 0) -> list[Event]:
        """Read events for a single stream."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM events WHERE stream_id = $1 "
                "AND version >= $2 ORDER BY version",
                stream_id, from_version,
            )
            return [self._to_event(r) for r in rows]

    async def read_all(self, from_position: int = 0,
                       limit: int = 1000) -> list[Event]:
        """Read global event stream for projections / subscriptions."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM events WHERE global_position > $1 "
                "ORDER BY global_position LIMIT $2",
                from_position, limit,
            )
            return [self._to_event(r) for r in rows]
```

## 数据投影（Projections）

数据投影通过重新播放事件来生成优化过的读取数据结构，它是CQRS框架中的“Q”部分（即查询相关功能）。

### 数据投影的生命周期（Projection Lifecycle）

1. **从检查点恢复**                | 从上次处理完成的全球位置开始恢复读取                 |
2. **应用事件**                  | 根据事件类型更新读取模型                         |
3. **保存检查点**                | 将当前读取状态原子性地保存到数据库                   |

### 数据投影示例（Projection Example）

```python
class OrderSummaryProjection:
    def __init__(self, db, event_store: EventStore):
        self.db = db
        self.store = event_store

    async def run(self, batch_size: int = 100):
        position = await self._load_checkpoint()
        while True:
            events = await self.store.read_all(position, batch_size)
            if not events:
                await asyncio.sleep(1)
                continue
            for evt in events:
                await self._apply(evt)
                position = evt.global_position
            await self._save_checkpoint(position)

    async def _apply(self, event: Event):
        match event.event_type:
            case "OrderPlaced":
                await self.db.execute(
                    "INSERT INTO order_summaries (id, customer, total, status) "
                    "VALUES ($1,$2,$3,'placed')",
                    event.data["order_id"], event.data["customer_id"],
                    event.data["total_cents"],
                )
            case "OrderShipped":
                await self.db.execute(
                    "UPDATE order_summaries SET status='shipped' "
                    "WHERE id=$1", event.data["order_id"],
                )
```

### 数据投影设计原则（Projection Design Rules）

- **操作幂等性**                | 同一事件被多次重放时，系统状态不应发生改变                 |
- **每个读取模型对应一个投影**                | 每个读取模型应使用独立的投影数据结构                 |
- **可重建性**                | 投影数据应可完全重放                         |
- **分离存储**                | 投影数据可以存储在不同的数据库中（如PostgreSQL、Elasticsearch、Redis）           |

## 快照生成（Snapshotting）

快照功能通过缓存特定版本的数据来加速聚合查询的效率。当事件流中的事件数量超过一定数量（例如100条），或者聚合查询的计算成本较高时，可以使用快照功能。

### 快照生成流程（Snapshot Generation Process）

```python
class SnapshottedRepository:
    def __init__(self, event_store: EventStore, pool):
        self.store = event_store
        self.pool = pool

    async def load(self, stream_id: str) -> Aggregate:
        # 1. Try loading snapshot
        snap = await self._load_snapshot(stream_id)
        from_version = 0
        aggregate = Aggregate(stream_id)

        if snap:
            aggregate.restore(snap["data"])
            from_version = snap["version"] + 1

        # 2. Replay events after snapshot
        events = await self.store.read_stream(stream_id, from_version)
        for evt in events:
            aggregate.apply(evt)

        # 3. Snapshot if too many events replayed
        if len(events) > 50:
            await self._save_snapshot(
                stream_id, aggregate.snapshot(), aggregate.version
            )

        return aggregate
```

## CQRS集成（CQRS Integration）

CQRS框架将写入模型（命令到事件的转换过程）与读取模型（数据投影的生成过程）分离。

```
Commands ──► Aggregate ──► Event Store ──► Projections ──► Query API
 (write)     (domain)      (append)        (build)        (read)
```

### CQRS的关键原则（Key Principles of CQRS）

1. **写入端**：验证命令内容，生成相应事件，并确保数据一致性         |
2. **读取端**：订阅事件，生成优化后的查询结果                 |
3. **最终一致性**：读取操作可能会在写入操作之后出现延迟（几毫秒到几秒）         |
4. **独立扩展**：读取和写入操作可以独立扩展                   |

### 命令处理模式（Command Handler Pattern）

```python
class PlaceOrderHandler:
    def __init__(self, event_store: EventStore):
        self.store = event_store

    async def handle(self, cmd: PlaceOrderCommand):
        # Load aggregate from events
        events = await self.store.read_stream(f"Order-{cmd.order_id}")
        order = Order.reconstitute(events)

        # Execute command — validates and produces new events
        new_events = order.place(cmd.customer_id, cmd.items)

        # Persist with concurrency check
        await self.store.append(
            f"Order-{cmd.order_id}", "Order", new_events,
            expected_version=order.version,
        )
```

## EventStoreDB的集成方式（Integration with EventStoreDB）

```python
from esdbclient import EventStoreDBClient, NewEvent, StreamState
import json

client = EventStoreDBClient(uri="esdb://localhost:2113?tls=false")

def append_events(stream_name: str, events: list, expected_revision=None):
    new_events = [
        NewEvent(
            type=event['type'],
            data=json.dumps(event['data']).encode(),
            metadata=json.dumps(event.get('metadata', {})).encode()
        )
        for event in events
    ]
    state = (StreamState.ANY if expected_revision is None
             else StreamState.NO_STREAM if expected_revision == -1
             else expected_revision)
    return client.append_to_stream(stream_name, new_events, current_version=state)

def read_stream(stream_name: str, from_revision: int = 0):
    return [
        {'type': e.type, 'data': json.loads(e.data),
         'stream_position': e.stream_position}
        for e in client.get_stream(stream_name, stream_position=from_revision)
    ]

# Category projection: read all events for Order-* streams
def read_category(category: str):
    return read_stream(f"$ce-{category}")
```

## DynamoDB事件存储（DynamoDB Event Store）

**DynamoDB表结构设计：** 主键（PK）= `STREAM#{id}`，二级键（SK）= `VERSION#{version}`；使用GSI1实现全局排序。

## 最佳实践（Best Practices）

- **为事件流命名**                | 例如：`Order-abc123`                         |
- **在元数据中记录事件之间的关联关系**            | 便于追踪事件之间的逻辑关系                         |
- **从项目一开始就为事件模式添加版本控制**          | 为未来的架构演进做好准备                         |
- **实现幂等写入操作**                | 使用事件ID来避免数据重复                         |
- **为常见查询创建索引**                | 为常见的查询路径创建索引                         |

### 需避免的做法（Avoid These Practices）

- **不要修改或删除事件**                | 事件是不可变的历史数据，应保持原样                     |
- **不要存储大型数据**                | 保持事件数据体积小；外部存储大型数据文件                   |
- **不要忽略系统的并发限制**                | 正确处理系统并发带来的性能问题                     |
- **不要将投影数据与写入操作耦合**                | 投影数据应独立于写入操作进行部署                     |

## 绝对禁止的做法（Absolutely Avoid These Practices）

- **绝不要更新或删除事件**                | 事件是不可变的历史数据，应避免任何修改                     |
- **绝不要在追加操作时省略版本检查**                | 乐观并发控制可以防止数据丢失或损坏                     |
- **绝不要在事件中嵌入大型数据文件**                | 大型数据文件应外部存储，并通过ID引用                     |
- **绝不要使用随机UUID作为事件ID**                | 随机UUID可能导致数据重复                         |
- **绝不要使用投影数据进行命令验证**                | 应始终以事件流作为数据来源                     |
- **绝不要将投影数据与写入操作耦合**                | 投影数据应能够独立于写入操作进行重建                     |