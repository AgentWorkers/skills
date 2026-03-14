---
name: kubeblocks-backup
metadata:
  version: "0.1.0"
description: 为 KubeBlocks 数据库集群创建备份。支持按需执行完整备份、基于 Cron 的定时备份以及用于点恢复（Point-in-Time Recovery, PITR）的连续备份。涵盖了针对 S3、GCS、Azure Blob 和 MinIO 的 BackupRepo 配置。适用于用户需要备份、生成数据快照、保护或归档数据库数据的情况。**不适用于从备份中恢复数据（请参阅“恢复”相关技能）或管理备份存储基础设施（请参阅 BackupRepo 文档）**。
---
# 备份 KubeBlocks 数据库集群

## 概述

KubeBlocks 通过全备份、定时备份和持续备份（用于实现精确时间点恢复，PITR）来提供数据保护。备份操作通过 `Backup` CR 或 `OpsRequest` CR 进行管理，并存储在配置好的 `BackupRepo` 中。

官方文档：https://kubeblocks.io/docs/preview/user_docs/concepts/backup-and-restore/introduction

## 各附加组件的备份方法

| 附加组件      | 物理备份方法 | 快照方法           | 持续备份（PITR）         |
|------------|----------------------|---------------------|---------------------|
| MySQL      | xtrabackup           | volume-snapshot     | archive-binlog      |
| PostgreSQL | pg-basebackup        | volume-snapshot     | wal-archive         |
| Redis      | datafile             | volume-snapshot     | —                   |
| MongoDB    | datafile             | volume-snapshot     | —                   |

### 选择备份方法

- **物理备份**（xtrabackup, pg-basebackup, datafile）：备份文件是存储在 `BackupRepo` 中的完整副本，具有便携性和独立性，适用于任何存储后端。由于不依赖于额外的基础设施，因此推荐作为默认备份方式。
- **卷快照**：利用存储层的原生快照功能（通过 CSI）。对于大型数据库来说，由于采用写时复制机制，速度非常快，但需要支持快照的 `VolumeSnapshotClass` 和 CSI 驱动程序——这在本地或开发环境中可能不可用。
- **持续备份**（archive-binlog, wal-archive）：实时流式传输事务日志以实现精确时间点恢复（PITR）。对于需要恢复到任意时间点的生产环境至关重要。

## 预检查

在开始之前，请确认集群运行正常且没有其他操作正在执行：

```bash
# Cluster must be Running
kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.status.phase}'

# No pending OpsRequests
kubectl get opsrequest -n <namespace> -l app.kubernetes.io/instance=<cluster-name> --field-selector=status.phase!=Succeed
```

如果集群未处于运行状态或有未完成的 `OpsRequest`，请等待其完成后再继续。

## 工作流程

```
- [ ] Step 1: Ensure BackupRepo exists
- [ ] Step 2: Check BackupPolicy for the cluster
- [ ] Step 3: Create backup (on-demand or scheduled)
- [ ] Step 4: Verify backup
```

## 第一步：确保 `BackupRepo` 存在

`BackupRepo` 定义了备份数据的存储位置（如 S3、OSS、MinIO、GCS 等）。在创建备份之前，至少需要配置一个 `BackupRepo`。

```bash
kubectl get backuprepo
```

如果不存在 `BackupRepo`，请参阅 [reference.md](references/reference.md) 以获取针对不同存储提供商的设置说明。

## 第二步：检查 `BackupPolicy`

每个集群在创建时会自动获得一个 `BackupPolicy`。请确认其是否存在：

```bash
kubectl get backuppolicy -n <ns>
```

默认的命名规则为 `<cluster>-<component>-backup-policy`。`BackupPolicy` 定义了可用的备份方法及其配置。

## 第三步：创建备份

### 选项 A：通过 `OpsRequest` 进行按需备份

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: <cluster>-backup-ops
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: Backup
  backup:
    backupPolicyName: <cluster>-<component>-backup-policy
    backupMethod: <method>    # xtrabackup / volume-snapshot / pg-basebackup etc.
    deletionPolicy: Delete
    retentionPeriod: 7d
