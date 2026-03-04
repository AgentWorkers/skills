---
name: peripheral-vision
version: 1.0.0
description: 监控相邻系统、上游依赖项以及下游用户端，以便及时发现可能影响您当前工作的任何变化——在这些变化导致问题发生之前就将其发现。就如同生物体的“周边视觉”能够检测到视野边缘的动静一样，这项技能能够检测到代码依赖关系范围内的任何异常变化。
author: J. DeVere Cooley
category: situational-awareness
tags:
  - dependency-monitoring
  - change-detection
  - context-awareness
  - proactive
metadata:
  openclaw:
    emoji: "👁️"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - cognitive
      - awareness
---
# 周边视野（Peripheral Vision）

> “你之所以会出错，并不是因为没有向前看，而是因为没有向旁边看。”

## 功能介绍

当你深入开发某个模块时，你的注意力会集中在当前正在编辑的代码上（即“中央视野”）。然而，导致问题出现的代码往往并不是你正在关注的那一部分，而是它旁边的代码：可能是上游服务改变了响应格式，或者是下游客户端发送了意外的输入数据，又或者是有人在你在开发某个功能时重构了某个共享工具。

“周边视野”功能会在你当前的开发环境中创建一个“情境感知场”，持续扫描你的注意力范围，并提醒你注意以下变化：
- 不在你正在编辑的文件中发生的变更；
- 但与你正在编辑的文件有依赖关系、交互频繁，或者你认为其稳定性可靠的文件中发生的变更。

## 感知模型

### 视野解剖结构

在人类视觉中：
- **中央视野**：位于视野中心的2°范围内，细节最为清晰，是你当前正在注视的区域。
- **周边视野**：位于中央视野周围的5°范围内，细节相对较少，但可以感知到一些信息。
- **盲点**：视野边缘的其他区域，无法感知到任何细节，但可以检测到运动或潜在的威胁。

在代码环境中：
| 区域        | 对应的代码部分                | “周边视野”的作用                        |
|-------------|------------------------|--------------------------------------|
| **中央视野**    | 你正在编辑的文件             | 无特殊作用（因为你已经在关注这部分代码了）            |
| **周边视野**    | 你的代码直接导入或调用的文件         | 监控这些文件的最新变更                    |
| **周边视野**    | 与你的代码有交互的文件（共享依赖项、下游客户端等） | 检测可能影响到你的变更                    |
| **盲点**      | 你没有直接感知到的文件（通过隐式渠道关联）     | 通过代码变更分析尝试检测这些文件的变更            |

## 六种感知渠道

### 渠道1：上游变化（Upstream Changes）
**监控对象**：你的代码导入或调用的库、模块和服务。

```
SCANS FOR:
├── Interface changes (new required params, removed fields, renamed exports)
├── Behavioral changes (same interface, different semantics)
├── Version bumps in dependencies that affect your used surface area
├── Deprecation warnings for functions you actively use
└── Changelog entries tagged "breaking" in your dependency tree
```

### 渠道2：下游影响（Downstream Influences）
**监控对象**：导入、调用或依赖于你的代码的其他代码。

```
SCANS FOR:
├── New consumers of your module you didn't know about
├── Consumers using your code in ways you didn't intend
├── Consumers that would break if you change your current interface
├── Test files in other modules that test your behavior (coupling signal)
└── Downstream code that reimplements your functionality (trust signal)
```

### 同模块内的变化（Sibling Changes）
**监控对象**：你所在模块或目录内最近被其他人修改的文件。

```
SCANS FOR:
├── Changes to shared utilities, helpers, or constants you use
├── Changes to configuration files that affect your module's behavior
├── New files that might conflict with or duplicate your current work
├── Refactors that changed naming conventions your code follows
└── Changes to test infrastructure or fixtures your tests depend on
```

### 数据结构变更（Schema Changes）
**监控对象**：数据库模式、API接口定义、protobuf格式、GraphQL类型等共享的数据结构。

```
SCANS FOR:
├── Column additions/removals in tables your code queries
├── Type changes in fields your code reads or writes
├── New constraints (NOT NULL, UNIQUE) that could cause your writes to fail
├── API version changes in services you consume
└── Protobuf/GraphQL field deprecations or renames
```

### 环境变化（Environmental Changes）
**监控对象**：基础设施、配置设置以及部署环境的变化。

