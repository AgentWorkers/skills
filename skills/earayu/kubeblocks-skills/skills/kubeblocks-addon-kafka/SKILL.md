---
name: kubeblocks-addon-kafka
metadata:
  version: "0.1.0"
description: 在 KubeBlocks 上部署和管理 Apache Kafka 集群，并提供拓扑结构选择的指导。支持两种模式：组合模式（broker 和 controller 位于同一节点）和分离模式（broker 和 controller 分别位于不同的节点），同时支持可选的监控功能。当用户需要使用 Kafka、消息队列、事件流处理或消息代理时，可参考本文档。文档内容包含拓扑结构对比、最佳实践配置以及连接方法。如需创建通用集群（适用于所有引擎），请参阅 `kubeblocks-create-cluster`；对于后续的操作（如扩展集群等），请使用相应的操作技能。
---
# 在 KubeBlocks 上部署 Kafka

## 概述

使用 KubeBlocks 在 Kubernetes 上部署 Apache Kafka 集群。支持组合模式（broker 和 controller 在同一个进程中）和分离模式（独立的 broker 和 controller 节点），并可通过 exporter 进行可选的监控。

官方文档：https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-kafka/cluster-management/create-a-kafka-cluster  
完整文档索引：https://kubeblocks.io/llms-full.txt  

## 先决条件

- 已经安装了 KubeBlocks 的运行中的 Kubernetes 集群（请参阅 [install-kubeblocks](../kubeblocks-install/SKILL.md)）  
- 必须启用 Kafka 插件：  

```bash
# Check if kafka addon is installed
helm list -n kb-system | grep kafka

# Install if missing
helm install kb-addon-kafka kubeblocks/kafka --namespace kb-system --version 1.0.0
```  

## 可用的拓扑结构  

| 拓扑结构 | 值 | 组件 | 使用场景 |  
|---|---|---|---|  
| 组合模式 | `combined` | kafka-combine | 开发/测试环境，broker 和 controller 在同一个进程中 |  
| 组合模式 + 监控 | `combined_monitor` | kafka-combine + exporter | 结合了监控功能 |  
| 分离模式 | `separated` | kafka-broker + kafka-controller | 生产环境，角色分离 |  
| 分离模式 + 监控 | `separated_monitor` | kafka-broker + kafka-controller + exporter | 生产环境并支持监控 |  

Kafka 使用 KRaft 协议（无需 ZooKeeper）。控制器通过 Raft 协议管理集群元数据。  

## 支持的版本  

| 版本 | serviceVersion |  
|---|---|  
| Kafka 3.3 | `3.3.2` |  

## 工作流程  

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster (choose topology)
- [ ] Step 4: Wait for cluster to be ready
- [ ] Step 5: Produce and consume messages
```  

## 第 1 步：确保插件已安装  

```bash
helm list -n kb-system | grep kafka
```  

如果插件未安装：  
```bash
helm install kb-addon-kafka kubeblocks/kafka --namespace kb-system --version 1.0.0
```  

## 第 2 步：创建命名空间  

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```  

## 第 3 步：创建集群  

### 组合模式（开发/测试环境）  

Broker 和 controller 在同一个进程中运行。这种方式较为简单，但不推荐用于生产环境：  
```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: kafka-cluster
  namespace: demo
spec:
  clusterDef: kafka
  topology: combined
  terminationPolicy: Delete
  componentSpecs:
    - name: kafka-combine
      serviceVersion: "3.3.2"
      replicas: 3
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      env:
        - name: KB_KAFKA_BROKER_HEAP
          value: "-Xmx256m -Xms256m"
        - name: KB_KAFKA_CONTROLLER_HEAP
          value: "-Xmx256m -Xms256m"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
        - name: metadata
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 5Gi}}
```  

### 分离模式（生产环境）  

使用独立的 broker 和 controller 节点，以实现更好的隔离性和可扩展性：  
```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: kafka-separated
  namespace: demo
spec:
  clusterDef: kafka
  topology: separated
  terminationPolicy: Delete
  componentSpecs:
    - name: kafka-broker
      serviceVersion: "3.3.2"
      replicas: 3
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      env:
        - name: KB_KAFKA_BROKER_HEAP
          value: "-Xmx256m -Xms256m"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
        - name: metadata
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 5Gi}}
    - name: kafka-controller
      serviceVersion: "3.3.2"
      replicas: 3
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      env:
        - name: KB_KAFKA_CONTROLLER_HEAP
          value: "-Xmx256m -Xms256m"
      volumeClaimTemplates:
        - name: metadata
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 5Gi}}
```  

