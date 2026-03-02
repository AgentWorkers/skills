---
name: cross-model-review
description: 使用两种不同的 AI 模型进行对抗性计划审查。支持静态模式（角色固定）和交替模式（每轮模型之间切换写作/审查角色，完全自主）。适用于开发涉及身份验证/支付/数据模型的功能，或需要超过 1 小时才能实现的计划。不适用于简单的修复任务、研究项目或快速编写脚本的情况。
---
# 跨模型评审（Cross-Model Review）

## 元数据
```yaml
name: cross-model-review
version: 2.0.0
description: >
  Adversarial plan review using two different AI models.
  v2: Alternating mode — models swap writer/reviewer each round.
  Fully autonomous loop — no human input between rounds.
  Use when: building features touching auth/payments/data models,
  plans that will take >1hr to implement.
  NOT for: simple one-file fixes, research tasks, quick scripts.
triggers:
  - "review this plan"
  - "cross review"
  - "challenge this"
  - "is this plan solid?"
  - "adversarial review"
```

---

## 何时激活该功能
在以下情况下激活该功能：
- 用户说出任何预设的触发语句；
- 用户分享计划并请求对手意见或第二意见的评审；
- 用户请求你对多步骤实施计划进行“合理性检查”。

**注意：** 该功能不适用于以下情况：
- 简单的修复工作；
- 单行代码的修改；
- 纯研究性质的任务。

---

## 运行模式

### 静态模式（v1 — 兼容旧版本）
- 角色固定：规划者始终负责编写计划，评审者始终负责评审；
- 每轮评审都需要人工触发。

### 交替模式（v2 — 推荐模式）
- 每轮评审中，两个模型的角色会互换；
- 完全自动化运行，无需人工干预。

**运行流程：**
- 第1轮：模型A编写计划；
- 第2轮：模型B根据评审结果修改计划，然后模型A进行评审；
- 第3轮：模型A再次修改计划，模型B再次进行评审；
- 以此类推，直到两个模型都同意（评审结果为“批准”）或达到最大轮次限制。

**该模式的有效性：**
- 每个模型都必须独立提出自己的评审意见，否则无法对问题进行深入分析；
- 另一个模型可以发现过度设计或比例失调等问题；
- 通过这种交替评审的方式，双方的意见能够自然地趋于一致。

---

## 自动化运行流程（交替模式）
该流程由你（主要操作者）负责启动。启动后，整个流程将完全自动化运行。

### 第1步：保存计划并初始化
```bash
node review.js init \
  --plan /path/to/plan.md \
  --mode alternating \
  --model-a "anthropic/claude-opus-4-6" \
  --model-b "openai-codex/gpt-5.3-codex" \
  --project-context "Brief description for reviewer calibration" \
  --out /home/ubuntu/clawd/tasks/reviews
```

从标准输出（stdout）中获取工作区的路径。

### 第2步：自动化运行循环
```
while true:
  step = next-step(workspace)

  if step.action == "done":
    break  # APPROVED!

  if step.action == "max-rounds":
    ask user: override or manual fix
    break

  if step.action == "review":
    spawn sub-agent with step.model, step.prompt
    save response to workspace/round-N-response.json
    parse-round(workspace, round, response)
    continue

  if step.action == "revise":
    spawn sub-agent with step.model, step.prompt
    save output plan to temp file
    save-plan(workspace, temp file, version)
    continue
```

### 第3步：完成评审
当循环结束时，输出以下信息：
- 运行的轮次数；
- 发现并解决的问题；
- 评审的评分结果；
- 计划的最终版本文件路径（plan-final.md）。

---

