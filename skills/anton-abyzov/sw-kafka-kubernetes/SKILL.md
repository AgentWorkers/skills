---
name: kafka-kubernetes
description: Kubernetes 部署专家，专注于使用 Helm、Strimzi 和 Confluent 操作符来部署 Apache Kafka。适用于在 Kubernetes 上部署 Kafka、配置 StatefulSets，以及在生产环境中选择合适的 Kafka 操作符的场景。
---

# 在 Kubernetes 上部署 Kafka

本文档提供了使用行业标准工具在 Kubernetes 上部署 Apache Kafka 的专家指导。

## 适用场景

当您需要以下帮助时，请参考本文档：
- **Kubernetes 部署**：在 Kubernetes 上部署 Kafka、在 K8s 中运行 Kafka、使用 Kafka Helm 图表
- **Kafka 运营商选择**：Strimzi 与 Confluent 运营商的比较
- **StatefulSet 模式**：Kafka StatefulSet 的最佳实践、Kafka 的持久化存储
- **生产级 Kubernetes 环境**：适用于生产环境的 Kafka 部署、Kafka 在 Kubernetes 中的高可用性配置

## 我所掌握的知识

### 部署方案对比

| 方案 | 难度 | 是否适合生产环境 | 适用场景 |
|---------|---------|-------------|---------|
| **Strimzi 运营商** | 简单 | ✅ 是 | 适用于自管理的 Kafka 部署（基于 CNCF 项目） |
| **Confluent 运营商** | 中等 | ✅ 是 | 提供企业级功能，支持 Confluent 生态系统 |
| **Bitnami Helm 图表** | 简单 | ⚠️ 主要适用于开发/测试环境 |
| **自定义 StatefulSet** | 复杂 | ⚠️ 需要专业知识 | 提供完全的控制权和自定义配置 |

**推荐方案**：对于大多数生产环境，建议使用 **Strimzi 运营商**（基于 CNCF 项目，拥有活跃的社区支持，并支持 KRaft 协议）。

## 部署方法 1：使用 Strimzi 运营商（推荐）

**Strimzi** 是一个基于 CNCF 的项目，提供了用于管理 Apache Kafka 的 Kubernetes 运营商。

### 主要特性
- ✅ 支持 KRaft 模式（Kafka 3.6 及更高版本，无需 ZooKeeper）
- ✅ 基于声明式配置（CRDs）进行 Kafka 管理
- ✅ 自动化升级
- 内置监控功能（Prometheus 指标）
- 支持 MirrorMaker 2 进行数据复制
- 支持与 Kafka Connect 的集成
- 通过 CRDs 进行用户和主题的管理

### 安装（使用 Helm）

```bash
# 1. Add Strimzi Helm repository
helm repo add strimzi https://strimzi.io/charts/
helm repo update

# 2. Create namespace
kubectl create namespace kafka

# 3. Install Strimzi Operator
helm install strimzi-kafka-operator strimzi/strimzi-kafka-operator \
  --namespace kafka \
  --set watchNamespaces="{kafka}" \
  --version 0.39.0

# 4. Verify operator is running
kubectl get pods -n kafka
# Output: strimzi-cluster-operator-... Running
```

### 部署 Kafka 集群（KRaft 模式）

```yaml
# kafka-cluster.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaNodePool
metadata:
  name: kafka-pool
  namespace: kafka
  labels:
    strimzi.io/cluster: my-kafka-cluster
spec:
  replicas: 3
  roles:
    - controller
    - broker
  storage:
    type: jbod
    volumes:
      - id: 0
        type: persistent-claim
        size: 100Gi
        class: fast-ssd
        deleteClaim: false
---
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-kafka-cluster
  namespace: kafka
  annotations:
    strimzi.io/kraft: enabled
    strimzi.io/node-pools: enabled
spec:
  kafka:
    version: 3.7.0
    metadataVersion: 3.7-IV4
    replicas: 3

    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
        authentication:
          type: tls
      - name: external
        port: 9094
        type: loadbalancer
        tls: true
        authentication:
          type: tls

    config:
      default.replication.factor: 3
      min.insync.replicas: 2
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      auto.create.topics.enable: false
      log.retention.hours: 168
      log.segment.bytes: 1073741824
      compression.type: lz4

    resources:
      requests:
        memory: 4Gi
        cpu: "2"
      limits:
        memory: 8Gi
        cpu: "4"

    jvmOptions:
      -Xms: 2048m
      -Xmx: 4096m

    metricsConfig:
      type: jmxPrometheusExporter
      valueFrom:
        configMapKeyRef:
          name: kafka-metrics
          key: kafka-metrics-config.yml
```

