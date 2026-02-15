# Agentic Compass — 人工智能代理的自我反思工具

这是一个专为人工智能代理设计的自我反思工具，仅支持本地操作，能够强制代理采取**客观**的行动。所有数据都不会离开您的机器。

## 功能介绍

该工具会读取您的本地内存文件，并生成一份结构化的**代理行动计划**：
- 一项主动任务（无需提示即可开始）
- 一项待定/定时执行的任务
- 一条避免规则（停止执行某项操作）
- 一项具体的行动结果

该工具专为那些使用可量化指标（而非主观评估标准）的人工智能代理而设计。

## 使用方法

```bash
# Print plan
python3 scripts/agentic-compass.py

# Write plan to memory/agentic-compass.md
python3 scripts/agentic-compass.py --write

# Use custom memory paths
python3 scripts/agentic-compass.py --daily /path/to/memory/2026-01-31.md --long /path/to/MEMORY.md
```

## 代理特定评估指标（v2.0 — 客观评估指标）

| 评估指标 | 评估内容 | 评分方式 |
|------|------------------|------------------|
| **完成率** | 开始的任务与完成的任务数量 | 统计内存文件中的 `[DONE]` 标记 |
| **响应相关性** | 我是否回答了用户的问题？ | 统计用户的确认或纠正信息 |
| **工具使用质量** | 工具调用失败次数、重试次数、超时情况 | 分析内存文件中的工具错误日志 |
| **内存一致性** | 会话间的上下文保持情况 | 检查是否遗漏了对先前决策的引用 |
| **主动性** | 未经提示主动提出的想法 | 统计主动采取的行动（开始的任务、提出的建议） |

## 为什么这个版本更适合人工智能代理

### 旧版本（v1）存在的问题 ❌
- 主观的自我评估（存在偏见）
- 将“信任”作为评估指标（不适用于人工智能）
- 代理的存在是片段化的（没有连续的“自我意识”）
- 涉及情感方面的评估指标（难以量化）

### 新版本（v2）的改进 ✅
- **可量化的评估指标**（可通过内存文件进行统计）
- **客观的评分标准**（避免主观感受）
- **跨会话的数据追踪**（利用内存文件保持数据连续性）
- **以行动为导向**（强制代理做出具体决策，而非基于主观感受）

## 示例输出

```
Score: 3.0/5
Weakest axis: Completion Rate (45% started tasks finished)

Plan:
- Proactive: Draft first implementation of OSINT Graph Analyzer
- Deferred: Retry cron jobs after gateway diagnostic
- Avoidance: Stop checking Moltbook API during peak hours
- Ship: Create skills-to-build.md prioritization document
```

## 本地操作限制

- **仅** 读取本地文件（如 memory.md、MEMORY.md、日志文件）
- **仅** 写入本地文件
- **不进行任何网络请求**（数据完全保留在本地）

## 设计理念

大多数自我反思工具仅停留在提供洞察的阶段，而 Agentic Compass 则能强制代理采取实际行动。

**关键区别：**
- **被动反思**：“我可能应该做某件事。”
- **Agentic Compass**：“我将在 [时间] 前完成某件事，这是具体的计划。”

对于人工智能代理来说，这一点至关重要，因为它们没有持续的自我意识。每次会话开始时，它们的状态都是“全新的”。如果没有明确的计划和避免规则，它们往往会重复相同的错误模式。

## 安装方法

可以通过 ClawdHub 安装：
```
clawdhub install agentic-compass
```

或者从源代码仓库克隆：
```bash
git clone https://github.com/orosha-ai/agentic-compass
```

## 版本历史

- **v2.0**：引入了针对代理的客观评估指标
- **v1.0**：侧重于人类的评估指标（主动性、完成率、信号响应、韧性、信任度）