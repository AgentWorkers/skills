---
name: hxxra
description: A Research Assistant workflow skill with four core commands: search papers, download PDFs, analyze content, and save to Zotero. Entry point is a Python script located at scripts/hxxra.py and invoked via stdin/stdout (OpenClaw integration). The search uses crawlers for Google Scholar and arXiv APIs; download uses Python requests or arXiv API; analyze uses an LLM; save uses Zotero API.
---

# hxxra

这个工具是一个研究助手，可以帮助用户搜索、下载、分析和保存研究论文。

## 推荐的目录结构

为了更好地组织文件，建议在您的 OpenClaw 工作目录下创建一个专门用于 `hxxra` 的工作空间：

```plaintext
📁 workspace/                              # OpenClaw 当前工作目录
└── 📁 hxxra/
    ├── 📁 searches/                       # 存储所有搜索结果的 JSON 文件
        ├── 2025-03-07_neural_radiance_fields_arxiv.json
        ├── 2025-03-07_transformer_architectures_scholar.json
        └── ...
    ├── 📁 papers/                           # 存储下载的 PDF 文件和每篇论文的分析结果（每个论文对应一个子文件夹）
        ├── 2023_Smith_NeRF_Explained/      # 以 PDF 文件名命名的文件夹（不包含扩展名）
          ├── 2023_Smith_NeRF_Explained.pdf
          ├── analysis.json                 # 来自 LLM 的分析结果
          └── notes.md                      # （可选）用户添加的注释
        ├── 2024_Zhang_Transformer_Survey/
          ├── 2024_Zhang_Transformer_Survey.pdf
          ├── analysis.json
          └── ...
        └── ...
    └── 📁 logs/      # 存储执行日志
        └── hxxra_2025-03-07.log
```

这种结构使所有相关文件都井井有条，便于查看和进一步处理。

## 核心命令

### 1. **hxxra search** - 搜索研究论文

**依赖库**: `pip install scholarly`

**功能**: 使用 Google Scholar 和 arXiv API 搜索论文

**学术说明**: 由于两个数据源的特点不同，该工具采用了不同的排序策略：
- **arXiv 的结果按提交日期降序排列**，优先显示最新的研究；
- **Google Scholar 的结果保留来源默认的相关性排名**，确保与查询关键词高度匹配，同时适当考虑权威或经典文献。

**参数**:

- `-q, --query <string>` （必选）: 搜索关键词
- `-s, --source <string>` （可选）: 数据源：`arxiv`（默认），`scholar`
- `-l, --limit <number>` （可选）: 结果数量（默认：10）
- `-o, --output <path>` （可选）: JSON 输出文件（默认：`{workspace}/hxxra/searches/search_results.json`）

**输入示例**:

```json
{"command": "search", "query": "neural radiance fields", "source": "arxiv", "limit": 10, "output": "results.json"} | python scripts/hxxra.py
{"command": "search", "query": "transformer architecture", "source": "scholar", "limit": 15} | python scripts/hxxra.py
```

**输出格式**:

```json
{
  "ok": true,
  "command": "search",
  "query": "<query>",
  "source": "<source>",
  "results": [
    {
      "id": "1",
      "title": "论文标题",
      "authors": ["作者1", "作者2"],
      "year": "2023",
      "source": "arxiv",
      "abstract": "摘要内容...",
      "url": "https://arxiv.org/abs/xxxx.xxxxx",
      "pdf_url": "https://arxiv.org/pdf/xxxx.xxxxx.pdf",
      "citations": 123
    },
  ],
  "total": 10,
  "output_file": "/path/to/results.json"
}
```

------

### 2. **hxxra download** - 下载 PDF 文件

**功能**: 下载指定论文的 PDF 文件

**参数**:

- `-f, --from-file <path>` （必选）: 包含搜索结果的 JSON 文件
- `-i, --ids <list>` （可选）: 论文 ID（逗号分隔或范围）
- `-d, --dir <path>` （可选）: 下载目录（默认：`{workspace}/hxxra/papers/`）

**输入示例**:

```json
{"command": "download", "from-file": "results.json", "ids": ["1", "3", "5"], "dir": "./downloads"} | python scripts/hxxra.py
{"command": "download", "from-file": "results.json", "dir": "./downloads"} | python scripts/hxxra.py
```

