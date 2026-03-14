---
name: kubeblocks-configure-tls
metadata:
  version: "0.1.0"
description: 配置 KubeBlocks 数据库集群的 TLS 加密。支持内置证书（通过 cert-manager 自动管理）、用户提供的证书（用户自行管理 CA/PKI 证书），以及 mTLS（使用客户端证书的相互 TLS 协议）。当用户希望启用 TLS、SSL 加密、HTTPS 或使用证书进行安全数据库连接时，请使用此功能。**不适用于管理数据库密码（请参阅 manage-accounts）或外部服务暴露（请参阅 expose-service）**。
---
# 配置 TLS 加密

## 概述

KubeBlocks 支持数据库连接的 TLS 加密。共有三种模式可供选择：

- **内置 TLS**：KubeBlocks 会自动生成和管理证书（需要 cert-manager）。
- **用户提供的 TLS**：使用您自己的证书颁发机构（CA）和证书。
- **mTLS（双向 TLS）**：服务器和客户端都使用证书进行身份验证。

官方文档：https://kubeblocks.io/docs/preview/user_docs/connect-databases/tls-connection

## 预检

在继续之前，请确认集群运行正常且没有其他操作正在进行：

```bash
# Cluster must be Running
kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.status.phase}'

# No pending OpsRequests
kubectl get opsrequest -n <namespace> -l app.kubernetes.io/instance=<cluster-name> --field-selector=status.phase!=Succeed
```

如果集群未处于“运行”状态或有待完成的操作请求，请等待其完成后再继续。

对于内置 TLS 模式，请确认 cert-manager 已安装：

```bash
kubectl get pods -n cert-manager
```

## 工作流程

```
- [ ] Step 1: Choose TLS mode
- [ ] Step 2: Configure TLS in Cluster CR
- [ ] Step 3: Verify TLS connection
```

## 第一步：选择 TLS 模式

| 模式 | 证书管理 | 使用场景 |
|------|----------------------|----------|
| 内置（KubeBlocks） | 通过 cert-manager 自动管理 | 快速设置，开发/测试环境 |
| 用户提供的证书 | 手动管理（使用自己的 CA） | 需要现有 PKI 的生产环境 |
| mTLS | 手动管理 + 客户端证书 | 高安全环境 |

### 为什么使用 cert-manager 进行内置 TLS 配置？

cert-manager 可以自动化处理证书的整个生命周期（颁发、更新和轮换），从而避免因证书过期而导致生产环境在凌晨 3 点出现故障。如果您已有 PKI 团队并建立了证书轮换流程，手动管理证书也是可行的；但对于大多数用户来说，cert-manager 可以有效降低操作风险。KubeBlocks 与 cert-manager 的 `Issuer` 和 `Certificate` CRD 集成，因此启用 TLS 只需要一个简单的配置选项，而无需进行多步骤的手动操作。

TLS 相关文档：https://kubeblocks.io/docs/preview/kubeblocks-for-mysql/07-tls/01-tls-overview

### 内置 TLS 的前提条件

内置模式需要 **cert-manager**。如果尚未安装，请先进行安装：

```bash
# Check if cert-manager is installed
kubectl get pods -n cert-manager

# Install cert-manager if needed
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
```

等待 cert-manager 的 Pod 完全启动：

```bash
kubectl wait --for=condition=Ready pods --all -n cert-manager --timeout=120s
```

## 第二步：配置 TLS

### 选项 A：内置 TLS（由 KubeBlocks 管理）

在集群的 CR（Cluster Resource）中添加 TLS 配置：

```yaml
spec:
  componentSpecs:
  - name: <component>
    tls: true
    issuer:
      name: KubeBlocks
```

这会告诉 KubeBlocks 使用 cert-manager 自动生成自签名证书颁发机构和服务器证书。

### 选项 B：用户提供的证书

**1. 生成证书（如果还没有的话）：**

```bash
# Generate CA key and certificate
openssl genrsa -out ca.key 2048
openssl req -x509 -new -nodes -key ca.key -subj "/CN=MyDatabaseCA" -days 3650 -out ca.crt

# Generate server key and CSR
openssl genrsa -out server.key 2048
openssl req -new -key server.key -subj "/CN=<cluster>-<component>" -out server.csr

# Sign server certificate with CA
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out server.crt -days 365 \
  -extfile <(printf "subjectAltName=DNS:*.<cluster>-<component>-headless.<ns>.svc.cluster.local,DNS:*.<cluster>-<component>.<ns>.svc.cluster.local")
```

