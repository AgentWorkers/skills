---
name: fossil-record
version: 1.0.0
description: 这是一个名为“Git Archaeology Engine”的工具，它的核心功能是探究代码背后的“原因”——并非简单地记录哪些内容发生了变化，而是深入分析哪些压力、失败以及决策转变促使代码库发展成当前的样子。该工具以类似古生物学家研究沉积层的方式来解读提交历史记录，旨在理解那些塑造了代码库现状的各种因素。
author: J. DeVere Cooley
category: code-archaeology
tags:
  - git-analysis
  - code-history
  - decision-reconstruction
  - archaeology
metadata:
  openclaw:
    emoji: "🦴"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - cognitive
      - history
---
# 化石记录（Fossil Record）

> “代码告诉你系统能做什么，而历史则告诉你系统是如何‘存活’下来的。”

## 它的功能

`git blame` 可以告诉你哪个人修改了某一行代码；`git log` 可以告诉你修改的时间；而 Fossil Record 则通过分析整个提交历史中的模式，来揭示代码库演变过程中的压力和决策，从而解释代码为何会变成现在的样子。

每一行代码都是某种决策的结果。大多数决策并没有被记录下来，但它们留下了“化石”——比如提交模式、代码回退的顺序、紧急修复的集中出现、重构的浪潮，以及无数微小决策累积而成的最终架构。

## 地质模型（Geological Model）

Fossil Record 将你的 Git 历史视为一份地质记录，其中包含不同的“地层”和“时代”：

| 地质概念 | 代码对应部分 |
|---|---|
| **沉积层** | 稳定发展的时期（新增功能的提交） |
| **断层线** | 大规模的重构、代码重写或架构变更 |
| **撞击坑** | 应急修复、临时解决方案或代码回退 |
| **化石层** | 长时间未发生变化的代码（是否已经稳定或被遗忘？） |
| **侵蚀模式** | 代码逐渐偏离原始设计意图 |
| **灭绝事件** | 被删除的模块、被弃用的功能、被移除的依赖关系 |
| **适应性辐射** | 在重大变更后出现的快速多样化（新的抽象层催生了多种实现方式） |

## 八种分析模式（Eight Excavation Modes）

### 1. 压力分析（Pressure Analysis）
**问题：** 是哪些外部因素影响了这段代码的演变？

通过分析提交信息、时间分布和代码变化的聚集模式，来识别：
- **截止日期压力**：提交频率在某个日期前加快，之后突然停止；
- **突发事件压力**：紧急修复 → 修复 → 再修复 → 回退 → 再次修复的循环；
- **利益相关者压力**：功能请求导致提交频繁中断；
- **技术债务压力**：开始但被放弃、后又重新启动的重构工作。

```
Output: Timeline of external pressures with their impact on code quality.
Example: "Between March 3-17, commit velocity tripled and test coverage
dropped from 84% to 61%. Three hotfixes followed in the next week.
This region of code still carries the scars of that deadline."
```

### 2. 决策重建（Decision Reconstruction）
**问题：** 这里做出了哪些决策？有哪些替代方案被考虑过？

分析：
- 被回退的提交（尝试过但被否决的方案）；
- 被创建但从未合并的分支（被放弃的实现方式）；
- 提及替代方案的注释（例如：“我们可以使用 X，但……”）；
- 同一功能的多次迭代实现过程。

```
Output: Decision tree showing what was tried, what stuck, and what was abandoned.
Example: "Authentication was implemented 3 times:
  v1 (session-based, commits a1b2..c3d4, reverted)
  v2 (JWT, commits e5f6..g7h8, lived 4 months)
  v3 (OAuth2, commits i9j0..k1l2, current)
  Pressure: v1→v2 driven by scaling issues. v2→v3 driven by SSO requirement."
```

### 3. 热点区域分析（Hotspot Archaeology）
**问题：** 为什么这段代码特别不稳定？

深入探究代码变化的原因，而不是简单地判断“这段代码修改频繁”。

```
CHANGE TAXONOMY:
├── Bug Fix: Same function modified to fix different bugs (fragile design)
├── Feature Accretion: Function grows as features are bolted on (missing abstraction)
├── Config Churn: Constants/thresholds repeatedly adjusted (unclear requirements)
├── Refactor Oscillation: Code restructured back and forth (no consensus on design)
└── Dependency Turbulence: Changes driven by upstream library updates (fragile coupling)
```

### 4. 代码灭绝映射（Extinction Mapping）
**问题：** 这里曾经有什么功能？为什么它们被移除了？

通过 Git 历史追踪被删除的代码，了解其被移除的原因：
- 它是被替换了吗？被什么替换了？
- 是逐渐被弃用还是突然被删除的？
- 它的移除是否引发了后续问题（是否有修复代码引用了被删除的模块）？
- 是否还有依赖于被删除模块的代码仍然存在？

```
Output: Extinction timeline showing what disappeared, when, and what it left behind.
Example: "The 'recommendations' module was deleted in commit x1y2z3 (June 2024).
  3 orphaned database tables still exist.
  2 API routes still reference recommendation types in their schemas.
  1 test file still imports a mock of the recommendation engine."
```

