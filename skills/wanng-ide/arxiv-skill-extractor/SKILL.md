---
name: arxiv-skill-extractor
description: 该技能可自动化从 arXiv 论文中提取可重用的代码片段，并将这些代码片段转化为实际的 OpenClaw 技能（即可在 OpenClaw 环境中使用的功能或模块）。通过这种方式，论文中的研究成果能够被直接转化为可操作的软件组件，从而加速技术创新和应用。
---
# ArXiv 技能提取器

该技能整合了 `arxiv-paper-reviews`，并提供了一个自动化流程，用于：
1. 下载论文。
2. 提取关键算法。
3. 生成技能模板。

## 使用方法

### 从论文中提取技能信息

```javascript
const { extractSkill } = require("./skills/arxiv-skill-extractor/index.js");

async function run() {
  const result = await extractSkill("4711d67c242a5ecba2751e6b");
  console.log(result);
}

run();
```

### 自动化流程

运行默认的提取循环（使用 `local_task:arxiv_skill_learning` 配置）：

```bash
# 自动读取 pending_skill_task.json 中的 paper_key
node skills/arxiv-skill-extractor/index.js

# 或直接指定 paper_key
node skills/arxiv-skill-extractor/index.js 4711d67c242a5ecba2751e6b
```

## 为什么需要这个工具？

我们需要持续从新的研究中学习。手动阅读论文的速度较慢。这个工具能够弥合论文知识与可执行代码之间的差距。