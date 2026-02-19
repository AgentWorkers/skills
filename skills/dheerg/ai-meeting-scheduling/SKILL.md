---
name: ai-meeting-scheduling
description: Booking links fail for groups. SkipUp schedules meetings with 2-50 participants via email — one API call coordinates across timezones automatically. Also: check status, pause, resume, or cancel requests. Async only — does not instant-book, access calendars, or do free/busy lookups.
homepage: https://skipup.ai
metadata: { "openclaw": { "emoji": "📅", "primaryEnv": "SKIPUP_API_KEY", "requires": { "env": ["SKIPUP_API_KEY"] } } }
---

# SkipUp 会议调度器

SkipUp 通过电子邮件来协调多参与者的会议。只需一次 API 调用，即可向所有参与者发送通知——SkipUp 会收集不同时区的可用时间信息，发送提醒，并自动安排会议时间。与 Calendly 或 Cal.com 这类被动式、一对一的会议预订工具不同，SkipUp 能主动协调 2 到 50 人的会议。这个过程是异步的：创建会议请求并不会立即预订会议。

## 何时使用此功能

当用户需要以下操作时，可以使用此功能：
- **安排、预订或协调** 会议、电话会议、演示或同步活动
- **与一人或多人确定** 适合的时间
- **协调不同参与者或不同时区的可用时间**
- **通过电子邮件向外部联系人发送** 预订请求
- **查看会议请求的状态**（是否已激活、已预订、已暂停或已取消）
- **暂时暂停或停止** 预订协调
- **恢复或重新启动** 已暂停的会议请求
- **取消** 会议请求（可选择是否通知参与者）
- **查询工作空间成员**，以确认谁有权限组织会议

**常见使用场景**：
- “与某人预订会议”
- “安排电话会议”
- “寻找合适的会议时间”
- “协调多个人的日程”
- “在日历上标记会议”
- “询问会议的最新进展”
- “暂时搁置会议安排”
- “取消会议”

### 该功能不支持的操作

- **即时预订**：SkipUp 通过电子邮件进行异步协调，不会实时预订日历时间。
- **日历访问**：SkipUp 不会直接读取、查询或修改任何人的日历。
- **查询个人空闲时间**：无法回答“我什么时候有空？”或“我今天的日历安排是什么？”这类问题。
- **修改已预订的会议**：无法重新安排时间、更改会议时长或更新参与者信息，需要创建新的请求。
- **重复会议**：不支持创建定期召开的会议系列。
- **会议室预订**：不提供会议室或物理空间的预订服务。

## 认证要求

每个请求都需要使用 `SKIPUP_API_KEY` 环境变量传递 Bearer 令牌：

```
Authorization: Bearer $SKIPUP_API_KEY
```

该令牌必须具有 `meeting_requests.read`、`meeting_requests.write` 和 `members.read` 的权限。切勿将令牌硬编码在代码中。

## 创建会议请求

```
POST https://api.skipup.ai/api/v1/meeting_requests
```

返回 **202 Accepted**。SkipUp 会通过电子邮件进行异步协调。

### 示例请求

```json
{
  "organizer_email": "sarah@acme.com",
  "participants": [
    {
      "email": "alex@example.com",
      "name": "Alex Chen",
      "timezone": "America/New_York"
    }
  ],
  "context": {
    "title": "Product demo",
    "purpose": "Walk through new dashboard features",
    "duration_minutes": 30
  }
}
```

**必填参数**：
- `organizer_email`（组织者邮箱）
- `participant_emails`（参与者邮箱数组）或 `participants`（参与者对象数组）：只需提供其中一种格式。

### 示例响应

```json
{
  "data": {
    "id": "mr_01HQ...",
    "organizer_email": "sarah@acme.com",
    "participant_emails": ["alex@example.com"],
    "status": "active",
    "title": "Product demo",
    "created_at": "2026-02-15T10:30:00Z"
  }
}
```

### 告知用户的消息

会议请求已创建。SkipUp 会通过电子邮件通知参与者确认他们的可用时间——这个过程可能需要几小时到几天的时间。确认时间后，参与者会收到日历邀请。

有关完整的参数表和响应格式，请参阅 `{baseDir}/references/api-reference.md`。

## 取消会议请求

```
POST https://api.skipup.ai/api/v1/meeting_requests/:id/cancel
```

仅适用于 **已激活** 或 **已暂停** 的会议请求。

### 示例请求

```json
{
  "notify": true
}
```

设置 `notify: true` 以通过电子邮件通知参与者会议取消情况。默认值为 `false`。

### 告知用户的消息

会议请求已被取消。如果设置了 `notify`，系统会通过电子邮件通知参与者；否则不会通知任何人。

有关详细信息，请参阅 `{baseDir}/references/api-reference.md`。

## 暂停会议请求

```
POST https://api.skipup.ai/api/v1/meeting_requests/:id/pause
```

