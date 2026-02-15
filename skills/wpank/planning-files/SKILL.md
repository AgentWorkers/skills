---
name: planning-with-files
model: reasoning
version: 3.0.0
description: >
  File-based planning for complex tasks. Use persistent markdown files as working memory
  to survive context resets. Creates task_plan.md, findings.md, and progress.md. Use for
  any task requiring >5 tool calls, research projects, or multi-step implementations.
tags: [planning, context, workflow, manus, memory, complex-tasks]
---

# 使用文件进行规划

将持久的 Markdown 文件作为你的“磁盘上的工作记忆”。这一方法基于 Manus 中提出的上下文工程（context engineering）原则。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install planning-with-files
```

## 本技能的作用

将文件系统视为持久性存储空间，以克服上下文窗口的限制。通过三个文件来记录你的工作状态：

| 文件名 | 用途 | 更新频率 |
|------|---------|-----------------|
| `task_plan.md` | 任务阶段、进度、决策 | 每完成一个阶段后更新 |
| `findings.md` | 研究成果、发现的内容、决策 | 每有新发现时更新 |
| `progress.md` | 会话日志、测试结果、错误信息 | 整个会话期间持续更新 |

## 适用场景

**适用于：**
- 多步骤任务（3 步以上）
- 需要网络搜索的研究任务
- 从零开始构建/创建项目
- 涉及多个工具调用的任务
- 需要在多个文件之间进行协作的任务
- 失去上下文会导致工作重复的任务

**不适用场景：**
- 简单的问题
- 单个文件的编辑
- 快速查找信息
- 可以在 1-2 个操作内完成的任务

**关键词：** 复杂任务、多步骤、研究、项目构建、计划、组织

## 核心模式

```
Context Window = RAM (volatile, limited)
Filesystem = Disk (persistent, unlimited)

→ Anything important gets written to disk.
```

## 工作流程

### 第 1 阶段：创建规划文件

在开始任何复杂任务之前，在项目根目录下创建以下三个文件：

1. **创建 `task_plan.md`** — 从 [templates/task_plan.md](templates/task_plan.md) 复制
2. **创建 `findings.md`** — 从 [templates/findings.md](templates/findings.md) 复制
3. **创建 `progress.md`** — 从 [templates/progress.md](templates/progress.md) 复制

### 第 2 阶段：有条不紊地执行任务

执行任务时，请遵循以下规则：

**“每 2 次操作后保存一次”规则：**
> 每进行 2 次查看、浏览或搜索操作后，立即将发现的内容保存到文本文件中。视觉或多媒体内容不会被持久保存，因此请在它们丢失之前将其记录下来。

**决策前先阅读计划：**
在做出重要决策之前，先阅读计划文件。这有助于你在多次使用工具后仍能记住任务目标。

**执行后进行更新：**
完成某个阶段后：
- 更新阶段状态：`in_progress` → `complete`
- 记录遇到的任何错误
- 记录创建或修改的文件

**记录所有错误：**
所有错误都应记录在计划文件中，这样可以避免重复出现相同的问题。

### 第 3 阶段：系统地处理错误

**“三次尝试原则”：**

```
ATTEMPT 1: Diagnose & Fix
  → Read error carefully
  → Identify root cause
  → Apply targeted fix

ATTEMPT 2: Alternative Approach
  → Same error? Try different method
  → Different tool? Different library?
  → NEVER repeat exact same failing action

ATTEMPT 3: Broader Rethink
  → Question assumptions
  → Search for solutions
  → Consider updating the plan

AFTER 3 FAILURES: Escalate to User
  → Explain what you tried
  → Share the specific error
  → Ask for guidance
```

**重要提示：** 如果某个操作失败，**请不要重复之前的操作**，而是尝试其他方法。

### 第 4 阶段：验证任务是否完成

使用“五问重启测试”（5-Question Reboot Test）来确认任务是否完成。如果你能够回答以下问题，说明你的上下文信息是完整的：

| 问题 | 答案来源 |
|----------|---------------|
| 我现在处于哪个阶段？ | `task_plan.md` 中的当前阶段 |
| 我的目标是什么？ | 计划文件中的目标陈述 |
| 我学到了什么？ | `findings.md` 中的内容 |
| 我完成了哪些工作？ | `progress.md` 中的记录 |

## 快速参考：何时阅读，何时写入

| 情况 | 应采取的行动 | 原因 |
|-----------|--------|--------|
| 刚刚写完文件 | **不要立即阅读** | 内容仍在上下文中 |
| 查看了图片/PDF | **立即将发现的内容写入文件** | 多媒体内容容易丢失 |
| 浏览器返回了数据 | **将数据写入文件** | 屏幕截图无法持久保存 |
| 开始新的阶段 | **阅读计划文件和发现的内容** | 如果上下文信息过时，需要重新调整 |
| 发生错误 | **阅读相关文件** | 需要了解当前的状态以便解决问题 |
| 中断后重新开始 | **阅读所有规划文件** | 恢复任务状态 |

## 会话恢复

在开始新的会话时，请检查之前的工作：

```bash
# Check if planning files exist
ls task_plan.md findings.md progress.md 2>/dev/null

# If they exist, read them all before continuing
cat task_plan.md findings.md progress.md
```

如果之前有规划文件：
1. 阅读所有三个文件以恢复上下文信息
2. 运行 `git diff --stat` 以查看有哪些内容发生了变化
3. 根据变化情况更新规划文件
4. 从上次停下的地方继续执行任务

## 模板

以下是用于初始化的模板文件：
- [templates/task_plan.md](templates/task_plan.md) — 用于跟踪任务阶段
- [templates/findings.md](templates/findings.md) — 用于存储研究结果
- [templates/progress.md](templates/progress.md) — 用于记录会话进度

## 脚本

以下是一些辅助脚本，用于自动化任务流程：
- `scripts/init-session.sh` — 初始化所有规划文件
- `scripts/check-complete.sh` — 检查所有阶段是否已完成

## 参考资料

- [references/manus-principles.md] — Manus 中提出的上下文工程原则

## 不推荐的做法

| 不要这样做 | 应该这样做 |
|-------|------------|
| 使用 TodoWrite 工具来保存数据 | 直接创建 `task_plan.md` 文件 |
| 一次性设定目标后就不再查看 | 在做出决策前重新阅读计划文件 |
| 隐藏错误并默默重试 | 将错误记录到计划文件中 |
| 将所有内容都放在同一个文件中 | 将大量信息存储在单个文件中 |
| 立即开始执行任务 | 先创建计划文件 |
| 重复失败的尝试 | 记录每次尝试的过程，并调整方法 |
| 将文件放在技能目录中 | 将文件放在项目根目录下 |

## 绝对禁止的行为：

1. **在没有 `task_plan.md` 的情况下绝不要开始复杂任务** — 这是绝对不可接受的
2. **绝不要重复失败的尝试** — 要记录尝试的过程并调整方法
3. **绝不要忽略错误** — 必须记录每个错误以及相应的解决方法
4. **在多次使用工具后绝不要依赖记忆** — 一定要重新阅读计划文件
5. **对于视觉内容，绝不要忽略“每 2 次操作后保存一次”的规则** — 多媒体内容容易丢失
6. **如果连续失败超过 3 次，绝不要继续执行** — 应该寻求帮助
7. **绝不要将规划文件放在技能目录中** — 应将文件放在项目根目录下