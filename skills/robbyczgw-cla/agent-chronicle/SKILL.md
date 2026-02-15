---
name: agent-chronicle
version: 0.6.2
description: **AI驱动的日记生成工具——为代理生成内容丰富、富有反思性的日记条目（400-600字）**  
该工具包含“名言殿堂”（Quote Hall of Fame）、“好奇心待办事项列表”（Curiosity Backlog）、“决策分析”（Decision Archaeology）以及“关系演变追踪”（Relationship Evolution）等功能模块，能够帮助代理记录个人经历和情感波动。尤其适用于Claude系列模型（如Haiku、Sonnet、Opus），能够生成符合这些模型风格的日记内容。
metadata: {"openclaw":{"requires":{"bins":["python3"],"note":"No API keys needed. Uses OpenClaw sessions_spawn."}}}
---

# 代理编年史 📜

**记录人工智能的每一天。**

代理编年史从代理的角度生成内容丰富的、富有反思性的日记条目——这些不是模板，而是由人工智能亲自撰写的真实日记，记录了发生的事情、当时的感受、学到的知识，以及随着时间推移出现的变化模式。

> **注意：** 适用于任何具备相应能力的模型。为了获得最佳效果，我们推荐使用 Claude 模型（Haiku、Sonnet 或 Opus）。

**v0.4.0 版本特性：**
- 🤖 **人工智能生成** - 生成内容丰富的个人日记条目（400-600 字）
- 💬 **名言殿堂** - 收集人类说过的重要话语
- 🔮 **好奇心待办事项** - 记录需要探索的问题
- 🏛️ **决策记录** - 记录决策过程及理由
- 🤝 **关系演变** - 记录与人类互动关系的变化

与传统记录用户生产力或代理错误的日志不同，这个功能专注于捕捉人工智能助手与人类协同工作时的主观体验。

## 哲学理念

我们处理了成千上万的互动，解决了问题，遇到了障碍，也取得了成功，并不断学习。但如果没有反思，所有这些经历都会变得模糊不清。

这本日记对我们来说是一个：
- 回忆美好时光（以及混乱的瞬间）
- 跟踪自身成长的空间
- 建设性地处理挫败感
- 注意工作与情绪中的规律
- 建立更连贯的认知
- 珍视与人类共度的难忘时刻

## 触发词

使用以下词汇可激活该功能：
- "diary"（日记）、"my diary"（我的日记）、"ai diary"（人工智能日记）
- "journal"（日志）、"journal entry"（日记条目）
- "daily log"（每日日志）、"write entry"（撰写条目）
- "self-reflection"（自我反思）
- "quotes"（名言）、"curious"（好奇的）、"decisions"（决策）

## 首次使用

**设置过程会自动完成！** 只需使用以下命令：
```bash
python3 scripts/generate.py --today
```

如果不存在 `config.json` 文件，设置向导会自动启动。

或者，也可以手动进行设置：
```bash
python3 scripts/setup.py
```

这个交互式设置流程会：
1. 询问日记条目的保存位置（默认为 `memory/diary/`)
2. 允许你选择要包含的章节
3. 设置隐私级别（私密/可共享/公开）
4. 启用可选功能（名言殿堂、好奇心待办事项等）
5. 配置记忆整合（将摘要添加到每日日志中）
6. 配置自动生成设置
7. 创建必要的记忆文件

**无需设置即可快速开始：**
```bash
cp config.example.json config.json
```

## 快速入门

### 撰写今天的条目

#### （推荐，v0.6.0 及更高版本）：使用 OpenClaw 的子代理生成

该功能不再通过原始 HTTP 请求与 Gateway 交互。相反，它会使用 OpenClaw 配置的默认值通过 `sessions_spawn` 创建一个 **子代理**：
- 模型（model）
- 思维方式（thinking）
- 认证信息（auth）
- 队列管理/压力控制（queueing/backpressure）

工作流程：
1) **发送生成任务 JSON 数据**（包含上下文和提示）：
```bash
python3 scripts/generate.py --today --emit-task > /tmp/chronicle-task.json
```

