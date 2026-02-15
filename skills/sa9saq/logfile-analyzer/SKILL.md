---
description: 解析并分析应用程序日志——提取错误模式、错误发生的频率、时间线以及可操作的洞察（即基于日志数据得出的实际建议或行动方案）。
---

# 日志分析工具

该工具用于解析和汇总应用程序日志，以发现错误、模式及异常情况。

**适用场景**：分析日志文件、调试错误或汇总系统事件。

## 所需工具

- 标准的 Unix 工具：`grep`、`awk`、`sort`、`uniq`
- 可选工具：`jq`（用于处理 JSON 格式的日志）
- 无需 API 密钥

## 使用步骤

1. **获取日志来源** — 常见日志存放位置：
   ```bash
   # System logs
   /var/log/syslog
   /var/log/auth.log
   journalctl -u <service> --since "1 hour ago" --no-pager

   # Web servers
   /var/log/nginx/error.log
   /var/log/nginx/access.log

   # Docker
   docker logs --since 1h <container> 2>&1

   # Application logs
   # Ask user for path
   ```

2. **快速分析** — 按以下顺序执行相应命令：
   ```bash
   # File overview
   wc -l logfile
   head -1 logfile && tail -1 logfile   # time range

   # Error counts by level
   grep -ciE '(error|fatal|critical)' logfile
   grep -ciE '(warn|warning)' logfile

   # Top error patterns (deduplicated)
   grep -iE '(error|exception|fatal)' logfile | \
     sed 's/[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}[T ][0-9:.]*//g' | \
     sed 's/\[.*\]//g' | sort | uniq -c | sort -rn | head -20

   # Error timeline (per hour)
   grep -iE '(error|fatal)' logfile | \
     grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}[T ][0-9]{2}' | \
     sort | uniq -c

   # Recent errors with context
   grep -iE '(error|exception|fatal)' logfile | tail -30
   ```

3. **JSON 格式日志**（结构化日志）：
   ```bash
   cat logfile | jq -r 'select(.level == "error") | .message' | sort | uniq -c | sort -rn
   cat logfile | jq -r 'select(.level == "error") | .timestamp' | head -5  # first errors
   ```

4. **输出格式**：
   ```
   📊 Log Analysis — filename.log (42,531 lines)
   Time range: 2025-01-15 00:00 → 2025-01-15 14:30

   ## Summary
   | Level | Count | % |
   |-------|-------|---|
   | ERROR | 67 | 0.16% |
   | WARN | 234 | 0.55% |
   | INFO | 42,230 | 99.3% |

   ## Top Errors
   | Count | Error Pattern |
   |-------|--------------|
   | 42 | Connection refused to db:5432 |
   | 18 | TimeoutError: request exceeded 30s |
   | 7 | OutOfMemoryError: heap space |

   ## Error Timeline
   | Hour | Errors | |
   |------|--------|-|
   | 14:00 | 3 | ▪ |
   | 15:00 | 47 | ▪▪▪▪▪▪▪▪▪▪▪▪▪ ⚠️ Spike |
   | 16:00 | 5 | ▪▪ |

   ## 🔍 Recommendations
   - [ ] Check database connectivity (42 connection refused errors)
   - [ ] Review timeout settings (18 timeouts at 30s)
   - [ ] Increase JVM heap size (7 OOM errors)
   ```

## 特殊情况处理

- **大文件（>100MB）**：建议先使用 `tail -n 10000` 或 `--since` 进行筛选，避免将整个文件加载到内存中。
- **非标准日志格式**：需询问用户日志的时间戳和级别格式，然后相应地调整 `grep` 的匹配规则。
- **二进制/压缩日志**：
  - 对 `.gz` 文件使用 `zgrep`；
  - 对 systemd 系统生成的日志使用 `journalctl`。
- **多行堆栈跟踪信息**：使用 `grep -A 5` 来获取错误发生后的上下文信息。
- **无时间戳**：在这种情况下，需依赖日志行号来进行分析。

## 实时监控

如需实现实时监控，建议使用以下方法：
```bash
tail -f logfile | grep --line-buffered -iE '(error|fatal)'
```

## 安全注意事项

- 日志文件可能包含敏感数据（如 IP 地址、电子邮件地址、令牌等），在分享分析结果前请对这些信息进行脱敏处理。
- 不要将日志内容通过管道传输到外部服务。