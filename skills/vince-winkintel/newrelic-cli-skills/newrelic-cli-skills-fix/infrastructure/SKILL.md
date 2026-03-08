# 基础设施监控

通过 New Relic Infrastructure 监控主机指标（CPU、内存、磁盘、进程）。

---

## 主机列表

```bash
newrelic entity search --name "" --type HOST | \
  jq '.[] | {name, alertSeverity, guid}'
```

---

## CPU 使用情况

```bash
# Average CPU per host (last hour)
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT average(cpuPercent)
  FROM SystemSample
  FACET hostname
  TIMESERIES 5 minutes
  SINCE 1 hour ago
"

# CPU spikes > 80%
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT percentage(count(*), WHERE cpuPercent > 80) AS 'Time > 80% CPU'
  FROM SystemSample
  FACET hostname
  SINCE 1 hour ago
"
```

---

## 内存使用情况

```bash
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT average(memoryUsedPercent), average(memoryFreeBytes / 1e9) AS 'Free GB'
  FROM SystemSample
  FACET hostname
  TIMESERIES 5 minutes
  SINCE 1 hour ago
"
```

---

## 磁盘使用情况

```bash
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT latest(diskUsedPercent)
  FROM StorageSample
  FACET hostname, mountPoint
  SINCE 10 minutes ago
"
```

---

## 网络 I/O

```bash
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT average(receiveBytesPerSecond), average(transmitBytesPerSecond)
  FROM NetworkSample
  FACET hostname
  TIMESERIES 5 minutes
  SINCE 1 hour ago
"
```

---

## CPU 使用率最高的进程

```bash
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT average(cpuPercent)
  FROM ProcessSample
  WHERE hostname = 'my-host'
  FACET processDisplayName
  SINCE 30 minutes ago
  LIMIT 10
  ORDER BY average(cpuPercent) DESC
"
```

---

## 内存使用率最高的进程

```bash
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT average(memoryResidentSizeBytes) / 1e6 AS 'RSS MB'
  FROM ProcessSample
  WHERE hostname = 'my-host'
  FACET processDisplayName
  SINCE 30 minutes ago
  LIMIT 10
  ORDER BY average(memoryResidentSizeBytes) DESC
"
```

---

## 将主机负载与应用程序性能关联起来

```bash
# Side-by-side: host CPU vs app response time
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT average(cpuPercent) AS 'CPU %'
  FROM SystemSample
  WHERE hostname = 'my-host'
  TIMESERIES 5 minutes
  SINCE 1 hour ago
"

newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT average(duration) AS 'Avg Response (s)'
  FROM Transaction
  WHERE appName = 'my-app'
  TIMESERIES 5 minutes
  SINCE 1 hour ago
"
# Compare the two time series to see if CPU pressure correlates with slowdowns
```

---

## 主机报告状态

```bash
newrelic entity search --name "" --type HOST | \
  jq '.[] | {name, reporting}'
```