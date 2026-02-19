---
name: agent-sleep
description: 一种受生物机制启发的休息与记忆巩固系统，专为智能代理（Agents）设计。该系统支持周期性的“睡眠”周期，通过这些周期来压缩内存数据、清理冗余信息，并帮助代理反思自身的学习成果（即“洞察”）。
metadata:
  {
    "openclaw":
      {
        "emoji": "🛌",
        "category": "system",
        "schedulable": true
      }
  }
---
# 代理睡眠系统 🛌

就像人类一样，代理也需要“睡眠”（离线维护）来防止内存碎片化和上下文污染。

## 功能

1. **微休眠**：在任务执行过程中快速清理不必要的上下文数据。
2. **深度睡眠**：每晚将日常日志整合到长期存储中。
3. **模拟休眠状态**：在后台进行模拟操作（可选）。

## 工具

### `sleep_check`
检查代理是否处于“疲劳”状态（基于运行时间或令牌使用情况）。
```bash
python3 src/sleep_status.py
```

### `sleep_cycle`
立即触发睡眠周期：
- **轻度睡眠**：压缩最近的日志。
- **深度睡眠**：对日志进行归档并清理临时文件。
```bash
python3 scripts/run_sleep_cycle.py --mode [light|deep]
```

### `sleep_schedule`
设置代理的睡眠周期（通过 Cron 任务实现）。
```bash
python3 src/schedule.py --set "0 3 * * *"  # Sleep at 3 AM
```

## 工作流程

1. **触发睡眠**：Cron 任务在凌晨 3:00 触发睡眠周期。
2. **数据整合**：读取 `memory/YYYY-MM-DD.md` 文件，提取关键信息。
3. **数据更新**：将提取的信息添加到 `MEMORY.md` 文件中。
4. **日志清理**：将原始日志移至 `memory/archive/` 目录。
5. **文件清理**：删除临时文件（如 `*.tmp`、`__pycache__`）。

## 设置要求

1. 确保系统中存在 `memory/` 目录。
2. 运行 `sleep_schedule` 命令以启用自动睡眠功能。