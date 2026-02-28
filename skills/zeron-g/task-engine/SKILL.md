---
name: task-engine
description: "多代理任务编排引擎，支持状态机跟踪功能。适用于需要自动化监控、多代理协作以及基于 Discord 的进度跟踪的复杂多步骤项目。"
---
# 任务引擎

该任务引擎使用基于状态机的机制，通过 JSON 数据进行持久化存储，来协调多个代理（如 Claude Code、Eva 等）执行的多步骤项目。每个任务都会被分解为子任务，并分配给相应的代理执行；执行进度通过心跳信号进行监控，最终结果通过 Discord 进行报告。

## 命令行接口 (CLI) 命令

所有命令都在技能的根目录下执行：

```bash
cd /home/zeron/.openclaw/workspace/skills/task-engine
```

所有命令都支持使用 `--json` 选项来生成机器可读的输出格式：
```json
{"ok": true, "task_id": "TASK-001", "status": "PLANNING", "message": "Created TASK-001"}
```

### 创建任务

```bash
python3 scripts/task_engine.py create "Implement feature X" --priority P0 --plan "3 phases: models, API, tests"
python3 scripts/task_engine.py create "Feature Y" --priority P1 --json
```

### 查看任务状态

```bash
python3 scripts/task_engine.py status                    # All active tasks (table)
python3 scripts/task_engine.py status TASK-001           # Detailed single task
python3 scripts/task_engine.py status TASK-001 --json    # Machine-readable
python3 scripts/task_engine.py status --all              # Include terminal tasks
```

### 更改任务状态

```bash
python3 scripts/task_engine.py transition TASK-001 approve --note "Plan approved" --json
python3 scripts/task_engine.py transition TASK-001 block --note "Waiting on API key"
python3 scripts/task_engine.py transition TASK-001 complete --note "All verified" --json
```

### 向代理分配子任务

```bash
python3 scripts/task_engine.py dispatch TASK-001 "Implement auth models" \
    --agent claude-code --type dev --json
python3 scripts/task_engine.py dispatch TASK-001 "Run integration tests" \
    --agent eva --type test --deps subtask_01,subtask_02
```

分配第一个子任务后，任务状态会自动从 “APPROVED” 更改为 “IN_PROGRESS”。

### 更新子任务进度

```bash
python3 scripts/task_engine.py subtask TASK-001 subtask_01 start --progress 30 --json
python3 scripts/task_engine.py subtask TASK-001 subtask_01 done --note "Models complete" --json
python3 scripts/task_engine.py subtask TASK-001 subtask_02 fail --note "Schema mismatch" --json
```

### 检查任务进度（通过心跳信号）

```bash
python3 scripts/task_engine.py check              # Check all active tasks (verbose)
python3 scripts/task_engine.py check TASK-001      # Check one task
python3 scripts/task_engine.py check --quiet       # Minimal output for cron
python3 scripts/task_engine.py check --json        # Machine-readable JSON
python3 scripts/task_engine.py check --discord     # Discord-formatted digest
```

### 归档已完成的任务

```bash
python3 scripts/task_engine.py archive TASK-001 --json    # Only works on terminal tasks
```

### 自动分配任务

系统会自动扫描所有子任务，并将状态为 “READY”的子任务分配给合适的代理：
```bash
python3 scripts/task_engine.py auto-dispatch TASK-001             # Dispatch ready subtasks
python3 scripts/task_engine.py auto-dispatch TASK-001 --dry-run   # Preview without acting
python3 scripts/task_engine.py auto-dispatch --all                # All active tasks
python3 scripts/task_engine.py auto-dispatch TASK-001 --subtask subtask_02  # Specific subtask
python3 scripts/task_engine.py auto-dispatch TASK-001 --subtask subtask_01 --show-context  # View dispatch context
```

命令的输出结果总是 JSON 格式，其中包含 `dispatches` 和 `skipped` 两个数组。

### 通知（使用 Discord 格式）

该引擎能够生成符合 Discord 格式的通知消息：
```bash
python3 scripts/task_engine.py notify digest               # Full heartbeat digest
python3 scripts/task_engine.py notify TASK-001 created     # Task creation message
python3 scripts/task_engine.py notify TASK-001 status      # Status update with progress
python3 scripts/task_engine.py notify TASK-001 transition   # Last transition
python3 scripts/task_engine.py notify TASK-001 completed    # Completion summary
python3 scripts/task_engine.py notify TASK-001 alert --type stuck --subtask-id subtask_01
```

### 重建索引（用于恢复）

如果 `index.json` 文件损坏，系统会重新生成该文件：
```bash
python3 scripts/task_engine.py rebuild-index         # Scan and rebuild
python3 scripts/task_engine.py rebuild-index --json  # Machine-readable output
```

## 心跳信号集成

在心跳信号的 `cmd_beat()` 函数中添加第 4.3 步骤（在检查 `ongoing.json` 文件之后执行）：
```python
# 4.3 Task Engine check
logger.info("[4.3/8] Task Engine check")
try:
    import sys
    sys.path.insert(0, str(Path("/home/zeron/.openclaw/workspace/skills/task-engine/scripts")))
    from engine.checker import check_all_tasks
    te_result = check_all_tasks()
    if te_result.get("alerts"):
        alerts.extend(te_result["alerts"])
        all_ok = False
    if te_result.get("summary"):
        logger.info("  Tasks: %s", te_result["summary"])
except ImportError:
    logger.debug("  Task engine not installed, skipping")
except Exception as e:
    logger.warning("  Task engine check failed: %s", e)
```

