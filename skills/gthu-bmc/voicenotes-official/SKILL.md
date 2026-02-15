---
name: voicenotes
description: 这项由 Voicenotes 团队提供的官方技能使 OpenClaw 能够访问新的 API，实现语义搜索、检索完整的语音记录、按标签或时间范围进行过滤，以及创建文本笔记——所有这些功能都通过自然语言对话来完成。

homepage: https://voicenotes.com
metadata:
  openclaw:
    emoji: "📝"
    requires:
      env:
        - VOICENOTES_API_KEY
    primaryEnv: VOICENOTES_API_KEY
---

# Voicenotes

使用 Voicenotes 技能可以创建、搜索和检索用户的笔记。

## 设置

1. 在 https://voicenotes.com/app?open-claw=true#settings 创建一个集成。
2. 复制 API 密钥。
3. 进行配置：

**Webchat：** 在侧边栏中选择 “Skills” → “Voicenotes” → “API Key”。
**终端：** 将配置添加到您的 OpenClaw 配置文件（`~/.openclaw/config.yaml`）中：
```yaml
skills:
  voicenotes:
    env:
      VOICENOTES_API_KEY: "your_key_here"
```

或者直接导出配置文件：
```bash
export VOICENOTES_API_KEY="your_key_here"
```

配置完成后，API 密钥将作为 `$VOICENOTES_API_KEY` 环境变量可用。

## API 基础知识

所有请求都需要包含 `Authorization` 头部信息：
```bash
curl -X GET "https://api.voicenotes.com/api/integrations/open-claw/..." \
  -H "Authorization: $VOICENOTES_API_KEY"
```

## 常用操作

**在用户笔记中搜索：**

查询参数：
- `query`（必填）：搜索查询字符串

```bash
curl -X GET "https://api.voicenotes.com/api/integrations/open-claw/search/semantic?query={search_query}" \
  -H "Authorization: $VOICENOTES_API_KEY"
```

**根据标签和日期范围获取多个 Voicenotes：**

查询参数：
- `tags`（可选）：有效的标签数组
- `date_range`（可选）：包含开始和结束时间的 UTC 时间戳数组

```bash
curl -X POST "https://api.voicenotes.com/api/integrations/open-claw/recordings" \
  -H "Authorization: $VOICENOTES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tags": ["tag1", "tag2"],
    "date_range": ["2026-01-01T00:00:00.000000Z", "2026-02-01T00:00:00.000000Z"]
  }'
```

**如需更多上下文信息，可以获取完整的转录内容：**

```bash
curl "https://api.voicenotes.com/api/integrations/open-claw/recordings/{recording_uuid}" \
  -H "Authorization: $VOICENOTES_API_KEY" \
```

**在 Voicenotes 中创建文本笔记：**

```bash
curl -X POST "https://api.voicenotes.com/api/integrations/open-claw/recordings/new" \
  -H "Authorization: $VOICENOTES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "recording_type": 3,
    "transcript": "note content here",
    "device_info": "open-claw"
  }'
```

## 响应结构

**语义搜索响应：**

返回按相关性排序的笔记及其片段数组：

```json
[
  {
    "type": "note",
    "uuid": "NTHiJljf",
    "title": "Quick idea about project",
    "transcript": "Full transcript text with <br> for line breaks...",
    "tags": ["idea", "project"],
    "created_at": "2025-01-15T10:30:00.000000Z"
  },
  {
    "type": "note_split",
    "uuid": "8JzkhEGh",
    "title": "Long meeting notes",
    "transcript": "Relevant chunk from a larger note...",
    "tags": ["meeting"],
    "created_at": "2025-01-14T09:00:00.000000Z"
  },
  {
    "type": "import_split",
    "uuid": "xYz12345",
    "title": "filename.extension",
    "transcript": "Chunk from an imported note...",
    "tags": ["imported"],
    "created_at": "2025-01-10T14:00:00.000000Z"
  }
]
```

- `type: "note"`：与搜索内容完全匹配的笔记。
- `type: "note_split"`：来自较长笔记的片段；如需获取完整转录内容，请使用 `uuid`。
- `type: "import_split"`：来自导入笔记的片段；标题即为文件名；**无法** 通过 `/recordings/{uuid}` 获取该片段。
- `transcript` 可能包含 HTML 格式的内容（如 `<br>`、`<b>`）。

**获取录音响应（支持过滤）：**

返回符合过滤条件的笔记（分页显示）：

```json
{
  "data": [
    {
      "id": "bTZI5t12",
      "title": null,
      "transcript": "this is a sample note",
      "duration": 0,
      "recorded_at": "2026-02-06T10:07:45.000000Z",
      "created_at": "2026-02-06T10:07:45.000000Z",
      "recording_type": 3,
      "tags": []
    }
  ],
  "links": {
    "first": "https://api.voicenotes.com/api/integrations/open-claw/recordings?page=1",
    "last": null,
    "prev": null,
    "next": null
  },
  "meta": {
    "current_page": 1,
    "from": 1,
    "path": "https://api.voicenotes.com/api/integrations/open-claw/recordings",
    "per_page": 10,
    "to": 1
  }
}
```

关键字段：
- `data`：录音对象数组。
- `links.next`：下一页的 URL（如果没有更多页面，则为 `null`）。
- `meta.per_page`：每页显示的结果数量（默认为 10）。

**获取录音详情响应：**

返回完整的笔记信息：

```json
{
  "data": {
    "id": "NTHiJljf",
    "title": "Meeting Connectivity Check",
    "transcript": "Full transcript text...",
    "duration": 12101,
    "recorded_at": "2025-08-07T09:50:14.000000Z",
    "created_at": "2025-08-07T09:50:14.000000Z",
    "recording_type": 2,
    "tags": ["meeting"],
    "subnotes": [],
    "attachments": []
  }
}
```

关键字段：
- `id`：笔记的 UUID。
- `transcript`：完整文本（会议记录中包含 `[HH:MM:SS] Speaker N:` 的时间戳）。
- `duration`：录音时长（以毫秒为单位）。
- `recording_type`：1=语音笔记，2=语音会议，3=文本笔记。
- `tags`：包含 `name` 字段的标签对象数组。

**创建笔记响应：**

```json
{
  "message": "Recording audio uploaded successfully!",
  "recording": {
    "id": "bPI3RcUP",
    "recording_id": "bPI3RcUP",
    "title": null,
    "transcript": "Sample note",
    "recording_type": 3,
    "created_at": "2026-02-04T08:51:29.000000Z",
    "tags": []
  }
}
```

关键字段：
- `message`：操作成功确认信息。
- `recording.id`：新创建笔记的 UUID。
- `recording.transcript`：笔记内容。

## 注意事项

- 笔记的 ID 为 UUID。
- 平均每秒请求次数限制约为 3 次。