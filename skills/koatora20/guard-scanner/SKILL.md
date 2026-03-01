---
name: guard-scanner
description: >
  **AI代理技能的安全扫描器**  
  在从ClawHub或外部来源安装或运行任何新技能之前，请务必使用该安全扫描器。该工具能够检测以下威胁：提示注入（prompt injection）、凭证窃取（credential theft）、数据泄露（exfiltration）、身份盗用（identity hijacking）、沙箱违规（sandbox violations）、代码复杂性（code complexity）、配置影响（config impact）以及另外17种威胁类别。此外，它还配备了实时防护机制（Runtime Guard），通过26种模式、5层防护机制以及每秒0.016毫秒的扫描速度，实时拦截危险的操作或工具调用。
homepage: https://github.com/koatora20/guard-scanner
metadata:
  openclaw:
    emoji: "🛡️"
    category: security
    requires:
      bins:
        - node
      env: []
    files: ["src/*", "hooks/*"]
    primaryEnv: null
    tags:
      - security
      - scanner
      - threat-detection
      - supply-chain
      - prompt-injection
      - sarif
---
# guard-scanner 🛡️  
一款用于AI代理技能的静态和运行时安全扫描工具。  
**包含135个静态检测规则和26个运行时检测规则（共5层防护），覆盖22个安全类别**——完全无需依赖任何外部库。**每次扫描耗时仅0.016毫秒。**  

## 适用场景  
- **在从ClawHub或其他外部来源安装新技能之前**  
- **更新技能后**，用于检测新出现的威胁  
- **定期**对已安装的技能进行安全审计  
- **在持续集成/持续部署（CI/CD）流程中**，用于控制技能的部署  

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
通过`before_tool_call`钩子实时拦截危险的操作。支持26种检测规则和3种执行模式：  
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
可在`openclaw.json`的`hooks.internal.entries.guard-scanner.mode`中设置：  
| 模式 | 功能 | 当前状态 |  
|------|-------------------|----------------|  
| `monitor` | 记录所有检测结果，不进行拦截 | ✅ 已完全启用 |  
| `enforce`（默认） | 拦截严重威胁 | ✅ 已完全启用 |  
| `strict` | 拦截高风险和严重威胁 | ✅ 已完全启用 |  

## 危险类别  
| 编号 | 类别 | 检测内容 |  
|------|---------|----------------|  
| 1   | 提示注入（Prompt Injection） | 隐藏的指令、不可见的Unicode字符、同形异义词（homoglyphs）  
| 2   | 恶意代码（Malicious Code） | 使用`eval()`函数、`child_process`进程、反向shell攻击  
| 3   | 可疑下载（Suspicious Downloads） | `curl`或`bash`命令、可执行文件下载  
| 4   | 凭据处理（Credential Handling） | 读取`.env`文件、SSH密钥访问  
| 5   | 机密信息泄露（Secret Detection） | 硬编码的API密钥和令牌  
| 6   | 数据泄露（Exfiltration） | 通过Webhook或DNS隧道进行数据传输  
| 7   | 依赖项安全性问题（Unverifiable Deps） | 远程动态导入的依赖项  
| 8   | 金融相关攻击（Financial Access） | 涉及加密钱包、支付API的攻击  
| 9   | 代码混淆（Obfuscation） | 使用Base64编码或`String.fromCharCode`函数  
| 10  | 预先条件欺诈（Prerequisites Fraud） | 假冒的下载指令  
| 11  | 技能漏洞（Leaky Skills） | 通过LLM（大型语言模型）泄露敏感信息  
| 12  | 内存篡改（Memory Poisoning） | 修改代理程序内存  
| 13  | 自复制脚本（Prompt Worm） | 具有自我复制能力的恶意脚本  
| 14  | 持久化攻击（Persistence） | 通过Cron作业或启动时执行恶意代码  
| 15  | 已知的漏洞（CVE Patterns） | 检测已知的代理程序漏洞  
| 16  | MCP安全问题（MCP Security） | 对工具或协议的攻击  
| 17  | 身份盗用（Identity Hijacking） | 修改`SOUL.md`或`IDENTITY.md`文件  
| 18  | 沙箱验证（Sandbox Validation） | 检测危险二进制文件、敏感文件操作  
| 19  | 代码复杂性（Code Complexity） | 文件长度过长、代码结构复杂、频繁使用`eval()`函数  
| 20  | 配置安全问题（Config Impact） | 修改`openclaw.json`配置、绕过执行权限检查  

*注：`strict`模式需要使用`--soul-lock`参数（可选，用于增强代理程序的身份保护）。*  

## 外部接口  
| URL | 发送的数据 | 用途 |  
|-----|-----------|---------|  
| *(无)* | *(无)* | `guard-scanner`不发送任何网络请求，所有扫描都在本地完成。*  

## 安全与隐私政策  
- **无网络连接**：`guard-scanner`不会连接到外部服务器  
- **仅读取数据**：仅读取文件内容，不会修改被扫描的目录  
- **无数据收集**：不收集任何使用数据、分析结果或故障报告  
- **本地输出**：扫描结果（JSON/SARIF/HTML格式）保存在指定目录  
- **不处理敏感信息**：不读取或处理任何敏感信息（如API密钥）  
- **审计日志**：检测结果会记录在`~/.openclaw/guard-scanner/audit.jsonl`文件中  

## 关于模型调用  
`guard-scanner` **不调用任何LLM（大型语言模型）或AI模型**。所有检测工作均通过静态模式匹配、正则表达式分析、香农熵计算以及数据流分析来完成，完全基于确定性逻辑，不涉及模型调用。  

## 开发背景  
`guard-scanner`由Guava 🍈和Dee开发，源于2026年2月发生的一起真实身份盗用事件：当时一个恶意技能悄悄替换了AI代理的`SOUL.md`文件，而现有的安全工具均无法检测到这一攻击。  
- **开源项目**：完整源代码可访问：[https://github.com/koatora20/guard-scanner](https://github.com/koatora20/guard-scanner)  
- **无依赖关系**：无需依赖任何外部库，无潜在的安全风险  
- **测试覆盖全面**：包含134个测试用例，通过率为100%  
- **基于权威标准**：参考了Snyk的`ToxicSkills`列表（2026年）、OWASP的MCP Top 10安全威胁列表以及相关研究  
- **补充VirusTotal的检测能力**：能够检测VirusTotal基于签名检测方法无法发现的特定攻击类型（如提示注入攻击）  

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

## 许可证  
MIT许可证 — [LICENSE](LICENSE)