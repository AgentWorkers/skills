---
name: zettel-link
description: 该技能负责维护 Zettelkasten 的笔记嵌入功能，支持搜索笔记、检索笔记以及发现笔记之间的关联。
---
# Zettel Link 技能

该技能提供了一套幂等的 Python 脚本，用于使用语义相似性在 Obsidian 文档库中嵌入、搜索和链接笔记。所有脚本都位于 `scripts/` 目录下，并支持多种嵌入提供者。

当用户需要搜索笔记、检索笔记或发现笔记之间的关联时，应触发此技能。

如果搜索目录已使用嵌入数据进行索引，系统会提示用户是否需要创建新的嵌入数据。

## 依赖项

- uv 0.10.0+
- Python 3.10+
- 以下任一嵌入提供者：
  - [Ollama](https://ollama.com)（使用 `mxbai-embed-large`，默认值）
  - [OpenAI API](https://platform.openai.com/)（使用 `text-embedding-3-small`）
  - [Google Gemini API](https://ai.google.dev/)（使用 `text-embedding-004`）

## 命令概览

- `uv run scripts/config.py`：配置嵌入模型和其他设置。
- `uv run scripts/embed.py`：将笔记嵌入并缓存到 `.embeddings/embeddings.json` 文件中。
- `uv run scripts/search.py`：对嵌入的笔记进行语义搜索。
- `uv run scripts/link.py`：发现笔记之间的语义关联，并将结果输出到 `.embeddings/links.json` 文件中。

## 工作流程

### 第 0 步 — 设置与配置

如果 `config/config.json` 文件不存在，请创建它：

```bash
uv run scripts/config.py
```

这将创建一个包含默认配置的 `config/config.json` 文件：

```json
{
    "model": "mxbai-embed-large",
    "provider": {
        "name": "ollama",
        "url": "http://localhost:11434"
    },
    "max_input_length": 8192,
    "cache_dir": ".embeddings",
    "default_threshold": 0.65,
    "top_k": 5,
    "skip_dirs": [".obsidian", ".trash", ".embeddings", "Spaces", "templates"],
    "skip_files": ["CLAUDE.md", "Vault.md", "Dashboard.md", "templates.md"]
}
```

要使用远程提供者，请执行以下操作：

```bash
# OpenAI
uv run scripts/config.py --provider openai

# Gemini
uv run scripts/config.py --provider gemini

# Custom model
uv run scripts/config.py --provider openai --model text-embedding-3-large
```

要调整配置参数，请执行以下操作：

```bash
uv run scripts/config.py --top-k 10 --threshold 0.7 --max-input-length 4096
```

### 第 1 步 — 创建嵌入数据

```bash
uv run scripts/embed.py --input <directory>
```

此步骤会生成 `<directory>/.embeddings/embeddings.json` 文件，其中包含嵌入缓存数据。

- **增量更新**：仅重新嵌入自上次运行以来被修改的文件（基于文件修改时间）。
- **文本截断**：在嵌入之前自动将文本截断到 `max_input_length` 长度。
- **失效数据清除**：删除已不存在的文件的条目。
- **强制重新嵌入**：使用 `--force` 选项强制重新嵌入所有文件。

### 第 2 步 — 语义搜索

```bash
uv run scripts/search.py --input <directory> --query "<query>"
```

使用配置的提供者将查询内容嵌入，并与所有缓存中的嵌入数据进行比较，返回最相似的 `top_k` 条笔记。

搜索结果将保存到 `<directory>/.embeddings/search_results.json` 文件中。

### 第 3 步 — 发现语义关联

```bash
uv run scripts/link.py --input <directory>
```

计算所有笔记对之间的余弦相似度，并将相似度超过 `default_threshold` 的关联输出到 `<directory>/.embeddings/links.json` 文件中。

输出内容包括：
- 所有关联对的列表及其得分
- 每个笔记的详细信息（便于查找）

**调整方法**：通过修改 `--threshold` 参数来扩大或缩小关联发现的范围。

## 缓存

- **格式**：包含元数据的 JSON 文件（`metadata` + `data`）
- **存储位置**：`<directory>/.embeddings/embeddings.json`
- **元数据**：记录生成时间、使用的模型、嵌入大小等信息
- **失效机制**：根据文件修改时间（`mtime`）来更新缓存
- **强制重建**：可以删除缓存文件或使用 `--force` 选项强制重建缓存

## 使用说明

使用此技能时，请遵循以下规则：
1. 如果 `config/config.json` 文件不存在，请先运行 `config.py`。
2. 在运行 `search.py` 或 `link.py` 之前，必须先运行 `embed.py`（以确保缓存已生成）。
3. 对于远程提供者（如 openai、gemini），请确保已设置 API 密钥环境变量（或在技能目录中提供 `.env` 文件）。
4. 所有脚本都是幂等的，可以安全地重复运行。