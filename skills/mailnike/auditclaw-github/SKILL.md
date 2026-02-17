---
name: auditclaw-github
description: >
  **auditclaw-grc 的 GitHub 合规性证据收集**  
  共进行了 9 项只读检查，涵盖以下方面：分支保护、秘密信息扫描（secret scanning）、双重身份验证（2FA）、Dependabot、部署密钥（deploy keys）、审计日志（audit logs）、Webhook、代码所有者（CODEOWNERS）以及持续集成/持续部署（CI/CD）的安全性。
version: 1.0.1
user-invocable: true
homepage: https://www.auditclaw.ai
source: https://github.com/avansaber/auditclaw-github
metadata: {"openclaw":{"type":"executable","install":{"pip":"scripts/requirements.txt"},"requires":{"bins":["python3"],"env":["GITHUB_TOKEN"]}}}
---# AuditClaw GitHub

这是一个用于 auditclaw-grc 的辅助技能，通过只读 API 调用从 GitHub 组织中收集合规性证据。

**9 项检查 | 只读令牌权限 | 证据存储在共享的 GRC 数据库中**

## 安全模型
- **只读访问**：使用具有只读仓库和组织权限的细粒度个人访问令牌。无写入权限。
- **凭据**：使用 `GITHUB_TOKEN` 环境变量。该技能不会存储任何凭据。
- **依赖项**：`PyGithub==2.8.1`（已固定）

- **数据流**：检查结果作为证据存储在 `~/.openclaw/grc/compliance.sqlite` 文件中，通过 auditclaw-grc 进行管理。

## 先决条件
- 具有只读权限的 GitHub 个人访问令牌（或具有 `repo`、`read:org`、`security_events` 权限的经典令牌）
- 将令牌设置为 `GITHUB_TOKEN` 环境变量
- 使用 `pip install -r scripts/requirements.txt` 安装依赖项
- 已安装并初始化 auditclaw-grc 技能

## 命令
- `Run GitHub evidence sweep`：运行所有检查并将结果存储在 GRC 数据库中
- `Check branch protection`：验证分支保护规则
- `Check secret scanning`：查看秘密扫描警报
- `Check Dependabot alerts`：查看依赖项漏洞警报
- `Show GitHub integration health`：显示上次同步情况、错误信息及证据数量

## 使用方法
所有证据都存储在共享的 GRC 数据库 `~/.openclaw/grc/compliance.sqlite` 中，通过 auditclaw-grc 技能的 `db_query.py` 脚本进行访问。

**运行全面证据扫描：**
```
python3 scripts/github_evidence.py --db-path ~/.openclaw/grc/compliance.sqlite --org my-org --all
```

**运行特定检查：**
```
python3 scripts/github_evidence.py --db-path ~/.openclaw/grc/compliance.sqlite --org my-org --checks branch_protection,secret_scanning
```

## 检查类别（9 项）

| 检查 | 检查内容 |
|-------|-----------------|
| **branch_protection** | 默认分支保护规则、所需审查内容、状态检查 |
| **secret_scanning** | 是否启用了秘密扫描、活跃警报数量 |
| **dependabot** | 按严重程度分类的 Dependabot 警报、自动修复的 Pull Request |
| **two_factor** | 组织级别的双因素认证（2FA）实施情况 |
| **deploy_keys** | 部署密钥的审计情况（只读 vs 可写） |
| **audit_log** | 管理员审计日志的访问权限 |
| **webhooks** | Webhook 安全性（HTTPS、配置的 secrets） |
| **codeowners** | 仓库中是否存在 CODEOWNERS 文件 |
| **ci_cd** | GitHub Actions 的安全性、工作流权限 |

## 证据存储
每项检查生成的 evidence 都包含以下信息：
- `source: "github"`
- `type: "automated"`
- `control_id`：与相关的 SOC2/ISO/HIPAA 控制标准相对应
- `description`：人类可读的发现摘要
- `file_content`：检查结果的 JSON 详细信息

## 设置指南

当用户请求设置 GitHub 集成时，指导他们按照以下步骤操作：

### 第一步：创建细粒度个人访问令牌
引导用户访问：GitHub → 设置 → 开发者设置 → 个人访问令牌 → 细粒度令牌

### 第二步：配置令牌权限
- 名称：`auditclaw-grc`
- 到期时间：90 天（推荐）
- 资源所有者：选择他们的组织
- 仓库访问权限：所有仓库（或特定仓库）
- 权限（全部为只读）：
  - **仓库**：内容、管理权限、秘密扫描警报、Dependabot 警报、代码扫描警报、Actions、Webhooks
  - **组织**：成员（读取权限）、管理权限（读取权限）

**经典令牌替代方案：** 如果无法使用细粒度令牌，可以使用以下权限范围：`repo`、`read:org`、`security_events`

### 第三步：设置令牌
将令牌设置为 `GITHUB_TOKEN` 环境变量。

### 第四步：验证连接
运行：`python3 {baseDir}/scripts/github_evidence.py --test-connection`

具体的权限信息记录在 `scripts/github-permissions.json` 文件中。可以通过以下命令查看：`python3 {baseDir}/../auditclaw-grc/scripts/db_query.py --action show-policy --provider github`