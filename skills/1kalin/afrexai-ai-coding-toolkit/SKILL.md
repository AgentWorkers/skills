# AI编码工具包——掌握每一个AI编码助手

> 一套完整的开发方法论，通过AI辅助开发将你的生产力提升10倍。涵盖了Cursor、Windsurf、Cline、Aider、Claude Code、GitHub Copilot等工具——这些工具通用性强，适用于各种场景。

## 第一阶段：快速评估——你的水平如何？

请对以下每个方面进行1-5分的评分：

| 维度 | 1（初学者） | 5（专家） |
|---|---|---|
| 提示质量 | “修复这个漏洞” | 结构化的上下文 + 限制条件 + 示例 |
| 上下文管理 | 粘贴整个文件 | 精选的上下文窗口、.cursorrules文件、AGENTS.md文件 |
| 工作流程整合 | 临时使用 | 系统化的、以AI为中心的开发流程 |
| 输出验证 | 直接接受结果 | 提交前进行审查、测试和迭代 |
| 工具选择 | 用一个工具完成所有任务 | 为每个任务选择合适的工具 |

**评分说明：**
- 5-10分：全面了解所有内容——你的工作效率将提升10倍 |
- 11-18分：可以直接进入第4阶段及以上，学习更高级的技术 |
- 19-25分：专注于第8-10阶段，掌握更高级的技巧和模式 |

---

## 第二阶段：工具选择矩阵

### 决策指南：何时使用哪种AI编码工具？

| 工具 | 最适合 | 上下文窗口 | 自主性 | 成本 |
|---|---|---|---|---|
| **GitHub Copilot** | 行/函数补全、内联建议 | 当前文件及相邻文件 | 低（自动完成功能） | 每月10-19美元 |
| **Cursor** | 全文件编辑、多文件重构、聊天功能 | 项目感知（索引功能） | 中等（标签页/聊天/代码编辑器） | 每月20美元 |
| **Windsurf (Cascade)** | 自主的多步骤任务处理 | 项目感知 + 流程管理 | 高（自主性强的流程管理） | 每月15美元 |
| **Cline** | VS Code扩展插件，模型无关，透明度高 | 手动上下文管理 + 自动化建议 | 高（工具使用成本） | 需通过API支付 |
| **Aider** | 基于终端的工具，支持Git操作 | 仓库映射 + 选定的文件 | 中等偏高（需要通过API支付） |
| **Claude Code** | 命令行工具，适用于复杂的多文件任务 | 工作区感知 | 高（需要通过API支付） |
| **OpenClaw** | 持久化的AI助手，支持定时任务 | 工作区 + 内存管理 + 多种工具集成 | 非常高（需要通过API支付） |

### 工具选择决策树

```
Need autocomplete while typing?
  → GitHub Copilot (layer it with any other tool)

Working in VS Code/IDE?
  ├─ Want integrated editor experience? → Cursor or Windsurf
  ├─ Want model flexibility + transparency? → Cline
  └─ Want minimal config, just works? → Cursor

Working in terminal?
  ├─ Want git-native pair programming? → Aider
  ├─ Want full agent with tools? → Claude Code
  └─ Want persistent autonomous agent? → OpenClaw

Building complex multi-file features?
  → Cursor Composer or Windsurf Cascade or Claude Code

Need autonomous background work?
  → OpenClaw (cron, heartbeats, multi-session)
```

### 推荐的工具组合（按层次使用）

**独立开发者：**
1. GitHub Copilot（始终开启自动完成功能）
2. Cursor 或 Windsurf（主要集成开发环境）
3. Claude Code 或 Aider（用于复杂任务的终端工具）

**团队：**
1. GitHub Copilot（在整个团队中统一使用）
2. Cursor（主要集成开发环境，并在仓库中配置.curserrules文件）
3. 使用CI/CD流程进行AI代码审查（自动化代码提交审查）

---

## 第三阶段：上下文工程——最重要的技能

上下文是关键。AI的输出质量直接取决于你提供的上下文质量。

### 上下文层次结构（从重要到不重要）

1. **系统指令**（.cursorrules文件、AGENTS.md文件、CLAUDE.md文件、.windsurfrules文件）
2. **显式上下文**（你在聊天中提到的文件或添加的文件）
3. **隐式上下文**（打开的标签页、最近的编辑记录、项目索引）
4. **模型知识**（训练数据——对于你的代码库来说可靠性较低）

### 项目规则文件模板

