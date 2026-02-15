---
name: enhanced-memory
description: 改进后的内存搜索功能结合了混合向量技术与关键词评分机制、时间路由算法、文件路径评分系统、自适应权重分配机制、伪相关性反馈机制以及知识图谱交叉引用功能。该系统用一个四信号融合检索系统替代了原有的内存搜索机制，适用于搜索内存数据、索引内存文件、构建交叉引用以及评估内存数据的显著性。使用时需要依赖配备 nomic-embed-text 模型的 Ollama 模型。
---

# 增强型内存系统

这是一个针对 OpenClaw 内存系统的插件式增强功能。它将原有的平面向量搜索方式替换为一种基于 4 个信号的混合检索流程，该流程的检索准确率达到了 **0.782 MRR**（相比之下，仅使用向量的方法准确率约为 0.45）。

## 设置

```bash
# Install Ollama and pull the embedding model
ollama pull nomic-embed-text

# Index your memory files (run from workspace root)
python3 skills/enhanced-memory/scripts/embed_memories.py

# Optional: build cross-reference graph
python3 skills/enhanced-memory/scripts/crossref_memories.py build
```

每当内存文件发生显著变化时，重新运行 `embed_memories.py` 脚本。

## 脚本

### `scripts/search_memory.py` — 主要搜索功能

采用基于 4 个信号的混合检索方式，并具备自动适应机制：

**融合的信号包括：**
1. **向量相似度**（0.4）——通过 `nomic-embed-text` 嵌入模型计算余弦相似度
2. **关键词匹配**（0.25）——查询词与文件片段的匹配程度
3. **标题匹配**（0.1）——查询词出现在文件标题中的情况
4. **文件路径匹配**（0.25）——查询词与文件/目录名称的匹配程度

**自动调整机制：**
- **时间相关性**：包含日期信息的查询（如 “昨天”、“2 月 8 日”、“上周一”）在匹配文件时获得 3 倍的权重加成
- **自适应权重分配**：当关键词匹配度较低时，系统会增加向量信息的权重占比至 85%
- **伪相关性反馈（PRF）**：当最高得分低于 0.45 时，系统会使用初始搜索结果中的词汇重新进行查询并重新评分

### `scripts/enhanced_memory_search.py` — 兼容 JSON 的搜索功能

该脚本使用相同的检索流程，但输出格式为 JSON，可与 OpenClaw 的 `memory_search` 工具直接对接：

**输出格式：`{results: [{path, startLine, endLine, score, snippet, header}], ...}`**

### `scripts/embed_memories.py` — 索引功能

该脚本会根据 `.md` 文件的 Markdown 标题对 `memory/` 目录下的所有文件以及核心工作区文件（如 `MEMORY.md`、`AGENTS.md` 等）进行索引处理：

**输出文件：`memory/vectors.json`**。嵌入数据按 20 个为一组进行分组处理，并将每个文件的片段截断至 2000 个字符。

### `scripts/memory_salience.py` — 重要性评分功能

该脚本用于识别出陈旧或重要的内存内容，以便在需要时自动提示用户：

**评分依据：** 文件的重要性 × 陈旧程度，同时考虑文件类型（核心文件 > 日常文件）、文件大小、访问频率以及查询词与内容的相关性。

### `scripts/crossref_memories.py** — 知识图谱构建功能

该脚本利用嵌入模型的相似度信息，在内存片段之间建立交叉引用链接：

**实现方式：** 为每个文件选取最具代表性的 5 个片段进行比较，从而将时间复杂度从 O(n²) 降低到可管理的水平。相似度阈值：0.75

## 配置参数

所有可调整的配置参数都位于每个脚本的顶部。主要参数如下：

| 参数            | 默认值        | 脚本           | 作用                |
|-----------------|-------------|-----------------|-------------------|
| `VECTOR_WEIGHT`     | 0.4         | search_memory.py     | 向量相似度的权重           |
| `KEYWORD_WEIGHT`     | 0.25         | search_memory.py     | 关键词匹配的权重           |
| `FILEPATH_WEIGHT`     | 0.25         | search_memory.py     | 文件路径匹配的权重           |
| `TEMPORAL_BOOST`     | 3.0         | search_memory.py     | 日期相关文件的权重加成因子       |
| `PRF_THRESHOLD`     | 0.45         | search_memory.py     | 触发伪相关性反馈的阈值       |
| `SIMILARITY_THRESHOLD` | 0.75         | crossref_memories.py     | 建立交叉引用的最低相似度阈值     |
| `MODEL`         | nomic-embed-text   | 所有脚本         | 使用的嵌入模型           |

如需使用其他嵌入模型（例如 `mxbai-embed-large`），请在相应脚本中修改 `MODEL` 参数，然后重新运行 `embed_memories.py`。

## 集成方式

要替换默认的内存搜索功能，只需将代理程序的搜索模块指向这些脚本即可。这些脚本要求：
- 工作区根目录下存在包含 `.md` 文件的 `memory/` 目录
- 存在由 `embed_memories.py` 生成的 `memory/vectors.json` 文件
- Ollama 模型需在本地运行，并监听 11434 端口

所有脚本仅依赖 Python 标准库和 Ollama 的 HTTP API，无需额外安装任何第三方库（如 pip）。