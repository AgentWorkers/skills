---
name: kafka-architecture
description: Apache Kafka 架构专家，专注于集群设计、容量规划以及高可用性的实现。在设计和构建 Kafka 集群时，我能够提供专业的建议，包括选择合适的分区策略以及为生产环境中的工作负载确定合适的 broker 规格。
---

# Kafka架构与设计专家

具备对Apache Kafka架构模式、集群设计原则以及构建弹性、可扩展事件流处理平台的最佳实践的全面了解。

## 核心架构概念

### Kafka集群组件

**Broker**：
- 单个Kafka服务器，用于存储和提供数据服务
- 每个Broker可以处理数千个分区
- 通常情况下：小型集群包含3-10个Broker；大型企业则使用10-100个或更多Broker

**Controller**：
- 通过KRaft或ZooKeeper选举产生的一个Broker
- 负责管理分区的领导者和副本分配
- 当发生故障时，会触发自动重新选举

**Topic**：
- 消息流的逻辑通道
- 被划分为多个分区以实现并行处理
- 每个Topic可以有不同的保留策略

**Partition**：
- 记录的有序、不可变的序列
- 是并行处理的单位（一个Group中的消费者只能处理一个Partition）

**Replica**：
- 分布在多个Broker上的分区副本
- 1个Leader Replica（负责读写操作）
- N-1个Follower Replica（仅负责复制）
- In-Sync Replicas（ISR）：与Leader保持同步的副本

### KRaft模式与ZooKeeper模式

**KRaft模式**（推荐使用，Kafka 3.3及以上版本）：
```yaml
Cluster Metadata:
  - Stored in Kafka itself (no external ZooKeeper)
  - Metadata topic: __cluster_metadata
  - Controller quorum (3 or 5 nodes)
  - Faster failover (<1s vs 10-30s)
  - Simplified operations
```

**ZooKeeper模式**（旧模式，已在Kafka 4.0中被弃用）：
```yaml
External Coordination:
  - Requires separate ZooKeeper ensemble (3-5 nodes)
  - Stores cluster metadata, configs, ACLs
  - Slower failover (10-30 seconds)
  - More complex to operate
```

**迁移**：Kafka 3.6及以上版本支持从ZooKeeper模式迁移到KRaft模式

## 集群规模规划指南

### 小型集群（开发/测试环境）

```yaml
Configuration:
  Brokers: 3
  Partitions per broker: ~100-500
  Total partitions: 300-1500
  Replication factor: 3
  Hardware:
    - CPU: 4-8 cores
    - RAM: 8-16 GB
    - Disk: 500 GB - 1 TB SSD
    - Network: 1 Gbps

Use Cases:
  - Development environments
  - Low-volume production (<10 MB/s)
  - Proof of concepts
  - Single datacenter

Example Workload:
  - 50 topics
  - 5-10 partitions per topic
  - 1 million messages/day
  - 7-day retention
```

### 中型集群（标准生产环境）

```yaml
Configuration:
  Brokers: 6-12
  Partitions per broker: 500-2000
  Total partitions: 3K-24K
  Replication factor: 3
  Hardware:
    - CPU: 16-32 cores
    - RAM: 64-128 GB
    - Disk: 2-8 TB NVMe SSD
    - Network: 10 Gbps

Use Cases:
  - Standard production workloads
  - Multi-team environments
  - Regional deployments
  - Up to 500 MB/s throughput

Example Workload:
  - 200-500 topics
  - 10-50 partitions per topic
  - 100 million messages/day
  - 30-day retention
```

### 大型集群（大规模生产环境）

```yaml
Configuration:
  Brokers: 20-100+
  Partitions per broker: 2000-4000
  Total partitions: 40K-400K+
  Replication factor: 3
  Hardware:
    - CPU: 32-64 cores
    - RAM: 128-256 GB
    - Disk: 8-20 TB NVMe SSD
    - Network: 25-100 Gbps

Use Cases:
  - Large enterprises
  - Multi-region deployments
  - Event-driven architectures
  - 1+ GB/s throughput

Example Workload:
  - 1000+ topics
  - 50-200 partitions per topic
  - 1+ billion messages/day
  - 90-365 day retention
```

### Kafka Streams / Exactly-Once语义（EOS）集群

