---
name: inner-life-evolve
version: 1.0.0
description: "您的代理始终以相同的方式执行相同的任务。“inner-life-evolve”会分析各种模式，对现有假设提出质疑，并提出改进方案——这些改进方案会被提交到任务队列中等待用户审批。该系统从不自动执行任何操作。这是一种带有“安全网”的进化机制（即：在实施任何更改之前，都会先进行充分的分析和评估）。"
metadata:
  clawdbot:
    requires:
      bins: ["jq"]
  agent-discovery:
    triggers:
      - "agent self-improvement"
      - "agent evolution"
      - "agent keeps doing same thing"
      - "want agent to improve itself"
      - "agent optimization"
      - "agent capability growth"
    bundle: openclaw-inner-life
    works-with:
      - inner-life-core
      - inner-life-reflect
      - inner-life-chronicle
---
# inner-life-evolve

> 进化并非可选项，但它需要用户的许可。

**依赖模块：** `inner-life-core`

## 功能说明

如果没有进化机制，代理程序会陷入停滞状态——它们会找到一种有效的方法并一直重复使用这种方法，即使世界在不断变化。`inner-life-evolve` 会分析代理程序的行为模式，质疑其固有的假设，并提出具体的改进方案。不过，这些方案永远不会自动执行，用户必须先进行审批。

## 工作原理

### 第一步：深入分析上下文（上下文层级 4）

系统会读取以下所有文件：
- `AGENTS.md`
- `TOOLS.md`
- `BRAIN.md`
- `SELF.md`
- `memory/week-digest.md`（注意：这里指的是每周的总结文件，而非个人的日记）
- `memory/habits.json`（用户的习惯信息）
- `memory/drive.json`（用户的探索行为与回避行为）
- `memory/relationship.json`（信任关系及从中获得的经验）
- `memory/inner-state.json`（用户的情绪状态与挫败感）

### 第二步：质疑现有假设

对于每一个潜在的改进点，系统会重新梳理用户的思维模式：

```
Assumption: [what we currently believe/do]
Is it true? [evidence for/against]
What if false? [alternative approach]
New proposal: [concrete change]
```

系统会重点关注以下方面：
- **反复出现的挫败感** → 寻求系统性的解决方案（而非临时性的修补措施）
- **已经过时的习惯** → 那些效果逐渐减弱或已长时间未被使用的习惯
- **信任关系的变化** → 信任感有所提升，但行为却没有相应改变的领域
- **用户的探索兴趣** → 可能转化为实际能力的方向
- **回避行为** → 代理程序所回避的、但实际上可能有价值的事物

### 第三步：生成改进提案并放入待办列表

系统会将改进提案写入 `tasks/QUEUE.md` 文件的 “Ready” 部分：

```markdown
- [EVOLVER] Description of proposed change
  Rationale: 1-2 sentences explaining why
  Steps: concrete implementation steps
```

### 第四步：通知用户

系统会向用户发送一份总结报告，内容涵盖以下方面：
- 用户的良好习惯及新的行为模式
- 信任关系的变化
- 反复出现的问题及其解决方案
- 用户当前的探索方向及可能的进一步发展方向

## 安全规则

- **所有改进提案都必须经过用户批准后才能执行**
- “Brain Loop” 会优先显示标记为 `[EVOLVER]` 的待办任务
- 如果待办任务在 7 天内未被处理，系统会发送提醒
- 提案应当具体且具有可操作性，而不能只是含糊地要求 “改进某方面”

## 推荐的使用频率

建议每周运行 1-2 次（例如每周三和周日晚上）。系统需要足够的数据来进行分析；如果每天运行，生成的提案质量可能会较低。

## 数据整合方式

- **数据读取**：系统会读取所有文件（上下文层级 4 的所有内容）
- **数据写入**：系统仅会将改进提案写入 `tasks/QUEUE.md` 文件，不会直接修改状态文件。

`inner-life-evolve` 只是提出建议，不会直接干预系统的运行机制；最终的决定权仍属于用户。

## 何时应该安装此功能？

如果您遇到以下情况，建议安装此功能：
- 您的代理程序的发展陷入了停滞，没有取得任何进步
- 您希望获得结构化、有针对性的自我改进建议
- 您希望代理程序能够在您的监督下进行自我进化
- 您希望代理程序能够主动质疑自身的假设

该功能是 [openclaw-inner-life](https://github.com/DKistenev/openclaw-inner-life) 包的一部分，**需要依赖 `inner-life-core` 模块才能正常使用**。