```bash
# Apply Kafka cluster
kubectl apply -f kafka-cluster.yaml

# Wait for cluster to be ready (5-10 minutes)
kubectl wait kafka/my-kafka-cluster --for=condition=Ready --timeout=600s -n kafka

# Check status
kubectl get kafka -n kafka
# Output: my-kafka-cluster   3.7.0   3         True
```

### 声明式创建主题

```yaml
# kafka-topics.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: user-events
  namespace: kafka
  labels:
    strimzi.io/cluster: my-kafka-cluster
spec:
  partitions: 12
  replicas: 3
  config:
    retention.ms: 604800000  # 7 days
    segment.bytes: 1073741824
    compression.type: lz4
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: order-events
  namespace: kafka
  labels:
    strimzi.io/cluster: my-kafka-cluster
spec:
  partitions: 6
  replicas: 3
  config:
    retention.ms: 2592000000  # 30 days
    min.insync.replicas: 2
```

### 声明式创建用户

```bash
# Apply topics
kubectl apply -f kafka-topics.yaml

# Verify topics created
kubectl get kafkatopics -n kafka
```

### 声明式配置用户权限

```yaml
# kafka-users.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaUser
metadata:
  name: my-producer
  namespace: kafka
  labels:
    strimzi.io/cluster: my-kafka-cluster
spec:
  authentication:
    type: tls
  authorization:
    type: simple
    acls:
      - resource:
          type: topic
          name: user-events
          patternType: literal
        operations: [Write, Describe]
      - resource:
          type: topic
          name: order-events
          patternType: literal
        operations: [Write, Describe]
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaUser
metadata:
  name: my-consumer
  namespace: kafka
  labels:
    strimzi.io/cluster: my-kafka-cluster
spec:
  authentication:
    type: tls
  authorization:
    type: simple
    acls:
      - resource:
          type: topic
          name: user-events
          patternType: literal
        operations: [Read, Describe]
      - resource:
          type: group
          name: my-consumer-group
          patternType: literal
        operations: [Read]
```

### 部署方法 2：使用 Confluent 运营商

**Confluent for Kubernetes (CFK)** 提供企业级 Kafka 管理功能。

### 主要特性
- 完整的 Confluent 生态系统（包括 Kafka、Schema Registry、ksqlDB、Connect）
- 支持混合部署（Kubernetes + 本地环境）
- 支持无停机时间的自动升级
- 支持多区域数据复制
- 具备高级安全特性（RBAC、加密）
- ⚠️ 需要购买 Confluent Platform 许可证

### 安装

```bash
# 1. Add Confluent Helm repository
helm repo add confluentinc https://packages.confluent.io/helm
helm repo update

# 2. Create namespace
kubectl create namespace confluent

# 3. Install Confluent Operator
helm install confluent-operator confluentinc/confluent-for-kubernetes \
  --namespace confluent \
  --version 0.921.11

# 4. Verify
kubectl get pods -n confluent
```

### 部署 Kafka 集群

```yaml
# kafka-cluster-confluent.yaml
apiVersion: platform.confluent.io/v1beta1
kind: Kafka
metadata:
  name: kafka
  namespace: confluent
spec:
  replicas: 3
  image:
    application: confluentinc/cp-server:7.6.0
    init: confluentinc/confluent-init-container:2.7.0

  dataVolumeCapacity: 100Gi
  storageClass:
    name: fast-ssd

  metricReporter:
    enabled: true

  listeners:
    internal:
      authentication:
        type: plain
      tls:
        enabled: true
    external:
      authentication:
        type: plain
      tls:
        enabled: true

  dependencies:
    zookeeper:
      endpoint: zookeeper.confluent.svc.cluster.local:2181

  podTemplate:
    resources:
      requests:
        memory: 4Gi
        cpu: 2
      limits:
        memory: 8Gi
        cpu: 4
```

