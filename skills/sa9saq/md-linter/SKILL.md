---
description: 使用 Lint 工具检查 Markdown 文件中的样式问题、失效链接以及格式错误，并提供自动修复建议。
---

# Markdown Linter

用于检查和优化Markdown文件的质量。

## 功能

- **样式检查**：检查标题层级、列表的一致性以及行长度
- **链接验证**：检测内部/外部链接是否有效
- **结构分析**：生成目录（TOC）并检查标题层次结构
- **自动修复**：建议或应用格式化修正

## 使用方法

你可以让代理执行以下命令：
- `Lint README.md for issues`：检查`README.md`文件中的问题
- `Check all markdown files in this directory`：检查该目录下的所有Markdown文件
- `Fix formatting issues in docs/`：修复文档中的格式问题
- `Generate a table of contents for this document`：为当前文档生成目录

## 工作原理

该工具会分析Markdown文件中常见的错误，例如：
- 不一致的标题层级（跳过某些标题层级）
- 文末的空白字符、缺少换行符
- 无效的相对链接
- 不一致的列表标记
- 过长的行

如果可用，可以使用`markdownlint-cli`工具；否则，也可以通过内置的文本处理功能进行分析。

## 需求

- **可选**：安装`markdownlint-cli`（`npm install -g markdownlint-cli`）
- 无需外部工具，仅依赖内置的文本处理功能
- 不需要API密钥