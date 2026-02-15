---
name: pagerduty
description: 通过 PagerDuty API 管理事件、值班排班以及警报。可以编程方式触发和解决事件。
metadata: {"clawdbot":{"emoji":"🚨","requires":{"env":["PAGERDUTY_API_KEY"]}}}
---

# PagerDuty

事件管理。

## 环境配置

```bash
export PAGERDUTY_API_KEY="u+xxxxxxxxxx"
export PAGERDUTY_SERVICE_ID="PXXXXXX"
export PAGERDUTY_ROUTING_KEY="xxxxxxxxxx"  # For Events API
```

## 触发事件（Events API v2）

```bash
curl -X POST "https://events.pagerduty.com/v2/enqueue" \
  -H "Content-Type: application/json" \
  -d '{
    "routing_key": "'$PAGERDUTY_ROUTING_KEY'",
    "event_action": "trigger",
    "dedup_key": "incident-123",
    "payload": {
      "summary": "Server CPU at 95%",
      "severity": "critical",
      "source": "monitoring-system"
    }
  }'
```

## 解决事件

```bash
curl -X POST "https://events.pagerduty.com/v2/enqueue" \
  -H "Content-Type: application/json" \
  -d '{
    "routing_key": "'$PAGERDUTY_ROUTING_KEY'",
    "event_action": "resolve",
    "dedup_key": "incident-123"
  }'
```

## 查看事件列表

```bash
curl "https://api.pagerduty.com/incidents?statuses[]=triggered&statuses[]=acknowledged" \
  -H "Authorization: Token token=$PAGERDUTY_API_KEY"
```

## 查看待命人员信息

```bash
curl "https://api.pagerduty.com/oncalls" \
  -H "Authorization: Token token=$PAGERDUTY_API_KEY"
```

## 查看服务列表

```bash
curl "https://api.pagerduty.com/services" \
  -H "Authorization: Token token=$PAGERDUTY_API_KEY"
```

## 链接：
- 仪表盘：https://app.pagerduty.com
- 文档：https://developer.pagerduty.com