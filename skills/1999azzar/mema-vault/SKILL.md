---
name: mema-vault
description: 使用 AES-256（Fernet）加密技术的安全凭证管理器。该工具通过强制性的“主密钥”来存储、检索和轮换敏感信息（如 API 密钥、数据库凭据等）。
metadata: {"openclaw":{"requires":{"env":["MEMA_VAULT_MASTER_KEY"]},"install":[{"id":"pip","kind":"exec","command":"pip install cryptography"}]}}
---
# Mema Vault

## 前提条件
- **密钥**: 必须设置为环境变量 `MEMA_VAULT_MASTER_KEY`。
- **依赖项**: 需要 `cryptography` Python 包。

## 核心工作流程

### 1. 存储凭证
对新的凭证进行加密并保存。
- **用法**: `python3 $WORKSPACE/skills/mema-vault/scripts/vault.py set <service> <user> <password> [--meta "info"]`

### 2. 获取凭证
检索凭证。默认情况下，密码会在输出中被屏蔽。
- **用法**: `python3 $WORKSPACE/skills/mema-vault/scripts/vault.py get <service>`
- **显示原始内容**: 仅在需要安全注入时使用 `--show` 标志。

### 3. 列出凭证
- **用法**: `python3 $WORKSPACE/skills/mema-vault/scripts/vault.py list`

## 安全标准
- **加密**: 使用 AES-256 CBC 算法进行加密，并结合 PBKDF2HMAC 加密算法（迭代次数为 480,000 次）。
- **屏蔽**: 除非明确要求，否则凭证信息会在标准日志/输出中被屏蔽。
- **隔离**: 密钥绝不能以明文形式存储在磁盘上。