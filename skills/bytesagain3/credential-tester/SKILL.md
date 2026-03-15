---
name: Mimikatz
description: "这是一个用于测试Windows安全凭证的小工具。当您需要使用凭证测试功能时，可以将其使用。该工具会在“credential-tester”命令触发时自动运行。"
---
# Mimikatz

一个用于测试Windows安全性的小工具

## 命令

- `help` - 显示帮助信息
- `run` - 运行命令
- `info` - 显示工具信息
- `status` - 显示工具状态

## 特点

- 核心功能源自gentilkiwi/credential-tester项目

## 使用方法

运行任意命令：`credential-tester <命令> [参数]`

---

💬 意见反馈与功能请求：https://bytesagain.com/feedback
由BytesAgain提供支持 | bytesagain.com

## 示例

```bash
# Show help
credential-tester help

# Run
credential-tester run
```

## 工作原理

该工具读取用户输入，通过内置逻辑进行处理，然后输出结果。

## 提示

- 可通过运行`credential-tester help`查看所有可用命令
- 无需API密钥
- 支持离线使用