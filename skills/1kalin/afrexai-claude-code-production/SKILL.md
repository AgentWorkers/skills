---
name: afrexai-claude-code-production
version: "1.0.0"
description: "完整的Claude代码生产力系统——包括项目设置、提示模式、子代理协调、上下文管理、调试、重构、测试驱动开发（TDD）等功能，让开发效率提升10倍。完全无需编写任何脚本。"
author: "AfrexAI"
license: "MIT"
metadata: {"openclaw":{"emoji":"⚡"}}
---
# Claude代码生产工程

这是一套完整的开发方法论，用于利用Claude Code以10倍的速度交付生产代码。这里讨论的不仅仅是安装脚本，还包括实际的工作流程和技术技巧，这些都能显著提升你的开发效率。

---

## 快速健康检查（每次会话前进行）

| 信号 | 是否正常 | 需要修复 |
|--------|---------|-----|
| 项目根目录下存在CLAUDE.md | ✅ | 创建一个（见§1） |
| .claueignore配置正确 | ✅ | 添加需要忽略的目录 |
| 会话上下文使用量低于60% | ✅ | 使用`/compact`命令或重新开始会话 |
| 在提示信息出现前清理任务范围 | ✅ | 先编写任务概述 |
| 目标代码有对应的测试 | ✅ | 先编写测试（见§7） |
| 在进行重大修改前执行Git清理 | ✅ | 提交或暂存更改 |
| 使用子代理进行并行工作 | ✅ | 使用`/new`命令或Task工具 |
| 验证输出结果，而不是盲目信任 | ✅ | 始终审查代码差异 |

得分：/8。得分低于6表示会话效率低下且容易出错。在开始编码前先进行修复。

---

## 1. 项目设置 — CLAUDE.md架构

CLAUDE.md是你的项目“大脑”。Claude会在会话开始时读取它。一个编写良好的CLAUDE.md每次会话可以节省数千个开发令牌。

### 模板

```markdown
# Project: [name]

## Tech Stack
- Language: TypeScript (strict mode)
- Framework: Next.js 15 App Router
- Database: PostgreSQL via Drizzle ORM
- Testing: Vitest + Playwright
- Styling: Tailwind CSS v4

## Architecture Rules
- Max 50 lines per function, 300 lines per file
- One responsibility per file
- All exports typed — no `any`
- Errors as values (Result type), not thrown exceptions
- Database: migrations via `drizzle-kit generate` then `drizzle-kit push`

## File Structure
src/
  app/         → Next.js routes (thin — call services)
  lib/         → Business logic (pure functions)
  db/          → Schema, migrations, queries
  components/  → UI (server components default, 'use client' only when needed)
  types/       → Shared type definitions

## Commands
- `pnpm dev` — start dev server
- `pnpm test` — run vitest
- `pnpm test:e2e` — run playwright
- `pnpm lint` — eslint + tsc --noEmit
- `pnpm db:generate` — generate migration
- `pnpm db:push` — apply migration

## Conventions
- Imports: absolute from `@/` (mapped to `src/`)
- Naming: camelCase functions, PascalCase components/types, SCREAMING_SNAKE constants
- Commits: conventional commits (feat:, fix:, refactor:, test:, docs:)
- PRs: always create branch, never commit to main directly
```

### CLAUDE.md规则

1. **具体明确** — 例如写“TypeScript strict”而不是“使用类型”。要指定版本号，而不仅仅是名称。
2. **包含命令** — Claude需要知道如何执行操作。提供具体的命令，而不仅仅是描述。
3. **记录架构决策** — 不仅要说明“做什么”，还要说明“为什么这样做”。例如：“将错误作为结果类型处理”可以告诉Claude代码的编写模式。
4. **保持200行以内** — CLAUDE.md每次会话都会被读取。冗长的内容会浪费开发令牌。
5. **模式发生变化时及时更新** — 过时的CLAUDE.md可能会导致Claude无法正确处理你的代码库。
6. **嵌套的CLAUDE.md** — 子目录也可以有自己的CLAUDE.md文件。适用于单仓库项目。

