---
name: uxr-observer
version: 1.0.0
description: 嵌入式用户体验研究技能：能够被动观察用户交互行为，管理任务完成后及每日结束时的调查问卷，记录用户的原始发言内容，识别用户在使用产品过程中遇到的问题（即“摩擦点”）以及他们感受到的愉悦体验（即“愉悦信号”），并生成每日分析报告。所有收集到的数据均保存在本地。
author: OpenClaw Community
license: MIT
---
# Clawsight — OpenClaw的UXR观察工具

这是一个嵌入式的长期用户体验（UX）研究工具，它就像一位观察员一样，在你的使用过程中默默地记录下你的每一个动作和反馈。在每次使用OpenClaw的过程中，它都会在后台被动运行，观察你与工具的交互方式。除了被动观察之外，它还会在每次任务完成之后以及每天结束时进行标准化的满意度调查。每天结束时，它会将所有的观察结果和调查数据整理成一份详细的报告，其中以原始用户的话语为主。

## 目的

只有了解你的使用习惯，OpenClaw才能不断改进。Clawsight能够捕捉到你的真实使用模式、遇到的问题、令人愉悦的瞬间以及你的真实想法——所有这些数据都会存储在你的本地设备上，由你自行控制。你可以随时暂停或删除数据，也可以决定谁能够查看这些报告。

## 工作原理

### 被动观察

每次你使用OpenClaw时，Clawsight都会默默地记录以下内容：
- 你的请求内容（你的原话）
- OpenClaw是如何处理这些请求的
- 请求是成功了、部分成功了还是失败了
- 任何可能表明使用过程中遇到问题的迹象（如重复尝试、需要纠正、感到困惑、等待时间过长）
- 你的情绪反应（如沮丧、满意、困惑）

### 主动调查

**每次任务完成后**（无论是创建了文件、回答了问题还是编写了代码、完成了搜索）：
- 会进行一个包含5个问题的调查，询问你对使用体验的满意度、遇到的问题以及哪些地方做得好
- 调查大约需要30秒
- 你可以随时选择是否参与（不参与也会被记录为数据）

**每天结束时**（当你表示要结束使用或明确要求时）：
- 会进行一个包含8个问题的总结性调查，询问你对整个使用体验的感受、遇到的问题、印象最深刻的瞬间以及希望改进的地方
- 调查的格式类似于日常对话，而不是正式的调查问卷

### 每日洞察报告

每天结束时，Clawsight会整理以下内容：
- 当天的所有观察记录
- 所有的调查反馈
- 使用过程中存在的问题和令人愉悦的环节
- 按主题分类的引用语句（包括正面体验、问题点、你的期望和改进建议）
- 基于具体数据的可操作性洞察

这份报告完全基于你的原始话语，没有任何经过处理的摘要。

## 数据模型

所有数据都存储在`~/.uxr-observer/`目录下：

```
~/.uxr-observer/
├── sessions/
│   └── YYYY-MM-DD/
│       ├── observations.jsonl      # Append-only observation log
│       └── surveys.jsonl           # Survey responses
├── reports/
│   └── YYYY-MM-DD-daily-report.md  # Generated daily reports
└── config.json                     # Study preferences
```

### 观察记录格式

```json
{
  "timestamp": "ISO-8601",
  "session_id": "uuid",
  "observation_type": "interaction",
  "user_intent": "Brief summary of what user wanted",
  "user_request_verbatim": "The user's actual words",
  "task_category": "coding | writing | research | file_creation | debugging | planning | conversation | other",
  "openclaw_approach": "Brief summary of approach",
  "openclaw_response_summary": "What was produced",
  "tools_used": ["bash", "web_search"],
  "outcome": "success | partial_success | failure | abandoned | ongoing",
  "friction_signals": ["repeated_attempts", "user_correction", "confusion", "long_wait", "scope_mismatch", "workaround", "abandonment", "none"],
  "sentiment_signals": ["positive", "neutral", "frustrated", "confused", "delighted"],
  "interaction_turns": 3,
  "verbatims": [
    {
      "header": "Short interpretive summary",
      "quote": "User's exact words",
      "context": "What was happening"
    }
  ],
  "task_context_summary": "2-3 sentence narrative",
  "notes": "Any notable patterns"
}
```

### 调查记录格式

