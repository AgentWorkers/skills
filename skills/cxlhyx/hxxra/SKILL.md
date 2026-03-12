---
name: hxxra
description: A Research Assistant workflow skill with five core commands: search papers, download PDFs, analyze content, generate reports, and save to Zotero. Entry point is a Python script located at scripts/hxxra.py and invoked via stdin/stdout (OpenClaw integration). The search uses crawlers for Google Scholar and arXiv APIs; download uses Python requests or arXiv API; analyze uses an LLM; report generates Markdown summaries from analysis.json files; save uses Zotero API.
---

# hxxra

hxxra 是一个研究辅助工具，可帮助用户搜索、下载、分析、报告和保存研究论文。

## 推荐的目录结构

为了更好地组织文件，建议在您的 OpenClaw 工作目录下为 hxxra 创建一个专门的工作空间：

```
📁 workspace/                              # OpenClaw current working directory
└── 📁 hxxra/
    ├── 📁 searches/                       # Stores all search result JSON files
        ├── 2025-03-07_neural_radiance_fields_arxiv.json
        ├── 2025-03-07_transformer_architectures_scholar.json
        └── ...
    ├── 📁 papers/                           # Stores downloaded PDF files and per-paper analysis results (each as a subfolder)
        ├── papers_report.md                # Generated Markdown report summarizing all analyzed papers
        ├── 2023_Smith_NeRF_Explained/      # Folder named after the PDF (without extension)
          ├── 2023_Smith_NeRF_Explained.pdf
          ├── analysis.json                 # Structured output from LLM analysis
          └── notes.md                      # (Optional) User-added notes
        ├── 2024_Zhang_Transformer_Survey/
          ├── 2024_Zhang_Transformer_Survey.pdf
          ├── analysis.json
          └── ...
        └── ...
    └── 📁 logs/ # Stores execution logs
        └── hxxra_2025-03-07.log
```

这种结构可以确保所有相关文件都井井有条，便于查看和进一步处理。

## 核心命令

### 1. **hxxra search** - 搜索研究论文

**依赖库**: `pip install scholarly`

**功能**: 使用 Google Scholar 和 arXiv API 搜索论文

**学术说明**: 由于每个数据源的特点不同，该工具采用了不同的排序策略：
- **arXiv 的结果按提交日期降序排列**，优先显示最新的研究论文；
- **Google Scholar 的结果保留来源的默认相关性排名**，确保与查询关键词高度匹配，同时适当考虑重要或经典的文献。

**参数**:
- `-q, --query <string>` (必选): 搜索关键词
- `-s, --source <string>` (可选): 数据源：`arxiv`（默认），`scholar`
- `-l, --limit <number>` (可选): 结果数量（默认：10）
- `-o, --output <path>` (可选): JSON 输出文件（默认：`{workspace}/hxxra/searches/search_results.json`）

**输入示例**:

```json
{"command": "search", "query": "neural radiance fields", "source": "arxiv", "limit": 10, "output": "results.json"} | python scripts/hxxra.py
{"command": "search", "query": "transformer architecture", "source": "scholar", "limit": 15} | python scripts/hxxra.py
```

**输出结构**:

```json
{
  "ok": true,
  "command": "search",
  "query": "<query>",
  "source": "<source>",
  "results": [
    {
      "id": "1",
      "title": "Paper Title",
      "authors": ["Author1", "Author2"],
      "year": "2023",
      "source": "arxiv",
      "abstract": "Abstract text...",
      "url": "https://arxiv.org/abs/xxxx.xxxxx",
      "pdf_url": "https://arxiv.org/pdf/xxxx.xxxxx.pdf",
      "citations": 123
    }
  ],
  "total": 10,
  "output_file": "/path/to/results.json"
}
```

------

### 2. **hxxra download** - 下载 PDF 文件

**功能**: 下载指定论文的 PDF 文件

