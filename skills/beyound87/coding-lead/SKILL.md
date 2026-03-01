---
name: coding-lead
description: 这是一种智能的编码技巧，能够根据任务的复杂程度来分配处理任务的方式：简单任务（代码量少于60行，文件数量较少）会直接通过OpenClaw代理工具执行；而中等或复杂的任务则会通过ACP（Agent Configuration Platform）生成Claude Code，其中包含了完整的项目上下文、编码规范以及代理系统中的历史决策记录。该技巧适用于用户需要编写代码、修复错误、开发新功能、重构代码、审查代码提交（PR）、部署软件或执行任何其他软件工程相关任务的情况。它结合了OpenClaw的长期记忆功能与Claude Code强大的编码能力，实现了高效的代码管理。
---
# 编码负责人

根据任务的复杂性来分配编码任务：简单任务由人工完成；复杂任务则使用 Claude Code 并提供完整的环境信息。

## 对系统的影响

- **简单任务**：直接使用读/写/编辑/执行工具来修改项目文件。
- **中等/复杂任务**：通过 `sessions_spawn(runtime: "acp")` 调用 Claude Code，该命令会创建一个具有指定项目目录文件系统访问权限的子进程。
- **内存写入**：在每次任务完成后，将决策和更改记录到代理的内存文件中。
- **无需凭证**：使用已配置的模型提供者。
- **ACP 要求**：对于中等/复杂任务，必须要有 Claude Code（或兼容的编码代理）作为 ACP 工具；简单任务则无需 ACP。

## 为什么需要这样的机制

OpenClaw 代理具有内存功能，但编码能力有限；Claude Code 具有强大的编码能力，但无法在不同会话之间保持状态。这种机制弥补了这一缺陷：代理充当具有持久上下文的工程管理者，而 Claude Code 则担任专家级编码者。

## 新项目的技术栈推荐

在开始新项目时，根据以下推荐的技术栈进行提案，并在开始编码前获得确认：

| 层次 | 首选技术栈 | 备选技术栈 |
|-------|-----------|----------|
| 后端 | PHP（Laravel 或 ThinkPHP） | Python |
| 前端 | Vue.js | React |
| 移动端 | Flutter | UniApp-X |
| CSS | Tailwind CSS | - |
| 数据库 | MySQL | PostgreSQL |

- **现有项目**：遵循当前的技术栈，未经明确批准不得迁移。
- **新项目**：在计划阶段提出技术栈建议，等待确认。
- 将技术栈选择包含在 Claude Code 的提示中，以确保使用正确的框架。

## 任务分类

在执行每个编码任务之前，先进行评估：

| 任务级别 | 判断标准 | 处理方式 |
|-------|----------|--------|
| **简单** | 单个文件，需求明确，修改量少于 60 行 | 直接使用读/写/编辑/执行工具执行 |
| **中等** | 涉及 2-5 个文件，需要进一步调查，任务范围明确 | 调用 Claude Code 并提供上下文信息 |
| **复杂** | 需要调整架构，涉及多个模块，不确定性较高 | 先制定计划，再调用 Claude Code |

如果有疑问，应提升任务难度等级。

## 简单任务：直接执行

使用代理工具：读、写、编辑、执行。

**编码前**：
1. 读取目标文件。
2. 检查编码规范（查看项目中的 tech-standards.md、CLAUDE.md、.cursorrules 或相关文档）。
3. 在内存中查找相关的过往决策。

**编码后**：
4. 自我检查：是否符合编码规范？
5. 将更改记录到每日内存文件中。

**示例**：配置编辑、小错误修复、添加字段、重命名文件、格式化。

## 中等/复杂任务：调用 Claude Code

### 第一步：收集上下文（由代理完成）

在调用 Claude Code 之前，从以下来源收集信息：
1. **项目信息**：读取 CLAUDE.md、README 或 package.json/composer.json。
2. **编码规范**：查看 tech-standards.md（共享知识）、CLAUDE.md（项目特定规范）、.cursorrules 或类似文档。
3. **过往决策**：在 MEMORY.md 和每日内存记录中查找相关内容。
4. **任务背景**：查看收件箱消息、看板任务、产品文档（如适用）。
5. **潜在问题**：从内存中了解关于该代码库的已知问题。

### 第二步：构建提示信息

为 Claude Code 构建提示结构：

```
## Project
- Path: [project directory]
- Tech stack: [from docs or memory]
- Key architecture notes: [from CLAUDE.md or memory]

## Coding Standards (mandatory)
[Paste or summarize from whatever standards file exists]
- [Key rule 1]
- [Key rule 2]
- [Project-specific rules]

## Historical Context
[From agent memory — skip if no relevant history]
- [Past decision 1]
- [Known pitfall]
- [Related prior work]

## Task
[Clear description]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] Existing tests pass
- [ ] No unrelated changes
- [ ] Cleaned up: no debug logs, unused imports, temp files
```

### 第三步：调用 Claude Code

- **中等任务**：`sessions_spawn(runtime: "acp", task: <提示信息>, cwd: <项目目录>, mode: "run")`
- **复杂任务**：`sessions_spawn(runtime: "acp", task: <提示信息>, cwd: <项目目录>, mode: "session")`

如果需要，可以通过 sessions_send 进行后续操作。

### 第四步：审查结果

Claude Code 完成后：
1. 检查是否符合接受标准。
2. 确认没有无关的更改。
3. 如果有测试需求，运行测试。
4. 如果不满意，通过 sessions_send 发送反馈。

### 第五步：记录到内存中

更新每日内存文件，内容包括：
- 所做的操作及其原因。
- 重要的决策。
- 遇到的问题。
- 未来会话需要了解的信息。

这是代理的关键优势：它可以在不同会话之间保留所有信息。

