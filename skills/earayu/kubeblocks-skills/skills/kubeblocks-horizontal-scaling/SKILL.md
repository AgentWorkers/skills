---
name: kubeblocks-horizontal-scaling
metadata:
  version: "0.1.0"
description: 通过 `OpsRequest`，可以使用 KubeBlocks 水平扩展数据库集群的副本或分片。该功能支持向外扩展（添加副本）、向内扩展（删除副本）、退役特定实例，以及针对 Redis 集群和 MongoDB 分片拓扑进行分片调整。适用于用户需要添加或删除副本、节点、实例或分片的情况。**不适用于调整 CPU/内存配置（请参阅垂直扩展）或扩展磁盘空间（请参阅磁盘扩展）**。
---
# 水平扩展：添加或删除副本和分片

## 概述

水平扩展会改变 KubeBlocks 数据库集群中的副本（或分片）数量。KubeBlocks 支持向外扩展（添加副本）和向内扩展（删除副本），包括停用特定实例以及调整分片集群（如 Redis 集群、MongoDB 分片集群）的分片数量。

官方文档：https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/scale-a-mysql-cluster  
完整文档索引：https://kubeblocks.io/llms-full.txt

### 何时使用哪种扩展类型

- **水平扩展**：增加读取容量、提高高可用性（HA）或分布分片数据。每个新副本都会拥有独立的 CPU、内存和存储资源——这是通过添加独立的数据库实例来实现的扩展。
- **垂直扩展**：在负载以写操作为主或 CPU 资源受限的情况下，增加现有副本的 CPU/内存资源（如果瓶颈在于单主节点的写入吞吐量，添加副本将无济于事）。
- **磁盘空间扩展**：当存储空间不足时，增加磁盘空间——这与计算能力无关。

### 最小副本数量限制

基于共识的拓扑结构（如 MySQL 组复制、Kafka KRaft 控制器）要求副本数量为奇数（至少 3 个），因为 Raft/Paxos 协议需要多数票来选举领导者。如果有 3 个副本，系统可以容忍 1 个副本故障；如果有 2 个副本，则任何单个副本的故障都会导致投票失败，从而使集群无法正常运行。

## 预检查

在继续操作之前，请确认集群处于正常运行状态，并且没有其他操作正在执行：

```bash
# Cluster must be Running
kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.status.phase}'

# No pending OpsRequests
kubectl get opsrequest -n <namespace> -l app.kubernetes.io/instance=<cluster-name> --field-selector=status.phase!=Succeed
```

如果集群未处于“运行”状态或存在待处理的操作请求（OpsRequest），请等待其完成后再进行操作。

检查当前的副本数量：

```bash
kubectl get cluster <cluster-name> -n <namespace> -o yaml | grep replicas
```

## 工作流程

```
- [ ] Step 1: Check current replicas
- [ ] Step 2: Apply horizontal scaling OpsRequest
- [ ] Step 3: Monitor the operation
- [ ] Step 4: Verify new topology
```

## 第一步：检查当前副本数量

```bash
kubectl get cluster <cluster-name> -n <namespace> -o yaml | grep replicas
```

或者列出所有 Pod：

```bash
kubectl get pods -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

## 第二步：执行水平扩展操作

### 向外扩展（添加副本）

```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scaleout-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: HorizontalScaling
  horizontalScaling:
    - componentName: <component-name>
      scaleOut:
        replicaChanges: <number-to-add>
```

示例：向 MySQL 集群添加 2 个副本。

在应用更改之前，先进行模拟测试（dry-run）：

```bash
kubectl apply -f - --dry-run=server <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scaleout-mysql-cluster
  namespace: default
spec:
  clusterName: mysql-cluster
  type: HorizontalScaling
  horizontalScaling:
    - componentName: mysql
      scaleOut:
        replicaChanges: 2
EOF
```

如果模拟测试报告错误，请修复相关 YAML 文件后再继续操作。

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scaleout-mysql-cluster
  namespace: default
spec:
  clusterName: mysql-cluster
  type: HorizontalScaling
  horizontalScaling:
    - componentName: mysql
      scaleOut:
        replicaChanges: 2
EOF
```

### 向内扩展（删除副本）

```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scalein-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: HorizontalScaling
  horizontalScaling:
    - componentName: <component-name>
      scaleIn:
        replicaChanges: <number-to-remove>
```

示例：从 PostgreSQL 集群中删除 1 个副本。

在应用更改之前，先进行模拟测试（dry-run）：

```bash
kubectl apply -f - --dry-run=server <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scalein-pg-cluster
  namespace: default
spec:
  clusterName: pg-cluster
  type: HorizontalScaling
  horizontalScaling:
    - componentName: postgresql
      scaleIn:
        replicaChanges: 1
EOF
```

