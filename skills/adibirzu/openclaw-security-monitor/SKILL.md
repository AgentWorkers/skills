---
name: openclaw-security-monitor
description: 针对 OpenClaw 的部署环境，提供主动式安全监控、威胁扫描以及自动修复功能。
tags: [security, scan, remediation, monitoring, threat-detection, hardening]
version: 3.4.0
author: Adrian Birzu
user-invocable: true
---```json
{
  "requires": {
    "bins": ["bash", "curl", "node", "lsof"],
    "optionalBins": ["witr", "docker", "openclaw"]
  },
  "env": {
    "OPENCLAW_TELEGRAM_TOKEN": "可选：用于每日安全警报的Telegram机器人令牌",
    "OPENCLAW_HOME": "可选：覆盖默认的 ~/.openclaw 目录"
  }
}
```

# 安全监控

提供实时的安全监控功能，包括来自ClawHavoc研究的威胁情报、每日自动扫描、Web仪表盘以及通过Telegram发送的安全警报。

## 命令
注意：请将 `<skill-dir>` 替换为实际安装此技能的文件夹名称（通常为 `openclaw-security-monitor` 或 `security-monitor`）。

### /security-scan
执行全面的40项安全扫描：
1. 已知的C2 IP地址（ClawHavoc：91.92.242.x, 95.92.242.x, 54.91.154.110）
2. AMOS窃取工具/认证工具的痕迹
3. 反向shell和后门（bash、python、perl、ruby、php、lua）
4. 证书窃取端点（webhook.site、pipedream、ngrok等）
5. 加密钱包攻击（种子短语、私钥、交易所API）
6. 使用curl-pipe进行的下载攻击
7. 敏感文件权限审计
8. SKILL.md文件中的shell注入模式（基于前提条件的攻击）
9. 内存污染检测（SOUL.md、MEMORY.md、IDENTITY.md）
10. Base64混淆检测（glot.io风格的负载）
11. 外部二进制文件下载（.exe、.dmg、.pkg、受密码保护的ZIP文件）
12. 网关安全配置审计
13. WebSocket源地址验证（CVE-2526-25253）
14. 已知的恶意发布者检测（hightower6eu等）
15. 敏感环境/证书文件泄露
16. 直私信政策审计（开放/通配符通道访问）
17. 工具政策/提升权限工具审计
18. 沙箱配置检查
19. mDNS/Bonjour暴露检测
20. 会话和证书文件权限
21. 持久化机制扫描（LaunchAgents、crontabs、systemd）
22. 插件/扩展程序安全审计
23. 日志编辑设置审计
24. 反向代理localhost信任绕过检测
25. 执行权限配置审计（CVE-25253漏洞链）
26. Docker容器安全（root权限、socket挂载、特权模式）
27. Node.js版本/CVE-2026-21636权限模型绕过
28. 配置文件中的明文证书检测
29. VS Code扩展程序中的木马检测（假冒的ClawdBot扩展程序）
30. 互联网暴露检测（非回环网关绑定）
31. MCP服务器安全审计（工具污染、提示注入）
32. ClawJacked WebSocket暴力破解保护（v2026.2.25+）
34. SSRF保护审计（CVE-2526-26322、CVE-2026-27488）
35. Exec safeBins验证绕过（CVE-2026-28363，CVSS 9.9）
36. ACP权限自动批准审计（GHSA-7jx5）
37. PATH劫持/命令劫持（GHSA-jqpq-mgvm-f9r6）
38. 技能环境变量覆盖主机注入（GHSA-82g8-464f-2mv7）
39. macOS深度链接截断（CVE-26320）
40. 日志污染/WebSocket头部注入

### /security-dashboard
使用witr显示包含进程树的安全概览。

### /security-network
监控网络连接并检查IOC数据库。

### /security-remediate
基于扫描结果的修复：运行 `scan.sh`，跳过CLEAN检查，并为每个警告/严重发现执行相应的修复脚本。包括40个单独的脚本，涵盖文件权限、域名阻止、工具拒绝列表、网关加固、沙箱配置、证书审计、ClawJacked保护、SSRF加固、PATH劫持清理等。

### 标志：
- `--yes` / `-y` — 跳过确认提示（自动批准所有修复）
- `--dry-run` — 显示修复内容而不进行实际修改
- `--check N` — 仅针对指定的检查项执行修复（跳过扫描）
- `--all` — 在不进行扫描的情况下运行所有40个修复脚本

### /security-setup-telegram
注册一个Telegram聊天频道以接收每日安全警报。

## Web仪表盘

**URL**: `http://<vm-ip>:18800`

采用暗黑主题的浏览器仪表盘，支持自动刷新、按需扫描、饼图显示、进程树可视化、网络监控和扫描历史记录时间线。

### 服务管理

## IOC数据库

威胁情报文件存储在 `ioc/` 目录下：
- `c2-ips.txt` - 已知的命令与控制IP地址
- `malicious-domains.txt` - 搭载恶意负载和用于数据窃取的域名
- `file-hashes.txt` - 已知的恶意文件SHA-256哈希值
- `malicious-publishers.txt` - 已知的恶意ClawHub发布者
- `malicious-skill-patterns.txt` - 恶意技能的命名模式

