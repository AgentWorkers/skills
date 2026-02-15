---
name: k8s-security-policies
description: 实施 Kubernetes 安全策略，包括 NetworkPolicy、PodSecurityPolicy 和 RBAC，以实现生产级安全。这些策略可用于保护 Kubernetes 集群、实现网络隔离或强制遵循 Pod 安全标准。
---

# Kubernetes安全策略

本文档提供了关于如何在Kubernetes中实施NetworkPolicy、PodSecurityPolicy、RBAC（角色基访问控制）以及Pod安全标准的全面指南。

## 目的

通过使用网络策略、Pod安全标准和RBAC，为Kubernetes集群构建深度防御的安全体系。

## 适用场景

- 实施网络隔离
- 配置Pod安全标准
- 设置基于最小权限的RBAC访问控制
- 创建符合安全规范的安全策略
- 实施访问控制机制
- 保护多租户集群的安全

## Pod安全标准

### 1. 特权级（无限制）
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: privileged-ns
  labels:
    pod-security.kubernetes.io/enforce: privileged
    pod-security.kubernetes.io/audit: privileged
    pod-security.kubernetes.io/warn: privileged
```

### 2. 基础级（最小限制）
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: baseline-ns
  labels:
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/audit: baseline
    pod-security.kubernetes.io/warn: baseline
```

### 3. 限制级（最高限制）
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: restricted-ns
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

## 网络策略

### 默认设置：拒绝所有请求
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### 允许前端访问后端服务
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

### 允许DNS请求
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
```

**参考文件：** `assets/network-policy-template.yaml`

## RBAC配置

### 基于命名空间的角色（Role）
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

### 集群范围内的角色（ClusterRole）
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "watch", "list"]
```

### 角色绑定（RoleBinding）
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: production
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
- kind: ServiceAccount
  name: default
  namespace: production
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

**参考文件：** `references/rbac-patterns.md`

## Pod安全上下文

### 受限的Pod权限
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: myapp:1.0
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
```

## 使用OPA Gatekeeper执行策略

### 约束模板（ConstraintTemplate）
```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg, "details": {"missing_labels": missing}}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("missing required labels: %v", [missing])
        }
```

### 约束条件（Constraint）
```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-app-label
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  parameters:
    labels: ["app", "environment"]
```

## 服务网格安全（Istio）

### 对等方身份验证（mTLS）
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
```

### 访问控制策略（AuthorizationPolicy）
```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/frontend"]
```

## 最佳实践

1. 在命名空间级别实施Pod安全标准。
2. 使用网络策略进行网络隔离。
3. 为所有服务账户应用最小权限的RBAC设置。
4. 启用访问控制机制（如OPA Gatekeeper或Kyverno）。
5. 以非root用户身份运行容器。
6. 使用只读的root文件系统。
7. 除非必要，否则禁用所有不必要的系统权限。
8. 实施资源配额并限制使用范围。
9. 启用安全事件的审计日志记录。
10. 定期对容器镜像进行安全扫描。

## 合规性框架

### CIS Kubernetes基准
- 使用RBAC进行权限控制。
- 启用审计日志记录。
- 遵循Pod安全标准。
- 配置网络策略。
- 对存储的数据进行加密。
- 启用节点身份验证。

### NIST网络安全框架
- 实施深度防御策略。
- 使用网络隔离机制。
- 配置安全监控系统。
- 实施访问控制措施。
- 启用日志记录和监控功能。

## 常见问题排查

- **NetworkPolicy无法生效**：```bash
# Check if CNI supports NetworkPolicy
kubectl get nodes -o wide
kubectl describe networkpolicy <name>
```
- **RBAC权限被拒绝**：```bash
# Check effective permissions
kubectl auth can-i list pods --as system:serviceaccount:default:my-sa
kubectl auth can-i '*' '*' --as system:serviceaccount:default:my-sa
```

## 参考文件

- `assets/network-policy-template.yaml` - 网络策略示例
- `assets/pod-security-template.yaml` - Pod安全策略配置文件
- `references/rbac-patterns.md` - RBAC配置模式参考

## 相关技能

- `k8s-manifest-generator` - 用于生成安全的Kubernetes配置文件。
- `gitops-workflow` - 用于自动化策略部署流程。