```

在应用之前，请先进行模拟测试（dry-run）：

```bash
kubectl apply -f backup-ops.yaml --dry-run=server
```

如果模拟测试报告错误，请修复 YAML 文件后再继续。

执行备份操作：

```bash
kubectl apply -f backup-ops.yaml
kubectl get ops <cluster>-backup-ops -n <ns> -w
```

> **成功条件**：`.status.phase` = `Succeed` | **通常情况**：结果因配置而异 | **如果超过 30 分钟未完成**：`kubectl describe ops <cluster>-backup-ops -n <ns>`

### 选项 B：通过 `Backup CR` 进行按需备份

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: <backup-name>
  namespace: <ns>
spec:
  backupMethod: <method>
  backupPolicyName: <policy-name>
  deletionPolicy: Delete
```

在应用之前，请先进行模拟测试（dry-run）：

```bash
kubectl apply -f backup.yaml --dry-run=server
```

如果模拟测试报告错误，请修复 YAML 文件后再继续。

执行备份操作：

```bash
kubectl apply -f backup.yaml
kubectl get backup <backup-name> -n <ns> -w
```

> **成功条件**：全备份完成时：`.status.phase` = `Completed` | **通常情况**：结果因配置而异 | **如果超过 30 分钟未完成**：`kubectl describe backup <backup-name> -n <ns>` | **持续备份中**：`.status.phase` = `Running` | **通常情况**：约 1 分钟完成 | **如果超过 5 分钟未完成**：`kubectl describe backup <backup-name> -n <ns>`

### 选项 C：通过集群 CR 进行定时备份

在集群的 CR 配置中添加 `backup` 部分：

```yaml
spec:
  backup:
    enabled: true
    retentionPeriod: 30d
    method: xtrabackup
    cronExpression: "0 0 * * *"
    repoName: <repo-name>
```

常见的 Cron 表达式：
- `"0 0 * * *"`：每天午夜
- `"0 2 * * 0"`：每周日凌晨 2 点
- `"0 */6 * * *"`：每 6 小时

### 选项 D：用于 PITR 的持续备份

持续备份会实时传输事务日志（binlog/WAL），以实现精确时间点恢复。使用相应的 `Backup CR` 进行配置：

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: <cluster>-continuous
  namespace: <ns>
spec:
  backupMethod: archive-binlog    # MySQL; use wal-archive for PostgreSQL
  backupPolicyName: <cluster>-<component>-backup-policy
  deletionPolicy: Delete
```

要使 PITR 功能正常工作，必须同时具备完整的全备份和正在运行的持续备份。

## 第四步：验证备份结果

```bash
kubectl get backup -n <ns>
```

预期的备份状态应为 `Completed`：

```
NAME              POLICY                              METHOD        STATUS      AGE
my-backup         mycluster-mysql-backup-policy        xtrabackup   Completed   5m
```

查看备份详细信息：

```bash
kubectl describe backup <backup-name> -n <ns>
```

## 故障排除

**备份状态为 `InProgress` 且无法完成**：
- 检查 `BackupRepo` 的连接是否正常：`kubectl describe backuprepo`
- 查看备份 Pod 的日志：`kubectl logs -n <ns> -l app.kubernetes.io/name=backup`

**找不到 `BackupPolicy`**：
- 确保集群正在运行：`kubectl get cluster -n <ns>`
- `BackupPolicy` 是随集群自动创建的；请检查相关附加组件的安装情况。

**卷快照备份失败**：
- 确保存在 `VolumeSnapshotClass`：`kubectl get volumesnapshotclass`
- CSI 驱动程序必须支持卷快照功能

## 额外参考

有关 `BackupRepo` 的设置（S3、OSS、MinIO、GCS）、持续备份配置以及 `BackupPolicy` 的高级定制，请参阅 [reference.md](references/reference.md)。

有关代理安全最佳实践（模拟测试、状态确认、生产环境保护等），请参阅 [safety-patterns.md](../../references/safety-patterns.md)。