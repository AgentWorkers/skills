---
name: boof
description: "将 PDF 文件和文档转换为 Markdown 格式，然后在本地建立索引以便进行 RAG（Retrieval Against Graphs）检索，并高效地进行文本分析。适用于以下场景：阅读/分析/总结 PDF 文件、处理文档、从论文、资料夹或 NOFO（Notice of Filing）中提取信息；或者在需要处理大量文档但不想占用太多屏幕空间的情况下使用该工具。支持批量处理和跨文档查询功能。"
---

# Boof 🍑

本地优先的文档处理流程：PDF → Markdown → RAG（Retrieval, Association, and Generation）索引 → 高效的文本分析。

文档始终保存在本地，只有相关的内容才会被传输到大型语言模型（LLM）中。这样既能最大限度地吸收知识，又能最小化文本处理过程中所需的“标记”（tokens）数量。

## 快速参考

### 将文档转换为Markdown并创建索引
```bash
bash {SKILL_DIR}/scripts/boof.sh /path/to/document.pdf
```

### 使用自定义集合名称进行转换
```bash
bash {SKILL_DIR}/scripts/boof.sh /path/to/document.pdf --collection my-project
```

### 查询索引内容
```bash
qmd query "your question" -c collection-name
```

## 核心工作流程

1. **转换文档**：运行 `boof.sh` 命令，将PDF文件通过Marker工具（基于本地机器学习模型，无需使用API）转换为Markdown格式，并将其索引到QMD系统中以便进行语义搜索。
2. **查询内容**：使用 `qmd query` 命令仅获取相关的内容片段，而不是整个文档。
3. **进行分析**：LLM仅接收经过筛选的、相关的文本片段，从而避免浪费标记资源，也避免了处理过程中出现的信息丢失问题。

## 各种方法的适用场景

- **“分析论文的某个特定方面”**：使用 `boof` 和 `query`（成本最低，最精准）。
- **“总结整篇文档”**：先使用 `boof` 将文档转换为Markdown格式，然后逐节阅读并总结每个部分的内容，最后合并这些总结。详情请参阅 [advanced-usage.md](references/advanced-usage.md)。
- **“比较多篇论文的发现结果”**：先将所有论文的内容转换为同一个集合，再进行查询。
- **“查找论文中提到某内容的地方”**：使用 `qmd search "X" -c collection` 进行精确匹配；使用 `qmd query "X" -c collection` 进行语义匹配。

## 输出位置

转换后的Markdown文件默认保存在 `knowledge/boofed/` 目录中（可通过 `--output-dir` 参数自定义输出路径）。

## 设置

如果 `boof.sh` 报告缺少依赖项，请参阅 [setup-guide.md](references/setup-guide.md) 以获取安装说明（涉及Marker和QMD工具的配置）。

## 环境变量

- `MARKER_ENV`：Marker工具的Python虚拟环境路径（默认：`~/.openclaw/tools/marker-env`）
- `QMD_BIN`：qmd工具的二进制文件路径（默认：`~/.bun/bin/qmd`）
- `BOOF_OUTPUT_DIR`：默认的输出目录（默认：`~/.openclaw/workspace/knowledge/boofed`）