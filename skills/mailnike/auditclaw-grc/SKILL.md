---
name: auditclaw-grc
description: OpenClaw 的 AI 内置 GRC（治理、风险与合规）功能：支持 13 个框架中的 97 项合规性要求，包括 SOC 2、ISO 27001、HIPAA、GDPR、NIST CSF、PCI DSS、CIS Controls、CMMC、HITRUST、CCPA、FedRAMP、ISO 42001 和 SOX ITGC。该功能可管理各类控制措施、相关证据、风险信息、政策文档、供应商信息、安全事件、资产信息、培训记录、漏洞详情、访问权限审核结果以及调查问卷等。同时能够生成合规性评分报告、仪表盘数据以及信任中心页面，并支持安全头部信息（security headers）的验证、SSL 证书的检测以及 GDPR 合规性检查。此外，还可通过配套工具与 AWS、Azure、GCP、GitHub 以及身份认证服务提供商进行集成。
version: 1.0.0
user-invocable: true
homepage: https://www.auditclaw.ai
source: https://github.com/avansaber/auditclaw-grc
metadata: {"openclaw":{"type":"executable","install":{"pip":"scripts/requirements.txt","post":"python3 scripts/init_db.py"},"requires":{"bins":["python3"],"anyBins":["chromium","google-chrome","brave","chromium-browser"],"env":[],"optionalEnv":["AWS_ACCESS_KEY_ID","GITHUB_TOKEN","AZURE_SUBSCRIPTION_ID","GCP_PROJECT_ID","GOOGLE_APPLICATION_CREDENTIALS","GOOGLE_WORKSPACE_SA_KEY","OKTA_ORG_URL"]},"os":["darwin","linux"]}}
---
# AuditClaw GRC

AuditClaw GRC 是一个专为 OpenClaw 设计的 AI 驱动的安全治理与合规 (GRC) 辅助工具，能够管理合规框架、控制措施、风险信息、政策文件、供应商信息、事件记录、资产清单、培训记录、漏洞数据、访问审查结果以及问卷调查内容。

**功能概览：**
- **支持 97 种操作**  
- **关联 30 个表格**  
- **涵盖 13 个主流合规框架**  
- **管理超过 990 条控制措施**

## 安全模型

- **数据库**：使用 SQLite 数据库（路径：`~/.openclaw/grc/compliance.sqlite`），采用 WAL 模式存储数据，仅允许数据库所有者（权限：0o600）进行读写操作。
- **凭证管理**：凭证信息存储在 `~/.openclaw/grc/credentials/` 目录下，每个提供商的凭证文件具有独立的权限设置（目录权限：0o700，文件权限：0o600）。所有写入操作都是原子的，并且在删除前会用随机字节覆盖数据以确保安全性。敏感信息从不会被记录或公开。具体实现细节请参考 `scripts/credential_store.py` 文件。
- **信任中心**：仅生成本地 HTML 报告，不会对外发布任何数据。用户可自行决定报告的托管方式。
- **依赖库**：依赖 `requests`（版本：2.31.0）用于处理 HTTP 请求头信息；对于云服务集成，可选地使用 `boto3`（针对 AWS）和 `PyJWT`（针对 Azure）。这些依赖库仅在用户安装并配置相应凭证后才会被激活。
- **扫描机制**：所有安全扫描（包括请求头检查、SSL 证书验证和 GDPR 相关检查）都在本地执行，且仅针对用户指定的 URL 进行。
- **数据传输限制**：所有数据操作都在本地完成，或仅发送到用户配置的云服务账户。

### 可选的环境变量（用于云服务集成）

这些环境变量对于 AuditClaw 的核心功能是**非必需的**，仅在用户通过相关插件配置云服务集成时才会使用：

