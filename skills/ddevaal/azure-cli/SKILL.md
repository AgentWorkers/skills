---
name: Azure CLI
description: 通过命令行接口实现对 Azure 云平台的全面管理
license: MIT
metadata:
  author: Dennis de Vaal <d.devaal@gmail.com>
  version: "1.0.0"
  keywords: "azure,cloud,infrastructure,devops,iac,management,scripting"
repository: https://github.com/Azure/azure-cli
compatibility:
  - platform: macOS
    min_version: "10.12"
  - platform: Linux
    min_version: "Ubuntu 18.04"
  - platform: Windows
    min_version: "Windows 10"
---

# Azure CLI 技能

**掌握 Azure 命令行接口，用于云基础设施管理、自动化和 DevOps 工作流程。**

Azure CLI 是微软提供的强大跨平台命令行工具，用于管理 Azure 资源。本技能涵盖了 Azure CLI 命令、身份验证、资源管理以及自动化模式的全面知识。

## 学习内容

### 核心概念
- Azure 订阅和资源组架构
- 身份验证方法和凭据管理
- 资源提供者的组织和注册
- 全局参数、输出格式和查询语法
- 自动化脚本和错误处理

### 主要服务领域（66 个命令模块）
- **计算服务：** 虚拟机、扩展集、Kubernetes (AKS)、容器
- **网络服务：** 虚拟网络、负载均衡器、CDN、流量管理器
- **存储与数据：** 存储账户、数据湖、Cosmos DB、数据库
- **应用服务：** App Service、函数、容器应用
- **数据库：** SQL Server、MySQL、PostgreSQL、CosmosDB
- **集成与消息传递：** 事件中心、服务总线、逻辑应用
- **监控与管理：** Azure Monitor、策略管理、RBAC（角色基于访问控制）、成本管理
- **人工智能与机器学习：** 认知服务、机器学习
- **DevOps：** Azure DevOps、管道、扩展程序

## 快速入门

### 安装

**macOS：**
```bash
brew install azure-cli
```

