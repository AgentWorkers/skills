---
name: openclaw-ledger
user-invocable: true
metadata: {"openclaw":{"emoji":"📒","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Ledger

OpenClaw Ledger为代理工作空间提供了防篡改的审计追踪功能。所有工作空间的变更都会被记录在一个基于哈希链的日志中——如果有人篡改了其中任何一条记录，哈希链就会断裂，从而能够立即发现异常。

## 问题所在

代理在执行操作（如修改文件、执行命令、安装技能等）时，不会留下任何可验证的记录。一旦出现问题，就无法追踪具体发生了什么；即使有日志存在，也无法证明这些日志在事后没有被篡改。

## 命令说明

### 初始化（Initialize）

创建账本，并生成当前工作空间的快照。

```bash
python3 {baseDir}/scripts/ledger.py init --workspace /path/to/workspace
```

### 记录变更（Record Changes）

生成当前工作空间的快照，并记录自上次记录以来的所有变更。

```bash
python3 {baseDir}/scripts/ledger.py record --workspace /path/to/workspace
python3 {baseDir}/scripts/ledger.py record -m "Installed new skill" --workspace /path/to/workspace
```

### 验证哈希链（Verify Chain）

检查哈希链是否完整，确保没有任何条目被篡改。

```bash
python3 {baseDir}/scripts/ledger.py verify --workspace /path/to/workspace
```

### 查看日志（View Log）

显示最近的账本记录。

```bash
python3 {baseDir}/scripts/ledger.py log --workspace /path/to/workspace
python3 {baseDir}/scripts/ledger.py log -n 20 --workspace /path/to/workspace
```

### 获取快速状态（Quick Status）

提供当前系统状态的简要信息。

```bash
python3 {baseDir}/scripts/ledger.py status --workspace /path/to/workspace
```

## 工作原理

每条记录包含以下信息：
- 时间戳
- 前一条记录的SHA-256哈希值
- 事件类型及相关数据（例如文件变更、工作空间快照等）

如果任何条目被修改、插入或删除，哈希链就会断裂，`verify`命令会立即检测到这一异常。

## 返回码（Exit Codes）

- `0`：账本正常，哈希链完整
- `1`：账本不存在或存在轻微问题
- `2`：哈希链被篡改，或有条目损坏

## 无外部依赖

仅使用Python标准库，无需安装任何第三方库（如pip），也不涉及网络请求。所有操作都在本地完成。

## 跨平台兼容性

该功能支持OpenClaw、Claude Code、Cursor以及任何遵循“代理技能规范”（Agent Skills Specification）的工具。