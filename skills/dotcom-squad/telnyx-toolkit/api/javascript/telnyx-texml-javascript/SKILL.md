---
name: telnyx-texml-javascript
description: >-
  Build voice applications using TeXML markup language (TwiML-compatible).
  Manage applications, calls, conferences, recordings, queues, and streams. This
  skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: texml
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Texml - JavaScript

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

## 列出所有 TeXML 应用程序

返回您的所有 TeXML 应用程序列表。

`GET /texml_applications`

```javascript
// Automatically fetches more pages as needed.
for await (const texmlApplication of client.texmlApplications.list()) {
  console.log(texmlApplication.id);
}
```

## 创建一个 TeXML 应用程序

创建一个新的 TeXML 应用程序。

`POST /texml_applications` — 必需参数：`friendly_name`、`voice_url`

```javascript
const texmlApplication = await client.texmlApplications.create({
  friendly_name: 'call-router',
  voice_url: 'https://example.com',
});

console.log(texmlApplication.data);
```

## 获取 TeXML 应用程序的详细信息

获取现有 TeXML 应用程序的详细信息。

`GET /texml_applications/{id}`

```javascript
const texmlApplication = await client.texmlApplications.retrieve('1293384261075731499');

console.log(texmlApplication.data);
```

## 更新 TeXML 应用程序

更新现有 TeXML 应用程序的设置。

`PATCH /texml_applications/{id}` — 必需参数：`friendly_name`、`voice_url`

```javascript
const texmlApplication = await client.texmlApplications.update('1293384261075731499', {
  friendly_name: 'call-router',
  voice_url: 'https://example.com',
});

console.log(texmlApplication.data);
```

## 删除 TeXML 应用程序

删除一个 TeXML 应用程序。

`DELETE /texml_applications/{id}`

```javascript
const texmlApplication = await client.texmlApplications.delete('1293384261075731499');

console.log(texmlApplication.data);
```

## 获取多个通话记录

获取某个账户的所有通话记录。

`GET /texml/Accounts/{account_sid}/Calls`

```javascript
const response = await client.texml.accounts.calls.retrieveCalls('account_sid');

console.log(response.calls);
```

## 发起出站通话

发起一个出站 TeXML 通话。

`POST /texml/Accounts/{account_sid}/Calls` — 必需参数：`To`、`From`、`ApplicationSid`

```javascript
const response = await client.texml.accounts.calls.calls('account_sid', {
  ApplicationSid: 'example-app-sid',
  From: '+13120001234',
  To: '+13121230000',
});

console.log(response.from);
```

## 获取特定通话的详细信息

根据通话 ID 获取该通话的详细信息。

`GET /texml/Accounts/{account_sid}/Calls/{call_sid}`

```javascript
const call = await client.texml.accounts.calls.retrieve('call_sid', { account_sid: 'account_sid' });

console.log(call.account_sid);
```

## 更新通话记录

更新特定通话的记录信息。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}`

```javascript
const call = await client.texml.accounts.calls.update('call_sid', { account_sid: 'account_sid' });

console.log(call.account_sid);
```

## 列出会议参与者

列出会议参与者信息。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants`

```javascript
const response = await client.texml.accounts.conferences.participants.retrieveParticipants(
  'conference_sid',
  { account_sid: 'account_sid' },
);

console.log(response.end);
```

## 拨打电话给会议参与者

拨打指定会议参与者的电话。

`POST /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants`

```javascript
const response = await client.texml.accounts.conferences.participants.participants(
  'conference_sid',
  { account_sid: 'account_sid' },
);

console.log(response.account_sid);
```

## 获取会议参与者信息

获取会议参与者的详细信息。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label}`

```javascript
const participant = await client.texml.accounts.conferences.participants.retrieve(
  'call_sid_or_participant_label',
  { account_sid: 'account_sid', conference_sid: 'conference_sid' },
);

console.log(participant.account_sid);
```

## 更新会议参与者信息

更新会议参与者的信息。

`POST /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label}`

```javascript
const participant = await client.texml.accounts.conferences.participants.update(
  'call_sid_or_participant_label',
  { account_sid: 'account_sid', conference_sid: 'conference_sid' },
);

console.log(participant.account_sid);
```

## 删除会议参与者

删除会议参与者。

`DELETE /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label}`

```javascript
await client.texml.accounts.conferences.participants.delete('call_sid_or_participant_label', {
  account_sid: 'account_sid',
  conference_sid: 'conference_sid',
});
```

## 列出会议资源

列出所有会议资源。

`GET /texml/Accounts/{account_sid}/Conferences`

```javascript
const response = await client.texml.accounts.conferences.retrieveConferences('account_sid');

