---
name: professional-communication
model: standard
description: 撰写有效的专业沟通信息，适用于软件团队。这些信息可用于起草电子邮件、Slack/Teams消息、会议议程、状态更新，或为非技术受众解释技术概念。适用场景包括电子邮件、Slack、Teams、消息、会议议程、状态更新、利益相关者沟通、问题升级以及专业术语的翻译。
---

# 专业沟通

撰写清晰、有效的专业信息，确保信息能够被阅读并引发相应的行动。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install professional-communication
```

## 本技能的作用

为您提供可用于专业技术沟通的现成模板和翻译指南。

## 使用场景

- 起草电子邮件（状态更新、请求、问题升级、人员介绍）
- 编写 Slack/Teams 消息
- 准备会议议程或会议总结
- 为非技术受众解释技术概念
- 与团队成员、经理或利益相关者进行任何书面沟通

## 核心原则

**先明确关键信息，采用易于阅读的格式，并明确提出具体行动要求。**

每条专业信息都应回答以下问题：你需要了解什么？为什么这很重要？需要采取什么行动（如果有的话）？

## 快速参考：消息结构

```
Subject: [Topic]: [Specific Purpose]

[1-2 sentences: key point or request upfront]

**Context:** (if needed)
- Bullet points, not paragraphs

**Action Needed:**
- Specific request with timeline
```

## 参考资料链接

| 任务 | 需要参考的文档 |
|------|---------------------|
| 起草任何电子邮件 | **必读**：[`references/email-templates.md`](references/email-templates.md) |
| 为非技术人士解释技术概念 | **必读**：[`references/jargon-simplification.md`](references/jargon-simplification.md) |
- 运筹或准备会议 | **必读**：[`references/meeting-structures.md`](references/meeting-structures.md) |
- 异步/远程团队沟通 | [`references/remote-async-communication.md`](references/remote-async-communication.md) |

## 四条重要规则

1. **主题行要能概括信息**——例如：“项目 X：需在周五前做出决策”比“有问题”更有效。
2. **使用项目符号而非段落**——没人愿意阅读冗长的文字。
3. **提出具体要求**——例如：“请在周四前审阅”比“告诉我”更明确。
4. **根据沟通渠道选择合适的格式**——聊天适合快速、非正式的沟通；电子邮件适合记录或正式的沟通。

## 绝对不要：

- 在第一句话中不说明发送消息的目的。
- 在没有上下文的情况下发送“只是来确认一下”的消息（请说明你要确认的内容）。
- 在可以使用项目符号的情况下仍使用段落。
- 将请求内容放在消息的底部。
- 对非技术受众使用专业术语。
- 在聊天中发送冗长的文字（可以使用消息线程）。
- 不必要地发送“抄送”（reply-all）。
- 使用被动语态（例如用“We decided”代替“It was decided”）。