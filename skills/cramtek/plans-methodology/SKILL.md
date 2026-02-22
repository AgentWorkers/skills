---
name: plans-methodology
description: >
  **使用“Plans”进行结构化工作跟踪的方法**  
  适用于创建、管理、审查或委派重要工作的计划时。该方法涵盖了计划的完整生命周期（草稿、已批准、进行中、已完成、已归档），以及文件夹结构、审批权限、跨代理的任务委派和任务跟踪等流程。当用户需要创建计划、跟踪工作、将任务委派给下属代理或审查计划状态时，均可使用该方法。
---
# 计划方法论（Plan Methodology）

适用于个人或多代理团队的结构化工作跟踪系统。每个代理都在他们的工作空间中维护一个名为 `plans/` 的文件夹。

## 目录结构

```
plans/
  README.md
  draft/          # Being defined, not yet approved
  approved/       # Ready for execution
  in_progress/    # Currently executing
  completed/      # Done
  archived/       # Historical reference
```

每个计划对应一个文件夹，格式为：`YYYY-MM-DD-plan-name/`（例如：`2023-01-01-my-project`）。

## 计划内容

```
YYYY-MM-DD-plan-name/
  specs/              # Problem statements, requirements
  proposal.md         # Why: justification, impact, risks
  design.md           # How: architecture, flows, decisions
  tasks.md            # What: checkboxes, owners, phases
```

### proposal.md  
（用于记录计划的提案内容）

```markdown
# Proposal: [Plan Name]

## Status
Draft | Submitted | Approved | Rejected

## Parent Plan
[agent]/plans/[state]/[plan-name] (if child plan)

## Problem
What problem are we solving?

## Proposed Solution
High-level approach.

## Impact
What changes? What improves?

## Cost / Effort
Time, resources, dependencies.

## Risks
What could go wrong?

## Decision
Approved by [name] on [date] | Rejected because [reason]
```

### design.md  
（用于记录计划的设计方案）

```markdown
# Design: [Plan Name]

## Overview
What are we building/doing?

## Architecture / Approach
How does it work? Diagrams, flows, decisions.

## Dependencies
What do we need? Other plans, external services, other agents.

## Constraints
Limitations, rules, non-negotiables.

## Open Questions
Things still to be decided.
```

### tasks.md  
（用于记录计划中的任务列表）

```markdown
# Tasks: [Plan Name]

## Summary
Brief overview.

## Tasks

### Phase 1: [Name]
- [x] Task description -> Owner
  Completed YYYY-MM-DD. Notes.
- [ ] Task description -> Owner
  Details, acceptance criteria.
- [ ] Delegate to [Agent]: [what] -> [Agent]
  Child plan: [agent]/plans/[state]/[plan-name]
```

## 计划的生命周期（Plan Lifecycle）

1. **草稿阶段（Draft）**：编写项目规格书，起草提案。  
2. **批准阶段（Approved）**：提案获得批准，设计方案和任务详细内容完成。  
3. **执行阶段（In Progress）**：开始执行计划中的任务。  
4. **完成阶段（Completed）**：所有任务均已完成。  
5. **归档阶段（Archived）**：计划被存档以供参考。  

通过将计划文件夹移动到不同的目录来改变其状态。

## 何时创建计划（When to Create a Plan）  

- 当需要多代理协作时。  
- 当工作需要投入大量精力时。  
- 当项目包含多个阶段时。  
- 当需要获得批准时。  
- 当需要跟踪项目进度时。  

- 对于简单的任务、快速查询或常规操作，可以跳过创建计划的步骤。  

## 审批权限（Approval Authority）  

自行定义审批层级。常见的审批模式如下：  
- **负责人/CEO**：负责审批战略性计划。  
- **主管代理（Lead Agent）**：有权审批符合公司愿景的计划。  
- **下属代理（Sub-Agent）**：将提案提交给主管代理进行审批。  

请在工作空间的 `plans/README.md` 文件中记录审批流程。  

## 工作委派（Delegation）  

在将任务委派给其他代理时，请注意以下规则：  
1. 上级计划的 `tasks.md` 文件中应包含下级计划的路径。  
2. 下级计划的 `proposal.md` 文件中应包含上级计划的路径。  

**示例：**  
- **上级计划的 `tasks.md` 文件示例：**  
  ```markdown
  tasks:
    - task1
    - task2
    - sub-plan1/
      - sub-task1
      - sub-task2
  ```
  ```  
- **下级计划的 `proposal.md` 文件示例：**  
  ```markdown
  proposal:
    - 任务描述
    - 需要完成的步骤
    - 上级计划的引用路径：../plans/2023-01-01-my-project
  ```
  

## 会议开始时的操作（On Session Start）  

- 检查 `plans/in_progress/` 目录，查看当前正在进行中的计划。  
- 检查 `plans/draft/` 目录，查看待处理的计划。  
- 从上次停止的地方继续执行计划。  

## 关于计划制定的建议（Granularity Tips）：  

- 并非所有工作都需要制定详细的计划。只有那些复杂、多步骤的任务才需要计划。  
- 单个代理处理简单问题时，无需制定计划。  
- 计划在需要协调、跟踪或审批的情况下才显得尤为重要。  
- 保持计划文档的简洁性；冗长的计划往往会被忽略。