### 部署方法 3：使用 Bitnami Helm 图表（适用于开发/测试环境）

**Bitnami Helm 图表** 配置简单，但不太适合生产环境。

### 安装

```bash
# 1. Add Bitnami repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# 2. Install Kafka (KRaft mode)
helm install kafka bitnami/kafka \
  --namespace kafka \
  --create-namespace \
  --set kraft.enabled=true \
  --set controller.replicaCount=3 \
  --set broker.replicaCount=3 \
  --set persistence.size=100Gi \
  --set persistence.storageClass=fast-ssd \
  --set metrics.kafka.enabled=true \
  --set metrics.jmx.enabled=true

# 3. Get bootstrap servers
export KAFKA_BOOTSTRAP=$(kubectl get svc kafka -n kafka -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'):9092
```

**注意事项**：
- ⚠️ 相较于 Strimzi/Confluent，其生产准备程度较低
- 声明式主题/用户管理功能有限
- 高级特性较少（不支持 MirrorMaker 2，RBAC 功能也较为简单）

## 生产环境最佳实践

### 1. 存储配置

**建议使用 SSD 支持的存储类来存储 Kafka 日志**：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs  # or pd.csi.storage.gke.io for GKE
parameters:
  type: gp3  # AWS EBS GP3 (or io2 for extreme performance)
  iopsPerGB: "50"
  throughput: "125"
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

**Kafka 的存储要求**：
- **每个 broker 的最低 IOPS**：3000+
- **每个 broker 的最低吞吐量**：125 MB/s
- **数据持久化**：设置 `deleteClaim: false`（避免在 Pod 删除时删除数据）

### 2. 资源限制

```yaml
resources:
  requests:
    memory: 4Gi
    cpu: "2"
  limits:
    memory: 8Gi
    cpu: "4"

jvmOptions:
  -Xms: 2048m  # Initial heap (50% of memory request)
  -Xmx: 4096m  # Max heap (50% of memory limit, leave room for OS cache)
```

**规模规划指南**：
- **小型环境（开发）**：2 个 CPU 核心，4 GiB 内存
- **中型环境（测试）**：4 个 CPU 核心，8 GiB 内存
- **大型环境（生产）**：8 个 CPU 核心，16 GiB 内存

### 3. 确保 Kubernetes 升级过程中的高可用性

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: kafka-pdb
  namespace: kafka
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: kafka
```

### 4. 资源亲和性配置

**将 Kafka broker 分布到不同的可用区**：

```yaml
spec:
  kafka:
    template:
      pod:
        affinity:
          podAntiAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              - labelSelector:
                  matchExpressions:
                    - key: strimzi.io/name
                      operator: In
                      values:
                        - my-kafka-cluster-kafka
                topologyKey: topology.kubernetes.io/zone
```

### 5. 网络策略

**限制对 Kafka broker 的访问**：

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: kafka-network-policy
  namespace: kafka
spec:
  podSelector:
    matchLabels:
      strimzi.io/name: my-kafka-cluster-kafka
  policyTypes:
    - Ingress
  ingress:
    - from:
      - podSelector:
          matchLabels:
            app: my-producer
      - podSelector:
          matchLabels:
            app: my-consumer
      ports:
      - protocol: TCP
        port: 9092
      - protocol: TCP
        port: 9093
```

## 监控集成

**使用 Prometheus 和 Grafana 进行监控**

**Strimzi** 内置了 Prometheus 指标导出功能**：

```yaml
# kafka-metrics-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kafka-metrics
  namespace: kafka
data:
  kafka-metrics-config.yml: |
    # Use JMX Exporter config from:
    # plugins/specweave-kafka/monitoring/prometheus/kafka-jmx-exporter.yml
    lowercaseOutputName: true
    lowercaseOutputLabelNames: true
    whitelistObjectNames:
      - "kafka.server:type=BrokerTopicMetrics,name=*"
      # ... (copy from kafka-jmx-exporter.yml)
```

