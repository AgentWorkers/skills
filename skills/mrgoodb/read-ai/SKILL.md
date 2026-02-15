---
name: read-ai
description: 您可以从 Read.ai 获取会议摘要、记录和待办事项。通过 API，您还可以获得由人工智能支持的会议分析结果。
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"env":["READAI_API_KEY"]}}}
---

# Read.ai

一款具备转录和会议总结功能的AI会议助手。

## 环境配置
```bash
export READAI_API_KEY="xxxxxxxxxx"
```

## 会议列表
```bash
curl "https://api.read.ai/v1/meetings" \
  -H "Authorization: Bearer $READAI_API_KEY"
```

## 获取会议详情
```bash
curl "https://api.read.ai/v1/meetings/{meeting_id}" \
  -H "Authorization: Bearer $READAI_API_KEY"
```

## 获取会议记录
```bash
curl "https://api.read.ai/v1/meetings/{meeting_id}/transcript" \
  -H "Authorization: Bearer $READAI_API_KEY"
```

## 获取会议总结
```bash
curl "https://api.read.ai/v1/meetings/{meeting_id}/summary" \
  -H "Authorization: Bearer $READAI_API_KEY"
```

## 获取待办事项
```bash
curl "https://api.read.ai/v1/meetings/{meeting_id}/action-items" \
  -H "Authorization: Bearer $READAI_API_KEY"
```

## 获取会议关键议题
```bash
curl "https://api.read.ai/v1/meetings/{meeting_id}/topics" \
  -H "Authorization: Bearer $READAI_API_KEY"
```

## 搜索会议
```bash
curl "https://api.read.ai/v1/meetings/search?query=project%20update" \
  -H "Authorization: Bearer $READAI_API_KEY"
```

## 主要功能：
- 支持对Zoom、Teams和Meet等会议平台的自动转录功能
- 由AI生成的会议总结
- 自动提取会议中的待办事项
- 识别会议发言者
- 进行情感分析

## 链接：
- 仪表盘：https://app.read.ai
- 文档：https://docs.read.ai