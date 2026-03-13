---
name: task-ledger
description: >
  OpenClaw 的持久化工作流程层：适用于需要长时间运行的任务。适用于以下场景：  
  - 任务包含多个阶段；  
  - 可恢复（即任务在失败后可以重新开始）；  
  - 能够在子代理/ACP 之间并行执行；  
  - 需要在后台执行或通过 cron 计划器触发；  
  - 具有外部副作用；  
  - 需要可审计的输出结果以及可恢复的执行能力。
metadata:
  {
    "openclaw": {
      "emoji": "🧾",
      "requires": { "bins": ["python3", "bash"] }
    }
  }
---
# 任务日志（Task Ledger）

使用“任务日志”（Task Ledger）将耗时较长的代理任务转换为持久化的任务对象，从而避免依赖不稳定的聊天记录或临时信息。

“任务日志”是一个基于 OpenClaw 执行原语的工作流层。它**不会**替代 ACP、子代理（sub-agents）、执行器（exec）、定时任务（cron）或相关技能（skills）。它为这些组件提供了一个持久化的任务结构：

- 任务检查点文件存储在 `tasks/` 目录中
- 执行日志存储在 `logs/` 目录中
- 任务输出物和报告存储在 `outputs/` 目录中
- 用于处理进程（process）、会话（session）或定时任务（cron）引用的执行绑定信息
- 支持父子任务结构
- 提供依赖关系检查和任务就绪状态检查功能
- 支持恢复机制
- 优先提供简短的更新信息，同时支持基于文件的详细报告

## 使用场景

在以下情况下使用该功能：

- 任务运行时间可能超过 5 分钟
- 任务包含多个执行阶段
- 任务使用了后台执行器（background exec）
- 任务使用了会话生成器（sessions_spawn）
- 任务使用了定时任务（cron）
- 任务具有外部副作用
- 任务涉及需要重启、部署或维护的工作流程，且这些操作可能带来风险
- 任务需要被拆分为父子任务，并需要跟踪其依赖关系
- 多个代理或子代理需要并行执行任务
- 在开始下游任务之前，需要检查任务的就绪状态
- 任务报告应优先提供简短的更新信息，同时支持基于文件的详细报告
- 用户希望任务的状态可以被恢复、重新执行或审计

**注意**：不要对每个小任务都使用该功能。它主要用于那些丢失状态或执行结构会导致重大损失的工作场景。

## 功能介绍

该功能包括：

- 任务检查点文件（JSON 格式），存储在 `tasks/` 目录中
- 执行日志，存储在 `logs/` 目录中
- 任务输出物和报告，存储在 `outputs/` 目录中
- 用于创建、更新、推进和结束任务生命周期的辅助工具
- 用于恢复、恢复和总结任务状态的辅助工具
- 用于处理进程、子任务或定时任务引用的绑定辅助工具
- 任务架构中的回滚元数据
- 支持父子任务关系和依赖关系的工具
- 考虑任务就绪状态的调度辅助工具
- 专为重启和部署工作流程设计的模板
- 适用于报告、交接、归档和图表展示的友好用户界面
- 支持优先提供简短更新信息，同时支持基于文件的详细报告

相关文件打包后存储在 `toolkit/` 目录下。

## 首次使用指南

如果当前工作区尚未包含该工具包，请将以下文件复制到工作区根目录：

- `toolkit/scripts/*` → `<workspace>/scripts/`
- `toolkit/task-templates/*` → `<workspace>/task-templates/`
- `toolkit/tasks/README.md` → `<workspace>/tasks/README.md`

如果缺少以下目录，请创建它们：

- `tasks/`
- `logs/`
- `outputs/`

**注意**：除非用户明确要求，否则不要覆盖用户已修改的文件。建议仅复制缺失的文件，并报告已安装的内容。

## 操作流程：

1. 在执行任务前与用户确认计划。
2. 首先创建任务的基本框架。
3. 根据实际情况选择具体的执行阶段。
4. 当存在相关执行引用时（如 `process.sessionId`、`subtask.sessionKey`、`cron.jobId`），记录这些信息。
5. 如果任务涉及多个部分，需要创建父子任务并建立依赖关系。
6. 如果任务需要并行执行，建议每个工作者对应一个父任务和一个子任务。
7. 在开始依赖任务之前，先检查任务的就绪状态；适当情况下使用“start-if-ready”机制。
8. 每完成一个执行阶段后，更新任务文件。
9. 在恢复任务时，先读取恢复总结信息并验证实际状态。
10. 如果实际状态与检查点信息不一致，先修正检查点数据再继续执行。
11. 仅继续未完成的部分。
12. 优先提供简洁的用户友好型总结信息；在必要时保留详细的报告文件。
13. 根据需要以用户友好的方式导出或总结任务状态。
14. 在任务完成时主动通知相关人员。
15. 如果任务执行过程中被中断后重新开始，也要主动通知相关人员。

## 并行任务模式

对于多代理或多子代理的任务处理方式：

- 为整个目标创建一个**父任务**。
- 为每个工作者或子任务分支创建一个**子任务**。
- 将每个子任务与其对应的执行引用关联起来。
- 在子任务中详细记录执行进度。
- 由父任务负责协调各个任务的就绪状态、完成情况和报告生成。

**注意**：不要将单个任务 JSON 文件视为共享的并发写入目标。使用任务树结构（task trees）比使用共享状态更加安全。

## 核心命令

创建任务基本框架：  
```bash
./scripts/new-task.sh <slug> <title> [goal] [executionMode] [stagesCsv] [priority] [owner]
```

**实用辅助工具：**  
```bash
./scripts/list-open-tasks.py
python3 ./scripts/task-ls-tree.py
python3 ./scripts/task-ready.py <taskId> [--json]
python3 ./scripts/task-start-if-ready.py <taskId> [nextAction]
python3 ./scripts/task-graph-export.py [--format markdown|dot|json] [--open-only]
./scripts/show-task.py <taskId>
./scripts/task-events.py <taskId> [limit] [--type <eventType>] [--json]
./scripts/update-task.py <taskId> ...
./scripts/task-advance.py <taskId> [nextAction]
./scripts/task-bind-process.py <taskId> <processSessionId> [pid] [--state <state>]
./scripts/task-bind-subtask.py <taskId> <sessionKey> [--agent-id <agentId>]
./scripts/task-bind-cron.py <taskId> <jobId> [--schedule <expr>] [--next-run-at <iso>]
./scripts/task-verify.py <taskId> <summary> ...
./scripts/task-resume-summary.py <taskId> [--json|--markdown]
./scripts/task-export.py <taskId> [--format markdown|json|short] [--write-report]
./scripts/close-task.py <taskId> <final-status> [summary]
./scripts/task-doctor.py [taskId] [--strict] [--json]
```

## 专用模板**

针对常见的高风险工作流程，提供了以下模板示例：  
- `restart-openclaw-gateway.example.json`  
- `deploy-service.example.json`  
- `sync-feishu-doc.example.json`

## 实用原则：

任务文件本身并不代表任务的真实状态。它们只是任务状态的缓存描述。最终应以实际执行结果为准。