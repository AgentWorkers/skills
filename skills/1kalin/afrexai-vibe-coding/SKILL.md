---
name: Vibe Coding Mastery
slug: afrexai-vibe-coding
version: 1.0.0
description: 这是一个用于开发包含人工智能功能的软件的完整操作系统。它涵盖了从用户首次输入指令到软件最终部署的整个流程，包括指令提示框架、架构模式、测试策略、调试方法以及生产环境部署前的检查清单。该系统兼容 Claude Code、Cursor、Windsurf、Copilot 以及任何其他人工智能辅助编码工具。
metadata: {"openclaw":{"emoji":"🎸","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
# Vibe编码精通

这是一个从零开始到生产环境构建软件的完整系统，它不提供技巧或理论，而是一种完整的操作方法论。

**什么是Vibe编码？**这是一种编程方式：你描述你的需求，让AI生成代码。你通过结果来评估代码的质量，而不是通过逐行阅读代码。这个术语由Andrej Karpathy在2025年2月提出。

**关键区别（Simon Willison）：**如果你需要审查、测试和解释代码，那就是AI辅助的软件开发。而Vibe编码意味着在接受AI的输出时，不需要完全理解每一个函数。这项技能涵盖了这两种方式以及它们之间的所有中间状态。

---

## 第1阶段：何时使用Vibe编码（决策矩阵）

在开始之前，对你的项目进行分类：

| 因素 | 可以使用Vibe编码 ✅ | 不适合使用Vibe编码 ❌ |
|--------|---------|---------------|
| **风险** | 低（原型、内部开发、学习阶段） | 高（支付系统、认证、合规性要求） |
| **时间线** | 几小时到几天 | 几个月以上 |
| **团队规模** | 单人或两人合作 | 有明确标准的团队 |
| **领域知识** | 你熟悉该领域 | 不熟悉该领域 |
| **可逆性** | 容易修改 | 后期修改困难 |
| **数据敏感性** | 公共数据/测试数据 | 包含个人身份信息、财务数据、健康数据 |

**评分标准：** 根据✅的数量来评分。
- 5-6分：完全使用Vibe编码模式。可以快速发布产品。
- 3-4分：在使用Vibe编码的同时设置安全防护措施。需要审查关键路径。
- 1-2分：使用AI辅助开发，但需要全面审查代码。
- 0分：自己编写代码，或者雇佣熟悉该领域的人。

### Vibe编码成熟度等级

| 等级 | 描述 | 适用人群 |
|-------|-------------|-----|
| **L1 — 初学者** | 直接复制AI的输出，希望它能正常工作 |
| **L2 — 中级者** | 通过上下文引导AI，捕捉明显的错误 |
| **L3 — 有经验者** | 自己做出架构决策，AI负责实现代码，你负责审查 |
| **L4 — 高级用户** | 调度多个AI会话，同时进行多个开发任务 |

**目标：**任何要投入生产环境的项目至少应达到L3等级。

---

## 第2阶段：工具选择

### 主要工具矩阵

| 工具 | 适用场景 | 上下文窗口 | 支持多文件编辑 | 是否支持终端操作 | 成本 |
|------|----------|---------------|------------|----------|------|
| **Claude Code** | 全栈开发、复杂的代码重构、支持命令行接口 | 20万美元 | 优秀工具 | 原生集成 | 需要API调用 |
| **Cursor** | 集成在编辑器中，支持快速迭代 | 12.8万美元 | 合适工具 | 需要通过终端操作 | 每月20美元 + API费用 |
| **Windsurf** | 面向初学者，提供引导式的开发流程 | 12.8万美元 | 功能有限 | 需要通过终端操作 | 每月10美元 + API费用 |
| **GitHub Copilot** | 提供代码补全功能，适用于小规模编辑 | 8,000-32,000美元 | 功能有限 | 不支持终端操作 | 每月10-19美元 |
| **Aider** | 支持Git操作，开源工具，支持命令行接口 | 根据使用情况而定 | 合适工具 | 原生集成 | 仅支持API调用 |
| **Cline (VS Code)** | 与VS Code集成，支持规划模式 | 根据使用情况而定 | 合适工具 | 需要通过终端操作 | 仅支持API调用 |

### 多工具使用策略

- **架构与规划** → 使用Claude Code或Claude Chat（提供最完整的上下文和最佳推理能力）
- **实现阶段** → 使用Cursor或Claude Code（支持快速迭代和多文件编辑）
- **快速修复与代码补全** → 使用Copilot（提供即时代码补全功能）
- **代码审查** → 使用Claude Chat（可以粘贴代码差异并获取全面审查）

---

## 第3阶段：规则文件（你的持续工作基础）

规则文件可以一次性教会AI你的编码规范。如果没有这些文件，每次编码会从零开始。

### 通用规则文件模板

```markdown
# Project Rules

## Stack
- Language: [TypeScript/Python/Go/etc.]
- Framework: [Next.js/FastAPI/etc.]
- Database: [PostgreSQL/SQLite/etc.]
- Styling: [Tailwind/CSS Modules/etc.]
- Package manager: [pnpm/npm/poetry/etc.]

## Code Style
- Max function length: 50 lines
- Max file length: 300 lines
- One export per file (prefer)
- Use [const/let, never var] / [type hints always]
- Error handling: [explicit try/catch, never swallow errors]
- Naming: [camelCase functions, PascalCase components, UPPER_SNAKE constants]

## Architecture
- File structure: [describe or reference]
- API pattern: [REST/tRPC/GraphQL]
- State management: [Zustand/Redux/signals/etc.]
- Auth pattern: [JWT/session/OAuth provider]

## Testing
- Framework: [Vitest/Jest/Pytest/etc.]
- Minimum coverage: [80%/90%/etc.]
- Test file location: [co-located/__tests__/tests/]
- Run before committing: [command]

## Do NOT
- Do not use `any` type in TypeScript
- Do not install new dependencies without asking
- Do not modify database schema without migration
- Do not hardcode secrets, URLs, or config values
- Do not remove existing tests

## When Unsure
- Ask before making architectural decisions
- Show the plan before implementing changes >100 lines
- Flag security-adjacent code for manual review
```

### 规则文件的存放位置

| 工具 | 文件名 | 说明 |
|------|------|-------|
| Claude Code | 仓库根目录下的`CLAUDE.md` | 也支持读取`.claude/`目录下的文件 |
| Cursor | 仓库根目录下的`.cursor/rules/*.mdc` | 支持使用通配符来定义条件规则 |
| Windsurf | 仓库根目录下的`.windsurfrules` | 单个文件 |
| Aider | `*.aider.conf.yml`文件及聊天中的配置 | 使用YAML格式进行配置 |
| 通用规则文件 | `AGENTS.md`或`CONVENTIONS.md` | 可以告诉任何工具读取这些文件 |

### Cursor规则文件（.mdc格式）

```markdown
---
description: React component standards
globs: src/components/**/*.tsx
alwaysApply: false
---

# Component Rules
- Functional components only (no class components)
- Props interface above component, named [Component]Props
- Use forwardRef for components that accept ref
- Co-locate styles in [component].module.css
- Co-locate tests in [component].test.tsx
- Export component as named export, not default
```

### 规则文件的质量检查清单

- 是否指定了技术栈和版本信息
- 是否定义了文件/函数的代码长度限制
- 是否记录了命名规范
- 是否包含了常见的AI使用错误及避免方法
- 是否明确了测试要求
- 是否描述或引用了架构模式
- 是否标出了敏感区域
- 是否说明了依赖关系管理策略

---

## 第4阶段：编写清晰、有效的提示语

### 五级提示语质量层次

**第1级 — 简单请求（质量较低）**
> “构建一个待办事项应用程序”

**第2级 — 明确要求（尚可）**
> “使用React和Tailwind框架构建一个待办事项应用程序”

**第3级 — 详细规范（质量较高）**
> “构建一个待办事项应用程序：使用React 18、TypeScript和Tailwind。功能包括：添加/编辑/删除/切换待办事项。数据存储在localStorage中。页面响应式设计。代码总行数不超过200行。”

**第4级 — 简洁明了（质量优秀）**
> “构建一个待办事项应用程序。以下是具体要求：
> - 技术栈：React 18 + TypeScript + Tailwind
- 功能：添加/编辑/删除/切换待办事项；数据存储在localStorage中
- 限制条件：单个组件文件；代码总行数不超过200行；不依赖外部库
- 完成标准：所有功能都能正常工作；页面刷新后状态保持不变；支持移动设备响应式设计”
- 具体步骤：先定义数据类型，然后再逐步实现功能”

**第5级 — 详细合同（适用于生产环境）**
```yaml
task: Todo application
stack:
  runtime: React 18 + TypeScript strict
  styling: Tailwind CSS 3.x
  build: Vite 5
  test: Vitest + Testing Library
features:
  - CRUD operations on todos
  - Toggle completion status
  - Filter: all | active | completed
  - Bulk actions: complete all, clear completed
  - Persist to localStorage with versioned schema
constraints:
  - Max 3 component files
  - Max 200 lines per file
  - No external state management library
  - Keyboard accessible (tab, enter, escape)
  - Mobile responsive (min 320px)
acceptance:
  - All features functional
  - Page refresh preserves state
  - 90%+ test coverage
  - No TypeScript errors (strict mode)
  - Lighthouse accessibility score > 90
approach: Start with types/interfaces, then hooks, then components, then tests.
```

### 12种经过验证的有效提示语模板

1. **搭建框架**：“使用空文件和类型定义来创建项目结构。暂时不需要实现具体功能。”
2. **逐步实现**：“只实现[特定功能]。不要修改其他文件。”
3. **先解释后实现**：“先描述你的架构设计，得到我的批准后再进行实现。”
4. **先测试后实现**：“根据这些要求编写测试用例，然后实现代码以通过测试。”
5. **重构**：“将[文件]重构为[目标状态]。保持原有功能不变。”
6. **调试**：“当[操作]发生错误时，[代码]会出现[问题]。相关代码位于[文件]中。”
7. **代码审查**：“审查这段代码的安全性/性能/可读性。具体说明问题及修复方法。”
8. **迁移**：“将[旧代码模式]转换为[新模式]。先展示迁移计划。”
9. **文档编写**：“为[文件]中的所有公共函数添加JSDoc文档。包括参数类型和示例。”
10. **优化**：“如果函数处理超过10,000条数据时性能较慢，进行性能分析，找出瓶颈并进行优化。保持API接口不变。”
11. **并行开发**：“阅读[这些文件]并总结代码架构。不要修改任何内容。”
12. **问题恢复**：“代码库出现故障。描述问题症状，帮助我找出问题根源。”

### 应避免的错误提示语模式

| 错误提示语模式 | 问题原因 | 解决方法 |
|-------------|-------------|-----|
| “为我构建一个应用程序” | 提示过于模糊，AI无法准确理解需求 | 使用更详细的第4级及以上级别的提示语 |
| “修复它”（没有提供上下文） | AI无法知道“它”指的是什么 | 提供错误信息及预期的行为 |
| “全部重写” | 会破坏现有的代码，可能导致回归问题 | 应采用逐步重构的方法 |
| “让它变得更好” | 主观性较强，AI可能会做出随机修改 | 明确“更好”的具体含义 |
| “使用最佳实践” | AI的“最佳实践”可能与你的技术栈不匹配 | 明确你希望使用的实践方式 |
| 同时提出多个无关要求 | 会导致上下文混乱，实现不完整 | 每个提示语只针对一个具体任务 |
| 长篇大论的对话 | 多次对话后上下文会变得混乱 | 应重新开始新的编码会话 |

---

## 第5阶段：RPIV工作流程

**研究 → 规划 → 实现 → 验证**

### 第1步：研究
> “阅读[相关文件/文档/代码库]。解释[功能/模块]的工作原理。不要修改任何内容。”

**目的：**在出现问题之前先了解背景信息。如果AI的解释有误，那么实现的代码也会出错。

### 第2步：规划
> “根据你的理解，制定计划：
> 1. 需要创建/修改哪些文件
> 2. 每个文件中需要做哪些修改
> 3. 实现的顺序是什么
> 4. 可能会遇到哪些问题”

**目的：**在提交代码之前先审查计划。修改计划比修复已经产生的错误要节省大量时间。”

**计划审查清单：**
- 是否涉及不应该修改的文件？
- 修改顺序是否合理（先修改基础文件，再修改工具/组件/测试文件）？
- 是否遗漏了某些文件或步骤？
- 是否遵循了现有的代码规范？
- 是否发现了潜在的风险或未知问题？

### 第3步：实施
> “按照计划逐步实施代码。每完成一个文件后停下来让我进行验证。”

**200行规则：**如果某个实现步骤的代码量超过200行，应将其拆分成更小的部分。较大的修改容易导致错误。**

**检查点系统：**
- 每完成一个文件后：快速检查是否存在明显问题
- 每实现一个功能后：运行测试
- 每完成一个重要功能后：进行手动测试并提交代码

### 第4步：验证
> “运行测试。展示测试结果。如果有任何问题，请解释原因并修复。”

**然后手动验证：**
- 功能是否按照预期工作
- 边缘情况是否得到处理（例如空状态、最大长度、特殊字符等）
- 用户界面是否响应正确
- 现有功能是否仍然可以正常使用（防止功能回归）

---

## 第5阶段：适合Vibe编码的架构设计

当你的架构清晰且一致时，AI生成的代码质量会更高。

### 推荐的项目结构

```
project/
├── CLAUDE.md (or .cursorrules)     # AI rules
├── README.md                        # What this is
├── src/
│   ├── types/                       # Shared types (AI reads these first)
│   │   ├── index.ts
│   │   └── [domain].ts
│   ├── lib/                         # Pure utilities (no side effects)
│   │   ├── [utility].ts
│   │   └── [utility].test.ts
│   ├── services/                    # External integrations (DB, API, etc.)
│   │   ├── [service].ts
│   │   └── [service].test.ts
│   ├── components/ (or routes/)     # UI or route handlers
│   │   ├── [Component]/
│   │   │   ├── index.tsx
│   │   │   ├── [Component].test.tsx
│   │   │   └── [Component].module.css
│   └── app/                         # App entry, layout, config
├── tests/                           # Integration/E2E tests
├── scripts/                         # Build/deploy/utility scripts
└── docs/                            # Architecture decisions, API docs
```

### 适合Vibe编码的编码规范

1. **先定义数据类型**：在编写任何代码之前，先定义数据的结构。AI会依据这些类型来生成代码。
2. **文件代码长度控制**：每个文件的代码长度不超过300行。AI处理较短文件的效率更高，生成的代码也更易于理解。
3. **明确导入语句**：避免使用复杂的导入语句（例如`index.ts`中的重新导入）。AI难以理解这种导入方式。
4. **将测试文件放在相同的位置**：将测试文件与实现文件放在同一目录下。AI可以在编写测试时直接找到它们。
5. **配置文件集中管理**：将环境配置、功能开关等设置放在一个文件中，以便AI能够统一参考。
6. **数据库模式作为代码的一部分**：将数据库模式文件作为AI可以读取的单一来源。

### 基于模式的设计

```typescript
// src/types/todo.ts — AI reads this and understands your domain
export interface Todo {
  id: string;          // UUID v4
  title: string;       // 1-200 chars, trimmed
  completed: boolean;  // default false
  createdAt: Date;
  updatedAt: Date;
}

export interface CreateTodoInput {
  title: string;       // Required, 1-200 chars
}

export interface UpdateTodoInput {
  title?: string;
  completed?: boolean;
}

// This is ALL AI needs to implement CRUD operations correctly.
```

---

## 第6阶段：Vibe编码模式下的测试

### Vibe编码下的测试原则

```
         /  E2E  \        ← 10% (critical user flows only)
        / Integration \    ← 30% (API endpoints, DB queries)
       /    Unit Tests  \  ← 60% (pure functions, utils, logic)
```

### 先编写测试的编码模式

```
Prompt: "Write tests for a function that validates email addresses.
Requirements:
- Returns true for valid emails
- Returns false for empty string, missing @, missing domain
- Handles edge cases: plus addressing, subdomains, international domains
Write ONLY the tests. I'll implement after."
```

**之后：**“现在实现代码，确保所有测试都能通过。”

这种模式能生成质量更高的代码，因为AI有明确的测试标准。

### 需要测试的内容（最低限度的测试要求）

| 测试类型 | 是否需要测试？ | 原因 |
|----------|-------|-----|
| 纯函数 | 必须测试 | 这些函数容易出错，且测试有助于发现逻辑错误 |
| 数据转换函数 | 必须测试 | 错误的转换操作可能会损坏数据 |
| API接口 | 必须测试 | 需要验证接口的正确性 |
| 用户界面组件 | 可以选择测试 | 主要测试功能的行为，而不是实现细节 |
| 数据库查询 | 可以选择测试 | 测试复杂的查询逻辑，简单的数据操作可以省略 |
| 配置/环境加载 | 可以选择测试 | 仅测试一次，之后就可以信任代码的正确性 |

### 当AI的测试结果不正确时

**AI测试错误的常见迹象：**
- 测试的是实现逻辑而非实际功能
- 无论输入如何测试结果总是正确的
- 对所有情况都进行模拟的测试（这种测试不够准确）
- 对所有情况都使用模拟环境的测试（这种测试不够可靠）

**解决方法：**
- “这些测试模拟得过于复杂。编写能够真实反映代码行为的测试用例。只模拟外部服务（如数据库、API调用）。在可能的情况下使用内存中的模拟环境。”

---

## 第7阶段：使用AI进行调试

### 错误信息的使用方法

**Karpathy的建议：**将错误信息直接复制粘贴给AI，通常AI能够修复问题。

**在什么情况下使用这种方法：**
- 当错误信息清晰、堆栈跟踪信息完整、错误类型明确、语法错误明显时。

**在其他情况下应如何操作：**
| 错误情况 | 更好的提示语方式 |
|-----------|--------------|
| 运行时错误信息模糊 | “当我执行[操作]时，出现了[问题]。预期结果是[预期结果]。相关代码位于[文件]中。” |
| 无声的错误 | “这个函数在输入[输入值]时返回了[错误结果]。请逐步说明代码的执行过程。” |
| 间歇性错误 | “这个功能有时能正常工作，但在[特定条件下会出错]。我认为这是[问题类型/状态问题/时间问题]。这里是相关代码。” |
| 代码在修复过程中出错 | “停止当前操作。让我们回到最初的状态。最初的问题是[问题X]。你引入了一个新的错误：[问题Y]。请先修复最初的问题，然后再修复新问题。” |

### 三种解决方法

如果AI在三次尝试后仍然无法解决问题：
1. **停止**：不要反复提出相同的问题。
2. **重新描述问题**：描述你希望实现的功能，而不是错误本身。
3. **简化问题**：创建一个最简单的重现场景。
4. **重新开始**：启动一个新的编码会话，确保上下文清晰。
5. **手动调试**：有时你需要自己阅读代码来解决问题。

### 处理各种问题情况

**代码混乱（AI导致的错误）**
```
1. git stash (save current mess)
2. git checkout [last good commit]
3. Start a NEW AI session
4. Paste only the requirements, not the broken code
5. "Implement this from scratch following these patterns: [your conventions]"
```

**重复出现的错误（修复时可能引发其他问题）**
```
1. Write a failing test for the bug
2. Write regression tests for the things that keep breaking
3. "Make ALL these tests pass. Don't modify the tests."
```

**依赖关系混乱****
```
1. Check `package.json` / `requirements.txt` — AI sometimes adds conflicting deps
2. "List all dependencies you added and why each is needed"
3. Remove anything that duplicates existing functionality
4. Lock versions: "Pin all dependencies to exact versions"
```

**上下文丢失（AI忘记了之前的指令）**
```
1. Start a new session
2. Load rules file + key files
3. Summarize what's done and what remains
4. Continue with fresh context
```

---

## 第9阶段：项目上线前的检查清单

在任何使用Vibe编码的项目上线之前，必须完成以下检查：

### P0级（安全要求）**
- **必须修复的问题**：
  - 代码中不能有硬编码的敏感信息（如API密钥、密码、令牌）
  - 对所有用户输入进行验证（防止XSS攻击、SQL注入、路径遍历等问题）
  - 对受保护的路由进行身份验证
  - 用户只能访问自己的数据
  - 强制使用HTTPS协议
  - 依赖库的审核结果：`npm audit`/`pip audit`显示没有严重的安全问题
  - 对公共接口实施速率限制
  - 配置CORS协议（在生产环境中不要使用通配符）
  - 错误信息不能泄露内部细节（避免向用户显示堆栈跟踪信息）

### P1级（性能优化）**
- **应该修复的问题**：
  - 数据库查询针对常见条件添加索引
  - 避免出现N+1查询（检查ORM的查询日志）
  - 图像文件进行优化（使用WebP格式、懒加载）
  - 代码包的大小控制在合理范围内（初始JavaScript文件大小小于200KB）
  - 异步操作时显示加载状态
  - 列表接口支持分页（避免无限量的数据请求）

### P2级（可靠性要求）**
- **应该修复的问题**：
  - 所有异步操作都应有错误处理机制
  - 服务异常时能够优雅地降级
  - 提供健康检查接口
  - 日志记录方式规范（不要使用`console.log`
  - 通过环境变量配置环境设置
  - 数据库迁移操作规范（不要使用原始SQL语句）

### P3级（推荐的最佳实践）**
- **如果有这些好处的话**：
  - 测试覆盖率超过80%
  - 使用TypeScript的严格模式并提供类型提示
  - 配置代码检查工具（如Linter）
  - 项目说明文档中包含设置指南
  - 推送代码时自动运行测试用例

**AI辅助的代码优化提示语：**
> “检查这个代码库是否具备上线所需的条件。根据以下清单进行核对：[列出检查项]。对于每个项目，说明是否通过/未通过/不适用，以及如果未通过需要修复什么。请具体说明问题所在的位置和代码行号。”

---

## 第10阶段：高级技巧

### 并行使用AI进行开发

可以同时运行多个AI会话：
- **会话A**：实现后端API
- **会话B**：构建前端组件
- **会话C**：编写测试用例

**并行开发时的规则：**
- 先定义接口和数据类型（作为共同的规范）
- 每个会话都有自己的规则文件
- 通过Git合并各个会话的代码
- 合并完成后进行集成测试

### 合作编程技巧

**导航者-驱动者模式（你负责引导，AI负责实现）**
> 你：“我们需要添加分页功能。API应该接受页码和查询参数。返回项目列表、项目总数以及是否有下一个页面。”
> AI：“已实现。”
> 你：“好的。现在再实现基于游标的分页功能。游标应该指向列表中的最后一个项目。”
> AI：“已实现。”

**交替实现模式**
> 你：编写测试用例
> AI：实现代码
> 你：编写下一个测试用例
> AI：实现下一个功能
> （这种模式类似于TDD，非常有效）

**辅助者模式（AI解释，你负责验证）**
> “一步步地跟我讲解这段代码。解释每个函数的作用、可能出错的地方以及你的假设。”
> （通过这种方式，你可以在问题变成实际错误之前发现它们）

### 上下文管理技巧

| 管理策略 | 适用场景 | 实施方法 |
|----------|------|-----|
| **重新开始** | 每15-20次对话后 | 启动新的编码会话，重新加载规则文件和关键文件 |
| **总结** | 在处理复杂任务之前 | “总结我们已经完成的工作，然后再开始下一个任务。” |
| **专注文件** | 在处理大型代码库时 | “只关注`src/services/auth.ts`文件。” |
| **进度记录** | 在处理多会话的项目时 | 保存`PROGRESS.md文件，记录已完成的工作和剩余任务 |

### Vibe编码的Git工作流程

```bash
# Before starting
git checkout -b feature/[name]
git status  # clean working tree

# During (commit often!)
git add -A && git commit -m "feat: [what AI just implemented]"
# Every 2-3 AI turns, commit. Your safety net.

# If things go wrong
git diff  # see what AI changed
git stash  # save mess
git checkout .  # nuclear option: discard all changes

# When done
git diff main..HEAD  # review ALL changes before merging
```

---

## 第11阶段：常见错误及避免方法

| 编码错误 | 后果 | 预防措施 |
|---|---------|-------------|------------|
| 1 | 没有规则文件 | 每次编码时AI都会重新定义编码规范 | 在每次使用AI之前先编写规则文件 |
| 2 | 先编写实现代码再制定计划 | 会导致错误的假设不断累积 | 始终遵循“研究 → 规划 → 实现”的步骤 |
| 3 | 不阅读AI生成的代码 | 会导致隐藏的错误和安全漏洞 | 至少审查关键部分的代码 |
| 4 | 提交一次包含所有代码的提示语 | AI会失去方向，导致代码实现不完整 | 每次只提交一个具体的任务 |
| 5 | 不频繁提交代码 | 如果AI出错，无法回滚代码 | 每2-3次编码后提交一次代码 |
| 6 | 忽视测试结果 | “在我的机器上测试通过了” | 只要测试通过了就认为代码没问题，这是错误的想法 |
| 7 | 允许AI随意添加依赖库 | 会导致代码包过大或版本冲突 | 在规则文件中明确禁止随意添加依赖库 |
| 8 | 上线前没有检查清单 | 会导致安全漏洞 | 在上线前必须完成P9级的检查 |
| 9 | 长时间连续使用AI进行编码 | 会导致上下文混乱，AI可能忘记之前的指令 | 每15-20次编码后重新开始一个新的会话 |
| 10 | 在处理敏感功能（如认证/支付系统）时使用Vibe编码 | 会导致关键功能出现严重错误 | 必须手动审查所有涉及安全的代码 |
| 11 | 不定义数据类型/模式 | AI每次都会生成不同的数据类型 | 在编写代码之前先定义数据类型 |
| 12 | 相信AI的判断** | AI可能会生成有问题的代码 | 自己验证代码的正确性，然后进行测试 |
| 13 | 同一个提示语被重复使用三次 | AI可能会陷入循环 | 重新描述问题，简化问题，或者手动解决问题 |
| 14 | 在一个会话中处理多个任务 | 会导致上下文混乱 | 每次只处理一个具体的任务 |
| 15 | 没有明确的架构指导 | AI可能会生成不一致的代码结构 | 在规则文件中明确编码规范 |

## 第12阶段：定期评估Vibe编码的效果

定期评估你的Vibe编码质量：

```yaml
week_of: "YYYY-MM-DD"
sessions: [count]
features_shipped: [count]
bugs_introduced: [count]  # found post-ship
bugs_caught_in_review: [count]  # caught before ship
avg_prompts_per_feature: [count]
time_saved_estimate_hours: [number]
fresh_session_restarts: [count]

# Score yourself (1-5):
prompt_quality: [1-5]      # Are you using Level 4+ prompts?
review_discipline: [1-5]   # Are you reviewing critical code?
testing_rigor: [1-5]       # Are you testing before shipping?
architecture: [1-5]        # Is the codebase staying clean?
commit_frequency: [1-5]    # Are you committing every 2-3 turns?

total_score: [5-25]
```

| 评分 | 评价 | 措施 |
|-------|--------|--------|
| 20-25分 | 高级使用者 | 你已经掌握了Vibe编码技巧，可以指导他人 |
| 15-19分 | 表现不错 | 有良好的编码习惯，需要关注薄弱环节 |
| 10-14分 | 学习中 | 每周阅读这份指南，培养良好的编码习惯 |
| 5-9分 | 存在风险 | 需要放慢编码速度，加强规划和测试 |

## Vibe编码的十大原则

1. **先定义数据类型**：在编写代码之前先定义数据结构。
2. **必须编写规则文件**：没有规则文件会导致代码不一致。
3. **先规划再实现**：花5分钟进行规划可以节省5小时的调试时间。
4. **每次只提交一个任务**：专注才能保证代码质量。
5. **每次完成代码后都提交**：Git是一个重要的安全保障。
6. **务必测试关键路径**：至少测试正常情况和边缘情况。
7. **每次使用AI后都重新开始新的会话**：避免上下文信息失效。
8. **手动审查涉及安全的代码**：对于认证、支付、数据访问相关的代码，必须进行手动审查。
9. **遵循200行规则**：如果修改的内容较多，应将其拆分成更小的部分。
10. **知道何时停止使用Vibe编码**：如果AI在三次尝试后仍无法解决问题，就需要改变开发方法。

## 快速参考命令

```
"Read [files] and explain the architecture. Don't change anything."
"Write a plan for [feature]. List files to create/modify and changes in each."
"Implement only [specific thing]. Don't touch other files."
"Write tests first for [requirements]. Then implement to pass them."
"Review this for [security/performance/readability]. Be specific."
"This error occurs when [action]. Expected [behavior]. Here's the code: [paste]"
"Refactor [file] to [goal]. Same behavior. Don't add features."
"What dependencies did you add and why? Remove anything unnecessary."
"Walk me through this code. Explain assumptions and potential issues."
"Stop. The original issue was [X]. Let's start fresh with a minimal approach."
"Run all tests. If any fail, fix them without breaking other tests."
"Check this against the production checklist: [paste P0-P3 items]."
```

*由AfrexAI团队开发——他们提供的不仅仅是AI提示工具，还有AI辅助的开发工具。*