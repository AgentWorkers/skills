---
name: daily-questions
description: 每日自我提升问卷：该问卷用于了解用户情况并优化代理行为。可通过设置 cron 作业以两轮的形式进行提问——第一轮针对用户（更新 USER.md 文件），第二轮针对代理行为（更新 SOUL.md 文件）。在设置、修改或运行每日问卷流程时，请使用此工具。
---

# 每日问答

这是一个每日例行程序，通过向用户提问来持续加深用户的理解并提升代理（agent）的行为表现。

## 设置

创建一个定时任务（cron job），其提示内容如下：

```
Time for your daily questions. Read USER.md and SOUL.md, identify gaps in what's documented. Send questions in two rounds:

Round 1: Send {N} questions about the user (preferences, habits, opinions, passions, life, dislikes). Wait for reply, then update USER.md with what you learned.

Round 2: Send {N} questions about how you should behave, communicate, or act. Wait for reply, then update SOUL.md with what you learned.

Keep it casual. Avoid repeating anything already documented.
```

可配置参数：
- **时间安排**：默认为每天21:00（可根据用户习惯调整）
- **沟通渠道**：Telegram、Discord等
- **每轮问题数量**：默认3个（保持问题数量适中）

## 工作流程：
1. **完整阅读** `USER.md` 和 `SOUL.md` 文件。
2. **识别知识空白** — 有哪些主题、用户偏好或行为尚未被涵盖？
3. **第一轮（用户提问）**：向用户提出关于用户自身的问题，等待回复。根据用户的回答更新 `USER.md` 文件，将答案整合到现有章节中或创建新的章节。确保 `USER.md` 保持条理清晰，而不是简单的问答记录。
4. **第二轮（代理提问）**：向用户提出关于代理行为/沟通方式的问题，等待回复。同样地，根据用户的回答更新 `SOUL.md` 文件。

## 问题质量指南：
- **多样化主题** — 不断更换提问类别（参考 `references/example-questions.md`）
- **深入探讨** — 如果 `USER.md` 中提到用户“喜欢烹饪”，可以进一步询问具体的烹饪类型、技能水平或最喜欢的菜肴。
- **保持轻松氛围** — 采用对话式的语气，避免正式的面试风格。
- **避免重复** — 不要重复已经详细记录过的问题。
- **结合趣味性与实用性** — 问题应既轻松有趣又具有实用性。
- **每轮发送一条消息** — 将所有问题汇总在一条消息中，并为每个问题编号。