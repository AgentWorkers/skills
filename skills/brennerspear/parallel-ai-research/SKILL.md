# 研究技能

## 描述
针对某个主题进行开放式研究，并生成一个实时更新的 Markdown 文档。对话是短暂的，但文档才是最重要的。

## 触发条件
当用户希望执行以下操作时，该功能会被激活：
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
适用于需要全面调查的复杂主题。该模式通过 `parallel-research` CLI 使用 Parallel AI API 进行处理，耗时数分钟到数小时，最终会生成详细的 Markdown 报告。

**何时使用深度研究：**
- 市场分析、竞争格局研究
- 需要大量收集技术资料的技术性深入研究
- 需要多方面探讨的多维度问题
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

4. 与用户确认 - 显示已创建的文件夹，并询问首先应该探索哪些内容。

### 2. 研究循环
每次交流时，执行以下步骤：
1. **进行研究** - 进行网络搜索、获取文档、查阅代码
2. **更新文档** - 添加研究发现、处理已解答的问题、添加参考资料
3. **展示进度** - 说明添加了哪些内容（避免重复）
4. **提示下一步的方向** - 以一个问题或建议结束对话

**关键操作：**
- 优先更新现有内容，而非创建新内容
- 使用项目符号列出研究发现，用段落形式总结
- 对不确定的内容注明（例如“看起来像是”、“根据 X 的说法”、“未经验证”）
- 尽可能提供资料链接

### 3. 合成与检查
每进行 5-10 次交流后，建议用户：
- 编写一个“当前理解”总结
- 删除冗余的信息
- 如果文档过于冗长，对其进行重组
- 检查是否存在遗漏的内容

### 4. 完成研究
当研究完成后，在 `research.md` 文件中更新状态：
- **“状态：已完成”** — 研究结束，文档作为参考资料保留
- **“状态：进行中”** — 文档仍在更新中

**如果研究是为了某个项目的开发：**
- 将文档移至 `~/specs/<project-name>.md` 作为项目规范
- 或者根据研究结果直接创建项目
- 将状态更新为 **“状态：已完成 → ~/specs/...”**

大多数研究只是初步探索，并不一定需要发展成项目规范。只有当用户确实打算基于这些研究结果进行开发时，才需要将其转化为项目规范。

---

## 深度研究工作流程

### 1. 开始深度研究
```bash
parallel-research create "Your research question" --processor ultra --wait
```

**处理器选项：**
- `lite`、`base`、`core`、`pro`、`ultra`（默认值）、`ultra2x`、`ultra4x`、`ultra8x`
- 通过添加后缀 `-fast` 来调整速度（例如 `ultra-fast`、`pro-fast` 等）

**其他选项：**
- `-w, --wait` — 等待研究完成后再显示结果
- `-p, --processor` — 选择处理器级别
- `-j, --json` — 以原始 JSON 格式输出结果

### 2. 自动检查安排
创建研究任务后，设置一个 cron 作业来检查结果并将其反馈给用户。使用 `deleteAfterRun: true` 选项以确保作业完成后自动删除。

**⚠️ 重要提示：** 必须正确计算 `atMs`（任务完成时间）！
```bash
# Get current timestamp in ms and add 15 minutes (900000 ms)
date +%s%3N  # Current time in epoch ms
# Example: 1770087600000 + 900000 = 1770088500000
```

**务必确认安排的检查时间在未来，并且年份正确：**
```bash
date -d @$((1770088500000/1000))  # Should show a time ~15 min from now, correct year
```

**关键步骤：**
- 使用 `cron` 工具，并设置 `action: "add"` 来执行任务
- **务必检查 `atMs` 是否正确** — 使用 `date -d @$((atMs/1000))` 来确认年份和时间
- `atMs` 应该设置在距离当前时间约 10-15 分钟（对于高性能处理器）或约 5 分钟（对于普通处理器）
- `deleteAfterRun: true` 选项会在任务完成后自动删除该作业
- 将结果发送回请求研究的相同频道或主题
- 如果任务仍在运行，cron 作业会自动再次执行检查
- `PARALLEL_API_KEY` 作为环境变量提供——无需在代码中直接写入

### 3. 手动检查（如有需要）
```bash
parallel-research status <run_id>
parallel-research result <run_id>
```

### 4. 保存研究结果
创建研究文件夹并保存所有研究成果：
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

`research.md` 文件应包含 Parallel API 的完整输出结果以及任何后续的补充说明。

---

## PDF 导出
使用 `export-pdf` 脚本将研究文档转换为 PDF 格式：
```bash
export-pdf ~/.openclaw/workspace/research/<topic-slug>/research.md
# Creates: ~/.openclaw/workspace/research/<topic-slug>/research.pdf
```

或者指定自定义的输出路径：
```bash
export-pdf research.md ~/Desktop/output.pdf
```

**注意：** 由于 PyMuPDF 的限制，表格在 PDF 中会显示为堆叠的行，但这对于研究文档来说是可以接受的。

---

## 命令
- **"new research: <topic>"** - 启动交互式研究文档
- **"deep research: <topic>"** - 启动异步深度研究
- **"show doc"** / **"show research"** - 显示当前的研究文档
- **"summarize"** - 执行合成检查
- **"graduate"** - 将研究结果推进到下一阶段
- **"archive"** - 将文档标记为已完成参考资料
- **"export pdf"** - 将文档导出为 PDF
- **"check research"** - 检查待处理的深度研究任务的状态

---

## 文档编写原则
- **每个发现点独立成条** - 每个重要发现都用项目符号列出
- **提供所有参考链接** - 包括资料来源、文档和代码仓库
- **说明研究背景** - 说明为何要研究这个主题
- **标注信息可靠性** - 对不确定的内容使用适当的限定词
- **标注重要发现的时间** - 尤其对于变化迅速的主题

---

## 设置
有关首次安装 `parallel-research` CLI 和 PDF 导出工具（pandoc、PyMuPDF）的详细信息，请参阅 `SETUP.md`。