---
name: PerfTest
description: "性能测试与基准测试工具。用于测量命令执行时间、评估磁盘I/O性能、测试网络吞吐量、比较不同命令的执行效率，并生成相应的测试报告。"
version: "1.0.0"
author: "BytesAgain"
tags: ["benchmark","performance","speed","test","profiling"]
categories: ["Developer Tools", "Utility"]
---# PerfTest

这是一个用于性能测试和基准测试的工具。它可以测量命令的执行时间、测试磁盘I/O性能、评估网络吞吐量、比较不同命令的执行效率，并生成相应的报告。

## 快速入门

运行 `perftest help` 可以查看所有可用命令及其使用示例。

## 主要特性

- 快速且轻量级：基于纯Bash脚本，内置了Python功能
- 无需任何外部依赖
- 数据存储在本地路径 `~/.perftest/` 下
- 支持Linux和macOS操作系统

## 使用方法

```bash
perftest help
```

---
💬 您的意见和建议请发送至：https://bytesagain.com/feedback
由BytesAgain提供支持 | bytesagain.com

## 工作原理

该工具读取输入数据，通过内置逻辑进行处理后输出结果。所有测试数据均保存在本地。

## 使用技巧

- 通过运行 `perftest help` 可以了解所有可用的命令
- 无需使用API密钥
- 支持离线测试模式

---