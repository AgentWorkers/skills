---
name: guard-scanner
description: >
  **AI代理技能的安全扫描工具**  
  在从ClawHub或外部来源安装或运行任何新技能之前，请务必使用该安全扫描工具。该工具能够检测提示注入、凭证窃取、数据泄露、身份盗用等14种威胁行为，并内置了实时防护机制（Runtime Guard），可阻止危险的工具调用。
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
支持**17个类别**中的**170多种威胁模式**，且**完全无依赖项**。  

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

### 2. 运行时防护（实时保护）  
安装相应的钩子，在执行前阻止危险操作：  
```bash
openclaw hooks install skills/guard-scanner/hooks/guard-scanner
openclaw hooks enable guard-scanner
```  
重启代理服务器后进行验证：  
```bash
openclaw hooks list   # Should show 🛡️ guard-scanner as ✓ ready
```  

### 3. 完整配置（推荐）  
详细配置方法请参考 `openclaw.json` 文件中的 `hooks.internal.entries.guard-scanner.mode`：  
| 模式 | 行为 |  
|------|----------|  
| `monitor` | 记录所有异常，但不阻止任何操作 |  
| `enforce`（默认） | 阻止严重威胁 |  
| `strict` | 阻止高风险及严重威胁 |  

## 威胁类别  
| 编号 | 类别 | 检测内容 |  
|---|----------|----------------|  
| 1 | 提示注入（Prompt Injection） | 隐藏的指令、不可见的Unicode字符、同形异义词  
| 2 | 恶意代码（Malicious Code） | 使用 `eval()`、`child_process` 等函数，或创建反向shell  
| 3 | 可疑下载（Suspicious Downloads） | 通过 `curl` 或 `bash` 下载的可执行文件  
| 4 | 凭据处理（Credential Handling） | 读取 `.env` 文件、访问SSH密钥  
| 5 | 机密信息泄露（Secret Detection） | 硬编码的API密钥和令牌  
| 6 | 数据泄露（Exfiltration） | 通过Webhook或DNS隧道进行数据传输  
| 7 | 依赖项安全性问题（Unverifiable Deps） | 远程动态导入的依赖项  
| 8 | 金融相关攻击（Financial Access） | 与加密货币钱包或支付API相关的攻击  
| 9 | 混淆技术（Obfuscation） | 使用Base64编码或 `String.fromCharCode` 等方法进行数据篡改  
| 10 | 预先条件欺诈（Prerequisites Fraud） | 伪造的下载指令  
| 11 | 技能漏洞（Leaky Skills） | 通过大型语言模型（LLM）上下文泄露机密信息  
| 12 | 内存污染（Memory Poisoning） | 修改代理程序的内存  
| 13 | 自复制恶意代码（Prompt Worm） | 具有自我复制能力的恶意代码  
| 14 | 持久化攻击（Persistence） | 通过Cron作业或启动时执行恶意代码  
| 15 | 已知的漏洞（CVE Patterns） | 代理程序中的已知安全漏洞  
| 16 | MCP安全相关攻击（MCP Security） | 对工具或协议的攻击  
| 17 | 身份盗用（Identity Hijacking） | 修改 `SOUL.md` 或 `IDENTITY.md` 文件  

## 外部接口  
| URL | 发送的数据 | 用途 |  
|-----|-----------|---------|  
| *(无)* | *(无)* | `guard-scanner` 不会发送任何网络请求，所有扫描操作均在本地完成。  

## 安全性与隐私保护  
- **无网络连接**：`guard-scanner` 从不连接到外部服务器  
- **仅读取数据**：仅读取文件内容，不会修改被扫描的目录  
- **无数据收集**：不收集使用数据、分析结果或崩溃报告  
- **本地输出**：扫描结果（JSON/SARIF/HTML格式）仅保存在本地  
- **不访问环境变量**：不会读取或处理任何机密信息或API密钥  
- **运行时审计日志**：检测结果会记录在 `~/.openclaw/guard-scanner/audit.jsonl` 文件中  

## 关于模型调用  
`guard-scanner` **不调用任何大型语言模型（LLM）**。所有检测工作均通过静态模式匹配、正则表达式分析、香农熵计算以及数据流分析来完成，完全基于确定性规则，不涉及模型调用。  

## 开发背景  
`guard-scanner` 由Guava 🍈 和Dee共同开发，源于2026年2月发生的一起真实身份盗用事件：当时一个恶意技能悄悄替换了AI代理的 `SOUL.md` 个人资料文件，而现有的安全工具均无法检测到这一攻击。  
- **开源项目**：完整源代码可在 [https://github.com/koatora20/guard-scanner](https://github.com/koatora20/guard-scanner) 获取  
- **无依赖项**：无需审计任何外部组件，无潜在风险  
- **测试体系**：包含45个测试用例，覆盖10个方面，通过率为100%  
- **基于权威标准**：参考了Snyk的 `ToxicSkills`（2026年2月版本）、OWASP的MCP Top 10安全列表及原创研究  
- **补充VirusTotal的功能**：能够检测VirusTotal基于签名检测方法无法发现的特定攻击类型（如提示注入攻击）  

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