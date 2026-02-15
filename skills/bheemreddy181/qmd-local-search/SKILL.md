---
name: qmd
description: 使用 qmd CLI 进行快速的本地搜索，可以查找 Markdown 文件、笔记和文档。它替代了传统的 `find` 命令来定位文件。该工具结合了 BM25 全文搜索、向量语义搜索以及大型语言模型（LLM）的重新排序功能，所有这些操作都在本地完成。适用于搜索文件、查找代码、定位文档或在已索引的集合中检索内容。
---

# qmd — 快速的本地Markdown搜索工具

## 使用场景

- **查找文件**：在大型目录中替代`find`命令使用，可避免搜索过程卡顿。
- **搜索笔记/文档**：在索引化的文件集合中进行语义搜索或关键词搜索。
- **代码查找**：查找代码实现、配置文件或特定模式。
- **收集上下文信息**：在回答问题前提取相关代码片段。

## 快速参考

### 搜索（最常用功能）

```bash
# Keyword search (BM25)
qmd search "alpaca API" -c projects

# Semantic search (understands meaning)
qmd vsearch "how to implement stop loss"

# Combined search with reranking (best quality)
qmd query "trading rules for breakouts"

# File paths only (fast discovery)
qmd search "config" --files -c kell

# Full document content
qmd search "pattern detection" --full --line-numbers
```

### 文件集合管理

```bash
# List collections
qmd collection list

# Add new collection
qmd collection add /path/to/folder --name myproject --mask "*.md,*.py"

# Re-index after changes
qmd update
```

### 文件下载

```bash
# Get full file
qmd get myproject/README.md

# Get specific lines
qmd get myproject/config.py:50 -l 30

# Get multiple files by glob
qmd multi-get "*.yaml" -l 50 --max-bytes 10240
```

### 输出格式

- `--files`：输出文件路径及搜索得分（适用于代码查找）。
- `--json`：以结构化格式输出代码片段。
- `--md`：输出Markdown格式的结果。
- `-n 10`：限制返回结果的数量。

## 使用技巧

1. **始终使用文件集合**（格式为`-c name`）来限定搜索范围。
2. 添加新文件后，请运行`qmd update`命令更新索引。
3. 可使用`qmd embed`命令启用向量搜索功能（只需一次操作，耗时几分钟）。
- 对于大型目录，建议使用`qmd search --files`而非`find`。

## 模型（自动下载）

- 嵌入模型：embeddinggemma-300M
- 重排序模型：qwen3-reranker-0.6b
- 生成模型：Qwen3-0.6B

所有模型均可在本地运行，无需使用API密钥。