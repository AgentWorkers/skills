---
name: auditclaw-aws
description: **AWS合规性证据收集**：用于auditclaw-grc工具的15项只读检查，涵盖S3、IAM、CloudTrail、VPC、KMS、EC2、RDS、Lambda、EBS、SQS、SNS、Secrets Manager、Config、GuardDuty以及Security Hub等服务。
version: 1.0.1
user-invocable: true
homepage: https://www.auditclaw.ai
source: https://github.com/avansaber/auditclaw-aws
metadata: {"openclaw":{"type":"executable","install":{"pip":"scripts/requirements.txt"},"requires":{"bins":["python3"],"env":["AWS_ACCESS_KEY_ID","AWS_SECRET_ACCESS_KEY"]}}}
---# AuditClaw AWS

这是一个与 `auditclaw-grc` 相配套的技能，用于通过只读 API 调用从 AWS 账户中收集合规性证据。

**15 项检查 | 只读 IAM 策略 | 证据存储在共享的 GRC 数据库中**

## 安全模型
- **只读访问**：自定义的 IAM 策略，包含 43 项只读 API 操作。没有写入/修改/删除的权限。
- **凭据**：使用标准的 AWS 凭据链（`aws configure`、环境变量或 IAM 实例角色）。该技能不会存储任何凭据。
- **依赖项**：`boto3==1.34.46`（固定版本）
- **数据流**：检查结果作为证据存储在 `~/.openclaw/grc/compliance.sqlite` 文件中，通过 `auditclaw-grc` 进行管理。

## 先决条件
- 已配置 AWS 凭据（通过 `aws configure` 或 IAM 实例角色）
- 使用 `pip install -r scripts/requirements.txt` 安装所需依赖项
- 已安装并初始化 `auditclaw-grc` 技能

## 命令
- `Run AWS evidence sweep`：运行所有检查，并将结果存储在 GRC 数据库中
- `Check S3 encryption`：运行针对 S3 的特定检查
- `Check IAM compliance`：运行针对 IAM 的特定检查
- `Check CloudTrail status`：验证 CloudTrail 的配置
- `Check VPC security`：审查 VPC 流量日志和安全组
- `Show AWS integration health`：显示最后一次同步情况、错误信息以及证据数量

## 使用方法
所有证据都存储在共享的 GRC 数据库 `~/.openclaw/grc/compliance.sqlite` 中，通过 `auditclaw-grc` 技能的 `db_query.py` 脚本进行访问。

**运行全面检查的命令：**
```
python3 scripts/aws_evidence.py --db-path ~/.openclaw/grc/compliance.sqlite --all
```

**运行特定检查的命令：**
```
python3 scripts/aws_evidence.py --db-path ~/.openclaw/grc/compliance.sqlite --checks iam,s3,cloudtrail
```

## 检查类别（共 15 项）

| 检查项 | 检查内容 |
|-------|-----------------|
| **iam** | 密码策略、多因素身份验证（MFA）的强制实施、访问密钥的轮换、未使用的凭据 |
| **s3** | 默认加密设置、公共访问控制、版本控制、访问日志记录 |
| **cloudtrail** | CloudTrail 是否启用、多区域支持、日志验证、S3 日志的传输方式 |
| **vpc** | 流量日志是否启用、安全组规则、网络访问控制列表（NACL）的配置 |
| **kms** | 密钥轮换是否启用、密钥策略、密钥的使用情况 |
| **ec2** | IMDSv2 是否启用、EBS 的加密设置、公共 IP 的暴露情况 |
| **rds** | 存储加密设置、自动备份功能、数据的公共可访问性 |
| **security_hub** | Security Hub 是否启用、按严重程度分类的活跃发现 |
| **guardduty** | 安全检测工具是否启用、活跃的检测结果、威胁情报 |
| **lambda** | Lambda 函数的运行环境、公共访问权限、VPC 的关联情况 |
| **cloudwatch** | 日志组的保留策略、指标警报的覆盖范围 |
| **config** | 配置记录器的运行状态、规则合规性 |
| **eks_ecs** | 容器集群的加密设置、日志记录、网络策略 |
| **elb** | HTTPS 监听器的配置、WAF 的关联情况、访问日志记录 |
| **credential_report** | 完整的 IAM 凭据报告分析 |

## 证据存储方式
每项检查生成的 evidence 都包含以下信息：
- `source: "aws"`：证据来源为 AWS
- `type: "automated"`：证据类型为自动化生成的
- `control_id`：与相关的 SOC2/ISO/HIPAA 控制标准相对应
- `description`：人类可读的发现摘要
- `file_content`：检查结果的 JSON 详细信息

## IAM 策略
有关所需的最低 IAM 权限，请参阅 `scripts/iam-policy.json` 文件。
遵循最小权限原则；该策略仅使用只读权限。

## 设置指南

当用户请求设置 AWS 集成时，指导他们按照以下步骤操作：

### 第一步：创建 IAM 策略
引导用户进入 AWS 控制台 → IAM → 策略 → 创建策略 → 选择 JSON 格式。
具体的策略内容位于 `scripts/iam-policy.json` 文件中。可以通过以下命令查看该策略：
```bash
python3 {baseDir}/../auditclaw-grc/scripts/db_query.py --action show-policy --provider aws
```
该策略包含了针对 14 个 AWS 服务的 43 项只读 API 操作权限。没有写入/修改/删除的权限。

### 第二步：创建 IAM 用户
用户名：`auditclaw-scanner`。将 `AuditClawReadOnly` 策略分配给该用户。
命令行操作：`aws iam create-user --user-name auditclaw-scanner`

### 第三步：生成访问密钥
在 AWS 控制台中选择“安全凭据” → “创建访问密钥”。
命令行操作：`aws iam create-access-key --user-name auditclaw-scanner`

### 第四步：配置凭据
可以通过 `aws configure` 命令配置凭据，或者将 `AWS_ACCESS_KEY_ID` 和 `AWS_SECRET_ACCESS_KEY` 设置为环境变量。

### 第五步：验证连接
运行以下命令：`python3 {baseDir}/scripts/aws_evidence.py --test-connection`
该命令会检查每个 AWS 服务的可访问性。

**不建议使用 `SecurityAudit` 或 `ViewOnlyAccess` 管理策略**。这些策略提供的访问权限远超实际需求。请始终使用我们提供的 `scripts/iam-policy.json` 中的自定义策略。