---
name: caduceusmail
description: "☤CaduceusMail 允许您使用一个域名和邮箱组合，让 OpenClaw 自动化管理企业级的通信系统。"
homepage: https://github.com/lmtlssss/caduceusmail
metadata: {"openclaw":{"emoji":"☤","skillKey":"caduceusmail","requires":{"bins":["bash","pwsh","python3","jq","rg"],"env":["ENTRA_TENANT_ID","ENTRA_CLIENT_ID","ENTRA_CLIENT_SECRET","EXCHANGE_DEFAULT_MAILBOX","EXCHANGE_ORGANIZATION","ORGANIZATION_DOMAIN","CLOUDFLARE_API_TOKEN","CLOUDFLARE_ZONE_ID"]}}}
---
# ☤CaduceusMail 5.1.1

**收件箱可靠性优化引擎**：该引擎自动化执行发送者信任加固、身份轮换以及可扩展的外联/支持流程，确保您的邮件不会被归类为垃圾邮件。

☤CaduceusMail 是一款适用于企业级别别名/域名管理的工具，基于单个 Microsoft 365 邮箱和 Cloudflare DNS 区域进行部署。

## 创新亮点

该工具通过协调以下功能，使一个邮箱和一个域名具备企业级电子邮件管理的能力：
- Graph 和 Exchange 的授权机制
- Exchange 的邮件传输流程及别名的生命周期管理
- Cloudflare 的 DNS 和身份验证设置

这意味着您可以轻松创建、验证并优化邮件发送流程，而无需管理大量的邮箱账户。

## 功能概述：
- 自动配置 Graph 和 Exchange 的身份验证机制
- 审计凭证和 DNS 设置
- 优化根邮件记录
- 为子域名配置回复或禁回复的邮件发送通道
- 验证邮件发送通道的可用性
- 优雅地关闭不再使用的邮件发送通道，并确保回复邮件的连续性
- 生成可读的状态报告和数据文件

## 重要规则：
- **严禁操作规范**：
  - 绝不允许通过一次操作发送群邮件
  - 绝不允许将同一条消息同时发送给多个接收者
  - 将禁回复的邮件通道视为“故意不接收邮件的身份”（即不配置 MX 记录且 SPF 设置为 `-all`）
  - 默认情况下，关闭的别名会保留回复功能，除非明确要求彻底删除

## 入门步骤：
在执行任何复杂操作之前，请先进行必要的“检查”（相当于“运行医生”程序，确保系统处于良好状态）。

```bash
python3 {baseDir}/scripts/caduceusmail-doctor.py --json
```

## 快速启动指南：
```bash
cp {baseDir}/credentials/entra.txt.template {baseDir}/credentials/entra.txt
cp {baseDir}/credentials/cloudflare.txt.template {baseDir}/credentials/cloudflare.txt

bash {baseDir}/scripts/caduceusmail.sh \
  --organization-domain "example.com" \
  --mailbox "ops@example.com" \
  --bootstrap-auth-mode device
```

## 启动后的日常自动化运行：
```bash
bash {baseDir}/scripts/caduceusmail.sh \
  --organization-domain "example.com" \
  --mailbox "ops@example.com" \
  --skip-m365-bootstrap
```

## 邮件发送通道管理：
```bash
python3 {baseDir}/scripts/email_alias_fabric_ops.py provision-lane \
  --mailbox "ops@example.com" \
  --local "support" \
  --domain "support-reply.example.com"

python3 {baseDir}/scripts/email_alias_fabric_ops.py verify-lane \
  --mailbox "ops@example.com" \
  --alias-email "support@support-reply.example.com" \
  --domain "support-reply.example.com"

python3 {baseDir}/scripts/email_alias_fabric_ops.py retire-lane \
  --mailbox "ops@example.com" \
  --alias-email "support@support-reply.example.com"
```

## 测试发送机制：
该工具提供了名为 `entra-exchange.sh` 的测试脚本，用于模拟邮件发送流程。该脚本仅通过 Graph 应用程序进行转发，并在 `from` 字段中使用相应的别名作为发件人信息。

## 沙箱与持续集成（CI）测试流程：
```bash
bash {baseDir}/scripts/caduceusmail-sandbox-smoke.sh
```

测试流程使用了 `--simulate-bootstrap` 参数，因此无需在测试主机上安装 PowerShell。

## OpenClaw 运行时配置：
建议通过 `skills.entries.caduceusmail.env` 文件来配置敏感信息，而非直接修改沙箱中的文件。具体配置参考 `examples/openclaw.config.json5` 和 `docs/openclaw.md`。

**数据持久化设置**：
数据持久化功能是可选的，可通过 `--persist-env` 和 `--persist-secrets` 参数来启用。

## 安全性与权限管理：
该工具的设计允许执行高权限操作：
- 需要 Microsoft Graph 应用程序的角色授权
- 需要 Exchange 服务 principal 和 RBAC 角色的分配
- 可根据需要调整 Exchange 的域名设置
- 需要修改 Cloudflare DNS 中的邮件发送通道记录

运行时的状态数据会保存在 `~/.caduceusmail/intel` 目录下。环境变量和敏感信息的持久化功能默认是关闭的，只有在通过 `--persist-env` 或 `--persist-secrets` 参数启用时才会生效。

**PowerShell 启动流程**：
如果系统中缺少某些 Microsoft 模块，PowerShell 脚本会自动从 PSGallery 安装这些模块（使用 `Install-Module` 命令）。

**外部脚本执行**：
默认情况下，系统禁止执行外部脚本。只有当 `CADUCEUSMAIL_ALLOW_EXTERNAL_SCRIPT_RESOLUTION=1` 被设置为 `1` 时，才会允许执行外部脚本。