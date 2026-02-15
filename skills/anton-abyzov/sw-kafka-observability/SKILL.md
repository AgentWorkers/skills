---
name: kafka-observability
description: Kafka监控与可观测性专家，专注于使用Prometheus、Grafana和JMX指标进行Kafka的监控工作。适用于设置Kafka监控机制、配置警报规则或构建性能仪表板等场景。
---

# Kafka 监控与可观测性

本文档提供了使用 Prometheus 和 Grafana 实现 Apache Kafka 全面监控与可观测性的专家指导。

## 适用场景

当您需要以下帮助时，请参考本文档：
- **监控设置**：配置 Kafka 监控、配置 Prometheus 以收集 Kafka 数据、创建 Grafana 仪表板
- **指标收集**：从 Kafka 收集 JMX 指标、将 Kafka 指标导出到 Prometheus
- **警报设置**：设置 Kafka 相关的警报规则（例如，当分区复制数量不足或关键指标异常时触发警报）
- **故障排除**：监控 Kafka 性能、跟踪消费者延迟、检查 broker 的健康状况

## 我所掌握的知识

### 可用的监控组件

本插件提供了完整的监控解决方案：

#### 1. **Prometheus JMX 导出器配置**
- **位置**：`plugins/specweave-kafka/monitoring/prometheus/kafka-jmx-exporter.yml`
- **功能**：将 Kafka 的 JMX 指标导出为 Prometheus 可识别的格式
- **导出的指标**：
  - Broker 的主题相关指标（发送/接收的字节数、消息数量、请求速率）
  - 复制管理器的相关指标（复制数量不足的分区、ISR 的变化）
  - 控制器的相关指标（活跃的控制器、离线分区、领导者选举情况）
  - 请求相关的指标（发送/获取操作的延迟）
  - 日志相关的指标（日志刷新频率、刷新延迟）
  - JVM 相关指标（堆内存使用情况、垃圾回收次数、线程数）

#### 2. **Grafana 仪表板**（共 5 个仪表板）
- **位置**：`plugins/specweave-kafka/monitoring/grafana/dashboards/`
- **仪表板内容**：
  1. `kafka-cluster-overview.json`：集群整体健康状况和吞吐量
  2. `kafka-broker-metrics.json`：每个 broker 的性能指标
  3. `kafka-consumer-lag.json`：消费者延迟监控
  4. `kafka-topic-metrics.json`：主题级别的指标
  5. `kafka-jvm-metrics.json`：JVM 的健康状况（堆内存使用情况、垃圾回收情况）

#### 3. **Grafana 配置**  
- **位置**：`plugins/specweave-kafka/monitoring/grafana/provisioning/`
- **配置文件**：
  - `dashboards/kafka.yml`：仪表板配置文件
  - `datasources/prometheus.yml`：Prometheus 数据源配置文件

## 设置流程 1：JMX 导出器（独立运行的 Kafka）

适用于在虚拟机或裸机上运行的 Kafka（非 Kubernetes 环境）

### 步骤 1：下载 JMX Prometheus 代理

```bash
# Download JMX Prometheus agent JAR
cd /opt
wget https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.20.0/jmx_prometheus_javaagent-0.20.0.jar

# Copy JMX Exporter config
cp plugins/specweave-kafka/monitoring/prometheus/kafka-jmx-exporter.yml /opt/kafka-jmx-exporter.yml
```

### 步骤 2：配置 Kafka Broker

在 Kafka 的启动脚本中添加 JMX 导出器：

```bash
# Edit Kafka startup (e.g., /etc/systemd/system/kafka.service)
[Service]
Environment="KAFKA_OPTS=-javaagent:/opt/jmx_prometheus_javaagent-0.20.0.jar=7071:/opt/kafka-jmx-exporter.yml"
```

或者将配置添加到 `kafka-server-start.sh` 文件中：

```bash
export KAFKA_OPTS="-javaagent:/opt/jmx_prometheus_javaagent-0.20.0.jar=7071:/opt/kafka-jmx-exporter.yml"
```

### 步骤 3：重启 Kafka 并验证配置

```bash
# Restart Kafka broker
sudo systemctl restart kafka

# Verify JMX exporter is running (port 7071)
curl localhost:7071/metrics | grep kafka_server

# Expected output: kafka_server_broker_topic_metrics_bytesin_total{...} 12345
```

