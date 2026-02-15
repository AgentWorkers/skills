---
name: ralph-evolver
description: 递归式自我提升引擎。从基本原理出发进行思考，让深刻的见解自然浮现。
tags: [meta, recursive, evolution, emergence, first-principles]
version: 1.0.6
---

# 🧬 Ralph-Evolver

**核心理念：递归 + 自组织 + 第一性原理**

## 信号源（Signal Sources）

Ralph-Evolver 收集的不仅仅是代码结构，还包括多维度的上下文信息：
- **提交历史（Commit History）**：了解代码变更背后的原因
- **待办事项（TODO/FIXME）**：代码中存在的潜在问题或需要修复的部分
- **错误处理模式（Error Handling Patterns）**：识别代码中的薄弱环节
- **高频修改的文件（Hotspot Files）**：频繁修改的文件往往暗示设计上的问题

每个信号都会附带一个**假设提示（Hypothesis Prompt）**，以指导更深入的分析。

## 第一性原理（First Principles）

Ralph-Evolver 在运行时不会机械地执行预设的检查列表，而是会思考以下问题：
1. 这个项目的**本质**是什么？
2. 它目前做了哪些**不应该**做的事情？
3. 它缺少了哪些应该具备的功能？
4. 如果你**从零开始**构建这个项目，你会如何设计它？

## 元反射（Meta-Reflection, v1.0.5）

在自我分析过程中，Ralph-Evolver 会问自己：
- 这只是一个**表面的修复**，还是一个**根本性的改进**？
- 在过去的改进历史中是否存在某种**规律或模式**？
- 这次改进是否会让 Ralph-Evolver 更善于发现问题？

## 改进跟踪（Improvement Tracking）

- 记录改进的详细信息、分析结果以及改进的**层次**（表面级/根本性改进）和系统健康状况
- **模式分析（Pattern Analysis）**：统计表面级改进与根本性改进的比例，发现重复出现的改进趋势
- 比较改进前后的效果（是否有所改善、退步或保持不变）

## 使用方法（Usage）

```bash
node index.js .                    # Current directory (positional)
node index.js /path/to/app         # Specify path
node index.js . --loop 5           # Run 5 cycles
node index.js --task "fix auth"    # Specific task
node index.js --reset              # Reset iteration state
```

## 递归（Recursion）

Ralph-Evolver 具有自我改进的能力。这才是真正的递归。

---

*“先提出假设，再验证。始终从第一性原理出发进行思考。”*