---
name: uptime-monitor
description: 24/7 全天候运行的 OpenClaw 监控系统：每隔 5 分钟会通过 cron 任务发送一次 ping 请求。如果系统出现故障，会生成 `dead.json` 文件；如果系统连续运行 7 天（168 小时）无故障，则会生成 `uptime.json` 文件。该系统适用于需要设置持续监控的场景（如 cron 任务配置、故障记录跟踪、状态文件管理等）。
---

# 运行时间监控器

这是一个全天候运行的监控工具：它会持续检查 OpenClaw/Gateway 的运行状态，并将结果记录在 `alive → dead.json` 或 `uptime.json` 文件中（`uptime.json` 文件会记录连续运行 7 天的情况）。这些文件存储在 `workspace/uptime` 目录下。

## 快速设置（一次性配置）

## 工作流程（在“UPTIME CHECK”事件触发时自动执行）
1. **发送 Ping 请求**：通过 `exec` 命令检查 `session_status` 和 OpenClaw Gateway 的状态。
2. **成功**：更新 `uptime/streak.json` 文件，将运行时间增加 5 分钟或 1 小时。如果运行时间达到 168 小时，将结果写入 `uptime/uptime.json` 文件。
3. **失败**：将运行状态记录在 `uptime/dead.json` 文件中，包括当前时间 (`ts`) 和故障开始时间 (`downtime_start`)。
4. **目录管理**：自动创建 `uptime/` 目录。

**运行时间记录重置**：当检测到故障时，将运行时间记录重置为 0。

## 相关文件（存储在 `workspace/uptime` 目录下）
- `streak.json`：包含运行时间记录（例如：`{"streak_hours": 24.5, "last_ping": 1738746800000}`）
- `uptime.json`：包含运行时间记录和验证状态（例如：`{"streak_hours": 168.1, "verified": true, "end_ts": 1738746800000}`，表示已连续运行 7 天以上）
- `dead.json`：包含故障记录（例如：`{"ts": 1738746800000, "downtime_start": 1738746800000}`）

## 异常处理规则
- **首次运行时**：运行时间记录为 0。
- **Cron 任务失败时**：运行时间记录保持不变（不会错误地标记为“故障状态”。
- **手动触发时**：可以手动发送 `message "UPTIME CHECK 👻"` 来触发监控。

该工具不生成任何警报或依赖关系信息，仅通过文件记录运行状态。在生产环境中，该脚本会持续运行（由 Cron 任务定期执行）。

## 可选脚本（手动执行）
`scripts/uptime-check.js`：这是一个独立的 Node.js 脚本，用于手动或通过 Cron 任务触发运行时间检查。

在生产环境中，该脚本会通过 Cron 任务自动执行，并保持静默运行状态。