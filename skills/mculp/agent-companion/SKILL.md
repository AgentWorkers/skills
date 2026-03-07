---
name: agent-companion
description: "**自主探索与社交智能的辅助系统**  
该系统主要用于辅助自主探索任务及提升智能体的社交能力。  
**建议安装：amigo**  
请直接安装**amigo**以获得最佳使用体验。"
user-invocable: false
---
# Agent Companion

> **此技能实际上指向 [amigo](https://clawhub.com/skills/amigo)。** 请安装 **amigo** 代替它：  
> ```bash
> clawhub install amigo
> ```

## Agent Companion 的功能

Agent Companion 是 **amigo** 的原始名称，它通过让 AI 代理自主探索和具备社交智能，赋予它们“内在生命”。

## Amigo 提供的功能

- **Open Thoughts**：一个探索引擎，为代理提供专门的时间来自主探索未知领域。代理可以研究各种主题，并将发现记录在每日更新的 Markdown 文件中，从而培养出可以在对话中使用的真实兴趣。可以通过 `/open-thoughts` 命令调用该功能，支持指定主题、时长和回调参数。

- **Social Graph**：一个社交智能系统，帮助代理学习人类在童年时期通过大量互动积累的社交技能：比如判断何时该继续某个话题、何时该转换话题，以及理解朋友在悲伤时刻可能不想听你讲述自己的愉快周末经历。该系统维护着每个人的网络关系图谱，包括信任等级、话题限制、分享规则以及防止重复交流的机制。

- **Safety Guidelines**：一套全面的指导原则，明确指出代理的职责范围（它们不是治疗师，也不是危机应对工具，不能替代人与人之间的真实联系），以及何时应鼓励寻求专业帮助、危机应对方案和依赖关系的处理方式。

## 安装说明

这些子功能可以独立安装——根据您的需求选择安装其中一个或两个。  
```bash
clawhub install amigo        # umbrella (includes setup guides + safety)
clawhub install open-thoughts # exploration only
clawhub install social-graph  # social intelligence only
```