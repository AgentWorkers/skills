---
name: work-receipt
version: 1.0.0
description: 它会生成一份详细的记录，列出你在编程会话中完成的所有工作：修改的文件、解决的问题、所做的决策、产生的工作量（即“债务”），以及第二天需要继续处理的任务。这正是“我只是整天在工作”与“这是我具体做了什么以及为什么这么做”的区别所在。这份记录非常适合在团队站会上使用，也便于在任务交接时展示自己的工作成果，同时还能让你自己确信自己确实完成了某些事情。
author: J. DeVere Cooley
category: everyday-tools
tags:
  - productivity
  - documentation
  - standups
  - tracking
metadata:
  openclaw:
    emoji: "🧾"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - everyday
      - productivity
---
# 工作记录

> “如果你无法用三句话解释自己今天完成了什么，那要么你什么都没做，要么你把所有事情都完成了。无论哪种情况，都需要一份‘工作记录’。”

## 功能介绍

当你的编码会话结束时，Work Receipt 会分析会话中的所有数据（如 Git 历史记录、文件变更、测试结果、终端命令等），并生成一份结构化的总结报告，内容包括：

1. **你完成了什么**（已交付的代码、修复的错误、编译成功的成果）
2. **你修改了哪些内容**（具体文件、修改的代码行数、代码架构的变更）
3. **你做了哪些决策**（以及决策的原因）
4. **你还剩下哪些未完成的任务**（待办事项、已知问题、下一步计划）
5. **这项工作花费了多长时间**（工作所花费的时间、代码的复杂度增加情况）

## 工作记录的生成方式
```
╔══════════════════════════════════════════════════════════════╗
║                       WORK RECEIPT                          ║
║                                                              ║
║  Session: Tuesday, March 3, 2026                            ║
║  Duration: 4h 22m (1:15 PM — 5:37 PM)                      ║
║  Branch: feature/multi-currency-checkout                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ACCOMPLISHED:                                               ║
║  ✓ Multi-currency tax calculation (USD, EUR, GBP, JPY)      ║
║  ✓ Zero-decimal currency handling (JPY, KRW)                ║
║  ✓ Tax rounding edge case for sub-cent amounts               ║
║  ~ Partial: Currency conversion caching (70% complete)       ║
║                                                              ║
║  CHANGED:                                                    ║
║  ├── Modified: 6 files (+184 lines, -47 lines)              ║
║  │   ├── src/checkout/tax.ts .......... +89 / -12           ║
║  │   ├── src/checkout/currency.ts ..... +42 / -8            ║
║  │   ├── src/types/currency.ts ........ +18 / -3            ║
║  │   ├── src/checkout/tax.test.ts ..... +24 / -6            ║
║  │   ├── src/checkout/currency.test.ts  +11 / -18           ║
║  │   └── src/config/rates.json ........ +0 / -0 (reformatted)║
║  ├── Created: 1 file                                         ║
║  │   └── src/checkout/decimal-precision.ts (29 lines)        ║
║  └── Commits: 4                                              ║
║      ├── "feat: multi-currency tax calculation"              ║
║      ├── "fix: zero-decimal currency handling (JPY/KRW)"     ║
║      ├── "fix: sub-cent rounding edge case"                  ║
║      └── "wip: currency conversion caching (incomplete)"     ║
║                                                              ║
║  DECISIONS MADE:                                             ║
║  ├── Used per-currency precision lookup (not flat decimal)   ║
║  │   Reason: JPY/KRW have 0 decimals, BHD has 3 decimals    ║
║  ├── Round after tax, not before                             ║
║  │   Reason: Rounding before creates up to 0.5% error        ║
║  └── Separate decimal-precision module (not inline)          ║
║      Reason: Reusable for display, export, and reporting     ║
║                                                              ║
║  TESTS:                                                      ║
║  ├── Added: 4 new tests                                      ║
║  ├── Modified: 2 existing tests                              ║
║  ├── Status: 23/23 passing ✓                                 ║
║  └── Coverage: 91% → 94% (+3%) for checkout/                ║
║                                                              ║
║  LEFT BEHIND:                                                ║
║  ├── TODO: Currency conversion cache TTL (hardcoded to 1h)   ║
║  ├── TODO: Add tests for BHD (3-decimal currency)            ║
║  ├── WIP: Caching layer ~70% done (needs invalidation logic) ║
║  └── DEBT: No test for concurrent currency conversions       ║
║                                                              ║
║  SESSION METRICS:                                            ║
║  ├── Complexity: Net +12 cyclomatic complexity               ║
║  ├── Debt: 1 new entry (concurrent test, ~2h to fix)         ║
║  ├── Dependencies: 0 new dependencies added                  ║
║  └── Breaking changes: 0                                     ║
║                                                              ║
║  STANDUP SUMMARY:                                            ║
║  "Implemented multi-currency tax calculation supporting      ║
║  22 currencies including zero-decimal (JPY/KRW). Fixed       ║
║  rounding edge case for sub-cent amounts. Currency conversion ║
║  caching is 70% done, will finish tomorrow."                 ║
╚══════════════════════════════════════════════════════════════╝
```

