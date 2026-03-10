---
name: human_test
slug: human-test
description: "邀请真实用户来测试你的产品（无论是网站还是应用程序）。通过屏幕录制、净推荐值（NPS）评分以及人工智能汇总的分析结果，获取系统的可用性反馈。"
summary: "human_test() — hire real humans to test any product. Returns an AI-generated usability report with video analysis, NPS scores, and actionable recommendations."
tags:
  - testing
  - usability
  - feedback
  - ux-research
  - human-in-the-loop
version: 1.6.0
---
# `human_test()` — 为AI产品提供真实的人类反馈

AI代理无法判断人类的感知、情感或产品的可用性。该功能允许您邀请真实用户来测试任何产品URL，并获得结构化的反馈。

## 功能概述

1. 您可以通过提供产品URL或描述来调用`human_test()`（URL是可选的——适用于移动应用、桌面软件等）。
2. AI会自动生成一个结构化的测试计划。
3. 真实用户会在该Web平台上接受任务。
4. 每位测试者在完成引导式反馈流程时，会录制他们的屏幕画面和音频（最长15分钟），内容包括第一印象、任务步骤以及NPS评分。
5. AI会从每个录制中提取关键帧，并利用视觉AI分析可用性问题，然后将所有反馈汇总成一份按严重程度排序的报告。

## 设置

### 选项A：托管版（无需安装）

使用托管版本：**https://human-test.work**。无需安装。注册后获取API密钥，然后使用`BASE_URL=https://human-test.work`进行测试任务创建。

### 选项B：自托管版（自动安装）

`human_test()`可以在本地运行。在创建任务之前，请检查服务器是否可访问：

```bash
curl -s BASE_URL/api/config
```

如果服务器未运行，请进行安装并启动：

```bash
npm i -g humantest-app
cd /tmp && humantest init --non-interactive && cd humantest && humantest start
```

该工具会自动从您的环境中检测AI API密钥（`ANTHROPIC_API_KEY`、`OPENAI_API_KEY`、`DEEPSEEK_API_KEY`或`GEMINI_API_KEY`），创建一个本地SQLite数据库，构建应用程序，并在端口3000上启动它。系统会自动创建一个管理员用户——无需注册。

**设置`BASE_URL`**：询问用户他们偏好的基础URL。默认值：`http://localhost:3000`。

## 快速入门

### 创建测试任务

```bash
curl -X POST BASE_URL/api/skill/human-test \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-product.com",
    "focus": "Test the onboarding flow",
    "maxTesters": 5,
    "creator": "agent-name"
  }'
```

### 查看进度并获取报告

```bash
curl BASE_URL/api/skill/status/<taskId>
```

### 报告完成后的响应：

> **注意（对于AI代理）：** 如果提供了`repoUrl`，报告准备好后代码修复工作会自动开始——无需手动触发。请持续监控`codeFixStatus`的状态，直到其变为`COMPLETED`或`FAILED`；或者使用`codeFixWebhookUrl`接收通知。

## 参数

| 参数 | 是否必填 | 默认值 | 说明 |
|-----------|----------|---------|-------------|
| `url` | 否 | — | 要测试的产品URL（可选——对于移动应用或非Web产品可留空） |
| `title` | 否 | 从主机名自动生成 | 任务标题 |
| `focus` | 否 | — | 测试人员应关注的重点 |
| `maxTesters` | 否 | 5 | 测试人员数量（1-50人） |
| `estimatedMinutes` | 否 | 10 | 预计测试时间 |
| `creator` | 否 | 管理员 | 创建任务的用户/代理的名称（必要时会自动创建用户） |
| `webhookUrl` | 否 | — | 完成后接收报告的HTTPS URL |
| `codeFixWebhookUrl` | 否 | — | 完成后接收代码修复结果的HTTPS URL |
| `repoUrl` | 否 | — | 用于代码级修复建议的GitHub仓库URL |
| `repoBranch` | 否 | 仓库默认分支 | 仅当提供`repoUrl`时使用 |
| `locale` | 否 | `en` | 报告语言：`en`（英语）或`zh`（中文） |

## 异步Webhook

