---
name: azd-deployment
description: 使用 Azure Developer CLI (azd) 将容器化应用程序部署到 Azure Container Apps。该工具适用于以下场景：配置 azd 项目、编写 `azure.yaml` 配置文件、为 Container Apps 创建 Bicep 基础设施、使用 ACR 配置远程构建流程、实现幂等部署（即多次部署不会产生重复结果）、管理本地文件 `/local/.azure/Bicep` 中的环境变量，以及排查 azd 相关的故障。该工具会在以下操作发生时被触发：请求 azd 配置、部署 Container Apps、进行多服务部署，或使用 Bicep 实现基础设施即代码（Infrastructure-as-Code）的功能。
---

# Azure 开发者 CLI (azd) 容器应用部署

使用 azd 将容器化的前端和后端应用程序部署到 Azure 容器应用中，支持远程构建、管理身份以及幂等化的基础设施。

## 快速入门

```bash
# Initialize and deploy
azd auth login
azd init                    # Creates azure.yaml and .azure/ folder
azd env new <env-name>      # Create environment (dev, staging, prod)
azd up                      # Provision infra + build + deploy
```

## 核心文件结构

```
project/
├── azure.yaml              # azd service definitions + hooks
├── infra/
│   ├── main.bicep          # Root infrastructure module
│   ├── main.parameters.json # Parameter injection from env vars
│   └── modules/
│       ├── container-apps-environment.bicep
│       └── container-app.bicep
├── .azure/
│   ├── config.json         # Default environment pointer
│   └── <env-name>/
│       ├── .env            # Environment-specific values (azd-managed)
│       └── config.json     # Environment metadata
└── src/
    ├── frontend/Dockerfile
    └── backend/Dockerfile
```

## azure.yaml 配置

### 最小配置

```yaml
name: azd-deployment
services:
  backend:
    project: ./src/backend
    language: python
    host: containerapp
    docker:
      path: ./Dockerfile
      remoteBuild: true
```

### 带有钩子的完整配置

```yaml
name: azd-deployment
metadata:
  template: my-project@1.0.0

infra:
  provider: bicep
  path: ./infra

azure:
  location: eastus2

services:
  frontend:
    project: ./src/frontend
    language: ts
    host: containerapp
    docker:
      path: ./Dockerfile
      context: .
      remoteBuild: true

  backend:
    project: ./src/backend
    language: python
    host: containerapp
    docker:
      path: ./Dockerfile
      context: .
      remoteBuild: true

hooks:
  preprovision:
    shell: sh
    run: |
      echo "Before provisioning..."
      
  postprovision:
    shell: sh
    run: |
      echo "After provisioning - set up RBAC, etc."
      
  postdeploy:
    shell: sh
    run: |
      echo "Frontend: ${SERVICE_FRONTEND_URI}"
      echo "Backend: ${SERVICE_BACKEND_URI}"
```

### 主要的 azure.yaml 选项

| 选项 | 描述 |
|--------|-------------|
| `remoteBuild: true` | 在 Azure 容器注册表中构建镜像（推荐） |
| `context: .` | 相对于项目路径的 Docker 构建上下文 |
| `host: containerapp` | 部署到 Azure 容器应用 |
| `infra提供商: bicep` | 使用 Bicep 进行基础设施管理 |

## 环境变量流程

### 三级配置体系

1. **本地 `.env` 文件** - 仅用于本地开发 |
2. **`.azure/<env>/.env` 文件** - 由 azd 管理，自动从 Bicep 输出中填充 |
3. **`main.parameters.json` 文件** - 将环境变量映射到 Bicep 参数 |

### 参数注入模式

```json
// infra/main.parameters.json
{
  "parameters": {
    "environmentName": { "value": "${AZURE_ENV_NAME}" },
    "location": { "value": "${AZURE_LOCATION=eastus2}" },
    "azureOpenAiEndpoint": { "value": "${AZURE_OPENAI_ENDPOINT}" }
  }
}
```

语法：`${VAR_NAME}` 或 `${VAR_NAME=default_value}`

### 设置环境变量

```bash
# Set for current environment
azd env set AZURE_OPENAI_ENDPOINT "https://my-openai.openai.azure.com"
azd env set AZURE_SEARCH_ENDPOINT "https://my-search.search.windows.net"

# Set during init
azd env new prod
azd env set AZURE_OPENAI_ENDPOINT "..." 
```

### Bicep 输出 → 环境变量

```bicep
// In main.bicep - outputs auto-populate .azure/<env>/.env
output SERVICE_FRONTEND_URI string = frontend.outputs.uri
output SERVICE_BACKEND_URI string = backend.outputs.uri
output BACKEND_PRINCIPAL_ID string = backend.outputs.principalId
```