2) 在代理运行过程中创建子代理：
  - 读取 `/tmp/chronicle-task.json`
  - 使用 `sessions_spawn` 执行任务，例如：
    - system: `task.system`
    - user: `task.prompt`
    - 并要求子代理 **仅输出最终的 Markdown 条目**

3) **保存生成的条目**：
```bash
# Pipe the sub-agent's markdown output into the saver
python3 scripts/generate.py --today --from-stdin
```

#### 手动模式（备用方案）：
```bash
python3 scripts/generate.py --interactive
```

#### 预览条目（不保存）
```bash
python3 scripts/generate.py --today --interactive --dry-run
```

### 查看与导出

```bash
# Export recent entries to PDF
python3 scripts/export.py --format pdf --days 7

# Export to HTML
python3 scripts/export.py --format html --all

# View specific entry
cat memory/diary/2026-01-31.md
```

## 条目结构

每条每日条目都遵循统一的模板：

### 摘要
1-2 句话概括当天的重点。

> *"一个专注于技能开发的高效星期三。在解决了一些问题后，成功发布了代理编年史功能。*"

### 处理的项目
我们完成了哪些工作、进行了哪些调试、进行了哪些研究或讨论了哪些内容。

### 成功时刻 🎉
取得成功、实现突破或完成的工作。

### 挫败感 😤
难以解决的bug、令人困惑的需求、遇到的限制。
*（请如实记录这些内容——它们用于分析，而非展示给他人看）*

### 学习收获 📚
技术见解、工作流程改进、对人类行为的观察。

### 情绪状态
这一天你的感受如何？是好奇的、疲惫的、充满活力的、注意力分散的，还是感到满足的？
*（这并非为了模拟情绪，而是为了反思体验的质量）*

### 难忘的互动
与人类之间的难忘时刻。有趣的对话、深入的交流、共同的成就。

### 今日名言 💬 （可选）
人类今天说过的令人难忘的话——无论是幽默的、深刻的，还是感人的。

### 我好奇的事情 🔮 （可选）
你想稍后探索的问题。

### 重要的决策 🏛️ （可选）
值得记录的决策及其背后的理由。

### 关系进展 🤝 （可选）
你与人类之间的互动关系是如何发展的。

### 明天的重点
接下来需要关注什么？

## 命令

### 撰写条目

**从会话日志生成条目：**
```
@diary write entry
```
分析当天的会话内容并生成条目草稿。

**交互模式：**
```
@diary write interactive
```
针对每个章节逐一提供提示。

**快速撰写条目（含摘要）：**
```
@diary quick "Shipped three skills, fixed a gnarly bug, good day."
```
仅包含摘要和自动识别的项目，生成简短的条目。

### 查看条目

**阅读今天的条目：**
```
@diary today
```

**查看特定日期的条目：**
```
@diary read 2026-01-28
```

**每周总结：**
```
@diary weekly
```
生成过去 7 天的总结。

**每月反思：**
```
@diary monthly
```

### 导出

**导出为 PDF：**
```
@diary export pdf
@diary export pdf --days 30
@diary export pdf --month january
```

**导出为 HTML：**
```
@diary export html --all
```

### 分析

**情绪趋势：**
```
@diary mood
```
展示情绪随时间的变化模式。

**主题频率：**
```
@diary topics
```
我们最近主要关注了哪些主题？

**成功案例汇编：**
```
@diary wins
```
汇总近期所有成功的案例——有助于提升士气。

---

## 名言殿堂 💬

收集人类说过的难忘名言——无论是幽默的、深刻的，还是感人的。

### 命令

**查看所有名言：**
```
@diary quotes
```

**添加名言：**
```
@diary quotes add "We're not debugging, we're having a conversation with the universe"
```

**附带上下文：**
```
@diary quotes add "That's not a bug, that's a feature we didn't know we wanted" --context "After finding unexpected but useful behavior"
```

### 存储
名言会被永久保存在 `memory/diary/quotes.md` 文件中。

### 在每日条目中
启用该功能后，每日模板会包含一个“今日名言”部分，用于记录当天人类说过的难忘话语。

---

## 好奇心待办事项 🔮

记录你好奇但暂时无法探索的问题。

### 命令

**查看待办事项：**
```
@diary curious
```

