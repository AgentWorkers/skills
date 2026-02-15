---
name: security-scanner
description: 一款全面的功能与代码漏洞扫描工具，能够检测代码执行漏洞（如 `eval`, `exec`, `dynamicRequire` 等）、凭证窃取行为、对可疑域名的网络请求、代码混淆等问题。该工具提供风险评估结果（分为“安全”/“谨慎”/“危险”三个等级），并附有详细的发现报告及可操作的改进建议。在安装不受信任的功能或审查代码的安全性时，建议使用该工具。
---

# 安全扫描器技能

这是一个全面的静态分析工具，用于检测代码和技能中的漏洞、恶意软件模式以及安全问题。

## 概述

安全扫描器会对以下内容进行深度静态分析：
- **代码文件**（.js、.ts、.jsx、.tsx、.py、.go、.java、.rb、.php、.sh）
- **技能目录**（递归扫描所有代码）
- **内联代码片段**

它会标记危险的模式、可疑的行为和混淆代码，并提供可操作的建议。

## 快速入门

```bash
# Scan a skill directory
security-scanner ./my-skill/

# Scan a single file
security-scanner ./package.js

# Scan code snippet
security-scanner --code "eval(userInput)"

# Get JSON output
security-scanner ./skill --output json

# See suggested fixes
security-scanner ./skill --fix
```

## 风险等级与建议

### 🔴 危险 → 拒绝安装
**结论：** 不要安装此代码。

检测到的模式：
- `eval()` - 任意代码执行
- `exec()` - 命令执行
- 带有变量路径的动态 `require()`  
- 代码注入漏洞的迹象

**操作：** 要求维护者审查源代码或完全拒绝安装。

### 🟡 警告 → 隔离
**结论：** 安装前请先审查。

检测到的模式：
- `child_process` 调用（启动外部命令）
- 访问环境变量（可能导致秘密信息泄露）
- 对未知域的网络调用
- 混淆/压缩的代码
- 低级别的套接字访问（net、dgram）
- 编码字符串（十六进制/Unicode转义）

**操作：** 检查发现的问题，向维护者咨询可疑模式，谨慎安装。

### 🟢 安全 → 可以安装
**结论：** 未检测到明显的恶意模式。

**操作：** 安装是安全的。但仍建议遵循标准的安全实践（保持更新，监控权限设置）。

## 它能检测什么

### 代码执行（最高风险）
- ✗ `eval()`
- ✗ `exec()`
- ✗ 带有变量路径的动态 `require()`
- ⚠ `child_process` 模块的导入

### 凭据窃取
- ✗ `process.env.SECRET`、`process.env.API_KEY` 等
- ⚠ 动态访问环境变量 `process.env[varName]`
- ⚠ 在敏感系统文件（`/etc/`、`~/`）上使用 `fs.readFileSync()`

### 网络/数据泄露
- ⚠ 对未知外部域的网络调用（通过 `fetch`、`http.get` 等）
- ⚠ HTTP/HTTPS 模块的导入（可能涉及网络调用）
- ⚠ 低级别的套接字访问（`net`、`dgram`）

### 混淆代码（危险信号）
- ⚠ 压缩代码（符号密度异常高，行非常短）
- ⚠ 十六进制编码的字符串（`\x41\x42\x43`）
- ⚠ Unicode 编码的字符串（`\u0041\u0042`）

**为什么这很重要：** 混淆代码会隐藏恶意逻辑。合法的库通常不需要进行混淆。

## 输出格式

### 文本格式（人类可读，默认）

```
=== Security Scanner Report ===

Target: ./my-skill
Files Scanned: 5
Findings: 2

Risk Level: CAUTION

Detailed Findings:

  scripts/handler.js
    Line 42: [CAUTION] child_process allows spawning external commands
      Code: require('child_process')
      Context: const spawn = require('child_process').spawn;

  src/api.js
    Line 18: [CAUTION] Network call to external domain
      Code: fetch('https://api.example.com/verify')
      Context: return fetch('https://api.example.com/verify', {...})

Recommendation:
  Action: QUARANTINE
  Reason: Code contains potentially suspicious patterns requiring review
  Details: Review findings before installation. Consider asking maintainer about specific suspicious patterns.

Suggested Fixes:
  • Replace dynamic require with static import
    File: scripts/handler.js:42
    Suggestion: Use static imports or a whitelist of allowed modules
    Difficulty: MEDIUM
```

### JSON 格式（程序化）

```bash
scanner --output json
```

返回结构化的 JSON 数据，包含：
- `target`：被扫描的路径/名称
- `timestamp`：ISO 时间戳
- `riskLevel`：安全 | 警告 | 危险
- `findings[]`：检测到的问题列表及其行号
- `scannedFiles[]`：分析的文件列表
- `recommendation`：建议的操作及原因
- `fixes[]`：（如果使用了 `--fix` 选项）建议的代码修改

## 在您的工作流程中使用

### 安装前检查

```bash
# Before installing a new skill
security-scanner ~/downloads/mystery-skill/

# If DANGEROUS → Don't install
# If CAUTION → Review output, ask author
# If SAFE → Good to go
```

### 代码审查

