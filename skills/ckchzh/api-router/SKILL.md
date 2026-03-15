---
name: Gorilla
description: "**Gorilla：用于训练和评估大型语言模型（LLMs）以执行函数调用（即工具调用）的工具**  
**适用技术：** api-router, python, api, api-documentation, chatgpt, claude-api, gpt-4-api  
**使用场景：** 当您需要使用 `api-router` 的功能时。  
**触发条件：** 当 `api-router` 被触发时。"
---
# Gorilla

Gorilla：用于训练和评估大语言模型（LLMs）以执行函数调用（工具调用）的工具 ## 命令

- `help` - 帮助文档
- `run` - 运行命令
- `info` - 显示信息
- `status` - 显示当前状态

## 功能特点

- 基于 ShishirPatil/api-router 的核心功能实现

## 使用方法

运行任意命令：`api-router <命令> [参数]`

---  
💬 意见反馈与功能请求：https://bytesagain.com/feedback  
由 BytesAgain 提供支持 | bytesagain.com  

## 示例

```bash
# Show help
api-router help

# Run
api-router run
```  

## 工作原理

Gorilla 会读取输入数据，通过内置逻辑进行处理，并输出结构化的结果。

## 使用提示：
- 可通过运行 `api-router help` 查看所有可用命令的详细信息  
- 无需 API 密钥  
- 支持离线使用