### 步骤 4：配置 Prometheus 的数据采集

在 Prometheus 配置文件中添加 Kafka broker 的数据源：

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'kafka'
    static_configs:
      - targets:
        - 'kafka-broker-1:7071'
        - 'kafka-broker-2:7071'
        - 'kafka-broker-3:7071'
    scrape_interval: 30s
```

```bash
# Reload Prometheus
sudo systemctl reload prometheus

# OR send SIGHUP
kill -HUP $(pidof prometheus)

# Verify scraping
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | select(.job=="kafka")'
```

## 设置流程 2：使用 Strimzi（Kubernetes 环境）

适用于在 Kubernetes 上运行 Kafka 且使用了 Strimzi Operator 的场景

### 步骤 1：创建 JMX 导出器的 ConfigMap

```bash
# Create ConfigMap from JMX exporter config
kubectl create configmap kafka-metrics \
  --from-file=kafka-metrics-config.yml=plugins/specweave-kafka/monitoring/prometheus/kafka-jmx-exporter.yml \
  -n kafka
```

### 步骤 2：配置 Kafka 的 ConfigMap（包含指标数据）

```yaml
# kafka-cluster.yaml (add metricsConfig section)
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-kafka-cluster
  namespace: kafka
spec:
  kafka:
    version: 3.7.0
    replicas: 3

    # ... other config ...

    metricsConfig:
      type: jmxPrometheusExporter
      valueFrom:
        configMapKeyRef:
          name: kafka-metrics
          key: kafka-metrics-config.yml
```

### 步骤 3：安装 Prometheus Operator（如果尚未安装）

```bash
# Add Prometheus Community Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install kube-prometheus-stack (Prometheus + Grafana + Alertmanager)
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
  --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false
```

### 步骤 4：为 Kafka 创建 PodMonitor

```yaml
# kafka-podmonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: kafka-metrics
  namespace: kafka
  labels:
    app: strimzi
spec:
  selector:
    matchLabels:
      strimzi.io/kind: Kafka
  podMetricsEndpoints:
    - port: tcp-prometheus
      interval: 30s
```

```bash
# Apply PodMonitor
kubectl apply -f kafka-podmonitor.yaml

# Verify Prometheus is scraping Kafka
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
# Open: http://localhost:9090/targets
# Should see kafka-metrics/* targets
```

## 设置流程 3：配置 Grafana 仪表板

### 使用 Docker Compose 进行安装（本地开发环境）

如果使用 Docker Compose 进行本地开发：

```yaml
# docker-compose.yml (add to existing Kafka setup)
version: '3.8'
services:
  # ... Kafka services ...

  prometheus:
    image: prom/prometheus:v2.48.0
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:10.2.0
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards
      - grafana-data:/var/lib/grafana

volumes:
  prometheus-data:
  grafana-data:
```

```bash
# Start monitoring stack
docker-compose up -d prometheus grafana

