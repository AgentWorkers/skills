# daily-digest 技能

**用途：** 从内存中提取数据并生成每日摘要，这些数据会被保存为 `digest/digest-YYYY-MM-DD.md` 文件。

**使用方法：**
- 运行 `digest_daily.py` 脚本以生成当天的摘要。
- 可选：通过 Cron 作业或调度器将脚本与 `clawdbot` 集成，实现自动运行。

**注意事项：**
- 该脚本会读取 `memory/YYYY-MM-DD.md` 文件（以及可选的昨天的 `memory/YYYY-MM-DD.md` 文件），从中提取决策、经验教训、行动内容及相关问题。
- 当内存中不存在结构化的条目时，脚本会提供一个占位符形式的摘要。