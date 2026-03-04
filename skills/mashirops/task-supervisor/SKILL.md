---
name: task-supervisor
description: Self-supervising long-running task manager with progress tracking and periodic status reports. Only activate for LARGE tasks — do NOT activate for quick or simple tasks. Activate when ALL of these are true: (1) Task has 5+ distinct steps OR estimated time >20 minutes, AND (2) at least one of: user says "take your time / do this overnight / finish by yourself / keep me posted", task requires sub-agents or cron jobs, task spans multiple tool calls across different domains (e.g. research + write + deploy). Do NOT activate for: single-step requests, quick searches, short code edits, simple Q&A, file reads, summarization of one document.
---

# 任务监督器

用于管理长时间运行的任务，包括设置检查点、生成进度文件以及定期通过 WhatsApp 发送任务进度报告。

## 这是一个大型任务吗？

在采取任何行动之前，先在心中判断一下：

| 任务特征 | 是否属于大型任务？ |
|--------|--------|
| 步骤数量 ≥ 5 或任务耗时 > 20 分钟 | ✅ 是 |
| 用户要求“慢慢来”/“隔夜完成”/“随时告知进度” | ✅ 是 |
| 需要子代理、定时任务（cron）以及处理多个域名 | ✅ 是 |
| 仅涉及单一工具调用、简单搜索、少量编辑或问答 | ❌ 否 — 可完全跳过此任务 |
| “帮我编写文档”（一次性完成） | ❌ 否 |
| “查找信息并总结”（几分钟内完成） | ❌ 否 |

如果任务不属于大型任务 → 按常规流程处理，直接跳过相关任务文件和定时任务设置。

## 任务开始时

收到大型任务后，立即执行以下操作：

1. 在 `.tasks/<任务名称>.md` 文件中创建任务文件（文件名使用驼峰式命名法）。
2. 将任务分解为多个步骤，并为每个步骤编号。
3. 启动一个定时任务（cron），用于定期发送任务进度更新。
4. 开始执行任务，并在每完成一个步骤后更新任务文件。

### 任务文件格式

```markdown
# Task: <Title>

**Started**: <ISO timestamp>
**Status**: in_progress | paused | done | failed
**Estimated Steps**: N
**Last Updated**: <ISO timestamp>

## Steps

- [ ] 1. First step
- [ ] 2. Second step
- [x] 3. Completed step ✓ (2026-03-02T22:05:00+08:00)
- [!] 4. Failed step — <error summary>

## Log

### Step 3 — 2026-03-02T22:05:00+08:00
Result or notes here.

### Error — 2026-03-02T22:07:00+08:00
What failed and how it was handled.

## Result

(Fill when done — final summary for the user)
```

## 任务执行过程中

在每完成一个步骤后（无论成功还是失败）：
- 更新步骤列表中的复选框状态（`[x]` 表示已完成，`[!]` 表示失败）。
- 添加一条包含时间戳和关键发现内容的日志记录。
- 更新文件的 `Last Updated` 时间戳。

如果任务失败：
- 将对应的步骤标记为 `[!]` 并附上错误原因。
- 如果有明显的解决方法，尝试其他方法。
- 如果确实遇到困难，将任务状态设置为 `paused`（暂停），并记录需要解决的问题。

## 进度报告（定时任务）

任务开始时，使用 `exec` 命令启动定时任务来发送进度报告：

```bash
openclaw cron add "task-report-<SLUG>" \
  --schedule "*/15 * * * *" \
  --message "Read .tasks/<SLUG>.md and send a Feishu message to the user with progress update. Include: completed steps, current step, blockers if any. Keep it under 5 sentences. Remove this cron when Status=done or Status=failed." \
  --once-complete
```

根据任务复杂程度调整定时任务的发送间隔：
- 简单任务（<30 分钟）：每 10 分钟发送一次报告。
- 中等复杂度任务（30 分钟–2 小时）：每 15 分钟发送一次报告。
- 复杂任务（>2 小时）：每 30 分钟发送一次报告。

## 任务完成时

1. 在文件中填写 `## 结果` 部分，提供任务完成的详细总结。
2. 将任务状态设置为 `done`（已完成）。
3. 发送一条 Feishu 消息，内容包括任务名称、已完成的工作以及需要注意的事项。
4. 删除用于发送进度报告的定时任务。

## 任务失败或遇到困难时

1. 将任务状态设置为 `paused`（暂停）。
2. 详细记录已经尝试过的解决方法以及当前遇到的障碍。
3. 立即通过 Feishu 发送警报消息（不要等待定时任务自动触发）。
4. 绝不要默默停止任务执行——必须及时通知相关人员。

## 恢复暂停的任务

当收到继续执行任务的请求时：
1. 读取 `.tasks/<任务名称>.md` 文件。
2. 找到最后一个已完成的步骤。
3. 从该步骤开始继续执行任务。
4. 如有必要，重新启动用于发送进度报告的定时任务。

## 多任务管理

如果同时运行多个任务，请为每个任务分别创建独立的文件。在心跳检测（heartbeat）过程中，检查 `.tasks/` 目录下是否有处于 `in_progress`（进行中）状态的任务，并在心跳响应中简要说明这些任务的当前状态。

## 快速参考

| 情况 | 应采取的行动 |
|-----------|--------|
| 任务被分配 | 创建任务文件、分解任务步骤、启动定时任务 |
| 任务步骤完成 | 更新步骤状态、添加日志记录 |
| 任务步骤失败 | 标记为失败、尝试其他方法、记录错误 |
| 遇到严重困难 | 将任务状态设置为暂停、立即通过 WhatsApp 发送警报 |
| 任务完成 | 填写任务总结、设置状态为已完成、发送最终通知、删除定时任务 |
| 被要求提供更新 | 读取任务文件、总结当前任务状态 |