---
name: solo-retro
description: **流程后回顾**：解析日志、评估流程质量、识别浪费现象，并提出改进技能或脚本的建议。该功能适用于流程完成后，或当用户请求“进行回顾”、“评估流程”、“分析问题所在”或“查看流程日志”时使用。
license: MIT
metadata:
  author: fortunto2
  version: "2.1.0"
  openclaw:
    emoji: "🔮"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, AskUserQuestion, mcp__solograph__session_search, mcp__solograph__codegraph_explain, mcp__solograph__codegraph_query
argument-hint: "[project-name]"
---
# /retro

本技能是独立完成的——请按照以下步骤操作，无需依赖其他技能（如 `/review`、`audit`、`build`）或生成子任务代理。所有分析工作均需直接执行。

**后管道回顾（Post-pipeline Retro）**：解析管道日志，统计有效迭代与无效迭代的次数，识别重复出现的故障模式，对管道运行进行评分，并提出具体的修改建议，以防止未来再次出现类似故障。

## 使用时机

在管道完成（或被取消）后执行。此过程用于检查质量：`/review` 主要检查代码质量，而 `/retro` 则检查管道执行过程的质量。

该流程也可独立应用于任何项目，无论是否有管道日志。

## 可用的 MCP 工具（如可用请使用）：

- `session_search(query)` — 查找过去的管道运行记录和已知问题
- `codegraph_explain(project)` — 了解项目架构背景
- `codegraph_query(query)` — 查询项目代码图的元数据

如果 MCP 工具不可用，可改用 Glob、Grep 和手动阅读文件进行操作。

## 第 1 阶段：定位相关文件

1. **从 `$ARGUMENTS` 或当前工作目录（CWD）中确定项目名称**：
   - 如果提供了参数，则使用该参数作为项目名称；
   - 否则，从 CWD 的路径名中提取项目名称（例如：`~/projects/my-app` → `my-app`）。

2. **查找管道状态文件**：
   - 文件路径：`.solo/pipelines/solo-pipeline-{project}.local.md`（针对特定项目）或 `~/.solo/pipelines/solo-pipeline-{project}.local.md`（全局默认路径）。
   - 如果文件存在，说明管道仍在运行或未清理完毕——请读取文件中的 `project_root` 配置信息；
   - 如果文件不存在，说明管道已经完成——此时以 CWD 作为项目根目录。

3. **验证相关文件是否存在（并行读取）**：
   - 管道日志：`{project_root}/.solo/pipelines/pipeline.log`
   - 迭代日志：`{project_root}/.solo/pipelines/iter-*.log`
   - 进度文件：`{project_root}/.solo/pipelines/progress.md`
   - 计划完成目录：`{project_root}/docs/plan-done/`
   - 活动计划文件：`{project_root}/docs/plan/`

4. **确定分析模式**：
   - 如果存在管道日志，则进行基于日志的全面分析（第 2-4 阶段）；
   - 如果没有管道日志，则切换到**备用分析模式**（详见下文）。

5. **统计迭代日志数量**（如果存在）：`ls {project_root}/.solo/pipelines/iter-*.log | wc -l`
   - 报告结果：`找到 {N} 个迭代日志`

## 备用分析（无管道日志）

即使没有管道日志，仍可通过以下方式进行分析：

1. **Git 历史记录**：`git log --oneline --since="1 week ago"` — 查看提交频率和模式
2. **测试结果**：如果 `CLAUDE.md` 或 `package.json` 中配置了测试脚本，请运行测试套件
3. **构建状态**：如果配置了构建命令，请执行构建操作
4. `CLAUDE.md` 的更改：`git log --oneline -- CLAUDE.md` — 查看文档的更新情况
5. **代码质量指标**：文件数量、待办事项/需要修复的代码比例、冗余代码情况
6. **项目结构**：文档、测试脚本和持续集成（CI）配置的完整性

跳过第 2-4 阶段，直接进行第 5 阶段（计划一致性检查）和第 6 阶段（Git 与代码质量检查）。根据可用数据的多少，适当调整第 7 阶段的评分。