**参数**:
- `-f, --from-file <path>` (必选): 包含搜索结果的 JSON 文件
- `-i, --ids <list>` (可选): 论文 ID（逗号分隔或范围）
- `-d, --dir <path>` (可选): 下载目录（默认：`{workspace}/hxxra/papers/`）

**输入示例**:

```json
{"command": "download", "from-file": "results.json", "ids": ["1", "3", "5"], "dir": "./downloads"} | python scripts/hxxra.py
{"command": "download", "from-file": "results.json", "dir": "./downloads"} | python scripts/hxxra.py
```

**输出结构**:

```json
{
  "ok": true,
  "command": "download",
  "downloaded": [
    {
      "id": "1",
      "title": "Paper Title",
      "status": "success",
      "pdf_path": "{workspace}/hxxra/papers/2023_Smith_NeRF_Explained/2023_Smith_NeRF_Explained.pdf",
      "size_bytes": 1234567,
      "url": "https://arxiv.org/pdf/xxxx.xxxxx.pdf"
    }
  ],
  "failed": [],
  "total": 3,
  "successful": 3,
  "download_dir": "{workspace}/hxxra/papers"
}
```

------

### 3. **hxxra analyze** - 分析 PDF 内容

**依赖库**: `pip install pymupdf pdfplumber openai`

**功能**: 使用大型语言模型（LLM）分析论文内容

**参数**:
- `-p, --pdf <path>` (可选): 要分析的单个 PDF 文件
- `-d, --directory <path>` (可选): 包含多个 PDF 文件的目录
- `-o, --output <path>` (可选): 输出目录。如果未指定，分析结果将保存在与 PDF 相同的子文件夹中（默认：`{workspace}/hxxra/papers/{paper_title}/analysis.json`）

**注意**: 必须提供 `--pdf` 或 `--directory` 中的一个参数，但不能同时提供两个。

**输入示例**:

```json
{"command": "analyze", "pdf": "paper.pdf", "output": "./analysis/"} | python scripts/hxxra.py
{"command": "analyze", "directory": "hxxra/papers/"} | python scripts/hxxra.py
```

**输出结构**:

```json
{
  "ok": true,
  "command": "analyze",
  "analyzed": [
    {
      "id": "paper_1",
      "original_file": "paper.pdf",
      "analysis_file": "{workspace}/hxxra/papers/2023_Smith_NeRF_Explained/analysis.json",
      "metadata": {
        "title": "Paper Title",
        "authors": ["Author1", "Author2"],
        "year": "2023",
        "abstract": "Abstract text..."
      },
      "analysis": {
        "background": "Problem background...",
        "methodology": "Proposed method...",
        "results": "Experimental results...",
        "conclusions": "Conclusions..."
      },
      "status": "success"
    }
  ],
  "summary": {
    "total": 1,
    "successful": 1,
    "failed": 0
  }
}
```

------

### 4. **hxxra report** - 生成 Markdown 报告

**功能**: 从目录中的所有 `analysis.json` 文件生成详细的 Markdown 报告

**参数**:
- `-d, --directory <path>` (必选): 包含 `analysis.json` 文件的目录
- `-o, --output <path>` (可选): 输出 Markdown 文件路径（默认：`{directory}/report.md`)
- `-t, --title <string>` (可选): 报告标题（默认："Research Papers Report")
- `-s, --sort <string>` (可选): 排序方式：`year`（默认，降序）、`title` 或 `author`

**输入示例**:

```json
{"command": "report", "directory": "hxxra/papers/", "output": "hxxra/papers/report.md", "title": "My Research Papers", "sort": "year"} | python scripts/hxxra.py
{"command": "report", "directory": "hxxra/papers/"} | python scripts/hxxra.py
```

**输出结构**:

```json
{
  "ok": true,
  "command": "report",
  "total_papers": 10,
  "output_file": "/path/to/hxxra/papers/report.md"
}
```