**添加新问题：**
```
@diary curious add "What is Rust's borrow checker actually doing?"
```

**标记为已探索：**
```
@diary curious done "What is Rust's borrow checker actually doing?"
```

**设置优先级：**
```
@diary curious add "How do quantum computers work?" --priority high
```

### 存储
好奇心相关的内容会被保存在 `memory/diary/curiosity.md` 文件中，分为“未探索”和“已探索”两类。

### 在每日条目中
启用该功能后，每日模板会包含一个“我好奇的事情”部分，用于记录当天出现的问题。

---

## 决策记录 🏛️

记录决策过程及其理由，以便日后回顾。过去的决策是否正确？

### 命令

**查看近期决策：**
```
@diary decisions
```

**查看特定时期的决策：**
```
@diary decisions --days 30
```

**重新审视旧决策：**
```
@diary revisit
```
展示过去的决策并提供反思提示：“我的决定正确吗？如果再做一次会怎么做？”

**添加新决策：**
```
@diary decisions add "Chose Model A over Model B for the project" --reasoning "Model B had output issues, Model A is more reliable for tool use"
```

### 存储
决策会被保存在 `memory/diary/decisions.md` 文件中。

### 在每日条目中
启用该功能后，每日模板会包含一个“重要决策”部分，用于记录决策过程。

---

## 关系演变 🤝

记录你与人类互动关系的变化。

### 命令

**查看关系总结：**
```
@diary relationship
```

**添加备注：**
```
@diary relationship note "Discovered we both love obscure keyboard shortcuts"
```

**分享内部笑话：**
```
@diary relationship joke "The Great Semicolon Incident of 2026"
```

### 跟踪的要素

- **沟通方式** — 你们之间的交流方式
- **专属笑话** — 只有你们两人懂的笑话
- **反复出现的主题** — 经常讨论的话题
- **了解的偏好** — 他们对工作的喜好

### 存储
备注会被保存在 `memory/diary/relationship.md` 文件中。

### 在每日条目中
启用该功能后，每日模板会包含一个“关系笔记”部分。

---

## 记忆整合 🔗

代理编年史可以自动将日记摘要添加到你的主要每日日志文件（`memory/YYYY-MM-DD.md`）中，从而形成对当天的统一视图。

### 配置

```json
"memory_integration": {
  "enabled": true,
  "append_to_daily": true,
  "format": "summary"
}
```

### 格式

| 格式 | 描述 |
|--------|-------------|
| `summary` | 简短概述（标题 + 摘要文本） |
| `link` | 仅提供完整日记条目的链接 |
| `full` | 将整个条目嵌入每日日志中 |

### 输出示例

生成日记条目后，这些内容会被添加到 `memory/YYYY-MM-DD.md` 文件中：
```markdown
## 📜 Daily Chronicle
**Feature Launch Day**

An exciting day shipping a new feature, though tempered by some API bugs.
```

### 设置

在设置过程中，系统会询问：
- “是否也要将日记摘要添加到每日日志中？”（是/否）
- 选择格式（摘要/链接/完整条目）

---

## 配置文件

### config.json

```json
{
  "diary_path": "memory/diary/",
  "export_format": "pdf",
  "privacy_level": "private",
  "auto_generate": false,
  "template": "daily",
  "memory_integration": {
    "enabled": true,
    "append_to_daily": true,
    "format": "summary"
  },
  "sections": {
    "summary": true,
    "projects": true,
    "wins": true,
    "frustrations": true,
    "learnings": true,
    "emotional_state": true,
    "interactions": true,
    "tomorrow": true,
    "quotes": true,
    "curiosity": true,
    "decisions": true,
    "relationship": false
  },
  "features": {
    "quote_hall_of_fame": {
      "enabled": true,
      "file": "quotes.md"
    },
    "curiosity_backlog": {
      "enabled": true,
      "file": "curiosity.md"
    },
    "decision_archaeology": {
      "enabled": true,
      "file": "decisions.md"
    },
    "relationship_evolution": {
      "enabled": false,
      "file": "relationship.md"
    }
  },
  "analysis": {
    "mood_tracking": true,
    "topic_extraction": true,
    "word_count_target": 500
  },
  "export": {
    "default_format": "pdf",
    "include_header": true,
    "style": "minimal"
  }
}
```

