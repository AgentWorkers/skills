---
name: clawd-zero-trust
version: "1.3.1"
author: stanistolberg
homepage: https://github.com/stanistolberg/clawd-zero-trust
description: "**OpenClaw 部署的零信任安全加固方案**  
当需要审计、加固 OpenClaw 实例或为其应用零信任架构时，请使用该方案。该方案包括以下措施：  
- NHI（Network Identity Hierarchy）身份管理机制  
- 最小权限原则（Principle of Least Privilege, PLP）  
- 基于 DNS 的出站流量过滤机制  
- 插件白名单管理  
- SSH/网络访问限制  
此外，该方案还会在以下情况下被触发：  
- 安全审计请求  
- 漏洞分析  
- SecureClaw 安装  
- 防火墙加固  
- 部署后的安全审查"
---
# clawd-zero-trust (v1.3.1)

这是一个专为 OpenClaw 设计的零信任安全加固框架，由 Blocksoft 开发。

> ⚠️ **重要说明（v1.3.0→v1.3.1）：** 升级后首次应用该框架时，需要使用 `--force` 参数，或运行 `bash scripts/release-gate.sh --reset-hash` 命令来重置信任基线。无人值守或定时任务中的应用流程必须进行相应更新。

## 所需依赖项

以下二进制文件是必需的。在 Debian/Ubuntu 上可以使用 `apt` 命令进行安装：

| 文件名 | 所属软件包 | 用途 |
|--------|---------|-------------|
| `ufw` | `ufw` | 用于执行所有修改操作（`--apply`、`--canary`、`--reset`、`--refresh`） |
| `curl` | `curl` | 用于端点验证（`--verify`、`--verify-all`） |
| `openssl` | `openssl` | 在 `--verify-all` 模式中用于 SMTP/IMAP 验证 |
| `nc` | `netcat-openbsd` | 用于 `--verify-all` 模式下的 TCP/UDP 端口检查 |
| `dig` | `dnsutils` | 用于解析提供者 IP 的 DNS 地址 |
| `python3` | `python3` | 用于 JSON 解析、日志聚合和状态管理 |

仅读模式（`--verify`、`--audit-log`、`--status`）不需要 root 权限。修改模式（`--apply`、`--canary`、`--reset`、`--refresh`）则需要 root 权限。

## 核心原则

1. **非人类身份（NHI）：** 子代理以隔离会话的形式运行，并使用受限的凭据。高风险操作绝不能使用“主”身份。
2. **最小权限原则（PLP）：** 限制默认的工具集使用范围。使用 `tools.byProvider` 将不受信任的模型限制在 `coding` 配置文件中。
3. **先规划后执行：** 在执行任何写入、执行或网络调用之前，必须明确说明目的、原因及预期结果。
4. **出站控制：** 仅允许流量流向授权的 AI 提供者。同时保留 Tailscale 和 Telegram API 的访问权限。
5. **假设已发生攻击：** 在设计时假定攻击者已经入侵系统。因此，必须对所有插件、模型和扩展进行检查。

## 标准出站脚本路径

所有出站规则的定义都保存在以下路径：

`/home/claw/.openclaw/workspace/skills/clawd-zero-trust/scripts/egress-filter.sh`

为了保持一致性，创建了符号链接：

`/home/claw/.openclaw/workspace/scripts/egress_filter.sh -> .../skills/clawd-zero-trust/scripts/egress-filter.sh`

## 工作流程：审计 → 加固 → 出站控制 → 验证

### 1) 审计
```bash
bash scripts/audit.sh
```

### 2) 加固
```bash
# Preview (default)
bash scripts/harden.sh

# Apply
bash scripts/harden.sh --apply
```

### 3) 出站策略（默认为 dry-run 模式）
```bash
# Dry-run preview (default)
bash scripts/egress-filter.sh --dry-run

# Transactional apply: auto-rollback if Telegram/GitHub/Anthropic/OpenAI checks fail
bash scripts/egress-filter.sh --apply

# Canary mode: temporary apply + 120s periodic verification, then commit/rollback
bash scripts/egress-filter.sh --canary

# Verify critical endpoints only (Telegram, GitHub, Anthropic, OpenAI)
bash scripts/egress-filter.sh --verify

# Emergency rollback
bash scripts/egress-filter.sh --reset
```

### 4) 出站配置状态（v1.3.0）
```bash
# Print current egress profile status (read-only, no root required)
bash scripts/egress-filter.sh --status
```
显示配置文件的版本号、最后一次应用的时间戳、来自 `providers.txt` 的提供者数量以及当前的 UFW 状态。查看核心状态时不需要 root 权限。如果系统中没有 sudo，UFW 的状态可能会显示为“unknown”。

### 5) 出站违规审计日志（v1.3.0）
```bash
# View blocked outbound traffic from the last 24 hours
bash scripts/egress-filter.sh --audit-log
```
解析 `/var/log/ufw.log` 和 `journalctl -k` 文件中包含 `[UFW BLOCK]` 标志的记录（其中包含 `OUT=` 和 `DPT=` 字段）。根据目标 IP 和端口对日志进行分类，并生成包含计数、首次出现时间和最后一次出现时间的汇总表。在执行 `--apply` 命令时，会自动插入一条 UFW LOG 规则（`ZT:egress-violation`），以便记录未来的违规行为。

