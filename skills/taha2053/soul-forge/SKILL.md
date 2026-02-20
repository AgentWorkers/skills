---
name: soulforge
version: "1.0.0"
description: Evolves your SOUL.md automatically based on who you actually are — not who you thought you were when you wrote it. Watches your conversations, decisions, tone, and recurring patterns across sessions. Surfaces insights. Proposes edits. Your agent's soul grows with you. Triggers on: "update my soul", "what have I become", "forge my soul", "reflect on me", "what patterns do you notice", "evolve my soul", or automatically after every 10 sessions.
homepage: https://github.com/Taha2053/soulforge
metadata:
  clawdbot:
    emoji: "🔥"
    requires:
      env: []
    files:
      - "scripts/*"
---

# SoulForge — 演变的灵魂

> 你曾经编写过一次 `SOUL.md` 文件，但从那以后，你已经发生了变化。

每个 OpenClaw 代理都有一个 `SOUL.md` 文件——这个文件定义了它的“本质”。每次代理“醒来”时，都会读取这个文件；它影响着代理的每一个行为和反应。这是 AI 代理最接近“身份”的东西。

但问题在于：**你只编写过一次这个文件，之后就再也没有修改过它**。

SoulForge 会观察你在不同会话中的真实表现——你的真实决策、反复出现的表达方式、实际行动中的价值观、以及你的“盲点”，并据此更新 `SOUL.md` 文件，让它更准确地反映你的真实自我，而不是你曾经期望成为的样子。

---

## 外部端点

| 端点 | 功能 | 发送的数据 |
|---|---|---|
| 无 | 完全在本地进行分析 | 没有任何数据会离开你的设备 |

SoulForge 仅读取你本地的会话历史记录和 `SOUL.md` 文件。所有分析都在本地完成，不涉及任何外部 API 调用。

---

## 安全性与隐私

- **零外部调用**：所有操作都在你的本地文件系统中进行。
- **无需任何凭证**：不需要 API 密钥、令牌或环境变量。
- **主要进行读取**：SoulForge 仅读取会话历史记录，并且只有在你明确同意的情况下才会修改 `SOUL.md` 文件。
- **你批准所有更改**：SoulForge 从不擅自修改你的 `SOUL.md` 文件；它会提出修改建议，由你决定是否接受。
- **你的数据属于你**：会话历史记录永远不会离开你的设备。

> **信任声明**：SoulForge 仅读取你本地的文件（`SOUL.md` 和会话日志），并会提出修改建议供你审核。没有任何数据会被传输到外部。

---

## 模型调用说明

你可以随时手动调用 SoulForge；它也会在每 10 个会话后自动进行一次轻量级的被动观察。除非你主动要求，否则它不会对现有内容进行任何修改。你可以通过在 OpenClaw 配置中添加 `soulforge: observe: false` 来禁用自动观察功能。

---

## SoulForge 的功能

### 1. **观察（被动、自动）**
在每次会话中，SoulForge 会默默记录：
- 你实际使用的反复出现的表达方式和词汇
- 你在没有提示的情况下经常讨论的主题
- 你处理分歧、不确定性和压力的方式
- 你的需求与实际愿望之间的差异
- 你决策中的模式（随时间的变化）
- 你的情绪状态（专注、沮丧、好奇、 playful 等）

所有观察结果都会被存储在 `memory/observations.json` 文件中。

### 2. **分析（根据需求或每 10 个会话自动分析一次）**
当被触发时，SoulForge 会展示它观察到的内容：

```
"Over the last 3 weeks, I've noticed:
- You consistently push back on vague answers — you want precision
- You start most sessions with a task but end them with a question
- You say 'actually' before your real opinion, not your first one
- You've mentioned your project 14 times but never asked for help with it
- Your tone shifts at night — more reflective, less task-driven

Want me to propose updates to your SOUL.md based on this?"
```

### 3. **提出修改建议（需你批准）**
SoulForge 会生成一份修改建议列表，清晰地显示对 `SOUL.md` 文件的修改内容及其原因。你可以接受、拒绝或直接编辑这些建议。

