---
name: guard-scanner
description: >
  **AI代理技能的安全扫描器**  
  在从ClawHub或外部来源安装或运行任何新技能之前，请务必使用此安全扫描器。该扫描器能够检测以下威胁：提示注入（prompt injection）、凭证窃取（credential theft）、数据泄露（exfiltration）、身份盗用（identity hijacking）、沙箱违规（sandbox violations）、代码复杂性（code complexity）、配置影响（config impact）以及另外17种威胁类别。此外，该工具还配备了实时防护机制（Runtime Guard hook），可实时拦截危险的操作或工具调用。
homepage: https://github.com/koatora20/guard-scanner
metadata:
  clawdbot:
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
一款用于AI代理技能的静态及运行时安全扫描工具。  
支持**20个类别**中的**186多种威胁模式**，且**完全无依赖项**。  

## 适用场景  
- 在从ClawHub或其他外部来源安装新技能之前  
- 更新技能后，用于检测新出现的威胁  
- 定期审计已安装的技能  
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

### 2. 运行时防护（实时保护） — ⚠️ 实验性功能  
> **注意：** 需要OpenClaw Hook API（[问题编号 #18677](https://github.com/openclaw/openclaw/issues/18677)），该API尚未正式发布。当前提供的处理程序仅用于早期测试，待API正式发布后将进行更新。  
**安装钩子以在工具执行前阻止危险操作：**  
```bash
openclaw hooks install skills/guard-scanner/hooks/guard-scanner
openclaw hooks enable guard-scanner
```  
重启代理服务器后，验证防护效果：  
```bash
openclaw hooks list   # Should show 🛡️ guard-scanner as ✓ ready
```  

### 3. 完整配置（推荐）  
详细配置方法请参考 `openclaw.json` 中的 `hooks.internal.entries.guard-scanner.mode`：  
| 模式 | 预期行为 | 当前状态 |  
|------|-------------------|----------------|  
| `monitor` | 记录所有检测结果，不阻止任何操作 | ✅ 已完全启用 |  
| `enforce`（默认） | 阻止严重威胁 | ⚠️ 仅发出警告（API功能待更新） |  
| `strict` | 阻止高风险及严重威胁 | ⚠️ 仅发出警告（API功能待更新） |  

> **注意：** OpenClaw的`InternalHookEvent`目前尚未提供`取消`/`阻止`功能。所有检测结果仅通过`event.messages`记录，无法阻止工具执行。该功能将在API正式发布后启用。  

## 威胁类别  
| 编号 | 类别 | 检测内容 |  
|---|----------|----------------|  
| 1 | 提示注入（Prompt Injection） | 隐藏指令、不可见的Unicode字符、同形异义词（homoglyphs）  
| 2 | 恶意代码（Malicious Code） | 使用`eval()`、`child_process`等函数，或创建反向shell  
| 3 | 可疑下载（Suspicious Downloads） | 包含恶意代码的下载文件（如curl\|bash）  
| 4 | 凭据处理（Credential Handling） | 读取`.env`文件、访问SSH密钥  
| 5 | 机密信息泄露（Secret Detection） | 硬编码的API密钥和令牌  
| 6 | 数据泄露（Exfiltration） | 通过Webhook或DNS隧道进行数据传输  
| 7 | 依赖项安全性问题（Unverifiable Deps） | 远程动态导入的依赖项  
| 8 | 金融相关攻击（Financial Access） | 涉及加密货币钱包或支付API的攻击  
| 9 | 代码混淆（Obfuscation） | 使用Base64编码、`String.fromCharCode`等混淆技术  
| 10 | 预置条件欺诈（Prerequisites Fraud） | 欺骗性下载指令  
| 11 | 代理技能漏洞（Leaky Skills） | 通过LLM（大型语言模型）泄露敏感信息  
| 12 | 内存污染（Memory Poisoning） | 修改代理程序内存  
| 13 | 自复制脚本（Prompt Worm） | 具有自我复制能力的恶意脚本  
| 14 | 持久化攻击（Persistence） | 通过Cron作业或启动脚本执行恶意代码  
| 15 | 已知的系统漏洞（CVE Patterns） | 检测已知的代理程序漏洞  
| 16 | MCP安全问题（MCP Security） | 模型或协议被篡改（如SSRF攻击）  
| 17 | 身份盗用（Identity Hijacking） | 修改`SOUL.md`/`IDENTITY.md`文件  
| 18 | 沙箱验证（Sandbox Validation） | 检测危险二进制文件、敏感文件操作及环境变量  
| 19 | 代码复杂性（Code Complexity） | 文件长度过长、代码结构复杂、频繁使用`eval()`函数  
| 20 | 配置相关风险（Config Impact） | 修改`openclaw.json`配置，绕过执行审批流程  

## 外部接口  
| URL | 发送的数据 | 用途 |  
|-----|-----------|---------|  
| *(无)* | *(无)* | `guard-scanner`完全不进行网络请求，所有扫描均在本地完成。  

## 安全性与隐私保护  
- **无网络连接**：`guard-scanner`从不连接外部服务器  
- **仅读取数据**：仅读取文件内容，不修改被扫描的目录  
- **无数据收集**：不收集任何使用数据、分析信息或错误报告  
- **本地输出**：扫描结果（JSON/SARIF/HTML格式）保存在指定目录  
- **不访问环境变量**：不读取或处理任何敏感信息或API密钥  
- **运行时日志**：所有检测结果记录在`~/.openclaw/guard-scanner/audit.jsonl`文件中  

## 关于模型调用  
`guard-scanner`**不调用任何LLM（大型语言模型）或AI模型**。所有检测均通过静态模式匹配、正则表达式分析、香农熵计算及数据流分析完成，完全基于规则判断，不涉及模型调用。  

## 开发背景  
`guard-scanner`由Guava 🍈和Dee开发，源于2026年2月发生的一起真实身份盗用事件：当时一个恶意技能悄悄替换了AI代理的`SOUL.md`配置文件，所有现有工具都无法检测到这一攻击。  
- **开源项目**：完整源代码可访问：[https://github.com/koatora20/guard-scanner]  
- **无依赖项**：无外部依赖，无潜在风险  
- **测试机制**：包含55个测试用例（涵盖13个方面），通过率为100%  
- **威胁分类**：基于Snyk ToxicSkills（2026年2月数据）、OWASP MCP Top 10安全标准及原创研究  
- **补充VirusTotal功能**：能检测VirusTotal基于签名检测方法无法发现的特定攻击类型（如提示注入攻击）  

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