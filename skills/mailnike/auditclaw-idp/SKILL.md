---
name: auditclaw-idp
description: >
  **auditclaw-grc 的身份提供者合规性检查**  
  这些检查涵盖了 Google Workspace（多因素认证 (MFA)、管理员审计、未活跃用户以及密码管理）以及 Okta（多因素认证 (MFA)、密码策略、未活跃用户和会话策略）方面的 8 项读-only（仅读取）功能。
version: 1.0.0
user-invocable: true
homepage: https://www.auditclaw.ai
source: https://github.com/avansaber/auditclaw-idp
metadata: {"openclaw":{"type":"executable","install":{"pip":"scripts/requirements.txt"},"requires":{"bins":["python3"],"env":[],"optionalEnv":["GOOGLE_WORKSPACE_SA_KEY","GOOGLE_WORKSPACE_ADMIN_EMAIL","OKTA_ORG_URL","OKTA_API_TOKEN"]}}}
---# AuditClaw IDP

这是一个与 `auditclaw-grc` 相配套的技能，用于通过只读 API 调用从 Google Workspace 和 Okta 身份提供者收集合规性证据。

**8 项检查 | 只读 API 访问 | 证据存储在共享的 GRC 数据库中**

## 安全模型
- **只读访问**：Google Workspace 仅使用 `admin_directory.user.readonly` 权限范围；Okta 仅使用 `okta.users.read`、`okta.factors.read`、`okta.policies.read` 权限范围。无写入/修改权限。
- **凭据**：使用每个提供者的标准环境变量。该技能不会存储任何凭据。
- **依赖项**：Google API 客户端 + 请求（均包含在 `requirements.txt` 文件中）
- **数据流**：检查结果作为证据存储在 `~/.openclaw/grc/compliance.sqlite` 文件中，通过 `auditclaw-grc` 进行管理。

## 先决条件
- **Google Workspace**：具有域范围委派权限的服务账户 JSON 文件，以及用于身份验证的管理员邮箱。
- **Okta**：具有只读权限范围的 API 令牌（SSWS）。
- 已安装并初始化 `auditclaw-grc` 技能。

## 环境变量

### Google Workspace（可选；未配置时可跳过）
- `GOOGLE_WORKSPACE_SA_KEY`：服务账户 JSON 文件的路径
- `GOOGLE_WORKSPACE_ADMIN_EMAIL`：用于身份验证的超级管理员邮箱

### Okta（可选；未配置时可跳过）
- `OKTA_ORG_URL`：Okta 组织 URL（例如：https://mycompany.okta.com）
- `OKTA_API_TOKEN`：Okta API 令牌

## 命令
- `Run IDP evidence sweep`：运行所有已配置提供者的检查
- `Check Google Workspace MFA`：运行 Google 多因素认证（MFA）检查
- `Check Okta password policies`：运行 Okta 密码策略检查
- `Show IDP integration health`：显示上次同步情况、错误信息及证据数量

## 使用方法
所有证据都存储在 `~/.openclaw/grc/compliance.sqlite` 文件中的共享 GRC 数据库中，通过 `auditclaw-grc` 技能的 `db_query.py` 脚本进行访问。

**运行全面检查（所有已配置的提供者）：**
```
python3 scripts/idp_evidence.py --db-path ~/.openclaw/grc/compliance.sqlite --all
```

**针对特定提供者运行检查：**
```
python3 scripts/idp_evidence.py --db-path ~/.openclaw/grc/compliance.sqlite --provider google
python3 scripts/idp_evidence.py --db-path ~/.openclaw/grc/compliance.sqlite --provider okta
```

**运行特定检查：**
```
python3 scripts/idp_evidence.py --db-path ~/.openclaw/grc/compliance.sqlite --checks google_mfa,okta_mfa
```

## 检查类别（共 8 项）
| 检查项 | 提供者 | 检查内容 |
|-------|----------|-----------------|
| **google_mfa** | Google Workspace | 所有活跃用户是否已启用并使用多因素认证 |
| **google_admins** | Google Workspace | 超级管理员的数量及是否都使用了多因素认证 |
| **googleinactive** | Google Workspace | 是否有超过 90 天未登录的活跃用户 |
| **google_passwords** | Google Workspace | 所有用户的密码强度是否为“强密码” |
| **okta_mfa** | Okta | 所有活跃用户是否至少启用了一个多因素认证因素 |
| **okta_passwords** | Okta | 密码策略是否满足最小长度要求（≥12 个字符）、历史记录要求（≥5 次修改）及最大尝试次数限制（≤5 次） |
| **okta_inactive** | Okta | 是否有超过 90 天未登录的活跃用户 |
| **okta_sessions** | Okta | 是否要求多因素认证、会话有效期是否≤12 小时、空闲时间是否≤1 小时 |

## 证据存储
每项检查产生的证据条目包含以下信息：
- `source: "idp"`  
- `type: "automated"`  
- `control_id`：与相关的 SOC2/ISO/NIST/HIPAA 控制标准相对应  
- `description`：人类可读的检查结果摘要  
- `file_content`：检查结果的 JSON 详细信息

## 设置指南
AuditClaw 支持两种身份提供者。您可以配置其中一种或两种。

### Google Workspace 设置

**步骤 1：启用 Admin SDK API**
- 登录 Google Cloud 控制台 → “APIs & Services” → “Library” → 启用 “Admin SDK API”。

**步骤 2：创建服务账户**
- 进入 “IAM & Admin” → “Service Accounts” → 创建服务账户，并启用域范围委派。

**步骤 3：授予 OAuth 权限**
- 在 Google Admin 中 → “Security” → “API controls” → “Domain-wide delegation”，为服务账户添加以下权限：
  - `https://www.googleapis.com/auth/admin_directory.user.readonly`
  - `https://www.googleapis.com/auth/admin.reports.audit.readonly`

**步骤 4：设置环境变量**
- `GOOGLE_WORKSPACE_SA_KEY`：服务账户 JSON 文件的路径
- `GOOGLE_WORKSPACE_ADMIN_EMAIL`：用于身份验证的超级管理员邮箱

### Okta 设置

**步骤 1：创建 API 令牌**
- 进入 Okta Admin → “Security” → “API” → “Tokens” → 创建令牌，名称设置为 `auditclaw-scanner`。

**步骤 2：设置所需权限**
该令牌继承创建它的管理员的权限，需要具有以下访问权限：用户信息、认证因素及策略信息。
- 权限范围：`okta.users.read`、`okta.factors.read`、`okta.policies.read`

**步骤 3：设置环境变量**
- `OKTA_ORG_URL`：Okta 组织 URL（例如：https://mycompany.okta.com）
- `OKTA_API_TOKEN`：Okta API 令牌

**验证连接**
运行命令：`python3 {baseDir}/scripts/idp_evidence.py --test-connection`

完整的权限信息记录在 `scripts/idp-permissions.json` 文件中。可以通过以下命令查看权限详情：
`python3 {baseDir}/../auditclaw-grc/scripts/db_query.py --action show-policy --provider idp`