---
name: para-second-brain
version: 2.0.1
description: 使用 PARA（项目、领域、资源、存档）来组织你的代理的知识结构——然后确保所有这些内容都是可搜索的。通过创建符号链接（symlink），你可以实现对你整个知识库的全方位语义搜索，而不仅仅局限于 MEMORY.md 文件。该系统还支持会话记录的索引功能以及内存刷新协议。你的代理终于拥有了一个真正的“第二大脑”（即一个强大的辅助决策工具）。
---

# PARA 第二大脑（Second Brain）

您的智能助手的记忆功能刚刚得到了大幅升级。现在它可以对您的整个知识库进行全面的语义搜索——而不仅仅是 `MEMORY.md` 文件。

## v2.0 的新功能

**v2.0 之前的情况：** `memory_search` 只能搜索 `MEMORY.md` 和每日日志中的内容。您的 `notes/` 文件夹完全无法被搜索到，您必须手动知道在哪里查找信息。

**v2.0 之后的情况：** 通过一个简单的符号链接命令，您的整个 PARA 知识库就可以被搜索了。您可以询问关于笔记中的任何内容，系统都会找到答案。此外，系统还加入了会话记录功能以及内存刷新机制，以防止信息丢失。

| v2.0 之前 | v2.0 之后 |
|--------|-------|
| 只能搜索 MEMORY.md 和每日日志 | 可以搜索所有内容 |
| “我没有这个信息” | 系统会立即找到相关信息 |
| 会话内容被压缩可能导致信息丢失 | 内存刷新机制可以保存关键信息 |
| 会话记录被遗忘 | 会话记录会被索引 |

## 这个功能的作用

该功能创建了一个“第二大脑”结构，将以下内容区分开来：
- **原始记录**（每日日志）与 **精选知识**（`MEMORY.md`）
- **正在进行的工作**（项目）与 **持续的责任**（领域）
- **参考资料**（资源）与 **已完成的工作**（归档）

## 与其他“第二大脑”功能的区别

