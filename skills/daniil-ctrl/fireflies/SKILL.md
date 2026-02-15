---
name: fireflies
description: 通过 GraphQL API 访问 Fireflies.ai 的会议记录、会议摘要、行动项以及分析数据
metadata: {"clawdbot":{"secrets":["FIREFLIES_API_KEY"]}}
---

# Fireflies.ai 技能

用于查询 Fireflies.ai 中的会议记录、摘要、待办事项和分析数据。

## 设置

设置您的 Fireflies API 密钥：
```bash
FIREFLIES_API_KEY=your_api_key_here
```

您可以从以下链接获取 API 密钥：https://app.fireflies.ai/integrations（滚动到 Fireflies API 部分）

## API 基础信息

GraphQL 端点：`https://api.fireflies.aigraphql`

授权头：`Bearer $FIREFLIES_API_KEY`

---

## 核心查询

### 获取当前用户

```bash
curl -s -X POST https://api.fireflies.ai/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -d '{"query":"{ user { user_id name email is_admin minutes_consumed num_transcripts recent_meeting } }"}' | jq
```

### 获取单条会议记录

```bash
curl -s -X POST https://api.fireflies.ai/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -d '{"query":"query($id:String!){transcript(id:$id){id title date duration participants fireflies_users summary{keywords action_items overview topics_discussed} speakers{name duration} sentences{speaker_name text start_time}}}","variables":{"id":"TRANSCRIPT_ID"}}' | jq
```

### 按日期范围搜索会议记录

```bash
# ISO 8601 format: YYYY-MM-DDTHH:mm:ss.sssZ
curl -s -X POST https://api.fireflies.ai/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -d '{"query":"query($from:DateTime,$to:DateTime,$limit:Int){transcripts(fromDate:$from,toDate:$to,limit:$limit){id title date duration organizer_email participants summary{keywords action_items overview}}}","variables":{"from":"2024-01-01T00:00:00.000Z","to":"2024-01-31T23:59:59.999Z","limit":50}}' | jq
```

### 按参与者搜索会议记录

```bash
# Search meetings where specific people participated
curl -s -X POST https://api.fireflies.ai/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -d '{"query":"query($participants:[String],$limit:Int){transcripts(participants:$participants,limit:$limit){id title date participants organizer_email summary{action_items}}}","variables":{"participants":["john@example.com","jane@example.com"],"limit":20}}' | jq
```

### 按组织者搜索会议记录

```bash
curl -s -X POST https://api.fireflies.ai/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -d '{"query":"query($organizers:[String],$limit:Int){transcripts(organizers:$organizers,limit:$limit){id title date organizer_email participants}}","variables":{"organizers":["sales@example.com"],"limit":25}}' | jq
```

### 按关键词（标题和/或会议内容）搜索会议记录

```bash
# scope: "TITLE", "SENTENCES", or "ALL"
curl -s -X POST https://api.fireflies.ai/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -d '{"query":"query($keyword:String,$scope:String){transcripts(keyword:$keyword,scope:$scope,limit:10){id title date summary{overview}}}","variables":{"keyword":"pricing","scope":"ALL"}}' | jq
```

### 获取我的近期会议记录

```bash
curl -s -X POST https://api.fireflies.ai/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -d '{"query":"{ transcripts(mine:true,limit:10) { id title date duration summary { action_items keywords } } }"}' | jq
```

---

## 高级查询

### 获取包含摘要和待办事项的完整会议记录

```bash
curl -s -X POST https://api.fireflies.ai/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -d '{"query":"query($id:String!){transcript(id:$id){id title date duration organizer_email participants fireflies_users workspace_users meeting_attendees{displayName email} summary{keywords action_items outline overview bullet_gist topics_discussed meeting_type} speakers{name duration word_count} sentences{speaker_name text start_time end_time}}}","variables":{"id":"TRANSCRIPT_ID"}}' | jq
```

### 获取包含分析数据的会议记录

```bash
# Requires Pro plan or higher
curl -s -X POST https://api.fireflies.ai/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -d '{"query":"query($id:String!){transcript(id:$id){id title analytics{sentiments{positive_pct neutral_pct negative_pct} speakers{name duration word_count filler_words questions longest_monologue words_per_minute}}}}","variables":{"id":"TRANSCRIPT_ID"}}' | jq
```

### 获取联系人信息

```bash
curl -s -X POST https://api.fireflies.ai/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -d '{"query":"{ contacts { email name picture last_meeting_date } }"}' | jq
```

### 获取正在进行的会议

```bash
curl -s -X POST https://api.fireflies.ai/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -d '{"query":"{ active_meetings { id title organizer_email meeting_link start_time state } }"}' | jq
```

