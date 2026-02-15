---
name: jtbd-analyzer
description: 揭示客户使用您的产品真正想要完成的任务。这不仅仅是了解产品的功能，还需要深入理解用户的功能性需求、情感需求以及社交需求。当用户提到“需要完成的任务”（jobs to be done）、“为什么客户会购买”（why do customers buy）、“用户需求是什么”（what user needs）、“人们为什么购买”（why do people buy）等问题时，可以使用这种方法进行深入分析。
---

# 待办事项分析器（Jobs-To-Be-Done Analyzer）

## 核心概念

客户购买的不是产品，而是产品能够完成的任务或工作。

“人们并不想要一把直径为四分之一英寸的钻头，他们想要的是一个直径为四分之一英寸的孔。”  
实际上，他们想要的是一个架子——用来展示照片，从而为自己的家庭感到自豪。

## 任务的三个维度

| 维度          | 问题                | 格式                |
|---------------|------------------|-------------------|
| **功能性**       | 需要完成什么任务？          | “请帮助我[动词]+[对象]”       |
| **情感性**       | 我希望有什么样的感受？         | “请让我感受到[情感]”        |
| **社会性**       | 我希望别人如何看待我？        | “请帮助我展现出[特质]”        |

## 工作流程

1. **任务描述**： “在[特定情境]下，我希望达到[目标动机]，从而实现[预期结果]。”
2. 为每种用户类型分析这三个维度。
3. **寻找真正的竞争对手**：还有哪些工具或方法可以完成这项任务？
4. **确定优先级**：哪些任务最为关键且目前服务不足？

## 输出格式

```
PRODUCT: [What you're analyzing]

For [User Type]:
JOB: "When [situation], I want [motivation], so I can [outcome]"

📋 FUNCTIONAL: [Task to accomplish]
💜 EMOTIONAL: [Feeling desired]
👥 SOCIAL: [Perception desired]

ALTERNATIVES: [What else could do this job?]
UNDERSERVED: [What part isn't done well?]
PRIORITY: Critical / Important / Nice-to-have
```

## 关键问题

1. “当你[执行某个动作]时，你试图达成什么目标？”
2. “请描述一下你上次需要完成[某项任务]时的具体情况。”
3. “如果[某个产品]不存在，你会怎么做？”
4. “你目前完成[某项任务]的过程中有哪些令人沮丧的地方？”

## 集成方式

该工具可与以下组件配合使用：
- **first-principles-decomposer**：将任务分解为最基本的、不可再细分的需求。
- **cross-pollination-engine**：研究其他工具或方法是如何解决类似问题的。
- **app-planning-skill**：利用JTBD分析结果来指导产品功能的开发。

---
有关Artem特定版本的JTBD分析示例，请参阅`references/examples.md`文件。