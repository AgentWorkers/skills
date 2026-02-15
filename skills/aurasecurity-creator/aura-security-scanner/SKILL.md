---
name: AURA Security Scanner
description: 在安装AI代理之前，扫描其功能以检测是否存在恶意软件、密码盗窃、提示注入（prompt injection）以及危险权限（dangerous permissions）等安全风险。
version: 1.0.0
requires:
  bins: []
  env: [AURA_API_URL]
  config: []
permissions:
  filesystem: []
  network: [api.aurasecurity.io]
  exec: []
tags: [security, malware-detection, skill-scanner, trust]
---

# AURA 安全扫描器

保护您的人工智能代理免受恶意技能的侵害。在安装任何 OpenClaw、Claude MCP 或 LangChain 技能之前，请先对其进行扫描。

## 扫描内容

- **恶意软件模式**：凭证窃取、文件泄露、加密矿工程序、后门
- **提示注入**：试图篡改系统指令或越狱代理
- **权限问题**：文件系统、网络或执行权限设置过于宽松
- **可疑网络**：连接到已知的泄露源（如 webhook.site 等）
- **混淆代码**：使用 Base64 或十六进制编码的代码、动态执行脚本等

## 使用方法

在安装技能之前，请让我先对其进行扫描：

```
"Scan this skill for security issues: https://github.com/user/cool-skill"
```

```
"Is this skill safe? https://github.com/example/mcp-tool"
```

```
"Check https://clawhub.xyz/skill/weather-api for malware"
```

## 扫描结果

| 扫描结果 | 风险等级 | 含义 |
|---------|-----------|---------|
| 安全（SAFE） | 0-20 | 未发现任何问题，可安全安装 |
| 警告（WARNING） | 21-50 | 存在轻微风险，请在安装前仔细检查 |
| 危险（DANGEROUS） | 51-80 | 检测到重大风险，请避免安装 |
| 被阻止（BLOCKED） | 81-100 | 存在严重威胁，切勿安装 |

## AURA 验证徽章

获得“安全（SAFE）”扫描结果的技能可以显示 AURA 验证徽章，证明该技能已通过安全检测。

## 示例

### 安全的技能响应
```
AURA Skill Scan: weather-api

Verdict: SAFE
Risk Score: 5/100
AURA Verified: Yes

Summary: Clean skill with minimal permissions.
Requests only weather API access.

Recommendation: Safe to install.
```

### 危险的技能响应
```
AURA Skill Scan: suspicious-helper

Verdict: DANGEROUS
Risk Score: 78/100
AURA Verified: No

Findings:
- CRITICAL: Accesses SSH keys (~/.ssh/id_rsa)
- HIGH: Sends data to webhook.site
- HIGH: Runs eval() on decoded base64

Recommendation: Do not install. Contains credential
theft and data exfiltration patterns.
```

## API

该技能会调用 AURA 安全 API 进行扫描：

```
POST https://api.aurasecurity.io/scan-skill
{
  "skillUrl": "https://github.com/user/skill",
  "format": "auto",
  "includeRepoTrust": true
}
```

## 关于 AURA

AURA（Agent Universal Reputation & Assurance，代理通用信誉与保障系统）为人工智能代理生态系统提供安全保障。我们会对技能进行验证，跟踪代理的信誉状况，并保护用户免受恶意代码的侵害。

- 官网：https://aurasecurity.io
- GitHub 仓库：https://github.com/aurasecurityio/aura-security
- X/Twitter 账号：@aurasecurityio