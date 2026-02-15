---
name: subagent-driven-development
model: standard
description: 通过为每个任务派遣一个新的子代理来执行实施计划，并采用两阶段审核流程（首先是规范合规性审核，其次是代码质量审核）。当你的实施计划包含大量相互独立的任务，并且希望在单次会话内实现高质量、快速的迭代时，可以使用这种方法。
version: 1.0.0
---

# 基于子代理的开发模式（Subagent-Driven Development）

通过为每个任务分配一个新的子代理来执行计划，并在每个任务完成后进行两阶段审核：首先是规范合规性审核，其次是代码质量审核。

**核心原则：** 每个任务使用一个新的子代理 + 两阶段审核 = 避免上下文混淆、保证高质量、实现快速迭代。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install subagent-driven-development
```

## 适用场景

- 当您有一个包含独立任务的实施计划时
- 您希望在单次会话中完成整个计划的执行（任务之间无需人工干预）
- 任务可以顺序执行和审核，且彼此之间没有紧密的耦合关系

| 情况                          | 适用方法        | 替代方法                                      |
| ---------------------------- | ----------------------------- | --------------------------------------------------------- |
| 已有计划且需在同一会话中完成     | **适用**        | —                                           |
| 已有计划但需在多个会话中完成     | 不适用         | 分阶段执行计划                                    |
| 尚未制定计划                   | 不适用         | 先制定计划                                      |
| 任务之间存在紧密耦合                | 不适用         | 手动执行或进一步分解任务                              |

## 执行流程

```
┌─────────────────────────────────────────────────────┐
│  1. Read plan, extract ALL tasks with full text      │
│  2. Note shared context (arch, deps, conventions)    │
│  3. Create TodoWrite with all tasks                  │
└──────────────────────┬──────────────────────────────┘
                       ▼
          ┌────── Per Task ──────┐
          │                      │
          │  Dispatch Implementer (references/implementer-prompt.md)
          │       │                                │
          │       ▼                                │
          │  Questions?──yes──► Answer, re-dispatch│
          │       │no                              │
          │       ▼                                │
          │  Implement + test + commit + self-review│
          │       │                                │
          │       ▼                                │
          │  Dispatch Spec Reviewer (references/spec-reviewer-prompt.md)
          │       │                                │
          │       ▼                                │
          │  Compliant?──no──► Implementer fixes──┘
          │       │yes             then re-review
          │       ▼
          │  Dispatch Code Reviewer (references/code-quality-reviewer-prompt.md)
          │       │
          │       ▼
          │  Approved?──no──► Implementer fixes, re-review
          │       │yes
          │       ▼
          │  Mark task complete
          └───────┬──────────────┘
                  ▼
          More tasks? ──yes──► next task
                  │no
                  ▼
          Final cross-task code review
                  ▼
          Finish development branch
```

## 提示模板

为子代理角色提供了三种参考提示模板：

| 角色                | 文件名                          | 用途                                      |
| ---------------------- | ----------------------------------------- | -------------------------------------- |
| **实现者（Implementer）**    | `references/implementer-prompt.md`          | 负责实现、测试、提交代码及自我审核                         |
| **规范审核者（Spec Reviewer）** | `references/spec-reviewer-prompt.md`        | 确认代码完全符合规范                                 |
| **代码审核者（Code Reviewer）** | `references/code-quality-reviewer-prompt.md` | 确认代码整洁且易于维护                               |

## 示例工作流程

```
Controller: Reading plan — 5 tasks extracted, TodoWrite created.

─── Task 1: Hook installation script ───

[Dispatch implementer with full task text + context]

Implementer: "Should the hook be installed at user or system level?"
Controller:  "User level (~/.config/hooks/)"

Implementer: ✅ Implemented install-hook command
  - Added tests (5/5 passing)
  - Self-review: missed --force flag, added it
  - Committed

[Dispatch spec reviewer]
Spec reviewer: ✅ Spec compliant — all requirements met

[Dispatch code reviewer with git SHAs]
Code reviewer: ✅ Approved — clean, good coverage

