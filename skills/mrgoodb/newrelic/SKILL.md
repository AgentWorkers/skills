---
name: newrelic
description: 通过 New Relic API 监控应用程序和基础设施。查询指标并管理警报。
metadata: {"clawdbot":{"emoji":"📈","requires":{"env":["NEWRELIC_API_KEY","NEWRELIC_ACCOUNT_ID"]}}}
---
# New Relic  
一个用于监控和诊断应用程序性能的平台。  

## 环境配置  
```bash
export NEWRELIC_API_KEY="xxxxxxxxxx"
export NEWRELIC_ACCOUNT_ID="xxxxxxxxxx"
```  

## 使用 NRQL 进行查询  
```bash
curl -X POST "https://api.newrelic.com/graphql" \
  -H "API-Key: $NEWRELIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ actor { account(id: '$NEWRELIC_ACCOUNT_ID') { nrql(query: \"SELECT count(*) FROM Transaction\") { results } } } }"}'
```  

## 列出所有应用程序  
```bash
curl "https://api.newrelic.com/v2/applications.json" -H "Api-Key: $NEWRELIC_API_KEY"
```  

## 链接  
- 仪表盘：https://one.newrelic.com  
- 文档：https://docs.newrelic.com/docs/apis/