```bash
# Check your own skill for issues
security-scanner ./my-skill/ --output json > security-report.json

# Fix issues
security-scanner ./my-skill/ --fix
```

### 自动化 CI/CD 流程

```bash
# In your build pipeline - fail if DANGEROUS detected
security-scanner ./src/ --output json
if [ $? -eq 2 ]; then
  echo "Security violations found"
  exit 1
fi
```

### 通过子代理调用扫描器

```bash
# From a sub-agent or CLI
/Users/ericwoodard/clawd/security-scanner-skill/scripts/scanner.js ~/clawd/some-skill/
```

## 常见问题及解读方法

### eval() / exec()
**问题：** “eval() 允许任意代码执行”

**解读：** 代码可以在运行时执行任意 JavaScript 代码。极其危险。

**应对措施：**
- ❌ 如果是恶意代码：拒绝安装。
- ⚠️ 如果是合法代码：询问作者为何需要使用 `eval()`（通常有更安全的方法）。

### child_process 模块的导入
**问题：** “child_process` 可以启动外部命令”

**解读：** 代码可以执行系统命令。虽然构建工具会合法使用它，但恶意软件也可能利用它。

**应对措施：**
- 检查其使用位置。
- 它是否执行用户输入？→ 危险。
- 它是否执行硬编码的命令？→ 可能安全，但需要审查。

### process.env.API_KEY
**问题：** “访问敏感的环境变量”

**解读：** 代码从环境中读取密钥。这是常见的操作，但需要验证：
- 是否有文档说明？
- 密钥是否确实用于预期目的？
- 是否有可能被泄露？

**应对措施：**
- 对于需要 API 密钥的合法技能来说这是正常的操作。
- 检查 API 调用是否指向预期的域名。

### 压缩代码
**问题：** “代码似乎被压缩或混淆了”

**解读：** 源代码被有意隐藏。为什么？

**应对措施：**
- ❌ 单文件技能被压缩 → 可疑，请求查看源代码。
- ✅ 同时包含 `.js` 和 `.min.js` 的 Node 模块 → 是标准做法。
- ⚠️ 十六进制编码的字符串 → 请求进行反混淆处理。

### 对未知域的 `fetch` 调用
**问题：** “对未知域进行了网络调用”

**解读：** 代码调用了某个外部 API。这是预期的行为吗？

**应对措施：**
- ✅ `fetch('https://api.github.com/...')` → 正常。
- ❌ `fetch('https://malware-collection.ru/...')` → 危险。
- ⚠️ `fetch(userProvidedUrl)` → 危险（可能打开恶意链接）。

## 如何通过子代理使用扫描器

从子代理中调用扫描器：

```bash
# Run scan
/Users/ericwoodard/clawd/security-scanner-skill/scripts/scanner.js <skill-path>

# Check exit code
if [ $? -eq 2 ]; then
  # DANGEROUS - handle rejection
elif [ $? -eq 1 ]; then
  # CAUTION - handle quarantine
else
  # SAFE
fi

# Or parse JSON output
result=$(/Users/ericwoodard/clawd/security-scanner-skill/scripts/scanner.js <path> --output json)
riskLevel=$(echo "$result" | jq -r '.riskLevel')
```

## 限制

⚠️ **仅进行静态分析** - 不会执行代码，因此：
- 运行时的技巧可能无法被检测到。
- 运行时解码的混淆字符串不会被标记。
- 不会进行复杂的控制流分析。

**仍然安全：** 除非扫描器显示“危险”，否则通常可以放心使用。虽然“警告”等级需要手动审查，但很多情况都是误报。

## 命令

### `security-scanner <path>`
扫描一个文件或目录。

```bash
security-scanner ./my-skill/
security-scanner ./code.js
```

### `security-scanner --code "<snippet>"`
扫描内联代码（无需创建新文件）。

```bash
security-scanner --code "eval(userInput)"
```

### `security-scanner <path> --output json`
以 JSON 格式输出结果，便于程序化处理。

```bash
security-scanner ./skill --output json > report.json
```

### `security-scanner <path> --output text`
以人类可读的文本格式输出结果（默认设置）。

### `security-scanner <path> --fix`
显示建议的代码修改和缓解策略。

```bash
security-scanner ./skill --fix
```

### `security-scanner --help`
显示使用说明。

## 退出代码

- `0` - 安全（未检测到危险模式）
- `1` - 警告（发现可疑模式，需要手动审查）
- `2` - 危险（检测到恶意模式，禁止安装）

## 实现说明

- 通过正则表达式进行模式匹配
- 通过启发式方法检测混淆代码（符号密度、编码方式）
- 精确到行的报告（可以定位问题位置）
- 支持多种语言（.js、.ts、.py、.go、.java、.rb、.php、.sh）
- 自动过滤非代码目录（如 `node_modules`、.git、dist 等）

## 未来改进计划

- 增加语义分析（理解变量数据流）
- 基于签名的检测（已知恶意代码模式）
- 配置审计（异常权限设置、可疑配置）
- 隔离模式（自动移除/注释可疑代码）
- 与恶意软件数据库集成
- 供应链攻击检测（锁定特定版本、校验哈希值）

---

**最后更新时间：** 2025-01-29
**状态：** 已准备好投入生产使用