这个检查过程的开销很低（每个心跳信号大约消耗 300-500 个令牌，适用于 1-3 个活跃任务）。系统首先读取 `index.json` 文件，然后仅加载活跃任务的子任务文件。

## 状态机

```
PLANNING ──approve──> APPROVED ──start──> IN_PROGRESS ──test──> TESTING ──review──> REVIEW ──complete──> COMPLETED
    │                                         │  │                 │  │                │
    │reject                              block│  │fail        reopen│  │fail       reopen│ fail
    v                                         v  v                 v  v                v   v
 REJECTED                                BLOCKED FAILED      IN_PROGRESS FAILED   IN_PROGRESS FAILED
                                           │
                                      unblock│
                                           v
                                      IN_PROGRESS
```

任务的状态有三种：COMPLETED（已完成）、FAILED（失败）和 REJECTED（被拒绝）。完整的状态转换规则请参阅 `references/state-transitions.md`。

### 子任务的状态

```
PENDING -> ASSIGNED -> IN_PROGRESS -> DONE
                │            │
                │block       │fail / block
                v            v
             BLOCKED      FAILED / BLOCKED
```

### 自动状态转换（由心跳信号触发）

| 条件 | 动作 |
|---------|--------|
| 所有类型为 “dev”的子任务已完成 | 任务状态变为 “TESTING”（测试中） |
| 所有类型为 “test”的子任务已完成 | 任务状态变为 “REVIEW”（审核中） |
| 首个子任务被分配给代理执行 | 任务状态变为 “IN_PROGRESS”（进行中） |
| 有任何子任务失败 | 发出警报，需要人工干预 |
| 子任务连续 3 次未收到心跳信号 | 通过 Discord 发出警报 |
| 任务超过截止时间 | 发出逾期警报 |

## Discord 格式化

`discord_formatter.py` 模块用于生成符合 Discord 格式的通知消息。所有格式化操作都是通过纯字符串实现的，不涉及任何 API 调用。

可用的通知格式包括：
- **任务创建**：包含任务优先级和计划的公告
- **状态更新**：显示进度条和子任务结构
- **状态转换**：用表情符号表示状态变化
- **警报**：针对卡住、逾期或失败的任务发出紧急通知
- **完成总结**：包含子任务结果的最终报告
- **心跳摘要**：所有活跃任务的完整概要

进度条的显示格式为：`[████░░░░░░] 40%`

## 代理能力

| 代理 | 关键参数 | 适用场景 | 最大并行处理能力 |
|-------|---------|----------------|----------------------|
| Claude Code | `claude-code` | 开发、重构、调试、文档编写 | 3 |
| Eva | `eva` | 测试、验证、系统操作 | 1 |

代理选择优先级如下：
1. 首选代理（如果已指定且具备相应能力）
2. 根据预设的 `preferred_types` 进行匹配
3. 根据代理的通用能力进行匹配
4. 在没有合适代理时默认使用 Eva

详细信息请参阅 `references/agent-capabilities.md`。

## 故障排除

### `index.json` 文件损坏

```bash
python3 scripts/task_engine.py rebuild-index --json
```

系统会扫描所有 `tasks/TASK-*/task.json` 文件，并重建索引。无效或无法读取的文件将被忽略。

### 常见错误

| 错误类型 | 原因 | 解决方法 |
|---------|---------|-------------------|
| “Invalid transition: X + ‘event’” | 当前状态不允许进行该状态转换 | 请查阅 `references/state-transitions.md` |
| “Task TASK-XXX not found” | 任务不存在或已被归档 | 请检查 `tasks/` 和 `tasks/archive/` 目录 |
| “Cannot archive: not terminal” | 任务必须处于 COMPLETED/FAILED/REJECTED 状态 | 需先将任务状态转换为终端状态（COMPLETED/FAILED/REJECTED） |
| “Agent at capacity” | 代理已达到最大并行处理能力 | 等待正在执行的子任务完成 |
| “Dependency not DONE” | 由于某个子任务未完成而导致任务无法继续执行 | 需先完成该阻塞子任务 |

### JSON 解析错误

该引擎能够优雅地处理损坏的 JSON 文件：
- 在检查任务进度时：跳过无效的文件，并记录警告信息，然后继续执行后续操作
- 在重建索引时：跳过无法读取的文件，并在输出中报告错误信息
- 所有 CLI 命令都会捕获异常，并返回清晰的错误信息（而非详细的错误堆栈）

## 数据存储位置

- 任务文件：`/home/zeron/.openclaw/workspace/tasks/TASK-NNN/`
- 索引文件：`/home/zeron/.openclaw/workspace/tasks/index.json`
- 归档文件：`/home/zeron/.openclaw/workspace/tasks/archive/`
- 配置文件：`/home/zeron/.openclaw/workspace/skills/task-engine/config/settings.yaml`
- 代理信息：`/home/zeron/.openclaw/workspace/skills/task-engine/references/agent-capabilities.md`
- 状态转换规则：`/home/zeron/.openclaw/workspace/skills/task-engine/references/state-transitions.md`