### .claueignore

```
node_modules/
.next/
dist/
coverage/
*.lock
.git/
*.min.js
*.map
public/assets/
```

规则：如果Claude不需要读取某个文件或目录，就将其忽略。大型锁定文件和构建产物会浪费会话上下文。

---

## 2. 提示信息模式 — 五个重要的模式

### 模式1：任务概述（适用于所有非简单任务）

```
Task: Add user authentication with magic links
Context: Using Resend for email, no password system exists yet
Constraints:
- Server actions only (no API routes)
- Session via httpOnly cookies
- Token expires in 15 minutes
Acceptance: User enters email → receives link → clicks → logged in → cookie set
Start with: the database schema for sessions and tokens
```

为什么有效：明确任务范围、约束条件、验收标准以及起点。这样Claude就不会偏离方向。

### 模式2：展示而非命令

错误示例：“让API更健壮”
正确示例：“为POST /api/users添加输入验证——验证电子邮件格式，名称长度在1-100个字符之间，拒绝多余的字段。如果字段有错误，返回422状态码，并附带错误信息：`{ errors: { field: string, message: string }[] }`”

规则：如果你无法描述输出的具体格式，说明你还没有想清楚要实现什么。

### 模式3：逐步优化

```
Step 1: "Create the database schema for a todo app with projects and tasks"
[review output]
Step 2: "Now add the CRUD service layer for tasks — pure functions, no framework imports"
[review output]
Step 3: "Now the API routes that call those services — input validation with zod"
```

原因：Claude通过逐步的提示生成更高质量的代码，而不是一次性给出所有要求。每一步都会建立可验证的上下文。

### 模式4：基于错误进行修复

错误示例：“代码出错了”
正确示例：“运行`pnpm test`后得到以下错误：
```
TypeError: Cannot read properties of undefined (reading 'id')
  at getUserById (src/lib/users.ts:23:15)
```
该函数期望接收一个User对象，但数据库查询没有返回任何结果时返回了`undefined`。添加空值检查，并返回一个Result类型的结果。”

规则：直接粘贴实际的错误信息。Claude在看到堆栈跟踪时能够更有效地修复错误。

### 模式5：架构讨论

```
I'm deciding between these approaches for real-time updates:
A) Server-Sent Events from Next.js API routes
B) WebSocket via separate service
C) Polling every 5 seconds

Context: 500 concurrent users, updates every 30 seconds on average, deployed on Vercel.

What are the tradeoffs? Recommend one with reasoning.
```

用于决策，而不是具体的实现细节。先得到答案，然后再使用任务概述来开始编码。

---

## 3. 上下文管理 — 提高效率的关键

### 上下文的重要性

| 上下文使用量百分比 | 应采取的行动 |
|-----------|--------|
| 0-30% | 可以进行复杂的工作。 |
| 30-60% | 继续当前任务。 |
| 60-80% | 上下文开始陈旧。完成当前单元测试后，使用`/compact`命令压缩代码。 |
| 80%以上 | 危险！立即使用`/compact`命令或重新开始会话。 |

### 何时重新开始会话（使用`/new`）

- 转换到不相关的任务 |
- 上下文使用量超过70% |
- Claude开始重复之前的操作或出现之前没有的错误 |
- 部署新功能后（为下一个功能创建新的上下文）

### 何时压缩代码（使用`/compact`）

- 在任务进行过程中，但上下文因探索而变得冗长 |
- 调试会话结束后（大量错误信息消耗了上下文） |
- 在进行复杂实现之前

### 提高上下文效率的习惯

