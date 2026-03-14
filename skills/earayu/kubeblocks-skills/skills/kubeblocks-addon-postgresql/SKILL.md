---
name: kubeblocks-addon-postgresql
metadata:
  version: "0.1.0"
description: 在 KubeBlocks 上部署和管理 PostgreSQL 集群，支持基于 Patroni 的高可用性和自动故障转移功能。提供了 Spilo 镜像配置、复制拓扑结构以及连接方式。当用户提及 PostgreSQL、Postgres 或明确希望创建 PostgreSQL 数据库集群时，请使用此技能。如需跨所有引擎创建通用集群，请参阅 `kubeblocks-create-cluster`；对于后续操作（如扩展、备份、参数调优等），请使用相应的操作技能。
---
# 在 KubeBlocks 上部署 PostgreSQL

## 概述

使用 KubeBlocks 部署高可用性的 PostgreSQL 集群。该方案基于 Spilo 镜像，并结合 Patroni 实现自动领导者选举和故障转移功能。

官方文档：https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/create-and-connect-a-postgresql-cluster  
完整文档索引：https://kubeblocks.io/llms-full.txt

## 先决条件

- 已经安装了 KubeBlocks 的运行中的 Kubernetes 集群（请参阅 [install-kubeblocks](../kubeblocks-install/SKILL.md)）  
- 必须启用 PostgreSQL 扩展插件：  

```bash
# Check if postgresql addon is installed
helm list -n kb-system | grep postgresql

# Install if missing
helm install kb-addon-postgresql kubeblocks/postgresql --namespace kb-system --version 1.0.0
```

## 集群架构

- **集群定义：** `postgresql`  
- **拓扑结构：** `replication`  
- **高可用性引擎：** Patroni（内置在 Spilo 镜像中）  
- **组件：** `postgresql`（主节点 + 读复制节点）  

Patroni 负责自动选举领导者节点、处理故障转移以及管理复制节点。主节点会在复制节点中选出，流式复制机制确保所有节点保持数据同步。

## 支持的版本

| 主版本 | 服务版本示例 |
|---|---|
| PostgreSQL 12 | `12.14.0`, `12.14.1`, `12.15.0` |
| PostgreSQL 14 | `14.7.2`, `14.8.0` |
| PostgreSQL 15 | `15.7.0` |
| PostgreSQL 16 | `16.4.0` |
| PostgreSQL 17 | `17.4.0` |
| PostgreSQL 18 | `18.0.0` |

## 工作流程

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster
- [ ] Step 4: Wait for cluster to be ready
- [ ] Step 5: Connect to PostgreSQL
```

## 第一步：确保扩展插件已安装  

```bash
helm list -n kb-system | grep postgresql
```

如果未安装，请先进行安装：  

```bash
helm install kb-addon-postgresql kubeblocks/postgresql --namespace kb-system --version 1.0.0
```

## 第二步：创建命名空间  

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```

## 第三步：创建集群  

### 复制集群（标准配置）  

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: pg-cluster
  namespace: demo
spec:
  clusterDef: postgresql
  topology: replication
  terminationPolicy: Delete
  componentSpecs:
    - name: postgresql
      serviceVersion: "14.7.2"
      replicas: 2
      disableExporter: false
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
kubectl apply -f pg-cluster.yaml
```

**关键配置字段：**  
- `disableExporter: false` — 启用用于监控的指标导出器  
- `replicas: 2` — 一个主节点 + 一个复制节点（Patroni 负责选举领导者节点）  

### 生产环境配置  

在生产环境中，建议增加资源配额和复制节点数量：  

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: pg-production
  namespace: demo
spec:
  clusterDef: postgresql
  topology: replication
  terminationPolicy: Halt
  componentSpecs:
    - name: postgresql
      serviceVersion: "16.4.0"
      replicas: 3
      disableExporter: false
      resources:
        limits: {cpu: "2", memory: "4Gi"}
        requests: {cpu: "2", memory: "4Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 100Gi}}
```

## 第四步：等待集群准备就绪  

```bash
kubectl -n demo get cluster pg-cluster -w
```

等待集群状态变为 “Running”。通常启动时间为 1-3 分钟。  

检查相关 Pod 的运行状态：  

```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=pg-cluster
```

## 第五步：连接 PostgreSQL  

### 获取连接凭据  

```bash
# Secret name format: <cluster>-postgresql-account-postgres
kubectl -n demo get secret pg-cluster-postgresql-account-postgres -o jsonpath='{.data.password}' | base64 -d
```

### 通过 `kubectl exec` 连接  

```bash
kubectl -n demo exec -it pg-cluster-postgresql-0 -- bash -c 'psql -U postgres'
```

### 通过端口转发连接  

```bash
kubectl -n demo port-forward svc/pg-cluster-postgresql 5432:5432
# Then from another terminal:
psql -h 127.0.0.1 -p 5432 -U postgres
```

## 备份  

PostgreSQL 支持以下三种备份方式：  

| 备份方式 | 功能 | 适用场景 |
|---|---|---|
| `pg-basebackup` | 逻辑备份 | 备份整个数据库 |
| `volume Snapshot` | 卷级快照 | 最快速的备份方式 |
| `wal-archive` | 持续归档 | 用于时间点恢复（PITR）  

示例备份命令：  

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: pg-backup
  namespace: demo
spec:
  backupMethod: pg-basebackup
  backupPolicyName: pg-cluster-postgresql-backup-policy
```

若需进行时间点恢复（PITR），请先启用 WAL 归档功能，然后恢复到指定时间点。  

## 故障排除  

**集群在创建过程中卡住怎么办？**  
```bash
kubectl -n demo describe cluster pg-cluster
kubectl -n demo get events --sort-by='.lastTimestamp'
```

**Patroni 相关问题？**  
```bash
# Check Patroni status
kubectl -n demo exec -it pg-cluster-postgresql-0 -- patronictl list
```

**复制延迟问题？**  
```bash
kubectl -n demo exec -it pg-cluster-postgresql-0 -- psql -U postgres -c "SELECT * FROM pg_stat_replication;"
```

## 日常维护操作  

| 操作 | 所需技能 | 外部文档参考 |  
|---|---|---|
| 停止/启动/重启集群 | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/stop-start-restart-a-postgresql-cluster) |
| 调整 CPU/内存资源 | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/scale-for-a-postgresql-cluster) |
| 添加/删除复制节点 | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/scale-for-a-postgresql-cluster) |
| 扩展存储空间 | [volume-expansion](../kubeblocks-volume-expansion/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/expand-volume-of-a-postgresql-cluster) |
| 修改配置参数 | [reconfigure-parameters](../kubeblocks-reconfigure-parameters/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/configuration/configure-cluster-parameters) |
| 切换主节点 | [switchover](../kubeblocks-switchover/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/switchover) |
| 升级引擎版本 | [minor-version-upgrade](../kubeblocks-minor-version-upgrade/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/upgrade) |
| 公开集群服务 | [expose-service](../kubeblocks-expose-service/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/expose-postgresql) |
| 备份数据 | [backup](../kubeblocks-backup/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/backup-and-restore/backup) |
| 恢复数据 | [restore](../kubeblocks-restore/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/backup-and-restore/restore) |

## 安全最佳实践  

在正式部署前，请遵循 [safety-patterns.md](../../references/safety-patterns.md) 中的建议，包括进行模拟测试、确认集群状态以及执行删除前的检查清单。  

## 下一步操作  

- 有关详细的 YAML 配置示例及基础配置方案，请参阅 [reference.md](references/reference.md)。