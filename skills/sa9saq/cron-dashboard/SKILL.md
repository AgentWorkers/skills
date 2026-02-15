---
description: 查看、管理和调试 OpenClaw 的 cron 作业，同时提供作业状态概览和健康检查（即作业是否正常运行的检查）。
---

# Cron 仪表板

一目了然地查看和管理 OpenClaw 的 cron 作业。

## 使用说明

1. **列出所有作业**：
   ```bash
   openclaw cron list
   ```
   以表格形式显示：名称 | 时间表 | 模型 | 状态 | 上次运行时间 | 下次运行时间

2. **作业详情**：`openclaw cron show <id>` — 查看完整配置、最近运行记录及输出日志

3. **健康检查** — 标记问题：
   - ⚠️ 作业未按预期运行（错过时间表）
   - 🔴 连续失败（3次以上）
   - 🟡 时间表失效（对于每小时运行的作业，超过 24 小时未运行）

4. **快速操作**：
   ```bash
   openclaw cron create --name "task" --schedule "*/30 * * * *" --prompt "..."
   openclaw cron pause <id>
   openclaw cron resume <id>
   openclaw cron delete <id>
   ```

5. **仪表板视图**（当请求概览时）：
   ```
   🕐 Cron Dashboard — 5 jobs

   ✅ Active (3)
   | Name          | Schedule    | Last Run      | Next Run      |
   |---------------|-------------|---------------|---------------|
   | email-check   | */30 * * *  | 5 min ago ✅  | in 25 min     |

   ⏸️ Paused (1)
   | backup-daily  | 0 2 * * *   | 2 days ago    | —             |

   🔴 Failing (1)
   | tweet-bot     | 0 9 * * *   | 1h ago ❌     | tomorrow 9:00 |
   ```

## Cron 表达式速查表

| 表达式 | 含义 |
|-----------|---------|
| `*/15 * * * *` | 每 15 分钟运行一次 |
| `0 */2 * * *` | 每 2 小时运行一次 |
| `0 9 * * 1-5` | 工作日早上 9 点运行 |
| `0 2 * * *` | 每天凌晨 2 点运行 |
| `0 0 1 * *` | 每月的第一天运行 |

## 故障排除

- **作业未运行**：检查是否被暂停；使用 `crontab.guru` 验证时间表设置
- **连续失败**：查看 `openclaw cron show <id>` 的错误输出
- **考虑使用心跳检测**：对于需要灵活定时检查的任务，建议使用 HEARTBEAT.md 而不是 cron

## 必备条件

- 已安装并配置 OpenClaw CLI
- 无需 API 密钥