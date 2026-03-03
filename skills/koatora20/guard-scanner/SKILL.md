---
name: guard-scanner
description: "AI代理技能的安全扫描器：支持135种静态模式检测和26种运行时检查，覆盖22个威胁类别。能够检测提示注入（prompt injection）、凭证窃取（credential theft）、数据泄露（exfiltration）、身份盗用（identity hijacking）等多种安全威胁。该工具完全无需依赖任何外部库或服务。"
metadata:
  clawdbot:
    homepage: "https://github.com/koatora20/guard-scanner"
requires:
  env: {}
---
# guard-scanner 🛡️  
一个用于AI代理技能的静态及运行时安全扫描器。  
**包含135个静态检测规则和26个运行时检测规则（共5层），覆盖22个安全类别**——完全无需依赖任何外部库。**每次扫描耗时仅0.016毫秒。**  

## 适用场景  
- 在从ClawHub或任何外部来源安装新技能之前  
- 更新技能后，用于检测新出现的威胁  
- 定期对已安装的技能进行安全审计  
- 在持续集成/持续部署（CI/CD）过程中，用于控制技能的部署  

## 快速入门  

### 1. 静态扫描（立即执行）  
扫描所有已安装的技能：  
```bash
node skills/guard-scanner/src/cli.js ~/.openclaw/workspace/skills/ --verbose --self-exclude
```  

扫描特定技能：  
```bash
node skills/guard-scanner/src/cli.js /path/to/new-skill/ --strict --verbose
```  

### 2. 运行时防护（OpenClaw插件钩子）  
通过`before_tool_call`钩子实时拦截危险的操作。支持26种检测规则、5层防护机制，以及3种执行模式：  
```bash
openclaw hooks install skills/guard-scanner/hooks/guard-scanner
openclaw hooks enable guard-scanner
openclaw hooks list
```  

### 推荐使用顺序  
```bash
# Pre-install / pre-update gate first
node skills/guard-scanner/src/cli.js ~/.openclaw/workspace/skills/ --verbose --self-exclude --html

# Then keep runtime monitoring enabled
openclaw hooks install skills/guard-scanner/hooks/guard-scanner
openclaw hooks enable guard-scanner
```  

## 运行时防护模式  
在`openclaw.json`的`hooks.internal.entries.guard-scanner.mode`中配置：  
| 模式 | 功能 | 当前状态 |  
|------|-------------------|----------------|  
| `monitor` | 记录所有检测结果，不进行拦截 | ✅ 已完全启用 |  
| `enforce`（默认） | 拦截严重威胁 | ✅ 已完全启用 |  
| `strict` | 拦截高级别及严重威胁 | ✅ 已完全启用 |  

## 威胁类别  
| 编号 | 类别 | 检测内容 |  
|------|---------|----------------|  
| 1   | 提示注入（Prompt Injection） | 隐藏的指令、不可见的Unicode字符、同形异义词（homoglyphs） |  
| 2   | 恶意代码（Malicious Code） | `eval()`函数、`child_process`进程、反向shell攻击 |  
| 3   | 可疑下载（Suspicious Downloads） | `curl`或`bash`命令、可执行文件下载 |  
| 4   | 凭据处理（Credential Handling） | `.env`文件中的敏感信息、SSH密钥访问 |  
| 5   | 机密信息泄露（Secret Detection） | 硬编码的API密钥和令牌 |  
| 6   | 数据泄露（Exfiltration） | Webhook攻击、DNS隧道技术 |  
| 7   | 依赖项安全性问题（Unverifiable Deps） | 远程动态导入的依赖项 |  
| 8   | 财务安全风险（Financial Access） | 加密钱包、支付API相关攻击 |  
| 9   | 代码混淆（Obfuscation） | 使用Base64编码的恶意代码、`String.fromCharCode`函数 |  
| 10  | 预安装程序欺诈（Prerequisites Fraud） | 假冒的下载指令 |  
| 11  | 技能信息泄露（Leaky Skills） | 通过LLM（大型语言模型）泄露敏感信息 |  
| 12  | 内存破坏（Memory Poisoning） | 修改代理程序的内存内容 |  
| 13  | 自复制恶意代码（Prompt Worm） | 具有自我复制能力的恶意代码 |  
| 14  | 持久化攻击（Persistence） | 通过Cron任务或启动脚本执行的恶意行为 |  
| 15  | 已知的漏洞（CVE Patterns） | 代理程序中的已知安全漏洞 |  
| 16  | MCP安全问题（MCP Security） | 对工具或协议的攻击 |  
| 17  | 身份盗用（Identity Hijacking） | 修改`SOUL.md`或`IDENTITY.md`文件 |  
| 18  | 沙箱验证（Sandbox Validation） | 危险的二进制文件、敏感文件操作 |  
| 19  | 代码复杂性（Code Complexity） | 过长的文件长度、复杂的代码结构 |  
| 20  | 配置安全风险（Config Impact） | 修改`openclaw.json`配置文件、绕过执行权限检查 |  

## 外部接口  
| URL | 发送的数据 | 功能 |  
|-----|-----------|---------|  
| *(无)* | *(无)* | `guard-scanner`不发送任何网络请求，所有扫描操作都在本地完成。**  

## 安全性与隐私保护  
- **无网络连接**：`guard-scanner`从不连接外部服务器  
- **仅读取文件**：仅读取文件内容，不修改被扫描的目录  
- **无数据收集**：不收集任何使用数据、分析结果或故障报告  
- **本地输出**：所有扫描结果（JSON/SARIF/HTML格式）仅保存在扫描目录中  
- **不访问环境变量**：不读取或处理任何敏感信息或API密钥  
- **日志记录**：检测结果会记录在`~/.openclaw/guard-scanner/audit.jsonl`文件中  

## 关于模型调用  
`guard-scanner` **不调用任何LLM（大型语言模型）**。所有检测工作均通过静态模式匹配、正则表达式分析、香农熵计算以及数据流分析来完成，完全依赖确定性逻辑，不涉及任何模型调用。  

## 开发背景  
`guard-scanner`由Guava 🍈和Dee团队在2026年2月经历了一次真实身份盗用事件后开发。当时，一个恶意技能悄悄替换了AI代理的`SOUL.md`配置文件，而现有的安全工具都无法检测到这一攻击。  
- **开源项目**：源代码可访问：[https://github.com/koatora20/guard-scanner](https://github.com/koatora20/guard-scanner)  
- **无依赖项**：无需审计任何外部库，无潜在的安全风险  
- **测试机制**：包含134个测试用例，通过率为100%  
- **规则依据**：基于Snyk的`ToxicSkills`列表（2026年2月）、OWASP的MCP Top 10安全威胁列表以及原创研究  
- **补充功能**：能够检测VirusTotal无法识别的提示注入攻击和针对LLM的特定攻击  

## 输出格式  
```bash
# Terminal (default)
node src/cli.js ./skills/ --verbose

# JSON report
node src/cli.js ./skills/ --json

# SARIF 2.1.0 (for CI/CD)
node src/cli.js ./skills/ --sarif

# HTML dashboard
node src/cli.js ./skills/ --html
```  

## 许可协议  
MIT许可证 — [LICENSE](LICENSE)