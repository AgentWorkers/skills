---
name: session-hygiene
description: >
  **防止 sessions.json 文件因孤立会话（如钩子、定时任务、子代理）而变得臃肿**  
  该机制通过设置定时任务来定期将过时的会话数据归档到每日更新的 JSONL 文件中，从而保持 sessions.json 文件的简洁性。适用于以下情况：  
  - sessions.json 文件体积过大；  
  - 网关运行缓慢或响应迟缓；  
  - 需要对包含钩子或定时任务的 OpenClaw 实例进行预防性维护。  
  该功能与 openclaw#15225 问题相关。
---
# 会话管理（Session Management）

OpenClaw 的会话存储文件（`sessions.json`）会不断增长——每个钩子（hook）、定时任务（cron）或子代理（subagent）的调用都会创建一个新的会话条目，而这些条目永远不会被清除。在复杂的部署环境中（例如同时使用大量 Webhook 和定时任务），`sessions.json` 的文件大小可能迅速超过 200MB，会话数量可能超过 7000 个，从而导致系统响应变慢或完全无法响应。

本技能提供了自动归档和轮换机制，以保持 `sessions.json` 文件的大小在可控范围内，同时仍能保留会话历史记录。

## 快速设置

创建一个每 6 小时运行一次的定时任务：

```javascript
cron(action: "add", job: {
  name: "Session Archive & Cleanup",
  schedule: { kind: "cron", expr: "0 */6 * * *", tz: "America/Los_Angeles" },
  sessionTarget: "isolated",
  payload: {
    kind: "agentTurn",
    message: "Archive and clean up stale sessions. Run the script: python3 <skill-dir>/scripts/archive_sessions.py",
    timeoutSeconds: 60
  },
  delivery: { mode: "announce", channel: "slack" }
})
```

请根据您的实际环境调整时区和数据传输渠道。

## 功能说明

1. **归档**：超过 48 小时的会话会被移动到 `sessions-archive/YYYY-MM-DD.jsonl` 文件中（每个会话占一行，按日期分组）。
2. **保留关键会话**：`agent:main:main` 类型的会话永远不会被删除。
3. **轮换**：超过 30 天的归档文件会被删除。
4. **报告**：会显示归档的会话数量、剩余的会话数量以及各文件的大小。

## 手动执行

- **立即清理**：如果 `sessions.json` 文件已经变得非常庞大，可以使用以下命令进行清理：
   ```bash
python3 <skill-dir>/scripts/archive_sessions.py
```

- **批量删除指定时间内的会话**：可以使用以下命令一次性删除所有超过 N 小时的会话：
   ```bash
python3 <skill-dir>/scripts/archive_sessions.py --max-age-hours 1
```

## 配置参数

| 参数          | 默认值         | 说明                |
|---------------|--------------|----------------------|
| `--max-age-hours` | 48           | 归档前的会话保留时间（小时）         |
| `--archive-retention-days` | 30           | 归档文件的保留天数            |
| `--sessions-path` | 自动检测       | `sessions.json` 文件的路径           |
| `--dry-run`     | off           | 预览归档结果（不实际执行任何操作）       |

## 规模估算

| 每天会话数量 | 会话保留时间（48 小时） | `sessions.json` 文件大小 |
|-------------|-----------------|-------------------|
| 50           | 约 100 个会话       | 约 3MB                 |
| 100           | 约 200 个会话       | 约 6MB                 |
| 200           | 约 400 个会话       | 约 12MB                 |

如果不使用此技能，同样的配置在一个月内文件大小可能会超过 200MB。