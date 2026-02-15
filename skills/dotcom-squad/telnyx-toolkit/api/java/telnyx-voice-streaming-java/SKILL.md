---
name: telnyx-voice-streaming-java
description: >-
  Stream call audio in real-time, fork media to external destinations, and
  transcribe speech live. Use for real-time analytics and AI integrations. This
  skill provides Java SDK examples.
metadata:
  author: telnyx
  product: voice-streaming
  language: java
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 语音流媒体服务 - Java

## 安装

```text
// See https://github.com/team-telnyx/telnyx-java for Maven/Gradle setup
```

## 设置

```java
import com.telnyx.sdk.client.TelnyxClient;
import com.telnyx.sdk.client.okhttp.TelnyxOkHttpClient;

TelnyxClient client = TelnyxOkHttpClient.fromEnv();
```

以下所有示例均假设 `client` 已按照上述方式初始化完成。

## 启动分叉流媒体传输

分叉流媒体传输功能允许您将通话中的媒体内容实时传输到指定的目标地址。

`POST /calls/{call_control_id}/actions/fork_start`

```java
import com.telnyx.sdk.models.calls.actions.ActionStartForkingParams;
import com.telnyx.sdk.models.calls.actions.ActionStartForkingResponse;

ActionStartForkingResponse response = client.calls().actions().startForking("call_control_id");
```

## 停止分叉流媒体传输

停止对通话内容的流媒体传输。

`POST /calls/{call_control_id}/actions/fork_stop`

```java
import com.telnyx.sdk.models.calls.actions.ActionStopForkingParams;
import com.telnyx.sdk.models.calls.actions.ActionStopForkingResponse;

ActionStopForkingResponse response = client.calls().actions().stopForking("call_control_id");
```

## 启动流媒体传输

将通话中的媒体内容以接近实时的方式传输到指定的 WebSocket 地址或 Dialogflow 连接。

`POST /calls/{call_control_id}/actions/streaming_start`

```java
import com.telnyx.sdk.models.calls.actions.ActionStartStreamingParams;
import com.telnyx.sdk.models.calls.actions.ActionStartStreamingResponse;

ActionStartStreamingResponse response = client.calls().actions().startStreaming("call_control_id");
```

## 停止流媒体传输

停止将通话内容传输到 WebSocket。

`POST /calls/{call_control_id}/actions/streaming_stop`

```java
import com.telnyx.sdk.models.calls.actions.ActionStopStreamingParams;
import com.telnyx.sdk.models.calls.actions.ActionStopStreamingResponse;

ActionStopStreamingResponse response = client.calls().actions().stopStreaming("call_control_id");
```

## 启动实时转录

开始实时转录通话内容。

`POST /calls/{call_control_id}/actions/transcription_start`

```java
import com.telnyx.sdk.models.calls.actions.ActionStartTranscriptionParams;
import com.telnyx.sdk.models.calls.actions.ActionStartTranscriptionResponse;
import com.telnyx.sdk.models.calls.actions.TranscriptionStartRequest;

ActionStartTranscriptionParams params = ActionStartTranscriptionParams.builder()
    .callControlId("call_control_id")
    .transcriptionStartRequest(TranscriptionStartRequest.builder().build())
    .build();
ActionStartTranscriptionResponse response = client.calls().actions().startTranscription(params);
```

## 停止实时转录

停止实时转录通话内容。

`POST /calls/{call_control_id}/actions/transcription_stop`

```java
import com.telnyx.sdk.models.calls.actions.ActionStopTranscriptionParams;
import com.telnyx.sdk.models.calls.actions.ActionStopTranscriptionResponse;

ActionStopTranscriptionResponse response = client.calls().actions().stopTranscription("call_control_id");
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL：
所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

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