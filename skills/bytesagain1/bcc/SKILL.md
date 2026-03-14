---
name: Bcc
description: "**BCC** – 用于基于 BPF（Binary Packet Filter）的 Linux I/O 分析、网络监控等功能的工具。  
**用途**：当需要使用 BPF 相关功能时，可选用 BCC 工具。  
**触发条件**：当执行 `bcc` 命令时，相关功能会被激活。"
---
# Bcc

BCC 是一套基于 BPF（Berkeley Packet Filter）的工具，用于 Linux 系统的 I/O 分析、网络监控等功能。## 命令

- `help` - 显示帮助信息
- `run` - 运行指定的命令
- `info` - 显示命令的详细信息
- `status` - 显示当前工具的状态

## 功能特点

- 兼容 iovisor/bcc 的核心功能

## 使用方法

只需执行以下命令即可使用 BCC：`bcc <命令> [参数]`

---
💬 意见反馈与功能请求：https://bytesagain.com/feedback
由 BytesAgain 提供支持 | bytesagain.com