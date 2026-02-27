---
name: md-docs-search
description: 使用 SQLite FTS5 对结构化的 Markdown 文档档案进行全文搜索。当您需要搜索由 “---” 分隔的大量 Markdown 文章时，该工具非常适用；这些文章中包含源代码链接（用 “*Source:” 标记）。它支持快速的 BM25 排序搜索，并能自动提取引用中的源代码链接。非常适合用于研究、文档查询和知识库探索。在使用前，需使用 `docs.py index` 命令对文档进行索引。
---
# Markdown 文档的全文搜索

使用 SQLite 的 FTS5 和 BM25 相关性排名算法，实现对 Markdown 文档档案的快速、索引化的全文搜索。

## 使用场景

- 在文档档案中搜索特定的功能、特性或信息
- 查找官方的源代码链接以供报告引用
- 查阅技术规范或配置细节
- 在多个文档来源中进行搜索

## 预期的文档格式

文章使用 `---` 作为分隔符，并附带 `*Source:` 指定的 URL：

```markdown
# Article Title

*Source: https://docs.example.com/path/to/article.html*

Article content here...

---

# Next Article Title

*Source: https://docs.example.com/another/article.html*

More content...
```

## 快速入门

```bash
# 1. Index the documentation (one-time or when docs change)
scripts/docs.py index ./docs

# 2. Search
scripts/docs.py search "kubernetes backup" --max 5

# 3. Check index status
scripts/docs.py status
```

## 主要工具：`docs.py`

这个统一的命令行工具（CLI）可以处理所有操作：

### 索引创建

```bash
# Index documentation directory
scripts/docs.py index ./docs

# Force full rebuild
scripts/docs.py index ./docs --rebuild

# Custom database location
scripts/docs.py index ./docs --db /path/to/custom.db
```

### 搜索

```bash
# Basic search
scripts/docs.py search "kubernetes backup"

# Boolean operators
scripts/docs.py search "AWS AND S3 AND snapshot"

# Phrase search
scripts/docs.py search '"exact phrase match"'

# Prefix search
scripts/docs.py search "kube*"

# Exclude terms
scripts/docs.py search "backup NOT restore"

# Title-only search
scripts/docs.py search "kubernetes" --title-only

# Output formats
scripts/docs.py search "kubernetes" --format json
scripts/docs.py search "kubernetes" --format markdown

# More context around matches
scripts/docs.py search "kubernetes" --context 400

# Include full content in JSON
scripts/docs.py search "kubernetes" --format json --full-content
```

### FTS5 查询语法

| 语法        | 含义                                      |
|-------------|-----------------------------------------|
| `term1 term2`    | 包含 term1 或 term2 的文档（按相关性排序）         |
| `term1 AND term2`  | 同时包含 term1 和 term2 的文档           |
| `term1 OR term2`    | 包含 term1 或 term2 的文档                 |
| `"exact phrase"`  | 完整匹配的短语                         |
| `prefix*`      | 以 prefix 开头的单词                      |
| `term1 NOT term2`  | 不包含 term2 的文档                     |
| `title:term`    | 仅搜索标题中包含 term 的文档                   |

### 获取特定文章

```bash
# Get article by partial URL or title
scripts/docs.py get "system_requirements" --full

# Find all matching articles
scripts/docs.py get "backup" --all
```

### 状态更新

```bash
# Check index statistics
scripts/docs.py status
```

## 研究任务的工作流程

### 发现阶段

```bash
# Check what's indexed
scripts/docs.py status

# Explore topics with broad searches
scripts/docs.py search "<feature>" --max 20
```

### 研究阶段

```bash
# Narrow down with boolean operators
scripts/docs.py search "<feature> AND <platform>"

# Find specific information
scripts/docs.py search "limitation OR restriction OR 'not supported'"
```

### 引用阶段

每个搜索结果都会包含 `Source:` URL — 请在报告中引用该链接：

```markdown
According to documentation, [finding]...

Source: https://docs.example.com/path/to/article.html
```

## 多源设置

每个代理或项目都可以拥有自己的文档和索引：

```
~/docs/VendorA/
    ├── docs_part_01.md
    ├── docs.db      # Index lives with docs
    └── ...

~/docs/VendorB/
    ├── docs.md
    ├── docs.db
    └── ...
```

`docs.py` 脚本会自动检测数据库的位置。

## 高级脚本

针对特殊需求：

- `scripts/fts_search.py` — 提供更多选项的直接 FTS5 搜索功能
- `scripts/index_docs.py` — 独立的索引创建工具
- `scripts/list_sources.py` — 列出所有源代码链接
- `scripts/get_article.py` — 直接获取文章内容
- `scripts/search_docs.py` — 基于正则表达式的搜索（无需索引）

## 常见搜索模式

有关常见的搜索模式（如功能研究、架构分析、安全性等），请参阅 [references/search-patterns.md](references/search-patterns.md)。

## 示例搜索过程

```bash
# What's available?
scripts/docs.py status
# Output: Files indexed: 37, Articles indexed: 32065

# Find information
scripts/docs.py search "kubernetes backup" --max 5

# Narrow to specific platform
scripts/docs.py search "kubernetes AND AWS" --max 5

# Find limitations
scripts/docs.py search "limitation OR 'not supported'"

# Get full article for citation
scripts/docs.py get "system_requirements" --full
```

## 最佳实践

1. **一次创建索引，多次使用** — FTS5 由于采用了索引技术，搜索速度非常快
2. **使用布尔运算符** — 使用 `AND`、`OR`、`NOT` 来提高搜索精度
3. **使用引号进行精确短语搜索** — 使用 `"exact match"` 来匹配完整短语
4. **始终引用来源** — 在报告中包含 `Source:` URL
5. **定期重建索引** — 当文档更新时重新生成索引
6. **使用 JSON 进行数据解析** — 将搜索结果导出到 `jq` 或其他工具进行处理