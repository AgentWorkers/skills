---
name: fork-and-skill-scanner-ultimate
version: 1.1.1
description: "每次运行时，会扫描 1,000 个 GitHub 的分支（forks）。只关注那些真正有价值的资源（即“金子”，即高质量的项目），忽略那些只是简单克隆过来的项目——整个过程完全自动化。"
metadata:
  openclaw:
    owner: kn7623hrcwt6rg73a67xw3wyx580asdw
    category: developer-tools
    tags:
      - github
      - forks
      - skill-discovery
      - automation
      - community-insights
    license: MIT
    notes:
      security: "Uses GitHub's public API (read-only) to list and compare forks. No write access, no authentication required for public repos. Sub-agents are spawned locally via OpenClaw's sessions_spawn. Reports delivered through existing configured channels (WhatsApp, etc). No credentials stored or requested."
---
# 终极分支与技能扫描器（Ultimate Fork and Skill Scanner）

**每天分析多达1,000个分支，仅将优质内容发送到您的邮箱。**

大多数分支只是毫无价值的克隆版本，它们只是被遗忘在角落里。但在这些分支中，可能有人重新编写了您的认证机制，提升了系统吞吐量，或者添加了您从未想到的新功能。这款工具能够自动识别这些有价值的“针尖”。

## 工作原理

我们采用了三阶段处理流程，以降低成本并提高筛选效率：

1. **Bash预过滤**：迅速过滤掉不活跃或完全相同的分支，避免浪费任何代币在无用的副本上。
2. **子代理深度分析**：剩余的分支会由多个代理并行进行详细检查，包括代码差异、新出现的模式以及性能变化。
3. **可操作的报告**：只有真正值得关注的分支才会被筛选出来，并通过WhatsApp发送给您。报告内容简洁明了，没有任何无关信息。

## 技能扫描器（Skill Scanner）

该工具每天会审查ClawHub平台上的10项技能，筛选出最优秀的内容，追踪行业趋势，并关注那些技术娴熟的开发者，以便发现他们的更多作品。

## 您将获得：

- 每次运行可分析多达1,000个分支
- 每日技能评估与趋势分析
- 仅在发现重要内容时才会发送报告
- 低代币消耗的设计——在代理开始处理之前，Bash脚本已经完成了大部分工作

*克隆它、修改它，然后让它成为您的专属工具吧。*

👉 访问完整项目：[github.com/globalcaos/clawdbot-moltbot-openclaw](https://github.com/globalcaos/clawdbot-moltbot-openclaw)