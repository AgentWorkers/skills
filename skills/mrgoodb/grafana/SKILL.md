---
name: grafana
description: 通过 API 管理 Grafana 仪表板、数据源和警报。可视化指标和日志数据。
metadata: {"clawdbot":{"emoji":"📉","requires":{"env":["GRAFANA_URL","GRAFANA_API_KEY"]}}}
---
# Grafana
可观测性仪表板（Observability dashboards）

## 环境（Environment）
```bash
export GRAFANA_URL="https://grafana.example.com"
export GRAFANA_API_KEY="xxxxxxxxxx"
```

## 仪表板列表（List Dashboards）
```bash
curl "$GRAFANA_URL/api/search?type=dash-db" -H "Authorization: Bearer $GRAFANA_API_KEY"
```

## 获取仪表板（Get Dashboard）
```bash
curl "$GRAFANA_URL/api/dashboards/uid/{uid}" -H "Authorization: Bearer $GRAFANA_API_KEY"
```

## 数据源列表（List Data Sources）
```bash
curl "$GRAFANA_URL/api/datasources" -H "Authorization: Bearer $GRAFANA_API_KEY"
```

## 创建警报规则（Create Alert Rule）
```bash
curl -X POST "$GRAFANA_URL/api/v1/provisioning/alert-rules" \
  -H "Authorization: Bearer $GRAFANA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "High CPU", "condition": "A", "data": [...]}'
```

## 链接（Links）
- 文档：https://grafana.com/docs/grafana/latest/developers/http_api/