如果模拟测试报告错误，请修复相关 YAML 文件后再继续操作。

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scalein-pg-cluster
  namespace: default
spec:
  clusterName: pg-cluster
  type: HorizontalScaling
  horizontalScaling:
    - componentName: postgresql
      scaleIn:
        replicaChanges: 1
EOF
```

### 停用特定实例（按名称进行扩展）

如果要删除某个特定的 Pod 而不是最后一个 Pod，可以使用 `onlineInstancesToOffline` 命令：

```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scalein-specific-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: HorizontalScaling
  horizontalScaling:
    - componentName: <component-name>
      scaleIn:
        replicaChanges: 1
        onlineInstancesToOffline:
          - "<pod-name>"
```

示例：停用某个特定的 MongoDB 副本。

在应用更改之前，先进行模拟测试（dry-run）：

```bash
kubectl apply -f - --dry-run=server <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scalein-specific-mongo
  namespace: default
spec:
  clusterName: mongo-cluster
  type: HorizontalScaling
  horizontalScaling:
    - componentName: mongodb
      scaleIn:
        replicaChanges: 1
        onlineInstancesToOffline:
          - "mongo-cluster-mongodb-2"
EOF
```

如果模拟测试报告错误，请修复相关 YAML 文件后再继续操作。

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scalein-specific-mongo
  namespace: default
spec:
  clusterName: mongo-cluster
  type: HorizontalScaling
  horizontalScaling:
    - componentName: mongodb
      scaleIn:
        replicaChanges: 1
        onlineInstancesToOffline:
          - "mongo-cluster-mongodb-2"
EOF
```

### 分片扩展（Redis 集群 / MongoDB 分片集群）

对于分片集群，可以使用 `shards` 字段来调整分片组的数量：

```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scale-shards-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: HorizontalScaling
  horizontalScaling:
    - componentName: <component-name>
      scaleOut:
        replicaChanges: <shards-to-add>
```

> **注意：** 对于 Redis 集群和 MongoDB 分片集群，组件中的每个“副本”实际上代表一个分片组。增加副本数量会自动触发数据重新平衡。

### 使用 `kubectl Patch` 的替代方法

对于简单的副本数量调整，也可以直接对集群进行更新：

```bash
kubectl patch cluster <cluster-name> -n <namespace> \
  --type merge -p '{"spec":{"componentSpecs":[{"name":"<component-name>","replicas":<new-total>}]}}'
```

示例：将 MySQL 的副本数量设置为 5：

```bash
kubectl patch cluster mysql-cluster -n default \
  --type merge -p '{"spec":{"componentSpecs":[{"name":"mysql","replicas":5}]}}'
```

## 第三步：监控操作进度

```bash
kubectl get ops -n <namespace> -w
```

> **成功条件**：`.status.phase` = `Succeed`  
> **通常完成时间**：1-5 分钟  
> **如果操作超时（超过 10 分钟）**：使用 `kubectl describe ops <ops-name> -n <namespace>` 命令查看操作状态。

观察 Pod 的运行状态：

```bash
kubectl get pods -n <namespace> -l app.kubernetes.io/instance=<cluster-name> -w
```

> **成功条件**：`.status.phase` = `Running`  
> **通常完成时间**：1-5 分钟  
> **如果操作超时（超过 10 分钟）**：使用 `kubectl describe pod <pod-name> -n <namespace>` 命令查看 Pod 的运行状态。

## 第四步：验证新的集群拓扑结构

```bash
kubectl get cluster <cluster-name> -n <namespace> -o yaml | grep replicas
```

确认副本数量是否已正确调整：

```bash
kubectl get pods -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

## 故障排除

**扩展操作卡在“Pending”状态**：
- 可能是由于节点资源不足。请使用 `kubectl describe pod <pod-name> -n <namespace>` 命令进行检查。
- 可能是由于持久化卷（PV）数量不足。请检查 `kubectl get sc` 命令以确认 StorageClass 的配置。

**扩展操作失败**：
- 可能是因为副本数量低于拓扑结构所要求的最低限制（例如，基于 Raft 的 MySQL 集群至少需要 3 个副本）。
- 请查看 `kubectl describe ops <ops-name> -n <namespace>` 命令以获取操作日志。

**分片扩展后的数据重新平衡**：
- 对于 Redis 集群，数据重新分片会自动完成。可以使用 `redis-cli --cluster check` 命令进行监控。
- 对于 MongoDB，数据重新分配可能需要一些时间（尤其是对于大型数据集）。

有关通用安全操作规范（如模拟测试、状态确认、生产环境保护措施），请参阅 [safety-patterns.md](../../references/safety-patterns.md)。

## 额外资源

有关引擎特定的扩展行为、最小副本数量限制、副本与分片的区别以及实例停用策略，请参阅 [reference.md](references/reference.md)。