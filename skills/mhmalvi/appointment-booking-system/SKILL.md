---
name: appointment-booking-system
description: 这是一个用于服务行业的通用预约预订和管理系统。系统支持预约的接收、确认、自动提醒（24小时/2小时间隔）、未到场的跟进处理，以及每日日程报告功能。系统内置了5个可立即使用的n8n工作流（workflows），并采用Google Sheets作为后端数据存储平台。
tags: [booking, appointments, scheduling, reminders, no-show, automation, n8n, google-sheets]
author: mhmalvi
version: 1.2.0
license: CC BY-NC-SA 4.0
metadata:
  clawdbot:
    emoji: "\U0001F4C5"
    requires:
      n8nCredentials: [google-sheets-oauth2, smtp]
      env: [BUSINESS_NAME, BUSINESS_PHONE, STAFF_EMAIL]
    os: [linux, darwin, win32]
---
# 预约管理系统

这是一个专为服务行业设计的完整预约预订和管理系统，支持预约接收、确认邮件发送、自动提醒、缺席检测以及每日日程报告等功能。

## 问题

服务行业（如美发沙龙、诊所、咨询公司、健身工作室）经常因客户缺席或预约安排混乱而损失收入。现有的预订平台通常每月收费30至100美元以上，且缺乏定制化功能；而手动提醒方式也不够可靠。

本系统提供自托管的预订管理服务，完全免费。

## 功能介绍

1. **预约接收**：通过Webhook API接收预约信息，验证填写的字段，生成唯一的预约ID，并将数据存储到Google Sheets中。
2. **确认通知**：立即向客户发送确认邮件，并通知工作人员。
3. **智能提醒**：自动发送24小时和2小时前的提醒通知。
4. **缺席处理**：检测客户缺席的情况，并发送重新预约的提醒邮件。
5. **每日日程**：每天早上发送包含当天和次日预约信息的邮件，同时提供每周统计报表。

## 包含的工作流程

| 编号 | 文件名 | 功能 |
| --- | --- | --- |
| 01 | `01-booking-intake.json` | 接收预约信息 → 验证数据 → 存储到Google Sheets → 向客户发送确认邮件 → 通知工作人员 |
| 02 | `02-booking-confirmation.json` | 通过Webhook更新预约状态（确认/取消） |
| 03 | `03-reminder-engine.json` | 每小时检查预约状态 → 自动发送24小时和2小时前的提醒 |
| 04 | `04-noshow-followup.json | 检查过去的预约记录 → 发送缺席提醒邮件 |
| 05 | `05-daily-schedule.json | 每天早上发送当日预约信息和每周统计报表 |

## 系统架构

```
Client books online (form/API)
    |
    v
Workflow 01: Booking Intake
    +-> Validate required fields
    +-> Generate booking ID
    +-> Save to Google Sheets
    +-> Email confirmation to client
    +-> Email notification to staff
    +-> Return booking ID

Status update (confirm/cancel):
    |
    v
Workflow 02: Booking Confirmation
    +-> Update status in Sheets

Hourly:
    |
    v
Workflow 03: Reminder Engine
    +-> Read confirmed appointments
    +-> Check: is appointment in 24h? -> send reminder
    +-> Check: is appointment in 2h? -> send reminder
    +-> Mark reminders as sent in Sheets

Every 2 hours:
    |
    v
Workflow 04: No-Show Followup
    +-> Check past appointments (1-48h ago)
    +-> IF no showed_up status -> mark as no-show
    +-> Send rescheduling email

Daily at 7 AM:
    |
    v
Workflow 05: Daily Schedule
    +-> Build today's and tomorrow's schedule tables
    +-> Calculate weekly stats (completed, no-shows, cancelled)
    +-> Email to staff
```

## 所需的n8n凭证

| 凭证类型 | 用途 | JSON中的占位符 |
| ---------------- | ---------- | --------------------- |
| Google Sheets OAuth2 | 预约数据存储 | `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` |
| SMTP | 发送确认邮件、提醒邮件和统计报表 | `YOUR_SMTP_CREDENTIAL_ID` |

## 环境变量

```bash
# Business Details (used in client-facing emails)
BUSINESS_NAME=Your Business Name
BUSINESS_PHONE=+1234567890
STAFF_EMAIL=staff@yourbusiness.com
```

> **注意：** Google Sheets的ID在流程配置文件中以`YOUR_BOOKING_SHEET_ID`的形式作为占位符存在（并非环境变量）。请在导入n8n后直接替换该值。

## 配置占位符

| 占位符 | 说明 |
| -------- | -------- |
| `YOUR_BOOKING_SHEET_ID` | 用于存储预约信息的Google Sheets表格ID |
| `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` | n8n使用的Google Sheets凭证ID |
| `YOUR_SMTP_CREDENTIAL_ID` | n8n使用的SMTP凭证ID |
| `YOUR_NOTIFICATION_EMAIL` | 用于接收日程报告的工作人员邮箱 |

## Google Sheets表格结构（预约信息）

| 列名 | 类型 | 说明 |
| -------- | ------ | ------------- |
| booking_id | 文本 | 唯一的预约ID（自动生成） |
| name | 文本 | 客户全名 |
| email | 文本 | 客户邮箱 |
| phone | 文本 | 客户电话 |
| service | 文本 | 服务类型（如理发、咨询） |
| date | 文本 | 预约日期（YYYY-MM-DD） |
| time | 文本 | 预约时间（HH:MM） |
| notes | 文本 | 客户备注 |
| status | 文本 | 预约状态（已确认/已取消/缺席/已完成） |
| showed_up | 布尔值 | 客户是否到场 |
| reminder_24h | 布尔值 | 是否发送了24小时前的提醒 |
| reminder_2h | 布尔值 | 是否发送了2小时前的提醒 |
| created_at | 字符串 | 预约创建时间 |

## 快速入门

### 1. 先决条件
- n8n版本2.4或更高（自托管环境）
- Google Sheets OAuth2凭证
- SMTP邮箱凭证

### 2. 创建预约表格
创建一个包含上述列的Google Sheets表格，并将标签命名为“Appointments”。

### 3. 导入并配置
将所有5个JSON文件导入n8n系统，并替换其中的`YOUR_*`占位符，同时设置相应的环境变量。

### 4. 测试预约功能
```bash
curl -X POST https://your-n8n.com/webhook/booking/new \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "+1234567890",
    "service": "Consultation",
    "date": "2026-03-10",
    "time": "14:00",
    "notes": "First visit"
  }'
```

## 使用场景

1. **美发沙龙**：为发型师提供预约接收、提醒及缺席客户跟踪功能。
2. **医疗/牙科诊所**：管理患者预约。
3. **咨询公司**：安排咨询会话，并自动发送提醒。
4. **健身工作室**：预订课程和个人训练服务。
5. **汽车修理店**：安排维修服务。

## 系统要求

- n8n版本2.4或更高（支持自托管或云部署）
- Google Sheets OAuth2凭证
- SMTP邮箱凭证