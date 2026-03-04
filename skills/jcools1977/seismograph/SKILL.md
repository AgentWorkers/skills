---
name: seismograph
version: 1.0.0
description: 在实施任何更改之前，该工具能够预测其可能产生的连锁反应。它能够模拟修改如何在代码库中传播：哪些部分会出错，哪些部分会受到影响，哪些部分会发生变化——就像地震仪记录地震能量如何通过不同密度的地质层和断层线传播一样。
author: J. DeVere Cooley
category: change-intelligence
tags:
  - impact-analysis
  - change-prediction
  - risk-assessment
  - pre-commit
metadata:
  openclaw:
    emoji: "📊"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - cognitive
      - risk
---
# 地震仪（Seismograph）

> “地震的破坏程度并不是在震中决定的，而是由震中与周围环境之间的地质条件决定的——包括断层线、土壤成分以及基岩的深度。代码的修改也是如此。”

## 地震仪的作用

在进行任何修改之前，地震仪会首先绘制出**传播路径**——即所有会受到影响的函数、模块、测试、数据类型以及下游系统。它关注的不仅仅是“哪些代码调用了这个函数”（这通常是集成开发环境（IDE）的工作），还包括：

- 其他地方对这段代码有哪些**假设**？
- 有哪些**测试**在验证你即将修改的代码行为？
- 有哪些**文档**描述了这段代码应有的行为？
- 有哪些**下游系统**依赖于你即将修改的输出结果？
- 这段代码有哪些**副作用**，尽管这些副作用并非最初设计时就预料到的？

## 地震模型（Seismic Model）

### 地震的构成与代码的对应关系

| 地震概念 | 代码对应部分 |
|---|---|
| **震中** | 你正在修改的代码行 |
| **断层线** | 接口边界、类型契约、API接口 |
| **P波**（第一种波，压缩波） | 直接调用者/导入者——会立即感受到变化 |
| **S波**（第二种波，剪切波） | 间接依赖者——通过中间层感受到变化 |
| **表面波**（最慢的一种波，破坏性最强） | 依赖于修改后代码行为的系统——会在后续运行中受到影响 |
| **地震波传播速度** | 变更的传播速度（耦合度越高，传播速度越快） |
| **液化** | 接口定义不清晰，在意外变化下可能导致系统崩溃 |
| **余震** | 由于修复主要问题而引发的次要错误 |
| **震级** | 变更的范围 × 结合度 × 下游系统的受影响范围 |
| **烈度**（因位置而异） | 变化的影响程度取决于距离和中间系统的架构 |

## 波的类型及其影响

### P波：直接影响
- **传播方式**：直接调用者、导入者以及直接使用该代码的部分。
- **传播速度**：立即生效。这类问题通常在编译或导入时就能被发现。
- **影响程度**：通常较小——可以通过静态分析发现。

```
ANALYSIS:
├── Every file that imports the changed module
├── Every function that calls the changed function
├── Every type that extends or implements the changed type
├── Every test that directly tests the changed behavior
└── Estimated: files affected, lines potentially impacted
```

### S波：间接影响
- **传播方式**：依赖于被修改代码的间接使用者。
- **传播速度**：较慢。这类问题通常在运行时或集成测试中发现。
- **影响程度**：中等——如果存在集成测试的话，通常能够被发现。

```
ANALYSIS:
├── Transitive importers (A uses B uses Changed)
├── Functions that consume the output of changed functions
├── Systems that read data written by changed code
├── Configurations parsed by changed logic
└── Estimated: propagation depth, weakest intermediary
```

### 表面波：副作用影响
- **传播方式**：依赖于被修改代码行为的系统，但并未直接调用该代码。例如事件监听器、数据库触发器、日志解析器、缓存数据、文件监控工具等。
- **传播速度**：最慢。这类问题可能在生产环境中数天或数周后才会显现。
- **影响程度**：最高——在引发问题之前可能难以察觉。

```
ANALYSIS:
├── Event subscribers that react to events emitted by changed code
├── Monitoring/alerting rules that pattern-match on changed behavior
├── Cached values computed from changed code's output
├── Database triggers fired by changed code's queries
├── Log parsers/aggregators that expect changed code's log format
├── Downstream services that learned (not contracted) the output shape
└── Estimated: probability of surface-wave damage, detection difficulty
```

## 震级等级

| 震级 | 描述 | 典型影响 |
|---|---|---|
| **1.0 - 2.0** | 微震。内部重构，没有接口变化。 | 影响范围有限，不会引发其他问题。 |
| **2.0 - 3.0** | 轻微调整。实现细节发生变化，但接口保持不变。 | 只影响直接使用该代码的部分。可能需要更新测试。 |
| **3.0 - 4.0** | 中等程度。接口发生变化，但语义保持一致。 | P波和S波都会受到影响，直接使用者会受到影响。 |
| **4.0 - 5.0** | 显著调整。公共接口的语义发生变化。 | 所有类型的代码都会受到影响，集成测试可能会失败。 |
| **5.0 - 6.0** | 重大调整。行为发生显著变化，影响下游系统。 | 需要跨团队协调部署。 |
| **6.0 - 7.0** | 严重调整。数据结构或契约发生变化。 | 需要迁移数据，涉及多个团队的协作。 |
| **7.0以上** | 灾难性调整。架构假设发生根本性变化。 | 对整个系统产生广泛影响，必须分阶段部署。 |

