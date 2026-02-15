---
name: ralph-operations
description: **使用场景：**  
在管理 Ralph 协调循环、分析诊断数据、调试帽子选择（hat selection，具体含义需结合上下文确定）、排查背压（backpressure）问题或进行事后分析（post-mortem analysis）时使用。
tags: [loops, diagnostics, debugging, analysis]
---

# Ralph 操作

用于管理、监控和诊断 Ralph 的编排循环。

## 循环管理

### 快速参考

| 任务 | 命令 |
|------|---------|
| 列出活动中的循环 | `ralph loops` |
| 列出所有循环（包括已合并的） | `ralph loops --all` |
| 查看循环变更 | `ralph loops diff <id>` |
| 查看循环日志 | `ralph loops logs <id>` |
| 实时查看日志 | `ralph loops logs <id> -f` |
| 停止运行循环 | `ralph loops stop <id>` |
| 合并已完成的循环 | `ralph loops merge <id>` |
| 重试失败的合并 | `ralph loops retry <id>` |
| 放弃循环 | `ralph loops discard <id>` |
| 清理无效的进程 | `ralph loops prune` |

**循环 ID 格式：** 部分匹配有效 - `a3f2` 与 `loop-20250124-143052-a3f2` 匹配

### 循环状态

| 状态 | 颜色 | 含义 |
|--------|-------|---------|
| 运行中 | 绿色 | 循环正在执行中 |
| 排队中 | 蓝色 | 合并已完成，等待合并 |
| 合并中 | 黄色 | 合并正在进行中 |
| 需要审核 | 红色 | 合并失败，需要干预 |
| 已合并 | 淡色 | 成功合并（使用 `--all` 命令） |
| 被放弃 | 淡色 | 被放弃（使用 `--all` 命令） |

### 启动与停止

循环通过 `ralph run` 自动启动：
- **主循环**：在主工作区运行，保存在 `.ralph/loop.lock` 文件中 |
- **工作树循环**：在主循环运行时创建，保存在 `.worktrees/<loop-id>/` 目录中 |

```bash
ralph loops                       # Any loops running?
cat .ralph/loop.lock 2>/dev/null  # Primary loop details
ralph loops stop <id>             # Graceful stop
ralph loops stop <id> --force     # Immediate stop
ralph loops discard <id>          # Abandon + clean worktree
```

### 检查循环

```bash
ralph loops diff <id>             # What changed
ralph loops logs <id> -f          # Live event log
ralph loops history <id>          # State changes
ralph loops attach <id>           # Shell into worktree
```

**工作树上下文文件**（`.worktrees/<loop-id>/`）：

| 文件 | 内容 |
|------|----------|
| `.ralph/events.jsonl` | 事件流：帽子选择、迭代次数、工具调用 |
| `.ralph/agent/summary.md` | 当前会话摘要 |
| `.ralph/agent/handoff.md` | 下一次迭代的交接信息 |
| `.ralph/agent/scratchpad.md` | 工作笔记 |
| `.ralph/agent/tasks.jsonl` | 运行时任务状态 |

**主循环** 使用仓库根目录下的 `.ralph/agent/` 目录中的相同文件。

### 合并队列

流程：`排队 → 合并 → 已合并` 或 `→ 需要审核 → 重新尝试合并` 或 `→ 被放弃`

```bash
ralph loops merge <id>            # Queue for merge
ralph loops process               # Process pending merges now
ralph loops retry <id>            # Retry failed merge
```

**读取状态：**
```bash
jq -r '.prompt' .ralph/loop.lock 2>/dev/null
tail -20 .ralph/merge-queue.jsonl | jq .
```

---

## 诊断

### 启用诊断功能

```bash
RALPH_DIAGNOSTICS=1 ralph run -p "your prompt"
```

禁用时不会产生任何开销。输出文件：`.ralph/diagnostics/<YYYY-MM-DDTHH-MM-SS>/`

### 会话发现

```bash
LATEST=$(ls -t .ralph/diagnostics/ | head -1)
SESSION=".ralph/diagnostics/$LATEST"
```

### 文件参考

