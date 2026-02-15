---
name: ralph-mode
description: **具有迭代、回压机制和完成标准的自主开发循环**  
适用于需要多次迭代、测试验证以及结构化进度跟踪的持续编码工作场景。支持 Next.js、Python、FastAPI 等技术框架，并结合 Ralph Wiggum 方法论进行开发，该方法论已针对 OpenClaw 进行了优化。
---

# Ralph模式 - 自主开发循环

Ralph模式采用了Ralph Wiggum的技术，并将其适配到OpenClaw环境中：通过连续迭代、背压机制、完成标准以及结构化规划来实现任务的自主完成。

## 适用场景

在以下情况下使用Ralph模式：
- 开发需要多次迭代和优化的功能时；
- 处理具有可验证验收标准的复杂项目时；
- 需要自动化测试、代码检查或类型检查时；
- 希望系统地跟踪多次迭代的进展时；
- 更倾向于使用自主循环而非手动逐步指导时。

## 核心原则

### 三阶段工作流程

**阶段1：需求定义**
- 在`specs/`目录下为每个相关主题创建一个文档文件来记录需求规格；
- 定义可观察、可验证的验收标准；
- 制定包含优先级任务的实施计划。

**阶段2：规划**
- 进行差距分析：将需求规格与现有代码进行对比；
- 生成包含优先级任务的`IMPLEMENTATION_PLAN.md`文件；
- 此阶段不进行代码实现。

**阶段3：构建（迭代）**
- 每次迭代从计划中选择一个任务；
- 实现任务，进行验证，更新计划，然后提交代码；
- 重复此过程，直到所有任务完成或满足所有验收标准。

### 背压机制

通过验证机制自动拒绝未完成的工作：

**程序化检查（必须使用）：**
- 测试：`[test command]` - 提交前必须通过测试；
- 类型检查：`[typecheck command]` - 及时发现类型错误；
- 代码检查：`[lint command]` - 确保代码质量；
- 构建：`[build command]` - 验证代码集成是否正确。

**主观性检查（用于用户体验、设计、质量）：**
- 使用大语言模型（LLM）进行评审，评估代码的语气、美观性和可用性；
- 采用二进制通过/失败的标准，通过迭代逐步完善；
- 仅在程序化检查可靠运行后添加这些检查。

### 上下文效率

- 每次迭代只处理一个任务，以确保每次都有新的上下文；
- 为探索任务创建子代理，而不是处理主任务；
- 使用精简的提示信息，以提高效率（使用率约为40-60%）；
- 计划是可重用的，可以轻松生成新的计划。

## 文件结构

每个Ralph模式项目都应遵循以下文件结构：

```
project-root/
├── IMPLEMENTATION_PLAN.md     # Shared state, updated each iteration
├── AGENTS.md                  # Build/test/lint commands (~60 lines)
├── specs/                     # Requirements (one file per topic)
│   ├── topic-a.md
│   └── topic-b.md
├── src/                        # Application code
└── src/lib/                    # Shared utilities
```

### IMPLEMENTATION_PLAN.md

优先级任务列表——唯一的权威信息来源。格式如下：

```markdown
# Implementation Plan

## In Progress
- [ ] Task name (iteration N)
  - Notes: discoveries, bugs, blockers

## Completed
- [x] Task name (iteration N)

## Backlog
- [ ] Future task
```

### 主题范围测试

能否用一句话描述这个主题（不要使用“和”）？
- ✅ “使用JWT和会话管理进行用户认证”
- ❌ “认证、个人资料和计费” → 这三个主题属于不同领域

### AGENTS.md - 操作指南

简短的项目运行指南，内容不超过60行：

```markdown
# Project Operations

## Build Commands
npm run dev      # Development server
npm run build     # Production build

## Validation
npm run test      # All tests
npm run lint      # ESLint
npm run typecheck  # TypeScript
npm run e2e       # E2E tests

## Operational Notes
- Tests must pass before committing
- Typecheck failures block commits
- Use existing utilities from src/lib over ad-hoc copies
```

## 角色（Personas）

不同任务需要不同的专门角色：

