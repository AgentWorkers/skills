# NRQL 查询

您可以使用 NRQL 查询来针对您的 New Relic 账户执行自定义查询。

---

## 基本语法

```bash
newrelic nrql query \
  --accountId $NEW_RELIC_ACCOUNT_ID \
  --query "YOUR NRQL HERE"
```

---

## 主要事件类型

| 事件类型 | 跟踪的内容 |
|---|---|
| `Transaction` | Web 或非 Web 请求的耗时 |
| `TransactionError` | 异常和错误 |
| `DatabaseTrace` | 单个数据库查询的耗时 |
| `ExternalTrace` | 出站 HTTP 请求 |
| `SystemSample` | 主机 CPU、内存、磁盘使用情况 |
| `ProcessSample` | 每个进程的指标 |
| `Log` | 日志记录（如果启用了日志转发） |
| `PageView` | 浏览器页面加载事件 |
| `JavaScriptError` | 前端 JavaScript 错误 |

---

## 常见查询模式

### 响应时间

```nrql
SELECT average(duration), percentile(duration, 95, 99)
FROM Transaction
WHERE appName = 'my-app'
TIMESERIES 5 minutes
SINCE 1 hour ago
```

### 错误率

```nrql
SELECT percentage(count(*), WHERE error IS true) AS 'Error %'
FROM Transaction
WHERE appName = 'my-app'
TIMESERIES 5 minutes
SINCE 1 hour ago
```

### 吞吐量（RPM）

```nrql
SELECT rate(count(*), 1 minute) AS 'RPM'
FROM Transaction
WHERE appName = 'my-app'
TIMESERIES
SINCE 1 hour ago
```

### 最慢的端点

```nrql
SELECT average(duration)
FROM Transaction
WHERE appName = 'my-app'
FACET name
SINCE 1 hour ago
LIMIT 10
ORDER BY average(duration) DESC
```

### 数据库瓶颈

```nrql
SELECT average(duration), count(*)
FROM DatabaseTrace
WHERE appName = 'my-app'
FACET statement
SINCE 1 hour ago
LIMIT 10
ORDER BY average(duration) DESC
```

### 比较两个时间窗口

```nrql
SELECT average(duration)
FROM Transaction
WHERE appName = 'my-app'
SINCE 1 hour ago
COMPARE WITH 1 day ago
```

### 按类型统计错误

```nrql
SELECT count(*)
FROM TransactionError
WHERE appName = 'my-app'
FACET error.class
SINCE 1 hour ago
```

### 主机 CPU 使用情况

```nrql
SELECT average(cpuPercent)
FROM SystemSample
FACET hostname
TIMESERIES 5 minutes
SINCE 1 hour ago
```

### 主机内存使用情况

```nrql
SELECT average(memoryUsedPercent)
FROM SystemSample
FACET hostname
TIMESERIES 5 minutes
SINCE 1 hour ago
```

---

## 时间范围快捷方式

```
SINCE 30 minutes ago
SINCE 1 hour ago
SINCE 3 hours ago
SINCE 1 day ago
SINCE 1 week ago
SINCE '2026-02-01 00:00:00' UNTIL '2026-02-02 00:00:00'
```

---

## 有用的子句

```nrql
FACET name          -- group by field
TIMESERIES 5 min    -- time series chart
LIMIT 20            -- max results
ORDER BY count() DESC
COMPARE WITH 1 day ago
WHERE appName = 'x' AND duration > 1
```

---

## 输出格式

```bash
# Raw JSON
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID \
  --query "SELECT count(*) FROM Transaction SINCE 1 hour ago" \
  --format json

# Pretty table (default)
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID \
  --query "SELECT count(*) FROM Transaction SINCE 1 hour ago"
```