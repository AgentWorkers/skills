---
name: openclaw-marshal-pro
description: "全面合规性与政策执行套件：用于定义安全策略、审核合规性、自动执行违规行为、隔离不符合规定的技能（即功能或模块）、生成运行时钩子（runtime hooks），以及应用合规性模板。该套件包含 openclaw-marshal（免费版本）的所有功能，并具备自动化执行能力。"
user-invocable: true
metadata: {"openclaw":{"emoji":"📋","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Marshal Pro

这是一个全面合规性和政策执行工具包。它包含了openclaw-marshal（免费版本）的所有功能，并增加了额外的强制执行机制：自动隔离不符合规定的技能、生成运行时钩子、应用合规性模板以及执行全自动的保护扫描。

**免费版本**仅提供警报功能；**Pro版本**则提供了更强大的功能，包括强制隔离违规技能、防御措施等。

## 命令

### 初始化策略

创建一个默认的安全策略文件（`.marshal-policy.json`），并设置合理的默认值。

```bash
python3 {baseDir}/scripts/marshal.py policy --init --workspace /path/to/workspace
```

### 显示策略

显示当前生效的策略。

```bash
python3 {baseDir}/scripts/marshal.py policy --show --workspace /path/to/workspace
```

### 策略概览

快速查看已加载的策略规则。

```bash
python3 {baseDir}/scripts/marshal.py policy --workspace /path/to/workspace
```

### 全面合规性审计

根据当前策略检查所有已安装的技能和工作区配置。生成合规性评分、违规情况以及改进建议。

```bash
python3 {baseDir}/scripts/marshal.py audit --workspace /path/to/workspace
```

### 检查特定技能

针对单个技能检查其是否符合策略要求。报告每条规则的检查结果（通过/失败）及相应的修复建议。

```bash
python3 {baseDir}/scripts/marshal.py check openclaw-warden --workspace /path/to/workspace
```

### 生成合规性报告

生成格式化的合规性报告，可直接用于审计文档。

```bash
python3 {baseDir}/scripts/marshal.py report --workspace /path/to/workspace
```

### 快速状态

提供简短的状态信息：策略是否已加载、合规性评分、严重违规数量、被隔离的技能数量。

```bash
python3 {baseDir}/scripts/marshal.py status --workspace /path/to/workspace
```

### 强制执行策略（Pro版本）

执行策略：扫描所有技能，自动隔离存在严重违规的技能，并为中等违规提供修复建议。

```bash
python3 {baseDir}/scripts/marshal.py enforce --workspace /path/to/workspace
```

### 隔离技能（Pro版本）

通过将违规技能的目录前缀添加“.quarantined-”来隔离该技能，使其对所有代理工具不可见。

```bash
python3 {baseDir}/scripts/marshal.py quarantine bad-skill --workspace /path/to/workspace
```

### 解除技能隔离（Pro版本）

在调查后恢复被隔离的技能。

```bash
python3 {baseDir}/scripts/marshal.py unquarantine bad-skill --workspace /path/to/workspace
```

### 生成运行时钩子（Pro版本）

生成用于在运行时执行策略的Claude Code钩子配置。包括Bash命令的允许/阻止列表（PreToolUse钩子）以及个人身份信息（PII）模式扫描的Write钩子。

```bash
python3 {baseDir}/scripts/marshal.py hooks --workspace /path/to/workspace
```

### 合规性模板（Pro版本）

列出或应用预先构建的合规性模板：通用模板（balanced）、企业级模板（strict）或基础模板（minimal）。

```bash
# List available templates
python3 {baseDir}/scripts/marshal.py templates --list --workspace /path/to/workspace

# Apply a template
python3 {baseDir}/scripts/marshal.py templates --apply enterprise --workspace /path/to/workspace
```

### 全面保护扫描（Pro版本）

推荐在会话启动时执行此操作：加载策略、检查所有技能、处理违规情况、隔离严重违规者，并生成总结报告。

```bash
python3 {baseDir}/scripts/marshal.py protect --workspace /path/to/workspace
```

## 工作区自动检测

如果省略了`--workspace`参数，脚本会尝试以下路径来查找工作区配置：
1. `OPENCLAW_WORKSPACE`环境变量
2. 当前目录（如果存在AGENTS.md文件）
3. `~/.openclaw/workspace`（默认路径）

## 检查内容

| 类别 | 检查项目 | 严重程度 |
|----------|--------|----------|
| **命令安全** | 危险的命令模式（如eval、exec、pipe-to-shell、rm -rf /） | 严重（CRITICAL） |
| **命令策略** | 策略中禁止的命令 | 高风险（HIGH/MEDIUM） |
| **网络策略** | 允许/禁止访问的域名、可疑的顶级域名（TLD） | 严重/高风险（CRITICAL/HIGH） |
| **数据管理** | 是否安装了秘密信息扫描工具、是否配置了个人身份信息扫描功能 | 高风险/中等风险（HIGH/MEDIUM） |
| **工作区管理** | .gitignore文件的存在、审计日志（ledger）的使用、技能的签名功能（signet） | 高风险/中等风险（HIGH/MEDIUM） |
| **配置设置** | 是否启用了调试模式或详细日志记录 | 低风险（LOW） |

## 策略格式

`.marshal-policy.json`文件定义了所有规则：
- `commands.allow`：允许执行的二进制文件
- `commands.block`：禁止执行的命令模式
- `commands.review`：需要人工审核的命令
- `network.allow_domains`：允许访问的域名
- `network.block_domains`：禁止访问的域名
- `network.block_patterns`：通配符域名屏蔽规则（例如`.tk`）
- `data_handling.pii_scan`：是否要求对个人身份信息进行扫描
- `data_handling.secret_scan`：是否要求对敏感数据进行扫描
- `workspace.require-gitignore`：是否要求使用.gitignore文件
- `workspace.require_audit_trail`：是否要求记录审计日志
- `workspace.require_skill_signing`：是否要求对技能进行签名验证

## 出错代码

- `0`：符合策略要求，无问题
- `1`：需要人工审核（发现中等/高风险违规）
- `2`：检测到严重违规

## 无外部依赖

仅依赖Python标准库，无需安装额外的库（如pip），也不进行网络请求。所有操作均在本地完成。

## 跨平台兼容性

该工具可与OpenClaw、Claude Code、Cursor以及任何遵循Agent Skills规范的工具配合使用。