---
name: kubeblocks-addon-milvus
metadata:
  version: "0.1.0"
description: 在 KubeBlocks 上部署和管理 Milvus 向量数据库集群，以支持 AI/ML 工作负载。该方案支持嵌入式相似性搜索功能，以及独立（开发/测试）和集群（生产）两种拓扑结构。当用户提到 Milvus、向量数据库、AI 嵌入技术或相似性搜索时，或者明确需要创建 Milvus 集群时，可使用该方案。文档提供了拓扑结构对比、连接方法以及后续运维操作（如扩展、服务暴露等）的详细信息。关于跨所有引擎创建通用集群的步骤，请参阅 `kubeblocks-create-cluster`；对于具体的运维操作，请使用相应的技能文档。
---
# 在 KubeBlocks 上部署 Milvus

## 概述

使用 KubeBlocks 在 Kubernetes 上部署 Milvus 向量数据库集群。Milvus 支持嵌入式相似性搜索和 AI 应用程序。它支持独立模式（单节点，开发/测试）和集群模式（分布式，生产环境），并使用 etcd 和 MinIO 作为存储方案，同时支持可选的 Pulsar/Kafka 用于日志存储。

官方文档：https://kubeblocks.io/docs/preview/kubeblocks-for-milvus/01-overview  
快速入门：https://kubeblocks.io/docs/preview/kubeblocks-for-milvus/02-quickstart

## 先决条件

- 已经安装了 KubeBlocks 的运行中的 Kubernetes 集群（请参阅 [install-kubeblocks](../kubeblocks-install/SKILL.md)）  
- 必须启用 Milvus 插件：

```bash
# Check if milvus addon is installed
helm list -n kb-system | grep milvus

# Install if missing
helm install kb-addon-milvus kubeblocks/milvus --namespace kb-system --version 1.0.0
```

## 可用的拓扑结构

| 拓扑结构 | 值 | 组件 | 使用场景 |
|---|---|---|---|
| 独立模式 | `standalone` | milvus + etcd + minio | 开发/测试，单节点 |
| 集群模式 | `cluster` | milvus-proxy, milvus-mixcoord, milvus-datanode, milvus-indexnode, milvus-querynode + etcd + minio (+ pulsar/kafka) | 生产环境，分布式 |

默认端口：19530（gRPC），9091（指标）。

## 支持的版本

| 版本 | serviceVersion |
|---|---|
| Milvus 2.3 | `v2.3.2` |
| Milvus 2.5 | `v2.5.13` |

可用版本列表：`kubectl get cmpv milvus`

## 工作流程

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster (choose topology)
- [ ] Step 4: Dry-run, then apply
- [ ] Step 5: Watch until Running, verify success
- [ ] Step 6: Connect and verify
```

## 第一步：确保插件已安装

```bash
helm list -n kb-system | grep milvus
```

如果未找到插件，请执行以下操作：

```bash
helm install kb-addon-milvus kubeblocks/milvus --namespace kb-system --version 1.0.0
```

## 第二步：创建命名空间

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```

## 第三步：创建集群

### 独立模式（开发/测试）

单节点部署，etcd 和 MinIO 共存。适用于开发和测试环境：

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: milvus-standalone
  namespace: demo
spec:
  clusterDef: milvus
  topology: standalone
  terminationPolicy: Delete
  componentSpecs:
    - name: etcd
      replicas: 1
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
    - name: minio
      replicas: 1
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
    - name: milvus
      replicas: 1
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
```

### 集群模式（生产环境）

分布式部署，包括代理节点（milvus-proxy）、协调节点（milvus-mixcoord）、数据节点（milvus-datanode）和查询节点（milvus-querynode）。需要预先创建 etcd 和 minio 集群；Pulsar/Kafka 可选。详细配置请参阅 [集群拓扑文档](https://kubeblocks.io/docs/preview/kubeblocks-for-milvus/03-topologies/02-cluster)。

关键组件：`milvus-proxy`（访问控制），`milvus-mixcoord`（协调），`milvus-datanode`，`milvus-indexnode`，`milvus-querynode`（计算），以及 `etcd` 和 `minio`。集群模式通过 `serviceRef` 引用外部 etcd、minio 和 Pulsar/Kafka 集群。

## 第四步：进行预测试并应用配置

在应用配置之前，先运行服务器端的预测试，以检查 RBAC、Webhook 或数据库模式配置是否有错误：

```bash
kubectl apply -f cluster.yaml --dry-run=server
```

如果预测试成功，则可以应用配置：

```bash
kubectl apply -f cluster.yaml
```

## 第五步：等待集群准备就绪

```bash
kubectl -n demo get cluster <cluster-name> -w
```

**成功条件：** `STATUS` 显示为 `Running`。通常需要 2–5 分钟。如果 10 分钟后集群仍处于创建/更新状态，请检查相关问题（参见 [安全最佳实践](../../references/safety-patterns.md)）。

检查 Pod 的运行状态：

```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=<cluster-name>
```

## 第六步：连接

### 端口转发（独立模式）

```bash
kubectl port-forward pod/<cluster-name>-milvus-0 -n demo 19530:19530
```

通过 `localhost:19530` 连接（gRPC）。对于集群模式，需要将端口转发到代理 Pod。

### 使用 Python 进行验证

```python
from pymilvus import connections
connections.connect(host="localhost", port=19530)
```

## 故障排除

**集群创建失败：**
```bash
kubectl -n demo describe cluster <cluster-name>
kubectl -n demo get events --sort-by='.lastTimestamp'
```

**Milvus Pod 无法启动：**
```bash
kubectl -n demo logs <milvus-pod>
```

**etcd 或 minio 依赖问题：**
- 确保在启动 Milvus 之前，etcd 和 minio Pod 已经运行正常。
- 检查 `componentSpecs` 中的组件顺序是否正确。

**内存不足：**
- 增加 milvus 组件的 `resources.limits.memory` 配置。
- 对于集群模式，调整数据节点（datanode）/索引节点（indexnode）/查询节点（querynode）的资源配额。

## 日常操作

| 操作 | 技能要求 | 外部文档 |
|---|---|---|
| 停止/启动/重启集群 | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-milvus/04-operations/01-stop-start-restart) |
| 调整 CPU/内存资源 | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-milvus/04-operations/02-vertical-scaling) |
| 增加/减少副本数量 | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-milvus/04-operations/03-horizontal-scaling) |
| 需要外部访问？ | [expose-service](../kubeblocks-expose-service/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-milvus/04-operations/) |

## 安全最佳实践

请遵循 [安全最佳实践](../../references/safety-patterns.md)：在应用配置前进行预测试，确认集群状态正常后才能正式部署，删除资源前请先执行删除前的检查流程。