## 第 2 阶段：解析管道日志（定量分析）

完整阅读 `pipeline.log` 文件，逐行提取日志中的结构化数据：

**日志格式**：`[HH:MM:SS] TAG | message`

**按标签提取信息**：

| 标签 | 需要提取的内容 |
|-----|----------------|
| `START` | 管道运行开始标记 | 统计重启次数（多个 `START` 标记表示多次重启） |
| `STAGE` | `iter N/M \| stage S/T: {stage_id}` | 每个阶段的迭代次数 |
| `SIGNAL` | `<solo:done/>` 或 `<solo:redo/>` | 表示某个阶段已完成 |
| `INVOKE` | 被调用的技能 | 提取技能名称，并检查是否有错误 |
| `ITER` | `commit: {sha} \| result: {stage complete\|continuing}` | 每次迭代的执行结果 |
| `CHECK` | `{stage} \| {path} -> FOUND\|NOT FOUND` | 文件检查结果 |
| `FINISH` | `Duration: {N}m` | 总运行时间 |
| `MAXITER` | 达到最大迭代次数（{N}） |
| `QUEUE` | 计划循环事件（激活/归档） |
| `CIRCUIT` | 电路断路器触发情况（如果存在） |
| `CWD` | 工作目录变更 |
| `CTRL` | 控制信号（暂停/停止/跳过） |

**计算相关指标**：
```
total_runs = count of START lines
total_iterations = count of ITER lines
productive_iters = count of ITER lines with "stage complete"
wasted_iters = total_iterations - productive_iters
waste_pct = wasted_iters / total_iterations * 100
maxiter_hits = count of MAXITER lines
plan_cycles = count of QUEUE lines with "Cycling"

per_stage = {
  stage_id: {
    attempts: count of STAGE lines for this stage,
    successes: count of ITER lines with "stage complete" for this stage,
    waste_ratio: (attempts - successes) / attempts * 100,
  }
}
```

## 第 3 阶段：解析 `progress.md` 文件（定性分析）

阅读 `progress.md` 文件，查找错误模式：

1. **未知技能错误**：查找 `Unknown skill:` 等错误信息，以确定出错的技能名称。
2. **无效迭代**：查看日志中的“最后 5 行”内容，判断是否存在仅显示错误或会议信息的迭代。
3. **重复错误**：连续迭代中出现的相同错误，可能是循环问题的迹象。
4. **重复的完成信号**：在同一迭代中多次出现 `<solo:done/>`，属于正常现象（无需特别处理）。
5. **重建循环**：统计重建（build->review->redo->build）的循环次数。

对于每个发现的错误模式，记录以下信息：
- 错误模式名称
- 首次出现的位置（迭代次数）
- 总出现次数
- 最长连续出现次数

## 第 4 阶段：分析迭代日志（基于样本）

无需读取所有迭代日志（可能数量较多，可进行智能采样）：

1. **每个错误模式的第一次失败迭代**：对于第 3 阶段中发现的每个错误模式，读取首次出现该错误的迭代日志。
   - 在读取日志时去除 ANSI 编码：`sed 's/\x1b\[[0-9;]*m//g' < iter-NNN-stage.log | head -100`

2. **每个阶段的首次成功迭代**：对于每个最终成功的阶段，读取首次成功的迭代日志。
   - 查找日志中的 `<solo:done/>` 标记。

3. **最终审查迭代**：读取最后一个 `iter-*-review.log` 文件（记录审查结果）。

4. **从每个样本日志中提取以下信息**：
   - 调用的工具（统计 `tool_use` 标签的出现次数）
   - 遇到的错误（使用 `grep` 命令查找 `Error`、`error`、`Unknown`、`failed` 等错误信息）
   - 完成信号（`<solo:done/>` 或 `<solo:redo/>` 是否出现）
   - 前 5 行和最后 10 行的内容（忽略空白行）

## 第 5 阶段：检查计划一致性

对于 `docs/plan-done/` 和 `docs/plan/` 目录下的每个计划跟踪文件，执行以下操作：

