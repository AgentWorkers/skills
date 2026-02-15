---
name: opsgenie
description: 通过 Opsgenie API 管理事件和值班排班。可以创建警报并进行事件升级处理。
metadata: {"clawdbot":{"emoji":"🚨","requires":{"env":["OPSGENIE_API_KEY"]}}}
---
# Opsgenie  
事件管理工具。  

## 环境配置  
```bash
export OPSGENIE_API_KEY="xxxxxxxxxx"
```  

## 创建警报  
```bash
curl -X POST "https://api.opsgenie.com/v2/alerts" \
  -H "Authorization: GenieKey $OPSGENIE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "Server down", "priority": "P1"}'
```  

## 查看警报列表  
```bash
curl "https://api.opsgenie.com/v2/alerts" -H "Authorization: GenieKey $OPSGENIE_API_KEY"
```  

## 回应警报  
```bash
curl -X POST "https://api.opsgenie.com/v2/alerts/{alertId}/acknowledge" \
  -H "Authorization: GenieKey $OPSGENIE_API_KEY"
```  

## 链接  
- 文档：https://docs.opsgenie.com/docs/api-overview