在项目根目录下创建该文件。文件名称根据所使用的工具而定：
- Cursor：.cursorrules
- Windsurf：.windsurfrules
- Claude Code：CLAUDE.md
- Aider：.aider.conf.yml文件 + 相关文档
- OpenClaw：AGENTS.md

```yaml
# [PROJECT] — AI Coding Context

## Project Overview
- Name: [project name]
- Stack: [e.g., Next.js 14 + TypeScript + Tailwind + Drizzle + PostgreSQL]
- Architecture: [e.g., App Router, server components by default]
- Monorepo: [yes/no, structure if yes]

## Code Standards (ENFORCE STRICTLY)
- TypeScript strict mode (`tsc --noEmit --strict`)
- Max 50 lines per function, 300 lines per file
- One responsibility per file
- Naming: camelCase functions, PascalCase types, SCREAMING_SNAKE constants
- Imports: named imports, no default exports
- Error handling: explicit try/catch, typed errors, no silent catches

## Patterns to Follow
- [Pattern 1 with example]
- [Pattern 2 with example]
- [Pattern 3 with example]

## Anti-Patterns (NEVER DO)
- [Anti-pattern 1]
- [Anti-pattern 2]
- [Anti-pattern 3]

## File Structure
```
src/
  components/     # React组件
  lib/            # 共享工具库
  server/         # 仅服务器相关的代码
  db/             # 数据库模式及查询代码
  types/          # 共享的TypeScript类型定义
```

## Testing
- Framework: [vitest/jest/pytest]
- Pattern: AAA (Arrange, Act, Assert)
- Naming: `should [expected behavior] when [condition]`
- Coverage target: [80%+]

## Dependencies
- Approved: [list]
- Banned: [list with reasons]

## Common Commands
- `npm run dev` — start dev server
- `npm run test` — run tests
- `npm run lint` — lint + typecheck
- `npm run build` — production build
```

### 上下文窗口管理

**80/20法则：**80%的上下文应该是与任务相关的具体文件/函数；20%应该是项目规范和标准。

**上下文压缩技巧：**
1. **总结而非复制**——不要直接粘贴500行的文件，而是描述文件的功能并仅粘贴相关部分。
2. **使用@提及**——例如使用`@file.ts`而不是直接复制粘贴（具体工具相关）。
3. **创建参考文档**——编写一页的架构概述，供AI参考。
4. **清理聊天记录**——为新任务开启新的聊天对话；过时的上下文会导致错误。
5. **使用`tree`命令**——向AI展示项目结构：`tree -I node_modules -L 3`

### 上下文更新规则

> 每5-10条消息后，检查：AI是否仍在正确跟踪上下文？
> 如果它开始错误地识别文件名或函数名，或者做出错误的假设——**使用新的上下文重新开始聊天**。
> 上下文就像牛奶一样，容易变质。

---

## 第四阶段：代码提示工程

### SPEC框架（结构、精确性、示例、限制条件）

**糟糕的提示：**
```
Fix the login bug
```

**好的提示（遵循SPEC框架）：**
```
## Structure
Fix the authentication flow in `src/auth/login.ts`

## Precision
- The login function throws "user not found" even when the user exists
- Error occurs on line 42 when querying by email (case-sensitive match)
- PostgreSQL query uses exact match but emails are stored lowercase

## Examples
- Input: "User@Example.com" → should match "user@example.com" in DB
- Current behavior: returns null
- Expected: returns user record

## Constraints
- Don't change the database schema
- Use the existing `normalizeEmail()` utility from `src/utils/email.ts`
- Add a test case for case-insensitive lookup
- Keep the existing error handling pattern (throw AppError)
```

### 不同任务类型的提示模板

**功能实现：**
```
Implement [feature] in [file/location].

Requirements:
1. [Requirement with acceptance criteria]
2. [Requirement with acceptance criteria]
3. [Requirement with acceptance criteria]

Constraints:
- Follow existing patterns in [reference file]
- Use [specific library/approach]
- Include error handling for [edge cases]
- Write tests in [test file location]

Reference: Here's how similar feature [X] was implemented:
[paste relevant code snippet]
```

**错误修复：**
```
Bug: [description]
File: [path]
Steps to reproduce: [1, 2, 3]
Expected: [behavior]
Actual: [behavior]
Error: [paste error message/stack trace]

Fix constraints:
- Don't change [protected areas]
- Add regression test
- Explain root cause before fixing
```

