# 秘密管理

使用 Vault、AWS Secrets Manager 以及平台自带的解决方案来安全地管理 CI/CD 流程中的敏感信息。

## 适用场景

- 安全存储 API 密钥和凭据
- 管理数据库密码
- 处理 TLS 证书
- 设置自动密钥轮换机制
- 实施最小权限访问策略
- 将敏感信息集成到 CI/CD 流程中（如 GitHub Actions、GitLab CI）
- 使用外部密钥将配置部署到 Kubernetes

## 不适用场景

- 仅需要本地开发环境下的配置（使用 `.env` 文件，而非 Git 存储）
- 无法确保对密钥存储后端的访问安全
- 计划将敏感信息硬编码到代码中（请避免这样做）

---

## 秘密管理工具比较

| 工具 | 适用场景 | 主要特性 |
|------|----------|--------------|
| **HashiCorp Vault** | 企业级应用、多云环境 | 动态密钥管理、密钥轮换、审计日志记录 |
| **AWS Secrets Manager** | 适用于 AWS 本地工作负载 | 与 RDS 集成、自动密钥轮换 |
| **Azure Key Vault** | 适用于 Azure 工作负载 | 基于 HSM 的存储机制、证书管理 |
| **Google Secret Manager** | 适用于 GCP 工作负载 | 支持版本控制、与 IAM 集成 |
| **GitHub Secrets** | 适用于 GitHub Actions | 简单易用、支持按仓库/组织/环境配置 |
| **GitLab CI Variables** | 适用于 GitLab CI | 保护相关分支、支持变量掩码功能 |

---

## HashiCorp Vault

### 设置

```bash
# Start Vault dev server
vault server -dev

# Set environment
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'

# Enable secrets engine
vault secrets enable -path=secret kv-v2

# Store secret
vault kv put secret/database/config username=admin password=secret
```

### 在 GitHub Actions 中使用 Vault

```yaml
name: Deploy with Vault Secrets

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Import Secrets from Vault
      uses: hashicorp/vault-action@v2
      with:
        url: https://vault.example.com:8200
        token: ${{ secrets.VAULT_TOKEN }}
        secrets: |
          secret/data/database username | DB_USERNAME ;
          secret/data/database password | DB_PASSWORD ;
          secret/data/api key | API_KEY

    - name: Use secrets
      run: |
        echo "Connecting to database as $DB_USERNAME"
        # Use $DB_PASSWORD, $API_KEY
```

### 在 GitLab CI 中使用 Vault

```yaml
deploy:
  image: vault:latest
  before_script:
    - export VAULT_ADDR=https://vault.example.com:8200
    - export VAULT_TOKEN=$VAULT_TOKEN
    - apk add curl jq
  script:
    - |
      DB_PASSWORD=$(vault kv get -field=password secret/database/config)
      API_KEY=$(vault kv get -field=key secret/api/credentials)
      echo "Deploying with secrets..."
```

---

## AWS Secrets Manager

### 存储密钥

```bash
aws secretsmanager create-secret \
  --name production/database/password \
  --secret-string "super-secret-password"
```

### 在 GitHub Actions 中获取密钥

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-west-2

- name: Get secret from AWS
  run: |
    SECRET=$(aws secretsmanager get-secret-value \
      --secret-id production/database/password \
      --query SecretString \
      --output text)
    echo "::add-mask::$SECRET"
    echo "DB_PASSWORD=$SECRET" >> $GITHUB_ENV

- name: Use secret
  run: ./deploy.sh  # $DB_PASSWORD available
```

### 与 Terraform 的集成

```hcl
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "production/database/password"
}

resource "aws_db_instance" "main" {
  allocated_storage    = 100
  engine              = "postgres"
  instance_class      = "db.t3.large"
  username            = "admin"
  password            = jsondecode(data.aws_secretsmanager_secret_version.db_password.secret_string)["password"]
}
```

---

## Kubernetes：外部密钥管理器

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: production
spec:
  provider:
    vault:
      server: "https://vault.example.com:8200"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "production"

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: database-credentials
    creationPolicy: Owner
  data:
  - secretKey: username
    remoteRef:
      key: database/config
      property: username
  - secretKey: password
    remoteRef:
      key: database/config
      property: password
```

---

## 密钥轮换

### 自动化轮换（使用 AWS Lambda）

```python
import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('secretsmanager')

    # Get current secret
    response = client.get_secret_value(SecretId='my-secret')
    current_secret = json.loads(response['SecretString'])

    # Generate new password
    new_password = generate_strong_password()

    # Update database password
    update_database_password(new_password)

    # Update secret
    client.put_secret_value(
        SecretId='my-secret',
        SecretString=json.dumps({
            'username': current_secret['username'],
            'password': new_password
        })
    )

    return {'statusCode': 200}
```

### 手动轮换流程

1. 生成新密钥
2. 更新密钥存储
3. 更新应用程序以使用新密钥
4. 验证功能是否正常
5. 废除旧密钥

---

## 密钥扫描

### 提交前钩子（Pre-commit Hook）

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for secrets with TruffleHog
docker run --rm -v "$(pwd):/repo" \
  trufflesecurity/trufflehog:latest \
  filesystem --directory=/repo

if [ $? -ne 0 ]; then
  echo "❌ Secret detected! Commit blocked."
  exit 1
fi
```

### 在 CI/CD 流程中扫描敏感信息

```yaml
secret-scan:
  stage: security
  image: trufflesecurity/trufflehog:latest
  script:
    - trufflehog filesystem .
  allow_failure: false
```

---

## 最佳实践

1. **切勿将敏感信息提交到 Git**  
2. **为不同环境配置不同的密钥**  
3. **定期轮换密钥**（最长 90 天）  
4. **实施最小权限访问策略**  
5. **启用审计日志记录**  
6. **使用密钥扫描工具（如 GitGuardian、TruffleHog）**  
7. **在日志中屏蔽敏感信息**  
8. **对静态存储的密钥进行加密**  
9. **尽可能使用临时令牌**  
10. **详细记录密钥的使用需求**  

---

## 相关技能

- `vulnerability-scanner`：用于检测代码中暴露的敏感信息  
- `api-security`：用于保护 API 凭据的安全性