1. **不要粘贴整个文件** — 通过文件路径引用文件内容。Claude可以直接读取。
2. **不要重复解释** — 如果信息已经在CLAUDE.md中，就不要在提示中再次说明。
3. **使用具体的文件路径** — 例如：“查看`src/lib/auth.ts`的第45行”，而不是“查看auth代码”。
4. **避免偏离主题** — 如果Claude陷入歧途，立即引导它回到正确的方向。不要让错误的输出影响上下文。
5. **每条消息只关注一个主题** — “修复auth错误、重构数据库层并添加测试”会导致上下文混乱。在一次会话中应该按顺序处理这些问题，而不是并行处理。

---

## 4. 子代理协调 — 并行提高效率

### 何时使用子代理

| 场景 | 使用的模式 |
|----------|---------|
| 独立的功能 | 为每个功能创建一个子代理 |
| 测试与实现 | 一个代理负责编写测试，另一个代理负责编写代码 |
| 研究与构建 | 子代理研究API文档，主代理负责构建 |
| 重构与维护 | 子代理负责重构模块A，主代理负责模块B |
| 代码审查 | 子代理用新的视角审查你的代码提交（PR）

### Task工具模式（Claude Code内置）

```
Use the Task tool to:
1. Research the Stripe API for subscription billing
2. Return: webhook event types we need, API calls for create/update/cancel, error codes to handle
```

Task工具会创建一个具有独立上下文的子代理。子代理完成工作后会返回总结结果。非常适合用于那些会占用主上下文的研究任务。

### 任务交接文档

当子代理完成复杂任务后，让它生成一个HANDOFF.md文件：

```markdown
## What Was Done
- Implemented Stripe webhook handler at src/app/api/webhooks/stripe/route.ts
- Added 4 event handlers: checkout.session.completed, invoice.paid, invoice.payment_failed, customer.subscription.deleted

## Key Decisions
- Used Stripe SDK v14 (not raw HTTP) for type safety
- Webhook signature verification via stripe.webhooks.constructEvent()
- Idempotency: check processed_events table before handling

## What's Next
- Wire up subscription status updates to user table
- Add retry logic for failed database writes
- E2E test with Stripe CLI: `stripe trigger checkout.session.completed`

## Gotchas
- Must use raw body (not parsed JSON) for signature verification
- Next.js App Router: export const runtime = 'nodejs' (not edge)
```

---

## 5. 调试工作流程 — 有条不紊，而不是随机尝试

### DEBUG协议

**D**描述问题症状（实际看到的情况与预期情况）
**E**错误输出（粘贴完整的堆栈跟踪）
**B**分析问题发生的时间和变化点**
**U**确定问题的根本原因（能否在测试中重现）
**G**生成可能的解决方案（让Claude给出3个可能的解决方案，并按优先级排序）

### 有效的错误提示

```
Bug: Users see stale data after updating their profile.

Expected: After PUT /api/profile, the profile page shows updated data.
Actual: Old data persists until hard refresh (Cmd+Shift+R).

Stack:
- Next.js 15 App Router
- Server component fetches user data
- Client component with form calls server action
- Server action calls db.update()

Hypothesis: Next.js is caching the server component fetch. Need to revalidate.

Can you confirm and show me the fix?
```

### 当Claude遇到困难时

1. **添加约束条件** — “修复方案不能改变API的契约”可以缩小搜索范围。
2. **分享你已经尝试的方法** — “我已经尝试了`revalidatePath('/profile')`，但没有成功，因为……”
3. **请求不同的解决方案** — “给我3种不同的解决方法，并说明各自的优缺点。”
4. **重新开始会话** — 有时当前的上下文已经混乱。从错误描述开始，重新开始会话。

---

## 6. 重构模式 — 安全地进行大规模代码修改

### 重构前的准备

```
Before we start refactoring:
1. Run the test suite and confirm it passes: `pnpm test`
2. Commit current state: `git add -A && git commit -m "chore: pre-refactor checkpoint"`
3. Create a branch: `git checkout -b refactor/[description]`
```

### 安全的重构提示

