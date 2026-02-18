---
name: index1
description: 基于人工智能（AI）的项目知识库。采用BM25算法与向量搜索技术相结合的混合搜索方式，通过MCP服务器实现。
version: 2.0.1
license: Apache-2.0
author: gladego
tags: [mcp, knowledge-base, semantic-search, bm25, rag, code-search]
---
# index1

这是一个基于AI的项目知识库，采用了BM25全文搜索技术与向量搜索技术的混合模式。它提供了5个MCP（Multi-Component Platform）工具，用于智能的代码和文档搜索。

## 功能介绍

- **混合搜索**：结合BM25全文搜索与基于向量的语义搜索，并通过RRF（Ranking and Retrieval Fusion）算法进行融合。
- **结构感知的分块处理**：支持Markdown、Python、Rust、JavaScript以及纯文本格式的文档。
- **MCP服务器**：包含5个工具（`docs_search`、`docs_get`、`docs_status`、`docs_reindex`、`docs_config`）。
- **针对中文、日语和韩语的优化**：能够检测这些语言的查询，并动态调整搜索权重。
- **优雅降级机制**：即使没有Ollama，也能仅使用BM25全文搜索功能正常运行。

## 安装

```bash
# Recommended
pipx install index1

# Or via pip
pip install index1

# Or via npm (auto-installs Python package)
npx index1@latest
```

## 配置MCP

在项目根目录下创建`.mcp.json`文件：

```json
{
  "mcpServers": {
    "index1": {
      "type": "stdio",
      "command": "index1",
      "args": ["serve"]
    }
  }
}
```

> 如果`index1`不在系统的PATH环境变量中，请使用`which index1`命令获取其完整路径。

## 添加搜索规则

将以下内容添加到项目的`.claude/CLAUDE.md`文件中：

```markdown
## Search Strategy

This project has index1 MCP Server configured (docs_search + 4 other tools). When searching code:

1. Known identifiers (function/class/file names) -> Grep/Glob directly (4ms)
2. Exploratory questions ("how does XX work") -> docs_search first, then Grep for details
3. CJK query for English code -> must use docs_search (Grep can't cross languages)
4. High-frequency keywords (50+ expected matches) -> prefer docs_search (saves 90%+ context)
```

## 使用效果

```
Without rules: Grep "search" -> 881 lines -> 35,895 tokens
With rules:    docs_search  -> 5 summaries -> 460 tokens (97% savings)
```

## 为项目创建索引

```bash
index1 index ./src ./docs    # Index source and docs
index1 status                # Check index stats
index1 search "your query"   # Test search
```

## 可选功能：向量搜索

如需进行语义搜索或跨语言搜索，请安装Ollama：

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull nomic-embed-text           # Standard, 270MB
# or
ollama pull bge-m3                     # Best for CJK, 1.2GB

index1 doctor                          # Verify setup
```

即使不安装Ollama，仅使用BM25全文搜索也能提供良好的搜索体验（延迟约60-80毫秒）。

## 可选功能：中文支持

```bash
pip install index1[chinese]
index1 doctor    # Check 6 shows CJK status
```

## Web用户界面

```bash
index1 web                   # Start Web UI on port 6888
index1 web --port 8080       # Custom port
```

## MCP工具参考

| 工具 | 功能描述 |
|------|-------------|
| `docs_search` | 结合BM25全文搜索与向量搜索，返回排序后的搜索结果 |
| `docs_get` | 根据ID获取指定文档的完整内容 |
| `docs_status` | 提供索引统计信息（文档数量、分块数量等） |
| `docs_reindex` | 为指定路径或文档集合重建索引 |
| `docs_config` | 查看或修改配置设置 |

## 常见问题与解决方法

| 问题 | 解决方案 |
|-------|-----|
| 工具无法使用 | 检查`.mcp.json`文件的格式及`index1`的路径是否正确 |
| AI未使用`docs_search`功能 | 确保在`.claude/CLAUDE.md`文件中添加了相应的搜索规则 |
| 命令无法执行 | 使用`which index1`命令获取`index1`的完整路径 |
| 中文搜索返回空结果 | 使用`pip install index1[chinese]`安装中文语言支持模块 |
| 无法使用向量搜索 | 安装Ollama并加载相应的模型 |