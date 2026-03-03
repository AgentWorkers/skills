---
name: lead-enrichment-pipeline
description: 自动化潜在客户捕获、去重、跟踪和通知流程：通过 Webhook 从网页表单中捕获潜在客户信息，在 Google Sheets 中通过电子邮件进行去重处理，根据信息来源和客户互动情况对潜在客户进行评分，并向团队发送通知。包含 3 个可立即投入使用的 n8n 工作流程。
tags: [leads, crm, google-sheets, sales, pipeline, automation, b2b, prospecting, webhooks, n8n]
author: mhmalvi
version: 1.2.0
license: CC BY-NC-SA 4.0
metadata:
  clawdbot:
    emoji: "🎯"
    requires:
      n8nCredentials: [google-sheets-oauth2, smtp]
    os: [linux, darwin, win32]
---
# 销售线索捕获与跟踪流程 🎯

通过任何渠道捕获销售线索，通过电子邮件进行去重处理，根据线索意图进行评分，然后在 Google Sheets 中进行跟踪，并通过 n8n 工作流自动通知您的团队。

## 问题

销售线索来自多种渠道（网站表单、新闻通讯、战略会议预约、产品等待名单）。手动将这些线索输入 CRM 并跟进不仅容易出错，而且效率低下。有价值的线索也可能因此被忽略。

该流程能够实时捕获、去重、评分并分配线索。

## 功能概述

1. **捕获** — 从 Webhook（网站表单、着陆页、聊天机器人）接收线索。
2. **去重** — 在 Google Sheets 中检查是否存在相同的线索（通过 `appendOrUpdate` 方法进行匹配）。
3. **评分** — 根据线索来源类型和用户互动情况对其进行基本评分。
4. **存储** — 将评分数据添加到 Google Sheets 中。
5. **通知** — 通过电子邮件向团队发送线索详情及下一步建议。

> **注意：** 该流程不包含第三方数据增强功能（如 Clearbit、FullContact）。如需使用这些功能，请在工作流中在 Webhook 节点和 Sheets 节点之间添加一个 HTTP Request 节点，调用您选择的第三方数据增强 API。

## 包含的工作流

| 编号 | 文件名 | 功能 |
|---|------|---------|
| 1 | `lead-tracker.json` | 从 Webhook 捕获线索 → 去重 → 存储到 Sheets → 通知负责人 |
| 2 | `lead-magnet.json` | 下载吸引用户的资料 → 存储线索 → 发送包含 PDF 附件的电子邮件 |
| 3 | `newsletter.json` | 新闻通讯订阅 → 存储订阅者信息 → 发送欢迎邮件 |

## 架构

```
Lead Source (form, chatbot, API)
    │
    ▼
Webhook Endpoint (n8n)
    │
    ├── Validate required fields (name, email)
    ├── Check for duplicates (email match in Sheets)
    │
    ├── IF new lead:
    │   ├── Score lead (source type + available fields)
    │   ├── Append to Google Sheets
    │   └── Send notification email to team
    │
    └── IF existing lead:
        ├── Update engagement count
        └── Log new touchpoint
```

## 所需的 n8n 凭据

在导入工作流之前，您需要在 n8n 实例中创建以下凭据：

| 凭据类型 | 用途 | JSON 中的占位符 |
|----------------|----------|---------------------|
| Google Sheets OAuth2 | 读写 Google Sheets 数据 | `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` |
| SMTP（Gmail 或自定义） | 发送通知邮件 | `YOUR_SMTP_CREDENTIAL_ID` |

导入完成后，请打开每个工作流并将相应的凭据节点更新为您自己的凭据。

## 配置占位符

在部署工作流之前，请将以下占位符替换为实际值：

| 占位符 | 说明 |
|-------------|-------------|
| `YOUR_LEADS_SHEET_ID` | 用于跟踪线索的 Google Sheets ID |
| `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` | n8n 的 Google Sheets 凭据 ID |
| `YOUR_SMTP_CREDENTIAL_ID` | n8n 的 SMTP 凭据 ID |
| `YOUR_FROM_EMAIL` | 发件人电子邮件地址 |
| `YOUR_NOTIFICATION_EMAIL` | 通知邮件的接收地址 |
| `YOUR_NAME` | 用于邮件模板中的发送者名称 |
| `YOUR_DOMAIN` | 电子邮件链接中的网站域名 |

## 支持的销售线索来源

| 来源 | Webhook 路径 | 收集的字段 |
|--------|-------------|--------|
| 新闻通讯订阅 | `/webhook/newsletter` | email |
| 下载吸引用户的资料 | `/webhook/lead-magnet` | name, email, company |
| 战略会议预约 | `/webhook/strategy-call` | name, email, phone, company, message |
| 产品等待名单 | `/webhook/product-waitlist` | name, email |
| 联系表单 | `/webhook/contact` | name, email, subject, message |
| 自定义来源 | `/webhook/add-lead-enriched` | 任意 JSON 格式的信息 |

## Google Sheets 数据结构

| 列名 | 类型 | 说明 |
|--------|------|-------------|
| name | text | 全名 |
| email | text | 电子邮件地址（用于去重） |
| company | text | 公司名称 |
| phone | text | 电话号码 |
| source | text | 线索来源 |
| score | number | 线索评分（0-100 分） |
| status | text | 新线索 / 已联系 / 符合条件 / 转化 |
| created_at | date | 首次捕获时间 |
| updated_at | date | 最后活动时间 |
| touchpoints | number | 总互动次数 |
| notes | text | 其他备注 |

## 快速入门

### 1. 先决条件
- n8n v2.4 或更高版本（自托管或云服务）
- Google Sheets API 凭据（OAuth2）
- SMTP 电子邮件凭据（Gmail 或自定义）

### 2. 创建跟踪表格
创建一个包含上述列的 Google Sheets 表格，并启用 `appendOrUpdate` 功能，以便根据 `email` 列来防止重复记录。

### 3. 导入工作流
将 `workflows/` 目录下的 3 个 JSON 文件导入 n8n，并将所有 `YOUR_*` 占位符替换为实际值。

### 4. 测试
```bash
curl -X POST https://your-n8n.com/webhook/add-lead-enriched \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@company.com",
    "company": "Acme Inc",
    "source": "website-contact"
  }'
```

## 线索评分规则

| 评分因素 | 分数 | 说明 |
|--------|--------|---------|
| 来源：战略会议预约 | +40 | 高意向度 |
| 来源：下载吸引用户的资料 | +25 | 中等意向度 |
| 来源：新闻通讯 | +10 | 低意向度 |
| 是否提供公司名称 | +10 | 表明有潜在的商业价值 |
| 是否提供电话号码 | +15 | 表示愿意进一步沟通 |
| 回访用户 | 每次互动 +10 分 | 表示用户活跃 |

## 使用场景

1. **自由职业者** — 跟踪来自网站表单的潜在客户。
2. **代理机构** — 多渠道线索捕获并自动通知团队。
3. **SaaS 服务提供商** — 管理等待名单并评分。
4. **内容创作者** — 跟踪新闻通讯订阅者并评估其互动情况。
5. **电子商务企业** — 管理客户咨询流程。

## 所需条件

- n8n v2.4 或更高版本（自托管或云服务）
- Google Sheets API 凭据（OAuth2）
- SMTP 电子邮件凭据