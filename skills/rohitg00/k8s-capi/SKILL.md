---
name: k8s-capi
description: 集群API生命周期管理功能用于配置、扩展和升级Kubernetes集群。适用于管理集群基础设施或执行多集群操作的场景。
---

# 集群 API 生命周期管理

使用 `kubectl-mcp-server` 的集群 API 工具（共 11 个工具）来管理 Kubernetes 集群。

## 检查安装情况

```python
capi_detect_tool()
```

## 列出集群

```python
# List all CAPI clusters
capi_clusters_list_tool(namespace="default")

# Shows:
# - Cluster name
# - Phase (Provisioning, Provisioned, Deleting)
# - Infrastructure ready
# - Control plane ready
```

## 获取集群详细信息

```python
capi_cluster_get_tool(name="my-cluster", namespace="default")

# Shows:
# - Spec (control plane, infrastructure)
# - Status (phase, conditions)
# - Network configuration
```

## 获取集群的 Kubeconfig 文件

```python
# Get kubeconfig for workload cluster
capi_cluster_kubeconfig_tool(name="my-cluster", namespace="default")

# Returns kubeconfig to access the cluster
```

## 机器资源

### 列出所有机器

```python
capi_machines_list_tool(namespace="default")

# Shows:
# - Machine name
# - Cluster
# - Phase (Running, Provisioning, Failed)
# - Provider ID
# - Version
```

### 获取机器详细信息

```python
capi_machine_get_tool(name="my-cluster-md-0-xxx", namespace="default")
```

## 机器部署

### 列出所有机器部署

```python
capi_machinedeployments_list_tool(namespace="default")

# Shows:
# - Deployment name
# - Cluster
# - Replicas (ready/total)
# - Version
```

### 扩展或缩减机器部署

```python
# Scale worker nodes
capi_machinedeployment_scale_tool(
    name="my-cluster-md-0",
    namespace="default",
    replicas=5
)
```

## 机器组（Machine Sets）

```python
capi_machinesets_list_tool(namespace="default")
```

## 机器健康检查

```python
capi_machinehealthchecks_list_tool(namespace="default")

# Health checks automatically remediate unhealthy machines
```

## 集群类别

```python
# List cluster templates
capi_clusterclasses_list_tool(namespace="default")

# ClusterClasses define reusable cluster configurations
```

## 创建新集群

```python
kubectl_apply(manifest="""
apiVersion: cluster.x-k8s.io/v1beta1
kind: Cluster
metadata:
  name: my-cluster
  namespace: default
spec:
  clusterNetwork:
    pods:
      cidrBlocks:
      - 192.168.0.0/16
    services:
      cidrBlocks:
      - 10.96.0.0/12
  controlPlaneRef:
    apiVersion: controlplane.cluster.x-k8s.io/v1beta1
    kind: KubeadmControlPlane
    name: my-cluster-control-plane
  infrastructureRef:
    apiVersion: infrastructure.cluster.x-k8s.io/v1beta1
    kind: AWSCluster
    name: my-cluster
""")
```

## 创建新的机器部署

```python
kubectl_apply(manifest="""
apiVersion: cluster.x-k8s.io/v1beta1
kind: MachineDeployment
metadata:
  name: my-cluster-md-0
  namespace: default
spec:
  clusterName: my-cluster
  replicas: 3
  selector:
    matchLabels:
      cluster.x-k8s.io/cluster-name: my-cluster
  template:
    spec:
      clusterName: my-cluster
      version: v1.28.0
      bootstrap:
        configRef:
          apiVersion: bootstrap.cluster.x-k8s.io/v1beta1
          kind: KubeadmConfigTemplate
          name: my-cluster-md-0
      infrastructureRef:
        apiVersion: infrastructure.cluster.x-k8s.io/v1beta1
        kind: AWSMachineTemplate
        name: my-cluster-md-0
""")
```

## 集群生命周期工作流

### 配置新集群
```python
1. kubectl_apply(cluster_manifest)
2. capi_clusters_list_tool(namespace)  # Wait for Provisioned
3. capi_cluster_kubeconfig_tool(name, namespace)  # Get access
```

### 扩展工作节点数量
```python
1. capi_machinedeployments_list_tool(namespace)
2. capi_machinedeployment_scale_tool(name, namespace, replicas)
3. capi_machines_list_tool(namespace)  # Monitor
```

### 升级集群
```python
1. # Update control plane version
2. # Update machine deployment version
3. capi_machines_list_tool(namespace)  # Monitor rollout
```

## 故障排除

### 集群配置失败
```python
1. capi_cluster_get_tool(name, namespace)  # Check conditions
2. capi_machines_list_tool(namespace)  # Check machine status
3. get_events(namespace)  # Check events
4. # Check infrastructure provider logs
```

### 机器运行异常
```python
1. capi_machine_get_tool(name, namespace)
2. get_events(namespace)
3. # Common issues:
   # - Cloud provider quota
   # - Invalid machine template
   # - Network issues
```

## 相关技能

- [k8s-multicluster](../k8s-multicluster/SKILL.md) - 多集群操作
- [k8s-operations](../k8s-operations/SKILL.md) - kubectl 命令操作