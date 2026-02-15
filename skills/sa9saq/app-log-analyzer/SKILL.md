---
description: "**使用场景：**  
当用户需要分析、解析或汇总应用程序日志时，该工具能够从日志文件中提取错误模式、错误发生频率以及可操作的洞察信息。"
---

# 日志分析器

用于解析和汇总应用程序日志，以发现错误、模式和异常情况。

## 功能概述

该工具通过分析日志文件，提供以下信息：
- 错误/警告的频率及分布情况
- 最常见的错误信息（按类型分组）
- 问题发生的时间线
- 可操作的总结报告

## 使用说明

1. **获取日志来源**：可以请求日志文件的路径，或接受通过管道传递的日志数据。常见日志位置包括：
   - `/var/log/syslog`、`/var/log/nginx/error.log`
   - 应用程序日志、Docker日志（`docker logs <container>`）
   - `journalctl -u <service> --since "1 hour ago"`（查看过去1小时内的系统日志）

2. **快速分析命令**：

### 错误汇总
```bash
# Count errors by level
grep -cE '(ERROR|FATAL|CRITICAL)' logfile
grep -cE '(WARN|WARNING)' logfile

# Top 10 error messages (deduplicated)
grep -iE '(error|exception|fatal)' logfile | \
  sed 's/[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}[T ][0-9:.]*//g' | \
  sed 's/\[.*\]//g' | \
  sort | uniq -c | sort -rn | head -20
```

### 问题时间线
```bash
# Errors per hour
grep -iE '(error|fatal)' logfile | \
  grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}[T ][0-9]{2}' | \
  sort | uniq -c
```

### 最近的错误记录
```bash
# Last 50 errors with context
grep -iE '(error|exception|fatal)' logfile | tail -50
```

3. **结构化输出格式**
```
📊 Log Analysis — <filename> (<line_count> lines)

## Summary
- Total lines: X
- Errors: X | Warnings: X | Info: X
- Time range: <start> → <end>

## Top Errors
| Count | Error Pattern |
|-------|--------------|
| 42    | Connection refused to db:5432 |
| 18    | TimeoutError: request exceeded 30s |

## Error Timeline
| Hour | Errors | Notes |
|------|--------|-------|
| 14:00 | 3 | Normal |
| 15:00 | 47 | ⚠️ Spike |

## Recommendations
- [ ] Check database connectivity (42 connection refused errors)
- [ ] Review timeout settings (18 timeout errors)
```

4. **对于大型日志文件（>100MB）**：建议先使用 `tail -n 10000` 或基于时间的过滤方式，避免将整个日志文件加载到内存中。

5. **JSON格式的日志**：可以使用 `jq` 进行解析：
   ```bash
   cat logfile | jq -r 'select(.level == "error") | .message' | sort | uniq -c | sort -rn
   ```

## 注意事项
- 无需使用API密钥——该工具仅依赖 `grep`、`awk`、`sort`、`uniq` 和 `jq` 等命令。
- 支持任何基于文本的日志格式。
- 如需实时监控，建议使用 `tail -f logfile | grep -i error` 命令。