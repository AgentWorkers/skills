---
name: arxiv-skill-learning
description: **协调从 arXiv 论文中持续学习新技能的过程。** 该系统能够触发一个学习循环：首先获取论文内容，然后提取其中的代码和技能信息，并将这些内容内化为用户的实际能力。
---
# ArXiv 技能学习

## 使用方法

```javascript
const learner = require('./index');
const result = await learner.main();
```

## 工作流程

1. **巡逻**：在 arXiv 上搜索相关的最新论文（由代理、大语言模型或工具完成）。
2. **提取**：使用 `arxiv-skill-extractor` 工具生成技能代码。
3. **测试**：运行生成的测试代码。
4. **固化**：将新生成的技能代码提交到工作区。

## 配置参数

- 目标类别：cs.AI（计算机科学·人工智能）、cs.CL（计算机科学·机器学习）、cs.LG（计算机科学·逻辑学）、cs.SE（计算机科学·软件工程）
- 定时任务频率：每小时一次