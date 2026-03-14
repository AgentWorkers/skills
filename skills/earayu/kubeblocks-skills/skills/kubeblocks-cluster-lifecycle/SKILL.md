---
name: kubeblocks-cluster-lifecycle
metadata:
  version: "0.1.0"
description: "管理 KubeBlocks 集群生命周期：通过 OpsRequest 命令停止、启动或重启数据库集群。停止操作会终止所有 Pod，但会保留 PVC（Persistent Volume Claims）以节省成本。此功能适用于用户需要临时停止、启动、重启、暂停或关闭数据库集群的场景。请注意：该功能不用于永久删除集群（请参阅 `delete-cluster`），也不适用于集群扩展操作（请参阅 `vertical-scaling` 和 `horizontal-scaling`）。"
---
# 管理集群生命周期：停止、启动、重启

## 概述

KubeBlocks 支持通过 `OpsRequest` CR（Custom Resource）来停止、启动和重启数据库集群。停止集群会终止所有 Pod，同时保留 PVC（Persistent Volume Claim），从而在集群不使用时节省成本。

官方文档：https://kubeblocks.io/docs/preview/user_docs/maintenance/stop-start-a-cluster  
完整文档索引：https://kubeblocks.io/llms-full.txt  

## 工作流程  

### 第一步：检查当前集群状态  

```
- [ ] Step 1: Check current cluster status
- [ ] Step 2: Apply the lifecycle operation (Stop / Start / Restart)
- [ ] Step 3: Verify the operation
```  

| 状态 | 含义 |  
|--------|---------|  
| `Running` | 集群运行正常，正在处理请求。可以停止或重启。 |  
| `Stopped` | 集群中的 Pod 已终止，但 PVC 仍然保留。可以重新启动。 |  
| `Updating` | 操作正在进行中。请等待操作完成。 |  

### 第二步：执行生命周期操作  

#### 停止集群  

停止集群中的所有 Pod。PVC 会被保留，因此数据不会丢失。  

**`OpsRequest` 方法：**  
```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: stop-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: Stop
```  

在应用操作之前，请先进行干运行（dry-run）验证：  
```bash
kubectl apply -f - --dry-run=server <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: stop-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: Stop
EOF
```  

如果干运行报告错误，请修复 YAML 文件后再继续操作。  

#### 备选方法——使用 `kubectl patch`：**  
```bash
kubectl patch cluster <cluster-name> -n <namespace> \
  --type merge -p '{"spec":{"componentSpecs":[{"name":"<component-name>","stop":true}]}}'
```  
> 将 `<component-name>` 替换为相应的组件名称（例如：`mysql`、`postgresql`、`redis`、`mongodb`、`kafka-combine`）。  

#### 启动集群  

从保留的 PVC 中重新创建 Pod，使集群恢复到之前的状态。  

**`OpsRequest` 方法：**  
```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: start-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: Start
```  

在应用操作之前，请先进行干运行验证：  
```bash
kubectl apply -f - --dry-run=server <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: start-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: Start
EOF
```  

如果干运行报告错误，请修复 YAML 文件后再继续操作。  

#### 备选方法——使用 `kubectl patch`：**  
```bash
kubectl patch cluster <cluster-name> -n <namespace> \
  --type merge -p '{"spec":{"componentSpecs":[{"name":"<component-name>","stop":false}]}}'
```  

#### 重启集群  

对指定的组件执行滚动重启（rolling restart）。Pod 会依次重启，以确保集群的可用性。  

**`OpsRequest` 方法：**  
```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: restart-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: Restart
  restart:
    - componentName: <component-name>
```  

在应用操作之前，请先进行干运行验证：  
```bash
kubectl apply -f - --dry-run=server <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: restart-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: Restart
  restart:
    - componentName: <component-name>
EOF
```  

如果干运行报告错误，请修复 YAML 文件后再继续操作。  

#### 注意：`componentName` 的具体值取决于所使用的组件。常见值如下：  
- MySQL：`mysql`  
- PostgreSQL：`postgresql`  
- Redis：`redis`  
- MongoDB：`mongodb`  
- Kafka：`kafka-combine`（组合拓扑）或 `kafka-broker` / `kafka-controller`（独立拓扑）  

您可以通过在 `restart` 列表中添加更多条目来重启多个组件。  

### 第三步：验证操作结果  

#### 监控 `OpsRequest` 的执行进度  

```bash
kubectl get ops -n <namespace> -w
```  
- **成功条件**：`.status.phase` = `Succeed`  
- **通常耗时**：1-3 分钟  
- **如果超过 5 分钟仍未完成**：`kubectl describe ops <ops-name> -n <namespace>`  

预期状态变化：`Pending` → `Running` → `Succeed`  

#### 检查集群状态  

```bash
kubectl get cluster <cluster-name> -n <namespace> -w
```  
- **停止操作成功**：`.status.phase` = `Stopped`  
- **启动/重启操作成功**：`.status.phase` = `Running`  
- **通常耗时**：1-3 分钟  
- **如果超过 5 分钟仍未完成**：`kubectl describe cluster <cluster-name> -n <namespace>`  

- **停止操作后**：状态变为 `Stopped`，所有 Pod 都会被终止。  
- **启动操作后**：状态变为 `Running`，所有 Pod 都会被重新创建。  
- **重启操作后**：状态会短暂显示 `Updating`，随后恢复为 `Running`。  

#### 检查 Pod 的状态  

```bash
kubectl get pods -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```  
- **停止操作后**：应看不到任何 Pod。  
- **启动/重启操作后**：所有 Pod 都应处于 `Running` 状态。  

## 故障排除  

- **`OpsRequest` 操作长时间处于 `Running` 状态**：  
  - 查看 `OpsRequest` 的事件日志：`kubectl describe ops <ops-name> -n <namespace>`  
  - 查看 KubeBlocks 控制器的日志：`kubectl logs -n kb-system -l app.kubernetes.io/name=kubeblocks --tail=50`  

- **停止操作后无法成功启动集群**：  
  - 确保 PVC 仍然存在：`kubectl get pvc -n <namespace> -l app.kubernetes.io/instance=<cluster-name>`  
  - 如果 PVC 被手动删除，则无法启动集群，需要重新创建集群。  

- **重启操作耗时过长**：  
  - 滚动重启是按顺序进行的。对于大型集群，每次只重启一个 Pod。  
  - 检查 Pod 的状态：`kubectl describe pod <pod-name> -n <namespace>`  

## 额外资源  

有关各组件的名称、`kubectl patch` 的使用方法、集群状态的变化以及成本优化策略，请参阅 [reference.md](references/reference.md)。  
有关代理的安全使用规范（如干运行、状态确认、生产环境保护措施），请参阅 [safety-patterns.md](../../references/safety-patterns.md)。