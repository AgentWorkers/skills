---
name: kafka-cli-tools
description: Kafka CLI工具专家，精通kcat、kafkactl以及原生Kafka命令。适用于通过命令行生产/消费消息、列出主题或使用CLI工具排查Kafka故障的场景。
---

# Kafka CLI 工具专家

具备对现代 Kafka CLI 工具的全面了解，能够应用于生产环境、开发及故障排查场景。

## 支持的 CLI 工具

### 1. kcat (kafkacat) – 万能工具

**安装**：
```bash
# macOS
brew install kcat

# Ubuntu/Debian
apt-get install kafkacat

# From source
git clone https://github.com/edenhill/kcat.git
cd kcat
./configure && make && sudo make install
```

**核心功能**：

- **生产消息**：
```bash
# Simple produce
echo "Hello Kafka" | kcat -P -b localhost:9092 -t my-topic

# Produce with key (key:value format)
echo "user123:Login event" | kcat -P -b localhost:9092 -t events -K:

# Produce from file
cat events.json | kcat -P -b localhost:9092 -t events

# Produce with headers
echo "msg" | kcat -P -b localhost:9092 -t my-topic -H "source=app1" -H "version=1.0"

# Produce with compression
echo "data" | kcat -P -b localhost:9092 -t my-topic -z gzip

# Produce with acks=all
echo "critical-data" | kcat -P -b localhost:9092 -t my-topic -X acks=all
```

- **消费消息**：
```bash
# Consume from beginning
kcat -C -b localhost:9092 -t my-topic -o beginning

# Consume from end (latest)
kcat -C -b localhost:9092 -t my-topic -o end

# Consume specific partition
kcat -C -b localhost:9092 -t my-topic -p 0 -o beginning

# Consume with consumer group
kcat -C -b localhost:9092 -G my-group my-topic

# Consume N messages and exit
kcat -C -b localhost:9092 -t my-topic -c 10

# Custom format (topic:partition:offset:key:value)
kcat -C -b localhost:9092 -t my-topic -f 'Topic: %t, Partition: %p, Offset: %o, Key: %k, Value: %s\n'

# JSON output
kcat -C -b localhost:9092 -t my-topic -J
```

- **元数据管理**：
```bash
# List all topics
kcat -L -b localhost:9092

# Get topic metadata (JSON)
kcat -L -b localhost:9092 -t my-topic -J

# Query topic offsets
kcat -Q -b localhost:9092 -t my-topic

# Check broker health
kcat -L -b localhost:9092 | grep "broker\|topic"
```

- **SASL/SSL 认证**：
```bash
# SASL/PLAINTEXT
kcat -b localhost:9092 \
  -X security.protocol=SASL_PLAINTEXT \
  -X sasl.mechanism=PLAIN \
  -X sasl.username=admin \
  -X sasl.password=admin-secret \
  -L

# SASL/SSL
kcat -b localhost:9093 \
  -X security.protocol=SASL_SSL \
  -X sasl.mechanism=SCRAM-SHA-256 \
  -X sasl.username=admin \
  -X sasl.password=admin-secret \
  -X ssl.ca.location=/path/to/ca-cert \
  -L

# mTLS (mutual TLS)
kcat -b localhost:9093 \
  -X security.protocol=SSL \
  -X ssl.ca.location=/path/to/ca-cert \
  -X ssl.certificate.location=/path/to/client-cert.pem \
  -X ssl.key.location=/path/to/client-key.pem \
  -L
```

### 2. kcli – 基于 Kubernetes 的 Kafka CLI

**安装**：
```bash
# Install via krew (Kubernetes plugin manager)
kubectl krew install kcli

# Or download binary
curl -LO https://github.com/cswank/kcli/releases/latest/download/kcli-linux-amd64
chmod +x kcli-linux-amd64
sudo mv kcli-linux-amd64 /usr/local/bin/kcli
```

**与 Kubernetes 的集成**：
```bash
# Connect to Kafka running in k8s
kcli --context my-cluster --namespace kafka

# Produce to topic in k8s
echo "msg" | kcli produce --topic my-topic --brokers kafka-broker:9092

# Consume from k8s Kafka
kcli consume --topic my-topic --brokers kafka-broker:9092 --from-beginning

# List topics in k8s cluster
kcli topics list --brokers kafka-broker:9092
```

**适用场景**：
- 基于 Kubernetes 的部署
- 使用 Helmfile 或 Kustomize 进行配置
- 与 ArgoCD/Flux 结合的 GitOps 流程

