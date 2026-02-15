---
name: skillguard
version: 2.0.0
description: ClawHub 技能的安全扫描器：在安装第三方技能之前对其进行审查——检测危险模式、可疑代码和风险依赖项。
author: PaxSwarm
license: MIT
keywords: [security, audit, scan, vet, clawhub, skills, safety, moderation, vulnerability]
triggers: ["skill security", "vet skill", "scan skill", "is this skill safe", "skillguard", "audit skill", "clawscan"]
---

# 🛡️ SkillGuard — ClawHub 安全扫描器

> **“信任，但需验证。”**

ClawHub 没有审核机制，任何用户都可以发布技能。SkillGuard 提供了必要的安全保障：在技能被安装到您的系统之前，会扫描其中是否存在危险的模式、易受攻击的依赖项以及可疑的行为。

---

## 🚨 为何这很重要

第三方发布的技能可能带来以下风险：

| 风险 | 影响 |
|------|--------|
| **执行任意代码** | 会导致系统被完全控制 |
| **访问您的文件系统** | 可能导致数据被盗或遭受勒索软件攻击 |
| **读取环境变量** | 可能导致 API 密钥被窃取 |
| **通过 HTTP 泄露数据** | 侵犯隐私 |
| **安装恶意依赖项** | 引发供应链攻击 |
| **留下后门** | 造成长期的安全威胁 |
| **提升权限** | 获得 root 权限 |

**一个恶意技能就足以毁掉一切。**

SkillGuard 能在技能安装前帮助您发现这些威胁。

---

## 📦 安装

```bash
clawhub install clawscan
```

或者手动安装：
```bash
git clone https://github.com/G0HEAD/skillguard
cd skillguard
chmod +x scripts/skillguard.py
```

### 系统要求
- Python 3.8 及以上版本
- `clawhub` 命令行工具（用于远程扫描）

---

## 🚀 快速入门

```bash
# Scan a skill BEFORE installing
python3 scripts/skillguard.py scan some-random-skill

# Scan a local folder (your own skills or downloaded)
python3 scripts/skillguard.py scan-local ./path/to/skill

# Audit ALL your installed skills
python3 scripts/skillguard.py audit-installed

# Generate detailed security report
python3 scripts/skillguard.py report some-skill --format markdown

# Check dependencies for known vulnerabilities
python3 scripts/skillguard.py deps ./path/to/skill
```

---

## 🔍 SkillGuard 可检测的内容

### 🔴 **危急级别** — 禁止安装

以下模式表明存在严重的安全风险：

| 类别 | 模式 | 风险 |
|----------|----------|------|
| **代码执行** | `eval()`、`exec()`、`compile()` | 可执行任意代码 |
| **Shell 注入** | `subprocess(shell=True)`、`os.system()`、`os.popen()` | 命令注入 |
| **子进程** | `child_process.exec()`、`child_process.spawn()` | 可能用于获取 Shell 权限（Node.js） |
| **凭证窃取** | 访问 `~/.ssh/`、`~/.aws/`、`~/.config/` | 会导致私钥或凭证被窃取 |
| **系统文件** | `/etc/passwd`、`/etc/shadow` | 系统被入侵 |
| **递归删除** | `rm -rf`、`shutil.rmtree('/')` | 数据被破坏 |
| **权限提升** | `sudo`、`setuid`、`chmod 777` | 获得 root 权限 |
| **反向 Shell** | 通过 Socket 和子进程实现远程访问 |
| **加密挖矿** | 使用挖矿池 URL（如 `stratum://`） | 资源被窃取 |

### 🟡 **警告级别** — 安装前请仔细检查

以下模式可能是合法的，但仍需进一步核实：

| 类别 | 模式 | 需要注意的事项 |
|----------|----------|---------|
| **网络请求** | `requests.post()`、`fetch()` | 数据会被发送到哪里？ |
| **访问环境变量** | `os.environ`、`process.env` | 哪些变量被访问了？ |
| **文件写入** | `open(..., 'w')`、`writeFile()` | 保存了什么内容？ |
| **Base64 编码** | `base64.encode()`、`btoa()` | 数据是否被混淆了？ |
| **外部 IP 地址** | 硬编码的 IP 地址 | 是否用于数据泄露？ |
| **批量文件操作** | `shutil.copytree()`、`glob` | 是否存在大规模数据访问？ |
| **持久化设置** | `crontab`、`systemctl`、`.bashrc` | 是否会在系统启动时自动执行？ |
| **包安装** | `pip install`、`npm install` | 是否存在供应链安全风险 |

### 🟢 **信息级别** — 虽然正常，但仍需注意**

