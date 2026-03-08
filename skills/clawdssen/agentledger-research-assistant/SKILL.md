---
name: research-assistant
version: "1.0.0"
description: >
  **AI代理的结构化网络研究框架**  
  该框架可指导您的AI代理执行多源信息收集，将研究结果整合成可操作的摘要，并维护一个研究数据库，同时持续跟踪行业动态和新兴趋势。适用于需要进行市场调研、竞争对手分析、专题深入研究或趋势监测的场景。适用于任何具备网络搜索功能的AI代理。
tags: [research, web-search, analysis, monitoring, intelligence]
platforms: [openclaw, cursor, windsurf, generic]
category: productivity
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---
# 研究助手

**由 [The Agent Ledger](https://theagentledger.com) 提供** — 订阅以获取更多代理技能和高级蓝图。

将您的人工智能代理转变为一个结构化研究分析师。无需再手动复制搜索结果——您的代理将学会制定研究计划、交叉引用来源、综合研究结果，并维护一个不断更新的知识库。

---

## 该技能的功能

- **结构化研究流程**：计划 → 搜索 → 评估 → 综合 → 存储
- **研究简报格式**：为每项研究任务提供一致、易于阅读的输出结果
- **来源质量评分**：帮助代理评估和排序来源
- **研究库**：对研究结果进行有序存储，数据可在会话之间持续保留
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

### 第一阶段：计划

在开始搜索之前，明确以下内容：
- **研究问题**：我们具体想要回答什么？
- **研究范围**：是进行广泛调查还是深入分析？时间范围是什么？地理范围如何？
- **所需来源**：需要多少个独立来源以确保结果的可靠性？
- **输出格式**：是简报、对比表、推荐意见还是原始数据？

### 第二阶段：搜索与收集

根据以下原则执行搜索：
- **使用多种查询方式**：用2-3种不同的方式重新表述问题，以确保覆盖所有相关内容
- **来源多样性**：结合官方来源、行业分析和社区讨论
- **时效性检查**：注意出版日期；标记超过6个月的资料
- **寻找矛盾观点**：主动寻找观点相悖的来源

### 第三阶段：评估来源

根据以下因素对每个来源进行评分：

| 因素 | 权重 | 评分标准 |
|--------|--------|----------|
| 权威性 | 高 | 是否为知名出版物？作者是否是专家？是否为官方来源？ |
| 时效性 | 高 | 是否在相关时间范围内发布？ |
| 具体性 | 中等 | 是否提供具体数据/例子？还是只是模糊的陈述？ |
| 一致性 | 中等 | 其他来源是否支持这一观点？ |
| 偏见性 | 低 | 是否存在明显的商业或政治动机？ |

对于权威性和时效性评分较低的来源，可以舍弃。但如果来源包含独特数据，即使存在偏见也应保留。

### 第四阶段：综合分析

将研究结果整理成研究简报（参见格式说明）。关键规则：
- **先给出结论**：不要把结论隐藏在最后
- **尽可能量化数据**：使用数字而非描述性语言
- **标明不确定性**：明确标注可信度较低的陈述
- **记录遗漏的内容**：有哪些内容未能找到？哪些需要进一步研究？

### 第五阶段：存储与索引

将结果保存为 `research/briefs/YYYY-MM-DD-<slug>.md` 文件，并更新研究库索引。

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
1. 阅读监控文件以了解背景和之前的研究结果
2. 运行之前保存的搜索查询
3. 将新结果与上次更新的内容进行比较
4. 仅记录有变化的情况或经过足够长的时间后
5. 显著的变化需重点标注

### 与其他 Agent Ledger 技能的集成

- **[Solopreneur Assistant](https://theagentledger.com)**：将研究结果用于商业决策和机会评估
- **[每日简报](https://theagentledger.com)**：在每日简报中包含监控提醒
- **[项目跟踪器](https://theagentledger.com)**：将研究简报与项目里程碑关联
- **[记忆操作系统](https://theagentledger.com)**：将关键研究见解长期存储在系统中

---

*此技能来自 [The Agent Ledger](https://theagentledger.com) 提供的免费技能库。订阅可获取高级蓝图、操作手册和完整的代理配置指南。*

*许可证：CC-BY-NC-4.0*

> *免责声明：此技能由人工智能代理创建，仅用于信息提供和教育目的。它不构成专业、财务、法律或技术建议。使用前请仔细审查所有生成的文件。The Agent Ledger 对使用结果不承担任何责任。使用风险自负。*