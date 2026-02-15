---
name: telnyx-voice-streaming-python
description: >-
  Stream call audio in real-time, fork media to external destinations, and
  transcribe speech live. Use for real-time analytics and AI integrations. This
  skill provides Python SDK examples.
metadata:
  author: telnyx
  product: voice-streaming
  language: python
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 语音流媒体服务 - Python

## 安装

```bash
pip install telnyx
```

## 设置

```python
import os
from telnyx import Telnyx

client = Telnyx(
    api_key=os.environ.get("TELNYX_API_KEY"),  # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 启动分叉流媒体传输

`POST /calls/{call_control_id}/actions/fork_start`  
（用于将通话中的媒体内容实时传输到指定目标。）

```python
response = client.calls.actions.start_forking(
    call_control_id="call_control_id",
)
print(response.data)
```

## 停止分叉流媒体传输

`POST /calls/{call_control_id}/actions/fork_stop`  
（用于停止分叉流媒体传输。）

```python
response = client.calls.actions.stop_forking(
    call_control_id="call_control_id",
)
print(response.data)
```

## 启动流媒体传输

`POST /calls/{call_control_id}/actions/streaming_start`  
（用于将通话中的媒体内容以接近实时的方式传输到指定的 WebSocket 地址或 Dialogflow 连接。）

```python
response = client.calls.actions.start_streaming(
    call_control_id="call_control_id",
)
print(response.data)
```

## 停止流媒体传输

`POST /calls/{call_control_id}/actions/streaming_stop`  
（用于停止向 WebSocket 的流媒体传输。）

```python
response = client.calls.actions.stop_streaming(
    call_control_id="call_control_id",
)
print(response.data)
```

## 启动实时转录

`POST /calls/{call_control_id}/actions/transcription_start`  
（用于启动实时转录功能。）

```python
response = client.calls.actions.start_transcription(
    call_control_id="call_control_id",
)
print(response.data)
```

## 停止实时转录

`POST /calls/{call_control_id}/actions/transcription_stop`  
（用于停止实时转录功能。）

```python
response = client.calls.actions.stop_transcription(
    call_control_id="call_control_id",
)
print(response.data)
```

---

## Webhook

以下 Webhook 事件会发送到您配置的 Webhook URL：
所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callForkStarted` | 分叉流媒体传输开始 |
| `callForkStopped` | 分叉流媒体传输停止 |
| `callStreamingStarted` | 流媒体传输开始 |
| `callStreamingStopped` | 流媒体传输停止 |
| `callStreamingFailed` | 流媒体传输失败 |
| `transcription` | 实时转录开始 |
| `transcriptionStopped` | 实时转录停止 |
```
```