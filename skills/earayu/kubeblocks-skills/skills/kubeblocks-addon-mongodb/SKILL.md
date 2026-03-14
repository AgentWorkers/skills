---
name: kubeblocks-addon-mongodb
metadata:
  version: "0.1.0"
description: 在 KubeBlocks 上部署和管理 MongoDB 集群，并提供拓扑选择指南。支持 ReplicaSet（高可用性）和分片（mongos + 配置服务器 + 分片）两种拓扑结构。当用户提到 MongoDB、Mongo、文档数据库或明确希望创建 MongoDB 集群时，请使用本文档。文档中包含拓扑结构对比、最佳实践设置以及连接方法。关于所有引擎的通用集群创建操作，请参考 `kubeblocks-create-cluster`；对于后续操作（如扩展、备份等），请使用相应的操作文档。
---
# 在 KubeBlocks 上部署 MongoDB

## 概述

使用 KubeBlocks 在 Kubernetes 上部署 MongoDB 集群。支持通过 ReplicaSet 实现高可用性（HA），并通过分片（Sharding）实现水平扩展，同时利用 mongos 路由器和配置服务器（config-server）进行管理。

官方文档：https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/cluster-management/create-and-connect-a-mongodb-cluster  
完整文档索引：https://kubeblocks.io/llms-full.txt

## 先决条件

- 已经安装了 KubeBlocks 的运行中的 Kubernetes 集群（请参阅 [install-kubeblocks](../kubeblocks-install/SKILL.md)）  
- 必须启用 MongoDB 插件：

```bash
# Check if mongodb addon is installed
helm list -n kb-system | grep mongodb

# Install if missing
helm install kb-addon-mongodb kubeblocks/mongodb --namespace kb-system --version 1.0.0
```

## 可用的拓扑结构

| 拓扑结构 | 拓扑值 | 组件 | 使用场景 |
|---|---|---|---|
| ReplicaSet | `replicaset` | MongoDB（3 个副本） | 标准高可用性配置，最常见的方式 |
| Sharding | `sharding` | 分片（N 个）+ 配置服务器（config-server）+ mongos | 实现水平扩展，适用于大型数据集 |

## 支持的版本

支持 MongoDB 4.0 至 7.0 版本。常见的 `serviceVersion` 值如下：

| 版本 | `serviceVersion` |
|---|---|
| MongoDB 4.0 | `4.0` |
| MongoDB 4.2 | `4.2` |
| MongoDB 4.4 | `4.4` |
| MongoDB 5.0 | `5.0` |
| MongoDB 6.0 | `6.0` |
| MongoDB 7.0 | `7.0.12` |

## 工作流程

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster (choose topology)
- [ ] Step 4: Wait for cluster to be ready
- [ ] Step 5: Connect to MongoDB
```

## 第 1 步：确保插件已安装

```bash
helm list -n kb-system | grep mongodb
```

如果插件未安装，请执行相应的安装步骤：

```bash
helm install kb-addon-mongodb kubeblocks/mongodb --namespace kb-system --version 1.0.0
```

## 第 2 步：创建命名空间

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```

## 第 3 步：创建集群

### ReplicaSet（推荐）

使用自动选举主节点的标准高可用性配置：

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mongo-cluster
  namespace: demo
spec:
  clusterDef: mongodb
  topology: replicaset
  terminationPolicy: Delete
  componentSpecs:
    - name: mongodb
      serviceVersion: "7.0.12"
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

应用配置：

```bash
kubectl apply -f mongo-cluster.yaml
```

**关键点：**
- 至少需要 3 个副本才能构成一个有效的 ReplicaSet（以便进行多数投票）
- MongoDB 会自动在副本中选举出一个主节点

### Sharding

用于在多个分片之间实现水平扩展。需要配置 `spec.shardings`（用于分片数据）和 `spec.componentSpecs`（用于配置服务器和 mongos）：

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mongo-sharded
  namespace: demo