| 文件 | 包含内容 | 关键字段 |
|------|----------|------------|
| `agent-output.jsonl` | 代理文本、工具调用、结果 | `type`, `iteration`, `hat` |
| `orchestration.jsonl` | 帽子选择、事件、背压信息 | `event.type`, `iteration`, `hat` |
| `performance.jsonl` | 性能数据、延迟、令牌计数 | `metric.type`, `iteration`, `hat` |
| `errors.jsonl` | 解析错误、验证失败信息 | `error_type`, `message`, `context` |
| `trace.jsonl` | 带有元数据的所有跟踪日志 | `level`, `target`, `message` |

### 诊断工作流程

**1. 先查看错误信息：**
```bash
wc -l "$SESSION/errors.jsonl"
jq '.' "$SESSION/errors.jsonl"
jq -s 'group_by(.error_type) | map({type: .[0].error_type, count: length})' "$SESSION/errors.jsonl"
```

**2. 查看编排流程：**
```bash
jq '{iter: .iteration, hat: .hat, event: .event.type}' "$SESSION/orchestration.jsonl"
jq 'select(.event.type == "hat_selected") | {iter: .iteration, hat: .event.hat, reason: .event.reason}' "$SESSION/orchestration.jsonl"
jq 'select(.event.type == "backpressure_triggered") | {iter: .iteration, reason: .event.reason}' "$SESSION/orchestration.jsonl"
```

**3. 代理活动：**
```bash
jq 'select(.type == "tool_call") | {iter: .iteration, tool: .name}' "$SESSION/agent-output.jsonl"
jq -s '[.[] | select(.type == "tool_call")] | group_by(.iteration) | map({iter: .[0].iteration, tools: [.[].name]})' "$SESSION/agent-output.jsonl"
```

**4. 性能分析：**
```bash
jq 'select(.metric.type == "iteration_duration") | {iter: .iteration, ms: .metric.duration_ms}' "$SESSION/performance.jsonl"
jq -s '[.[] | select(.metric.type == "token_count")] | {total_in: (map(.metric.input) | add), total_out: (map(.metric.output) | add)}' "$SESSION/performance.jsonl"
```

**5. 跟踪日志：**
```bash
jq 'select(.level == "ERROR" or .level == "WARN")' "$SESSION/trace.jsonl"
```

### 快速健康检查

```bash
SESSION=".ralph/diagnostics/$(ls -t .ralph/diagnostics/ | head -1)"
echo "=== Session: $SESSION ==="
echo -e "\n--- Errors ---"
wc -l < "$SESSION/errors.jsonl" 2>/dev/null || echo "0"
echo -e "\n--- Iterations ---"
jq -s 'map(select(.event.type == "iteration_started")) | length' "$SESSION/orchestration.jsonl"
echo -e "\n--- Hats Used ---"
jq -s '[.[] | select(.event.type == "hat_selected") | .event.hat] | unique' "$SESSION/orchestration.jsonl"
echo -e "\n--- Backpressure Count ---"
jq -s 'map(select(.event.type == "backpressure_triggered")) | length' "$SESSION/orchestration.jsonl"
echo -e "\n--- Termination ---"
jq 'select(.event.type == "loop_terminated")' "$SESSION/orchestration.jsonl"
```

---

## 故障排除

### 无效的进程
使用 `ralph loops` 查看未运行的循环 → 使用 `ralph loops prune` 清理这些进程

### 孤立的 worktree
如果 `.worktrees/` 目录不在 `ralph loops` 列表中 → 使用 `ralph loops prune` 或 `git worktree remove .worktrees/<id> --force` 删除这些目录

### 合并冲突
循环卡在 “需要审核” 状态：
1. 使用 `ralph loops diff <id>` 查看冲突的更改 |
2. 使用 `ralph loops attach <id>` 手动解决冲突，然后提交并重试 |
3. 如果不值得修复，使用 `ralph loops discard <id>` 放弃该循环

### 锁定问题
如果显示 “循环已经在运行”，但实际上没有任何活动 → 删除 `.ralph/loop.lock` 文件（如果相关进程已终止则安全操作）

### 代理在循环中卡住
**警告信号：** 多次迭代但事件很少 = 代理未能取得进展。

### 合并过程卡住
如果合并过程卡住：
1. 使用 `ralph loops diff <id>` 查看冲突内容 |
2. 手动解决冲突后提交更改 |
3. 如果问题无法解决，使用 `ralph loops discard <id>` 放弃该循环

### worktree 损坏
```bash
git worktree repair
ralph loops prune
```

### 清理
```bash
ralph clean --diagnostics              # Delete all sessions
ralph clean --diagnostics --dry-run    # Preview deletions
```