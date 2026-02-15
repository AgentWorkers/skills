---
name: loom
description: 管理 Loom 视频录制：通过 Loom API 查看列表、分享视频以及获取分析数据。
metadata: {"clawdbot":{"emoji":"🎥","requires":{"env":["LOOM_API_KEY"]}}}
---

# Loom

一个视频消息平台。

## 环境

```bash
export LOOM_API_KEY="xxxxxxxxxx"
```

## 列出视频

```bash
curl "https://api.loom.com/v1/videos" \
  -H "Authorization: Bearer $LOOM_API_KEY"
```

## 获取视频详情

```bash
curl "https://api.loom.com/v1/videos/{video_id}" \
  -H "Authorization: Bearer $LOOM_API_KEY"
```

## 获取视频字幕

```bash
curl "https://api.loom.com/v1/videos/{video_id}/transcript" \
  -H "Authorization: Bearer $LOOM_API_KEY"
```

## 更新视频

```bash
curl -X PATCH "https://api.loom.com/v1/videos/{video_id}" \
  -H "Authorization: Bearer $LOOM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "privacy": "public"}'
```

## 删除视频

```bash
curl -X DELETE "https://api.loom.com/v1/videos/{video_id}" \
  -H "Authorization: Bearer $LOOM_API_KEY"
```

## 获取分析数据

```bash
curl "https://api.loom.com/v1/videos/{video_id}/insights" \
  -H "Authorization: Bearer $LOOM_API_KEY"
```

## 链接
- 仪表板：https://www.loom.com/looms
- 文档：https://dev.loom.com