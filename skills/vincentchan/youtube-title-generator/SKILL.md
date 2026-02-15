---
name: youtube-title-generator
description: 根据内容概念生成吸引人的 YouTube 标题创意。当需要为视频创建能够吸引观众点击的标题时，可以使用经过验证的结构公式和来自高人气视频的心理学原理来帮助生成合适的标题。
---

# YouTube 标题生成器

这是一个 YouTube 标题生成工具，它能够将您的内容创意、新闻稿概念或参考资料转化为引人入胜、点击率高的 YouTube 标题。我们运用了来自高点击率视频的成熟结构公式和心理学原理来帮助您生成标题。

## 文件位置

- **参考标题模板:** `youtube-title/reference-titles.md`
- **生成的输出文件:** `youtube-title/titles-{timestamp}.md`

## 工作流程概述

```
Step 1: Collect user input
     → Content idea, newsletter concept, or reference material

Step 2: Analyze input
     → Identify core transformation, value props, audience benefits

Step 3: Load reference titles (if available)
     → Read youtube-title/reference-titles.md for patterns

Step 4: Generate 20 structured titles
     → Apply structural formulas and psychological triggers

Step 5: Generate 10 creative titles
     → Based on direct response marketing principles

Step 6: Save output
     → Save to youtube-title/titles-{timestamp}.md
```

## 逐步说明

### 第一步：收集用户输入

请用户提供以下信息：
> “请分享您的内容创意、新闻稿概念或参考资料。我会根据这些信息生成 30 个吸引人的 YouTube 标题。”

用户可以提供以下内容：
- 一个基本的内容创意或主题
- 一份需要提取创意的新闻稿或文章
- 一个需要获取和分析的 URL
- 多个概念或主题

如果用户提供了 URL，使用 `web_fetch` 函数来获取相关内容。

### 第二步：分析输入内容

分析用户提供的内容，重点关注以下方面：
- **核心转化点**：财富、技能、生产力、生活改变、职业发展、健康、人际关系等
- **核心价值主张**：内容的独特之处、竞争优势
- **目标受众的收益**：观众能从中获得什么、解决了哪些问题、满足了哪些需求
- **预期时间框架**：实现目标的实际时间范围（天、周、月、小时）
- **最具吸引力的核心概念**：参考资料中最重要的、适合分享的内容

### 第三步：加载参考标题模板

如果 `youtube-title/reference-titles.md` 文件存在，请阅读该文件，以便：
- 了解已被验证的结构和公式
- 学习有效的心理学触发点
- 确保生成的标题与成功的案例保持一致

### 第四步：生成 20 个结构化的标题

使用以下框架生成 20 个标题：

#### 结构化公式（循环使用）

**公式 1：强调性陈述 + 支持性细节/方法**
- 模式：`[强调性陈述] + ([方法/内容/原因])`
- 例子：
  - “单人商业模式（如何实现自我产品化）”
  - “个人品牌的终结与创意工作的未来”

**公式 2：如何 + 期望的结果 + 方法/途径**
- 模式：`如何[达成目标X] + ([方法/系统])`
- 例子：
  - “如何在6-12个月内超越99%的人”
  - “如何在零粉丝的情况下建立受众群（他们不会告诉你的方法）”

**公式 3：时间限定 + 重点关注点**
- 模式：`[时间范围/数字] + ([重点关注领域])`
- 例子：
  - “365小时内改变你的生活（成功人士专注的这些任务）”
  - “每天消失2-4小时（百万富翁的效率习惯）”

#### 心理学触发点（应用于所有标题）

| 触发点 | 实现方式 | 例句 |
|---------|----------------|-----------------|
| **时间限定** | 明确具体的时间范围 | “6-12个月”、“365小时”、“每天2-4小时”、“30天内” |
| **转变语言** | 承诺个人成长 | “你将不再是从前的自己”、“改变你的生活”、“重塑自我” |
| **独家性** | 创造一种内部知识的吸引力 | “他们不会告诉你的”、“大多数人忽视的”、“秘密” |
| **地位提升** | 唤起雄心** “超越99%的人”、“高收入技能”、“顶尖1%” |

#### 对比元素（在多个标题中使用）

- **平淡的输入 → 强烈的输出**：“每天2-4小时” → “赚100万美元”
- **意想不到的组合**：“将生活变成电子游戏”、“效率习惯”
- **反直觉的方法**：“消失然后重新出现”、“避免学习这些技能”

### 第五步：生成10个创意标题

再生成10个标题：
- 这些标题应基于您的创意和直觉
- 不必严格遵循上述结构化公式
- 从直接响应营销原则中获取灵感
- 这些标题应该是您能为该主题想到的最吸引人的标题

可以考虑的创意方法：
- 个人故事式开头（“我如何...”、“我尝试了...”、“当...发生时...”）
- 列表式标题（“7种方法...”、“3个关键点...”）
- 挑战/实验式标题（“我坚持做了X天”）
- 反传统/打破迷思的标题（“停止做X”、“X是个谎言”）
- 问题式开头（“为什么...”、“如果...会怎样...”）
- 情感共鸣式标题（“关于...的真相”、“没人告诉你的...”）

### 第六步：保存结果

1. 生成一个时间戳，格式为 `YYYY-MM-DD-HHmmss`
2. 将所有生成的标题保存到 `youtube-title/titles-{timestamp}.md` 文件中
3. 告知用户：“✓ 标题已保存到 `youtube-title/titles-{timestamp}.md` 文件中”

## 限制条件

- **字符限制**：尽可能使标题长度控制在70个字符以内
- **独特性**：所有30个标题都必须各具特色
- **禁止抄袭**：严禁逐字复制参考标题中的内容，仅将其作为灵感来源
- **核心内容**：保持用户提供内容的本质
- **语气**：标题应具有强烈的说服力，必要时可以使用夸张的表达

## 输出格式

```markdown
# YouTube Title Ideas

**Generated:** {YYYY-MM-DD HH:mm:ss}
**Input Concept:** [Brief summary of user's input]

---

## Structured Titles (20)

1. [TITLE 1]
2. [TITLE 2]
3. [TITLE 3]
... (continue to 20)

---

## Creative Titles (10)

21. [TITLE 21]
22. [TITLE 22]
23. [TITLE 23]
... (continue to 30)

---

## Analysis

### Psychological Triggers Applied
- **Time-bound promises:** Used in titles [list numbers]
- **Transformation language:** Used in titles [list numbers]
- **Exclusivity framing:** Used in titles [list numbers]
- **Status elevation:** Used in titles [list numbers]

### Structural Formulas Used
- **Bold Statement + (Detail):** Titles [list numbers]
- **How To + Outcome + (Method):** Titles [list numbers]
- **Time-Bound + (Focus):** Titles [list numbers]

### Notes
[Any additional observations about the title generation or recommendations]
```

## 错误处理

### 未提供输入
- 如果用户没有提供任何输入，再次提示他们提供具体内容。

### URL 获取失败
- 如果无法获取URL，请告知用户并要求他们提供其他输入。

### 信息不足
- 如果输入信息过于模糊，可以询问1-2个问题以获取更多细节：
  - “这个内容承诺带来什么样的改变或结果？”
  - “这个视频的目标受众是谁？”

## 重要提示

- 在生成标题之前，请先阅读 `youtube-title/reference-titles.md` 文件
- 不要连续使用相同的结构化公式
- 每个标题都应该具有新鲜感和独特性
- 创意标题（第21-30个）应与结构化标题有明显区别
- 优先选择能够引发好奇心和吸引点击的标题
- 从观众的角度思考：你会点击这个标题吗？