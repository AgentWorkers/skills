---
name: gong
description: Gong API 用于搜索通话记录、通话文字记录以及分析通话内容。适用于处理 Gong 的通话录音、销售对话、文字记录、会议数据或通话分析场景。该 API 支持列出通话记录、获取文字记录、管理用户信息以及查看活动统计信息。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎙️",
        "requires":
          {
            "config": ["~/.config/gong/credentials.json"],
          },
      },
  }
---

# Gong

访问Gong的对话智能功能——包括通话记录、通话文字记录、用户信息及分析数据。

## 设置

将凭据存储在`~/.config/gong/credentials.json`文件中：
```json
{
  "base_url": "https://us-XXXXX.api.gong.io",
  "access_key": "YOUR_ACCESS_KEY",
  "secret_key": "YOUR_SECRET_KEY"
}
```

从Gong获取凭据：进入“设置” → “生态系统” → “API” → “创建API密钥”。

## 认证

```bash
GONG_CREDS=~/.config/gong/credentials.json
GONG_BASE=$(jq -r '.base_url' $GONG_CREDS)
GONG_AUTH=$(jq -r '"\(.access_key):\(.secret_key)"' $GONG_CREDS | base64)

curl -s "$GONG_BASE/v2/endpoint" \
  -H "Authorization: Basic $GONG_AUTH" \
  -H "Content-Type: application/json"
```

## 核心操作

### 列出用户
```bash
curl -s "$GONG_BASE/v2/users" -H "Authorization: Basic $GONG_AUTH" | \
  jq '[.users[] | {id, email: .emailAddress, name: "\(.firstName) \(.lastName)"}]'
```

### 列出通话记录（可指定时间范围）
```bash
curl -s -X POST "$GONG_BASE/v2/calls/extensive" \
  -H "Authorization: Basic $GONG_AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "fromDateTime": "2025-01-01T00:00:00Z",
      "toDateTime": "2025-01-31T23:59:59Z"
    },
    "contentSelector": {}
  }' | jq '{
    total: .records.totalRecords,
    calls: [.calls[] | {
      id: .metaData.id,
      title: .metaData.title,
      started: .metaData.started,
      duration_min: ((.metaData.duration // 0) / 60 | floor),
      url: .metaData.url
    }]
  }'
```

### 获取通话文字记录
```bash
curl -s -X POST "$GONG_BASE/v2/calls/transcript" \
  -H "Authorization: Basic $GONG_AUTH" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"callIds": ["CALL_ID"]}}' | \
  jq '.callTranscripts[0].transcript[] | "\(.speakerName // "Speaker"): \(.sentences[].text)"' -r
```

### 获取通话详细信息
```bash
curl -s -X POST "$GONG_BASE/v2/calls/extensive" \
  -H "Authorization: Basic $GONG_AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"callIds": ["CALL_ID"]},
    "contentSelector": {"exposedFields": {"content": true, "parties": true}}
  }' | jq '.calls[0]'
```

### 活动统计
```bash
curl -s -X POST "$GONG_BASE/v2/stats/activity/aggregate" \
  -H "Authorization: Basic $GONG_AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "fromDateTime": "2025-01-01T00:00:00Z",
      "toDateTime": "2025-01-31T23:59:59Z"
    }
  }'
```

## 端点参考

| 端点          | 方法        | 用途                |
|--------------|------------|----------------------|
| `/v2/users`     | GET         | 列出所有用户             |
| `/v2/calls/extensive` | POST         | 列出/过滤通话记录         |
| `/v2/calls/transcript` | POST         | 获取通话文字记录         |
| `/v2/stats/activity/aggregate` | POST         | 获取活动统计数据         |
| `/v2/meetings`     | GET         | 查看已安排的会议           |

## 分页

响应中包含用于分页的游标信息：
```json
{"records": {"totalRecords": 233, "cursor": "eyJ..."}}
```

在后续请求中包含游标信息：`{"cursor": "eyJ..."}`

## 日期格式

```bash
# Last 7 days
FROM=$(date -v-7d +%Y-%m-%dT00:00:00Z 2>/dev/null || date -d "7 days ago" +%Y-%m-%dT00:00:00Z)
TO=$(date +%Y-%m-%dT23:59:59Z)
```

## 注意事项

- 请求速率限制：约3次/秒
- 通话ID以字符串形式表示（实际为较大的整数）
- 通话文字记录可能在通话结束后需要一段时间才能处理完成
- 日期格式遵循ISO 8601标准（例如：`2025-01-15T00:00:00Z`）