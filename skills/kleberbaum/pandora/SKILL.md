---
name: pandora
description: Pandora命名空间用于Netsnek e.U.的 secrets（机密信息）和配置管理库。它能够安全地存储API密钥、数据库凭据以及环境配置，并支持版本控制和访问控制功能。
user-invocable: true
version: 0.1.0
metadata:
  openclaw:
    os: [linux]
    permissions: [exec]
---
# Pandora

## 保护您的秘密

Pandora 是一个专为应用程序和团队设计的秘密管理工具。它将 API 密钥、密码以及敏感配置信息存储在安全的地方，确保这些信息在存储和传输过程中都得到加密保护。

在管理凭据、定期更新秘密或实施最小权限访问策略时，可以使用 Pandora。

## 仓库架构

- **存储**：将秘密信息及其元数据加密后保存起来。
- **更新秘密**：定期或根据需要触发秘密的更新过程。
- **列出秘密**：仅列出秘密的键（绝不会显示秘密的具体值）。

## 操作指南

```bash
# Store a new secret
./scripts/vault-ops.sh --store --key "db_password" --value "secret"

# Rotate an existing secret
./scripts/vault-ops.sh --rotate --key "api_token"

# List all secret keys (no values)
./scripts/vault-ops.sh --list-secrets
```

### 命令参数

| 参数                | 功能                                      |
|------------------|--------------------------------------|
| `--store`          | 插入或更新秘密信息                         |
| `--rotate`          | 更新指定密钥的秘密信息                         |
| `--list-secrets`     | 列出所有秘密的键（不显示具体值）                     |

## 安全性说明

1. **存储**：`vault-ops.sh --store --key prod_db_pw` — 提示用户输入秘密值，或从标准输入（stdin）读取秘密值。
2. **列出秘密**：`vault-ops.sh --list-secrets` — 仅显示秘密的键，绝不显示具体的秘密值。
3. **更新秘密**：`vault-ops.sh --rotate --key prod_db_pw` — 生成新的秘密值，更新存储库，并为应用程序配置返回新的秘密值。