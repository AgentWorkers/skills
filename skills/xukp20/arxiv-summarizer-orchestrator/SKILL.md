---
name: arxiv-summarizer-orchestrator
description: "端到端的编排技能，用于定期从 arXiv 网站收集数据并生成报告。该技能由三个子技能组成：`arxiv-search-collector`（用于搜索论文）、`arxiv-paper-processor`（用于处理收集到的论文）以及 `arxiv-batch-reporter`（用于批量生成报告）。支持对所有 Markdown 输出内容进行手动语言设置，并支持第二阶段（Stage-B）的处理策略（默认为 `subagent_parallel`，最多支持 5 个并发任务；也可选择串行处理）。"
---

# ArXiv 摘要生成与报告编排器

通过组合三个子技能来运行整个流程。

## 子技能执行顺序

1. `arxiv-search-collector`
2. `arxiv-paper-processor`
3. `arxiv-batch-reporter`

## 工作流参数

- `language`：所有阶段使用的手动语言参数。省略时默认为英语。
- `paper_processing_mode`：`subagent_parallel` 或 `serial`。
- `max_parallel_papers`：当 `paper_processing_mode` 为 `subagent_parallel` 时，默认值为 `5`。

## 工作流流程

### 第一阶段：数据收集与查询检索

1. 使用 `arxiv-search-collector/scripts/init_collection_run.py` 初始化一次运行。
2. 模型根据原始主题生成多个针对性的查询，并生成一个简化的 `query_plan.json` 文件（仅包含 `label` 和 `query`）。
3. 推荐使用 `arxiv-search-collector/scripts/fetch_queries_batch.py` 根据该计划文件执行查询。
4. （可选）手动调用 `arxiv-search-collector/scripts/fetch_query_metadata.py` 进行逐个查询的获取。
5. 模型读取每个索引的查询列表并决定哪些查询需要保留。
6. 使用 `arxiv-search-collector/scripts/merge_selected_papers.py` 合并选定的查询结果。
7. 如果查询的相关性或覆盖范围仍然不理想，重复执行第一阶段：
   - 生成新的查询计划。
   - 重新执行查询。
   - 使用 `--incremental` 参数和更新的 `selection-json` 文件重新合并结果。
   - 将不需要的查询标记为空列表（`[]`），以明确排除它们。

通过传递 `--language <LANG>` 参数给收集脚本，可以确保第一阶段生成的 markdown 文件使用指定的语言。
在第一阶段使用串行查询方式，并设置适当的控制参数（例如 `--min-interval-sec 5`、`--retry-max 4`）。
默认的收集器设置已经包含了重试、退避机制以及运行状态管理（`<run_dir>/.runtime/arxiv_api_state.json`），因此通常不需要手动调整。
除非查询参数发生变化或需要数据更新，否则建议重用缓存（不使用 `--force` 参数）。

**输出**：一个包含每篇论文元数据的子目录的运行目录。

### 第二阶段：下载论文文档并生成摘要

对于每篇论文的目录，调用子技能 `arxiv-paper-processor` 一次，让该技能生成 `<paper_dir>/summary.md` 文件。

**推荐的操作步骤（适用于多篇论文的情况）：**

1. 在读取每篇论文之前，先执行一次批量文档下载：

```bash
python3 arxiv-paper-processor/scripts/download_papers_batch.py \
  --run-dir /path/to/run \
  --artifact source_then_pdf \
  --max-workers 3 \
  --min-interval-sec 5 \
  --language <LANG>
```

**`arxiv-paper-processor` 内部的执行步骤：**

1. 如果 `<paper_dir>/summary.md` 文件已经存在且内容完整，则跳过该论文。
2. 如果论文的源代码（`source/source_extract/*.tex`）或 PDF 文件（`source/paper.pdf`）已经存在，则跳过下载。
3. 如果文档缺失，使用 `arxiv-paper-processor/scripts/download_arxiv_source.py` 下载源代码。
4. 如果源代码无法使用，使用 `arxiv-paper-processor/scripts/download_arxiv_pdf.py` 下载 PDF 文件。
5. 模型读取内容，并使用指定的语言手动生成 `<paper_dir>/summary.md` 文件。

**多篇论文的并行处理策略：**

- 默认设置：`paper_processing_mode=subagent_parallel`，`max_parallel_papers=5`。
- 可选设置：`paper_processing_mode=serial`，以顺序处理每篇论文。
- 在并行模式下，分批运行多个 `arxiv-paper-processor` 实例；同时处理的论文数量不得超过 `max_parallel_papers`。
- 等待一批任务完成后，再开始下一批任务。
- 在串行模式下，每次只运行一个 `arxiv-paper-processor` 实例。
- 每个子代理工作进程应只负责处理一个论文目录，以避免文件冲突。
- 不要使用脚本自动生成摘要内容；这些脚本仅用于下载文档。

**输出**：所有论文目录中都包含 `summary.md` 文件。

### 第三阶段：合并摘要并生成最终报告

1. 运行 `arxiv-batch-reporter/scripts/collect_summaries_bundle.py --language <LANG>`。
2. 模型读取 `summaries_bundle.md` 文件，并在基础目录中生成 `collection_report_template.md`。
3. 在模板中，每篇论文的条目中必须包含一个占位符：`{{ARXIV_BRIEF:<arxiv_id>}`。
4. 运行 `arxiv-batch-reporter/scripts/render_collection_report.py` 生成最终的 `collection_report.md`。
5. 最终报告中的结论部分不应手动重新编写；这些内容应通过脚本从每篇论文的 `summary.md` 文件的第 10 节中提取。

如果指定的语言不是英语（例如中文），所有中间生成的 markdown 文件和最终报告都应使用该语言。

## 定期调度

此编排器适合在 OpenClaw 中通过 cron 或定时任务执行：

- 常见执行频率：每日、每周、每月。
- 在初始化运行时，可以使用 `1d`、`7d`、`30d` 等时间窗口进行数据回顾。

## 输出文件结构

`<output-root>/<topic>-<timestamp>-<range>/`

- `task_meta.json`, `task_meta.md`
- `query_results/`, `query_selection/`
- `<arxiv_id>/metadata.md` + 下载的源代码/PDF 文件 + `summary.md`
- `summaries_bundle.md`
- `collection_report_template.md`
- 最终生成的报告文件（例如 `collection_report.md`

使用 `references/workflow-checklist.md` 作为执行检查清单。

## 相关技能

这是顶层编排技能。在使用之前，请安装并启用以下三个子技能：

- `arxiv-search-collector`
- `arxiv-paper-processor`
- `arxiv-batch-reporter`

**此编排器内的执行顺序：**

1. `arxiv-search-collector`（第一阶段）
2. `arxiv-paper-processor`（第二阶段）
3. `arxiv-batch-reporter`（第三阶段）