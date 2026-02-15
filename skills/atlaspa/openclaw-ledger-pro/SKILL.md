---
name: openclaw-ledger-pro
description: "完整的审计追踪套件：包括工作区变更的哈希链记录功能、冻结机制、取证分析、链式数据恢复以及自动化保护措施。所有功能均基于 openclaw-ledger（免费开源工具）实现，并配备了自动化应对策略。"
user-invocable: true
metadata: {"openclaw":{"emoji":"📒","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Ledger Pro

这是一个专为代理工作空间设计的全套审计追踪工具。所有工作空间的更改都会被记录在一个基于哈希链的日志中——如果有人篡改了日志条目，哈希链就会断裂，从而能够立即发现异常。OpenClaw Pro 提供了自动化的应对措施，包括冻结数据、进行取证分析、恢复哈希链、导出日志以及执行全面的保护操作。

## 问题所在

代理在修改文件、执行命令或安装技能时，往往不会留下任何可验证的记录。一旦出现问题，就很难追踪到底发生了什么。即使有日志存在，也无法证明这些日志在事后没有被篡改。

**openclaw-ledger**（免费版）仅提供基本的日志记录和验证功能。

**openclaw-ledger-pro** 则提供了更全面的功能：包括数据恢复、隔离受影响的系统以及加强系统安全。

## 命令

### 初始化

创建账本，并生成当前工作空间的快照。

```bash
python3 {baseDir}/scripts/ledger.py init --workspace /path/to/workspace
```

### 记录更改

生成当前工作空间的快照，并记录自上次记录以来的所有更改。

```bash
python3 {baseDir}/scripts/ledger.py record --workspace /path/to/workspace
python3 {baseDir}/scripts/ledger.py record -m "Installed new skill" --workspace /path/to/workspace
```

### 验证哈希链

检查哈希链是否完整，确保没有条目被篡改。

```bash
python3 {baseDir}/scripts/ledger.py verify --workspace /path/to/workspace
```

### 查看日志

显示最近的账本记录。

```bash
python3 {baseDir}/scripts/ledger.py log --workspace /path/to/workspace
python3 {baseDir}/scripts/ledger.py log -n 20 --workspace /path/to/workspace
```

### 快速状态检查

```bash
python3 {baseDir}/scripts/ledger.py status --workspace /path/to/workspace
```

## OpenClaw Pro 的高级功能

### 冻结数据

创建链文件的只读备份，将当前链文件复制到 `.ledger/frozen/chain-{timestamp}.jsonl`。在复制之前会记录一个“冻结”事件。定期执行此操作可以确保有可靠的恢复点。

```bash
python3 {baseDir}/scripts/ledger.py freeze --workspace /path/to/workspace
```

### 取证分析

对哈希链进行详细分析，展示所有更改的完整时间线，包括文件级别的差异、会话边界以及异常情况（如时间间隔异常、批量更改、时间戳倒退等）。

```bash
python3 {baseDir}/scripts/ledger.py forensics --workspace /path/to/workspace
python3 {baseDir}/scripts/ledger.py forensics --from 2025-01-01 --workspace /path/to/workspace
python3 {baseDir}/scripts/ledger.py forensics --from 2025-01-01 --to 2025-01-31 --workspace /path/to/workspace
```

### 恢复数据

从冻结的备份中恢复哈希链。在恢复之前会验证备份的完整性。在覆盖现有数据之前会先备份当前链文件。如果未指定 `--from-frozen` 参数，系统会使用最新的备份。

```bash
python3 {baseDir}/scripts/ledger.py restore --workspace /path/to/workspace
python3 {baseDir}/scripts/ledger.py restore --from-frozen 20250115T120000Z --workspace /path/to/workspace
```

### 导出数据

将整个哈希链导出为结构化的 JSON 格式或可读的文本报告，以便外部分析。

```bash
python3 {baseDir}/scripts/ledger.py export --workspace /path/to/workspace
python3 {baseDir}/scripts/ledger.py export --format text --workspace /path/to/workspace
python3 {baseDir}/scripts/ledger.py export --format json --workspace /path/to/workspace
```

### 加强保护

执行全面的自动化保护操作。建议在每次会话开始时使用此功能。具体步骤如下：
1. 验证哈希链的完整性；
2. 如果检测到篡改行为：自动冻结相关数据，并尝试从干净的备份中恢复；
3. 记录当前工作空间的状态；
4. 报告分析结果。

```bash
python3 {baseDir}/scripts/ledger.py protect --workspace /path/to/workspace
```

## 工作原理

每个日志条目包含以下信息：
- 时间戳；
- 前一条记录的 SHA-256 哈希值；
- 事件类型及具体操作内容（如文件更改、快照生成等）。

如果任何条目被修改、插入或删除，哈希链就会断裂，`verify` 命令会立即检测到这一情况。`protect` 命令会自动执行一系列响应措施：检测篡改行为、保存证据、从干净的备份中恢复数据，并记录当前的工作空间状态。

## 返回码

- `0`：系统正常运行，哈希链完整；
- `1`：检测到警告性错误（存在更改或轻微异常）；
- `2`：系统出现严重问题（哈希链被篡改、数据损坏或恢复失败）。

## 无外部依赖

仅依赖 Python 标准库，无需安装额外的库（如 pip），也不需要进行网络请求。所有操作都在本地完成。

## 跨平台兼容性

支持 OpenClaw、Claude Code、Cursor 以及任何遵循 Agent Skills 规范的工具。