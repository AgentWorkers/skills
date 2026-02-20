# 监控功能

OpenClaw 的系统健康监控功能可追踪令牌使用情况、任务成功率、Cron任务的运行状态以及各项技能的使用情况。

## 命令
```
monitor status                                          # Health summary
monitor tokens [--period 7d|30d] [--by model|skill]    # Token report
monitor crons                                           # Cron health
monitor tasks [--failed]                                # Task history
monitor cost [--period month|week]                      # Cost breakdown
monitor ingest token|task|cron                          # Manual ingestion
monitor aggregate [--date YYYY-MM-DD]                   # Daily aggregates
monitor refresh                                         # Regenerate interchange
monitor backup [--output path]                          # Backup DB
monitor restore <file>                                  # Restore DB
```

## 相关文档
- `ops/capabilities.md` — 命令参考（可共享）
- `ops/health.md` — 仅包含状态指标（可共享，不涉及费用/令牌）
- `state/status.md` — 完整的详细状态信息（仅限内部使用）
- `state/token-spend.md` — 令牌使用及费用明细（仅限内部使用）