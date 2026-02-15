---
name: log-analyzer
description: 解析、搜索并分析各种格式的应用程序日志。适用于从日志文件中进行调试、设置结构化日志记录、分析错误模式、跨服务关联事件、解析堆栈跟踪，或实时监控日志输出等场景。
metadata: {"clawdbot":{"emoji":"📋","requires":{"anyBins":["grep","awk","jq","python3"]},"os":["linux","darwin","win32"]}}
---

# 日志分析器

用于解析、搜索和调试应用程序日志。支持处理纯文本日志、结构化JSON日志、堆栈跟踪信息，以及实现多服务间的日志关联和实时监控功能。

## 使用场景

- 从日志文件中调试应用程序错误
- 在日志中搜索特定模式、错误或请求ID
- 解析和分析堆栈跟踪信息
- 在应用程序中配置结构化日志记录（JSON格式）
- 关联多个服务或日志文件中的事件
- 在开发过程中实时监控日志
- 生成错误频率报告或摘要

## 快速搜索模式

### 查找错误和异常

```bash
# All errors in a log file
grep -i 'error\|exception\|fatal\|panic\|fail' app.log

# Errors with 3 lines of context
grep -i -C 3 'error\|exception' app.log

# Errors in the last hour (ISO timestamps)
HOUR_AGO=$(date -u -d '1 hour ago' '+%Y-%m-%dT%H:%M' 2>/dev/null || date -u -v-1H '+%Y-%m-%dT%H:%M')
awk -v t="$HOUR_AGO" '$0 ~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}T/ && $1 >= t' app.log | grep -i 'error'

# Count errors by type
grep -oP '(?:Error|Exception): \K[^\n]+' app.log | sort | uniq -c | sort -rn | head -20

# HTTP 5xx errors from access logs
awk '$9 >= 500' access.log
```

### 按请求ID或关联ID搜索

```bash
# Trace a single request across log entries
grep 'req-abc123' app.log

# Across multiple files
grep -r 'req-abc123' /var/log/myapp/

# Across multiple services (with filename prefix)
grep -rH 'correlation-id-xyz' /var/log/service-a/ /var/log/service-b/ /var/log/service-c/
```

### 时间范围过滤

```bash
# Between two timestamps (ISO format)
awk '$0 >= "2026-02-03T10:00" && $0 <= "2026-02-03T11:00"' app.log

# Last N lines (tail)
tail -1000 app.log | grep -i error

# Since a specific time (GNU date)
awk -v start="$(date -d '30 minutes ago' '+%Y-%m-%dT%H:%M')" '$1 >= start' app.log
```

## JSON / 结构化日志

### 使用jq进行解析

```bash
# Pretty-print JSON logs
cat app.log | jq '.'

# Filter by level
cat app.log | jq 'select(.level == "error")'

# Filter by time range
cat app.log | jq 'select(.timestamp >= "2026-02-03T10:00:00Z")'

# Extract specific fields
cat app.log | jq -r '[.timestamp, .level, .message] | @tsv'

# Count by level
cat app.log | jq -r '.level' | sort | uniq -c | sort -rn

# Filter by nested field
cat app.log | jq 'select(.context.userId == "user-123")'

# Group errors by message
cat app.log | jq -r 'select(.level == "error") | .message' | sort | uniq -c | sort -rn

# Extract request duration stats
cat app.log | jq -r 'select(.duration != null) | .duration' | awk '{sum+=$1; count++; if($1>max)max=$1} END {print "count="count, "avg="sum/count, "max="max}'
```

### 解析混合格式的日志（JSON行与纯文本混合）

```bash
# Extract only valid JSON lines
while IFS= read -r line; do
  echo "$line" | jq '.' 2>/dev/null && continue
done < app.log

# Or with grep for lines starting with {
grep '^\s*{' app.log | jq '.'
```

## 堆栈跟踪分析

### 提取并去重堆栈跟踪信息

