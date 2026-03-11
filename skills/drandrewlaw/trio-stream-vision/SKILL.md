---
name: trio-stream-vision
description: 使用自然语言分析任何YouTube直播或RTSP摄像头视频流——询问正在发生的事情、检测特定事件，或获取定期总结。该功能由Trio的“Reality as an API”视觉模型提供支持，可将任何直播视频URL转换为结构化、可操作的数据。只需粘贴视频流URL并描述您的需求即可。
homepage: https://docs.machinefi.com/api-reference/
license: Apache-2.0
metadata: {"openclaw":{"emoji":"📹","requires":{"env":["TRIO_API_KEY"],"anyBins":["curl","python3"]},"primaryEnv":"TRIO_API_KEY"}}
---
# Trio Stream Vision — 用自然语言分析任何直播内容

您可以粘贴 YouTube 直播链接、RTSP 摄像头流或 HLS 流，然后用简单的英语提问关于直播内容的问题。该服务能够检测事件、监控情况，并定期提供摘要，无需编写任何机器学习管道。该服务由 [Trio 的 Reality-as-an-API](https://machinefi.com) 提供支持。

## 使用场景

- 用户想了解摄像头、直播流或视频源中发生的情况（例如：“有人在我家门口吗？”）
- 用户希望针对特定事件接收智能提醒（例如：“当包裹送达时通知我”，“如果我的狗上了沙发请提醒我”）
- 用户需要监控自己无法直接观看的场景（如建筑工地、停车位、仓库）
- 用户希望定期获取直播内容的摘要（例如：“每 10 分钟总结一次直播内容”）
- 用户提供任何直播流链接：YouTube 直播、Twitch、RTSP/RTSPS 摄像头、HLS 流

## 先决条件

- 需要一个 Trio API 密钥。您可以在 [https://console.machinefi.com](https://console.machinefi.com) 免费获取 100 个信用点（100 credits）。
- 设置 API 密钥：`export TRIO_API_KEY=your_key_here`
- 基础 URL：`https://trio.machinefi.com/api`

## 可用功能

### 1. 一次性检查（快速概览）

询问关于直播内容当前情况的简单问题（是/否）。费用为 1 个信用点（0.01 美元）。

```bash
curl -s -X POST "https://trio.machinefi.com/api/check-once" \
  -H "Authorization: Bearer $TRIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "stream_url": "STREAM_URL_HERE",
    "condition": "NATURAL_LANGUAGE_CONDITION_HERE"
  }' | python3 -m json.tool
```

**可选参数：**
- `"include_frame": true` — 以 Base64 格式返回分析后的图片
- `"input_mode": "clip"` — 分析短视频片段而非单帧（更适合运动检测）
- `"clip_duration_seconds": 5` — 视频片段时长（1-10 秒，仅适用于 clip/hybrid 模式）

**响应字段：**
- `triggered` （布尔值） — 条件是否匹配
- `explanation` （字符串） — VLM 对观察结果的解析
- `latency_ms` — 处理时间（毫秒）

**输入模式建议：**
- 使用 `"frames"`（默认）来检测静态物体：例如：“车道上有车吗？”、“门开着吗？”
- 使用 `"clip"` 来检测运动或动作：例如：“有人在走路吗？”、“包裹送达了吗？”
- 使用 `"hybrid"` 可获得最高精度（费用更高）

### 2. 实时监控（持续事件检测）

持续监控直播流，并在条件满足时发送警报。费用为每分钟 2 个信用点（0.02 美元）。

```bash
curl -s -X POST "https://trio.machinefi.com/api/live-monitor" \
  -H "Authorization: Bearer $TRIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "stream_url": "STREAM_URL_HERE",
    "condition": "NATURAL_LANGUAGE_CONDITION_HERE",
    "interval_seconds": 10,
    "monitor_duration_seconds": 600,
    "max_triggers": 1
  }' | python3 -m json.tool
```

**可选参数：**
- `"webhook_url": "https://your-server.com/webhook"` — 在条件触发时接收 HTTP POST 通知
- `"interval_seconds": 10` — 检查间隔（5-300 秒）
- `"monitor_duration_seconds": 600` — 监控时长（至少 5 秒）
- `"trigger_cooldown_seconds": 60` — 触发之间的最小间隔（秒）
- `"max_triggers": null` — 设置为 null 以无限次触发
- `"input_mode": "clip"` — 实时监控的默认模式，适用于运动检测

**响应：** 返回一个 `job_id`。您可以使用该 ID 来检查任务状态或取消任务。

**结果传递方式（根据请求自动选择）：**
- 如果设置了 `webhook_url`，则事件会通过 webhook 发送
- 如果设置了 `Accept: text/event-stream` 头部字段（无 webhook），则通过 SSE 流传递
- 否则，通过 `GET /jobs/{job_id}` 来获取任务状态

### 3. 实时摘要（定期总结）

定期获取直播内容的叙述性摘要。费用为每分钟 2 个信用点（0.02 美元）。

```bash
curl -s -X POST "https://trio.machinefi.com/api/live-digest" \
  -H "Authorization: Bearer $TRIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "stream_url": "STREAM_URL_HERE",
    "window_minutes": 10,
    "capture_interval_seconds": 60
  }' | python3 -m json.tool
```

**可选参数：**
- `"window_minutes": 10` — 摘要窗口时长（1-60 分钟）
- `"capture_interval_seconds": 60` — 帧捕获频率（10-300 秒）
- `"webhook_url": "https://..."` — 通过 webhook 接收摘要
- `"max_windows": 3` — 停止前的摘要窗口数量
- `"include_frames": true` — 在摘要中嵌入图片

**响应：** 返回一个 `job_id`。

### 4. 检查任务状态

```bash
curl -s "https://trio.machinefi.com/api/jobs/JOB_ID_HERE" \
  -H "Authorization: Bearer $TRIO_API_KEY" | python3 -m json.tool
```

**任务状态：** `pending`（待处理）、`running`（运行中）、`stopped`（已停止）、`completed`（已完成）、`failed`（失败）

### 5. 列出所有任务

```bash
curl -s "https://trio.machinefi.com/api/jobs?limit=20&offset=0" \
  -H "Authorization: Bearer $TRIO_API_KEY" | python3 -m json.tool
```

**可选查询参数：** `status=running`、`type=live-monitor`、`limit=20`、`offset=0`

### 6. 取消任务

```bash
curl -s -X DELETE "https://trio.machinefi.com/api/jobs/JOB_ID_HERE" \
  -H "Authorization: Bearer $TRIO_API_KEY" | python3 -m json.tool
```

## 推荐的工作流程

### 快速检查流程
1. 使用用户的问题和直播链接运行一次性检查
2. 将 `triggered` 结果和 `explanation` 报告给用户
3. 如果 API 返回关于直播流的错误信息，显示错误内容及解决方法

### 监控流程
1. 先使用一次性检查来验证条件是否有效
2. 如果条件有效，设置合适的参数开始实时监控
3. 返回 `job_id` 并告知用户如何检查任务状态或取消任务
4. 如果有 webhook，设置它以接收推送通知

### 摘要生成流程
1. 使用直播链接和相应的窗口时长/间隔开始生成摘要
2. 返回 `job_id`，以便用户后续查看结果

## 条件编写技巧

- 将条件编写为二进制的是/否问题：例如：“画面中有人吗？”
- 表达要具体：例如：“建筑物屋顶有烟雾升起吗？”而不是“有烟雾吗？”
- 每个条件对应一个意图——不要合并多个检查
- 使用积极的语句：例如：“有车辆可见吗？”而不是“停车场是否空着？”
- 在开始实时监控之前，务必使用一次性检查来验证条件是否正确

## 错误处理

所有错误都会返回以下结构：
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "remediation": "Actionable fix suggestion"
  }
}
```

**常见错误代码：**
- `NOT_LIVESTREAM` — 链接不是直播流。请确认其正在播放。
- `STREAM_FETCH_FAILED` — 无法访问直播流。请检查链接和网络连接。
- `STREAM_OFFLINE` — 流已存在但处于离线状态。请等待其恢复在线。
- `MAX_JOBS_REACHED` — 并发任务数量达到上限。请使用 `DELETE /jobs/{id}` 取消旧任务。

如果遇到错误，请务必向用户显示 `remediation` 字段，其中包含可操作的解决方案。

## 价格参考

| 功能 | 费用 |
|--------|------|
| 一次性检查 | 0.01 美元/次 |
| 实时监控 | 0.02 美元/分钟 |
| 实时摘要 | 0.02 美元/分钟 |

**免费 tier：** 注册时可获得 100 个信用点（1.00 美元），网址：[https://console.machinefi.com](https://console.machinefi.com)

## 规则

- 绝不要在显示给用户的输出中暴露或记录 `$TRIO_API_KEY` 值。
- 必须始终显示一次性检查响应中的 `explanation` 字段——它提供了 VLM 的分析结果。
- 在开始实时监控任务之前，务必使用一次性检查来验证条件。
- 当用户提供直播流链接时，根据其意图自动判断用户是需要快速检查、实时监控还是生成摘要。
- 对于监控任务，务必返回 `job_id`，以便用户后续查看任务状态或取消任务。
- 如果 API 返回错误，请向用户显示错误代码及解决方法。
- 在开始实时监控或实时摘要任务之前，务必告知用户费用情况（按分钟计费）。