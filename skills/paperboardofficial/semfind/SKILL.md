---
name: semfind
description: >
  **使用嵌入技术对本地文本文件进行语义搜索**  
  当 `grep` 或 `ripgrep` 由于无法识别精确的关键词而无法找到相关结果时，或者需要根据语义而非模式进行搜索时（例如，在日志中搜索 “deployment issue”，而实际文本却是 “container build failed”），可以使用这种方法。可以通过 `pip install semfind` 来安装该工具。它非常适合用于按语义搜索内存文件、项目文档、日志和笔记等内容。
---
# semfind

这是一个用于终端的“语义搜索”工具，它通过使用本地嵌入模型（基于 BAAI/bge-small-en-v1.5 和 FAISS 技术）来根据文件的内容进行搜索。无需使用 API 密钥。

## 何时使用 semfind

- 当 `grep` 或 `ripgrep` 没有找到结果或返回的结果不相关时；
- 当你不知道要搜索的关键词的具体表述时；
- 当你想根据概念或含义进行搜索，而不是精确的文本时。

**注意：** 如果 `grep` 能够正常工作，请不要使用 semfind，因为 `grep` 的搜索速度更快且没有任何性能开销。

## 安装

```bash
pip install semfind
```

首次运行时会下载一个约 65MB 大小的模型（耗时约 10-30 秒），后续运行将使用已缓存的模型。

## 使用方法

```bash
# Basic search
semfind "deployment issue" logs.md

# Search multiple files, top 3 results
semfind "permission error" memory/*.md -k 3

# With context lines
semfind "database migration" notes.md -n 2

# Force re-index after file changes
semfind "query" file.md --reindex

# Minimum similarity threshold
semfind "auth bug" *.md -m 0.5
```

## 常用选项

| 选项          | 描述                        | 默认值       |
|-----------------|----------------------------|------------|
| `-k, --top-k`     | 显示前 k 个结果                   | 5           |
| `-n, --context`    | 显示结果前后的上下文行数             | 0           |
| `-m, --max-distance` | 最小相似度阈值                 | 无            |
| `--reindex`     | 强制重新生成嵌入模型                 | false         |
| `--no-cache`    | 跳过嵌入模型缓存                   | false         |

## 输出格式

输出格式类似于 `grep`，同时会显示每个匹配项的相似度分数（分数越接近 1.0，表示匹配度越高）。

## 资源消耗

- 运行时占用约 250MB 的内存，退出程序后会立即释放这些内存；
- 约 65MB 的模型数据会被缓存到 `/tmp/fastembed_cache/` 目录中；
- 第一次查询耗时约 2 秒（用于加载模型），后续查询则利用缓存；
- 嵌入模型缓存文件位于 `~/.cache/semfind/`，文件内容更改后缓存会自动失效。

## 工作流程示例

```bash
# Step 1: Try grep first
grep "deployment" memory/*.md

# Step 2: If grep fails, use semfind
semfind "something went wrong with the deployment" memory/*.md -k 5
```