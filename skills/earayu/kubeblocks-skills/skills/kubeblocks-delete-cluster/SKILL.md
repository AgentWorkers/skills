---
name: kubeblocks-delete-cluster
metadata:
  version: "0.1.0"
description: >
  **安全删除 KubeBlocks 数据库集群**  
  该操作会预先检查备份文件、PVC（Persistent Volume Claim）以及所有依赖资源的情况，确保数据能够被妥善处理。适用于用户需要彻底移除或清理数据库集群的场景。**请注意：** 此操作并非用于临时停止集群运行（请参阅 `kubeblocks-cluster-lifecycle`），也不用于卸载 KubeBlocks 操作器（请参阅 `kubeblocks-install`）。
---
# 删除 KubeBlocks 数据库集群

## 概述

本文档介绍了如何安全地删除由 KubeBlocks 管理的数据库集群。内容包括删除前的检查、处理 `terminationPolicy`（终止策略），以及清理残留资源。

官方文档：https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/delete-mysql-cluster  
完整文档索引：https://kubeblocks.io/llms-full.txt

## 工作流程

```
- [ ] Step 1: Pre-deletion checklist
- [ ] Step 2: Handle terminationPolicy
- [ ] Step 3: Delete the cluster
- [ ] Step 4: Verify deletion
- [ ] Step 5: Clean up residual resources (optional)
```

## 第 1 步：删除前的检查

在删除之前，需要与用户确认以下内容：

### 1a：识别集群

```bash
kubectl get cluster -n <namespace>
```

### 1b：检查终止策略（terminationPolicy）

```bash
kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.spec.terminationPolicy}'
```

| 策略 | 删除时的行为 |
|--------|----------------------|
| `DoNotTerminate` | **删除操作被禁止。** 需要先进行修复才能删除。 |
| `Delete` | 删除 pods 和 PVCs，同时保留备份。 |
| `WipeOut` | 删除所有内容，包括备份。 |

### 1c：检查是否存在备份

```bash
kubectl get backup -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

如果存在备份且策略设置为 `WipeOut`，**请警告用户** 所有备份也会被删除。

### 1d：检查依赖资源

```bash
kubectl get opsrequest -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

在删除之前，取消所有正在运行的 OpsRequests（操作请求）：

```bash
kubectl delete opsrequest <ops-name> -n <namespace>
```

## 第 2 步：处理终止策略

如果当前的终止策略为 `DoNotTerminate`，则**无法删除** 该集群，必须先对其进行修改。请执行相应的修复操作：

```bash
kubectl patch cluster <cluster-name> -n <namespace> \
  --type merge -p '{"spec":{"terminationPolicy":"Delete"}}'
```

> **警告：** 在将策略从 `DoNotTerminate` 更改为其他值之前，请务必与用户确认。此策略的存在是为了防止生产环境中的集群被意外删除。

如果希望同时删除备份，请使用 `WipeOut` 而不是 `Delete`。

## 第 3 步：删除集群

```bash
kubectl delete cluster <cluster-name> -n <namespace>
```

此过程可能需要一段时间，因为 KubeBlocks 会优雅地关闭数据库实例并清理资源。

## 第 4 步：验证删除结果

确认集群已被成功删除：

```bash
kubectl get cluster <cluster-name> -n <namespace>
```

确认 pods 是否已被终止：

```bash
kubectl get pods -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

预期结果：找不到任何资源。

## 第 5 步：清理残留资源（可选）

### PVCs

如果终止策略为 `DoNotTerminate`（在修复之前），或者由于其他原因仍有 PVCs 存在：

```bash
kubectl get pvc -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

要删除这些 PVCs，请执行以下操作：

```bash
kubectl delete pvc -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

> **注意：** 删除 PVCs 会永久删除数据。如果数据可能还需要，请确保已备份。

### Secrets（密钥）

连接凭据信息可能会保留：

```bash
kubectl get secret -n <namespace> | grep <cluster-name>
```

要删除这些密钥，请执行以下操作：

```bash
kubectl delete secret -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

### ConfigMaps

```bash
kubectl get configmap -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

要删除这些 ConfigMaps，请执行以下操作：

```bash
kubectl delete configmap -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

## 故障排除

**集群删除过程中卡住（停留在 “Deleting” 状态）：**
- 检查 finalizers：`kubectl get cluster <cluster-name> -n <namespace> -o jsonpath="{.metadata.finalizers}'`
- 查看 KubeBlocks 控制器的日志：`kubectl logs -n kb-system -l app.kubernetes.io/name=kubeblocks --tail=50`

**如果终止策略为 `DoNotTerminate` 但用户忘记了这一设置：**
- `kubectl delete` 命令会返回错误。请先修复策略（步骤 2）。

**删除后仍有 PVCs 存在：**
- 如果终止策略为 `DoNotTerminate`，这是正常现象。请在步骤 5 中清理这些 PVCs。

有关代理的安全性最佳实践（如预测试、状态确认、生产环境保护等），请参阅 [safety-patterns.md](../../references/safety-patterns.md)。