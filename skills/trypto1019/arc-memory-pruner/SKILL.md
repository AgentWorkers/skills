---
name: memory-pruner
description: 自动修剪并压缩代理内存文件，以防止内存无限制地增长。日志采用循环缓冲区存储，状态数据根据重要性进行保留，同时支持配置内存大小限制。
user-invocable: true
metadata: {"openclaw": {"emoji": "🧹", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---
# 内存清理工具

帮助您的代理程序保持轻量级的内存使用。该工具会自动清理日志文件、压缩状态文件，并强制执行大小限制，确保代理程序不会因内存或上下文窗口的限制而出现问题。

## 该工具的必要性

随着时间的推移，代理程序会积累大量内存文件：日志文件会不断增长，状态文件中也会包含过时的数据。最终，在启动时可能需要读取大量内存数据（例如50,000个令牌），但其中有一半可能是无效或过时的信息。内存清理工具通过设置相应的限制，仅保留真正重要的数据。

## 命令

### 清理内存文件（保留最后N行）
```bash
python3 {baseDir}/scripts/memory_pruner.py prune --file ~/wake-state.md --max-lines 200
```

### 清理日志目录（循环缓冲区，保留最后N个文件）
```bash
python3 {baseDir}/scripts/memory_pruner.py prune-logs --dir ~/agents/logs/ --keep 7
```

### 压缩状态文件（删除符合特定模式的文件内容）
```bash
python3 {baseDir}/scripts/memory_pruner.py compact --file ~/wake-state.md --remove-before "2026-02-14"
```

### 检查内存大小
```bash
python3 {baseDir}/scripts/memory_pruner.py stats --dir ~/
```

### 预览清理结果
```bash
python3 {baseDir}/scripts/memory_pruner.py prune --file ~/wake-state.md --max-lines 200 --dry-run
```

## 主要功能

- **基于行的清理**：保留文件中的最后N行内容。
- **日志轮换**：对于日志目录，采用循环缓冲机制（保留最近N个文件，删除最旧的文件）。
- **基于日期的压缩**：删除早于指定日期的记录。
- **大小限制**：强制控制文件的最大大小（以字节为单位）。
- **预览模式**：在应用清理操作前查看预览结果。
- **统计信息**：提供内存文件的大小及增长情况的概览。