**Linux (Ubuntu/Debian：**
```bash
curl -sL https://aka.ms/InstallAzureCliLinux | bash
```

**Windows：**
```powershell
choco install azure-cli
# Or download MSI from https://aka.ms/InstallAzureCliWindowsMSI
```

**验证安装：**
```bash
az --version          # Show version
az --help             # Show general help
```

### 第一步

```bash
# 1. Login to Azure (opens browser for authentication)
az login

# 2. View your subscriptions
az account list

# 3. Set default subscription (optional)
az account set --subscription "My Subscription"

# 4. Create a resource group
az group create -g myResourceGroup -l eastus

# 5. List your resource groups
az group list
```

## 必备命令

### 身份验证与账户
```bash
az login                                    # Interactive login
az login --service-principal -u APP_ID -p PASSWORD -t TENANT_ID
az login --identity                         # Managed identity
az logout                                   # Sign out
az account show                             # Current account
az account list                             # All accounts
az account set --subscription SUBSCRIPTION  # Set default
```

### 全局标志（适用于任何命令）
```bash
--subscription ID       # Target subscription
--resource-group -g RG  # Target resource group
--output -o json|table|tsv|yaml  # Output format
--query JMESPATH_QUERY  # Filter/extract output
--verbose -v            # Verbose output
--debug                 # Debug mode
--help -h               # Command help
```

### 资源组
```bash
az group list           # List all resource groups
az group create -g RG -l LOCATION  # Create
az group delete -g RG   # Delete
az group show -g RG     # Get details
az group update -g RG --tags key=value  # Update tags
```

### 虚拟机（计算服务）
```bash
az vm create -g RG -n VM_NAME --image UbuntuLTS
az vm list -g RG
az vm show -g RG -n VM_NAME
az vm start -g RG -n VM_NAME
az vm stop -g RG -n VM_NAME
az vm restart -g RG -n VM_NAME
az vm delete -g RG -n VM_NAME
```

### 存储操作
```bash
az storage account create -g RG -n ACCOUNT --sku Standard_LRS
az storage account list
az storage container create --account-name ACCOUNT -n CONTAINER
az storage blob upload --account-name ACCOUNT -c CONTAINER -n BLOB -f LOCAL_FILE
az storage blob download --account-name ACCOUNT -c CONTAINER -n BLOB -f LOCAL_FILE
```

### Azure Kubernetes 服务 (AKS)
```bash
az aks create -g RG -n CLUSTER --node-count 2
az aks get-credentials -g RG -n CLUSTER
az aks list
az aks show -g RG -n CLUSTER
az aks delete -g RG -n CLUSTER
```

## 常见模式

### 模式 1：输出格式化
```bash
# Get only specific fields
az vm list --query "[].{name: name, state: powerState}"

# Get just the names
az vm list --query "[].name" -o tsv

# Filter and extract
az vm list --query "[?powerState=='VM running'].name"
```

### 模式 2：自动化与脚本编写
```bash
#!/bin/bash
set -e  # Exit on error

# Get VM ID
VM_ID=$(az vm create \
  -g myRG \
  -n myVM \
  --image UbuntuLTS \
  --query id \
  --output tsv)

echo "Created VM: $VM_ID"

# Check provisioning state
az vm show --ids "$VM_ID" --query provisioningState
```

### 模式 3：批量操作
```bash
# Delete all VMs in a resource group
az vm list -g myRG -d --query "[].id" -o tsv | xargs az vm delete --ids

# List all resources by tag
az resource list --tag env=production
```

### 模式 4：使用默认值
```bash
# Set defaults to reduce typing
az configure --defaults group=myRG subscription=mySubscription location=eastus

# Now commands are simpler
az vm create -n myVM --image UbuntuLTS  # group, subscription, location inherited
```

## 辅助脚本

本技能包含一些用于常见操作的辅助 Bash 脚本：
- **azure-vm-status.sh** — 检查整个订阅范围内的虚拟机状态
- **azure-resource-cleanup.sh** — 识别并删除未使用的资源
- **azure-storage-analysis.sh** — 分析存储账户的使用情况和成本
- **azure-subscription-info.sh** — 获取订阅配额和限制
- **azure-rg-deploy.sh** — 部署带有监控功能的基础设施

**使用方法：**
```bash
./scripts/azure-vm-status.sh -g myResourceGroup
./scripts/azure-storage-analysis.sh --subscription mySubscription
```

## 高级主题

### 使用 JMESPath 进行输出查询
Azure CLI 支持使用 JMESPath 进行强大的输出过滤：
```bash
# Sort results
az vm list --query "sort_by([], &name)"

# Complex filtering
az vm list --query "[?location=='eastus' && powerState=='VM running'].name"

# Aggregation
az vm list --query "length([])"  # Count VMs
```

### 错误处理
```bash
# Check exit codes
az vm create -g RG -n VM --image UbuntuLTS
if [ $? -eq 0 ]; then
  echo "VM created successfully"
else
  echo "Failed to create VM"
  exit 1
fi
```

### 身份验证方法
- **服务主体（自动化）：**
```bash
az login --service-principal \
  --username $AZURE_CLIENT_ID \
  --password $AZURE_CLIENT_SECRET \
  --tenant $AZURE_TENANT_ID
```

- **托管身份（Azure 资源）：**
```bash
# On an Azure VM or Container Instance
az login --identity
```

- **基于令牌的身份验证（CI/CD）：**
```bash
echo "$AZURE_ACCESS_TOKEN" | az login --service-principal -u $AZURE_CLIENT_ID --password-stdin --tenant $AZURE_TENANT_ID
```

## 关键资源
- **官方文档：** https://learn.microsoft.com/en-us/cli/azure/
- **命令参考：** https://learn.microsoft.com/en-us/cli/azure/reference-index
- **GitHub 仓库：** https://github.com/Azure/azure-cli
- **综合指南：** 查看 [references/REFERENCE.md](references/REFERENCE.md)
- **版本说明：** https://github.com/Azure/azure-cli/releases

## 提示与技巧
1. **启用 Tab 完成：**
   ```bash
   # macOS with Homebrew
   eval "$(az completion init zsh)"
   
   # Linux (bash)
   eval "$(az completion init bash)"
   ```

2. **快速查找命令：**
   ```bash
   az find "create virtual machine"  # Search for commands
   ```

3. **对耗时操作使用 `--no-wait` 选项：**
   ```bash
   az vm create -g RG -n VM --image UbuntuLTS --no-wait
   # Check status later with az vm show
   ```

4. **保存常用参数：**
   ```bash
   az configure --defaults group=myRG location=eastus
   ```

5. **与其他工具结合使用：**
   ```bash
   # Use with jq for advanced JSON processing
   az vm list | jq '.[] | select(.powerState == "VM running") | .name'
   
   # Use with xargs for batch operations
   az storage account list --query "[].name" -o tsv | xargs -I {} az storage account show -g RG -n {}
   ```

## 下一步
- 阅读 [references/REFERENCE.md](references/REFERENCE.md) 以获取完整的命令文档
- 浏览 `scripts/` 目录中的辅助脚本
- 先在非生产环境中进行练习
- 学习 Azure 的最佳实践和成本优化策略

---

**版本：** 1.0.0  
**许可证：** MIT  
**兼容版本：** Azure CLI v2.50+ 及更高版本，需具备 Azure 订阅权限