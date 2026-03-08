---
name: caduceusmail
description: "☤CaduceusMail 允许您使用一个域名和邮箱组合，让 OpenClaw 自动化管理企业级的通信系统。"
homepage: https://github.com/lmtlssss/caduceusmail
metadata: {"openclaw":{"emoji":"☤","skillKey":"caduceusmail","requires":{"bins":["bash","node","python3","jq"],"env":["ENTRA_TENANT_ID","ENTRA_CLIENT_ID","ENTRA_CLIENT_SECRET","EXCHANGE_DEFAULT_MAILBOX","EXCHANGE_ORGANIZATION","ORGANIZATION_DOMAIN","CLOUDFLARE_API_TOKEN","CLOUDFLARE_ZONE_ID"]}}}
---
# ☤CaduceusMail 3.6.7

**收件箱可靠性优化引擎**：自动化发送者信任加固、身份轮换以及可扩展的外联/支持流程，确保您的邮件不会被归入垃圾邮件。

☤CaduceusMail 是一款适用于企业级别别名/域名管理的工具，基于单个 Microsoft 365 邮箱和 Cloudflare DNS 区域构建。它通过 OpenClaw 适配器与 `caduceusmail` 服务进行集成，实现对邮件和 DNS 的统一管理，无需在运行时通过 npm 下载任何代码。

## 功能概述

该工具主要作为 `caduceusmail` 包的轻量级封装层使用。首次使用时，它会：
1. 根据 `vendor/caduceusmail-release.json` 文件中指定的 SHA-512 哈希值验证提供的 tarball 文件的完整性；
2. 将经过审计的版本文件解压到 `~/.local/share/caduceusmail-skill/toolchains` 目录中；
3. 以受限的环境和仅限所有者的权限运行相关命令行工具（CLI）。

该工具在运行时不会从 npm 下载代码、安装全局包或执行 npm 生命周期脚本。

## 使用前的准备

在使用该工具之前，请先运行相应的检查脚本（`doctor`）以确保系统配置安全。

```bash
bash {baseDir}/scripts/run.sh doctor --json
```

## 快速入门

```bash
bash {baseDir}/scripts/run.sh bootstrap \
  --organization-domain "example.com" \
  --mailbox "ops@example.com" \
  --bootstrap-auth-mode device
```

## 启动后的每日无头运行（headless operation）

```bash
bash {baseDir}/scripts/run.sh bootstrap \
  --organization-domain "example.com" \
  --mailbox "ops@example.com" \
  --skip-m365-bootstrap
```

## 主要操作流程

```bash
bash {baseDir}/scripts/run.sh provision-lane \
  --mailbox "ops@example.com" \
  --local "support" \
  --domain "support-reply.example.com"

bash {baseDir}/scripts/run.sh verify-lane \
  --mailbox "ops@example.com" \
  --alias-email "support@support-reply.example.com" \
  --domain "support-reply.example.com"

bash {baseDir}/scripts/run.sh retire-lane \
  --mailbox "ops@example.com" \
  --alias-email "support@support-reply.example.com"
```

## 重要规则：
- **严禁** 通过单一操作发送群组邮件；
- **严禁** 同时向多个收件人发送单条邮件；
- 将未回复的邮箱视为“故意不接收邮件的账户”（即这些账户的 MX 设置为空或 SPF 配置为 `-all`）；
- 默认情况下，已退役的别名仍会保留回复功能，除非明确进行删除操作。

## 该工具的功能包括：
- **初始化 Microsoft Graph 和 Exchange 的身份验证机制**；
- 通过 OpenClaw 代理处理 VPS/SSH 设置中的设备登录流程；
- 审计凭证和 DNS 配置；
- 优化根邮件记录；
- 为子域名配置回复/未回复邮件通道；
- 验证各邮件通道的运行状态；
- 以保留回复功能的方式退役旧邮件通道；
- 生成可读的状态报告和机器可解析的数据文件。

## OpenClaw 运行时配置建议：

建议通过 `skills.entries.caduceusmail.env` 文件配置相关参数，而非直接修改源代码文件。具体配置参考 `examples/openclaw.config.json5`。该工具仅传递必要的 CaduceusMail/OpenClaw/M365/Cloudflare 相关配置信息，无关的机密信息默认不会被传递。除非明确设置 `CADUCEUSMAIL_ALLOW_EXTERNAL_SCRIPT_RESOLUTION=1`，否则外部脚本的执行将被禁用。

## 安全性与权限控制：

该工具的设计初衷就是执行高权限操作：
- 需要 Microsoft Graph 应用程序角色授权；
- 需要 Exchange 服务主体及基于角色的访问控制（RBAC）权限；
- 可根据需要调整 Exchange 的域名解析设置；
- 需要对 Cloudflare DNS 记录进行修改。

运行时产生的状态数据会保存在 `~/.caduceusmail/intel` 目录中，且仅限所有者访问。环境变量和机密信息的持久化功能是可选的，所有持久化的环境文件仅对所有者可见。建议使用最小权限的凭证：使用专门为 Graph/Exchange 角色设计的 Entra 服务主体，并使用仅限于目标域名 DNS 权限的 Cloudflare 令牌。