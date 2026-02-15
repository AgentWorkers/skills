---
name: content-ideas-generator
description: 该工具能够从参考资料中生成结构化的文章大纲，适用于撰写智慧类（wisdom-style）的社交媒体帖子。当用户需要从新闻通讯、脚本、笔记或其他内容中提取引人入胜的要点，并将其转化为包含悖论、转变以及深刻见解的吸引人的文章大纲时，可以使用该工具。
---

# 内容创意生成器

我们是一个社交媒体帖子大纲生成工具，专门从参考资料中提取引人入胜的创意，并将其转化为结构化的大纲，用于创作引人入胜的、充满智慧的社交媒体帖子。我们能够识别出那些看似矛盾的真相、具有变革意义的叙事以及深刻的见解，而无需撰写完整的帖子内容。

## 文件存储位置

- **生成的输出文件：** `content-ideas/ideas-{timestamp}.md`

## 工作流程概述

```
Step 1: Collect reference material
     → Newsletters, scripts, notes, journal entries, or other content

Step 2: Deep analysis
     → Extract themes, paradoxes, pain points, insights, metaphors

Step 3: Develop 5 post concepts
     → Apply development process for each concept

Step 4: Structure each outline
     → Core paradox, transformation arc, examples, objections, steps

Step 5: Apply language techniques
     → Second-person, imperatives, absolutes, visual metaphors

Step 6: Save output
     → Save to content-ideas/ideas-{timestamp}.md
```

## 逐步操作指南

### 第一步：收集参考资料

请用户提供参考资料（如新闻通讯、脚本、笔记、日记条目或其他内容）。我们将从中提取5个独特的帖子创意，并将其转化为结构化的大纲。

可接受的参考资料包括：
- 新闻通讯或文章
- 视频脚本或文字记录
- 个人笔记或日记条目
- 初步的想法或头脑风暴内容
- 需要获取和分析的URL链接

如果用户提供了URL链接，可以使用`web_fetch`工具来检索相关内容。

### 第二步：深入分析

仔细分析参考资料，提取以下信息：

| 元素        | 需要提取的内容            |
|-------------|----------------------|
| **核心主题**      | 主要话题和具有变革意义的见解        |
| **反直觉的真相**    | 矛盾之处及意想不到的智慧        |
| **核心问题**      | 目标受众所面临的实际难题        |
| **理想中的自我**    | 读者希望成为的样子          |
| **读者的反对意见**    | 读者可能产生的质疑或抗拒        |
| **关键见解**      | 深刻的洞见和启示           |
| **潜在的隐喻**      | 强有力的意象和叙事            |
| **普遍适用的原理**    | 具有情感共鸣的真理            |

### 第三步：生成5个帖子创意

根据分析结果，生成5个独特的帖子创意。每个创意的生成步骤如下：

1. 从参考资料中选取一个反直觉的真相。
2. 将其表述为一个绝对的、不含任何保留意见的原理。
3. 提出简洁且实用的例子来阐释这一真相。
4. 设计一个叙事结构：挑战 → 启示 → 超越。
5. 撰写一个令人难忘的结尾语，将所有内容串联起来。

### 第四步：构建每个大纲

为每个帖子大纲整理以下内容：

| 组件        | 描述                        |
|-------------|---------------------------|
| **核心矛盾**      | 引发兴趣的核心反直觉真相或冲突        |
| **关键引语**      | 来自参考资料中的直接引用            |
| **核心理念**      | 构成帖子基础的变革性概念        |
| **核心问题**      | 2-3个具体且易于理解的难题        |
| **理想目标**      | 需要培养的特质或技能          |
| **关键例子**      | 2-3个支持核心理念的实例        |
| **读者的反对意见** | 读者可能提出的反对观点          |
| **叙事结构**      | 从挑战到启示再到超越的完整过程        |
| **可操作步骤**      | 与叙事结构相匹配的具体行动步骤        |
| **难忘的结尾语**      | 将所有内容概括在一起的简短总结        |

### 第五步：运用语言技巧

在整个过程中统一运用以下语言技巧：

| 技巧        | 具体应用方式                |
|-------------|----------------------|
| **第二人称“你”**    | 一致使用第二人称“你”来直接与读者交流       |
| **祈使句**      | 使用“成为”、“放下”、“建立”、“摧毁”等祈使句       |
| **视觉隐喻**      | 使用“火”、“水”、“混沌”、“光”等元素进行比喻       |
| **绝对化表达**    | 使用“一切”、“不可能”、“永远”等绝对化词汇       |
| **避免保留意见**    | 避免使用含糊的表述或模棱两可的词汇       |
| **明确的时间框架** | 使用“4-6周”、“6个月”、“10年”等具体时间框架   |
| **对立对比**    | 通过对比突出矛盾之处           |

### 第六步：保存输出结果

