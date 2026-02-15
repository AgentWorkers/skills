---
name: arxiv-paper-processor
description: "仅支持工具处理的论文处理功能，允许用户手动指定语言参数：支持批量下载多篇论文的成果文件或单篇论文的成果文件；之后模型会自动读取论文的源代码或PDF文件，并用用户选定的语言生成相应的`summary.md`文件。该功能适用于需要通过模型驱动而非脚本生成的方式来理解每篇论文内容的情况。"
---

# ArXiv 论文处理器

使用此技能可对每篇论文进行手动总结，并可选择批量下载相关文件。

- **单篇论文模式**：处理一个论文目录（例如 `<run_dir>/<arxiv_id>/`）。
- **批量预下载模式**：在编写摘要之前，先处理多个论文目录。

## 语言参数

- 使用一个工作流程语言参数（例如 `English` 或 `Chinese`），并手动设置该参数。
- 每篇论文的 `summary.md` 必须用所选语言编写。
- 如果直接调用下载脚本，请传递 `--language <LANG>` 以确保可追溯性。

## 核心原理

脚本仅负责下载文件；模型的任务是读取和编写摘要。

## 不可协商的约束

- 禁止通过基于脚本的片段提取、正则表达式匹配或模板填充来生成 `summary.md`。
- 禁止使用 Python 或 Shell 脚本来自动组合摘要或引言部分的文本。
- 本技能中的脚本仅用于下载文件（`source`/`pdf`）和记录日志。
- 最终的 `summary.md` 必须通过模型对论文内容的解析和合成来生成。

## 可选的批量文件下载（处理多篇论文）

当第二阶段包含大量论文时，请优先使用此功能：

```bash
python3 scripts/download_papers_batch.py \
  --run-dir /path/to/run \
  --artifact source_then_pdf \
  --max-workers 3 \
  --min-interval-sec 5 \
  --language English
```

**主要功能**：

- 支持 `--artifact source`、`--artifact pdf` 或 `--artifact source_then_pdf`（默认值）。
- 支持并发处理（`--max-workers`）以及安全的节流和重试机制（`--min-interval-sec`、重试参数）。
- 默认使用运行时的节流状态文件（`<run_dir>/.runtime/arxiv_download_state.json`）以降低 429 错误的风险。
- 如果论文已有可用的 `source/source_extract/*.tex` 文件或 `source/paper.pdf` 文件，则跳过该论文的下载（除非设置了 `--force`）。
- 具有良好的恢复能力：如果论文的 `summary.md` 已经生成，可以跳过该论文的摘要编写步骤。
- 默认将批量日志写入 `<run_dir>/download_batch_log.json`。

## 第一步：下载源文件（推荐）

```bash
python3 scripts/download_arxiv_source.py \
  --paper-dir /path/to/run/2602.00528 \
  --language English
```

此步骤会生成以下文件：

- `source/source_bundle.bin`
- `source/source_extract/`
- `source/download_source_log.json`

如果已存在可用的源文件且未设置 `--force`，脚本会重用现有的文件。

## 第二步（如有需要）：下载 PDF 文件

```bash
python3 scripts/download_arxiv_pdf.py \
  --paper-dir /path/to/run/2602.00528 \
  --language English
```

此步骤会生成以下文件：

- `source/paper.pdf`
- `source/download_pdf_log.json`

如果 PDF 文件已存在且未设置 `--force`，脚本会重用现有的文件。

## 第三步：模型读取并生成摘要

1. 如果 `summary.md` 已存在且格式正确，则跳过该论文并标记为已完成。
2. 首先读取 `metadata.md` 文件。
3. 如果 `source/source_extract/` 目录下有可读取的 `.tex` 文件，则直接使用这些文件。
4. 如果 `source/paper.pdf` 文件已存在，则直接使用 PDF 文件。
5. 如果两者都不存在，则先运行下载脚本（单篇论文脚本或批量脚本）。
6. 在同一论文目录中，用所选语言手动编写 `summary.md`。

**注意事项**：
- 不要依赖基于规则的自动摘要生成功能。
- 不要将自动提取的片段作为撰写摘要的主要依据。

## 质量要求**

- 每个部分都应包含可追溯到全文阅读的具体论文细节。
- 第 4、5、10 节应详细说明研究方法和评估过程，避免使用通用性表述。
- 如果原始文档中的关键细节不明确，请明确标注不确定性，而非猜测。
- 生成的摘要应与 `references/summary-example-en.md` 和 `references/summary-example-zh.md` 中展示的细节水平保持一致。
- 如果您的摘要草稿比示例内容简短或不够具体，请在完成前进行补充。

## 必需的输出结果**

- 生成格式规范的 `<paper_dir>/summary.md` 文件。
- 特别注意第 10 节（**简要结论**）：撰写一段 3-4 句的总结，涵盖论文的贡献、研究方法、评估方法和结果，并包含具体细节。
- 在第 1 节（**论文基本信息**）中，使用以下关键字段：`ArXiv ID`、`标题`、`作者`、`发表日期`、`主要类别`、`阅读依据`。
- 请使用标准的字段名称，避免使用变体形式（如 `Reading source`、`Author list`、`Published on` 等）。

有关详细的章节格式要求，请参阅 `references/summary-format.md`。

## 相关技能

此技能是 `arxiv-summarizer-orchestrator` 的子技能。

**在流水线中的位置**：

1. **第一步（上游）**：`arxiv-search-collector` 负责收集选定的论文目录和元数据。
2. **第二步（本技能）**：`arxiv-paper-processor` 下载文件并为每篇论文生成 `summary.md`。
3. **第三步（下游）**：`arxiv-batch-reporter` 使用这些摘要生成最终的汇总报告。

请将此技能与第一步和第三步结合使用，以实现完整的端到端处理流程。