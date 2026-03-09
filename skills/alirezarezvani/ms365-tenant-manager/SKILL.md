---
name: "ms365-tenant-manager"
description: >
  **Microsoft 365租户管理工具（适用于全局管理员）**  
  该工具可自动化M365租户的配置、Office 365管理任务、Azure AD用户管理、Exchange Online配置以及Teams管理流程，并支持安全策略的制定。它能够生成用于批量操作的PowerShell脚本，实现条件访问策略的配置、许可证管理以及合规性报告的生成。适用于M365租户管理员、Office 365管理员、Azure AD用户及全局管理员，可用于租户配置及Microsoft 365相关自动化工作。
---
# Microsoft 365 租户管理器

为 Microsoft 365 全局管理员提供专业指导与自动化工具，帮助管理租户设置、用户生命周期、安全策略及组织优化。

---

## 快速入门

### 运行安全审计

```powershell
Connect-MgGraph -Scopes "Directory.Read.All","Policy.Read.All","AuditLog.Read.All"
Get-MgSubscribedSku | Select-Object SkuPartNumber, ConsumedUnits, @{N="Total";E={$_.PrepaidUnits.Enabled}}
Get-MgPolicyAuthorizationPolicy | Select-Object AllowInvitesFrom, DefaultUserRolePermissions
```

### 从 CSV 文件批量配置用户

```powershell
# CSV columns: DisplayName, UserPrincipalName, Department, LicenseSku
Import-Csv .\new_users.csv | ForEach-Object {
    $passwordProfile = @{ Password = (New-Guid).ToString().Substring(0,16) + "!"; ForceChangePasswordNextSignIn = $true }
    New-MgUser -DisplayName $_.DisplayName -UserPrincipalName $_.UserPrincipalName `
               -Department $_.Department -AccountEnabled -PasswordProfile $passwordProfile
}
```

### 创建条件访问策略（针对管理员启用多因素认证）

```powershell
$adminRoles = (Get-MgDirectoryRole | Where-Object { $_.DisplayName -match "Admin" }).Id
$policy = @{
    DisplayName = "Require MFA for Admins"
    State = "enabledForReportingButNotEnforced"   # Start in report-only mode
    Conditions = @{ Users = @{ IncludeRoles = $adminRoles } }
    GrantControls = @{ Operator = "OR"; BuiltInControls = @("mfa") }
}
New-MgIdentityConditionalAccessPolicy -BodyParameter $policy
```

---

## 工作流程

### 工作流程 1：新租户设置

**步骤 1：生成设置检查清单**

在配置用户之前，请确认以下前提条件：
- 已创建并启用多因素认证的全局管理员账户
- 已购买自定义域名，并可进行 DNS 编辑
- 确认所需的许可证 SKU（注意 E3 与 E5 特性的不同要求）

**步骤 2：配置并验证 DNS 记录**

```powershell
# After adding the domain in the M365 admin center, verify propagation before proceeding
$domain = "company.com"
Resolve-DnsName -Name "_msdcs.$domain" -Type NS -ErrorAction SilentlyContinue
# Also run from a shell prompt:
# nslookup -type=MX company.com
# nslookup -type=TXT company.com   # confirm SPF record
```

等待 DNS 记录传播完成（最长 48 小时），然后再进行批量用户创建。

**步骤 3：应用安全基线**

```powershell
# Disable legacy authentication (blocks Basic Auth protocols)
$policy = @{
    DisplayName = "Block Legacy Authentication"
    State = "enabled"
    Conditions = @{ ClientAppTypes = @("exchangeActiveSync","other") }
    GrantControls = @{ Operator = "OR"; BuiltInControls = @("block") }
}
New-MgIdentityConditionalAccessPolicy -BodyParameter $policy

# Enable unified audit log
Set-AdminAuditLogConfig -UnifiedAuditLogIngestionEnabled $true
```

**步骤 4：配置用户**

```powershell
$licenseSku = (Get-MgSubscribedSku | Where-Object { $_.SkuPartNumber -eq "ENTERPRISEPACK" }).SkuId

