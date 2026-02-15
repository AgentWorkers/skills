---
name: detector
description: 该工具能够检测 SpecWeave 的上下文环境，并为可用的命令提供工作流程文档。适用于学习 SpecWeave 命令、理解各种命令（如 /sw:increment、/sw:do、/sw:progress、/sw:done）或获取工作流程指导时使用。它会解释命令的语法以及推荐的工作流程模式。
---

# SpecWeave - 智能工作流文档

SpecWeave 提供了明确的斜杠命令，以确保工作流的可靠执行。

**注意**：产品描述的自动检测由 `increment-planner` 技能负责。该技能提供命令文档和工作流指导。

## SpecWeave 的工作原理

**使用方法**：输入 `/inc "功能描述"` 来开始使用。

**智能工作流特性**：
- ✅ 自动恢复（`/do` 会找到下一个未完成的任务）
- ✅ 自动关闭（如果项目经理（PM）设置的检查通过，`/inc` 会自动关闭上一个任务）
- ✅ 进度跟踪（`/progress` 可随时显示进度）
- ✅ 自然流畅的流程（完成一个任务后直接开始下一个任务，无需额外操作）

## 可用的斜杠命令

### 核心工作流命令

| 命令 | 别名 | 描述 | 示例 |
|---------|-------|-------------|---------|
| `/increment` | `/inc` | **计划工作增量**（由项目经理主导，自动关闭上一个任务） | `/inc "用户认证"` |
| `/do` | - | **执行任务**（智能恢复，每个任务完成后会触发相关操作） | `/do` |
| `/progress` | - | **显示进度**（任务完成百分比、项目经理设置的检查、下一步操作） | `/progress` |
| `/validate` | - | **验证质量**（基于规则，可选使用大型语言模型（LLM）进行判断） | `/validate 0001 --quality` |
| `/done` | - | **手动关闭任务**（可选，`/inc` 会自动关闭任务） | `/done 0001` |

### 支持命令

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `/list-increments` | 列出所有工作增量的状态 | `/list-increments` |
| `/sw:sync-docs` | 同步战略文档与代码 | `/sw:sync-docs --increment=003` |
| `/sync-github` | 将工作增量同步到 GitHub 问题（issue） | `/sync-github` |

## 为什么只使用一个别名？

**设计决策**：`/inc` 是唯一的别名（因为它是使用最频繁的命令）。
- ✅ 减少认知负担（只需记住一个别名）
- ✅ 其他命令使用全名以提高清晰度
- ✅ 使用户思维更简单

## 典型工作流程

**自然的工作流程**（0001 → 0002 → 0003）：

```bash
# 1. Initialize project (CLI, before Claude session)
npx specweave init my-saas

# 2. Plan your first increment (PM-led)
/inc "AI-powered customer support chatbot"
# PM creates: spec.md + plan.md + tasks.md (auto!) + tests.md

# 3. Build it (smart resume)
/do
# Auto-resumes from next incomplete task
# Hooks run after EVERY task

# 4. Check progress anytime
/progress
# Shows: 5/12 tasks (42%), next: T006, PM gates status

# 5. Continue building
/do
# Picks up where you left off

# 6. Start next feature (auto-closes previous!)
/inc "real-time chat dashboard"
# Smart check:
#   PM gates pass → Auto-close 0001, create 0002
#   PM gates fail → Present options (never forces)

# 7. Keep building
/do
# Auto-finds active increment 0002

# Repeat: /sw:increment → /sw:do → /sw:progress → /sw:increment (auto-closes) → /sw:do...
```

## 命令详情

### `/inc` 或 `/increment` - 计划工作增量

**最重要的命令！** 由项目经理主导的计划过程，具有自动关闭功能。

```bash
# Short form (recommended)
/inc "User authentication with JWT and RBAC"

# Full form
/increment "User authentication with JWT and RBAC"
```

**操作流程**：
1. **智能检查上一个任务**：
   - 如果当前的工作增量正在进行中：
     - 如果项目经理设置的检查通过，自动关闭上一个任务并创建新的工作增量
     - 如果检查未通过，显示选项（完成当前任务、移动任务或取消）
2. **项目经理主导的计划**：项目经理代理分析需求
3. **创建文档**：`spec.md`（说明任务内容及原因），`plan.md`（制定执行计划）
4. **自动生成**：`tasks.md`（任务列表），`tests.md`（测试策略）
5. **准备构建**：状态设置为“已计划”

### `/do` - 执行任务（智能恢复）

**智能恢复**：自动找到下一个未完成的任务。

```bash
# Auto-finds active increment, resumes from next task
/do

# Or specify increment explicitly
/do 0001
```

**操作流程**：
1. 找到当前正在进行的工作增量（或使用指定的 ID）
2. 解析 `tasks.md`，找到第一个未完成的任务
3. 显示任务信息（任务编号、描述、优先级）
4. 执行任务
5. **每个任务完成后会触发相关操作**（更新文档、进行质量验证）
6. 当再次运行 `/do` 时，会继续执行下一个任务

**无需手动跟踪！** 只需持续运行 `/do` 即可。

### `/progress` - 显示进度

