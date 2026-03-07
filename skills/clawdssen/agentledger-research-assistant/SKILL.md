---
name: research-assistant
version: 1.0.0
description: >
  **AI代理的结构化网络研究框架**  
  该框架能够指导您的AI代理进行多源信息收集，将研究结果整合成可操作的简报，同时维护一个研究数据库，并持续跟踪各类主题的发展动态。适用于需要进行市场调研、竞争对手分析、深度主题研究，或持续监控趋势与新闻的场景。适用于任何具备网络搜索功能的AI代理。
tags:
  - research
  - web-search
  - analysis
  - monitoring
  - intelligence
platforms:
  - openclaw
  - cursor
  - windsurf
  - generic
category: productivity
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---
# 研究助手

**由 [The Agent Ledger](https://theagentledger.com) 提供** — 订阅以获取更多代理技能和高级蓝图。

将您的人工智能代理转变为一个结构化研究分析师。无需再手动复制搜索结果——您的代理将学会规划研究、交叉引用资料、整合发现内容，并维护一个不断更新的知识库。

---

## 该技能的功能

- **结构化研究流程**：规划 → 搜索 → 评估 → 整合 → 存储
- **研究简报格式**：为每项研究任务提供一致、易于阅读的输出结果
- **来源质量评分**：帮助代理评估和排序资料来源
- **研究库**：有序存储研究结果，数据可在会话之间持续保留
- **主题监控**：通过定期重新研究来跟踪不断变化的主题
- **竞争对手/市场分析模板**：提供现成的分析框架

---

## 设置（5分钟）

### 第一步：创建研究目录

```
research/
├── README.md          ← Library index (auto-maintained)
├── briefs/            ← Completed research briefs
├── monitoring/        ← Topics being tracked over time
└── templates/         ← Custom research templates (optional)
```

### 第二步：创建 `research/README.md`

```markdown
# Research Library

## Recent Briefs
<!-- Agent maintains this list automatically -->

## Monitored Topics
<!-- Topics being tracked with periodic updates -->

## Quick Stats
- Total briefs: 0
- Active monitors: 0
- Last research: never
```

### 第三步：添加到代理指令中

将以下内容添加到您的 `AGENTS.md`、`SOUL.md` 或系统提示中：

```
## Research Protocol

When asked to research something:
1. Read `research/README.md` for existing work on this topic
2. Follow the Research Protocol below
3. Save the brief to `research/briefs/YYYY-MM-DD-<slug>.md`
4. Update `research/README.md` index
```

---

## 研究流程

### 第一阶段：规划

在开始搜索之前，明确以下内容：
- **研究问题**：我们具体想回答什么？
- **研究范围**：是进行广泛调查还是深入分析？时间范围是什么？地理范围如何？
- **所需资料来源**：需要多少独立来源才能确保结果的可靠性？
- **输出格式**：是简报、对比表、推荐意见还是原始数据？

### 第二阶段：搜索与收集

根据以下原则执行搜索：
- **使用多种查询方式**：用2-3种不同的方式重新表述问题，以确保覆盖所有相关内容
- **来源多样性**：结合官方资料、行业分析报告和社区讨论
- **时效性检查**：注意资料的发布日期；标记超过6个月的资料
- **寻找矛盾观点**：主动寻找与现有观点相悖的资料

### 第三阶段：评估资料来源

根据以下标准对每个资料来源进行评分：

| 评分因素 | 权重 | 评估标准 |
|--------|--------|----------|
| 权威性 | 高 | 是否为知名出版物？作者是否是专家？是否为官方来源？ |
| 及时性 | 高 | 是否在相关时间范围内发布？ |
| 具体性 | 中等 | 是否提供具体数据或实例？还是只是模糊的陈述？ |
| 一致性 | 中等 | 是否有其他资料支持这一观点？ |
| 偏见性 | 低 | 是否存在明显的商业或政治偏见？ |

对于权威性和及时性评分较低的资料来源，可以将其标记为不合格；但如果这些资料包含独特的数据，仍可保留。

### 第四阶段：整合资料

将研究结果整理成研究简报（参见下方格式）。关键规则：
- **先给出结论**：不要把结论隐藏在最后
- **尽可能量化数据**：使用数字而非描述性语言
- **标注不确定性**：明确标出可靠性较低的陈述
- **记录缺失的信息**：哪些信息未能找到？哪些需要进一步研究？

### 第五阶段：存储与索引

将研究结果保存为 `research/briefs/YYYY-MM-DD-<slug>.md` 文件，并更新研究库索引。

---

## 研究简报格式

```markdown
# [Research Question]

**Date:** YYYY-MM-DD
**Requested by:** [context]
**Confidence:** High / Medium / Low
**Staleness risk:** [when this research might become outdated]

## TL;DR
[2-3 sentence executive summary with the key finding]

## Key Findings

### Finding 1: [Title]
[Detail with supporting evidence]
- Source: [name] ([link]) — [date]
- Confidence: High/Medium/Low

### Finding 2: [Title]
[Detail with supporting evidence]
- Source: [name] ([link]) — [date]
- Confidence: High/Medium/Low

[Continue as needed]

## Data Points
| Metric | Value | Source | Date |
|--------|-------|--------|------|
| [key stat] | [value] | [source] | [date] |

## Contradictions & Caveats
- [Any conflicting information found]
- [Limitations of this research]

## Knowledge Gaps
- [What we couldn't find]
- [What needs deeper investigation]

## Sources
1. [Full citation with URL and access date]
2. [...]

## Recommendations
- [Actionable next steps based on findings]

---
*Research conducted by AI agent using the Research Assistant skill by [The Agent Ledger](https://theagentledger.com)*
```

---

## 主题监控

对于会随时间变化的主题（如市场趋势、竞争对手动态、法规变化）：

### 设置监控机制

创建 `research/monitoring/<topic-slug>.md` 文件：

```markdown
# Monitoring: [Topic Name]

**Started:** YYYY-MM-DD
**Frequency:** [daily / weekly / bi-weekly]
**Search queries:** 
- "[query 1]"
- "[query 2]"
**Alert triggers:** [what constitutes a notable change]

## Updates

### YYYY-MM-DD
- [What changed since last check]
- [New data points]
- [Assessment: significant / minor / no change]
```

### 定期检查流程

在进行监控时：
1. 阅读监控文件，了解背景信息和之前的研究结果
2. 重新运行之前保存的搜索查询
3. 将新结果与上次更新的内容进行比较
4. 仅记录有变化的情况或达到指定时间间隔的情况
5. 突出显示重要的变化

### 与 Heartbeats/Cron 的集成

将相关设置添加到您的 `HEARTBEAT.md` 文件中，或设置定时任务（cron）：

```
## Research Monitors
Check research/monitoring/ for topics due for refresh.
Only check topics whose frequency interval has elapsed.
```

---

## 专用模板

- **竞争对手分析模板**  
- **市场规模分析模板**  
- **决策分析模板**  

---

## 定制化设置

### 调整研究深度

在代理指令中添加相应设置：

```
Research depth levels:
- **Quick scan** — 3-5 sources, 5 minutes, key facts only
- **Standard brief** — 8-12 sources, full brief format
- **Deep dive** — 15+ sources, include academic/primary sources, extended analysis
Default to standard unless specified.
```

### 针对特定领域的研究

针对专业领域，提供额外的指导：

```
When researching [your domain]:
- Prioritize sources from: [trusted sources list]
- Key metrics to always check: [domain-specific KPIs]
- Common pitfalls: [domain-specific biases to watch for]
```

### 引用格式

```
Citation preference: [choose one]
- Inline links (default) — [Source Name](url)
- Numbered footnotes — [1], [2], etc.
- Academic — Author (Year). Title. Publication.
```

---

## 常见问题与解决方法

| 问题 | 解决方案 |
|-------|-----|
| 研究过于肤浅 | 增加研究深度；在提示中加入“查找原始资料”的要求 |
| 资料来源过多，无法整合 | 强调第四阶段的整合步骤；要求先提供“总结”，再提供详细信息 |
| 研究结果过时 | 添加时效性筛选条件（例如“仅使用过去6个月内的资料”） |
| 代理直接输出原始搜索结果 | 强制使用简报格式；提醒代理进行整合而非简单复制 |
| 监控频率过高 | 调整监控文件的更新频率；根据资料时效性来决定检查频率 |
| 研究库变得混乱 | 定期清理旧简报（超过6个月的文件）

---

## 与其他 Agent Ledger 技能的集成

- **[Solopreneur Assistant](https://theagentledger.com)**：将研究结果用于商业决策和机会评估
- **[每日简报](https://theagentledger.com)**：在每日简报中包含监控结果
- **[项目跟踪器](https://theagentledger.com)**：将研究简报与项目里程碑关联
- **[Memory OS](https://theagentledger.com)**：将关键研究结果存储在长期记忆系统中

---

*本技能属于 [The Agent Ledger](https://theagentledger.com) 提供的免费技能库的一部分。订阅即可获取高级蓝图、操作手册和完整的代理配置指南。*

*许可协议：CC-BY-NC-4.0*