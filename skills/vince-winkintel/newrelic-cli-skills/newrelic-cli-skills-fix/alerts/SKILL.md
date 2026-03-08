# 警报管理

通过命令行界面（CLI）管理警报策略、条件及通知渠道。

---

## 列出警报策略

```bash
newrelic alerts policy list
```

## 获取策略信息

```bash
newrelic alerts policy get --policyId <ID>
```

## 创建策略

```bash
newrelic alerts policy create \
  --name "My App - Performance" \
  --incidentPreference "PER_CONDITION_AND_TARGET"
```

事件优先级选项：
- `PER_POLICY`：每个策略违规事件触发一次警报
- `PER_condition`：每个条件违规事件触发一次警报
- `PER_condition_AND_TARGET`：最细粒度的选项，每个条件+目标对象组合触发一次警报

---

## 警报条件

### 列出策略的条件

```bash
newrelic alerts conditions list --policyId <POLICY_ID>
```

### 创建 APM 指标条件

```bash
newrelic alerts apmCondition create \
  --policyId <POLICY_ID> \
  --name "High Response Time" \
  --type "apm_app_metric" \
  --metric "response_time_web" \
  --conditionScope "application" \
  --violationCloseTimer 24 \
  --threshold 2.0 \
  --thresholdDuration 5 \
  --thresholdOccurrences "ALL"
```

### 删除条件

```bash
newrelic alerts conditions delete --conditionId <ID>
```

---

## NRQL 警报条件

```bash
newrelic alerts nrqlCondition static create \
  --policyId <POLICY_ID> \
  --name "Error Rate > 5%" \
  --query "SELECT percentage(count(*), WHERE error IS true) FROM Transaction WHERE appName='my-app'" \
  --threshold 5 \
  --thresholdDuration 5 \
  --thresholdOccurrences "ALL" \
  --violationTimeLimitSeconds 86400
```

---

## 通知渠道

```bash
# List channels
newrelic alerts channel list

# Create email channel
newrelic alerts channel create \
  --name "On-Call Email" \
  --type email \
  --configuration '{"recipients": "team@example.com", "include_json_attachment": false}'
```

---

## 查看未解决的警报事件

```bash
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT *
  FROM NrAiIncident
  WHERE event = 'open'
  SINCE 24 hours ago
  LIMIT 20
"
```

---

## 检查实体警报的严重程度

```bash
newrelic entity search --name "my-app" --type APPLICATION --domain APM | \
  jq '.[] | {name, alertSeverity}'
```

严重程度等级：`NOT_CONFIGURED`、`NOT_ALERTING`、`WARNING`、`CRITICAL`