**重构：**
```
Refactor [file/module] to [goal].

Current state: [describe current architecture]
Target state: [describe desired architecture]
Motivation: [why — performance, readability, maintainability]

Rules:
- Preserve all existing behavior (no functional changes)
- Keep all existing tests passing
- Break into small, reviewable commits
- Each commit should be independently deployable
```

**代码审查：**
```
Review this code for:
1. Correctness — logic errors, edge cases, race conditions
2. Security — injection, auth bypass, data exposure
3. Performance — N+1 queries, unnecessary allocations, missing indexes
4. Maintainability — naming, complexity, test coverage

Be specific: quote the line, explain the issue, suggest the fix.
Skip style/formatting — linter handles that.

[paste code]
```

---

## 第五阶段：以AI为中心的工作流程模式

### 模式1：测试驱动的AI开发（TDD-AI）

```
1. Write the test first (yourself or with AI help)
2. Ask AI to implement the code that passes the test
3. Run tests — verify green
4. Ask AI to refactor while keeping tests green
5. Review the final code yourself
```

**为什么有效：**测试本身就是需求规格。当AI有明确的目标时，它能够编写出更好的代码。这样可以立即发现错误。

### 模式2：搭建框架 → 填充内容 → 审查

```
1. Ask AI to scaffold the architecture (file structure, interfaces, types)
2. Review and approve the scaffold
3. Ask AI to fill in implementation file by file
4. Review each file individually
5. Integration test the full feature
```

**为什么有效：**你保持了对架构的控制。AI负责处理繁琐的工作。这样可以在每个阶段发现错误。

### 模式3：聊天式开发

```
Chat 1: Architecture discussion → decisions documented
Chat 2: Implementation of Component A (reference architecture doc)
Chat 3: Implementation of Component B (reference architecture doc)
Chat 4: Integration + testing
```

**为什么有效：**每个组件都有最新的上下文，防止代码偏离设计方向。架构文档提供了连贯性。

### 模式4：AI辅助的结对编程（Aider/Claude Code）

```
1. Start session with repo context
2. Describe the task in natural language
3. AI proposes changes as git diffs
4. Review each diff before accepting
5. AI commits with meaningful messages
6. You handle edge cases and integration
```

### 模式5：自主运行的AI工作流程（OpenClaw/Claude Code）

```
1. Define task in structured format (acceptance criteria, constraints)
2. Agent plans → executes → verifies (reads files, runs tests)
3. Agent creates PR/branch with changes
4. You review the complete changeset
5. Iterate on feedback
```

---

## 第六阶段：特定工具的高级技巧

### Cursor

| 功能 | 高级技巧 |
|---|---|
| **标签页补全** | 在接受建议前让它补全3-5个代码片段——这样可以及早发现错误预测 |
| **Cmd+K**（内联编辑） | 仅选择需要修改的行——减少上下文信息，提高准确性 |
| **聊天** | 使用`@file`来提供上下文信息，使用`@codebase`来询问项目相关问题 |
| **代码编辑器** | 支持多文件修改——详细描述功能，让AI跨文件进行编辑 |
| **.cursorrules** | 为项目定制的AI指令——将结果提交到仓库中，确保团队成员理解一致 |
| **笔记簿** | 可复用的上下文信息（API文档、设计文档）——可以附加到任何聊天对话中 |

**Cursor的高级使用技巧：**
- 使用`@git`来引用最近的代码更改
- 使用`@docs`来引用官方库文档
- 为不同的领域创建`.cursorrules`文件夹
- 使用“应用”按钮将聊天建议直接应用到代码中

### Windsurf (Cascade)

| 功能 | 高级技巧 |
|---|---|
| **多步骤自主任务** | 支持多步骤的自主任务处理 |
| **写入模式** | 直接在文件中进行编辑 |
| **聊天模式** | 仅用于讨论，不进行编辑 |
| **.windsurfrules** | 项目专用上下文文件 |
| **快速模式** | 更快但准确性较低——适合简单任务 |

**Windsurf的高级使用技巧：**
- Windsurf擅长多文件重构——提供完整的任务范围 |
- 使用“撤销流程”来恢复多步骤的更改 |
- 将重要文件固定在上下文中 |
- 让AI读取终端输出以自动修复错误

### Cline

| 功能 | 高级技巧 |
|---|---|
| **模型选择** | 根据任务选择合适的模型（简单任务使用便宜的模型，复杂任务使用昂贵的模型） |
| **工具使用** | 可以读取文件、运行命令、打开浏览器——提供全面的AI支持 |
| **透明度** | 在执行前显示所有操作——便于审计 |
| **自定义指令** | 为每个项目定制提示 |

