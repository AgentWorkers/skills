---
name: crawler
version: 1.0.0
author: BytesAgain
license: MIT-0
tags: [crawler, tool, utility]
---

# Crawler

这是一个用于网站爬取的工具包，支持站点爬取、链接提取、内容抓取、站点地图生成、速率限制以及数据导出等功能。

## 命令

| 命令 | 描述 |
|---------|-------------|
| `crawler run` | 执行主功能 |
| `crawler list` | 显示所有项目列表 |
| `crawler add <项目>` | 添加新项目 |
| `crawler status` | 显示当前状态 |
| `crawler export <格式>` | 导出数据 |
| `crawler help` | 显示帮助信息 |

## 使用方法

```bash
# Show help
crawler help

# Quick start
crawler run
```

## 示例

```bash
# Run with defaults
crawler run

# Check status
crawler status

# Export results
crawler export json
```

## 工作原理

该工具包使用内置逻辑处理输入数据，并输出结构化的结果。所有数据均存储在本地。

## 提示

- 可通过运行 `crawler help` 查看所有命令的详细信息 |
- 数据存储在 `~/.local/share/crawler/` 目录下 |
- 基本功能无需使用 API 密钥 |
- 支持离线使用

---
*由 BytesAgain 提供支持 | bytesagain.com*