---
name: kubeblocks-addon-qdrant
metadata:
  version: "0.1.0"
description: 在 KubeBlocks 上部署和管理 Qdrant 向量数据库集群，用于向量搜索、相似性搜索以及嵌入存储功能。当用户提到 Qdrant、向量数据库、向量搜索、相似性搜索、嵌入（embedding）或明确表示希望创建 Qdrant 集群时，可参考本文档。本文档涵盖了集群的创建、通过 REST API 进行连接以及后续的日常运维操作。如需针对所有引擎进行通用集群创建，请参阅 `kubeblocks-create-cluster`；对于扩展（scaling）等后续运维操作，请使用相应的操作文档。
---
# 在 KubeBlocks 上部署 Qdrant

## 概述

使用 KubeBlocks 在 Kubernetes 上部署 Qdrant 向量数据库集群。Qdrant 是一款高性能的向量相似性搜索引擎，专为基于人工智能的应用程序（如语义搜索、RAG 和推荐系统）而设计。多个副本共同构成一个分布式集群，并实现数据分片。

官方文档：https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/01-overview  
快速入门：https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/02-quickstart

## 先决条件

- 已经安装了 KubeBlocks 的运行中的 Kubernetes 集群（请参阅 [install-kubeblocks](../kubeblocks-install/SKILL.md)）  
- 必须启用 Qdrant 插件：

```bash
# Check if qdrant addon is installed
helm list -n kb-system | grep qdrant

# Install if missing
helm install kb-addon-qdrant kubeblocks/qdrant --namespace kb-system --version 1.0.0
```

## 架构

| 架构 | 值 | 组件 | 用例 |
|---|---|---|---|
| 集群 | `cluster` | qdrant | 单一架构，支持数据分片 |

## 支持的版本

| 版本 | serviceVersion |
|---|---|
| 1.5 | `1.5.0` |
| 1.7 | `1.7.3` |
| 1.8 | `1.8.1`, `1.8.4` |
| 1.10 | `1.10.0` |
| 1.13 | `1.13.4` |
| 1.15 | `1.15.4` |

查看可用版本：`kubectl get cmpv qdrant`

## 工作流程

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster (dry-run then apply)
- [ ] Step 4: Wait for cluster to be ready
- [ ] Step 5: Connect via REST API
```

## 第 1 步：确保插件已安装

```bash
helm list -n kb-system | grep qdrant
```

如果未找到插件，请执行以下操作：  
```bash
helm install kb-addon-qdrant kubeblocks/qdrant --namespace kb-system --version 1.0.0
```

## 第 2 步：创建命名空间

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```

## 第 3 步：创建集群

默认端口：6333（HTTP REST API），6334（gRPC）。推荐的副本数量为 3、5 或 7 个。

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: qdrant-cluster
  namespace: demo
spec:
  clusterDef: qdrant
  topology: cluster
  terminationPolicy: Delete
  componentSpecs:
    - name: qdrant
      serviceVersion: "1.10.0"
      replicas: 3
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
```

**应用前的测试：**

```bash
kubectl apply -f cluster.yaml --dry-run=server
```

如果测试成功，则继续下一步：

```bash
kubectl apply -f cluster.yaml
```

## 第 4 步：等待集群准备好

```bash
kubectl -n demo get cluster qdrant-cluster -w
```

**成功条件：** `STATUS` 显示为 `Running`。通常需要 1–2 分钟。如果 10 分钟后集群仍未准备好，请检查原因。

检查 Pod 的状态：  
```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=qdrant-cluster
```

## 第 5 步：通过 REST API 连接集群

端口 6333 提供 HTTP REST API 接口。可以使用端口转发或无头服务来访问集群：

```bash
# Port-forward to a pod
kubectl -n demo port-forward qdrant-cluster-qdrant-0 6333:6333
```

```bash
# Health check
curl http://localhost:6333/health
```

```bash
# List collections
curl http://localhost:6333/collections
```

内部服务地址：`qdrant-cluster-qdrant-qdrant.demo.svc.cluster.local:6333`（REST），`:6334`（gRPC）。

## 备份

KubeBlocks 支持通过 HTTP API `snapshot` 对所有数据集进行完整备份。详情请参阅：  
https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/05-backup-restore/02-create-full-backup

## 故障排除

**集群在创建过程中卡住：**  
```bash
kubectl -n demo describe cluster qdrant-cluster
kubectl -n demo get events --sort-by='.lastTimestamp'
```

**Pod 无法启动：**  
```bash
kubectl -n demo logs qdrant-cluster-qdrant-0
kubectl -n demo describe pod qdrant-cluster-qdrant-0
```

**连接被拒绝：** 确保端口转发功能正在运行，或者从集群内部直接访问内部服务。

## 日常操作

| 操作 | 所需技能 | 外部文档 |
|---|---|---|
| 停止/启动/重启集群 | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/04-operations/01-stop-start-restart) |
| 调整 CPU/内存资源 | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/04-operations/) |
| 添加/删除副本 | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/04-operations/) |
| 扩展存储空间 | [volume-expansion](../kubeblocks-volume-expansion/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/04-operations/) |
| 升级引擎版本 | [minor-version-upgrade](../kubeblocks-minor-version-upgrade/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/04-operations/) |
| 将服务暴露到外部 | [expose-service](../kubeblocks-expose-service/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/04-operations/) |
| 备份数据 | [backup](../kubeblocks-backup/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/05-backup-restore/02-create-full-backup) |
| 恢复数据 | [restore](../kubeblocks-restore/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/05-backup-restore/) |

## 安全最佳实践

请遵循 [安全最佳实践](../../references/safety-patterns.md)：在应用新配置前先进行测试，确认操作成功后再正式部署，删除资源前请执行预删除检查。