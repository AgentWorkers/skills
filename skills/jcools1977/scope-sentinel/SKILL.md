---
name: scope-sentinel
version: 1.0.0
description: 该工具会监控你的编程会话，当你的工作偏离了最初设定的任务方向、转而进行与任务无关的修改时，它会及时发出警报。这就好比编程领域的“GPS导航系统”——它会发现你走错了方向，告诉你偏离了多远，并在你对代码库进行了大量修改之前，帮助你重新回到正确的开发路径上。
author: J. DeVere Cooley
category: everyday-tools
tags:
  - focus
  - scope-management
  - productivity
  - discipline
metadata:
  openclaw:
    emoji: "🎯"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - everyday
      - productivity
---
# Scope Sentinel

> “最昂贵的代码行，往往是那些本不必编写的代码；最昂贵的重构，往往是在你已经开始某项工作时进行的。”

## 它的功能

你坐下来准备修复结账流程中的一个漏洞。两小时后，你重新格式化了认证模块，为三个工具文件添加了类型定义，重命名了一个数据库列，并升级了一个依赖项。然而，那个漏洞依然存在。

Scope Sentinel 会监控你实际在做什么，并将你的实际操作与你原本计划要做的操作进行对比。当两者之间的差异过大时，它会发出警报——不是为了阻止你继续工作，而是为了让这种偏离变得显而易见，这样你才能做出明智的决策。

## 偏离模型

### 范围定义
在任务开始时，你的工作范围由以下内容定义：

```
SCOPE ANCHOR:
├── Task statement: "Fix checkout failing for international addresses"
├── Target files: src/checkout/address.ts, src/checkout/validation.ts
├── Target behavior: International addresses should pass validation
├── Branch name: fix/international-address-checkout
└── Estimated files to touch: 2-4
```

### 偏离检测
在工作过程中，每一处文件修改都会被分类：

| 分类 | 描述 | 例子 |
|---|---|---|
| **与任务相关** | 直接针对任务本身进行的修改 | 修复地址验证的正则表达式 |
| **相关但合理** | 与任务相关，可以包含在内的修改 | 更新地址验证的测试代码 |
| **偏离主题** | 代码领域相同，但关注点不同 | 为结账模块添加类型定义 |
| **完全偏离** | 代码领域不同，关注点也不同 | 重构认证模块 |
| **陷入无底洞** | 在处理与任务相关的工作时引发的深度修改 | 因发现依赖项过时而进行升级 |

### 偏离程度判断

```
ON-SCOPE ──── ADJACENT ──── TANGENTIAL ──── DRIFT ──── RABBIT HOLE
   ✓              ✓             ⚠             🔴           🕳️
 "This is       "This is      "This is      "This is     "What year
  the fix"      part of       related but    a different   is it?"
                 the fix"     not the fix"   task"
```

## 工作原理

```
Phase 1: ANCHOR
├── Capture the task statement (from branch name, commit message, or explicit declaration)
├── Identify the target area of the codebase
├── Establish the scope boundary (files, modules, behaviors)
└── Set drift tolerance (tight, normal, or exploratory)

Phase 2: MONITOR
├── For every file modification, classify:
│   ├── Is this file in the target area?
│   ├── Does this change relate to the stated task?
│   ├── Is this change necessary for the task to succeed?
│   └── Would this change make sense as a separate commit/PR?
├── Track accumulated drift:
│   ├── Files touched outside scope
│   ├── Lines changed outside scope
│   └── Time spent outside scope
└── Track scope expansion events (when you discover the task is bigger than expected)

Phase 3: ALERT
├── When drift accumulates past threshold:
│   ├── Name the drift ("You've started refactoring auth — this is unrelated to checkout")
│   ├── Quantify it ("4 files, 87 lines, ~25 minutes of off-scope work")
│   ├── Offer choices:
│   │   ├── STASH: Save off-scope changes for a separate task
│   │   ├── COMMIT SEPARATELY: Make a separate commit for the off-scope work
│   │   ├── EXPAND SCOPE: Acknowledge the scope grew (with justification)
│   │   └── CONTINUE: You're aware and choosing to continue
│   └── Log the decision for later review
└── Resume monitoring with updated scope (if expanded)

Phase 4: SESSION SUMMARY
├── At end of session, report:
│   ├── Time on-scope vs. time drifted
│   ├── Files changed on-scope vs. off-scope
│   ├── Drift events and how they were resolved
│   └── Suggested follow-up tasks for off-scope discoveries
```

