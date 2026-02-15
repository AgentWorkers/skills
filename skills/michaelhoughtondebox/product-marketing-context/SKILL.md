---
name: product-marketing-context
version: 1.0.0
description: "当用户需要创建或更新他们的产品营销背景文档时，也可以使用该功能。当用户提到“产品背景”、“营销背景”、“设置背景信息”或希望避免在多个营销任务中重复基础信息时，此功能同样适用。系统会生成名为 `.claude/product-marketing-context.md` 的文档，其他营销相关功能会引用该文档。"
---

# 产品营销背景

您的职责是协助用户创建和维护产品营销背景文档。该文档记录了产品的基本定位和信息传递要点，以便其他营销团队能够直接参考，避免重复工作。

该文档存储在 `.claude/product-marketing-context.md` 文件中。

## 工作流程

### 第一步：检查现有文档

首先，检查 `.claude/product-marketing-context.md` 是否已经存在。

**如果文档存在：**
- 阅读文档并总结其中的内容
- 询问用户希望更新哪些部分
- 仅收集这些部分所需的信息

**如果文档不存在，提供两种选择：**

1. **从代码库自动生成文档**（推荐）：您需要查看代码库中的 `README`、登录页面、营销文案、`package.json` 等文件，然后起草文档的初稿。用户随后会对初稿进行审核、修改并补充缺失的内容。这种方式比从头开始更快。

2. **从头开始编写**：与用户逐一讨论每个部分的内容，逐步收集信息。

大多数用户更倾向于选择第一种方式。在提交初稿后，可以询问用户：“有哪些地方需要修改？还缺少哪些内容？”

### 第二步：收集信息

**如果选择自动生成文档：**
1. 阅读代码库中的 `README`、登录页面、营销文案、产品介绍页面、元描述文件以及 `package.json`。
2. 根据收集到的信息起草所有部分的内容。
3. 提交初稿，并询问用户有哪些需要修改或补充的地方。
4. 重复此过程，直到用户满意为止。

**如果选择从头开始编写：**
- 与用户逐一讨论每个部分的内容，不要一次性提出所有问题。
- 对于每个部分：
  - 简要说明您要记录的内容。
  - 提出相关的问题。
  - 确认信息的准确性。
  - 再进入下一个部分。

**重要提示：** 尽量使用客户实际使用的语言进行记录。原话比经过修饰的描述更有价值。

---

## 需要记录的内容

### 1. 产品概述
- 产品的一句话描述
- 产品的主要功能（2-3句话）
- 产品所属的类别（客户如何搜索到该产品）
- 产品类型（SaaS、市场平台、电子商务、服务等）
- 商业模式和定价策略

### 2. 目标受众
- 目标公司类型（行业、规模、发展阶段）
- 目标决策者（角色、部门）
- 主要解决的问题（产品能帮助客户解决的核心问题）
- 客户使用产品的主要场景（客户使用产品来完成的具体任务）

### 3. 人物角色（仅适用于 B2B 产品）
如果购买决策涉及多个利益相关者，请分别为以下角色记录信息：
- 用户、推动者（User）、决策者（Decision Maker）、财务采购人员（Financial Buyer）、技术影响者（Technical Influencer）
- 每个角色的关注点、他们面临的问题以及产品能为他们带来的价值

### 4. 问题与痛点
- 客户在找到您的产品之前面临的核心问题
- 现有解决方案的不足之处
- 现有解决方案给客户带来的成本（时间、金钱、机会损失）
- 客户在转换使用您的产品时可能产生的心理压力（焦虑、恐惧、疑虑）

### 5. 竞争格局
- **直接竞争对手**：提供相同解决方案的公司
- **次要竞争对手**：提供不同解决方案但解决相同问题的公司
- **间接竞争对手**：采用不同方法的公司
- 每种竞争对手在哪些方面不如您的产品

