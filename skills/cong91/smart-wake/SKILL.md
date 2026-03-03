---
name: smart-wake
version: 1.0.0
owner: platform-team
description: 通过检查点（checkpoint）、定时任务（cron wake）以及会话生成（session spawn）机制来防止子代理（subagent）超时。
---
# 技能：智能唤醒（Smart-Wake）

## 目标
确保在子代理超时发生时，长时间运行的任务不会丢失已取得的进度。

**标准机制：**
1. 在超时前或达到超时阈值时自动保存任务状态。
2. 通过定时任务（Cron）在预定时间重新启动子代理。
3. 使用 `sessions_spawn`（或根据运行时环境选择合适的函数）从最新的检查点恢复任务，并设置正确的 `wakeMode`。

---

## 激活条件
在满足以下任意条件时，使用 `smart-wake`：
- 任务持续时间超过默认的子代理超时时间。
- 需要定期进行轮询（每分钟/每小时）以继续处理任务。
- 多步骤工作流程在执行过程中可能会暂停，但必须能够准确恢复。
- 任务在夜间或非工作时间运行，但仍需要自动继续。

---

## 可用的工具（内置）
- `sessions_spawn` / `session_spawn`（用于创建新的工作会话）
- 门户定时任务（用于安排唤醒事件）
- 内存/存储空间用于保存任务状态（作为检查点）

> 请勿创建新的工具，仅使用现有的机制。

---

## 状态契约（强制要求）
每个任务都必须实现检查点功能，至少包含以下内容：

```json
{
  "task_id": "smartwake_<slug>_<timestamp>",
  "goal": "Final objective",
  "status": "running|waiting|blocked|done|failed",
  "current_step": "step_name",
  "progress_pct": 0,
  "last_completed": ["step_a", "step_b"],
  "next_actions": ["action_1", "action_2"],
  "artifacts": ["path/file1", "path/file2"],
  "errors": [],
  "retry_count": 0,
  "updated_at": "ISO_TIMESTAMP"
}
```

**要求：**
- 每完成一个步骤后更新检查点。
- 在超时前生成最终检查点。
- 恢复任务时始终读取最新的检查点；切勿盲目重新运行任务。

---

## 标准工作流程

### 第1步 — 预估超时时间
- 确定子代理的超时时间和任务的总持续时间。
- 如果 `estimated_duration > 70%` 超时时间：立即启用 `smart-wake`。
- 生成 `task_id` 并创建初始检查点。

### 第2步 — 分阶段执行任务
- 将任务划分为5–15分钟的小部分。
- 对于每个小部分：
  - 将进度写入检查点，
  - 记录生成的成果文件或路径，
  - 更新 `next_actions`（下一步操作）。

### 第3步 — 超时前自动保存状态
- 当剩余超时时间约为10–20%时：
  - 提交最终检查点，
  - 将状态设置为 `waiting`（等待中），
  - 准备恢复任务所需的参数（`task_id` 和 `next_actions`）。

### 第4步 — 安排定时任务唤醒
- 注册一个定时任务，在适当的时间间隔（例如2–10分钟，具体取决于系统负载）唤醒子代理。
- 定时任务发送的参数必须包含：
  - `task_id`
  - `resume_from=latest_checkpoint`（从最新检查点恢复）
  - `reason=timeout_recovery`（超时恢复）

### 第5步 — 启动恢复会话
- 在定时任务唤醒子代理时，调用 `sessionsspawn`（或相应的函数），并设置 `wakeMode` 以支持自动恢复。
- 传递必要的上下文信息：
  - 任务目标，
  - 最新的检查点，
  - 下一步操作，
  - 完成任务的条件。

### 第6步 — 恢复任务并确保幂等性
- 新启动的会话必须：
  1. 读取检查点内容，
  2. 确认生成的成果文件存在，
  3. 跳过已经完成的部分，
  4. 严格按照 `next_actions` 继续执行任务。
- 当任务全部完成后，将状态设置为 `done`（已完成），并取消剩余的定时任务。

---

## 恢复任务的示例数据包（参考）

```json
{
  "task": "Resume long-running task",
  "task_id": "smartwake_repo_scan_20260301T120000Z",
  "wakeMode": "cron",
  "resume": {
    "from": "latest_checkpoint",
    "current_step": "collect_phase_2",
    "next_actions": ["fetch page 6-10", "dedupe", "export report"]
  },
  "done_criteria": [
    "output file generated",
    "validation passed",
    "status marked done"
  ]
}
```

> 注意：字段名称可能因门户或 OpenClaw 的版本而有所不同，但检查点、`wakeMode` 和恢复任务所需的上下文信息是强制性的。

---

## 运行规则
1. **没有有效的检查点，切勿尝试恢复任务。**
2. 在没有校验文件完整性或时间戳的情况下，切勿覆盖已生成的成果文件。
3. 避免无限循环的唤醒操作：限制重试次数（例如最多5次）。
4. 每次唤醒操作都必须有明确的原因（如 `timeout_recovery`、`dependency_ready`、`scheduled_progress`）。
5. 完成任务后，必须清理相关的定时任务。

---

## 每次唤醒后的输出格式

```json
{
  "task_id": "smartwake_<...>",
  "status": "running|waiting|done|failed",
  "progress_pct": 65,
  "current_step": "...",
  "resumed_from_checkpoint": true,
  "next_wake_scheduled": true,
  "next_wake_at": "ISO_TIMESTAMP|null",
  "notes": "concise, auditable"
}
```

---

## 禁止的做法
- 不进行定期检查点检查就运行长时间的任务。
- 在唤醒子代理时未传递 `task_id` 或恢复任务所需的上下文信息。
- 仅因为缺少一个步骤就重新运行整个任务流程。
- 完成任务后不取消相关的定时任务。

---

## 预期结果
- 子代理超时时不会丢失任务进度。
- 通过定时任务，长时间运行的任务能够稳定地继续执行。
- 系统具有完整的可审计性：检查点 → 唤醒 → 恢复 → 完成。