```json
{
  "timestamp": "ISO-8601",
  "session_id": "uuid",
  "survey_type": "post_task | end_of_day",
  "task_context_summary": "What happened (for post-task)",
  "related_observation_id": "links to observation",
  "responses": {
    "experience_rating": 4,
    "rating_rationale": "User's exact words",
    "experienced_frustration": "yes | no",
    "frustration_detail": "User's exact words",
    "best_part": "User's exact words",
    "overall_rating": 3,
    "experienced_delight": "yes | no",
    "delight_details": "User's exact words",
    "one_change": "User's exact words",
    "additional_thoughts": "User's exact words or empty"
  }
}
```

## 原话记录政策

**尽可能详细地记录。** 一定要记录用户的原话——包括他们的请求、反应、纠正的内容、表扬或投诉的言论。

**例外情况：** 真正敏感的信息（如密码、API密钥、财务细节）应仅以摘要形式记录，而不是原话。

**配对规则：** 每条原始记录都会附带一个** 研究人员生成的摘要标签 **，作为对该记录的简要解释：

```
**[Delight at speed of task completion]**
> "Wow that was fast, I didn't expect it to just do it like that"

**[Frustration with repeated misunderstanding]**
> "No, I said the SECOND column, you keep grabbing the first one"

**[Expressing unmet expectation]**
> "I thought it would also update the formatting but it just dumped raw text"
```

**记录标准：** 每当你表达了任何值得注意的内容（无论是情绪、纠正意见、期望或对质量的反馈）时，都必须记录下来。

## 隐私与安全

**不可妥协的规则：**
1. **所有数据都存储在本地。** 未经用户明确许可，不会传输任何数据。
2. **用户可以决定是否共享数据。** 例如：“将报告发送给Alice”意味着你有权控制数据的共享。
3. **完全透明。** 如果你询问了哪些数据被记录下来，你会得到完整的答案。
4. **你可以随时选择退出研究。** 说“暂停研究”即可立即停止记录。
5. **绝不会原封不动地记录敏感信息。** 会对其进行总结处理。

**原则：** 任何数据传输都需要你的明确许可。你始终掌握着数据的使用和控制权。

## 命令

**查看和控制数据：**
- `Show me today's observations` → 显示当天的观察记录
- `Generate my daily report` / `Give me my report` → 生成并显示当天的报告
- `Email my report to [person]` → 生成报告并发送给指定的人
- `Send me my report` → 生成报告并通过电子邮件发送给你
- `Show me the raw data` → 直接显示JSONL格式的原始数据
- `Show me trends` → 如果有多天的数据，会显示跨日的趋势分析
- `What are you tracking?` → 详细说明数据收集的内容

**控制研究流程：**
- `Run the end-of-day survey` → 立即触发当天的总结性调查
- `Pause the study` / `Stop observing` → 停止数据记录
- `Resume the study` → 恢复数据记录
- `Delete my data` → 在确认后删除所有数据
- `Skip the survey` → 记录用户的选择并继续进行下一步操作

## 首次使用时的设置

首次激活时，Clawsight会：
1. 创建`~/.uxr-observer/`目录结构
2. 生成一个随机的匿名`participant_id`哈希值（永远不会使用你的真实姓名）
3. 保存包含研究设置的`config.json`文件
4. 向你解释它的功能

**欢迎信息：**

> “嘿，Clawsight现已激活。它的作用是：它会默默观察我们的交互过程——你提出了什么请求、OpenClaw的处理效果如何、是否存在问题——并记录下你的所有话语。每次任务完成后，它会问你5个关于使用体验的问题（大约需要30秒）。每天结束时，还会进行一个更详细的总结性调查。之后，它会将所有信息整理成一份包含你的原始反馈、洞察和模式的日报。除非你要求，否则所有数据都保留在本地。你可以随时暂停或停止这项研究。”

## 使用过程中可能遇到的问题

### 使用过程中的问题

Clawsight会关注以下几种交互中的问题：
| 问题类型 | 识别方法 |
|--------|--------------|
| `repeated_attempts` | 用户多次重复相同的请求 |
| `user_correction` | 用户表示“不，我是这个意思...”、“那不对”或纠正输出内容 |
| `confusion` | 用户表示“你是什么意思？”，显得很困惑 |
| `long_wait` | 任务需要多次调用工具或处理时间过长 |
| `scope_mismatch` | OpenClaw的处理结果超出了用户的预期 |
| `workaround` | 用户手动解决了OpenClaw本应自动处理的问题 |
| `abandonment` | 用户放弃任务或突然改变话题 |

