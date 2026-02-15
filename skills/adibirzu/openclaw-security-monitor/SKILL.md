---
name: openclaw-security-monitor
description: 针对 OpenClaw 的部署环境，提供主动式安全监控、威胁扫描以及自动修复功能。
tags: [security, scan, remediation, monitoring, threat-detection, hardening]
version: 3.0.0
author: Adrian Birzu
user-invocable: true
---
```markdown
<!-- {"requires":{"bins":["bash","curl"]}} -->

# 安全监控

提供实时的安全监控服务，包括来自ClawHavoc的研究成果、每日自动扫描、Web仪表盘以及通过Telegram发送的警报。

## 命令

### /security-scan
执行全面的安全扫描，涵盖以下方面：
1. 已知的C2 IP地址（ClawHavoc提供的地址：91.92.242.x、95.92.242.x、54.91.154.110）
2. AMOS窃取工具/认证工具的痕迹
3. 反向shell和后门程序（支持多种编程语言：bash、python、perl、ruby、php、lua）
4. 用于窃取凭证的终端点（如webhook.site、pipedream、ngrok等）
5. 针对加密钱包的攻击（包括种子短语、私钥、交易所API等）
6. 利用curl进行的下载攻击
7. 敏感文件的权限审计
8. SKILL.md文件中的shell注入模式（基于预置条件的攻击）
9. 内存污染检测（涉及SOUL.md、MEMORY.md、IDENTITY.md文件）
10. Base64编码的混淆检测（检测glot.io风格的恶意载荷）
11. 外部二进制文件的下载（如.exe、.dmg、.pkg格式，以及受密码保护的ZIP文件）
12. 网关安全配置审计
13. WebSocket源地址验证（CVE-2026-25253相关问题）
14. 已知的恶意发布者检测（如hightower6eu等）
15. 敏感环境/凭证文件的泄露情况
16. DM策略审计（包括开放通道和通配符通道的访问权限）
17. 工具策略及权限提升情况的审计
18. 沙箱配置检查
19. mDNS/Bonjour协议的暴露检测
20. 会话文件和凭证文件的权限检查
21. 持久化机制的扫描（如LaunchAgents、crontabs、systemd等）
22. 插件/扩展程序的安全审计
23. 日志编辑设置的审计
24. 反向代理的本地主机信任绕过检测
25. 执行权限配置的审计（CVE-25253相关漏洞）
26. Docker容器的安全检查（包括root权限、socket挂载、特权模式等）
27. Node.js版本的漏洞检测（CVE-2026-21636相关问题）
28. 配置文件中的明文凭证检测
29. VS Code扩展程序中的恶意代码检测（如假冒的ClawdBot扩展）
30. 系统对外部的网络暴露情况检测
31. MCP服务器的安全审计（包括工具注入和提示注入等）

**退出代码说明**：
0 = 安全状态
1 = 发现警告
2 = 系统被入侵

### /security-dashboard
使用witr工具显示包含进程树的安全概览。

### /security-network
监控网络连接，并与IOC数据库进行比对。

### /security-remediate
根据扫描结果自动执行修复措施：运行`scan.sh`脚本，跳过CLEAN检查，并针对每个警告/严重风险执行相应的修复脚本。这些脚本涵盖文件权限调整、阻止数据泄露的域名、限制工具使用、加强网关安全、配置沙箱等功能。

**标志参数**：
- `--yes` / `-y`：跳过确认提示，自动批准所有修复操作
- `--dry-run`：仅显示修复方案，不实际进行任何修改
- `--check N`：仅针对指定的检查项执行修复操作（跳过扫描）
- `--all`：不进行扫描，直接执行所有修复脚本

**退出代码说明**：
0 = 所有修复操作已完成
1 = 部分修复失败
2 = 无需要修复的问题

### /security-setup-telegram
注册一个Telegram聊天频道，用于接收每日安全警报。

## Web仪表盘

**访问地址**：`http://<vm-ip>:18800`

该仪表盘采用暗黑主题设计，支持自动刷新、按需扫描、饼图显示、进程树可视化、网络监控以及扫描历史记录的查看。

### 服务管理

## IOC数据库

威胁情报文件存储在`ioc/`目录下：
- `c2-ips.txt`：已知的命令与控制IP地址
- `malicious-domains.txt`：用于托管恶意载荷和窃取数据的域名
- `file-hashes.txt`：已知的恶意文件SHA-256哈希值
- `malicious-publishers.txt`：已知的恶意ClawHub发布者信息
- `malicious-skill-patterns.txt`：恶意技能的命名模式

## 每日自动扫描

每日06:00 UTC通过Cron作业执行自动扫描，并通过Telegram发送警报。相关安装步骤请参考...

## 威胁覆盖范围

我们的威胁情报来源于40多个安全研究机构，包括：
- [ClawHavoc：发现的341种恶意技能](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting)（Koi Security）
- [CVE-2026-25253：一键远程代码执行漏洞](https://thehackernews.com/2026/02/openclaw-bug-enables-one-click-remote.html)
- [从SKILL.md文件到Shell访问的攻击路径](https://snyk.io/articles/skill-md-shell-access/)（Snyk）
- [VirusTotal：从自动化到感染的攻击过程](https://blog.virustotal.com/2026/02/from-automation-to-infection-how.html)
- [OpenClaw官方安全文档](https://docs.openclaw.ai/gateway/security)
- [DefectDojo安全检查清单](https://defectdojo.com/blog/the-openclaw-hardening-checklist-in-depth-edition)
- [Vectra：自动化工具如何成为数字后门](https://www.vectra.ai/blog/clawdbot-to-moltbot-to-openclaw-when-automation-becomes-a-digital-backdoor)
- [Cisco：AI代理的安全隐患](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare)
- [Bloom Security/JFrog：发现的37种恶意技能](https://jfrog.com/blog/giving-openclaw-the-keys-to-your-kingdom-read-this-first/)
- [OpenSourceMalware：恶意技能对加密资产的攻击](https://opensourcemalware.com/blog/clawdbot-skills-ganked-your-crypto)
- [Snyk：关于ClawdHub的深度分析](https://snyk.io/articles/clawdhub-malicious-campaign-ai-agent-skills/)
- [OWASP 2026年十大安全风险](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)
- [CrowdStrike：OpenClaw AI超级代理](https://www.crowdstrike.com/en-us/blog/what-security-teams-need-to-know-about-openclaw-ai-super-agent/)
- [Argus Security的安全审计报告（512项发现）](https://github.com/openclaw/openclaw/issues/1796)
- [ToxSec：OpenClaw安全检查清单](https://www.toxsec.com/p/openclaw-security-checklist)
- [Aikido.dev：假冒的ClawdBot VS Code扩展程序](https://www.aikido.dev/blog/fake-clawdbot-vscode-extension-malware)
- [Prompt Security：MCP安全的十大风险](https://prompt.security/blog/top-10-mcp-security-risks)

## 安装说明

OpenClaw代理会自动从`~/.openclaw/workspace/skills/`目录下的SKILL.md文件中识别恶意技能。克隆完成后，用户可以通过`/security-scan`、`/security-remediate`、`/security-dashboard`、`/security-network`和`/security-setup-telegram`命令来使用这些安全功能。
```

```bash
bash ~/.openclaw/workspace/skills/security-monitor/scripts/scan.sh
```

```