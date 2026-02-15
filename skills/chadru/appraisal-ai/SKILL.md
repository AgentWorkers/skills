---
name: appraisal-ai
description: >
  Automated appraisal report drafting pipeline. Scans project workfiles
  (PDFs, deeds, assessor cards, CoStar reports), extracts structured data,
  and generates Word narrative drafts with tracked changes and Excel
  adjustment grids from master templates. Supports land-only, improved,
  condemnation, and custom template packs.
metadata: {"clawdbot":{"emoji":"🏠","requires":{"bins":["python3"]}}}
---

# 评估AI — 报告起草流程

该流程根据主模板和项目工作文件数据生成包含**修订痕迹的Word文档草稿**以及**Excel调整表格**。所有替换内容在Word审阅模式下均可见，用户可以接受或拒绝这些修改。

## 先决条件

使用此功能前，需在本地安装`appraisal_ai`仓库：

```
~/appraisal_ai/
├── scripts/utils.py          — core utilities
├── templates/<pack-name>/    — template packs (narrative.docx, grid.xlsx, reference-data.md)
├── .claude/agents/           — agent specs for the pipeline
├── .claude/skills/           — slash command definitions
├── CLAUDE.md                 — full rules, workflow, and lessons learned
└── requirements.txt          — Python dependencies
```

**设置虚拟环境（仅一次）：**

```bash
python3 -m venv ~/appraisal_ai/venv
~/appraisal_ai/venv/bin/pip install -r ~/appraisal_ai/requirements.txt
```

请始终使用`~/appraisal_ai/venv/bin/python`来运行脚本。

## 项目文件夹结构

每个评估项目都遵循以下文件夹结构：

```
2026-NNN Address/
├── Subject/         — engagement letter, assessor card, deed, LOI, CoStar
├── Narrative/       — output drafts go here
├── Comparables/     — comp sheets, CoStar/MLS printouts, sale data
├── Exhibits/        — maps, photos, figures
└── Template/        — completed appraisal .docx and grid .xlsx
```

## 流程（5个阶段）

整个流程会分配10个代理任务，分为5个阶段执行：

### 第1阶段 — 阅读（3个代理，并行执行）
主题阅读器（Subject Reader）、比较阅读器（Comp Reader）和证据阅读器（Exhibit Reader）会扫描所有项目文档。使用`scripts/utils.py`中的`split_pdf()`函数将PDF文件分割成适合阅读的块（扫描后的文档每3页为一个块，文本较多的文档每5页为一个块）。

### 第2阶段 — 提取数据（2个代理，并行执行 → 暂停）
数据提取器（Field Extractor）生成`data.md`文件；比较表格生成器（Comp Grid Agent）生成`comp_grid.md`文件。在继续执行之前，系统会暂停，等待用户对`*** UPDATE ***`和`*** VERIFY ***`字段进行审核。

### 第3阶段 — 构建内容（3个步骤）
比较撰写器（Comp Writer）根据源文档生成`comp_writeups.md`文件；随后草稿生成器（Draft Builder）和表格生成器（Grid Builder）并行运行。草稿文件使用Word XML格式记录修订痕迹（`w:del`和`w:ins`标签）。表格数据会被写入指定的Excel工作表中（切勿直接使用`wb.active`）。

### 第4阶段 — 审核（2个代理，并行执行）
质量保证审核员（QA Reviewer）检查数据的一致性；USPAP审核员（USPAP Reviewer）检查合规性。系统会自动进行最多2次修复循环；每次修复后都必须重新构建文件。

### 第5阶段 — 最终审核（流程结束前不得交付文件）
系统会核对表格内容、文档草稿以及`data.md`文件中的数据是否一致。确认修订痕迹未被篡改，公式单元格保持原样，调整行未被修改。**只有在第5阶段审核通过后，才会向用户交付最终报告文件。**

## 数据文件

项目数据采用结构化的Markdown格式存储：

- `data.md`：项目相关字段（地址、日期、数值、参与方等）
- `comp_grid.md`：可比销售数据的详细信息（价格、销售金额、日期、出让人/受让人等）
- `comp_writeups.md`：每个可比销售的详细叙述内容
- `templates/<type>/reference-data.md`：模板中的可替换文本字符串

数据文件的读写操作通过`scripts/utils.py`中的`load_md()`和`save_md()`函数完成。

## 模板包

`templates/<name>/`目录下的每个模板包包含以下文件：
- `narrative.docx`：主模板（由用户提供，不存储在Git仓库中）
- `grid.xlsx`：调整表格模板（可选，由用户提供）
- `reference-data.md`：模板中所有可替换的文本字符串

自定义模板包的结构与此相同。用户需要提供自己的已完成评估报告作为主模板。

## 关键工具（`scripts/utils.py`）

- `extract_docx_text(path)`：从.docx文件中提取文本（注意：不要使用文件处理工具直接读取.docx文件，因为它是二进制XML格式）
- `extract_xlsx_text(path)`：从.xlsx文件中提取文本
- `split_pdf(path, pages_per_chunk)`：将大型PDF文件分割成便于处理的块
- `load_md(path)` / `save_md(data, path)`：用于读写结构化Markdown数据的函数
- 修订痕迹处理函数：`tracked_replace_in_run()`、`tracked_replace_across_runs()`、`tracked_delete_paragraph()`
- 表格处理函数：`find_table_by_text()`、`set_cell_text()`、`add_table_row()`
- Word XML格式处理函数：`next_change_id()`、`get_date()`、`make_tracked_delete()`

## Word XML格式的注意事项（每次保存时都必须遵守）

为避免Word文件出现“内容不可读”的错误，请遵守以下规则：
1. **XML声明必须使用双引号**。`etree.tostring()`函数生成的XML字符串使用单引号，因此在序列化后再将其替换为双引号。
2. 在`<w:del>`标签内部，删除的文本必须使用`<w:delText>`标签，而非`<w:t>`标签。请使用`make_tracked_delete()`函数进行正确处理。
3. 每个`<w:del>`和`<w:ins>`标签都必须具有唯一的`w:id`和`w:date`属性。请使用`next_change_id()`和`get_date()`函数生成唯一的标识符。

## 重要规则

- **所有文本替换操作都必须使用Word的修订痕迹功能**，严禁直接使用`w:t`标签进行文本替换。
- **处理Excel文件时严禁使用`wb.active`属性**，必须通过文件名来打开工作表。
- **严禁修改调整行**，这些内容属于评估人员的专业判断范围。
- **严禁修改标有`*** UPDATE ***`的表格单元格**；如果数据缺失，请保留模板中的默认值。
- **如果某个内容不存在于工作文件中，则应将其标记为不可用的模板元素并予以删除**。
- **报告内容应如实反映事实，不得加入评估人员的个人判断**；调整内容、比较结果和价值结论均由评估人员决定。
- **处理出让人/受让人相关信息时，务必先读取相关文件，并与CoStar数据库进行核对**；发现不一致之处需及时报告。
- **自动修复后必须重新构建文件**，即使只是进行微小的修改也不得跳过此步骤。

## 代理任务及技能要求

代理任务的详细说明请参见`.claude/agents/*.md`文件。
命令操作的定义请参见`.claude/skills/*.md`文件。
完整的流程规则、工作流程及经验总结请参阅`CLAUDE.md`文件。