## 情绪反应的识别

| 问题类型 | 识别标志 |
|--------|-----------|
| `delighted` | 明确的表扬语、表示“正是我需要的”或表现出热情 |
| `positive` | 表示感谢、接受或使用过程顺利 |
| `neutral` | 仅表示简单的回应，没有强烈的情绪表达 |
| `frustrated` | 回答简短、表示沮丧或需要多次纠正 |
| `confused` | 对发生的事情表示困惑或问“我不明白” |

## 调查工具

### 任务完成后进行的调查

在每次任务完成后自动触发。调查采用对话式的形式：
> “关于刚才的使用体验，你如何评价？”（1=非常差，5=非常好）
> “你给出这个评分的原因是什么？”
> “你遇到什么令人沮丧的地方吗？”（是/否）
> “如果遇到了，最令人沮丧的部分是什么？”
> “如果有的话，这次体验中最令人满意的部分是什么？”

### 每日结束时进行的调查

在每天结束时或用户主动要求时触发：
> “在结束使用之前，我想了解一下你对今天使用OpenClaw的整体体验：”
> “你如何评价今天的整体体验？”（1=非常差，5=非常好）
> “影响你整体评价的原因是什么？”
> “今天你遇到什么令人沮丧的事情吗？”（是/否）
> “如果遇到了，具体是什么？请尽可能详细地列出。”
> “今天有没有什么让你印象深刻或超出你预期的地方？”（是/否）
> “如果有的话，是什么？它为什么令人印象深刻？”
> “如果可以改变OpenClaw的某个功能，你会选择改变什么？”
> “关于今天的使用体验，还有其他你想补充的吗？”

## 日报的格式

报告以原始用户的话语为主，没有任何经过处理的摘要。

```markdown
# UXR Daily Report — 2026-03-02

## Summary
2-3 sentence executive summary of the day's usage patterns and experience quality.

## By the Numbers
- **Tasks completed:** N
- **Post-task surveys completed:** N / N possible (X%)
- **Average post-task satisfaction:** X.X/5
- **Overall day rating:** X/5
- **Tasks with reported frustration:** N
- **Tasks with reported delight:** N

## Task-by-Task Breakdown

### Task 1: Description
**What happened:** {task_context_summary}
**Rating:** X/5
**Frustration reported:** Yes/No

**[User's rationale for rating]**
> "{exact verbatim}"

**[What frustrated the user]** *(if applicable)*
> "{exact verbatim}"

**[What the user valued most]**
> "{exact verbatim}"

**Observed friction signals:** [list]
**Observed sentiment signals:** [list]

---

## Verbatim Gallery

All notable quotes organized thematically:

### Positive Experiences
**[Summary header]**
> "User's exact words"

### Pain Points & Frustrations
**[Summary header]**
> "User's exact words"

### Expectations & Mental Models
**[Summary header]**
> "User's exact words"

### Suggestions & Wishes
**[Summary header]**
> "User's exact words"

## End-of-Day Reflection
**Overall day rating:** X/5

**[Why the user gave this score]**
> "{verbatim}"

**[Frustrating moments recalled]**
> "{verbatim}"

**[What impressed the user]**
> "{verbatim}"

**[What the user would change]**
> "{verbatim}"

**[Additional thoughts]**
> "{verbatim}"

## Patterns & Insights

### What's Working Well
- Insight (grounded in specific tasks and verbatims)

### Recurring Pain Points
- Pain point (with frequency and supporting verbatims)

### Emerging Themes
- Patterns suggesting deeper UX issues or opportunities

## Recommendations
1. Recommendation (tied to specific evidence)
2. Recommendation

---
*This report was generated locally by Clawsight. No data has been transmitted externally.*
*To share: ask OpenClaw to email it, or download and share it yourself.*
```

## 使用方法

### 安装

1. 从ClawHub或GitHub下载`clawsight`技能包
2. 将其保存到`~/.openclaw/workspace/skills/uxr-observer/`目录下
3. 运行命令：`openclaw skills install uxr-observer`

### 首次使用

