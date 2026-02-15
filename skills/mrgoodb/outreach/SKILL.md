---
name: outreach
description: 通过Outreach API管理销售互动：创建销售流程、管理潜在客户，并跟踪各项销售活动。
metadata: {"clawdbot":{"emoji":"📧","requires":{"env":["OUTREACH_ACCESS_TOKEN"]}}}
---
# 外展（Outreach）
销售协作平台。

## 环境（Environment）
```bash
export OUTREACH_ACCESS_TOKEN="xxxxxxxxxx"
```

## 列出潜在客户（List Prospects）
```bash
curl "https://api.outreach.io/api/v2/prospects" \
  -H "Authorization: Bearer $OUTREACH_ACCESS_TOKEN" \
  -H "Content-Type: application/vnd.api+json"
```

## 创建潜在客户（Create Prospect）
```bash
curl -X POST "https://api.outreach.io/api/v2/prospects" \
  -H "Authorization: Bearer $OUTREACH_ACCESS_TOKEN" \
  -H "Content-Type: application/vnd.api+json" \
  -d '{"data": {"type": "prospect", "attributes": {"firstName": "John", "lastName": "Doe", "emails": ["john@example.com"]}}}'
```

## 列出工作流程（List Sequences）
```bash
curl "https://api.outreach.io/api/v2/sequences" \
  -H "Authorization: Bearer $OUTREACH_ACCESS_TOKEN"
```

## 添加到工作流程中（Add to Sequence）
```bash
curl -X POST "https://api.outreach.io/api/v2/sequenceStates" \
  -H "Authorization: Bearer $OUTREACH_ACCESS_TOKEN" \
  -H "Content-Type: application/vnd.api+json" \
  -d '{"data": {"type": "sequenceState", "relationships": {"prospect": {"data": {"type": "prospect", "id": "123"}}, "sequence": {"data": {"type": "sequence", "id": "456"}}}}}'
```

## 链接（Links）
- 仪表板：https://app.outreach.io
- 文档：https://api.outreach.io/api/v2/docs