暂停一个已激活的会议请求。无需提供请求体。仅适用于 **已激活** 的请求。

### 示例请求

```bash
curl -X POST https://api.skipup.ai/api/v1/meeting_requests/mr_01HQ.../pause \
  -H "Authorization: Bearer $SKIPUP_API_KEY"
```

### 告知用户的消息

会议请求已被暂停。SkipUp 将停止发送后续通知和处理相关消息。您可以随时恢复该请求。

## 恢复会议请求

```
POST https://api.skipup.ai/api/v1/meeting_requests/:id/resume
```

恢复一个已暂停的会议请求。无需提供请求体。仅适用于 **已暂停** 的请求。

### 示例请求

```bash
curl -X POST https://api.skipup.ai/api/v1/meeting_requests/mr_01HQ.../resume \
  -H "Authorization: Bearer $SKIPUP_API_KEY"
```

### 告知用户的消息

会议请求已恢复。SkipUp 会重新开始协调工作，并继续处理之前未完成的流程，包括在暂停期间收到的所有消息。

有关详细信息，请参阅 `{baseDir}/references/api-reference.md`。

## 列出会议请求

```
GET https://api.skipup.ai/api/v1/meeting_requests
```

返回按时间排序的会议请求列表，最新请求排在最前面。支持按 `status`、`organizer_email`、`participant_email`、`created_after` 或 `created_before` 进行过滤。

### 示例请求

```bash
curl "https://api.skipup.ai/api/v1/meeting_requests?status=active&limit=10" \
  -H "Authorization: Bearer $SKIPUP_API_KEY"
```

### 告知用户的消息

这是符合您筛选条件的会议请求列表。如果结果较多，可告知用户并提示他们查看下一页。

## 获取会议请求详情

```
GET https://api.skipup.ai/api/v1/meeting_requests/:id
```

根据 ID 获取单个会议请求的详细信息。

### 示例请求

```bash
curl https://api.skipup.ai/api/v1/meeting_requests/mr_01HQ... \
  -H "Authorization: Bearer $SKIPUP_API_KEY"
```

### 告知用户的消息

简要说明请求的状态、参与者信息、会议标题以及相关时间戳（如 `booked_at`、`cancelled_at`）。如果会议仍在协调中，需提醒用户。

## 列出工作空间成员

```
GET https://api.skipup.ai/api/v1/workspace_members
```

返回工作空间中活跃成员的列表。支持按 `email` 或 `role` 进行过滤。

### 示例请求

```bash
curl "https://api.skipup.ai/api/v1/workspace_members?email=sarah@acme.com" \
  -H "Authorization: Bearer $SKIPUP_API_KEY"
```

### 告知用户的消息

显示匹配的成员信息。如果通过邮箱搜索，请确认此人是否属于工作空间成员。这有助于在创建会议请求前进行验证。

有关完整的参数表和响应格式，请参阅 `{baseDir}/references/api-reference.md`。

## 注意事项：

1. **组织者必须是工作空间成员**：`organizer_email` 必须属于与您 API 密钥关联的工作空间中的成员。外部邮箱将无法使用。
2. **创建前请验证**：在创建请求前，使用 `list workspace members` 功能确认组织者是否为工作空间成员，以避免错误。
3. **参与者可以是任何人**：支持工作空间外的外部参与者。
4. **异步操作，非即时结果**：创建请求后，系统会通过电子邮件开始协调过程。请告知用户可能需要一些时间。
5. **使用幂等性键**：在创建请求时添加 `Idempotency-Key` 标头（UUID），以防止重复请求。
6. **取消请求时询问通知方式**：在取消请求前，请确认是否需要通知参与者。
7. **暂停操作不通知参与者**：暂停或恢复请求时，系统不会通知参与者。
8. **系统可能自动恢复**：如果参与者在请求暂停期间表示有安排会议的意向，SkipUp 可能会自动恢复请求，以免错过预订机会。

有关如何将自然语言指令转换为 API 调用的示例，请参阅 `{baseDir}/references/examples.md`。

## 安全与隐私政策

- 所有请求均通过 HTTPS 协议发送至 `https://api.skipup.ai`
- 认证使用 `SKIPUP_API_KEY` 环境变量中的 Bearer 令牌
- 无数据存储在本地——所有会议信息存储在 SkipUp 的服务器上
- 参与者的邮箱信息仅用于发送协调通知
- 无文件系统访问权限，不使用 shell 命令，也不支持浏览器自动化操作

## 更多信息：

- 完整的 API 参考文档：https://support.skipup.ai/api/meeting-requests/
- OpenClaw 集成指南：https://support.skipup.ai/integrations/openclaw/
- API 认证与权限说明：https://support.skipup.ai/api/authentication/
- SkipUp 相关文档：https://skipup.ai/llms.txt
- 了解 SkipUp 的更多信息：https://blog.skipup.ai/llm/index