```yaml
Configuration:
  Brokers: 6-12+ (same as standard, but more control plane load)
  Partitions per broker: 500-1500 (fewer due to transaction overhead)
  Total partitions: 3K-18K
  Replication factor: 3
  Hardware:
    - CPU: 16-32 cores (more CPU for transactions)
    - RAM: 64-128 GB
    - Disk: 4-12 TB NVMe SSD (more for transaction logs)
    - Network: 10-25 Gbps

Special Considerations:
  - More brokers due to transaction coordinator load
  - Lower partition count per broker (transactions = more overhead)
  - Higher disk IOPS for transaction logs
  - min.insync.replicas=2 mandatory for EOS
  - acks=all required for producers

Use Cases:
  - Stream processing with exactly-once guarantees
  - Financial transactions
  - Event sourcing with strict ordering
  - Multi-step workflows requiring atomicity
```

## 分区策略

### 分区数量如何确定？

**计算公式**：
```
Partitions = max(
  Target Throughput / Single Partition Throughput,
  Number of Consumers (for parallelism),
  Future Growth Factor (2-3x)
)

Single Partition Limits:
  - Write throughput: ~10-50 MB/s
  - Read throughput: ~30-100 MB/s
  - Message rate: ~10K-100K msg/s
```

**示例**：

- **高吞吐量Topic**（日志、事件）：
```yaml
Requirements:
  - Write: 200 MB/s
  - Read: 500 MB/s (multiple consumers)
  - Expected growth: 3x in 1 year

Calculation:
  Write partitions: 200 MB/s ÷ 20 MB/s = 10
  Read partitions: 500 MB/s ÷ 40 MB/s = 13
  Growth factor: 13 × 3 = 39

Recommendation: 40-50 partitions
```

- **低延迟Topic**（命令、请求）：
```yaml
Requirements:
  - Write: 5 MB/s
  - Read: 10 MB/s
  - Latency: <10ms p99
  - Order preservation: By user ID

Calculation:
  Throughput partitions: 5 MB/s ÷ 20 MB/s = 1
  Parallelism: 4 (for redundancy)

Recommendation: 4-6 partitions (keyed by user ID)
```

- **死信队列**：
```yaml
Recommendation: 1-3 partitions
Reason: Low volume, order less important
```

### 分区键的选择

**理想的分区键**（高基数、均匀分布）：
```yaml
✅ User ID (UUIDs):
  - Millions of unique values
  - Even distribution
  - Example: "user-123e4567-e89b-12d3-a456-426614174000"

✅ Device ID (IoT):
  - Unique per device
  - Natural sharding
  - Example: "device-sensor-001-zone-a"

✅ Order ID (E-commerce):
  - Unique per transaction
  - Even temporal distribution
  - Example: "order-2024-11-15-abc123"
```

**不理想的分区键**（低基数、数据热点）：
```yaml
❌ Country Code:
  - Only ~200 values
  - Uneven (US, CN >> others)
  - Creates partition hotspots

❌ Boolean Flags:
  - Only 2 values (true/false)
  - Severe imbalance

❌ Date (YYYY-MM-DD):
  - All today's traffic → 1 partition
  - Temporal hotspot
```

**复合分区键**（结合两种优点）：
```yaml
✅ Country + User ID:
  - Partition by country for locality
  - Sub-partition by user for distribution
  - Example: "US:user-123" → hash("US:user-123")

✅ Tenant + Event Type + Timestamp:
  - Multi-tenant isolation
  - Event type grouping
  - Temporal ordering
```

## 复制与高可用性

### 复制因子指南

```yaml
Development:
  Replication Factor: 1
  Reason: Fast, no durability needed

Production (Standard):
  Replication Factor: 3
  Reason: Balance durability vs cost
  Tolerates: 2 broker failures (with min.insync.replicas=2)

Production (Critical):
  Replication Factor: 5
  Reason: Maximum durability
  Tolerates: 4 broker failures (with min.insync.replicas=3)
  Use Cases: Financial transactions, audit logs

Multi-Datacenter:
  Replication Factor: 3 per DC (6 total)
  Reason: DC-level fault tolerance
  Requires: MirrorMaker 2 or Confluent Replicator
```

### `min.insync.replicas`配置参数：
```yaml
min.insync.replicas=2:
  - At least 2 replicas must acknowledge writes
  - Typical for replication.factor=3
  - Prevents data loss if 1 broker fails

min.insync.replicas=1:
  - Only leader must acknowledge (dangerous!)
  - Use only for non-critical topics

min.insync.replicas=3:
  - At least 3 replicas must acknowledge
  - For replication.factor=5 (critical systems)
```

