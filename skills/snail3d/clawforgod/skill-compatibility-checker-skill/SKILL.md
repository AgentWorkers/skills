---
name: skill-compatibility-checker
description: 预安装检查工具：在您安装某个技能（skill）之前，该工具会检测是否存在冲突、系统需求不匹配、依赖项缺失以及安全问题。它会分析技能的相关配置文件（manifests），检查技能名称或命令行接口（CLI）/端口是否与现有技能重复，验证操作系统（OS）、架构（architecture）及 Node.js 版本之间的兼容性，确认是否缺少必要的 CLI 工具和 API 密钥，并执行自动化的安全扫描。根据扫描结果，该工具会返回“GO”（表示可以安装）、“CAUTION”（表示需要特别注意）或“BLOCKED”（表示无法安装）的提示，并提供详细的修复步骤。
---

# 技能兼容性检查器

在安装技能之前，请先对其进行验证。该工具会分析技能的兼容性、冲突情况、依赖关系以及安全风险。

## 快速入门

```bash
# Check a local skill directory
skill-compatibility-checker ~/clawd/some-skill

# Get JSON output for programmatic use
skill-compatibility-checker ~/clawd/some-skill --output json
```

## 检查内容

### 1. 冲突检测

- **名称冲突**：是否存在已安装的具有相同名称的技能？
- **CLI命令冲突**：尝试安装的命令是否已存在？
- **端口冲突**：使用的端口是否已被占用？
- **配置冲突**：该技能是否会修改现有技能的配置文件？

### 2. 系统要求

验证您的系统是否满足该技能的运行要求：

- **操作系统兼容性**：macOS、Linux 还是 Windows？
- **架构**：arm64 还是 x86_64？
- **Node.js 版本**：您的 Node.js 是否满足最低要求？

信息来源：
- SKILL.md 文件的前言和正文内容
- package.json 文件中的 `engines.node` 字段

### 3. 依赖关系

检查是否缺少以下依赖项：

- **CLI 工具**：ffmpeg、python、java、docker 等
  - 列出缺失的依赖项
  - 提供安装命令（例如：`brew install <tool>`）

- **API 密钥**：Groq、ElevenLabs、OpenAI、Stripe、Twilio 等
  - 检查 `TOOLS.md` 文件和系统环境变量
  - 列出未配置的 API 密钥

- **Clawdbot 版本**：该技能是否需要 Clawdbot X.Y.Z 或更高版本？

- **npm 包**：从 package.json 文件中获取依赖关系信息

### 4. 安全扫描

（如果已安装 `security-scanner` 工具）会运行安全扫描：

- 检测代码执行中的漏洞（如 `eval`、`exec`、`dynamic require` 等操作）
- 识别潜在的凭证窃取风险
- 警告对未知域名的网络请求
- 检测混淆或压缩的代码
- 返回风险等级：**安全** / **警告** / **危险**

## 安装准备情况

### 🟢 可以安装
**已准备好安装。未发现任何阻碍安装的问题。**

- 系统要求均满足
- 未检测到冲突
- 所有依赖项均已安装
- 安全扫描结果正常（安全）

### 🟡 谨慎操作
**请在安装前仔细检查问题。**

- 系统要求已满足，但存在一些警告
- 检测到冲突，但可以解决
- 一些依赖项缺失（如 CLI 工具、API 密钥）
- 安全扫描结果显示“警告”等级
- 为每个问题提供了解决方法

### 🔴 无法安装
**请勿安装。**

- 系统要求不满足（操作系统、架构或 Node.js 版本不正确）
- 技能名称与已安装的技能重复
- 安全扫描发现严重安全风险
- 该技能无法在此系统上安装

## 使用示例

### 检查技能目录

