---
name: kubeblocks-expose-service
metadata:
  version: "0.1.0"
description: 通过 `ExposeOpsRequest`，可以使用 LoadBalancer 或 NodePort 服务将 KubeBlocks 数据库集群暴露到外部。该功能提供了针对 AWS NLB、Azure LB、GCP 和 Alibaba Cloud 的云平台特定配置选项。当用户需要从 Kubernetes 集群外部访问数据库、将服务公开到外部网络、建立外部连接或创建公共端点时，可以使用此功能。**请注意：**此功能不适用于配置内部的 ClusterIP 服务（这是默认行为），也不适用于设置连接所需的 TLS 安全机制（请参阅 `configure-tls`）。
---
# 将数据库服务公开给外部访问

## 概述

默认情况下，KubeBlocks 数据库集群仅能在 Kubernetes 集群内部访问。可以使用 `Expose` 操作请求（OpsRequest）通过 LoadBalancer 或 NodePort 创建面向外部的服务，从而允许外部访问。

官方文档：https://kubeblocks.io/docs/preview/user_docs/connect-databases/expose-database-service

## 预检

在继续之前，请确认集群运行正常且没有其他操作正在执行：

```bash
# Cluster must be Running
kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.status.phase}'

# No pending OpsRequests
kubectl get opsrequest -n <namespace> -l app.kubernetes.io/instance=<cluster-name> --field-selector=status.phase!=Succeed
```

如果集群未处于“运行”状态或有未完成的操作请求，请等待其完成后再进行下一步。

检查集群中的现有服务：

```bash
kubectl get svc -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

## 工作流程

```
- [ ] Step 1: Choose exposure method
- [ ] Step 2: Create Expose OpsRequest
- [ ] Step 3: Verify external service
- [ ] Step 4: Connect from outside
```

## 第一步：选择公开方式

| 公开方式 | 使用场景 | 要求 |
|--------|----------|-------------|
| LoadBalancer | 云环境（AWS、Azure、GCP、Alibaba） | 需要云负载均衡器控制器 |
| NodePort | 本地或私有集群 | 无特殊要求 |

## 第二步：创建公开操作请求（Expose OpsRequest）

### 启用外部访问

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: <cluster>-expose
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: Expose
  expose:
  - componentName: <component>
    switch: Enable
    services:
    - name: <cluster>-<component>-internet
      roleSelector: primary
      serviceType: LoadBalancer
```

- `switch`：`Enable` 表示创建服务；`Disable` 表示删除服务
- `roleSelector`：`primary` 仅公开主节点（建议用于写入操作）
- `serviceType`：`LoadBalancer` 或 `NodePort`

### 云提供商特定配置注释

添加针对不同云提供商的负载均衡器配置注释：

**AWS（网络负载均衡器）：**

```yaml
    services:
    - name: <cluster>-<component>-internet
      roleSelector: primary
      serviceType: LoadBalancer
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-type: nlb
        service.beta.kubernetes.io/aws-load-balancer-internal: "false"
```

**Azure：**

```yaml
    services:
    - name: <cluster>-<component>-internet
      roleSelector: primary
      serviceType: LoadBalancer
      annotations:
        service.beta.kubernetes.io/azure-load-balancer-internal: "false"
```

**GCP：**

```yaml
    services:
    - name: <cluster>-<component>-internet
      roleSelector: primary
      serviceType: LoadBalancer
      annotations:
        networking.gke.io/load-balancer-type: External
```

**阿里云：**

```yaml
    services:
    - name: <cluster>-<component>-internet
      roleSelector: primary
      serviceType: LoadBalancer
      annotations:
        service.beta.kubernetes.io/alibaba-cloud-loadbalancer-address-type: internet
```

### NodePort（适用于本地/私有集群）

```yaml
    services:
    - name: <cluster>-<component>-nodeport
      roleSelector: primary
      serviceType: NodePort
```

在应用配置之前，请先进行模拟测试（dry-run）：

```bash
kubectl apply -f expose-ops.yaml --dry-run=server
```

如果模拟测试报告错误，请修复 YAML 文件后再继续。

应用配置：

```bash
kubectl apply -f expose-ops.yaml
kubectl get ops <cluster>-expose -n <ns> -w
```

> **成功条件**：`.status.phase` = `Succeed` | **通常耗时**：1-2 分钟 | **如果超过 5 分钟仍未完成**：`kubectl describe ops <cluster>-expose -n <ns>`

### 禁用外部访问

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: <cluster>-unexpose
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: Expose
  expose:
  - componentName: <component>
    switch: Disable
    services:
    - name: <cluster>-<component>-internet
      roleSelector: primary
      serviceType: LoadBalancer
```

## 第三步：验证外部服务是否可用

```bash
kubectl get svc -n <ns> | grep internet
```

**LoadBalancer 的预期输出：**

```
mycluster-mysql-internet   LoadBalancer   10.96.x.x   a1b2c3.elb.amazonaws.com   3306:30123/TCP   2m
```

等待 `EXTERNAL-IP` 被分配（在云服务提供商上可能需要 1-2 分钟）。

**NodePort 的验证方法：**

```bash
kubectl get svc -n <ns> | grep nodeport
```

```
mycluster-mysql-nodeport   NodePort   10.96.x.x   <none>   3306:31234/TCP   2m
```

## 第四步：从外部连接

### 使用 LoadBalancer 连接

```bash
# MySQL
mysql -h <EXTERNAL-IP> -P 3306 -u root -p

# PostgreSQL
psql -h <EXTERNAL-IP> -p 5432 -U postgres

# Redis
redis-cli -h <EXTERNAL-IP> -p 6379 -a <password>

# MongoDB
mongosh mongodb://<user>:<password>@<EXTERNAL-IP>:27017
```

### 使用 NodePort 连接

```bash
# Use any node's IP + the assigned NodePort
mysql -h <NODE-IP> -P <NODE-PORT> -u root -p
```

获取节点的 IP 地址：

```bash
kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="ExternalIP")].address}'
```

## 故障排除

**LoadBalancer 的 `EXTERNAL-IP` 状态仍为 `<pending>`：**
- 确保云负载均衡器控制器正在运行
- 检查云提供商的配额限制
- 对于本地集群，可以考虑使用 MetalLB 或切换到 NodePort 公开方式

**连接超时：**
- 检查云提供商的安全组/防火墙规则
- 确认服务指向的 Pod 是正常的：`kubectl describe svc <svc-name> -n <ns>`
- 确保数据库正在指定的端口上监听请求

## 额外资源

有关完整的云提供商配置注释、如何公开读复制副本、在没有云负载均衡器的情况下进行本地开发（使用 MetalLB 或端口转发），以及安全注意事项，请参阅 [reference.md](references/reference.md)。

有关代理安全最佳实践（模拟测试、状态确认、生产环境保护措施），请参阅 [safety-patterns.md](../../references/safety-patterns.md)。