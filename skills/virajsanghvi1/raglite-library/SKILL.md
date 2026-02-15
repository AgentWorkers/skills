---
name: raglite
version: 1.0.0
description: "**本地优先的RAG缓存机制：**  
将文档内容转化为结构化的Markdown格式，随后通过Chroma工具进行索引和查询，该查询机制结合了向量搜索和关键词搜索技术。"
metadata:
  {
    "openclaw": {
      "emoji": "🔎",
      "os": ["darwin", "linux"],
      "requires": { "bins": ["python3", "pip"] }
    }
  }
---

# RAGLite — 一个本地 RAG 缓存（并非内存替代品）

RAGLite 是一个 **以本地数据为主导的 RAG 缓存系统**。它 **不会** 替代模型的内存或聊天过程中的上下文数据**，而是为你的智能代理提供了一个持久性的存储空间，用于存储和检索模型未训练过的数据——尤其适用于存储 **本地/私有信息**（如学校作业、个人笔记、医疗记录、内部运行手册等）。

## 为什么它比付费的 RAG 服务/知识库更优秀（适用于许多使用场景）：

- **优先使用本地数据**：将敏感数据保存在本地机器或网络中。
- **基于开源技术构建**：使用 **Chroma** 🧠 和 **ripgrep** ⚡，无需依赖任何托管的向量数据库。
- **在嵌入数据前进行压缩**：先对数据进行压缩处理，减少冗余信息，从而生成更简洁、更高效的查询提示，并提升检索的可靠性。
- **可审计的存储格式**：压缩后的 Markdown 文档易于人类阅读且版本可控。

如果你后续需要扩展存储空间，可以更换为托管的数据库，但实际上大多数情况下并不需要这样做。

## RAGLite 的主要功能：

### 1) 数据压缩 ✍️
将文档转换为结构化的 Markdown 格式，去除冗余内容，只保留关键信息。

### 2) 数据索引 🧠
将压缩后的数据嵌入到 **Chroma** 数据库中（一个数据库可以存储多个数据集）。

### 3) 数据查询 🔎
支持混合检索方式：
- 通过 **Chroma** 进行向量相似度查询；
- 通过 `ripgrep` （`rg` 命令）进行关键词匹配。

## 默认引擎

除非你明确指定 `--engine` 参数，否则该技能默认使用 **OpenClaw** 🦞 作为数据压缩工具。

## 前置要求：

- **Python 3.11 或更高版本**。
- **索引/查询功能**：需要能够访问 **Chroma** 服务器（默认地址：`http://127.0.0.1:8100`）。
- **关键词搜索功能**：需要安装 `ripgrep`（通过 `brew install ripgrep` 安装）。
- **使用 OpenClaw 引擎**：需要确保 OpenClaw Gateway（地址：`/v1/responses`）可访问，并设置 `OPENCLAW_GATEWAY_TOKEN`（如果 Gateway 需要身份验证的话）。

## 安装（技能运行时）

RAGLite 会被安装到技能对应的虚拟环境中（`skill-local venv`）：

```bash
./scripts/install.sh
```

RAGLite 可以通过 GitHub 安装：
- `git+https://github.com/VirajSanghvi1/raglite.git@main`

## 使用方法：

### 推荐的单一命令使用方式

```bash
./scripts/raglite.sh run /path/to/docs \
  --out ./raglite_out \
  --collection my-docs \
  --chroma-url http://127.0.0.1:8100 \
  --skip-existing \
  --skip-indexed \
  --nodes
```

### 数据查询

```bash
./scripts/raglite.sh query ./raglite_out \
  --collection my-docs \
  --top-k 5 \
  --keyword-top-k 5 \
  "rollback procedure"
```

## 输出结果：

安装完成后，系统会生成以下文件：
- `*.tool-summary.md`
- `*.execution-notes.md`
- 可选：`*.outline.md`
- 可选：`*/nodes/*.md`，以及每个文档对应的 `*.index.md` 和根目录下的 `index.md`
- 元数据文件位于 `.raglite/` 目录中（包含缓存信息、运行统计数据和错误日志）。

## 常见问题解决方法：

- **无法访问 Chroma 服务器**：检查 `--chroma-url` 参数是否正确设置，并确保 Chroma 服务正在运行。
- **关键词查询无结果**：请确保已安装 `ripgrep`（运行 `rg --version` 检查版本）。
- **OpenClaw 引擎出现错误**：确认 Gateway 正在运行，并检查 `OPENCLAW_GATEWAY_TOKEN` 环境变量是否已设置。

## RAGLite 的优势（适用于 ClawHub 的产品介绍）：

RAGLite 是一个专为重复查询设计的 **本地 RAG 缓存系统**。当你或你的智能代理需要反复查找非训练数据（如本地笔记、学校作业、医疗记录等）时，RAGLite 为你提供了一个私密且可审计的数据存储解决方案：
1. **数据压缩**：将文档压缩为结构化的 Markdown 格式，减少存储空间。
2. **本地索引**：将压缩后的数据存储在本地 Chroma 数据库中。
3. **混合检索**：支持向量相似度查询和关键词搜索。

RAGLite 并不会替代模型的内存或聊天过程中的上下文数据，而是为你提供一个方便、可靠的私有数据存储解决方案。