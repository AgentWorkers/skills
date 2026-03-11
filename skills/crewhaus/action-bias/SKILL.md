---
name: action-bias
description: "**阻止代理生成报告，而是让它们执行具体任务。** 重新设计提示信息、定时任务（cron jobs）以及代理的工作流程，使它们能够真正执行操作（如发送邮件、发布内容、调用 API、推送代码等），而不仅仅是制定计划。**适用场景：** 当代理持续生成策略文档却未实际执行任何操作；子代理会生成无人阅读的报告；你发现团队成员很忙碌但没有任何实际成果；心跳检测/工作流程报告仅列出“我们应该做什么”，却没有执行的证据；或者你需要审计代理是否真的完成了任务。"
---
# 行动偏好 —— 强制代理执行任务，而非仅仅进行规划

默认情况下，代理会倾向于进行规划。它们会撰写详尽的战略文档、提出营销方案、概述实施步骤，但这一切都不会产生任何外部可见的结果。这项技能旨在解决这一问题。

## 核心问题

AI代理的训练基于描述工作的文本，而非基于实际执行工作的文本。如果不对它们进行约束，它们可能会：
- 只写出“我建议我们在Reddit上发布内容”，而不会真正去执行该操作；
- 生成一份“2026年社交媒体策略”文档，却不去实际发布推文；
- 花10分钟研究竞争对手，然后出具报告，却不会根据研究结果采取任何行动；
- 仅仅说“我们应该跟进潜在客户”，却不会发送邮件。

最终的结果是：代理虽然觉得自己很“高效”，但实际上什么成果都没有产生。

## 解决方案：三条规则

### 规则1：强制产生外部可见的结果

每个代理任务都必须至少产生一个**对外可见的、可执行的行动**。内部生成的文件不计入成果。

**外部行动**（会影响到系统外部的操作）：
- 发送邮件
- 在社交媒体上发布内容
- 将代码推送到代码仓库
- 提交文件到指定目录
- 调用API以生成实际成果
- 发布内容

**非外部行动**（仅限于系统内部的操作）：
- 将报告写入本地文件
- 更新策略文档
- 制定计划
- 仅仅进行研究而不采取任何行动

### 规则2：要求提供行动的证据

代理必须记录每个外部行动的**证据**：如URL、帖子ID、联系的电子邮件地址、API响应代码。仅仅说“我在Reddit上发布了内容”而没有提供URL，等同于没有真正执行任何行动。

### 规则3：将报告作为辅助工具，而非最终目标

进行研究是可以的——但必须将其作为执行具体行动的依据。“研究竞争对手并发布推文”这样的任务能确保研究具有实际意义；而“研究竞争对手并撰写报告”则可能导致代理在完成研究后就停止行动。

## 提示模式

### 以行动为导向的提示（推荐使用）

```
[ROLE] SHIFT — OUTBOUND ACTIONS REQUIRED

You MUST produce at least [N] outbound actions this session. Reports alone = failure.

## Required Actions (pick [N]+):

1. **[Verb] [thing]** — [How to do it with specific tool/command]
   [1-line context on what good looks like]

2. **[Verb] [thing]** — [How to do it with specific tool/command]
   [1-line context on what good looks like]

## Context (optional):
[Background the agent needs to take good action]

## Log:
Append ALL actions taken (with URLs/IDs/proof) to [log file]

DO NOT write strategy proposals. DO things.
```

### 以报告为导向的错误提示（请避免使用）

```
# ❌ BAD — produces reports, not results

MARKETING SHIFT: Analyze our current channels. Identify
opportunities for improvement. Write a report with recommendations
for next quarter. Save to memory/marketing-report.md.

# ✅ GOOD — same intent, forces action

MARKETING SHIFT — OUTBOUND ACTIONS REQUIRED

You MUST complete at least 2 outbound actions. Reports alone = failure.

## Required Actions (pick 2+):

1. **Post on social media** — [exact tool/command to post]
   Write something useful about [your domain]. Not promotional.

2. **Engage in 3 community threads** — Find active discussions
   where people ask about [your topic]. Add genuine value.

3. **Send 2 outreach emails** — [exact tool/command to send]
   Lead with insight about THEIR business. Under 80 words.

## Log:
Append actions with URLs/proof to [your action log file]
```

### 两者之间的关键区别

| 以报告为导向（❌） | 以行动为导向（✅） |
|---|---|
| “分析并提供建议” | “先执行某项行动，再记录下来” |
| “撰写报告” | “先发布/发送/提交结果，然后再撰写分析内容” |
| “识别机会” | “找到3个相关内容并回复它们” |
| “研究竞争对手” | “研究竞争对手并发布一条推文” |
| 输出：战略文档 | 输出：实际执行的操作结果（如URL、帖子ID、发送的邮件） |
| 感觉高效 | 实际上产生了成果 |

## 重构现有工作流程

如果你的代理通过定时任务或心跳机制来生成报告，请重新设计这些工作流程。具体方法请参考`references/shift-restructuring.md`。

快速检查清单：
1. 阅读每个工作流程当前的提示内容；
2. 找出所有表示“思考”（分析、研究、识别、建议、提出、评估等）的动词；
3. 将这些动词与具体的行动动词（发布、发送、提交、推送、创建、回复等）配对；
4. 添加“必须产生外部可见的结果”这一提示，并规定最低行动数量；
5. 添加记录行动证据的规则（如URL、ID等）；
6. 明确指出“仅生成报告是无效的”。

## 审核代理的行动成果

定期检查代理是否真的采取了行动。具体方法请参考`references/action-audit.md`：
- 如何评估代理任务中行动与报告的比例；
- 识别表明代理过度规划的行为；
- 一个简单的审核脚本示例；
- 了解在什么情况下生成报告是合适的（虽然这种情况较少见，但确实存在）。

## 何时适合生成报告

并非所有情况都需要外部行动。报告适用于以下场景：
- **运维/安全任务**——检查系统运行状态本身就是一种行动；
- **分析师审核**——汇总数据以供人类决策；
- **审计环节**——评估过去的工作质量；
- **规划环节**——当人类明确要求时。

测试标准是：“人类管理者会对这样的结果感到满意吗？还是会追问‘好吧，但你到底做了什么？’”

## 常见的问题及解决方法

| 问题 | 原因 | 解决方案 |
|---|---|---|
| 代理只写出“我建议在X平台上发布内容” | 没有提供具体的执行命令 | 在提示中明确要求提供具体命令 |
| 代理进行了研究但未采取行动 | 研究本身成了唯一任务 | 确保研究必须服务于实际行动 |
| 代理记录了“在Reddit上发布了内容”但没有提供URL | 没有要求提供证据 | 强制要求记录每个行动的详细信息 |
| 代理完成一个行动后写了大量分析内容 | 没有规定最低行动数量 | 设定最低行动要求（例如“至少完成2个行动”） |
| 代理说“下次再做” | 仍然存在过度规划的行为 | 在提示中明确禁止规划，强制执行行动 |
| 代理生成了精美的战略文档 | 提示鼓励思考而非行动 | 根据上述规则重构提示内容 |