**输出格式**:

```json
{
  "ok": true,
  "command": "download",
  "downloaded": [
    {
      "id": "1",
      "title": "论文标题",
      "status": "成功",
      "pdf_path": "{workspace}/hxxra/papers/2023_Smith_NeRF_Explained/2023_Smith_NeRF_Explained.pdf",
      "size_bytes": 1234567,
      "url": "https://arxiv.org/pdf/xxxx.xxxxx.pdf"
    },
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

**功能**: 使用 LLM 分析 PDF 内容

**参数**:

- `-p, --pdf <path>` （可选）: 要分析的单个 PDF 文件
- `-d, --directory <path>` （可选）: 包含多个 PDF 文件的目录
- `-o, --output <path>` （可选）: 输出目录。如果未指定，分析结果将保存在 PDF 所在的子文件夹中（默认：`{workspace}/hxxra/papers/{paper_title}/analysis.json`）

**注意**: 必须提供 `--pdf` 或 `--directory` 中的一个参数，但不能同时提供两个。

**输入示例**:

```json
{"command": "analyze", "pdf": "paper.pdf", "output": "./analysis/"} | python scripts/hxxra.py
{"command": "analyze", "directory": "hxxra/papers/"} | python scripts/hxxra.py
```

**输出格式**:

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
        "title": "论文标题",
        "authors": ["作者1", "作者2"],
        "year": "2023",
        "abstract": "摘要内容..."
      },
      "analysis": {
        "背景": "问题背景...",
        "方法论": "提出的方法...",
        "结果": "实验结果...",
        "结论": "结论..."
      },
      "status": "成功"
    },
  },
  "summary": {
    "total": 1,
    "successful": 1,
    "failed": 0
  }
}
```

------

### 4. **hxxra save** - 保存到 Zotero

**功能**: 将论文保存到 Zotero 收藏夹

**参数**:

- `-f, --from-file <path>` （必选）: 包含搜索结果的 JSON 文件（例如 `hxxra/searches/search_results.json`）
- `-i, --ids <list>` （可选）: 要保存的论文 ID
- `-c, --collection <string>` （必选）: Zotero 收藏夹名称

**输入示例**:

```json
{"command": "save", "from-file": "hxxra/searches/search_results.json", "ids": ["1", "2", "3"], "collection": "AI Research"} | python scripts/hxxra.py
{"command": "save", "from-file": "hxxra/searches/search_results.json", "collection": "My Collection"} | python scripts/hxxra.py
```

**输出格式**:

```json
{
  "ok": true,
  "command": "save",
  "collection": "AI Research",
  "saved_items": [
    {
      "id": "1",
      "title": "论文标题",
      "zotero_key": "ABCD1234",
      "url": "https://www.zotero.org/items/ABCD1234",
      "status": "成功"
    },
  },
  "failed_items": [],
  "total": 3,
  "successful": 3,
  "zotero_collection": "ABCD5678"
}
```

## 工作流程示例

### 完整工作流程

```bash
# 1. 搜索论文
{"command": "search", "query": "graph neural networks", "source": "arxiv", "limit": 10, "output": "hxxra/searches/gnn_arxiv.json"} | python scripts/hxxra.py

# 2. 下载前 5 篇论文
{"command": "download", "from-file": "hxxra/searches/gnn_arxiv.json", "dir": "hxxra/papers"} | python scripts/hxxra.py

# 3. 分析下载的论文
{"command": "analyze", "directory": "hxxra/papers/"} | python scripts/hxxra.py

# 4. 保存到 Zotero
{"command": "save", "from-file": "hxxra/searches/gnn_arxiv.json", "collection": "GNN Papers"} | python scripts/hxxra.py
```

### 单个命令示例