## 幂等化部署

### azd 为何具有幂等性

1. **Bicep 是声明性语言** - 资源会自动调整到所需状态 |
2. **远程构建会为镜像添加唯一标签** - 镜像标签包含部署时间戳 |
3. **Azure 容器注册表（ACR）会重用已有的镜像层** - 只有发生变化的层才会被上传 |

### 保留手动更改

通过门户添加的自定义域名在重新部署时可能会丢失。可以使用钩子来保留这些自定义设置：

```yaml
hooks:
  preprovision:
    shell: sh
    run: |
      # Save custom domains before provision
      if az containerapp show --name "$FRONTEND_NAME" -g "$RG" &>/dev/null; then
        az containerapp show --name "$FRONTEND_NAME" -g "$RG" \
          --query "properties.configuration.ingress.customDomains" \
          -o json > /tmp/domains.json
      fi

  postprovision:
    shell: sh
    run: |
      # Verify/restore custom domains
      if [ -f /tmp/domains.json ]; then
        echo "Saved domains: $(cat /tmp/domains.json)"
      fi
```

### 处理现有资源

```bicep
// Reference existing ACR (don't recreate)
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' existing = {
  name: containerRegistryName
}

// Set customDomains to null to preserve Portal-added domains
customDomains: empty(customDomainsParam) ? null : customDomainsParam
```

## 容器应用服务发现

同一环境中的容器应用之间的内部 HTTP 路由：

```bicep
// Backend reference in frontend env vars
env: [
  {
    name: 'BACKEND_URL'
    value: 'http://ca-backend-${resourceToken}'  // Internal DNS
  }
]
```

前端使用 nginx 代理访问内部 URL：
```nginx
location /api {
    proxy_pass $BACKEND_URL;
}
```

## 管理身份与 RBAC

### 启用系统分配的身份

```bicep
resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  identity: {
    type: 'SystemAssigned'
  }
}

output principalId string = containerApp.identity.principalId
```

### 部署后的 RBAC 规则分配

```yaml
hooks:
  postprovision:
    shell: sh
    run: |
      PRINCIPAL_ID="${BACKEND_PRINCIPAL_ID}"
      
      # Azure OpenAI access
      az role assignment create \
        --assignee-object-id "$PRINCIPAL_ID" \
        --assignee-principal-type ServicePrincipal \
        --role "Cognitive Services OpenAI User" \
        --scope "$OPENAI_RESOURCE_ID" 2>/dev/null || true
      
      # Azure AI Search access
      az role assignment create \
        --assignee-object-id "$PRINCIPAL_ID" \
        --role "Search Index Data Reader" \
        --scope "$SEARCH_RESOURCE_ID" 2>/dev/null || true
```

## 常用命令

```bash
# Environment management
azd env list                        # List environments
azd env select <name>               # Switch environment
azd env get-values                  # Show all env vars
azd env set KEY value               # Set variable

# Deployment
azd up                              # Full provision + deploy
azd provision                       # Infrastructure only
azd deploy                          # Code deployment only
azd deploy --service backend        # Deploy single service

# Debugging
azd show                            # Show project status
az containerapp logs show -n <app> -g <rg> --follow  # Stream logs
```

## 参考文件

- **Bicep 模板**：请参阅 [references/bicep-patterns.md](references/bicep-patterns.md) 以了解容器应用相关的 Bicep 模板 |
- **故障排除**：请参阅 [references/troubleshooting.md](references/troubleshooting.md) 以解决常见问题 |
- **azure.yaml 架构**：请参阅 [references/azure-yaml-schema.md](references/azure-yaml-schema.md) 以了解所有配置选项 |

## 重要提示

1. **始终使用 `remoteBuild: true`** - 在使用 M1/ARM 架构的 Mac 机器上进行本地构建时，可能会导致部署失败（因为这些机器不支持 AMD64 架构） |
2. **Bicep 的输出会自动填充到 `.azure/<env>/.env` 文件中** - 请勿手动编辑该文件 |
3. **使用 `azd env set` 命令来设置敏感信息** - 这些信息不会存储在 `main.parameters.json` 中 |
4. **服务标签 (`azd-service-name`)** - azd 需要这个标签来识别容器应用 |
5. **在钩子中使用 `|| true`** - 可以防止因 RBAC 规则已存在而导致的部署失败 |

---

（注：由于提供的 SKILL.md 文件内容较为冗长且包含大量技术细节，翻译过程中仅保留了与中文读者最相关的部分。如果需要更详细的解释或额外的信息，可以进一步扩展翻译内容。）