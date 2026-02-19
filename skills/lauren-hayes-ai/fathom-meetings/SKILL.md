---
name: fathom
description: 您可以通过 Fathom API 访问 Fathom AI 的会议记录、会议纪要、会议总结以及会议中的待办事项。当用户询问会议笔记、电话会议总结、会议中的待办事项，或与 Fathom 录音相关的任何内容时，都可以使用该 API。此外，该 API 还可用于将 Fathom 数据同步到日历中，或构建会议责任追踪工作流程。
---
# Fathom

从 Fathom AI 记事本中提取会议记录、文字记录、会议摘要和待办事项。

## 设置

将 API 密钥保存在 `~/.openclaw/secrets/fathom.env` 文件中：
```
FATHOM_API_KEY=your-api-key-here
FATHOM_WEBHOOK_SECRET=your-webhook-secret-here
```

从 Fathom 获取 API 密钥的方法：设置 → 集成 → API → 生成密钥。

## API 参考

基础 URL：`https://api.fathom.ai/external/v1`
认证头：`X-Api-Key: <FATHOM_API_KEY>`

### 列出会议

```bash
curl "https://api.fathom.ai/external/v1/meetings?limit=20" \
  -H "X-Api-Key: $FATHOM_API_KEY"
```

关键查询参数：
- `limit`（1-100，默认值为 10）
- `created_after` / `created_before`（ISO 8601 格式）
- `recorded_by[]`（用于筛选记录者的电子邮件）
- `include_transcript=true`（包含完整文字记录）
- `include_action_items=true`（包含待办事项）
- `include_summary=true`（包含会议摘要）

响应格式：
```json
{
  "items": [{
    "title": "Meeting Name",
    "meeting_title": "Calendar Event Name",
    "url": "https://fathom.video/calls/123",
    "share_url": "https://fathom.video/share/abc",
    "created_at": "2026-02-17T20:00:00Z",
    "scheduled_start_time": "...",
    "scheduled_end_time": "...",
    "recording_start_time": "...",
    "recording_end_time": "...",
    "recording_id": 123,
    "transcript": "...",
    "default_summary": "...",
    "action_items": ["..."],
    "calendar_invitees": [{"name": "...", "email": "...", "is_external": true}],
    "recorded_by": {"name": "...", "email": "..."}
  }],
  "next_cursor": "..."
}
```

### 分页

在后续请求中将响应中的 `next_cursor` 作为 `cursor` 参数使用。

### 将 Fathom 会议与日历同步

可以通过时间重叠（会议开始时间在日历事件时间窗口内 ± 15 分钟）或标题相似度来匹配会议。`calendarInvitees` 字段显示了被邀请的人员；`is_external` 标志表示非组织内部的参与者。

## 常见工作流程

### 从最近的会议中提取待办事项

```bash
source ~/.openclaw/secrets/fathom.env
curl -s "https://api.fathom.ai/external/v1/meetings?include_action_items=true&limit=20" \
  -H "X-Api-Key: $FATHOM_API_KEY"
```

### 获取指定日期范围内的完整文字记录

```bash
curl -s "https://api.fathom.ai/external/v1/meetings?include_transcript=true&created_after=2026-02-17T00:00:00Z&created_before=2026-02-18T00:00:00Z" \
  -H "X-Api-Key: $FATHOM_API_KEY"
```

### 仅过滤外部会议

在获取会议信息后，筛选出至少有一个 `calendarInvitees` 字段值为 `is_external: true` 的会议，或者检查 `calendarInviteesDomainsType` 字段是否为 `"one_or_more_external"`。

### 同步脚本（日历 + Fathom → 数据库）

请参考 `scripts/sync-fathom.js` 脚本，该脚本可完成以下操作：
1. 更新 Google OAuth 令牌
2. 获取指定日期范围内的 Google 日历事件
3. 提取包含待办事项的 Fathom 会议信息
4. 将 Fathom 会议记录与日历事件进行匹配
5. 将所有数据同步到 Supabase（或其他数据库）

请根据实际需求调整数据库层的设计。

## Webhook

当会议记录完成后，Fathom 可以向您的端点发送 POST 请求。请使用 `FATHOM_WEBHOOK_SECRET` 进行验证，以实现实时同步（而非轮询）。

## 提示：
- Fathom 生成的待办事项为人工智能生成的结果，请仔细核对准确性。
- `recorded_by` 字段显示的是运行 Fathom 工具的团队成员，不一定是会议的组织者。
- 如果多个团队成员对同一会议使用了 Fathom 工具，可能会导致记录重复，可以通过匹配 `scheduled_start_time` 和相似的会议标题来消除重复记录。
- 如果使用团队 API 密钥，API 会返回所有团队成员的会议信息。