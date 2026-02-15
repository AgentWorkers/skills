---
name: telnyx-voice-media-java
description: >-
  Play audio files, use text-to-speech, and record calls. Use when building IVR
  systems, playing announcements, or recording conversations. This skill
  provides Java SDK examples.
metadata:
  author: telnyx
  product: voice-media
  language: java
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Voice Media - Java

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

以下所有示例均假设 `client` 已按上述方式初始化。

## 播放音频 URL

在通话中播放音频文件。

`POST /calls/{call_control_id}/actions/playback_start`

```java
import com.telnyx.sdk.models.calls.actions.ActionStartPlaybackParams;
import com.telnyx.sdk.models.calls.actions.ActionStartPlaybackResponse;

ActionStartPlaybackResponse response = client.calls().actions().startPlayback("call_control_id");
```

## 停止音频播放

停止通话中的音频播放。

`POST /calls/{call_control_id}/actions/playback_stop`

```java
import com.telnyx.sdk.models.calls.actions.ActionStopPlaybackParams;
import com.telnyx.sdk.models.calls.actions.ActionStopPlaybackResponse;

ActionStopPlaybackResponse response = client.calls().actions().stopPlayback("call_control_id");
```

## 暂停录音

暂停通话的录音。

`POST /calls/{call_control_id}/actions/record_PAUSE`

```java
import com.telnyx.sdk.models.calls.actions.ActionPauseRecordingParams;
import com.telnyx.sdk.models.calls.actions.ActionPauseRecordingResponse;

ActionPauseRecordingResponse response = client.calls().actions().pauseRecording("call_control_id");
```

## 恢复录音

恢复通话的录音。

`POST /calls/{call_control_id}/actions/record_resume`

```java
import com.telnyx.sdk.models.calls.actions.ActionResumeRecordingParams;
import com.telnyx.sdk.models.calls.actions.ActionResumeRecordingResponse;

ActionResumeRecordingResponse response = client.calls().actions().resumeRecording("call_control_id");
```

## 开始录音

开始通话的录音。

`POST /calls/{call_control_id}/actions/record_start` — 必需参数：`format`、`channels`

```java
import com.telnyx.sdk.models.calls.actions.ActionStartRecordingParams;
import com.telnyx.sdk.models.calls.actions.ActionStartRecordingResponse;

ActionStartRecordingParams params = ActionStartRecordingParams.builder()
    .callControlId("call_control_id")
    .channels(ActionStartRecordingParams.Channels.SINGLE)
    .format(ActionStartRecordingParams.Format.WAV)
    .build();
ActionStartRecordingResponse response = client.calls().actions().startRecording(params);
```

## 停止录音

停止通话的录音。

`POST /calls/{call_control_id}/actions/record_stop`

```java
import com.telnyx.sdk.models.calls.actions.ActionStopRecordingParams;
import com.telnyx.sdk.models.calls.actions.ActionStopRecordingResponse;
import com.telnyx.sdk.models.calls.actions.StopRecordingRequest;

ActionStopRecordingParams params = ActionStopRecordingParams.builder()
    .callControlId("call_control_id")
    .stopRecordingRequest(StopRecordingRequest.builder().build())
    .build();
ActionStopRecordingResponse response = client.calls().actions().stopRecording(params);
```

## 语音合成

将文本转换为语音并在通话中播放。

`POST /calls/{call_control_id}/actions/speak` — 必需参数：`payload`、`voice`

```java
import com.telnyx.sdk.models.calls.actions.ActionSpeakParams;
import com.telnyx.sdk.models.calls.actions.ActionSpeakResponse;

ActionSpeakParams params = ActionSpeakParams.builder()
    .callControlId("call_control_id")
    .payload("Say this on the call")
    .voice("female")
    .build();
ActionSpeakResponse response = client.calls().actions().speak(params);
```

---

## Webhook

以下 webhook 事件会被发送到您配置的 webhook URL。所有 webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 头部字段以供验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callPlaybackStarted` | 通话录音开始 |
| `callPlaybackEnded` | 通话录音结束 |
| `callSpeakEnded` | 通话语音合成结束 |
| `callRecordingSaved` | 通话录音保存 |
| `callRecordingError` | 通话录音出现错误 |
| `callRecordingTranscriptionSaved` | 通话录音转录文件保存 |
| `callSpeakStarted` | 通话语音合成开始 |
```
```