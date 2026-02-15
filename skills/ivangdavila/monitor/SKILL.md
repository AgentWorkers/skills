---
name: Monitor
description: 创建灵活的监控脚本，支持结构化日志记录、警报功能以及针对任何目标的智能数据分析。
metadata: {"clawdbot":{"emoji":"📡","os":["linux","darwin","win32"]}}
---

## 目录结构

```
.monitors/
├── config.json          # Global settings (alert defaults, retention)
├── monitors/            # One script per monitor
│   ├── web-mysite.sh
│   ├── twitter-elonmusk.py
│   └── api-stripe-health.sh
├── logs/                # Structured logs per monitor
│   ├── web-mysite/
│   │   └── 2024-03.jsonl
│   └── twitter-elonmusk/
│       └── 2024-03.jsonl
└── alerts/              # Alert history
    └── 2024-03.jsonl
```

## 监控脚本

- 每个监控脚本都是一个独立的脚本（支持 bash、python、node），存储在 `.monitors/monitors/` 目录下。
- 脚本必须以 0 的状态退出表示成功，非 0 的状态表示失败。
- 脚本会将结果以 JSON 格式输出到标准输出（stdout）：`{"status": "ok|warn|fail", "value": "任意值", "message": "人类可读的文本"}`。
- 保持脚本的简洁性和高效性——它们按计划运行，而不是持续运行。
- 脚本命名规则：`{类型}-{目标}.{扩展名}`（例如：`web-api-prod.sh`、`content-competitor-blog.py`）。

## 日志格式

- 每个监控脚本每月生成一个 JSONL 格式的日志文件：`logs/{监控脚本名称}/YYYY-MM.jsonl`。
- 日志条目格式：`{"ts": "ISO8601", "status": "ok|warn|fail", "value": "...", "latency_ms": N, "message": "..."}`。
- 日志文件仅支持追加写入，不允许修改已有条目。
- 默认保留 12 个月的日志记录，具体保留时间可通过 `config.json` 配置文件进行调整。

## 创建监控脚本

当用户请求监控功能时，系统会创建相应的监控脚本：

- **Web 系统运行状态监控**：使用 `curl` 命令检查网站的响应状态码，并设置超时时间。
```bash
#!/bin/bash
START=$(date +%s%3N)
STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$URL")
LATENCY=$(($(date +%s%3N) - START))
if [ "$STATUS" = "200" ]; then
  echo "{\"status\":\"ok\",\"value\":$STATUS,\"latency_ms\":$LATENCY}"
else
  echo "{\"status\":\"fail\",\"value\":$STATUS,\"message\":\"HTTP $STATUS\"}"
  exit 1
fi
```

- **内容变化监控**：计算页面内容的哈希值，并与上次记录进行比较。
- **API 健康状况监控**：调用 API 端点并验证响应数据的结构是否正确。
- **社交媒体监控**：获取最新的帖子内容并检查是否有新的更新。
- **自定义指标监控**：执行任意命令并解析其输出结果。

## 运行监控脚本

- 监控脚本通过 cron 任务或定时任务来执行——系统会根据用户的请求设置相应的执行计划。
- 建议的监控间隔如下：关键任务（1 分钟一次）、重要任务（5 分钟一次）、常规任务（15 分钟一次）、每日任务（24 小时一次）。
- 监控脚本会读取所有需要监控的脚本，执行它们，并将执行结果写入日志文件，同时触发相应的警报。
- 监控脚本的运行日志记录在 `logs/runner.log` 文件中，便于排查调度问题。

## 警报配置

警报配置信息存储在 `config.json` 文件中：
```json
{
  "alerts": {
    "default": {"type": "log"},
    "channels": {
      "pushover": {"token": "...", "user": "..."},
      "agent": {"enabled": true},
      "webhook": {"url": "..."}
    }
  },
  "monitors": {
    "web-mysite": {"alert": ["pushover", "agent"], "interval": "5m"}
  }
}
```

- **警报类型**：
  - **log**：仅将警报信息写入 `alerts/YYYY-MM.jsonl` 文件。
  - **agent**：标记需要由系统管理员在后续沟通中提及的警报。
  - **pushover/ntfy**：发送推送通知。
  - **webhook**：向指定 URL 发送 POST 请求。
  - **email**：通过配置好的 SMTP 服务器发送电子邮件。

## 警报逻辑

- 当监控状态发生变化（从 “ok” 变为 “fail” 或从 “fail” 变为 “ok”）时触发警报，以避免因连续失败而产生大量冗余警报。
- 警报中会包含连续失败的次数。
- 恢复提示：例如：“监控脚本 X 在连续失败 3 次（12 分钟后）恢复正常”。
- 可配置警报触发条件：仅在实际发生 N 次连续失败时才触发警报。

## 智能分析（系统管理员辅助）

当用户询问监控情况时，系统会：
- 分析最近的日志记录，计算网站的运行时间百分比。
- 识别异常模式（例如：“周末网站响应速度变慢”、“API 每周一上午 9 点出现故障”）。
- 根据用户的关注点推荐新的监控任务。
- 如用户要求，生成每周的监控报告，内容包括运行时间统计、故障事件及趋势分析。

## 高效的数据处理策略

- 不需要存储完整的响应内容，只需保存状态码、延迟时间以及相关的提取数据。
- 对于内容监控，仅保存内容的哈希值和变化摘要，而非全部内容。
- 如果存储空间有限，会压缩超过 30 天的日志文件。
- 通过状态码对日志进行索引，以便快速查询所有失败的记录。