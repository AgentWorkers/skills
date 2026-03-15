---
name: font
version: 1.0.0
author: BytesAgain
license: MIT-0
tags: [font, tool, utility]
---

# 字体管理工具包

该工具包提供了一系列功能，用于预览字体、查找字体搭配、检查字体可用性、生成字体堆叠、比较字体粗细以及生成CSS代码片段。

## 命令

| 命令 | 描述 |
|---------|-------------|
| `font preview` | 预览指定字体 |
| `font pair` | 查找两种字体之间的搭配效果 |
| `font stack` | 生成包含多种字体的堆叠组合 |
| `font compare` | 比较两种字体的视觉效果 |
| `font weights` | 显示指定字体的不同粗细级别 |
| `font css` | 生成用于CSS的字体样式代码 |

## 使用方法

```bash
# Show help
font help

# Quick start
font preview <font>
```

## 示例

```bash
# Example 1
font preview <font>

# Example 2
font pair <font>
```

- 运行 `font help` 可查看所有可用命令。

---
*由 BytesAgain 提供支持 | bytesagain.com*

## 配置

通过设置 `FONT_DIR` 可更改数据目录。默认值：`~/.local/share/font/`

## 使用场景

- 从终端快速完成字体相关操作
- 用于自动化处理流程

## 输出结果

所有输出结果会显示在标准输出（stdout）中。若需保存结果，可执行 `font run > output.txt`。

## 配置

通过设置 `FONT_DIR` 可更改数据目录。默认值：`~/.local/share/font/`