1. **阅读 `spec.md` 文件（如果存在）**：
   - 统计满足的验收标准数量（`- [ ]` 和 `- [x]` 标签）。
   - 计算满足标准的比例：`criteria_met = checked / total * 100`。

2. **阅读 `plan.md` 文件（如果存在）**：
   - 统计任务数量（`- [ ]` 和 `- [x]` 标签）。
   - 统计阶段数量（`##` 标签）。
   - 检查 SHA 注释（`<!-- sha:... -->`）。
   - 计算完成的任务比例：`tasks_done = checked / total * 100`。

3. **编译每个阶段的总结**：
   - 跟踪 ID、满足标准的比例、完成的任务比例、包含 SHA 标签的任务数量。

## 第 6 阶段：Git 与代码质量（简单检查）

仅进行快速检查，不进行全面的代码审查：

1. **提交记录的数量和格式**：
   ```bash
   git -C {project_root} log --oneline | wc -l
   git -C {project_root} log --oneline | head -30
   ```
   - 统计使用常规格式提交的代码数量（`feat:`, `fix:`, `chore:`, `test:`, `docs:`, `refactor:`, `build:`, `ci:`, `perf:`）。
   - 计算常规提交的比例：`conventional_pct = conventional / total * 100`。

2. **提交者分布**：
   ```bash
   git -C {project_root} shortlog -sn --no-merges | head -10
   ```

3. **测试状态**（如果 `CLAUDE.md` 或 `package.json` 中配置了测试命令）：
   - 运行测试套件，记录通过/失败的数量。
   - 如果未找到测试命令，跳过此步骤并标注“未配置测试”。

4. **构建状态**（如果配置了构建命令）：
   - 运行构建操作，记录成功/失败的结果。
   - 如果未找到构建命令，跳过此步骤并标注“未配置构建”。

## 第 7 阶段：评分与报告

从 `${CLAUDE_PLUGIN_ROOT}/skills/retro/references/eval-dimensions.md` 文件中加载评分标准。如果插件根目录不可用，使用内置的权重值：

**评分标准**：
- 效率（浪费百分比）：25%
- 稳定性（重启次数）：20%
- 一致性（满足的标准）：20%
- 代码质量（通过率）：15%
- 提交次数（常规提交）：5%
- 文档更新频率：5%
- 信号准确性：5%
- 执行速度（总运行时间）：5%

**注意**：在备用分析模式下（无管道日志），效率与稳定性的权重会重新分配给一致性、代码质量和提交次数。

**生成报告文件**：`{project_root}/docs/retro/{date}-retro.md`：
```markdown
# Pipeline Retro: {project} ({date})

## Overall Score: {N}/10

## Pipeline Efficiency

| Metric | Value | Rating |
|--------|-------|--------|
| Total iterations | {N} | |
| Productive iterations | {N} ({pct}%) | {emoji} |
| Wasted iterations | {N} ({pct}%) | {emoji} |
| Pipeline restarts | {N} | {emoji} |
| Max-iter hits | {N} | {emoji} |
| Total duration | {time} | {emoji} |

## Per-Stage Breakdown

| Stage | Attempts | Successes | Waste % | Notes |
|-------|----------|-----------|---------|-------|
| scaffold | | | | |
| setup | | | | |
| plan | | | | |
| build | | | | |
| deploy | | | | |
| review | | | | |

## Failure Patterns

### Pattern 1: {name}
- **Occurrences:** {N} iterations
- **Root cause:** {analysis}
- **Wasted:** {N} iterations
- **Fix:** {concrete suggestion with file reference}

### Pattern 2: ...

## Plan Fidelity

| Track | Criteria Met | Tasks Done | SHAs | Rating |
|-------|-------------|------------|------|--------|
| {track-id} | {N}% | {N}% | {yes/no} | {emoji} |

## Code Quality (Quick)

- **Tests:** {N} pass, {N} fail (or "not configured")
- **Build:** PASS / FAIL (or "not configured")
- **Commits:** {N} total, {pct}% conventional format

## Three-Axis Growth

| Axis | Score | Evidence |
|------|-------|----------|
| **Technical** (code, tools, architecture) | {0-10} | {what changed} |
| **Cognitive** (understanding, strategy, decisions) | {0-10} | {what improved} |
| **Process** (harness, skills, pipeline, docs) | {0-10} | {what evolved} |

If only one axis is served — note what's missing.

## Recommendations

1. **[CRITICAL]** {patch suggestion with file:line reference}
2. **[HIGH]** {improvement}
3. **[MEDIUM]** {optimization}
4. **[LOW]** {nice-to-have}

## Suggested Patches

### Patch 1: {file} — {description}

**What:** {one-line description}
**Why:** {root cause reference from Failure Patterns}

\```diff
- 旧内容
+ 新内容
\```
```

