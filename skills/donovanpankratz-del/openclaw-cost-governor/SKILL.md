---
name: cost-governor
version: 1.0.0
description: >
  **子代理生成及审批流程的预飞成本估算**  
  该功能用于预防API使用过度导致的费用超支和意外账单问题，实现对`sessions_spawn`调用行为的预算控制，并提供每日支出跟踪功能。对于采用多代理架构的OpenClaw部署来说，这一功能至关重要。
homepage: https://clawhub.com
changelog: Initial release - Pre-flight gates, historical multipliers, spend tracking
metadata:
  openclaw:
    emoji: "💰"
    requires:
      bins: []
    os:
      - linux
      - darwin
      - win32
---
# 成本管理器 - 子代理成本控制

在创建子代理之前，会进行预先的成本检查，并跟踪所有支出。该工具能够阻止意外产生的高额费用（例如超过300美元的账单）。

## 包含的文件

- `SKILL.md` — 本文件（代理使用说明）
- `README.md` — 供人类阅读的设置指南
- `cost-tracking-template.md` — 将此文件复制到 `notes/cost-tracking.md` 以开始使用
- `lib/cost-tracker.js` — 核心成本估算和日志记录库
- `bin/cost-summary.js` — 命令行工具：用于生成每日/每月的支出汇总

## 解决的问题

假设你在 Opus 上创建了一个子代理来“研究被动收入的方法”，30分钟后发现竟然花费了12美元。该工具能够在执行任务前估算成本，并对高成本任务（费用超过0.50美元）进行审批，同时会记录所有的支出情况。

## 使用场景

- **在创建任何子代理之前**：估算成本并记录下来
- **每日支出审查**：汇总实际支出与预算的差异
- **任务完成后进行对账**：比较估算成本与实际支出

## 核心规则

1. **所有预计成本超过0.50美元的子代理创建** 需要用户的明确批准
2. **所有支出记录** 会被保存到 `$WORKSPACE/notes/cost-tracking.md` 文件中
3. **估算成本时会使用基于历史数据的乘数**（详见成本模型）
4. **禁止未经审批的高成本操作** — 所有高成本操作都必须在执行前显示其成本

## 成本模型

成本模型基于 `cost-tracking.md` 中的历史数据：

| 任务类型 | 基本估算成本 | 乘数 | 实际估算成本 |
|-----------|--------------|------------|-------------------|
| 创意类（开放性任务） | 每个令牌的成本估算 | **7.5倍** | 适用于所有创意类任务 |
| 研究类（有明确要求的任务） | 每个令牌的成本估算 | **3倍** | 包括网络搜索和内容合成 |
| 技术类（结构化任务） | 每个令牌的成本估算 | **2倍** | 包括代码编写、配置设置和结构化输出 |
| 简单类任务（使用模板） | 每个令牌的成本估算 | **1.5倍** | 适用于填写信息或生成简短回复 |

**模型成本费率（大约每1000个令牌的成本）：**
- Claude Opus：输入成本约0.075美元，输出成本约0.375美元
- Claude Sonnet：输入成本约0.003美元，输出成本约0.015美元
- GPT-4：输入成本约0.03美元，输出成本约0.06美元
- Grok 4.1 Fast Reasoning：输入成本约0.003美元，输出成本约0.015美元
- Claude Haiku 4.5：输入成本约0.0008美元，输出成本约0.004美元

### 估算公式

```
estimated_cost = (estimated_output_tokens / 1000) * output_rate * task_multiplier
```

**示例：**
- 任务：创意写作（在 Opus 上需要5000个令牌）
- 计算：(5000 / 1000) * 0.375 * 7.5 = **14.06美元**
- 处理方式：**需要用户批准**（因为成本超过了0.50美元的阈值）

## 设置步骤

1. 创建成本跟踪文件：
```bash
mkdir -p ~/.openclaw/workspace/notes
touch ~/.openclaw/workspace/notes/cost-tracking.md
```

2. 为 `cost-tracking.md` 文件添加头部信息：
```markdown
# Cost Tracking Log

| Date | Task | Model | Est. | Actual | Ratio | Notes |
|------|------|-------|------|--------|-------|-------|
```

