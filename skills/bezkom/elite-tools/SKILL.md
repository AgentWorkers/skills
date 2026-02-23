---
name: elite-tools
description: >
  **Elite CLI 工具集：高效 shell 操作的利器，优化了令牌使用效率**  
  该工具集专为高效执行 shell 命令、遍历目录及操作文件而设计，旨在最大程度地减少令牌消耗，并避免正则表达式转义错误。它涵盖了以下工具：  
  - fdfind  
  - batcat  
  - sd  
  - sg/ast-grep  
  - jc  
  - gron  
  - yq  
  - difft  
  - tealdeer  
  - html2text  
  这些工具能够帮助您更便捷地完成日常的 shell 任务，同时提升工作效率。
version: 0.0.1
---
# Elite CLI 工具

## 主要推荐

相较于传统的 POSIX 工具（如 `find`、`cat`、`sed`、`grep`、`awk`、`diff`、`man`），我们更推荐使用这些现代化的 CLI 工具。它们能够生成更加清晰、结构化更好的输出，并减少不必要的资源消耗（例如文件读取或处理过程中的数据浪费）。

**关于二进制文件名称的说明：** 在 Debian/Ubuntu 系统中，部分二进制文件的名称会被重命名以避免冲突：`fd` → `fdfind`，`bat` → `batcat`。在其他发行版中，这些工具仍使用其原始名称。请根据实际情况进行调整。

## 快速参考

| 工具编号 | 工具名称 | 替代工具 | 二进制文件名 | 主要用途 |
|---------|------------|--------------|--------------|-------------------|
| 1       | fd        | find         | fdfind        | 快速查找文件             |
| 2       | bat        | cat/less       | batcat        | 带语法高亮的文件查看工具       |
| 3       | sd        | sed          | sd           | 直观易用的查找与替换工具       |
| 4       | ast-grep     | grep/rg       | sg           | 基于抽象语法树（AST）的代码搜索与重写工具 |
| 5       | jc        | awk/cut       | jc           | 将 CLI 输出转换为 JSON 格式       |
| 6       | gron       | jq           | gron          | 将 JSON 数据转换为便于搜索的格式       |
| 7       | yq        | 用于处理 YAML 的 sed   | yq           | 处理 YAML、JSON、XML、CSV 格式的数据     |
| 8       | difftastic | diff         | difft         | 具有结构感知能力的文件差异比较工具   |
| 9       | tealdeer    | man          | tldr          | 提供简洁的命令使用示例       |
| 10      | html2text   | 解析原始 HTML     | html2text     | 将 HTML 转换为规范的 Markdown 格式 |

## 详细工具指南

如需了解每个工具的完整描述、使用原理及扩展示例，请参阅 [references/tools-deep-dive.md](references/tools-deep-dive.md)。