还有另一个流行的 [第二大脑功能](https://clawdhub.com/christinetyip/second-brain)，它是由 Ensue 提供的。这两个功能都很棒，但它们解决的是不同的问题：

| | **PARA 第二大脑** | **Ensue 第二大脑** |
|---|---|---|
| **存储方式** | 本地文件（在工作区） | 云 API（Ensue 提供） |
| **成本** | 免费，自托管 | 需要 Ensue API 密钥 |
| **适用场景** | 工作上下文管理、助手行为连续性、项目跟踪 | 永恒的知识库、语义查询 |
| **搜索方式** | Clawdbot 的 `memory_search` | Ensue 的向量搜索 |
| **结构** | PARA（项目/领域/资源/归档） | 命名空间（概念/工具箱/模式） |
| **使用场景** | “我们昨天决定了什么？” | “递归是如何工作的？” |

**如果需要以下功能，请使用 PARA 第二大脑：**  
- 需要一个基于文件的记忆系统，可以离线使用，无需成本，并能跟踪正在进行的工作上下文。  

**如果需要以下功能，请使用 Ensue 第二大脑：**  
- 需要一个基于云的知识库，能够高效地回答“我对 X 了解多少”这类语义查询。  

**如果同时需要这两种功能：**  
- 可以结合使用 PARA 第二大脑来管理工作上下文，同时使用 Ensue 第二大脑来构建永久性的知识库。它们可以互相补充。**

## 快速设置

### 1. 创建目录结构

```
workspace/
├── MEMORY.md              # Curated long-term memory
├── memory/
│   └── YYYY-MM-DD.md      # Daily raw logs
└── notes/
    ├── projects/          # Active work with end dates
    ├── areas/             # Ongoing life responsibilities  
    ├── resources/         # Reference material
    │   └── templates/     # Content templates
    └── archive/           # Completed/inactive items
```

运行以下命令来搭建基础结构：  
```bash
mkdir -p memory notes/projects notes/areas notes/resources/templates notes/archive
```

### 2. 使笔记可搜索（使用符号链接）

默认情况下，`memory_search` 只会索引 `MEMORY.md` 和 `memory/*.md` 文件。您的整个 `notes/` 文件夹无法被搜索到！

**通过一个命令解决这个问题：**  
```bash
ln -s /path/to/your/workspace/notes /path/to/your/workspace/memory/notes
```

示例：  
```bash
ln -s /Users/yourname/clawd/notes /Users/yourname/clawd/memory/notes
```

**这个命令的作用：** 创建一个符号链接，使 `memory/notes/` 指向您实际的 `notes/` 文件夹。这样 Clawdbot 的 `memory_search` 就可以搜索到所有的 PARA 笔记了。

**验证是否生效：**  
```bash
ls -la memory/notes  # Should show: memory/notes -> /path/to/notes
```

**测试搜索效果：**  
向智能助手询问一些在笔记中存在但在 `MEMORY.md` 中不存在的内容。如果系统找到了答案，说明符号链接设置成功。

**为什么这很重要：**  
| v2.0 之前 | v2.0 之后 |
|--------|-------|
| 只能搜索 MEMORY.md 和每日日志 | 可以搜索所有内容 |
| 必须手动查找信息 | 可以对所有内容进行语义搜索 |
| “我没有这个信息” | 系统会找到相关信息 |

### 3. 启用会话记录索引

现在，您过去的对话记录也可以被搜索了。在 Clawdbot 的配置文件中添加以下内容：  
```json
"memorySearch": {
  "sources": ["memory", "sessions"],
  "query": {
    "minScore": 0.3,
    "maxResults": 20
  }
}
```

**这个命令的作用：** 将会话记录与笔记一起索引。这样当您询问“上周我们讨论了什么？”时，系统就能找到相关内容。

### 4. 初始化 `MEMORY.md`

在工作区根目录下创建 `MEMORY.md` 文件——这是您的精选长期记忆存储空间：  
```markdown
# MEMORY.md — Long-Term Memory

## About [Human's Name]
- Role/occupation
- Key goals and motivations
- Communication preferences
- Important relationships

## Active Context
- Current focus areas
- Ongoing projects (summaries, not details)
- Deadlines or time-sensitive items

## Preferences & Patterns
- Tools and workflows they prefer
- Decision-making style
- Pet peeves and likes

## Lessons Learned
- What worked
- What didn't
- Principles discovered

## Key Dates
- Birthdays, anniversaries
- Recurring events
- Important milestones
```

### 5. 将这些设置添加到 AGENTS.md 中

将以下指令添加到您的 `AGENTS.md` 文件中：  
```markdown
## Memory

You wake up fresh each session. These files are your continuity:
- **Daily notes:** `memory/YYYY-MM-DD.md` — raw logs of what happened
- **Long-term:** `MEMORY.md` — curated memories (like human long-term memory)
- **Topic notes:** `notes/` — organized by PARA structure (all searchable via memory_search)

### Writing Rules
- If it has future value, write it down NOW
- Don't rely on "mental notes" — they don't survive restarts
- Text > Brain 📝

### PARA Structure
- **Projects** (`notes/projects/`) — Active work with end dates
- **Areas** (`notes/areas/`) — Ongoing responsibilities (health, finances, relationships)
- **Resources** (`notes/resources/`) — Reference material, how-tos, research
- **Archive** (`notes/archive/`) — Completed or inactive items

### Memory Flush Protocol
Monitor your context usage with `session_status`. Before compaction wipes your memory, flush important context to files:

| Context % | Action |
|-----------|--------|
| < 50% | Normal operation |
| 50-70% | Write key points after substantial exchanges |
| 70-85% | Active flushing — write everything important NOW |
| > 85% | Emergency flush — full summary before next response |
| After compaction | Note what context may have been lost |

**The rule:** Act on thresholds, not vibes. If it's important, write it down NOW.
```

## 内存刷新机制（非常重要！）

智能助手的上下文存储空间是有限的。当存储空间满时，旧的信息会被压缩或丢失。**请不要丢失重要信息。**

### 如何监控内存使用情况

定期运行 `session_status` 命令来检查内存使用情况：  
```
📚 Context: 36k/200k (18%) · 🧹 Compactions: 0
```

### 根据内存使用情况采取相应措施

| 内存使用百分比 | 应采取的行动 |
|-----------|------------|
| **< 50%** | 正常运行，随时记录决策内容。 |
| **50-70%** | 提高警惕，每次重要交流后记录关键点。 |
| **70-85%** | 开始主动刷新内存，立即将重要内容写入每日笔记。 |
| **> 85%** | 紧急刷新，响应前先写出完整的上下文总结。 |
| **压缩后** | 立即记录可能丢失的信息，并检查上下文的连续性。 |

### 需要刷新的内容：
1. **已做出的决策**——决策内容及原因
2. **待办事项**——谁负责什么任务
3. **未完成的任务**——将未完成的任务记录到 `notes/areas/open-loops.md` 文件中
4. **讨论中的变更**——如果讨论了文件变更，立即记录下来

### 内存刷新检查清单
在长时间会话结束或内存使用率达到较高水平之前，请检查以下内容：
- [ ] 关键决策是否已记录？
- [ ] 待办事项是否已捕获？
- [ ] 新学到的内容是否已写入相应的文件？
- [ ] 未完成的任务是否已记录下来以便后续处理？

## 知识质量

**核心问题：** “未来的我是否会感谢我现在所做的这些记录？”

### 什么应该保存：
- 您真正理解的概念（而不是半懂不懂的想法）
- 您实际使用过的工具（而不仅仅是听说过）
- 有效的模式（并附有具体示例）
- 从错误中吸取的教训

### 什么不应该保存：
- 仅部分理解的概念（先学习，再保存）
- 尚未尝试过的工具（书签不等于知识）
- 没有解释原因的简单记录
- 重复的笔记

### 保存前的质量检查标准：
在保存任何精选笔记之前，请确保：
1. 这些内容是为未来的自己准备的（以便将来忘记时可以参考）
2. 包含原因而不仅仅是结果
3. 有具体的示例或关键见解
4. 结构清晰，便于查找

## 内容模板

使用以下模板来创建结构化、高质量的知识条目：  
### 概念模板  
```markdown
# [CONCEPT NAME]

## What It Is
[One-line definition]

## Why It Matters
[What problem it solves, when you'd need it]

## How It Works
[Explanation with examples]

## Key Insight
[The "aha" moment — what makes this click]
```

### 工具模板  
```markdown
# [TOOL NAME]

**Category:** [devtools | productivity | etc.]

## What It Does
[Brief description]

## Why I Use It
[What problem it solved for YOU]

## When to Reach For It
[Scenarios where this is the right choice]

## Gotchas
- [Things that tripped you up]
```

### 模式模板  
```markdown
# [PATTERN NAME]

## Problem
[What situation triggers this pattern]

## Solution
[The approach]

## Trade-offs
**Pros:** [Why this works]
**Cons:** [When NOT to use it]
```

## PARA 的工作原理

PARA 是由 [Tiago Forte](https://fortelabs.com/) 创建的知识组织系统，他是《构建第二大脑》（*Building a Second Brain*）一书的作者。PARA 将所有内容分为四个类别，以便于管理和使用：

### 项目（Projects）
**定义：** 有截止日期或最终目标的工作  
**示例：** “启动网站”、“计划去日本旅行”、“完成客户提案”  
**文件保存方式：** `notes/projects/website-launch.md`

### 领域（Areas）
**定义：** 没有固定结束时间的持续责任  
**示例：** 健康、财务、人际关系、职业发展  
**文件保存方式：** `notes/areas/health.md`, `notes/areas/dating.md`

### 资源（Resources）
**定义：** 供将来使用的参考资料  
**示例：** 研究资料、教程、模板、有趣的文章  
**文件保存方式：** `notes/resources/tax-guide.md`, `notes/resources/api-docs.md`

### 归档（Archive）
**定义：** 来自其他类别的不再使用的内容  
**处理方式：** 完成后移至 `notes/archive/` 文件夹  

### 日志格式

为每一天创建 `memory/YYYY-MM-DD.md` 文件：  
```markdown
# YYYY-MM-DD

## Key Events
- [What happened, decisions made]

## Learnings
- [What worked, what didn't]

## Open Threads
- [Carry-forward items]
```

## 知识管理的工作流程

### 每日（5 分钟）：
- 将重要事件记录到 `memory/YYYY-MM-DD.md` 文件中  
- 将特定主题的笔记保存到相应的 `notes/` 文件夹中

### 每周（15 分钟）：
- 回顾本周的每日日志  
- 提取模式和经验教训并保存到 `MEMORY.md` 中  
- 将已完成的项目移至归档文件夹

### 每月（30 分钟）：
- 检查 `MEMORY.md` 中过时的信息  
- 合并或归档旧的项目笔记  
- 确保各个领域的信息反映当前的优先级

### 决策树：这些内容应该保存在哪里？  

```
Is it about today specifically?
  → memory/YYYY-MM-DD.md

Is it a task with an end date?
  → notes/projects/

Is it an ongoing responsibility?
  → notes/areas/

Is it reference material for later?
  → notes/resources/

Is it done or no longer relevant?
  → notes/archive/

Is it a distilled lesson or preference?
  → MEMORY.md
```

## 为什么需要两层记忆系统？

| 日志 | MEMORY.md |
|------------|-----------|
| 原始记录，按时间顺序保存 | 精选内容，结构化存储 |
| 涵盖所有内容 | 仅保存重要信息 |
| 按时间顺序记录 | 按主题分类 |
| 日志量较大 | 内容经过压缩 |
| 记录“发生了什么” | 记录“我学到了什么” |

日志是您的日常记录，而 `MEMORY.md` 则是您的智慧结晶。

## 设计原则：

1. **质量优先于数量** — 精选的笔记比随意积累的笔记更有价值  
2. **快速记录，谨慎筛选** — 日志记录较为随意；精选笔记质量更高  
3. **文字胜过记忆** — 如果内容重要，就写下来  
4. **未来自我测试** — “未来的我是否会感谢我现在所做的这些记录？”  
5. **每个内容只有一个存储位置** — 避免重复，使用链接代替重复记录  
6. **包含原因** — 仅提供事实而没有解释是毫无意义的  
7. **在信息丢失前及时保存** — 定期检查内存使用情况，并在数据被压缩前及时记录  

---

**PARA 第二大脑与以下工具搭配使用效果更佳：**  
- [memory-setup](https://clawdhub.com/jrbobbyhansen-pixel/memory-setup)（用于技术配置）  
- [proactive-agent](https://clawdhub.com/halthelobster/proactive-agent)（用于优化智能助手的行为模式）