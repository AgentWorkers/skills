---
name: mailcaduceus
description: "☤MailCaduceus 允许您使用一个域名/邮箱组合来自动化 OpenClaw 的企业级通信系统。其内置的收件箱可靠性优化引擎能够自动强化发送者的身份验证机制、实现用户身份的定期轮换，并提供可扩展的外展/支持流程，确保您的邮件不会被误判为垃圾邮件。"
homepage: https://github.com/lmtlssss/MailCaduceus
metadata: {"openclaw":{"emoji":"📬","requires":{"bins":["bash","pwsh","python3","jq","rg"],"env":["ENTRA_CLIENT_ID","ENTRA_TENANT_ID","ENTRA_CLIENT_SECRET","EXCHANGE_DEFAULT_MAILBOX","EXCHANGE_ORGANIZATION","CLOUDFLARE_API_TOKEN","CLOUDFLARE_ZONE_ID"]}}}
---
# ☤MailCaduceus

☤MailCaduceus 是一项可用于企业级别别名/域名管理的功能，它基于单个 Microsoft 365 邮箱和 Cloudflare DNS 区域来实现这些功能。

## 创新概述

该功能通过协调以下方面，使一个邮箱和一个域名具备企业级电子邮件管理的能力：
- Entra/Graph 授权
- Exchange 数据传输与别名生命周期管理
- Cloudflare DNS/身份验证设置

这意味着用户可以轻松创建、验证和优化邮件通道，而无需管理大量的邮箱。

## 功能介绍

- 通过一次交互式登录，即可配置 Microsoft Graph 和 Exchange 应用的权限。
- 审查 Graph、Exchange RBAC 以及 Cloudflare 令牌范围内的凭证配置。
- 使用安全默认设置优化根域的邮件配置（如 SPF、MX、DMARC）。
- 在子域名下创建可回复或不可回复的别名通道。
- 验证邮件通道的可用性（如是否为可接受域名、别名是否已关联、Graph 状态、DNS 配置是否正确）。
- 原子性地存储操作结果，以便后续操作或操作员查看。

## 重要规则

- 禁止通过一次操作发送群组邮件。
- 禁止一次性向多个收件人发送邮件。
- 将不可回复的别名视为故意设置的“不接收邮件”的身份（即不设置 MX 和 SPF 的“all”配置）。
- 默认情况下，删除别名时不会影响其他功能：除非明确删除，否则别名会保留并继续正常使用。

## 快速入门

```bash
# 1) Copy strict credential templates
cp {baseDir}/credentials/entra.txt.template {baseDir}/credentials/entra.txt
cp {baseDir}/credentials/cloudflare.txt.template {baseDir}/credentials/cloudflare.txt

# 2) Edit values in both .txt files

# 3) Run ☤MailCaduceus (autoloads credentials/*.txt)
{baseDir}/scripts/mail-caduceus.sh \
  --organization-domain "northorizon.ca"
```

## 先进行测试运行

```bash
{baseDir}/scripts/mail-caduceus.sh \
  --tenant-id "<entra-tenant-id>" \
  --client-id "<entra-app-client-id>" \
  --organization-domain "northorizon.ca" \
  --mailbox "john@northorizon.ca" \
  --dry-run
```

## 配置邮件通道

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

## 删除带有回复功能的邮件通道（推荐）

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

**彻底删除（无恢复机制）**

```bash
python3 {baseDir}/scripts/email_alias_fabric_ops.py control-json --ops-json \
  '{"action":"alias.remove","mailbox":"john@northorizon.ca","email":"support@support-reply.northorizon.ca","preserve_reply":false}'
```

**重要提示：**
- 恢复机制要求别名域名仍然可路由（即必须支持入站 DNS 和 MX 设置）。
- 如果删除了域名本身，发送到该旧地址的邮件将无法被接收。

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

## 凭证和权限说明

- 凭证文件格式要求：
  - 文件名：`credentials/entra.txt`、`credentials/cloudflare.txt`
  - 第一行必须包含：`MAIL_CADUCEUS_CREDENTIALS_V1`
  - 其余行应为严格的 `KEY=VALUE` 对（不允许使用不支持的键）
  - 相关模板位于 `skills` 文件夹中的 `*.txt.template` 文件中
- `mail-caduceus-bootstrap.ps1.txt` 是一个安全的 PowerShell 源代码模板。
- 运行时，`mail-caduceus.sh` 会将该模板生成一个临时的 `.ps1` 文件并执行它。
- 可通过以下配置文件覆盖默认路径：
  - `MAIL_CADUCEUS_BOOTSTRAP_SCRIPT`
  - `MAIL_CADUCEUS_FABRIC_SCRIPT`
  - `MAIL_CADUCEUS_ENV_FILE`
  - `MAIL_CADUCEUS_INTEL_DIR`
  - `MAIL_CADUCEUS_CREDENTIALS_DIR`
  - `MAIL_CADUCEUS_ALLOW_EXTERNAL_SCRIPT_RESOLUTION`（默认：禁用）

**删除行为设置：**
- `EMAIL_ALIAS_FABRIC_DELETE_PRESERVE_REPLY_DEFAULT=true|false`（默认：`true`）
- `EMAIL_ALIAS_FABRIC_FALLBACK_MAILBOX=<mailbox@domain>`（可选的默认回复目标邮箱）

**持久化设置：**
- `--persist-env`：允许将非敏感的运行时配置写入 `ENV_FILE`。
- `--persist-secrets`：允许将敏感配置写入 `ENV_FILE`（仅限启用）。
- 默认模式下，不会生成 `.env` 文件。

## 登录方式（重要）

- 首次配置时需要交互式登录（获取权限或管理员同意/Exchange RBAC）。
- 配置完成后，后续操作可以完全无界面化进行（使用 `ENTRA_CLIENT_SECRET` 和 `--skip-m365-bootstrap`）。
- 推荐的生产流程是：首次进行管理员配置，之后通过无界面化脚本进行日常操作。

## 安全性设置（v1.0.0）

- 外部脚本的执行范围是受限的（默认情况下仅限于当前功能目录）。
- 除非明确更改，否则凭证的自动发现功能也仅限于当前功能目录。
- 在将配置写入 JSON 文件之前，会隐藏生成的客户端密钥。
- 智能状态输出文件的权限设置较为严格（目录权限为 700，文件权限为 600）。

## 主要优势

- 一个邮箱可以安全地管理多个独立的邮件通道。
- 域名和别名的生命周期管理可以自动化。
- 全面的状态监控减少了操作员的猜测工作量。
- 适用于支持、销售、外联和交易性邮件发送，支持设置不同的回复/不可回复模式。
- 适用于个性化、高量的邮件发送，支持自定义身份信息（显示名称、别名、子域名）。
- 通过限制每次操作只能发送给一个收件人以及针对特定通道设置邮件规则，降低了垃圾邮件的风险。

## 最终效果

☤MailCaduceus 通过简单的架构提供了类似 Fortune 500 公司级别的电子邮件管理功能：
- 仅需一个域名和一个邮箱
- 通过一个配置命令即可完成所有配置
- 实现全面的生命周期管理