---
name: flaw0
description: OpenClaw 代码、插件、技能以及 Node.js 依赖项的安全性和漏洞扫描工具。该工具基于 OpenClaw 的 AI 模型进行开发。
version: 1.0.0
author: Tom
homepage: https://github.com/yourusername/flaw0
license: MIT
metadata:
  openclaw:
    emoji: "🔍"
    category: "security"
tags:
  - security
  - vulnerability-scanner
  - code-analysis
  - dependency-checker
  - openclaw
---

# flaw0 - 零缺陷安全扫描器

这是一个专为 OpenClaw 生态系统设计的安全与漏洞扫描工具。它通过分析源代码、插件、技能以及 Node.js 依赖项来检测潜在的安全隐患。

**目标：实现零缺陷（flaw 0）** 🎯

## 安装

您可以通过 [ClawHub](https://www.clawhub.ai) 安装此工具：

```bash
npx clawhub@latest install flaw0
```

或者通过 npm 全局安装：

```bash
npm install -g flaw0
```

## 何时使用此工具

使用 **flaw0** 可以确保您的 OpenClaw 代码及其依赖项的安全性：

### 安装技能之前

```bash
# Check a skill before installing
flaw0 scan ~/.openclaw/skills/new-skill
```

### 开发过程中

```bash
# Scan your code as you develop
flaw0 scan src/

# Check dependencies
flaw0 deps
```

### 提交代码之前

```bash
# Full security audit
flaw0 audit
```

### 审计 OpenClaw 安装情况

```bash
# Scan all OpenClaw components
flaw0 scan --target all

# Check specific components
flaw0 scan --target skills
flaw0 scan --target plugins
flaw0 scan --target core
```

## 使用方法

### 基本命令

#### 扫描代码

```bash
# Scan current directory
flaw0 scan

# Scan specific directory
flaw0 scan /path/to/code

# Use specific AI model
flaw0 scan --model claude-opus-4-6
```

#### 检查依赖项

```bash
# Quick dependency scan
flaw0 deps

# Deep scan (entire dependency tree)
flaw0 deps --deep
```

#### 进行全面安全审计

```bash
# Comprehensive scan (code + dependencies)
flaw0 audit

# Save report to file
flaw0 audit --output report.json

# JSON output for CI/CD
flaw0 audit --json
```

#### 扫描 OpenClaw 组件

```bash
# Scan OpenClaw core
flaw0 scan --target core

# Scan all plugins
flaw0 scan --target plugins

# Scan all skills
flaw0 scan --target skills

# Scan everything
flaw0 scan --target all
```

## flaw0 能检测到哪些问题

### 代码漏洞（12 种以上类型）

1. **命令注入**
   - 使用未经清理的输入调用 `exec()`
   - 使用用户输入构建 Shell 命令

2. **代码注入**
   - 使用 `eval()`
   - 使用字符串创建 `Function()` 对象

3. **SQL 注入**
   - 在 SQL 查询中拼接字符串
   - 使用未参数化的查询

4. **跨站脚本攻击（XSS）**
   - 使用 `innerHTML` 赋值
   - 使用 `dangerouslySetInnerHTML`

5. **路径遍历**
   - 对文件路径的操作未经验证
   - 使用用户输入调用 `readFile()`

6. **硬编码的秘密信息**
   - 源代码中的 API 密钥
   - 密码和令牌
   - AWS 凭据

7. **弱加密**
   - 使用 MD5 和 SHA1 加密算法
   - 使用弱哈希算法

8. **不安全的随机数生成**
   - 在安全操作中使用 `Math.random()`
   - 生成的令牌可预测

9. **不安全的反序列化**
   - 未经验证地使用 `JSON.parse()`
   - 未经验证的输入解析

10. **缺乏身份验证**
    - API 端点没有身份验证中间件
    - 路由未受保护

### 依赖项问题

1. **已知的 CVE（安全漏洞）** - 来自 CVE 数据库的漏洞
2. **过时的包** - 有安全更新可用的包
3. **恶意包** - 已知的恶意软件或可疑包
4. **重复的依赖项** - 依赖项树过于庞大

## 理解扫描结果

### 漏洞评分

扫描结果会附带一个 **漏洞评分**——评分越低表示安全性越好：

- **flaw 0** 🎯 - 完美！未检测到任何问题
- **flaw 1-3** 🟡 - 轻微问题
- **flaw 4-10** 🟠 - 需要关注
- **flaw 10+** 🔴 - 严重问题

### 评分计算方式

每个问题的严重程度会被赋予相应的分数：
- **严重**：3 分
- **较高**：2 分
- **中等**：1 分
- **较低**：0.5 分

**总漏洞评分** = 所有问题分数之和（四舍五入）

### 示例输出

#### 代码干净（flaw 0）

```
🔍 flaw0 Security Scan Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Result: flaw 0
✅ Status: SECURE

✓ No security issues detected!
✓ All checks passed

Great job! 🎉
```

#### 检测到的问题（flaw 12）

```
🔍 flaw0 Security Scan Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Result: flaw 12
⚠️  Status: ISSUES FOUND

Code Flaws: 5
├─ 🔴 Critical: 2
├─ 🟠 High: 1
├─ 🟡 Medium: 2
└─ ⚪ Low: 0

Dependency Flaws: 7
├─ 🔴 Critical CVEs: 3
├─ 🟠 High CVEs: 2
├─ 🟡 Medium: 2
└─ ⚪ Low: 0

Detailed Report:
─────────────────────────────────

1. [CRITICAL] Command Injection
   Location: src/executor.js:78
   Code: `exec(\`ls ${userInput}\`)`
   Description: Unsanitized exec() call
   → Fix: Use execFile() or validate input
   🤖 AI Confidence: high
   💡 AI Suggestion: Replace exec() with execFile()
      and validate input against whitelist

2. [HIGH] Hardcoded API Key
   Location: config/api.js:5
   Code: `const API_KEY = "sk-1234..."`
   Description: API key exposed in source code
   → Fix: Use process.env.API_KEY

3. [CRITICAL] CVE-2024-12345 in lodash@4.17.19
   Package: lodash@4.17.19
   Description: Prototype pollution vulnerability
   → Fix: npm install lodash@4.17.21

...
```

## 基于 AI 的分析

flaw0 利用 OpenClaw 的 AI 模型进行智能代码审查：

### 可用的 AI 模型

#### claude-sonnet-4-5（默认模型）
- 速度和准确性平衡
- 适用于大多数场景
- 减少误报的效果较好

```bash
flaw0 scan --model claude-sonnet-4-5
```

#### claude-opus-4-6
- 分析最为彻底
- 对代码上下文的理解最深入
- 扫描速度较慢，但准确性最高

```bash
flaw0 scan --model claude-opus-4-6
```

#### claude-haiku-4-5
- 扫描速度最快
- 适合快速检查
- 适用于持续集成/持续部署（CI/CD）流程

### AI 功能

- **上下文感知分析** - 理解代码流程和上下文
- **减少误报** - 过滤非安全问题
- **置信度评分** - 评估检测结果的可靠性
- **修复建议** - 提供具体的修复步骤

## 配置

### 创建配置文件

```bash
flaw0 init
```

这将生成一个 `.flaw0rc.json` 文件：

```json
{
  "severity": {
    "failOn": "high",
    "ignore": ["low"]
  },
  "targets": {
    "code": true,
    "dependencies": true,
    "devDependencies": false
  },
  "exclude": [
    "node_modules/**",
    "test/**",
    "*.test.js"
  ],
  "model": "claude-sonnet-4-5",
  "maxFlawScore": 0
}
```

### 配置选项

- **severity.failOn** - 在达到此严重程度或更高级别时退出程序
- **severity.ignore** - 跳过这些严重程度的问题
- **targets** - 需要扫描的内容（代码、依赖项）
- **exclude** - 需要忽略的文件模式
- **model** - 使用的 AI 模型
- **maxFlawScore** - 可接受的最高漏洞评分

## 集成到持续集成/持续部署（CI/CD）流程中

### GitHub Actions

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  flaw0:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3

      - name: Install flaw0
        run: npm install -g flaw0

      - name: Run security scan
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: flaw0 audit

      - name: Check flaw score
        run: |
          SCORE=$(flaw0 audit --json | jq '.flawScore')
          if [ "$SCORE" -gt 0 ]; then
            echo "❌ Flaws detected: flaw $SCORE"
            exit 1
          fi
          echo "✅ No flaws: flaw 0"
```

### 提交代码前的钩子

```bash
#!/bin/bash
echo "🔍 Running flaw0 scan..."
flaw0 scan

if [ $? -ne 0 ]; then
  echo "❌ Flaws detected! Commit blocked."
  exit 1
fi
```

## 示例

### 在安装技能之前进行扫描

```bash
# Download a skill to review
git clone https://github.com/user/some-skill.git /tmp/some-skill

# Scan it
flaw0 scan /tmp/some-skill

# If flaw 0, safe to install
# If flaw > 0, review issues first
```

### 审计您的 OpenClaw 技能

```bash
# Scan all installed skills
flaw0 scan --target skills

# Example output:
# ✓ clawdex - flaw 0
# ✓ database-helper - flaw 0
# ⚠ crypto-bot - flaw 3
# ✓ git-assistant - flaw 0
# Overall: flaw 3
```

### 安装后检查依赖项

```bash
# After installing new packages
npm install some-package

# Check for vulnerabilities
flaw0 deps
```

### 对整个项目进行安全审计

```bash
# Comprehensive security check
flaw0 audit --output security-report.json

# Review the report
cat security-report.json | jq '.flawScore'
```

## 程序化使用 flaw0

您可以在自己的工具中编程方式使用 flaw0：

```javascript
const Flaw0 = require('flaw0');

const scanner = new Flaw0({
  target: './src',
  model: 'claude-sonnet-4-5'
});

// Run full scan
const results = await scanner.scan();

console.log(`Flaw Score: ${results.flawScore}`);

if (results.flawScore === 0) {
  console.log('✅ No flaws detected!');
} else {
  results.codeFlaws.forEach(flaw => {
    console.log(`[${flaw.severity}] ${flaw.name}`);
    console.log(`  Location: ${flaw.file}:${flaw.line}`);
    console.log(`  Fix: ${flaw.fix}`);
  });
}
```

## 工作原理

1. **模式匹配** - 基于正则表达式快速检测常见漏洞
2. **AI 分析** - Claude AI 在上下文中审查每个问题
3. **误报过滤** - AI 识别并排除非安全问题
4. **依赖项检查** - 与 npm 审计工具和 CVE 数据库集成
5. **评分** - 计算漏洞总分
6. **生成报告** - 生成详细且可操作的报告

## 实现零缺陷的建议

1. **优先修复严重问题** - 这些问题对安全性的影响最大
2. **更新依赖项** - 及时修复已知的 CVE
3. **使用参数化查询** - 防止 SQL 注入
4. **验证所有输入** - 防止注入攻击
5. **使用环境变量** - 避免硬编码秘密信息
6. **添加安全头部** - 使用 helmet.js
7. **实施身份验证** - 保护所有 API 端点
8. **使用强加密算法** - 优先选择 SHA-256 或更高级的加密算法
9. **清理输出** - 防止 XSS 攻击
10. **参考 AI 建议** - 根据建议进行修复

## 与其他工具的比较

| 功能 | flaw0 | npm audit | Snyk | ESLint Security |
|---------|-------|-----------|------|-----------------|
| 依赖项的 CVE 检查** | ✅ | ✅ | ✅ | ❌ |
| 基于 AI 的代码分析** | ✅ | ❌ | ❌ | ❌ |
| 适用于 OpenClaw 的特性** | ✅ | ❌ | ❌ | ❌ |
| 上下文感知分析** | ✅ | ❌ | ⚠️ | ⚠️ |
| 减少误报** | ✅ | ❌ | ⚠️ | ❌ |
| 提供修复建议** | ✅ | ⚠️ | ✅ | ⚠️ |

## 系统要求

- **Node.js**：版本 14 及以上
- **API 密钥**：用于 AI 分析的 Anthropic API 密钥
- **npm**：用于检查依赖项

### 设置 API 密钥

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

从以下链接获取您的 API 密钥：https://console.anthropic.com/

## 故障排除

### “未找到 API 密钥”

```bash
export ANTHROPIC_API_KEY='sk-...'
# Or add to ~/.bashrc or ~/.zshrc
```

### “npm audit 失败”

请确保您拥有有效的 `package.json` 文件：

```bash
npm init -y
npm install
```

### 超过 API 使用频率限制

如果遇到 API 使用频率限制：
1. 使用 `haiku` 模型：`--model haiku`
2. 扫描较小的代码片段
3. 等待一段时间后重试

## 支持

- **文档**：请参阅 USAGE.md 以获取详细指南
- **示例**：查看 examples/ 目录
- **问题报告**：在 GitHub 仓库中报告问题
- **演示**：运行 `./demo.sh` 进行交互式演示

## 关于 flaw0

**flaw0** 帮助 OpenClaw 社区实现代码的安全性，消除所有漏洞。

- 由 OpenClaw 和 Claude AI 构建
- 遵循行业标准的安全实践
- 随着新漏洞的出现持续更新
- 采用 MIT 许可证，代码开源

## 贡献方式

欢迎贡献！可以参与以下方面的开发：
- 新的漏洞检测规则
- 新的 AI 模型
- 对 Python/Go 的支持
- 开发 Web 管理面板
- 定制规则引擎

## 许可证

MIT 许可证 - 详情请参阅 LICENSE 文件

---

**目标：让每个人都能实现零缺陷（flaw 0）！🎯**

**请记住**：安全性不是一次性检查的结果。定期运行 flaw0 以保持代码的零缺陷状态！