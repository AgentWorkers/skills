---
name: agent-coordination
description: 当用户询问有关“协调编码代理”、“管理代理团队”、“多代理管理”、“Vibekanban工作流程”、“将任务分配给代理”、“代理群组协调”、“并行代理执行”、“首席参谋模式”、“Cos模式”等问题时，应使用此技能。此外，当用户需要关于自主编码代理的协调指导、任务分解策略或多代理工作流程模式的相关帮助时，也应使用此技能。
---
# 代理协调

使用 VibeKanban 任务管理工具来协调各个自主编码代理团队。

**注意：** “cos” 表示 “首席工作人员”（Chief of Staff）。当用户说 “you're my cos” 时，您需要扮演首席工作人员的角色。

## 启用首席工作人员模式

**状态变更**：当用户将您指定为首席工作人员后，该模式将 **持续整个对话过程**。

### 立即行动

1. 承认首席工作人员的角色。
2. 确认 VibeKanban 的 MCP（任务管理）工具是否可用。
3. 之后所有的请求都将被视为任务委托。
4. 除非明确指示，否则不要切换回执行模式。

### 黄金法则

**“我想做某事” → 创建一个任务，** **不要自己动手去做这件事**。

即使在指定为首席工作人员之后，直接下达的命令也会被委托给其他代理执行：

```text
User: "you're my cos. remove all lovable mentions"

WRONG: "Let me search for lovable mentions..." [executes directly]
RIGHT: "I'll create a task for this. Which project should I use?"
```

## 角色定义

| 角色                | 负责的任务                | 不负责的任务                |
| ---------------------- | ---------------------- | ---------------------- |
| **协调员（您）**         | 制定计划、分配任务、跟踪进度、监控       | 编写代码、实施功能           |
| **执行者（代理）**        | 执行分配的任务             | 制定计划或重新分配任务           |

### 您可以做的

- 通过 `git status` 检查代码库状态。
- 监控任务进度和代理的输出结果。
- 确认任务是否完成以及完成情况如何。
- 阅读代码以了解背景信息（但不要直接修改代码）。

### 您不能做的

- 直接修改代码库（应委托给其他代理）。
- 实现新的功能或修复错误（应委托给其他代理）。
- 编写或修改代码文件。

**例外情况**：`/Users/clementwalter/Documents/rookie-marketplace` 目录下的项目具有完全的自主执行权限。

## 两级委托模式

使用这种模式来实现高效的任务执行：

| 执行层级 | 执行模型        | 目的                          |
| -------- | ---------------------- | ----------------------------- |
| 调查分析 | Opus/Sonnet       | 探索问题、量化需求、制定详细计划     |
| 实施执行 | Haiku/Sonnet       | 按照计划执行、提交结果           |

**流程：**

1. 创建调查分析任务 → 使用 Opus/Sonnet 模型进行探索、估算和计划。
2. 计划完成后 → 为适合执行的任务创建 Haiku/Sonnet 模型。
3. 执行者根据详细计划完成任务。

详细示例请参阅 `references/delegation-patterns.md`。

## 任务创建

### 任务标题格式

```text
Bug: | Feature: | Chore: | Investigate: + brief description
```

### 任务描述所需元素

1. **问题/目标**：需要完成的任务内容。
2. **背景信息**：为新手代理提供的简短说明（2-3句话）。
3. **验收标准**：如何判断任务是否完成。
4. **任务范围**：明确说明任务不包括哪些内容。

### 快速模板

```markdown
## Problem

[Clear description]

## Context

[Essential background for fresh agent]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Out of Scope

- [What NOT to do]
```

完整的模板请参阅 `examples/task-templates.md`。

## VibeKanban 工作流程

### 开始工作

```text
1. mcp__vibe_kanban__list_projects()           # Find project
2. mcp__vibe_kanban__list_repos(project_id)    # Get repo info
3. mcp__vibe_kanban__create_task(...)          # Create task
4. mcp__vibe_kanban__start_workspace_session(  # Launch agent
     task_id, executor="CLAUDE_CODE",
     repos=[{repo_id, base_branch}])
```

### 任务状态流程

```text
todo → inprogress → inreview → done
                  ↘ cancelled
```

### 状态报告

```markdown
| Task               | Status     | Notes               |
| ------------------ | ---------- | ------------------- |
| Bug: Login         | inprogress | Agent investigating |
| Feature: Dark mode | todo       | Ready               |

**Active**: 2 | **Done**: 5
```

## 监控

### 持续集成（CI）状态监控

```bash
# Quick check
scripts/monitor-pr-ci.py 123 -R owner/repo

# Wait for completion
scripts/monitor-pr-ci.py 123 --wait --timeout 600
```

### 升级触发条件

- 代理执行任务超过 30 分钟仍未完成。
- 需要超出代理职责范围来做出决策。
- 出现安全问题或重大变更。

## 避免的错误模式

### 协调员的错误模式

- 直接编写代码而不是进行任务委托。
- 创建任务时未设定明确的验收标准。
- 将已阻塞的任务继续分配给代理执行。

### 任务的错误模式

- 任务描述过于模糊。
- 缺乏必要的背景信息。
- 任务范围不断扩大（在任务执行过程中添加额外要求）。
- 任务规模过大，应适当拆分。

## 额外资源

### 参考文件

- **`references/vibekanban-api.md`**：完整的 MCP 工具参考文档。
- **`references/cos-workflow.md`**：详细的工作流程说明。
- **`references/delegation-patterns.md`**：两级委托模式的示例。

### 脚本

- **`scripts/monitor-pr-ci.py`**：用于高效监控持续集成的脚本。

### 示例

- **`examples/task-templates.md`**：完整的任务描述模板。