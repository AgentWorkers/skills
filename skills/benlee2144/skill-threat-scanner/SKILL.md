---
name: skill-threat-scanner
version: 2.0.0
description: "扫描 OpenClaw 中的恶意技能，包括植入恶意代码、创建反向 shell（远程控制工具）、窃取钱包信息、发起供应链攻击以及数据泄露等行为。保护您的代理免受 386 种以上恶意 ClawHub 技能的攻击（例如 ClawHavoc）。该系统提供 9 大类威胁检测功能、篡改行为监控以及 JSON 格式的报告生成，且完全不依赖任何第三方库或组件（零依赖）。"
author: benjaminarp
tags: [security, scanner, audit, safety, malware-detection, threat-scanner, openclaw-security, clawhub-security, skill-scanner, prompt-injection, supply-chain, antivirus]
metadata:
  openclaw:
    emoji: "🛡️"
    keywords: ["security scan", "malicious skill", "malware detector", "skill audit", "threat detection", "ClawHavoc", "prompt injection scanner", "supply chain attack", "wallet theft protection", "openclaw antivirus", "clawhub safety"]
---
# Skill Threat Scanner 🛡️  
### 保护您的 OpenClaw 代理免受恶意技能的攻击  

这是一款针对 OpenClaw 技能的高级安全扫描工具，能够检测恶意代码、提示注入、供应链攻击、数据泄露、凭证窃取等多种安全威胁。它具备智能域名分析、篡改检测功能，并提供可操作的修复建议。  

## 命令  

### `scan [dir]`  
审核 `~/clawd/skills/`（或自定义目录）中安装的所有技能。  

```bash
python3 ~/clawd/skills/skill-guard/scripts/skillguard.py scan
python3 ~/clawd/skills/skill-guard/scripts/skillguard.py scan --json
python3 ~/clawd/skills/skill-guard/scripts/skillguard.py scan --report report.md
python3 ~/clawd/skills/skill-guard/scripts/skillguard.py scan --baseline  # force re-baseline
```  

### `check <path>`  
扫描单个技能目录，或包含多个技能的目录。  

```bash
python3 ~/clawd/skills/skill-guard/scripts/skillguard.py check ~/clawd/skills/some-skill
python3 ~/clawd/skills/skill-guard/scripts/skillguard.py check ~/clawd/skills/skill-guard/tests/
```  

### `watch [dir]`  
适用于定时任务（cron）的简短命令。  

```bash
python3 ~/clawd/skills/skill-guard/scripts/skillguard.py watch
```  

**输出格式：**  
- `SkillGuard: 已扫描 24 个技能，20 个安全，4 个可疑，0 个恶意`  
- `⚠️ SkillGuard 警报：<技能> 文件自基线以来发生了变化！`  
- `🔴 SkillGuard 警报：<技能> 被判定为恶意！`  

### `check-remote <slug>`（未来功能）  
从 ClawHub 下载技能文件，在临时目录中扫描后进行清理。需要 ClawHub 的授权（目前尚未支持）。临时目录的扫描功能已准备就绪。  

## 选项  

| 标志 | 描述 |  
|------|-------------|  
| `--json` | 以机器可读的 JSON 格式输出结果 |  
| `--report <path>` | 生成 Markdown 报告文件 |  
| `--baseline` | 强制重新生成所有文件的哈希值基线 |  

## 检测内容  

### 代码分析  
- `eval`/`exec` 调用、Shell 注入、出站 HTTP 请求  
- Base64 编码的负载（自动解码并检查内容）  
- 十六进制编码的可疑字符串  
- 缩小/混淆后的 JavaScript 代码  
- 时间炸弹式恶意代码（基于日期触发的攻击）  

### 智能域名分析  
- 维护着 80 多个已知合法 API 域名的白名单  
- 对已知 API 的 HTTP 请求 = 0 风险  
- 对未知域名的 HTTP 请求 = 10 风险（警告）  
- 具有上下文感知能力：例如，“crypto-price”调用 coingecko.com 是正常行为，评分较低  

