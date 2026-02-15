---
name: statuspage
description: 通过 API 管理 Statuspage 的事件和组件，更新状态信息并通报服务中断情况。
metadata: {"clawdbot":{"emoji":"📟","requires":{"env":["STATUSPAGE_API_KEY","STATUSPAGE_PAGE_ID"]}}}
---
# Statuspage  
用于状态信息的沟通。  

## 环境  
```bash
export STATUSPAGE_API_KEY="xxxxxxxxxx"
export STATUSPAGE_PAGE_ID="xxxxxxxxxx"
```  

## 创建事件  
```bash
curl -X POST "https://api.statuspage.io/v1/pages/$STATUSPAGE_PAGE_ID/incidents" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"incident": {"name": "Service Degradation", "status": "investigating", "body": "We are investigating..."}}'
```  

## 列出事件  
```bash
curl "https://api.statuspage.io/v1/pages/$STATUSPAGE_PAGE_ID/incidents" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY"
```  

## 更新组件  
```bash
curl -X PATCH "https://api.statuspage.io/v1/pages/$STATUSPAGE_PAGE_ID/components/{id}" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"component": {"status": "operational"}}'
```  

## 链接  
- 文档：https://developer.statuspage.io