Import-Csv .\employees.csv | ForEach-Object {
    try {
        $user = New-MgUser -DisplayName $_.DisplayName -UserPrincipalName $_.UserPrincipalName `
                           -AccountEnabled -PasswordProfile @{ Password = (New-Guid).ToString().Substring(0,12)+"!"; ForceChangePasswordNextSignIn = $true }
        Set-MgUserLicense -UserId $user.Id -AddLicenses @(@{ SkuId = $licenseSku }) -RemoveLicenses @()
        Write-Host "Provisioned: $($_.UserPrincipalName)"
    } catch {
        Write-Warning "Failed $($_.UserPrincipalName): $_"
    }
}
```

**验证：** 在 Microsoft 365 管理门户中抽查 3–5 个用户账户，确认其许可证状态为“活动”（Active）。

---

### 工作流程 2：安全强化

**步骤 1：运行安全审计**

```powershell
Connect-MgGraph -Scopes "Directory.Read.All","Policy.Read.All","AuditLog.Read.All","Reports.Read.All"

# Export Conditional Access policy inventory
Get-MgIdentityConditionalAccessPolicy | Select-Object DisplayName, State |
    Export-Csv .\ca_policies.csv -NoTypeInformation

# Find accounts without MFA registered
$report = Get-MgReportAuthenticationMethodUserRegistrationDetail
$report | Where-Object { -not $_.IsMfaRegistered } |
    Select-Object UserPrincipalName, IsMfaRegistered |
    Export-Csv .\no_mfa_users.csv -NoTypeInformation

Write-Host "Audit complete. Review ca_policies.csv and no_mfa_users.csv."
```

**步骤 2：首先创建仅用于报告的多因素认证策略**

```powershell
$policy = @{
    DisplayName = "Require MFA All Users"
    State = "enabledForReportingButNotEnforced"
    Conditions = @{ Users = @{ IncludeUsers = @("All") } }
    GrantControls = @{ Operator = "OR"; BuiltInControls = @("mfa") }
}
New-MgIdentityConditionalAccessPolicy -BodyParameter $policy
```

**验证：** 48 小时后，查看 Entra ID 的登录日志，确认目标用户会被提示输入多因素认证信息；然后将策略状态更改为“启用”（Enabled）。

**步骤 3：查看安全评分**

```powershell
# Retrieve current Secure Score and top improvement actions
Get-MgSecuritySecureScore -Top 1 | Select-Object CurrentScore, MaxScore, ActiveUserCount
Get-MgSecuritySecureScoreControlProfile | Sort-Object -Property ActionType |
    Select-Object Title, ImplementationStatus, MaxScore | Format-Table -AutoSize
```

---

### 工作流程 3：用户离职处理

**步骤 1：阻止登录并终止会话**

```powershell
$upn = "departing.user@company.com"
$user = Get-MgUser -Filter "userPrincipalName eq '$upn'"

# Block sign-in immediately
Update-MgUser -UserId $user.Id -AccountEnabled:$false

# Revoke all active tokens
Invoke-MgInvalidateAllUserRefreshToken -UserId $user.Id
Write-Host "Sign-in blocked and sessions revoked for $upn"
```

**步骤 2：使用 `-WhatIf` 功能预览离职操作（包括许可证移除的影响）**

```powershell
# Identify assigned licenses
$licenses = (Get-MgUserLicenseDetail -UserId $user.Id).SkuId

# Dry-run: print what would be removed
$licenses | ForEach-Object { Write-Host "[WhatIf] Would remove SKU: $_" }
```

**步骤 3：执行离职处理**

```powershell
# Remove licenses
Set-MgUserLicense -UserId $user.Id -AddLicenses @() -RemoveLicenses $licenses

# Convert mailbox to shared (requires ExchangeOnlineManagement module)
Set-Mailbox -Identity $upn -Type Shared

# Remove from all groups
Get-MgUserMemberOf -UserId $user.Id | ForEach-Object {
    try { Remove-MgGroupMemberByRef -GroupId $_.Id -DirectoryObjectId $user.Id } catch {}
}
Write-Host "Offboarding complete for $upn"
```

**验证：** 在 Microsoft 365 管理门户中确认用户账户状态为“已阻止”（Blocked），且没有活动许可证，邮箱类型为“共享”（Shared）。

---

## 最佳实践

### 租户设置

1. 在添加用户之前启用多因素认证
2. 为条件访问策略配置相关位置信息
3. 为管理员账户配置个人身份信息（PIM）
4. 在批量创建用户之前验证自定义域名及 DNS 记录的传播情况
5. 遵循 Microsoft 安全评分的建议

### 安全操作

1. 先以仅用于报告的模式启用条件访问策略
2. 在实施新策略前查看登录日志（至少 48 小时）
3. 不要在脚本中硬编码凭据——使用 Azure Key Vault 或 `Get-Credential` 来获取凭据
4. 为所有操作启用统一审计日志记录
5. 每季度进行安全审查和安全评分检查

### PowerShell 自动化

1. 建议优先使用 Microsoft Graph（`Microsoft.Graph` 模块）而非旧版的 MSOnline
2. 使用 `try/catch` 块进行错误处理
3. 通过 `Write-Host`/`Write-Warning` 输出日志以记录操作过程
4. 在执行批量破坏性操作前使用 `-WhatIf` 功能进行预览
5. 先在非生产环境中进行测试

---

## 参考指南

**references/powershell-templates.md**
- 可直接使用的脚本模板
- 条件访问策略示例
- 批量用户配置脚本
- 安全审计脚本

**references/security-policies.md**
- 条件访问策略配置指南
- 多因素认证策略实施方法
- 数据丢失防护（DLP）和数据保留策略
- 安全基线设置

**references/troubleshooting.md**
- 常见问题解决方案
- PowerShell 模块相关问题
- 权限问题排查
- DNS 记录传播问题

---

## 限制

| 限制 | 影响 |
|------------|--------|
| 需要全局管理员权限 | 完整的租户设置需要最高权限 |
| API 使用频率限制 | 批量操作可能会受到速率限制 |
| 许可证依赖性 | 高级功能需要 E3 或 E5 许可证 |
| 混合环境 | 需要额外配置本地 AD（On-premises AD） |
| PowerShell 使用要求 | 需要 `Microsoft.Graph` 模块 |

### 所需的 PowerShell 模块

```powershell
Install-Module Microsoft.Graph -Scope CurrentUser
Install-Module ExchangeOnlineManagement -Scope CurrentUser
Install-Module MicrosoftTeams -Scope CurrentUser
```

### 所需权限

- **全局管理员权限** — 全面管理租户设置
- **用户管理员权限** — 用户管理
- **安全管理员权限** — 安全策略管理
- **Exchange 管理员权限** — 邮箱管理