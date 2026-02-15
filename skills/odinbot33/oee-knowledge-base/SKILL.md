# 🐾 知识库（RAG）——您的“第二大脑”

> 由 Odin's Eye Enterprises 开发 — 古老的智慧，现代的智能。

您可以保存任何内容，并能以语义方式检索它们。这是一个基于 RAG（Retrieval-Augmented Question Answering）技术的个人知识库，使用 SQLite 数据库和嵌入模型进行处理。

## 功能介绍

1. **导入内容** — 将文本、URL、文件和笔记保存到知识库中。
2. **查询** — 对您保存的所有内容进行语义搜索。
3. **检索信息** — 为任何问题提供相关的上下文信息。

## 常用指令

- “记住这个”
- “将这个内容保存到知识库中”
- “我知道关于……什么”
- “搜索我的笔记”
- “知识库查询”

## 使用方法

```bash
# Ingest text
python ingest.py "The key insight from today's meeting was..."

# Ingest from a file
python ingest.py --file notes.md

# Query the knowledge base
python query.py "What did we discuss about pricing?"

# Full KB management
python kb.py stats
python kb.py search "topic"
```

## 相关文件

- `kb.py` — 知识库的核心引擎（负责嵌入模型处理、数据存储和信息检索）
- `ingest.py` — 用于添加内容的命令行工具
- `query.py` — 用于搜索的命令行工具
- `kb.db` — 自动创建的 SQLite 数据库

## 系统要求

- Python 3.10 或更高版本
- 需要 `ANTHROPIC_API_KEY` 或 `OPENAI_API_KEY` 来使用嵌入模型

## 对于代理程序（Agents）的使用方法

- 保存信息：`python ingest.py "文本内容"`
- 检索信息：`python query.py "问题内容"`

<!-- 🐾 Muninn 永远不会忘记……