---
name: telnyx-voice-streaming-javascript
description: >-
  Stream call audio in real-time, fork media to external destinations, and
  transcribe speech live. Use for real-time analytics and AI integrations. This
  skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: voice-streaming
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 语音流媒体服务 - JavaScript

## 安装

```bash
npm install telnyx
```

## 设置

```javascript
import Telnyx from 'telnyx';

const client = new Telnyx({
  apiKey: process.env['TELNYX_API_KEY'], // This is the default and can be omitted
});
```

以下所有示例均假设 `client` 已经按照上述方式初始化。

## 启动分叉流媒体传输

分叉流媒体传输功能允许您将通话中的媒体内容实时传输到指定的目标。

`POST /calls/{call_control_id}/actions/fork_start`

```javascript
const response = await client.calls.actions.startForking('call_control_id');

console.log(response.data);
```

## 停止分叉流媒体传输

停止对通话的分叉流媒体传输。

`POST /calls/{call_control_id}/actions/fork_stop`

```javascript
const response = await client.calls.actions.stopForking('call_control_id');

console.log(response.data);
```

## 启动流媒体传输

将通话中的媒体内容以接近实时的方式传输到指定的 WebSocket 地址或 Dialogflow 连接。

`POST /calls/{call_control_id}/actions/streaming_start`

```javascript
const response = await client.calls.actions.startStreaming('call_control_id');

console.log(response.data);
```

## 停止流媒体传输

停止将通话中的媒体内容传输到 WebSocket。

`POST /calls/{call_control_id}/actions/streaming_stop`

```javascript
const response = await client.calls.actions.stopStreaming('call_control_id');

console.log(response.data);
```

## 启动实时转录

开始实时转录通话内容。

`POST /calls/{call_control_id}/actions/transcription_start`

```javascript
const response = await client.calls.actions.startTranscription('call_control_id');

console.log(response.data);
```

## 停止实时转录

停止实时转录通话内容。

`POST /calls/{call_control_id}/actions/transcription_stop`

```javascript
const response = await client.calls.actions.stopTranscription('call_control_id');

console.log(response.data);
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 头部信息以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callForkStarted` | 通话分叉传输开始 |
| `callForkStopped` | 通话分叉传输停止 |
| `callStreamingStarted` | 通话流媒体传输开始 |
| `callStreamingStopped` | 通话流媒体传输停止 |
| `callStreamingFailed` | 通话流媒体传输失败 |
| `transcription` | 实时转录开始 |
```
```