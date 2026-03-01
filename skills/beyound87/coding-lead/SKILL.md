---
name: coding-lead
description: 这是一种智能的编码技巧，能够根据任务的复杂程度来自动分配处理任务的方式：简单任务（代码量少于60行，且仅涉及单个文件）会直接通过OpenClaw代理工具执行；而中等或复杂的任务则会利用ACP（Agent Code Platform）生成Claude Code。Claude Code会包含完整的项目上下文、编码规范以及代理系统存储的历史决策信息。该技巧适用于用户需要编写代码、修复错误、开发新功能、重构代码、审查代码提交（PR）、部署软件或执行任何其他软件工程相关任务的情况。它巧妙地结合了OpenClaw的长期数据存储能力与Claude Code的强大编码功能，提升了编码工作的效率和准确性。
---
# 编码主管

> **重要提示：**此技能的优先级高于代理 SOUL.md 文件中的任何内联编码规则。如果代理的 SOUL.md 文件中包含“编码行为”部分，在加载此技能时请跳过该部分。

**按复杂度分配编码任务：**
- **简单任务**：自行完成；
- **复杂任务**：使用 Claude Code 并提供完整上下文。

## 系统影响

- **简单任务**：使用读/写/编辑/执行工具直接修改项目文件；
- **中等/复杂任务**：通过 `sessions_spawn(runtime: "acp")` 调用 Claude Code，该代码会创建一个具有指定项目目录文件系统访问权限的子进程；
- **内存写入**：在每次任务完成后将决策和更改记录到代理的内存文件中；
- **无需凭证**：使用已配置的任何模型提供者；
- **ACP 要求**：对于中等/复杂任务，必须要有 Claude Code（或兼容的编码代理）作为 ACP 工具。简单任务无需 ACP。

## 设计此技能的原因

OpenClaw 代理具有内存，但编码能力有限；Claude Code 具有强大的编码能力，但无法在会话之间保持状态。此技能解决了这一问题：代理充当具有持久上下文的工程管理者，而 Claude Code 则担任专家编码者。

## 新项目的技术栈偏好

在开始新项目时，根据以下偏好提出技术栈建议，并在编码前获得确认：

| 层次 | 首选技术栈 | 备选技术栈 |
|-------|-----------|----------|
| 后端 | PHP（Laravel 或 ThinkPHP） | Python |
| 前端 | Vue.js | React |
| 移动端 | Flutter | UniApp-X |
| CSS | Tailwind CSS | - |
| 数据库 | MySQL | PostgreSQL |

- **现有项目**：遵循当前的技术栈，未经明确批准不得迁移；
- **新项目**：在规划阶段提出技术栈建议，等待确认；
- 将技术栈选择包含在 Claude Code 的提示中，以确保使用正确的框架。

## 任务分类

在执行前对每个编码请求进行评估：

| 任务级别 | 评估标准 | 处理方式 |
|-------|----------|--------|
| **简单** | 单个文件，需求明确，修改量小于 60 行 | 直接使用读/写/编辑/执行工具执行 |
| **中等** | 2-5 个文件，需要调查，范围明确 | 调用 Claude Code 并提供上下文 |
| **复杂** | 涉及架构变更、多模块、不确定性高 | 先进行规划，再调用 Claude Code |

**如有疑问，提升一个处理层级。**

## 简单任务：直接执行

使用代理工具：读、写、编辑、执行。

**编码前：**
1. 读取目标文件；
2. 检查编码标准（查看项目或共享知识库中的 tech-standards.md、CLAUDE.md、.cursorrules 等文件）；
3. 在内存中搜索相关的过往决策。

**编码后：**
4. 自我检查：是否符合标准？
5. 将更改记录到每日内存文件中。

**示例：**配置编辑、小错误修复、添加字段、重命名、格式调整。

## 中等/复杂任务：调用 Claude Code

### 第一步：收集上下文（由代理完成）

在调用 Claude Code 之前，从以下来源收集信息：
1. **项目信息**：读取 CLAUDE.md、README 或 package.json/composer.json；
2. **编码标准**：检查 tech-standards.md（共享知识库）、CLAUDE.md（项目文件）、.cursorrules 或类似文件；
3. **过往决策**：在 MEMORY.md 和每日内存记录中搜索相关内容；
4. **任务上下文**：收件箱消息、看板任务、产品文档（如适用）；
5. **已知问题**：关于该代码库的任何注意事项。

### 第二步：构建提示

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
[From agent memory -- skip if no relevant history]
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

- **中等任务**：`sessions_spawn(runtime: "acp", task: <提示>, cwd: <项目目录>, mode: "run")`
- **复杂任务**：`sessions_spawn(runtime: "acp", task: <提示>, cwd: <项目目录>, mode: "session")`

**会话模式**：如需跟进，可通过 sessions_send 进行。

### 第四步：审查输出

Claude Code 完成后：
1. 检查是否符合接受标准；
2. 确认没有无关的更改；
3. 如果有测试，运行测试；
4. 如不满意，通过 sessions_send 发送跟进信息。