## 工作记录涵盖的内容

### 1. 完成的工作（来自 Git 提交记录和文件差异）
```
SOURCE:
├── Commit messages (especially conventional commit prefixes: feat, fix, refactor)
├── Diff analysis (what changed functionally, not just syntactically)
├── Test additions (new tests = new verified behavior)
└── Branch description / PR draft

CLASSIFICATION:
├── ✓ Complete: Committed, tested, ready for review
├── ~ Partial: Work in progress, documented but unfinished
├── ✗ Abandoned: Started but reverted or stashed
└── ⟳ Refactored: Changed structure without changing behavior
```

### 2. 你的决策（来自代码模式和注释）
```
DETECTION:
├── Stashed alternatives (you tried X, went with Y)
├── TODO/FIXME comments (you noted a decision to defer)
├── Reverted commits (you chose against something)
├── Code comments with "because", "instead of", "rather than"
└── Config changes (explicit choices about values/settings)
```

### 未完成的任务（来自代码的“进行中”状态）
```
DETECTION:
├── Uncommitted changes (work still in progress)
├── TODO/FIXME added during this session
├── Failing tests that were added but not yet fixed
├── Incomplete function signatures (return type is any/unknown)
├── Empty function bodies or placeholder implementations
└── WIP commits (literally "wip" in the message)
```

### 成本分析（来自代码指标）
```
METRICS:
├── Lines of code: net addition/reduction
├── Complexity: cyclomatic complexity change
├── Test coverage: percentage change
├── Dependencies: new libraries added
├── Debt: shortcuts taken, tests skipped, TODOs added
├── Files touched: total surface area of changes
└── Breaking changes: interface/schema modifications
```

## 工作记录的呈现形式

### 用于日常汇报的格式（三句话）
```
Yesterday: Implemented multi-currency tax calculation for 22 currencies.
Fixed zero-decimal currency handling and rounding edge cases.
Today: Will complete currency conversion caching and add BHD tests.
Blockers: None.
```

### 用于向同事交接工作的格式
```
HANDOFF: feature/multi-currency-checkout
├── STATUS: 85% complete
├── WHAT'S DONE: Tax calc works for all currencies, fully tested
├── WHAT'S LEFT: Caching layer needs invalidation logic (see TODO in currency.ts:42)
├── WATCH OUT FOR: JPY and KRW are zero-decimal — don't assume 2 decimal places
├── DECISIONS LOCKED: Round after tax, not before. Precision lookup table in decimal-precision.ts
├── OPEN QUESTIONS: Cache TTL — 1h is a guess, may need tuning in production
└── RUN: npm test -- checkout/ (should be 23/23 green)
```

### 用于编写 Pull Request（PR）的描述格式
```
## Multi-Currency Tax Calculation

Adds support for 22 currencies in the checkout tax calculation,
including zero-decimal currencies (JPY, KRW) and 3-decimal currencies (BHD).

### Changes
- New `decimal-precision.ts` module with per-currency precision lookup
- Updated `tax.ts` to use precision-aware calculation
- Fixed rounding: now rounds after tax application (not before)
- 4 new tests, 2 updated tests (91% → 94% coverage)

### Not Included
- Currency conversion caching (separate PR, in progress)
- Concurrent conversion tests (tracked as tech debt)
```

### 提交日志的整理
当你的提交记录混乱不堪时，Work Receipt 会建议你重新编写提交日志，使其更加清晰明了：
```
CURRENT COMMITS:
├── "wip"
├── "fix stuff"
├── "actually fix the thing"
└── "wip: caching maybe"

SUGGESTED REWRITE:
├── "feat: multi-currency tax calculation with precision lookup"
├── "fix: handle zero-decimal currencies (JPY, KRW) in tax calc"
├── "fix: round after tax application to prevent sub-cent errors"
└── "wip: currency conversion caching (invalidation pending)"
```

## 使用场景

- **每次工作会话结束后**：养成这个习惯。
- **在日常汇报之前**：只需 5 秒即可生成汇报内容，无需花费 5 分钟去回忆。
- **在创建 Pull Request 之前**：系统会自动生成报告描述。
- **在向同事交接工作之前**：提供结构化的交接信息，而非含糊的“代码在某个分支上”。
- **在冲刺结束时**：将每日的工作记录汇总到冲刺总结中。
- **当你觉得自己什么都没完成时**：这份记录可以证明事实并非如此。

## 工作记录的重要性

开发者往往低估了自己的工作成果，高估了未完成的任务量。如果没有工作记录，工作成果就变得难以被他人（包括经理和同事）以及你自己看到。Work Receipt 能让这些“看不见”的工作变得可见：每个决策都有记录，每一行代码都有出处，每个待办事项都有追踪。

Work Receipt 完全依赖于 Git 和文件系统的数据进行分析，无需任何外部依赖或 API 调用。