---
name: linux-kernel-crash-debug
description: 使用 `crash` 工具调试 Linux 内核崩溃问题。当用户提到内核崩溃、内核恐慌、`vmcore` 分析、内核转储调试、`crash` 工具的使用、内核错误（`oops`）调试、分析内核崩溃转储文件，或定位内核问题的根本原因时，可以使用该工具。
requires:
  - crash
  - gdb
  - readelf
  - objdump
  - makedumpfile
---
# Linux内核崩溃调试

本文档将指导您如何使用`crash`工具分析Linux内核崩溃转储文件。

## 安装

### Claude Code
```bash
claude skill install linux-kernel-crash-debug.skill
```

### OpenClaw
```bash
# Method 1: Install via ClawHub
clawhub install linux-kernel-crash-debug

# Method 2: Manual installation
mkdir -p ~/.openclaw/workspace/skills/linux-kernel-crash-debug
cp SKILL.md ~/.openclaw/workspace/skills/linux-kernel-crash-debug/
```

## 快速入门

### 启动会话
```bash
# Analyze a dump file
crash vmlinux vmcore

# Debug a running system
crash vmlinux

# Raw RAM dump
crash vmlinux ddr.bin --ram_start=0x80000000
```

### 核心调试工作流程
```
1. crash> sys              # Confirm panic reason
2. crash> log              # View kernel log
3. crash> bt               # Analyze call stack
4. crash> struct <type>    # Inspect data structures
5. crash> kmem <addr>      # Memory analysis
```

## 先决条件

| 项目 | 要求 |
|------|-------------|
| **vmlinux** | 必须启用调试符号（`CONFIG_DEBUG_INFO=y`） |
| **vmcore** | 必须支持kdump/netdump/diskdump/ELF格式 |
| **版本** | vmlinux的版本必须与vmcore内核版本完全匹配 |

### 包安装

#### Anolis OS / Alibaba Cloud Linux
```bash
# Install crash utility
sudo dnf install crash

# Install kernel debuginfo (match your kernel version)
sudo dnf install kernel-debuginfo-$(uname -r)

# Install additional analysis tools
sudo dnf install gdb readelf objdump makedumpfile

# Optional: Install kernel-devel for source code reference
sudo dnf install kernel-devel-$(uname -r)
```

#### RHEL / CentOS / Rocky / AlmaLinux
```bash
sudo dnf install crash kernel-debuginfo-$(uname -r)
sudo dnf install gdb binutils makedumpfile
```

#### Ubuntu / Debian
```bash
sudo apt install crash linux-crashdump gdb binutils makedumpfile
sudo apt install linux-image-$(uname -r)-dbgsym
```

### 自编译内核
```bash
# Enable debug symbols in kernel config
make menuconfig  # Enable CONFIG_DEBUG_INFO, CONFIG_DEBUG_INFO_REDUCED=n

# Or set directly
scripts/config --enable CONFIG_DEBUG_INFO
scripts/config --enable CONFIG_DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT
```

### 验证安装
```bash
# Check crash version
crash --version

# Verify debuginfo matches kernel
crash /usr/lib/debug/lib/modules/$(uname -r)/vmlinux /proc/kcore
```

## 核心命令参考

### 调试分析

| 命令 | 用途 | 示例 |
|---------|---------|---------|
| `sys` | 系统信息/panic原因 | `sys`, `sys -i` |
| `log` | 内核消息缓冲区 | `log`, `log \| tail` |
| `bt` | 堆栈回溯 | `bt`, `bt -a`, `bt -f` |
| `struct` | 查看结构体 | `struct task_struct <addr>` |
| `p/px/pd` | 打印变量 | `p jiffies`, `px current` |
| `kmem` | 内存分析 | `kmem -i`, `kmem -S <cache>` |

### 任务和进程

| 命令 | 用途 | 示例 |
|---------|---------|---------|
| `ps` | 进程列表 | `ps`, `ps -m \| grep UN` |
| `set` | 切换上下文 | `set <pid>`, `set -p` |
| `foreach` | 批量处理任务 | `foreach bt`, `foreach UN bt` |
| `task` | 查看task_struct内容 | `task <pid>` |
| `files` | 打开文件 | `files <pid>` |

### 内存操作

| 命令 | 用途 | 示例 |
|---------|---------|---------|
| `rd` | 读取内存 | `rd <addr>`, `rd -p <phys>` |
| `search` | 在内存中搜索 | `search -k deadbeef` |
| `vtop` | 地址转换 | `vtop <addr>` |
| `list` | 遍历链表 | `list task_struct.tasks -h <addr>` |

## `bt`命令详解

最重要的调试命令：
```
crash> bt              # Current task stack
crash> bt -a           # All CPU active tasks
crash> bt -f           # Expand stack frame raw data
crash> bt -F           # Symbolic stack frame data
crash> bt -l           # Show source file and line number
crash> bt -e           # Search for exception frames
crash> bt -v           # Check stack overflow
crash> bt -R <sym>     # Only show stacks referencing symbol
crash> bt <pid>        # Specific process
```

