---
model: fast
description: |
  WHAT: Kubernetes manifest generation - Deployments, StatefulSets, CronJobs, Services, Ingresses, 
  ConfigMaps, Secrets, and PVCs with production-grade security and health checks.
  
  WHEN: User needs to create K8s manifests, deploy containers, configure Services/Ingress, 
  manage ConfigMaps/Secrets, set up persistent storage, or organize multi-environment configs.
  
  KEYWORDS: kubernetes, k8s, manifest, deployment, statefulset, cronjob, service, ingress, 
  configmap, secret, pvc, pod, container, yaml, kustomize, helm, namespace, probe, security context
version: 1.0.0
---

# Kubernetes

本文档介绍了如何生成适用于生产环境的Kubernetes配置文件（manifests），这些文件涵盖了部署（Deployments）、有状态工作负载（StatefulSets）、定时任务（CronJobs）、服务（Services）、Ingresses、配置映射（ConfigMaps）、秘密（Secrets）以及持久化存储（PVCs）等组件的配置。同时，还涵盖了安全设置、健康检查（health checks）和资源管理（resource management）的相关内容。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install kubernetes
```

## 适用场景

| 场景 | 例子 |
|------|---------|
| 创建部署配置文件 | 需要部署（Deployment）和服务（Service）的新微服务 |
| 定义网络资源 | ClusterIP、LoadBalancer、支持TLS的Ingress |
| 管理配置 | 使用ConfigMaps存储应用程序配置，使用Secrets存储凭证 |
| 有状态的工作负载 | 使用StatefulSets和PVCs管理数据库 |
| 定时任务 | 使用CronJobs执行批量处理 |
| 多环境设置 | 为开发（dev）、测试（staging）和生产（prod）环境定制配置 |

## 工作负载选择

| 工作负载类型 | 所需资源 | 适用场景 |
|------------|------------|-------------------|
| 无状态应用 | Deployment | Web服务器、API、微服务 |
| 有状态应用 | StatefulSet | 数据库、消息队列、缓存 |
| 一次性任务 | Job | 数据迁移、数据导入 |
| 定时任务 | CronJob | 备份、报告生成、清理操作 |
| 节点代理 | DaemonSet | 日志收集、监控代理 |

## 部署（Deployment）

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: production
  labels:
    app.kubernetes.io/name: my-app
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/component: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app.kubernetes.io/name: my-app
  template:
    metadata:
      labels:
        app.kubernetes.io/name: my-app
        app.kubernetes.io/version: "1.0.0"
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: my-app
          image: registry.example.com/my-app:1.0.0
          ports:
            - containerPort: 8080
              name: http
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: [ALL]
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
            - name: LOG_LEVEL
              valueFrom:
                configMapKeyRef:
                  name: my-app-config
                  key: LOG_LEVEL
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: my-app-secret
                  key: DATABASE_PASSWORD
```

## 服务（Services）

### ClusterIP（内部访问）

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app
  namespace: production
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: my-app
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
```

### LoadBalancer（外部访问）

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-lb
  namespace: production
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
spec:
  type: LoadBalancer
  selector:
    app.kubernetes.io/name: my-app
  ports:
    - name: http
      port: 80
      targetPort: 8080
```

### 服务类型快速参考

| 类型 | 作用范围 | 使用场景 |
|------|---------|-------------------|
| ClusterIP | 集群内部访问 | 服务之间的通信 |
| NodePort | 通过节点IP地址进行外部访问 | 开发/测试环境 |
| LoadBalancer | 通过云负载均衡器进行外部访问 | 生产环境 |
| ExternalName | DNS别名 | 将服务映射到外部域名 |

## Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app
  namespace: production
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  ingressClassName: nginx
  tls:
    - hosts: [app.example.com]
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-app
                port:
                  number: 80
```

## ConfigMap与Secret

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-app-config
  namespace: production
data:
  LOG_LEVEL: info
  APP_MODE: production
  DATABASE_HOST: db.internal.svc.cluster.local
  app.properties: |
    server.port=8080
    server.host=0.0.0.0
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-app-secret
  namespace: production
type: Opaque
stringData:
  DATABASE_PASSWORD: "changeme"
  API_KEY: "secret-api-key"
```

> **重要提示：** **切勿将明文Secrets提交到Git仓库。** 应使用Sealed Secrets、External Secrets Operator或Vault来保护Secrets的安全。

## 持久化存储（Persistent Storage）

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-app-data
  namespace: production
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: gp3
  resources:
    requests:
      storage: 10Gi
```

## 在容器中挂载配置文件：

```yaml
containers:
  - name: app
    volumeMounts:
      - name: data
        mountPath: /var/lib/app
volumes:
  - name: data
    persistentVolumeClaim:
      claimName: my-app-data
