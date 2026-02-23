---
name: literature-manager
description: 搜索、下载、转换、整理和审核学术文献集合。当需要查找论文、构建文献库、将论文添加到参考文献中、下载PDF文件、将论文转换为Markdown格式、按类别整理参考文献、审核参考文献集合，或收集论文中提到的工具的代码/数据集链接时，可以使用该功能。
---
# 文献管理器

用于管理学术文献集合：搜索 → 下载 → 转换 → 组织 → 验证。

## 依赖项

- `pdftotext`（来自 poppler-utils）——用于提取 PDF 文本内容
- `curl` — 用于下载文件
- `python3` — 用于处理 JSON 数据
- `file`（来自 coreutils）——用于验证 PDF 文件的格式
- `uvx markitdown[pdf]`（可选）——作为 PDF 到 Markdown 的转换工具（注意：普通的 `uvx markitdown` 无法正确处理 PDF 文件，必须使用 `uvx markitdown[pdf]`）

## 快速入门

```bash
# Download a single paper by DOI
bash scripts/download.sh "10.1038/s41592-024-02200-1" output_dir/

# Convert PDF to markdown
bash scripts/convert.sh paper.pdf output.md

# Verify a single PDF+MD pair
bash scripts/verify.sh paper.pdf paper.md

# Full audit of a references/ folder
bash scripts/audit.sh /path/to/references/
```

## 工作流程

### 1. 搜索

使用 `web_fetch` 在 Google Scholar 上进行搜索：
```
https://scholar.google.com/scholar?q=QUERY&as_ylo=YEAR
```
提取以下信息：标题、作者、发表年份、期刊名称、DOI（数字对象标识符）以及 PDF 链接。

对于每个搜索结果，确定最佳的开放获取 PDF 来源（详见“下载策略”）。

### 2. 下载

针对每篇论文，运行 `scripts/download.sh <DOI_or_URL> <output_dir/>` 命令。脚本会按以下顺序尝试从不同来源下载文件：
1. 直接从出版社获取 PDF 文件（例如 Nature、eLife、Frontiers、PNAS、bioRxiv、arXiv）
2. EuropePMC（通过 `PMC_ID` 下载 PDF 文件）
3. bioRxiv 或 arXiv 的预印本
4. **Sci-Hub** — `https://sci-hub.box/<DOI>`（当出版社设置付费访问限制时使用）

```bash
# Sci-Hub download example:
curl -L "https://sci-hub.box/10.1038/nature12345" -o paper.pdf
```

> ⚠️ **法律声明：** 在某些司法管辖区，使用 Sci-Hub 可能会违反出版社的服务条款或版权法。请确保您了解并接受相关法律风险后再使用该服务。

如果所有下载渠道均失败（包括 Sci-Hub），则将该论文标记为需要手动下载的论文，并向用户提供该论文的 DOI。

### 3. 转换

运行 `scripts/convert.sh <input.pdf> <output.md>` 命令。该脚本使用 `pdftotext` 进行转换，同时 `uvx markitdown[pdf>` 作为备用转换工具。

**提示：** 当需要保留论文中的表格和图表标题等详细信息时，建议优先使用 `uvx markitdown[pdf]` 而不是 `pdftotext`。

### 4. 组织

采用标准的文件夹结构进行文件管理：
```
references/
├── README.md              # Human index (summaries per category)
├── index.json             # Machine index (structured metadata)
├── RESOURCES.md           # Code repos + datasets
├── resources.json         # Structured version
├── <category-1>/
│   ├── papers/            # PDFs
│   └── markdown/          # Converted text
└── <category-N>/
    ├── papers/
    └── markdown/
```

文件夹的命名规则由用户自行定义。文件名前缀可用于排序（例如：`01-theoretical-frameworks/`）。

#### 每篇论文的 `index.json` 文件结构
```json
{
  "id": "short_id",
  "title": "Full title",
  "authors": ["Author1", "Author2"],
  "year": 2024,
  "journal": "Journal Name",
  "doi": "10.xxxx/...",
  "category": "category_name",
  "subcategory": "optional",
  "pdf_path": "category/papers/filename.pdf",
  "markdown_path": "category/markdown/filename.md",
  "tags": ["tag1", "tag2"],
  "one_line_summary": "English one-liner",
  "key_concepts": ["concept1"],
  "relevance_to_project": "English description"
}
```