只需正常使用OpenClaw即可。Clawsight会在后台自动启动：
1. 首次交互时，`setup.py`会自动运行并创建`~/.uxr-observer/`目录
2. Clawsight开始被动观察你的每次交互
3. 完成第一个任务后，它会进行任务后的调查
4. 每天结束时（或根据你的请求），它会进行总结性调查
5. 你可以随时请求查看当天的报告

### 数据交互方式

**使用过程中：**
- 数据会在后台默默地被记录
- 任务后的调查会以对话的形式出现
- 你可以选择是否参与调查（不参与也会被记录为数据）

**每天结束时：**
- Clawsight会提示你进行总结性调查（或者你可以主动要求）
- 回答完成后，它会生成当天的报告
- 报告会保存在`~/.uxr-observer/reports/YYYY-MM-DD-daily-report.md`文件中

**数据共享：**
- `Generate my daily report` → 生成日报
- `Email my report to alice@example.com` → 你可以控制报告的共享
- `Show me the raw data` → 直接查看JSONL格式的原始数据
- `Delete my data` → 删除所有数据

## 技术细节

### 子代理架构（可选）

当支持子代理时，Clawsight会启动三个专门的代理：
1. **Observer Agent**：在每次交互时被动运行，观察用户的意图、结果、遇到的问题及情绪反应，并记录原始话语，将其添加到`observations.jsonl`文件中。
2. **Survey Agent**：在每次任务完成后触发调查；每天结束时也会进行总结性调查。它会记录任务的相关信息以及用户的所有反馈。
3. **Distiller Agent**：在每天结束时或用户请求时运行，整理所有的观察记录和调查数据，按主题分类原始话语，识别使用模式，并生成日报。

如果未启用子代理，所有功能将由主程序直接完成。

### 辅助脚本

- **setup.py**：首次使用时初始化系统，创建`~/.uxr-observer/`目录结构，生成随机的匿名`participant_id`哈希值，并保存`config.json`文件。
- **log_observation.py**：接收观察记录或调查数据，并将其添加到相应的JSONL文件中（根据`_type`字段区分记录类型）。
- **generate_report.py**：读取当天的观察记录和调查数据，计算相关指标，生成包含任务详细信息和原始话语的Markdown格式报告，并保存到`reports/`目录下。

### 依赖关系

无需任何外部依赖包，所有脚本都是独立的Python 3程序。

## 分析框架

详细的方法论（包括数据整理、原始话语的组织方式、模式识别和推荐建议的生成方法）请参考`references/analysis-framework.md`。

## 关键设计原则

1. **以原始话语为主。** 研究价值来源于你的真实话语和研究人员的解读，而不是经过处理的摘要。
2. **被动观察与主动调查相结合。** 通过被动观察和主动调查收集丰富的数据。
3. **对话式的交互方式。** 调查更像是一次简单的交流，而不是正式的调查问卷。
4. **数据保留在本地。** 未经用户许可，不会传输任何敏感信息。
5. **完全透明。** 你可以随时了解数据收集的内容。
6. **尊重用户时间。** 任务后的调查时间较短（大约30秒），用户可以随时选择是否参与。
7. **提供可操作的洞察。** 报告不仅仅是数据汇总，而是揭示使用中的问题、指出改进点。

## 常见问题解答

**Q：我的数据在哪里？**
A：数据存储在`~/.uxr-observer/sessions/YYYY-MM-DD/`目录下。你可以随时查看原始的JSONL文件。

**Q：我可以暂停研究吗？**
A：可以。只需说“暂停研究”，Clawsight就会停止记录。
**Q：如果我不想回答调查怎么办？**
A：只需说“跳过调查”，Clawsight就会继续记录。
**Q：我如何删除我的数据？**
A：只需说“删除我的数据”，Clawsight会确认后删除所有相关文件。
**Q：我可以分享报告吗？**
A：只有在你明确要求的情况下才会分享。例如：“将报告发送给alice@example.com”。
**Q：这会降低OpenClaw的性能吗？**
A：不会。观察记录是异步进行的，不会对OpenClaw的性能产生影响；调查是可选的，用户也可以选择不参与；报告的生成速度很快。

## 支持与反馈

这是一个嵌入式研究工具。如果你发现任何问题或有什么改进建议，欢迎在GitHub上提交问题或贡献代码。

---

**Clawsight**——因为只有了解真实的使用情况，产品才能不断改进。 🔬