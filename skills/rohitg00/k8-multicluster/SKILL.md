---
name: k8s-multicluster
description: 管理多个 Kubernetes 集群，切换上下文，并执行跨集群操作。适用于需要处理多个集群、比较不同环境或管理集群生命周期的场景。
---

# 多集群Kubernetes管理

使用`kubectl-mcp-server`的多集群支持进行跨集群操作和上下文管理。

## 上下文管理

### 列出可用上下文
```
list_contexts_tool()
```

### 查看当前上下文
```
kubeconfig_view()  # Shows sanitized kubeconfig
```

### 切换上下文
CLI：`kubectl-mcp-server context <上下文名称>`

## 跨集群操作

所有`kubectl-mcp-server`工具都支持`context`参数：

```python
# Get pods from production cluster
get_pods(namespace="default", context="production-cluster")

# Get pods from staging cluster
get_pods(namespace="default", context="staging-cluster")
```

## 常见的多集群模式

### 比较环境
```
# Compare deployment across clusters
compare_namespaces(
    namespace1="production",
    namespace2="staging",
    resource_type="deployment",
    context="production-cluster"
)
```

### 并发查询
同时查询多个集群：
```
# Production cluster
get_pods(namespace="app", context="prod-us-east")
get_pods(namespace="app", context="prod-eu-west")

# Development cluster
get_pods(namespace="app", context="development")
```

### 跨集群健康检查
```
# Check all clusters
for context in ["prod-1", "prod-2", "staging"]:
    get_nodes(context=context)
    get_pods(namespace="kube-system", context=context)
```

## 集群API（CAPI）管理

用于管理集群生命周期：

### 列出管理的集群
```
capi_clusters_list_tool(namespace="capi-system")
```

### 获取集群详细信息
```
capi_cluster_get_tool(name="prod-cluster", namespace="capi-system")
```

### 获取工作负载集群的Kubeconfig文件
```
capi_cluster_kubeconfig_tool(name="prod-cluster", namespace="capi-system")
```

### 机器管理
```
capi_machines_list_tool(namespace="capi-system")
capi_machinedeployments_list_tool(namespace="capi-system")
```

### 扩展集群
```
capi_machinedeployment_scale_tool(
    name="prod-cluster-md-0",
    namespace="capi-system",
    replicas=5
)
```

有关详细模式，请参阅[CONTEXT-SWITCHING.md](CONTEXT-SWITCHING.md)。

## 多集群Helm

将Helm图表部署到特定集群：
```
install_helm_chart(
    name="nginx",
    chart="bitnami/nginx",
    namespace="web",
    context="production-cluster"
)

list_helm_releases(
    namespace="web",
    context="staging-cluster"
)
```

## 多集群GitOps

### 在集群间传输数据流
```
flux_kustomizations_list_tool(
    namespace="flux-system",
    context="cluster-1"
)

flux_reconcile_tool(
    kind="kustomization",
    name="apps",
    namespace="flux-system",
    context="cluster-2"
)
```

### 在集群间使用ArgoCD
```
argocd_apps_list_tool(namespace="argocd", context="management-cluster")
```

## 联邦模式

### 机密同步
```
# Read from source cluster
get_secrets(namespace="app", context="source-cluster")

# Apply to target cluster (via manifest)
apply_manifest(secret_manifest, namespace="app", context="target-cluster")
```

### 跨集群服务发现
使用Cilium ClusterMesh或Istio实现多集群服务发现：
```
cilium_nodes_list_tool(context="cluster-1")
istio_proxy_status_tool(context="cluster-2")
```

## 最佳实践

1. **命名规范**：使用描述性的上下文名称
   - `prod-us-east-1`、`staging-eu-west-1`

2. **访问控制**：为每个环境配置不同的Kubeconfig文件
   - 生产环境：大多数用户仅具有读取权限
   - 开发环境：开发人员具有完全访问权限

3. **始终指定上下文**：避免意外进行跨集群操作
   ```
   # Explicit is better
   get_pods(namespace="app", context="production")
   ```

4. **集群分组**：按用途进行分类
   - 生产环境：`prod-*`
   - 预发布环境：`staging-*`
   - 开发环境：`dev-*`

## 相关技能
- [k8s-troubleshoot](../k8s-troubleshoot/SKILL.md) - 跨集群调试
- [k8s-gitops](../k8s-gitops/SKILL.md) - 多集群GitOps操作