**生成的 Markdown 格式**:

报告包括：
- **标题**: 报告标题、生成日期、论文总数、数据来源
- **关键词表**: 所有论文中出现频率最高的 15 个关键词
- **概述表**: 所有论文的快速摘要（标题、作者、年份、关键词）
- **详细内容**: 每篇论文包括：
  - 标题、作者、年份、关键词、代码链接（如果有的话）
  - 摘要
  - 研究背景
  - 方法论
  - 主要结果
  - 结论
  - 限制因素
  - 影响力
  - 来源文件夹路径

**注意**: `report` 命令会递归扫描所有子目录中的 `analysis.json` 文件，并仅包含状态为 "success" 的论文。

------

### 5. **hxxra save** - 保存到 Zotero

**功能**: 将论文保存到 Zotero 收藏夹中

**参数**:
- `-f, --from-file <path>` (必选): 包含搜索结果的 JSON 文件（例如：`hxxra/searches/search_results.json`）
- `-i, --ids <list>` (可选): 要保存的论文 ID
- `-c, --collection <string>` (必选): Zotero 收藏夹名称

**输入示例**:

```json
{"command": "save", "from-file": "hxxra/searches/search_results.json", "ids": ["1", "2", "3"], "collection": "AI Research"} | python scripts/hxxra.py
{"command": "save", "from-file": "hxxra/searches/search_results.json", "collection": "My Collection"} | python scripts/hxxra.py
```

**输出结构**:

```json
{
  "ok": true,
  "command": "save",
  "collection": "AI Research",
  "saved_items": [
    {
      "id": "1",
      "title": "Paper Title",
      "zotero_key": "ABCD1234",
      "url": "https://www.zotero.org/items/ABCD1234",
      "status": "success"
    }
  ],
  "failed_items": [],
  "total": 3,
  "successful": 3,
  "zotero_collection": "ABCD5678"
}
```

---

## 工作流程示例

### 完整工作流程

```bash
# 1. Search for papers
{"command": "search", "query": "graph neural networks", "source": "arxiv", "limit": 10, "output": "hxxra/searches/gnn_arxiv.json"} | python scripts/hxxra.py

# 2. Download papers
{"command": "download", "from-file": "hxxra/searches/gnn_arxiv.json", "dir": "hxxra/papers"} | python scripts/hxxra.py

# 3. Analyze downloaded papers
{"command": "analyze", "directory": "hxxra/papers/"} | python scripts/hxxra.py

# 4. Generate comprehensive report
{"command": "report", "directory": "hxxra/papers/", "output": "hxxra/papers/report.md", "sort": "year"} | python scripts/hxxra.py

# 5. Save to Zotero
{"command": "save", "from-file": "hxxra/searches/gnn_arxiv.json", "collection": "GNN Papers"} | python scripts/hxxra.py
```

### 单个命令示例

```bash
# Search with scholar
{"command": "search", "query": "reinforcement learning", "source": "scholar", "limit": 15} | python scripts/hxxra.py

# Download specific papers
{"command": "download", "from-file": "hxxra/searches/search_results.json", "ids": ["2", "4", "6"], "dir": "hxxra/papers"} | python scripts/hxxra.py

# Analyze single PDF in detail
{"command": "analyze", "pdf": "hxxra/papers/2024_Zhang_Transformer_Survey/2024_Zhang_Transformer_Survey.pdf"} | python scripts/hxxra.py

# Generate report sorted by title
{"command": "report", "directory": "hxxra/papers/", "sort": "title", "output": "hxxra/papers/report_by_title.md"} | python scripts/hxxra.py

# Save with custom notes
{"command": "save", "from-file": "hxxra/searches/search_results.json", "ids": ["1"], "collection": "To Read"} | python scripts/hxxra.py
```

## 配置要求

### API 凭据（config.json）

1. **arXiv API**: 基本访问无需密钥
2. **Google Scholar**: 大规模查询可能需要身份验证
3. **Zotero API**: 需要提供凭据：