### 5. 代码年代测定（Sediment Dating）
**问题：** 这段代码的实际年龄是多少？它是否得到了维护，还是仅仅被保留了下来？

针对每个模块/文件，确定：
- **创建时间**：它最初是什么时候创建的？
- **最后一次有意义的修改**：不仅仅是格式上的变化，而是实际功能的修改；
- **维护频率**：它是否定期更新，还是几乎未被修改？
- **维护者多样性**：是否只有一个人负责维护它？
- **时代分类**：这段代码属于哪个架构阶段？

```
Output: Age map of the codebase with era boundaries.
Example:
  src/auth/     Born: 2023-01, Last modified: 2025-11, Era: "Current" (3rd gen)
  src/utils/    Born: 2021-06, Last modified: 2022-03, Era: "Founding" (1st gen)
  src/payments/ Born: 2024-08, Last modified: 2024-08, Era: "Growth" (2nd gen)
  ⚠️ src/utils/ hasn't been meaningfully modified in 3 years. Fossil bed.
```

### 6. 架构断层检测（Fault Line Detection）
**问题：** 代码库中的重大架构变化在哪里？

通过识别以下行为来发现重大的架构转变：
- 大规模的文件重命名或移动；
- 依赖关系的更换（从库 A 更改为库 B）；
- 目录结构的调整；
- 构建系统、框架或部署目标的变更。

```
Output: Fault line map showing architectural eras and their boundaries.
Example: "3 major fault lines detected:
  1. [2022-09] Monolith → microservices split (142 files moved)
  2. [2023-06] REST → GraphQL migration (89 files modified)
  3. [2024-03] JavaScript → TypeScript conversion (204 files renamed)
  Warning: Fault line #2 is incomplete. 23 endpoints still REST."
```

### 7. 开发者分布分析（Author Topology）
**问题：** 知识是如何分布的？哪些领域存在知识缺口？

映射哪些开发者负责了哪些代码模块，并识别：
- **知识垄断**：只有一个人负责修改的领域；
- **知识转移**：新开发者接手某个领域时的情况；
- **知识空白**：所有开发者都离开的领域；
- **协作模式**：哪些领域有多个开发者共同参与开发。

```
Output: Knowledge topology map with risk assessment.
Example: "src/billing/ — ALL 247 commits by developer X (last active: 2024-01).
  Developer X is no longer on the team.
  No other contributor has ever modified this module.
  Knowledge void. Recommend: dedicated onboarding session for this module."
```

### 8. 进化轨迹分析（Evolution Trajectory）
**问题：** 代码库的未来发展方向是什么？

根据历史模式预测：
- 哪些领域正在积极发展（提交频率和多样性都在增加）；
- 哪些领域正在停滞（修改减少，开发者流失）；
- 哪些架构模式正在扩张或收缩；
- 下一次可能的“灭绝事件”或“架构断层”会是什么。

```
Output: Trajectory forecast based on historical momentum.
Example: "The codebase is trending toward:
  ✓ Full TypeScript adoption (92% converted, ~2 months to completion)
  ✓ GraphQL as primary API layer (78% migrated)
  ⚠ Growing divergence between /api and /services naming conventions
  ⚠ Test coverage declining in modules > 2 years old (neglect pattern)"
```

## 集成（Integration）

```
Invoke Fossil Record when:
├── Joining a new project      → Run full geological survey
├── Before modifying old code  → Run sediment dating + decision reconstruction
├── After an incident          → Run pressure analysis on the affected area
├── During architecture review → Run fault line detection + evolution trajectory
├── When someone asks "why?"   → Run decision reconstruction on that specific area
└── Onboarding new developers  → Generate the complete evolutionary narrative
```

## 输出结果：地质调查报告（Output: The Geological Survey）

```
╔══════════════════════════════════════════════════════════════╗
║                 FOSSIL RECORD: GEOLOGICAL SURVEY            ║
║                 Repository: acme-platform                   ║
║                 History depth: 3 years, 4,721 commits       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ERAS IDENTIFIED: 3                                          ║
║  ├── Founding (2022-01 → 2022-09): Monolith, Express, JS    ║
║  ├── Growth (2022-09 → 2024-03): Microservices, REST, JS/TS ║
║  └── Current (2024-03 → now): Microservices, GraphQL, TS    ║
║                                                              ║
║  FAULT LINES: 3 major, 7 minor                              ║
║  IMPACT CRATERS: 12 incidents (3 P0, 5 P1, 4 P2)           ║
║  FOSSIL BEDS: 4 modules unchanged > 18 months               ║
║  KNOWLEDGE VOIDS: 2 modules (all authors departed)          ║
║  EXTINCTION EVENTS: 8 modules deleted, 3 left artifacts     ║
║                                                              ║
║  TRAJECTORY: Healthy evolution with 2 risk areas             ║
╚══════════════════════════════════════════════════════════════╝
```

## 它的重要性（Why It Matters）

代码审查关注的是“现在”，测试验证的是“预期结果”；而 Fossil Record 则揭示了“过去”。因为一个不了解自己历史的代码库注定会重复过去的错误。

**特点：**
- 完全依赖 Git 数据进行分析；
- 不使用任何外部 API 或云服务；
- 免费使用。