**关键点：**  
- Broker 需要 `data` 和 `metadata` 两个卷  
- Controller 仅需要 `metadata` 卷（不存储消息数据）  
- 需要 3 个 controller 复制副本以保证 Raft 共识  

### 带监控的分离模式  

添加一个 exporter 组件以生成兼容 Prometheus 的监控指标：  
```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: kafka-monitored
  namespace: demo
spec:
  clusterDef: kafka
  topology: separated_monitor
  terminationPolicy: Delete
  componentSpecs:
    - name: kafka-broker
      serviceVersion: "3.3.2"
      replicas: 3
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      env:
        - name: KB_KAFKA_BROKER_HEAP
          value: "-Xmx256m -Xms256m"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
        - name: metadata
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 5Gi}}
    - name: kafka-controller
      serviceVersion: "3.3.2"
      replicas: 3
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      env:
        - name: KB_KAFKA_CONTROLLER_HEAP
          value: "-Xmx256m -Xms256m"
      volumeClaimTemplates:
        - name: metadata
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 5Gi}}
    - name: kafka-exporter
      replicas: 1
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
```  

## 环境变量  

可以通过组件规范中的环境变量来调整 Kafka 的配置：  

| 变量 | 描述 | 示例 |  
|---|---|---|  
| `KB_KAFKA_BROKER_HEAP` | Broker 的 JVM 堆内存设置 | `-Xmx512m -Xms512m` |  
| `KB_KAFKA_CONTROLLER_heap` | Controller 的 JVM 堆内存设置 | `-Xmx256m -Xms256m` |  
| `KB_KAFKA_ENABLE_SASL` | 启用 SASL 认证 | `true` |  
| `KB_KAFKA_PUBLIC_ACCESS` | 启用外部访问模式 | `true` |  

## 第 4 步：等待集群准备好  

```bash
kubectl -n demo get cluster <cluster-name> -w
```  

等待 `STATUS` 显示为 `Running`。Kafka 集群通常需要 2-4 分钟才能启动完成。  
检查各个 Pod 的状态：  
```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=<cluster-name>
```  

## 第 5 步：生产与消费消息  

### 创建主题  

```bash
kubectl -n demo exec -it kafka-cluster-kafka-combine-0 -- \
  kafka-topics.sh --bootstrap-server localhost:9092 --create --topic test-topic --partitions 3 --replication-factor 1
```  

### 生产消息  

```bash
kubectl -n demo exec -it kafka-cluster-kafka-combine-0 -- \
  kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test-topic
```  

### 消费消息  

```bash
kubectl -n demo exec -it kafka-cluster-kafka-combine-0 -- \
  kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test-topic --from-beginning
```  

### 对于分离模式  

请将 `pod_name` 替换为实际的 broker Pod 名称：  
```bash
kubectl -n demo exec -it kafka-separated-kafka-broker-0 -- \
  kafka-topics.sh --bootstrap-server localhost:9092 --list
```  

## 故障排除  

**集群创建失败：**  
```bash
kubectl -n demo describe cluster <cluster-name>
kubectl -n demo get events --sort-by='.lastTimestamp'
```  

**Broker 无法启动：**  
```bash
kubectl -n demo logs <broker-pod>
```  

**Controller 共识问题：**  
- 确保有 3 个 controller 复制副本以保证 Raft 共识  
- 检查 controller 的日志以查找选举错误  

**内存不足：**  
- 通过 `KB_KAFKA_BROKER_heap` / `KB_KAFKA_controller_heap` 环境变量调整堆内存大小  
- 确保容器的内存限制大于堆内存大小  

## 日常操作  

| 操作 | 所需技能 | 外部文档 |  
|---|---|---|  
| 停止/启动/重启集群 | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-kafka/cluster-management/stop-start-restart-a-kafka-cluster) |  
| 调整 CPU/内存资源 | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-kafka/cluster-management/scale-for-a-kafka-cluster) |  
| 增加/减少副本数量 | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-kafka/cluster-management/scale-for-a-kafka-cluster) |  
| 扩展存储空间 | [volume-expansion](../kubeblocks-volume-expansion/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-kafka/cluster-management/expand-volume-of-a-kafka-cluster) |  
| 修改参数 | [reconfigure-parameters](../kubeblocks-reconfigure-parameters/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-kafka/configuration/configure-cluster-parameters) |  

## 安全最佳实践  

在正式部署前，请遵循 [safety-patterns.md](../../references/safety-patterns.md) 中的建议，进行模拟测试；部署后确认集群状态；并在删除集群前执行必要的检查。  

## 下一步操作  

- 如需查看所有拓扑结构（组合模式、带监控的分离模式以及生产环境下的配置示例）、环境变量参考信息以及组件/卷的详细信息，请参阅 [reference.md](references/reference.md)。