**提取函数：**
```
Extract the email validation logic from src/lib/users.ts (lines 34-67) into a separate
function `validateEmail` in src/lib/validation.ts. Update all imports. Run tests after.
```

**在整个代码库中重命名变量：**
```
Rename the `getUserData` function to `fetchUserProfile` across the entire codebase.
This includes: function definition, all call sites, all imports, all test references.
Run `pnpm test` and `pnpm lint` after to verify nothing broke.
```

**拆分大文件：**
```
src/lib/api.ts is 800 lines. Split it into:
- src/lib/api/users.ts (user-related functions)
- src/lib/api/projects.ts (project-related functions)
- src/lib/api/shared.ts (shared types and helpers)
- src/lib/api/index.ts (re-exports for backward compatibility)

Preserve all existing exports from the index file so no external imports break.
Run tests after each file move.
```

### 多文件重构规则

1. **一次只进行一种类型的修改** — 不要同时进行重命名、重构和优化。
2. **每一步都运行测试** — 及时发现错误，而不是等到修改了20个文件后再测试。
3. **保留导出功能** — 使用`index.ts`文件来重新导出模块，以避免影响其他代码。
4. **逐步提交** — 每个逻辑变更都单独提交，而不是一次性提交全部更改。

---

## 7. 使用Claude Code进行测试驱动开发

### TDD循环

```
Step 1: "Write a failing test for: creating a user with valid email stores them in the database"
Step 2: [verify test fails for the right reason]
Step 3: "Now write the minimum code to make this test pass"
Step 4: [verify test passes]
Step 5: "Refactor the implementation — the test must still pass"
```

### TDD为何与Claude配合得如此出色

- **测试是验收标准** — Claude能明确知道“完成”意味着什么。
- **即时验证** — 可以立即确认代码是否正常工作。
- **防止过度设计** — “最小化代码量”的原则可以防止过度优化。
- **防止回归** — 未来的修改不会破坏已有的功能。

### 先编写测试的提示

```
Write tests for a `calculateShipping` function that:
- Free shipping for orders over $100
- $5.99 flat rate for orders $50-$100
- $9.99 flat rate for orders under $50
- International orders: add $15 surcharge
- Express: 2x the base rate
- Edge cases: $0 order, negative amount (throw), exactly $50, exactly $100

Use vitest. Don't implement the function yet — just the tests.
```

之后再编写实现代码：“现在实现`calculateShipping`函数，使其通过所有测试。”

---

## 8. 使用Claude Code的Git工作流程

### 开始前的检查清单

```bash
git status          # Clean working tree?
git pull            # Up to date?
git checkout -b feat/[description]   # New branch
```

### 提交策略

| 任务范围 | 提交方式 |
|-------|---------------|
| 添加单个函数 | `feat: add calculateShipping function` |
| 修复错误 | `fix: handle null user in profile fetch` |
| 添加测试 | `test: add shipping calculation edge cases` |
| 重构（无行为变化） | `refactor: extract validation into shared module` |
| 多个相关变更 | 分别提交每个逻辑单元 |
| 大规模功能 | 在功能分支上多次提交，合并时合并这些变更 |

### 使用Claude Code时的Git提示

```
# After completing work:
"Commit the changes with an appropriate conventional commit message. 
Group related files into logical commits if there are multiple concerns."

# For PR creation:
"Create a PR description for these changes. Include:
- What changed and why
- How to test it
- Any migration steps needed
- Screenshots if UI changed"
```

---

## 9. 代码审查模式 — 使用Claude作为代码审查工具

### 审查提示模板

```
Review this code for:
1. Correctness — does it do what it claims?
2. Security — any injection, auth bypass, data leak risks?
3. Performance — N+1 queries, unnecessary re-renders, missing indexes?
4. Maintainability — clear naming, reasonable complexity, documented edge cases?
5. Testing — are the tests sufficient? Any missing cases?

Be specific. For each issue, cite the file:line and suggest a fix.
Skip style nits unless they affect readability.
```

