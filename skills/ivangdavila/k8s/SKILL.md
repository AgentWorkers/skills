---
name: Kubernetes
description: 避免常见的 Kubernetes 错误：资源限制、探针配置问题、选择器不匹配以及基于角色的访问控制（RBAC）的陷阱。
metadata: {"clawdbot":{"emoji":"☸️","requires":{"bins":["kubectl"]},"os":["linux","darwin","win32"]}}
---

## 资源管理  
- `requests`：资源请求的最低限制——调度器会依据此限制来分配资源。  
- `limits`：资源使用的最大限制——超出限制可能导致内存溢出（OOM）或CPU使用受限。  
- 如果不设置 `limits`，则资源可以使用到节点的全部容量——务必为生产环境设置相应的资源限制。  
- 如果只设置 `requests` 而不设置 `limits`，则资源使用是可突发性的（即在有空闲资源时可以额外使用）。  

## 探针（Probes）  
- `readinessProbe`：用于检测 Pod 是否处于可用状态；如果检测失败，该 Pod 会被从服务端点中移除。  
- `livenessProbe`：用于检测 Pod 是否存活；如果检测失败，容器会被重启。  
- `startupProbe`：用于处理启动缓慢的 Pod；在启动成功之前，该探针会阻止对 Pod 的正常访问（包括 `livenessProbe` 和 `readinessProbe` 的检测）。  
- **注意**：不要在同一端点同时使用 `livenessProbe` 和 `readinessProbe`——因为 `livenessProbe` 的主要目的是进行基本的健康检查。  

## 使用探针时的常见陷阱  
- 如果依赖项（如数据库）不可用，所有相关 Pod 可能会无限循环重启。  
- 如果 `initialDelaySeconds` 设置得太短，Pod 可能在应用程序启动之前就被终止。  
- 如果 `timeoutSeconds` 设置得太短，响应缓慢可能导致容器不断重启。  
- 如果探针使用 HTTP 协议访问 HTTPS 端点，需要指定 `scheme: HTTPS`。  

## 标签（Labels）与选择器（Selectors）  
- 服务（Service）的选择器必须与 Pod 的标签完全匹配；否则，服务将无法找到对应的 Pod。  
- 部署（Deployment）的选择器是不可更改的，创建完成后无法修改。  
- 使用统一的标签命名规范（例如 `app`、`version`、`environment`）。  
- 使用 `matchExpressions` 进行复杂的选择：`In`、`NotIn`、`Exists`。  

## ConfigMap 与 Secrets  
- 修改 ConfigMap 的内容不会自动重启 Pod；可以通过挂载为卷（volume）来实现自动更新，或者手动重启 Pod。  
- Secrets 数据采用 Base64 编码，而非加密；对于敏感数据，建议使用外部 Secrets 管理工具。  
- `envFrom` 会导入所有配置项；`env.valueFrom` 用于获取特定的配置项。  
- 卷挂载后，文件会位于指定的 `subPath` 下，而不会替换整个目录。  

## 网络配置（Networking）  
- `ClusterIP`：仅用于集群内部，只能在集群内部访问。  
- `NodePort`：在节点的 IP 上暴露端口（范围为 30000–32767）；不适合生产环境使用。  
- `LoadBalancer`：用于配置云负载均衡器（Cloud LoadBalancer），仅在支持的环境中有效。  
- Ingress 需要额外的 Ingress Controller（例如 nginx-ingress、traefik 等）来处理外部请求。  

## 持久化存储（Persistent Storage）  
- PVC（Persistent Volume Claim）必须与对应的 PV（Persistent Volume）匹配，包括容量和访问模式。  
- `storageClassName` 必须匹配；如果不设置，则表示不进行动态资源分配。  
- `ReadWriteOnce`：适用于单 Pod 的存储策略；`ReadWriteMany` 适用于多 Pod 的存储需求。  
- 删除 Pod 不会自动删除对应的 PVC；`persistentVolumeReclaimPolicy` 决定 PVC 的最终处理方式。  

## 常见错误  
- `kubectl apply` 用于声明性配置（可以更新现有资源），而 `create` 用于创建新资源（如果资源已存在则会失败）。  
- 忘记指定命名空间（使用 `-n namespace` 或设置默认上下文）。  
- 在生产环境中使用 `latest` 作为镜像标签会导致版本不可预测的更新。  
- 未设置 `imagePullPolicy`：使用 `Always` 表示总是拉取最新版本的镜像；`IfNotPresent` 表示仅拉取指定版本的镜像。  
- 注意 `Service` 的端口（`servicePort`）与容器内的端口（`targetPort`）的区别。  

## 调试（Debugging）  
- 使用 `kubectl describe pod` 查看 Pod 的相关事件（包括调度失败和探针失败信息）。  
- 使用 `kubectl logs -f pod` 查看 Pod 的日志（使用 `-p` 可查看容器崩溃后的日志）。  
- 使用 `kubectl exec -it pod -- sh` 在容器内部执行命令进行调试。  
- 使用 `kubectl get events --sort-by=.lastTimestamp` 查看集群范围内的事件时间线。  

## RBAC（Role-Based Access Control）  
- 每个工作负载都应该使用独立的 `ServiceAccount`，以最小化权限风险。  
- `Role` 是基于命名空间的；`ClusterRole` 是全局范围内的。  
- `RoleBinding` 将 `Role` 绑定到具体的用户/ServiceAccount；`ClusterRoleBinding` 用于全局范围内的权限控制。  
- 检查权限：`kubectl auth can-i verb resource --as=system:serviceaccount:ns:sa`