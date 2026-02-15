---
name: surveymonkey
description: 通过 SurveyMonkey API 创建调查问卷并收集用户反馈。您可以管理这些调查问卷、查看调查结果，并导出相关数据。
metadata: {"clawdbot":{"emoji":"📋","requires":{"env":["SURVEYMONKEY_ACCESS_TOKEN"]}}}
---

# SurveyMonkey

一个用于进行调查和收集反馈的平台。

## 环境配置

```bash
export SURVEYMONKEY_ACCESS_TOKEN="xxxxxxxxxx"
```

## 列出所有调查问卷

```bash
curl "https://api.surveymonkey.com/v3/surveys" \
  -H "Authorization: Bearer $SURVEYMONKEY_ACCESS_TOKEN"
```

## 查看调查问卷详情

```bash
curl "https://api.surveymonkey.com/v3/surveys/{survey_id}/details" \
  -H "Authorization: Bearer $SURVEYMONKEY_ACCESS_TOKEN"
```

## 获取调查问卷的回复数据

```bash
curl "https://api.surveymonkey.com/v3/surveys/{survey_id}/responses/bulk" \
  -H "Authorization: Bearer $SURVEYMONKEY_ACCESS_TOKEN"
```

## 创建新的调查问卷

```bash
curl -X POST "https://api.surveymonkey.com/v3/surveys" \
  -H "Authorization: Bearer $SURVEYMONKEY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Customer Feedback"}'
```

## 为调查问卷添加页面

```bash
curl -X POST "https://api.surveymonkey.com/v3/surveys/{survey_id}/pages" \
  -H "Authorization: Bearer $SURVEYMONKEY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Page 1"}'
```

## 添加问题（Question）

```bash
curl -X POST "https://api.surveymonkey.com/v3/surveys/{survey_id}/pages/{page_id}/questions" \
  -H "Authorization: Bearer $SURVEYMONKEY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "family": "single_choice",
    "subtype": "vertical",
    "headings": [{"heading": "How satisfied are you?"}],
    "answers": {"choices": [{"text": "Very satisfied"}, {"text": "Satisfied"}, {"text": "Not satisfied"}]}
  }'
```

## 链接：
- 仪表板：https://www.surveymonkey.com
- 文档：https://developer.surveymonkey.com/api/v3/