**规则**：`min.insync.replicas ≤ replication.factor - 1`（允许最多1个副本发生故障）

### Rack Awareness（机架感知）

```yaml
Configuration:
  broker.rack=rack1  # Broker 1
  broker.rack=rack2  # Broker 2
  broker.rack=rack3  # Broker 3

Benefit:
  - Replicas spread across racks
  - Survives rack-level failures (power, network)
  - Example: Topic with RF=3 → 1 replica per rack

Placement:
  Leader: rack1
  Follower 1: rack2
  Follower 2: rack3
```

## 保留策略

### 基于时间的保留策略
```yaml
Short-Term (Events, Logs):
  retention.ms: 86400000  # 1 day
  Use Cases: Real-time analytics, monitoring

Medium-Term (Transactions):
  retention.ms: 604800000  # 7 days
  Use Cases: Standard business events

Long-Term (Audit, Compliance):
  retention.ms: 31536000000  # 365 days
  Use Cases: Regulatory requirements, event sourcing

Infinite (Event Sourcing):
  retention.ms: -1  # Forever
  cleanup.policy: compact
  Use Cases: Source of truth, state rebuilding
```

### 基于大小的保留策略
```yaml
retention.bytes: 10737418240  # 10 GB per partition

Combined (Time OR Size):
  retention.ms: 604800000      # 7 days
  retention.bytes: 107374182400  # 100 GB
  # Whichever limit is reached first
```

### 数据压缩（日志压缩）

```yaml
cleanup.policy: compact

How It Works:
  - Keeps only latest value per key
  - Deletes old versions
  - Preserves full history initially, compacts later

Use Cases:
  - Database changelogs (CDC)
  - User profile updates
  - Configuration management
  - State stores

Example:
  Before Compaction:
    user:123 → {name: "Alice", v:1}
    user:123 → {name: "Alice", v:2, email: "alice@ex.com"}
    user:123 → {name: "Alice A.", v:3}

  After Compaction:
    user:123 → {name: "Alice A.", v:3}  # Latest only
```

## 性能优化

### Broker配置优化
```yaml
# Network threads (handle client connections)
num.network.threads: 8  # Increase for high connection count

# I/O threads (disk operations)
num.io.threads: 16  # Set to number of disks × 2

# Replica fetcher threads
num.replica.fetchers: 4  # Increase for many partitions

# Socket buffer sizes
socket.send.buffer.bytes: 1048576    # 1 MB
socket.receive.buffer.bytes: 1048576  # 1 MB

# Log flush (default: OS handles flushing)
log.flush.interval.messages: 10000  # Flush every 10K messages
log.flush.interval.ms: 1000         # Or every 1 second
```

### 生产者端优化
```yaml
High Throughput:
  batch.size: 65536            # 64 KB
  linger.ms: 100               # Wait 100ms for batching
  compression.type: lz4        # Fast compression
  acks: 1                      # Leader only

Low Latency:
  batch.size: 16384            # 16 KB (default)
  linger.ms: 0                 # Send immediately
  compression.type: none
  acks: 1

Durability (Exactly-Once):
  batch.size: 16384
  linger.ms: 10
  compression.type: lz4
  acks: all
  enable.idempotence: true
  transactional.id: "producer-1"
```

### 消费者端优化
```yaml
High Throughput:
  fetch.min.bytes: 1048576     # 1 MB
  fetch.max.wait.ms: 500       # Wait 500ms to accumulate

Low Latency:
  fetch.min.bytes: 1           # Immediate fetch
  fetch.max.wait.ms: 100       # Short wait

Max Parallelism:
  # Deploy consumers = number of partitions
  # More consumers than partitions = idle consumers
```

## 多数据中心架构模式

### 主从架构（灾难恢复）
```yaml
Architecture:
  Primary DC: Full Kafka cluster
  Secondary DC: Replica cluster (MirrorMaker 2)

Configuration:
  - Producers → Primary only
  - Consumers → Primary only
  - MirrorMaker 2: Primary → Secondary (async replication)

Failover:
  1. Detect primary failure
  2. Switch producers/consumers to secondary
  3. Promote secondary to primary

Recovery Time: 5-30 minutes (manual)
Data Loss: Potential (async replication lag)
```