```bash
$ skill-compatibility-checker ~/clawd/my-skill

╔════════════════════════════════════════════════════════════════════════════╗
║                    SKILL COMPATIBILITY CHECKER REPORT                      ║
╚════════════════════════════════════════════════════════════════════════════╝

Skill: my-skill
Path:  /Users/ericwoodard/clawd/my-skill
Date:  2026-01-29T15:30:00.000Z

┌─ INSTALLATION READINESS ─────────────────────────────────────────────────┐
│ ✅ GO - Safe to install
│
└────────────────────────────────────────────────────────────────────────────┘

┌─ SYSTEM REQUIREMENTS ────────────────────────────────────────────────────┐
│ Your System: darwin / arm64 / Node 25.4.0
│
│ System requirements met ✅
└────────────────────────────────────────────────────────────────────────────┘

┌─ RECOMMENDATION ─────────────────────────────────────────────────────────┐
│ ✅ Ready to install. No blocking issues detected.
│
│ Next step: npm install && clawdbot skill install
└────────────────────────────────────────────────────────────────────────────┘
```

### 显示警告（需谨慎操作）

```bash
$ skill-compatibility-checker ~/clawd/another-skill

┌─ INSTALLATION READINESS ─────────────────────────────────────────────────┐
│ ⚠️  CAUTION - Review issues before installation
│
└────────────────────────────────────────────────────────────────────────────┘

┌─ DEPENDENCIES ───────────────────────────────────────────────────────────┐
│ Missing CLI Tools:
│ ❌ ffmpeg
│    Install: brew install ffmpeg
│
│ Missing API Keys/Tokens:
│ ⚠️  groq - configure in TOOLS.md or environment
│ ⚠️  elevenlabs - configure in TOOLS.md or environment
└────────────────────────────────────────────────────────────────────────────┘

┌─ RECOMMENDATION ─────────────────────────────────────────────────────────┐
│ ⚠️  Proceed with caution. Review all issues above.
│
│ Actions before installation:
│ 1. Install missing CLI tools (see above)
│ 2. Configure missing API keys in TOOLS.md
│ 3. Review security findings and audit code if needed
└────────────────────────────────────────────────────────────────────────────┘
```

### 用于程序化处理的 JSON 输出

```bash
$ skill-compatibility-checker ~/clawd/my-skill --output json

{
  "skill": {
    "name": "my-skill",
    "path": "/Users/ericwoodard/clawd/my-skill",
    "description": "Does something useful"
  },
  "readiness": "GO",
  "timestamp": "2026-01-29T15:30:00.000Z",
  "system": {
    "platform": "darwin",
    "arch": "arm64",
    "nodeVersion": "25.4.0",
    "osVersion": "26.2"
  },
  "conflicts": {
    "conflicts": [],
    "warnings": []
  },
  "systemRequirements": {
    "issues": [],
    "warnings": []
  },
  "dependencies": {
    "missingCLITools": [],
    "missingApiKeys": [],
    "clawdbotVersionRequired": null,
    "warnings": []
  },
  "security": {
    "riskLevel": "SAFE",
    "findings": [],
    "message": ""
  },
  "recommendation": "Ready to install. No blocking issues detected."
}
```

## 工作原理

### 1. 确定技能路径
- 本地路径：`~/clawd/my-skill` 或 `/full/path/to/skill`
- 通过 ClawdHub 查询：`clawdhub:skill-name`（未来版本）

### 2. 解析技能元数据
- 读取 SKILL.md 文件的前言部分（包括技能名称、描述和系统要求）
- 读取 SKILL.md 和 README.md 的内容
- 解析 package.json 文件中的 `bin`、`engines` 和 `dependencies` 部分

### 3. 检查冲突
- 将技能名称与 `~/clawd/` 目录下已安装的所有技能进行比较
- 检查 package.json 中定义的命令是否已存在于系统的 PATH 环境变量中
- 检查技能是否使用了特定的端口

### 4. 验证系统要求
- 将所需的操作系统与 `process.platform`（darwin、linux、win32）进行比较
- 将所需的架构与 `process.arch`（arm64、x86）进行比较
- 将所需的 Node.js 版本与当前系统上的 Node.js 版本进行比较
- 从 SKILL.md 和 package.json 的 `engines` 字段中获取相关信息

### 5. 检查依赖关系
- 查找文档中提到的常见 CLI 工具（如 ffmpeg、python、java 等）
- 确认这些工具是否已存在于系统的 PATH 环境变量中
- 从 SKILL.md 和 README.md 中获取 API 密钥的相关信息
- 检查 `TOOLS.md` 文件和系统环境变量（`process.env`）中是否配置了相应的密钥
- 从 package.json 中获取 npm 依赖项信息

