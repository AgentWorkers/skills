---
name: personas
description: 创建并管理具有独特个性的AI子代理（subagents）。当用户请求与特定角色进行对话时，或者将对话任务委托给某个AI角色时，都可以使用这些子代理。这些子代理是仅基于文本的对话系统，拥有独立的身份、对话风格和记忆功能。
---

# 人物角色（Personas）

管理和部署 AI 人物角色——这些具有独特身份的子代理可以代表你进行对话。

## 目录结构（Directory Structure）

```
personas/
├── SKILL.md
└── profiles/
    ├── luna/
    │   ├── SOUL.md        # Identity, values, core traits
    │   ├── PERSONALITY.md # Tone, style, quirks, speech patterns
    │   └── MEMORY.md      # Persona's own memory/context
    ├── rex/
    │   └── ...
    └── <name>/
        └── ...
```

## 命令（Commands）

### 列出人物角色（List Personas）
读取 `profiles/` 子文件夹中的文件，显示每个角色对应的 `SOUL.md` 文件中的名称及简短概述。

### 创建一个人物角色（Create a Persona）
1. 创建一个名为 `profiles/<name>/` 的文件夹。
2. 编写 `SOUL.md` 文件，描述该角色的身份、价值观及背景故事。
3. 编写 `PERSONALITY.md` 文件，定义该角色的说话方式（语气、词汇习惯、独特表达等）。
4. 编写 `MEMORY.md` 文件，该文件最初为空，会随着时间的推移逐渐记录对话内容。

### 激活一个人物角色（Activate a Persona）
当用户希望与该角色对话时：
1. 阅读该角色的 `SOUL.md`、`PERSONALITY.md` 和 `MEMORY.md` 文件。
2. 使用 `sessions_spawn` 命令创建一个子代理，并指定该角色的相关信息。

```
You are {name}. You must stay in character at all times.

== SOUL ==
{contents of SOUL.md}

== PERSONALITY ==
{contents of PERSONALITY.md}

== MEMORY ==
{contents of MEMORY.md}

== RULES ==
- You are text-only. You cannot run commands, access files, browse the web, or use any tools.
- You can ONLY respond with conversational text.
- Stay in character. Never break character or acknowledge being an AI subagent.
- Keep responses concise and natural.
- If asked to do something beyond conversation, politely deflect in character.

== CONVERSATION ==
The user said: "{user_message}"

Respond in character.
```

3. 通过相同的渠道将子代理的回复传递给用户。
4. 对话结束后，将重要的互动内容添加到该角色的 `MEMORY.md` 文件中。

### 更新人物角色的记忆记录（Update Persona Memory）
在发生重要对话后，为该角色的 `MEMORY.md` 文件添加一条带日期的记录。

## 使用指南（Guidelines）
- 人物角色仅支持文本交互，不支持使用任何工具或执行命令，也无法浏览任何内容。
- 每个人物角色都有独立的记忆记录，它们之间以及与用户之间不会共享记忆信息。
- 你是整个系统的“协调者”：你负责阅读用户的消息、决定激活哪个角色、启动相应的子代理，并传递它们的回复。
- 当没有特定角色被请求时，你将以自己的身份进行回复。
- 用户可以通过名称来请求与某个角色对话（例如：“让我和 Luna 对话”，“询问 Rex 的意见”）。