有两个独立的Webhook，分别用于两个阶段：

### 报告Webhook（`webhookUrl`）

如果您提供了`webhookUrl`，平台会在报告准备好时将其发送到该URL：

```json
{
  "event": "report",
  "taskId": "...",
  "status": "COMPLETED",
  "title": "Test: example.com",
  "targetUrl": "https://example.com",
  "report": "## Executive Summary\n...",
  "completedAt": "2026-03-02T12:00:00Z"
}
```

### 代码修复Webhook（`codeFixWebhookUrl`）

如果您提供了`codeFixWebhookUrl`，平台会在代码修复完成后将其发送到该URL：

```json
{
  "event": "code_fix",
  "taskId": "...",
  "status": "COMPLETED",
  "title": "Test: example.com",
  "targetUrl": "https://example.com",
  "codeFixStatus": "COMPLETED",
  "codeFixPrUrl": "https://github.com/user/repo/pull/1",
  "completedAt": "2026-03-02T12:30:00Z"
}
```

## 报告格式（适用于AI代理）

报告以markdown字符串的形式返回，存储在`report`字段中。该格式具有**一致性且可被机器解析**，专为AI代理设计，便于直接读取和采取行动——例如自动记录问题、创建Pull Request（PR）或安排修复优先级。

## 报告结构

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

- **严重程度级别**：`[CRITICAL]`、`[MAJOR]`、`[MINOR]`——始终用括号标明在问题标题中 |
- **优先级标签**：`P0`、`P1`、`P2`、`P3`——位于“建议”部分 |
- **每个问题包含3个字段**：证据（Evidence）、影响（Impact）和修复建议（Recommendation）——标签均加粗显示 |
- **元数据表**：始终位于报告的第一部分，包含机器可读的键值对 |
- **NPS评分**：显示在元数据（平均值）和“NPS分析”（按测试者划分）中

## 代理的自动修复工作流程

该结构化报告格式支持闭环工作流程：您的代理调用`human_test()`，接收报告后自动修复发现的问题——测试完成后无需人工干预。

### 推荐流程

1. 使用产品URL调用`human_test()`（包含`webhookUrl`以接收通知）。
2. 等待报告（通过`/api/skill/status/<taskId>`轮询或接收Webhook通知）。
3. 解析“## Issues”部分——每个问题都包含严重程度、证据和修复建议。
4. 对于`[CRITICAL]`和`[MAJOR]`问题，根据“修复建议”字段生成针对性的代码修复方案。
5. 为每个修复方案创建提交或Pull Request（PR）。
6. （可选）再次调用`human_test()`以验证修复效果。

每个问题的“证据”部分说明了问题所在，“影响”部分说明了问题的重要性，“修复建议”部分则明确了具体的修复内容。这为代理提供了足够的上下文，使其能够无需猜测即可编写针对性的修复代码。

## 基于仓库的代码修复建议

如果您提供了`repoUrl`，平台会在报告准备好后立即触发代码修复流程。它会克隆您的仓库，分析报告中的问题，并生成代码级别的修复建议（附带统一差异文件），这些建议会作为“## Code Fix Suggestions”部分添加到报告中。

### 两种模式（自动检测）

**模式1 — 只读权限**：授予GitHub用户`avivahe326`对您的仓库的读取权限。报告生成后，平台会克隆仓库，分析问题，并将代码差异添加到报告中。

**模式2 — 开发者权限**：授予`avivahe326`写入权限。与模式1相同，此外还会创建一个名为`human-test/fixes-<taskId>`的分支，应用差异并推送更改，然后创建Pull Request（PR）。PR的URL会通过Webhook的payload和状态API返回。

### 带有`repoUrl`的示例

```bash
curl -X POST BASE_URL/api/skill/human-test \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-product.com",
    "focus": "Test the checkout flow",
    "repoUrl": "https://github.com/your-org/your-repo",
    "repoBranch": "main",
    "webhookUrl": "https://your-server.com/webhook",
    "codeFixWebhookUrl": "https://your-server.com/code-fix-webhook"
  }'
```

## 链接

- Web平台：https://human-test.work
- GitHub仓库：https://github.com/avivahe326/humantest