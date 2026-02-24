---
name: clawhub-scanner
description: "扫描已安装的 ClawHub 技能，以检测恶意软件、凭证窃取、命令注入以及安全风险。能够识别出与 ClawHavoc 活动相关的已知 C2（命令与控制）基础设施、经过混淆的载荷以及数据泄露模式。"
---
# clawhub-scanner

这是一个用于扫描 ClawHub 技能（skills）的安全工具。它会将已安装的技能与已知的恶意模式、入侵指标（IoCs）以及可疑行为进行比对。

## 使用方法

当用户请求扫描技能、检测恶意软件或审计其 ClawHub 安装情况时，可以使用该工具：

```bash
# Scan all installed skills
clawhub-scanner scan

# Scan a specific skill
clawhub-scanner scan --skill ~/.openclaw/skills/some-skill

# JSON output for automation
clawhub-scanner scan --json

# Include low-severity findings
clawhub-scanner scan --verbose
```

## 检测内容：

- **严重级别（Critical）：** 已知的 C2 服务器 IP 地址和恶意域名（属于 ClawHavoc 策略）
- **高风险级别（High）：** 评估（eval()）操作、凭证收集（SSH/AWS/浏览器/钱包信息）、数据泄露（通过 Discord/Telegram 的 Webhook 实现）、混淆后的恶意代码
- **中等风险级别（Medium）：** 强制注入攻击、广泛的文件系统访问权限、剪贴板内容被窃取
- **低风险级别（Low）：** 出站 HTTP 请求、WebSocket 连接

## 安装方法

需要安装以下 npm 包：

```bash
npm install -g @elvatis_com/clawhub-scanner
```

## 返回代码（Exit Codes）：

- 0：扫描完成，无问题
- 1：发现高风险问题
- 2：发现严重问题