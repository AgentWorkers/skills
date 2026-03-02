---
name: toon-adoption
description: 通过采用紧凑的 TOON 格式来存储数据和上下文信息，从而优化令牌的使用效率。
version: 1.0.0
author: Agent Zero Community
tags: [token-optimization, toon, format, efficiency]
---
# TOON 采用技巧

## 描述
使用基于令牌的对象表示法（Token-Oriented Object Notation, TOON）高效地解析、生成和存储数据。TOON 是为大型语言模型（LLMs）设计的，它是一种无损的数据表示方式，能够通过缩进、减少引号的使用以及采用表格布局等方式将 JSON 数据的令牌使用量降低约 40%。

## TOON 语法规则

### 1. 基于缩进的嵌套
- 使用两个空格的缩进来定义层次结构，类似于 YAML 的方式。
- 除非需要定义表格结构，否则避免使用大括号 `{}` 和方括号 `[]` 来进行嵌套。

### 2. 最小化引号的使用
- 键和值通常不需要引号，除非它们包含逗号或大量的前导/尾随空白字符。

### 3. 明确指定数组长度
- 使用 `[N]` 的格式来声明数组中的元素数量（例如：`friends[3]`）。

### 4. 表格格式的数组（对象数组）
- 对于结构统一的对象数组，使用以下格式：`key[N]{field1,field2,...}:`。
- 在头部列出字段名称，然后使用逗号分隔各行的值。

### 5. 编码
- 始终使用 UTF-8 编码。

## 代理使用指南
1. **存储**：优先使用 `.toon` 文件来存储日志、计划信息以及长期数据。
2. **上下文压缩**：在总结历史记录或笔记时，使用 TOON 将更多信息压缩到上下文窗口中。
3. **解析**：将缩进理解为嵌套的对象层级，将 CSV 行解析为与头部结构匹配的对象。

## 示例文档
```toon
metadata:
  name: Sample Configuration
  format: TOON
  efficiency_gain: 0.4
goals[3]{id,title,category}:
  1,Lose weight,health
  2,Increase self-esteem,personal
  3,Get out of loneliness,social
```