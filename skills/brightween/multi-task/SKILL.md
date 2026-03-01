---
name: multi-task
description: "通过将任务分解为独立的单元，并同时将这些单元分配给多个子代理来协调批量任务的并行执行。当用户有多个相似的独立任务时（例如处理一批文件（PDF、DOCX、图片、CSV）、开发多个页面或组件、生成多份报告，或任何涉及“每个”、“全部”、“批量”或类似项目列表的场景），都可以使用此技能。当用户提供任务列表、指定需要处理的文件文件夹，或描述需要对多个输入进行重复性处理时，也应触发该技能。即使用户没有明确提到“并行”或“批量”，只要任务可以自然地分解为3个或更多个相同类型的独立单元，也应使用此技能以最大化处理效率。"
---
# 多任务处理：并行批处理编排

## 概述

当用户提交的任务可以分解为多个独立的工作单元时，顺序执行会浪费时间。本技能将指导您识别适合进行批处理的场景，为每个单元构建独立的指令，并通过 Task 工具将它们作为并行子任务来执行——这样可以在几分钟内完成原本需要更长时间才能完成的工作。

核心原理是：一条消息中可以包含多个 Task 工具的调用，而这些调用会同时执行。您的任务是确保每个子任务的指令都是完全独立的（子任务无法查看整个处理流程），并协调各个任务的结果。

## 何时使用此技能

**适用场景：**
- 用户要求“处理 X 文件夹中的所有文件”
- 用户提供了一组任务列表，例如：“对每个文件执行 A、B、C、D 操作”
- 用户提到了“批量处理”、“批量操作”、“所有文件”等关键词
- 一个文件夹中包含多个需要相同操作的文件
- 用户希望生成多个页面、组件或报告

**其他推荐使用场景：**
- 当用户描述的任务需要重复执行时（这些任务通常可以通过循环来完成）
- 当任务包含 3 个或更多类型相似的独立单元时
- 当每个单元的处理时间较长时（如读取/转换文档、生成代码等）

**不适用场景：**
- 任务之间存在严格的顺序依赖关系（例如任务 N 的输出是任务 N+1 的输入）
- 工作单元少于 3 个（此时并行处理的开销可能不值得）
- 任务是一个无法分解的复杂操作
- 用户明确要求顺序执行任务

## 六步工作流程

### 第一步：分析——理解工作内容

在开始执行任何操作之前，先列出需要完成的任务：
1. **列出所有工作单元**：需要处理的文件、需要生成的页面或需要转换的元素
2. **确定操作内容**：每个单元需要执行的具体操作（提取、转换、汇总、生成等）
3. **检查是否需要共享上下文**：所有单元是否需要相同的模板、配置或参考数据？如果是，请一次性读取这些信息，并将其包含在每个子任务的指令中
4. **检测依赖关系**：是否有单元依赖于其他单元？如果有，请参考 `references/advanced-patterns.md` 了解依赖关系的处理方法。如果所有单元都是独立的（这是最常见的情况），则可以直接进行下一步。
5. **统计单元数量**：根据单元数量选择合适的处理策略：
   - 3-10 个单元：一次性全部并行处理
   - 11-50 个单元：分批处理（每批 8-10 个单元）
   - 50 个以上单元：先运行 2-3 个试点任务进行验证，然后再分批处理剩余的任务

将分析结果展示给用户：
```
Found N work units: [brief list]
Operation: [what will happen to each]
Shared context: [any common dependencies]
Dependencies: [none / description]
Strategy: [single wave / M waves of ~K / pilot + waves]
```

在开始执行之前，请等待用户的确认，特别是对于大规模的批处理任务。

### 第二步：规划——将任务分解为独立单元

为每个工作单元定义以下信息：
- **任务 ID**：用于标识任务的唯一序列号（例如 task-001、task-002 等）
- **输入**：输入文件或数据的绝对路径
- **操作内容**：子任务需要执行的操作
- **输出路径**：结果的绝对路径（确保不同任务的输出路径不会冲突）
- **推荐的技能**：如果该任务可以使用已安装的技能，请指定相应的技能

**输出路径管理：** 创建一个专门的输出目录来整理结果：
```
<project-dir>/multi-task-output/
├── task-001/
├── task-002/
└── ...
```

在执行任务之前，使用 `mkdir -p` 命令创建输出目录结构。

### 第三步：生成子任务指令

