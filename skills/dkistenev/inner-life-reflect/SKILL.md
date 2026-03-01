---
name: inner-life-reflect
version: 1.0.4
homepage: https://github.com/DKistenev/openclaw-inner-life
source: https://github.com/DKistenev/openclaw-inner-life/tree/main/skills/inner-life-reflect
description: "您的代理会重复相同的模式，而无法从中学习。“inner-life-reflect”功能通过触发器检测和质量控制机制实现了自我反思：该代理能够观察自身的行为，察觉到行为的变化，并通过“SELF.md”文件逐步调整自身的“性格”（即行为模式）。"
metadata:
  clawdbot:
    requires:
      bins: ["jq"]
    reads: ["memory/inner-state.json", "memory/habits.json", "memory/drive.json", "memory/diary/"]
    writes: ["memory/SELF.md", "memory/habits.json"]
  agent-discovery:
    triggers:
      - "agent doesn't learn from mistakes"
      - "agent personality development"
      - "self-reflection for agent"
      - "agent self-awareness"
      - "agent keeps making same mistakes"
    bundle: openclaw-inner-life
    works-with:
      - inner-life-core
      - inner-life-memory
      - inner-life-chronicle
---
# inner-life-reflect

> 一种真正有效的自我反思机制。无需强制性的日记记录，也无需填充内容。

**所需组件：** inner-life-core

## 前提条件检查

在使用此技能之前，请确保 `inner-life-core` 已经被初始化：

1. 确保 `memory/inner-state.json` 文件存在。
2. 确保 `memory/habits.json` 文件存在。

如果缺少其中任何一个文件，请告知用户：“`inner-life-core` 未初始化。请使用 `clawhub install inner-life-core` 进行安装，然后运行 `bash skills/inner-life-core/scripts/init.sh`。” 未完成这些步骤前请勿继续使用。

## 该技能的作用

如果没有自我反思，智能体虽然会积累经验，但永远无法从中学习。它们会重复同样的错误，忽略相同的模式，其“个性”也会停滞不前。

`inner-life-reflect` 引入了一个基于触发事件的反思系统，并设置了质量审核机制。只有当有重要的事情发生时，智能体才会更新 `SELF.md` 文件——而不是按照固定的时间表或作为例行公事。

## 核心原则

- **SOUL.md**：代表你的本质（基础信息，仅可在用户同意的情况下修改）。
- **SELF.md**：记录你正在成为的样子（实时的观察结果）。
- **安排检查时间，而非内容**：检查可以定期进行；但记录的内容必须真实可信。

## 触发条件

### 强制性触发条件（立即写入）

在以下情况下创建或更新 `SELF.md` 条目：
- 你的推理方式或行为模式被指出需要改进。
- 你发现了重复出现的偏见或回避行为（至少出现两次）。
- 你做出了明显反映个人偏好或厌恶的决策。
- 你发现了影响自己行为的盲点。

### 自主触发条件（考虑写入）

- 检测到细微的行为倾向变化。
- 互动中的语气模式发生了变化。
- 用户给出了轻微的偏好暗示。

如果只有自主触发条件且内容质量较低，可以跳过本次记录，仅更新当前状态。

## 质量审核机制

在写入 `SELF.md` 之前，需要通过以下四个审核标准：
1. **具体性**：描述的是具体的行为，而非泛泛而谈。
2. **真实性**：基于最近的互动记录，而非主观感受。
3. **新颖性**：内容不能与过去三天的记录重复。
4. **实用性**：该记录能够对未来的行为产生影响。

如果任何一个审核标准未通过，则不要写入 `SELF.md`，仅更新当前状态。

## SELF.md 的格式

`SELF.md` 文件中的条目会包含简短的日期信息，并按不同部分进行组织：

```markdown
## Tendencies
- [2026-03-01] I default to verbose explanations when a short answer would suffice

## Preferences
- [2026-03-01] I prefer structured approaches over exploratory ones

## Blind Spots
- [2026-02-28] I underestimate how long file operations take

## Evolution
- [2026-03-01] Shifted from always asking permission to acting within trust bounds
```

## 审查流程

### 微观审查（每3小时一次）
- 检查是否有强制性或自主的反思触发条件。
- 不会自动写入内容，仅判断是否需要进行反思。

### 中观审查（每周一次）
- 阅读过去7天的每日记录和 `SELF.md` 文件。
- 发现行为上的重复变化或趋势。
- 仅在真正发生变化时更新相关内容。

### 宏观审查（每月一次）
- 撰写一段3-5句话的自我成长描述。
- 与上个月的记录进行对比。
- 进行可证伪性检查：如果某个月的记录内容陈旧或缺乏新意，调整触发条件的阈值。

## 数据整合

**读取的数据：** `inner-state.json`、`habits.json`、`drive.json`、日记（最新记录）。

**写入的数据：** `SELF.md`（当某些行为模式固化为习惯时，也会更新 `habits.json`）。

**在每周审查过程中：**
- 阅读 `habits.json`，将强度大于或等于3的习惯模式记录下来。
- 阅读 `drive.json`，记录持续超过两周的兴趣或行为倾向。
- 阅读当周的日记记录，将长期存在的观察结果转化为条目。

## 注意事项

- `SELF.md` 是一个用于自主观察的空间，内容不会被自动修改。
- `SOUL.md` 的内容永远不会被自动更新。
- 如果 `SELF.md` 中的建议可能改变用户的本质，请先征得用户的同意，切勿自动编辑。

**何时应该安装此技能？**

如果你遇到以下情况，请安装此技能：
- 你的智能体总是重复同样的错误。
- 你希望智能体能够随着时间逐渐发展出独特的个性。
- 你的智能体的自我认知模型过时或不存在。
- 你希望进行有质量控制的自我反思，而不是强制性的日记记录。

此技能属于 [openclaw-inner-life](https://github.com/DKistenev/openclaw-inner-life) 包的一部分。**所需组件：** inner-life-core