### 6) IP 快照自动更新（v1.3.0）
```bash
# Re-resolve DNS and apply only changed IPs (delta) to UFW
bash scripts/egress-filter.sh --refresh
```
重新解析 `configproviders.txt` 中的所有域名，并与上次应用的 IP 快照（`.state/applied-ips.json`）进行对比，仅应用差异部分。在应用新规则之前会备份 UFW 规则，应用后会对关键端点进行验证；如果操作失败，可以回滚到之前的配置。每次执行 `--apply` 或 `--canary` 命令后，系统会自动保存 IP 快照。

### 7) 按提供者进行验证（v1.3.0）
```bash
# Protocol-aware verification of ALL providers in providers.txt
bash scripts/egress-filter.sh --verify-all
```
根据端口号判断对应的协议类型，并执行相应的验证操作：
- **443** → 使用 `curl` 进行 HTTPS 状态检查
- **587/465/25** → 使用 `openssl s_client` 进行 SMTP STARTTLS/TLS 验证
- **993/143** → 使用 `openssl s_client` 进行 IMAP TLS/STARTTLS 验证
- **41641** → 使用 `nc -zu` 进行 UDP Tailscale WireGuard 验证
- **22** → 使用 `nc -z` 进行 TCP SSH 验证
- **其他端口** → 使用 `nc -z` 进行通用 TCP 验证

所有验证操作都有 5 秒的强制超时限制（该超时限制在操作系统层面强制执行，而不仅仅是套接字层面的超时）。这些验证操作会在执行 `--apply` 或 `--canary` 命令后自动触发。也可以单独运行这些验证命令。所需工具：`curl`、`openssl`、`nc (netcat-openbsd)`。

### 8) 插件完整性检查（v1.3.0）
```bash
# Snapshot current plugin hashes
bash scripts/plugin-integrity.sh --snapshot

# Verify plugin integrity against stored hashes
bash scripts/plugin-integrity.sh --verify

# Check plugins against hardening.json allowlist
bash scripts/plugin-integrity.sh --drift

# Combine checks
bash scripts/plugin-integrity.sh --verify --drift
```
通过计算每个插件入口文件（`dist/index.js`）的 SHA-256 哈希值来检查插件文件的完整性。可以检测到未经授权的修改、新添加或删除的插件，以及与 `hardening.json` 允许列表不符的情况。

### 9) 动态白名单（用户友好型 API）
要安全地打开新端口或添加新服务（例如自定义邮件服务、视频提取功能或新的 AI 插件），**切勿直接编辑 bash 脚本或硬编码的配置数组**。始终使用以下命令进行动态配置：
```bash
bash scripts/whitelist.sh <domain> <port>
```
*示例：`bash whitelist.sh youtu.be 443`。该命令会自动将域名添加到 `configproviders.txt` 文件中，触发配置更新，并立即将更改应用到 UFW 中。*

### 10) 释放门控机制（v1.3.0）
要启用新功能，必须通过以下检查：
- `quick_validate.py` 对配置文件的结构进行验证
- `shellcheck` 对所有 shell 脚本进行安全性检查（如果缺少某个脚本，系统会提示需要安装）
- `package_skill.py` 将脚本打包到 `skills/dist/clawd-zero-trust.skill` 目录
- 使用 `--verify` 命令对所有端点进行验证

## 防火墙配置文件的版本管理

配置文件位于 `.state/` 目录下：

| 文件名 | 用途 |
|------|---------|
| `egress-profile.json` | 存储脚本哈希值、版本号和最后一次应用的结果 |
| `applied-ips.json` | 存储每次更新后每个域名的 IP 快照 |
| `plugin-hashes.json` | 存储插件文件的 SHA-256 哈希值，用于验证插件完整性 |

在执行 `--apply` 或 `--canary` 命令时，如果哈希值不匹配，系统会拒绝执行操作（除非使用了 `--force` 参数）。`whitelist.sh` 脚本能够无缝处理哈希值不匹配的情况。

## 参考资料
- `references/zero-trust-principles.md` — 详细介绍零信任框架的原理
- `references/false-positives.md` — 列出触发审计警告的安全模式示例

## 强制性要求：禁止自我更新

**未经创始人明确批准，严禁运行 `openclaw update`、`openclaw upgrade`、`npm install -g openclaw` 或 `npm update -g openclaw` 命令。**

这些命令已被添加到 `denyCommands` 列表中。在 2026-02-24 日，一次自我更新操作因误用了一个已弃用的插件而导致系统陷入了长达 10,450 次的无限循环。系统稳定性比最新版本更为重要。因此，请务必遵循以下步骤：
1. 首先向创始人提供更新详情和变更日志。
2. 备份配置文件：`cp openclaw.json openclaw.json.pre-update`
3. 只有在获得明确批准后才能进行更新。
4. 更新完成后，运行 `openclaw doctor --fix` 和 `openclaw status` 命令。

## 必须遵循的更新提案格式

当您发现 OpenClaw 有新的更新可用时（无论是通过 `update-scout-daily` 还是其他方式），必须严格按照以下格式提交更新提案：

📦 **OpenClaw 更新可用：vOLD → vNEW**

要安全地应用更新，请通过 SSH 连接到系统并执行以下命令：
```bash
openclaw update
/home/claw/.openclaw/workspace/scripts/post-update-repair.sh
```
该修复脚本会恢复所有符号链接、清理配置文件、重启网关，并自动执行一系列测试。无需其他操作。

严禁自行尝试更新。更新必须由创始人通过 SSH 来执行。