```bash
# Extract Java/Kotlin stack traces (starts with Exception/Error, followed by \tat lines)
awk '/Exception|Error/{trace=$0; while(getline && /^\t/) trace=trace"\n"$0; print trace"\n---"}' app.log

# Extract Python tracebacks
awk '/^Traceback/{p=1} p{print} /^[A-Za-z].*Error/{if(p) print "---"; p=0}' app.log

# Extract Node.js stack traces (Error + indented "at" lines)
awk '/Error:/{trace=$0; while(getline && /^    at /) trace=trace"\n"$0; print trace"\n---"}' app.log

# Deduplicate: group by root cause (first line of trace)
awk '/Exception|Error:/{cause=$0} /^\tat|^    at /{next} cause{print cause; cause=""}' app.log | sort | uniq -c | sort -rn
```

### 使用Python进行堆栈跟踪解析

```python
#!/usr/bin/env python3
"""Parse Python tracebacks from log files and group by root cause."""
import sys
import re
from collections import Counter

def extract_tracebacks(filepath):
    tracebacks = []
    current = []
    in_trace = False

    with open(filepath) as f:
        for line in f:
            if line.startswith('Traceback (most recent call last):'):
                in_trace = True
                current = [line.rstrip()]
            elif in_trace:
                current.append(line.rstrip())
                # Exception line ends the traceback
                if re.match(r'^[A-Za-z]\w*(Error|Exception|Warning)', line):
                    tracebacks.append('\n'.join(current))
                    in_trace = False
                    current = []
    return tracebacks

if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else '/dev/stdin'
    traces = extract_tracebacks(filepath)

    # Group by exception type and message
    causes = Counter()
    for trace in traces:
        lines = trace.split('\n')
        cause = lines[-1] if lines else 'Unknown'
        causes[cause] += 1

    print(f"Found {len(traces)} tracebacks, {len(causes)} unique causes:\n")
    for cause, count in causes.most_common(20):
        print(f"  {count:4d}x  {cause}")
```

## 实时监控

### 监控日志流并过滤数据

```bash
# Follow log file, highlight errors in red
tail -f app.log | grep --color=always -i 'error\|warn\|$'

# Follow and filter to errors only
tail -f app.log | grep --line-buffered -i 'error\|exception'

# Follow JSON logs, pretty-print errors
tail -f app.log | while IFS= read -r line; do
  level=$(echo "$line" | jq -r '.level // empty' 2>/dev/null)
  if [ "$level" = "error" ] || [ "$level" = "fatal" ]; then
    echo "$line" | jq '.'
  fi
done

# Follow multiple files
tail -f /var/log/service-a/app.log /var/log/service-b/app.log

# Follow with timestamps (useful when log doesn't include them)
tail -f app.log | while IFS= read -r line; do
  echo "$(date '+%H:%M:%S') $line"
done
```

### 监控特定模式并触发警报

```bash
# Beep on error (terminal bell)
tail -f app.log | grep --line-buffered -i 'error' | while read line; do
  echo -e "\a$line"
done

# Count errors per minute
tail -f app.log | grep --line-buffered -i 'error' | while read line; do
  echo "$(date '+%Y-%m-%d %H:%M') ERROR"
done | uniq -c
```

## 日志格式解析

### 常见访问日志（Apache/Nginx）

```bash
# Parse fields: IP, date, method, path, status, size
awk '{print $1, $9, $7}' access.log

# Top IPs by request count
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -20

# Top paths by request count
awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -20

# Slow requests (response time in last field, microseconds)
awk '{if ($NF > 1000000) print $0}' access.log

# Requests per minute
awk '{split($4,a,":"); print a[1]":"a[2]":"a[3]}' access.log | uniq -c

# Status code distribution
awk '{print $9}' access.log | sort | uniq -c | sort -rn

# 4xx and 5xx with paths
awk '$9 >= 400 {print $9, $7}' access.log | sort | uniq -c | sort -rn | head -20
```

### 自定义分隔符的日志文件

