---
name: wireframe
version: 1.0.0
author: BytesAgain
license: MIT-0
tags: [wireframe, tool, utility]
---

# Wireframe

Wireframe生成工具——用于创建ASCII格式和基于文本的线框图、页面布局图、组件草图、用户流程图，并支持导出到多种格式。

## 命令

| 命令 | 描述 |
|---------|-------------|
| `wireframe page` | 创建一个新的页面线框图 |
| `wireframe component` | 创建一个新的组件线框图 |
| `wireframe flow` | 创建用户流程图 |
| `wireframe export` | 将线框图导出为指定格式 |
| `wireframe templates` | 查看或管理线框图模板 |
| `wireframe annotate` | 为线框图添加注释 |

## 使用方法

```bash
# Show help
wireframe help

# Quick start
wireframe page <type>
```

## 示例

```bash
# Example 1
wireframe page <type>

# Example 2
wireframe component <name>
```

## 工作原理

该工具会读取用户输入的数据，通过内置逻辑进行处理，并生成结构化的输出结果。所有数据都存储在本地（除非用户进行了额外的配置），因此无需调用任何外部API。

## 提示

- 使用 `wireframe help` 命令可查看所有可用命令的详细信息 |
- 所有数据都存储在工作区中 |
- 基本功能无需使用API密钥 |
- 支持离线使用

---
*由BytesAgain提供支持 | bytesagain.com*