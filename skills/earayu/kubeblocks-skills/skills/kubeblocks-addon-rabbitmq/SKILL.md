---
name: kubeblocks-addon-rabbitmq
metadata:
  version: "0.1.0"
description: 在 KubeBlocks 上部署和管理 RabbitMQ 集群。RabbitMQ 是一个开源的消息代理服务器，支持 AMQP、MQTT 和 STOMP 协议。当用户提到 RabbitMQ、消息代理服务器、AMQP 或消息队列时，或者明确表示需要创建一个 RabbitMQ 集群时，可以使用该功能。该功能提供集群创建、连接方法（通过管理界面或 rabbitmqctl 命令）以及后续的运维操作。如需在所有引擎上创建通用集群，请参考 `kubeblocks-create-cluster`；如需进行扩展等后续运维操作，请使用相应的运维技能。
---
# 在 KubeBlocks 上部署 RabbitMQ

## 概述

使用 KubeBlocks 在 Kubernetes 上部署 RabbitMQ 集群。RabbitMQ 是一个轻量级的消息代理，支持 AMQP、MQTT 和 STOMP 协议。多个副本共同构成一个集群，该集群具备队列镜像和法定投票（quorum）功能。默认端口如下：5672（AMQP）、15672（管理界面）、15692（Prometheus 监控指标）。

官方文档：https://kubeblocks.io/docs/preview/kubeblocks-for-rabbitmq/01-overview  
快速入门：https://kubeblocks.io/docs/preview/kubeblocks-for-rabbitmq/02-quickstart

## 先决条件

- 已经安装了 KubeBlocks 的运行中的 Kubernetes 集群（请参阅 [install-kubeblocks](../kubeblocks-install/SKILL.md)）  
- 必须启用 RabbitMQ 插件：

```bash
# Check if rabbitmq addon is installed
helm list -n kb-system | grep rabbitmq

# Install if missing
helm install kb-addon-rabbitmq kubeblocks/rabbitmq --namespace kb-system --version 1.0.0
```

## 架构拓扑

| 拓扑类型 | 参数 | 组件 | 适用场景 |
|---|---|---|---|
| 集群模式 | `clustermode` | rabbitmq | 单一架构；多个副本构成集群，并支持队列镜像和法定投票功能 |

## 支持的版本

| 版本 | 对应的 serviceVersion |  
|---|---|
| RabbitMQ 3.8 | `3.8.34` |  
| RabbitMQ 3.9 | `3.9.29` |  
| RabbitMQ 3.10 | `3.10.25` |  
| RabbitMQ 3.11 | `3.11.28` |  
| RabbitMQ 3.12 | `3.12.14` |  
| RabbitMQ 3.13 | `3.13.7` |  
| RabbitMQ 4.0 | `4.0.9` |  
| RabbitMQ 4.1 | `4.1.6` |  
| RabbitMQ 4.2 | `4.2.1` |  

可用版本列表：`kubectl get cmpv rabbitmq`

## 工作流程

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster (dry-run, then apply)
- [ ] Step 4: Wait for cluster to be ready
- [ ] Step 5: Connect (Management UI or rabbitmqctl)
```

## 第一步：确保插件已安装

```bash
helm list -n kb-system | grep rabbitmq
```

如果插件未安装，请执行相应的安装步骤：

```bash
helm install kb-addon-rabbitmq kubeblocks/rabbitmq --namespace kb-system --version 1.0.0
```

## 第二步：创建命名空间

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```

## 第三步：创建集群

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: rabbitmq-cluster
  namespace: demo
spec:
  clusterDef: rabbitmq
  topology: clustermode
  terminationPolicy: Delete
  componentSpecs:
    - name: rabbitmq
      serviceVersion: "3.13.7"
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

**应用前的测试（Dry-run）：**

```bash
kubectl apply -f cluster.yaml --dry-run=server
```

如果测试成功，则可以继续下一步：

```bash
kubectl apply -f cluster.yaml
```

## 第四步：等待集群准备就绪

```bash
kubectl -n demo get cluster rabbitmq-cluster -w
```

**成功条件：** 集群状态显示为 `Running`。通常需要 1-2 分钟完成部署。如果超过 10 分钟仍未完成，请检查集群状态。

检查集群中的 Pod：  

```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=rabbitmq-cluster
```

## 第五步：连接集群

### 通过管理界面进行连接（使用端口转发）

凭据存储在 Secret 中，格式为 `<clusterName>-<componentName>-account-root`（例如：`rabbitmq-cluster-rabbitmq-account-root`）：

```bash
# Get credentials
NAME=$(kubectl get secrets -n demo rabbitmq-cluster-rabbitmq-account-root -o jsonpath='{.data.username}' | base64 -d)
PASSWD=$(kubectl get secrets -n demo rabbitmq-cluster-rabbitmq-account-root -o jsonpath='{.data.password}' | base64 -d)

# Port-forward Management UI (port 15672)
kubectl port-forward svc/rabbitmq-cluster-rabbitmq -n demo 15672:15672
```

使用这些凭据访问 `http://localhost:15672` 并登录。

### 使用 `rabbitmqctl`（命令行工具）

```bash
kubectl -n demo exec -it rabbitmq-cluster-rabbitmq-0 -- rabbitmqctl cluster_status
```

## 故障排除

**集群创建失败：**
```bash
kubectl -n demo describe cluster rabbitmq-cluster
kubectl -n demo get events --sort-by='.lastTimestamp'
```

**Pod 无法启动：**
```bash
kubectl -n demo logs rabbitmq-cluster-rabbitmq-0
```

**集群组建问题：**
- 确保副本数量为奇数（例如 3、5、7 个，以满足法定投票要求）  
- 检查节点间的通信是否正常；KubeBlocks 会创建具有必要权限的安全账户（SA）  

## 日常维护操作

| 操作 | 所需技能 | 外部文档参考 |  
|---|---|---|
| 停止/启动/重启集群 | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-rabbitmq/04-operations/01-stop-start-restart) |
| 调整 CPU/内存资源 | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-rabbitmq/04-operations/02-vertical-scaling) |
| 增加/减少副本数量 | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-rabbitmq/04-operations/03-horizontal-scaling) |
| 扩展存储空间 | [volume-expansion](../kubeblocks-volume-expansion/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-rabbitmq/04-operations/04-volume-expansion) |
| 将集群服务公开给外部访问 | [expose-service](../kubeblocks-expose-service/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-rabbitmq/04-operations/) |

## 安全最佳实践

请遵循 [安全最佳实践](../../references/safety-patterns.md)：在正式应用前进行测试，应用完成后确认集群状态，并在删除集群前执行必要的检查流程。