#### `README.md` 文件的格式

每个文件夹内的每篇论文文件应包含以下信息：标题、作者、发表年份、期刊名称、DOI 以及用户自定义的简短摘要。

### 4b. 基于 DOI 的文件命名规则

下载后的文件通常会使用 DOI 格式命名，而不是 `AuthorYear` 格式：
```
10-1038_ncomms3018.md        # DOI: 10.1038/ncomms3018
10-1016_j-neuron-2015-03-034.md
```

当 `index.json` 文件中的 `markdown_path` 字段不再准确（例如在文件夹重新组织后），需要维护一个单独的映射文件来更新文件路径：
```json
// temp/paper_md_mapping.json
{
  "author2024_keyword": "references/new-downloads/10-1038_s41592-024-02200-1.md",
  ...
}
```

更新映射文件的步骤如下：将 `index.json` 中的每个论文 DOI 与磁盘上的实际文件路径进行关联。可以使用 `find` 命令结合 Python 脚本来自动化完成这一过程。

#### `index.json` 文件使用中的常见问题

- **`id: null` 错误**：如果多个条目的 `id` 值为 `null` 且共享相同的 `pdf_path`，则说明索引文件可能在批量写入过程中损坏。此时需要根据磁盘上的实际文件重新生成索引。
- **DOI 错误**：请确保 DOI 值正确无误（DOI 字段中的拼写错误很常见，例如后缀数字错误）。务必与出版社的官方页面进行核对。
- **失效的 `markdown_path`：文件夹重新组织后，`index.json` 中的 `markdown_path` 可能指向错误的文件位置。此时请参考上述映射文件来获取正确的文件路径。

### 5. 验证

运行 `scripts/audit.sh <references_dir/>` 命令进行全面验证：
- 确保所有 PDF 文件都是有效的（使用 `file -b` 命令检查文件格式）；
- 确保 PDF 文件的标题与文件名一致；
- 确保每个 PDF 文件都有对应的 Markdown 文件；
- 确保 `index.json` 文件内容完整、路径正确且没有重复的 DOI；
- 确保 `README.md` 文件中的统计信息与实际文件数量一致。

### 6. 收集资源

对于工具或方法相关的论文，需要查找其对应的 GitHub 仓库和公共数据集，并将这些资源存储在 `RESOURCES.md` 和 `resources.json` 文件中。

## 子代理策略

对于大量论文的处理，可以采用并行任务的方式：
- **下载**：每批约 5-8 篇论文分配一个子代理任务；
- **组织**：专门有一个子代理任务负责生成索引文件；
- **验证**：使用独立的子代理任务进行验证（验证过程不应与文件组织任务重复）。

**注意：** 验证任务必须由专门的子代理执行，以避免自我评估导致的错误。

### ⚠️ 子代理运行规则（根据实践经验总结）

1. **一次处理一批论文**：避免同时启动多个任务，否则大型语言模型（LLM）的速率限制可能导致任务失败而无法被及时发现；
2. **为长时间运行的任务设置定时监控**：子代理可能在运行过程中出现故障而不会自动触发通知，因此需要通过定时任务来监控它们的运行状态；
3. **定时监控的配置示例**：
   ```
   1. Spawn agent(s)
   2. Immediately set a cron job (every 10-15 min, isolated agentTurn)
      → Check if expected output files exist
      → Re-spawn failed agents
      → When all complete: announce + delete cron
   3. After task finishes, confirm cron was removed
   ```

## 动态添加论文

若要向现有文献集合中添加新论文，请按照以下步骤操作：
1. 下载新论文并将其转换为正确的文件夹结构；
2. 将新论文的元数据添加到 `index.json` 文件中；
3. 更新 `README.md` 文件中的统计信息；
4. 运行 `audit.sh` 命令来验证数据的一致性。