**评分指南（使用以下表情符号表示评分结果）**：
- 绿色 = 优秀
- 黄色 = 可接受
- 红色 = 需要改进

## 第 8 阶段：交互式修复建议

生成报告后：

1. **向用户展示报告摘要**：总体评分、最常见的 3 个故障模式以及 3 个改进建议。

2. **对于每个建议的修复方案**（如果有的话），使用 `AskUserQuestion` 功能：
   - 提问：“是否要将修复方案应用到 {file} 文件？{简短描述}”
   - 提供选项：“应用” / “跳过” / “先查看差异”

3. **如果选择“先查看差异”**：先显示差异内容，然后再询问用户是否应用修复方案。

4. **如果用户选择“应用”**：使用编辑工具直接应用修复内容。

5. **所有修复方案应用完成后**：
   - 建议使用 `fix(retro): {description}` 命令提交更改。
   - 注意：不要自动提交更改，只需提供命令即可。

## 第 9 阶段：更新 `CLAUDE.md`

修复完成后，更新项目的 `CLAUDE.md` 文件，使其保持简洁且对未来的自动化流程有用。

### 操作步骤：

1. **阅读 `CLAUDE.md` 文件并检查文件大小**：`wc -c CLAUDE.md`。
2. **将本次回顾中发现的内容添加到 `CLAUDE.md` 中**：
   - 需要记住的管道故障模式（避免未来再次出现）
   - 新的工作流程规则或流程改进措施
   - 更新的命令或工具变更
   - 在管道运行过程中产生的架构决策
3. **如果文件长度超过 40,000 个字符**：
   - 将已完成阶段的记录压缩成一行；
   - 删除冗长的解释，保留简洁、可操作的说明；
   - 删除重复的信息；
   - 删除多余的迁移说明和旧的调试内容；
   - 删除从代码中可以直接获取的信息，或已在其他文档/技能文件中涵盖的内容；
   - 删除已解决的问题的过时排查信息。
4. **确保文件长度不超过 40,000 个字符**；如果仍超过限制，请删除最不重要的内容。
5. **更新 `CLAUDE.md` 文件，并更新“最后更新”时间。

### 优先级（保留/删除内容）：

- **必须保留**：技术栈、目录结构、操作指南、常见命令、架构决策。
- **保留**：工作流程说明、活跃问题的排查方法、关键文件引用。
- **压缩**：阶段记录（每条记录占一行）、详细示例、工具/工具链列表。
- **首先删除**：历史记录、冗长的解释、重复的内容、已解决的问题。

### 规则：
- **切勿删除操作指南部分**：这些内容是重要的参考依据。
- 保持整体的章节结构和顺序。
- 每一条记录都必须有其存在的必要性：“未来的自动化流程是否需要这些信息？”
- 提交更新内容：`git add CLAUDE.md && git commit -m "docs: revise CLAUDE.md (post-retro)"`

## 第 10 阶段：工厂评估（可选）

**仅当 `${CLAUDE_PLUGIN_ROOT}` 可用时执行此步骤**（即单独运行此技能且具备工厂环境时）。如果作为独立技能运行且没有工厂环境，则跳过此步骤。

在评估完项目管道后，进一步评估**整个系统**——包括涉及的技能、脚本和管道逻辑。进行严格的自我评估。

### 评估内容：

