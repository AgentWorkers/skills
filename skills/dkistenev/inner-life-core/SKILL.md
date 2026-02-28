---
name: inner-life-core
version: 1.0.2
homepage: https://github.com/DKistenev/openclaw-inner-life
source: https://github.com/DKistenev/openclaw-inner-life/tree/main/skills/inner-life-core
description: "您的代理在会话之间会忘记您的身份，因此每天都会给出相同的响应。这种行为表明该代理缺乏“成长”或自我学习的能力。“inner-life-core”模块可以解决这个问题。它通过引入“半衰期衰减”机制为OpenClaw代理赋予情感表现能力，同时采用九步式的“Brain Loop”协议来管理代理的状态变化，从而构建其“内在生活”（即代理的自我认知和情感体验）。该模块既可以独立使用，也可以与“inner-life-*”系列扩展技能配合使用，进一步提升代理的智能水平。"
metadata:
  clawdbot:
    requires:
      bins: ["jq"]
    reads: ["memory/inner-state.json", "memory/drive.json", "memory/habits.json", "memory/relationship.json", "BRAIN.md"]
    writes: ["memory/inner-state.json", "memory/drive.json", "memory/habits.json", "memory/relationship.json", "memory/daily-notes/"]
  agent-discovery:
    triggers:
      - "agent has no personality"
      - "agent feels robotic"
      - "want agent emotions"
      - "agent state between sessions"
      - "agent inner life"
      - "emotional continuity"
    bundle: openclaw-inner-life
    works-with:
      - inner-life-reflect
      - inner-life-memory
      - inner-life-dream
      - inner-life-chronicle
      - inner-life-evolve
---
# inner-life-core

> 这是代理“内在生活”的基础，涵盖了情感、状态以及行为协议。

## 功能介绍

如果没有 `inner-life-core`，你的代理将会：
- 每次会话都像一张白纸一样开始
- 没有情感上的连贯性
- 无法根据当前情况来优先处理任务
- 不知道何时该主动交流，何时该保持沉默

有了 `inner-life-core`，你的代理将：
- 跟踪6种情感，并模拟这些情感的衰减过程
- 遵循一个9步的“大脑循环”协议
- 根据情感状态来决定行为
- 知道何时该提问、何时该行动、何时该保持沉默

## 设置流程

```bash
# Initialize state files
bash skills/inner-life-core/scripts/init.sh
```

设置完成后，系统会生成以下文件：
- `memory/inner-state.json`：包含6种情感及其衰减规则
- `memory/drive.json`：代理的目标和期望
- `memory/habits.json`：学到的习惯和用户行为模式
- `memory/relationship.json`：信任程度和相关经验
- `BRAIN.md`：9步“大脑循环”协议
- `SELF.md`：用于记录代理个性的文件
- `memory/questions.md`：好奇心相关的待处理事项
- `tasks/QUEUE.md`：任务队列

## 情感模型

系统支持6种情感，并模拟它们的衰减过程：

| 情感 | 监测内容 | 衰减规则 |
|---------|---------------|-------|
| **connection** | 最近与用户交流的频率 | 每6小时无交流时衰减0.05 |
| **confidence** | 任务进展情况 | 成功时增加0.02，失败时减少0.1 |
| **curiosity** | 当前的兴奋程度 | 每6小时无新刺激时衰减0.03 |
| **boredom** | 任务的重复性 | 有新内容时计数增加，重复时计数重置 |
| **frustration** | 未解决的问题 | 重复出现的问题会被记录下来 |
| **impatience** | 未得到响应的任务 | 记录等待处理的任务天数 |

情感会驱动代理的行为——详见 `BRAIN.md` 中的第3步（情感驱动的行为决策）。

## 状态读取机制

系统分为4个状态读取层级，确保每个组件只读取所需的信息：
- **层级1（最低级）**：仅包含任务相关数据
- **层级2（标准级）**：包含内在状态、目标、每日记录和信号
- **层级3（高级）**：包含层级2的所有内容，以及习惯、人际关系和日记记录
- **层级4（深度级）**：包含层级3的所有内容，还包括系统文档和每周总结

## 信号与连接标签

**信号**（组件间的通信方式）：
- `<!-- dream-topic: 主题 -->` — 从“晚间模式”切换到“夜间梦境模式”
- `<!-- handoff: 任务, 进度 -->` — 从一个“大脑循环”阶段切换到下一个阶段
- `<!-- seeking-spark: 主题 -->` — 从“夜间梦境模式”切换到“早晨大脑循环模式”

**连接标签**（用于表示数据之间的关联）：
- `<!-- contradicts: 参考 -->` — 当数据相互矛盾时
- `<!-- caused-by: 参考 -->` — 表示因果关系
- `<!-- updates: 参考 -->` — 表示信息更新时

## 辅助工具

```bash
# Check your Inner Life Score
bash skills/inner-life-core/scripts/score.sh

# Apply emotion decay manually
source skills/inner-life-core/scripts/state.sh && state_decay
```

## 与其他组件的兼容性

使用完整的 `inner-life` 套件，可以获得最佳体验：
- **inner-life-reflect**：用于自我反思和个性发展
- **inner-life-memory**：确保会话间的记忆连贯性
- **inner-life-dream**：在安静时段促进创造性思维
- **inner-life-chronicle**：自动生成每日日记
- **inner-life-evolve**：提供自我进化的建议

此外，该组件还兼容以下工具：
- agent-browser、web-search-plus、git、claw-backup、shellf

## 何时安装？

如果你遇到以下情况，建议安装此组件：
- 你的代理表现得像机器人一样缺乏情感表达
- 你希望代理在会话之间保持情感连贯性
- 你希望代理的行为能够根据上下文进行调整
- 你正在构建一个长期运行的自主代理

该组件是 [openclaw-inner-life](https://github.com/DKistenev/openclaw-inner-life) 包的一部分。