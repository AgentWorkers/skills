---
name: mail-caduceus
description: "不要再把邮件误投到垃圾邮件文件夹里了。Mail Caduceus 通过提供品牌化的发件人分类、增强邮件安全性以及实现对邮件整个生命周期的全面控制，大幅提升了收件箱的可靠性。"
homepage: https://github.com/lmtlssss/mail-caduceus
metadata: {"openclaw":{"emoji":"📬","requires":{"bins":["bash","pwsh","python3","jq","rg"],"env":["ENTRA_CLIENT_ID","ENTRA_TENANT_ID","ENTRA_CLIENT_SECRET","EXCHANGE_DEFAULT_MAILBOX","EXCHANGE_ORGANIZATION","CLOUDFLARE_API_TOKEN","CLOUDFLARE_ZONE_ID"]}}}
---
# Mail Caduceus

Mail Caduceus 是一项可部署的技能，它基于单个 Microsoft 365 邮箱和 Cloudflare DNS 区域，为企业级别提供别名/域名控制功能。

## 创新亮点

该技能通过协调以下方面，使一个邮箱和一个域名具备企业级电子邮件控制平台的特性：
- Entra/Graph 授权机制
- Exchange 数据传输与别名生命周期管理
- Cloudflare DNS/身份验证配置

这意味着用户可以无需管理大量邮箱，即可轻松创建、验证和优化邮件发送流程。

## 功能概述

- 通过一次交互式登录操作，即可配置 Microsoft Graph 和 Exchange 应用程序的权限。
- 审查 Graph、Exchange RBAC 以及 Cloudflare 令牌范围内的身份验证配置。
- 使用安全默认设置优化根域的邮件配置（如 SPF、MX、DMARC 规则）。
- 在子域名下创建支持回复或禁止回复的别名通道。
- 验证邮件通道的可用性（包括目标域名、别名关联情况、Graph 状态以及 DNS 配置）。
- 原子级存储操作结果，以便后续操作或管理员查看。

## 规则限制

- 禁止通过一次操作发送群组邮件。
- 禁止一次性向多个收件人发送邮件。
- 将禁止回复的别名视为故意不接收邮件的身份（即不设置 MX 配置且 SPF 设置为 “-all”）。
- 默认情况下，删除别名时系统会保留回复功能；除非明确要求彻底移除该别名。

## 快速入门

```bash
# 1) Copy strict credential templates
cp {baseDir}/credentials/entra.txt.template {baseDir}/credentials/entra.txt
cp {baseDir}/credentials/cloudflare.txt.template {baseDir}/credentials/cloudflare.txt

# 2) Edit values in both .txt files

# 3) Run Mail Caduceus (autoloads credentials/*.txt)
{baseDir}/scripts/mail-caduceus.sh \
  --organization-domain "northorizon.ca"
```

## 预测试

```bash
{baseDir}/scripts/mail-caduceus.sh \
  --tenant-id "<entra-tenant-id>" \
  --client-id "<entra-app-client-id>" \
  --organization-domain "northorizon.ca" \
  --mailbox "john@northorizon.ca" \
  --dry-run
```

## 邮件通道配置

```bash
# Reply-capable lane
python3 {baseDir}/scripts/email_alias_fabric_ops.py provision-lane \
  --mailbox "john@northorizon.ca" \
  --local "support" \
  --domain "support-reply.northorizon.ca" \
  --send-to "edge0100@icloud.com"

# No-reply lane
python3 {baseDir}/scripts/email_alias_fabric_ops.py provision-lane \
  --mailbox "john@northorizon.ca" \
  --local "support" \
  --domain "support-noreply.northorizon.ca" \
  --no-reply
```

## 创建带回复功能的别名通道（推荐）

```bash
# Keeps reply continuity by default (fallback mailbox defaults to --mailbox)
python3 {baseDir}/scripts/email_alias_fabric_ops.py retire-lane \
  --mailbox "john@northorizon.ca" \
  --alias-email "support@support-reply.northorizon.ca"

# Explicitly move fallback replies to another mailbox
python3 {baseDir}/scripts/email_alias_fabric_ops.py retire-lane \
  --mailbox "john@northorizon.ca" \
  --alias-email "support@support-reply.northorizon.ca" \
  --fallback-mailbox "inbox@northorizon.ca"
```

