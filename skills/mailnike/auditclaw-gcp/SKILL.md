---
name: auditclaw-gcp
description: >
  **auditclaw-grc 的 GCP 合规性证据收集**  
  auditclaw-grc 支持对 Cloud Storage、防火墙（Firewall）、身份与访问管理（IAM）、日志记录（Logging）、KMS（Key Management Service）、DNS（Domain Name System）、BigQuery、计算资源（Compute）以及 Cloud SQL 进行 12 项只读检查，以收集用于审计的合规性证据。
version: 1.0.1
user-invocable: true
homepage: https://www.auditclaw.ai
source: https://github.com/avansaber/auditclaw-gcp
metadata: {"openclaw":{"type":"executable","install":{"pip":"scripts/requirements.txt"},"requires":{"bins":["python3"],"env":["GCP_PROJECT_ID","GOOGLE_APPLICATION_CREDENTIALS"]}}}
---# AuditClaw GCP

这是 auditclaw-grc 的配套技能，用于通过只读 API 调用从 Google Cloud Platform (GCP) 项目中收集合规性证据。

**12 项检查 | 仅限 Viewer 和 Security Reviewer 角色 | 证据存储在共享的 GRC 数据库中**

## 安全模型
- **只读访问**：需要 6 个只读的 IAM 角色（Viewer、Security Reviewer、Cloud SQL Viewer、Logging Viewer、DNS Reader、Cloud KMS Viewer）。无写入/修改权限。
- **凭据**：使用标准的 GCP 凭据链（`GOOGLE_APPLICATION_CREDENTIALS` 或 `gcloud auth`）。该技能不会存储任何凭据。
- **依赖项**：Google Cloud SDK 包（所有依赖项均包含在 `requirements.txt` 文件中）。
- **数据流**：检查结果作为证据存储在 `~/.openclaw/grc/compliance.sqlite` 文件中，通过 auditclaw-grc 进行管理。

## 先决条件
- 配置了 GCP 凭据（使用 `gcloud auth application-default login` 或服务账户 JSON 文件）
- 设置了 `GCP_PROJECT_ID` 环境变量
- 使用 `pip install -r scripts/requirements.txt` 安装并初始化 auditclaw-grc 技能

## 命令
- `Run GCP evidence sweep`：运行所有检查，并将结果存储在 GRC 数据库中
- `Check GCP storage compliance`：检查 Cloud Storage 的合规性
- `Check GCP firewall rules`：检查防火墙规则
- `Check GCP IAM compliance`：检查 IAM 服务账户的合规性
- `Check GCP logging status`：验证审计日志配置
- `Check GCP KMS keys`：检查 KMS 密钥的轮换情况
- `Show GCP integration health`：显示上次同步信息、错误详情及证据数量

## 使用方法
所有证据都存储在共享的 GRC 数据库 `~/.openclaw/grc/compliance.sqlite` 中，通过 auditclaw-grc 的 `db_query.py` 脚本进行访问。

**运行全面检查的命令：**
```
python3 scripts/gcp_evidence.py --db-path ~/.openclaw/grc/compliance.sqlite --all
```

**运行特定检查的命令：**
```
python3 scripts/gcp_evidence.py --db-path ~/.openclaw/grc/compliance.sqlite --checks storage,firewall,iam
```

## 检查类别（9 个文件，12 项发现内容）

| 检查项目 | 检查内容 |
|-------|-----------------|
| **storage** | 确保桶级别的访问控制一致，防止公共访问 |
| **firewall** | 防止 SSH/RDP 等服务的无限制访问（0.0.0.0/0） |
| **iam** | 服务账户密钥定期轮换（90 天），限制服务账户管理员的权限 |
| **logging** | 启用审计日志记录（所有服务），并确保有日志导出功能 |
| **kms** | KMS 密钥的轮换周期不超过 90 天 |
| **dns** | 公共区域已启用 DNSSEC |
| **bigquery** | 防止所有用户（allUsers/allAuthenticatedUsers）访问公共数据集 |
| **compute** | 不存在具有 cloud-platform 权限范围的默认服务账户 |
| **cloudsql**：强制使用 SSL 协议，且没有允许公共 IP（0.0.0.0/0）访问的账户 |

## 证据存储方式
每项检查产生的证据条目包含以下信息：
- `source: "gcp"`：证据来源为 GCP
- `type: "automated"`：证据类型为自动化检查
- `control_id`：与相关的 SOC2/ISO/HIPAA 控制标准相对应
- `description`：人类可读的检查结果摘要
- `file_content`：检查结果的 JSON 详细信息

## 所需的 IAM 角色
- `roles/viewer`：具有查看权限
- `roles/iam.securityReviewer`：具有安全审查权限
- `roles/cloudsqlviewer`：具有 Cloud SQL 查看权限
- `roles/loggingviewer`：具有日志查看权限
- `roles/dnsreader`：具有 DNS 相关的查看权限
- `roles/cloudkmsviewer`：具有 KMS 相关的查看权限

所有检查仅使用只读访问权限。

## 设置指南

当用户请求设置 GCP 集成时，按照以下步骤进行指导：

### 第 1 步：创建服务账户
```
gcloud iam service-accounts create auditclaw-scanner --display-name="AuditClaw Scanner"
```

### 第 2 步：授予 IAM 角色
授予以下 6 个只读角色：
```
for role in roles/viewer roles/iam.securityReviewer roles/cloudsql.viewer roles/logging.viewer roles/dns.reader roles/cloudkms.viewer; do
  gcloud projects add-iam-policy-binding PROJECT_ID \
    --member=serviceAccount:auditclaw-scanner@PROJECT_ID.iam.gserviceaccount.com \
    --role=$role
done
```

### 第 3 步：生成 JSON 密钥
```
gcloud iam service-accounts keys create key.json --iam-account=auditclaw-scanner@PROJECT_ID.iam.gserviceaccount.com
```

### 第 4 步：配置凭据
设置环境变量：
- `GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json`
- `GCP_PROJECT_ID=your-project-id`

### 第 5 步：验证连接
运行命令：`python3 {baseDir}/scripts/gcp_evidence.py --test-connection`

具体的 IAM 角色在 `scripts/gcp-roles.json` 文件中有详细说明。可以通过以下命令查看这些角色：`python3 {baseDir}/../auditclaw-grc/scripts/db_query.py --action show-policy --provider gcp`