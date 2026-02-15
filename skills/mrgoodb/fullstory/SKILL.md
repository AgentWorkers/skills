---
name: fullstory
description: 通过 FullStory API 访问会话回放和分析数据，以便调试用户体验。
metadata: {"clawdbot":{"emoji":"📹","requires":{"env":["FULLSTORY_API_KEY"]}}}
---
# FullStory
数字体验分析平台。
## 环境
```bash
export FULLSTORY_API_KEY="xxxxxxxxxx"
```
## 搜索会话
```bash
curl -X POST "https://api.fullstory.com/v2/sessions/search" \
  -H "Authorization: Basic $FULLSTORY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"type": "And", "filters": [{"type": "Event", "name": "Error"}]}}'
```
## 获取会话信息
```bash
curl "https://api.fullstory.com/v2/sessions/{sessionId}" \
  -H "Authorization: Basic $FULLSTORY_API_KEY"
```
## 设置用户属性
```bash
curl -X POST "https://api.fullstory.com/v2/users" \
  -H "Authorization: Basic $FULLSTORY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"uid": "user123", "properties": {"displayName": "John Doe", "email": "john@example.com"}}'
```
## 链接
- 仪表板：https://app.fullstory.com
- 文档：https://developer.fullstory.com