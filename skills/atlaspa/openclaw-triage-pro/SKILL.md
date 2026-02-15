---
name: openclaw-triage-pro
description: "完整的事件响应套件：包括调查安全漏洞、自动遏制威胁、指导性修复措施、证据导出、事件后的系统加固，以及预先构建的响应方案。该套件能够跨引用所有 OpenClaw 安全工具以实现统一分析。涵盖了 openclaw-triage（免费版本）中的所有功能，并提供了自动化响应机制。"
user-invocable: true
metadata: {"openclaw":{"emoji":"🚨","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Triage Pro

这是一个专为代理工作空间设计的全套事件响应工具。当出现问题时——比如某个技能行为异常、文件被未经解释地修改，或者其他安全工具检测到异常情况——Triage 会调查事件经过、控制威胁、修复损失，并采取措施防止类似事件再次发生。

[openclaw-triage](https://github.com/AtlasPA/openclaw-triage) 提供了所有基础功能（免费），此外还支持自动化威胁控制、引导式修复、证据导出、事件后的系统加固以及预先构建的事件响应脚本。

## 免费命令（包含在内）

### 全面调查

执行全面的事件调查。收集工作空间的状态信息，检查是否存在被入侵的迹象（如最近被修改的关键文件、新出现的技能、异常权限、非工作时间进行的修改、大型文件、隐藏文件等），与 Warden/ledger/signet/sentinel 的数据相互关联，生成事件时间线，并计算事件严重程度（CRITICAL / HIGH / MEDIUM / LOW）。

```bash
python3 {baseDir}/scripts/triage.py investigate --workspace /path/to/workspace
```

### 事件时间线

生成工作空间中所有文件修改的按时间顺序排列的时间线。按小时分组事件，突出显示可疑的突发活动，显示受影响的目录和技能，并在可用情况下与 ledger 数据进行关联。

```bash
python3 {baseDir}/scripts/triage.py timeline --workspace /path/to/workspace
```

可以查看超过默认 24 小时的历史记录：

```bash
python3 {baseDir}/scripts/triage.py timeline --hours 72 --workspace /path/to/workspace
```

### 威胁扩散范围

评估潜在入侵的扩散范围。根据风险等级对所有文件进行分类（关键文件、内存相关文件、技能相关文件、配置文件），检查最近被修改的文件中是否存在凭证泄露的迹象，扫描是否存在数据外泄的 URL，并将威胁范围判断为“受控（CONTAINED）”、“正在扩散（SPREADING）”或“系统性（SYSTEMIC）”。

```bash
python3 {baseDir}/scripts/triage.py scope --workspace /path/to/workspace
```

### 证据收集

在修复之前收集并保存法证证据。对整个工作空间的状态进行快照（包括文件列表及其 SHA-256 哈希值、文件大小、时间戳），复制所有可用的安全工具数据，并生成总结报告。

```bash
python3 {baseDir}/scripts/triage.py evidence --workspace /path/to/workspace
```

将结果保存到自定义的输出目录：

```bash
python3 {baseDir}/scripts/triage.py evidence --output /path/to/evidence/dir --workspace /path/to/workspace
```

### 快速状态概览

提供 Triage 的当前状态概览：最后一次调查的时间戳、当前的威胁等级、威胁控制及修复的历史记录，以及是否已收集到证据。

```bash
python3 {baseDir}/scripts/triage.py status --workspace /path/to/workspace
```

## 高级命令

### 自动化威胁控制

隔离调查中标记的所有技能，锁定关键文件（仅允许读取），并禁用任何可疑的挂载点（hook）。被隔离的技能会被移动到 `.triage/quarantine/` 目录中，可以在修复过程中恢复。

```bash
python3 {baseDir}/scripts/triage.py contain --workspace /path/to/workspace
```

### 引导式修复

从 Warden 的快照中恢复关键文件（如果可用），使用 Signet 重新签署技能的配置，重新记录相关数据，并重建系统基线。该功能会自动与所有 OpenClaw 安全工具集成。

```bash
python3 {baseDir}/scripts/triage.py remediate --workspace /path/to/workspace
```

### 事件报告导出

导出完整的事件报告以供外部审查。报告内容包括事件时间线、威胁范围、收集到的证据以及采取的所有措施。报告格式支持 JSON（便于机器处理）和文本格式（便于人类阅读）。

```bash
python3 {baseDir}/scripts/triage.py export --format text --workspace /path/to/workspace
python3 {baseDir}/scripts/triage.py export --format json --output report.json --workspace /path/to/workspace
```

### 事件后的系统加固

检查已安装的安全工具，建议补充缺失的工具，提出政策调整建议，并提供按优先级排序的修复步骤。

```bash
python3 {baseDir}/scripts/triage.py harden --workspace /path/to/workspace
```

### 事件响应脚本

为常见场景预先构建了详细的事件响应脚本。

```bash
# List available playbooks
python3 {baseDir}/scripts/triage.py playbook --workspace /path/to/workspace

# Run a specific playbook
python3 {baseDir}/scripts/triage.py playbook --scenario skill-compromise --workspace /path/to/workspace
python3 {baseDir}/scripts/triage.py playbook --scenario injection-attack --workspace /path/to/workspace
python3 {baseDir}/scripts/triage.py playbook --scenario credential-leak --workspace /path/to/workspace
python3 {baseDir}/scripts/triage.py playbook --scenario chain-break --workspace /path/to/workspace
```

### 全自动防护扫描（Protect）

执行全自动的防护扫描：调查并控制关键威胁，收集证据，并生成报告。建议在系统启动时自动执行此操作。

```bash
python3 {baseDir}/scripts/triage.py protect --workspace /path/to/workspace
```

## 工作空间自动检测

如果省略了 `--workspace` 参数，脚本会尝试以下路径：
1. `OPENCLAW_WORKSPACE` 环境变量
2. 当前目录（如果存在 AGENTS.md 文件）
3. `~/.openclaw/workspace`（默认路径）

## 数据来源的交叉引用

| 工具            | 数据路径                | Triage 检查的内容                |
|------------------|------------------|---------------------------|
| **Warden**         | `.integrity/manifest.json`      | 基线偏差——自上次已知正常状态以来的文件修改情况 |
| **Ledger**         | `.ledger/chain.jsonl`        | 链条中断、无法解析的条目、可疑的日志记录       |
| **Signet**         | `.signet/manifest.json`      | 被篡改的技能签名——签名后的文件修改情况     |
| **Sentinel**        | `.sentinel/threats.json`      | 已知的威胁和高严重性事件             |

## 事件严重程度等级

| 等级            | 含义                        | 触发条件                        |
|------------------|------------------|---------------------------|
| **CRITICAL**       | 需要立即响应                | 任何关键性安全问题，或存在 3 个或以上高严重性问题     |
| **HIGH**          | 建议进行调查                | 来自任何来源的高严重性安全问题             |
| **MEDIUM**         | 建议进行审查                | 多个中等严重性问题的存在，或达到预设数量阈值     |
| **LOW**          | 无需立即行动                | 仅发现信息性问题                   |

## 输出代码

- `0`    | 无问题，未发现可采取行动的安全问题             |
- `1`    | 发现安全问题，建议进行调查                |
- `2`    | 发现关键性安全问题，需要立即采取行动           |

## 无需外部依赖

仅使用 Python 标准库，无需安装任何第三方库（如 pip），也不进行网络请求。所有操作都在本地完成。

## 跨平台兼容性

支持 OpenClaw、Claude Code、Cursor 以及任何遵循 Agent Skills 规范的工具。