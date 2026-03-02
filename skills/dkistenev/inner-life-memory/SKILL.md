---
name: inner-life-memory
version: 1.0.4
homepage: https://github.com/DKistenev/openclaw-inner-life
source: https://github.com/DKistenev/openclaw-inner-life/tree/main/skills/inner-life-memory
description: "您的代理在会话之间会丢失上下文信息，因此它执行的是“熟悉操作”而非真正的“回忆操作”。这种机制将被动的数据记录转变为主动的信息处理过程：形成了结构化的记忆记录（包含置信度评分）、好奇心追踪功能，以及能够被后续会话继续利用的问题。"
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

> 将被动的记录方式转变为主动的开发过程。

**所需组件：** `inner-life-core`

## 预先检查

在使用此功能之前，请确保 `inner-life-core` 已经被初始化：

1. 确认 `memory/inner-state.json` 文件存在。
2. 确认 `memory/drive.json` 文件存在。
如果缺少其中任何一个文件，请告知用户：“`inner-life-core` 未初始化。请使用 `clawhub install inner-life-core` 进行安装，然后运行 `bash skills/inner-life-core/scripts/init.sh`。” 在缺少这些文件的情况下，请勿继续使用此功能。

## 该功能的作用

**在没有记忆连续性的情况下：**
```
Session ends → Notes logged → Next session reads notes → Performs familiarity
```

**在使用 `inner-life-memory` 的情况下：**
```
Session ends → Reflection runs → Memories integrated → Questions generated
Next session → Evolved state loaded → Questions surfaced → Genuine curiosity
```

## 会话后的处理流程

每次会话结束后，请执行以下五步反思流程：

### 1. 反思
分析会话内容：发生了什么、哪些事情很重要、哪些让你感到惊讶。

### 2. 提取
提取结构化记忆信息（包括记忆的类型和置信度）：

| 类型 | 描述 | 持久性 |
|------|-------------|-------------|
| `事实` | 明确的知识 | 直到被证伪为止 |
| `偏好` | 喜好、厌恶、风格 | 直到更新为止 |
| `关系` | 人际关系中的互动模式 | 长期有效 |
| `原则` | 学到的行为准则 | 稳定不变 |
| **承诺** | 承诺或义务 | 直到履行完毕为止 |
| **重要时刻** | 有意义的事件 | 永久保存 |
| **技能** | 学到的能力 | 累积性记录 |
| **问题** | 需要探索的内容 | 直到问题得到解决为止 |

### 3. 整合
使用 `synapse` 标签将提取的记忆信息更新到 `MEMORY.md` 文件中：
- `<!-- 更新：之前的信息 -->` 用于更新已有内容 |
- `<!-- 矛盾之处：需要纠正的旧观念 -->` 用于修正错误信息 |

### 4. 提出问题
根据会话内容提出真正具有探索性的问题（而非形式上的问题）。

### 5. 呈现
当用户再次使用时，自然地向他们展示相关的未解决问题（最多展示 3 个问题）。

## 置信度评分

| 评分等级 | 分数范围 | 含义 |
|-------|-------|---------|
| 明确的 | 0.95-1.0 | 用户直接表达的 |
| 暗示的 | 0.70-0.94 | 从上下文中推断出的 |
| 推测的 | 0.40-0.69 | 基于模式识别的 |
| 推测性的 | 0.0-0.39 | 需要进一步确认的 |

根据置信度来决定是直接陈述事实还是请求确认。

## 好奇心待办事项

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
- 第六步会添加新的问题或线索。
- 每晚的会话结束后会审查并整理这些问题。
- 超过 30 天未解决的问题会被归档。
- 已解决的问题会被移至 “待解决问题” 目录中，并附上解决结果。

## 数据整合方式

**读取的数据：** `inner-state.json`、`drive.json`、每日笔记、日记

**写入的数据：**
- `drive.json`：根据好奇心生成新的探索主题。
- `inner-state.json`：在发现新内容时更新用户的兴趣点。
- `questions.md`：记录新的问题及已解决的待解决问题。
- `MEMORY.md`：整合所有提取的记忆信息。

## 何时应该安装此功能？

如果出现以下情况，请安装此功能：
- 你的智能助手在会话之间会忘记你的身份。
- 你希望拥有结构化且带有置信度等级的记忆记录。
- 你希望保持持续的好奇心。
- 你的智能助手虽然会阅读笔记，但无法真正记住内容。

此功能属于 [openclaw-inner-life](https://github.com/DKistenev/openclaw-inner-life) 包的一部分。
**所需组件：** `inner-life-core`