**Cline的高级使用技巧：**
- 设置使用成本上限，防止API费用过高 |
- 对于简单任务，使用成本较低的模型（如Haiku/GPT-4o-mini） |
- 启用“差异模式”来查看具体的更改内容 |
- 创建特定于任务的指令文件

### Aider

| 功能 | 高级技巧 |
|---|---|
| **/add`文件** | 明确控制AI可以查看/编辑的文件 |
| **/read`文件** | 提供只读的上下文信息（参考文件） |
| **/architect** | 结合两种模型进行开发——规划者制定方案，编辑器执行 |
| **仓库映射** | 自动生成代码库的概览 |
| **Git集成** | 每次更改都会触发提交——便于回滚 |

**Aider的高级使用技巧：**
- 对于复杂任务，使用`--architect`标志 |
- 使用`/drop`命令删除不需要的文件，释放上下文窗口 |
- 使用`--map-tokens`来控制仓库映射的大小 |
- 运行`aider --model claude-sonnet-20250514`以获得最佳代码质量

### Claude Code

| 功能 | 高级技巧 |
|---|---|
| **全功能AI助手** | 可以读取文件、编写代码、运行测试、执行Git操作 |
| **CLAUDE.md** | 项目指令文件，会自动加载 |
| **子助手** | 为复杂任务生成并行工作线程 |
| **内存管理** | 会话间数据持久化 |

**Claude Code的高级使用技巧：**
- 先编写详细的CLAUDE.md文件——这是最大的优势 |
- 对于复杂任务，先使用“规划模式”，然后再使用“执行模式” |
- 让AI运行测试并自动修正错误——不要中断这个过程 |
- 当上下文过长时，使用`/compact`命令

---

## 第七阶段：代码质量保障

### “信任但验证”检查清单

在每次AI生成代码更改后：

- [ ] **仔细阅读每一行**——不要盲目接受。AI可能会生成看似合理的代码 |
- [ ] **检查导入语句**——AI可能会导入不存在的模块或使用错误的版本 |
- [ ] **验证函数签名**——参数名称、类型、返回类型是否正确 |
- [ ] **测试边缘情况**——AI可能针对最佳情况进行优化 |
- [ ] **检查安全性**——是否存在硬编码的秘密信息、缺少授权检查、SQL注入等问题 |
- [ ] **运行测试**——如果测试通过，则说明代码正确；如果不存在测试，则需要先编写测试 |
- [ ] **检查代码是否偏离了预期**——AI是否修改了你不要求它修改的文件 |
- [ ] **验证依赖关系**——AI是否添加了新的包？这些包是否真实存在？是否安全？

### 常见的AI编码问题

| 问题 | 检测方法 | 解决方法 |
|---|---|---|
| AI生成的错误代码 | 代码使用了不存在的函数 | 在接受代码前先查看库文档 |
| 使用过时的模式 | 使用了已被弃用的API（例如React的类组件） | 在上下文中指定所需的版本 |
| 缺少错误处理 | 仅针对最佳情况编写代码，没有异常处理机制 | 明确要求处理异常情况 |
| 安全漏洞 | 代码中包含硬编码的秘密信息、缺少授权检查、存在XSS漏洞 | 作为单独的步骤进行安全审查 |
| 过度设计 | 用20行的代码实现5个功能 | 要求最简单的解决方案 |
| 抽象过度 | 过早进行抽象 | 要求使用具体的实现方式 |
| 测试不全面 | 编写的测试无法覆盖所有情况 | 仔细检查测试用例 |

### 三步阅读审查流程

1. **快速浏览**——代码结构是否合理？使用的文件和方法是否正确？
2. **逻辑检查**——每个函数是否实现了预期的功能？边缘情况是否得到了处理？
3. **集成测试**——代码是否与其他代码库兼容？是否会导致系统崩溃？

---

## 第八阶段：成本优化

### 每百万个提示词的成本

| 模型 | 每百万个提示词的成本 | 每百万个输出代码的成本 | 最适合的任务类型 |
|---|---|---|---|
| GPT-4o mini | 0.15美元 | 0.60美元 | 适用于简单的代码补全和格式化 |
| Claude Haiku | 0.25美元 | 1.25美元 | 适用于快速编辑和简单问题 |
| GPT-4o | 2.50美元 | 10.00美元 | 适用于复杂代码的生成 |
| Claude Sonnet | 3.00美元 | 15.00美元 | 适用于复杂的代码和长上下文 |
| Claude Opus | 15.00美元 | 75.00美元 | 适用于复杂的代码和高级任务 |
| o3 | 10.00美元 | 40.00美元 | 适用于需要复杂推理的任务 |

