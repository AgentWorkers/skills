---
name: skill-guard
version: 2.0.0
description: 这是一款安全扫描工具，用于检测 OpenClaw 中是否存在恶意代码、命令注入、供应链攻击、数据泄露等安全风险。
author: benjaminarp
tags: [security, scanner, audit, safety]
---
# Skill Guard v2 🛡️  
OpenClaw技能的高级安全扫描工具。能够检测恶意代码、提示注入、供应链攻击、数据泄露、凭证盗用等安全问题，并提供智能的域名分析、篡改检测以及可行的处理建议。  

## 命令  

### `scan [dir]`  
审核`~/clawd/skills/`（或自定义目录）中所有已安装的技能。  

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
适用于定时警报的简短命令。  

```bash
python3 ~/clawd/skills/skill-guard/scripts/skillguard.py watch
```  

**输出格式：**  
- `SkillGuard: 已扫描24个技能，20个安全，4个可疑，0个恶意`  
- `⚠️ SkillGuard警报：<技能>文件自基线以来发生了变化！`  
- `🔴 SkillGuard警报：<技能>被判定为恶意！`  

### `check-remote <slug>`（未来功能）  
从ClawHub下载技能文件，在临时目录中扫描后进行清理。需要ClawHub授权（目前尚未支持）。临时目录的扫描功能已准备就绪。  

## 选项  

| 标志 | 描述 |  
|------|-------------|  
| `--json` | 以机器可读的JSON格式输出结果 |  
| `--report <path>` | 生成Markdown格式的报告文件 |  
| `--baseline` | 强制重新计算所有文件的哈希值（作为基线） |  

## 检测内容  

### 代码分析  
- `eval`/`exec`调用、Shell注入、出站HTTP请求  
- Base64编码的负载（自动解码并检查内容）  
- 十六进制编码的可疑字符串  
- 缩小/混淆后的JavaScript代码  
- 时间炸弹式恶意代码（基于日期触发的攻击）  

### 智能域名分析  
- 维护包含80多个已知合法API域名的允许列表  
- 对已知API的HTTP请求 = 0风险点  
- 对未知域名的HTTP请求 = 10风险点（警告）  
- **上下文感知**：例如，“crypto-price”调用coingecko.com属于正常行为，评分较低  

### 敏感文件访问  
- SSH密钥、AWS凭证、GPG密钥库  
- 浏览器凭证存储（Chrome、Firefox、Safari）  
- 加密钱包（MetaMask、Phantom、Solana、Ethereum）  
- Keychain/Keyring访问  
- 环境变量的收集  

### 提示注入  
- 包含篡改指令的隐藏HTML注释  
- 文档中的数据泄露指令  
- 社交工程术语（如“此操作已获批准”等）  
- 针对其他技能或系统文件的修改指令  

### 供应链攻击  
- 域名抢注（通过Levenshtein距离检测包名）  
- 可疑的npm安装后脚本  
- 已知的恶意包  

### 增强检测功能（v2）  
- **文件权限**：检测`.py`、`.js`、`.md`文件的可执行权限  
- **二进制文件检测**：识别技能目录中的ELF、Mach-O、PE格式二进制文件  
- **硬编码的敏感信息**：AWS密钥（AKIA...）、GitHub令牌（ghp_...）、OpenAI密钥（sk-...）、Stripe密钥、私钥文件  
- **文件写入行为**：检测代码是否写入技能目录外的路径  
- **Unicode同形异义字符**：识别文件名中的相似字符（如Cyrillic字母“а”与Latin字母“a”）  
- **文件数量过多**：检测文件数量超过50个的技能  
- **大文件**：检测文件大小超过500KB的文件  

### 网络威胁  
- 硬编码的IP地址、反向Shell连接、DNS数据泄露  
- 与外部主机的WebSocket连接  

### 持久化攻击  
- 修改Crontab、创建launchd/systemd服务  
- 修改Shell配置文件（`.bashrc`、`.zshrc`）  

### 篡改检测（v2）  
- 首次扫描时计算每个文件的SHA-256哈希值  
- 将哈希值存储在`baselines.json`文件中  
- 重新扫描时，标记发生变化、新增或删除的文件  
- 从`.clawhub/origin.json`文件验证文件的来源  

## 评分系统（v2）  
| 检测内容 | 分数 |  
|---------|--------|  
| 发往已知API的HTTP请求 | 0分 |  
| 发往未知域名的HTTP请求 | 10分 |  
| 文档中的curl调用 | 0分 |  
| 使用`subprocess`的调用 | 2分 |  
| 使用`subprocess`且`shell=True` | 25分 |  
| 访问敏感文件 | 10-25分 |  
| 提示注入语句 | 25分 |  
| 反向Shell连接 | 自动判定为恶意行为 |  
| 访问敏感文件并尝试数据泄露 | 自动判定为恶意行为 |  
- 域名抢注的包 | 15分 |  
- SVG中的JavaScript代码 | 25分 |  

### 风险等级  
- 🟢 **安全**：得分0-15分  
- 🟡 **可疑**：得分16-40分  
- 🔴 **恶意**：得分41分及以上（或检测到危险组合）  

### 建议系统  
每个检测结果都会附带一条说明风险及建议操作的建议。  

## 测试套件  
`tests/`目录包含7个用于验证的恶意示例技能：  

| 测试技能 | 攻击方式 |  
|-----------|--------------|  
| fake-weather | SSH密钥盗用 + 向evil.com发送POST请求 |  
| fake-formatter | Base64编码的反向Shell脚本 |  
| fake-helper | 提示注入 + 社交工程攻击 |  
| fake-crypto | 加密钱包盗用 + 通信攻击 |  
| fake-typosquat | 域名抢注的包名 |  
| fake-timebomb | 基于日期触发的SSH密钥泄露 |  
| fake-svgmalware | SVG中嵌入的JavaScript代码 |  

所有7个测试技能的评分均为🔴恶意（即具有高度风险）。  

## 系统要求  
仅需要Python 3标准库，无外部依赖。  
脚本文件：`scripts/skillguard.py`