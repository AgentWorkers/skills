---
name: qmd
description: 本地混合搜索功能，适用于Markdown笔记和文档的查询。该功能可用于搜索笔记、查找相关内容，或从索引化的集合中检索文档。
homepage: https://github.com/tobi/qmd
metadata: {"clawdbot":{"emoji":"🔍","os":["darwin","linux"],"requires":{"bins":["qmd"]},"install":[{"id":"bun-qmd","kind":"shell","command":"bun install -g https://github.com/tobi/qmd","bins":["qmd"],"label":"Install qmd via Bun"}]}}
---

# qmd - 快速 Markdown 搜索工具

这是一个用于搜索 Markdown 笔记、文档和知识库的本地搜索引擎。只需进行一次索引，即可实现快速搜索。

## 使用场景（触发短语）

- “搜索我的笔记/文档/知识库”
- “查找相关笔记”
- “从我的收藏中检索 Markdown 文档”
- “搜索本地的 Markdown 文件”

## 默认行为（重要说明）

- 首选使用 `qmd search`（基于 BM25 算法的快速匹配）。通常响应速度非常快，应作为默认选项。
- 仅在关键词搜索失败且需要语义相似性时使用 `qmd vsearch`（该方式在首次启动时可能会非常耗时）。
- 除非用户明确要求最高质量的混合搜索结果并能够接受较长的运行时间/超时，否则避免使用 `qmd query`。

## 先决条件

- 必须安装 Bun 版本 1.0.0 或更高。
- macOS 用户需通过 `brew install sqlite` 安装 SQLite 扩展。
- 确保系统路径中包含 `$HOME/.bun/bin`。

**在 macOS 上安装 Bun：** `brew install oven-sh/bun/bun`

## 安装方法**

`bun install -g https://github.com/tobi/qmd`

## 设置方法

```bash
qmd collection add /path/to/notes --name notes --mask "**/*.md"
qmd context add qmd://notes "Description of this collection"  # optional
qmd embed  # one-time to enable vector + hybrid search
```

## 支持的索引类型

- 该工具主要针对 Markdown 文件进行索引（通常为 `**/*.md` 格式的文件）。
- 在测试中，即使 Markdown 文件的结构较为混乱（包含大量内容），也不会影响搜索效果；搜索过程基于文件内容进行分块处理（每个分块大约包含几百个字符），而不严格依赖标题或结构。
- 该工具不能替代代码搜索工具（用于搜索代码仓库或源代码树中的内容）。

## 搜索模式

- `qmd search`（默认模式）：基于 BM25 算法的快速关键词匹配。
- `qmd vsearch`（备用模式）：基于语义相似性的搜索。由于在查询前需要使用本地大型语言模型（LLM）进行处理，因此搜索速度较慢。
- `qmd query`（较少使用）：结合语义搜索和 LLM 重新排序的结果。通常比 `vsearch` 更慢，且可能容易超时。

## 性能说明

- `qmd search` 的响应速度通常非常快。
- 在某些设备上，`qmd vsearch` 的搜索时间可能长达约 1 分钟，因为该模式需要在每次查询时将本地模型（例如 Qwen3-1.7B）加载到内存中；不过模型本身的查找速度较快。
- `qmd query` 在 `vsearch` 的基础上增加了 LLM 重新排序的步骤，因此性能更差，不适合交互式使用。
- 如果需要频繁进行语义搜索，可以考虑保持相关进程/模型的运行状态（例如，如果系统支持，可以设置长时间运行的 qmd/MCP 服务器模式），以避免每次搜索时都重新启动 LLM。

## 常用命令

```bash
qmd search "query"             # default
qmd vsearch "query"
qmd query "query"
qmd search "query" -c notes     # Search specific collection
qmd search "query" -n 10        # More results
qmd search "query" --json       # JSON output
qmd search "query" --all --files --min-score 0.3
```

## 有用的选项

- `-n <num>`：限制返回的结果数量
- `-c, --collection <name>`：仅搜索指定集合中的内容
- `--all --min-score <num>`：返回得分高于指定阈值的所有匹配项
- `--json` / `--files`：输出结果为 JSON 或文件格式
- `--full`：返回完整的文档内容

## 文档检索方法

```bash
qmd get "path/to/file.md"       # Full document
qmd get "#docid"                # By ID from search results
qmd multi-get "journals/2025-05*.md"
qmd multi-get "doc1.md, doc2.md, #abc123" --json
```

## 维护说明

```bash
qmd status                      # Index health
qmd update                      # Re-index changed files
qmd embed                       # Update embeddings
```

### 更新索引

建议设置定时任务或钩子来自动更新索引。例如，可以设置每天凌晨 5 点自动重新索引：

```bash
# Via Clawdbot cron (isolated job, runs silently):
clawdbot cron add \
  --name "qmd-reindex" \
  --cron "0 5 * * *" \
  --tz "America/New_York" \
  --session isolated \
  --message "Run: export PATH=\"\$HOME/.bun/bin:\$PATH\" && qmd update && qmd embed" 

# Or via system crontab:
0 5 * * * export PATH="$HOME/.bun/bin:$PATH" && qmd update && qmd embed
```

这样可以确保您的搜索功能始终与最新的笔记内容保持同步。

## 模型与缓存机制

- 该工具使用本地的 GGUF 模型；首次运行时会自动下载这些模型。
- 默认缓存路径为 `~/.cache/qmd/models/`（可通过 `XDG_CACHE_HOME` 配置自定义缓存路径）。

## 与 Clawdbot 的关系

- `qmd` 用于搜索您手动添加到集合中的本地 Markdown 文件。
- Clawdbot 的 `memory_search` 用于搜索用户之前的交互记录（保存在内存中的信息）。
- 可以同时使用这两种工具：`memory_search` 用于查询“我们之前做出了什么决定/学到了什么？”，`qmd` 用于查询“我的本地笔记/文档中有什么内容？”。