### 成本优化策略

1. **分层使用**——简单任务使用成本较低的模型；复杂任务使用成本较高的模型 |
2. **减少上下文信息**——不必要的文件会增加成本 |
3. **开启新的聊天对话**——长时间的对话会积累大量的历史数据 |
4. **简单任务使用自动完成功能**——Copilot采用固定费用模式，每次使用成本较低 |
5. **缓存项目上下文**——使用规则文件，避免重复解释上下文 |
6. **批量处理相关任务**——将相关的更改集中在一次聊天中处理 |

### 每月成本基准（全职开发者）

| 使用频率 | 预计每月成本 |
|---|---|
| 轻量级使用（主要使用Copilot，偶尔使用聊天功能） | 20-40美元 |
| 中等频率使用（主要使用Cursor，并每天进行聊天） | 40-80美元 |
| 高频率使用（依赖AI工具，处理复杂任务） | 80-200美元 |
| 高级用户（全天使用自主AI工具） | 200-500美元以上 |

---

## 第九阶段：团队采用AI编码工具

### 在团队中推广AI编码工具

**第1-2周：基础阶段**
- 选择主要使用的工具（推荐使用Cursor或Windsurf）
- 将.curserrules文件/windsurfrules文件提交到仓库 |
- 举办1小时的研讨会：介绍基础知识和提示技巧，以及如何进行代码验证 |
- 制定团队使用指南（包括审查要求和安全规范）

**第3-4周：实践阶段**
- 每天进行15分钟的“AI辅助开发成果”分享会议 |
- 组织结对编程练习 |
- 收集常见的提示语句，建立团队提示库 |
- 监控并解决使用过程中遇到的问题（如代码质量、依赖关系等问题）

**第2个月：优化阶段**
- 测量代码提交所需的时间、每个功能的错误数量、开发者的满意度 |
- 根据团队反馈调整.curserrules文件的内容 |
- 在共享文档中创建特定任务的提示模板 |
- 分析团队成员的使用情况，找出需要帮助的成员

**第3个月：系统化阶段**
- 将AI辅助的代码审查纳入持续集成流程 |
- 为新功能自动生成测试用例 |
- 为团队工作流程定制命令或脚本 |
- 每季度进行评估：分析投资回报率、代码质量等指标，并更新工具配置

### 团队使用指南模板

```markdown
# AI Coding Guidelines — [Team Name]

## Approved Tools
- [Tool 1] for [use case]
- [Tool 2] for [use case]

## Rules
1. AI-generated code gets the SAME review rigor as human code
2. Never paste proprietary/customer data into AI tools without approved data handling
3. All AI-generated tests must be reviewed for assertion quality
4. Security-sensitive code (auth, payments, PII) requires human-first approach
5. Commit messages should NOT mention AI — own the code you commit

## Quality Gates
- [ ] Typecheck passes (`tsc --noEmit --strict`)
- [ ] All tests pass
- [ ] No new warnings
- [ ] Manual review of all AI-generated code
- [ ] Security-sensitive areas reviewed by security champion
```

---

## 第十阶段：高级开发模式

### 多个AI助手的协同开发

```
Task: Build feature X

Agent 1 (Architect): Plans the approach, defines interfaces
Agent 2 (Implementer): Writes the code
Agent 3 (Tester): Writes and runs tests
Agent 4 (Reviewer): Reviews for quality, security, patterns

Orchestrator: Coordinates, resolves conflicts, maintains context
```

### 自动修复的开发循环

```
1. Agent writes code
2. Agent runs tests
3. Tests fail → agent reads error, fixes code
4. Repeat until tests pass
5. Agent runs linter
6. Lint fails → agent fixes
7. All green → create PR
```

### 提示库的维护

在项目中维护一个`prompts/`目录：

```
prompts/
  feature-implementation.md
  bug-fix.md
  refactoring.md
  code-review.md
  test-generation.md
  migration.md
  documentation.md
```

每个文件都是一个可复用的提示模板。使用时可以参考：“按照prompts/feature-implementation.md文件中的模板进行操作”。

### 模型选择策略

