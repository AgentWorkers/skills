---
name: mspot-generator
description: 创建一页的战略对齐文档，内容包括：使命、战略、项目、未完成的事项以及跟踪机制。这些文档有助于明确团队将要做的事情以及不能做的事情。当用户提到“mspot”、“战略计划”、“季度计划”、“我们没有在做什么”、“未完成的事项”、“团队对齐”、“OKR的替代方案”、“优先级”或“我们应该关注什么”时，可以使用这些文档。
---

# MSPOT生成器

## 什么是MSPOT？

MSPOT是一种用于清晰呈现企业战略的一页文档（源自HubSpot的概念）：
- **使命（Mission）**：我们存在的理由（通常不会频繁更改）
- **战略（Strategy）**：我们如何在当前阶段取得成功
- **项目（Projects）**：我们重点投资的3-5个关键项目
- **未涉及的事项（Omissions）**：我们明确不打算做的事情
- **跟踪指标（Tracking）**：我们如何衡量成功

## MSPOT为何有效？

1. **明确“未涉及的事项”**：明确表示“不”做某些事情更加困难，但同时也更有价值。
2. **限制项目数量**：最多只列出3-5个项目，避免资源分散。
3. **一页呈现**：如果内容无法容纳在一页内，说明战略不够清晰。
4. **可追踪性**：仅包含对决策有实际帮助的指标。

## 输出格式

```
═══════════════════════════════════════════════
MSPOT: [Name]
Period: [Timeframe] | Owner: [Person]
═══════════════════════════════════════════════

MISSION: [One sentence: Why this exists]

STRATEGY: [2-3 sentences: How we'll win]

PROJECTS (3-5 max):
1. [Name] - Outcome: [X] - Owner: [Y] - Due: [Z]
2. [Name] - Outcome: [X] - Owner: [Y] - Due: [Z]
3. [Name] - Outcome: [X] - Owner: [Y] - Due: [Z]

OMISSIONS:
✗ NOT [X] - Because: [reason]
✗ NOT [Y] - Because: [reason]

TRACKING:
Lead: [Activity] → Target: [X]
Lag: [Result] → Target: [Y] by [date]
═══════════════════════════════════════════════
```

## 关键问题

| 部分        | 问题                          |
|-------------|------------------------------|
| **使命**       | “如果我们成功了，会发生什么变化？”                |
| **战略**       | “我们的竞争优势是什么？”                   |
| **项目**       | “如果只能选择3个项目，应该选择哪些？”             |
| **未涉及的事项** | “有哪些事情我们可能会想做，但实际上不应该做？”         |
| **跟踪指标**     | “哪个指标能告诉我们我们是否取得了成功？”           |

## 集成方式

MSPOT可以与以下工具结合使用：
- **预评估工具（pre-mortem-analyst）**：在项目启动前进行预评估。
- **逆向策略分析工具（inversion-strategist）**：通过逆向分析来识别需要避免的事项。
- **决策记录工具（artem-decision-journal）**：记录与MSPOT相关的重大决策。

---
更多关于TeddySnaps/TISA/GolfTab的MSPOT模板，请参阅references/examples.md。