**随时查看进度**：可以随时了解工作进度。

```bash
/progress

# Auto-finds active increment, shows:
# - Task completion % (P1 weighted higher)
# - PM gates preview (tasks, tests, docs)
# - Next action guidance
# - Time tracking & stuck task warnings
```

### `/validate` - 验证质量

**双重验证**：基于规则的验证（120 项检查）+ 可选的人工智能质量评估。

```bash
# Rule-based validation only
/validate 0001

# With AI quality assessment (LLM-as-judge)
/validate 0001 --quality

# Export suggestions to tasks.md
/validate 0001 --quality --export

# Auto-fix issues (experimental)
/validate 0001 --quality --fix
```

### `/done` - 手动关闭任务

**可选命令**：在需要手动关闭任务时使用（通常 `/inc` 会自动完成关闭）。

```bash
/done 0001

# System validates:
# - All P1 tasks completed
# - All tests passing
# - Documentation updated
#
# Offers leftover transfer options for P2/P3 tasks
```

**使用场景**：
- 在长时间休息前手动关闭任务
- 强制关闭任务而不启动新的工作增量
- 仅生成关闭报告

**通常不需要使用**：如果项目经理设置的检查通过，`/inc` 会自动关闭上一个任务。

### `/list-increments` - 列出所有工作增量

**查看所有工作增量的状态和完成情况**。

```bash
# All increments
/list-increments

# Filter by status
/list-increments --status in-progress

# Filter by priority
/list-increments --priority P1

# Show task breakdown
/list-increments --verbose

# Only WIP increments
/list-increments --wip-only
```

## 智能工作流特性

### 1. 自动恢复（无需手动跟踪）

**问题**：传统工作流需要手动跟踪当前正在执行的任务。

**解决方案**：`/do` 会自动找到下一个未完成的任务。

```
/do

📋 Resuming increment 0001-authentication
   Next: T006 - Implement JWT token validation
   Priority: P1
   Estimate: 2 hours
   Context: After T005 (token generation)

Starting task T006...
```

### 2. 自动关闭（流畅的流程）

**问题**：手动关闭任务需要额外的操作。

**解决方案**：如果项目经理设置的检查通过，`/inc` 会自动关闭上一个任务。

**理想的工作流程**（自动关闭）：
```
/inc "payment processing"

📊 Checking previous increment 0001-authentication...
   PM Gates: ✅ All P1 complete, tests pass, docs updated

✅ Auto-closing 0001 (seamless)
Creating 0002-payment-processing...
```

**发现问题时**（会显示选项）：
```
/inc "payment processing"

📊 Checking previous increment 0001-authentication...
   PM Gates: ❌ 2 P1 tasks remaining

❌ Cannot auto-close 0001 (incomplete)

Options:
  A) Complete 0001 first (recommended)
  B) Move incomplete tasks to 0002
  C) Cancel new increment

Your choice? _
```

### 3. 建议而非强制

**关键原则**：用户始终拥有控制权：
- ✅ 发现问题时提供选项
- ✅ 清晰解释后果
- ✅ 允许用户自行决定
- ❌ 绝不强制用户关闭任务

### 4. 进度可视化

**问题**：进度不明确（完成了多少工作？）

**解决方案**：`/progress` 可随时显示进度。

```
/progress

📊 Increment 0001-authentication

Status: in-progress
Progress: 42% (5/12 tasks) ⏳

Task Breakdown:
  P1: 60% (3/5) ⏳
  P2: 33% (2/6)
  P3: 0% (0/1)

PM Gates Preview:
  ✅ All P1 tasks: 60% (not ready)
  ⏳ Tests passing: Running...
  ✅ Docs updated: Yes

Next Action: Complete T006 (P1, 2h)
Time on increment: 3 days
```

## 为什么使用斜杠命令？

**问题**：在 Claude Code 中，自动激活功能并不可靠。

**SpecWeave 的解决方案**：使用明确的斜杠命令以确保 100% 的可靠性。

**优势**：
- ✅ 100% 的可靠性（无需猜测）
- ✅ 用户意图明确（操作直观）
- **行为一致**（没有意外）
- **易于学习**（可以在 `.claude/commands/` 中查看）

## 如何获取帮助

**在 Claude Code 中**：
```
User: "How do I use SpecWeave?"
→ Claude shows this documentation
```

**可用命令**：
```
User: "What SpecWeave commands are available?"
→ Claude lists all slash commands
```

**命令语法**：
```
User: "How do I create a new increment?"
→ Claude explains /sw:increment command with examples
```

## 文档说明

- **命令参考**：请参阅 `.claude/commands/` 以获取所有命令的详细信息
- **快速参考**：请参阅 `CLAUDE.md` 以获取命令参考表
- **官方文档**：https://spec-weave.com/docs/commands

---

**💡 专业提示**：掌握这个智能工作流循环！

**核心流程**：`/inc`（计划）→ `/do`（执行）→ `/progress`（检查）→ `/inc`（继续下一个任务）

**关键要点**：工作流程自然流畅，无需额外操作。专注于任务开发，而非项目管理。

**只需记住一个别名**：`/inc`（即 `/increment`）