---
name: human_test
slug: human-test
description: "邀请真实用户来测试你的产品。通过净推荐值（NPS）分数、详细的任务执行报告以及人工智能汇总的分析结果，获取结构化的用户体验反馈。"
summary: "human_test() — hire real humans to test any URL. Returns an AI-generated usability report with NPS analysis and actionable recommendations."
tags:
  - testing
  - usability
  - feedback
  - ux-research
  - human-in-the-loop
version: 1.0.0
---
# `human_test()` — 为AI产品提供真实的人类反馈

AI代理无法评估人类的感知、情感或产品的可用性。该功能允许您邀请真实用户来测试任何产品URL，并获得结构化的反馈。

## 功能概述

1. 您通过提供产品URL来调用`human_test()`函数。
2. AI会自动生成一个结构化的测试计划。
3. 真实用户会在该Web平台上接受测试任务。
4. 每位测试者需要完成一个包含三个步骤的反馈流程（初步印象、任务步骤、NPS评分）。
5. AI会将所有反馈汇总成一份按严重程度排序的报告。

## 快速入门

您需要一个API密钥。请访问https://human-test.work/register进行注册（免费注册，注册即可获得100个信用点）。

### 创建测试任务

```bash
curl -X POST https://human-test.work/api/skill/human-test \
  -H "Authorization: Bearer <your-api-key>" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-product.com",
    "focus": "Test the onboarding flow",
    "maxTesters": 5
  }'
```

### 查看进度并获取报告

```bash
curl https://human-test.work/api/skill/status/<taskId> \
  -H "Authorization: Bearer <your-api-key>"
```

### 报告完成后的响应：

```json
{
  "taskId": "cm...",
  "status": "COMPLETED",
  "submittedCount": 5,
  "report": "## Executive Summary\n..."
}
```

## 参数说明

| 参数            | 是否必填 | 默认值     | 说明                                      |
|-----------------|---------|-----------|-----------------------------------------|
| `url`           | 是        | —        | 需要测试的产品URL                          |
| `title`          | 否        | 从域名自动生成 | 任务标题                                      |
| `focus`          | 否        | 测试者应关注的焦点                        |
| `maxTesters`       | 否        | 5         | 测试者数量（1-50人）                          |
| `rewardPerTester`     | 否        | 20        | 每位测试者的奖励信用点数                          |
| `estimatedMinutes`    | 否        | 10        | 预计的测试时间（分钟）                          |
| `webhookUrl`       | 否        | —        | 完成测试后接收报告的HTTPS地址                        |

## 异步Webhook

如果您提供了`webhookUrl`，平台会在所有测试者提交反馈后，将完整报告发送到该URL：

```json
{
  "taskId": "...",
  "status": "COMPLETED",
  "title": "Test: example.com",
  "targetUrl": "https://example.com",
  "report": "## Executive Summary\n...",
  "completedAt": "2026-03-02T12:00:00Z"
}
```

## 信用点系统

- 注册：免费获得100个信用点。
- 创建测试任务：`rewardPerTester × maxTesters`信用点。
- 通过测试他人的产品来赚取信用点（每次测试20个信用点）。

## 报告内容

AI生成的报告包括：
- 执行摘要
- 关键发现（按严重程度排序，并标注具体测试者）
- 可用性问题（严重/主要/次要）
- 积极亮点
- NPS分析（详细数据）
- 可操作的改进建议

## 链接

- Web平台：https://human-test.work
- API文档：https://human-test.work/settings（登录后可见curl使用示例）