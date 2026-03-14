---
name: kubeblocks-addon-mysql
metadata:
  version: "0.1.0"
description: 在 KubeBlocks 上部署和管理 MySQL 集群，并提供拓扑选择指导。内容涵盖半同步复制、MySQL 组复制（MGR）、由 Orchestrator 管理的高可用性（HA）以及可选的 ProxySQL 负载均衡功能。当用户提到 MySQL 或 MariaDB，或明确希望创建 MySQL 数据库集群时，请参考本文档。文档提供了针对不同数据库引擎的拓扑结构比较、最佳实践配置以及连接方法。如需创建通用类型的集群（适用于所有数据库引擎），请参阅 `kubeblocks-create-cluster` 文档；关于后续操作（如扩展、备份等），请使用相应的操作指南。
---
# 在 KubeBlocks 上部署 MySQL

## 概述

使用 KubeBlocks 部署高可用性的 MySQL 集群。提供了多种拓扑结构——从简单的半同步复制到完全由 Orchestration 管理的配置（包含 ProxySQL）。

官方文档：https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/create-and-connect-a-mysql-cluster  
完整文档索引：https://kubeblocks.io/llms-full.txt

## 先决条件

- 已经安装了 KubeBlocks 的运行中的 Kubernetes 集群（请参阅 [install-kubeblocks](../kubeblocks-install/SKILL.md)）  
- 必须启用 MySQL 插件：

```bash
# Check if mysql addon is installed
helm list -n kb-system | grep mysql

# Install if missing
helm install kb-addon-mysql kubeblocks/mysql --namespace kb-system --version 1.0.0
```

## 可用的拓扑结构

| 拓扑结构 | 参数 | 组件 | 使用场景 |
|---|---|---|---|
| 半同步复制 | `semisync` | mysql | 标准的高可用性（HA）配置，至少 2 个副本 |
| 半同步复制 + ProxySQL | `semisync-proxysql` | mysql + proxysql | 带有查询路由功能的高可用性配置 |
| 组复制（Group Replication） | `mgr` | mysql | 支持多主节点，至少 3 个副本 |
| MGR + ProxySQL | `mgr-proxysql` | mysql + proxysql | 带有负载均衡功能的 MGR 配置 |
| Orchestration 管理 | `orc` | mysql + orchestrator | 使用外部 HA 管理器 |
| Orchestration + ProxySQL | `orc-proxysql` | mysql + orc + proxysql | 完整的高可用性栈 |

**推荐配置：** `semisync` —— 最简单且应用最广泛的配置。

## 支持的 MySQL 版本

| MySQL 版本 | 对应的服务版本 |
|---|---|
| MySQL 5.7 | `5.7.44` |
| MySQL 8.0 | `8.0.33`, `8.0.35` |
| MySQL 8.4 | `8.4.2` |

## 工作流程

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster
- [ ] Step 4: Wait for cluster to be ready
- [ ] Step 5: Connect to MySQL
```

## 第 1 步：确保插件已安装

```bash
helm list -n kb-system | grep mysql
```

如果插件未安装，请进行安装：

```bash
helm install kb-addon-mysql kubeblocks/mysql --namespace kb-system --version 1.0.0
```

## 第 2 步：创建命名空间

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```

## 第 3 步：创建集群

### 半同步复制（推荐配置）

这是最常见的拓扑结构。包含一个主节点和至少一个或多个副本，采用半同步复制机制以确保数据安全。

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mysql-cluster
  namespace: demo
spec:
  clusterDef: mysql
  topology: semisync
  terminationPolicy: Delete
  componentSpecs:
    - name: mysql
      serviceVersion: "8.0.35"
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

应用相应的配置：

```bash
kubectl apply -f mysql-cluster.yaml
```

### 组复制（MGR）

支持多主节点配置，需要至少 3 个副本：

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mysql-mgr
  namespace: demo