spec:
  clusterDef: mongodb
  topology: sharding
  terminationPolicy: Delete
  shardings:
    - name: shard
      shards: 2
      template:
        name: mongodb
        serviceVersion: "7.0.12"
        replicas: 3
        resources:
          limits: {cpu: "0.5", memory: "0.5Gi"}
          requests: {cpu: "0.5", memory: "0.5Gi"}
        volumeClaimTemplates:
          - name: data
            spec:
              accessModes: [ReadWriteOnce]
              resources: {requests: {storage: 20Gi}}
  componentSpecs:
    - name: config-server
      serviceVersion: "7.0.12"
      replicas: 3
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
    - name: mongos
      serviceVersion: "7.0.12"
      replicas: 2
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
```

**关键点：**
- 分片使用 `spec.shardings` 进行配置（每个分片都是一个 ReplicaSet）
- 配置服务器和 mongos 使用 `spec.componentSpecs` 进行配置
- 设置 `shards: 2` 会创建 2 个分片（每个分片包含 3 个副本）
- 通过端口 27017 连接到 mongos 进行数据操作
- 配置服务器负责存储分片元数据

## 第 4 步：等待集群准备就绪

```bash
kubectl -n demo get cluster <cluster-name> -w
```

等待集群状态变为 “Running”。分片集群的启动时间可能较长（3-5 分钟）。

检查相关 Pod 的状态：

```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=<cluster-name>
```

## 第 5 步：连接 MongoDB

### 获取登录凭据

```bash
# Secret name format: <cluster>-mongodb-account-root
kubectl -n demo get secret mongo-cluster-mongodb-account-root -o jsonpath='{.data.password}' | base64 -d
```

### 通过 kubectl exec 连接

```bash
# ReplicaSet
kubectl -n demo exec -it mongo-cluster-mongodb-0 -- mongosh --username root --authenticationDatabase admin

# Sharded cluster (connect via mongos)
kubectl -n demo exec -it mongo-sharded-mongos-0 -- mongosh --username root --authenticationDatabase admin
```

### 通过端口转发连接

```bash
# ReplicaSet
kubectl -n demo port-forward svc/mongo-cluster-mongodb 27017:27017

# Sharded (via mongos)
kubectl -n demo port-forward svc/mongo-sharded-mongos 27017:27017

# Then from another terminal:
mongosh mongodb://root:<password>@127.0.0.1:27017/admin
```

## 故障排除

**集群在创建过程中卡住：**
```bash
kubectl -n demo describe cluster <cluster-name>
kubectl -n demo get events --sort-by='.lastTimestamp'
```

**ReplicaSet 无法正常形成：**
```bash
kubectl -n demo exec -it mongo-cluster-mongodb-0 -- mongosh --eval "rs.status()"
```

**分片状态：**
```bash
kubectl -n demo exec -it mongo-sharded-mongos-0 -- mongosh --eval "sh.status()"
```

## 日常操作

| 操作 | 需要的技能 | 外部文档参考 |
|---|---|---|
| 停止/启动/重启集群 | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/cluster-management/stop-start-restart-a-mongodb-cluster) |
| 调整 CPU/内存资源 | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/cluster-management/scale-for-a-mongodb-cluster) |
| 添加/删除副本 | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/cluster-management/scale-for-a-mongodb-cluster) |
| 扩展存储空间 | [volume-expansion](../kubeblocks-volume-expansion/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/cluster-management/expand-volume-of-a-mongodb-cluster) |
| 修改配置参数 | [reconfigure-parameters](../kubeblocks-reconfigure-parameters/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/configuration/configure-cluster-parameters) |
| 备份数据 | [backup](../kubeblocks-backup/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/backup-and-restore/backup) |
| 恢复数据 | [restore](../kubeblocks-restore/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/backup-and-restore/restore) |

## 安全最佳实践

请遵循 [safety-patterns.md](../../references/safety-patterns.md) 中的建议，进行预测试，确认集群状态后再正式应用配置，并在删除集群前完成必要的检查。

## 下一步

- 如需查看详细的分片配置示例，请参阅 [reference.md](references/reference.md)。