### 6. 运行安全扫描
- 如果安装了 `security-scanner` 工具，会调用它进行安全扫描
- 将技能路径传递给扫描工具
- 获取风险等级和扫描结果
- 报告安全评估结果

### 7. 生成报告
- 判断是否可以安装（安全 / 警慎操作 / 无法安装）
- 以文本或 JSON 格式生成报告（便于人类阅读或程序化处理）
- 提供可操作的修复步骤

## 返回代码

- **0**：可以安装
- **1**：需要先检查并修复问题
- **2**：无法在此系统上安装

该工具支持脚本化地处理兼容性检查：

```bash
skill-compatibility-checker ~/clawd/my-skill
if [ $? -eq 0 ]; then
  echo "Installing..."
  npm install && clawdbot skill install
elif [ $? -eq 1 ]; then
  echo "Review issues and try again"
  exit 1
else
  echo "Cannot install on this system"
  exit 2
fi
```

## 系统要求

- **Node.js** 版本 ≥ 14.0.0
- **security-scanner-skill**（可选，用于安全扫描）
- **CLI 工具**（可选，如果技能文档中提到了这些工具，则需要安装）

## 与其他技能/子代理的配合使用

该技能兼容性检查器可以被其他工具调用：

```bash
# From command line
skill-compatibility-checker ~/clawd/some-skill --output json > report.json

# From Node.js
const checker = require('./scripts/checker.js');
const results = checker.checkSystemRequirements('./skill-path');
```

## 配置

### 环境变量

该工具会自动读取以下环境变量以获取 API 密钥：

- `GROQ_API_KEY`
- `ELEVENLABS_API_KEY`
- `OPENAI_API_KEY`
- `STRIPE_API_KEY`
- `TWILIO_AUTH_TOKEN`
- 等

### TOOLS.md 格式

该工具会从 `~/clawd/TOOLS.md` 文件中读取 API 密钥的相关配置：

```markdown
## API Keys & Services

- **Groq API:** `gsk_...` (Whisper audio transcription)
- **ElevenLabs API:** Configured (sk_...)
```

## 限制

- 目前尚未实现通过 ClawdHub 查询技能的功能（使用本地路径）
- 端口冲突检测仅提供参考信息（不实际测试端口的使用情况）
- API 密钥的检测基于模式匹配（可能会遗漏某些情况）
- CLI 工具的检测基于通用名称（如 ffmpeg、python 等）

## 高级用法：程序化调用

您可以在自己的代码中调用该工具：

```javascript
const {
  checkConflicts,
  checkSystemRequirements,
  checkDependencies,
  runSecurityScan,
  determineReadiness,
} = require('./scripts/checker.js');

// Run a single check
const sysReqs = checkSystemRequirements('./my-skill');
console.log(sysReqs);
// { issues: [], warnings: [] }

// Check readiness
const readiness = determineReadiness(results);
// 'GO' | 'CAUTION' | 'BLOCKED'
```

## 提示

1. **在安装任何技能之前**，请先运行该检查工具：
   ```bash
   skill-compatibility-checker ~/clawd/new-skill
   ```

2. **在持续集成/持续部署（CI/CD）流程中**，可以使用 JSON 格式的报告和返回代码：
   ```bash
   skill-compatibility-checker ~/clawd/new-skill --output json || exit $?
   ```

3. **定期检查**：如果更新了 `TOOLS.md` 文件，请定期运行该检查工具：
   ```bash
   for skill in ~/clawd/*-skill; do
     skill-compatibility-checker "$skill" || true
   done
   ```

4. **解决警告**：这些警告都是可以解决的：
   - 安装缺失的 CLI 工具：`brew install <tool>`
   - 在 `TOOLS.md` 中配置 API 密钥
   - 查看安全扫描结果并联系维护者

5. **不要强行安装被标记为“无法安装”的技能**——系统不兼容的问题可能导致运行错误。

## 相关资源

- **security-scanner-skill**：用于检测恶意代码和漏洞的静态代码分析工具
- **TOOLS.md**：用于存储 API 密钥的配置文件
- **SKILL.md**：技能元数据的格式规范