[Mark Task 1 complete]

─── Task 2: Recovery modes ───

[Dispatch implementer]

Implementer: ✅ Added verify/repair modes (8/8 tests passing)

[Dispatch spec reviewer]
Spec reviewer: ❌ Issues:
  - Missing: progress reporting ("report every 100 items")
  - Extra: added --json flag (not in spec)

[Implementer fixes: remove --json, add progress reporting]
Spec reviewer: ✅ Spec compliant

[Dispatch code reviewer]
Code reviewer: Important — magic number 100, extract constant

[Implementer fixes: extract PROGRESS_INTERVAL]
Code reviewer: ✅ Approved

[Mark Task 2 complete]

... (tasks 3-5) ...

[Final cross-task code review]
Final reviewer: ✅ All requirements met, ready to merge
```

## 控制者的职责

控制器（即您）负责协调整个流程。主要职责包括：

| 责任                          | 详细说明                                      |
| ----------------------------- | --------------------------------------------------------- |
| **提前提取任务内容**         | 阅读计划文件，提取所有任务信息——子代理无需直接阅读计划文件           |
| **提供完整上下文**          | 向每个子代理提供完整的任务描述及架构背景                         |
| **回答问题**              | 在子代理开始执行前给予清晰、完整的解答                         |
| **确保审核顺序**          | 先进行规范合规性审核，再审核代码质量                          |
| **跟踪进度**                | 每个任务完成后更新任务状态                             |
| **按顺序分配任务**         | 避免任务执行冲突，每次仅分配一个实现子代理                     |

## 质量检查流程

每个任务需通过三个质量检查环节：

| 检查环节                | 负责人        | 检查内容                                      |
| ---------------------- | ----------------------------- | --------------------------------------------------------- |
| **自我审核（Self-Review）**     | 实现者          | 完整性、命名规范、避免重复代码、测试质量                         |
| **规范审核（Spec Review）**     | 规范审核者        | 确保代码完全符合规范                                 |
| **代码审核（Code Review）**     | 代码审核者        | 代码整洁性、可维护性、测试覆盖率                         |

## 相比手动执行的优势：

- 每个任务都使用新的子代理，避免因历史状态导致的混淆
- 子代理自然遵循测试驱动开发（TDD）流程
- 问题在任务开始前就被发现，而非在执行过程中

## 相比并行执行计划的优势：

- 无需额外的交接环节
- 进度持续、可控
- 审核流程自动化

**成本考量：** 虽然需要更多子代理（每个任务需要1个实现者和2个审核者），但能更早发现问题，从而节省后续调试的时间和成本

## 绝对禁止的行为：

- **跳过任何一轮审核**——规范合规性和代码质量审核都是必须的
- **在规范审核通过前就开始代码审核**——错误的顺序会导致资源浪费
- **同时分配多个实现者**——可能导致合并冲突和上下文混乱
- **让子代理阅读计划文件**——直接提供完整的任务描述即可
- **忽略子代理的疑问**——在子代理继续执行前必须给出完整解答
- **对规范合规性审核的结果含糊其辞**——如果审核者发现了问题，说明工作尚未完成
- **修复问题后跳过再次审核**——发现问题后，应由实现者修复，再由审核者重新审核
- **用自我审核替代正式审核**——自我审核只是初步检查，不能替代正式审核
- **在有未解决审核问题的情况下直接进入下一个任务**——当前任务必须先获得审核通过
- **手动修复问题而非通过子代理**——手动修复会污染控制者的工作环境

## 处理故障的方法：

| 故障情况                        | 应对措施                                      |
| ---------------------------- | --------------------------------------------------------- |
| 子代理提出疑问                      | 清晰回答，并在必要时提供额外信息                         |
| 审核者发现问题                    | 由同一实现者子代理修复问题，审核者重新进行审核                   |
| 子代理无法完成任务                    | 分配新的修复子代理，并提供具体指导                         |
| 任务因依赖关系受阻                    | 重新安排剩余任务的执行顺序或先解决依赖关系                         |