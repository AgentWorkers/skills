---
name: font
version: 1.0.0
author: BytesAgain
license: MIT-0
tags: [font, tool, utility]
---

# 字体管理工具包

该工具包提供了一系列功能，用于预览字体、查找字体搭配、检查字体可用性、生成字体组合、比较字体粗细，以及生成相应的CSS代码片段。

## 命令

| 命令          | 描述                                      |
|---------------|-----------------------------------------|
| `font preview`     | 预览指定字体                              |
| `font pair`     | 查找适合搭配使用的字体对                        |
| `font stack`     | 生成包含多种字体的组合                         |
| `font compare`    | 比较两个字体的视觉效果                        |
| `font weights`    | 显示指定字体的不同粗细级别                     |
| `font css`     | 生成用于网页设计的CSS代码                         |

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

## 工作原理

该工具包会读取用户输入的数据，通过内置逻辑进行处理，并输出结构化结果。所有数据均存储在本地（除非用户进行了外部API调用的配置）。因此，无需依赖任何外部服务。

## 使用技巧

- 使用 `font help` 命令可查看所有可用命令的详细信息。
- 所有数据均保存在用户的工作区中，无需使用API密钥即可使用基本功能。
- 该工具包支持离线使用。

---
*由BytesAgain提供支持 | bytesagain.com*