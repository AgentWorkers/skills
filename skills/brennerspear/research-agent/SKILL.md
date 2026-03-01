---
name: research
slug: research-agent
version: 1.0.0
description: 针对某个主题进行开放式研究，并生成一个实时更新的 Markdown 文档。该工具支持交互式和深入的研究模式。
---
# 研究技能

## 描述
对某个主题进行开放式研究，并构建一个实时更新的 Markdown 文档。对话是短暂的；真正重要的是文档本身。

## 触发条件
当用户想要以下操作时，该功能会被激活：
- 研究某个主题、想法或问题
- 在开始实际开发之前先探索相关内容
- 调查各种选项、模式或方法
- 创建一个“研究文档”或“调查报告”
- 对复杂主题进行深入的异步研究

## 研究目录
每个研究主题都会有自己的文件夹：
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
适用于用户通过对话共同探索的主题。用户可以实时搜索、整理并更新文档。

### 2. 深度研究（异步模式）
适用于需要全面调查的复杂主题。该模式通过 `parallel-research` CLI 使用 Parallel AI API 进行处理，耗时数分钟到数小时，最终生成详细的 Markdown 报告。

**何时使用深度研究：**
- 市场分析、竞争格局研究
- 需要大量收集资料的技术性深度研究
- 需要多方面探索的多方面问题
- 当用户要求进行“深度研究”或希望获得全面覆盖时

---

## 交互式研究工作流程

### 1. 初始化研究
1. 在 `~/.openclaw/workspace/research/<topic-slug>/` 目录下创建研究文件夹。
2. 创建 `prompt.md` 文件，记录原始问题：
   ```markdown
   # <Topic Title>

   > <The core question or curiosity>

   **Started:** <date>
   ```

3. 创建 `research.md` 文件，设置文档的基本结构：
   ```markdown
   # <Topic Title>

   **Status:** Active Research
   **Started:** <date>
   **Last Updated:** <date>

   ---

   ## Open Questions
   - <initial questions to explore>

   ## Findings
   <!-- Populated as we research -->

   ## Options / Approaches
   <!-- If comparing solutions -->

   ## Resources
   <!-- Links, references, sources -->

   ## Next Steps
   <!-- What to explore next, or "graduate to project" -->
   ```

4. 与用户确认——展示已创建的文件夹，并询问首先应该探索哪些内容。

### 2. 研究循环
每次交流时，执行以下步骤：
1. **进行研究**：进行网络搜索、查阅文档、探索相关代码。
2. **更新文档**：添加研究发现的内容、回答已有的问题、引用来源。
3. **展示进度**：说明添加了哪些内容（避免重复相同的信息）。
4. **提示下一步的方向**：以一个问题或建议结束对话。

**关键操作：**
- 优先更新现有内容，而非创建新内容。
- 使用项目符号列出研究发现，用段落形式总结要点。
- 对不确定的内容注明“似乎如此”、“根据 X 来说”或“未经验证”。
- 尽可能提供来源链接。

### 3. 综合检查点
每进行 5-10 次交流后，建议用户：
- 编写“当前理解”总结。
- 去除冗余的信息。
- 如果文档过于冗长，进行重新组织。
- 检查是否存在遗漏的部分。

### 4. 完成研究
研究完成后，在 `research.md` 文件中更新状态：
- **“状态：已完成”** — 研究完成，作为参考资料保留。
- **“状态：进行中”** — 文档仍在更新中。

**如果研究是为了某个项目的开发：**
- 将文档移至 `~/specs/<project-name>.md` 作为项目规范。
- 或者根据研究发现直接创建项目。
- 将状态更新为 “状态：已完成 → ~/specs/...”。

大多数研究只是初步探索，并不一定需要发展成为正式的项目规范。只有当用户真正打算基于这些研究结果进行开发时，才需要将其升级为规范。

---

## 深度研究工作流程

### 1. 开始深度研究
```bash
parallel-research create "Your research question" --processor ultra --wait
```

**处理器选项：**
- `lite`、`base`、`core`、`pro`、`ultra`（默认值）、`ultra2x`、`ultra4x`、`ultra8x`
- 通过添加 `-fast` 后缀来提高处理速度：`ultra-fast`、`pro-fast` 等。

**其他选项：**
- `-w, --wait` — 等待研究完成并显示结果。
- `-p, --processor` — 选择处理器等级。
- `-j, --json` — 输出原始 JSON 数据。

### 2. 自动检查（可选）
深度研究任务可能需要数分钟到数小时才能完成。建议使用自动检查机制来节省时间。
**选项：**
- **OpenClaw 用户：** 参见 `OPENCLAW.md` 以了解基于 cron 的自动检查调度方法。
- **其他环境：** 使用任何调度工具（如 cron、systemd 定时器、CI 作业）定期运行 `parallel-research status <run_id>` 和 `parallel-research result <run_id>`，直到任务完成。
- **简单方法：** 直接使用 `parallel-research create "..." --wait` 命令，直到任务完成。

### 3. 手动检查（如有需要）
```bash
parallel-research status <run_id>
parallel-research result <run_id>
```

### 4. 保存研究成果
创建研究文件夹并保存所有结果：
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

`research.md` 文件包含 `parallel-research` 的完整输出结果以及任何后续的补充说明。

---

## PDF 导出
所有生成的 PDF 文件都应保存在研究文件夹中（切勿保存到 `tmp/` 目录）。无论是使用 `export-pdf` 命令、浏览器内置的 PDF 导出功能，还是其他方法，输出路径都必须是 `research/<topic-slug>/`。

可以使用 `export-pdf` 脚本将研究文档转换为 PDF 格式：
```bash
export-pdf ~/.openclaw/workspace/research/<topic-slug>/research.md
# Creates: ~/.openclaw/workspace/research/<topic-slug>/research.pdf
```

**注意：** 浏览器生成的 PDF 文件（例如将网页保存为 PDF）中，表格可能会显示为堆叠的行（这是 PyMuPDF 的限制）。对于研究文档来说，这种格式是可以接受的。

---

## 命令
- **"new research: <topic>"** — 开始交互式研究。
- **"deep research: <topic>"** — 开始异步深度研究。
- **"show doc"** / **"show research"** — 显示当前的研究文档。
- **"summarize"** — 进行综合总结。
- **"graduate"** — 将研究结果移至下一阶段。
- **"archive"** — 将文档标记为已完成并作为参考资料。
- **"export pdf"** — 将文档导出为 PDF。
- **"check research"** — 检查待处理的深度研究任务的状态。

---

## 文档编写原则
- **每个发现点独立成条**：每个重要的发现都用一个项目符号表示。
- **提供所有来源链接**：包括原始资料、相关文档和代码仓库的链接。
- **说明研究背景**：解释为什么选择研究这个主题。
- **标注信息的可靠性**：对不确定的内容使用适当的限定词。
- **标注重要发现的时间**：特别是对于变化迅速的主题，这一点尤为重要。

---

## 设置指南
首次安装 `parallel-research` CLI 和 PDF 导出工具（如 pandoc、PyMuPDF）的详细步骤，请参考 `SETUP.md` 文件。