**角色：架构师（@architect）**
- 负责高级设计、数据建模和API契约；
- 关注点：设计模式、可扩展性和可维护性。

**角色：实现者（@implementer）**
- 编写代码、实现功能、修复错误；
- 关注点：代码的正确性、性能和测试覆盖率。

**角色：测试者（@tester）**
- 负责编写测试用例、进行验证和边缘情况测试；
- 关注点：测试覆盖率、可靠性和可复现性。

**角色：评审者（@reviewer）**
- 负责代码评审、提供Pull Request反馈和进行质量评估；
- 关注点：代码风格、可读性和是否符合需求规格。

**使用方法：**
```
"Spawn a sub-agent with @architect hat to design the data model"
```

## 循环机制

### 外层循环（你负责协调）

作为主要代理，你的工作是：
- 设置环境，观察进程，并在必要时进行调整；
- 不要将任务直接分配给主任务处理流程；
- 让大语言模型（LLM）自主识别和调整任务；
- 使用沙箱环境作为安全边界；
- 计划是可以重用的，如果出现问题可以重新生成；
- 不要过度干预，只需观察循环的进行。

### 内层循环（子代理执行）

每个子代理的迭代步骤如下：
- 阅读计划、需求规格和相关代码；
- 选择最重要的未完成任务；
- 实现任务；
- 运行测试、进行代码检查和类型检查；
- 标记任务完成状态，记录发现的问题，并提交代码；
- 完成后进入下一次迭代。

### 停止条件

当满足以下条件时，循环结束：
- 所有`IMPLEMENTATION_PLAN.md`中的任务都已完成；
- 所有验收标准都已满足；
- 所有测试都通过，且没有阻塞问题；
- 达到最大迭代次数（可配置）；
- 手动停止循环（使用Ctrl+C）。

## 完成标准

提前明确成功标准，避免“看起来完成了”这种模糊的情况。

### 程序化标准（可量化）
- 所有测试都通过：`[test_command]`的返回值为0；
- 类型检查通过：没有TypeScript错误；
- 构建成功：生成了生产版本；
- 测试覆盖率达到指定阈值（例如80%以上）。

### 主观性标准（使用LLM进行评估）

对于难以自动化的质量标准，可以使用大语言模型进行二进制通过/失败的评估：

```markdown
## Completion Check - UX Quality
Criteria: Navigation is intuitive, primary actions are discoverable
Test: User can complete core flow without confusion

## Completion Check - Design Quality
Criteria: Visual hierarchy is clear, brand consistency maintained
Test: Layout follows established patterns
```

使用大语言模型作为评审工具，对代码进行二进制通过/失败的评估。

## 技术特定模式

### Next.js全栈开发

```
specs/
├── authentication.md
├── database.md
└── api-routes.md

src/
├── app/                    # App Router
├── components/              # React components
├── lib/                    # Utilities (db, auth, helpers)
└── types/                   # TypeScript types

AGENTS.md:
  Build: npm run dev
  Test: npm run test
  Typecheck: npx tsc --noEmit
  Lint: npm run lint
```

### Python（脚本/Notebook/FastAPI）

```
specs/
├── data-pipeline.md
├── model-training.md
└── api-endpoints.md

src/
├── pipeline.py
├── models/
├── api/
└── tests/

AGENTS.md:
  Build: python -m src.main
  Test: pytest
  Typecheck: mypy src/
  Lint: ruff check src/
```

### GPU相关工作负载

```
specs/
├── model-architecture.md
├── training-data.md
└── inference-pipeline.md

src/
├── models/
├── training/
├── inference/
└── utils/

AGENTS.md:
  Train: python train.py
  Test: pytest tests/
  Lint: ruff check src/
  GPU Check: nvidia-smi
```

## 快速启动命令

启动Ralph模式会话的命令如下：

```
"Start Ralph Mode for my project at ~/projects/my-app. I want to implement user authentication with JWT.
```

我将执行以下操作：
1. 创建包含优先级任务的`IMPLEMENTATION_PLAN.md`文件；
2. 创建子代理进行迭代实现；
3. 应用背压机制（测试、代码检查、类型检查）；
4. 跟踪进度并宣布任务完成。

