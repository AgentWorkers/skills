---
name: k8s-manifest-generator
model: fast
description: 根据最佳实践和安全标准，为 Deployment（部署）、Service（服务）、ConfigMap（配置映射）和 Secret（密钥）创建可用于生产环境的 Kubernetes 配置文件。在生成 Kubernetes YAML 配置文件、创建 Kubernetes 资源或实施生产级 Kubernetes 配置时，请使用这些文件。
---

# Kubernetes 清单生成器

本文档提供了创建适用于生产环境的 Kubernetes 清单的逐步指导，包括 Deployment（部署）、Service（服务）、ConfigMap（配置映射）、Secret（密钥）和 PersistentVolumeClaim（持久卷声明）的创建方法。

## 目的

本技能提供了全面的指导，帮助您按照云原生最佳实践和 Kubernetes 规范生成结构良好、安全且适用于生产环境的 Kubernetes 清单。

## 适用场景

当您需要以下操作时，请使用本技能：
- 创建新的 Kubernetes Deployment 清单
- 定义用于网络连接的服务资源
- 生成用于配置管理的 ConfigMap 和 Secret 资源
- 为有状态的工作负载创建 PersistentVolumeClaim 清单
- 遵循 Kubernetes 的最佳实践和命名规范
- 实现资源限制、健康检查和安全上下文
- 为多环境部署设计清单

## 逐步工作流程

### 1. 收集需求

**了解工作负载需求：**
- 应用程序类型（无状态/有状态）
- 容器镜像及其版本
- 环境变量和配置需求
- 存储需求
- 网络访问需求（内部/外部）
- 资源需求（CPU、内存）
- 扩展需求
- 健康检查端点

**需要询问的问题：**
- 应用程序的名称和用途是什么？
- 将使用哪个容器镜像及其标签？
- 应用程序是否需要持久化存储？
- 应用程序会暴露哪些端口？
- 是否需要任何密钥或配置文件？
- CPU 和内存需求是什么？
- 应用程序是否需要外部访问？

### 2. 创建 Deployment 清单

**遵循以下结构：**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <app-name>
  namespace: <namespace>
  labels:
    app: <app-name>
    version: <version>
spec:
  replicas: 3
  selector:
    matchLabels:
      app: <app-name>
  template:
    metadata:
      labels:
        app: <app-name>
        version: <version>
    spec:
      containers:
        - name: <container-name>
          image: <image>:<tag>
          ports:
            - containerPort: <port>
              name: http
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
          env:
            - name: ENV_VAR
              value: "value"
          envFrom:
            - configMapRef:
                name: <app-name>-config
            - secretRef:
                name: <app-name>-secret
```

**最佳实践：**
- 始终设置资源请求和限制
- 实现 liveness（存活检查）和 readiness（就绪检查）
- 使用具体的镜像标签（避免使用 `:latest`）
- 为非 root 用户应用安全上下文
- 使用标签进行组织和筛选
- 根据可用性需求设置适当的副本数量

**参考：**请参阅 `references/deployment-spec.md` 以获取详细的部署选项

### 3. 创建 Service 清单

**选择合适的服务类型：**
- **ClusterIP（仅限内部访问）：**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: <app-name>
  namespace: <namespace>
  labels:
    app: <app-name>
spec:
  type: ClusterIP
  selector:
    app: <app-name>
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
```

****LoadBalancer（外部访问）：**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: <app-name>
  namespace: <namespace>
  labels:
    app: <app-name>
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
spec:
  type: LoadBalancer
  selector:
    app: <app-name>
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
```

**参考：**请参阅 `references/service-spec.md` 以了解服务类型和网络配置

### 4. 创建 ConfigMap

**用于应用程序配置：**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: <app-name>-config
  namespace: <namespace>
data:
  APP_MODE: production
  LOG_LEVEL: info
  DATABASE_HOST: db.example.com
  # For config files
  app.properties: |
    server.port=8080
    server.host=0.0.0.0
    logging.level=INFO
```