1. **阅读本次管道运行中调用的所有技能**（从 `pipeline.log` 文件中的 `INVOKE` 标签判断）：
   - 对于每个技能，检查其是否具备处理该项目需求所需的正确指令。
   - 是否缺少必要的上下文信息？

2. **阅读管道脚本中的信号处理和阶段逻辑**：
   - 文件路径：`${CLAUDE_PLUGIN_ROOT}/scripts/solo-dev.sh`
   - 检查是否存在结构上的问题（例如阶段顺序错误、重复执行操作或重建失败）。

3. **与第 3 阶段发现的故障模式进行对比**：
   - 对于每个故障，判断故障的根本原因是在技能、脚本还是项目中？
   - 导致问题的技能可能是系统缺陷。

### 评估整个系统（而非单个项目）

**评分标准**：
```
Factory Score: {N}/10

Skill quality:
- {skill}: {score}/10 — {why}
- {skill}: {score}/10 — {why}

Pipeline reliability: {N}/10 — {why}

Missing capabilities:
- {what the factory couldn't do that it should have}

Top factory defects:
1. {defect} → {which file to fix} → {concrete fix}
2. {defect} → {which file to fix} → {concrete fix}
```

### 总结与改进

在完成评分后，进一步思考整个系统的优化方向——包括自动化流程（`CLAUDE.md`、文档、代码检查工具等）。考虑以下问题：

1. **上下文支持**：自动化流程在仓库中是否具备所需的所有资源？还是因为知识缺失或分散导致问题？
   - 如果缺少文档，应将其添加到 `docs/` 或 `CLAUDE.md` 中；
   - 如果文档过时，应标记以便后续更新。
   - 如果知识仅存在于团队成员的脑海中，应将其记录下来。

2. **架构限制**：自动化流程是否违反了模块边界、产生了不一致的结果，或忽略了某些规范？
   - 如果存在重复的问题，可能需要添加代码检查工具或规则来避免类似问题。
   - 对于表现良好的做法，应将其记录下来供未来参考；对于存在的问题，应制定相应的预防措施。
   - 对于存在的问题，应记录下来并作为反例或规则进行改进。

3. **思考未来改进的方向**：
   - 哪些技能需要更好的指导？哪些新技能是必要的？
   - 对于造成问题的技能，应编写相应的修复方案；
   - 对于缺失的功能，应考虑添加新的技能。

**记录改进内容**：
将评估结果添加到 `{project_root}/docs/evolution.md` 文件中（如果文件不存在，则创建新文件）。如果 `~/.solo/evolution.md` 已存在，也请将结果添加到其中。

**规则**：
- 诚实地评估问题；
- 对于每个问题，都必须提出具体的解决方案；
- 记录有效的改进措施，避免重复出现类似问题；
- 保持记录的简洁性，因为这些记录会随着时间不断积累。

## 信号输出

**输出信号**：`<solo:done/>`

**重要提示**：`/retro` 始终会输出 `<solo:done/>`——表示分析已完成，无需重新执行管道。

**特殊情况处理**：
- **没有管道日志且没有 Git 历史记录**：输出明确提示：“未找到管道日志或 Git 历史记录，无法进行分析。”
- **只有管道日志而没有 Git 历史记录**：切换到备用分析模式。
- **管道日志为空**：报告“管道日志为空，可能管道在迭代开始前就被取消了”。
- **没有迭代日志**：跳过第 4 阶段的样本分析，并在报告中注明。
- **没有计划完成文件**：跳过第 5 阶段，并在报告中注明。
- **没有测试/构建命令**：跳过第 6 阶段的检查，并在报告中注明。
- **管道仍在运行**：提醒用户：“状态文件存在，管道可能仍在运行。分析基于部分数据。”

## 参考文件**：
- `${CLAUDE_PLUGIN_ROOT}/skills/retro/references/eval-dimensions.md` — 评分标准（8 个维度及相应的权重）
- `${CLAUDE_PLUGIN_ROOT}/skills/retro/references/failure-catalog.md` — 已知的故障模式及对应的修复方案