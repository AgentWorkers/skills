---
name: telnyx-voice-media-javascript
description: >-
  Play audio files, use text-to-speech, and record calls. Use when building IVR
  systems, playing announcements, or recording conversations. This skill
  provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: voice-media
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Voice Media - JavaScript

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

以下所有示例均假设 `client` 已按照上述方式初始化。

## 播放音频 URL

在通话中播放音频文件。

`POST /calls/{call_control_id}/actions/playback_start`

```javascript
const response = await client.calls.actions.startPlayback('call_control_id');

console.log(response.data);
```

## 停止音频播放

停止通话中的音频播放。

`POST /calls/{call_control_id}/actions/playback_stop`

```javascript
const response = await client.calls.actions.stopPlayback('call_control_id');

console.log(response.data);
```

## 暂停录音

暂停通话的录音。

`POST /calls/{call_control_id}/actions/record_PAUSE`

```javascript
const response = await client.calls.actions.pauseRecording('call_control_id');

console.log(response.data);
```

## 恢复录音

恢复通话的录音。

`POST /calls/{call_control_id}/actions/record.resume`

```javascript
const response = await client.calls.actions.resumeRecording('call_control_id');

console.log(response.data);
```

## 开始录音

开始通话的录音。

`POST /calls/{call_control_id}/actions/record_start` — 必需参数：`format`, `channels`

```javascript
const response = await client.calls.actions.startRecording('call_control_id', {
  channels: 'single',
  format: 'wav',
});

console.log(response.data);
```

## 停止录音

停止通话的录音。

`POST /calls/{call_control_id}/actions/record_stop`

```javascript
const response = await client.calls.actions.stopRecording('call_control_id');

console.log(response.data);
```

## 将文本转换为语音并在通话中播放

将文本转换为语音并在通话中播放。

`POST /calls/{call_control_id}/actions/speak` — 必需参数：`payload`, `voice`

```javascript
const response = await client.calls.actions.speak('call_control_id', {
  payload: 'Say this on the call',
  voice: 'female',
});

console.log(response.data);
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL：
所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以用于验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callPlaybackStarted` | 通话播放开始 |
| `callPlaybackEnded` | 通话播放结束 |
| `callSpeakEnded` | 通话语音播放结束 |
| `callRecordingSaved` | 通话录音保存 |
| `callRecordingError` | 通话录音错误 |
| `callRecordingTranscriptionSaved` | 通话录音转录文件保存 |
| `callSpeakStarted` | 通话语音播放开始 |
```