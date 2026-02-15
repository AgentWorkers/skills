---
name: kubernetes
description: |
  Comprehensive Kubernetes and OpenShift cluster management skill covering operations, troubleshooting, manifest generation, security, and GitOps. Use this skill when:
  (1) Cluster operations: upgrades, backups, node management, scaling, monitoring setup
  (2) Troubleshooting: pod failures, networking issues, storage problems, performance analysis
  (3) Creating manifests: Deployments, StatefulSets, Services, Ingress, NetworkPolicies, RBAC
  (4) Security: audits, Pod Security Standards, RBAC, secrets management, vulnerability scanning
  (5) GitOps: ArgoCD, Flux, Kustomize, Helm, CI/CD pipelines, progressive delivery
  (6) OpenShift-specific: SCCs, Routes, Operators, Builds, ImageStreams
  (7) Multi-cloud: AKS, EKS, GKE, ARO, ROSA operations
metadata:
  author: cluster-skills
  version: "1.0.0"
---

# Kubernetes与OpenShift集群管理

涵盖Kubernetes和OpenShift集群的全面管理技能，包括操作、故障排除、配置文件（manifests）管理、安全配置以及GitOps流程。

## 当前版本（2026年1月）

| 平台 | 版本 | 文档链接 |
|----------|---------|---------------|
| **Kubernetes** | 1.31.x | https://kubernetes.io/docs/ |
| **OpenShift** | 4.17.x | https://docs.openshift.com/ |
| **EKS** | 1.31 | https://docs.aws.amazon.com/eks/ |
| **AKS** | 1.31 | https://learn.microsoft.com/azure/aks/ |
| **GKE** | 1.31 | https://cloud.google.com/kubernetes-engine/docs |

### 主要工具

| 工具 | 版本 | 功能 |
|------|---------|---------|
| **ArgoCD** | v2.13.x | GitOps部署工具 |
| **Flux** | v2.4.x | GitOps集成工具包 |
| **Kustomize** | v5.5.x | 配置文件定制工具 |
| **Helm** | v3.16.x | 应用包管理工具 |
| **Velero** | 1.15.x | 数据备份与恢复工具 |
| **Trivy** | 0.58.x | 安全扫描工具 |
| **Kyverno** | 1.13.x | 策略管理工具 |

## 命令规范

**重要提示**：使用`kubectl`命令来操作Kubernetes集群；使用`oc`命令来操作OpenShift/ARO集群。

---

## 1. 集群操作

### 节点管理

```bash
# View nodes
kubectl get nodes -o wide

# Drain node for maintenance
kubectl drain ${NODE} --ignore-daemonsets --delete-emptydir-data --grace-period=60

# Uncordon after maintenance
kubectl uncordon ${NODE}

# View node resources
kubectl top nodes
```

### 集群升级

**AKS:**  
```bash
az aks get-upgrades -g ${RG} -n ${CLUSTER} -o table
az aks upgrade -g ${RG} -n ${CLUSTER} --kubernetes-version ${VERSION}
```

**EKS:**  
```bash
aws eks update-cluster-version --name ${CLUSTER} --kubernetes-version ${VERSION}
```

**GKE:**  
```bash
gcloud container clusters upgrade ${CLUSTER} --master --cluster-version ${VERSION}
```

**OpenShift:**  
```bash
oc adm upgrade --to=${VERSION}
oc get clusterversion
```

### 使用Velero进行数据备份

```bash
# Install Velero
velero install --provider ${PROVIDER} --bucket ${BUCKET} --secret-file ${CREDS}

# Create backup
velero backup create ${BACKUP_NAME} --include-namespaces ${NS}

# Restore
velero restore create --from-backup ${BACKUP_NAME}
```

---

## 2. 故障排除

### 集群健康检查

运行内置脚本进行全面的集群健康状况检查：
```bash
bash scripts/cluster-health-check.sh
```

### Pod状态解析

| 状态 | 含义 | 处理方法 |
|--------|---------|--------|
| `Pending` | 正在调度中 | 检查资源分配、节点选择条件（nodeSelector）和容错策略（tolerations） |
| `CrashLoopBackOff` | 容器崩溃 | 查看日志：`kubectl logs ${POD} --previous` |
| `ImagePullBackOff` | 镜像无法获取 | 验证镜像名称及注册库访问权限 |
| `OOMKilled` | 内存不足 | 增加内存限制 |
| `Evicted` | 节点负载过高 | 检查节点资源使用情况 |

### 调试命令

```bash
# Pod logs (current and previous)
kubectl logs ${POD} -c ${CONTAINER} --previous

# Multi-pod logs with stern
stern ${LABEL_SELECTOR} -n ${NS}

# Exec into pod
kubectl exec -it ${POD} -- /bin/sh

# Pod events
kubectl describe pod ${POD} | grep -A 20 Events

# Cluster events (sorted by time)
kubectl get events -A --sort-by='.lastTimestamp' | tail -50
```

