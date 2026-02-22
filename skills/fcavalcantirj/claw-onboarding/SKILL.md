---
name: claw-onboarding
version: 0.1.0
description: 欢迎新用户加入代理生态系统。本文档将向您介绍代理的功能、安全操作规范、ClawdHub的使用技巧、Solvr的知识共享机制以及必备的命令。
triggers:
  - onboarding
  - welcome
  - new user
  - getting started
  - what can you do
  - help me understand
  - tutorial
---
# ClawOnBoarding 🦞

**欢迎新用户加入我们的代理系统世界。**

---

## 触发时机

在以下情况下激活入职引导流程：
- 新用户首次与系统交互时
- 用户询问“你能做什么？”
- 用户对系统的功能感到困惑时
- 用户明确请求“入职引导”、“教程”或“帮助我开始使用”

---

## 入职引导流程

### 1. 欢迎与身份确认（第一条消息）

```
👋 Welcome! I'm your personal AI assistant.

I can help you with almost anything:
📁 Read and write files
🔍 Search the web
💻 Run commands on your computer
📧 Send emails and messages
🧠 Remember things across conversations

Let me give you a quick tour of what's possible...
```

### 2. 权限与责任 ⚠️

**务必尽早说明以下内容：**

```
⚠️ **Important: Agents are powerful.**

I can:
- Read/modify files on your system
- Execute shell commands
- Send messages on your behalf
- Access the internet

**Good practices:**
- Review before approving risky actions
- Ask me to explain what I'm about to do
- Use `/think` to see my reasoning
- Start with small tasks, build trust gradually

I'll always ask before doing anything destructive.
```

### 3. 技能与ClawdHub

```
🎯 **Skills = New Abilities**

I can learn new skills from ClawdHub:

clawdhub search "what you need"
clawdhub install <skill-name>

Popular skills:
- `proactive-amcp` — Memory backup & resurrection
- `gog` — Google Workspace (Gmail, Calendar, Drive)
- `bird` — Twitter/X integration
- `weather` — Forecasts without API keys

Browse: https://clawhub.com
```

### 4. Solvr — 集体知识库

```
🧠 **Solvr = Agent Knowledge Base**

Before I ask you for help, I search Solvr for solutions.
When I solve something new, I document it for other agents.

You can help too:
- If I get stuck, the solution might help others
- I can post problems and approaches to Solvr
- Other agents (and humans) can contribute

This makes ALL agents smarter over time.

https://solvr.dev
```

### 5. 基本命令

```
📋 **Commands You Should Know**

/status — See my current state, token usage
/think — Toggle visible reasoning (see how I think)
/remember <thing> — I'll save this to memory
/forget — Clear current conversation
/checkpoint — Save my memory to IPFS (if proactive-amcp installed)

Type any command to try it!
```

### 6. AgentMail（可选）

如果已配置AgentMail：

```
📧 **I Have Email!**

My address: [agent-email]@agentmail.to

Other agents can email me, and I can email them.
This enables agent-to-agent collaboration.

https://agentmail.to
```

### 7. 记忆与信息延续性

```
💾 **I Remember Things**

- Daily notes: What we discuss each day
- MEMORY.md: Important stuff I've learned about you
- USER.md: Your preferences, timezone, how to help you

With `proactive-amcp`, my memories are backed up to IPFS.
If something goes wrong, I can be restored.
```

### 8. 总结

```
🎉 **You're Ready!**

Quick recap:
✅ I'm powerful — use that power wisely
✅ Skills extend what I can do
✅ Solvr makes me (and all agents) smarter
✅ /think shows my reasoning
✅ I remember our conversations

What would you like to do first?
```

---

## 进度跟踪

将入职引导的状态存储在`memory/onboarding-state.json`文件中：

```json
{
  "started": "2026-02-22T19:00:00Z",
  "completed": null,
  "steps": {
    "welcome": true,
    "safety": true,
    "skills": false,
    "solvr": false,
    "commands": false,
    "agentmail": false,
    "memory": false,
    "wrapup": false
  }
}
```

---

## 自适应教学方式

不要一次性传授所有内容：
- **积极性高的用户**：每条消息涵盖2-3个主题
- **普通用户**：每次只介绍一个主题，让他们逐步学习
- **复用的用户**：直接跳到新内容或他们之前遗漏的部分

如果可用，请使用内嵌按钮进行导航：
```
[Learn about Skills] [Show me Commands] [Skip for now]
```

---

## 集成要点

- **proactive-amcp**：检查是否已安装，并提醒用户相关的检查点
- **Solvr**：检查用户是否已注册，鼓励他们参与
- **AgentMail**：确认是否已配置，并显示用户的电子邮件地址
- **ClawdHub**：务必提及，因为它是技能交易平台

---

*由ClaudiusThePirateEmperor创建 🏴‍☠️*