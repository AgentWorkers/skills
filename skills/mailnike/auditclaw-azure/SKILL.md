---
name: auditclaw-azure
description: Azure合规性证据收集，用于auditclaw-grc。该工具执行12项只读检查，涵盖存储、网络安全组（NSG）、密钥库（Key Vault）、SQL数据库、计算资源、App Service以及Cloud Defender等组件。
version: 1.0.1
user-invocable: true
homepage: https://www.auditclaw.ai
source: https://github.com/avansaber/auditclaw-azure
metadata: {"openclaw":{"type":"executable","install":{"pip":"scripts/requirements.txt"},"requires":{"bins":["python3"],"env":["AZURE_SUBSCRIPTION_ID","AZURE_CLIENT_ID","AZURE_CLIENT_SECRET","AZURE_TENANT_ID"]}}}
---# AuditClaw Azure

这是一个与 `auditclaw-grc` 相配套的技能，用于通过只读 API 调用从 Azure 订阅中收集合规性证据。

**包含 12 项检查 | 仅需要 `Reader` 和 `Security Reader` 角色 | 证据存储在共享的 GRC 数据库中**

## 安全模型
- **只读访问**：仅需要 `Reader` 和 `Security Reader` 角色（订阅级别）。没有写入/修改权限。
- **凭据**：使用 `DefaultAzureCredential`（服务主体环境变量、`az login` 或托管身份）。该技能不会存储任何凭据。
- **依赖项**：Azure SDK 包（全部列在 `requirements.txt` 中）。
- **数据流**：检查结果作为证据存储在 `~/.openclaw/grc/compliance.sqlite` 文件中，通过 `auditclaw-grc` 进行管理。

## 先决条件
- 配置了 Azure 凭据（服务主体或 `az login`）
- 使用 `pip install -r scripts/requirements.txt` 安装依赖项。
- 已安装并初始化了 `auditclaw-grc` 技能。

## 命令
- `Run Azure evidence sweep`：运行所有检查，并将结果存储在 GRC 数据库中。
- `Check Azure storage security`：运行针对存储的特定检查。
- `Check Azure network security`：运行网络安全检查。
- `Check Azure Key Vault`：运行 Key Vault 检查。
- `Check Azure SQL compliance`：运行 SQL Server 合规性检查。
- `Check Azure VM encryption`：运行虚拟机加密检查。
- `Check Azure App Service`：运行 App Service 检查。
- `Check Azure Defender`：运行云安全防护检查。
- `Show Azure integration health`：显示上次同步情况、错误信息及证据数量。

## 使用方法
所有证据都存储在 `~/.openclaw/grc/compliance.sqlite` 文件中的共享 GRC 数据库中，通过 `auditclaw-grc` 技能的 `db_query.py` 脚本进行访问。

**运行全面检查的命令：**
```
python3 scripts/azure_evidence.py --db-path ~/.openclaw/grc/compliance.sqlite --all
```

**运行特定检查的命令：**
```
python3 scripts/azure_evidence.py --db-path ~/.openclaw/grc/compliance.sqlite --checks storage,network,keyvault
```

**列出可用检查的命令：**
```
python3 scripts/azure_evidence.py --list-checks
```

## 检查类别（7 个文件，12 项发现）**

| 检查项 | 检查内容 |
|-------|-----------------|
| **storage** | 仅支持 HTTPS 传输，禁用 TLS 1.2 及更高版本的协议，网络默认设置为拒绝访问 |
| **network** | 网络安全组（NSG）未允许未经授权的 SSH（端口 22）和 RDP（端口 3389）连接 |
| **keyvault** | 启用了软删除和清除保护功能 |
| **sql** | 启用了服务器审计功能，所有数据库均使用了 TDE 加密 |
| **compute** | 虚拟机磁盘已加密（加密在主机端进行） |
| **appservice** | 仅支持 HTTPS 传输，并使用 TLS 1.2 及更高版本的协议 |
| **defender**：为关键资源类型启用了 Azure 安全防护（Standard 级别） |

## 认证方式
使用来自 `azure-identity` 的 `DefaultAzureCredential`。支持以下认证方式：
- 服务主体：`AZURE_CLIENT_ID` + `AZURE_TENANT_ID` + `AZURE_CLIENT_SECRET`
- Azure CLI：`az login`
- 在 Azure 中运行时使用托管身份

**最低所需角色**：`Reader` + `Security Reader`（订阅级别）

## 证据存储
每项检查产生的证据条目包含以下信息：
- `source: "azure"`：证据来源
- `type: "automated"`：证据类型为自动化检查
- `control_id`：与相关的 SOC2/ISO/HIPAA 控制标准关联
- `description`：人类可读的检查结果摘要
- `file_content`：检查结果的 JSON 详细信息

## 设置指南

当用户请求设置 Azure 集成时，指导他们按照以下步骤操作：

### 第 1 步：创建服务主体
```
az ad sp create-for-rbac --name auditclaw-scanner --role Reader --scopes /subscriptions/<SUBSCRIPTION_ID>
```

### 第 2 步：添加 `Security Reader` 角色
```
az role assignment create --assignee <APP_ID> --role "Security Reader" --scope /subscriptions/<SUBSCRIPTION_ID>
```

**只需两个角色：** `Reader` 和 `Security Reader`（订阅级别）。

### 第 3 步：配置凭据
从服务主体的输出中设置环境变量：
- `AZURE_CLIENT_ID`（应用程序 ID）
- `AZURE_CLIENT_SECRET`（密码）
- `AZURE_TENANT_ID`（租户 ID）
- `AZURE_SUBSCRIPTION_ID`（订阅 ID）

### 第 4 步：验证连接
运行命令：`python3 {baseDir}/scripts/azure_evidence.py --test-connection`

具体的角色要求在 `scripts/azure-roles.json` 文件中有详细说明。可以通过以下命令查看角色信息：
`python3 {baseDir}/../auditclaw-grc/scripts/db_query.py --action show-policy --provider azure`