## 命令行接口（CLI）参考
```
Commands:
  init           Create a review workspace
  next-step      Get next action for autonomous loop
  parse-round    Parse a reviewer response, update issue tracker
  save-plan      Save a revised plan version from writer output
  finalize       Generate plan-final.md, changelog.md, summary.json
  status         Print current workspace state

init options:
  --plan <file>            Path to plan file (required)
  --mode <m>               "static" (default) or "alternating"
  --model-a <m>            Model A — writes first (alternating mode, required)
  --model-b <m>            Model B — reviews first (alternating mode, required)
  --reviewer-model <m>     Reviewer model (static mode, required)
  --planner-model <m>      Planner model (static mode, required)
  --project-context <s>    Brief project context for reviewer calibration
  --out <dir>              Output base dir (default: tasks/reviews)
  --max-rounds <n>         Max rounds (default: 5 static, 8 alternating)
  --token-budget <n>       Token budget for context (default: 8000)

next-step options:
  --workspace <dir>        Path to review workspace (required)
  Returns JSON: { action, model, round, prompt, planVersion, saveTo }
  Actions: "review", "revise", "done", "max-rounds"

parse-round options:
  --workspace <dir>        Path to review workspace (required)
  --round <n>              Round number (required)
  --response <file>        Path to raw reviewer response (required)

save-plan options:
  --workspace <dir>        Path to review workspace (required)
  --plan <file>            Path to revised plan markdown (required)
  --version <n>            Plan version number (required)

finalize options:
  --workspace <dir>        Path to review workspace (required)
  --override-reason <s>    Reason for force-approving with open issues
  --ci-force               Required in non-TTY mode when overriding

status options:
  --workspace <dir>        Path to review workspace (required)

Exit codes:
  0   Approved / OK
  1   Revise / max-rounds
  2   Error
```

---

## 详细运行流程（供操作者实现）

### 生成评审者
```
step = next-step(workspace)  # action: "review"
response = sessions_spawn(model=step.model, task=step.prompt, timeout=120s)
# Save raw response to workspace/round-{step.round}-response.json
parse-round(workspace, step.round, response_file)
```

系统给评审者的提示：**“你是一名资深工程评审员。请仅输出符合格式的有效JSON数据。禁止使用任何工具或Markdown格式。”**

### 生成规划者
```
step = next-step(workspace)  # action: "revise"
revised_plan = sessions_spawn(model=step.model, task=step.prompt, timeout=300s)
# Save raw output as temp file
save-plan(workspace, temp_file, step.planVersion)
```

系统对规划者的提示：无需额外提示，因为提示内容已经包含所有必要的信息。

### 错误处理
- 评审者超时或失败：重试一次，然后询问用户；
- 规划者超时或失败：重试一次，然后询问用户；
- 评审JSON解析错误：再次提示评审者：“您的回复格式无效”；
- 达到最大轮次限制：向用户显示当前状态，并询问是否需要手动干预或重新开始评审。

### 评审结果判定
当评审者给出“批准”意见且不存在任何严重的阻碍因素时，流程结束。如果评审者仍提出反对意见，系统会自动将流程切换回“修订”状态。

---

## 静态模式（v1 — 兼容旧版本）
对于静态模式，仍可使用v1版本的原始运行流程：

### 第1步：初始化
```bash
node review.js init --plan <file> --reviewer-model <m> --planner-model <m>
```

### 第2步：手动运行循环
- 根据模板生成评审者的提示；
- 启动评审者；
- 解析评审者的反馈；
- 自行修改计划；
- 重复上述步骤。

### 第3步：完成评审
与交替模式相同。

---

## 与编码代理的集成
在将任何计划发送给编码代理之前，如果计划涉及以下情况，请先执行跨模型评审：
- 与身份验证、支付或数据模型相关；
- 包含3个或更多实施步骤；
- 用户尚未对计划进行过对手意见的评审。

只有当评审结果为“批准”（退出代码为0）时，才能继续下一步操作。

---

## 其他注意事项：
- 工作区数据会保存在`tasks/reviews/`目录下，便于后续查阅；
- `issues.json`文件记录了所有问题的完整生命周期；
- `meta.json`文件存储了当前运行模式、使用的模型、当前轮次、评审结果以及是否需要修订的标志；
- `next-step`是一个状态管理机制，用于决定后续的操作步骤；
- 通过去重警告功能可以避免不同轮次之间的语义差异；
- 参与评审的模型必须来自不同的供应商或团队（确保评审的客观性）；
- `--project-context`参数会被添加到评审者的提示中，以帮助进行适当的校准。