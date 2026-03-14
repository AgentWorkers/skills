---
name: kubeblocks-addon-redis
metadata:
  version: "0.1.0"
description: 在 KubeBlocks 上部署和管理 Redis 集群，并提供拓扑选择指南。支持独立（开发/测试）模式、使用 Sentinel 的复制模式（高可用性）以及 Redis 集群分片（水平扩展）拓扑。当用户需要使用 Redis、缓存、内存存储，或明确希望创建 Redis 集群时，请参考本文档。文档包含拓扑结构对比、最佳实践配置以及连接方法。如需跨所有引擎创建通用集群，请参阅 `kubeblocks-create-cluster`。关于后续操作（如扩展、备份等），请使用相应的操作技能。
---
# 在 KubeBlocks 上部署 Redis

## 概述

使用 KubeBlocks 在 Kubernetes 上部署 Redis。共有三种拓扑结构可供选择：独立部署（适用于开发）、带 Sentinel 的复制部署（用于高可用性，HA）以及 Redis 集群（用于水平扩展）。

官方文档：https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/cluster-management/create-and-connect-a-redis-cluster  
完整文档索引：https://kubeblocks.io/llms-full.txt

## 先决条件

- 已经安装了 KubeBlocks 的运行中的 Kubernetes 集群（请参阅 [install-kubeblocks](../kubeblocks-install/SKILL.md)）  
- 必须启用 Redis 插件：  

```bash
# Check if redis addon is installed
helm list -n kb-system | grep redis

# Install if missing
helm install kb-addon-redis kubeblocks/redis --namespace kb-system --version 1.0.0
```  

## 可用的拓扑结构  

| 拓扑结构 | `clusterDef` | `topology` | 组件 | 使用场景 |  
|---|---|---|---|---|  
| 独立部署 | `redis` | `standalone` | 单个 Redis 实例 | 适用于开发/测试，无需高可用性 |  
| 复制部署（带 Sentinel） | `redis` | `replication` | 多个 Redis 实例 + Sentinel（3 个实例） | 适用于生产环境的高可用性配置 |  
| Redis 集群（分片） | N/A | N/A | 使用 `spec.shardings` 和 `componentDef: redis-cluster-7` | 用于水平扩展 |

**注意：** 分片拓扑结构使用 `spec.shardings` 而不是 `spec.componentSpecs`，这是两种不同的配置规范。

## 支持的 Redis 版本  

| Redis 版本 | `serviceVersion` |  
|---|---|  
| Redis 7.0 | `7.0.6` |  
| Redis 7.2 | `7.2.4` |  

## 工作流程  

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster (choose topology)
- [ ] Step 4: Wait for cluster to be ready
- [ ] Step 5: Connect to Redis
```  

## 第 1 步：确保插件已安装  

```bash
helm list -n kb-system | grep redis
```  

如果插件未安装，请执行相应的安装步骤：  

```bash
helm install kb-addon-redis kubeblocks/redis --namespace kb-system --version 1.0.0
```  

## 第 2 步：创建命名空间  

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```  

## 第 3 步：创建集群  

### 独立部署  

最简单的部署方式，仅包含一个 Redis 实例，适用于开发环境：  

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: redis-standalone
  namespace: demo
spec:
  clusterDef: redis
  topology: standalone
  terminationPolicy: Delete
  componentSpecs:
    - name: redis
      serviceVersion: "7.2.4"
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

### 带 Sentinel 的复制部署  

适用于生产环境的高可用性配置。Sentinel 负责监控主节点并自动执行故障转移：  

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: redis-replication
  namespace: demo