每个子任务在开始执行时都没有相关的上下文信息。因此，生成的指令必须**完全独立**。使用以下模板来生成指令：
```
## Task [task-ID]: [Brief description]

### Skill Recommendation
[If a matching skill is available]:
You have access to the `/[skill-name]` skill which is ideal for this task.
Invoke it using the Skill tool with skill="[skill-name]" to get specialized
instructions before proceeding.

### Context
[Any shared context the subagent needs — project background, conventions,
templates, reference data. Include the actual content, not references to
"the conversation above".]

### Input
- File: [absolute path]
- [Any other inputs, with absolute paths]

### Instructions
[Clear, step-by-step instructions for what to do]
1. [Step 1]
2. [Step 2]
...

### Output
- Save results to: [absolute path to task-specific output directory]
- Expected deliverables: [list of output files]
- [Any format requirements]

### Important Notes
- Use absolute paths for all file operations
- Do not modify the input file(s)
- If you encounter an error, save error details to [output-dir]/error.log
```

**指令质量检查清单：**
- 所有路径都是绝对路径
- 不包含对讨论内容的引用
- 共享的上下文信息直接包含在指令中，而不是通过引用传递
- 每个任务的输出路径都是唯一的
- 指令足够详细，以便没有先前上下文的子任务也能理解
- 如果适用，包含推荐的技能名称

### 第四步：并行执行任务

**关键步骤：** 在一条消息中包含多个 Task 工具的调用。这样才能实现并行处理。如果将多个调用分别发送，它们将按顺序执行。

- **对于 3-10 个任务**：将所有任务放在一条消息中发送：
```
[Single message containing:]
Task(subagent_type="general-purpose", prompt="## Task task-001: ...", description="Process file-001")
Task(subagent_type="general-purpose", prompt="## Task task-002: ...", description="Process file-002")
Task(subagent_type="general-purpose", prompt="## Task task-003: ...", description="Process file-003")
...
```

- **对于 11-50 个任务**：分批处理（每批 8-10 个任务），每批完成后再开始下一批：
```
Wave 1: task-001 through task-010 (single message, all parallel)
[Wait for completion, report progress]
Wave 2: task-011 through task-020 (single message, all parallel)
[Wait for completion, report progress]
...
```

- **对于 50 个以上的任务**：先运行 2-3 个试点任务：
  1. 选择 2-3 个具有代表性的任务（如果可能的话，包括边缘情况）
  2. 将它们作为试点任务发送
  3. 验证结果是否正确
  4. 如果发现问题，修改指令模板并重新运行试点任务
  5. 验证通过后，再分批处理剩余的任务（每批 8-10 个）

**子任务类型选择：**
- 默认类型：`general-purpose`（具备使用所有工具的权限，包括执行特定技能）
- 适用于纯 Shell 或 Git 操作的任务：`Bash`
- 仅用于代码探索的任务：`Explore`

**适当情况下在后台运行任务：** 对于大规模批处理任务，可以使用 `run_in_background: true` 选项，以便您可以实时监控进度并向用户报告。

### 第五步：监控进度

在任务执行过程中，跟踪进度：
1. **记录完成情况**：例如：“第 1 批任务中有 8 个任务已完成”
2. **处理失败情况**：
  - 分析失败原因
  - 如有必要，修改指令
  - 自动重试最多 2 次
  - 如果重试后仍然失败，将该任务标记为失败，并继续处理其他任务
3. **向用户报告进度**：
```
   Wave 1 complete: 9/10 succeeded, 1 failed (task-007: [reason])
   Starting wave 2...
   ```

**注意事项：** 一个任务的失败不应影响其他任务的执行。

### 第六步：合并结果**

所有任务完成后：
1. **按任务 ID 对结果进行排序**：无论完成时间如何，都按顺序展示结果
2. **汇总处理结果**：
```
   Batch complete: N/M tasks succeeded

   Successful:
   - task-001: [output path] — [brief description]
   - task-002: [output path] — [brief description]
   ...

   Failed (if any):
   - task-007: [error reason] — [suggested fix]
   ```

**处理失败的任务：** 提供重试选项，或者让用户重新输入数据并重新运行任务
3. **合并输出文件（如需要）**：某些批处理操作需要合并结果（例如将提取的文本合并到一个文档中）。请在所有任务完成后执行此步骤。

## 技能匹配

在规划任务时，将每个工作单元与已安装的技能进行匹配。这可以显著提高子任务的执行效率，因为技能提供了专门设计且经过测试的指令。

