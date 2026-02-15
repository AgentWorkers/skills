---
name: heap
description: 通过 Heap API 分析用户行为。可以查询事件、用户信息以及用户行为路径（funnels）。
metadata: {"clawdbot":{"emoji":"📈","requires":{"env":["HEAP_APP_ID","HEAP_API_KEY"]}}}
---
# 堆（Heap）  
产品分析（Product Analytics）  

## 环境（Environment）  
```bash
export HEAP_APP_ID="xxxxxxxxxx"
export HEAP_API_KEY="xxxxxxxxxx"
```  

## 跟踪事件（服务器端）（Track Events – Server-side）  
```bash
curl -X POST "https://heapanalytics.com/api/track" \
  -H "Content-Type: application/json" \
  -d '{"app_id": "'$HEAP_APP_ID'", "identity": "user@example.com", "event": "Purchase", "properties": {"amount": 99}}'
```  

## 添加用户属性（Add User Properties）  
```bash
curl -X POST "https://heapanalytics.com/api/add_user_properties" \
  -H "Content-Type: application/json" \
  -d '{"app_id": "'$HEAP_APP_ID'", "identity": "user@example.com", "properties": {"plan": "premium"}}'
```  

## 查询 API（Query API）  
```bash
curl "https://heapanalytics.com/api/partner/v1/events?app_id=$HEAP_APP_ID" \
  -H "Authorization: Bearer $HEAP_API_KEY"
```  

## 链接（Links）  
- 仪表盘：https://heapanalytics.com  
- 文档：https://developers.heap.io