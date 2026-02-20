---
name: index1
description: 用于编码代理的AI内存系统：代码索引与认知信息，可在会话之间持续保存。
version: 2.0.3
license: Apache-2.0
author: gladego
tags: [mcp, memory, semantic-search, bm25, rag, cognitive, coding-agent]
---
# index1

这是一个专为编码代理设计的AI内存系统，采用BM25与向量混合搜索技术。它提供了6个MCP工具，用于智能代码/文档搜索以及认知事实的记录。

## 功能介绍

- **双内存架构**：包含代码索引（corpus）和认知数据（episodic facts）。
- **混合搜索机制**：结合BM25全文搜索与基于向量语义的搜索，并通过RRF（Ranking and Retrieval Fusion）算法进行融合。
- **结构感知的分块处理**：支持Markdown、Python、Rust、JavaScript等多种语言格式的文件。
- **MCP服务器**：提供6个核心工具（`recall`、`learn`、`read`、`status`、`reindex`、`config`）。
- **针对中文/日文/韩文的优化**：支持中文、日文、韩文查询，并可动态调整权重。
- **内置ONNX嵌入功能**：无需额外安装Ollama模型，即可直接使用向量搜索功能。
- **优雅的降级方案**：即使没有嵌入服务，也能仅使用BM25模式正常运行。

## 安装

```bash
# Recommended
pipx install index1

# Or via pip
pip install index1

# Or via npm (auto-installs Python package)
npx index1@latest
```

一键插件安装方法：

```bash
index1 setup                 # Auto-configure hooks + MCP for Claude Code
```

安装完成后，请进行验证：

```bash
index1 --version
index1 doctor        # Check environment
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

> 如果`index1`不在系统路径中，请使用`which index1`命令获取其完整路径。

## 添加搜索规则

将相关配置添加到项目的`.claude/CLAUDE.md`文件中：

```markdown
## Search Strategy

This project has index1 MCP Server configured (recall + 5 other tools). When searching code:

1. Known identifiers (function/class/file names) -> Grep/Glob directly (4ms)
2. Exploratory questions ("how does XX work") -> recall first, then Grep for details
3. CJK query for English code -> must use recall (Grep can't cross languages)
4. High-frequency keywords (50+ expected matches) -> prefer recall (saves 90%+ context)
```

## 系统影响

```
Without rules: Grep "search" -> 881 lines -> 35,895 tokens
With rules:    recall        -> 5 summaries -> 460 tokens (97% savings)
```

## 为项目创建索引

```bash
index1 index ./src ./docs    # Index source and docs
index1 status                # Check index stats
index1 search "your query"   # Test search
```

## 可选功能：多语言支持

index1 v2版本内置了ONNX嵌入功能（版本号bge-small-en-v1.5），可提升多语言支持能力：

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull nomic-embed-text           # Standard, 270MB
# or
ollama pull bge-m3                     # Best for CJK, 1.2GB

index1 config embed_backend ollama
index1 doctor                          # Verify setup
```

即使不安装Ollama，ONNX嵌入功能也能实现向量搜索。

## Web界面

```bash
index1 web                   # Start Web UI on port 6888
index1 web --port 8080       # Custom port
```

## MCP工具参考

| 工具 | 功能描述 |
|------|-------------|
| `recall` | 统一搜索功能：结合代码内容和认知事实，支持BM25与向量混合搜索 |
| `learn` | 记录见解、决策及经验教训（自动分类并去重） |
| `read` | 读取文件内容并查看索引元数据 |
| `status` | 提供索引和认知数据的统计信息 |
| `reindex` | 为指定路径或文件集合重建索引 |
| `config` | 查看或修改系统配置 |

## 常见问题与解决方法

| 问题 | 解决方案 |
|-------|-----|
| 工具无法使用 | 确认`.mcp.json`文件的格式是否正确，以及`index1`的路径是否正确 |
| AI搜索功能未生效 | 在`.claude/CLAUDE.md`文件中添加相应的搜索规则 |
| 命令无法执行 | 使用`which index1`命令获取`index1`的完整路径 |
| 中文搜索结果为空 | 请安装Ollama及`bge-m3`模型 |
| 无法使用向量搜索功能 | 确保已启用内置的ONNX嵌入功能；可以尝试运行`index1 doctor`命令进行检查。