```
SCANS FOR:
├── Changes to environment variables your code reads
├── Changes to Docker/container configurations
├── CI/CD pipeline modifications that affect your build/test/deploy
├── Infrastructure changes (new regions, changed timeouts, updated limits)
└── Changes to shared tooling (linter rules, formatter settings, build configs)
```

### 时间关联的变更（Temporal Neighbors）
**监控对象**：历史上与你的代码同时发生变化的其他文件。

```
SCANS FOR:
├── Files that have changed in the same commit as your files > 3 times
├── Files that have changed within 24h of your files > 5 times
├── Files that have triggered the same CI failures as your files
└── Files that share the same bug-fix pattern as your files
```

## 工作原理

```
Phase 1: CONTEXT CAPTURE
├── Identify the foveal zone (files currently open/modified)
├── Trace parafoveal zone (direct dependencies, both import and export)
├── Map peripheral zone (transitive deps, shared resources, co-changers)
└── Identify blind spots (connected through implicit channels)

Phase 2: CHANGE DETECTION
├── For each zone, detect changes since your work started:
│   ├── Git: commits by others to files in your awareness field
│   ├── Schema: migrations or type definition changes
│   ├── Config: environment or infrastructure changes
│   └── Dependency: upstream version bumps or changelog entries
├── Classify each change by relevance to your current work
└── Score impact probability (how likely this affects you)

Phase 3: ALERT TRIAGE
├── Filter out noise (changes with < 20% impact probability)
├── Classify remaining by urgency:
│   ├── STOP: Your current work may be invalidated
│   ├── REVIEW: Your current work should account for this
│   ├── NOTE: Awareness-only, no action needed yet
│   └── EMERGING: Pattern forming, not yet actionable
└── Generate contextual alert with specific implications for your work

Phase 4: CONTINUOUS MONITOR
├── Re-scan periodically (configurable interval)
├── Update awareness field as your focus shifts
├── Accumulate pattern data for temporal neighbor analysis
└── Fade old alerts that are no longer relevant
```

## 警报格式

```
╔══════════════════════════════════════════════════════════════╗
║               PERIPHERAL VISION ALERT                       ║
║          Context: You're working on src/checkout/            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔴 STOP (1)                                                 ║
║  ├── [Schema] payments table: 'currency' column type changed ║
║  │   from varchar(3) to enum — your INSERT will fail         ║
║  │   Changed by: @devB in migration 2025_03_01_alter_pmts    ║
║  │   Action: Update PaymentBuilder to use enum values        ║
║                                                              ║
║  🟡 REVIEW (2)                                               ║
║  ├── [Upstream] CartService.getTotal() now returns            ║
║  │   {amount, currency} instead of just amount               ║
║  │   Changed by: @devC in commit a8f3d2e (2h ago)            ║
║  │   Action: Destructure correctly or your amounts are objects║
║  │                                                           ║
║  ├── [Sibling] src/checkout/utils.ts was refactored          ║
║  │   formatPrice() renamed to formatCurrency()               ║
║  │   Changed by: @devA in commit b9c4e1f (4h ago)            ║
║  │   Action: Update your imports before pushing              ║
║                                                              ║
║  🔵 NOTE (1)                                                 ║
║  ├── [Temporal] test/fixtures/cart-data.json was updated     ║
║  │   This file co-changes with checkout/ 73% of the time     ║
║  │   Your checkout tests may need updated fixtures            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## 使用场景

- 在开始一个新的功能分支时（建立你的“情境感知场”）；
- 在提交代码之前（检查在你专注于当前工作期间周围发生了哪些变化）；
- 在提交 pull request 之前（确保你的代码能够处理这些并行发生的变更）；
- 从主代码库拉取代码后（了解哪些变更可能影响到你的代码）；
- 当持续集成（CI）构建失败时（判断问题是由于你的代码引起的，还是由于其他地方的变更引起的）。

## 重要性

最令人沮丧的错误往往不是你主动引入的，而是那些在你专注于自己工作的过程中，在你原本无需关注的代码部分出现的错误。等到你发现这些问题时，往往已经基于错误的假设进行了进一步的开发。

“周边视野”功能并不会替代细致的代码审查，但它能为你的代码审查提供额外的“周边感知”能力——让你不仅能看到哪些地方发生了变化，还能了解这些变化对整个系统的影响。

该功能完全不依赖任何外部服务或API调用，仅通过 Git 和静态分析来实现。