spec:
  clusterDef: mysql
  topology: mgr
  terminationPolicy: Delete
  componentSpecs:
    - name: mysql
      serviceVersion: "8.0.35"
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

关于使用 ProxySQL 或 Orchestration 的拓扑结构，请参阅 [reference.md](references/reference.md)。

## 第 4 步：等待集群启动完成

```bash
kubectl -n demo get cluster mysql-cluster -w
```

等待集群状态显示为 “Running”。通常启动时间为 1-3 分钟。

检查组件状态：

```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=mysql-cluster
```

## 第 5 步：连接 MySQL

### 获取登录凭据

MySQL 的 root 密码存储在 Kubernetes 的秘密配置中：

```bash
# Secret name format: <cluster>-mysql-account-root
kubectl -n demo get secret mysql-cluster-mysql-account-root -o jsonpath='{.data.password}' | base64 -d
```

### 通过 `kubectl exec` 连接

```bash
kubectl -n demo exec -it mysql-cluster-mysql-0 -- bash -c 'mysql -uroot -p"$(cat /etc/mysql/secret/password)"'
```

### 通过端口转发连接

```bash
kubectl -n demo port-forward svc/mysql-cluster-mysql 3306:3306
# Then from another terminal:
mysql -h 127.0.0.1 -P 3306 -u root -p
```

## 备份

MySQL 支持三种备份方法：

| 方法 | 功能 | 使用场景 |
|---|---|---|
| XtraBackup | `xtrabackup` | 物理备份，适用于大型数据库 |
| 卷快照 | `mysql-volumesnapshot` | 存储级别的快照，速度最快 |
| Binlog 归档 | `archive-binlog` | 持续归档，用于数据恢复（PITR，Point-In-Time Recovery） |

示例备份操作：

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: mysql-backup
  namespace: demo
spec:
  backupMethod: xtrabackup
  backupPolicyName: mysql-cluster-mysql-backup-policy
```

## 故障排除

**集群在创建过程中卡住：**
```bash
kubectl -n demo describe cluster mysql-cluster
kubectl -n demo get events --sort-by='.lastTimestamp'
```

**Pod 进入 CrashLoopBackOff 状态：**
```bash
kubectl -n demo logs mysql-cluster-mysql-0
```

**半同步副本无法连接：**
- 确保半同步拓扑结构中的副本数量大于或等于 2 个。
- 检查 Pod 之间的网络配置。

## 日常维护操作

| 操作 | 所需技能 | 外部文档参考 |
|---|---|---|
| 停止/启动/重启集群 | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/stop-start-restart-a-mysql-cluster) |
| 调整 CPU/内存资源 | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/scale-for-a-mysql-cluster) |
| 增加/减少副本数量 | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/scale-for-a-mysql-cluster) |
| 扩展存储空间 | [volume-expansion](../kubeblocks-volume-expansion/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/expand-volume-of-a-mysql-cluster) |
| 修改配置参数 | [reconfigure-parameters](../kubeblocks-reconfigure-parameters/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/configuration/configure-cluster-parameters) |
| 切换主节点 | [switchover](../kubeblocks-switchover/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/switchover) |
| 升级 MySQL 版本 | [minor-version-upgrade](../kubeblocks-minor-version-upgrade/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/upgrade) |
| 公开集群服务 | [expose-service](../kubeblocks-expose-service/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/expose-mysql) |
| 备份数据 | [backup](../kubeblocks-backup/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/backup-and-restore/backup) |
| 恢复数据 | [restore](../kubeblocks-restore/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/backup-and-restore/restore) |

## 安全最佳实践

在正式应用配置之前，请遵循 [safety-patterns.md](../../references/safety-patterns.md) 中提供的最佳实践，包括进行预测试、确认集群状态以及执行删除前的检查清单。

## 下一步操作

- 如需查看所有拓扑结构的详细 YAML 配置示例，请参阅 [reference.md](references/reference.md)。