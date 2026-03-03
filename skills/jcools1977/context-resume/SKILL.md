---
name: context-resume
version: 1.0.0
description: 当你在中断后（比如开会、吃午饭、睡觉、度过周末或休假三周后）重新开始工作时，这个功能会帮助你快速恢复整个工作环境。它并不是简单地恢复之前的会话状态，而是帮助你恢复工作时的“心理状态”（即对当前任务的认知和准备状态）。这解决了每个开发者每周都会遇到的问题：“我刚才在做什么来着？”
author: J. DeVere Cooley
category: everyday-tools
tags:
  - context-switching
  - productivity
  - workflow
  - daily-driver
metadata:
  openclaw:
    emoji: "🧵"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - everyday
      - productivity
---
# 上下文恢复（Context Resume）

> “普通开发者每11分钟就会被打断一次，而重新进入深度工作状态需要23分钟。算一算吧——大多数开发者根本无法进入深度工作状态。”

## 它的作用

周五晚上，在开发某个功能的过程中，你关闭了笔记本电脑。周一早上，你重新打开电脑，发现文件还在，代码分支还在，终端的历史记录也在。但你的思维状态却已经改变了。你之前所考虑的功能、刚刚发现的边缘情况、失败的测试及其原因、以及你曾经决定采用但后来又放弃的解决方案，都已经被遗忘了。

“上下文恢复”功能会根据你留下的各种痕迹，帮助你重新构建之前的思维状态。

## 它能恢复的内容：

### 1. 你之前的工作位置
```
LAST SESSION ANALYSIS:
├── Branch: feature/checkout-v2
├── Last commit: "wip: tax calculation for multi-currency" (uncommitted changes present)
├── Modified files (uncommitted):
│   ├── src/checkout/tax.ts ......... +47 lines (function incomplete, ends mid-logic)
│   ├── src/checkout/tax.test.ts .... +12 lines (2 tests, 1 failing)
│   └── src/types/currency.ts ....... +3 lines (new type added)
├── Last meaningful edit: src/checkout/tax.ts:84 (3:47 PM Friday)
├── Git stash: 1 entry ("experimental: flat tax approach — didn't work")
└── Uncommitted deletions: none
```

### 2. 你之前正在做的事情
```
ACTIVITY RECONSTRUCTION:
├── Primary task: Implementing multi-currency tax calculation
├── Current state: Mid-implementation
│   ├── calculateTax() is 60% complete (has happy path, missing edge cases)
│   ├── One test is passing (USD → USD, simple case)
│   ├── One test is FAILING: "should handle JPY zero-decimal currency"
│   │   └── Error: Expected 100, got 1.00 (decimal handling bug)
│   └── CurrencyType enum was just added but not yet used in calculateTax
├── Approach taken: Per-currency decimal precision lookup table
├── Approach rejected: Flat percentage (stashed, labeled "didn't work")
└── Likely next step: Fix decimal handling for zero-decimal currencies (JPY, KRW)
```

### 你之前的决策
```
DECISION CONTEXT (reconstructed from commits, comments, and stash):
├── Decided FOR: Lookup table approach for currency decimals
│   └── Evidence: Current implementation uses this pattern
├── Decided AGAINST: Flat percentage approach
│   └── Evidence: Stashed with note "didn't work"
├── Open question: How to handle currencies not in the lookup table
│   └── Evidence: TODO comment on line 67: "// fallback for unknown currencies?"
└── Unresolved: Whether to round before or after tax application
    └── Evidence: Both orderings present in different test cases
```

### 阻碍你继续工作的因素
```
BLOCKERS DETECTED:
├── ACTIVE: JPY test failing (zero-decimal currency handling)
│   └── This was likely the last thing you were working on
├── PENDING: No test for rounding edge cases
│   └── TODO on line 72: "// test rounding: 33.33% of $10?"
└── EXTERNAL: None detected
```

## 它的工作原理
```
Phase 1: ARTIFACT COLLECTION
├── Git state: branch, commits, diff, stash, reflog
├── File state: modification times, partial edits, cursor bookmarks
├── Test state: last test run results, which tests are failing and why
├── Comment state: TODOs, FIXMEs, HACKs, and inline questions
├── Terminal state: recent commands (build, test, run attempts)
└── Time analysis: order of modifications, last-touch timestamps

Phase 2: NARRATIVE RECONSTRUCTION
├── From artifacts, reconstruct the story:
│   ├── What task were you working on? (branch name, commit messages)
│   ├── What approach did you take? (code pattern analysis)
│   ├── What did you reject? (stashes, reverted changes, deleted code in diff)
│   ├── What was working? (passing tests, committed code)
│   ├── What was broken? (failing tests, incomplete functions)
│   └── What were you about to do? (partial code, TODOs, cursor position)
├── Sequence the story chronologically
└── Identify the exact point of interruption

Phase 3: CONTEXT BRIEFING
├── One-paragraph summary: "Here's where you left off"
├── Immediate next action: "You were about to..."
├── Active blockers: "This was stopping you..."
├── Open decisions: "You hadn't decided..."
└── Quick wins: "These are close to done..."

Phase 4: WARM-UP SUGGESTIONS
├── Recommend a re-entry point (easiest way back into flow)
├── Suggest running the failing test first (immediate feedback loop)
├── Flag anything that changed externally while you were away
│   └── (new commits on main, dependency updates, CI status)
└── Estimated time to full context recovery: X minutes
```

## 何时使用它：

- **每天早上**：在开始编写代码之前。
- 在任何超过30分钟的会议之后。
- 在切换代码分支或任务时。
- 在接手别人未完成的代码分支时。
- 休假或休息回来之后。
- 当同事询问“你在X处的工作进展到哪里了？”时。

## 不使用它的后果：

| 上下文丢失 | 浪费的时间 | 风险 |
|---|---|---|
| 忘记了自己放弃的解决方案 | 花30-60分钟重新探索无用的路径 | 重复犯已经犯过的错误 |
| 忘记了哪个测试失败了 | 花10-20分钟重新定位问题 | 误以为自己引入了新的错误 |
| 忘记了之前做出的设计决策 | 需要花费数小时重新调整代码 | 选择与之前的工作不一致的方案 |
| 忘记了外部环境的变化 | 变数很大 | 基于过时的假设继续工作 |
| 完全丢失上下文 | 花1-4小时 | 重新开始已经解决的问题 |

## 为什么它很重要：

上下文切换不仅仅是简单地关闭和打开文件。更重要的是**加载你的思维模型**——这个模型包含了你在特定代码领域中的所有决策、发现和意图。没有这个模型，你就像在自己的代码库中迷路的游客一样，无法高效地工作。

“上下文恢复”功能并不保存你的会话信息，而是保存你对代码的理解。它完全不依赖任何外部服务或API，仅通过Git和文件系统的操作来实现恢复。