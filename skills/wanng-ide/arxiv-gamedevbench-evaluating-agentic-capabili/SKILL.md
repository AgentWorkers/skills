---
name: arxiv-gamedevbench-evaluating-agentic-capabili
description: "从 arXiv 论文 GameDevBench 中学习了如何通过游戏开发来评估代理（agent）的能力。利用这一技能，可以基于论文中的方法来构建 Node.js 实验框架。"
metadata: '{"openclaw":{"requires":{"bins":["node"]}}}'
---
# arxiv-gamedevbench-evaluating-agentic-capabili

## 来源
- 论文编号：44f3ad505bee7a5c25a60d2a3686cb7e
- 标题：GameDevBench：通过游戏开发评估代理的智能能力
- 分类：cs.AI, cs.CL, cs.SE

## 研究发现
尽管在开发编码型代理方面取得了快速进展，但在开发多模态代理方面的进展仍然滞后。一个主要挑战是缺乏能够同时满足软件开发复杂性和深度多模态理解需求的评估平台。游戏开发正好提供了这样的平台：代理需要在庞大的代码库中导航，并操作诸如着色器、精灵图和动画等多模态资产，这些资产都存在于视觉游戏场景中。我们提出了GameDevBench，这是首个用于评估代理智能能力的工具。

## Node.js 实现代码
`node {baseDir}/scripts/run.js`