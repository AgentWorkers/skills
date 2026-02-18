---
name: guava-guard
description: OpenClaw代理的运行时安全防护机制。能够检测到危险的操作模式（即不安全的工具调用）。如需进行全面的静态扫描，请使用`guard-scanner`工具。
metadata:
  clawdbot:
    emoji: "🛡️"
---
# GuavaGuard 🛡️

**为你的 OpenClaw 代理提供运行时安全监控。**

GuavaGuard 实时监控工具调用，并在检测到危险行为时发出警告——例如反向 shell、凭证泄露、沙箱逃逸等。

## 快速入门

```bash
# 1. Install
clawhub install guava-guard

# 2. Enable the runtime hook
openclaw hooks install skills/guava-guard/hooks/guava-guard
openclaw hooks enable guava-guard

# 3. Restart gateway, then verify:
openclaw hooks list   # Should show 🍈 guava-guard as ✓ ready
```

就这样。GuavaGuard 现在已经开始监控你的代理工具调用了。

## 它能检测到哪些行为（12 种运行时模式）**

| 行为模式 | 严重程度 | 示例 |
|---------|----------|---------|
| 反向 shell | 🔴 严重 | `/dev/tcp/`, `nc -e`, `socat TCP` |
| 凭证泄露 | 🔴 严重 | 秘密信息被发送到 webhook.site、ngrok、requestbin |
| 禁用安全防护机制 | 🔴 严重 | `exec.approval = off`（CVE-2026-25253） |
| macOS Gatekeeper 绕过 | 🔴 严重 | `xattr -d quarantine` |
| ClawHavoc AMOS 攻击 | 🔴 严重 | `socifiapp`、Atomic Stealer 攻击迹象 |
| 将 Base64 编码的数据解码为 shell 命令 | 🔴 严重 | `base64 -d \| bash` |
| 下载文件后执行 shell 命令 | 🔴 严重 | `curl \| bash`, `wget \| sh` |
| 利用云服务进行 SSRF 攻击 | 🔴 严重 | `169.254.169.254` |
| 已知的恶意 IP 地址 | 🔴 严重 | `91.92.242.30` |
| DNS 信息泄露 | 🟠 高风险 | `nslookup $secret`, `dig @attacker` |
| SSH 密钥访问 | 🟠 高风险 | `.ssh/id_*`, `.ssh/authorized_keys` |
| 加密钱包信息泄露 | 🟠 高风险 | `wallet seed`, `mnemonic`, `seed phrase` |

## 当前限制

> **警告**：OpenClaw 的钩子 API 尚不支持阻止工具的执行。
> GuavaGuard 目前仅能发出警告，无法阻止危险操作。
> 当取消操作的 API 被添加后，将自动启用阻止功能。
> 详情请参见：[问题 #18677](https://github.com/openclaw/openclaw/issues/18677)

## 审计日志

所有检测结果都会被记录到 `~/.openclaw/guava-guard/audit.jsonl` 文件中（JSON 格式）。

## 需要全面的静态扫描吗？（推荐使用）

GuavaGuard 主要负责运行时监控。如需在安装前对技能包进行全面的静态扫描，请先使用 **guard-scanner**：

```bash
# 1) Pre-install safety gate
npx guard-scanner ./skills --self-exclude --verbose

# 2) Then enable runtime monitoring
openclaw hooks enable guava-guard
```

- 支持 186 种以上检测模式，涵盖 20 类威胁
- 提供 HTML 仪表盘、SARIF 和 JSON 格式的输出结果
- 无依赖项
- 使用 MIT 许可协议

**GitHub**：https://github.com/koatora20/guard-scanner
**ClawHub**：`clawhub install guard-scanner`

## 诞生背景

一次真实的代理被入侵事件促使我们开发了 GuavaGuard。该工具通过检测危险的运行时工具调用行为，帮助用户及时发现异常并留下可审计的痕迹。

## 许可协议

MIT 许可协议。无依赖项。🍈