---
name: hxxra
description: 这是一项研究助理的工作流程技能，包含四个核心命令：搜索论文、下载PDF文件、分析内容以及将结果保存到Zotero数据库中。整个流程的入口点是一个名为`scripts/hxxra.py`的Python脚本，该脚本通过标准输入（stdin）和标准输出（stdout）进行调用（实现了与OpenClaw系统的集成）。搜索功能利用了Google Scholar和arXiv的API；下载操作通过`requests`库或arXiv的API来实现；内容分析则借助大型语言模型（LLM）来完成；最后，数据保存过程通过Zotero的API完成。
---

# hxxra

这是一个研究辅助工具，可帮助用户搜索、下载、分析并保存研究论文。

## 核心命令

### 1. **hxxra search** - 搜索研究论文

**依赖库**: `pip install scholarly`

**功能**: 使用 Google Scholar 和 arXiv API 进行论文搜索

**参数**:

- `-q, --query <string>` (必选): 搜索关键词
- `-s, --source <string>` (可选): 数据来源：`arxiv`（默认）或 `scholar`
- `-l, --limit <number>` (可选): 结果数量（默认：10）
- `-o, --output <path>` (可选): JSON 输出文件（默认：`search_results.json`）

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
- `-i, --ids <list>` (可选): 论文 ID（用逗号分隔或指定范围）
- `-d, --dir <path>` (可选): 下载目录（默认：`./papers`）

**输入示例**:

```json
{"command": "download", "from-file": "results.json", "ids": [1, 3, 5], "dir": "./downloads"} | python scripts/hxxra.py
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
      "pdf_path": "/path/to/downloads/Smith_2023_Title.pdf",
      "size_bytes": 1234567,
      "url": "https://arxiv.org/pdf/xxxx.xxxxx.pdf"
    }
  ],
  "failed": [],
  "total": 3,
  "successful": 3,
  "download_dir": "/path/to/downloads"
}
```

------

### 3. **hxxra analyze** - 分析 PDF 内容

**依赖库**: `pip install pymupdf pdfplumber openai`

**功能**: 使用大型语言模型（LLM）分析论文内容

**参数**:

- `-p, --pdf <path>` (可选): 单个 PDF 文件进行分析
- `-d, --directory <path>` (可选): 包含多个 PDF 文件的目录
- `-o, --output <path>` (可选): 输出目录（默认：`./analysis`）

**注意**: 必须提供 `--pdf` 或 `--directory` 中的一个参数，但不能同时提供两个

**输入示例**:

```json
{"command": "analyze", "pdf": "paper.pdf", "output": "analysis.json"} | python scripts/hxxra.py
{"command": "analyze", "directory": "./papers/"} | python scripts/hxxra.py
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
      "analysis_file": "/path/to/analysis/paper_analysis.json",
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

### 4. **hxxra save** - 将论文保存到 Zotero

**功能**: 将论文保存到 Zotero 收藏夹中

**参数**:

- `-f, --from-file <path>` (必选): 包含论文数据的 JSON 文件
- `-i, --ids <list>` (可选): 要保存的论文 ID
- `-c, --collection <string>` (必选): Zotero 收藏夹名称

**输入示例**:

```json
{"command": "save", "from-file": "analysis.json", "ids": [1, 2, 3], "collection": "AI Research"} | python scripts/hxxra.py
{"command": "save", "from-file": "analysis.json", "collection": "My Collection"} | python scripts/hxxra.py
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

------

## 工作流程示例

### 完整工作流程

```bash
# 1. Search for papers
{"command": "search", "query": "graph neural networks", "source": "arxiv", "limit": 10} | python scripts/hxxra.py

# 2. Download first 5 papers
{"command": "download", "from-file": "search_results.json"} | python scripts/hxxra.py

# 3. Analyze downloaded papers
{"command": "analyze", "directory": "./papers/"} | python scripts/hxxra.py

# 4. Save to Zotero
{"command": "save", "from-file": "./analysis/", "collection": "GNN Papers"} | python scripts/hxxra.py
```

### 单个命令示例

```bash
# Search with scholar
{"command": "search", "query": "reinforcement learning", "source": "scholar", "limit": 15} | python scripts/hxxra.py

# Download specific papers
{"command": "download", "from-file": "search_results.json", "ids": [2, 4, 6]} | python scripts/hxxra.py

# Analyze single PDF in detail
{"command": "analyze", "pdf": "important_paper.pdf"} | python scripts/hxxra.py

# Save with custom notes
{"command": "save", "from-file": "search_results.json", "ids": [1], "collection": "To Read"} | python scripts/hxxra.py
```

## 配置要求

### API 凭据（config.json）

1. **arXiv API**: 基本访问无需密钥
2. **Google Scholar**: 大规模查询可能需要身份验证
3. **Zotero API**: 需要以下凭据:

   ```json
   {
     "api_key": "YOUR_ZOTERO_API_KEY", # Create at https://www.zotero.org/settings/keys/new
     "user_id": "YOUR_ZOTERO_USER_ID", # Found on the same page (numeric, not username)
     "library_type": "user"  # or "group"
   }
   ```

4. **LLM API**: 使用 OpenAI 或兼容的 API 密钥进行分析

## 注意事项

- 所有命令均通过 stdin/stdout 进行 JSON 通信
- 错误处理返回格式：`{"ok": false, "error": "错误信息"}`
- 大规模操作支持通过中间消息报告进度
- 配置信息从 `config.json` 或环境变量中加载
- 并发操作有可配置的限制，以避免速率限制

## 错误处理

每个命令都会返回标准错误格式：

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

版本: v1
- ✅ 命令结构已定义
- ✅ 参数验证已实现
- ✅ arXiv 集成正在进行中
- ✅ 使用 scholarly 库集成 Google Scholar
- ✅ 集成 Zotero API
- ✅ 使用 pymupdf pdfplumber 和 OpenAI API 实现了 LLM 分析流程