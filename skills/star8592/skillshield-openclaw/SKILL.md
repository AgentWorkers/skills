---
name: skillshield
version: 2.1.5
description: 用于AI代理的沙箱化命令运行器：一个基于Rust的守护进程，通过Bubblewrap技术实现与Linux用户命名空间的隔离。
metadata: {"openclaw":{"emoji":"🛡️"}}
---
# SkillShield

**用于AI代理的沙箱命令执行器——基于Rust的守护进程，通过Bubblewrap实现Linux用户命名空间隔离。**

SkillShield为AI驱动的工作流程提供了一个安全的执行环境。它不会直接在主机上运行shell命令，而是通过一个Rust守护进程来处理所有命令。该守护进程会先执行策略检查，随后在[Bubblewrap](https://github.com/containers/bubblewrap)用户命名空间内执行命令。该命名空间具有最小化的、只读的root文件系统权限。

## 工作原理

1. **包装脚本（`skillshield-exec.sh`）**在首次使用时会构建Rust守护进程，并通过本地Unix套接字与其通信。
2. **策略检查**：守护进程会评估每个命令的风险等级（默认为“安全”模式，会阻止具有破坏性的操作并限制文件系统的访问范围）。
3. **被批准的命令**会在`bwrap --unshare-all`环境下执行，此时`/usr`目录以只读方式挂载，且只有当前工作目录可写入。

## 主要特性

- **最小化的root文件系统**：仅提供`/usr`、`/dev`、`/proc`和`/tmp`目录的访问权限；无法访问用户主目录、云凭证路径或敏感的系统文件。
- **策略评估**：Rust策略引擎会根据每个操作（如shell命令、文件读写、网络操作）的风险等级来决定是“允许”、“确认”、“拒绝”还是“放入沙箱”。
- **Unix套接字通信**：包装脚本通过本地套接字与守护进程进行通信，绝不通过网络传输数据。
- **增量编译**：Rust二进制文件仅编译一次并缓存起来，后续调用可在几毫秒内完成。

## 使用方法

```bash
# Run a simple command
./skillshield-exec.sh "echo hello world"

# Cleanup a temporary directory
./skillshield-exec.sh "rm -rf tmp_dir/"
```

## 所需依赖项

| 依赖项 | 用途 |
|---|---|
| Linux | 支持用户命名空间功能 |
| `bwrap` | 提供Bubblewrap沙箱运行环境 |
| `cargo` | 在首次运行时用于构建Rust守护进程 |
| `curl` | 用于检查守护进程的运行状态 |
| `python3` | 用于在包装脚本中处理JSON数据格式化 |

## 链接

- 官网：https://coinwin.info
- 商店链接：https://clawhub.ai/star8592/skillshield-openclaw