```yaml
task_routing:
  autocomplete: copilot  # Always-on, flat rate
  simple_edit: haiku     # Quick, cheap
  feature_impl: sonnet   # Good balance
  architecture: opus     # When it matters
  debugging: sonnet      # Needs to reason about code
  documentation: haiku   # Simple transformation
  security_review: opus  # Can't afford mistakes
  test_generation: sonnet # Needs understanding of code logic
```

---

## 第十一阶段：避免常见的错误做法

| 错误做法 | 为什么会导致问题 | 应该怎么做 |
|---|---|---|
| **仅依赖提示而不进行验证** | 不进行验证会导致生产环境中的错误 | 必须始终进行审查和测试 |
| **粘贴整个代码库** | 会导致上下文信息过载，增加成本 | 只选择相关的文件 |
| **从不开启新的聊天对话** | 旧的上下文会导致错误 | 新的任务应该开启新的聊天对话 |
| **不阅读AI生成的代码就直接信任它** | AI生成的代码也可能有错误 | 必须仔细阅读每一行代码 |
| **因为代码是由AI生成的就跳过测试** | AI生成的代码也可能有错误 | 应该对AI生成的代码进行更多的测试 |
| **对所有任务都使用同一个模型** | 在简单任务上浪费资源 | 根据任务的复杂性选择合适的模型 |
| **不制定项目规则文件** | AI无法理解你的使用习惯 | 必须创建.curserrules文件/CLAUDE.md文件 |
| **提示语句模糊不清** | 会导致错误的输出 | 使用SPEC框架来确保提示的准确性 |
| **过度依赖AI** | 会削弱自己的开发能力，无法调试AI生成的代码 | 必须了解AI的工作原理 |
| **忽视安全性** | AI可能忽略安全问题 | 必须进行专门的安全性审查 |

## 第十二阶段：持续改进

### AI辅助开发的质量评估（0-100分）

| 维度 | 权重 | 评估标准 |
|---|---|---|
| 上下文工程 | 20% | 规则文件、精选的上下文、新鲜的聊天记录 |
| 提示质量 | 15% | 使用SPEC框架，提供适合任务的提示模板 |
| 验证流程 | 20% | 严格的审查流程、测试覆盖范围、安全审查 |
| 工具选择 | 10% | 为每个任务选择合适的工具，合理分配模型 |
| 成本效率 | 10% | 分层使用工具、有效的上下文管理、批量处理任务 |
| 输出质量 | 15% | 代码的正确性、可维护性、代码的稳定性 |
| 工作流程整合 | 10% | 系统化的开发流程、团队之间的协作 |

### 每周自我评估问题

1. 这周我使用AI辅助完成的最佳成果是什么？是什么让这个成果变得出色？
2. AI在哪里浪费了我的时间？上下文或提示语句在哪里出了问题？
3. 我的审查是否足够细致？还是只是走形式？
4. 哪些提示模板使用效果良好？可以将它们添加到提示库中？
5. 我是否过度依赖AI来完成那些我本应该自己理解的任务？

### 每月评估指标

- **效率提升**：使用AI辅助后每天完成的任务数量与使用AI之前的对比 |
- **错误率**：AI辅助生成的代码与手动编写代码的错误率对比 |
- **成本效率**：每个功能的开发成本 |
- **上下文效率**：每次聊天对话的平均长度 |
- **代码覆盖率**：项目中有多少代码使用了AI辅助进行测试 |

---

## 快速参考：常用的语法命令

1. `“为[项目]设置AI编码环境”**——生成规则文件和工具推荐 |
2. `“为[任务类型]生成提示语句”**——生成符合SPEC框架的提示模板 |
3. `“审查这个AI生成的代码”**——执行“信任但验证”检查清单 |
4. `“比较[工具A]和[工具B]在[使用场景]下的表现”**——分析不同工具的适用性 |
5. **优化我的AI编码成本**——分析使用情况并推荐合适的模型 |
6. **为团队生成AI编码指南**——制定团队使用指南 |
7. **调试AI为何总是出错”**——诊断上下文问题 |
8. **为[功能]设置测试驱动的开发流程**——指导如何使用TDD-AI模式 |
9. **为[项目类型]生成提示库**——创建相应的提示模板 |
10. **评估我的AI编码水平**——运行质量评估 |
11. **帮助[某人]掌握AI编码**——制定培训计划 |
12. **审核AI编码的安全性**——进行安全审查 |

---

---

（由于文件内容较长，上述翻译仅包含了SKILL.md文件的主要部分。如果需要完整翻译，请提供完整的文件内容。）