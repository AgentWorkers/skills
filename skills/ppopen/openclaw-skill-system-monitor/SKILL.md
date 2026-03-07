---
name: system-monitor
description: "实时系统指标监控（包括CPU、内存、磁盘、网络和进程状态）。适用场景：当用户需要查看系统状态、CPU使用率、内存使用情况、磁盘空间、网络流量、正在运行的进程或系统性能时。支持macOS和Linux操作系统。可用工具：top、htop、df、iostat、vm_stat、host、free、lsof、uptime。"
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins:
        - top
        - df
        - vm_stat
        - free
        - lsof
        - uptime
---
# 系统监控技能

监控实时的系统指标，包括CPU、内存、磁盘、网络和进程信息。

## 使用场景

✅ **在以下情况下使用此技能：**

- “检查系统状态”
- “CPU使用率”
- “内存使用情况”
- “磁盘空间”
- “网络流量”
- “正在运行的进程”
- “系统性能”
- “系统负载”

## 设置

某些工具可能需要通过Homebrew进行安装：

```bash
# Install optional enhanced tools
brew install htop      # Enhanced top (better UI)
brew install nettop    # Real-time network monitoring (macOS)
brew install iostat    # I/O statistics (Linux)
```

## 平台检测

检测当前平台以使用相应的命令：

```bash
uname -s  # Darwin = macOS, Linux = Linux
```

## CPU使用率

### macOS

```bash
# CPU usage summary (user, system, idle)
top -l 1 -n 0 | grep "CPU usage"

# Detailed per-core usage
top -l 2 -n 0 | tail -1

# Overall CPU percentage
vm_stat | head -5
```

### Linux

```bash
# CPU usage summary
top -bn1 | head -5

# Detailed per-core
mpstat -P ALL 1 1

# Overall
uptime
```

### 一键式命令（跨平台通用）

```bash
# macOS
top -l 1 -n 0 -s 0 | awk '/CPU usage/ {print}'

# Linux  
top -bn1 | grep "Cpu(s)"
```

### 适用于JSON格式的脚本

```bash
# macOS: CPU stats with specific fields
top -l 1 -n 0 -s 0 -stats pid,pcpu,pmem,comm
```

## 内存使用率

### macOS

```bash
# Memory info (page size, pages active, wired, compressed, free)
vm_stat

# Human-readable summary
top -l 1 -n 0 | grep "PhysMem"

# Full memory details
hostinfo | grep "memory"
```

### Linux

```bash
# Human-readable
free -h

# Detailed in MB
free -m

# Swap info
swapon -s
```

### macOS下的内存计算方法

```bash
# Calculate used memory from vm_stat
vm_stat | awk '/Pages active/ {active=$3} /Pages wired/ {wired=$3} /Pages free/ {free=$3} END {print "Active: " active " Wired: " wired " Free: " free}'
```

## 磁盘空间

### macOS & Linux

```bash
# All filesystems, human-readable
df -h

# Specific volume (macOS)
df -h /

# Linux root
df -h /

# Show inode usage (Linux)
df -i

# Sorted by usage (macOS)
df -h | sort -k5 -h

# Only local filesystems
df -h -t local
```

## 目录级别的磁盘使用情况

```bash
# Current directory (macOS)
du -sh .

# Top-level directories
du -h --max-depth=1

# Linux sorted by size
du -h --max-depth=1 | sort -h
```

## 网络统计信息

### macOS

```bash
# Network interfaces (use ifconfig instead)
ifconfig -a

# Active connections
lsof -i -n | head -20

# Listening ports
lsof -i -n | grep LISTEN

# Real-time network usage
nettop -P -L 1 -J bytes_in,bytes_out
```

### Linux

```bash
# Interface statistics
ip -s link

# TCP/UDP stats
ss -s

# Active connections
ss -tunap
```

## 进程列表

### macOS

```bash
# Top processes by CPU
top -o cpu -l 1 -n 15

# Top processes by memory
top -o mem -l 1 -n 15

# All processes
ps aux

# User processes
ps -U $(whoami)
```

### Linux

```bash
# Top processes by CPU
top -bn1 | head -12

# Top by memory
top -bo %MEM -bn1 | head -12

# Process tree
pstree

# User processes
ps -U $(whoami) --sort=-%mem
```

## 系统负载

### macOS

```bash
# Load average
uptime

# Detailed
hostinfo | grep "load"
```

### Linux

```bash
uptime
# or
cat /proc/loadavg
```

## 综合系统状态

### 快速健康检查

```bash
# CPU, Memory, Disk in one view (macOS)
echo "=== CPU ===" && top -l 1 -n 0 | grep "CPU usage"
echo "=== Memory ===" && top -l 1 -n 0 | grep "PhysMem"
echo "=== Disk ===" && df -h / | tail -1

# Linux
echo "=== CPU ===" && top -bn1 | head -5
echo "=== Memory ===" && free -h
echo "=== Disk ===" && df -h /
echo "=== Load ===" && uptime
```

## 组合脚本

### system-stats.sh

一个用于快速系统健康检查的组合脚本：

```bash
#!/bin/bash
# Combined system stats - run from skills/system-monitor/scripts/

PLATFORM=$(uname -s)

echo "=== System Stats ==="
echo "Time: $(date)"
echo "Platform: $PLATFORM"
echo ""

if [ "$PLATFORM" = "Darwin" ]; then
    echo "--- CPU ---"
    top -l 1 -n 0 -s 0 | grep "CPU usage"
    echo ""
    
    echo "--- Memory ---"
    top -l 1 -n 0 | grep "PhysMem"
    vm_stat | head -5
    echo ""
    
    echo "--- Disk ---"
    df -h / | tail -1
    echo ""
    
    echo "--- Load Average ---"
    uptime
else
    echo "--- CPU ---"
    top -bn1 | head -5
    echo ""
    
    echo "--- Memory ---"
    free -h
    echo ""
    
    echo "--- Disk ---"
    df -h / | tail -1
    echo ""
    
    echo "--- Load Average ---"
    uptime
fi
```

## 注意事项

- macOS使用`vm_stat`来获取内存信息，Linux使用`free`
- 不同平台上的`top`命令输出格式可能有所不同
- 在macOS上使用`hostinfo`来获取系统概览信息
- 使用`lsof`或`nettop`代替已弃用的`netstat`
- 对于持续监控，可以使用`watch`命令或循环执行`top`命令