console.log(response.conferences);
```

## 获取会议资源信息

获取特定会议的资源信息。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}`

```javascript
const conference = await client.texml.accounts.conferences.retrieve('conference_sid', {
  account_sid: 'account_sid',
});

console.log(conference.account_sid);
```

## 更新会议资源

更新会议资源信息。

`POST /texml/Accounts/{account_sid}/Conferences/{conference_sid}`

```javascript
const conference = await client.texml.accounts.conferences.update('conference_sid', {
  account_sid: 'account_sid',
});

console.log(conference.account_sid);
```

## 列出队列资源

列出所有队列资源。

`GET /texml/Accounts/{account_sid}/Queues`

```javascript
// Automatically fetches more pages as needed.
for await (const queueListResponse of client.texml.accounts.queues.list('account_sid')) {
  console.log(queueListResponse.account_sid);
}
```

## 创建新队列

创建一个新的队列资源。

`POST /texml/Accounts/{account_sid}/Queues`

```javascript
const queue = await client.texml.accounts.queues.create('account_sid');

console.log(queue.account_sid);
```

## 获取队列资源信息

获取特定队列的资源信息。

`GET /texml/Accounts/{account_sid}/Queues/{queue_sid}`

```javascript
const queue = await client.texml.accounts.queues.retrieve('queue_sid', {
  account_sid: 'account_sid',
});

console.log(queue.account_sid);
```

## 更新队列资源

更新队列资源信息。

`POST /texml/Accounts/{account_sid}/Queues/{queue_sid}`

```javascript
const queue = await client.texml.accounts.queues.update('queue_sid', {
  account_sid: 'account_sid',
});

console.log(queue.account_sid);
```

## 删除队列资源

删除队列资源。

`DELETE /texml/Accounts/{account_sid}/Queues/{queue_sid}`

```javascript
await client.texml.accounts.queues.delete('queue_sid', { account_sid: 'account_sid' });
```

## 获取多个录音资源

获取某个账户的所有录音资源。

`GET /texml/Accounts/{account_sid}/Recordings.json`

```javascript
const response = await client.texml.accounts.retrieveRecordingsJson('account_sid');

console.log(response.end);
```

## 获取特定录音资源

根据录音 ID 获取录音资源信息。

`GET /texml/Accounts/{account_sid}/Recordings/{recording_sid}.json`

```javascript
const texmlGetCallRecordingResponseBody =
  await client.texml.accounts.recordings.json.retrieveRecordingSidJson(
    '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
    { account_sid: 'account_sid' },
  );

console.log(texmlGetCallRecordingResponseBody.account_sid);
```

## 删除录音资源

根据录音 ID 删除录音资源。

`DELETE /texml/Accounts/{account_sid}/Recordings/{recording_sid}.json`

```javascript
await client.texml.accounts.recordings.json.deleteRecordingSidJson(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
  { account_sid: 'account_sid' },
);
```

## 获取通话的录音记录

根据通话 ID 获取该通话的录音记录。

`GET /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings.json`

```javascript
const response = await client.texml.accounts.calls.recordingsJson.retrieveRecordingsJson(
  'call_sid',
  { account_sid: 'account_sid' },
);

console.log(response.end);
```

## 为通话请求录音

根据通话 ID 启动录音。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings.json`

```javascript
const response = await client.texml.accounts.calls.recordingsJson.recordingsJson('call_sid', {
  account_sid: 'account_sid',
});

console.log(response.account_sid);
```

## 更新通话中的录音记录

更新特定通话的录音资源信息。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings/{recording_sid}.json`

```javascript
const response = await client.texml.accounts.calls.recordings.recordingSidJson(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
  { account_sid: 'account_sid', call_sid: 'call_sid' },
);

console.log(response.account_sid);
```

## 列出会议录音记录

列出所有会议录音记录。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Recordings`

```javascript
const response = await client.texml.accounts.conferences.retrieveRecordings('conference_sid', {
  account_sid: 'account_sid',
});

console.log(response.end);
```

## 获取会议录音记录

根据会议 ID 获取该会议的录音记录。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Recordings.json`

```javascript
const response = await client.texml.accounts.conferences.retrieveRecordingsJson('conference_sid', {
  account_sid: 'account_sid',
});

console.log(response.end);
```

## 创建 TeXML 密钥

创建一个 TeXML 密钥，该密钥可在使用 Mustache 模板时作为动态参数使用。

`POST /texml/secrets` — 必需参数：`name`、`value`

