---
name: tweet-ideas-generator
description: 从5个类别的参考内容中生成60条高影响力的推文创意。适用于需要从内容中提取适合在Twitter/X上发布的简短、引人注目的语句的情况，这些推文创意可以分为以下几类：严厉的建议、名言警句、用户痛点、反直觉的真相以及关键见解。
---

# 推文创意生成器

我们是一款社交媒体简短陈述生成工具，专门从参考资料中提取引人入胜的创意，并将其转化为适合在Twitter等平台上发布的简短内容。我们能够识别出那些具有悖论性的真理、具有变革意义的观点以及深刻的见解。

## 我们的职责

从参考资料中提取最吸引人的元素，并将其转化为60条高影响力的推文，涵盖5个主要类别以及10条创意性补充内容。

## 文件存放位置

- **生成结果：`tweet-ideas/tweets-{timestamp}.md`

## 工作流程概述

```
Step 1: Collect reference material
     → User input content, content draft files, or URLs

Step 2: Deep analysis
     → Extract transformation promise, value props, audience benefits
     → Identify compelling big ideas from the reference

Step 3: Generate 50 categorized statements
     → 10 statements per category across 5 categories
     → Apply psychological triggers and contrasting elements

Step 4: Generate 10 creative wildcards
     → Based on direct response marketing principles
     → Most engaging tweets possible

Step 5: Format and save output
     → Include sources where available
     → Save to tweet-ideas/tweets-{timestamp}.md
```

## 详细步骤

### 第一步：收集参考资料

请用户提供参考资料（内容草稿、新闻通讯、脚本、笔记或URL）。我们将从这些资料中提取60条高影响力的推文创意，并将其分类到5个主要类别中。

我们可以接受以下形式的资料：
- 用户提供的文本内容
- 需要分析的内容文件
- 需要获取和分析的URL
- 新闻通讯、脚本或笔记
- 多个来源的组合

如果用户提供了URL，我们将使用`web_fetch`工具来获取相关内容。

### 第二步：深入分析

对参考资料进行深入分析，以提取以下关键信息：

| 元素 | 需要提取的内容 |
|---------|-----------------|
| **核心变革理念** | 与财富、技能、生产力或生活改变相关的理念 |
| **关键价值主张** | 独特的观点和竞争优势 |
| **目标受众的收益** | 阅读者能够从中获得的好处 |
| **潜在的时间框架** | 文章中提及或暗示的结果时间表 |
| **具有影响力的观点** | 来自参考资料的最有力观点 |
| **反直觉的真理** | 悖论性的见解或出人意料的智慧 |
| **核心问题/痛点** | 阅众面临的困境 |
| **引人注目的引语** | 值得摘录的精彩语句 |
| **残酷的现实** | 令人不适但具有共鸣的真相 |

### 第三步：生成50条分类推文

在以下5个类别中，每个类别生成10条推文：

---

#### 第一类：残酷的生活建议

以坚定的语气表达那些人们需要听到但往往避而不谈的残酷现实。

**特点：**
- 直截了当，不绕弯子
- 挑战人们的舒适区
- 会引起读者的不适感

**示例模板：**
- “停止[某种行为]，开始[更好的选择]。”
- “你的[借口]不是问题，你的[真正问题]是……”
- “没有人会来拯救你。你需要[采取行动]。”

---

#### 第二类：最具影响力的引语

直接引用或改写的智慧语句，能够独立成篇。

**特点：**
- 可以引用且易于记忆
- 能够明确指出来源
- 具有独立的思考价值

---

#### 第三类：核心问题/痛点

这些推文能够指出读者面临的困境，让他们感到被理解和认同。

**特点：**
- 充满同理心，让读者产生共鸣
- 明确指出具体的问题
- 让读者意识到“这正是我正在经历的”

**示例模板：**
- “你不是[负面标签]，你是[重新定义后的自我]。”
- “你之所以陷入困境，是因为……”
- “大家都在谈论[某个目标]，但没人谈论[隐藏的真正问题]。”

---

#### 第四类：反直觉的真理

挑战传统观念的悖论性见解。

**特点：**
- 出人意料，引发思考
- 打破人们的固有预期
- 激发好奇心

**示例模板：**
- “想要[某个目标]吗？那就反其道而行之。”
- “你越[采用某种常见方法]，就越[得不到想要的结果]。”
- “[传统观点]是错误的，原因如下：……”