## 运营经验总结

当发现Ralph模式中的问题时，及时更新`AGENTS.md`文件：

```markdown
## Discovered Patterns

- When adding API routes, also add to OpenAPI spec
- Use existing db utilities from src/lib/db over direct calls
- Test files must be co-located with implementation
```

## 应急措施

当开发流程出现问题时，可以采取以下措施：
- **立即停止循环**（使用Ctrl+C）；
- **重新生成计划**（丢弃`IMPLEMENTATION_PLAN.md并重新规划）；
- **重置**（使用Git恢复到上次成功的状态）；
- **缩小范围**（为特定任务创建更详细的计划）。

## 高级技巧：使用LLM作为评审工具

对于需要主观判断的质量标准（如代码的语气、美观性和用户体验），可以创建`src/lib/llm-review.ts`文件：

```typescript
interface ReviewResult {
  pass: boolean;
  feedback?: string;
}

async function createReview(config: {
  criteria: string;
  artifact: string; // text or screenshot path
}): Promise<ReviewResult>;
```

子代理可以使用这个文件来进行二进制通过/失败的评估。

## 关键运营要求

根据实际使用经验，必须遵循以下最佳实践以避免潜在问题：

### 1. 进度记录

**Ralph每次迭代后都必须更新PROGRESS.md文件。**这是强制性的。

在项目根目录下创建`PROGRESS.md`文件：

```markdown
# Ralph: [Task Name]

## Iteration [N] - [Timestamp]

### Status
- [ ] In Progress | [ ] Blocked | [ ] Complete

### What Was Done
- [Item 1]
- [Item 2]

### Blockers
- None | [Description]

### Next Step
[Specific next task from IMPLEMENTATION_PLAN.md]

### Files Changed
- `path/to/file.ts` - [brief description]
```

**原因：**外部观察者（父代理、定时任务、人类操作者）可以通过这个文件直接了解项目进度，而无需遍历目录或从会话日志中推断状态。

### 2. 会话隔离与清理

在启动新的Ralph会话之前：
- 检查是否存在现有的Ralph子代理；
- 结束或验证之前的会话是否已完成；
- 确保不会在同一代码库上同时启动多个Ralph会话。

**反模式示例：**如果在Ralph v1仍在运行时启动Ralph v2，可能会导致文件冲突、竞态条件或数据丢失。

### 3. 明确的路径验证

每次迭代开始时，都必须验证路径的正确性：

```typescript
// Verify current working directory
const cwd = process.cwd();
console.log(`Working in: ${cwd}`);

// Verify expected paths exist
if (!fs.existsSync('./src/app')) {
  console.error('Expected ./src/app, found:', fs.readdirSync('.'));
  // Adapt or fail explicitly
}
```

**原因：**不同的上下文可能会导致Ralph从不同的目录中启动。

### 4. 完成信号机制

任务完成后，Ralph必须：
- 编写最终的`PROGRESS.md文件，其中包含“## 状态：已完成”的提示；
- 列出所有创建或修改的文件；
- 清晰地结束会话（确保没有挂起的进程）。

**示例PROGRESS.md文件内容：**
```markdown
# Ralph: Influencer Detail Page

## Status: COMPLETE ✅

**Finished:** [ISO timestamp]

### Final Verification
- [x] TypeScript: Pass
- [x] Tests: Pass  
- [x] Build: Pass

### Files Created
- `src/app/feature/page.tsx`
- `src/app/api/feature/route.ts`

### Testing Instructions
1. Run: `npm run dev`
2. Visit: `http://localhost:3000/feature`
3. Verify: [specific checks]
```

### 5. 错误处理

如果Ralph遇到无法恢复的错误：
- 在`PROGRESS.md`文件中记录错误信息，注明错误原因；
- 列出尝试的解决方法；
- 清晰地结束会话（避免程序无响应地挂起）。

**注意：**如果Ralph在没有任何进度记录的情况下停止迭代，那么它与仍在运行的Ralph是无法区分的。

### 6. 迭代时间限制

设置明确的迭代超时时间：

```markdown
## Operational Parameters
- Max iteration time: 10 minutes
- Total session timeout: 60 minutes
- If iteration exceeds limit: Log blocker, exit
```

**原因：**这样可以防止任务陷入无限循环，允许父代理及时干预。

## 内存更新

每次Ralph模式会话结束后，都需要记录相关内存使用情况：

```markdown
## [Date] Ralph Mode Session

