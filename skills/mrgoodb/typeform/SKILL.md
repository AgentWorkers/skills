---
name: typeform
description: 通过 Typeform API 创建和管理表单、调查问卷以及测验。可以检索用户的回答数据及相关的分析结果。
metadata: {"clawdbot":{"emoji":"📝","requires":{"env":["TYPEFORM_API_TOKEN"]}}}
---

# Typeform

用于创建表单和调查问卷的工具。

## 环境配置

```bash
export TYPEFORM_API_TOKEN="tfp_xxxxxxxxxx"
```

## 表单列表

```bash
curl "https://api.typeform.com/forms" \
  -H "Authorization: Bearer $TYPEFORM_API_TOKEN"
```

## 获取表单详情

```bash
curl "https://api.typeform.com/forms/{form_id}" \
  -H "Authorization: Bearer $TYPEFORM_API_TOKEN"
```

## 获取用户反馈

```bash
curl "https://api.typeform.com/forms/{form_id}/responses" \
  -H "Authorization: Bearer $TYPEFORM_API_TOKEN"
```

## 获取反馈数量

```bash
curl "https://api.typeform.com/forms/{form_id}/responses?page_size=1" \
  -H "Authorization: Bearer $TYPEFORM_API_TOKEN" | jq '.total_items'
```

## 创建新表单

```bash
curl -X POST "https://api.typeform.com/forms" \
  -H "Authorization: Bearer $TYPEFORM_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Feedback Survey",
    "fields": [
      {"type": "short_text", "title": "What is your name?"},
      {"type": "rating", "title": "How would you rate us?", "properties": {"steps": 5}}
    ]
  }'
```

## 删除用户反馈

```bash
curl -X DELETE "https://api.typeform.com/forms/{form_id}/responses?included_response_ids={response_id}" \
  -H "Authorization: Bearer $TYPEFORM_API_TOKEN"
```

## 链接：
- 仪表板：https://admin.typeform.com
- 文档：https://developer.typeform.com