```

| 访问模式 | 缩写 | 使用场景 |
|---------|---------|-------------------|
| ReadWriteOnce | RWO | 单个Pod使用的数据库 |
| ReadOnlyMany | ROX | 共享配置文件/静态资源 |
| ReadWriteMany | RWX | 多个Pod共享的存储空间 |

## 安全设置

### Pod级别安全配置

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
```

### 容器级别安全配置

```yaml
securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop: [ALL]
```

### 安全检查清单

| 检查项 | 状态 |
|---------|--------|
| `runAsNonRoot: true` | 必须设置 |
| `allowPrivilegeEscalation: false` | 必须设置 |
| `readOnlyRootFilesystem: true` | 建议设置 |
| `capabilities.drop: [ALL]` | 必须设置 |
| `seccompProfile: RuntimeDefault` | 建议设置 |
| 使用特定的镜像标签（切勿使用`:latest`） | 必须设置 |
| 设置资源请求和限制 | 必须设置 |

## 标签（Labels）

```yaml
metadata:
  labels:
    app.kubernetes.io/name: my-app
    app.kubernetes.io/instance: my-app-prod
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/component: backend
    app.kubernetes.io/part-of: my-system
    app.kubernetes.io/managed-by: kubectl
```

## 配置文件的组织结构

### 选项1：使用单独的文件

```
manifests/
├── configmap.yaml
├── secret.yaml
├── deployment.yaml
├── service.yaml
└── pvc.yaml
```

### 选项2：自定义配置文件

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
    ├── kustomization.yaml
    └── resource-patch.yaml
```

## 配置文件验证

```bash
# Client-side dry run
kubectl apply -f manifest.yaml --dry-run=client

# Server-side validation
kubectl apply -f manifest.yaml --dry-run=server

# Lint with kube-score
kube-score score manifest.yaml

# Lint with kube-linter
kube-linter lint manifest.yaml
```

## 故障排除快速指南

| 问题 | 原因 | 解决方法 |
|---------|---------|-------------------|
| Pod处于`Pending`状态 | 使用`kubectl describe pod`查看事件日志 | 检查资源请求、节点容量和PVC绑定情况 |
| `ImagePullBackOff`错误 | 镜像名称/标签错误或缺少Pull Secret | 确认镜像存在，并添加`imagePullSecrets`配置 |
| 应用程序启动时崩溃 | 检查日志：`kubectl logs <pod> --previous` |
| 服务无法访问 | 选择器（selector）不匹配 | 确认`kubectl get endpoints <svc>`的结果是否为空 |
| ConfigMap加载失败 | 名称错误或命名空间错误 | 确认名称和命名空间设置正确 |
| 健康检查失败 | 路径或端口错误 | 检查容器内的健康检查端点是否正常工作 |
| Pod因内存不足而终止 | 内存限制过低 | 增加`resources.limits.memory`的值 |

## **绝对禁止的行为**

| 不推荐的做法 | 原因 | 正确的做法 |
|------------|---------|-------------------|
| 使用`:latest`镜像标签 | 配置无法复现 | 使用具体的镜像版本，例如`image:1.2.3` |
| 忽略资源限制 | Pod可能会耗尽节点资源 | 必须设置`requests`和`limits` |
| 以root权限运行容器 | 容器可能获得完整主机访问权限 | 设置`runAsNonRoot: true`并指定用户 |
| 将明文Secrets提交到Git | 密码会永久保存在Git历史记录中 | 使用Sealed Secrets、External Secrets或Vault |
| 忽略健康检查 | Kubernetes无法检测不健康的Pod | 必须配置健康检查（liveness probes） |
| 省略标签 | 无法过滤、筛选或组织资源 | 使用标准的`app.kubernetes.io/*`标签 |
| 生产环境仅使用一个Replica | 更新时会导致服务不可用 | 至少使用3个Replica以确保高可用性（HA） |
| 在容器中硬编码配置 | 配置更改时需要重新构建容器 | 使用ConfigMaps和Secrets来存储配置 |

## 资源与参考文档

### 资源模板

| 模板 | 说明 |
|---------|---------|
| [assets/deployment-template.yaml] | 包含安全设置和健康检查功能的部署模板 |
| [assets/service-template.yaml] | ClusterIP、LoadBalancer、NodePort的配置示例 |
| [assets/configmap-template.yaml] | 包含数据类型的ConfigMap模板 |
| [assets/statefulset-template.yaml] | 包含无状态服务（StatefulSet）和PVC的配置模板 |
| [assets/cronjob-template.yaml] | 包含并发控制和历史记录功能的CronJob模板 |
| [assets/ingress-template.yaml] | 包含TLS、速率限制和CORS功能的Ingress模板 |

### 参考文档

| 文档 | 说明 |
|---------|---------|
| [references/deployment-spec.md] | 详细的部署规范 |
| [references/service-spec.md] | 服务类型和网络配置的详细说明 |