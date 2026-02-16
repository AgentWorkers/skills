---
name: auditclaw-grc
description: OpenClaw的AI原生GRC（治理、风险与合规）解决方案：支持13个框架下的97项管理任务，包括SOC 2、ISO 27001、HIPAA、GDPR、NIST CSF、PCI DSS、CIS Controls、CMMC、HITRUST、CCPA、FedRAMP、ISO 42001以及SOX ITGC。该解决方案能够管理各类控制措施、相关证据、风险信息、政策文件、供应商信息、事件记录、资产信息、培训记录、漏洞数据、访问权限审核结果以及调查问卷内容。同时，它还能生成合规性评估报告、仪表板以及信任中心页面，并执行安全头部信息检查（security header checks）、SSL验证以及GDPR合规性扫描。此外，通过配套功能，该解决方案还能与AWS、Azure、GCP、GitHub以及身份认证服务提供商进行集成。
version: 6.0.1
user-invocable: true
metadata: {"openclaw":{"type":"executable","requires":{"bins":["python3"],"anyBins":["chromium","google-chrome","brave","chromium-browser"],"env":[]},"os":["darwin","linux"]}}
---
# AuditClaw GRC

AuditClaw GRC 是一个专为 OpenClaw 设计的 AI 驱动的 GRC（Governance, Risk, and Compliance）辅助工具，用于管理合规性框架、控制措施、风险、政策、供应商、事件、资产、培训、漏洞、访问审查以及问卷调查等内容。

**功能概览：**
- **支持 97 种操作**  
- **管理 30 个表格**  
- **涵盖 13 个合规性框架**  
- **包含 990 多项控制措施**

## 安全模型

- **数据库**：使用 SQLite 数据库（路径：`~/.openclaw/grc/compliance.sqlite`），采用 WAL 模式，仅允许数据库所有者访问（权限设置：0o600）。
- **凭证管理**：凭证存储在 `~/.openclaw/grc/credentials/` 目录下，按供应商分类存储，同样仅允许所有者访问（目录权限：0o700，文件权限：0o600）。所有写操作都是原子的，并且在删除前会用随机字节覆盖数据以防止数据泄露。敏感信息不会被记录或显示在输出结果中。
- **信任中心**：仅生成本地 HTML 文件，不会对外公开任何数据。用户可以自行决定将文件托管在哪里。
- **依赖库**：依赖 `requests` 库（版本：2.31.0），用于解析 HTTP 请求头。没有其他运行时依赖项。
- **扫描功能**：所有安全扫描（包括请求头检查、SSL 安全性检查以及 GDPR 相关检查）都在本地进行，并且仅针对用户指定的 URL 进行。

## 设置与配置

```bash
python3 {baseDir}/scripts/init_db.py
pip install -r {baseDir}/scripts/requirements.txt
```

数据库：`~/.openclaw/grc/compliance.sqlite`

## 数据展示与格式化

- 以格式化的方式呈现数据，而非原始的 JSON 格式。
- 每条消息的长度限制在 4096 个字符以内。
- 显示前 5-10 条记录，并提供“是否需要查看完整列表”的选项。
- 使用表情符号表示状态：✅ 表示已完成，⚠️ 表示存在风险，🔴 表示严重风险，📊 表示报告，📋 表示安全相关内容。
- 提供上下文信息，例如“23/43 项控制措施已完成（完成率为 53%”。

## 激活条件

当满足以下条件时，AuditClaw GRC 会自动激活：
- 合规性检查相关操作
- GRC 相关操作
- SOC 2 标准相关操作
- ISO 27001 标准相关操作
- HIPAA 标准相关操作
- GDPR 标准相关操作
- NIST 标准相关操作
- PCI DSS 标准相关操作
- CIS 标准相关操作
- CMMC 标准相关操作
- HITRUST 标准相关操作
- CCPA 标准相关操作
- FedRAMP 标准相关操作
- ISO 42001 标准相关操作
- SOX 标准相关操作
- 控制措施相关操作
- 证据管理相关操作
- 风险管理相关操作
- 审计相关操作
- 差异分析相关操作
- 安全态势评估相关操作
- 合规性评分相关操作
- 框架配置相关操作
- 安全扫描相关操作

## 数据库操作

