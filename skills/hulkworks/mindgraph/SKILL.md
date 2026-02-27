---
name: mindgraph
description: Obsidian-style [[wikilink]] knowledge graph and learnable MindSkills for OpenClaw workspaces. Use for ALL of these: (1) Any workspace file read/write — always use [[wikilinks]] for people, projects, tools, concepts. (2) Running learned processes like knockout-test, seo-validator, competitor-analysis. (3) Querying knowledge — "what do I know about X", "show connections to Y". (4) Learning new repeatable processes — "learn a new mindskill called Z". (5) Memory maintenance — finding orphans, dead links, unconnected files. This skill is always active — treat [[wikilinks]] as standard practice in every markdown file you write.
---

# MindGraph 🕸️🧠

这是一个专为 OpenClaw 设计的知识图谱与可学习流程引擎。它具备两大核心功能：

1. **知识图谱**：支持在所有工作区文件中使用类似 Obsidian 的 `[[wikilinks]]` 标记来创建超链接。
2. **MindSkills**：用户可以学习并复用这些流程，这些流程会将执行结果以图谱的形式保存下来。

## 常规规则

**每次编写或编辑 markdown 文件时，请使用 `[[wikilinks]]` 来引用以下内容：**
- 人员：`[[Alice]]`, `[[Bob]]`
- 项目：`[[my-saas]]`, `[[landing-page]]`
- 公司/工具：`[[Stripe]]`, `[[Vercel]]`, `[[GitHub]]`
- 概念/框架：`[[Knockout Test]]`, `[[B2B SaaS]]`
- 其他代理/模型：`[[Claude Code]]`, `[[Sonnet]]`

使用 `[[wikilinks]]` 是强制性的。链接是知识之间连接的关键。如果没有链接，这些笔记就只是孤立的信息，毫无用处。

**请** **绝对不要在发送给用户的消息（如 Telegram、Discord 等）中使用 `[[wikilinks]]**。`[[wikilinks]]** 仅适用于工作区文件。在对话中，请直接使用名称，例如 “Alice”，而不是 “[[Alice]]”。

**在对文件进行重大修改后，请重新构建索引：**
```bash
python3 skills/mindgraph/scripts/mindgraph.py index
```

## 图谱相关命令

```bash
# Build/rebuild index
python3 skills/mindgraph/scripts/mindgraph.py index

# Query a topic (backlinks + context + connections)
python3 skills/mindgraph/scripts/mindgraph.py query "<name>"

# Backlinks only (what references this?)
python3 skills/mindgraph/scripts/mindgraph.py backlinks "<name>"

# Forward links (what does this link to?)
python3 skills/mindgraph/scripts/mindgraph.py links "<file>"

# Bidirectional connections
python3 skills/mindgraph/scripts/mindgraph.py connections "<name>"

# ASCII tree visualization
python3 skills/mindgraph/scripts/mindgraph.py tree "<name>" [depth]

# Find orphans, dead links, unconnected files
python3 skills/mindgraph/scripts/mindgraph.py orphans
python3 skills/mindgraph/scripts/mindgraph.py deadlinks
python3 skills/mindgraph/scripts/mindgraph.py lonely

# Full statistics
python3 skills/mindgraph/scripts/mindgraph.py stats
```

## MindSkills — 可复用的学习流程

MindSkills 是存储在 `skills/mindgraph/mindskills/` 目录下的可复用流程框架。每个 MindSkill 都有明确的执行步骤，并会将执行结果以图谱的形式保存为 markdown 文件。

### 使用 MindSkill

```bash
# List all learned mindskills
python3 skills/mindgraph/scripts/mindgraph.py skills

# Show a mindskill's process
python3 skills/mindgraph/scripts/mindgraph.py skill <name>

# List results for a mindskill
python3 skills/mindgraph/scripts/mindgraph.py results <name>
```

当用户请求执行某个流程（例如：“对 X 进行 knockout 测试”）时，请按照以下步骤操作：
1. 阅读该 MindSkill 对应的 `PROCESS.md` 文件以了解具体流程。
2. 与用户进行交互式对话，引导他们完成流程。
3. 将执行结果保存到 `skills/mindgraph/mindskills/<name>/results/<subject>.md` 文件中。
4. 在结果文件中使用 `[[wikilinks]]` 来引用相关内容。
5. 在结果文件的开头添加 YAML 标签以包含元数据。
6. 重新构建知识图谱索引。

**结果文件模板：**
```markdown
---
mindskill: <skill-name>
subject: <what was tested/analyzed>
date: <YYYY-MM-DD>
verdict: <outcome>
aliases: [<aliases>]
---
# [[<MindSkill Name>]]: [[<Subject>]]

<Results following the process defined in PROCESS.md>

## Connections
- Related: [[link1]], [[link2]]
```

### 学习新的 MindSkill

当用户表示想要学习某个名为 “X”的 MindSkill 或描述一个可复用的流程时，系统会自动创建相应的文件结构，并根据用户的描述生成 `PROCESS.md` 文件。

一个优秀的 `PROCESS.md` 文件应包含以下内容：
- **用途**：该流程的功能及其适用场景。
- **触发语句**：用户可以用来调用该流程的指令。
- **执行步骤**：具体的操作流程（需编号）。
- **输出格式**：结果文件应包含的内容。
- **总结/评分**：如何对执行结果进行总结（如适用）。

### 发现可用的 MindSkills

当用户的请求与已学习的 MindSkill 匹配时，系统会主动建议使用该流程：
- “需要我为你运行 [[Knockout Test]] 吗？”
- “你有一个 [[SEO Validator]] MindSkill — 需要我帮你审核一下吗？”
- “这看起来像是一个 [[Competitor Analysis]] 流程 — 你需要完整的框架吗？”

## 链接解析规则

链接的匹配规则（不区分大小写）如下：
1. 文件名：`[[MEMORY]]` 对应 `MEMORY.md`
2. 项目目录：`[[my-saas]]` 对应 `projects/my-saas/`
3. MindSkill 的结果文件：`[[Pet Tracker KT]]` 对应相应的结果文件。
4. YAML 别名：`aliases: [AV-Check]` 对应 `[[AV-Check]]`
5. 未匹配的链接：会被视为概念节点，并继续被跟踪以等待后续的链接关联。

## 文件位置

- 知识图谱索引：`mindgraph.json`（位于工作区根目录）
- MindSkills：`skills/mindgraph/mindskills/`
- 脚本：`skills/mindgraph/scripts/mindgraph.py`