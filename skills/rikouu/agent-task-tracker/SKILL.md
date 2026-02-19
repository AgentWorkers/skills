---
name: task-tracker
description: 主动式任务状态管理。在每个任务开始、进度更新、完成或失败时都会被触发。该系统会记录任务的具体要求、正在运行的进程（包括后台进程和SSH会话）、已经完成的工作以及后续需要执行的操作。即使在会话重置的情况下，也能保持状态信息的完整性。触发方式是自动的，无需用户手动操作。
---
# 任务跟踪器

维护一个实时的任务状态文件，以确保在会话重置或压缩后仍能保留任务的相关信息。

## 状态文件

`memory/tasks.md` — 任务的唯一信息来源。

## 何时更新文件

1. **收到任务** → 添加一条状态为 `🔄 进行中` 的记录。
2. **后台进程启动** → 记录会话 ID、进程 ID（PID）、服务器名称和执行的命令。
3. **任务进度更新** → 更新任务状态或备注。
4. **任务完成** → 标记为 `✅ 完成`，并记录结果或相关链接。
5. **任务失败** → 标记为 `❌ 失败`，并记录错误信息。
6. **会话开始** → 读取 `memory/tasks.md` 以恢复对任务状态的认知。

## 格式

```markdown
# Active Tasks

## [task-id] Short description
- **Status**: 🔄 进行中 | ✅ 完成 | ❌ 失败 | ⏸️ 暂停
- **Requested**: YYYY-MM-DD HH:MM
- **Updated**: YYYY-MM-DD HH:MM
- **Background**: session-id (PID) on server-name — `command`
- **Notes**: progress details, partial results
- **Result**: final output, links, summary

# Completed (recent)
<!-- Move completed tasks here, keep last 10, prune older -->
```

## 规则

- 在向用户报告任务状态之前，必须先更新文件（先写后读）。
- 提供足够的详细信息，以便无需之前的对话记录即可理解任务状态。
- 对于后台进程：务必记录会话 ID、服务器名称和执行的命令。
- 对于多步骤任务：在每个步骤完成后更新文件。
- 保持文件简洁——这不是日志文件，而是一个任务状态的快照。
- **文件大小限制**：控制在 50 行以内（约 2KB）——每次会话开始时都会读取该文件。
- 已完成的任务：简化为一行摘要，详细信息可参考每日记录。
- 删除超过 3 天的已完成任务。
- 如果 `Active` 列为空，应写入 “无” 以明确表示当前没有活跃任务。