### 主主架构（地理复制）
```yaml
Architecture:
  DC1: Kafka cluster (region A)
  DC2: Kafka cluster (region B)
  Bidirectional replication via MirrorMaker 2

Configuration:
  - Producers → Nearest DC
  - Consumers → Nearest DC or both
  - Conflict resolution: Last-write-wins or custom

Challenges:
  - Duplicate messages (at-least-once delivery)
  - Ordering across DCs not guaranteed
  - Circular replication prevention

Use Cases:
  - Global applications
  - Regional compliance (GDPR)
  - Load distribution
```

### 扩展集群（同步复制）
```yaml
Architecture:
  Single Kafka cluster spanning 2 DCs
  Rack awareness: DC1 = rack1, DC2 = rack2

Configuration:
  min.insync.replicas: 2
  replication.factor: 4 (2 per DC)
  acks: all

Requirements:
  - Low latency between DCs (<10ms)
  - High bandwidth link (10+ Gbps)
  - Dedicated fiber

Trade-offs:
  Pros: Synchronous replication, zero data loss
  Cons: Latency penalty, network dependency
```

## 监控与可观测性

### 关键指标

- **Broker指标**：
```yaml
UnderReplicatedPartitions:
  Alert: > 0 for > 5 minutes
  Indicates: Replica lag, broker failure

OfflinePartitionsCount:
  Alert: > 0
  Indicates: No leader elected (critical!)

ActiveControllerCount:
  Alert: != 1 (should be exactly 1)
  Indicates: Split brain or no controller

RequestHandlerAvgIdlePercent:
  Alert: < 20%
  Indicates: Broker CPU saturation
```

- **Topic指标**：
```yaml
MessagesInPerSec:
  Monitor: Throughput trends
  Alert: Sudden drops (producer failure)

BytesInPerSec / BytesOutPerSec:
  Monitor: Network utilization
  Alert: Approaching NIC limits

RecordsLagMax (Consumer):
  Alert: > 10000 or growing
  Indicates: Consumer can't keep up
```

- **磁盘指标**：
```yaml
LogSegmentSize:
  Monitor: Disk usage trends
  Alert: > 80% capacity

LogFlushRateAndTimeMs:
  Monitor: Disk write latency
  Alert: > 100ms p99 (slow disk)
```

## 安全策略

### 认证与授权
```yaml
SASL/SCRAM-SHA-512:
  - Industry standard
  - User/password authentication
  - Stored in ZooKeeper/KRaft

ACLs (Access Control Lists):
  - Per-topic, per-group permissions
  - Operations: READ, WRITE, CREATE, DELETE, ALTER
  - Example:
      bin/kafka-acls.sh --add \
        --allow-principal User:alice \
        --operation READ \
        --topic orders

mTLS (Mutual TLS):
  - Certificate-based auth
  - Strong cryptographic identity
  - Best for service-to-service
```

## 与SpecWeave的集成

- **自动架构检测**：
```typescript
import { ClusterSizingCalculator } from './lib/utils/sizing';

const calculator = new ClusterSizingCalculator();
const recommendation = calculator.calculate({
  throughputMBps: 200,
  retentionDays: 30,
  replicationFactor: 3,
  topicCount: 100
});

console.log(recommendation);
// {
//   brokers: 8,
//   partitionsPerBroker: 1500,
//   diskPerBroker: 6000 GB,
//   ramPerBroker: 64 GB
// }
```

- **SpecWeave命令**：
  - `/sw-kafka:deploy`：部署前验证集群规模
  - `/sw-kafka:monitor-setup`：配置关键指标的监控设置

## 相关技能

- `/sw-kafka:kafka-mcp-integration`：MCP服务器的配置与管理
- `/sw-kafka:kafka-cli-tools`：Kafka的命令行工具

## 外部链接

- [Kafka官方文档 - 架构部分](https://kafka.apache.org/documentation/#design)
- [Confluent - 如何选择Kafka集群中的Topic数量与分区数量](https://www.confluent.io/blog/how-to-choose-the-number-of-topics-partitions-in-a-kafka-cluster/)
- [KRaft模式概述](https://kafka.apache.org/documentation/#kraft)
- [LinkedIn Engineering - Kafka的大规模部署实践](https://engineering.linkedin.com/kafka/running-kafka-scale)