## 复杂任务的流程：研究 > 规划 > 执行 > 审查

### 研究
以会话模式调用 Claude Code 进行调查（不进行任何修改）：
- 列出需要修改的文件。
- 识别依赖关系和调用链。
- 查找可重用的现有代码。
- 标记潜在风险。

### 规划
审查调查结果。如果存在多种方案，提出选择并获取确认后再继续。

### 执行
根据确认后的计划和完整上下文调用 Claude Code。如有必要，可以将任务分解为多个子任务。

### 审查
验证结果。运行测试。将决策和经验教训记录到内存中。

## 对 Claude Code 的工具提示

在为 Claude Code 构建提示时，提醒它使用以下工具：
- LSP（goToDefinition、findReferences）用于理解代码结构。
- Grep/Glob 用于查找文件和模式。
- mcp__context7 用于获取库文档。
- mcp__mcp-deepwiki 用于获取开源项目文档。

这些是 Claude Code 的工具，而非 OpenClaw 的工具。只需在提示中包含这些工具的名称。

## 内存整合方式

### 调用前
在调用 Claude Code 之前，从内存中查找相关的过往记录，并将这些信息作为“历史背景”包含在提示中。

### 完成后
详细记录更改内容、做出的决策、遇到的问题以及测试结果。

### 跨会话连续性
当任务跨越多个会话时：
- 会话结束时：将详细状态记录到内存中。
- 下一个会话开始时：读取内存内容，重建上下文。
- 使用累积的上下文再次调用 Claude Code。

这是 Claude Code 的核心优势：每次会话结束后，Claude Code 会“忘记”之前的所有信息，而代理则可以保持记忆。

## 进度更新

在调用 Claude Code 处理中等/复杂任务时，及时向用户反馈：
1. **启动时**：发送一条简短消息，说明任务内容、项目名称和预估复杂度。
2. **达到里程碑时**：只有在有重要进展时（如代码构建完成、测试通过等）才发送消息。
3. **出错时**：立即报告问题及是否需要重试。
4. **完成时**：总结更改内容、修改的文件以及测试结果。

**注意**：不要静默运行。不要长时间不与用户沟通。用户不应怀疑“任务是否还在运行中”。

## 完成后自动通知

在调用 Claude Code 时，在提示信息末尾添加通知命令，以便自动触发通知：

```
... your task description here.

When completely finished, run this command to notify:
openclaw system event --text "Done: [brief summary of what was built/changed]" --mode now
```

这样可以立即通知用户任务已完成。

## 工作目录隔离

调用 Claude Code 时，务必指定 `cwd`，以确保编码代理专注于任务相关的内容：
- 将 `cwd` 设置为 **项目目录**，而非代理的工作目录。
- 这可以防止代理读取团队管理文件（如 SOUL.md、收件箱等）。
- 如果项目路径未知，在调用前请先询问用户。

```
sessions_spawn(runtime: "acp", task: <prompt>, cwd: "/path/to/project", mode: "run")
```

## 并行任务

独立的编码任务可以并行执行：
- 启动多个 ACP 会话，每个会话负责不同的任务和项目目录。
- 通过 `sessions_list` 或 `subagents(action: "list")` 追踪任务进度。
- 每个会话都有独立的上下文，避免相互干扰。
- 所有任务完成后，汇总结果并记录到内存中。

**示例**：同时修复 3 个独立的问题，每个问题都在各自的会话中处理。

**注意**：注意 API 的速率限制和系统资源限制。通常同时运行 2-3 个会话是安全的。

## 智能重试（最多尝试 3 次）

如果 Claude Code 会话失败，不要使用相同的提示重新尝试。而是：
1. **分析失败原因**：
   - 上下文不足？→ 缩小范围：“仅关注这 3 个文件”。
   - 方向错误？→ 明确要求：“实际需求是 X，而不是 Y”。
   - 缺少信息？→ 添加缺失的信息（如类型定义、配置文件或文档）。
   - 环境问题？→ 先解决环境问题，再尝试。
2. **修改提示信息**：根据分析结果调整提示内容，添加必要的限制或上下文。
3. **重新尝试**：使用修改后的提示信息启动新的会话。
4. **最多尝试 3 次**：如果三次尝试都失败，停止尝试并向用户报告：
   - 尝试的内容。
   - 每次失败的原因。
   - 你的分析结果。
   - 建议的下一步操作（可能需要人工干预）。

**注意**：不要盲目重试。每次尝试都应有所不同。

## 提示信息模板库

每次成功完成任务后，将有效的操作方式记录到内存中：

```
## Prompt Pattern: [task type]
- What worked: [prompt structure that succeeded]
- Key ingredients: [what context was essential]
- Pitfalls: [what caused failures before success]
- Example: [brief prompt snippet]
```

随着时间的积累，这些成功的操作方式会形成模板库。在调用 Claude Code 之前，可以从内存中查找类似的过往任务并复用这些模板。

**值得记录的模板示例**：
- “处理计费功能时，需要提前获取完整的数据库架构信息”。
- “重构代码时，提供明确的文件列表和依赖关系图会更有效”。
- “API 端点开发时，需要参考现有的路由模式”。
- “处理与测试相关的任务时，务必包含测试文件路径”。

这些累积的知识可以使未来的任务更加高效和可靠。

## 安全规则
- **切勿在 ~/.openclaw/ 或代理工作目录中执行编码任务**——代理可能会读取或修改配置文件、文档或内存文件。
- **未经明确批准，禁止代理修改项目目录之外的文件**。
- **在提交更改前，务必审查输出结果**——尤其是对于复杂任务。
- **终止失控的会话**：如果会话超时或产生无意义的输出，立即终止该会话并报告问题。

## 参考资料
- references/prompt-examples.md：不同类型任务的真实提示示例。