```bash
# Apply metrics config
kubectl apply -f kafka-metrics-configmap.yaml

# Install Prometheus Operator (if not already installed)
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace

# Create PodMonitor for Kafka
kubectl apply -f - <<EOF
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: kafka-metrics
  namespace: kafka
spec:
  selector:
    matchLabels:
      strimzi.io/kind: Kafka
  podMetricsEndpoints:
    - port: tcp-prometheus
      interval: 30s
EOF

# Access Grafana dashboards (from kafka-observability skill)
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Open: http://localhost:3000
# Dashboards: Kafka Cluster Overview, Broker Metrics, Consumer Lag, Topic Metrics, JVM Metrics
```

## 常见问题及解决方法

### “Pod 处于 ‘Pending’ 状态”

**原因**：资源不足或未找到合适的存储类
**解决方法**：
```bash
# Check events
kubectl describe pod kafka-my-kafka-cluster-0 -n kafka

# Check storage class exists
kubectl get storageclass

# If missing, create fast-ssd storage class (see Production Best Practices above)
```

### “Kafka broker 在 10 分钟后仍未准备好”

**原因**：存储资源分配缓慢或资源限制过低
**解决方法**：
```bash
# Check broker logs
kubectl logs kafka-my-kafka-cluster-0 -n kafka

# Common issues:
# 1. Low IOPS on storage → Use GP3 or better
# 2. Low memory → Increase resources.requests.memory
# 3. KRaft quorum not formed → Check all brokers are running
```

### “无法从外部连接到 Kafka”

**原因**：未配置外部监听器
**解决方法**：
```yaml
# Add external listener (Strimzi)
spec:
  kafka:
    listeners:
      - name: external
        port: 9094
        type: loadbalancer
        tls: true
        authentication:
          type: tls

# Get external bootstrap server
kubectl get kafka my-kafka-cluster -n kafka -o jsonpath='{.status.listeners[?(@.name=="external")].bootstrapServers}'
```

## 扩展操作

### 水平扩展（增加 broker）

```bash
# Strimzi: Update KafkaNodePool replicas
kubectl patch kafkanodepool kafka-pool -n kafka --type='json' \
  -p='[{"op": "replace", "path": "/spec/replicas", "value": 5}]'

# Confluent: Update Kafka CR
kubectl patch kafka kafka -n confluent --type='json' \
  -p='[{"op": "replace", "path": "/spec/replicas", "value": 5}]'

# Wait for new brokers
kubectl rollout status statefulset/kafka-my-kafka-cluster-kafka -n kafka
```

### 垂直扩展（调整资源）

```bash
# Update resources in Kafka CR
kubectl patch kafka my-kafka-cluster -n kafka --type='json' \
  -p='[
    {"op": "replace", "path": "/spec/kafka/resources/requests/memory", "value": "8Gi"},
    {"op": "replace", "path": "/spec/kafka/resources/requests/cpu", "value": "4"}
  ]'

# Rolling restart will happen automatically
```

## 其他相关技能

- **kafka-iac-deployment**：Kubernetes 部署 Kafka 的另一种方案（可使用 Terraform 进行云管理）
- **kafka-observability**：用于配置 Prometheus 和 Grafana 监控面板以监控 Kafka 集群
- **kafka-architecture**：提供 Kafka 集群的规模规划和分区策略
- **kafka-cli-tools**：使用 kcat 工具测试 Kafka 集群

## 快速参考命令

```bash
# Strimzi
kubectl get kafka -n kafka                    # List Kafka clusters
kubectl get kafkatopics -n kafka              # List topics
kubectl get kafkausers -n kafka               # List users
kubectl logs kafka-my-kafka-cluster-0 -n kafka  # Check broker logs

# Confluent
kubectl get kafka -n confluent                # List Kafka clusters
kubectl get schemaregistry -n confluent       # List Schema Registry
kubectl get ksqldb -n confluent               # List ksqlDB

# Port-forward for testing
kubectl port-forward -n kafka svc/my-kafka-cluster-kafka-bootstrap 9092:9092
```

---

**Kubernetes 部署完成后，请执行以下操作**：
1. 使用 **kafka-observability** 工具验证 Prometheus 指标和 Grafana 监控面板
2. 使用 **kafka-cli-tools** 工具通过 kcat 测试 Kafka 集群
3. 将生产应用程序部署到 Kubernetes 上
4. 配置 GitOps 系统以实现声明式的主题和用户管理（例如使用 ArgoCD 或 Flux）