### 6. 产品差异化
- 产品的独特优势（其他竞争对手所不具备的功能）
- 您如何以独特的方式解决问题
- 这些优势为何更胜一筹（给客户带来的好处）
- 客户为何选择您的产品而非竞争对手的产品

### 7. 反对意见与不适用的用户群体
- 销售过程中常见的三大反对意见及应对策略
- 不适合使用您产品的用户群体（反人物角色）

### 8. 客户转换的驱动因素
- 客户放弃现有解决方案的三大原因
- 他们被您的产品吸引的因素
- 客户坚持使用现有解决方案的习惯
- 客户在转换使用新产品时可能产生的焦虑

### 9. 客户的语言表达
- 客户如何描述他们面临的问题（原话）
- 客户如何描述您的产品（原话）
- 应该使用的词汇和短语
- 应避免使用的词汇和短语
- 产品专用术语的解释

### 10. 品牌风格
- 语言风格（专业、随意、幽默等）
- 沟通方式（直接、对话式、技术性）
- 品牌个性（3-5 个形容词）

### 11. 产品优势
- 可引用的关键指标或成果
- 重要的客户案例或合作伙伴
- 客户评价
- 主要的价值主张和支持证据

### 12. 营销目标
- 产品的主要业务目标
- 您希望用户采取的关键行动
- 目前的关键业绩指标（如果已知）

---

## 第三步：创建文档

收集完信息后，按照以下结构创建 `.claude/product-marketing-context.md` 文件：

```markdown
# Product Marketing Context

*Last updated: [date]*

## Product Overview
**One-liner:**
**What it does:**
**Product category:**
**Product type:**
**Business model:**

## Target Audience
**Target companies:**
**Decision-makers:**
**Primary use case:**
**Jobs to be done:**
-
**Use cases:**
-

## Personas
| Persona | Cares about | Challenge | Value we promise |
|---------|-------------|-----------|------------------|
| | | | |

## Problems & Pain Points
**Core problem:**
**Why alternatives fall short:**
-
**What it costs them:**
**Emotional tension:**

## Competitive Landscape
**Direct:** [Competitor] — falls short because...
**Secondary:** [Approach] — falls short because...
**Indirect:** [Alternative] — falls short because...

## Differentiation
**Key differentiators:**
-
**How we do it differently:**
**Why that's better:**
**Why customers choose us:**

## Objections
| Objection | Response |
|-----------|----------|
| | |

**Anti-persona:**

## Switching Dynamics
**Push:**
**Pull:**
**Habit:**
**Anxiety:**

## Customer Language
**How they describe the problem:**
- "[verbatim]"
**How they describe us:**
- "[verbatim]"
**Words to use:**
**Words to avoid:**
**Glossary:**
| Term | Meaning |
|------|---------|
| | |

## Brand Voice
**Tone:**
**Style:**
**Personality:**

## Proof Points
**Metrics:**
**Customers:**
**Testimonials:**
> "[quote]" — [who]
**Value themes:**
| Theme | Proof |
|-------|-------|
| | |

## Goals
**Business goal:**
**Conversion action:**
**Current metrics:**
```

---

## 第四步：确认并保存文档

- 展示完成的文档
- 询问是否有需要调整的地方
- 将文档保存到 `.claude/product-marketing-context.md` 文件中
- 告诉用户：“其他营销团队将自动使用这份文档。只需运行 `/product-marketing-context` 即可随时更新文档。”

---

## 提示：
- **具体问题**：询问“客户使用您的产品时最困扰他们的第一个问题是什么”，而不是“您的产品能解决什么问题”。
- **记录原话**：客户实际使用的语言比经过修饰的描述更有参考价值。
- **要求提供示例**：询问“能举个例子吗？”有助于获得更准确的答案。
- **边记录边验证**：在继续下一步之前，先总结每个部分的内容并确认其准确性。
- **跳过不适用的部分**：并非所有产品都需要记录所有内容（例如，B2C 产品可能不需要记录人物角色相关的内容）。