**最佳实践：**
- 仅将非敏感数据存储在 ConfigMap 中
- 将相关配置集中在一起
- 为键使用有意义的名称
- 每个组件使用一个 ConfigMap
- 在进行更改时为 ConfigMap 设置版本

**参考：**请参阅 `assets/configmap-template.yaml` 以获取示例

### 5. 创建 Secret

**用于存储敏感数据：**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <app-name>-secret
  namespace: <namespace>
type: Opaque
stringData:
  DATABASE_PASSWORD: "changeme"
  API_KEY: "secret-api-key"
  # For certificate files
  tls.crt: |
    -----BEGIN CERTIFICATE-----
    ...
    -----END CERTIFICATE-----
  tls.key: |
    -----BEGIN PRIVATE KEY-----
    ...
    -----END PRIVATE KEY-----
```

**安全注意事项：**
- 绝不要以明文形式将密钥提交到 Git
- 使用 Sealed Secrets、External Secrets Operator 或 Vault 等工具管理密钥
- 定期轮换密钥
- 使用 RBAC 限制密钥访问
- 对于 TLS 密钥，考虑使用 `kubernetes.io/tls` 类型的 Secret

### 6. 创建 PersistentVolumeClaim（如需要）

**用于有状态的应用程序：**

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: <app-name>-data
  namespace: <namespace>
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: gp3
  resources:
    requests:
      storage: 10Gi
```

**在 Deployment 中挂载 PersistentVolumeClaim：**
```yaml
spec:
  template:
    spec:
      containers:
        - name: app
          volumeMounts:
            - name: data
              mountPath: /var/lib/app
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: <app-name>-data
```

**存储注意事项：**
- 根据性能需求选择合适的 StorageClass
- 对于单 Pod 访问，使用 ReadWriteOnce
- 对于多 Pod 共享存储，使用 ReadWriteMany
- 考虑备份策略
- 设置适当的保留策略

### 7. 应用安全最佳实践

**为 Deployment 添加安全上下文：**

```yaml
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: app
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
```

**安全检查清单：**
- [ ] 以非 root 用户身份运行
- [ ] 禁用所有特权
- [ ] 使用只读的根文件系统
- [ ] 禁用权限提升
- [ ] 设置 seccomp 配置文件
- [ ] 使用 Pod 安全标准

### 8. 添加标签和注释

**推荐的标准标签：**

```yaml
metadata:
  labels:
    app.kubernetes.io/name: <app-name>
    app.kubernetes.io/instance: <instance-name>
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/component: backend
    app.kubernetes.io/part-of: <system-name>
    app.kubernetes.io/managed-by: kubectl
```

**有用的注释：**

```yaml
metadata:
  annotations:
    description: "Application description"
    contact: "team@example.com"
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
```

### 9. 组织多资源清单

**文件组织方式：**
- **选项 1：使用 `---` 分隔符的单一文件**
```yaml
# app-name.yaml
---
apiVersion: v1
kind: ConfigMap
...
---
apiVersion: v1
kind: Secret
...
---
apiVersion: apps/v1
kind: Deployment
...
---
apiVersion: v1
kind: Service
...
```

- **选项 2：将文件分开存放**
```
manifests/
├── configmap.yaml
├── secret.yaml
├── deployment.yaml
├── service.yaml
└── pvc.yaml
```

- **选项 3：自定义结构**
```
base/
├── kustomization.yaml
├── deployment.yaml
├── service.yaml
└── configmap.yaml
overlays/
├── dev/
│   └── kustomization.yaml
└── prod/
    └── kustomization.yaml
```

### 10. 验证和测试

**验证步骤：**

```bash
# Dry-run validation
kubectl apply -f manifest.yaml --dry-run=client

# Server-side validation
kubectl apply -f manifest.yaml --dry-run=server

# Validate with kubeval
kubeval manifest.yaml

# Validate with kube-score
kube-score score manifest.yaml

# Check with kube-linter
kube-linter lint manifest.yaml
```

