---
name: planning-with-files
description: "此技能应在用户请求开始执行复杂任务、研究项目、多步骤实施过程，或任何预计需要使用超过5个工具的任务时使用。触发条件包括：“plan this”（制定计划）、“start planning”（开始规划）、“help me build”（帮助我构建）、“research and implement”（研究并实施）以及“/plan”（/计划）。"
metadata: { "openclaw": { "emoji": "📋", "version": "1.0.0", "author": "shannon/openclaw-port" } }
---
# 使用文件进行规划

这是一种基于手写Markdown的持续性规划方法。文件系统相当于长期存储空间，而“上下文窗口”则代表当前可用的工作内存。

## 核心原则

```
Context Window = RAM (volatile, limited)
Filesystem     = Disk (persistent, unlimited)
→ Anything important MUST be written to disk.
```

## 适用场景

- 需要分多个步骤完成的任务（包含3个以上阶段或5个以上工具调用）
- 需要研究并实施的任务
- 跨多个会话持续进行的任务
- 任何存在目标偏离风险的任务

**不适用场景：** 单个文件的编辑、快速查询或简单问题。

## 会话开始流程

**务必首先执行以下步骤——无例外：**

1. 运行初始化脚本，创建三个规划文件：
   ```
   exec: bash {baseDir}/scripts/init-session.sh "<task description>"
   ```

2. 在`task_plan.md`文件中填写`## Goal`部分，详细描述任务目标。
3. 将任务分解为3到7个阶段，并将这些阶段添加到`## Phases`部分中。
4. 在继续之前，确认所有文件都已创建。

如果无法使用`exec`命令，可以使用`{baseDir}/templates/`目录中的模板手动创建这三个文件。

## 三个文件

### `task_plan.md` —— 目标跟踪文件（最为重要）
- 在会话开始时创建，切勿删除。
- 在做出任何重大决策之前，务必重新阅读该文件。
- 在阶段完成、决策确定或遇到错误时，及时更新该文件。

### `findings.md` —— 知识存储文件
- 存储研究结果、发现的内容以及技术决策。
- **2-Action规则**：每次查看、搜索或获取数据后，立即更新`findings.md`文件。

### `progress.md` —— 会话日志文件
- 记录所采取的行动、测试结果以及遇到的错误。
- 该文件为只读模式，切勿修改历史记录。

## 工作流程

```
BEFORE every major action:
  → Re-read task_plan.md (keeps goal in attention)

EVERY 2 view/search/fetch operations:
  → Save key findings to findings.md NOW

AFTER completing a phase:
  → Update phase status in task_plan.md to "complete"
  → Append phase summary to progress.md

WHEN an error occurs:
  → Log it in task_plan.md under ## Errors table
  → Never repeat the same failing action

BEFORE stopping:
  → Run: exec bash {baseDir}/scripts/check-complete.sh
  → Only stop if all phases show "complete"
```

## 文件更新规则

| 触发条件 | 需要更新的文件 | 更新内容 |
|---------|---------------|---------|
| 开始新任务 | `task_plan.md` | 更新任务目标及阶段信息 |
| 进行第二次研究 | `findings.md` | 更新关键发现内容 |
- 做出决策 | `findings.md` | 更新技术决策内容 |
- 阶段完成 | `task_plan.md` | 更新阶段状态（例如：完成） |
| 阶段完成 | `progress.md` | 更新阶段总结 |
- 发生错误 | `task_plan.md` | 更新错误信息 |
- 测试结果 | `progress.md` | 更新测试结果 |

## 错误处理机制

```
ATTEMPT 1: Diagnose & Fix
  → Read error carefully → identify root cause → targeted fix

ATTEMPT 2: Alternative Approach
  → Same error? Try different tool/library/method
  → NEVER repeat the exact same failing action

ATTEMPT 3: Broader Rethink
  → Question assumptions → search for solutions → update plan

AFTER 3 FAILURES:
  → Escalate to user: explain what was tried, share the error, ask for guidance
```

## 任务完成验证

在告知用户任务已完成之前，请执行以下操作：
1. 运行`exec bash {baseDir}/scripts/check-complete.sh`命令。
2. 如果有任何阶段尚未完成，则继续执行任务。
3. 只有在所有阶段都通过验证后，才能向用户交付最终结果。

## 会话恢复机制

如果会话中的上下文信息被清除（例如，通过`/clear`命令），请按照以下步骤恢复会话：
1. 读取`task_plan.md`以恢复任务目标和阶段状态。
2. 读取`progress.md`以了解已完成的操作。
3. 读取`findings.md`以恢复研究过程中的关键信息。
4. 从第一个未完成的阶段开始继续执行任务。

## 关键原则

- **规划是必不可少的**：在没有`task_plan.md`文件的情况下，切勿开始执行复杂任务。
- **文件是长期存储的依据**：会话中的信息可能随时丢失，但文件系统中的数据是永久保存的。请务必将重要内容记录下来。
- **切勿重复失败的原因**：记录每次尝试的方法，并及时调整策略。
- **有效的错误处理机制至关重要**：处理错误的方式直接关系到任务的质量。
- **决策前务必重新阅读相关文件**：通过不断回顾规划内容，确保始终明确任务目标。