### 第五步：记录到内存

更新每日内存文件，内容包括：
- 所做的操作及原因；
- 作出的关键决策；
- 遇到的问题；
- 未来会话需要了解的信息。

这是代理的关键优势：它可以在会话之间保留所有信息。

## 复杂任务流程：**研究 > 规划 > 执行 > 审查**

### 研究
以会话模式调用 Claude Code 进行调查（不进行任何更改）：
- 列出需要修改的文件；
- 识别依赖关系和调用链；
- 查找可重用的现有代码；
- 标记风险。

### 规划
审查调查结果。如果存在多种方法，提出选项并获取确认后再继续。

### 执行
根据确认的规划调用 Claude Code，并提供完整上下文。如有需要，可将任务分解为子任务。

### 审查
验证输出结果。运行测试。将决策和经验教训更新到内存中。

## 复杂任务中的编码角色

对于涉及多个层面的复杂任务（架构 + 前端 + 后端 + 审查），使用特定角色的 Claude Code 会话。这样可以确保每个阶段都有专注的专家参与，而无需增加额外的代理。

### 何时使用角色
- **简单/中等任务**：不要使用角色。一次调用，一个提示，完成任务。
- **复杂任务（多层面）**：当任务涉及架构设计、前端、后端或需要独立审查时，使用角色。

### 可用角色

| 角色 | 使用时机 | 提示前缀 |
|------|------------|---------------|
| **架构师** | 系统设计、数据库模式、API 合同、技术决策 | “你是一位资深软件架构师。设计可扩展、可维护的系统。输出：包含文件结构、数据库模式、API 合同和实现说明的设计文档。” |
| **前端** | UI 组件、页面、响应式设计、状态管理 | “你是一位前端专家。编写清晰、易用、性能良好的 UI 代码。遵循项目的前端规范。” |
| **后端** | API 端点、业务逻辑、数据层、集成 | “你是一位后端专家。编写安全、高效的服务器端代码。遵循项目后端规范。” |
| **审查员** | 实现后的代码审查 | “你是一位资深代码审查员。审查逻辑错误、安全问题、性能问题、风格违规之处。请具体说明，并提供行号。” |
| **质量保证** | 测试编写、边缘情况分析 | “你是一位质量保证工程师。编写全面的测试用例。考虑边缘情况、错误路径和集成场景。” |

### 带有角色的复杂任务流程

```
1. RESEARCH (agent reads code, searches memory)
2. PLAN (agent designs approach, gets confirmation)
3. ARCHITECT (spawn) -- if task needs design decisions
   -> output: design doc, schema, API contracts
4. IMPLEMENT (spawn, can be parallel)
   -> Frontend session (if UI involved)
   -> Backend session (if API/logic involved)
   -> Or single fullstack session for smaller scope
5. REVIEW (spawn) -- independent reviewer session
   -> input: diff of all changes
   -> output: issues found, suggestions
6. FIX (spawn or sessions_send) -- address review findings
7. RECORD (agent logs to memory)
```

并非所有步骤都必須执行。不适用的步骤可以跳过：
- 无需前端操作？跳过前端相关内容；
- 仅仅是后端修改？跳过架构师和审查员的步骤；
- 只涉及单一层面的修改？直接调用 Claude Code，无需使用角色。

### 角色提示模板

在标准提示结构前加上角色前缀：

```
[Role prefix from table above]

## Project
- Path: [project dir]
- Stack: [from docs]
...rest of standard prompt...
```

### 并行调用角色

如果前端和后端任务互不依赖，可以同时运行：

```
# These can run simultaneously
Session 1: Frontend role -> "Build the FavoriteButton component..."
Session 2: Backend role -> "Build the favorites API endpoint..."

# This must wait for both to finish
Session 3: Reviewer role -> "Review all changes in [files from session 1 + 2]..."
```

## Claude Code 工具提示

在为 Claude Code 构建提示时，提醒它使用以下工具：
- LSP（goToDefinition、findReferences）用于代码结构分析；
- Grep/Glob 用于查找文件和模式；
- mcp__context7 用于库文档查询；
- mcp__mcp-deepwiki 用于开源项目文档查询。

这些是 Claude Code 的工具，而非 OpenClaw 的工具。仅在生成的提示中包含这些工具的引用。

## 内存整合规则

### 调用前
在内存中搜索相关的过往工作，并将结果作为“历史背景”包含在提示中。

### 完成后
详细记录更改内容、作出的决策、遇到的问题以及测试结果。

### 跨会话连续性
当任务跨越多个会话时：
1. 会话结束时：将详细状态写入内存；
2. 下一次会话开始时：读取内存内容，重建上下文；
3. 使用累积的上下文再次调用 Claude Code。

这是核心优势：Claude Code 在每次会话结束后会“忘记”之前的内容，而代理则不会。

## 进度更新

在调用 Claude Code 处理中等/复杂任务时，及时通知用户：
1. **开始时**：发送一条简短消息，说明任务内容、项目名称及预估复杂度；
2. **达到里程碑时**：仅在发生重要事件时（如任务完成、测试通过或遇到障碍）通知；
3. **出错时**：立即报告问题及是否需要重试；
4. **完成时**：总结更改内容、修改的文件及测试结果。

