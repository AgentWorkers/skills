---
name: MindMap
description: "基于文本的思维导图工具：用于创建、组织和可视化想法，支持将思维导图以树形结构呈现。支持导出为Markdown格式。无需图形用户界面（GUI）。"
version: "1.0.0"
author: "BytesAgain"
tags: ["mindmap","brainstorm","ideas","organize","thinking","productivity"]
---# MindMap
在终端中创建并可视化思维导图。

## 命令
- `create <名称>` — 创建新的思维导图
- `add <地图名称> <父节点> <节点名称>` — 添加节点（使用“root”表示顶级节点）
- `show <名称>` — 显示思维导图结构
- `list` — 列出所有思维导图
- `export <名称>` — 将思维导图导出为Markdown格式

---

由 BytesAgain 提供支持 | bytesagain.com

## 示例

```bash
# Show help
mindmap help

# Run
mindmap run
```

- 运行 `mindmap help` 可以查看所有命令
- 无需API密钥

- 运行 `mindmap help` 可以查看所有命令的详细信息

---

## 使用场景
- 从终端快速创建思维导图
- 用于自动化流程

## 输出结果
输出结果会显示在标准输出（stdout）中。可以使用 `mindmap run > output.txt` 将结果保存到文件中。

## 配置
可以通过设置 `MINDMAP_DIR` 来更改数据存储目录。默认值为：`~/.local/share/mindmap/`

---

*由 BytesAgain 提供支持 | bytesagain.com*
*反馈与功能请求：https://bytesagain.com/feedback*