---
name: openclaw-marshal
user-invocable: true
metadata: {"openclaw":{"emoji":"📋","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Marshal

用于为您的工作空间定义安全策略并审核合规性。检查已安装的技能是否符合命令执行、网络访问和数据处理的规则，并生成可用于审计的合规性报告。

## 重要性

代理工作空间会积累能够执行命令、访问网络和处理数据的技能。如果没有明确的安全策略，就无法判断已安装的技能是否符合组织的要求，也无法确定工作空间本身是否达到了基本的安全标准。

该工具允许您一次性定义安全策略，然后根据该策略对所有内容进行审核。

## 命令

### 初始化策略

创建一个包含合理默认值的默认安全策略文件（`.marshal-policy.json`）。

```bash
python3 {baseDir}/scripts/marshal.py policy --init --workspace /path/to/workspace
```

### 显示策略

显示当前生效的策略。

```bash
python3 {baseDir}/scripts/marshal.py policy --show --workspace /path/to/workspace
```

### 策略概要

快速查看已加载的策略规则。

```bash
python3 {baseDir}/scripts/marshal.py policy --workspace /path/to/workspace
```

### 全面合规性审核

根据当前生效的策略，审核所有已安装的技能和工作空间配置。报告合规性得分、违规情况以及改进建议。

```bash
python3 {baseDir}/scripts/marshal.py audit --workspace /path/to/workspace
```

### 检查特定技能

根据策略检查单个技能。按规则报告是否通过。

```bash
python3 {baseDir}/scripts/marshal.py check openclaw-warden --workspace /path/to/workspace
```

### 生成合规性报告

生成一份格式化好的、可直接用于审计文档的合规性报告。

```bash
python3 {baseDir}/scripts/marshal.py report --workspace /path/to/workspace
```

### 快速状态

一行总结：策略是否已加载、合规性得分以及严重违规的数量。

```bash
python3 {baseDir}/scripts/marshal.py status --workspace /path/to/workspace
```

## 自动检测工作空间

如果省略了 `--workspace` 参数，脚本会尝试：
1. `OPENCLAW_WORKSPACE` 环境变量
2. 当前目录（如果存在 AGENTS.md 文件）
3. `~/.openclaw/workspace`（默认路径）

## 检查内容

| 类别 | 检查项目 | 严重程度 |
|----------|--------|----------|
| **命令安全** | 危险的操作模式（如 eval、exec、pipe-to-shell、rm -rf /） | 严重（CRITICAL） |
| **命令策略** | 策略中禁止的或需要人工审核的命令 | 高/中等（HIGH/MEDIUM） |
| **网络策略** | 允许/禁止的域名列表、可疑的顶级域名（TLD） | 严重/高等（CRITICAL/HIGH） |
| **数据处理** | 是否安装了秘密信息扫描工具、是否配置了个人身份信息（PII）扫描功能 | 高/中等（HIGH/MEDIUM） |
| **工作空间规范** | 是否使用了 `.gitignore` 文件、是否保留了审计记录（ledger）、是否要求技能签名（signet） | 高/中等（HIGH/MEDIUM） |
| **配置** | 是否启用了调试模式或详细日志记录 | 低（LOW） |

## 策略格式

`.marshal-policy.json` 文件定义了所有规则：
- **commands.allow** — 允许执行的二进制文件
- **commands.block** — 被禁止的命令模式
- **commands.review** — 需要人工审核的命令
- **network.allow_domains** — 允许访问的域名
- **network.block_domains** — 被禁止的域名
- **network.block_patterns** — 通配符域名屏蔽规则（例如 `*.tk`）
- **data_handling.pii_scan** — 是否要求对个人身份信息进行扫描
- **data_handling.secret_scan** — 是否要求对敏感数据进行扫描
- **workspace.require-gitignore** — 是否要求使用 `.gitignore` 文件
- **workspace.require_audit_trail** — 是否要求保留审计记录
- **workspace.require_skill_signing** — 是否要求对技能进行签名验证

## 出错代码

- `0` — 合规，无问题
- `1` — 需要人工审核（发现中等/严重问题）
- `2` — 检测到严重违规

## 无需外部依赖

仅依赖 Python 标准库，无需安装其他库（如 pip），也不进行网络调用。所有操作都在本地完成。

## 跨平台兼容性

支持 OpenClaw、Claude Code、Cursor 以及任何遵循代理技能规范的工具。