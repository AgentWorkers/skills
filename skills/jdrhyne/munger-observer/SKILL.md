---
name: munger-observer
description: 每日智慧回顾：将查理·芒格的思维模型应用到你的工作和思考中。适用于需要评估决策、分析思维模式、识别偏见、运用思维模型、进行“芒格式审查”或运行“Munger Observer”（芒格观察工具）的场景。该功能会在每日定时回顾时自动触发，也可通过手动指令触发，例如“运行Munger Observer”、“审视我的思维方式”、“检查是否存在盲点”或“应用思维模型”。
---

# Munger Observer

这是一个自动化的每日审查工具，它运用查理·芒格（Charlie Munger）的思维模型来帮助发现潜在的盲点和认知陷阱。

## 工作流程

### 1. 收集当天的活动信息
- 阅读当天的记忆记录文件（`memory/YYYY-MM-DD.md`）
- 扫描当天的会话日志，提取当天的所有活动信息
- 包括：所做的决策、处理的任务、解决的问题以及用户提出的请求

### 2. 应用思维模型

**逆向思维（Inversion）**
- 什么可能会出错？成功的反面是什么？
- “告诉我我可能会失败的地方，这样我就不会去那里。”

**二级思考（Second-Order Thinking）**
- 那之后呢？这些后果又会带来什么影响？
- 短期的收益是否会导致长期的问题？

**激励分析（Incentive Analysis）**
- 哪些行为会得到奖励？是否存在隐藏的激励机制？
- “告诉我激励是什么，我就能告诉你结果会怎样。”

**机会成本（Opportunity Cost）**
- 有哪些事情没有被去做？这种专注带来的代价是什么？
- 放弃的最佳替代方案是什么？

**偏见检测（Bias Detection）**
- 证实性偏见：是否只寻找能够验证自己观点的信息？
- 沉没成本谬误：是否因为过去的投入而继续做某事？
- 社会认同偏见：是否因为别人也在做而跟风？
- 可得性偏见：是否过分重视最近或最显眼的信息？

**能力范围（Circle of Competence）**
- 是在熟悉的领域内工作，还是在未知的领域内工作？
- 如果是在未知领域，是否需要保持适当的谦逊和谨慎？

**安全边际（Margin of Safety）**
- 如果出现问题，有什么缓冲措施？
- 在哪些方面做得过于冒险了？

### 3. 生成输出结果

- **如果发现了问题**：生成1-2条简洁的、符合芒格思维风格的观察结果。
- **如果没有发现明显问题**：输出“一切正常——今天没有发现任何认知陷阱。”

## 输出格式
```
🧠 **Munger Observer** — [Date]

[Insight 1: Model applied + observation + implication]

[Insight 2 if applicable]

— "Invert, always invert." — Carl Jacobi (Munger's favorite)
```

## 示例
```
🧠 **Munger Observer** — January 19, 2026

**Opportunity Cost Alert:** Heavy focus on infrastructure today. The content queue is aging — are drafts decaying in value while we polish tools?

**Second-Order Check:** Speed improvement is good first-order thinking. Second-order: faster responses may raise expectations for response quality. Speed without substance is a trap.

— "Invert, always invert."
```

## 安排（可选）
可以设置一个定时任务（cron job）来自动执行每日审查：
- 建议的时间：工作日结束时（例如，当地时间下午5点）
- 触发消息：`MUNGER_OBSERVER_RUN`