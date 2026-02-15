---
name: datadog
description: 通过 Datadog API 监控基础设施和应用程序。查询指标数据、管理仪表板，并设置警报。
metadata: {"clawdbot":{"emoji":"🐕","requires":{"env":["DD_API_KEY","DD_APP_KEY"]}}}
---

# Datadog

基础设施监控工具。

## 环境配置

```bash
export DD_API_KEY="xxxxxxxxxx"
export DD_APP_KEY="xxxxxxxxxx"
export DD_SITE="datadoghq.com"  # or datadoghq.eu, us3.datadoghq.com, etc.
```

## 提交指标数据

```bash
curl -X POST "https://api.$DD_SITE/api/v2/series" \
  -H "DD-API-KEY: $DD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "series": [{
      "metric": "custom.metric",
      "type": 0,
      "points": [{"timestamp": '$(date +%s)', "value": 42}],
      "tags": ["env:prod"]
    }]
  }'
```

## 查询指标数据

```bash
curl "https://api.$DD_SITE/api/v1/query?from=$(date -d '1 hour ago' +%s)&to=$(date +%s)&query=avg:system.cpu.user{*}" \
  -H "DD-API-KEY: $DD_API_KEY" \
  -H "DD-APPLICATION-KEY: $DD_APP_KEY"
```

## 列出监控项

```bash
curl "https://api.$DD_SITE/api/v1/monitor" \
  -H "DD-API-KEY: $DD_API_KEY" \
  -H "DD-APPLICATION-KEY: $DD_APP_KEY"
```

## 创建监控项

```bash
curl -X POST "https://api.$DD_SITE/api/v1/monitor" \
  -H "DD-API-KEY: $DD_API_KEY" \
  -H "DD-APPLICATION-KEY: $DD_APP_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "CPU High Alert",
    "type": "metric alert",
    "query": "avg(last_5m):avg:system.cpu.user{*} > 90",
    "message": "CPU usage is above 90%!"
  }'
```

## 发送事件

```bash
curl -X POST "https://api.$DD_SITE/api/v1/events" \
  -H "DD-API-KEY: $DD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "Deployment", "text": "Deployed v1.2.3", "tags": ["env:prod"]}'
```

## 列出仪表板

```bash
curl "https://api.$DD_SITE/api/v1/dashboard" \
  -H "DD-API-KEY: $DD_API_KEY" \
  -H "DD-APPLICATION-KEY: $DD_APP_KEY"
```

## 链接：
- 仪表板：https://app.datadoghq.com
- 文档：https://docs.datadoghq.com/api