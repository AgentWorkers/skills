---
name: PerfTest
description: "性能测试与基准测试工具。用于测量命令执行时间、评估磁盘I/O性能、测试网络吞吐量、比较不同命令的执行效率，并生成相应的报告。"
version: "1.0.0"
author: "BytesAgain"
tags: ["benchmark","performance","speed","test","profiling"]
categories: ["Developer Tools", "Utility"]
---# PerfTest

这是一个用于性能测试和基准测试的工具。它可以测量命令的执行时间、测试磁盘I/O性能、评估网络吞吐量、比较不同命令的性能，并生成相应的报告。

## 快速入门

运行 `perftest help` 可以查看可用的命令及其使用示例。

## 主要特性

- 快速且轻量级：基于纯Bash脚本，内置了Python功能
- 不需要任何外部依赖
- 所有配置文件都存储在 `~/.perftest/` 目录下
- 支持Linux和macOS操作系统

## 使用方法

```bash
perftest help
```

---
💬 您的意见对我们非常重要：https://bytesagain.com/feedback
由BytesAgain提供支持 | bytesagain.com

- 通过运行 `perftest help` 可以查看所有可用的命令

## 配置

您可以通过设置 `PERFTEST_DIR` 来更改数据存储目录。默认目录为 `~/.local/share/perftest/`