3. 设置每日预算（可选）：
```bash
echo "DAILY_BUDGET=20.00" >> ~/.openclaw/workspace/.env
```

## 使用方法

### 创建子代理前的检查

```
User: "Research passive income methods"
Agent: Checking cost... Estimated $3.50 (Research task, Opus, ~3K tokens * 3x multiplier). Approve?
User: Yes
Agent: [spawns, logs to cost-tracking.md]
```

### 每日支出汇总

可以手动执行或通过 cron 任务来生成每日支出汇总：
```markdown
## Daily Spend — 2026-02-21
| Task | Model | Est. | Actual | Ratio |
|------|-------|------|--------|-------|
| PassiveIncomeResearch | Opus | $3.50 | $4.20 | 1.2x |
| AIHardwareResearch | Sonnet | $0.80 | $0.65 | 0.8x |
**Total:** $4.30 est / $4.85 actual
**Budget remaining:** $15.15 / $20.00 daily
```

### 任务完成后进行对账

每个子代理完成任务后：
1. 查看实际成本（可以通过 `/status` 命令获取）
2. 将实际成本记录到 `cost-tracking.md` 文件中
3. 如果成本与估算值存在持续差异，需要更新乘数

## 触发机制

- **创建子代理前的检查**：在 `sessions_spawn` 执行前进行成本估算并记录。如果成本超过0.50美元，请求用户批准。
- **每日自动检查（可选）**：汇总每日支出，标记超出预算的情况。
- **任务完成后**：记录实际成本，并在数据可用时更新乘数。

## 审批流程

1. 使用模型、任务类型和乘数来估算成本
2. 如果估算成本 ≤ 0.50美元，则直接执行任务并默默记录
3. 如果估算成本 > 0.50美元，则向用户展示估算结果并等待用户批准
4. 将审批结果（批准/拒绝/修改）记录到成本跟踪文件中

## 预算警报

设置每日预算上限。当支出超过预算时，系统会停止创建新的子代理并通知用户。

**设置方法：**
在您的工作空间配置中设置预算上限，或通过系统提示告知用户：
> “每日API使用预算：XX美元。如果预计总成本超过此限额，将停止创建子代理。”

**基于 cron 的每日支出汇总（可选）：**
将以下代码添加到您的 cron 任务中：
```bash
# Daily cost summary at 11 PM
0 23 * * * node ~/.openclaw/workspace/skills/cost-governor/bin/cost-summary.js --daily
```

## 避免的错误做法

- ❌ 不要使用 Opus 来执行简单的查询任务（应使用 Sonnet 或 Haiku）
- ❌ 对于没有成本上限的创意任务（如“写一部小说”），不要使用 Opus
- ❌ 如果只需要一个子代理，就不要创建多个
- ❌ 忽略成本与估算值之间的差异（需要及时更新乘数）
- ❌ 不要进行任务完成后的对账

## 高级功能：自定义乘数

您可以在 `cost-tracking.md` 文件的头部信息中自定义乘数：
```markdown
## Multipliers (Updated 2026-02-21)
- Creative: 10x (our tasks run long)
- Research: 2.5x (bounded queries)
```

代理会在每次检查时读取这些自定义乘数。

## 与其他技能的集成

- **sessions_spawn**：在创建子代理之前，始终执行成本检查
- **AGENTS.md**：在代理日志中记录支出情况（例如：“上次使用：X.XX美元”）
- **Cron 任务**：为高成本的重复性任务设置成本检查机制

## 常见问题解答

**Q：为什么估算成本总是不准确？**
A：根据实际支出情况，定期更新 `cost-tracking.md` 文件中的乘数。

**Q：如何获取实际成本？**
A：可以在子代理完成任务后使用 `/status` 命令查看，或者查看服务提供商的仪表盘。

## 重要性说明

来自 r/LocalLLM 的真实案例（2026年1月）：
> “我让 OpenClaw 代理运行了一整晚，在 Opus 上创建了8个研究子代理。结果发现API费用达到了340美元。如果使用了这个成本管理工具，就能避免这笔费用。”

请不要犯类似的错误。

---

**作者：** OpenClaw 社区  
**许可证：** MIT  
**使用要求：** 需要具备子代理功能的 OpenClaw，以及 `notes/` 目录的存在