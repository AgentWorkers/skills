---
name: azure-bicep-deploy
description: Deploy and validate Azure Bicep files and ARM templates. Use for: (1) Deploying Bicep (.bicep) or ARM (JSON) templates to Azure, (2) Validating Bicep/ARM templates for syntax errors, (3) Creating Azure resources via Bicep, (4) Managing multi-environment deployments (dev/staging/prod) via parameters. Supports Azure Container Apps commonly used workloads. Prerequisites: Azure CLI (az) installed, Azure CLI authenticated (az login), Bicep CLI installed (az bicep install), appropriate Azure subscription access.
---

# Azure Bicep 部署

## 先决条件（必需）

在使用此功能之前，请确保满足以下要求：

1. **已安装 Azure CLI**  
   ```bash
   az --version
   ```  
   安装地址：https://docs.microsoft.com/cli/azure/install-azure-cli

2. **已登录 Azure CLI**  
   ```bash
   az login          # Interactive login
   az login --tenant <tenant-id>  # For specific tenant
   az account show   # Verify logged in
   ```

3. **选择了正确的订阅**（如果有多个订阅）  
   ```bash
   az account list                           # List subscriptions
   az account set --subscription <sub-id>   # Switch subscription
   ```

4. **已安装 Bicep CLI**  
   ```bash
   az bicep install      # Install Bicep
   az bicep version      # Verify installation
   ```  
   或者使用内置命令：`az deployment group create`（该命令会自动编译 Bicep 脚本）

### 部署 Bicep 脚本

```bash
az deployment group create \
  --resource-group <rg-name> \
  --template-file <path-to-bicep> \
  --parameters <params-file>.json
```

### 部署 ARM 模板

```bash
az deployment group create \
  --resource-group <rg-name> \
  --template-file <path-to-arm.json> \
  --parameters <params-file>.json
```

### 预测试模板（What-If 模拟）

```bash
az deployment group what-if \
  --resource-group <rg-name> \
  --template-file <path-to-bicep>
```

### 仅验证语法（针对 Bicep 脚本）

```bash
az bicep build --file <bicep-file>
```

## 多环境部署

为每个环境使用单独的参数文件：

```
params/
├── dev.bicepparam      # or dev.json
├── staging.bicepparam  # or staging.json
└── prod.bicepparam     # or prod.json
```

根据环境进行部署：

```bash
az deployment group create \
  --resource-group <rg>-dev \
  --template-file main.bicep \
  --parameters @params/dev.json
```

## Azure 容器应用

有关容器应用的详细信息，请参阅 [references/container-apps.md](references/container-apps.md)，内容包括：
- 基本容器部署
- 入口（Ingress）配置
- 扩展规则
- 版本管理

## 创建新资源

当需要通过 Bicep 创建 Azure 资源时，请执行以下操作：
1. 检查 `references/` 目录下是否有适合您需求的现有模板。
2. 对于容器应用，请使用 `assets/container-app/` 目录中的示例模板。
3. 对于其他资源，可以使用 `az bicep build-params --file` 命令生成新的模板，或参考 Azure 快速启动模板（QuickStart Templates）。

## 脚本

可以从参考文档中复制脚本，或直接使用以下脚本：
- [references/deploy.md](references/deploy.md) — 带有环境选择的部署脚本
- [references/validate.md](references/validate.md) — 验证脚本及预测试功能
- [references/bicep-build.md](references/bicep-build.md) — 用于将 Bicep 脚本编译为 ARM 模板

**快速部署（只需复制并粘贴一行代码）：**
```bash
az deployment group create --resource-group <rg> --template-file main.bicep --parameters @params/dev.json
```