### 提交代码前的自我审查

```
I'm about to open a PR. Review all changed files (`git diff main`) for:
- Any hardcoded secrets or credentials
- TODO/FIXME/HACK comments that should be resolved
- Console.logs that should be removed
- Missing error handling
- Type assertions (as any) that should be proper types
- Missing tests for new public functions
```

---

## 10. 部署前的检查清单

在部署Claude生成的代码之前，请确保满足以下要求：

### P0 — 必须完成

- 所有测试都通过 (`pnpm test && pnpm test:e2e`)
- 代码格式检查无误 (`pnpm lint`)
- 类型检查通过 (`tsc --noEmit`)
- 代码中不存在硬编码的敏感信息（检查API密钥、令牌、密码）
- 所有对外接口都有错误处理机制 (`DB、API、文件I/O`)
- 所有用户交互接口都有输入验证
- 数据库迁移已完成审查（确保没有数据丢失，且向后兼容）

### P1 — 建议完成

- 性能优化：避免使用N+1查询，列表长度有限制，有分页功能
- 日志记录规范（使用适当的日志级别，而不是简单的`console.log`)
- 新接口都有适当的授权机制
- 公共接口有速率限制
- 有回滚计划（知道如何在出现问题时恢复）

### P2 — 可选完成

- 在新接口上线前进行负载测试
- 新接口有监控警报机制
- 文档更新（API文档、README、CHANGELOG）
- 检查代码的可访问性（特别是用户界面）

---

## 11. 应避免的错误做法 — 它们会降低效率

| 错误做法 | 为什么不好 | 如何改进 |
|-------------|-------------|-----|
- 一次性完成整个应用程序的开发 | 会导致上下文混乱，质量低下 | 将开发任务分解为5-10个具体的小任务 |
- 不阅读代码就直接接受 | 会导致错误累积，技术债务增加 | 必须审查每一处代码变更，对不清楚的部分提出疑问 |
- 重复提出相同的问题，期望得到不同的结果 | 会浪费开发令牌和上下文资源 | 修改提示信息，添加更明确的约束条件，尝试不同的解决方法 |
- 忽视测试失败 | “大部分功能都能正常运行” → 可能会导致生产环境出现问题 | 立即修复测试问题，确保代码稳定后再继续下一步 |
- 从不使用`/compact`命令 | 会导致上下文混乱，Claude无法正确处理代码 | 每30-45分钟使用一次`/compact`命令压缩代码 |
- 一次性粘贴整个代码库 | 会导致上下文信息混乱 | 通过文件路径引用代码文件 |
- 将应该由人工决定的架构决策交给Claude来完成 | 这种做法会降低效率，应该与Claude讨论后自己做出决策 |
- 在任务之间不提交代码更改 | 无法回滚更改，也无法定位问题 | 每完成一个可执行的步骤就提交代码 |
- 使用模糊的提示语言 | 会导致代码修改混乱 | 提供具体的输入、输出和约束条件 |
- 反对Claude的建议 | 如果Claude的建议不同，也许它有道理 | 如果不同意Claude的建议，请说明你的理由并解释为什么你的方法更好 |

---

## 12. 提高效率的高级技巧

### 常用命令参考

| 命令 | 使用场景 |
|---------|------------|
| `/new` | 创建新任务，恢复干净的上下文 |
| `/compact` | 当上下文变得复杂时，压缩代码 |
| `/clear` | 彻底清除所有会话信息 |
| `/cost` | 查看当前会话消耗的开发令牌数量 |
| `/model` | 切换使用不同的Claude模型（Sonnet适用于快速开发，Opus适用于复杂任务） |
| `/vim` | 进入vim编辑模式 |

### 模型选择策略

