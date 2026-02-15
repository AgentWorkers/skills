---
name: ms365-tenant-manager
description: **Microsoft 365租户管理工具（适用于全局管理员）**  
该工具可自动化M365租户的配置、Office 365管理任务、Azure AD用户管理、Exchange Online配置以及Teams管理流程，并支持安全策略的制定。它能够生成用于批量操作的PowerShell脚本，实现条件访问控制策略、许可证管理及合规性报告的自动化处理。适用于M365租户管理员、Office 365管理员、Azure AD用户及全局管理员，适用于租户配置及Microsoft 365相关自动化场景。
---

# Microsoft 365 租户管理器

为 Microsoft 365 全局管理员提供专家指导与自动化工具，帮助管理租户设置、用户生命周期、安全策略及组织优化。

---

## 目录

- [触发短语](#trigger-phrases)
- [快速入门](#quick-start)
- [工具](#tools)
- [工作流程](#workflows)
- [最佳实践](#best-practices)
- [参考指南](#reference-guides)
- [限制](#limitations)

---

## 触发短语

当您听到以下需求时，请使用此技能：
- “设置 Microsoft 365 租户”
- “创建 Office 365 用户”
- “配置 Azure AD”
- “生成用于 M365 的 PowerShell 脚本”
- “设置条件访问（Conditional Access）”
- “批量用户配置”
- “M365 安全审计”
- “许可证管理”
- “Exchange Online 配置”
- “Teams 管理”

---

## 快速入门

### 生成安全审计脚本

```bash
python scripts/powershell_generator.py --action audit --output audit_script.ps1
```

### 创建批量用户配置脚本

```bash
python scripts/user_management.py --action provision --csv users.csv --license E3
```

### 配置条件访问策略

```bash
python scripts/powershell_generator.py --action conditional-access --require-mfa --include-admins
```

---

## 工具

### powershell_generator.py

生成可用于 Microsoft 365 管理的 PowerShell 脚本。

**使用方法：**

```bash
# Generate security audit script
python scripts/powershell_generator.py --action audit

# Generate Conditional Access policy script
python scripts/powershell_generator.py --action conditional-access \
  --policy-name "Require MFA for Admins" \
  --require-mfa \
  --include-users "All"

# Generate bulk license assignment script
python scripts/powershell_generator.py --action license \
  --csv users.csv \
  --sku "ENTERPRISEPACK"
```

**参数：**

| 参数 | 是否必填 | 说明 |
|-----------|----------|-------------|
| `--action` | 是 | 脚本类型：`audit`（审计）、`conditional-access`（条件访问）、`license`（许可证）、`users`（用户） |
| `--policy-name` | 否 | 条件访问策略的名称 |
| `--require-mfa` | 否 | 是否在策略中要求多因素认证（MFA） |
| `--include-users` | 否 | 要包含的用户：`All`（全部）或特定 UPN（用户统一资源名称） |
| `--csv` | 否 | 用于批量操作的 CSV 文件路径 |
| `--sku` | 否 | 要分配的许可证 SKU（产品密钥） |
| `--output` | 否 | 输出文件路径（默认：stdout） |

**输出：** 包含错误处理、日志记录及最佳实践的完整 PowerShell 脚本。

### user_management.py

自动化用户生命周期操作和批量用户配置。

**使用方法：**

```bash
# Provision users from CSV
python scripts/user_management.py --action provision --csv new_users.csv

# Offboard user securely
python scripts/user_management.py --action offboard --user john.doe@company.com

# Generate inactive users report
python scripts/user_management.py --action report-inactive --days 90
```

**参数：**

| 参数 | 是否必填 | 说明 |
|-----------|----------|-------------|
| `--action` | 是 | 操作类型：`provision`（配置用户）、`offboard`（注销用户）、`report-inactive`（报告不活跃用户）、`sync`（同步数据） |
| `--csv` | 否 | 用于批量操作的 CSV 文件 |
| `--user` | 否 | 单个用户的 UPN（用户统一资源名称） |
| `--days` | 否 | 不活跃用户的阈值（默认：90 天） |
| `--license` | 否 | 要分配的许可证 SKU |

### tenant_setup.py

初始化租户配置和服务配置自动化。

**使用方法：**

```bash
# Generate tenant setup checklist
python scripts/tenant_setup.py --action checklist --company "Acme Inc" --users 50

# Generate DNS records configuration
python scripts/tenant_setup.py --action dns --domain acme.com

# Generate security baseline script
python scripts/tenant_setup.py --action security-baseline
```

---

## 工作流程

### 工作流程 1：新租户设置

**步骤 1：生成设置检查清单**

```bash
python scripts/tenant_setup.py --action checklist --company "Company Name" --users 100
```

**步骤 2：配置 DNS 记录**

```bash
python scripts/tenant_setup.py --action dns --domain company.com
```

**步骤 3：应用安全基线**

```bash
python scripts/powershell_generator.py --action audit > initial_audit.ps1
```

**步骤 4：配置用户**

```bash
python scripts/user_management.py --action provision --csv employees.csv --license E3
```

### 工作流程 2：安全强化

**步骤 1：运行安全审计**

```bash
python scripts/powershell_generator.py --action audit --output security_audit.ps1
```

**步骤 2：创建多因素认证策略**

```bash
python scripts/powershell_generator.py --action conditional-access \
  --policy-name "Require MFA All Users" \
  --require-mfa \
  --include-users "All"
```

**步骤 3：查看结果**

执行生成的脚本，并查看输出目录中的 CSV 报告。

### 工作流程 3：用户注销

**步骤 1：生成注销脚本**

```bash
python scripts/user_management.py --action offboard --user departing.user@company.com
```

**步骤 2：使用 `-WhatIf` 参数测试脚本**

```powershell
.\offboard_user.ps1 -WhatIf
```

**步骤 3：实际执行脚本**

```powershell
.\offboard_user.ps1 -Confirm:$false
```

---

## 最佳实践

### 租户设置

1. 在添加用户之前启用多因素认证（MFA）。
2. 为条件访问（Conditional Access）配置指定的位置。
3. 使用具有 PIM（Personal Information Management）功能的独立管理员账户。
4. 在批量创建用户之前验证自定义域名。
5. 遵循 Microsoft 安全评分建议。

### 安全操作

1. 以仅报告模式启动条件访问策略。
2. 在执行脚本之前使用 `-WhatIf` 参数进行测试。
3. 不要在脚本中硬编码凭证。
4. 为所有操作启用审计日志记录。
5. 定期进行季度安全审查。

### PowerShell 自动化

1. 尽量使用 Microsoft Graph 模块而非旧的 MSOnline 模块。
2. 使用 try/catch 块进行错误处理。
3. 实施日志记录以追踪操作过程。
4. 使用 Azure Key Vault 管理凭证。
5. 先在非生产环境中进行测试。

---

## 参考指南

### 各参考资料的用途

**references/powershell-templates.md**

- 可直接使用的脚本模板
- 条件访问策略示例
- 批量用户配置脚本
- 安全审计脚本

**references/security-policies.md**

- 条件访问配置指南
- 多因素认证策略
- 数据丢失防护（DLP）和保留策略
- 安全基线设置

**references/troubleshooting.md**

- 常见问题解决方法
- PowerShell 模块相关问题
- 权限问题排查
- DNS 传播问题

---

## 限制

| 限制 | 影响 |
|------------|--------|
| 需要全局管理员权限 | 完整的租户设置需要最高权限 |
| API 使用率限制 | 批量操作可能会受到速率限制 |
| 许可证依赖性 | 高级功能需要 E3/E5 许可证 |
| 混合环境 | 需要额外配置本地 AD（On-premises AD） |
| PowerShell 先决条件 | 需要 Microsoft.Graph 模块 |

### 所需 PowerShell 模块

```powershell
Install-Module Microsoft.Graph -Scope CurrentUser
Install-Module ExchangeOnlineManagement -Scope CurrentUser
Install-Module MicrosoftTeams -Scope CurrentUser
```

### 所需权限

- **全局管理员（Global Administrator）**：完整租户设置
- **用户管理员（User Administrator）**：用户管理
- **安全管理员（Security Administrator）**：安全策略管理
- **Exchange 管理员（Exchange Administrator）**：邮箱管理