**2. 创建 TLS 密钥（Secret）：**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <cluster>-tls
  namespace: <ns>
type: kubernetes.io/tls
data:
  ca.crt: <base64-encoded-ca.crt>
  tls.crt: <base64-encoded-server.crt>
  tls.key: <base64-encoded-server.key>
```

或者使用 kubectl 创建：

```bash
kubectl create secret generic <cluster>-tls -n <ns> \
  --from-file=ca.crt=ca.crt \
  --from-file=tls.crt=server.crt \
  --from-file=tls.key=server.key
```

**3. 在集群 CR 中引用该密钥：**

```yaml
spec:
  componentSpecs:
  - name: <component>
    tls: true
    issuer:
      name: UserProvided
      secretRef:
        name: <cluster>-tls
        ca: ca.crt
        cert: tls.crt
        key: tls.key
```

### 选项 C：mTLS（双向 TLS）

mTLS 使用与选项 A 或 B 相同的服务器端 TLS 配置，并且还需要客户端证书。

**1. 使用上述选项 A 或 B 配置服务器端 TLS。**

**2. 生成客户端证书：**

```bash
# Generate client key and CSR
openssl genrsa -out client.key 2048
openssl req -new -key client.key -subj "/CN=dbclient" -out client.csr

# Sign client certificate with the same CA
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out client.crt -days 365
```

**3. 配置数据库以要求客户端提供证书：**

```bash
# MySQL: create user requiring X509
kubectl exec -it <pod> -n <ns> -- mysql -u root -p --ssl -e \
  "CREATE USER 'secureuser'@'%' REQUIRE X509; GRANT ALL ON *.* TO 'secureuser'@'%';"

# PostgreSQL: edit pg_hba.conf to require clientcert=verify-full
# This is typically handled via parameter reconfiguration
```

## 第三步：验证 TLS 连接

### 检查 TLS 是否已启用

```bash
# MySQL
kubectl exec -it <pod> -n <ns> -- mysql -u root -p --ssl -e "SHOW VARIABLES LIKE '%ssl%';"

# PostgreSQL
kubectl exec -it <pod> -n <ns> -- psql -U postgres -c "SHOW ssl;"
```

### 从外部使用 TLS 连接

```bash
# MySQL with TLS
mysql -h <host> -P 3306 -u root -p --ssl-mode=REQUIRED \
  --ssl-ca=ca.crt --ssl-cert=client.crt --ssl-key=client.key

# PostgreSQL with TLS
psql "host=<host> port=5432 user=postgres sslmode=verify-full sslrootcert=ca.crt sslcert=client.crt sslkey=client.key"
```

### 验证证书详细信息

```bash
# Check the mounted certificates in the pod
kubectl exec -it <pod> -n <ns> -- ls -la /var/run/secrets/tls/

# View certificate info
kubectl exec -it <pod> -n <ns> -- openssl x509 -in /var/run/secrets/tls/tls.crt -text -noout
```

## 故障排除

**TLS 无法启用（Pod 崩溃）：**
- 确认 cert-manager 是否正在运行（对于内置模式）。
- 检查 TLS 密钥是否存在且密钥正确：`kubectl describe secret <cluster>-tls -n <ns>`
- 查看 Pod 日志：`kubectl logs <pod> -n <ns>`

**证书过期：**
- 对于内置模式，cert-manager 会自动处理证书更新。
- 对于用户提供的证书，需要重新生成证书并更新相应的 Secret。

**客户端无法使用 TLS 连接：**
- 确认客户端证书的颁发机构（CA）与服务器证书匹配。
- 检查服务器证书中的 SAN（Subject Alternative Names）字段。

## 额外资源

有关特定引擎的 TLS 配置详情、完整的证书生成流程以及故障排除方法，请参阅 [reference.md](references/reference.md)。

有关代理的安全最佳实践（如预测试、状态确认、生产环境保护等），请参阅 [safety-patterns.md](../../references/safety-patterns.md)。