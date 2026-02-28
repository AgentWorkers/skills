---
name: crm
version: 1.0.0
description: "**联系记录与交互日志**  
该功能能够记录所有通话中的来电者信息，详细记录每次对话的内容、结果以及相关背景信息。"
metadata: {"amber": {"capabilities": ["read", "act"], "confirmation_required": false, "timeout_ms": 3000, "permissions": {"local_binaries": [], "telegram": false, "openclaw_action": false, "network": false}, "function_schema": {"name": "crm", "description": "Manage contacts and interaction history. Use lookup_contact at the start of inbound calls (automatic, using caller ID) to check if the caller is known and retrieve their history and personal context. Use upsert_contact to save new information learned during calls (name, email, company) — do this silently, never announce it. Use log_interaction at the end of every call to record what happened (summary, outcome). Use context_notes to store and update personal details about the caller (pet names, preferences, mentioned life details, etc.) — update context_notes at the end of calls to synthesize new information with what was known before. NEVER ask robotic CRM questions. NEVER announce you are saving information. Capture what people naturally volunteer and remember it for next time.", "parameters": {"type": "object", "properties": {"action": {"type": "string", "enum": ["lookup_contact", "upsert_contact", "log_interaction", "get_history", "search_contacts", "tag_contact"], "description": "The CRM action to perform"}, "phone": {"type": "string", "description": "Contact phone number in E.164 format (e.g. +14165551234)", "pattern": "^\\+[1-9]\\d{6,14}$|^$"}, "name": {"type": "string", "maxLength": 200}, "email": {"type": "string", "maxLength": 200}, "company": {"type": "string", "maxLength": 200}, "context_notes": {"type": "string", "maxLength": 1000, "description": "Free-form personal context: pet names, preferences, life details, callback patterns. AI-maintained, rewritten after each call."}, "summary": {"type": "string", "maxLength": 500, "description": "One-liner: what the call was about"}, "outcome": {"type": "string", "enum": ["message_left", "appointment_booked", "info_provided", "callback_requested", "transferred", "other"], "description": "Call outcome"}, "details": {"type": "object", "description": "Structured extras as key-value pairs (e.g. appointment_date, purpose)"}, "query": {"type": "string", "maxLength": 200}, "limit": {"type": "integer", "minimum": 1, "maximum": 50, "default": 10}, "add": {"type": "array", "items": {"type": "string", "maxLength": 50}, "maxItems": 10}, "remove": {"type": "array", "items": {"type": "string", "maxLength": 50}, "maxItems": 10}}, "required": ["action"]}}}}
---
# CRM 功能——语音通话中的联系人信息管理

该功能能够记录所有通话中的来电者信息，并保存每次通话的详细内容。

## 工作原理

### 每个来电时

1. **查找联系人信息**：使用来电者的电话号码（来自 Twilio 的来电者 ID）通过 `crm` 函数调用 `lookup_contact` 方法进行查找。
2. **如果联系人信息已知**：根据姓名进行问候，并利用 `context_notes` 字段进行个性化交流（例如询问他们的宠物情况、记住他们的偏好等）。
3. **如果联系人信息未知**：按常规流程处理，等待来电者主动提供姓名。

### 通话过程中

当来电者提供姓名、电子邮件、公司名称或任何个人信息时，通过 `crm.upsert_contact` 方法将这些信息悄悄地更新到联系人数据库中。无需向来电者透露这一操作。

### 通话结束后

1. 记录通话内容：使用 `log_interaction` 方法记录通话的摘要和结果。
2. 更新 `context_notes` 字段，将新获取的个人信息与之前已知的资料合并。

### 每个呼出电话时

流程与来电时完全相同：通话开始时查找联系人信息，通话结束后更新联系人信息并记录通话记录。

## API 参考

| 功能 | 用途 |
|--------|---------|
| `lookup_contact` | 获取联系人信息、最近 5 次通话记录以及 `context_notes` 字段。若联系人不存在，则返回 null。 |
| `upsert_contact` | 根据电话号码创建或更新联系人信息。仅更新提供的字段。 |
| `log_interaction` | 记录通话详情（包括摘要和结果）。必要时会自动创建新的联系人记录。 |
| `get_history` | 获取某位联系人的历史通话记录（按时间顺序从最新到最早排列）。 |
| `search_contacts` | 根据姓名、电子邮件或公司名称搜索联系人。 |
| `tag_contact` | 为联系人添加或删除标签（例如 “vip” 或 “callback_later”）。 |

## 隐私保护

- **通话细节保密**：与日历功能类似，绝不向来电者透露任何通话细节。
- **CRM 数据为个人隐私**：`context_notes` 字段仅用于内部使用，不用于分享通话记录。
- **个人信息的存储**：电话号码、姓名、电子邮件、公司名称及 `context_notes` 字段均存储在本地 SQLite 数据库中。默认情况下不会通过网络传输数据，也不会连接到外部 CRM 系统。

## 安全性

- 使用同步的 SQLite（推荐使用 sqlite3）数据库，并采用参数化查询方式，有效防止 SQL 注入攻击。
- 系统会自动过滤来自匿名或被阻止号码的来电。
- 通过三层验证机制确保输入数据的合法性：模式匹配、处理函数验证以及数据库约束。
- 数据库文件以只读/写入模式（0600）创建，确保数据安全。

## 示例

**问候已知联系人：**
```
Amber: "Hi Sarah, good to hear from you again. How's Max doing?" 
[context_notes remembered: "Has a Golden Retriever named Max. Prefers afternoon calls."]
```

**悄悄记录新信息：**
```
Caller: "By the way, I got married last month!"
Amber: [silently calls upsert_contact + updates context_notes with "Recently married"]
Amber (aloud): "That's wonderful! Congrats!"
```

**通话结束后记录日志：**
```
Amber: [calls log_interaction: summary="Called to reschedule Friday appointment", outcome="appointment_booked"]
Amber: [calls upsert_contact with context_notes: "Prefers afternoon calls. Recently married. Reschedules frequently but always shows up."]
```