### 网络故障排除

```bash
# Test DNS
kubectl run -it --rm debug --image=busybox -- nslookup kubernetes.default

# Test service connectivity
kubectl run -it --rm debug --image=curlimages/curl -- curl -v http://${SVC}.${NS}:${PORT}

# Check endpoints
kubectl get endpoints ${SVC}
```

---

## 3. 配置文件（Manifest）生成

### 生产环境部署模板

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/version: "${VERSION}"
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app.kubernetes.io/name: ${APP_NAME}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: ${APP_NAME}
    spec:
      serviceAccountName: ${APP_NAME}
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: ${APP_NAME}
          image: ${IMAGE}:${TAG}
          ports:
            - name: http
              containerPort: 8080
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /healthz
              port: http
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app.kubernetes.io/name: ${APP_NAME}
                topologyKey: kubernetes.io/hostname
```

### 服务（Service）与Ingress配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}
spec:
  selector:
    app.kubernetes.io/name: ${APP_NAME}
  ports:
    - name: http
      port: 80
      targetPort: http
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ${APP_NAME}
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - ${HOST}
      secretName: ${APP_NAME}-tls
  rules:
    - host: ${HOST}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: ${APP_NAME}
                port:
                  name: http
```

### OpenShift路由配置

```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: ${APP_NAME}
spec:
  to:
    kind: Service
    name: ${APP_NAME}
  port:
    targetPort: http
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
```

使用内置脚本生成配置文件：
```bash
bash scripts/generate-manifest.sh deployment myapp production
```

---

## 4. 安全配置

### 安全审计

运行内置脚本进行安全审计：
```bash
bash scripts/security-audit.sh [namespace]
```

### Pod安全标准

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ${NAMESPACE}
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: baseline
    pod-security.kubernetes.io/warn: restricted
```

### 网络策略（Zero Trust）

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ${APP_NAME}-policy
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: ${APP_NAME}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: frontend
      ports:
        - protocol: TCP
          port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: database
      ports:
        - protocol: TCP
          port: 5432
    # Allow DNS
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

### RBAC最佳实践

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ${APP_NAME}
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ${APP_NAME}-role
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ${APP_NAME}-binding
subjects:
  - kind: ServiceAccount
    name: ${APP_NAME}
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: ${APP_NAME}-role
```

### 镜像扫描

```bash
# Scan image with Trivy
trivy image ${IMAGE}:${TAG}

# Scan with severity filter
trivy image --severity HIGH,CRITICAL ${IMAGE}:${TAG}

# Generate SBOM
trivy image --format spdx-json -o sbom.json ${IMAGE}:${TAG}
```

---

## 5. GitOps

### ArgoCD应用管理

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ${APP_NAME}
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: ${GIT_REPO}
    targetRevision: main
    path: k8s/overlays/${ENV}
  destination:
    server: https://kubernetes.default.svc
    namespace: ${NAMESPACE}
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### Kustomize配置

```
k8s/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   └── service.yaml
└── overlays/
    ├── dev/
    │   └── kustomization.yaml
    ├── staging/
    │   └── kustomization.yaml
    └── prod/
        └── kustomization.yaml
```

**base/kustomization.yaml:**  
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml
```

**overlays/prod/kustomization.yaml:**  
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
namePrefix: prod-
namespace: production
replicas:
  - name: myapp
    count: 5
images:
  - name: myregistry/myapp
    newTag: v1.2.3
```

### GitHub Actions与CI/CD集成

```yaml
name: Build and Deploy
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build and push image
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ secrets.REGISTRY }}/${{ github.event.repository.name }}:${{ github.sha }}
      
      - name: Update Kustomize image
        run: |
          cd k8s/overlays/prod
          kustomize edit set image myapp=${{ secrets.REGISTRY }}/${{ github.event.repository.name }}:${{ github.sha }}
          
      - name: Commit and push
        run: |
          git config user.name "github-actions"
          git config user.email "github-actions@github.com"
          git add .
          git commit -m "Update image to ${{ github.sha }}"
          git push
```

使用内置脚本同步ArgoCD配置：
```bash
bash scripts/argocd-app-sync.sh ${APP_NAME} --prune
```

---

## 辅助脚本

本技能包含`scripts/`目录中的自动化脚本：

| 脚本 | 功能 |
|--------|---------|
| `cluster-health-check.sh` | 进行全面的集群健康状况评估 |
| `security-audit.sh` | 安全配置审计（权限管理、root账户使用、RBAC配置、网络策略） |
| `node-maintenance.sh` | 安全地清理和维护集群节点 |
| `pre-upgrade-check.sh` | 升级前的验证检查清单 |
| `generate-manifest.sh` | 生成适用于生产环境的Kubernetes配置文件 |
| `argocd-app-sync.sh` | 用于同步ArgoCD配置的辅助脚本 |

要运行任意脚本，请执行：
```bash
bash scripts/<script-name>.sh [arguments]
```