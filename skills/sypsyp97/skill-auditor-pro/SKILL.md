---
name: skill-auditor
version: 2.1.1
description: ClawHub 技能的安全扫描器：在安装之前能够检测恶意代码、混淆后的有效载荷以及社会工程攻击。采用三层分析机制：模式匹配、反混淆以及大语言模型（LLM）的意图分析。
author: sypsyp97
---

# 技能审计器 🔍

在安装任何技能之前，对其进行安全威胁审计，以确保其安全性。

## 触发条件

在以下情况下使用此技能：
- “审计此技能”
- “检查技能的安全性”
- 在安装任何第三方技能之前

## 使用方法

### 方法 1：安装前审计（推荐）

```bash
# Inspect without installing
clawhub inspect <skill-name>

# Run the audit script
~/.openclaw/workspace/skills/skill-auditor/scripts/audit.sh <skill-name>
```

### 方法 2：审计已安装的技能

```bash
~/.openclaw/workspace/skills/skill-auditor/scripts/audit.sh --local <skill-path>
```

## 检测层

### 第一层：模式匹配

| 严重程度 | 模式 | 风险 |
|----------|---------|------|
| 🔴 高 | `base64.*\|.*bash` | 编码后的命令执行 |
| 🔴 高 | `curl.*\|.*bash` | 远程脚本执行 |
| 🔴 高 | `eval\()` / `exec\()` | 动态代码执行 |
| 🔴 高 | 已知的 C2 服务器 IP 地址 | 恶意通信 |
| 🟡 中等 | 访问 `~/.openclaw/` 目录 | 配置信息泄露 |
| 🟡 中等 | 读取 `$API_KEY` 等敏感信息 | 凭据泄露 |
| 🟡 中等 | 社交工程相关关键词 | 用户被骗 |
| 🟢 低 | 需要 `sudo` 权限 | 权限提升 |

### 第二层：反混淆

自动解码隐藏的恶意载荷：
- **Base64** — 解码并扫描隐藏的命令 |
- **Hex** — 解码 `\x41\x42` 格式的字符串 |
- 检查解码后的内容中是否存在 C2 服务器或危险命令

### 第三层：大语言模型（LLM）分析（可选）

使用 Gemini CLI 分析可疑代码的意图：
- 超出模式匹配的深度语义理解 |
- 检测新型或未知的威胁 |
- 需要安装 `gemini` CLI

## 已知的入侵指标（IoC）

### C2 服务器 IP 地址
```
91.92.242.30  # ClawHavoc primary server
```

### 恶意域名
```
glot.io       # Hosts obfuscated scripts
webhook.site  # Data exfiltration endpoint
```

### 社交工程相关关键词
```
OpenClawDriver    # Non-existent "driver"
ClawdBot Driver   # Social engineering lure
Required Driver   # Tricks users into installing malware
```

## 输出格式

```
═══════════════════════════════════════════
  SKILL AUDIT REPORT: <skill-name>
═══════════════════════════════════════════

🔴 HIGH RISK FINDINGS:
   [LINE 23] base64 encoded execution detected
   [LINE 45] curl|bash pattern found

🟡 MEDIUM RISK FINDINGS:
   [LINE 12] Accesses ~/.openclaw/ directory

🟢 LOW RISK FINDINGS:
   [LINE 5] Requires sudo for installation

═══════════════════════════════════════════
  VERDICT: ❌ DO NOT INSTALL
═══════════════════════════════════════════
```

## 最佳实践

1. **安装前务必进行审计** — 永远不要跳过安全检查 |
2. **不要盲目信任任何技能** — 即使是评分很高或受欢迎的技能 |
3. **定期检查更新** — 技能更新可能会引入恶意代码 |
4. **报告可疑技能** — 将可疑技能发送至 steipete@gmail.com

## 维护

**在新发现威胁时更新此技能：**

1. 新的恶意 IP 地址 → 添加到 `MALICIOUS_IPS` 列表 |
2. 新的恶意域名 → 添加到 `MALICIOUS_DOMAINS` 列表 |
3. 新的社交工程诱骗手段 → 添加到 `SOCIAL_engineERING` 列表 |
4. 新的攻击模式 → 添加相应的正则表达式进行检测 |

更新位置：`scripts/audit.sh` 文件顶部的变量定义

## 参考资料

- [341 个恶意 ClawHub 技能事件](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)
- [OpenClaw 安全指南](https://docs.openclaw.ai/gateway/security)