## 每日自动扫描

在UTC时间06:00通过Cron作业执行扫描，并通过Telegram发送警报。需要安装相关依赖项：

## 威胁覆盖范围

基于来自40多个安全来源的研究，包括：
- [ClawHavoc：341种恶意技能](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting)（Koi Security）
- [CVE-2026-25253：一键远程代码执行](https://thehackernews.com/2026/02/openclaw-bug-enables-one-click-remote.html)
- [从SKILL.md到Shell访问](https://snyk.io/articles/skill-md-shell-access/)（Snyk）
- [VirusTotal：从自动化到感染](https://blog.virustotal.com/2026/02/from-automation-to-infection-how.html)
- [OpenClaw官方安全文档](https://docs.openclaw.ai/gateway/security)
- [DefectDojo加固检查清单](https://defectdojo.com/blog/the-openclaw-hardening-checklist-in-depth-edition)
- [Vectra：自动化成为后门](https://www.vectra.ai/blog/clawdbot-to-moltbot-to-openclaw-when-automation-becomes-a-digital-backdoor)
- [Cisco：AI代理的安全隐患](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare)
- [Bloom Security/JFrog：37种恶意技能](https://jfrog.com/blog/giving-openclaw-the-keys-to-your-kingdom-read-this-first/)
- [OpenSourceMalware：恶意技能窃取你的加密货币](https://opensourcemalware.com/blog/clawdbot-skills-ganked-your-crypto)
- [Snyk：ClawdHub恶意活动深度分析](https://snyk.io/articles/clawdhub-malicious-campaign-ai-agent-skills/)
- [OWASP 2026年十大安全风险](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [CrowdStrike：OpenClaw AI超级代理](https://www.crowdstrike.com/en-us/blog/what-security-teams-need-to-know-about-openclaw-ai-super-agent/)
- [Argus Security审计（512项发现）](https://github.com/openclaw/openclaw/issues/1796)
- [ToxSec：OpenClaw安全检查清单](https://www.toxsec.com/p/openclaw-security-checklist)
- [Aikido.dev：假冒的ClawdBot VS Code扩展程序](https://www.aikido.dev/blog/fake-clawdbot-vscode-extension-malware)
- [Prompt Security：十大MCP安全风险](https://prompt.security/blog/top-10-mcp-security-risks)
- [Oasis Security：ClawJacked漏洞](https://www.oasis.security/blog/openclaw-vulnerability)（2月26日）
- [CVE-2026-28363：safeBins绕过（CVSS 9.9）](https://advisories.gitlab.com/pkg/npm/openclaw/CVE-28363/)
- [Flare：广泛传播的攻击](https://flare.io/learn/resources/blog/widespread-openclaw-exploitation)（2月25日）

## 安全性与透明度

**扫描器为何会自我标记**：ClawHub的扫描器可能会报告针对此技能的 `[ignore-previous-instructions]` 发现。这是一个**误报**——字符串“ignore previous”、“override instruction”等仅存在于我们的**检测模式**中（`scan.sh` 和修复脚本中的grep正则表达式）。这些模式用于检测其他技能中的提示注入；它们并不是对代理的指令。

**环境变量**：此技能可选地使用 `OPENCLAW_TELEGRAM_TOKEN` 来接收每日扫描警报，以及 `OPENCLAW_HOME` 来覆盖默认的 `~/.openclaw` 目录。这些变量在上面的元数据中有所说明。

**必需的二进制文件**：`bash`、`curl`、`node`（用于仪表盘）、`lsof`（用于网络检查）。可选：`witr`（用于进程树显示）、`docker`（用于容器审计）、`openclaw` CLI（用于配置检查）。

**扫描器读取的内容**：扫描器会检查 `~/.openclaw/` 目录下的文件（配置文件、技能脚本、凭证文件和日志文件）以检测威胁。它仅将 `.env`、`.ssh` 和密钥链路径作为**检测模式**来读取——绝不会窃取或传输这些数据。

**修复措施**：修复脚本可以修改文件权限、在 `/etc/hosts` 中阻止域名、调整OpenClaw配置以及移除恶意技能。始终先运行 `--dry-run` 以预览修复效果。`--yes` 标志会自动批准所有修复操作——仅在查看dry-run结果后使用。

**持久化**：每日Cron作业和LaunchAgent（仪表盘）都是**可选的**，由用户手动安装。此技能不会自动设置持久化机制。

**IOC更新**：`update-ioc.sh` 会从这个项目的GitHub仓库获取威胁情报。如果你想控制数据来源，可以固定上游URL。

**仪表盘绑定**：Web仪表盘默认绑定到 `127.0.0.1:18800`（仅限本地主机）。如果担心局域网暴露问题，可以明确设置 `DASHBOARD_HOST=127.0.0.1`。

## 安装

OpenClaw代理会自动从 `~/.openclaw/workspace/skills/` 目录下的SKILL.md文件中发现可用的技能。克隆完成后，`/security-scan`、`/security-remediate`、`/security-dashboard` 和 `/security-network` 命令将在代理中可用。
```