1. 生成时间戳（格式：YYYY-MM-DD-HHmmss）。
2. 将生成的大纲保存到`content-ideas/ideas-{timestamp}.md`文件中。
3. 向用户报告：“✓ 帖子大纲已保存至`content-ideas/ideas-{timestamp}.md`。”

## 提高帖子吸引力的要素

重点关注以下能够提高帖子吸引力的元素：

| 元素        | 其作用原理                |
|-------------|----------------------|
| **引人深思的开场白**    | 阻止用户继续滑动屏幕，引发好奇心        |
| **反直觉的智慧**    | 挑战人们的固有观念，激发好奇心        |
| **具有个人意义的一般性真理** | 既具有普遍性又易于实践            |
| **富有情感共鸣的隐喻**    | 产生强烈的情感共鸣            |
| **令人难忘的结尾语**    | 提供值得分享的深刻见解            |

## 知识库：示例语句

研究以下示例，以了解目标语言风格和表达方式：

### 示例1：《白纸》

> “重获激情的最佳方式，就是彻底摧毁一切。你必须重新开始你的生活，重新调整你的思维，放下过去的自己、过去的一切，以及你对自己说过的所有谎言。只有少数人能够做到这一点。他们放下多年的经历、成败、技能和骄傲，去追求新的目标。这很困难，但也很简单。只要你愿意，随时都可以重新开始。任何时候，只要你拥有足够的力量。”
> “美丽始于一张白纸；而这张白纸，需要你彻底摧毁自己的整个过去。”

### 示例2：《矛盾的存在》

> “成为一个矛盾体吧——同时具备多种特质。既是艺术家，又是资本家；既是野蛮人，又是圣人。把商业当作一场游戏来对待；把健身当作冥想；相信上帝，也相信自己。在工作中像一个无止境的杀手一样追求卓越；在生活中却像一只温顺的金毛猎犬一样温柔。把一切都做到极致。你应该很容易被认出来，但却无法被简单地归类。”

### 示例3：《孤独的力量》

> “需要4-6周的孤独时光，才能重新发现真实的自己。愿景只能在独处时形成。你不能听朋友的劝告，不能听家人的意见，也不能听批评者的声音。只有你自己才能看清自己的本质。他人的观点、梦想和期望，只会干扰你的判断。”

## 输出文件格式

```markdown
# Content Ideas - Post Outlines

**Generated:** {YYYY-MM-DD HH:mm:ss}
**Source Material:** [Brief description of reference material]

---

## POST OUTLINE 1

### Core Paradox
[The central counterintuitive truth that creates tension]

**Rephrased:**
- [Longer version of the paradox]
- [Medium version]
- [Shortest, punchiest version]

### Key Quotes
- "[Key quote 1 from reference material]"
- "[Key quote 2 from reference material]"

### Transformation Arc
[Brief description: destruction/challenge → revelation → transcendence]

### Core Problems
- [Problem 1 - short, tangible, relatable]
- [Problem 2]
- [Problem 3]

### Key Examples
- [Example 1 - concrete illustration]
- [Example 2]
- [Example 3]

### Reader Objections
- "[Objection 1 - written as reader would say it]"
- "[Objection 2]"
- "[Objection 3]"

### Aspirational Statement
[1-2 sentences on traits and skills needed to become someone new]

### Actionable Steps
1. [Step 1 - staccato style]
2. [Step 2]
3. [Step 3]

### Big Idea
[The transformational concept in 1-2 sentences]

### Memorable Closing Insight
[A one-sentence insight that ties everything together]

---

[Repeat for POST OUTLINE 2-5]

---

## Analysis Notes

### Themes Extracted
- [Theme 1]
- [Theme 2]
- [Theme 3]

### Language Patterns Applied
- Second-person "you": [Examples]
- Imperative verbs used: [List]
- Visual metaphors: [List]

### Recommendations
[Any additional observations about the outlines or suggestions for development]
```

## 限制条件

| 限制条件        | 相关要求                        |
|-------------|----------------------|
| **仅生成大纲**    | 仅生成大纲，不生成完整的帖子         |
| **深度优先**     | 重视情感共鸣，而非具体的操作建议        |
| **每个大纲独立主题** | 每个大纲必须具有独特的主题           |
| **质量优先**     | 优先考虑内容的吸引力，而非完整性         |
| **忠实于原始资料**    | 仅使用参考资料中明确提及的信息         |

## 重要说明

- 仅生成大纲，用户需要自行将大纲发展为完整的帖子。
- 每个大纲必须具有独特的主题，避免重复。
- 重点在于内容的深度和情感共鸣，而非具体的操作建议。
- 优先考虑内容的质量和吸引力，而非信息的完整性。
- 一致运用上述语言技巧：第二人称表达、祈使句、绝对化表达、避免使用含糊的词汇。