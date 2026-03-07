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

AI代理无法判断人类的感知、情感或产品的可用性。此功能允许您邀请真实用户来测试任何产品URL，并获得结构化的反馈。

## 功能概述

1. 您通过提供产品URL来调用`human_test()`函数。
2. AI会自动生成一个结构化的测试计划。
3. 真实用户会在该测试平台上接受任务。
4. 每位测试者需要完成一个包含三个步骤的反馈流程（初步印象、任务步骤、NPS评分）。
5. AI会将所有反馈汇总成一份按严重程度排序的报告。

## 快速入门

您需要一个API密钥。请访问https://human-test.work/register进行免费注册以获取密钥。

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

## 参数

| 参数          | 是否必填 | 默认值     | 说明                                      |
|--------------|---------|-----------|-----------------------------------------|
| `url`         | 是       |           | 需要测试的产品URL                              |
| `title`        | 否        | 从域名自动生成 | 任务标题                                    |
| `focus`        | 否        |           | 测试者应关注的焦点                              |
| `maxTesters`     | 否        | 5         | 测试者数量（1-50人）                              |
| `estimatedMinutes` | 否        | 10         | 预计测试时间                                  |
| `webhookUrl`     | 否        |           | 完成后接收报告的HTTPS链接                         |
| `repoUrl`       | 否        |           | 用于代码修复建议的GitHub/Gitee仓库URL                   |
| `repoBranch`     | 否        | repo默认分支   | 仅当提供`repoUrl`时使用                         |

## 异步Webhook

如果您提供了`webhookUrl`，平台会在所有测试者提交完成后将完整报告发送到该URL：

```json
{
  "taskId": "...",
  "status": "COMPLETED",
  "title": "Test: example.com",
  "targetUrl": "https://example.com",
  "report": "## Executive Summary\n...",
  "codeFixPrUrl": "https://github.com/user/repo/pull/1",
  "completedAt": "2026-03-02T12:00:00Z"
}
```

## 报告格式（适用于AI代理）

报告以markdown字符串的形式通过`report`字段返回。该格式采用**一致且可被机器解析的结构**，便于AI代理直接读取并采取行动（例如：自动创建问题、提交Pull Request或安排修复优先级）。

### 报告结构

每份报告都包含以下固定部分：

```markdown
## Metadata
| Field | Value |
|-------|-------|
| Product | ... |
| URL | ... |
| Testers | N |
| Avg NPS | X.X/10 |

## Executive Summary
(3-5 sentences, most critical finding first)

## Issues
### [CRITICAL] Issue title
- **Evidence:** (specific testers and observations)
- **Impact:** (effect on users)
- **Recommendation:** (actionable fix)

### [MAJOR] Issue title
- **Evidence:** ...
- **Impact:** ...
- **Recommendation:** ...

### [MINOR] Issue title
...

## Positive Highlights
(What worked well)

## NPS Analysis
(Score breakdown, interpretation)

## Recommendations
- **P0** (fix immediately): ... (references issue)
- **P1** (fix this sprint): ...
- **P2** (next sprint): ...
- **P3** (backlog): ...
```

### 代理解析提示

- **严重程度级别**：`[CRITICAL]`、`[MAJOR]`、`[MINOR]` — 始终用括号标注在问题标题中
- **优先级标签**：`P0`、`P1`、`P2`、`P3` — 显示在“建议”部分
- **每个问题包含3个字段**：**证据**、**影响**、**建议** — 标签均为加粗显示
- **元数据表**：始终位于报告的第一部分，包含机器可读的键值对
- **NPS评分**：显示在“元数据”部分（平均值）和“NPS分析”部分（按测试者划分）

## 代理自动修复工作流程

该结构化报告格式支持闭环工作流程：您的代理调用`human_test()`，接收报告后自动修复发现的问题——测试结束后无需人工干预。

### 推荐的操作流程

1. 使用产品URL调用`human_test()`（如果需要接收通知，请包含`webhookUrl`）。
2. 等待报告结果（可以通过`/api/skill/status/<taskId>`轮询或接收Webhook通知）。
3. 解析“## Issues”部分：每个问题都包含严重程度、证据、影响和修复建议。
4. 对于`[CRITICAL]`和`[MAJOR]`级别的问题，根据“建议”字段生成针对性的代码修复方案。
5. 为每个修复方案创建提交或Pull Request。
6. （可选）再次调用`human_test()`以验证修复效果。

每个问题的“证据”部分说明了问题出在哪里，“影响”部分说明了问题的重要性，“建议”部分则明确了具体的修复内容。这为代理提供了足够的上下文，使其能够无需猜测即可编写针对性的修复代码。

### 基于仓库的代码修复建议

如果您提供了`repoUrl`，平台会在生成报告后克隆您的仓库，并在报告的“## Code Fix Suggestions”部分提供代码修复建议（附带统一差异文件）。

### 两种模式（自动检测）

**模式1 — 只读权限**：授予GitHub用户`avivahe326`对您的仓库的读权限。报告生成后，平台会克隆仓库，分析代码中的问题，并在报告中添加代码差异文件。

**模式2 — 开发者权限**：授予`avivahe326`写权限。与模式1相同，此外还会：
- 创建一个名为`human-test/fixes-<taskId>`的分支
- 应用差异文件并推送更改
- 提交Pull Request（PR）。PR的URL会通过Webhook返回，同时在状态API中提供。

### 带有`repoUrl`的示例

```bash
curl -X POST https://human-test.work/api/skill/human-test \
  -H "Authorization: Bearer <your-api-key>" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-product.com",
    "focus": "Test the checkout flow",
    "repoUrl": "https://github.com/your-org/your-repo",
    "repoBranch": "main",
    "webhookUrl": "https://your-server.com/webhook"
  }'
```

## 链接

- 测试平台：https://human-test.work
- API文档：https://human-test.work/settings（登录后可查看curl示例）