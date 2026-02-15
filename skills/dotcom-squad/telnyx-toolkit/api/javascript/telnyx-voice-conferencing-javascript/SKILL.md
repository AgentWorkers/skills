---
name: telnyx-voice-conferencing-javascript
description: >-
  Create and manage conference calls, queues, and multi-party sessions. Use when
  building call centers or conferencing applications. This skill provides
  JavaScript SDK examples.
metadata:
  author: telnyx
  product: voice-conferencing
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 语音会议 - JavaScript

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

## 将呼叫加入队列

将呼叫放入队列中。

`POST /calls/{call_control_id}/actions/enqueue` — 必需参数：`queue_name`

```javascript
const response = await client.calls.actions.enqueue('call_control_id', { queue_name: 'support' });

console.log(response.data);
```

## 从队列中移除呼叫

从队列中移除呼叫。

`POST /calls/{call_control_id}/actions/leave_queue`

```javascript
const response = await client.calls.actions.leaveQueue('call_control_id');

console.log(response.data);
```

## 列出会议

列出所有会议。

`GET /conferences`

```javascript
// Automatically fetches more pages as needed.
for await (const conference of client.conferences.list()) {
  console.log(conference.id);
}
```

## 创建会议

使用 `call_control_id` 和会议名称从现有的通话中创建会议。

`POST /conferences` — 必需参数：`call_control_id`, `name`

```javascript
const conference = await client.conferences.create({
  call_control_id: 'v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg',
  name: 'Business',
});

console.log(conference.data);
```

## 查找会议

检索现有的会议。

`GET /conferences/{id}`

```javascript
const conference = await client.conferences.retrieve('id');

console.log(conference.data);
```

## 暂停会议参与者的发言

暂停会议中所有参与者的发言。

`POST /conferences/{id}/actions/hold`

```javascript
const response = await client.conferences.actions.hold('id');

console.log(response.data);
```

## 加入会议

加入现有的通话以参与会议。

`POST /conferences/{id}/actions/join` — 必需参数：`call_control_id`

```javascript
const response = await client.conferences.actions.join('id', {
  call_control_id: 'v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg',
});

console.log(response.data);
```

## 退出会议

将通话从会议中移除并恢复到待处理状态。

`POST /conferences/{id}/actions/leave` — 必需参数：`call_control_id`

```javascript
const response = await client.conferences.actions.leave('id', {
  call_control_id: 'c46e06d7-b78f-4b13-96b6-c576af9640ff',
});

console.log(response.data);
```

## 静音会议参与者

静音会议中所有参与者。

`POST /conferences/{id}/actions/mute`

```javascript
const response = await client.conferences.actions.mute('id');

console.log(response.data);
```

## 向会议参与者播放音频

向会议中的所有或部分参与者播放音频。

`POST /conferences/{id}/actions/play`

```javascript
const response = await client.conferences.actions.play('id');

console.log(response.data);
```

## 暂停会议录制

暂停会议录制。

`POST /conferences/{id}/actions/record_PAUSE`

```javascript
const response = await client.conferences.actions.recordPause('id');

console.log(response.data);
```

## 恢复会议录制

恢复会议录制。

`POST /conferences/{id}/actions/record_resume`

```javascript
const response = await client.conferences.actions.recordResume('id');

console.log(response.data);
```

## 开始会议录制

开始会议录制。

`POST /conferences/{id}/actions/record_start` — 必需参数：`format`

```javascript
const response = await client.conferences.actions.recordStart('id', { format: 'wav' });

console.log(response.data);
```

## 停止会议录制

停止会议录制。

`POST /conferences/{id}/actions/record_stop`

```javascript
const response = await client.conferences.actions.recordStop('id');

console.log(response.data);
```

## 向会议参与者朗读文本

将文本转换为语音并播放给所有或部分参与者。

`POST /conferences/{id}/actions/speak` — 必需参数：`payload`, `voice`

```javascript
const response = await client.conferences.actions.speak('id', {
  payload: 'Say this to participants',
  voice: 'female',
});

console.log(response.data);
```

## 停止向会议参与者播放音频

停止向会议中的所有或部分参与者播放音频。

`POST /conferences/{id}/actions/stop`

```javascript
const response = await client.conferences.actions.stop('id');

console.log(response.data);
```

## 恢复会议参与者的发言权限

恢复会议中所有参与者的发言权限。

`POST /conferences/{id}/actions/unhold` — 必需参数：`call_control_ids`

```javascript
const response = await client.conferences.actions.unhold('id', {
  call_control_ids: ['v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg'],
});

console.log(response.data);
```

## 解除会议参与者的静音状态

解除会议中所有参与者的静音状态。

`POST /conferences/{id}/actions/unmute`

```javascript
const response = await client.conferences.actions.unmute('id');

console.log(response.data);
```

## 更新会议参与者信息

更新会议参与者的角色。

`POST /conferences/{id}/actions/update` — 必需参数：`call_control_id`, `supervisor_role`

```javascript
const action = await client.conferences.actions.update('id', {
  call_control_id: 'v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg',
  supervisor_role: 'whisper',
});

console.log(action.data);
```

## 列出会议参与者

列出会议中的所有参与者。

`GET /conferences/{conference_id}/participants`

```javascript
// Automatically fetches more pages as needed.
for await (const conferenceListParticipantsResponse of client.conferences.listParticipants(
  'conference_id',
)) {
  console.log(conferenceListParticipantsResponse.id);
}
```

---

## Webhook

以下 webhook 事件会被发送到您配置的 webhook 地址：
所有 webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 头部信息以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callEnqueued` | 呼叫被加入队列 |
| `callLeftQueue` | 呼叫离开队列 |
| `conferenceCreated` | 会议创建 |
| `conferenceEnded` | 会议结束 |
| `conferenceFloorChanged` | 会议主持人变更 |
| `conferenceParticipantJoined` | 会议参与者加入 |
| `conferenceParticipantLeft` | 会议参与者离开 |
| `conferenceParticipantPlaybackEnded` | 会议参与者停止发言 |
| `conferenceParticipantPlaybackStarted` | 会议参与者开始发言 |
| `conferenceParticipantSpeakEnded` | 会议参与者结束发言 |
| `conferenceParticipantSpeakStarted` | 会议参与者开始发言 |
| `conferencePlaybackEnded` | 会议播放结束 |
| `conferencePlaybackStarted` | 会议播放开始 |
| `conferenceRecordingSaved` | 会议录制保存 |
| `conferenceSpeakEnded` | 会议发言结束 |
| `conferenceSpeakStarted` | 会议发言开始 |
```
```