# Access Grafana
# URL: http://localhost:3000
# Username: admin
# Password: admin
```

### 使用 Kubernetes 进行安装

如果使用 kube-prometheus-stack，仪表板会自动配置：

```bash
# Create ConfigMaps for each dashboard
for dashboard in plugins/specweave-kafka/monitoring/grafana/dashboards/*.json; do
  name=$(basename "$dashboard" .json)
  kubectl create configmap "kafka-dashboard-$name" \
    --from-file="$dashboard" \
    -n monitoring \
    --dry-run=client -o yaml | kubectl apply -f -
done

# Label ConfigMaps for Grafana auto-discovery
kubectl label configmap -n monitoring kafka-dashboard-* grafana_dashboard=1

# Grafana will auto-import dashboards (wait 30-60 seconds)

# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# URL: http://localhost:3000
# Username: admin
# Password: prom-operator (default kube-prometheus-stack password)
```

### 手动导入仪表板

如果自动配置失败，可以手动导入仪表板配置：

```bash
# 1. Access Grafana UI
# 2. Go to: Dashboards → Import
# 3. Upload JSON files from:
#    plugins/specweave-kafka/monitoring/grafana/dashboards/

# Or use Grafana API
for dashboard in plugins/specweave-kafka/monitoring/grafana/dashboards/*.json; do
  curl -X POST http://admin:admin@localhost:3000/api/dashboards/db \
    -H "Content-Type: application/json" \
    -d @"$dashboard"
done
```

## 仪表板介绍

### 1. **Kafka 集群概览**（`kafka-cluster-overview.json`）

**功能**：展示集群的整体健康状况

**关键指标**：
- 活跃控制器的数量（应为 1）
- 复制数量不足的分区数量（应为 0）⚠️ 严重问题
- 离线分区数量（应为 0）⚠️ 严重问题
- 未完成的领导者选举次数（应为 0）
- 集群吞吐量（每秒发送/接收的字节数）
- 请求速率（每秒的发送/获取请求数量）
- ISR（In-Sync Replicas）的变化情况
- 领导者选举频率

**使用场景**：检查集群的整体健康状况

### 2. **Kafka Broker 指标**（`kafka-broker-metrics.json`）

**功能**：展示每个 broker 的性能指标

**关键指标**：
- Broker 的 CPU 使用率
- Broker 的堆内存使用情况
- Broker 的网络吞吐量（发送/接收的字节数）
- 请求处理器的空闲百分比（低值表示 CPU 利用率较低）
- 文件描述符的使用情况（打开的文件描述符数与最大值对比）
- 日志刷新延迟（50% 和 99% 分位数）
- JVM 的垃圾回收次数和时间

**使用场景**：排查 broker 的性能问题

### 3. **Kafka 消费者延迟**（`kafka-consumer-lag.json`）

**功能**：监控消费者的延迟情况

**关键指标**：
- 每个主题/分区的消费者延迟
- 每个消费者组的总延迟
- 偏移量提交频率
- 当前消费者的偏移量
- 消费者组的成员信息

**使用场景**：排查消费者性能缓慢或延迟突然增加的问题

### 4. **Kafka 主题指标**（`kafka-topic-metrics.json`）

**功能**：展示主题级别的指标

**关键指标**：
- 每个主题产生的消息数量
- 每个主题的发送/接收字节数
- 每个主题的分区数量
- 复制因子
- 同步分区的数量
- 每个分区的日志大小
- 当前分区的偏移量
- 分区的领导者分布情况

**使用场景**：分析主题的吞吐量和热点数据

### 5. **Kafka JVM 指标**（`kafka-jvm-metrics.json`）

**功能**：监控 JVM 的健康状况

**关键指标**：
- 堆内存的使用情况（实际使用量与最大值对比）
- 堆内存利用率
- 垃圾回收的频率（每次回收操作的次数）
- 垃圾回收所需的时间（毫秒）
- JVM 的线程数量
- 堆内存的分配情况（年轻代、老年代、存活代）
- 堆内存之外的内存使用情况（元空间、代码缓存）
- 垃圾回收暂停的时间百分比（50% 和 99% 分位数）

**使用场景**：排查内存泄漏或垃圾回收暂停的问题

## 重要警报配置

为关键 Kafka 指标创建 Prometheus 警报规则：

```yaml
# kafka-alerts.yml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: kafka-alerts
  namespace: monitoring
spec:
  groups:
    - name: kafka.rules
      interval: 30s
      rules:
        # CRITICAL: Under-Replicated Partitions
        - alert: KafkaUnderReplicatedPartitions
          expr: sum(kafka_server_replica_manager_under_replicated_partitions) > 0
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "Kafka has under-replicated partitions"
            description: "{{ $value }} partitions are under-replicated. Data loss risk!"

        # CRITICAL: Offline Partitions
        - alert: KafkaOfflinePartitions
          expr: kafka_controller_offline_partitions_count > 0
          for: 1m
          labels:
            severity: critical
          annotations:
            summary: "Kafka has offline partitions"
            description: "{{ $value }} partitions are offline. Service degradation!"

        # CRITICAL: No Active Controller
        - alert: KafkaNoActiveController
          expr: kafka_controller_active_controller_count == 0
          for: 1m
          labels:
            severity: critical
          annotations:
            summary: "No active Kafka controller"
            description: "Cluster has no active controller. Cannot perform administrative operations!"

        # WARNING: High Consumer Lag
        - alert: KafkaConsumerLagHigh
          expr: sum by (consumergroup) (kafka_consumergroup_lag) > 10000
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: "Consumer group {{ $labels.consumergroup }} has high lag"
            description: "Lag is {{ $value }} messages. Consumers may be slow."

        # WARNING: High CPU Usage
        - alert: KafkaBrokerHighCPU
          expr: os_process_cpu_load{job="kafka"} > 0.8
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Broker {{ $labels.instance }} has high CPU usage"
            description: "CPU usage is {{ $value | humanizePercentage }}. Consider scaling."

        # WARNING: Low Heap Memory
        - alert: KafkaBrokerLowHeapMemory
          expr: jvm_memory_heap_used_bytes{job="kafka"} / jvm_memory_heap_max_bytes{job="kafka"} > 0.9
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Broker {{ $labels.instance }} has low heap memory"
            description: "Heap usage is {{ $value | humanizePercentage }}. Risk of OOM!"

        # WARNING: High GC Time
        - alert: KafkaBrokerHighGCTime
          expr: rate(jvm_gc_collection_time_ms_total{job="kafka"}[5m]) > 500
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Broker {{ $labels.instance }} spending too much time in GC"
            description: "GC time is {{ $value }}ms/sec. Application pauses likely."
```

```bash
# Apply alerts (Kubernetes)
kubectl apply -f kafka-alerts.yml

# Verify alerts loaded
kubectl get prometheusrules -n monitoring
```

## 常见问题及解决方法

### “Prometheus 无法收集 Kafka 指标”

**症状**：Prometheus 中没有 Kafka 的指标数据

**解决方法**：
```bash
# 1. Verify JMX exporter is running
curl http://kafka-broker:7071/metrics

# 2. Check Prometheus targets
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | select(.job=="kafka")'

# 3. Check Prometheus logs
kubectl logs -n monitoring prometheus-kube-prometheus-prometheus-0

# Common issues:
# - Firewall blocking port 7071
# - Incorrect scrape config
# - Kafka broker not running
```

### “Grafana 仪表板无法显示数据”

**症状**：仪表板显示“无数据”

**解决方法**：
```bash
# 1. Verify Prometheus datasource
# Grafana UI → Configuration → Data Sources → Prometheus → Test

# 2. Check if Kafka metrics exist in Prometheus
# Prometheus UI → Graph → Enter: kafka_server_broker_topic_metrics_bytesin_total

# 3. Verify dashboard queries match your Prometheus job name
# Dashboard panels use job="kafka" by default
# If your job name is different, update dashboard JSON
```

### “消费者延迟指标缺失”

**症状**：消费者延迟相关的仪表板为空

**解决方法**：消费者延迟指标需要通过单独的 Kafka 导出器来收集（与 JMX 导出器分开配置）：

```bash
# Install Kafka Exporter (Kubernetes)
helm install kafka-exporter prometheus-community/prometheus-kafka-exporter \
  --namespace monitoring \
  --set kafkaServer={kafka-bootstrap:9092}

# Or run as Docker container
docker run -d -p 9308:9308 \
  danielqsj/kafka-exporter \
  --kafka.server=kafka:9092 \
  --web.listen-address=:9308

# Add to Prometheus scrape config
scrape_configs:
  - job_name: 'kafka-exporter'
    static_configs:
      - targets: ['kafka-exporter:9308']
```

## 与其他工具的集成

- **kafka-iac-deployment**：在 Terraform 部署过程中配置监控
- **kafka-kubernetes**：为使用 Strimzi 的 Kafka 配置监控
- **kafka-architecture**：利用集群规模指标进行容量规划
- **kafka-cli-tools**：使用 kcat 生成测试流量并验证指标数据

## 快速参考命令

```bash
# Check JMX exporter metrics
curl http://localhost:7071/metrics | grep -E "(kafka_server|kafka_controller)"

# Prometheus query examples
curl -g 'http://localhost:9090/api/v1/query?query=kafka_server_replica_manager_under_replicated_partitions'

# Grafana dashboard export
curl http://admin:admin@localhost:3000/api/dashboards/uid/kafka-cluster-overview | jq .dashboard > backup.json

# Reload Prometheus config
kill -HUP $(pidof prometheus)

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | select(.job=="kafka")'
```

---

**监控设置完成后，请执行以下操作**：
1. 查看所有 5 个 Grafana 仪表板，熟悉各项指标
2. 设置警报通知（Slack、PagerDuty、电子邮件）
3. 为关键警报（如分区复制数量不足、 broker 离线、控制器缺失）创建自动化处理流程
4. 监控 7 天以获取基准数据
5. 根据 JVM 指标调整相关配置