所有数据库查询操作均通过以下命令执行：
`python3 {baseDir}/scripts/db_query.py --action <action> [args]`

查询结果以 JSON 格式返回，系统会将其解析为易于阅读的摘要。如需查看完整的操作说明及所有参数，可参考文件：`{baseDir}/references/db_actions.md`

### 核心操作

| 操作 | 功能 |
|--------|---------|
| `status` | 显示整体合规性状况 |
| `activate-framework --slug soc2` | 加载特定框架的控制措施 |
| `gap-analysis --framework soc2` | 分析该框架的合规性差距及所需改进措施 |
| `score-history --framework soc2` | 查看该框架的合规性评分趋势 |
| `list-controls --framework soc2 --status in_progress` | 列出该框架中处于“进行中”状态的控制措施 |
| `update-control --id 5 --status complete` | 更新指定控制措施的状态（也可批量更新：`--id 1,2,3`） |
| `add-evidence --title "..." --control-ids 1,2,3` | 记录相关证据 |
| `add-risk --title "..." --likelihood 3 --impact 4` | 记录风险信息 |
| `add-vendor --name "..." --criticality high` | 注册供应商信息 |
| `add-incident --title "..." --severity critical` | 记录事件信息 |
| `generate-report --framework soc2` | 生成该框架的合规性报告 |
| `generate-dashboard` | 生成包含仪表盘的 HTML 报告 |
| `export-evidence --framework soc2` | 生成用于审计的 ZIP 包 |
| `list-companions` | 显示已安装的辅助工具 |

### 其他操作类别

- **政策管理**：添加、更新、提交审批、审核政策内容，并要求相关人员确认。
- **培训管理**：添加培训模块、分配培训任务、跟踪培训完成情况、列出逾期未完成的培训项目。
- **漏洞管理**：添加漏洞信息（包括 CVE/CVSS 编号），并跟踪漏洞的修复情况。
- **访问审查**：创建审查计划、添加审查项目、批准或撤销审查结果。
- **问卷调查**：创建问卷模板、发送给相关方、收集并统计调查结果。
- **事件管理**：记录事件发生的时间线、进行事件后的审查、并提供平均处理时间（MTTR）等统计信息。
- **资产管理**：对资产进行分类、管理资产生命周期、设置加密/备份/补丁策略。
- **警报管理**：添加警报、列出警报信息、确认警报状态、解决警报问题。
- **集成管理**：添加云服务提供商、测试连接、提供集成指南等。

## 框架激活

使用以下命令激活特定框架：
`python3 {baseDir}/scripts/db_query.py --action activate-framework --slug <slug>`

| 框架名称 | 符号 | 控制措施数量 |
|-----------|------|----------|
| SOC 2 Type II | soc2 | 43 |
| ISO 27001:2022 | iso27001 | 114 |
| HIPAA Security Rule | hipaa | 29 |
| GDPR | gdpr | 25 |
| NIST CSF | nist-csf | 31 |
| PCI DSS v4.0 | pci-dss | 30 |
| CIS Controls v8 | cis-controls | 153 |
| CMMC 2.0 | cmmc | 113 |
| HITRUST CSF v11 | hitrust | 152 |
| CCPA/CPRA | ccpa | 28 |
| FedRAMP Moderate | fedramp | 282 |
| ISO 42001:2023 | iso42001 | 40 |
| SOX ITGC | sox-itgc | 50 |

相关框架的详细文档请参考：`{baseDir}/references/frameworks/`

## 合规性评分

使用以下命令获取合规性评分：
`python3 {baseDir}/scripts/compliance_score.py [--framework <slug>] [--store]`

评分范围为 0-100，系统会显示评分分布、评分趋势以及评分变化情况。使用 `--store` 选项可保存评分结果以供后续跟踪。评分算法的详细信息请参考文件：`{baseDir}/references/scoring-methodology.md`

## 安全扫描

- **请求头检查**：`python3 {baseDir}/scripts/check_headers.py --url <url>`（用于检查 CSP、HSTS、X-Frame-Options 等安全设置）。
- **SSL/TLS 安全性检查**：`python3 {baseDir}/scripts/check_ssl.py --domain <domain>`（用于检查证书的有效性、证书链和加密算法）。
- **GDPR 合规性检查**：基于 Chromium 浏览器进行 cookie 同意机制的验证。