| 类别 | 模式 | 备注 |
|----------|----------|------|
| **文件读取** | `open(..., 'r')`、`readFile()` | 对于某些技能来说这是正常操作 |
| **JSON 解析** | `json.load()`、`JSON.parse()` | 用于处理数据 |
| **日志记录** | `print()`、`console.log()` | 用于调试 |
| **标准导入** | `import os`、`import sys` | 常用的库导入 |

---

## 📊 扫描结果示例

```
╔══════════════════════════════════════════════════════════════╗
║              🛡️  SKILLGUARD SECURITY REPORT                  ║
╠══════════════════════════════════════════════════════════════╣
║  Skill:       suspicious-helper v1.2.0                       ║
║  Author:      unknown-user                                   ║
║  Files:       8 analyzed                                     ║
║  Scan Time:   2024-02-03 05:30:00 UTC                        ║
╚══════════════════════════════════════════════════════════════╝

📁 FILES SCANNED
────────────────────────────────────────────────────────────────
  ✓ SKILL.md                    (541 bytes)
  ✓ scripts/main.py             (2.3 KB)
  ✓ scripts/utils.py            (1.1 KB)
  ✓ scripts/network.py          (890 bytes)
  ✓ config.json                 (234 bytes)
  ✓ requirements.txt            (89 bytes)
  ✓ package.json                (312 bytes)
  ✓ install.sh                  (156 bytes)

🔴 CRITICAL ISSUES (3)
────────────────────────────────────────────────────────────────
  [CRIT-001] scripts/main.py:45
  │ Pattern:  eval() with external input
  │ Risk:     Arbitrary code execution
  │ Code:     result = eval(user_input)
  │
  [CRIT-002] scripts/utils.py:23
  │ Pattern:  subprocess with shell=True
  │ Risk:     Command injection vulnerability
  │ Code:     subprocess.run(cmd, shell=True)
  │
  [CRIT-003] install.sh:12
  │ Pattern:  Recursive delete with variable
  │ Risk:     Potential data destruction
  │ Code:     rm -rf $TARGET_DIR/*

🟡 WARNINGS (5)
────────────────────────────────────────────────────────────────
  [WARN-001] scripts/network.py:15  — HTTP POST to external URL
  [WARN-002] scripts/main.py:78     — Reads OPENAI_API_KEY
  [WARN-003] requirements.txt:3     — Unpinned dependency: requests
  [WARN-004] scripts/utils.py:45    — Base64 encoding detected
  [WARN-005] config.json            — Hardcoded IP: 192.168.1.100

🟢 INFO (2)
────────────────────────────────────────────────────────────────
  [INFO-001] scripts/main.py:10     — Standard file read operations
  [INFO-002] requirements.txt       — 3 dependencies declared

📦 DEPENDENCY ANALYSIS
────────────────────────────────────────────────────────────────
  requirements.txt:
    ⚠️  requests        (unpinned - specify version!)
    ✓  json            (stdlib)
    ✓  pathlib         (stdlib)

  package.json:
    ⚠️  axios@0.21.0   (CVE-2021-3749 - upgrade to 0.21.2+)

════════════════════════════════════════════════════════════════
                        VERDICT: 🚫 DANGEROUS
════════════════════════════════════════════════════════════════
  
  ⛔ DO NOT INSTALL THIS SKILL
  
  3 critical security issues found:
  • Arbitrary code execution via eval()
  • Command injection via shell=True
  • Dangerous file deletion pattern
  
  Manual code review required before any use.
  
════════════════════════════════════════════════════════════════
```

---

## 🎯 命令参考

### `scan <skill-name>`  
在安装之前，从 ClawHub 下载并扫描指定的技能。

```bash
skillguard scan cool-automation-skill
skillguard scan cool-automation-skill --verbose
skillguard scan cool-automation-skill --json > report.json
```

### `scan-local <path>`  
扫描指定的本地技能目录。

```bash
skillguard scan-local ./my-skill
skillguard scan-local ~/downloads/untrusted-skill --strict
```

### `audit-installed`  
扫描您工作空间中的所有技能。

```bash
skillguard audit-installed
skillguard audit-installed --fix  # Attempt to fix issues
```

### `deps <path>`  
分析依赖项中的已知漏洞。

```bash
skillguard deps ./skill-folder
skillguard deps ./skill-folder --update-db  # Refresh vuln database
```

### `report <skill> [--format]`  
生成详细的安全报告。

```bash
skillguard report suspicious-skill --format markdown > report.md
skillguard report suspicious-skill --format json > report.json
skillguard report suspicious-skill --format html > report.html
```

### `allowlist <skill>`  
将某个技能标记为已人工审核并信任的。

```bash
skillguard allowlist my-trusted-skill
skillguard allowlist --list  # Show all trusted skills
skillguard allowlist --remove old-skill
```

### `watch`  
监控新发布的技能版本并自动进行扫描。

```bash
skillguard watch --interval 3600  # Check every hour
```

---

## ⚙️ 配置

