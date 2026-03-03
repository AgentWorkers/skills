---
name: newsletter-automation
description: >
  这是一个完整的新闻通讯管理系统，具备以下功能：  
  - 订阅者注册（需经过双重确认流程）  
  - 自动化的欢迎邮件发送序列  
  - 新闻通讯发送功能  
  - 订阅者数据分析  
  该系统还包含4个可直接投入使用的n8n工作流（N8N：Node-RED-based workflow framework），这些工作流与Google Sheets后端进行集成。
tags: [newsletter, email, subscribers, drip, automation, marketing, n8n, google-sheets]
author: mhmalvi
version: 1.2.0
license: CC BY-NC-SA 4.0
metadata:
  clawdbot:
    emoji: "\U0001F4EC"
    requires:
      n8nCredentials: [google-sheets-oauth2, smtp]
      env: [NEWSLETTER_ADMIN_EMAIL, NEWSLETTER_BASE_URL, NEWSLETTER_SECRET]
    os: [linux, darwin, win32]
---
# 新闻通讯自动化系统

这是一个基于 n8n 和 Google Sheets 构建的完整新闻通讯管理系统。它支持双重确认机制的订阅者注册、自动发送欢迎邮件、批量发送新闻通讯以及每日数据分析报告。

## 问题

手动管理新闻通讯意味着需要在多个工具之间协调处理注册表单、确认邮件、欢迎邮件和批量发送邮件等流程。大多数新闻通讯平台都是按订阅者数量收费的，这会让你失去对数据的控制。

该系统为你提供了一个免费且可自托管的新闻通讯解决方案，完全基于 n8n 和 Google Sheets 构建。

## 功能介绍

1. **双重确认注册**：通过 Webhook 接收注册请求，验证电子邮件地址，发送确认链接，并将信息存储到 Google Sheets 中。
2. **欢迎邮件序列**：自动在注册后的第 0 天、第 3 天和第 7 天发送欢迎邮件和资源分享邮件。
3. **批量发送功能**：通过 API 触发，向所有已确认的订阅者发送新闻通讯，并提供退订链接。
4. **每日数据分析**：提供订阅者数量、增长指标、确认率等数据统计。

## 包含的工作流

| 编号 | 文件名 | 功能 |
| --- | --- | --- |
| 01 | `01-subscriber-signup.json` | 通过 Webhook 处理注册请求，进行验证和双重确认，并将数据存储到 Google Sheets 中 |
| 02 | `02-welcome-sequence.json` | 安排在第 0 天、第 3 天和第 7 天自动发送欢迎邮件 |
| 03 | `03-broadcast-sender.json` | 通过 Webhook 向所有已确认的订阅者发送新闻通讯 |
| 04 | `04-subscriber-analytics.json` | 每日发送订阅者数据分析报告邮件 |

## 架构（此处为代码块，具体实现细节请参考原文）

## 所需的 n8n 凭据

| 凭据类型 | 用途 | JSON 中的占位符 |
| --- | --- | --- |
| Google Sheets OAuth2 | 用于存储订阅者信息 | `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` |
| SMTP（Gmail 或自定义） | 用于发送所有邮件（确认邮件、欢迎邮件、批量邮件和报告邮件） | `YOUR_SMTP_CREDENTIAL_ID` |

## 环境变量（此处为代码块，具体配置细节请参考原文）

## 配置占位符

| 占位符 | 说明 |
| --- | --- |
| `YOUR_SUBSCRIBERS_SHEET_ID` | 用于存储订阅者信息的 Google Sheets 表格 ID |
| `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` | n8n 与 Google Sheets 之间的连接凭证 ID |
| `YOUR_SMTP_CREDENTIAL_ID` | 用于发送邮件的 SMTP 服务凭证 ID |
| `YOUR_NOTIFICATION_EMAIL` | 管理员的备用通知邮箱（也可通过 `NEWSLETTER_ADMIN_EMAIL` 环境变量设置） |
| `YOUR_DOMAIN` | 系统的备用域名（也可通过 `NEWSLETTER_BASE_URL` 环境变量设置） |

## Google Sheets 数据表结构（订阅者信息）

| 列名 | 类型 | 说明 |
| --- | --- | --- |
| email | text | 订阅者的电子邮件地址 |
| name | text | 订阅者的姓名 |
| status | text | 订阅状态（待确认、已确认或已退订） |
| source | text | 订阅者注册的来源（网站、着陆页等） |
| subscribed_at | datetime | 注册时间 |
| confirmed | boolean | 电子邮件是否已确认 |
| token | text | 确认邮件中的令牌 |
| last_drip_day | number | 最后一次发送欢迎邮件的日期（0、3 或 7） |
| last_drip_at | datetime | 最后一次发送欢迎邮件的时间 |

## 快速入门

### 1. 先决条件
- n8n 版本 2.4 或更高（建议自托管）
- Google Sheets 的 OAuth2 凭据
- SMTP 服务账号

### 2. 创建订阅者表格
创建一个包含上述列的 Google Sheets 表格，并将表格标签命名为 “Subscribers”。

### 3. 导入工作流
将所有 4 个 JSON 文件导入 n8n，并替换其中的 `YOUR_*` 占位符。

### 4. 测试注册功能
```bash
curl -X POST https://your-n8n.com/webhook/newsletter/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "name": "Test User", "source": "api-test"}'
```

### 5. 测试批量发送功能
```bash
curl -X POST https://your-n8n.com/webhook/newsletter/broadcast \
  -H "Content-Type: application/json" \
  -d '{
    "_secret": "your-newsletter-secret",
    "subject": "Test Broadcast",
    "content": "<p>This is a test broadcast.</p>"
  }'
```

## 使用场景

1. **个人新闻通讯**：作为 Substack 或 ConvertKit 的自托管替代方案。
2. **企业新闻通讯**：每周向客户发送更新信息，且不收取任何费用。
3. **产品更新**：通知用户新功能或发布的更新内容。
4. **社区新闻通讯**：管理社区或组织的订阅者列表。
5. **内容创作者**：利用自动化流程建立受众群体。

## 所需软件/服务

- n8n 版本 2.4 或更高（建议自托管）
- Google Sheets 的 OAuth2 凭据
- SMTP 服务账号（Gmail、SES 或自定义服务）