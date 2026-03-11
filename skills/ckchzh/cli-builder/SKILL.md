---
name: CLI Builder
description: CLI工具生成器：负责项目框架的搭建、命令的添加、参数解析、帮助文档的生成、配置文件的处理、发布前的检查列表的生成、交互式提示的提供以及彩色输出的功能。支持Python、Node.js、Bash和Go语言。相关技术包括`cli`（命令行接口）、`argparse`（命令行参数解析库）、`commander`（命令行工具框架）以及开发工具（developer-tools）。
---
# CLI Builder — 命令行工具生成器

> 从零开始构建专业的命令行工具，覆盖完整的开发生命周期

## 快速入门

```bash
bash scripts/cli-builder.sh init myapp python
bash scripts/cli-builder.sh command myapp serve "Start dev server"
bash scripts/cli-builder.sh args python --name,--port,--verbose
```

## 命令

| 命令 | 功能 | 参数 |
|---------|---------|-----------|
| `init` | 创建项目框架 | `<名称> <语言>` |
| `command` | 添加新命令 | `<应用程序> <命令> <描述>` |
| `args` | 参数解析器代码 | `<语言> <参数>` |
| `help` | 生成帮助文档 | `<应用程序> <命令>` |
| `config` | 处理配置文件 | `<语言> <格式>` |
| `publish` | 发布工具清单 | `<平台>` |
| `interactive` | 提供交互式提示 | `<语言> <提示内容>` |
| `color` | 为输出代码添加颜色格式 | `<语言>` |

## 支持的语言

- **Python** — argparse / click / typer
- **Node.js** — commander / yargs / inquirer
- **Bash** — getopts / case patterns
- **Go** — cobra / flag

## 输出结果

生成的所有代码都可以直接复制粘贴使用，其中包含注释和最佳实践指南。