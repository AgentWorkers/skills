---
name: azure-keyvault-py
description: |
  Azure Key Vault SDK for Python. Use for secrets, keys, and certificates management with secure storage.
  Triggers: "key vault", "SecretClient", "KeyClient", "CertificateClient", "secrets", "encryption keys".
package: azure-keyvault-secrets, azure-keyvault-keys, azure-keyvault-certificates
---

# Python 版 Azure Key Vault SDK

用于安全存储和管理密钥、加密密钥及证书。

## 安装

```bash
# Secrets
pip install azure-keyvault-secrets azure-identity

# Keys (cryptographic operations)
pip install azure-keyvault-keys azure-identity

# Certificates
pip install azure-keyvault-certificates azure-identity

# All
pip install azure-keyvault-secrets azure-keyvault-keys azure-keyvault-certificates azure-identity
```

## 环境变量

```bash
AZURE_KEYVAULT_URL=https://<vault-name>.vault.azure.net/
```

## 密钥（Secrets）

### SecretClient 的设置

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
vault_url = "https://<vault-name>.vault.azure.net/"

client = SecretClient(vault_url=vault_url, credential=credential)
```

### 密钥操作

```python
# Set secret
secret = client.set_secret("database-password", "super-secret-value")
print(f"Created: {secret.name}, version: {secret.properties.version}")

# Get secret
secret = client.get_secret("database-password")
print(f"Value: {secret.value}")

# Get specific version
secret = client.get_secret("database-password", version="abc123")

# List secrets (names only, not values)
for secret_properties in client.list_properties_of_secrets():
    print(f"Secret: {secret_properties.name}")

# List versions
for version in client.list_properties_of_secret_versions("database-password"):
    print(f"Version: {version.version}, Created: {version.created_on}")

# Delete secret (soft delete)
poller = client.begin_delete_secret("database-password")
deleted_secret = poller.result()

# Purge (permanent delete, if soft-delete enabled)
client.purge_deleted_secret("database-password")

# Recover deleted secret
client.begin_recover_deleted_secret("database-password").result()
```

## 密钥（Keys）

### KeyClient 的设置

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient

credential = DefaultAzureCredential()
vault_url = "https://<vault-name>.vault.azure.net/"

client = KeyClient(vault_url=vault_url, credential=credential)
```

### 密钥操作

```python
from azure.keyvault.keys import KeyType

# Create RSA key
rsa_key = client.create_rsa_key("rsa-key", size=2048)

# Create EC key
ec_key = client.create_ec_key("ec-key", curve="P-256")

# Get key
key = client.get_key("rsa-key")
print(f"Key type: {key.key_type}")

# List keys
for key_properties in client.list_properties_of_keys():
    print(f"Key: {key_properties.name}")

# Delete key
poller = client.begin_delete_key("rsa-key")
deleted_key = poller.result()
```

### 加密操作（Cryptographic Operations）

```python
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

# Get crypto client for a specific key
crypto_client = CryptographyClient(key, credential=credential)
# Or from key ID
crypto_client = CryptographyClient(
    "https://<vault>.vault.azure.net/keys/<key-name>/<version>",
    credential=credential
)

# Encrypt
plaintext = b"Hello, Key Vault!"
result = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, plaintext)
ciphertext = result.ciphertext

# Decrypt
result = crypto_client.decrypt(EncryptionAlgorithm.rsa_oaep, ciphertext)
decrypted = result.plaintext

# Sign
from azure.keyvault.keys.crypto import SignatureAlgorithm
import hashlib

digest = hashlib.sha256(b"data to sign").digest()
result = crypto_client.sign(SignatureAlgorithm.rs256, digest)
signature = result.signature

# Verify
result = crypto_client.verify(SignatureAlgorithm.rs256, digest, signature)
print(f"Valid: {result.is_valid}")
```

## 证书（Certificates）

### CertificateClient 的设置

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.certificates import CertificateClient, CertificatePolicy

credential = DefaultAzureCredential()
vault_url = "https://<vault-name>.vault.azure.net/"

client = CertificateClient(vault_url=vault_url, credential=credential)
```

### 证书操作

```python
# Create self-signed certificate
policy = CertificatePolicy.get_default()
poller = client.begin_create_certificate("my-cert", policy=policy)
certificate = poller.result()

# Get certificate
certificate = client.get_certificate("my-cert")
print(f"Thumbprint: {certificate.properties.x509_thumbprint.hex()}")

# Get certificate with private key (as secret)
from azure.keyvault.secrets import SecretClient
secret_client = SecretClient(vault_url=vault_url, credential=credential)
cert_secret = secret_client.get_secret("my-cert")
# cert_secret.value contains PEM or PKCS12

# List certificates
for cert in client.list_properties_of_certificates():
    print(f"Certificate: {cert.name}")

# Delete certificate
poller = client.begin_delete_certificate("my-cert")
deleted = poller.result()
```

## 客户端类型表（Client Types Table）

| 客户端（Client） | 包（Package） | 用途（Purpose） |
|--------|---------|---------|
| `SecretClient` | `azure-keyvault-secrets` | 存储/检索密钥 |
| `KeyClient` | `azure-keyvault-keys` | 管理加密密钥 |
| `CryptographyClient` | `azure-keyvault-keys` | 加密/解密/签名/验证 |
| `CertificateClient` | `azure-keyvault-certificates` | 管理证书 |

## 异步客户端（Async Clients）

```python
from azure.identity.aio import DefaultAzureCredential
from azure.keyvault.secrets.aio import SecretClient

async def get_secret():
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    
    async with client:
        secret = await client.get_secret("my-secret")
        print(secret.value)

import asyncio
asyncio.run(get_secret())
```

## 错误处理（Error Handling）

```python
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

try:
    secret = client.get_secret("nonexistent")
except ResourceNotFoundError:
    print("Secret not found")
except HttpResponseError as e:
    if e.status_code == 403:
        print("Access denied - check RBAC permissions")
    raise
```

## 最佳实践（Best Practices）：

1. **使用 `DefaultAzureCredential` 进行身份验证**  
2. **在 Azure 托管的应用程序中使用托管身份（managed identity）**  
3. **启用“软删除”功能以便后续恢复数据（默认已启用）**  
4. **使用基于角色的访问控制（RBAC）而非简单的访问策略来实现细粒度控制**  
5. **定期通过版本控制机制轮换密钥**  
6. **在 App Service/Function 的配置中引用 Key Vault 的资源**  
7. **适当缓存密钥以减少 API 调用次数**  
8. **在高吞吐量场景下使用异步客户端**