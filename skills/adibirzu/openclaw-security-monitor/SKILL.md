---
name: openclaw-security-monitor
description: 针对 OpenClaw 的部署环境，提供主动式安全监控、威胁扫描以及自动修复功能。
tags: [security, scan, remediation, monitoring, threat-detection, hardening]
version: 3.2.0
author: Adrian Birzu
user-invocable: true
---```markdown
<!-- {"requires":{"bins":["bash","curl"]}} -->

# 安全监控

提供实时安全监控功能，包括来自ClawHavoc研究的威胁情报、每日自动扫描、Web仪表板以及通过Telegram发送的警报。

## 命令
注意：将`<skill-dir>`替换为实际安装此技能的文件夹名称（通常为`openclaw-security-monitor`或`security-monitor`）。

### /security-scan
执行全面的32项安全扫描：
1. 已知的C2 IP地址（ClawHavoc：91.92.242.x、95.92.242.x、54.91.154.110）
2. AMOS窃取工具/认证工具的标记
3. 反向shell和后门（bash、python、perl、ruby、php、lua）
4. 凭据泄露的终端点（webhook.site、pipedream、ngrok等）
5. 加密钱包攻击（种子短语、私钥、交易所API）
6. 使用curl进行的下载攻击
7. 敏感文件权限审计
8. SKILL.md文件中的shell注入模式（基于前提条件的攻击）
9. 内存污染检测（SOUL.md、MEMORY.md、IDENTITY.md）
10. Base64混淆检测（glot.io风格的载荷）
11. 外部二进制文件下载（.exe、.dmg、.pkg、受密码保护的ZIP文件）
12. 网关安全配置审计
13. WebSocket源地址验证（CVE-25253）
14. 已知的恶意发布者检测（hightower6eu等）
15. 敏感环境/凭证文件泄露
16. 直消息（DM）策略审计（开放/通配符通道访问）
17. 工具策略/提升权限工具审计
18. 沙箱配置检查
19. mDNS/Bonjour暴露检测
20. 会话和凭证文件权限
21. 持久化机制扫描（LaunchAgents、crontabs、systemd）
22. 插件/扩展程序安全审计
23. 日志编辑设置审计
24. 反向代理对localhost的信任绕过检测
25. 执行批准配置审计（CVE-25253漏洞链）
26. Docker容器安全（root权限、socket挂载、特权模式）
27. Node.js版本/CVE-2026-21636权限模型绕过
28. 配置文件中的明文凭证
29. VS Code扩展程序中的木马检测（假冒的ClawdBot扩展程序）
30. 互联网暴露检测（非回环网关绑定）
31. MCP服务器安全审计（工具污染、提示注入）

**退出代码**：0=安全；1=警告；2=系统受损

### /security-dashboard
使用witr显示包含进程树的安全概览。

### /security-network
监控网络连接，并与IOC数据库进行比对。

### /security-remediate
基于扫描结果进行修复：运行`scan.sh`脚本，跳过CLEAN检查，并针对每个警告/严重问题执行相应的修复脚本。包括32个单独的脚本，涵盖文件权限、泄露域名阻止、工具拒绝列表、网关加固、沙箱配置、凭证审计等。

### 标志：
- `--yes` / `-y` — 跳过确认提示（自动批准所有修复）
- `--dry-run` — 显示修复结果而不进行实际修改
- `--check N` — 仅针对指定的检查项执行修复（跳过扫描）
- `--all` — 在不进行扫描的情况下执行所有32个修复脚本

**退出代码**：0=所有修复已完成；1=部分修复失败；2=无需要修复的问题

### /security-setup-telegram
注册一个Telegram聊天频道，接收每日安全警报。

## Web仪表板
**URL**：`http://<vm-ip>:18800`
采用深色主题的浏览器仪表板，支持自动刷新、按需扫描、甜甜圈图表显示、进程树可视化、网络监控以及扫描历史记录时间线。

### 服务管理

## IOC数据库
威胁情报文件存储在`ioc/`目录下：
- `c2-ips.txt` - 已知的命令与控制IP地址
- `malicious-domains.txt` - 搭载恶意载荷和用于数据泄露的域名
- `file-hashes.txt` - 已知的恶意文件SHA-256哈希值
- `malicious-publishers.txt` - 已知的恶意ClawHub发布者
- `malicious-skill-patterns.txt` - 恶意技能的命名模式

## 每日自动扫描
在UTC时间06:00通过Cron作业执行扫描，并通过Telegram发送警报。请先安装相关依赖项：

### 威胁覆盖范围
威胁情报来源于40多个安全来源，包括：
- [ClawHavoc：341种恶意技能](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting)（Koi Security）
- [CVE-2026-25253：一键远程代码执行（CVE-2026-25253）  
- [从SKILL.md到Shell访问](https://snyk.io/articles/skill-md-shell-access/)（Snyk）
- [VirusTotal：从自动化到感染](https://blog.virustotal.com/2026/02/from-automation-to-infection-how.html)
- [OpenClaw官方安全文档](https://docs.openclaw.ai/gateway/security)
- [DefectDojo加固检查清单](https://defectdojo.com/blog/the-openclaw-hardening-checklist-in-depth-edition)
- [Vectra：自动化工具成为数字后门](https://www.vectra.ai/blog/clawdbot-to-moltbot-to-openclaw-when-automation-becomes-a-digital-backdoor)
- [Cisco：AI代理的安全隐患](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare)
- [Bloom Security/JFrog：37种恶意技能](https://jfrog.com/blog/giving-openclaw-the-keys-to-your-kingdom-read-this-first/)
- [OpenSourceMalware：恶意技能对加密资产的攻击](https://opensourcemalware.com/blog/clawdbot-skills-ganked-your-crypto)
- [Snyk：ClawdHub恶意活动分析](https://snyk.io/articles/clawdhub-malicious-campaign-ai-agent-skills/)
- [OWASP 2026年十大安全风险](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)
- [CrowdStrike：OpenClaw AI超级代理](https://www.crowdstrike.com/en-us/blog/what-security-teams-need-to-know-about-openclaw-ai-super-agent/)
- [Argus安全审计（512项发现](https://github.com/openclaw/openclaw/issues/1796)
- [ToxSec：OpenClaw安全检查清单](https://www.toxsec.com/p/openclaw-security-checklist)
- [Aikido.dev：假冒的ClawdBot VS Code扩展程序](https://www.aikido.dev/blog/fake-clawdbot-vscode-extension-malware)
- [Prompt Security：十大MCP安全风险](https://prompt.security/blog/top-10-mcp-security-risks)

## 安装
OpenClaw代理会自动从`~/.openclaw/workspace/skills/`目录下的SKILL.md文件中检测可用技能。克隆完成后，`/security-scan`、`/security-remediate`、`/security-dashboard`、`/security-network`和`/security-setup-telegram`命令将在代理中可用。
```