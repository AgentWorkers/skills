---
name: debug
version: 1.0.0
author: BytesAgain
license: MIT-0
tags: [debug, tool, utility]
---

# 调试

调试工具包提供了日志分析、错误追踪、内存分析、网络检查、性能瓶颈检测以及崩溃报告解析等功能。

## 命令

| 命令 | 描述 |
|---------|-------------|
| `debug logs` | <文件> | 查看指定文件的日志内容 |
| `debug trace` | <错误信息> | 根据错误信息进行调试 |
| `debug memory` | <进程ID> | 分析指定进程的内存使用情况 |
| `debug network` | <进程ID> | 检查指定进程的网络连接 |
| `debug profile` | <命令> | 分析指定命令的执行性能 |
| `debug crash` | <崩溃报告> | 分析崩溃报告的详细信息 |

## 使用方法

```bash
# Show help
debug help

# Quick start
debug logs <file>
```

## 示例

```bash
# Example 1
debug logs <file>

# Example 2
debug trace <error>
```

- 运行 `debug help` 可以查看所有可用的命令。

---
*由 BytesAgain 提供支持 | bytesagain.com*
*反馈与功能请求：https://bytesagain.com/feedback*

## 使用场景

- 从终端快速执行调试任务 |
- 用于自动化流程中

## 输出结果

调试结果会输出到标准输出（stdout）。可以使用 `debug run > output.txt` 将结果保存到文件中。

## 配置

可以通过设置 `DEBUG_DIR` 来更改数据存储目录。默认目录为：`~/.local/share/debug/`

## 使用场景

- 从终端快速执行调试任务 |
- 用于自动化流程中