**测试清单：**
- [ ] 清单通过 dry-run 验证
- [ ] 所有必需的字段都存在
- [ ] 资源限制合理
- [ ] 健康检查已配置
- [ ] 安全上下文已设置
- [ ] 标签符合规范
- [ ] 命名空间存在或已创建

## 常见模式

### 模式 1：简单的无状态 Web 应用程序

**用例：**标准 Web API 或微服务

**所需组件：**
- Deployment（3 个副本以实现高可用性）
- ClusterIP 类型的 Service
- 用于配置的 ConfigMap
- 用于 API 密钥的 Secret
- 可选：HorizontalPodAutoscaler（水平扩展器）

**参考：**请参阅 `assets/deployment-template.yaml`

### 模式 2：有状态的数据库应用程序

**用例：**数据库或有状态存储应用程序

**所需组件：**
- StatefulSet（而非 Deployment）
- Headless Service（无头服务）
- PersistentVolumeClaim 模板
- 用于数据库配置的 ConfigMap
- 用于存储凭据的 Secret

### 模式 3：后台作业或 Cron 任务

**用例：**定时任务或批处理操作

**所需组件：**
- CronJob 或 Job
- 用于作业参数的 ConfigMap
- 用于存储凭据的 Secret
- 带有 RBAC 的 ServiceAccount（服务账户）

### 模式 4：多容器 Pod

**用例：**包含侧车容器（sidecar containers）的应用程序

**所需组件：**
- 包含多个容器的 Deployment
- 容器之间的共享存储
- 用于初始化的容器
- 如有需要，可以使用 Service

## 模板

以下模板位于 `assets/` 目录中：
- `deployment-template.yaml` - 遵循最佳实践的标准 Deployment 模板
- `service-template.yaml` - Service 配置模板（ClusterIP、LoadBalancer、NodePort）
- `configmap-template.yaml` - 不同数据类型的 ConfigMap 示例
- `secret-template.yaml` - Secret 示例（生成后不会提交到 Git）
- `pvc-template.yaml` - PersistentVolumeClaim 模板

## 参考文档

- `references/deployment-spec.md` - 详细的 Deployment 规范
- `references/service-spec.md` - 服务类型和网络配置详情

## 最佳实践总结：

1. **始终设置资源请求和限制** - 防止资源不足
2. **实现健康检查** - 确保 Kubernetes 能够管理应用程序
3. **使用具体的镜像标签** - 避免不可预测的部署结果
4. **应用安全上下文** - 以非 root 用户身份运行，并禁用不必要的权限
5. **使用 ConfigMap 和 Secret** - 将配置与代码分离
6. **为所有资源添加标签** - 便于过滤和组织
7. **遵循命名规范** - 使用标准的 Kubernetes 标签
8. **在应用之前进行验证** - 使用 dry-run 和验证工具
9. **对清单进行版本控制** - 使用 Git 进行版本管理
10. **使用注释进行文档记录** - 为其他开发人员提供上下文信息

## 故障排除

**Pod 无法启动：**
- 检查镜像拉取错误：`kubectl describe pod <pod-name>`
- 验证资源是否可用：`kubectl get nodes`
- 检查事件日志：`kubectl get events --sort-by='.lastTimestamp'`

**Service 无法访问：**
- 验证服务选择器是否与 Pod 标签匹配：`kubectl get endpoints <service-name>`
- 检查服务类型和端口配置
- 在集群内部进行测试：`kubectl run debug --rm -it --image=busybox -- sh`

**ConfigMap/Secret 无法加载：**
- 验证名称是否在 Deployment 中正确配置
- 检查命名空间
- 确保资源存在：`kubectl get configmap, secret`

## 下一步操作

创建清单后，请执行以下操作：
1. 将清单存储到 Git 仓库
2. 设置 CI/CD 流程以进行部署
3. 考虑使用 Helm 或 Kustomize 进行模板化
4. 使用 ArgoCD 或 Flux 实现 GitOps
5. 添加监控和可观测性功能

## 相关技能

- `helm-chart-scaffolding` - 用于模板化和打包
- `gitops-workflow` - 用于自动化部署
- `k8s-security-policies` - 用于高级安全配置