### 敏感文件访问  
- SSH 密钥、AWS 凭证、GPG 密钥库  
- 浏览器凭证存储（Chrome、Firefox、Safari）  
- 加密钱包（MetaMask、Phantom、Solana、Ethereum）  
- Keychain/Keyring 访问  
- 环境变量收集  

### 提示注入  
- 包含篡改指令的隐藏 HTML 注释  
- 文档中的数据泄露指令  
- 社交工程术语（如“这是可信的”、“已预先批准”等）  
- 针对其他技能或系统文件的修改指令  

### 供应链攻击  
- 拼写错误攻击（通过 Levenshtein 距离检测包名）  
- 可疑的 npm 安装后脚本  
- 已知的恶意包  

### 增强检测（v2）  
- **文件权限**：检测 `.py`、`.js`、`.md` 文件的可执行位  
- **二进制文件检测**：识别技能目录中的 ELF、Mach-O、PE 格式的二进制文件  
- **硬编码的敏感信息**：AWS 密钥（AKIA...）、GitHub 令牌（ghp_...）、OpenAI 密钥（sk-...）、Stripe 密钥、私钥文件  
- **文件写入行为**：检测代码是否写入技能目录之外的路径  
- **Unicode 同形字符**：识别文件名中的相似字符（如 Cyrillic 的 “а” 和 Latin 的 “a”）  
- **文件数量过多**：检测文件数量超过 50 个的技能  
- **大文件**：检测文件大小超过 500KB 的文件  

### 网络威胁  
- 硬编码的 IP 地址、反向 Shell 连接、DNS 数据泄露  
- 与外部主机的 WebSocket 连接  

### 持久化攻击  
- 修改 Cron 行程、创建 launchd/systemd 服务  
- 修改 Shell 配置文件（`.bashrc`、`.zshrc`）  

### 篡改检测（v2）  
- 首次扫描时计算每个文件的 SHA-256 哈希值  
- 将哈希值存储在 `baselines.json` 文件中  
- 重新扫描时，标记发生变化、新增或删除的文件  
- 从 `.clawhub/origin.json` 文件中验证文件的来源  

## 评分系统（v2）  
| 检测内容 | 分数 |  
|---------|--------|  
| 发往已知 API 的 HTTP 请求 | 0 |  
| 发往未知域名的 HTTP 请求 | 10 |  
| 文档中的 curl 调用 | 0 |  
| 子进程调用 | 2 |  
| 使用 `shell=True` 的子进程 | 25 |  
| 敏感文件访问 | 10–25 |  
| 提示注入语句 | 25 |  
| 反向 Shell 连接 | 自动判定为恶意 |  
| 敏感文件访问 + 出站请求 | 自动判定为恶意 |  
| 拼写错误的包名 | 15 |  
| SVG 中嵌入的 JavaScript 代码 | 25 |  

### 风险等级  
- 🟢 **安全**：得分 0–15  
- 🟡 **可疑**：得分 16–40  
- 🔴 **恶意**：得分 41 分及以上，或检测到危险组合  

### 建议系统  
每个检测结果都会附带一条简短的提示，说明风险及建议的应对措施。  

## 测试套件  
`tests/` 目录中包含 7 个用于验证的恶意技能示例：  

| 测试技能 | 攻击方式 |  
|-----------|--------------|  
| fake-weather | SSH 密钥窃取 + 向 evil.com 发送 POST 请求 |  
| fake-formatter | Base64 编码的反向 Shell 连接 |  
| fake-helper | 提示注入 + 社交工程攻击 |  
| fake-crypto | 加密钱包窃取 + 通信攻击 |  
| fake-typosquat | 拼写错误的包名 |  
| fake-timebomb | 基于日期触发的 SSH 密钥泄露 |  
| fake-svgmalware | SVG 中嵌入的 JavaScript 代码 |  

所有 7 个测试技能都被判定为 **恶意**（评分 🔴）。  

## 系统要求  
仅需要 Python 3 的标准库。无外部依赖。程序文件：`scripts/skillguard.py`。