---

## 示例：管道审查

获取过去 7 天内包含特定参与者的所有会议记录：

```bash
FROM_DATE=$(date -u -v-7d +"%Y-%m-%dT00:00:00.000Z")  # macOS
TO_DATE=$(date -u +"%Y-%m-%dT23:59:59.999Z")

curl -s -X POST https://api.fireflies.ai/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -d "{\"query\":\"query(\$from:DateTime,\$to:DateTime,\$participants:[String]){transcripts(fromDate:\\\"\$FROM_DATE\\\",toDate:\\\"\$TO_DATE\\\",participants:\$participants,limit:50){id title date duration organizer_email participants summary{keywords action_items topics_discussed meeting_type}}}\",\"variables\":{\"from\":\"$FROM_DATE\",\"to\":\"$TO_DATE\",\"participants\":[\"prospect@company.com\"]}}" | jq
```

---

## 关键数据结构字段

### 会议记录字段
- `id` - 唯一标识符
- `title` - 会议标题
- `date` - Unix 时间戳（毫秒）
- `dateString` - ISO 8601 格式的日期时间
- `duration` - 会议时长（分钟）
- `organizer_email` - 会议组织者邮箱
- `participants` - 所有参与者的邮箱
- `fireflies_users` - 参与的 Fireflies 用户
- `workspace_users` - 参与的团队成员
- `meeting_attendees` - 详细的参会者信息（显示名称、邮箱）
- `transcript_url` - 在仪表板上查看会议记录的链接
- `audio_url` - 下载音频文件（Pro+ 订阅者可用，有效期 24 小时）
- `video_url` - 下载视频文件（Business+ 订阅者可用，有效期 24 小时）

### 摘要字段
- `keywords` - 关键主题
- `action_items` - 提取的待办事项
- `overview` - 会议概述
- `topics_discussed` - 主要讨论的主题
- `meeting_type` - 会议类型
- `outline` - 结构化的会议大纲
- `bullet_gist` - 会议内容的要点总结

### 句子字段
- `text` - 句子文本
- `speaker_name` - 说话者名称
- `start_time` - 说话开始时间（秒）
- `end_time` - 说话结束时间
- `ai_filters` - 过滤条件（任务、问题、价格等）

### 演讲者字段
- `name` - 演讲者名称
- `duration` - 演讲时长
- `word_count` - 说话所用单词数
- `filler_words` - 闲聊或重复性话语的数量
- `questions` - 提出的问题数量
- `longest_monologue` - 最长的连续讲话时间
- `words_per_minute` - 每分钟的讲话速度

---

## 过滤示例

### 按日期范围（ISO 8601 格式）过滤

```json
{
  "fromDate": "2024-01-01T00:00:00.000Z",
  "toDate": "2024-01-31T23:59:59.999Z"
}
```

### 按多个参与者过滤

```json
{
  "participants": ["user1@example.com", "user2@example.com"]
}
```

### 按频道过滤

```json
{
  "channel_id": "channel_id_here"
}
```

### 综合过滤

```json
{
  "fromDate": "2024-01-01T00:00:00.000Z",
  "toDate": "2024-01-31T23:59:59.999Z",
  "participants": ["sales@example.com"],
  "keyword": "pricing",
  "scope": "ALL",
  "limit": 50
}
```

---

## PowerShell 示例

```powershell
$headers = @{
  "Authorization" = "Bearer $env:FIREFLIES_API_KEY"
  "Content-Type" = "application/json"
}

# Get recent transcripts
$body = @{
  query = "{ transcripts(mine:true,limit:10) { id title date } }"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.fireflies.ai/graphql" -Method POST -Headers $headers -Body $body
```

---

## 注意事项

- **速率限制**：请咨询 Fireflies 客服了解当前的请求限制。
- **分页**：对于大量数据，使用 `limit`（最多 50 条）和 `skip` 参数进行分页处理。
- **日期格式**：始终使用 ISO 8601 格式（例如：`YYYY-MM-DDTHH:mm:ss.sssZ`）。
- **音频/视频链接**：链接有效期为 24 小时，需要时可重新生成。
- **分析数据**：需要 Pro 订阅才能使用相关功能。
- **视频录制**：必须在仪表板设置中启用。

---

## 常见使用场景

1. **每周管道审查**：按日期和参与者搜索会议记录。
2. **后续任务**：从近期会议中提取待办事项。
3. **竞争对手提及**：在句子中搜索特定关键词。
4. **演讲分析**：分析演讲者的发言时间和提出的问题。
5. **会议洞察**：获取会议摘要和关键主题。