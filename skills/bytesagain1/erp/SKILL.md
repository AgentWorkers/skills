---
name: erp
version: 1.0.0
author: BytesAgain
license: MIT-0
tags: [erp, tool, utility]
---

# ERP

企业资源规划工具包——用于管理业务流程、跟踪资源、进行库存规划、部门协调以及生成报告。

## 命令

| 命令 | 描述 |
|---------|-------------|
| `erp run` | 执行主功能 |
| `erp list` | 列出所有项目 |
| `erp add <项目>` | 添加新项目 |
| `erp status` | 显示当前状态 |
| `erp export <格式>` | 导出数据 |
| `erp help` | 显示帮助信息 |

## 使用方法

```bash
# Show help
erp help

# Quick start
erp run
```

## 示例

```bash
# Run with defaults
erp run

# Check status
erp status

# Export results
erp export json
```

- 运行 `erp help` 以查看所有命令的详细信息
- 数据存储在 `~/.local/share/erp/` 目录下

---
*由 BytesAgain 提供支持 | bytesagain.com*

- 运行 `erp help` 以查看所有命令的详细信息

## 输出结果

输出结果会显示在标准输出（stdout）中。可以使用 `erp run > output.txt` 将结果保存到文件中。

## 配置

通过设置 `ERP_DIR` 变量来更改数据存储目录。默认目录为 `~/.local/share/erp/`