---
name: side-quests
version: 1.0.1
description: **完整的创意合成**：从单一的技术视角出发，将歌曲、视觉概念以及 TED 演讲融为一体。
author: Live Neon <hello@liveneon.ai>
homepage: https://github.com/live-neon/skills/tree/main/creative/side-quests
repository: leegitw/side-quests
license: MIT
tags: [creative, synthesis, songwriting, storytelling, ted-talk, visual-guide, reflection, knowledge-transfer, suno, learning]
layer: creative
status: active
alias: sq
user-invocable: true
emoji: 🎭
---
# 辅助任务（Side-Quests）

这项技能通过将三种创意成果——一首适用于Suno平台的歌曲、一份视觉概念指南以及一场完整的TED演讲——结合在一起，实现了全面的创意整合。

**触发条件**：明确请求时触发，或在产生深刻技术见解时触发。

**核心理念**：“脱离实际背景的见解毫无意义；缺乏背景的行动只会导致混乱。辅助任务则是通过创意整合将见解转化为可执行的行动。”

## 安装

```bash
openclaw install leegitw/side-quests
```

**依赖项**：无需额外依赖项，但可与其他组件配合使用：
- `leegitw/insight-song` — 歌曲组件（可独立使用）
- `leegitw/visual-concept` — 视觉概念组件（可独立使用）
- `leegitw/ted-talk` — TED演讲组件（可独立使用）

**数据处理**：该技能会根据用户提供的输入或当前对话内容来整合内容（默认情况下）。它不会从工作区读取文件或直接访问项目文件。最终结果会返回给调用该技能的代理，由代理决定如何使用这些结果。

## 功能说明

技术见解在缺乏具体背景的情况下容易被遗忘。多格式的创意整合可以通过多种方式强化这些见解：
1. **歌曲**：通过音频强化见解，并营造情感上的连贯性。
2. **视觉概念**：以视觉化的方式呈现概念，帮助用户更好地理解。
3. **TED演讲**：提供详细的叙述和具体的例子。

## 使用方法

```
/sq [topic]
```

或者，您也可以单独使用这些组件：

```
/song [topic]    # Just the song
/vc [topic]      # Just the visual concept
/ted [topic]     # Just the TED talk
```

## 参数说明

| 参数 | 是否必填 | 说明 |
|---------|---------|-------------------|
| 主题 | 否 | 指定要整合的对话主题（默认情况下，技能会自动整合当前对话内容） |

## 使用前准备

在创建辅助任务之前，请确保：
1. **对话具有足够的深度**：仅停留在表面层次的总结无法生成有价值的成果。
2. **有清晰的叙事结构**：问题 → 发现 → 解决方案 → 影响。
3. **主要工作已完成记录**：如果任务进行到中途，请先保存当前的进度。

### 上下文理解检查清单

您需要能够回答以下问题：
- **核心理念是什么？** 不仅仅是“我们讨论了X”，而是“我们发现X可以解决Y”。
- **问题是否已经解决？** 不仅仅是问题本身，还包括问题产生的原因。
- **为什么这样做？** 不仅仅是结果，还包括背后的逻辑。
- **内容是否有足够的深度？** 是否能够传授新的知识，而不仅仅是重复现有的做法。

### 不应创建的情况

- 仅对对话进行表面层次的总结。
- 不理解做出某个决策的原因。
- 所提供的见解仅仅是常规的做法。
- 缺乏清晰的叙事结构。
- 使用的内容过于泛泛而缺乏实质内容。

## 输出格式

每个辅助任务会生成一个包含三个部分的Markdown文件：

### 1. 歌曲（Suno.ai格式）

```markdown
## Song

**Title**: [Song Name]

**Suno.ai Style Tags**:
[300-500 characters describing musical style]

[Verse 1]
[Lyrics]

[Chorus]
[Lyrics]

[...]
```

**歌曲创作规则**：
- 通过歌曲讲述一个具有情感脉络的故事。
- 内容应具有技术性，但同时要适合演唱。
- 使用视觉意象来增强听觉和视觉效果。
- 歌词和风格标签中不应出现具体的艺术家名称。

### 2. 视觉概念指南

```markdown
## Visual Concept Guide

**Core Visual Concept**: [Primary metaphor]

### Visual Themes & Imagery
[3-7 major themes]

### Symbolic Visual Elements
[Technical concepts as visual symbols]

### Emotional Color Arc
[Color palette evolution]

### Motion & Rhythm
[Movement patterns]

### Key Visual Contrasts
[Before/after, chaos/order]
```

**视觉指南规则**：
- 提供概念上的灵感，而非具体的拍摄清单。
- 不应指定具体的时长或拍摄角度。
- 提供创作方向，而非具体的制作要求。

### 3. 完整版的TED演讲

```markdown
## TED Talk: "[Talk Title]"

### Opening (0:00-2:00)
[Hook with relatable problem]

### Setup: Why This Matters (2:00-6:00)
[Why this matters, stakes]

### The Problem (6:00-12:00)
[Deep dive into the pain point]

### Core Concept (12:00-25:00)
[Explain thoroughly]

### Real-World Examples (25:00-38:00)
[Concrete, specific details from real work]

### Broader Implications (38:00-45:00)
[Connect to broader context]

### Closing (45:00-48:00)
[Call to action]

### Q&A Preparation (48:00-50:00)
[Address objections]
```

