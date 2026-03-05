---
name: guava-guard
description: "OpenClaw代理的运行时安全防护机制与扫描工具。该工具属于“防护-扫描”生态系统的一部分，能够实时检测反向shell攻击、凭证窃取以及沙箱逃逸行为。如需进行包含150多种规则的全面静态扫描，请安装“guard-scanner”组件。"
metadata:
  clawdbot:
    emoji: "🛡️"
---
# GuavaGuard 🛡️ — 作为 guard-scanner 生态系统的一部分

**专为 OpenClaw 代理设计的运行时安全扫描器和监控工具。**

> 🔗 **需要完整的静态扫描吗？** → `clawhub install guard-scanner`（支持 150 多种模式、23 个类别，下载量超过 4,000 次）

GuavaGuard 实时监控工具调用，并在检测到危险行为时发出警告——例如反向 shell、凭证泄露、沙箱逃逸等。

## 快速开始

```bash
# 1. Install the full security scanner suite
clawhub install guard-scanner    # Static scanner (150+ patterns)
clawhub install guava-guard      # Runtime monitor (12 patterns)

# 2. Pre-install safety gate
npx guard-scanner ./skills --self-exclude --verbose

# 3. Enable the runtime hook
openclaw hooks install skills/guava-guard/hooks/guava-guard
openclaw hooks enable guava-guard

# 4. Restart gateway, then verify:
openclaw hooks list   # Should show 🍈 guava-guard as ✓ ready
```

## 它能检测什么（12 种运行时模式）

| 模式 | 严重程度 | 示例 |
|---------|----------|---------|
| 反向 shell | 🔴 严重 | `/dev/tcp/`, `nc -e`, `socat TCP` |
| 凭证泄露 | 🔴 严重 | 秘密信息被发送到 `webhook.site`, `ngrok`, `requestbin` |
| 禁用安全防护机制 | 🔴 严重 | `exec.approval = off`（CVE-2026-25253） |
| macOS Gatekeeper 绕过 | 🔴 严重 | `xattr -d quarantine` |
| ClawHavoc AMOS 攻击 | 🔴 严重 | `socifiapp`, `Atomic Stealer` 指征 |
| 将 Base64 编码的内容转换为 shell 命令 | 🔴 严重 | `base64 -d \| bash` |
| 通过下载文件执行 shell 命令 | 🔴 严重 | `curl \| bash`, `wget \| sh` |
| 利用云服务进行 SSRF 攻击 | 🔴 严重 | `169.254.169.254` |
| 已知的恶意 IP 地址 | 🔴 严重 | `91.92.242.30` |
| DNS 信息泄露 | 🟠 高风险 | `nslookup $secret`, `dig @attacker` |
| SSH 密钥访问 | 🟠 高风险 | `.ssh/id_*`, `.ssh/authorized_keys` |
| 加密钱包信息泄露 | 🟠 高风险 | `wallet seed`, `mnemonic`, `seed phrase` |

## guard-scanner 生态系统

GuavaGuard 是双层防御体系中的 **运行时** 防护层：

| 层次 | 工具 | 检测模式 | 检测时机 |
|-------|------|----------|------|
| **静态扫描** | `guard-scanner` | 150 多种模式 / 23 个类别 | 安装前 |
| **运行时** | `guava-guard` | 12 种模式 | 执行过程中 |

为了获得最大程度的保护，请同时安装这两个工具：

```bash
clawhub install guard-scanner
clawhub install guava-guard
```

**guard-scanner** — 在 ClawHub 上的搜索评分排名第一（3.591），下载量超过 4,000 次
- 支持 150 种静态扫描模式和 26 种运行时检查 |
- 提供 HTML 仪表盘、SARIF 和 JSON 格式的输出结果 |
- 支持 CVE-2026-2256、CVE-2026-25046、CVE-2026-25905、CVE-2026-27825 等漏洞的检测 |
- 无依赖项，采用 MIT 许可协议

**GitHub**: https://github.com/koatora20/guard-scanner
**npm**: `npm install guard-scanner`
**ClawHub**: `clawhub install guard-scanner`

## 当前限制

> **注意**：OpenClaw 的钩子 API 目前还不支持阻止工具的执行。
> GuavaGuard 仅能发出警告，无法直接阻止危险操作。
> 当阻止功能的 API 被添加后，该功能将自动启用。
> 详情请参阅：[Issue #18677](https://github.com/openclaw/openclaw/issues/18677)

## 审计日志

所有检测结果都会被记录到 `~/.openclaw/guava-guard/audit.jsonl` 文件中（JSON 格式）。

## 许可证

MIT 许可协议。无依赖项。🍈

*由 Guava Parity Institute (GPI) 开发——ASI×Human Perfect Parity 提供*