## 上下文管理

崩溃会话具有“当前上下文”，这会影响`bt`, `files`, `vm`等命令的执行：
```
crash> set              # View current context
crash> set <pid>        # Switch to specified PID
crash> set <task_addr>  # Switch to task address
crash> set -p           # Restore to panic task
```

## 会话控制
```
# Output control
crash> set scroll off   # Disable pagination
crash> sf               # Alias for scroll off

# Output redirection
crash> foreach bt > bt.all

# GDB passthrough
crash> gdb bt           # Single gdb invocation
crash> set gdb on       # Enter gdb mode
(gdb) info registers
(gdb) set gdb off

# Read commands from file
crash> < commands.txt
```

## 常见调试场景

### 内核BUG定位
```
crash> sys                    # Confirm panic
crash> log | tail -50         # View logs
crash> bt                     # Call stack
crash> bt -f                  # Expand frames for parameters
crash> struct <type> <addr>   # Inspect data structures
```

### 死锁分析
```
crash> bt -a                  # All CPU call stacks
crash> ps -m | grep UN        # Uninterruptible processes
crash> foreach UN bt          # View waiting reasons
crash> struct mutex <addr>    # Inspect lock state
```

### 内存问题
```
crash> kmem -i                # Memory statistics
crash> kmem -S <cache>        # Inspect slab
crash> vm <pid>               # Process memory mapping
crash> search -k <pattern>    # Search memory
```

### 堆栈溢出
```
crash> bt -v                  # Check stack overflow
crash> bt -r                  # Raw stack data
```

## 高级技巧

### 链式查询
```
crash> bt -f                  # Get pointers
crash> struct file.f_dentry <addr>
crash> struct dentry.d_inode <addr>
crash> struct inode.i_pipe <addr>
```

### 批量检查slab内存
```
crash> kmem -S inode_cache | grep counter | grep -v "= 1"
```

### 遍历内核链表
```
crash> list task_struct.tasks -s task_struct.pid -h <start>
crash> list -h <addr> -s dentry.d_name.name
```

## 扩展参考

有关详细信息，请参阅以下参考文件：

| 文件 | 内容 |
|------|---------|
| `references/advanced-commands.md` | 高级命令：list, rd, search, vtop, kmem, foreach |
| `references/vmcore-format.md` | vmcore文件格式、ELF结构、VMCOREINFO |
| `references/case-studies.md` | 详细调试案例：内核BUG、死锁、OOM、空指针、堆栈溢出 |

## 常见错误
```
crash: vmlinux and vmcore do not match!
# -> Ensure vmlinux version exactly matches vmcore

crash: cannot find booted kernel
# -> Specify vmlinux path explicitly

crash: cannot resolve symbol
# -> Check if vmlinux has debug symbols
```

## 安全警告

⚠️ **危险操作**

以下命令可能导致系统损坏或数据丢失：

| 命令 | 风险 | 建议 |
|---------|------|----------------|
| `wr` | 向正在运行的内核内存写入数据 | **严禁在生产系统中使用** - 可能导致系统崩溃或损坏内核 |
| GDB passthrough | 无限制的内存访问 | 使用时需谨慎，可能会修改内存或寄存器 |

🔒 **敏感数据处理**

- **vmcore文件** 包含完整的内核内存信息，可能包含：
  - 用户进程内存和凭据
  - 加密密钥和敏感信息
  - 网络连接数据和密码
- **访问控制**：仅允许授权人员访问vmcore文件
- **安全存储**：将转储文件存储在加密或受控制的目录中
- **安全删除**：使用`shred`等工具安全删除vmcore文件

🛡️ **最佳实践**

1. 尽可能在隔离/测试环境中分析vmcore文件
2. 未经处理前切勿公开共享原始vmcore文件
3. 考虑使用`makedumpfile -d`过滤敏感数据
4. 记录并审计所有调试会话以确保合规性

## 重要注意事项

1. **版本匹配**：vmlinux的版本必须与vmcore内核版本完全匹配
2. **调试信息**：必须使用启用调试符号的vmlinux
3. **上下文影响**：`bt`, `files`, `vm`等命令会受到当前上下文的影响
4. **修改运行中的系统**：`wr`命令会修改正在运行的内核，极其危险

## 资源

- [Crash Utility白皮书](https://crash-utility.github.io/crash_whitepaper.html)
- [Crash Utility文档](https://crash-utility.github.io/)
- [Crash帮助页面](https://crash-utility.github.io/help_pages/)

## 贡献

这是一个开源项目，欢迎贡献！

- **GitHub仓库**：https://github.com/crazyss/linux-kernel-crash-debug
- **报告问题**：[GitHub问题](https://github.com/crazyss/linux-kernel-crash-debug/issues)
- **提交PR**：欢迎提交用于修复漏洞、添加新功能或改进文档的Pull请求

请参阅[CONTRIBUTING.md](https://github.com/crazyss/linux-kernel-crash-debug/blob/main/CONTRIBUTING.md)以获取贡献指南。