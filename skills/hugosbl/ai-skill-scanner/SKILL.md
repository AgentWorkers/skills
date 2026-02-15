---
name: skill-scanner
description: 在安装 OpenBot/Clawdbot 的技能之前，先对其进行安全漏洞、恶意代码以及可疑模式的扫描。当用户需要对某个技能进行审计、检查 ClawHub 技能的安全性、扫描是否存在凭证泄露风险、检测提示注入行为或审查技能的安全性时，可以使用该工具。该功能会在安全审计、技能安全性检查、恶意软件扫描或信任验证过程中被触发。
---

# 技能安全扫描器

在安装技能之前，会扫描其中是否存在恶意代码模式。该工具能够检测到凭证泄露、可疑的网络请求、混淆代码、提示注入等安全风险。

## 快速入门

```bash
# Scan a local skill folder
python3 scripts/scan.py /path/to/skill

# Verbose output (show matched lines)
python3 scripts/scan.py /path/to/skill --verbose

# JSON output (for automation)
python3 scripts/scan.py /path/to/skill --json
```

## 工作流程：安装前扫描

1. 下载或找到技能对应的文件夹。
2. 运行 `python3 scripts/scan.py <skill-path> --verbose` 命令。
3. 根据风险等级（CRITICAL/HIGH：禁止安装）查看扫描结果。
4. 将扫描结果告知用户，并提供相应的建议。

## 分数解读

| 分数 | 含义 | 建议 |
|-------|---------|----------------|
| CLEAN | 未发现任何问题 | 可以安全安装 |
| INFO | 仅发现轻微问题 | 可以安全安装 |
| REVIEW | 发现中等风险的问题 | 安装前需手动检查 |
| SUSPICIOUS | 发现高风险问题 | 未经彻底手动检查前禁止安装 |
| DANGEROUS | 检测到严重问题 | 禁止安装——可能存在恶意行为 |

## 退出代码

- `0` = CLEAN/INFO
- `1` = REVIEW
- `2` = SUSPICIOUS
- `3` = DANGEROUS

## 规则参考

请参阅 `references/rules.md` 文件，以获取完整的检测规则、风险等级及白名单域名列表。

## 限制

- 采用基于模式的检测方法，可能无法识别所有混淆技术。
- 仅进行静态扫描，不支持运行时分析。
- 对于合法但需要访问网络或文件的工具，可能会出现误报。
- 对于高风险或中等风险的扫描结果，必须结合手动审查进行判断。