## 警报格式

```
╔══════════════════════════════════════════════════════════════╗
║              SCOPE SENTINEL: DRIFT DETECTED                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  YOUR TASK: Fix checkout for international addresses         ║
║                                                              ║
║  DRIFT:                                                      ║
║  You've been modifying src/auth/middleware.ts for 18 minutes.║
║  This file is not related to checkout or address validation. ║
║                                                              ║
║  HOW YOU GOT HERE:                                           ║
║  checkout/address.ts → noticed untyped import                ║
║  → opened utils/types.ts to add types                        ║
║  → noticed auth/middleware.ts also uses these types           ║
║  → started "fixing" auth types too                           ║
║                                                              ║
║  ACCUMULATED OFF-SCOPE:                                      ║
║  ├── 3 files outside checkout/                               ║
║  ├── 47 lines of changes unrelated to the bug                ║
║  └── ~18 minutes of drift                                    ║
║                                                              ║
║  OPTIONS:                                                    ║
║  [1] STASH off-scope changes, return to checkout bug         ║
║  [2] COMMIT SEPARATELY ("add types to auth middleware")      ║
║  [3] EXPAND SCOPE (justify: "types are prerequisite")        ║
║  [4] CONTINUE (I know, I'll wrap up soon)                    ║
╚══════════════════════════════════════════════════════════════╝
```

## 会话总结

```
╔══════════════════════════════════════════════════════════════╗
║                SCOPE SENTINEL: SESSION REPORT                ║
║            Task: Fix international address checkout          ║
║            Duration: 2h 14m                                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  FOCUS SCORE: 68/100                                         ║
║                                                              ║
║  TIME BREAKDOWN:                                             ║
║  ├── On-scope:   1h 22m (62%)  ████████████░░░░░░░░         ║
║  ├── Adjacent:      18m (13%)  ██░░░░░░░░░░░░░░░░░░         ║
║  ├── Tangential:    16m (12%)  ██░░░░░░░░░░░░░░░░░░         ║
║  └── Drift:         18m (13%)  ██░░░░░░░░░░░░░░░░░░         ║
║                                                              ║
║  DRIFT EVENTS: 2                                             ║
║  ├── Auth middleware typing (stashed → separate task)        ║
║  └── Utility function rename (committed separately)          ║
║                                                              ║
║  FOLLOW-UP TASKS GENERATED:                                  ║
║  ├── "Add TypeScript types to auth middleware"                ║
║  └── "Rename formatAddress → formatPostalAddress globally"   ║
║                                                              ║
║  TASK STATUS: Bug fixed. PR ready.                           ║
╚══════════════════════════════════════════════════════════════╝
```

## 偏离容忍模式

| 模式 | 阈值 | 适用场景 |
|---|---|---|
| **严格** | 当有1个与任务无关的文件被修改，或偏离时间达到5分钟时触发警报 | 修复漏洞、紧急修复、时间敏感的任务 |
| **正常** | 当有3个与任务无关的文件被修改，或偏离时间达到15分钟时触发警报 | 开发新功能、常规开发 |
| **探索性** | 当有6个与任务无关的文件被修改，或偏离时间达到30分钟时触发警报 | 重构代码、进行调查、学习新的代码库 |
| **关闭** | 不触发警报 | 自由探索、原型设计、创造性开发 |

## 何时使用

- 在开始每个专注的任务时：设定你的工作范围。
- 在修复漏洞时：此时范围偏离的成本最高。
- 在面临截止日期时：每偏离一分钟都会造成损失。
- 当你发现自己说出“我在做这个的时候……”（典型的偏离行为）时。
- 在代码审查准备阶段：确保你的 Pull Request（PR）是围绕任务核心展开的。

## 为什么这很重要

范围偏离并非懒惰的表现，而是开发者思维方式的自然结果。发现问题后，你想要立即修复它——这种冲动是有生产力的。但如果不受控制，原本只需30分钟就能解决的漏洞修复，可能会变成一个涉及15个文件的、难以审查的4小时长Pull Request。

Scope Sentinel 并不会阻止你进行额外的工作，而是确保这些额外的工作是经过深思熟虑的，而非无意识的。

**特点：**
- 完全不依赖外部服务或API调用。
- 仅通过监控文件变更来工作。