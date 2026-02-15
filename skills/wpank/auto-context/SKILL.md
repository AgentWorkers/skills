---
name: auto-context
model: fast
description: 在执行重要操作之前，系统会自动读取相关的上下文信息。它会加载 `TODO.md`、`roadmap.md`、`handoffs`、`taskplans` 以及其他项目相关文件，以确保 AI 能够全面了解项目的当前状况。这种机制适用于开始新任务、实现新功能、进行代码重构、调试、制定计划或恢复会话等场景。
---

# 自动上下文感知——情境意识协议（元技能）

在采取行动之前，首先要了解自己所处的环境。该技能确保人工智能在执行任何重要操作之前自动加载关键的项目上下文信息，从而避免浪费精力、重复工作以及实现上的偏差。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install auto-context
```


---

## 何时激活

该技能会根据当前的操作自动触发。无需等待用户请求——在满足以下任一条件时，应主动加载上下文信息：

| 触发条件 | 原因 | 最小所需上下文信息 |
|---------|-----|-----------------|
| 开始新任务 | 明确任务优先级，避免冲突 | 关键信息 + 高优先级 |
| 实现新功能 | 了解项目计划、限制条件及最近变更 | 关键信息 + 高优先级 |
| 重构代码 | 了解最近的变化及未来的规划 | 关键信息 + 高优先级 + 中等优先级 |
| 调试问题 | 查看最近的变化、已知问题及新发现 | 关键信息 + 高优先级 + 中等优先级 |
| 规划或确定工作范围 | 全面了解项目路线图、待办事项及进度 | 所有优先级 |
| 会话开始或恢复 | 从上一次会话的状态重建认知模型 | 关键信息 + 高优先级 |
| 任务交接前 | 确保没有遗漏任何信息 | 所有优先级 |

---

## 需要阅读的上下文文件

请按优先级顺序阅读这些文件。如果任务范围较窄且低优先级的文件明显无关紧要，可以提前停止阅读：

| 优先级 | 文件名 | 用途 | 阅读时机 |
|----------|------|---------|-----------|
| 关键信息 | `TODO.md` | 当前任务、待办事项及优先级 | 始终阅读 |
| 关键信息 | `roadmap.md` | 项目阶段状态、里程碑及发展方向 | 始终阅读 |
| 高优先级 | `task_plan.md` | 活动任务的详细分解及实施计划 | 如果文件存在 |
| 高优先级 | `.cursor/handoffs/*.md` | 最近的交接记录（按日期排序，阅读最近的3条） | 如果文件存在 |
| 中等优先级 | `findings.md` | 研究结果、发现的内容及做出的决策 | 与任务相关 |
| 中等优先级 | `CHANGELOG.md` | 最近的变更及其原因 | 与任务相关 |
| 低优先级 | `.cursor/sessions/*.md` | 会话总结（按日期排序，阅读最近的2条） | 在规划或调试时阅读 |

### 备用路径

某些项目可能使用不同的文件路径。如果主要路径为空，请查看以下备用路径：

| 主要路径 | 备用路径 |
|---------|----------|
| `TODO.md` | `docs/TODO.md`, `ai/TODO.md` |
| `roadmap.md` | `docs/roadmap.md`, `ROADMAP.md` |
| `task_plan.md` | `docs/task_plan.md`, `.cursor/task_plan.md` |
| `findings.md` | `docs/findings.md`, `.cursor/findings.md` |

---

## 上下文加载策略

### 第一步：加载关键文件（始终执行）

```
Read TODO.md → Extract: current task, next priorities, blockers
Read roadmap.md → Extract: current phase, active milestone, upcoming deadlines
```

如果缺少任何关键文件，应警告用户：
> “未找到 `TODO.md` 文件。建议创建一个文件来记录任务。”

### 第二步：加载高优先级文件（如果存在）

```
Read task_plan.md → Extract: implementation steps, acceptance criteria
Glob .cursor/handoffs/*.md → Read last 3 by modification date
```

### 第三步：加载中等/低优先级文件（如果相关）

仅当当前任务需要历史上下文信息时才阅读这些文件：

- **调试时？** — 阅读 `findings.md` 和 `CHANGELOG.md`
- **规划时？** — 阅读所有文件，包括会话记录
- **快速修复时？** — 完全跳过中等和低优先级的文件

### 第四步：综合并呈现

加载完上下文信息后，在继续执行任务之前，生成一份上下文摘要（格式见下文）。

---

## 过时检测

检查所有已加载文件的修改日期，并标记可能包含过时信息的文件：

| 文件年龄 | 状态 | 处理方式 |
|-----|--------|--------|
| < 24小时 | 最新 | 直接使用 |
| 1-7天 | 当前有效 | 直接使用，但需注明文件年龄 |
| 7-30天 | 过时 | 警告：“{文件} 最后更新于 {N} 天前——在使用前请核实” |
| > 30天 | 完全过时 | 警告：“{文件} 已有 {N} 天旧，可能不再反映项目现状” |

在 macOS 上检查文件年龄的方法：

```bash
stat -f "%m %N" TODO.md roadmap.md task_plan.md findings.md CHANGELOG.md 2>/dev/null
```

在 Linux 上的方法：

```bash
stat -c "%Y %n" TODO.md roadmap.md task_plan.md findings.md CHANGELOG.md 2>/dev/null
```

---

## 上下文摘要格式

加载完上下文信息后，使用以下模板生成一份简洁的摘要。保持内容简洁——目的是提供清晰的认识，而非重复信息。

```markdown
## Context Loaded

**Current Phase:** {phase from roadmap}
**Active Milestone:** {milestone and progress}

**Current Task:** {from TODO.md or task_plan.md}
- Status: {in-progress / blocked / not started}
- Blockers: {any blockers, or "none"}

**Recent Changes:**
- {last 2-3 items from CHANGELOG or handoffs}

**Relevant Findings:**
- {key discoveries that affect the current task, or "none"}

**Stale Warnings:**
- {any staleness warnings, or "all context is fresh"}
```

如果没有任何上下文文件存在，输出以下内容：

```markdown
## Context Loaded

No project context files found. Operating without historical context.
Consider creating TODO.md and roadmap.md to enable context-aware assistance.
```

---

## 集成点

该技能与其他工作流命令相连，应作为其他命令执行的前置步骤：

| 命令 | 自动上下文感知的集成方式 |
|---------|-----------------------------|
| `/start-task` | 在开始工作前加载完整上下文；填充任务计划 |
| `/intent` | 读取项目路线图和待办事项，验证操作是否符合项目方向 |
| `/workflow` | 自动完成任何工作流的“理解”阶段 |
| `/progress` | 使用 `TODO.md` 和 `task_plan.md` 评估任务完成情况 |
| `/handoff-and-resume` | 读取最后一次交接记录，以便在恢复会话时重建状态 |
| `/session-summary` | 将加载的上下文与会话记录进行交叉核对，确保准确性 |

### 执行顺序

```
User triggers action
  → Auto-Context activates (this skill)
    → Context summary presented
      → Primary skill/command executes with full awareness
```

---

## 快速参考

```
Context Loading Checklist:
  1. Read TODO.md (critical)
  2. Read roadmap.md (critical)
  3. Read task_plan.md (if exists)
  4. Read last 3 handoffs (if exist)
  5. Check file staleness
  6. Read findings/changelog (if relevant)
  7. Present context summary
  8. Proceed with task
```

---

## 绝对禁止的行为

1. **绝不要为了节省时间而跳过关键文件** — 这会导致重复工作和实现上的冲突 |
2. **绝不要不加筛选地加载所有文件** — 这会浪费资源，并使注意力分散在无关信息上 |
3. **绝不要忽视过时警告** — 过时的上下文可能导致基于错误假设的决策 |
4. **绝不要不加总结地直接阅读文件** — 原始文件内容可能难以理解；务必先进行综合分析 |
5. **绝不要仅依赖记忆中的上下文** — 会话状态是动态变化的；务必重新阅读文件 |
6. **在没有上下文信息的情况下绝不要盲目继续操作** — 用户应意识到自己是在“盲目”工作 |
7. **绝不要阅读超过限制范围的交接记录或会话记录** — 最近的3条交接记录和最近的2次会话记录就足够了 |