## 地质调查：修改前的分析

```
Phase 1: EPICENTER MAPPING
├── Identify exact lines being changed
├── Classify change type:
│   ├── Rename (lowest risk)
│   ├── Signature change (medium risk)
│   ├── Behavioral change (high risk)
│   ├── Removal (highest risk)
│   └── Addition (usually safe, unless overloading existing names)
└── Determine magnitude baseline

Phase 2: WAVE PROPAGATION
├── P-Wave analysis:
│   ├── Static dependency graph traversal
│   ├── Type system impact (what breaks at compile time?)
│   └── Direct test impact (what tests fail?)
├── S-Wave analysis:
│   ├── Transitive dependency traversal (2-3 hops)
│   ├── Data flow tracing (output consumed where?)
│   └── Integration test impact
└── Surface-Wave analysis:
    ├── Event/message subscribers
    ├── Database triggers and views
    ├── Monitoring and alerting rules
    ├── Cache invalidation implications
    └── Log format dependencies

Phase 3: FAULT LINE ASSESSMENT
├── For each wave path, assess intervening architecture:
│   ├── Strong boundaries (typed interfaces, contracts) → wave dampened
│   ├── Weak boundaries (duck typing, convention) → wave amplified
│   ├── No boundary (direct coupling) → wave passes through
│   └── Fault lines (known fragile points) → wave magnified
└── Adjust intensity at each affected location

Phase 4: AFTERSHOCK PREDICTION
├── If you fix the primary breakage, what secondary breaks occur?
├── Which fixes are "safe" (localized) vs "cascading" (cause more waves)?
├── Estimated total change set: original change + all required adaptations
└── Is the total change set larger than the original intention warrants?

Phase 5: SEISMOGRAPH REPORT
├── Magnitude and intensity map
├── Prioritized list of affected locations
├── Recommended change strategy (direct, staged, behind flag)
├── Aftershock forecast
└── Go / staged-rollout / reconsider recommendation
```

## 输出格式

```
╔══════════════════════════════════════════════════════════════╗
║                  SEISMOGRAPH ANALYSIS                       ║
║    Proposed: Rename User.email → User.emailAddress           ║
║    Magnitude: 4.7 (Significant)                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  EPICENTER: src/models/user.ts:24                            ║
║                                                              ║
║  P-WAVES (Direct Impact):                                    ║
║  ├── 14 files import User and access .email                  ║
║  ├── 8 tests assert on .email                                ║
║  ├── 2 API serializers include 'email' key                   ║
║  └── Compile-time breakage: YES (TypeScript will catch)      ║
║                                                              ║
║  S-WAVES (Indirect Impact):                                  ║
║  ├── 3 services consume User API response with 'email' field ║
║  ├── 1 webhook payload includes 'email' (external consumers) ║
║  ├── 1 CSV export uses 'email' as column header              ║
║  └── Runtime breakage: LIKELY in downstream services         ║
║                                                              ║
║  SURFACE WAVES (Side-Effect Impact):                         ║
║  ├── Elasticsearch index maps 'email' field → search breaks  ║
║  ├── Monitoring alert matches on "email" in log output       ║
║  ├── 2 Zapier integrations reference 'email' field           ║
║  └── Detection difficulty: HIGH (weeks before discovery)     ║
║                                                              ║
║  AFTERSHOCK FORECAST:                                        ║
║  ├── Fixing the 14 P-wave files triggers 0 new waves ✓      ║
║  ├── Fixing the API serializer triggers 3 client-side breaks ║
║  ├── Fixing the webhook requires partner notification        ║
║  └── Total change set: 24 files + 3 external systems        ║
║                                                              ║
║  FAULT LINES CROSSED: 2                                      ║
║  ├── API boundary (typed but externally consumed)            ║
║  └── Webhook contract (no versioning, external consumers)    ║
║                                                              ║
║  RECOMMENDATION: STAGED ROLLOUT                              ║
║  1. Add emailAddress as alias, keep email (backward compat)  ║
║  2. Migrate internal consumers to emailAddress               ║
║  3. Notify external consumers, add deprecation warning       ║
║  4. Remove email after deprecation period                    ║
╚══════════════════════════════════════════════════════════════╝
```

## 何时需要使用地震仪

- 在对任何公共接口、API或共享数据类型进行修改之前
- 在更改跨越模块边界的名称之前
- 在修改数据库模式或数据传输格式之前
- 在删除任何函数、字段或参数之前
- 当有人认为“这只是一个简单的修改”时（但实际上往往并非如此）
- 在进行代码审查（PR）时，评估修改可能带来的全面影响

## 为什么这很重要

生产环境中问题的主要来源并非代码本身，而是那些**传播范围超出预期的修改**。比如一个看似简单的重命名操作破坏了Webhook的运行；一个看似微小的优化改变了系统的时序保证；一个本应清理的代码重构却移除了下游系统依赖的字段。

地震仪并不能阻止修改，但它能防止**意外情况的发生**。因为问题从来不是“我们是否应该进行这个修改”，而是“我们是否理解这个修改会带来什么影响？”

地震仪完全依赖静态分析和历史数据，不涉及任何外部依赖或API调用。