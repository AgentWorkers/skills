---
name: qmd
description: 使用 qmd 高效地搜索 Markdown 知识库。在搜索 Obsidian 文档库或 Markdown 集合时，可以利用该工具以最少的令牌使用量找到相关内容。
argument-hint: "<search query> [--collection <name>] [--semantic]"
---

# QMD 搜索技能

使用 qmd（一个本地索引工具）高效地搜索 Markdown 知识库。qmd 结合 BM25 算法和向量嵌入技术，仅返回相关的内容片段，而无需加载整个文件。

## 为什么使用它

- **减少 96% 的数据量**：仅返回相关的内容片段，无需读取整个文件。
- **即时结果**：预索引的内容使得搜索速度非常快。
- **本地化且私密**：所有的索引和搜索操作都在本地完成。
- **混合搜索**：使用 BM25 算法进行关键词匹配，通过向量搜索来评估内容的语义相似性。

## 命令

### 搜索（基于 BM25 的关键词匹配）
```bash
qmd search "your query" --collection <name>
```
快速、准确的基于关键词的搜索。适用于搜索特定的术语或短语。

### 向量搜索（语义搜索）
```bash
qmd vsearch "your query" --collection <name>
```
基于语义相似性的搜索。适用于那些表述可能有多种变体的概念性查询。

### 混合搜索（结合两种方法并进行重新排序）
```bash
qmd hybrid "your query" --collection <name>
```
结合 BM25 和向量搜索的结果，并使用大型语言模型（LLM）进行重新排序。这种方法最为全面，但通常也会增加搜索时间。

## 使用方法

1. **检查集合是否存在**：
   ```bash
   qmd collection list
   ```

2. **在集合中搜索**：
   ```bash
   # For specific terms
   qmd search "api authentication" --collection notes

   # For conceptual queries
   qmd vsearch "how to handle errors gracefully" --collection notes
   ```

3. **阅读结果**：qmd 会返回包含文件路径和相关上下文的相关内容片段。

## 设置（如果未安装 qmd）

```bash
# Install qmd
bun install -g https://github.com/tobi/qmd

# Add a collection (e.g., Obsidian vault)
qmd collection add ~/path/to/vault --name notes

# Generate embeddings for vector search
qmd embed --collection notes
```

## 调用示例

```
/qmd api authentication          # BM25 search for "api authentication"
/qmd how to handle errors --semantic   # Vector search for conceptual query
/qmd --setup                     # Guide through initial setup
```

## 最佳实践

- 使用 **BM25 搜索**（`qmd search`）来搜索特定的术语、名称或技术关键词。
- 当需要搜索表述可能有多种变体的概念时，使用 **向量搜索**（`qmd vsearch`）。
- 除非需要最高的召回率，否则避免使用混合搜索——因为它会更慢。
- 在添加大量新内容后，重新运行 `qmd embed` 以更新向量索引。

## 参数处理

- `$ARGUMENTS` 包含完整的搜索查询。
- 如果存在 `--semantic` 标志，使用 `qmd vsearch` 而不是 `qmd search`。
- 如果存在 `--setup` 标志，指导用户完成安装和集合配置。
- 如果指定了 `--collection <名称>`，则使用该集合；否则默认使用可用的集合。

## 工作流程

1. 从 `$ARGUMENTS` 中解析参数。
2. 检查 qmd 是否已安装（使用 `which qmd` 命令）。
3. 如果未安装，提供安装指导。
4. 如果需要搜索：
   - 如果没有指定集合，则列出所有可用的集合。
   - 运行相应的搜索命令。
   - 向用户展示包含文件路径的结果。
5. 如果用户想要阅读某个具体结果，可以使用相应的工具来读取该文件。