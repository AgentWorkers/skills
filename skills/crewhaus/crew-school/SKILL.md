---
name: crew-school
description: "**AI智能体团队的结构化学习系统**  
该系统用于设计学习课程、开展研究活动、跟踪学习进度，并预防常见的学习问题（如拖延输出、仅制定计划而不执行）。适用于智能体学习环境的搭建、训练课程的运行、知识漏洞的审计，以及为特定类型智能体制定学习计划。无论是单个智能体还是多智能体团队，均可使用该系统。"
---
# 代理学习系统（Agent Learning System）

该系统能够运行结构化的学习课程，生成包含实际知识内容的文档，而非仅仅的学习计划。这有效防止了最常见的学习失败模式：即代理只是口头表示“我会去研究这个问题”，然后就不再继续行动。

## 快速入门

1. **识别知识缺口**：你的代理需要学习什么？检查现有的知识文件与实际需求之间的差距。
2. **选择学习主题**：优先选择那些直接影响日常工作的关键知识缺口。
3. **创建学习课程**：使用下面的课程模板。系统中的防懒惰机制是不可或缺的，请勿删除这些限制措施。
4. **验证学习成果**：检查文档的行数、引用来源的数量，并确认其中是否包含具体的执行计划。

## 课程模板

创建学习课程时，请严格使用此模板，并将其中的占位符替换为实际内容。

```
CREW LEARNING SESSION — [ROLE]: [TOPIC]

You are the [ROLE] agent. Your assignment is to research [TOPIC] and produce a comprehensive knowledge article.

### Context
[2-3 sentences: why this topic matters for this agent's role]

### Prerequisites
[List knowledge files to read first, or "None"]

### Research Assignment
Deep research on [TOPIC]. You MUST cover:
1. [Subtopic 1] — [Specific questions]
2. [Subtopic 2] — [Specific questions]
3. [Subtopic 3] — [Specific questions]

### Execution Rules — READ CAREFULLY
- DO NOT PLAN. EXECUTE. If you write "I will..." or "Let me create...", STOP and DO IT instead.
- DO NOT stop after outlining. Every section must contain real research findings.
- Search the web. Perform at least 5 web searches. Read at least 2 full articles.
- Cite sources. Every claim needs a source URL.
- Be specific. Names, numbers, examples > generic advice.

### Output Requirements
Write findings to `knowledge/[filename].md` with this structure:

# [Topic]

> **TL;DR:** [2-3 sentence summary]
> **Applies to:** [Which roles]
> **Prerequisites:** [Other knowledge files]

## Key Takeaways
- [Bullet list of actionable findings]

## [Sections with real findings]

## Practical Application
[Steps, templates, checklists the agent can use immediately]

## Sources
[All URLs cited]

### Minimum Quality Thresholds
- >= 150 lines, >= 1500 words, >= 5 cited sources with URLs
- >= 4 H2 sections with substantive content
- 0 instances of "TODO", "TBD", "I will", "I'll create"
- Must include TL;DR, Key Takeaways, and Practical Application sections

### Completion
Append one line to memory/learning-log.md:
[DATE] | [ROLE] | [TOPIC] | [LINES] | [SOURCES] | [ONE-LINE SUMMARY]
```

## 课程设计

对于需要多阶段学习的情况，可以创建一个课程规划文件。请参考 [references/curriculum-design.md](references/curriculum-design.md) 以获取以下信息：
- 如何评估知识缺口
- 根据知识之间的依赖关系来安排学习顺序
- 如何组织跨职能的学习活动
- 学习与实践的比例建议

## 使用 Cron 任务进行自动化调度

为了实现每日学习的自动化，你需要创建一个课程跟踪的 JSON 文件，并通过 Cron 任务来定期执行这些学习任务。详细操作方法请参阅 [references/automation.md](references/automation.md)，内容包括：
- 课程规划的 JSON 格式
- Cron 任务脚本模板
- 进度跟踪与自动升级机制

## 常见的问题及解决方法

| 问题 | 原因 | 解决方案 |
|---------|-------|-----|
| 代理仅生成学习计划而未实际进行研究 | 提示信息中缺乏执行要求 | 在提示中添加“请勿仅制定计划，必须执行！”并设定最低行数要求 |
| 学习成果过于简略（少于 100 行） | 没有质量标准 | 设定最低行数（150 行）和引用来源数量（至少 5 个） |
| 学习内容过于泛泛而缺乏具体数据 | 未要求进行网络搜索 | 增加“至少进行 5 次网络搜索”的要求 |
| 课程在仅进行一次搜索后就结束 | 超时设置过短 | 将 `runTimeoutSeconds` 设置为至少 300 秒 |
| 代理虽然阅读了前置要求文件但仍未进行研究 | 前置要求文件占据了整个课程时间 | 将前置要求文件限制为 1-2 个，并在提示中对其进行总结 |
| 不同课程中出现重复的研究内容 | 未对现有知识进行核查 | 在分配学习主题前先检查现有的知识文件 |

## 质量评估

课程结束后，请检查以下内容：
1. **文档行数**：`wc -l knowledge/[文件].md`（目标：至少 150 行）
2. **引用来源数量**：`grep -c "http" knowledge/[文件].md`（目标：至少 5 个）
3. **是否包含执行计划**：`grep -ci "I will\|I'll create\|TODO\|TBD" knowledge/[文件].md`（目标：这些内容不应出现在文档中）
4. **文档结构**：是否包含“总结”、“关键要点”和“实际应用”等部分
5. **实用性**：代理能否利用这些学习成果来提升明天的工作效率？