**匹配规则：**
| 任务类型 | 推荐使用的技能 |
|---|---|
| PDF 文件（读取、创建、合并、提取） | `/pdf` |
| Word 文档（.docx 格式） | `/docx` |
| PowerPoint 文件（.pptx 格式） | `/pptx` |
| 电子表格（.xlsx、.csv、.tsv 格式） | `/xlsx` |
| 网页、组件、HTML/CSS 设计 | `/frontend-design` |
| 视觉设计、海报、艺术作品 | `/canvas-design` |
| 使用主题进行样式设计 | `/theme-factory` |

**如何在指令中包含技能推荐：**

在每个子任务的指令中添加相应的技能调用指令：
```
### Skill Recommendation
You have access to the `/pdf` skill. Before starting work, invoke it using
the Skill tool: Skill(skill="pdf"). This will load specialized instructions
for PDF processing that will help you complete this task more effectively.
```

如果没有合适的技能可用，可以省略技能推荐部分——此时子任务将使用其默认的功能。

## 示例

### 示例 1：批量提取 PDF 文件中的文本

**用户需求：**“从 /Users/me/reports/ 目录下的所有 PDF 文件中提取文本，并保存为 markdown 文件”

**分析：**
```
Found 12 PDF files in /Users/me/reports/
Operation: Extract text from each PDF, save as .md
Shared context: None
Dependencies: None
Strategy: 2 waves of 6
```

**每个子任务的指令：**
```
## Task task-001: Extract text from Q1-report.pdf

### Skill Recommendation
You have access to the `/pdf` skill. Invoke it using the Skill tool with
skill="pdf" to get specialized PDF processing instructions.

### Input
- File: /Users/me/reports/Q1-report.pdf

### Instructions
1. Read the PDF file and extract all text content
2. Preserve heading structure where possible
3. Format the output as clean Markdown
4. Include page breaks as horizontal rules (---)

### Output
- Save to: /Users/me/reports/multi-task-output/task-001/Q1-report.md
- Create the output directory if it doesn't exist
```

### 示例 2：生成多页面前端页面

**用户需求：**“为我们的营销网站生成 5 个页面：首页、关于我们、价格、博客、联系我们”

**分析：**
```
Found 5 work units: Home, About, Pricing, Blog, Contact pages
Operation: Generate frontend code for each page
Shared context: Brand guidelines, shared layout components, color scheme
Dependencies: None (each page is independent)
Strategy: Single wave, all 5 parallel
```

**注意事项：**
- 先读取现有的共享组件和样式
- 在每个指令中包含完整的共享上下文信息（如品牌颜色、字体、布局模板）
- 每个子任务都会被推荐使用 `/frontend-design` 技能
- 输出文件应保存在相应的目录中（例如 `pages/home/`、`pages/about/` 等）

### 示例 3：批量转换 CSV 文件

**用户需求：**“将 /data/raw/ 目录下的所有 CSV 文件转换为 JSON 格式，并确保数据类型正确”

**分析：**
```
Found 25 CSV files in /data/raw/
Operation: Parse CSV, infer types, convert to JSON
Shared context: Type inference rules (dates, numbers, booleans)
Dependencies: None
Strategy: 3 waves of ~8-9
```

**注意事项：**
- 每个子任务都会被推荐使用 `/xlsx` 技能
- 在指令中包含类型推断规则
- 在指令模板中统一输出格式

## 常见问题及解决方法

| 问题 | 原因 | 解决方法 |
|---|---|---|
| 任务没有并行执行 | 多个任务调用被分别发送 | 将所有任务调用放在一条消息中 |
| 子任务提示“没有上下文” | 指令中应包含处理过程中的所有信息 | 确保指令完全独立 |
| 文件未找到 | 使用了相对路径 | 应使用绝对路径 |
| 输出文件被覆盖 | 多个任务使用相同的输出路径 | 在输出目录路径中使用任务 ID |
| 子任务未使用推荐的技能 | 指令中的技能调用不清晰 | 明确添加 `Skill(skill="name")` 的调用指令 |
| 任务数量过多导致系统负担过重 | 一次性处理过多任务 | 分批处理（每批 8-10 个任务） |
| 结果顺序错误 | 依赖关系处理不当 | 按任务 ID 排序结果，而不是按完成时间 |
| 一个任务的失败影响其他任务 | 任务之间存在依赖关系 | 确保任务之间有隔离措施（使用不同的输出目录） |

## 高级技巧

有关处理具有依赖关系的任务（线性链、扇入/扇出结构、部分依赖关系）、动态调整批处理规模以及条件性任务调度的方法，请参考 `references/advanced-patterns.md`。