**彻底删除别名（无恢复机制）**

```bash
python3 {baseDir}/scripts/email_alias_fabric_ops.py control-json --ops-json \
  '{"action":"alias.remove","mailbox":"john@northorizon.ca","email":"support@support-reply.northorizon.ca","preserve_reply":false}'
```

**重要提示：**
- 若要恢复别名的接收功能，必须确保该别名域名仍然可路由（支持 inbound DNS 和 MX 配置）。
- 如果删除了整个域名，发送到该旧地址的邮件将无法被接收。

## 验证邮件通道配置

```bash
python3 {baseDir}/scripts/email_alias_fabric_ops.py verify-lane \
  --mailbox "john@northorizon.ca" \
  --alias-email "support@support-reply.northorizon.ca" \
  --domain "support-reply.northorizon.ca"
```

## 沙箱测试

```bash
bash {baseDir}/scripts/mail-caduceus-sandbox-smoke.sh
```

## 凭据与权限配置说明

- 凭据文件格式要求：
  - 文件名：`credentials/entra.txt`、`credentials/cloudflare.txt`
  - 首行必须为：`MAIL_CADUCEUS_CREDENTIALS_V1`
  - 其余行应为标准的 `KEY=VALUE` 对格式（不允许使用不支持的键）
  - 相关模板位于技能文件夹中的 `*.txt.template` 文件中
- `mail-caduceus-bootstrap.ps1.txt` 是一个安全的 PowerShell 脚本模板。
- 运行时，`mail-caduceus.sh` 会将该模板转换为临时 `.ps1` 文件并执行它。
- 可通过以下参数覆盖配置路径：
  - `MAIL_CADUCEUS_BOOTSTRAP_SCRIPT`
  - `MAIL_CADUCEUS_FABRIC_SCRIPT`
  - `MAIL_CADUCEUS_ENV_FILE`
  - `MAIL_CADUCEUS_INTEL_DIR`
  - `MAIL_CADUCEUS_CREDENTIALS_DIR`
  - `MAIL_CADUCEUS_ALLOW_EXTERNAL_SCRIPT_RESOLUTION`（默认禁用）

**删除行为设置：**
- `EMAIL_ALIAS_FABRIC_DELETE_PRESERVE_REPLY_DEFAULT=true|false`（默认为 `true`）：决定是否保留回复功能
- `EMAIL_ALIAS_FABRIC_FALLBACK_MAILBOX=<mailbox@domain>`（可选的默认回复目标邮箱）

**数据持久化设置：**
- `--persist-env`：允许将非敏感运行时配置写入 `ENV_FILE`。
- `--persist-secrets`：允许将敏感配置写入 `ENV_FILE`（仅限启用）
- 默认情况下，配置不会持久化（不会生成 `.env` 文件）。

## 登录方式（重要说明）

- 首次配置时需要交互式登录（获取权限或管理员同意/Exchange RBAC 授权）。
- 配置完成后，后续操作可完全无界面化执行（使用 `ENTRA_CLIENT_SECRET` 和 `--skip-m365-bootstrap` 参数）。
- 推荐的生产环境流程：首次进行管理员配置，之后通过无界面化脚本进行日常操作。

## 安全性设置（v1.0.0）

- 外部脚本的调用范围受到严格限制。
- 除非明确修改，否则凭证自动发现功能仅在该技能目录内生效。
- 在写入状态数据之前，系统会隐藏生成的客户端密钥。
- 相关日志和状态文件具有严格的权限设置（目录权限为 700，文件权限为 600）。

## 主要优势

- 一个邮箱可安全地管理多个邮件通道。
- 域名和别名的生命周期管理实现自动化。
- 全面的状态监控减少了操作人员的猜测工作量。
- 适用于支持、销售、外联等场景，支持设置明确的回复/禁止回复模式。
- 适用于个性化、高并发量的外联需求，支持自定义身份信息（显示名称、别名、子域名）。
- 通过限制单次发送目标及通道特定的配置，有效降低垃圾邮件风险。

## 效果

Mail Caduceus 以轻量级的架构实现了类似 Fortune 500 公司级别的电子邮件管理功能：
- 仅需一个域名和一个邮箱
- 通过一个简单的命令即可完成全部配置
- 提供全面的生命周期控制