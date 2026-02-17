---
name: kvcore-mcp-cli
description: 当用户需要通过 MCP/CLI 执行 KVcore CRM 操作（如联系人管理、标签设置、备注记录、电话通话、电子邮件发送、短信发送以及活动管理）时，请使用此技能。该技能支持直接访问原始 API 端点，并提供可选的 Twilio 通话回退机制。
---
# KVcore MCP/CLI 技能

使用此技能可通过聊天界面执行 KVcore 客户关系管理（CRM）操作。

## 环境要求

必备参数：
- `KVCORE_API_TOKEN`

可选参数：
- `KVCORE_BASE_URL`（默认值：`https://api.kvcore.com`）
- `KVCORE_TIMEOUT_MS`
- `TWILIO_ACCOUNT_sid`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_FROM_NUMBER`

## MCP 服务器

相关函数/命令：
```bash
npm run dev:kvcore-mcp
```

主要使用的工具：
- `kvcore_contact_search`：搜索联系人
- `kvcore_contact_get`：获取联系人信息
- `kvcore_contact_create`：创建联系人
- `kvcore_contact_update`：更新联系人信息
- `kvcore_contact_tag_add`：为联系人添加标签
- `kvcore_contact_tag_remove`：删除联系人标签
- `kvcore_note_add`：添加备注
- `kvcore_call_log`：记录通话记录
- `kvcore_call_schedule`：安排通话
- `kvcore_email_send`：发送电子邮件
- `kvcore_text_send`：发送短信
- `kvcore_user_tasks`：管理用户任务
- `kvcore_user_calls`：查看用户通话记录
- `kvcore_campaigns_refresh`：刷新营销活动信息
- `kvcore_request`：直接访问原始 API 端点
- `twilio_call_create`：用于发起外拨通话（备用功能）

## CLI（命令行接口）

相关命令：
```bash
npm run build
```

示例用法：
```bash
node packages/kvcore-cli/dist/index.js contact search --query "john smith" --pretty
node packages/kvcore-cli/dist/index.js email:send --contact-id 123 --subject "Quick update" --body "Following up" --pretty
node packages/kvcore-cli/dist/index.js text:send --contact-id 123 --body "Can we connect today?" --pretty
node packages/kvcore-cli/dist/index.js call:schedule --json '{"contact_id":123,"user_id":456,"scheduled_at":"2026-02-15 10:00:00"}' --pretty
node packages/kvcore-cli/dist/index.js call:twilio --to "+14165550001" --twiml "<Response><Say>Hello</Say></Response>" --pretty
```

## 功能说明

KVcore 公共 API v2 支持以下功能：
- 管理联系人信息
- 记录通话记录
- 发送电子邮件/短信
- 安排通话
- 查看用户任务和通话记录
- 刷新营销活动信息

对于尚未实现封装的 API 端点，可以直接使用 `kvcore_request` 或 CLI 命令进行操作。