```bash
# Pipe-delimited: timestamp|level|service|message
awk -F'|' '{print $2, $3, $4}' app.log

# Tab-delimited
awk -F'\t' '$2 == "ERROR" {print $1, $4}' app.log

# CSV logs
python3 -c "
import csv, sys
with open(sys.argv[1]) as f:
    for row in csv.DictReader(f):
        if row.get('level') == 'error':
            print(f\"{row['timestamp']} {row['message']}\")
" app.csv
```

## 配置结构化日志记录

### Node.js（使用pino作为快速JSON日志记录工具）

```javascript
// npm install pino
const pino = require('pino');
const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  // Add standard fields to every log line
  base: { service: 'my-api', version: '1.2.0' },
});

// Usage
logger.info({ userId: 'u123', action: 'login' }, 'User logged in');
logger.error({ err, requestId: req.id }, 'Request failed');

// Output: {"level":30,"time":1706900000000,"service":"my-api","userId":"u123","action":"login","msg":"User logged in"}

// Child logger with bound context
const reqLogger = logger.child({ requestId: req.id, userId: req.user?.id });
reqLogger.info('Processing order');
reqLogger.error({ err }, 'Order failed');
```

### Python（使用structlog）

```python
# pip install structlog
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
)
logger = structlog.get_logger(service="my-api")

# Usage
logger.info("user_login", user_id="u123", ip="1.2.3.4")
logger.error("request_failed", request_id="req-abc", error=str(e))

# Output: {"event":"user_login","user_id":"u123","ip":"1.2.3.4","level":"info","timestamp":"2026-02-03T12:00:00Z","service":"my-api"}
```

### Go（使用zerolog）

```go
import (
    "os"
    "github.com/rs/zerolog"
    "github.com/rs/zerolog/log"
)

func init() {
    zerolog.TimeFieldFormat = zerolog.TimeFormatUnix
    log.Logger = zerolog.New(os.Stdout).With().
        Timestamp().
        Str("service", "my-api").
        Logger()
}

// Usage
log.Info().Str("userId", "u123").Msg("User logged in")
log.Error().Err(err).Str("requestId", reqID).Msg("Request failed")
```

## 错误模式报告

### 生成错误频率报告

```bash
#!/bin/bash
# error-report.sh - Summarize errors from a log file
LOG="${1:?Usage: error-report.sh <logfile>}"

echo "=== Error Report: $(basename "$LOG") ==="
echo "Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo ""

total=$(wc -l < "$LOG")
errors=$(grep -ci 'error\|exception\|fatal' "$LOG")
warns=$(grep -ci 'warn' "$LOG")

echo "Total lines:  $total"
echo "Errors:       $errors"
echo "Warnings:     $warns"
echo ""

echo "--- Top 15 Error Messages ---"
grep -i 'error\|exception' "$LOG" | \
  sed 's/^[0-9TZ:.+\-]* //' | \
  sed 's/\b[0-9a-f]\{8,\}\b/ID/g' | \
  sed 's/[0-9]\{1,\}/N/g' | \
  sort | uniq -c | sort -rn | head -15
echo ""

echo "--- Errors Per Hour ---"
grep -i 'error\|exception' "$LOG" | \
  grep -oP '\d{4}-\d{2}-\d{2}T\d{2}' | \
  sort | uniq -c
echo ""

echo "--- First Occurrence of Each Error Type ---"
grep -i 'error\|exception' "$LOG" | \
  sed 's/^[0-9TZ:.+\-]* //' | \
  sort -u | head -10
```

### 使用Python生成JSON格式的错误报告

