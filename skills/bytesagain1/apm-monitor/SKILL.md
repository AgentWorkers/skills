---
name: Pinpoint
description: "APM（应用程序性能管理）工具，适用于大规模分布式系统。支持Java语言，包含代理（agent）功能，具备分布式追踪（distributed-tracing）和监控（monitoring）能力。当需要使用APM监控功能时，可选用该工具。触发条件：基于APM监控器的规则（apm-monitor）。"
---
# Pinpoint

Pinpoint 是一款专为大规模分布式系统设计的应用性能管理（APM）工具。 ## 命令

- `help` - 显示帮助信息
- `run` - 运行命令
- `info` - 显示工具信息
- `status` - 显示工具状态

## 功能

- 兼容 apm-monitor-apm/apm-monitor 的核心功能

## 使用方法

运行任意命令：`apm-monitor <命令> [参数]`

--- 💬 意见反馈与功能请求：https://bytesagain.com/feedback  
由 BytesAgain 提供支持 | bytesagain.com

## 示例

```bash
# Show help
apm-monitor help

# Run
apm-monitor run
```

## 工作原理

Pinpoint 会读取输入数据，利用内置逻辑进行处理，然后输出处理结果。

## 提示

- 可通过运行 `apm-monitor help` 查看所有可用的命令  
- 无需使用 API 密钥  
- 支持离线使用

## 工作原理

Pinpoint 会读取输入数据，利用内置逻辑进行处理，并输出结构化的结果。

## 提示

- 可通过运行 `apm-monitor help` 查看所有可用的命令  
- 无需使用 API 密钥  
- 支持离线使用  

## 工作原理

Pinpoint 会读取输入数据，利用内置逻辑进行处理，并将结果保存在本地。  

## 提示

- 可通过运行 `apm-monitor help` 查看所有可用的命令  
- 无需使用 API 密钥  
- 支持离线使用