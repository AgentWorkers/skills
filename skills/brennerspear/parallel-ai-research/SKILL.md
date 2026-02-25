---
name: research
description: 针对某个主题进行开放式研究，同时构建一个动态更新的 Markdown 文档。该工具支持交互式和深入的研究模式。
---
# 研究技能

## 描述
针对某个主题进行开放式研究，并生成一个实时更新的 Markdown 文档。对话是短暂的，但文档才是最重要的。

## 触发条件
当用户希望：
- 对某个主题、想法或问题进行研究
- 在开始实际开发之前先探索相关内容
- 调查各种选项、模式或方法
- 创建一个“研究文档”或“调查报告”
- 对复杂主题进行深入的异步研究时，该功能会被激活。

## 研究目录结构
每个研究主题都有一个独立的文件夹：
```
~/.openclaw/workspace/research/<topic-slug>/
├── prompt.md          # Original research question/prompt
├── research.md        # Main findings (Parallel output or interactive notes)
├── research.pdf       # PDF export (when generated)
└── ...                # Any other related files (data, images, etc.)
```

---

## 两种研究模式

### 1. 交互式研究（默认模式）
适用于用户通过对话共同探索某个主题的情况。用户可以实时搜索、整理并更新文档。

### 2. 深度研究（异步模式）
适用于需要全面调查的复杂主题。该模式通过 `parallel-research` CLI 使用 Parallel AI API 进行处理，耗时数分钟至数小时，最终会生成详细的 Markdown 报告。

**何时使用深度研究：**
- 市场分析、竞争态势研究
- 需要大量收集技术资料的技术性深入研究
- 需要多方面探讨的多维度问题
- 当用户明确要求进行深度研究或希望获得全面覆盖时

---

## 交互式研究工作流程

### 1. 初始化研究
1. 在 `~/.openclaw/workspace/research/<主题名>/` 目录下创建研究文件夹。
2. 创建 `prompt.md` 文件，记录原始研究问题。
3. 创建 `research.md` 文件，设置文档的基本结构。
4. 与用户确认文件夹已创建，并询问首先应该探索哪些内容。

### 2. 研究循环
- 进行研究：进行网络搜索、查阅文档、研究相关代码。
- 更新文档：添加研究发现的结果、已解答的问题以及参考资料。
- 展示进度：仅展示新增内容，避免重复已有信息。
- 提出下一步的研究方向：以问题或建议的形式结束对话。

**关键操作：**
- 优先更新现有内容，而不是创建新章节。
- 使用项目符号列出研究发现，用段落形式总结要点。
- 对不确定的内容标注“似乎如此”、“根据某来源”或“未经验证”。
- 尽可能提供资料来源的链接。

### 3. 综合整理（定期检查）
每进行 5-10 次交流后，建议：
- 编写“当前理解”总结。
- 删除冗余的信息。
- 如果文档结构过于复杂，进行重新整理。
- 检查是否存在遗漏的方面。

### 4. 研究完成
当研究完成后，在 `research.md` 文件中更新状态：
- “状态：完成” — 研究已完成，可作为参考资料长期保存。
- “状态：进行中” — 文档仍处于更新状态。

**如果研究是为了某个项目的开发：**
- 将文档移至 `~/specs/<项目名>.md` 作为项目规范。
- 或者根据研究结果直接创建项目。
- 将状态更新为“状态：已完成 → ~/specs/...”。

大多数研究只是初步探索，并不需要直接转化为项目规范。只有当您真正打算基于这些研究结果开展实际工作时，才需要将其转化为项目规范。

---

## 深度研究工作流程

### 1. 启动深度研究
```bash
parallel-research create "Your research question" --processor ultra --wait
```

**处理器选项：**
- `lite`、`base`、`core`、`pro`、`ultra`（默认值）、`ultra2x`、`ultra4x`、`ultra8x`
- 通过添加后缀 `-fast` 可提高处理速度（例如：`ultra-fast`、`pro-fast` 等）。

**其他选项：**
- `-w, --wait` — 等待研究完成后再显示结果。
- `-p, --processor` — 选择处理器等级。
- `-j, --json` — 以原始 JSON 格式输出结果。

### 2. 自动检查（可选）
深度研究任务可能需要较长时间。建议使用自动化工具定期检查进度：
- **OpenClaw 用户：** 可参考 `OPENCLAW.md` 中关于基于 cron 的自动检查设置。
- **其他环境：** 可使用任何调度工具（如 cron、systemd 定时器或 CI 工程）定期运行 `parallel-research status <运行ID>` 和 `parallel-research result <运行ID>` 直到任务完成。
- **简单方法：** 直接使用 `parallel-research create "..." --wait` 命令，直到任务完成。

### 3. 手动检查（如有需要）
```bash
parallel-research status <run_id>
parallel-research result <run_id>
```

### 4. 保存研究成果
将所有研究结果保存到相应的文件夹中：
```
~/.openclaw/workspace/research/<topic-slug>/
├── prompt.md          # Original question + run metadata
├── research.md        # Full Parallel output
```

`prompt.md` 文件应包含以下内容：
```markdown
# <Topic Title>

> <Original research question>

**Run ID:** <run_id>
**Processor:** <processor>
**Started:** <date>
**Completed:** <date>
```

`research.md` 文件应包含 `parallel-research` 的完整输出结果以及任何后续的补充说明。

---

## PDF 导出
所有生成的 PDF 文件都应保存在研究文件夹中（切勿保存到 `tmp/` 目录）。无论使用 `export-pdf` 命令、浏览器内置的 PDF 导出功能还是其他方法，输出路径都必须是 `research/<主题名>/`。

可以使用 `export-pdf` 脚本将研究文档转换为 PDF 格式：
```bash
export-pdf ~/.openclaw/workspace/research/<topic-slug>/research.md
# Creates: ~/.openclaw/workspace/research/<topic-slug>/research.pdf
```

**注意：** 浏览器生成的 PDF 文件（例如将网页保存为 PDF）中，表格可能会显示为堆叠的行（这是 PyMuPDF 的限制，但对于研究文档来说是可以接受的）。

---

## 常用命令
- `new research: <主题名>` — 启动交互式研究。
- `deep research: <主题名>` — 启动异步深度研究。
- `show doc` / `show research` — 显示当前的研究文档。
- `summarize` — 进行综合整理。
- `graduate` — 将研究结果转入下一阶段。
- `archive` — 将文档标记为已完成并作为参考资料。
- `export pdf` — 将文档导出为 PDF。
- `check research` — 检查待处理的深度研究任务的状态。

---

## 文档编写原则
- **每个发现点应独立成条**：每个重要发现都用项目符号单独列出。
- **提供所有资料链接**：包括资料来源、相关文档和代码仓库的链接。
- **说明研究背景**：说明为什么要研究这个主题。
- **标注信息可靠性**：对不确定的内容使用适当的限定词。
- **标注重要发现的时间**：尤其是对于变化迅速的主题，这一点尤为重要。

---

## 安装说明
首次使用 `parallel-research` CLI 和 PDF 导出工具（如 pandoc、PyMuPDF）时，请参考 `SETUP.md` 文件进行安装。