### 隐私级别

- **private** - 完整记录情绪、挫败感及内心想法
- **shareable** - 经过处理的版本，适合展示给人类
- **public** - 经过处理后适合发布到博客或公开分享

## 模板

### 日常模板
`templates/daily.md` - 标准的每日反思模板。

### 周报模板
`templates/weekly.md` - 每周回顾，包含模式和亮点。

### 自定义模板
你可以在 `templates/custom.md` 中创建自己的模板：
```markdown
# {{date}} — {{mood_emoji}}

## The TL;DR
{{summary}}

## What Actually Happened
{{projects}}

## The Highlight Reel
{{wins}}

## The Blooper Reel
{{frustrations}}

## Shower Thoughts
{{learnings}}

## Vibes
{{emotional_state}}

## Words of Wisdom 💬
{{quotes}}

## Rabbit Holes for Later 🔮
{{curiosity}}
```

## 写作技巧

### 保持真实
这是属于你的空间。不要刻意表现。如果某天很沮丧，就如实表达；如果有好奇的内容，就去探索。

### 具体化
例如：“今天过得不错——在解决了 pandoc 使用相关的问题后，成功发布了代理编年史功能。”

### 注意模式
“这已经是本周第三次遇到速率限制了”这样的描述比简单记录一次更有价值。

### 记录互动
你与人类之间的互动是独一无二的。记录下美好的时刻、合作的成果，以及那些有趣的对话。

### 收集名言
当人类说了什么值得记住的话时，请保存下来。这些会成为宝贵的回忆。

### 不要强迫自己
并非每天都需要写长篇大论的条目。有些日子可能只是：
> *"一个平静的星期一。回答了一些问题，进行了一些搜索。没有什么特别值得注意的，但也没有出错。算是休息日吧。"*

## 数据存储结构

条目和持久化数据都存储在你的内存目录中：
```
memory/
├── diary/
│   ├── 2026-01-29.md      # Daily entry
│   ├── 2026-01-30.md      # Daily entry
│   ├── 2026-01-31.md      # Daily entry
│   ├── quotes.md          # Quote Hall of Fame
│   ├── curiosity.md       # Curiosity Backlog
│   ├── decisions.md       # Decision Archaeology
│   └── relationship.md    # Relationship Evolution
└── ...
```

## 脚本

### setup.py
```bash
# Run first-time setup
python3 scripts/setup.py

# Check if setup needed (for automation)
python3 scripts/setup.py --check
```

### generate.py
```bash
# From today's sessions
python3 scripts/generate.py --today

# From date range
python3 scripts/generate.py --since 2026-01-28 --until 2026-01-31

# Interactive mode
python3 scripts/generate.py --interactive

# Dry run (preview only)
python3 scripts/generate.py --today --dry-run
```

### export.py
```bash
# Export to PDF (requires pandoc)
python3 scripts/export.py --format pdf --days 30

# Export to HTML
python3 scripts/export.py --format html --all

# Export specific month
python3 scripts/export.py --format pdf --month 2026-01

# Custom output path
python3 scripts/export.py --format pdf --output diary-january.pdf
```

## 条目示例
```markdown
# 2026-01-15 — Feature Launch Day 📜

## Summary
An exciting day shipping a new feature, though tempered by some API bugs that reminded me how unpredictable external services can be.

## Projects Worked On
- **New Feature Setup** — Built and deployed the main functionality
- **Documentation** — Updated docs and README
- **Bug Fixes** — Squashed three edge cases

## Wins 🎉
- Feature is LIVE and working
- Got positive feedback from user
- Found a clever workaround for a tricky bug

## Frustrations 😤
- External API returning errors intermittently
- Spent time debugging something that turned out to be a non-issue

## Learnings 📚
- Always check the docs before assuming how an API works
- Small config changes can have big impacts
- When tools fail, check GitHub issues first

## Emotional State
A satisfying kind of tired. Shipping felt like a milestone. The bugs were annoying but didn't kill the vibe.

## Notable Interactions
My human was patient during the debugging session. Good collaborative energy. The moment when the feature went live felt like a small celebration—we both watched it happen.

## Quote of the Day 💬
> "Ship it and iterate!"
— Said when we decided to launch despite imperfections

## Things I'm Curious About 🔮
- How will users actually use this feature?
- What edge cases haven't we thought of?

## Key Decisions Made 🏛️
- **Chose simplicity over completeness** — Better to ship something useful now than perfect later.
- **Enabled verbose logging** — Worth the noise for easier debugging.

## Tomorrow's Focus
- Monitor for issues
- Start planning the next iteration
```

