---
name: password
version: 1.0.0
author: BytesAgain
license: MIT-0
tags: [password, tool, utility]
---

# 密码管理器

这款密码管理器能够生成强密码、检查密码的强度、在本地存储用户凭证、检测密码是否已被泄露，并支持安全地导出数据。

## 命令

| 命令          | 描述                          |
|--------------|---------------------------------------------|
| `password run`    | 执行主功能                        |
| `password list`   | 列出所有存储的密码项                    |
| `password add <item>` | 添加新的密码项                      |
| `password status` | 显示当前的状态                        |
| `password export <format>` | 以指定格式导出数据                     |
| `password help`   | 显示帮助信息                        |

## 使用方法

```bash
# Show help
password help

# Quick start
password run
```

## 示例

```bash
# Run with defaults
password run

# Check status
password status

# Export results
password export json
```

## 工作原理

该工具通过内置逻辑处理用户输入，并输出结构化的数据结果。所有数据均存储在本地。

## 提示

- 可通过运行 `password help` 查看所有命令的详细信息。
- 数据存储在 `~/.local/share/password/` 目录下。
- 基本功能无需使用 API 密钥。
- 支持离线使用。

---
*由 BytesAgain 提供支持 | bytesagain.com*

## 工作原理

该工具读取用户输入，利用内置逻辑进行处理，并输出处理结果。所有数据均保存在本地。

## 提示

- 可通过运行 `password help` 查看所有命令的详细信息。
- 无需使用 API 密钥。
- 支持离线使用。