```json
   {
     "api_key": "YOUR_ZOTERO_API_KEY", # Create at https://www.zotero.org/settings/keys/new
     "user_id": "YOUR_ZOTERO_USER_ID", # Found on the same page (numeric, not username)
     "library_type": "user"  # or "group"
   }
   ```

## 注意事项

- 所有命令都通过 stdin/stdout JSON 进行通信
- 错误处理返回 `{"ok": false, "error": "错误信息"}`
- 大规模操作支持通过中间消息进行进度报告
- 配置从 `config.json` 或环境变量中加载
- 并发操作有可配置的限制，以避免速率限制

## 错误处理

每个命令都会返回标准的错误格式：

```json
{
  "ok": false,
  "command": "<command>",
  "error": "Error description",
  "error_code": "ERROR_TYPE",
  "suggestion": "How to fix it"
}
```

## 开发状态

### 当前版本: v1.2.0 (2026/3/8)

### 版本历史

**v1.2.0 · 2026/3/8**

- 添加了 `report` 命令，可以从所有 `analysis.json` 文件生成详细的 Markdown 报告
- 报告包括关键词统计、概述表和每篇论文的详细内容
- 支持按年份（默认）、标题或作者排序
- 生成的 Markdown 格式清晰易读，包含表格、标题和结构化内容
- 更新了文档，将新的报告命令包含在工作流程和示例中

**v1.1.1 · 2026/3/7**

- 添加了 `sanitize_filename()` 函数，统一下载论文的文件名和文件夹名处理方式
- 修改了 `handle_download` 函数，使用新的清理函数处理作者名和标题
- 提高了文件名的安全性：现在只允许字母、数字和下划线；连续的下划线会被合并；长度限制为 50 个字符

**v1.1.0 · 2026/3/7**

- 添加了推荐的目录结构，以优化搜索结果、论文、分析和日志的组织
- 更新了所有示例和默认输出位置，以匹配新的 `{workspace}/hxxra/` 文件夹布局
- 明确了文件存储方式：每篇下载的论文现在都有自己的子文件夹，其中包含 PDF 和分析文件
- 更新了命令参数和输出的文档，以反映目录结构的变化
- 提高了工作流程步骤的清晰度，便于管理和共享研究输出
- 修复了 ID 数据处理问题：改进了 ID 匹配逻辑，以支持下载和保存命令中的字符串和数字 ID 比较
- 修复了 Zotero API 的 "400 Bad Request" 错误：将数据格式从对象更改为数组 (`[item_data]`)，以符合 Zotero API 的要求

**v1.0.2 · 2026/3/6**

- 修改了 hxxra.py 脚本，添加了 fix_proxy_env() 函数调用，解决了在新 OpenClaw 会话中 ALL_PROXY 和 all_proxy 被重置为 socks://127.0.0.1:7897/ 从而导致搜索失败的问题

**v1.0.1 · 2026/3/6**

- 添加了学术说明，明确指出 arXiv 的搜索结果按最新提交日期排序，而 Google Scholar 的结果使用来源的默认相关性排名
- 命令结构、参数或输出格式没有变化

**v1.0.0 · 2026/2/9**

hxxra 的初始版本——一个用于搜索、下载、分析和保存研究论文的研究辅助工具。
- 提供了四个基于 JSON 的核心命令：搜索、下载、分析和保存
- 支持通过 Google Scholar 和 arXiv 搜索论文，具有灵活的参数和输出结构
- 支持使用搜索结果下载 PDF 文件，并提供细粒度的 ID 选择和状态报告
- 集成了基于 LLM 的 PDF 内容分析功能，为一篇或多篇论文提供结构化的输出
- 允许将论文保存到 Zotero 收藏夹中，需要用户提供 API 凭据
- 具有强大的参数验证、错误处理和带有使用示例的文档