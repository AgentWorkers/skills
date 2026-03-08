# APM 性能排查

适用于调查响应缓慢的端点、高错误率或性能下降的情况。

---

## 第一步：确定问题应用程序

```bash
# Get APM summary for all apps
newrelic entity search --name "" --type APPLICATION --domain APM | \
  jq '.[] | {name, alertSeverity, applicationId}'

# Get detailed APM summary for a specific app
newrelic apm application get --applicationId <APP_ID>
```

---

## 第二步：分析交易处理速度

```bash
# Top 10 slowest transactions (last 1 hour)
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT average(duration), percentile(duration, 95), count(*)
  FROM Transaction
  WHERE appName = 'my-app'
  FACET name
  SINCE 1 hour ago
  LIMIT 10
  ORDER BY average(duration) DESC
"

# Transactions over SLA threshold (e.g. > 2 seconds)
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT count(*), average(duration)
  FROM Transaction
  WHERE appName = 'my-app' AND duration > 2
  FACET name
  SINCE 1 hour ago
"
```

---

## 第三步：分析数据库查询性能

```bash
# Slowest DB operations
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT average(duration), count(*)
  FROM DatabaseTrace
  WHERE appName = 'my-app'
  FACET statement
  SINCE 1 hour ago
  LIMIT 10
  ORDER BY average(duration) DESC
"

# DB time as % of total transaction time
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT average(databaseDuration), average(duration),
         percentage(average(databaseDuration), average(duration)) AS 'DB %'
  FROM Transaction
  WHERE appName = 'my-app'
  SINCE 1 hour ago
"
```

---

## 第四步：分析错误原因

```bash
# Error rate by transaction
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT count(*), percentage(count(*), WHERE error IS true) AS 'Error Rate'
  FROM Transaction
  WHERE appName = 'my-app'
  FACET name
  SINCE 1 hour ago
"

# Recent errors with messages
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT message, count(*)
  FROM TransactionError
  WHERE appName = 'my-app'
  FACET message
  SINCE 1 hour ago
  LIMIT 20
"

# Full error details including stack trace fields
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT timestamp, name, message, error.class
  FROM TransactionError
  WHERE appName = 'my-app'
  SINCE 30 minutes ago
  LIMIT 10
"
```

---

## 第五步：检查吞吐量和 Apdex 值

```bash
# Requests per minute + Apdex trend
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT rate(count(*), 1 minute) AS 'RPM', apdex(duration, 0.5) AS 'Apdex'
  FROM Transaction
  WHERE appName = 'my-app'
  TIMESERIES 5 minutes
  SINCE 1 hour ago
"
```

---

## 第六步：分析与应用部署之间的关系

```bash
# List recent deployments
newrelic apm deployment list --applicationId <APP_ID>

# Check if performance changed after a deploy
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT average(duration)
  FROM Transaction
  WHERE appName = 'my-app'
  TIMESERIES 10 minutes
  SINCE 3 hours ago
"
# Look for inflection points that align with deployment timestamps
```

---

## 获取应用程序 ID

```bash
newrelic entity search --name "my-app" --type APPLICATION --domain APM | \
  jq '.[] | {name, applicationId, guid}'
```