| 变量                | 用途                                      |
|-------------------|----------------------------------------|
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` | 用于 AWS 服务集成（通过 auditclaw-aws 插件）         |
| `GITHUB_TOKEN`         | 用于 GitHub 服务集成（通过 auditclaw-github 插件）         |
| `AZURE_SUBSCRIPTION_ID` / `AZURE_CLIENT_ID` | 用于 Azure 服务集成（通过 auditclaw-azure 插件）         |
| `GCP PROJECT_ID` / `GOOGLE_APPLICATION_CREDENTIALS` | 用于 GCP 服务集成（通过 auditclaw-gcp 插件）         |
| `GOOGLE_WORKSPACE_SA_KEY` / `GOOGLE_WORKSPACE_ADMIN_EMAIL` | 用于 Google Workspace 服务集成（通过 auditclaw-idp 插件）     |
| `OKTA_ORG_URL` / `OKTA_API_TOKEN` | 用于 Okta 服务集成（通过 auditclaw-idp 插件）         |

## 设置流程

```bash
python3 {baseDir}/scripts/init_db.py
pip install -r {baseDir}/scripts/requirements.txt
```

## 数据展示与格式化

- 以格式化后的摘要形式呈现数据，而非原始的 JSON 格式。
- 每条消息的长度限制在 4096 个字符以内。
- 显示前 5-10 条记录，并提供“是否需要查看完整列表”的选项。
- 使用表情符号表示状态：✅ 表示已完成，⚠️ 表示存在风险，🔴 表示情况危急，📊 表示报告生成中，📋 表示安全相关内容。
- 提供上下文信息，例如“已完成 23/43 条控制措施（53%）”，而不仅仅是简单的数字“23”。
- 每条操作完成后，会提示用户下一步应执行的操作。

## 激活条件

- 当用户选择合规性检查（compliance）、GRC 管理、SOC 2 标准、ISO 27001、HIPAA、GDPR、NIST、PCI DSS、CIS、CMMC、HITRUST、CCPA、FedRAMP、ISO 42001、SOX、ITGC 等相关选项时，AuditClaw GRC 会被激活。

## 数据库操作

所有数据库查询操作均通过以下命令执行：
```bash
python3 {baseDir}/scripts/db_query.py --action <action> [args]
```
查询结果将以 JSON 格式返回，系统会将其解析为易于阅读的摘要。如需查看完整的操作参数信息，请参考文件：`{baseDir}/references/db_actions.md`。

### 核心操作列表

| 操作                | 功能                                      |
|-------------------|----------------------------------------|
| `status`            | 显示整体合规性状况                        |
| `activate-framework --slug soc2`    | 加载指定框架的控制措施                    |
| `gap-analysis --framework soc2`    | 分析框架中的合规性差距及所需改进措施            |
| `score-history --framework soc2`    | 查看指定框架的合规性评分趋势                |
| `list-controls --framework soc2 --status in_progress` | 列出指定框架中处于进行中的控制措施            |
| `update-control --id 5 --status complete` | 更新指定控制措施的状态（可批量操作：`--id 1,2,3`）       |
| `add-evidence --title "..." --control-ids 1,2,3` | 记录相关证据                        |
| `add-risk --title "..." --likelihood 3 --impact 4` | 登录风险信息                        |
| `add-vendor --name "..." --criticality high` | 注册新的供应商                        |
| `add-incident --title "..." --severity critical` | 记录安全事件                        |
| `generate-report --framework soc2` | 生成指定框架的合规性报告                |
| `generate-dashboard`       | 生成包含仪表盘的 HTML 报告                  |
| `export-evidence --framework soc2` | 生成可供审计人员使用的证据文件包                |
| `list-companions`       | 显示已安装的辅助工具列表                        |

### 其他操作类别

- **政策管理**：添加新政策、更新政策版本、提交审批、审核政策内容、要求供应商确认等。
- **培训管理**：添加培训模块、分配培训任务、跟踪培训完成情况、列出未完成的培训项目。
- **漏洞管理**：添加漏洞信息（附带 CVE/CVSS 分类）、跟踪漏洞修复进度。
- **访问审查**：创建审查计划、添加审查项目、批准或撤销审查结果。
- **问卷调查**：创建问卷模板、发送给相关方、收集反馈并评分。
- **事件管理**：记录事件详情（包含时间线）、进行事件后的审查、统计平均处理时间（MTTR）。
- **资产管理**：对资产进行分类管理、记录资产生命周期、设置加密/备份/补丁状态。
- **警报管理**：添加新的警报、列出所有警报、确认警报状态、解决警报问题。
- **集成管理**：添加新的云服务提供商、测试连接、提供集成配置指南等。

## 框架激活

使用以下命令激活指定的合规框架：
```bash
python3 {baseDir}/scripts/db_query.py --action activate-framework --slug <slug>
```
**支持的合规框架示例：**
- **SOC 2 Type II**         | 43 条控制措施
- **ISO 27001:2022**       | 114 条控制措施
- **HIPAA Security Rule**     | 29 条控制措施
- **GDPR**           | 25 条控制措施
- **NIST CSF**          | 31 条控制措施
- **PCI DSS v4.0**        | 30 条控制措施
- **CIS Controls v8**       | 153 条控制措施
- **CMMC 2.0**         | 113 条控制措施
- **HITRUST CSF v11**       | 152 条控制措施
- **CCPA/CPRA**         | 28 条控制措施
- **FedRAMP Moderate**      | 282 条控制措施
- **ISO 42001:2023**       | 40 条控制措施
- **SOX ITGC**         | 50 条控制措施

更多框架的详细信息请参考文件：`{baseDir}/references/frameworks/`。

## 合规性评分

使用以下命令获取合规性评分：
```bash
python3 {baseDir}/scripts/compliance_score.py --framework <slug> [--store]
```
评分范围为 0-100 分，系统会显示评分分布、评分趋势以及评分变化情况。使用 `--store` 选项可保存评分结果以供后续跟踪。评分算法的详细信息请参考文件：`{baseDir}/references/scoring-methodology.md`。

## 安全扫描

- **请求头检查**：`python3 {baseDir}/scripts/check_headers.py --url <url>`（检查 CSP、HSTS、X-Frame-Options 等安全设置）。
- **SSL/TLS 证书验证**：`python3 {baseDir}/scripts/check_ssl.py --domain <domain>`（验证 SSL 证书的有效性、证书链和加密算法）。
- **GDPR 合规性检查**：基于 Chromium 浏览器检测用户对隐私政策的同意情况。

扫描完成后，系统会提供将扫描结果保存为证据文件的选项。

## 报告与数据导出

- **生成报告**：`python3 {baseDir}/scripts/generate_report.py --framework <slug> --format html`
- **生成信任中心报告**：`python3 {baseDir}/scripts/generate_trust_center.py --org-name "Acme Corp"`
- **导出证据文件**：`python3 {baseDir}/scripts/export_evidence.py --framework <slug>`

## 交互式操作流程

- **首次设置**：当用户首次设置合规性检查时，系统会静默初始化数据库，展示各框架的选项及控制措施数量，并在激活后提供合规性差距分析。
- **智能默认设置**：根据操作上下文自动推断证据类型（手动/自动化/集成模式）；在保存风险信息前会提示用户确认风险评估结果。
- **主动建议**：在激活框架后建议进行差距分析或云服务集成设置；在完成部分控制措施后建议重新计算评分；扫描完成后建议保存扫描结果；评分低于 30% 时建议优先处理关键控制措施；评分高于 90% 时建议生成审计报告。

## 命令行快捷操作

| 命令            | 功能                                      |
|-------------------|----------------------------------------|
| `/grc-score`        | 快速查看合规性评分                        |
| `/grc-gaps`        | 查看合规性差距                        |
| `/grc-scan`        | 启动安全扫描                        |
| `/grc-report`        | 生成合规性报告                        |
| `/grc-risks`        | 查看所有风险信息                        |
| `/grc-incidents`        | 查看当前发生的事件                        |
| `/grc-trust`        | 生成信任中心报告                        |

## 定时任务（通过 Cron 任务触发）

- **证据文件过期提醒**：每天早上 7 点自动发送提醒。
- **评分重新计算**：每 6 小时自动重新计算评分。
- **每周总结报告**：每周一早上 8 点发送每周总结报告。

## 辅助工具

AuditClaw 提供了一系列可选的辅助工具，用于自动化收集云服务相关的证据数据。这些工具会将收集到的证据导入到共享的 GRC 数据库中：

| 工具名称            | 检查内容                                      | 设置要求                                      |
|-------------------|----------------------------------------|----------------------------------------|
| **auditclaw-aws**      | 检查 AWS 相关服务（如 S3、IAM、CloudTrail 等）         | 需配置仅读权限的 IAM 角色                    |
| **auditclaw-github**      | 检查 GitHub 相关服务（如分支保护、秘密管理、2FA 等）       | 需设置 `GITHUB_TOKEN` 环境变量                |
| **auditclaw-azure**      | 检查 Azure 相关服务（如存储资源、NSG、Key Vault 等）       | 需设置服务 principal 及安全权限                |
| **auditclaw-gcp**      | 检查 GCP 相关服务（如存储资源、防火墙、IAM 等）       | 需设置 `GOOGLE_APPLICATION_CREDENTIALS`                  |
| **auditclaw-idp**      | 检查 Google Workspace 和 Okta 相关服务             | 需设置 SA 密钥及 Okta API 令牌                    |

安装方法：`clawhub install auditclaw-<provider>`

如果用户需要连接新的云服务提供商，请先使用 `list-companions` 命令查看可用的辅助工具列表。如果相关工具未安装，系统会提示用户进行安装。

## 集成指南

- 使用 `setup aws`、`setup github` 等命令获取详细的集成步骤及权限设置指南。
- 在执行扫描前，可以使用 `test aws connection` 命令测试连接是否正常。

## 参考文件

- `{baseDir}/references/db_actions.md`：包含所有操作的详细参数参考。
- `{baseDir}/references/schema.md`：数据库架构文档。
- `{baseDir}/references/scoring-methodology.md`：评分算法说明。
- `{baseDir}/referencescommands/`：命令使用指南。
- `{baseDir}/references/frameworks/`：各合规框架的详细文档。
- `{baseDir}/references/integrations/`：云服务集成指南。