spec:
  clusterDef: redis
  topology: replication
  terminationPolicy: Delete
  componentSpecs:
    - name: redis
      serviceVersion: "7.2.4"
      replicas: 2
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
    - name: redis-sentinel
      serviceVersion: "7.2.4"
      replicas: 3
      resources:
        limits: {cpu: "0.2", memory: "256Mi"}
        requests: {cpu: "0.2", memory: "256Mi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
```  

**关键点：**  
- `redis` 组件至少包含 2 个副本（1 个主节点 + 多个副本，由 Sentinel 管理）  
- `redis-sentinel` 组件需要 3 个副本才能达到法定人数（quorum）  

### Redis 集群（分片）  

用于通过数据分片实现水平扩展。该拓扑结构使用 `spec.shardings` 而不是 `spec.componentSpecs`：  

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: redis-cluster
  namespace: demo
spec:
  terminationPolicy: Delete
  shardings:
    - name: shard
      shards: 3
      template:
        name: redis-shard
        componentDef: redis-cluster-7
        serviceVersion: "7.2.4"
        replicas: 2
        resources:
          limits: {cpu: "0.5", memory: "0.5Gi"}
          requests: {cpu: "0.5", memory: "0.5Gi"}
        volumeClaimTemplates:
          - name: data
            spec:
              accessModes: [ReadWriteOnce]
              resources: {requests: {storage: 20Gi}}
```  

**关键点：**  
- 使用 `spec.shardings` 进行配置  
- `shards: 3` 表示创建 3 个分片（建议至少设置这么多分片）  
- 每个分片包含 2 个副本（1 个主节点 + 1 个副本）  
- 使用 `componentDef: redis-cluster-7` 进行配置  
- 不需要在集群级别设置 `clusterDef` 或 `topology`  

## 第 4 步：等待集群准备就绪  

```bash
kubectl -n demo get cluster <cluster-name> -w
```  

等待集群状态变为 “Running”。  

检查集群中的 Pod：  

```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=<cluster-name>
```  

## 第 5 步：连接 Redis  

### 获取连接凭据  

```bash
# Secret name format: <cluster>-redis-account-default
kubectl -n demo get secret redis-standalone-redis-account-default -o jsonpath='{.data.password}' | base64 -d
```  

### 通过 `kubectl exec` 连接 Redis  

```bash
# Standalone / Replication
kubectl -n demo exec -it redis-standalone-redis-0 -- redis-cli

# Redis Cluster (use -c flag for cluster mode)
kubectl -n demo exec -it redis-cluster-shard-ckvks-0 -- redis-cli -c
```  

### 通过端口转发连接 Redis  

```bash
kubectl -n demo port-forward svc/redis-standalone-redis 6379:6379
# Then from another terminal:
redis-cli -h 127.0.0.1 -p 6379
```  

## 故障排除  

**集群在创建过程中卡住？**  
```bash
kubectl -n demo describe cluster <cluster-name>
kubectl -n demo get events --sort-by='.lastTimestamp'
```  

**Sentinel 故障转移问题？**  
```bash
kubectl -n demo exec -it redis-replication-redis-sentinel-0 -- redis-cli -p 26379 SENTINEL masters
```  

**Redis 集群的分片未分配？**  
```bash
kubectl -n demo exec -it <any-shard-pod> -- redis-cli -c CLUSTER INFO
```  

## 日常操作  

| 操作 | 所需技能 | 外部文档 |  
|---|---|---|  
| 停止/启动/重启集群 | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/cluster-management/stop-start-restart-a-redis-cluster) |  
| 调整 CPU/内存资源 | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/cluster-management/scale-for-a-redis-cluster) |  
| 添加/删除副本 | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/cluster-management/scale-for-a-redis-cluster) |  
| 扩展存储空间 | [volume-expansion](../kubeblocks-volume-expansion/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/cluster-management/expand-volume-of-a-redis-cluster) |  
| 修改配置参数 | [reconfigure-parameters](../kubeblocks-reconfigure-parameters/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/configuration/configure-cluster-parameters) |  
| 外部访问配置 | [expose-service](../kubeblocks-expose-service/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/cluster-management/expose-redis) |  
| 备份数据 | [backup](../kubeblocks-backup/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/backup-and-restore/backup) |  
| 恢复数据 | [restore](../kubeblocks-restore/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/backup-and-restore/restore) |  

## 安全最佳实践  

在正式部署前，请遵循 [safety-patterns.md](../../references/safety-patterns.md) 中的建议，包括进行模拟测试、确认集群状态以及执行删除前的检查列表。  

## 下一步  

- 如需查看所有拓扑结构的完整 YAML 配置示例，请参阅 [reference.md](references/reference.md)。