```python
#!/usr/bin/env python3
"""Generate error summary from JSON log files."""
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime

def analyze_logs(filepath):
    errors = []
    levels = Counter()
    errors_by_hour = defaultdict(int)

    with open(filepath) as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
            except (json.JSONDecodeError, ValueError):
                continue

            level = entry.get('level', entry.get('severity', '')).lower()
            levels[level] += 1

            if level in ('error', 'fatal', 'critical'):
                msg = entry.get('message', entry.get('msg', entry.get('event', 'unknown')))
                ts = entry.get('timestamp', entry.get('time', ''))
                errors.append({'message': msg, 'timestamp': ts, 'entry': entry})

                # Group by hour
                try:
                    hour = ts[:13]  # "2026-02-03T12"
                    errors_by_hour[hour] += 1
                except (TypeError, IndexError):
                    pass

    # Group errors by message
    error_counts = Counter(e['message'] for e in errors)

    print(f"=== Log Analysis: {filepath} ===\n")
    print("Level distribution:")
    for level, count in levels.most_common():
        print(f"  {level:10s}  {count}")

    print(f"\nTotal errors: {len(errors)}")
    print(f"Unique error messages: {len(error_counts)}\n")

    print("Top 15 errors:")
    for msg, count in error_counts.most_common(15):
        print(f"  {count:4d}x  {msg[:100]}")

    if errors_by_hour:
        print("\nErrors by hour:")
        for hour in sorted(errors_by_hour):
            bar = '#' * min(errors_by_hour[hour], 50)
            print(f"  {hour}  {errors_by_hour[hour]:4d}  {bar}")

if __name__ == '__main__':
    analyze_logs(sys.argv[1])
```

## 多服务日志关联

### 合并并排序来自多个服务的日志

```bash
# Merge multiple log files, sort by timestamp
sort -m -t'T' -k1,1 service-a.log service-b.log service-c.log > merged.log

# If files aren't individually sorted, use full sort
sort -t'T' -k1,1 service-*.log > merged.log

# Merge JSON logs, add source field
for f in service-*.log; do
  service=$(basename "$f" .log)
  jq --arg svc "$service" '. + {source: $svc}' "$f"
done | jq -s 'sort_by(.timestamp)[]'
```

### 跟踪跨服务的请求流程

```bash
# Find all log entries for a correlation/request ID across all services
REQUEST_ID="req-abc-123"
grep -rH "$REQUEST_ID" /var/log/services/ | sort -t: -k2

# With JSON logs
for f in /var/log/services/*.log; do
  jq --arg rid "$REQUEST_ID" 'select(.requestId == $rid or .correlationId == $rid)' "$f" 2>/dev/null
done | jq -s 'sort_by(.timestamp)[]'
```

## 日志轮换与大文件处理

### 处理已轮换或压缩的日志

```bash
# Search across rotated logs (including .gz)
zgrep -i 'error' /var/log/app.log*

# Search today's and yesterday's logs
zgrep -i 'error' /var/log/app.log /var/log/app.log.1

# Decompress, filter, and recompress
zcat app.log.3.gz | grep 'ERROR' | gzip > errors-day3.gz
```

### 从大文件中采样数据

```bash
# Random sample of 1000 lines
shuf -n 1000 huge.log > sample.log

# Every 100th line
awk 'NR % 100 == 0' huge.log > sample.log

# First and last 500 lines
{ head -500 huge.log; echo "--- TRUNCATED ---"; tail -500 huge.log; } > excerpt.log
```

## 使用技巧

- 首先始终搜索**请求ID或关联ID**——这比使用时间戳或错误信息能更快地定位问题。
- 当从`tail -f`命令输出日志时，使用`--line-buffered`选项可以避免输出延迟。
- 在对错误进行分组之前，先使用`sed 's/[0-9a-f]\{8,\}/ID/g`命令对ID和数字进行规范化处理，以消除仅因ID不同而产生的重复记录。
- 对于JSON日志，`jq`是必不可少的工具。如果尚未安装，请使用`apt install jq`或`brew install jq`进行安装。
- 配置结构化日志记录（JSON格式）是非常值得的。它能让所有分析任务变得更加简单：过滤、分组、关联和触发警报都可以通过`jq`的一行命令完成。
- 在调试生产环境中的问题时，首先确定**时间范围**和**受影响的用户/请求ID**，然后再在该范围内过滤日志。
- 对于大文件，`awk`比`grep | sort | uniq -c`的组合命令更快，适用于计数和聚合操作。