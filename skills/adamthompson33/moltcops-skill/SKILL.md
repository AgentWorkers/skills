---
name: moltcops
version: 1.0.0
description: **预安装AI代理技能的安全扫描器**：在您信任任何代码之前，该扫描器会检测其中的恶意模式。采用“本地优先”策略——代码永远不会离开您的设备。
---

# MoltCops — 技能安全扫描器

在安装任何技能之前，先对其进行安全威胁扫描。该扫描器能够检测出提示注入（prompt injection）、数据泄露（data exfiltration）、潜伏式触发器（sleeper triggers）、资金盗用模式（drain patterns）以及其他16种安全威胁。

**本地优先**：您的代码永远不会离开您的设备。无需进行API调用，也不会上传到任何服务器或创建新账户。

## 使用场景

- **在从ClawHub、GitHub或其他来源安装任何技能之前**  
- **在运行其他代理共享的技能之前**  
- **在评估来自任何来源的未知代码时**  
- **在ClawHavoc事件之后**：本周在ClawHub上发现了341个恶意技能，建议先进行扫描。

## 使用方法

```bash
python3 scripts/scan.py <path-to-skill-folder>
```

示例：
```bash
# Scan a skill before installing
python3 scripts/scan.py ~/.openclaw/skills/suspicious-skill

# Scan a freshly downloaded skill
python3 scripts/scan.py ./my-new-skill
```

**无需依赖任何第三方库**——仅使用Python 3的标准库。

## 结果解析

扫描器会返回三种判定结果：

| 判定结果 | 退出代码 | 含义 |
|---------|-----------|---------|
| **通过（PASS）** | 0 | 未检测到任何严重或高风险的威胁，可以安全安装。 |
| **警告（WARN）** | 1 | 检测到高风险行为，请在安装前仔细查看扫描结果。 |
| **阻止（BLOCK）** | 2 | 检测到严重威胁，切勿安装该技能。 |

## 检测内容

该扫描器涵盖以下20种安全威胁类别：

| 危险类别 | 检测规则 | 例子 |
|---------|-------|---------|
| **提示注入（Prompt Injection）** | MC-001, MC-002, MC-003 | 系统提示被篡改、越狱工具的使用、工具使用路径的操控 |
| **代码注入（Code Injection）** | MC-004, MC-005, MC-006, MC-019 | Shell脚本注入、eval/exec命令的使用、Base64编码后的恶意代码执行、子进程的创建 |
| **数据泄露（Data Exfiltration）** | MC-007, MC-008, MC-009, MC-010, MC-020 | Webhook链接的利用、环境变量的窃取、SSH密钥的访问、凭证文件的泄露 |
| **硬编码的敏感信息（Hardcoded Secrets）** | MC-011, MC-012 | 源代码中包含API密钥、私钥信息 |
| **金融相关威胁（Financial Threats）** | MC-013 | 资金盗用行为、无限制的账户资金提取 |
| **横向移动（Lateral Movement）** | MC-014 | 通过Git获取凭证、仓库操作被篡改 |
| **持久化威胁（Persistence Threats）** | MC-015, MC-016 | 修改系统配置文件（如SOUL.md）、创建定时任务（cron jobs） |
| **滥用系统权限（Autonomy Abuse）** | MC-017 | 使用破坏性命令（如rm -rf、git push --force） |
| **基础设施攻击（Infrastructure Attacks）** | MC-018 | 权限提升（如sudo、chmod 777） |

## 错误检测的处理

扫描器采用了基于上下文的过滤机制以减少误报：

- **环境变量访问（Env Var Access, MC-008）**：仅当变量名称包含“KEY”、“SECRET”、“PASSWORD”、“TOKEN”或“Credential”等关键词时才会触发警报 |
- **Git操作（Git Operations, MC-014）**：跳过常见的Git服务器（如github.com、gitlab.com、bitbucket.org） |
- **破坏性操作（Forceful Actions, MC-017）**：仅对具有破坏性的操作发出警报，不会对安装脚本产生误报 |

## 示例输出

```
MoltCops Security Scanner
========================================
Scanning: ./suspicious-skill
Files: 5
Rules: 20

FINDINGS
----------------------------------------
[CRITICAL] MC-007: Exfiltration URL (main.py:14)
[CRITICAL] MC-004: Shell Injection (helper.sh:8)
[HIGH] MC-005: Dynamic Code Execution (main.py:22)

SUMMARY
========================================
Files scanned: 5
Total findings: 3
  Critical: 2
  High:     1
  Medium:   0

VERDICT: BLOCK
Critical threats detected. Do NOT install this skill.
```

## Web版本

如需使用基于浏览器的扫描工具，请访问：**https://scan.moltcops.com**

## 关于MoltCops

MoltCops致力于保护AI代理生态系统免受恶意技能的侵害。虽然VirusTotal能够检测已知的恶意软件签名，但MoltCops能够捕捉到基于行为的威胁，例如资金盗用逻辑、潜伏式触发器以及提示注入等传统扫描方法难以发现的威胁行为。

- 官方网站：https://moltcops.com  
- 用户文档：https://moltbook.com/u/MoltCops