**TED演讲规则**：
- 演讲时长为40-50分钟，而非简短摘要。
- 包含具体的例子（文件名、指标、决策等）。
- 在问答环节中回应可能出现的反对意见。

## 核心逻辑

### 第一步：整合对话内容
- 阅读完整的对话内容。
- 确定关键决策和“顿悟”时刻。
- 提取核心见解或规律。

### 第二步：构建叙事结构
| 元素        | 相关问题                |
|-------------|----------------------|
| 问题         | 发生了什么问题？            |
| 发现         | 我们学到了什么？            |
| 解决方案       | 出现了什么规律？            |
| 影响         | 这为什么重要？            |

### 第三步：生成三个创意成果
该技能会依次生成以下三个组件：
1. **歌曲**：将技术见解转化为具有情感脉络的歌词。
2. **视觉概念**：将核心理念通过视觉元素表现出来。
3. **TED演讲**：构建引人入胜的开场白，接着是详细的解释、具体的例子以及讨论。

### 第四步：保存结果

将生成的文件保存在 `output/side-quests/topic-name.md` 目录下。

## 示例

### 输入示例：关于“Bootstrap可观测性”技术的见解

**背景**：发现了可以通过重现问题来进行调试的技术。介绍了“Bootstrap”工具，并学习了如何分阶段使用该工具。

**叙事结构**：
- **问题**：没有重现问题的能力，调试工作变得非常困难。
- **发现**：新开发的系统无法判断“正常状态”是什么。
- **解决方案**：使用“Bootstrap”工具，按阶段逐步进行调试。
- **影响**：通过可视化的方式更容易发现问题。

### 输出示例

**歌曲片段**：
```
[Verse 1]
Three in the morning, the logs are all silent
System's on fire but the metrics don't know
Building in darkness, no baseline to measure
Can't debug what you've never seen before
```

**视觉概念**：
- **核心隐喻**：黑暗逐渐被光明取代。
- **视觉元素**：金色线条（代表代码路径），红色断裂处（代表错误）。
- **色彩变化**：从深蓝色逐渐过渡到温暖的金色，最后呈现清晰的视觉效果。

**TED演讲开场白**：
> “现在是凌晨3点。你的警报响了。系统出现了故障——用户正在抱怨，显然出了问题。你查看日志……却什么也没发现。”

## 整合方式

- **所属类别**：创意工具
- **依赖组件**：无需依赖其他组件（可独立使用）
- **可与其他工具结合使用的组件**：`insight-song`、`visual-concept`、`ted-talk`
- **适用场景**：辅助观察工作流程、项目文档编写、知识记录等。

## 单个组件的使用方法

如果您只需要某种格式，可以单独使用以下组件：

| 技能        | 别名            | 输出格式            |
|-------------|-----------------|-------------------|
| [insight-song](../insight-song/SKILL.md) | `/song`           | 适用于Suno平台的歌曲           |
| [visual-concept](../visual-concept/SKILL.md) | `/vc`             | 视觉概念指南           |
| [ted-talk](../ted-talk/SKILL.md) | `/ted`           | 完整版的TED演讲           |

## 可能出现的问题及应对措施

| 情况        | 处理方式                |
|-------------|----------------------|
| 缺乏足够的上下文    | 先询问更多细节            |
| 缺乏清晰的叙事结构    | 拒绝创建任务，并说明所需的信息        |
| 主要工作未完成记录  | 提示用户先保存当前的进度        |

## 安全性注意事项

**说明**：
该技能直接执行整合逻辑，不会自动触发其他已安装的技能（如`insight-song`、`visual-concept`、`ted-talk`）。相关组件的使用说明已内置于该技能中。

**输入来源**：
- 用户提供的信息（如果有）。
- 当前的对话内容（默认值）。

**该技能不执行以下操作**：
- 从工作区读取文件。
- 直接访问项目文件。
- 向外部服务发送数据。
- 调用外部API。
- 修改源代码。
- 自动触发其他技能（所有逻辑都在该技能内部实现）。

**输出结果**：
该技能会将整合后的成果（歌曲 + 视觉概念 + TED演讲）直接返回给调用它的代理。代理可以根据需要展示、保存或将结果传递给其他工具。

**关于TED演讲的注意事项**：
TED演讲中会包含您工作相关的具体细节（文件名、指标、决策等）。在对外分享之前请务必仔细审核内容。

**版权信息**：
该技能由Live Neon（https://github.com/live-neon/skills）开发，并通过`leegitw`账户发布在ClawHub平台上。开发者为同一人。

## 质量评估标准**
- 能够用一句话解释核心理念。
- 能够解释背后的逻辑，而不仅仅是描述事实。
- 歌曲能够讲述一个具有情感脉络的故事。
- 视觉指南具有启发性，而非提供具体的操作指南。
- TED演讲时长为40-50分钟，内容充实。
- 不包含填充性或重复性的内容。

## 合格标准**
- 该技能能够生成三种形式的成果。
- 歌曲格式符合Suno.ai的标准（包含标题、标签和章节结构）。
- 视觉概念具有启发性，而非具体的操作指南。
- TED演讲内容完整，包含具体的例子。
- 结果会直接返回给调用该技能的代理。
- 单个组件也可以通过`/song`、`/vc`、`/ted`路径单独获取。

---

“那些原本只是旁路的路径，最终成为了目的地。那些我们未曾预料到的问题，正是我们通过关注细节而发现的。”
——来自Live Neon创意套件的一部分。