### 3. kaf – 现代化的终端用户界面 (TUI)

**安装**：
```bash
# macOS
brew install kaf

# Linux (via snap)
snap install kaf

# From source
go install github.com/birdayz/kaf/cmd/kaf@latest
```

**交互式功能**：
```bash
# Configure cluster
kaf config add-cluster local --brokers localhost:9092

# Use cluster
kaf config use-cluster local

# Interactive topic browsing (TUI)
kaf topics

# Interactive consume (arrow keys to navigate)
kaf consume my-topic

# Produce interactively
kaf produce my-topic

# Consumer group management
kaf groups
kaf group describe my-group
kaf group reset my-group --topic my-topic --offset earliest

# Schema Registry integration
kaf schemas
kaf schema get my-schema
```

**适用场景**：
- 开发工作流程
- 快速探索主题信息
- 消费者组调试
- 架构注册表管理

### 4. kafkactl – 高级管理工具

**安装**：
```bash
# macOS
brew install deviceinsight/packages/kafkactl

# Linux
curl -L https://github.com/deviceinsight/kafkactl/releases/latest/download/kafkactl_linux_amd64 -o kafkactl
chmod +x kafkactl
sudo mv kafkactl /usr/local/bin/

# Via Docker
docker run --rm -it deviceinsight/kafkactl:latest
```

**高级功能**：
```bash
# Configure context
kafkactl config add-context local --brokers localhost:9092

# Topic management
kafkactl create topic my-topic --partitions 3 --replication-factor 2
kafkactl alter topic my-topic --config retention.ms=86400000
kafkactl delete topic my-topic

# Consumer group operations
kafkactl describe consumer-group my-group
kafkactl reset consumer-group my-group --topic my-topic --offset earliest
kafkactl delete consumer-group my-group

# ACL management
kafkactl create acl --allow --principal User:alice --operation READ --topic my-topic
kafkactl list acls

# Quota management
kafkactl alter client-quota --user alice --producer-byte-rate 1048576

# Reassign partitions
kafkactl alter partition --topic my-topic --partition 0 --replicas 1,2,3
```

**适用场景**：
- 生产集群管理
- 访问控制列表 (ACL) 管理
- 分区重新分配
- 配额管理

## 工具对比表

| 功能 | kcat | kcli | kaf | kafkactl |
|---------|------|------|-----|----------|
| **安装难度** | 简单 | 中等 | 简单 | 简单 |
| **消息生产** | 支持高级操作 | 支持基本操作 | 支持交互式操作 | 支持基本操作 |
| **消息消费** | 支持高级操作 | 支持基本操作 | 支持交互式操作 | 支持基本操作 |
| **元数据管理** | 支持 JSON 格式输出 | 支持基本操作 | 支持图形化界面 | 支持详细信息 |
| **图形化界面** | 不支持 | 不支持 | 支持 | 支持（但功能有限） |
| **管理功能** | 不支持 | 不支持 | 有限支持 | 支持高级管理 |
| **SASL/SSL 认证** | 支持 | 支持 | 支持 | 支持 |
| **Kubernetes 原生集成** | 不支持 | 支持 | 不支持 | 不支持 |
| **架构注册表** | 不支持 | 不支持 | 支持 | 不支持 |
| **访问控制列表 (ACLs)** | 不支持 | 不支持 | 不支持 | 支持 |
| **配额管理** | 不支持 | 不支持 | 不支持 | 支持 |
| **适用场景** | 适用于脚本编写和运维 | 适用于 Kubernetes 环境 | 适用于开发 | 适用于生产环境的管理 |

## 常见使用场景

### 1. 使用最佳配置创建主题

```bash
# Using kafkactl (recommended for production)
kafkactl create topic orders \
  --partitions 12 \
  --replication-factor 3 \
  --config retention.ms=604800000 \
  --config compression.type=lz4 \
  --config min.insync.replicas=2

# Verify with kcat
kcat -L -b localhost:9092 -t orders -J | jq '.topics[0]'
```

### 2. 死信队列 (Dead Letter Queue) 的实现

```bash
# Produce failed message to DLQ
echo "failed-msg" | kcat -P -b localhost:9092 -t orders-dlq \
  -H "original-topic=orders" \
  -H "error=DeserializationException" \
  -H "timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Monitor DLQ
kcat -C -b localhost:9092 -t orders-dlq -f 'Headers: %h\nValue: %s\n\n'
```