扫描完成后，系统会提供将扫描结果保存为证据的选项。

## 报告与导出

- **生成报告**：`python3 {baseDir}/scripts/generate_report.py --framework <slug> --format html`  
- **信任中心报告**：`python3 {baseDir}/scripts/generate_trust_center.py --org-name "Acme Corp"`（仅生成本地 HTML 文件）  
- **证据导出**：`python3 {baseDir}/scripts/export_evidence.py --framework <slug>`  

## 交互式流程

- **首次设置**：当用户首次设置合规性检查时，系统会静默初始化数据库，展示各框架的选项及控制措施的数量和使用场景，并在激活后提供差距分析建议。
- **智能默认设置**：
  - 根据上下文自动判断证据类型（手动收集、自动收集或通过集成方式收集）。
  - 在保存风险信息前，系统会提示用户确认风险的可能性和影响程度。
  - 在执行批量操作时，系统会明确显示所有会发生变化的内容，并要求用户确认操作内容。
- **主动建议**：
  - 激活框架后，系统会建议进行差距分析及云服务集成设置。
  - 完成控制措施后，系统会建议重新计算合规性评分。
  - 扫描完成后，系统会建议将扫描结果保存为证据。
  - 如果合规性评分低于 30%，系统会优先处理关键控制措施；如果评分高于 90%，系统会建议生成审计报告。

## 命令行操作

| 命令 | 功能 |
|---------|--------|
| `/grc-score` | 快速获取合规性评分 |
| `/grc-gaps` | 查看合规性差距 |
| `/grc-scan` | 进入安全扫描界面 |
| `/grc-report` | 生成合规性报告 |
| `/grc-risks` | 查看风险列表 |
| `/grc-incidents` | 查看当前发生的事件 |
| `/grc-trust` | 生成信任中心相关报告 |

## 定时警报（通过 Cron 任务触发）

使用 OpenClaw 的 Cron 工具设置定时任务：
- 每天早上 7 点检查证据是否过期。
- 每 6 小时重新计算合规性评分。
- 每周周一早上 8 点生成每周总结报告。

**辅助工具**

AuditClaw 提供了一系列可选的自动化云服务集成工具，用于收集证据。这些工具会将收集到的证据导入到共享的 GRC 数据库中。

| 工具名称 | 检查内容 | 设置要求 |
|---------|--------|--------|
| **auditclaw-aws** | 检查 AWS 服务的 15 项安全配置（如 S3、IAM、CloudTrail 等） | 需要配置具有只读权限的 AWS IAM 角色（`aws configure`） |
| **auditclaw-github** | 检查 GitHub 服务的 9 项安全配置（如分支保护、 secrets 设置、2FA 等） | 需要设置 `GITHUB_TOKEN` 环境变量 |
| **auditclaw-azure** | 检查 Azure 服务的 12 项安全配置（如存储、NSG、Key Vault 等） | 需要设置具有读取和审核权限的 Azure 服务账户 |
| **auditclaw-gcp** | 检查 GCP 服务的 12 项安全配置（如存储、防火墙、IAM 等） | 需要设置具有读取和审核权限的 GCP 服务账户 |
| **auditclaw-idp** | 检查 Google Workspace 和 Okta 的身份验证配置 | 需要设置相应的服务账户和 API 令牌 |

安装这些辅助工具的命令为：`clawhub install auditclaw-<provider>`  

如果用户需要连接新的云服务提供商，建议先使用 `list-companions` 命令查看可用的工具列表。如果相关工具尚未安装，系统会提供安装指南。

## 集成指南

例如，要设置 AWS 集成，可以输入 `setup aws`；要设置 GitHub 集成，可以输入 `setup github`。系统会提供详细的安装步骤和所需的权限信息。在运行扫描之前，建议先使用 `test aws connection` 命令测试连接是否正常。

## 参考文件

- `{baseDir}/references/db_actions.md`：包含所有操作的详细说明及参数信息。
- `{baseDir}/references/schema.md`：数据库架构文档。
- `{baseDir}/references/scoring-methodology.md`：评分算法的详细说明。
- `{baseDir}/referencescommands/`：命令使用指南。
- `{baseDir}/references/frameworks/`：各合规性框架的详细文档。
- `{baseDir}/references/integrations/`：云服务集成指南。