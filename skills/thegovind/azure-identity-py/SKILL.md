---
name: azure-identity-py
description: |
  Azure Identity SDK for Python authentication. Use for DefaultAzureCredential, managed identity, service principals, and token caching.
  Triggers: "azure-identity", "DefaultAzureCredential", "authentication", "managed identity", "service principal", "credential".
package: azure-identity
---

# Python版Azure身份验证SDK

这是一个用于Azure SDK客户端的身份验证库，它基于Microsoft Entra ID（旧称Azure AD）进行身份验证。

## 安装

```bash
pip install azure-identity
```

## 环境变量

```bash
# Service Principal (for production/CI)
AZURE_TENANT_ID=<your-tenant-id>
AZURE_CLIENT_ID=<your-client-id>
AZURE_CLIENT_SECRET=<your-client-secret>

# User-assigned Managed Identity (optional)
AZURE_CLIENT_ID=<managed-identity-client-id>
```

## DefaultAzureCredential

这是大多数场景下推荐的认证方式。它会按顺序尝试多种认证方法：

```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# Works in local dev AND production without code changes
credential = DefaultAzureCredential()

client = BlobServiceClient(
    account_url="https://<account>.blob.core.windows.net",
    credential=credential
)
```

### 认证凭证的优先级顺序

| 顺序 | 认证凭证 | 使用场景 |
|-------|-----------|-------------|
| 1 | EnvironmentCredential | CI/CD、容器环境 |
| 2 | WorkloadIdentityCredential | Kubernetes环境 |
| 3 | ManagedIdentityCredential | Azure虚拟机、App Service、Functions环境 |
| 4 | SharedTokenCacheCredential | 仅限Windows环境 |
| 5 | VisualStudioCodeCredential | 安装了Azure扩展的VS Code |
| 6 | AzureCliCredential | 使用`az login`命令进行登录 |
| 7 | AzurePowerShellCredential | 使用`Connect-AzAccount`命令进行登录 |
| 8 | AzureDeveloperCliCredential | 使用`azd auth login`命令进行登录 |

### 自定义DefaultAzureCredential

```python
# Exclude credentials you don't need
credential = DefaultAzureCredential(
    exclude_environment_credential=True,
    exclude_shared_token_cache_credential=True,
    managed_identity_client_id="<user-assigned-mi-client-id>"  # For user-assigned MI
)

# Enable interactive browser (disabled by default)
credential = DefaultAzureCredential(
    exclude_interactive_browser_credential=False
)
```

## 各种认证凭证类型

### ManagedIdentityCredential

适用于托管在Azure上的资源（如虚拟机、App Service、Functions、AKS等）：

```python
from azure.identity import ManagedIdentityCredential

# System-assigned managed identity
credential = ManagedIdentityCredential()

# User-assigned managed identity
credential = ManagedIdentityCredential(
    client_id="<user-assigned-mi-client-id>"
)
```

### ClientSecretCredential

适用于具有客户端密钥的服务主体（service principal）：

```python
from azure.identity import ClientSecretCredential

credential = ClientSecretCredential(
    tenant_id=os.environ["AZURE_TENANT_ID"],
    client_id=os.environ["AZURE_CLIENT_ID"],
    client_secret=os.environ["AZURE_CLIENT_SECRET"]
)
```

### AzureCliCredential

使用`az login`命令中指定的账户进行登录：

```python
from azure.identity import AzureCliCredential

credential = AzureCliCredential()
```

### ChainedTokenCredential

自定义的认证凭证链：

```python
from azure.identity import (
    ChainedTokenCredential,
    ManagedIdentityCredential,
    AzureCliCredential
)

# Try managed identity first, fall back to CLI
credential = ChainedTokenCredential(
    ManagedIdentityCredential(client_id="<user-assigned-mi-client-id>"),
    AzureCliCredential()
)
```

## 认证凭证类型表

| 认证凭证 | 使用场景 | 认证方式 |
|------------|----------|-------------|
| `DefaultAzureCredential` | 大多数场景 | 自动检测认证方式 |
| `ManagedIdentityCredential` | 托管在Azure上的应用 | 使用Azure管理身份（Managed Identity） |
| `ClientSecretCredential` | 服务主体 | 使用客户端密钥（Client Secret） |
| `ClientCertificateCredential` | 服务主体 | 使用证书进行认证 |
| `AzureCliCredential` | 本地开发环境 | 使用Azure CLI进行登录 |
| `AzureDeveloperCliCredential` | 本地开发环境 | 使用Azure Developer CLI进行登录 |
| `InteractiveBrowserCredential` | 用户通过浏览器登录 | 使用浏览器OAuth进行认证 |
| `DeviceCodeCredential` | 无头/SSH环境 | 使用设备代码（Device Code）进行认证 |

## 直接获取认证令牌

```python
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

# Get token for a specific scope
token = credential.get_token("https://management.azure.com/.default")
print(f"Token expires: {token.expires_on}")

# For Azure Database for PostgreSQL
token = credential.get_token("https://ossrdbms-aad.database.windows.net/.default")
```

## 异步客户端（Async Client）

```python
from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient

async def main():
    credential = DefaultAzureCredential()
    
    async with BlobServiceClient(
        account_url="https://<account>.blob.core.windows.net",
        credential=credential
    ) as client:
        # ... async operations
        pass
    
    await credential.close()
```

## 最佳实践

1. 对于在本地和Azure环境中运行的代码，建议使用`DefaultAzureCredential`。
2. **切勿将认证凭证硬编码**——应使用环境变量或Azure管理身份（Managed Identity）。
3. 在生产环境的Azure部署中，优先使用Azure管理身份（Managed Identity）。
4. 当需要自定义认证凭证的顺序时，使用`ChainedTokenCredential`。
5. 显式关闭异步认证相关的资源，或使用上下文管理器（context managers）来管理认证凭证。
6. 对于用户分配的Azure管理身份（user-assigned managed identities），请设置`AZURE_CLIENT_ID`。
7. 删除未使用的认证凭证，以加快认证速度。