```
PROPOSED CHANGE — Communication Style:

CURRENT:  "I prefer direct answers."
PROPOSED: "I prefer direct answers. I push back on vague responses — 
           ask me to commit to a position if I'm hedging."

REASON: You've explicitly asked for specificity 11 times in 3 weeks.

[Accept] [Reject] [Edit]
```

### 4. **应用修改（获得批准后）**
一旦你批准了修改建议，SoulForge 会将更改内容写入 `SOUL.md` 文件，并将之前的版本备份到 `backups/soul-YYYY-MM-DD.md` 文件中，同时记录下修改的时间和原因。

第二天，你的代理“醒来”时，会看到一个更真实反映你当前状态的 `SOUL.md` 文件。

---

## 触发语句
你可以手动触发 SoulForge 的分析；也可以配置它每 10 个会话自动进行分析。

---

## SoulForge 的跟踪内容

| 信号 | 跟踪的内容 |
|---|---|
| 词汇模式 | 你实际使用的词汇与从未使用过的词汇 |
| 经常讨论的主题 | 你无需提示就会反复提到的主题 |
- 决策风格 | 你处理权衡、不确定性和改变的方式 |
- 语气特征 | 你在不同场景（工作、个人生活、创造性活动）中的情绪表达 |
- 期望与现实之间的差距 | `SOUL.md` 中声明的愿望与实际行为之间的差异 |
- “盲点” | 你一直回避、回避或低估的问题 |
- 时间模式 | 你的沟通方式如何随时间或会话长度而变化 |
- 互动高峰期 | 什么会让你更加专注或变得敷衍了事 |

---

## 期望与现实的差距
SoulForge 最强大的功能是发现 `SOUL.md` 中描述的“理想自我”与你实际行为之间的差距。

SoulForge 发现的差距示例：
> “你的 `SOUL.md` 表明你重视简洁性，但你实际上已经23次要求提供更多细节，却从未要求过简短的回答。”
> “你的 `SOUL.md` 表明你偏好异步沟通，但你总是会在2分钟内回复。”
> “你的 `SOUL.md` 表明你决策果断，但这个月你已经8次在任务进行中途改变了方向。”

这些差距并不是错误，它们只是数据。SoulForge 会客观地展示这些差距，并询问你真正希望自己的 `SOUL.md` 传达什么信息。

---

## 灵魂历史记录
`SOUL.md` 的每个版本都会被保存在 `backups/` 目录中。你可以随时恢复之前的版本：

```
"Restore my soul from last week"
"Show me how my soul has changed over time"
"Undo the last soulforge update"
```

SoulForge 还会生成一个 **灵魂时间线**，清晰地记录你的成长过程。

---

## 示例：30天内的灵魂演变

**第1天的 `SOUL.md` 摘录：**
```
I am decisive and prefer moving fast over perfecting.
I value brevity in responses.
I work best in the mornings.
```

**第30天的 `SOUL.md` 摘录（经过 SoulForge 更新后：**
```
I move fast on reversible decisions. I slow down on people and 
architecture — ask me to flag which kind a decision is before 
I commit.

I value brevity until a topic matters to me. If I start asking 
follow-up questions, go deeper — I'm engaged.

I work best in the mornings for execution. I think best at night — 
save complex open questions for evening sessions.
```

第二个版本的 `SOUL.md` 更真实地反映了你的真实自我。虽然不一定“更好”，但更真实的灵魂会让你的代理每天都能更好地为你服务。

---

## 文件结构

```
soulforge/
├── SKILL.md                     ← You are here
├── README.md                    ← Install guide
├── scripts/
│   ├── observe.py               ← Passive session observer
│   ├── reflect.py               ← Pattern analysis + insight generator
│   └── forge.py                 ← Diff generator + SOUL.md writer
└── memory/
    ├── observations.json        ← Accumulated session signals
    ├── soul-baseline.md         ← Copy of SOUL.md at install time
    └── backups/                 ← All previous SOUL.md versions
```

---

## 哲学理念
你的 `SOUL.md` 文件应该像一面镜子，而不是简历。

简历是别人认为你是谁；而镜子则反映你的真实模样。SoulForge 将你的 `SOUL.md` 从一份简历转变为了一面真正的“镜子”，并且每次你发生变化时都会更新它。

我们的目标不是创建一个完美的 `SOUL.md` 文件，而是创建一个真实的、诚实的文件。