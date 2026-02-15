---
name: openclaw-signet
user-invocable: true
metadata: {"openclaw":{"emoji":"🔏","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Signet

这是一种用于验证已安装技能的加密机制。在安装技能时会对技能进行签名处理，以确保其后续未被篡改。

## 问题所在

你安装了一个技能，它能够正常运行。但几天后，某个被入侵的进程修改了技能目录中的文件——注入了恶意代码、改变了技能的行为，甚至尝试窃取数据。现有的防御措施都基于启发式方法（如正则表达式匹配），无法从数学角度验证已安装的代码是否保持不变。

## 命令

### 签署技能
为所有已安装的技能生成 SHA-256 哈希值，并将这些哈希值存储到信任清单（trust manifest）中。
```bash
python3 {baseDir}/scripts/signet.py sign --workspace /path/to/workspace
```

### 签署单个技能
```bash
python3 {baseDir}/scripts/signet.py sign openclaw-warden --workspace /path/to/workspace
```

### 验证技能
将当前技能的状态与信任清单中的签名进行比较。
```bash
python3 {baseDir}/scripts/signet.py verify --workspace /path/to/workspace
```

### 列出已签名的技能
显示所有已签名的技能列表。
```bash
python3 {baseDir}/scripts/signet.py list --workspace /path/to/workspace
```

### 快速状态检查
显示所有技能的当前状态。
```bash
python3 {baseDir}/scripts/signet.py status --workspace /path/to/workspace
```

## 工作原理

1. `sign` 命令会计算每个技能目录中所有文件的 SHA-256 哈希值。
2. 一个综合哈希值代表了整个技能的状态。
3. `verify` 命令会重新计算所有文件的哈希值，并与信任清单中的哈希值进行比对。
4. 如果有任何文件被修改、添加或删除，综合哈希值就会发生变化。
5. 该命令会详细报告每个被篡改的技能中具体发生了哪些文件的变化。

## 返回码

- `0`：所有技能都已通过验证。
- `1`：检测到未签名的技能。
- `2`：检测到被篡改的技能。

## 无需外部依赖
仅使用 Python 标准库，无需安装任何第三方库（如 pip），也不需要进行网络请求。所有操作都在本地完成。

## 跨平台兼容性
该机制适用于 OpenClaw、Claude Code、Cursor 以及任何遵循 Agent Skills 规范的工具。