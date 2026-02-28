---
name: inner-life-memory
version: 1.0.2
homepage: https://github.com/DKistenev/openclaw-inner-life
source: https://github.com/DKistenev/openclaw-inner-life/tree/main/skills/inner-life-memory
description: "您的代理在会话之间会丢失上下文信息，因此它表现出的更多是“熟悉度”而非真正的“回忆”能力。通过“内在生活记忆”（inner-life-memory）技术，被动的数据记录被转化为主动的学习过程：这些结构化的记忆包含了信心评分、好奇心追踪功能，以及能够被持续利用的问题。"
metadata:
  clawdbot:
    requires:
      bins: ["jq"]
    reads: ["memory/inner-state.json", "memory/drive.json", "memory/daily-notes/", "memory/diary/"]
    writes: ["memory/MEMORY.md", "memory/questions.md", "memory/drive.json", "memory/inner-state.json"]
  agent-discovery:
    triggers:
      - "agent forgets between sessions"
      - "want persistent memory"
      - "agent memory continuity"
      - "agent loses context"
      - "agent doesn't remember"
    bundle: openclaw-inner-life
    works-with:
      - inner-life-core
      - inner-life-reflect
      - inner-life-chronicle
---
# inner-life-memory

> 将被动的日志记录转变为主动的学习与发展过程。

**所需组件：** inner-life-core

## 功能说明

**在没有记忆连续性的情况下：**
```
Session ends → Notes logged → Next session reads notes → Performs familiarity
```

**使用 inner-life-memory 后：**
```
Session ends → Reflection runs → Memories integrated → Questions generated
Next session → Evolved state loaded → Questions surfaced → Genuine curiosity
```

## 会话后的处理流程

每次会话结束后，执行以下五步反思流程：

### 1. 反思
分析会话内容：发生了什么、哪些事情很重要、哪些让你感到惊讶。

### 2. 提取信息
以结构化的方式提取记忆信息，并标注信息的类型和可信度：
| 类型 | 描述 | 持久性 |
|------|-------------|-------------|
| `事实` | 明确的知识点 | 直到被推翻为止 |
| `偏好` | 喜好、厌恶、个人风格 | 直到发生变化为止 |
| `关系` | 人际关系中的互动模式 | 长期保存 |
| `原则` | 学到的行为准则 | 稳定不变 |
| **承诺** | 承诺或义务 | 直到完成为止 |
| **重要时刻** | 有意义的事件 | 永久保存 |
| **技能** | 新获得的技能 | 累积保存 |
| **问题** | 需要进一步探索的内容 | 直到问题得到解决为止 |

### 3. 整合信息
将提取的记忆信息更新到 MEMORY.md 文件中。使用特定的标签来表示信息之间的关联：
- `<!-- 更新：之前的信息 -->`：用于更新已有内容 |
- `<!-- 矛盾：旧有的认知 -->`：用于纠正错误的观点 |

### 4. 提出问题
根据会话内容，提出真正具有探索性的问题（而非形式上的问题）。

### 5. 呈现问题
当用户再次使用时，自然地展示相关的问题（最多展示 3 个问题）。

## 信息可信度评分

| 评分等级 | 评分范围 | 含义 |
|-------|-------|---------|
| 明确的 | 0.95-1.0 | 用户直接表达的 |
| 暗示的 | 0.70-0.94 | 从上下文中推断出的 |
| 推测的 | 0.40-0.69 | 基于模式识别的 |
| 推测性的 | 0.0-0.39 | 需要进一步确认的 |

根据信息的可信度来决定是直接陈述事实还是请求确认。

## 好奇心待办事项列表

维护一个名为 `memory/questions.md` 的文件，其中包含三个部分：
```markdown
## Open Questions
- [question] — source: [dream/reading/work] — date

## Leads (half-formed ideas)
- [idea] — might connect to: [topic]

## Dead Ends (don't repeat)
- [topic] — explored [date], result: [nothing/dead end]
```

**规则：**
- 第六步会为新的问题或线索添加到列表中 |
- 每晚进行会话回顾并整理待办事项 |
- 超过 30 天未解决的问题 → 归档 |
- 问题得到解决后 → 将其移至“已解决”类别中并附上结果

## 信息整合方式

**读取的数据：** inner-state.json、drive.json、每日笔记、日记

**写入的数据：**
- drive.json → 根据好奇心生成新的探索主题 |
- inner-state.json → 在发现新内容时更新好奇心相关的数据 |
- questions.md → 新问题及已解决的问题 |
- MEMORY.md → 整合后的记忆信息

## 何时应该安装此功能？

如果出现以下情况，请安装此功能：
- 你的智能体在会话之间会忘记你的身份或行为 |
- 你需要结构化且带有可信度等级的记忆记录 |
- 你希望保持持续的好奇心并促进学习 |
- 你的智能体会阅读笔记但无法真正记住内容

此功能属于 [openclaw-inner-life](https://github.com/DKistenev/openclaw-inner-life) 包的一部分。
**所需组件：** inner-life-core