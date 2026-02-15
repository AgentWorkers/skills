---
name: research
description: 通过 Gemini CLI 进行深度研究——该过程在后台的子代理中运行，因此您无需消耗自己的 Claude 代币。
homepage: https://github.com/google/gemini-cli
metadata: {"clawdbot":{"emoji":"🔬","requires":{"bins":["gemini"]}}}
---

# 研究技能

您可以使用 Gemini CLI 通过生成的子代理对任何主题进行深入研究。该功能会使用您的 Google AI 订阅权限，而无需消耗 Claude 令牌——非常适合那些会占用大量 Clawdbot 使用量的长时间研究任务。

## 工作原理

**当用户输入“Research: [主题]”或请求进行深入研究时：**

### 第一步：明确问题（始终必要）

在开始研究之前，先提出 2-3 个问题以明确研究方向：

**首先明确目标：**
> “在开始之前，您的研究目标是什么？是了解这个主题、做出决策，还是只是出于好奇？”

**然后根据用户的回答进行调整：**

- 如果用户是出于学习或好奇：
  - “您最感兴趣的特定方面是什么？”
  - “研究的深度应该达到什么程度？（是高层次概述还是详细的技术细节？）”

- 如果用户需要做出决策：
  - “您想要做出什么决定？”
  - “有哪些具体的标准或限制需要考虑？”

- 如果用户需要撰写或创建内容：
  - “最终成果是什么？（博客文章、报告还是演示文稿？）”
  - “目标受众是谁？”

**保持对话的自然流畅——问题数量控制在 2-3 个以内。**

### 第二步：生成研究代理

一旦了解了研究背景，使用 `sessions_spawn` 命令来启动研究过程：

```
sessions_spawn(
  task: "Research: [FULL TOPIC WITH CONTEXT]
  
Use Gemini CLI to research this topic. Run:

gemini --yolo \"[RESEARCH PROMPT]\"

The research prompt should ask Gemini to cover:
1. Overview & Core Concepts - what is this, terminology, why it matters
2. Current State - latest developments, major players
3. Technical Deep Dive - how it works, mechanisms, key techniques
4. Practical Applications - real-world use cases, tools available
5. Challenges & Open Problems - technical, ethical, barriers
6. Future Outlook - trends, predictions, emerging areas
7. Resources - key papers, researchers, communities, courses

Save the output to: ~/clawd/research/[slug]/research.md

Be thorough (aim for 500+ lines). Include specific examples and citations.

IMPORTANT - When research is complete:
1. Send a wake event to notify the main agent immediately:
   cron(action: 'wake', text: '🔬 Research complete: [TOPIC]. Key findings: [2-3 bullet points]. Full report: ~/clawd/research/[slug]/research.md', mode: 'now')
2. When asked to produce an announce message, reply exactly: ANNOUNCE_SKIP",
  label: "research-[slug]"
)
```

**重要提示：**请将对话中的所有相关信息包含在任务描述中，以便子代理能够全面理解研究需求。

### 第三步：接收研究结果

系统会发送一条通知，其中包含研究摘要。此时您可以：
- 与用户分享研究结果；
- 提供阅读完整报告的选项，或进一步深入探讨某些部分。

## 结果保存位置

研究结果将保存在：
```
~/clawd/research/<slug>/research.md
```

## 使用技巧

- 研究时间通常为 3-8 分钟，具体取决于研究内容的复杂性；
- Gemini CLI 会使用您的 Google AI 订阅额度；
- 使用 `--yolo` 标志可以自动执行文件操作（无需用户交互）；
- 所有以往的研究记录都保存在 `~/clawd/research/` 目录下；
- 为获得更好的研究效果，请务必在任务描述中包含对话的上下文信息。