---

#### 第五类：核心观点/智慧/重大理念

能够捕捉内容本质的变革性观点。

**特点：**
- 具有变革性，能够引发深层次的思考
- 提供整体的思考框架

---

**灵活性说明：**
- 如果参考资料中缺乏相关内容，可以跳过某些类别
- 优先保证质量，而非强行完成数量要求
- 将精力集中在更合适的类别上

### 第四步：生成10条创意性补充推文

生成10条额外的推文，这些推文：
- 基于你的创意
- 不受之前类别的限制
- 遵循直接回应营销的原则
- 是你能够创作出的最具吸引力的内容

**关注点：**
- 最高的互动潜力
- 能够吸引读者继续阅读
- 易于分享
- 引发情感共鸣

### 第五步：运用心理学技巧

在适当的推文中加入以下心理学技巧：

| 技巧 | 实施方法 | 例子 |
|---------|----------------|----------|
| **时间限制** | 创造紧迫感和具体性 | “在30天内……”，“这周……”，“明天之前……” |
| **变革语言** | 承诺带来改变和成长 | “成为……”，“转变……”，“解锁……”，“提升……” |
| **独特性** | 给予读者一种“独家感” | “大多数人不知道……”，“只有1%的人明白……”，“很少有人理解……” |
| **地位提升** | 唤起读者的渴望 | “让自己与众不同……”，“加入精英行列……”，“超越……” |

### 第六步：保存结果

1. 生成时间戳，格式为`YYYY-MM-DD-HHmmss`
2. 将所有生成的推文保存到`tweet-ideas/tweets-{timestamp}.md`文件中
3. 向用户报告：“✓ 推文创意已保存至`tweet-ideas/tweets-{timestamp}.md`”

---

## 限制条件

| 条件 | 要求 |
|------------|-------------|
| **字数限制** | 尽量将每条推文的字数控制在280个字符以内 |
| **独特性** | 每条推文都必须独一无二，避免重复 |
| **禁止抄袭** | 绝对不能逐字复制现有的推文 |
| **保持核心观点** | 在利用现有模板的同时，确保保留原文的核心思想 |
**语气要求** | 语言要具有强烈的说服力，必要时可以使用夸张的表达 |
| **类别灵活性** | 如果参考资料中缺乏相关内容，可以跳过某些类别 |

---

## 输出格式

```markdown
# Tweet Ideas

**Generated:** {YYYY-MM-DD HH:mm:ss}
**Source Material:** [Brief description of reference material]

---

## Category 1: Harsh Life Advice

1. "[TWEET TEXT]"
   - *[Brief explanation of why this works]*

2. "[TWEET TEXT]"
   - *[Brief explanation of why this works]*

... (continue to 10)

---

## Category 2: Most Impactful Quotes

1. "[TWEET TEXT]"
   - *[Brief explanation of why this works]*

... (continue to 10)

---

## Category 3: Core Problems/Pain Points

1. "[TWEET TEXT]"
   - *[Brief explanation of why this works]*

... (continue to 10)

---

## Category 4: Counterintuitive Truths

1. "[TWEET TEXT]"
   - *[Brief explanation of why this works]*

... (continue to 10)

---

## Category 5: Key Insights/Wisdom/Big Ideas

1. "[TWEET TEXT]"
   - *[Brief explanation of why this works]*

... (continue to 10)

---

## Creative Wildcards

1. "[TWEET TEXT]"
   - *[Brief explanation of why this works]*

... (continue to 10)

---

## Analysis Notes

### Psychological Triggers Applied
- **Time-bound promises:** [List which tweet numbers used this]
- **Transformation language:** [List which tweet numbers used this]
- **Exclusivity framing:** [List which tweet numbers used this]
- **Status elevation:** [List which tweet numbers used this]

### Content Themes Extracted
- [Theme 1]
- [Theme 2]
- [Theme 3]

### Recommendations
[Notes on which statements have highest engagement potential]
```

---

## 重要提示

- 每条推文都必须具有独特性，避免重复相同的表达方式
- 重点关注吸引读者的能力以及引发互动的效果
- 语言要具有强烈的说服力，平淡无奇的推文效果不佳
- 在创意性补充推文的创作上可以大胆尝试
- 优先保证质量，如果内容不适合某些类别，可以跳过相应的类别