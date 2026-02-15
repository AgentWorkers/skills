---
name: logseq-import
description: 将 Logseq 页面中的笔记导入到 Slipbox 中。当用户粘贴包含属性和项目符号笔记的 Logseq 页面时，该功能会自动执行：解析页面级别的属性，将每个项目符号提取为单独的笔记；对于嵌套的项目符号，会添加相应的父级上下文；最后对每个笔记使用 Slipbot 进行处理。
---

# Logseq 导入

解析 Logseq 页面，并为每个项目符号创建单独的便签条目。

## 重要规则：忽略所有标签

**不要从 Logseq 中导入任何标签**。这包括：
- 页面级别的 `tags::` 属性
- 项目符号内容中的内联 `#tags`
- `block-tags::` 元数据

Slipbot 会根据内容自动生成标签。Logseq 的标签可能会导致冲突。

## 输入格式

Logseq 页面分为两部分：

**1. 页面属性**（页面顶部，`key:: value` 格式）：
```
type:: #literature
source:: Book
author:: David Kadavy
title:: Digital Zettelkasten
alias:: zettelkasten-book
status::
tags::
```

**2. 项目符号笔记**（markdown 列表）：
```
- First note content here
- Second note with [[page ref]] link
  - Nested bullet under second
- Third note id:: abc123-uuid
```

## 属性映射

| Logseq 属性 | Slipbox 字段 |
|-----------------|---------------|
| `title::` | `source.title` |
| `source::` | `source.type`（如果是纯文本，如 "Book"） |
| `source:: [text](url)` | `source.title` + `source.url`（如果是 markdown 链接） |
| `author::` | `source.author` |
| `type:: #literature` | 笔记类型提示（映射到 `note`） |
| `alias::` | 忽略 |
| `status::` | 忽略 |
| `tags::` | **忽略**（Slipbot 会生成更合适的标签） |

空属性（例如，没有值的 `author::`） → `null`

## 解析规则

### 属性
1. 提取页面顶部的所有 `key:: value` 行
2. 遇到第一个项目符号（`- `）时停止解析
3. 从值中删除 `#`，例如 `#literature`
4. 解析 markdown 链接：`[text](url)` → 提取链接的两部分

### 项目符号
1. 每个顶级项目符号（`- `）都会成为一条独立的便签
2. **嵌套项目符号**：添加父级上下文，使其独立
   - 父级示例：`- [[Fleeting Notes]]: 随处记录的快速笔记`
   - 子级示例：`  - 可以是纸质或数字形式`
   - 结果：`Fleeting Notes (随时记录的快速笔记) 可以是纸质或数字形式`
3. 从项目符号中删除 Logseq 元数据：
   - `id:: uuid` → 删除
   - `block-tags:: #xxx` → 完全删除
   - 内联标签 `#tag` → 完全删除（Slipbot 会生成自己的标签）
   - 错误的标签格式（如 `#{"{"`） → 删除
4. 将 `[[page refs]]` 转换为纯文本（可能的链接目标）

### 内容清理
- 从项目符号中删除末尾的 `id:: xxx`
- 完全删除 `block-tags:: xxx`
- 删除所有内联标签 `#tag`（Slipbot 会生成自己的标签）
- 保留 markdown 格式（加粗、斜体、代码）

## 工作流程

1. **预检查（导入前）**
   - 解析页面属性和项目符号（此时不创建笔记）
   - 根据标题、作者和内容主题生成页面的简要概述（1-2 句）
   - 统计将创建的笔记总数（包括独立的嵌套项目符号）
   - 向用户展示概述、笔记数量和来源信息
   - **请求确认**后再进行导入
   - 如果用户拒绝，则停止操作，不创建任何笔记

2. **解析页面**（确认后）
   - 提取页面属性 → 来源元数据
   - 提取所有项目符号 → 笔记列表
   - 通过添加父级上下文来处理嵌套项目符号

3. **对于每个项目符号**，调用 Slipbot 工作流程：
   - 使用 `- {content}` 作为前缀（表示笔记类型）
   - 包含来源信息：`~ {source.type}, {source.title} by {source.author}`
   - 由 Slipbot 处理文件名、标签、链接和图表更新

4. **报告结果**
   - 创建的笔记数量
   - 遇到的任何问题

## 示例

**输入：**
```
type:: #literature
source:: Book
author:: David Kadavy
title:: Digital Zettelkasten

- Rewriting ideas helps decide their importance
- [[Fleeting Notes]]: quick notes written anywhere
  - Can be captured on paper or digitally
- Keywords should be specific to the idea id:: abc123
```

**处理结果：**
1. 来源：`Book, "Digital Zettelkasten" by David Kadavy`
2. 提取的项目符号：
   - "重写想法有助于判断其重要性"
   - "Fleeting Notes: 随处记录的快速笔记"
   - "Fleeting Notes 可以是纸质或数字形式"（包含嵌套项目符号，添加了父级上下文）
   - "关键词应该具体针对想法"（删除了 `id`）

3. 每条笔记发送给 Slipbot 的格式为：
   - `- 重写想法有助于判断其重要性 ~ Book, Digital Zettelkasten by David Kadavy`
   - 等等

## 特殊情况
- **没有属性**：视为独立的笔记，不包含来源信息
- **深度嵌套的项目符号（3 层以上）**：扁平化处理，累积所有祖先的上下文
- **引用部分**（`## Citation:`）：忽略（与页面属性重复）
- **非项目符号内容**：忽略标题和项目符号外的段落
- **一个项目符号中有多个 `[[refs]]`：保留所有引用，并将其转换为纯文本