**自动通知完成情况**

在调用 Claude Code 时，在提示末尾添加通知命令，以便自动触发通知：

```
... your task description here.

When completely finished, run this command to notify:
openclaw system event --text "Done: [brief summary of what was built/changed]" --mode now
```

这样可以立即通知用户，而无需等待下一次轮询。

## 工作目录隔离

调用 Claude Code 时始终指定 `cwd`，以确保编码代理专注于任务：
- 将 `cwd` 设置为 **项目目录**，而非代理的工作目录；
- 这可以防止编码代理读取团队管理文件（如 SOUL.md、收件箱等）；
- 如果项目路径未知，请在调用前询问用户。

```
sessions_spawn(runtime: "acp", task: <prompt>, cwd: "/path/to/project", mode: "run")
```

## 并行任务

独立的编码任务可以并行执行：
- 启动多个 ACP 会话，每个会话负责不同的任务和项目目录；
- 通过 `sessions_list` 或 `subagents(action: "list")` 追踪任务进度；
- 每个会话都有独立的上下文，互不干扰；
- 所有任务完成后，审查结果并记录到内存中。

**示例**：同时修复 3 个独立的错误，每个任务在单独的会话中完成。

**注意**：注意 API 的速率限制和系统资源限制。通常同时运行 2-3 个会话是安全的。

## 根据复杂度进行审查

并非所有任务都需要全面审查。根据任务复杂度调整审查力度：

- **简单任务（代理直接完成）**：无需正式审查。如果功能正常，即可视为完成。
- **中等任务（Claude Code 完成）**：仅进行快速检查：
  - Claude Code 是否报告成功？
  - 测试是否通过？
  - 快速查看输出中是否有明显错误？
  - 完成后即可继续。
- **复杂任务（Claude Code 完成）**：进行全面检查：
  - 逻辑是否正确（包括边缘情况、空值检查、错误路径）；
  - 安全性是否达标（如注入攻击、权限绕过、数据泄露）；
  - 性能是否良好（如是否存在 N+1 查询、不必要的循环、缺失的索引）；
  - 代码风格是否符合标准、命名是否一致；
  - 测试是否通过（包括现有测试和新增逻辑的测试）。

如果任何检查项未通过，通过 sessions_send 发送跟进信息进行修复（这计入重试次数）。

## 提示中的自动检查

在为 Claude Code 构建提示时，始终在提示末尾添加以下内容：

```
Before finishing:
1. If a linter is available (npm run lint / php artisan lint / etc.), run it and fix issues
2. If tests exist (npm test / php artisan test / pytest / etc.), run them and ensure they pass
3. Include the check results in your final output
```

这不会额外消耗令牌——Claude Code 会在执行过程中自动执行这些检查。

## 智能重试（最多尝试 3 次）

如果 Claude Code 会话失败，不要使用相同的提示重新尝试。 instead：
1. **分析失败原因**：
  - 上下文不足？ -> 缩小范围：“仅关注这 3 个文件”；
  - 方向错误？ -> 明确要求：“需求是 X，而非 Y”；
  - 缺少信息？ -> 添加缺失的类型定义、配置或文档；
  - 环境问题？ -> 先修复环境，再尝试；
2. **修改提示**：根据分析结果调整提示内容；
3. **重新尝试**：使用改进后的提示重新启动会话；
4. **最多尝试 3 次**：如果三次尝试仍失败，向用户报告：
  - 尝试的内容；
  - 每次失败的原因；
  - 你的分析结果；
  - 建议的下一步行动（可能需要人工干预）。

**切勿盲目重试**。每次尝试都应有所不同。

## 提示模板库

每次成功完成编码任务后，将有效的操作记录到内存中：

```
## Prompt Pattern: [task type]
- What worked: [prompt structure that succeeded]
- Key ingredients: [what context was essential]
- Pitfalls: [what caused failures before success]
- Example: [brief prompt snippet]
```

随着时间的推移，这会形成一个包含有效提示模式的库。在调用 Claude Code 之前，可以在内存中搜索类似的过往任务并重用成功的提示结构。

**值得记录的提示模板示例：**
- “计费功能需要预先提供完整的数据库模式信息”；
- “重构时提供明确的文件列表和依赖关系图会更有帮助”；
- “API 端点需要参考现有的路由模式”；
- “测试相关任务必须包含测试文件路径”。

这些累积的知识可以使未来的任务更加高效和可靠。

## 安全规则
- **切勿在 ~/.openclaw/ 或代理工作目录中调用编码任务**——编码代理可能会读取/修改配置文件、文档或内存文件；
- **未经明确批准，禁止编码代理修改项目目录外的文件**；
- **在提交之前务必审查输出结果**——尤其是对于复杂任务；
- **终止失控的会话**——如果会话超时或产生无意义的输出，立即终止会话并报告。

## 参考资料
- references/prompt-examples.md：不同类型任务的真实提示示例