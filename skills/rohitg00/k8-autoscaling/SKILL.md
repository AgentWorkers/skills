---
name: k8s-autoscaling
description: 配置 Kubernetes 的自动扩展功能，可以使用 HPA（Horizontal Pod Autoscaling）、VPA（Vertical Pod Autoscaling）和 KEDA（Kubernetes Deployment Auto Scaling）。这些工具可用于实现 Pod 的水平/垂直扩展、基于事件的扩展以及容量管理。
---

# Kubernetes 自动扩展

使用 HPA（水平 Pod 自动扩展器）、VPA（垂直 Pod 自动扩展器）和 KEDA（事件驱动的自动扩展器），结合 kubectl-mcp-server 工具实现全面的自动扩展功能。

## 快速参考

### HPA（水平 Pod 自动扩展器）

基于 CPU 的基本扩展：
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

应用并验证配置：
```
apply_manifest(hpa_yaml, namespace)
get_hpa(namespace)
```

### VPA（垂直 Pod 自动扩展器）

根据需求自动调整资源请求：
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  updatePolicy:
    updateMode: "Auto"
```

## KEDA（事件驱动的自动扩展器）

### 检查 KEDA 是否已安装
```
keda_detect_tool()
```

### 列出已自动扩展的 Pod 对象
```
keda_scaledobjects_list_tool(namespace)
keda_scaledobject_get_tool(name, namespace)
```

### 列出已自动扩展的作业
```
keda_scaledjobs_list_tool(namespace)
```

### 触发认证过程
```
keda_triggerauths_list_tool(namespace)
keda_triggerauth_get_tool(name, namespace)
```

### 由 KEDA 管理的 HPA
```
keda_hpa_list_tool(namespace)
```

有关触发器配置的详细信息，请参阅 [KEDA-TRIGGERS.md](KEDA-TRIGGERS.md)。

## 常见的 KEDA 触发器类型

### 基于队列的扩展（使用 AWS SQS）
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: sqs-scaler
spec:
  scaleTargetRef:
    name: queue-processor
  minReplicaCount: 0  # Scale to zero!
  maxReplicaCount: 100
  triggers:
  - type: aws-sqs-queue
    metadata:
      queueURL: https://sqs.region.amazonaws.com/...
      queueLength: "5"
```

### 基于 Cron 的扩展
```yaml
triggers:
- type: cron
  metadata:
    timezone: America/New_York
    start: 0 8 * * 1-5   # 8 AM weekdays
    end: 0 18 * * 1-5    # 6 PM weekdays
    desiredReplicas: "10"
```

### 使用 Prometheus 指标进行扩展
```yaml
triggers:
- type: prometheus
  metadata:
    serverAddress: http://prometheus:9090
    metricName: http_requests_total
    query: sum(rate(http_requests_total{app="myapp"}[2m]))
    threshold: "100"
```

## 扩展策略

| 策略 | 工具 | 使用场景 |
|----------|------|----------|
| CPU/内存 | HPA | 流量模式稳定的场景 |
| 自定义指标 | HPA v2 | 使用业务相关指标进行扩展 |
| 事件驱动 | KEDA | 适用于队列处理、Cron 任务等场景 |
| 垂直扩展 | VPA | 根据实际需求调整资源 |
| 扩展至零 | KEDA | 适用于节省成本的空闲工作负载 |

## 优化成本的自动扩展

### 使用 KEDA 将工作负载扩展至零
如何减少空闲工作负载的成本：
```
keda_scaledobjects_list_tool(namespace)
# ScaledObjects with minReplicaCount: 0 can scale to zero
```

### 使用 VPA 自动调整资源需求
如何根据需求自动调整资源：
```
get_resource_recommendations(namespace)
# Apply VPA recommendations
```

### 预测性扩展
如何利用 Cron 触发器处理可预测的扩展需求：
```yaml
# Scale up before traffic spike
triggers:
- type: cron
  metadata:
    start: 0 7 * * *  # 7 AM
    end: 0 9 * * *    # 9 AM
    desiredReplicas: "20"
```

## 多集群自动扩展
如何在多个集群中配置 KEDA：
```
keda_scaledobjects_list_tool(namespace, context="production")
keda_scaledobjects_list_tool(namespace, context="staging")
```

## 故障排除

### HPA 无法自动扩展
如何解决 HPA 无法自动扩展的问题：
```
get_hpa(namespace)
get_pod_metrics(name, namespace)  # Metrics available?
describe_pod(name, namespace)     # Resource requests set?
```

### KEDA 无法触发扩展
如何解决 KEDA 无法触发扩展的问题：
```
keda_scaledobject_get_tool(name, namespace)  # Check status
get_events(namespace)                        # Check events
```

### 常见问题及解决方法

| 问题 | 检查内容 | 解决方法 |
|---------|-------|------------|
| HPA 无法正常工作 | 确保已安装指标服务器 | 安装并配置指标服务器 |
| KEDA 无法触发扩展 | 检查认证配置 | 确保 TriggerAuthentication 配置正确 |
| VPA 无法更新资源配置 | 更改更新模式 | 将 updateMode 设置为 Auto |
| 扩展速度过慢 | 调整 stabilizationWindowSeconds 参数 | 增加稳定时间 |

## 最佳实践

1. **务必设置资源请求**：
   HPA 需要明确的资源请求才能计算资源利用率。
2. **使用多种指标**：
   结合 CPU 指标和自定义指标以提高扩展的准确性。
3. **设置稳定时间窗口**：
   通过 stabilizationWindowSeconds 参数防止扩展频率波动。
4. **谨慎地将工作负载扩展至零**：
   考虑冷启动时间，并设置合适的激活阈值。

## 相关技能

- [k8s-cost](../k8s-cost/SKILL.md) – 成本优化技巧
- [k8s-troubleshoot](../k8s-troubleshoot/SKILL.md) – 故障排除指南