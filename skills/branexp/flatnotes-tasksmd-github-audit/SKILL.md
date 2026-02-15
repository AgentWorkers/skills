---
name: flatnotes-tasksmd-github-audit
description: "对 `Tasks.md` 和 `Flatnotes` 文件进行全面审计，检查其中的数据是否发生变动以及内容是否准确；使用 GitHub 的 `gh CLI` 命令行工具来识别过时的笔记/卡片以及缺失的链接。审计完成后，生成一份报告，并提供一个可选的修复方案。"
---

# Flatnotes + Tasks.md + GitHub 审计

当 Brandon 要求对 Flatnotes/Tasks.md 系统进行准确性审计，并确保其内容是最新的时，请使用此技能，同时以 GitHub 作为数据的权威来源。

## 快速入门
运行捆绑的审计工具（仅生成报告）：

```bash
node skills/flatnotes-tasksmd-github-audit/scripts/audit.mjs --since-days 30 --write
```

输出结果：
- Markdown 报告：`tmp/flatnotes-tasksmd-audit.md`
- JSON 报告：`tmp/flatnotes-tasksmd-audit.json`

> 如果未进行 GitHub 认证，审计仍会执行，但 GitHub 的检查会被标记为 `SKIPPED_GITHUB`。

---

## 数据来源（默认值）
- Tasks.md 的存储路径：`/home/ds/.config/appdata/tasksmd/tasks`
- Flatnotes 的存储路径：`/home/ds/.config/appdata/flatnotes/data`
- Flatnotes 的“系统笔记”镜像路径：`notes/resources/flatnotes-system/`

可以通过环境变量进行覆盖：
- `TASKS_ROOT`
- `FLATNOTES_ROOT`

---

## 审计目标（“准确性”的含义）

### A) Tasks.md 的规范性
- 必须存在以下全局任务分类：`00 收件箱`、`05 待办事项`、`10 进行中`、`30 被阻塞`、`40 等待中`、`90 已完成`。
- **任务分类规则**：默认情况下，优先级为 `prio-p2` 的任务应归类到 `05 待办事项` 中（`10 进行中` 中不应包含 `prio-p2` 的任务）。
- 进行中的任务（Doing）的数量应不超过 3 个。
- 任务卡片应保持一致的格式（包括结果/步骤）和标签（项目/优先级/类型）。
- 被阻塞的任务卡片应包含“解除阻塞”（Unblock:）的标记。
- 项目卡片应包含指向 Flatnotes 的链接（例如：`Flatnotes: ...`）。

### B) Flatnotes 的完整性
对于 `SYS Workspace - Project Registry` 中的每个活跃项目：
- 必须存在以下项目笔记：
  - `PJT <slug> - 00 概述`
  - `PJT <slug> - 10 研究`
  - `PJT <slug> - 20 计划`
  - `PJT <slug> - 90 日志`
- 项目中心（Hub）的笔记应包含：
  - 当前状态（以项目编号为编号的列表项）
  - 包含仓库链接和任务筛选功能的链接部分
  - 包含指向相关决策记录（ADR）的链接部分

### C) 确保数据与 GitHub 一致（GitHub 为权威数据来源）
对于注册表中的每个项目仓库：
- 打开的 Pull Request（PR）应对应一个 Tasks 卡片（状态为进行中/待办/被阻塞/等待中），或者应说明为什么没有对应的卡片。
- 最近合并的 PR 应在相应的地方得到体现：
  - 最好是在项目日志中添加简短说明（例如：`PJT <slug> - 90 日志`）并更新项目中心的状态，或者
  - 创建一个状态为“已完成”的卡片并附上 PR 的链接。
  - （审计会将这种情况视为数据已对齐；如果合并的 PR 只出现在“已完成”卡片中但未在日志中显示，系统会发出警告。）
- 完成的卡片在理想情况下应包含 PR 的链接，以表明工作是通过 PR 完成的。

---

## 推荐的工作流程
1) **解析注册表数据**
   - 从 Flatnotes 中读取 `SYS Workspace - Project Registry` 的信息。
   - 提取项目编号（slug）、状态、任务标签（Tasks tag）以及 GitHub 仓库的 URL。

2) **扫描 Tasks.md 文件**
   - 按任务分类和 `proj-*` 标签对卡片进行索引。
   - 标记违反任务分类规则的情况（例如：将优先级为 `prio-p2` 的任务归类到“待办事项”中）。
   - 标记缺少 Flatnotes 链接的卡片。

3) **扫描 Flatnotes 文件**
   - 检查所需的项目笔记是否存在。
   - 检查项目中心笔记中的决策记录链接是否正确。

4) **与 GitHub 数据进行交叉核对**
   - 使用 `gh` 命令：
     - `gh pr list --state open --json ...`
     - `gh pr list --state merged --search "merged:>=<date>" --json ...`（或等效命令）
   - 尝试通过以下方式匹配 PR 和 Tasks 卡片：
     - 卡片内容中的 PR URL
     - PR 编号
     - PR 标题中的相关子字符串

5) **生成报告**
   - 输出审计结果、各项目的差异列表以及修复计划。

---

## 修复措施的应用（限制）
默认情况下，系统仅生成审计报告。

如果 Brandon 明确要求进行修复：
- 允许进行以下安全的自动修复操作：
  - 使用现有模板创建缺失的 Flatnotes 笔记（例如：`10 研究` 等）。
  - 在项目中心的决策记录部分添加缺失的 ADR 链接。
  - 将优先级为 `prio-p2` 的任务从“进行中”分类移动到“待办事项”分类。
  - 为 Tasks 卡片添加缺失的 Flatnotes 链接。
- 任何涉及文件重命名或删除内容的操作都需要事先获得许可。

---

## 搭载的脚本
- `scripts/audit.mjs` — 用于生成报告（Markdown 和 JSON 格式）。如有需要，可以直接修改该脚本而不是重新编写代码。