---
name: dex-crm
description: |
  Manage Dex personal CRM (getdex.com) contacts, notes, and reminders.
  Use when you need to: (1) Search or browse contacts, (2) Add notes about people,
  (3) Create or check reminders, (4) Look up contact details (phone, email, birthday).
  Requires DEX_API_KEY environment variable.
---

# Dex 个人 CRM

您可以直接通过 Clawdbot 管理您的 Dex CRM 系统，执行诸如搜索联系人、添加备注、管理提醒等操作。

## 认证

请在网关配置的环境变量中设置 `DEX_API_KEY`。

## API 基础信息

- **基础 URL：** `https://api.getdex.com/api/rest`
- **请求头：** `Content-Type: application/json` 以及 `x-hasura-dex-api-key: $DEX_API_KEY`

## 快速参考

### 联系人

```bash
# List contacts (paginated)
curl -s -H "Content-Type: application/json" \
  -H "x-hasura-dex-api-key: $DEX_API_KEY" \
  "https://api.getdex.com/api/rest/contacts?limit=10&offset=0"

# Get contact by ID
curl -s -H "Content-Type: application/json" \
  -H "x-hasura-dex-api-key: $DEX_API_KEY" \
  "https://api.getdex.com/api/rest/contacts/{contactId}"

# Search contact by email
curl -s -H "Content-Type: application/json" \
  -H "x-hasura-dex-api-key: $DEX_API_KEY" \
  "https://api.getdex.com/api/rest/search/contacts?email=someone@example.com"

# Create contact
curl -s -X POST -H "Content-Type: application/json" \
  -H "x-hasura-dex-api-key: $DEX_API_KEY" \
  -d '{"first_name":"John","last_name":"Doe","emails":["john@example.com"]}' \
  "https://api.getdex.com/api/rest/contacts"

# Update contact
curl -s -X PUT -H "Content-Type: application/json" \
  -H "x-hasura-dex-api-key: $DEX_API_KEY" \
  -d '{"job_title":"CEO"}' \
  "https://api.getdex.com/api/rest/contacts/{contactId}"

# Delete contact
curl -s -X DELETE -H "Content-Type: application/json" \
  -H "x-hasura-dex-api-key: $DEX_API_KEY" \
  "https://api.getdex.com/api/rest/contacts/{contactId}"
```

### 备注（时间线项目）

```bash
# List notes
curl -s -H "Content-Type: application/json" \
  -H "x-hasura-dex-api-key: $DEX_API_KEY" \
  "https://api.getdex.com/api/rest/timeline_items?limit=10&offset=0"

# Notes for a contact
curl -s -H "Content-Type: application/json" \
  -H "x-hasura-dex-api-key: $DEX_API_KEY" \
  "https://api.getdex.com/api/rest/timeline_items/contacts/{contactId}"

# Create note
curl -s -X POST -H "Content-Type: application/json" \
  -H "x-hasura-dex-api-key: $DEX_API_KEY" \
  -d '{"note":"Met for coffee, discussed project","contact_ids":["contact-uuid"],"event_time":"2026-01-27T12:00:00Z"}' \
  "https://api.getdex.com/api/rest/timeline_items"

# Update note
curl -s -X PUT -H "Content-Type: application/json" \
  -H "x-hasura-dex-api-key: $DEX_API_KEY" \
  -d '{"note":"Updated note text"}' \
  "https://api.getdex.com/api/rest/timeline_items/{noteId}"

# Delete note
curl -s -X DELETE -H "Content-Type: application/json" \
  -H "x-hasura-dex-api-key: $DEX_API_KEY" \
  "https://api.getdex.com/api/rest/timeline_items/{noteId}"
```

### 提醒

```bash
# List reminders
curl -s -H "Content-Type: application/json" \
  -H "x-hasura-dex-api-key: $DEX_API_KEY" \
  "https://api.getdex.com/api/rest/reminders?limit=10&offset=0"

# Create reminder
curl -s -X POST -H "Content-Type: application/json" \
  -H "x-hasura-dex-api-key: $DEX_API_KEY" \
  -d '{"body":"Follow up on proposal","due_at_date":"2026-02-01","contact_ids":["contact-uuid"]}' \
  "https://api.getdex.com/api/rest/reminders"

# Update reminder
curl -s -X PUT -H "Content-Type: application/json" \
  -H "x-hasura-dex-api-key: $DEX_API_KEY" \
  -d '{"is_complete":true}' \
  "https://api.getdex.com/api/rest/reminders/{reminderId}"

# Delete reminder
curl -s -X DELETE -H "Content-Type: application/json" \
  -H "x-hasura-dex-api-key: $DEX_API_KEY" \
  "https://api.getdex.com/api/rest/reminders/{reminderId}"
```

## 联系人字段

- `first_name`（名字）
- `last_name`（姓氏）
- `job_title`（职位）
- `description`（备注）
- `emails`（`{email}` 类型的数组）
- `phones`（`{phone_number}` 类型的数组）
- `education`（教育背景）
- `website`（网站）
- `linkedin`（领英链接）
- `facebook`（Facebook 账号）
- `twitter`（Twitter 账号）
- `instagram`（Instagram 账号）
- `telegram`（Telegram 账号）
- `birthday`（生日）
- `image_url`（头像链接）
- `last_seen_at`（最后查看时间）
- `next_reminder_at`（下一个提醒时间）
- `is_archived`（是否已归档）
- `created_at`（创建时间）
- `updated_at`（更新时间）

## 搜索联系人

该 API 仅支持通过电子邮件进行搜索。如需通过姓名搜索联系人，请分批次获取结果并在本地进行过滤。建议设置合理的搜索数量限制（50-100条）以便于浏览。

## 备注

- 在创建、更新或删除联系人/备注/提醒之前，请务必先进行确认。
- 通过姓名搜索联系人时需要在本地进行过滤（API 仅支持电子邮件搜索）。
- 对于大量结果，建议使用分页功能（通过 `limit` 和 `offset` 参数进行分页显示）。
- 备注中的 `event_time` 字段表示交互发生的时间，而非备注创建的时间。