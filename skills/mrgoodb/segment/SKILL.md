---
name: segment
description: 通过 Segment API 追踪事件并管理客户数据。将数据路由到指定的目的地。
metadata: {"clawdbot":{"emoji":"📊","requires":{"env":["SEGMENT_WRITE_KEY"]}}}
---
# 客户数据平台  
## 环境  
```bash
export SEGMENT_WRITE_KEY="xxxxxxxxxx"
```  
## 跟踪事件  
```bash
curl -X POST "https://api.segment.io/v1/track" \
  -u "$SEGMENT_WRITE_KEY:" \
  -H "Content-Type: application/json" \
  -d '{"userId": "user123", "event": "Order Completed", "properties": {"revenue": 99.99}}'
```  
## 识别用户  
```bash
curl -X POST "https://api.segment.io/v1/identify" \
  -u "$SEGMENT_WRITE_KEY:" \
  -H "Content-Type: application/json" \
  -d '{"userId": "user123", "traits": {"email": "user@example.com", "plan": "premium"}}'
```  
## 页面浏览  
```bash
curl -X POST "https://api.segment.io/v1/page" \
  -u "$SEGMENT_WRITE_KEY:" \
  -H "Content-Type: application/json" \
  -d '{"userId": "user123", "name": "Home", "properties": {"url": "https://example.com"}}'
```  
## 链接  
- 仪表盘：https://app.segment.com  
- 文档：https://segment.com/docs/connections/sources/catalog/libraries/server/http-api/