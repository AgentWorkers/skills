---
name: competitor-docs
description: 使用全文搜索（FTS）来搜索和分析竞争对手的文档档案。当您需要在包含带有源URL的文章的结构化文档文件夹中查找信息时，可以使用该功能（这些文章的源URL会以“*Source:”为标记）。该工具能够快速地对数千篇文章进行BM25排序搜索，并自动提取引用中的源URL。非常适合用于竞争情报研究、功能对比以及文档查询。在使用前，需要先使用`docs.py index`命令对文档进行索引。
---
# 竞争对手文档搜索

通过 SQLite 的 FTS5 支持快速的全文搜索，并采用 BM25 相关性排名算法对竞争对手的文档进行索引。

## 使用场景

- 在竞争对手的文档中搜索特定的功能、能力或限制信息
- 查找官方文档的 URL 以用于研究报告的引用
- 比较多个竞争对手的文档内容
- 查阅技术规格或配置细节

## 预期的文档格式

文档以 `---` 作为分隔符，每个文档前包含 `*Source:` 标签和相应的 URL：

```markdown
# Article Title

*Source: https://documentation.vendor.com/path/to/article.html*

Article content here...

---

# Next Article Title

*Source: https://documentation.vendor.com/another/article.html*

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

## 主要工具：docs.py

`docs.py` 是一个统一的命令行工具（CLI），用于处理所有操作：

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

| 语法          | 含义                                      |
|-----------------|-----------------------------------------|
| `term1 term2`     | 包含 term1 或 term2 的文档（按相关性排序）         |
| `term1 AND term2`    | 同时包含 term1 和 term2 的文档             |
| `term1 OR term2`     | 包含 term1 或 term2 的文档             |
| `"exact phrase"`    | 精确匹配指定短语                   |
| `prefix*`       | 以指定前缀开头的单词                 |
| `term1 NOT term2`    | 不包含 term2 的文档                   |
| `title:term`     | 仅搜索标题中包含 term 的文档             |

### 获取特定文档

```bash
# Get article by partial URL or title
scripts/docs.py get "system_requirements_for_kubernetes" --full

# Find all matching articles
scripts/docs.py get "backup" --all
```

### 状态更新

```bash
# Check index statistics
scripts/docs.py status
```

## 研究任务的工作流程

- **发现阶段**  
- **研究阶段**  
- **引用阶段**  

每个搜索结果都会包含 `Source:` 标签中的文档 URL，请在报告中引用这些文档：

```markdown
According to Commvault documentation, Kubernetes backup requires...

Source: https://documentation.commvault.com/11.42/software/kubernetes.html
```

## 多竞争对手设置

每个竞争对手都可以拥有自己的文档和索引：

```
~/OpenClaw/CI/frodo/docs/CommvaultDocumentation/
    ├── commvault_cloud_docs_part_01.md
    ├── competitor_docs.db      # Index lives with docs
    └── ...

~/OpenClaw/CI/sam/docs/DattoDocumentation/
    ├── datto_docs.md
    ├── competitor_docs.db
    └── ...
```

`docs.py` 脚本会自动检测数据库的位置。

## 高级脚本

针对特殊需求，可使用以下脚本：

- `scripts/fts_search.py` — 提供更多选项的 FTS5 直接搜索功能
- `scripts/index_docs.py` — 独立的文档索引工具
- `scripts/list_sources.py` — 列出所有文档的 URL
- `scripts/get_article.py` — 直接检索文档内容
- `scripts/search_docs.py` — 基于正则表达式的搜索（无需索引）

## 竞争情报搜索模式

有关常见的竞争情报搜索模式，请参阅 [references/ci-patterns.md](references/ci-patterns.md)。

## 示例研究流程

```bash
# What's available?
scripts/docs.py status
# Output: Files indexed: 37, Articles indexed: 32065

# Find Kubernetes backup info
scripts/docs.py search "kubernetes backup" --max 5

# Narrow to specific platform
scripts/docs.py search "kubernetes AND AWS" --max 5

# Find limitations
scripts/docs.py search "kubernetes AND (limitation OR 'not supported')"

# Get full article for citation
scripts/docs.py get "system_requirements_for_kubernetes" --full
```

## 最佳实践

1. **一次创建索引，多次使用**：FTS5 因为采用了索引机制，所以搜索速度很快。
2. **使用布尔运算符**：使用 `AND`、`OR`、`NOT` 来提高搜索精度。
3. **使用引号进行精确短语搜索**：使用 `"exact match"` 来确保匹配准确。
4. **始终引用来源**：在报告中务必包含文档的 `Source:` URL。
5. **定期重建索引**：当文档更新时重新构建索引。
6. **使用 JSON 进行数据分析**：将搜索结果导出到 `jq` 等工具进行处理。