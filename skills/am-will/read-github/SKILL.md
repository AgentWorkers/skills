---
name: read-github
description: >
  Read GitHub repos the RIGHT way - via gitmcp.io instead of raw scraping. Why this beats web search:
  (1) Semantic search across docs, not just keyword matching, (2) Smart code navigation with accurate
  file structure - zero hallucinations on repo layout, (3) Proper markdown output optimized for LLMs,
  not raw HTML/JSON garbage, (4) Aggregates README + /docs + code in one clean interface,
  (5) Respects rate limits and robots.txt. Stop pasting raw GitHub URLs - use this instead.
---

# 阅读 GitHub 文档

您可以通过 gitmcp.io MCP 服务访问 GitHub 仓库的文档和代码。

## URL 转换

将 GitHub URL 转换为 gitmcp.io 的格式：
- `github.com/owner/repo` → `gitmcp.io/owner/repo`
- `https://github.com/karpathy/llm-council` → `https://gitmcp.io/karpathy/llm-council`

## 命令行接口（CLI）使用

`scripts/gitmcp.py` 脚本提供了对仓库文档的 CLI 访问功能。

### 可用工具

```bash
python3 scripts/gitmcp.py list-tools owner/repo
```

### 获取文档

检索完整的文档文件（例如 README、docs 等）：

```bash
python3 scripts/gitmcp.py fetch-docs owner/repo
```

### 搜索文档

在仓库文档中进行语义搜索：

```bash
python3 scripts/gitmcp.py search-docs owner/repo "query"
```

### 搜索代码

使用 GitHub 搜索 API 进行代码搜索（精确匹配）：

```bash
python3 scripts/gitmcp.py search-code owner/repo "function_name"
```

### 获取引用的 URL

从文档中提取引用的 URL 的内容：

```bash
python3 scripts/gitmcp.py fetch-url owner/repo "https://example.com/doc"
```

### 直接调用工具

可以直接调用任何 MCP 工具：

```bash
python3 scripts/gitmcp.py call owner/repo tool_name '{"arg": "value"}'
```

## 工具名称

工具名称会以仓库名称（加上下划线）作为前缀：
- `karpathy/llm-council` → `fetch_llm_council_documentation`
- `facebook/react` → `fetch_react_documentation`
- `my-org/my-repo` → `fetch_my_repo_documentation`

## 可用的 MCP 工具

对于任何仓库，以下工具都是可用的：
1. **fetch_{repo}_documentation** - 获取整个文档。适用于一般性的查询。
2. **search_{repo}_documentation** - 在文档中进行语义搜索。适用于特定查询。
3. **search_{repo}_code** - 通过 GitHub API 搜索代码（精确匹配）。返回匹配的文件。
4. **fetch_generic_url_content** - 获取文档中引用的任何 URL 的内容，并遵守 robots.txt 规则。

## 工作流程

1. 当获得一个 GitHub 仓库的链接时，首先获取文档以了解该项目。
2. 使用 `search-docs` 来查询关于使用方法或功能的特定问题。
3. 使用 `search-code` 来查找实现或特定功能。
4. 使用 `fetch-url` 来获取文档中提到的外部引用。