### 3. 监控消费者组的延迟情况

```bash
# Using kafkactl
kafkactl describe consumer-group my-app | grep LAG

# Using kcat (via external tool like kcat-lag)
kcat -L -b localhost:9092 -J | jq '.topics[].partitions[] | select(.topic=="my-topic")'

# Using kaf (interactive)
kaf groups
# Then select group to see lag in TUI
```

### 4. 多集群复制测试

```bash
# Produce to source cluster
echo "test" | kcat -P -b source-kafka:9092 -t replicated-topic

# Consume from target cluster
kcat -C -b target-kafka:9092 -t replicated-topic -o end -c 1

# Compare offsets
kcat -Q -b source-kafka:9092 -t replicated-topic
kcat -Q -b target-kafka:9092 -t replicated-topic
```

### 5. 性能测试

```bash
# Produce 10,000 messages with kcat
seq 1 10000 | kcat -P -b localhost:9092 -t perf-test

# Consume and measure throughput
time kcat -C -b localhost:9092 -t perf-test -c 10000 -o beginning > /dev/null

# Test with compression
seq 1 10000 | kcat -P -b localhost:9092 -t perf-test -z lz4
```

## 故障排查

### 连接问题

```bash
# Test broker connectivity
kcat -L -b localhost:9092

# Check SSL/TLS connection
openssl s_client -connect localhost:9093 -showcerts

# Verify SASL authentication
kcat -b localhost:9092 \
  -X security.protocol=SASL_PLAINTEXT \
  -X sasl.mechanism=PLAIN \
  -X sasl.username=admin \
  -X sasl.password=wrong-password \
  -L
# Should fail with authentication error
```

### 消息未显示

```bash
# Check topic exists
kcat -L -b localhost:9092 | grep my-topic

# Check partition count
kcat -L -b localhost:9092 -t my-topic -J | jq '.topics[0].partition_count'

# Query all partition offsets
kcat -Q -b localhost:9092 -t my-topic

# Consume from all partitions
for i in {0..11}; do
  echo "Partition $i:"
  kcat -C -b localhost:9092 -t my-topic -p $i -c 1 -o end
done
```

### 消费者组卡住（无法正常工作）

```bash
# Check consumer group state
kafkactl describe consumer-group my-app

# Reset to beginning
kafkactl reset consumer-group my-app --topic my-topic --offset earliest

# Reset to specific offset
kafkactl reset consumer-group my-app --topic my-topic --partition 0 --offset 12345

# Delete consumer group (all consumers must be stopped first)
kafkactl delete consumer-group my-app
```

## 与 SpecWeave 的集成

**自动检测 CLI 工具**：
SpecWeave 可自动检测已安装的 CLI 工具，并推荐最适合当前操作的工具：

```typescript
import { CLIToolDetector } from './lib/cli/detector';

const detector = new CLIToolDetector();
const available = await detector.detectAll();

// Recommended tool for produce operation
if (available.includes('kcat')) {
  console.log('Use kcat for produce (fastest)');
} else if (available.includes('kaf')) {
  console.log('Use kaf for produce (interactive)');
}
```

**SpecWeave 命令示例**：
- `/sw-kafka:dev-env` – 使用 Docker Compose 和 kcat 进行本地测试
- `/sw-kafka:monitor-setup` – 设置基于 kcat 的延迟监控
- `/sw-kafka:mcp-configure` – 验证 CLI 工具是否已正确安装

## 安全最佳实践

1. **切勿硬编码凭证** – 使用环境变量或秘密管理工具进行配置
2. **在生产环境中使用 SSL/TLS** – 配置 `-X security.protocol=SASL_SSL`
3. **优先使用 SCRAM 协议** – 设置 `-X sasl.mechanism=SCRAM-SHA-256`
4. **定期更新凭证** – 定期更换密码和证书
5. **最小权限原则** – 仅向用户授予必要的访问权限

## 相关技能

- `/sw-kafka:kafka-mcp-integration` – MCP 服务器的设置与配置
- `/sw-kafka:kafka-architecture` – 集群的设计与规模规划

## 外部链接

- [kcat GitHub](https://github.com/edenhill/kcat)
- [kcli GitHub](https://github.com/cswank/kcli)
- [kaf GitHub](https://github.com/birdayz/kaf)
- [kafkactl GitHub](https://github.com/deviceinsight/kafkactl)
- [Apache Kafka 官方文档](https://kafka.apache.org/documentation/)