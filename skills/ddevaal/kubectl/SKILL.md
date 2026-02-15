---
name: kubectl-skill
description: 通过 `kubectl` 命令来执行和管理 Kubernetes 集群。可以查询资源、部署应用程序、调试容器、管理配置以及监控集群的健康状况。适用于处理 Kubernetes 集群、容器、部署任务或 Pod 相关的诊断工作。
license: MIT
metadata:
  author: Dennis de Vaal <d.devaal@gmail.com>
  version: "1.0.0"
  keywords: "kubernetes,k8s,container,docker,deployment,pods,cluster"
compatibility: Requires kubectl binary (v1.20+) and active kubeconfig connection to a Kubernetes cluster. Works on macOS, Linux, and Windows (WSL).
---

# kubectl 技能

使用 `kubectl` 命令行工具执行 Kubernetes 集群管理操作。

## 概述

此技能使代理能够：
- **查询资源** — 列出并获取有关Pod、部署、服务、节点等的信息
- **部署和更新** — 创建、应用、修补和更新Kubernetes资源
- **调试和故障排除** — 查看日志、在容器中执行命令、检查事件
- **管理配置** — 更新kubeconfig文件、切换上下文、管理命名空间
- **监控健康状况** — 检查资源使用情况、滚动发布状态、事件和Pod状态
- **执行操作** — 扩展部署、释放节点、管理污点和标签

## 先决条件

1. 已安装 `kubectl` 可执行文件，并且可以在 `PATH` 中找到（版本要求：v1.20+）
2. `kubeconfig` 文件已配置集群凭据（默认位置：`~/.kube/config`）
3. 与Kubernetes集群保持活动连接

## 快速设置

### 安装 kubectl

**macOS:**
```bash
brew install kubernetes-cli
```

**Linux:**
```bash
apt-get install -y kubectl  # Ubuntu/Debian
yum install -y kubectl      # RHEL/CentOS
```

**验证安装：**
```bash
kubectl version --client
kubectl cluster-info  # Test connection
```

## 必需命令

### 查询资源
```bash
kubectl get pods                    # List all pods in current namespace
kubectl get pods -A                 # All namespaces
kubectl get pods -o wide            # More columns
kubectl get nodes                   # List nodes
kubectl describe pod POD_NAME        # Detailed info with events
```

### 查看日志
```bash
kubectl logs POD_NAME                # Get logs
kubectl logs -f POD_NAME             # Follow logs (tail -f)
kubectl logs POD_NAME -c CONTAINER   # Specific container
kubectl logs POD_NAME --previous     # Previous container logs
```

### 执行命令
```bash
kubectl exec -it POD_NAME -- /bin/bash   # Interactive shell
kubectl exec POD_NAME -- COMMAND         # Run single command
```

### 部署应用程序
```bash
kubectl apply -f deployment.yaml         # Apply config
kubectl create -f deployment.yaml        # Create resource
kubectl apply -f deployment.yaml --dry-run=client  # Test
```

### 更新应用程序
```bash
kubectl set image deployment/APP IMAGE=IMAGE:TAG  # Update image
kubectl scale deployment/APP --replicas=3          # Scale pods
kubectl rollout status deployment/APP              # Check status
kubectl rollout undo deployment/APP                # Rollback
```

### 管理配置
```bash
kubectl config view                  # Show kubeconfig
kubectl config get-contexts          # List contexts
kubectl config use-context CONTEXT   # Switch context
```

## 常见用法

### 调试Pod
```bash
# 1. Identify the issue
kubectl describe pod POD_NAME

# 2. Check logs
kubectl logs POD_NAME
kubectl logs POD_NAME --previous

# 3. Execute debug commands
kubectl exec -it POD_NAME -- /bin/bash

# 4. Check events
kubectl get events --sort-by='.lastTimestamp'
```

### 部署新版本
```bash
# 1. Update image
kubectl set image deployment/MY_APP my-app=my-app:v2

# 2. Monitor rollout
kubectl rollout status deployment/MY_APP -w

# 3. Verify
kubectl get pods -l app=my-app

# 4. Rollback if needed
kubectl rollout undo deployment/MY_APP
```

### 为维护准备节点
```bash
# 1. Drain node (evicts all pods)
kubectl drain NODE_NAME --ignore-daemonsets

# 2. Do maintenance
# ...

# 3. Bring back online
kubectl uncordon NODE_NAME
```

## 输出格式

`--output`（`-o`）标志支持多种格式：
- `table` — 默认的表格格式
- `wide` — 带有额外列的扩展表格格式
- `json` — JSON格式（适用于 `jq` 工具）
- `yaml` — YAML格式
- `jsonpath` — JSONPath表达式
- `custom-columns` — 定义自定义输出列
- `name` — 仅显示资源名称

**示例：**
```bash
kubectl get pods -o json | jq '.items[0].metadata.name'
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase
```

## 全局标志（所有命令均可使用）

```bash
-n, --namespace=<ns>           # Operate in specific namespace
-A, --all-namespaces           # Operate across all namespaces
--context=<context>            # Use specific kubeconfig context
-o, --output=<format>          # Output format (json, yaml, table, etc.)
--dry-run=<mode>               # Dry-run mode (none, client, server)
-l, --selector=<labels>        # Filter by labels
--field-selector=<selector>    # Filter by fields
-v, --v=<int>                  # Verbosity level (0-9)
```

## 干运行模式

- `--dry-run=client` — 快速的客户端验证（安全地测试命令）
- `--dry-run=server` — 服务器端验证（更准确）
- `--dry-run=none` — 真正执行命令（默认值）

**建议始终先使用 `--dry-run=client` 进行测试：**
```bash
kubectl apply -f manifest.yaml --dry-run=client
```

## 高级主题

有关详细参考资料、命令文档、故障排除指南和高级工作流程，请参阅：
- [references/REFERENCE.md](references/REFERENCE.md) — 完整的 `kubectl` 命令参考
- [scripts/](scripts/) — 用于常见任务的辅助脚本

## 有用的提示

1. **使用标签选择器进行批量操作：**
   ```bash
   kubectl delete pods -l app=myapp
   kubectl get pods -l env=prod,tier=backend
   ```

2. **实时监控资源状态：**
   ```bash
   kubectl get pods -w  # Watch for changes
   ```

3. **使用 `-A` 标志查看所有命名空间中的资源：**
   ```bash
   kubectl get pods -A  # See pods everywhere
   ```

4. **保存输出以供后续比较：**
   ```bash
   kubectl get deployment my-app -o yaml > deployment-backup.yaml
   ```

5. **删除前请先检查：**
   ```bash
   kubectl delete pod POD_NAME --dry-run=client
   ```

## 获取帮助

```bash
kubectl help                      # General help
kubectl COMMAND --help            # Command help
kubectl explain pods              # Resource documentation
kubectl explain pods.spec         # Field documentation
```

## 环境变量

- `KUBECONFIG` — kubeconfig 文件的路径（可以包含多个路径，用冒号分隔）
- `KUBECTL_CONTEXT` — 覆盖默认上下文

## 资源链接

- [官方 kubectl 文档](https://kubernetes.io/docs/reference/kubectl/)
- [kubectl 快速参考](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes API 参考](https://kubernetes.io/docs/reference/generated/kubernetes-api/)
- [代理技能规范](https://agentskills.io/)

---

**版本：** 1.0.0  
**许可证：** MIT  
**兼容版本：** kubectl v1.20+，Kubernetes v1.20+