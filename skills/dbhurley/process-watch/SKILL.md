---
name: process-watch
description: 监控系统进程：CPU使用情况、内存使用情况、磁盘I/O操作、网络活动、打开的文件以及使用的端口。识别占用大量系统资源的进程，终止那些失控运行的进程，并追踪到底是什么在消耗系统的性能。
metadata:
  clawdhub:
    emoji: "📊"
    requires:
      bins: ["python3"]
---

# Process Watch

这是一个全面的系统进程监控工具，其功能远超基本的 `top` 命令：
- 显示每个进程的 CPU 和内存使用情况
- 显示每个进程的磁盘 I/O 操作
- 显示每个进程的网络连接信息
- 显示每个进程打开的文件及文件描述符
- 显示每个进程绑定的端口
- 显示进程树结构

## 命令

### 列出所有进程
```bash
process-watch list [--sort cpu|mem|disk|name] [--limit 20]
```

### 显示资源消耗最大的进程
```bash
process-watch top [--type cpu|mem|disk|net] [--limit 10]
```

### 查看进程详细信息
```bash
process-watch info <pid>
# Shows: CPU, memory, open files, network connections, children, environment
```

### 按名称查找进程
```bash
process-watch find <name>
# e.g., process-watch find chrome
```

### 查看进程绑定的端口
```bash
process-watch ports [--port 3000]
# What's listening on which port?
```

### 查看进程的网络连接信息
```bash
process-watch net [--pid <pid>] [--established]
```

### 强制终止进程
```bash
process-watch kill <pid> [--force]
process-watch kill --name "chrome" [--force]
```

### 启动监控模式
```bash
process-watch watch [--interval 2] [--alert-cpu 80] [--alert-mem 90]
# Continuous monitoring with threshold alerts
```

### 查看系统概览
```bash
process-watch summary
# Quick overview: load, memory, disk, top processes
```

## 使用示例

```bash
# What's eating my CPU?
process-watch top --type cpu

# What's on port 3000?
process-watch ports --port 3000

# Details on a specific process
process-watch info 1234

# Kill all Chrome processes
process-watch kill --name chrome

# Watch with alerts
process-watch watch --alert-cpu 90 --alert-mem 85
```

## 平台支持

- **macOS**：完全支持
- **Linux**：完全支持
- **Windows**：部分支持（仅提供基本进程列表，没有 `lsof` 命令的功能）