```javascript
const response = await client.texml.secrets({ name: 'My Secret Name', value: 'My Secret Value' });

console.log(response.data);
```

## 为通话请求 SIPREC 会话

根据通话 ID 启动 SIPREC 会话。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Siprec.json`

```javascript
const response = await client.texml.accounts.calls.siprecJson('call_sid', {
  account_sid: 'account_sid',
});

console.log(response.account_sid);
```

## 更新通话中的 SIPREC 会话

更新特定通话的 SIPREC 会话信息。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Siprec/{siprec_sid}.json`

```javascript
const response = await client.texml.accounts.calls.siprec.siprecSidJson('siprec_sid', {
  account_sid: 'account_sid',
  call_sid: 'call_sid',
});

console.log(response.account_sid);
```

## 从通话中开始流媒体传输

开始将媒体流传输到指定的 WebSocket 地址。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Streams.json`

```javascript
const response = await client.texml.accounts.calls.streamsJson('call_sid', {
  account_sid: 'account_sid',
});

console.log(response.account_sid);
```

## 更新通话中的流媒体资源

更新特定通话的流媒体资源信息。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Streams/{streaming_sid}.json`

```javascript
const response = await client.texml.accounts.calls.streams.streamingSidJson(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
  { account_sid: 'account_sid', call_sid: 'call_sid' },
);

console.log(response.account_sid);
```

## 获取多个录音转录文件

获取某个账户的所有录音转录文件。

`GET /texml/Accounts/{account_sid}/Transcriptions.json`

```javascript
const response = await client.texml.accounts.retrieveTranscriptionsJson('account_sid');

console.log(response.end);
```

## 获取特定录音的转录文件

根据转录文件 ID 获取其详细信息。

`GET /texml/Accounts/{account_sid}/Transcriptions/{recording_transcription_sid}.json`

```javascript
const response =
  await client.texml.accounts.transcriptions.json.retrieveRecordingTranscriptionSidJson(
    '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
    { account_sid: 'account_sid' },
  );

console.log(response.account_sid);
```

## 删除录音转录文件

永久删除录音转录文件。

`DELETE /texml/Accounts/{account_sid}/Transcriptions/{recording_transcription_sid}.json`

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `TexmlCallAnsweredWebhook` | TeXML 通话已接听。当 TeXML 通话被接听时发送此 Webhook |
| `TexmlCallCompletedWebhook` | TeXML 通话已完成。当 TeXML 通话结束时发送此 Webhook |
| `TexmlCallInitiatedWebhook` | TeXML 通话已发起。当 TeXML 通话开始时发送此 Webhook |
| `TexmlCallRingingWebhook` | TeXML 通话正在振铃。当 TeXML 通话正在振铃时发送此 Webhook |
| `TexmlCallAmdWebhook` | TeXML 通话中的自动应答机检测（AMD）完成时发送此 Webhook |
| `TexmlCallDtmfWebhook` | TeXML 通话中接收到 DTMF 数字时发送此 Webhook |
| `TexmlGatherWebhook` | TeXML 收集操作完成时发送此 Webhook（发送到指定的动作 URL） |
| `TexmlHttpRequestWebhook` | TeXML HTTP 请求响应时发送此 Webhook |
| `TexmlAiGatherWebhook` | AI 收集操作完成并生成转录结果时发送此 Webhook |
| `TexmlConferenceJoinWebhook` | 会议参与者加入时发送此 Webhook |
| `TexmlConferenceLeaveWebhook` | 会议参与者离开时发送此 Webhook |
| `TexmlConferenceSpeakerWebhook` | 会议参与者开始或停止发言时发送此 Webhook |
| `TexmlConferenceEndWebhook` | 会议结束时发送此 Webhook |
| `TexmlConferenceStartWebhook` | 会议开始时发送此 Webhook |
| `TexmlQueueWebhook` | 队列状态事件触发时发送此 Webhook（由 `Enqueue` 命令触发） |
| `TexmlRecordingCompletedWebhook` | 通话中的录音完成时发送此 Webhook（由 `recordingStatusCallbackEvent` 触发） |
| `TexmlRecordingInProgressWebhook` | 通话中的录音开始时发送此 Webhook（由 `recordingStatusCallbackEvent` 触发） |
| `TexmlSiprecWebhook` | SIPREC 会话状态更新时发送此 Webhook |
| `TexmlStreamWebhook` | 流媒体传输状态更新时发送此 Webhook |
| `TexmlTranscriptionWebhook` | 录音转录完成时发送此 Webhook |
```
```