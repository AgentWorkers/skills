---
name: gitops-workflow
description: 使用 ArgoCD 和 Flux 实现 GitOps 工作流程，以实现自动化、声明式的 Kubernetes 部署，并具备持续协调（continuous reconciliation）功能。适用于实施 GitOps 实践、自动化 Kubernetes 部署或设置声明式基础设施管理时。
---

# GitOps 工作流程

本文档提供了使用 ArgoCD 和 Flux 实现 GitOps 工作流程的完整指南，以实现 Kubernetes 的自动化部署。

## 目的

通过 ArgoCD 或 Flux CD，遵循 OpenGitOps 原则，为 Kubernetes 实现基于 Git 的声明式、持续交付机制。

## 适用场景

- 为 Kubernetes 集群设置 GitOps 环境
- 从 Git 自动化应用程序部署
- 实施渐进式交付策略
- 管理多集群部署
- 配置自动化同步策略
- 在 GitOps 中管理敏感信息（ secrets）

## OpenGitOps 原则

1. **声明式**：整个系统以声明性方式描述
2. **版本化且不可变**：所需状态存储在 Git 中
3. **自动拉取**：软件代理自动拉取所需状态
4. **持续协调**：代理不断比较实际状态与所需状态，并进行同步

## ArgoCD 设置

### 1. 安装

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

**参考：**请参阅 `references/argocd-setup.md` 以获取详细安装步骤

### 2. 仓库结构

```
gitops-repo/
├── apps/
│   ├── production/
│   │   ├── app1/
│   │   │   ├── kustomization.yaml
│   │   │   └── deployment.yaml
│   │   └── app2/
│   └── staging/
├── infrastructure/
│   ├── ingress-nginx/
│   ├── cert-manager/
│   └── monitoring/
└── argocd/
    ├── applications/
    └── projects/
```

### 3. 创建应用程序

```yaml
# argocd/applications/my-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/gitops-repo
    targetRevision: main
    path: apps/production/my-app
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

### 4. “App of Apps” 模式

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: applications
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/gitops-repo
    targetRevision: main
    path: argocd/applications
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated: {}
```

## Flux CD 设置

### 1. 安装

```bash
# Install Flux CLI
curl -s https://fluxcd.io/install.sh | sudo bash

# Bootstrap Flux
flux bootstrap github \
  --owner=org \
  --repository=gitops-repo \
  --branch=main \
  --path=clusters/production \
  --personal
```

### 2. 创建 Git 仓库

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: my-app
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/org/my-app
  ref:
    branch: main
```

### 3. 创建自定义配置（Kustomizations）

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: my-app
  namespace: flux-system
spec:
  interval: 5m
  path: ./deploy
  prune: true
  sourceRef:
    kind: GitRepository
    name: my-app
```

## 同步策略

### 自动同步配置

**ArgoCD：**
```yaml
syncPolicy:
  automated:
    prune: true      # Delete resources not in Git
    selfHeal: true   # Reconcile manual changes
    allowEmpty: false
  retry:
    limit: 5
    backoff:
      duration: 5s
      factor: 2
      maxDuration: 3m
```

**Flux：**
```yaml
spec:
  interval: 1m
  prune: true
  wait: true
  timeout: 5m
```

**参考：**请参阅 `references/sync-policies.md` 以获取更多信息

## 渐进式交付

### 使用 ArgoCD 进行 Canary 部署

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {duration: 1m}
      - setWeight: 50
      - pause: {duration: 2m}
      - setWeight: 100
```

### 使用 Flux 进行蓝绿部署（Blue-Green Deployment）

```yaml
strategy:
  blueGreen:
    activeService: my-app
    previewService: my-app-preview
    autoPromotionEnabled: false
```

## 敏感信息管理

### 外部敏感信息操作符（External Secrets Operator）

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: db-credentials
  data:
  - secretKey: password
    remoteRef:
      key: prod/db/password
```

### 加密敏感信息（Sealed Secrets）

```bash
# Encrypt secret
kubeseal --format yaml < secret.yaml > sealed-secret.yaml

# Commit sealed-secret.yaml to Git
```

## 最佳实践

1. 为不同环境使用独立的仓库或分支
2. 为 Git 仓库实施基于角色的访问控制（RBAC）
3. 为同步失败设置通知机制
4. 为自定义资源启用健康检查
5. 在生产环境前设置审批流程
6. 将敏感信息存储在外部存储系统中（避免直接存储在 Git 中）
7. 采用 “App of Apps” 模式来组织应用程序结构
8. 为版本添加标签以便于回滚
9. 通过警报监控同步状态
10. 首先在测试环境中测试更改

## 故障排除

**同步失败：**
```bash
argocd app get my-app
argocd app sync my-app --prune
```

**状态不同步：**
```bash
argocd app diff my-app
argocd app sync my-app --force
```

## 相关技能

- `k8s-manifest-generator`：用于生成 Kubernetes 配置文件（manifests）
- `helm-chart-scaffolding`：用于打包应用程序资源