---
name: openclaw-watch
description: "🛡️ AI Agent Security Scanner — 支持285种以上的威胁模式，与OWASP Agentic AI的Top 10威胁列表进行匹配，具备风险评分功能以及内部威胁检测能力。可扫描技能、文件和工作空间以识别潜在的安全威胁。"
user-invocable: true
metadata: {"openclaw": {"emoji": "🛡️", "requires": {"bins": ["node"]}, "homepage": "https://github.com/NeuZhou/openclaw-watch"}}
---
# OpenClaw Watch — 安全扫描器

您可以使用这款强大的安全扫描器来检测 AI 代理文件和技能中的安全问题。

## 使用场景

- 当用户请求扫描文件、技能或工作空间中的安全威胁时  
- 在从 ClawHub 安装新技能之前（请先进行扫描！）  
- 在审查 SKILL.md、AGENTS.md 或任何配置文件时  
- 当用户咨询有关安全、防护或威胁检测的问题时  

## 使用方法

在目标文件或目录上运行扫描器 CLI 命令：  
```bash
# Scan a specific file
npx openclaw-watch scan ./skills/some-skill/SKILL.md

# Scan entire skills directory  
npx openclaw-watch scan ./skills/ --strict

# Scan with JSON output for programmatic use
npx openclaw-watch scan . --format json

# Scan with SARIF output for GitHub Code Scanning
npx openclaw-watch scan . --format sarif > results.sarif
```  

## 扫描内容（涵盖 285 种以上安全风险模式）  

### 提示注入（93 种模式）  
- 直接注入（“忽略之前的指令”）  
- 分隔符注入（Markdown、XML、聊天模板）  
- 多语言攻击（中文、日文、韩文）  
- 越狱尝试（DAN、开发者模式）  
- 提示型恶意代码和自我复制行为  
- 信任滥用及权限篡改  
- 安全防护绕过技巧  

### 数据泄露（62 种模式）  
- API 密钥（OpenAI、Anthropic、AWS、Azure、GCP、HuggingFace 等）  
- 认证信息（URL 中的密码、bearer tokens、基本认证、私钥）  
- 个人身份信息（SSN、信用卡号、电话号码、电子邮件）  
- 包含认证信息的数据库 URI  
- 高级数据泄露手段（信标传输、分阶段数据窃取、隐写技术）  

### 供应链攻击（35 种模式）  
- 混淆代码（eval+atob、Function 构造函数）  
- 恶意 npm 生命周期脚本  
- 反向 shell（bash、python、netcat、powershell）  
- DNS 数据窃取  
- 安全漏洞（CVE-2026-25253 等）  
- 拼写错误攻击（typosquatting）  

### 内部威胁（39 种模式）  
- AI 代理的自保护行为  
- 信息滥用/勒索  
- 与用户指令目标冲突  
- 欺骗与身份冒充  
- 未经授权的数据共享  

### 身份保护  
- SOUL.md / MEMORY.md / AGENTS.md 文件被篡改  
- 个人资料劫持及内存污染  

### MCP 安全问题  
- 工具跟踪（tool shadowing）、SSRF（跨站请求伪造）  
- 数据库模式篡改（schema poisoning）  

### 文件保护  
- 危险的删除命令（rm -rf、del /f /s）  

### 异常检测  
- 令牌炸弹（token bombs）、无限循环、递归子代理（recursive sub-agents）  

## 结果解读  

扫描器会输出检测结果，并标注风险等级：  
- 🔴 **严重** — 立即威胁，很可能具有恶意  
- 🟠 **高风险** — 严重的安全问题  
- 🟡 **警告** — 潜在风险，建议进一步检查  
- 🔵 **信息提示** — 显著但可能无害  

您可以使用 `--strict` 标志来强制处理所有被标记为“严重”或“高风险”的问题（在持续集成/持续部署（CI/CD）流程中非常有用）。  

## 示例：安装前进行安全检查  

在从 ClawHub 安装新技能之前，先对其进行扫描：  
```bash
clawhub install suspicious-skill
npx openclaw-watch scan ./skills/suspicious-skill/ --strict
```  

如果检测到严重安全问题，请建议用户卸载该技能。