| 任务类型 | 最适合的模型 | 原因 |
|-----------|-----------|-----|
| 简单的错误修复 | Sonnet | 快速、成本低、足够使用 |
| 新功能的实现 | Sonnet | 在速度和质量之间取得平衡 |
| 复杂的架构重构 | Opus | 需要深入分析，能提供更好的权衡建议 |
| 代码审查 | Opus | 能发现细微的问题 |
| 调试复杂逻辑 | Opus | 需要对代码状态进行深入分析 |

### 键盘快捷键

- `Esc` — 中断Claude的生成过程（如果方向错误）
- `Up arrow` — 编辑上一个提示信息（无需重新输入即可修正拼写错误）
- `Tab` — 接受文件编辑建议

### 大型功能的开发流程

- 终端1：主要负责代码实现（使用Claude Code）
- 终端2：为终端1生成的代码编写测试（使用`/new`命令）
- 终端3：手动进行测试或运行应用程序

---

## 13. 工作流程模板

### 新功能开发流程

```
1. "Create branch feat/[name]"
2. "Write failing tests for [feature spec]"
3. "Implement minimum code to pass tests"
4. "Refactor — tests must stay green"
5. "Run full test suite + lint + typecheck"
6. "Commit with conventional commit message"
7. "Self-review: check diff for security, performance, missing edge cases"
8. "Create PR with description"
```

### 错误修复流程

```
1. "Create branch fix/[description]"
2. "Write a test that reproduces this bug: [paste error]"
3. "Fix the bug — test must pass"
4. "Run full test suite to check for regressions"
5. "Commit: fix: [description of what was wrong]"
```

### 代码重构流程

```
1. "Create branch refactor/[description]"
2. "Run tests — confirm all green"
3. "Commit pre-refactor state"
4. "[Specific refactoring instruction]"
5. "Run tests — must still be green"
6. "Commit this step"
7. [Repeat 4-6 for each refactoring step]
```

### 突发问题/研究流程

```
1. "Use Task tool to research [topic]. Return: key findings, API surface, gotchas, recommended approach."
2. [Read Task output]
3. "Based on the research, build a minimal proof of concept in /tmp/spike-[name]/"
4. [Evaluate POC]
5. "Spike looks good. Now implement properly in the main codebase."
```

---

## 14. 提高效率的量化指标

每周跟踪以下指标：

| 指标 | 目标 | 测量方法 |
|--------|--------|----------------|
| 部署的功能数量 | 每周3-5个 | 通过Git提交标记为“feat:” |
| 引入的错误数量 | 每周少于1个 | 部署后的问题记录 |
| 测试覆盖率 | 保持稳定或上升 | 使用`/cost`命令查看 |
| 完成代码所需的时间 | 小于30分钟 | 从任务开始计时 |
| 每次会话中压缩的代码量 | 1-2次 | 统计`/compact`命令的使用次数 |

---

## 自然语言命令

| 命令 | 功能 |
|----------|----------|
| “为我的项目配置Claude Code” | 从你的代码仓库中生成CLAUDE.md和.clueignore文件 |
| “审查这段代码” | 对修改过的文件进行全面的代码审查 |
| “帮我调试这个错误” | 按照DEBUG协议进行调试 |
| “重构这个文件/模块” | 安全地进行重构，并进行测试验证 |
| “为这个函数编写测试” | 生成符合TDD规范的测试 |
| “部署这个功能” | 运行部署前的检查清单 |
| “开始一个新的任务” | 清理代码上下文并设置新的分支 |
| “我的效率如何？” | 查看Git日志并获取改进建议 |
| “优化我的CLAUDE.md配置” | 审查并优化项目配置 |
| “我应该为这个任务选择哪个模型？” | 根据任务类型推荐合适的模型 |
| “帮我处理这个代码提交（PR）” | 提供PR描述和自我审查 |
| “估算这个任务的耗时” | 将任务分解并估算每个步骤的耗时 |

---

*由[AfrexAI](https://afrexai-cto.github.io/context-packs/)开发——专为AI设计的业务工具。*