```bash
# 使用 scholar 搜索
{"command": "search", "query": "reinforcement learning", "source": "scholar", "limit": 15} | python scripts/hxxra.py

# 下载特定的论文
{"command": "download", "from-file": "hxxra/searches/search_results.json", "ids": ["2", "4", "6"], "dir": "hxxra/papers"} | python scripts/hxxra.py

# 详细分析单个 PDF
{"command": "analyze", "pdf": "hxxra/papers/2024_Zhang_Transformer_Survey/2024_Zhang_Transformer_Survey.pdf"} | python scripts/hxxra.py

# 带有自定义注释的保存
{"command": "save", "from-file": "hxxra/searches/search_results.json", "ids": ["1"], "collection": "To Read"} | python scripts/hxxra.py
```

## 配置要求

### API 凭据（config.json）

1. **arXiv API**: 基本访问无需密钥

2. **Google Scholar**: 对于大量查询可能需要身份验证

3. **Zotero API**: 需要以下凭据：

   ```json
   {
     "api_key": "YOUR_ZOTERO_API_KEY", // 在 https://www.zotero.org/settings/keys/new 创建
     "user_id": "YOUR_ZOTERO_USER_ID", // 在同一页面上找到（数字，不是用户名）
     "library_type": "user"  // 或 "group"
   }
   ```

4. **LLM API**: 需要 OpenAI 或兼容的 API 密钥来进行分析

## 注意事项

- 所有命令都通过 stdin/stdout 进行 JSON 通信
- 错误处理返回 `{"ok": false, "error": "错误信息"}`
- 大规模操作支持通过中间消息报告进度
- 配置从 `config.json` 或环境变量加载
- 并发操作有可配置的限制，以避免速率限制

## 错误处理

每个命令都会返回标准的错误格式：

```json
{
  "ok": false,
  "command": "<command>",
  "error": "错误描述",
  "error_code": "ERROR_TYPE",
  "suggestion": "如何修复它"
}
```

## 开发状态

### 当前版本: v1.1.1 (2026/3/7)

### 版本历史

**v1.1.1 · 2026/3/7**

- 添加了 `sanitize_filename()` 函数，以统一下载论文的文件名和文件夹名处理方式。
- 修改了 `handle_download` 函数，使用新的清理函数处理作者名和标题。
- 提高了文件名的安全性：现在只允许字母、数字和下划线；多个连续的下划线会被合并；文件名长度限制为 50 个字符。

**v1.1.0 · 2026/3/7**

- 添加了推荐的目录结构，以优化搜索结果、论文、分析和日志的组织。
- 更新了所有示例和默认输出位置，以适应新的 `{workspace}/hxxra/` 文件夹布局。
- 明确了文件存储方式：每篇下载的论文现在都有自己的子文件夹，其中包含 PDF 和分析文件。
- 更新了命令参数和输出的文档，以反映目录结构的变化。
- 提高了工作流程步骤的清晰度，便于管理和共享研究输出。
- 修复了 ID 数据处理问题：改进了 ID 匹配逻辑，以支持下载和保存命令中的字符串和数字 ID 比较。
- 修复了 Zotero API 的 "400 Bad Request" 错误：将数据格式从对象更改为数组 (`[item_data]`)，以符合 Zotero API 的要求。

**v1.0.2 · 2026/3/6**

- 修改了 `hxxra.py` 脚本，添加了 `fix_proxy_env()` 函数调用，解决了在新 OpenClaw 会话中 `ALL_PROXY` 和 `all_proxy` 被重置为 `socks://127.0.0.1:7897/` 从而导致搜索失败的问题。

**v1.0.1 · 2026/3/6**

- 添加了学术说明，明确指出 arXiv 的搜索结果按最新提交日期排序，而 Google Scholar 的结果使用来源默认的相关性排名。
- 命令结构、参数和输出格式未作更改。

**v1.0.0 · 2026/2/9**

- hxxra 的初始版本——一个用于搜索、下载、分析和保存研究论文的研究助手工具。
- 引入了四个基于 JSON 的核心命令：搜索、下载、分析和保存。
- 支持通过 Google Scholar 和 arXiv 搜索论文，具有灵活的参数和输出格式。
- 支持使用搜索结果下载 PDF 文件，并提供细粒度的 ID 选择和状态报告。
- 集成了基于 LLM 的 PDF 内容分析，为一篇或多篇论文提供结构化的输出。
- 允许将论文保存到 Zotero 收藏夹，需要用户提供 API 凭据。
- 具有强大的参数验证、错误处理和带有使用示例的文档。
```