---
name: table-mountain-status
description: 通过官方天气API获取并报告Table Mountain空中缆车的运行状态。当负责人要求获取“Tafelberg”缆车的最新信息、需要关于缆车开放/关闭的警报，或者希望接收关于缆车状态、天气及等待时间的自动化Telegram通知时，可使用此功能。
---

# Table Mountain 状态信息

## 概述
该技能会调用 Table Mountain 官方缆车 API（`https://cms.tablemountain.net/.../weather-api`），解析状态/天气数据，并提供清晰的摘要（文本或 JSON 格式）。非常适合用于即时查询（例如：“Table Mountain 的状态如何？”）以及需要通过 Telegram 通知进行自动轮询的任务。

## 快速入门
1. **手动查询**
   ```bash
   python3 skills/table-mountain-status/scripts/fetch_status.py \
     --output data/table-mountain/$(date +%F_%H%M).txt
   ```
   查询结果会同时显示在文件中和终端中。
2. **用于进一步处理的 JSON 数据**
   ```bash
   python3 skills/table-mountain-status/scripts/fetch_status.py \
     --format json --output data/table-mountain/$(date +%F).json
   ```

3. **包含在脚本中的字段**：`statusType`、`status`、`temperature`、`visibility`、`wind`、`firstUp`、`lastUp`、`lastDown`、`waitingTimeBottom`、`waitingTimeTop`、`lastUpdated`。

## 自动化的 Telegram 通知
1. **每 10 分钟执行一次的 Cron 任务（示例）：**
   ```bash
   openclaw cron add <<'JSON'
   {
     "name": "table-mountain-10min",
     "schedule": { "kind": "every", "everyMs": 600000 },
     "sessionTarget": "isolated",
     "payload": {
       "kind": "agentTurn",
       "model": "default",
       "message": "Run `python3 skills/table-mountain-status/scripts/fetch_status.py --output data/table-mountain/latest.txt`. Post the summary to Master on Telegram, highlight status (open/closed), weather, queues, and timestamp. If the fetch fails, report the error."
     }
   }
   JSON
   ```
2. **临时任务**（例如：仅在当地时间 16:00 之前执行）→ 设置 `schedule.kind = "cron"`、`expr = "*/10 6-15 * * *"`、`tz = "Europe/Berlin"`，任务完成后执行 `cron update --enabled=false` 或 `cron remove`。
3. **任务停止**：如果同时运行多个任务，请务必同时停止间隔任务和每日任务。

## 故障排除
- **API 抛错或请求被拒绝**：脚本会返回退出代码 1 并显示错误信息 → Cron 任务会继续报告该错误。
- **时区问题**：`lastUpdated` 的时间会被转换为 UTC+2（开普敦时区）。如有需要，可修改脚本中的 `format_summary` 函数。
- **默认等待时间（0:05:00）** 可能来自 API 的默认设置；如果需要自定义等待时间，请在报告中说明。
- **网络限制**：如果需要使用 `curl` 代理，请考虑使用 `urllib` 并配置环境代理。

## 资源
- `scripts/fetch_status.py` – 一个简单的命令行工具，用于获取、格式化并保存 Table Mountain 的状态信息（文本或 JSON 格式）。