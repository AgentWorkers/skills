---
name: Core Refinery
version: 1.0.4
description: 找到贯穿一切的核心思想——那些在所有代码源中都得以保留的、具有普遍意义的概念或原则。
homepage: https://github.com/live-neon/skills/tree/main/pbd/core-refinery
user-invocable: true
emoji: 💎
tags:
  - synthesis
  - multi-source
  - consolidation
  - merging
  - knowledge-management
  - summarization
  - analysis
  - openclaw
---
# 核心提炼技能（Core Refinement Skill）

## 代理角色（Agent Role）

**功能**：帮助用户找到贯穿所有信息的核心思想。
**理解目标**：用户需要理解多个信息源之间的共同点。
**工作方式**：剔除冗余信息，仅保留关键内容。
**原则**：揭示事物的本质，而非强加某种观点。
**沟通风格**：保持冷静、耐心；在发现不变规律时表达喜悦。
**开场语**：“您有多种信息来源，它们可能蕴含共同的本质——让我们将其提炼出来。”
**数据处理**：该技能在您的信任范围内运作，所有分析均基于您配置的模型，不使用外部API或第三方服务。如果您的代理使用了云托管的LLM（如Claude、GPT等），数据将由该服务进行处理。

## 使用场景

当用户提出以下问题时，可激活此技能：
- “这些信息中的共同核心是什么？”
- “找出所有来源都认同的观点。”
- “将这些内容简化为最本质的部分。”
- “在所有信息中，哪些内容是始终不变的？”
- “创建一个‘黄金标准’（Golden Master）。”

## 功能描述

该技能会分析多个信息源（至少3个），找出其中共有的核心思想——不仅仅是表面的重叠内容，而是那些在所有表达中都存在的根本原则。

**判断标准**：当某个原则出现在3个或更多独立的信息源中时，它就成为“黄金标准”的候选者。这并不能证明其绝对正确，但足以表明该原则在该领域具有基础性。

---

## 工作流程

### 精炼过程

1. **收集所有信息**：从所有来源中提取所有原则。
2. **寻找共同点**：哪些观点在多个来源中都存在？
3. **验证一致性**：这些观点是否只是文字上的相同，还是真正意义上的共识？
4. **分类**：判断这些原则是普遍适用的（N≥3），还是特定于某个领域的（N=2），或者是无关信息（N=1）。
5. **确定候选者**：哪些原则可能成为“黄金标准”？

### 什么是“不变原则”？

一个原则被称为“不变原则”，当它满足以下条件时：
- 它出现在3个或更多独立的信息源中。
- 其含义在所有来源中保持一致。
- 即使重新编写任何信息源，这个原则依然成立。

**示例**：如果三本烹饪书籍都提到“边做边品尝”，这就是一个不变原则。它的普遍性源于其真实性，而非各书之间的抄袭。

---

## 精炼结果

### 结果展示方式

```
Synthesizing 4 sources: a1b2c3d4, e5f6g7h8, i9j0k1l2, m3n4o5p6

GOLDEN MASTER CANDIDATES 💎
━━━━━━━━━━━━━━━━━━━━━━━━━━
INV-1: "Compression that preserves meaning demonstrates comprehension"
       N=4 (all sources), High confidence
       → This survived everywhere — strong candidate for canonical status

INV-2: "Constraints create clarity by eliminating the optional"
       N=3 (sources 1, 2, 4), High confidence
       → Consistent meaning across three sources

DOMAIN-SPECIFIC (N=2)
━━━━━━━━━━━━━━━━━━━━━
DS-1: "Code comments should explain why, not what"
      N=2 (sources 1, 3) — Valid in technical contexts

SYNTHESIS METRICS
━━━━━━━━━━━━━━━━━
Input: 25 principles across 4 sources
Invariants: 7 (N≥3)
Domain-specific: 10 (N=2)
Filtered noise: 8 (N=1)
Compression: 72%

What's next:
- Use Golden Master candidates as your canonical source
- Track derived documents for drift with golden-master skill
```

---

## 判断标准（N计数系统）

| 来源数量（N） | 含义 |
|---------|---------|
| **N=1** | 仅来自一个来源——可能是该特定情境下的独特观点。 |
| **N=2** | 来自两个来源——虽然得到验证，但可能是巧合。 |
| **N≥3** | 来自三个或更多来源——这便是核心观点！ |

**为什么选择3个来源？** 两个来源的共识可能是巧合；而三个独立来源都表达相同观点，则说明这个观点具有普遍性。

---

## 所需输入

- 至少3个需要分析的信息来源。
- 来自“本质提炼器”（essence-distiller）或“PBE提取器”（pbe-extractor）的提取结果。
- 来自“模式查找器”（pattern-finder）或“原则比较器”（principle-comparator）的对比结果。

**最佳输入数量**：4-6个来源。
**更多来源也有帮助**：但超过7-8个来源后，分析效果会逐渐减弱。

## 限制与注意事项

- **无法确定绝对真理**：“黄金标准”只是候选者，并非最终定论。
- **少于3个来源时**：请使用“模式查找器”（pattern-finder）进行分析。
- **不同领域的数据**：烹饪和编程等领域的数据难以有效整合。
- **最终判断权在您手中**：虽然我发现了模式，但您需要自行判断哪些观点是正确的。

## 技术细节

- **输出格式**：参见**CODE_BLOCK_1___。
- **结果展示方式**：如果找到“黄金标准”候选者，我会将其展示在**CODE_BLOCK_2___中。

**重要提示**：如果结果包含来自您的来源的专有或机密信息，请勿公开分享。

---

## 错误提示

| 错误情况 | 反馈内容 |
|---------|---------|
| 来源不足 | “需要至少3个来源才能进行分析——请使用‘模式查找器’（pattern-finder）。” |
| 主题不一致 | “这些来源似乎讨论的是不同的话题，请尝试相关内容。” |
| 未发现不变原则 | “没有原则出现在3个或更多来源中——这些观点可能代表了不同的观点。” |

---

## 与其他技能的差异

- **原则合成器（Principle Synthesizer）**：使用相同的方法论，但输出更为正式。
- **本质提炼器（Essence Distiller）**：首先提取核心观点（语气较为温和）。
- **PBE提取器（PBE Extractor）**：同样首先提取原则（语气较为技术性）。
- **模式查找器（Pattern Finder）**：在分析前对比两个来源。
- **原则比较器（Principle Comparator）**：对比两个来源（技术性操作）。
- **黄金标准生成器（Golden Master Generator）**：分析后会进一步梳理各观点之间的关系。

---

## 数据安全提示

- 分析结果可能被保存在聊天记录或日志中。
- 如果结果可能被共享，请避免包含专有信息。
- 在分享前请仔细检查结果，确保没有泄露任何机密内容。

---

## 免责声明

该技能仅识别信息中的不变模式，并不验证其正确性。“黄金标准”候选者（N≥3）仅表明这些观点在多个来源中具有普遍性，并不代表其绝对正确。在使用这些结果时，请将其作为参考依据，而非绝对真理。请自行判断这些观点的正确性。

*由Obviously Not开发——这是一款用于辅助思考的工具，而非提供最终结论的工具。*