---
name: cron-retry
description: 当 cron 作业因网络错误而失败时，系统会自动尝试重试。该功能在网络连接恢复后触发，确保失败的作业能够被重新执行。该系统与心跳检测机制（heartbeat detection）集成，用于识别失败的作业并自动重新运行它们。
---

# Cron 任务重试功能

自动检测并重试因网络/连接问题而失败的 Cron 任务。

## 快速入门（与 Heartbeat 功能集成）

将以下代码添加到您的 `HEARTBEAT.md` 文件中：

```markdown
## Cron Recovery Check
Check for cron jobs with lastStatus: "error". If the error matches network patterns (connection error, sendMessage failed, fetch failed, ETIMEDOUT, ECONNREFUSED), retry the job using cron tool with action: "run" and the job ID. Report what was recovered.
```

完成以上操作后，每次系统发送 Heartbeat 信号时，失败的 Cron 任务将自动被重试。

## 工作原理

1. 在每次发送 Heartbeat 信号时，通过 `cron list` 命令检查所有 Cron 任务。
2. 筛选出 `lastStatus` 为 “error” 且 `enabled` 为 “true”的任务。
3. 检查 `lastError` 是否与网络错误相关的提示信息相匹配。
4. 使用 `cron run` 命令重新运行符合条件的任务。
5. 报告重试结果。

## 可重试的网络错误类型

以下错误表明存在短暂的网络问题，可以尝试重试：

- `Network request.*failed`
- `Connection error`
- `ECONNREFUSED`
- `ETIMEDOUT`
- `ENOTFOUND`
- `sendMessage.*failed`
- `fetch failed`
- `socket hang up`

## 重试与跳过的任务类型

**会被重试的任务：**
- 网络超时
- 连接被拒绝
- 发送消息失败
- DNS 查询失败

**不会被重试的任务：**
- 逻辑错误（配置错误、数据缺失）
- 认证失败
- 被禁用的任务
- 已成功执行的任务

## 手动恢复检查

若需手动检查和重试失败的 Cron 任务，请执行以下操作：

```bash
# List all jobs and their status
clawdbot cron list

# Find failed jobs
clawdbot cron list | jq '.jobs[] | select(.state.lastStatus == "error") | {name, error: .state.lastError}'

# Retry a specific job
clawdbot cron run --id <JOB_ID>
```

## 代理实现方式

在实现 Heartbeat 检查功能时，请参考以下代码示例：

```
1. Call cron tool with action: "list"
2. For each job in response.jobs:
   - Skip if job.enabled !== true
   - Skip if job.state.lastStatus !== "error"
   - Check if job.state.lastError matches network patterns
   - If retryable: call cron tool with action: "run", jobId: job.id
3. Report: "Recovered X jobs" or "No failed jobs to recover"
```

## 示例场景

1. **晚上 7:00**：晚上简报的 Cron 任务被触发。
2. **网络中断**：发送到 Telegram 的消息失败。
3. 任务的状态被标记为 `lastStatus: "error"`，`lastError: "Network request for 'sendMessage' failed!"`。
4. **晚上 7:15**：网络恢复，系统再次发送 Heartbeat 信号。
5. 该功能检测到任务失败，并判断为网络错误。
6. 任务被重试，简报成功发送。
7. 报告：**成功恢复 1 个任务：晚上简报**。

## 安全性注意事项

- 仅重试短暂的网络错误。
- 保留任务的启用状态。
- 避免无限重试（通过 `lastRunAtMs` 参数进行控制）。
- 报告所有的恢复尝试情况。