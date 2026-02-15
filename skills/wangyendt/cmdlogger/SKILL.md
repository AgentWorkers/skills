---
name: pywayne-bin-cmdlogger
description: 执行命令时需进行完整的输入/输出（I/O）日志记录。当用户需要将命令的执行过程（包括标准输入（stdin）、标准输出（stdout）和标准错误输出（stderr）全部记录到日志文件中，同时仍保留实时的控制台输出时，应使用此功能。该功能会在用户请求记录、监控或追踪命令执行情况时被触发，尤其适用于构建过程、长时间运行的脚本、调试会话或持续集成/持续交付（CI/CD）流程。
---
# Pywayne Bin Cmdlogger

该工具用于执行命令，并将所有的标准输入（stdin）、标准输出（stdout）和标准错误（stderr）内容记录到文件中，同时实时地将这些数据转发到控制台。

## 快速入门

```bash
# Log command execution to default file (io_log.log in script directory)
cmdlogger <command> [args...]

# Specify custom log file path
cmdlogger --log-path <log_path> <command> [args...]
```

## 使用示例

### 构建过程记录

```bash
# Log CMake configuration
cmdlogger --log-path cmake_config.log cmake ..

# Log build process
cmdlogger --log-path build.log make -j$(nproc)
```

### 脚本执行监控

```bash
# Log Python script execution
cmdlogger --log-path script_run.log python3 my_script.py --arg1 value1

# Log shell script execution
cmdlogger --log-path deploy.log ./deploy.sh production
```

### 调试会话

```bash
# Log GDB debug session
cmdlogger --log-path debug_session.log gdb ./my_program

# Log Python interactive session
cmdlogger --log-path python_debug.log python3 -i my_module.py
```

### 网络操作

```bash
# Log curl request with verbose output
cmdlogger --log-path api_test.log curl -v https://api.example.com/data

# Log SSH connection process
cmdlogger --log-path ssh_session.log ssh user@remote-host
```

### 简单命令日志记录

```bash
# Log git status
cmdlogger git status

# Log echo command
cmdlogger echo "Hello World"
```

## 命令参考

| 参数 | 说明 |
| ---------- | ------------- |
| `command` | 要执行的命令 |
| `[args...]` | 命令参数 |
| `--log-path <path>` | 可选的日志文件路径。默认值为脚本目录下的 `io_log.log` |

## 日志格式

日志文件中的每一行都会以流类型作为前缀：

- `输入: <内容>` - 标准输入
- `输出: <内容>` - 标准输出
- `错误: <内容>` - 标准错误

### 日志输出示例

运行 `cmdlogger echo "Hello World"` 会产生如下日志：

```
输出: Hello World
```

运行 `cmdlogger python3 -c "import sys; print('stdout'); print('stderr', file=sys.stderr)"` 会产生如下日志：

```
输出: stdout
错误: stderr
```

## 主要特性

- **全套输入/输出记录**：捕获所有的 stdin、stdout 和 stderr 数据。
- **实时转发**：在记录日志的同时，将数据实时转发到控制台。
- **多线程处理**：分别为 stdin、stdout 和 stderr 使用独立的线程。
- **编码处理**：能够优雅地处理非 UTF-8 编码的数据。
- **资源清理**：自动清理相关进程和文件。

## 使用场景

- 记录复杂的构建过程以供后续分析。
- 监控长时间运行的脚本并保留完整的日志记录。
- 进行调试时保留完整的输入/输出历史记录。
- 用于持续集成/持续部署（CI/CD）流程的日志记录。
- 通过执行轨迹进行性能分析。

## 重要说明

- **交互式命令**：用户输入的内容（包括密码）也会被记录下来。请注意保护敏感信息。
- **大量输出**：对于输出量较大的命令，日志文件可能会变得很大。请确保有足够的磁盘空间。
- **默认日志位置**：如果未指定 `--log-path`，日志文件将创建在脚本目录下，文件名为 `io_log.log`。
- **退出代码**：返回执行命令的退出代码（如果命令不存在，返回 127）。