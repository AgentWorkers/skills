---
name: sms
version: 1.0.0
author: BytesAgain
license: MIT-0
tags: [sms, tool, utility]
---

# SMS

SMS工具包 — 支持发送消息、管理联系人、模板管理、追踪消息送达情况、批量发送消息以及查看对话记录。

## 命令

| 命令 | 描述 |
|---------|-------------|
| `sms run` | 执行主功能 |
| `sms list` | 列出所有项目 |
| `sms add <项目>` | 添加新项目 |
| `sms status` | 显示当前状态 |
| `sms export <格式>` | 导出数据 |
| `sms help` | 显示帮助信息 |

## 使用方法

```bash
# Show help
sms help

# Quick start
sms run
```

## 示例

```bash
# Run with defaults
sms run

# Check status
sms status

# Export results
sms export json
```

## 工作原理

该工具包使用内置逻辑处理输入数据，并输出结构化结果。所有数据均存储在本地。

## 提示

- 可通过运行`sms help`查看所有命令的详细信息 |
- 数据存储在`~/.local/share/sms/`目录下 |
- 基本功能无需API密钥 |
- 支持离线使用

---
*由BytesAgain提供支持 | bytesagain.com*