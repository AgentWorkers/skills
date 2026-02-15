---
name: qmd
description: 使用 qmd 从本地知识库中搜索和检索 Markdown 文档。支持 BM25 关键词搜索、向量语义搜索以及结合大型语言模型（LLM）进行重新排序的混合搜索功能。适用于查询已索引的笔记、文档、会议记录以及任何基于 Markdown 的知识内容。需要先安装 qmd 命令行工具（通过 `bun install -g https://github.com/tobi/qmd` 进行安装）。
---

# QMD - 本地 Markdown 搜索工具

该工具用于从本地索引的 Markdown 知识库中搜索和检索文档。

## 安装

```bash
bun install -g https://github.com/tobi/qmd
```

## 设置

```bash
# Add a collection
qmd collection add ~/notes --name notes --mask "**/*.md"

# Generate embeddings (required for vsearch/query)
qmd embed
```

## 使用规则

在调用 qmd 命令时，**务必使用 `--json` 标志** 以获得结构化的输出结果。

## 搜索命令

### search （基于 BM25 算法的快速关键词搜索）

```bash
qmd search "authentication flow" --json
qmd search "error handling" --json -n 10
qmd search "config" --json -c notes
```

### vsearch （基于向量语义的搜索）

```bash
qmd vsearch "how does login work" --json
qmd vsearch "authentication best practices" --json -n 20
```

### query （结合大型语言模型（LLM）进行重新排序的混合搜索方式——最高质量的结果）

```bash
qmd query "implementing user auth" --json
qmd query "deployment process" --json --min-score 0.5
```

### 搜索选项

| 选项 | 描述 |
|--------|-------------|
| `-n 数量` | 返回的结果数量（默认值为 5，使用 `--json` 时为 20） |
| `-c, --collection 名称` | 限制搜索范围至特定集合 |
| `--min-score 分数` | 最小得分阈值 |
| `--full` | 在结果中返回完整的文档内容 |
| `--all` | 返回所有匹配项 |

## 检索命令

### get （获取单篇文档）

```bash
qmd get docs/guide.md --json
qmd get "#a1b2c3" --json
qmd get notes/meeting.md:50 -l 100 --json
```

### multi-get （获取多篇文档）

```bash
qmd multi-get "docs/*.md" --json
qmd multi-get "api.md, guide.md, #abc123" --json
qmd multi-get "notes/**/*.md" --json --max-bytes 20480
```

## 维护命令

```bash
qmd update              # Re-index changed files
qmd status              # Check index health
qmd collection list     # List all collections
```

## 搜索模式选择

| 模式 | 速度 | 质量 | 适用场景 |
|------|-------|---------|----------|
| search | 快速 | 良好 | 精确的关键词、已知术语 |
| vsearch | 中等 | 更好 | 概念性查询、同义词搜索 |
| query | 慢速 | 最佳 | 复杂问题、不确定的术语 |

**性能说明：** `vsearch` 和 `query` 在初始化向量数据时会有约 1 分钟的延迟。对于交互式使用，建议选择 `search` 模式。

## MCP 服务器

qmd 可以作为 MCP 服务器运行，以实现直接集成：

```bash
qmd mcp
```

提供的工具包括：`qmd_search`、`qmd_vsearch`、`qmd_query`、`qmd_get`、`qmd_multi_get`、`qmd_status`