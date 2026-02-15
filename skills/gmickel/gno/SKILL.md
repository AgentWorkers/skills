---
name: gno
description: 搜索本地文档、文件、笔记和知识库。对目录进行索引，使用 BM25、向量或混合算法进行搜索；提供带有引用的人工智能答案。适用于用户需要查找文件、查询笔记、在本地文件夹中检索信息、设置文档搜索功能、构建知识库、实现 RAG（Retrieval, Augmentation, and Generation）/语义搜索，或希望为文档创建本地 Web 用户界面等情况。
allowed-tools: Bash(gno:*) Read
---

# GNO - 本地知识引擎

快速本地语义搜索。只需索引一次，即可立即进行搜索。无需使用云服务，也无需API密钥。

## 适用场景

- 用户需要搜索文件、文档或笔记。
- 用户希望在本地文件夹中查找信息。
- 用户需要为搜索目的创建文档索引。
- 用户需要搜索PDF文件、Markdown文档、Word文档或代码文件。
- 用户询问关于知识库（knowledge base）或RAG（Retrieval-Augmented Grammar）的设置。
- 用户希望对文件进行语义/向量搜索。
- 用户需要设置MCP（Machine Learning Proxy）以访问文档。
- 用户希望使用Web界面来浏览和搜索文档。
- 用户希望从文档中获取AI生成的答案。
- 用户需要对文档进行标记、分类或过滤。
- 用户需要查看文档之间的关联关系或知识图谱。

## 快速入门

```bash
gno init                              # Initialize in current directory
gno collection add ~/docs --name docs # Add folder to index
gno index                             # Build index (ingest + embed)
gno search "your query"               # BM25 keyword search
```

## 命令概览

| 分类        | 命令                                      | 描述                                                                                   |
|------------|---------------------------------------------------------|-------------------------------------------------------------------------|
| **搜索**      | `search`, `vsearch`, `query`, `ask`                        | 通过关键词、语义内容或AI生成答案来查找文档           |
| **链接**      | `links`, `backlinks`, `similar`, `graph`                   | 查看文档之间的关联关系并进行可视化            |
| **检索**     | `get`, `multi-get`, `ls`                          | 根据URI或ID获取文档内容                         |
| **索引**      | `init`, `collection add/list/remove`, `index`, `update`, `embed`       | 创建和维护文档索引                         |
| **标签**      | `tags`, `tags add`, `tags rm`                        | 对文档进行组织和过滤                         |
| **上下文**    | `context add/list/rm/check`                        | 添加上下文信息以提高搜索准确性                   |
| **模型**     | `models list/use/pull/clear/path`                    | 管理本地AI模型                         |
| **服务**      | `serve`                                      | 提供Web界面用于浏览和搜索                         |
| **MCP**     | `mcp`, `mcp install/uninstall/status`                   | 集成AI助手                         |
| **技能**      | `skill install/uninstall/show/paths`                     | 安装用于AI代理的技能                         |
| **管理**     | `status`, `doctor`, `cleanup`, `reset`, `vec`, `completion`       | 系统维护和诊断                         |

## 搜索模式

| 命令                | 执行速度 | 适用场景                                      |
|----------------------|-----------------------------------------|---------------------------------------------------------|
| `gno search`           | 即时       | 精确匹配关键词                         |
| `gno vsearch`          | 约0.5秒     | 查找相似概念                         |
| `gno query --fast`       | 约0.7秒     | 快速查询                         |
| `gno query`            | 约2-3秒     | 平衡性能（默认模式）                     |
| `gno query --thorough`      | 约5-8秒     | 适合复杂查询，具有较高的召回率                   |
| `gno ask --answer`       | 约3-5秒     | 生成包含引用信息的AI答案                   |

**重试策略**：首先使用默认搜索模式。如果没有结果，尝试重新表述查询语句，然后使用`--thorough`模式。

## 常用参数

```
-n <num>              Max results (default: 5)
-c, --collection      Filter to collection
--tags-any <t1,t2>    Has ANY of these tags
--tags-all <t1,t2>    Has ALL of these tags
--json                JSON output
--files               URI list output
--line-numbers        Include line numbers
```

## 全局参数

```
--index <name>    Alternate index (default: "default")
--config <path>   Override config file
--verbose         Verbose logging
--json            JSON output
--yes             Non-interactive mode
--offline         Use cached models only
--no-color        Disable colors
--no-pager        Disable paging
```

## 重要提示：更改后的文件处理

如果您编辑或创建了需要通过向量搜索来查找的文件，请注意：

```bash
gno index              # Full re-index (sync + embed)
# or
gno embed              # Embed only (if already synced)
```

`MCP gno.sync` 和 `gnocapture` 命令不会自动执行文件嵌入操作。请使用命令行界面（CLI）来手动嵌入文件。

## 参考文档

| 文档类型            | 文件名                                      |
|------------------|----------------------------------------|
| 完整的命令行参考（所有命令、选项、参数） | [cli-reference.md](cli-reference.md)       |
| MCP服务器设置与工具           | [mcp-reference.md](mcp-reference.md)         |
| 使用示例与最佳实践         | [examples.md](examples.md)                 |