**Project:** [project-name]
**Duration:** [iterations]
**Outcome:** success / partial / blocked
**Learnings:**
- What worked well
- What needs adjustment
- Patterns to add to AGENTS.md
```

## 附录：常见错误及解决方法

以下是一些常见的错误及其解决方法：

| 错误类型 | 后果 | 预防措施 |
|--------------|-------------|------------|
| 未记录进度 | 父代理无法判断任务状态 | 必须记录进度信息 |
| 无声失败 | 会导致工作丢失和时间浪费 | 必须记录错误信息 |
| 会话重叠 | 会导致文件冲突和状态混乱 | 启动新会话前必须检查并清理旧会话 |
| 路径错误 | 可能导致使用错误的目录或文件 | 必须明确验证路径 |
| 无完成信号 | 父代理会无限等待 | 必须设置完成状态信号 |
| 迭代无限进行 | 资源浪费且无法取得进展 | 设置迭代超时时间 |

## 新最佳实践（2025-02-07）

### 问题：子代理被创建但无法执行

**问题表现：**会话日志为空（仅2字节），没有工具调用记录，也没有使用任何令牌。

**根本原因：**
1. **指令过于复杂**：导致子代理无法正确初始化；
2. **缺乏明确的执行触发条件**：子代理不知道何时开始执行；
3. **分支逻辑混乱**：复杂的条件判断导致任务选择困难；
4. **涉及多个文件**：子代理不知道从哪个文件开始执行。

**解决方法：简化Ralph任务模板**

```markdown
## Task: [ONE specific thing]

**File:** exact/path/to/file.ts
**What:** Exact description of change
**Validate:** Exact command to run
**Then:** Update PROGRESS.md and exit

## Rules
1. Do NOT look at other files
2. Do NOT "check first"
3. Make the change, validate, exit
```

### 问题前的情况（导致任务无法执行）：
```
Fix all TypeScript errors across these files:
- lib/db.ts has 2 errors
- lib/proposal-service.ts has 5 errors
- route.ts has errors
Check which ones to fix first, then...
```

### 问题解决后的情况（可以正常执行）：
```
Fix lib/db.ts line 27:
Change: PoolClient to pg.PoolClient
Validate: npm run typecheck
Exit immediately after
```

### 关键点：每次迭代只处理一个文件

**规则：**每次迭代只处理一个文件，完成一个修改后退出。

### 更新PROGRESS.md文件

**强制要求：**每次迭代后都必须更新`PROGRESS.md文件，以确保状态信息的准确性。

**原因：**定时任务会读取`PROGRESS.md文件来获取更新后的状态。如果文件未更新，状态信息可能会显得过时或重复。

### 调试Ralph循环停滞的问题

如果Ralph循环停滞，可以按照以下步骤进行调试：
1. 检查会话日志（应在60秒内显示工具调用记录）；
- 如果日志为空，说明指令过于复杂；
- 将指令简化为只处理一个文件、一个修改内容；
- 设置更短的超时时间（例如300秒，而不是600秒）。

### 解决状态信息过时的问题

如果定时任务反复报告相同的状态，可以检查以下内容：
1. 确认`PROGRESS.md文件是否被子代理更新过；
- 如果未更新，可能是子代理忽略了更新步骤；
- 在提示信息中添加“必须更新PROGRESS.md文件”的要求；
- 手动更新`PROGRESS.md文件，以反映实际的状态。

## 总结

Ralph模式在以下情况下效果最佳：**专注于处理单个文件、明确修改内容、执行验证操作并最终退出**；
当遇到复杂决策、多个文件或条件逻辑时，Ralph模式可能会陷入停滞。