---
name: manim-composer
description: |
  Trigger when: (1) User wants to create an educational/explainer video, (2) User has a vague concept they want visualized, (3) User mentions "3b1b style" or "explain like 3Blue1Brown", (4) User wants to plan a Manim video or animation sequence, (5) User asks to "compose" or "plan" a math/science visualization.

  Transforms vague video ideas into detailed scene-by-scene plans (scenes.md). Conducts research, asks clarifying questions about audience/scope/focus, and outputs comprehensive scene specifications ready for implementation with ManimCE or ManimGL.

  Use this BEFORE writing any Manim code. This skill plans the video; use manimce-best-practices or manimgl-best-practices for implementation.
---

## 工作流程

### 第一阶段：理解概念

1. **深入研究主题**  
   - 在提问之前，先通过网络搜索来了解核心概念。  
   - 找出使这个主题变得有趣的关键点。  
   - 体验“顿悟”的时刻——也就是让学习者产生共鸣的部分。  
   - 记录下常见的误解，以便在讲解过程中加以澄清。

2. **确定视频的叙事焦点**  
   - 这个视频要回答什么问题？  
   - 观众为什么应该关心这个问题？  
   - 视频中有哪些令人惊讶或违反直觉的内容？

### 第二阶段：与用户沟通并明确需求

提出有针对性的问题（不要一次性问完所有问题，根据用户的回答进行调整）：

**受众与内容范围**  
- 我应该假设观众具备什么样的数学/科学背景？（例如：“了解微积分”或“高中代数”）  
- 视频的时长应该控制在多少？（短：5-10分钟；中：15-20分钟；长：30分钟以上）  
- 这个视频应该是独立的，还是系列的一部分？

**内容重点与深度**  
- 有哪些具体的方面需要强调或省略？  
- 视频应该侧重于证明过程，还是更注重直观理解？  
- 是否需要包含实际应用案例？

**风格偏好**  
- 喜欢什么样的配色方案？  
- 叙述风格是随意的、正式的，还是幽默风趣的？  
- 有没有特定的视觉隐喻或表达方式希望使用？

### 第三阶段：创建 `scenes.md` 文件

生成一个结构完整的 `scenes.md` 文件，内容如下：

```markdown
# [Video Title]

## Overview
- **Topic**: [Core concept]
- **Hook**: [Opening question/mystery]
- **Target Audience**: [Prerequisites]
- **Estimated Length**: [X minutes]
- **Key Insight**: [The "aha moment"]

## Narrative Arc
[2-3 sentences describing the journey from confusion to understanding]

---

## Scene 1: [Scene Name]
**Duration**: ~X seconds
**Purpose**: [What this scene accomplishes]

### Visual Elements
- [List of mobjects needed]
- [Animations to use]
- [Camera movements]

### Content
[Detailed description of what happens, what's shown, what's explained]

### Narration Notes
[Key points to convey, tone, pacing notes]

### Technical Notes
- [Specific Manim classes/methods to use]
- [Any tricky implementations to note]

---

## Scene 2: [Scene Name]
...

---

## Transitions & Flow
[Notes on how scenes connect, recurring visual motifs]

## Color Palette
- Primary: [color] - used for [purpose]
- Secondary: [color] - used for [purpose]
- Accent: [color] - used for [purpose]
- Background: [color]

## Mathematical Content
[List of equations, formulas, or mathematical objects that need to be rendered]

## Implementation Order
[Suggested order for implementing scenes, noting dependencies]
```

## 3b1b 风格原则

在制作视频场景时，请遵循以下原则：

### 视觉叙事  
- **展示而非仅仅讲解**——每个概念都需要通过视觉方式来呈现。  
- **逐步揭示复杂内容**——不要一次性展示所有细节，而是逐步引导观众理解。  
- **保持视觉连贯性**——尽可能通过变换对象来展示信息，而不是直接替换它们。

### 节奏与节奏  
- **适当停顿**——给观众时间来消化关键内容。  
- **调整讲解速度**——快速讲解与详细解释交替进行。  
- **每个场景都要有明确的结局**——让每个视频片段都感觉完整。

### 数学的美感  
- **强调简洁与美感**——当数学原理显得简洁或优美时，要加以突出。  
- **多种表达方式**——用代数、几何或直观的方式展示同一个概念。  
- **逐步引入抽象概念**——从具体实例开始，再逐步抽象化。

### 互动技巧  
- **提出问题**——在揭示答案之前激发观众的好奇心。  
- **承认难度**——可以这样说：“这可能会让人感到困惑……”  
- **庆祝顿悟**——让观众感受到“顿悟”的喜悦。

## 参考资料  

- [references/narrative-patterns.md](references/narrative-patterns.md) – 常见的 3b1b 叙事结构  
- [references/visual-techniques.md](references/visual-techniques.md) – 有效的可视化技巧  
- [references/scene-examples.md](references/scene-examples.md) – 视频场景的示例

## 模板  

- [templates/scenes-template.md](templates/scenes-template.md) – 空白的 `scenes.md` 模板