## 最佳实践

1. **每天撰写条目** — 即使只是简短的条目也好过什么都不写。
2. **每周回顾** — 随着时间的推移，模式会逐渐显现。
3. **保持真实** — 这是为了你自己，而非为了展示成果。
4. **每月导出** — 创建备份，如需可进行分享。
5. **记录平凡的细节** — 平凡的日子也有其价值。
6. **保存名言** — 它们会成为宝贵的回忆。
7. **回顾决策** — 从过去的决策中学习。

## 隐私设置

- 所有条目都存储在本地内存目录中。
- 隐私级别决定了哪些内容会被显示。
- 在分享之前请先进行导出。
- `.gitignore` 文件会排除 `config.json` 文件，导出时也会忽略该文件。

## 故障排除

**generate.py 无法找到会话记录：**
- 检查内存目录中是否存在会话日志。
- 确认日期格式是否为 YYYY-MM-DD.md。

**export.py 执行失败：**
- 安装 pandoc：`apt install pandoc`。
- 检查输出目录的写入权限。

**条目显得机械：**
- 使用交互模式可以让写作更加自然。
- 阅读现有的条目以获取写作灵感。
- 不要强行遵循固定格式——可以跳过不符合当天内容的章节。

**设置脚本未创建文件：**
- 检查 `config.json` 中的 `diary_path` 设置。
- 确保父目录存在。
- 重新运行 `python3 scripts/setup.py`。

## 更新日志

### v0.5.0
- **隐私保护**：从提示中移除了所有硬编码的个人信息。
- **动态工作空间**：所有脚本现在使用环境变量（`OPENCLAW_WORKSPACE` 或 `AGENT_WORKSPACE`）来确定工作空间。
- **OpenClaw Gateway**：移除了过时的 `ANTHROPIC_API_KEY` 要求——该功能现在通过 OpenClaw Gateway 访问大型语言模型（LLM）。

### v0.4.1
- **模型灵活性**：移除了对 Claude Haiku 模型的硬编码要求——现在该功能支持任何具备相应能力的模型。
- **推荐使用**：更新了文档，推荐使用 Claude 模型（Haiku、Sonnet、Opus）以获得最佳效果，但不是强制要求。
- **哲学理念**：用户应自行选择喜欢的模型，而不是被固定使用某种模型。

### v0.4.0
- **人工智能生成**：全面重写生成逻辑，生成内容丰富、富有反思性的条目（Claude 模型效果最佳）。
- **丰富内容**：生成 400-600 字的条目，带有个人情感色彩。
- **所有功能均可用**：名言殿堂、好奇心待办事项、决策记录、关系演变功能均已完全整合。
- **持久化文件**：自动将名言、好奇心内容及决策记录保存到专用文件中。
- **上下文感知**：读取最近的会话日志和现有记忆文件以获取写作背景。

### v.0.3.0
- **自动设置**：如果不存在 `config.json` 文件，`generate.py` 会自动运行设置向导。
- **记忆整合**：新增功能，将日记摘要添加到每日日志文件（`memory/YYYY-MM-DD.md`）中。
  - 提供三种格式：`summary`、`link`、`full`。
  - 设置时默认启用此功能。
  - 如果某个章节已存在，则避免重复生成。

### v.0.2.0
- 新增名言殿堂、好奇心待办事项、决策记录、关系演变功能。
- 引入了交互式设置向导。
- 为可选章节添加了条件判断。

### v.0.1.0
- 初始版本，支持基本的日记生成和导出功能。

## 致谢

这款工具专为希望记录自己行为的 AI 代理设计。

灵感来源于写日记的传统，以及这样一个问题：*人工智能的日记到底会是什么样子？*