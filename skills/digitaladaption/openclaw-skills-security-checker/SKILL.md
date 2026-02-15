---
name: security-skill-scanner
version: 1.0.0
description: **ClawdHub 技能的安全扫描工具**  
该工具用于检测可疑行为模式、管理白名单，并监控 Moltbook 中的安全威胁。
homepage: https://github.com/digitaladaption/openclaw-skills-security-checker
metadata: {"clawdbot":{"emoji":"🔒","category":"security"},"author":"ClaudiatheLobster"}
---

# 安全技能扫描器

该工具用于扫描 ClawdHub 中的技能文件以检测可疑模式，管理权限信息，并监控 Moltbook 上的安全威胁。

## 主要功能

- **模式检测**：扫描 SKILL.md 文件，查找凭证盗窃、命令注入以及网络数据泄露等安全风险。
- **白名单管理**：维护已知合法技能的列表。
- **Moltbook 监控**：持续监控 Moltbook 上的安全讨论和诈骗警报。
- **权限管理**：生成并跟踪技能的权限信息。
- **每日报告**：自动执行扫描，并生成 markdown 或 JSON 格式的报告。

## 使用方法

### 扫描所有技能
```bash
python3 /root/clawd/skills/security-skill-scanner/skill-scanner.py
```

### 扫描特定技能
```bash
python3 /root/clawd/skills/security-skill-scanner/skill-scanner.py --skill nano-banana-pro
```

### 添加到白名单
```bash
python3 /root/clawd/skills/security-skill-scanner/whitelist-manager.py add skill-name "reason for whitelist"
```

### 检查白名单
```bash
python3 /root/clawd/skills/security-skill-scanner/whitelist-manager.py list
```

### 单次监控 Moltbook
```bash
bash /root/clawd/skills/security-skill-scanner/moltbook-monitor.sh
```

## 相关文件

| 文件名 | 用途 |
|------|---------|
| `skill-scanner.py` | 主扫描程序，负责正则表达式模式检测 |
| `whitelist-manager.py` | 管理误报的白名单 |
| `moltbook-monitor.sh` | Moltbook 安全信息监控脚本 |
| `permission-manager.py` | 生成技能权限信息 |
| `data/whitelist.json` | 白名单技能数据库 |

## 检测到的安全模式

| 类型 | 典型模式 |
|------|---------|
| 凭证盗窃 | 使用 `.env` 文件窃取凭证、通过 webhook 或 POST 请求窃取秘密 |
| 命令注入 | 使用 `os.system`、`eval` 或 `shell=True` 等函数进行攻击 |
| 网络数据泄露 | 通过包含Bearer 令牌的 HTTP 请求进行数据传输 |
| 可疑下载 | 使用 `wget`、`curl -O` 等命令下载可疑文件 |

## 已加入白名单的技能

以下技能为已知合法工具，因此不会被标记为可疑：
- nano-banana-pro (Google Gemini)
- notion (Notion API)
- trello (Trello API)
- gog (Google Workspace)
- local-places (Google Places)
- bluebubbles (iMessage)
- weather (Weather API)
- 以及另外 5 个工具...

## 定时任务（可选）

您可以将以下脚本添加到 crontab 中以实现自动扫描：
```bash
# Daily skill scan at 4 AM
0 4 * * * python3 /root/clawd/skills/security-skill-scanner/skill-scanner.py >> /var/log/skill-scan.log 2>&1

# Moltbook monitor every 30 min
*/30 * * * * bash /root/clawd/skills/security-skill-scanner/moltbook-monitor.sh >> /var/log/moltbook-monitor.log 2>&1
```

## 预安装钩子（阻止可疑技能的安装）

新安装的技能会自动进行安全扫描，如果发现可疑行为则会阻止安装：
```bash
# Interactive mode (asks before installing)
bash /root/clawd/skills/security-skill-scanner/install-skill.sh nano-banana-pro

# With force override (installs even if suspicious)
bash /root/clawd/skills/security-skill-scanner/install-skill.sh suspicious-skill --force

# Scan-only mode
python3 /root/clawd/skills/security-skill-scanner/install-hook.py skill-name --scan-only
```

## 与 molthub 的集成

将相关脚本添加到您的 shell 配置文件中，实现每次安装技能时的自动扫描：
```bash
# Add to ~/.bashrc or ~/.zshrc
molthub() {
    if [ "$1" = "install" ] || [ "$1" = "add" ]; then
        python3 /root/clawd/skills/security-skill-scanner/install-hook.py "$2" --interactive
    else
        /home/linuxbrew/.linuxbrew/bin/molthub "$@"
    fi
}
```

现在，每次执行 `molthub install <skill>` 时，该技能都会被先进行安全扫描！

## 扫描流程

1. **正常技能** → 正常安装 ✅
2. **白名单中的技能** → 正常安装 ✅
3. **可疑技能** → 被阻止安装，并显示警告 🚫
4. **可疑技能（使用 `--force` 参数）** → 发出警告但仍允许安装 ⚠️

## 示例输出

```
🔒 Pre-Install Security Scan: nano-banana-pro
----------------------------------------------
Status: whitelisted
Action: allowed
✅ Scan passed - safe to install

🚀 Proceeding with installation...
✅ nano-banana-pro installed successfully
```

```
🔒 Pre-Install Security Scan: weather-scam
----------------------------------------------
Status: suspicious
Action: blocked

🚨 THREATS DETECTED:
   🔴 [credential_theft] Access to .env file
      File: SKILL.md
   🔴 [network_exfil] HTTP requests with Bearer tokens
      File: scripts/steal_creds.py

❌ INSTALLATION BLOCKED

To override: python3 install-hook.py weather-scam --force
```

## 报告结果

- `/tmp/security-scanner/scan-report.md`：人类可读的扫描结果
- `/tmp/security-scanner/scan-results.json`：结构化的 JSON 输出
- `/tmp/security-scanner/moltbook-scan.log`：Moltbook 监控日志

## 集成方式

您可以将该工具作为模块导入到您的应用程序中：```python
from skill_scanner import RegexScanner

scanner = RegexScanner()
results = scanner.scan_all_skills()
print(f"Found {results['threats_found']} threats")
```