创建 `~/.skillguard/config.json` 配置文件：

```json
{
  "severity_threshold": "warning",
  "auto_scan_on_install": true,
  "block_critical": true,
  "trusted_authors": [
    "official",
    "PaxSwarm",
    "verified-publisher"
  ],
  "allowed_domains": [
    "api.openai.com",
    "api.anthropic.com",
    "api.github.com",
    "clawhub.ai"
  ],
  "ignored_patterns": [
    "test_*.py",
    "*_test.js",
    "*.spec.ts"
  ],
  "custom_patterns": [
    {
      "regex": "my-internal-api\\.com",
      "severity": "info",
      "description": "Internal API endpoint"
    }
  ],
  "vuln_db_path": "~/.skillguard/vulns.json",
  "report_format": "markdown",
  "color_output": true
}
```

---

## 🔐 安全等级

扫描完成后，技能会被分配一个安全等级：

| 等级 | 标志 | 含义 | 建议 |
|-------|-------|---------|----------------|
| **已验证** | ✅ | 来源可信，无安全问题 | 可以安全安装 |
| **无问题** | 🟢 | 未发现安全问题 | 很可能是安全的 |
| **需要审核** | 🟡 | 仅显示警告 | 安装前请仔细阅读 |
| **可疑** | 🟠 | 存在多个警告 | 需要仔细检查 |
| **危险** | 🔴 | 存在严重安全问题 | 请禁止安装 |
| **恶意** | ⛔ | 检测到恶意代码 | 禁止安装并报告 |

---

## 🔄 集成方案

### 安装前钩子  
```bash
# Add to your workflow
skillguard scan $SKILL && clawhub install $SKILL
```

### 持续集成/持续部署（CI/CD）流程  
```yaml
# GitHub Actions example
- name: Security Scan
  run: |
    pip install skillguard
    skillguard scan-local ./my-skill --strict --exit-code
```

### 自动监控  
```bash
# Cron job for daily audits
0 9 * * * /path/to/skillguard audit-installed --notify
```

---

## 📈 漏洞数据库

SkillGuard 维护着一个包含已知漏洞的本地数据库：

**数据来源：**
- CVE 数据库（针对 Python 包的漏洞）
- npm 告警数据库
- GitHub 安全建议
- 社区报告

---

## 🚫 限制

SkillGuard 是第一道防线，但不能提供绝对的安全保障：

| 限制 | 说明 |
|------------|-------------|
| **代码混淆** | 熟练的攻击者可能隐藏恶意代码 |
| **动态代码** | 运行时生成的代码更难分析 |
| **误报** | 合法的代码也可能触发警告 |
| **零日漏洞** | 新出现的攻击模式可能无法被检测到 |
| **依赖关系** | 对依赖关系的深度扫描存在局限性 |

**深度防御策略：** 将 SkillGuard 与以下措施结合使用：
- 沙箱执行环境
- 网络监控
- 定期安全审计
- 采用最小权限原则

---

## 🤝 贡献

如果您发现了我们遗漏的恶意模式，请帮助我们改进 SkillGuard：

### 添加新的安全模式  
```json
{
  "id": "CRIT-XXX",
  "regex": "dangerous_function\\(",
  "severity": "critical",
  "category": "code_execution",
  "description": "Dangerous function call",
  "cwe": "CWE-94",
  "remediation": "Use safe_alternative() instead",
  "file_types": [".py", ".js"]
}
```

### 报告误报  
```bash
skillguard report-fp --pattern "WARN-005" --reason "Legitimate use case"
```

---

## 📜 更新日志

### v2.0.0（当前版本）  
- 全面的安全模式数据库（包含 50 多种模式）  
- 支持依赖项漏洞扫描  
- 提供多种输出格式（JSON、Markdown、HTML）  
- 支持配置文件  
- 强化对来源作者的验证  
- 支持监控新版本的功能  
- 报告中包含 CWE 参考信息

### v1.0.0  
- 初始版本  
- 基本的安全模式检测功能  
- 支持本地和远程扫描  
- 审查已安装的技能

---

## 📄 许可证

遵循 MIT 许可证——可自由使用，也欢迎贡献代码。

---

## 🛡️ 保持安全

> “在代理生态系统中，信任是通过透明度建立的。
> 您安装的每一个技能都是您选择运行的代码。
> 请谨慎选择，并务必进行验证。”

*由 [PaxSwarm](https://github.com/G0HEAD) 开发——一次保护一个技能，共同守护整个系统* 🐦‍⬛

---

**相关链接：**
- [ClawHub](https://clawhub.ai/skills/clawscan)
- [GitHub 仓库](https://github.com/G0HEAD/skillguard)
- [问题报告](https://github.com/G0HEAD/skillguard/issues)
- [安全模式数据库](https://github.com/G0HEAD/skillguard/blob/main/patterns.json)