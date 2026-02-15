---
name: engram
description: 使用 Pinecone 和 Gemini 嵌入技术，为本地知识库提供语义搜索功能。
---

# 🧠 Engram - 语义搜索技能

该技能使 AI 代理能够在本地 Markdown 文件夹（例如 Obsidian 文档库）中执行语义搜索。它根据查询的含义和上下文来查找信息，而不仅仅是精确的关键词。

## 工具

### engram_search

用于搜索索引的知识库：

-   **`query`**（字符串，必填）：需要提出的问题。
-   **`top_k`**（数字，可选）：返回的结果数量。
-   **`min_score`**（数字，可选）：结果的最小相关性得分（范围为 0.0 到 1.0）。

### engram_index

用于从本地 Markdown 文件中构建或更新搜索索引。应定期运行此工具以保持搜索索引的同步。

## 开发者

-   **Andrie Wijaya** ([@Anwitch](https://github.com/Anwitch))