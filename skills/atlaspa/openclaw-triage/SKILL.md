---
name: openclaw-triage
user-invocable: true
metadata: {"openclaw":{"emoji":"🚨","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw 故障排查（Incident Triage）

该工具用于处理代理工作空间的事件响应和取证工作。当出现异常情况（如技能行为异常、文件被未经解释地修改，或其他安全工具检测到异常）时，故障排查功能会调查具体原因、评估损失情况，并指导恢复流程。

它就像一名“侦探”，将来自所有 OpenClaw 安全工具的证据整合成一份统一的事件报告。

## 命令

### 全面调查（Full Investigation）

执行全面的事件调查。收集工作空间的状态信息，检查是否存在被入侵的迹象（如最近被修改的关键文件、新添加的技能、异常权限、非工作时间进行的修改、大型文件或隐藏文件），与 Warden/ledger/signet/sentinel 的数据相互关联，构建事件时间线，并计算事件严重程度（CRITICAL / HIGH / MEDIUM / LOW）。

```bash
python3 {baseDir}/scripts/triage.py investigate --workspace /path/to/workspace
```

### 事件时间线（Event Timeline）

按时间顺序记录工作空间中所有文件的变化情况。按小时分组事件，突出显示可疑的批量修改行为（在短时间内修改了大量文件），显示受影响的目录和技能，并在可用时与 ledger 的记录进行关联。

```bash
python3 {baseDir}/scripts/triage.py timeline --workspace /path/to/workspace
```

**查看更久远的历史数据（超出默认的 24 小时范围）：**

```bash
python3 {baseDir}/scripts/triage.py timeline --hours 72 --workspace /path/to/workspace
```

### 传播范围（Blast Radius）

评估潜在入侵的传播范围。根据文件的风险等级（关键文件、内存相关文件、技能相关文件、配置文件）对文件进行分类，检查最近被修改的文件中是否存在凭证泄露的迹象，扫描是否有数据外泄的 URL，并判断入侵范围是“受控的”（仅限于单个区域）、“扩散的”（涉及多个技能）还是“系统性的”（影响整个工作空间）。

```bash
python3 {baseDir}/scripts/triage.py scope --workspace /path/to/workspace
```

### 证据收集（Evidence Collection）

在采取修复措施之前，先收集并保存取证证据。生成工作空间的完整快照（包含文件的列表及其 SHA-256 哈希值、文件大小和修改时间戳），复制所有可用的安全工具数据（.integrity/、.ledger/、.signet/、.sentinel/），并生成一份总结报告。务必在修复前执行此操作以保留完整的证据链。

```bash
python3 {baseDir}/scripts/triage.py evidence --workspace /path/to/workspace
```

**将结果保存到自定义输出目录：**

```bash
python3 {baseDir}/scripts/triage.py evidence --output /path/to/evidence/dir --workspace /path/to/workspace
```

### 快速状态（Quick Status）

以一行文字显示故障排查的当前状态：最后一次调查的时间戳、当前的威胁等级以及是否已收集到证据。

```bash
python3 {baseDir}/scripts/triage.py status --workspace /path/to/workspace
```

## 工作空间自动检测（Workspace Auto-Detection）

如果省略了 `--workspace` 参数，脚本会尝试以下路径来查找工作空间信息：
1. `OPENCLAW_WORKSPACE` 环境变量
2. 当前目录（如果存在 AGENTS.md 文件）
3. `~/.openclaw/workspace`（默认路径）

## 数据来源的交叉引用（Cross-Reference Sources）

故障排查功能会自动从以下 OpenClaw 工具中获取数据：

| 工具            | 数据路径                | 检查内容                                      |
|------------------|------------------|-----------------------------------------|
| **Warden**        | `.integrity/manifest.json`      | 文件自上次正常状态以来的变更情况                   |
| **Ledger**        | `.ledger/chain.jsonl`      | 链条中断、无法解析的条目、可疑的日志记录                |
| **Signet**        | `.signet/manifest.json`      | 被篡改的技能签名（签名后的修改）                          |
| **Sentinel**       | `.sentinel/threats.json`      | 已知的威胁和高风险发现                            |

## 事件严重程度等级（Incident Severity Levels）

| 等级            | 含义                          | 触发条件                                      |
|------------------|----------------------------------|-----------------------------------------|
| **CRITICAL**       | 需立即响应                    | 任何关键性发现，或存在 3 个以上高风险发现                |
| **HIGH**          | 建议进行调查                    | 来自任何来源的高风险发现                          |
| **MEDIUM**         | 建议审查                        | 多个中等风险发现或达到一定数量阈值                    |
| **LOW**          | 无需立即行动                    | 仅发现一般性问题                          |

## 输出代码（Exit Codes）

- `0`    | 无问题，未发现可操作的安全隐患                |
- `1`    | 发现安全问题，建议进行调查                    |
- `2`    | 发现严重问题，需要立即采取行动                    |

## 无外部依赖（No External Dependencies）

仅使用 Python 标准库，无需安装任何第三方库（如 pip），也不进行网络请求。所有操作都在本地完成。

## 跨平台兼容性（Cross-Platform）

该工具可与 OpenClaw、Claude Code、Cursor 以及任何遵循 Agent Skills 规范的工具配合使用。