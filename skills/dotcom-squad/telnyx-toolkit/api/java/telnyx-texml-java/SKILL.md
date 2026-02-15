---
name: telnyx-texml-java
description: >-
  Build voice applications using TeXML markup language (TwiML-compatible).
  Manage applications, calls, conferences, recordings, queues, and streams. This
  skill provides Java SDK examples.
metadata:
  author: telnyx
  product: texml
  language: java
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 本文档由 Telnyx OpenAPI 规范自动生成，请勿修改。 |

# Telnyx Texml - Java

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

以下所有示例均假设 `client` 已经按照上述方式初始化。

## 列出所有 TeXML 应用程序

返回您的所有 TeXML 应用程序列表。

`GET /texml_applications`

```java
import com.telnyx.sdk.models.texmlapplications.TexmlApplicationListPage;
import com.telnyx.sdk.models.texmlapplications.TexmlApplicationListParams;

TexmlApplicationListPage page = client.texmlApplications().list();
```

## 创建一个 TeXML 应用程序

创建一个新的 TeXML 应用程序。

`POST /texml_applications` — 必需参数：`friendly_name`, `voice_url`

```java
import com.telnyx.sdk.models.texmlapplications.TexmlApplicationCreateParams;
import com.telnyx.sdk.models.texmlapplications.TexmlApplicationCreateResponse;

TexmlApplicationCreateParams params = TexmlApplicationCreateParams.builder()
    .friendlyName("call-router")
    .voiceUrl("https://example.com")
    .build();
TexmlApplicationCreateResponse texmlApplication = client.texmlApplications().create(params);
```

## 获取 TeXML 应用程序的详细信息

检索现有 TeXML 应用程序的详细信息。

`GET /texml_applications/{id}`

```java
import com.telnyx.sdk.models.texmlapplications.TexmlApplicationRetrieveParams;
import com.telnyx.sdk.models.texmlapplications.TexmlApplicationRetrieveResponse;

TexmlApplicationRetrieveResponse texmlApplication = client.texmlApplications().retrieve("1293384261075731499");
```

## 更新 TeXML 应用程序

更新现有 TeXML 应用程序的设置。

`PATCH /texml_applications/{id}` — 必需参数：`friendly_name`, `voice_url`

```java
import com.telnyx.sdk.models.texmlapplications.TexmlApplicationUpdateParams;
import com.telnyx.sdk.models.texmlapplications.TexmlApplicationUpdateResponse;

TexmlApplicationUpdateParams params = TexmlApplicationUpdateParams.builder()
    .id("1293384261075731499")
    .friendlyName("call-router")
    .voiceUrl("https://example.com")
    .build();
TexmlApplicationUpdateResponse texmlApplication = client.texmlApplications().update(params);
```

## 删除 TeXML 应用程序

删除一个 TeXML 应用程序。

`DELETE /texml_applications/{id}`

```java
import com.telnyx.sdk.models.texmlapplications.TexmlApplicationDeleteParams;
import com.telnyx.sdk.models.texmlapplications.TexmlApplicationDeleteResponse;

TexmlApplicationDeleteResponse texmlApplication = client.texmlApplications().delete("1293384261075731499");
```

## 获取账户的所有通话记录

返回账户的所有通话记录。

`GET /texml/Accounts/{account_sid}/Calls`

```java
import com.telnyx.sdk.models.texml.accounts.calls.CallRetrieveCallsParams;
import com.telnyx.sdk.models.texml.accounts.calls.CallRetrieveCallsResponse;

CallRetrieveCallsResponse response = client.texml().accounts().calls().retrieveCalls("account_sid");
```

## 发起一个出站通话

发起一个出站 TeXML 通话。

`POST /texml/Accounts/{account_sid}/Calls` — 必需参数：`To`, `From`, `ApplicationSid`

```java
import com.telnyx.sdk.models.texml.accounts.calls.CallCallsParams;
import com.telnyx.sdk.models.texml.accounts.calls.CallCallsResponse;

CallCallsParams params = CallCallsParams.builder()
    .accountSid("account_sid")
    .applicationSid("example-app-sid")
    .from("+13120001234")
    .to("+13121230000")
    .build();
CallCallsResponse response = client.texml().accounts().calls().calls(params);
```

## 获取特定通话的详细信息

根据通话 ID 获取该通话的详细信息。

`GET /texml/Accounts/{account_sid}/Calls/{call_sid}`

```java
import com.telnyx.sdk.models.texml.accounts.calls.CallRetrieveParams;
import com.telnyx.sdk.models.texml.accounts.calls.CallRetrieveResponse;

CallRetrieveParams params = CallRetrieveParams.builder()
    .accountSid("account_sid")
    .callSid("call_sid")
    .build();
CallRetrieveResponse call = client.texml().accounts().calls().retrieve(params);
```

## 更新通话信息

更新特定通话的详细信息。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}`

```java
import com.telnyx.sdk.models.texml.accounts.calls.CallUpdateParams;
import com.telnyx.sdk.models.texml.accounts.calls.CallUpdateResponse;
import com.telnyx.sdk.models.texml.accounts.calls.UpdateCall;

CallUpdateParams params = CallUpdateParams.builder()
    .accountSid("account_sid")
    .callSid("call_sid")
    .updateCall(UpdateCall.builder().build())
    .build();
CallUpdateResponse call = client.texml().accounts().calls().update(params);
```

## 列出会议参与者

列出会议参与者。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants`

```java
import com.telnyx.sdk.models.texml.accounts.conferences.participants.ParticipantRetrieveParticipantsParams;
import com.telnyx.sdk.models.texml.accounts.conferences.participants.ParticipantRetrieveParticipantsResponse;

ParticipantRetrieveParticipantsParams params = ParticipantRetrieveParticipantsParams.builder()
    .accountSid("account_sid")
    .conferenceSid("conference_sid")
    .build();
ParticipantRetrieveParticipantsResponse response = client.texml().accounts().conferences().participants().retrieveParticipants(params);
```

## 添加新的会议参与者

添加一个新的会议参与者。

`POST /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants`

```java
import com.telnyx.sdk.models.texml.accounts.conferences.participants.ParticipantParticipantsParams;
import com.telnyx.sdk.models.texml.accounts.conferences.participants.ParticipantParticipantsResponse;

ParticipantParticipantsParams params = ParticipantParticipantsParams.builder()
    .accountSid("account_sid")
    .conferenceSid("conference_sid")
    .build();
ParticipantParticipantsResponse response = client.texml().accounts().conferences().participants().participants(params);
```

## 获取会议参与者信息

获取特定会议参与者的信息。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label}`

```java
import com.telnyx.sdk.models.texml.accounts.conferences.participants.ParticipantRetrieveParams;
import com.telnyx.sdk.models.texml.accounts.conferences.participants.ParticipantRetrieveResponse;

ParticipantRetrieveParams params = ParticipantRetrieveParams.builder()
    .accountSid("account_sid")
    .conferenceSid("conference_sid")
    .callSidOrParticipantLabel("call_sid_or_participant_label")
    .build();
ParticipantRetrieveResponse participant = client.texml().accounts().conferences().participants().retrieve(params);
```

## 更新会议参与者信息

更新特定会议参与者的信息。

`POST /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label}`

```java
import com.telnyx.sdk.models.texml.accounts.conferences.participants.ParticipantUpdateParams;
import com.telnyx.sdk.models.texml.accounts.conferences.participants.ParticipantUpdateResponse;

ParticipantUpdateParams params = ParticipantUpdateParams.builder()
    .accountSid("account_sid")
    .conferenceSid("conference_sid")
    .callSidOrParticipantLabel("call_sid_or_participant_label")
    .build();
ParticipantUpdateResponse participant = client.texml().accounts().conferences().participants().update(params);
```

## 删除会议参与者

删除一个会议参与者。

`DELETE /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label}`

```java
import com.telnyx.sdk.models.texml.accounts.conferences.participants.ParticipantDeleteParams;

ParticipantDeleteParams params = ParticipantDeleteParams.builder()
    .accountSid("account_sid")
    .conferenceSid("conference_sid")
    .callSidOrParticipantLabel("call_sid_or_participant_label")
    .build();
client.texml().accounts().conferences().participants().delete(params);
```

## 列出会议资源

列出所有会议资源。

`GET /texml/Accounts/{account_sid}/Conferences`

```java
import com.telnyx.sdk.models.texml.accounts.conferences.ConferenceRetrieveConferencesParams;
import com.telnyx.sdk.models.texml.accounts.conferences.ConferenceRetrieveConferencesResponse;

ConferenceRetrieveConferencesResponse response = client.texml().accounts().conferences().retrieveConferences("account_sid");
```

## 获取会议资源信息

获取特定会议资源的详细信息。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}`

```java
import com.telnyx.sdk.models.texml.accounts.conferences.ConferenceRetrieveParams;
import com.telnyx.sdk.models.texml.accounts.conferences.ConferenceRetrieveResponse;

ConferenceRetrieveParams params = ConferenceRetrieveParams.builder()
    .accountSid("account_sid")
    .conferenceSid("conference_sid")
    .build();
ConferenceRetrieveResponse conference = client.texml().accounts().conferences().retrieve(params);
```

## 更新会议资源信息

更新特定会议资源的详细信息。

`POST /texml/Accounts/{account_sid}/Conferences/{conference_sid}`

```java
import com.telnyx.sdk.models.texml.accounts.conferences.ConferenceUpdateParams;
import com.telnyx.sdk.models.texml.accounts.conferences.ConferenceUpdateResponse;

ConferenceUpdateParams params = ConferenceUpdateParams.builder()
    .accountSid("account_sid")
    .conferenceSid("conference_sid")
    .build();
ConferenceUpdateResponse conference = client.texml().accounts().conferences().update(params);
```

## 列出队列资源

列出所有队列资源。

`GET /texml/Accounts/{account_sid}/Queues`

```java
import com.telnyx.sdk.models.texml.accounts.queues.QueueListPage;
import com.telnyx.sdk.models.texml.accounts.queues.QueueListParams;

QueueListPage page = client.texml().accounts().queues().list("account_sid");
```

## 创建新的队列资源

创建一个新的队列资源。

`POST /texml/Accounts/{account_sid}/Queues`

```java
import com.telnyx.sdk.models.texml.accounts.queues.QueueCreateParams;
import com.telnyx.sdk.models.texml.accounts.queues.QueueCreateResponse;

QueueCreateResponse queue = client.texml().accounts().queues().create("account_sid");
```

## 获取队列资源信息

获取特定队列资源的详细信息。

`GET /texml/Accounts/{account_sid}/Queues/{queue_sid}`

```java
import com.telnyx.sdk.models.texml.accounts.queues.QueueRetrieveParams;
import com.telnyx.sdk.models.texml.accounts.queues.QueueRetrieveResponse;

QueueRetrieveParams params = QueueRetrieveParams.builder()
    .accountSid("account_sid")
    .queueSid("queue_sid")
    .build();
QueueRetrieveResponse queue = client.texml().accounts().queues().retrieve(params);
```

## 更新队列资源信息

更新特定队列资源的详细信息。

`POST /texml/Accounts/{account_sid}/Queues/{queue_sid}`

```java
import com.telnyx.sdk.models.texml.accounts.queues.QueueUpdateParams;
import com.telnyx.sdk.models.texml.accounts.queues.QueueUpdateResponse;

QueueUpdateParams params = QueueUpdateParams.builder()
    .accountSid("account_sid")
    .queueSid("queue_sid")
    .build();
QueueUpdateResponse queue = client.texml().accounts().queues().update(params);
```

## 删除队列资源

删除一个队列资源。

`DELETE /texml/Accounts/{account_sid}/Queues/{queue_sid}`

```java
import com.telnyx.sdk.models.texml.accounts.queues.QueueDeleteParams;

QueueDeleteParams params = QueueDeleteParams.builder()
    .accountSid("account_sid")
    .queueSid("queue_sid")
    .build();
client.texml().accounts().queues().delete(params);
```

## 获取账户的所有录制资源

返回账户的所有录制资源。

`GET /texml/Accounts/{account_sid}/Recordings.json`

```java
import com.telnyx.sdk.models.texml.accounts.AccountRetrieveRecordingsJsonParams;
import com.telnyx.sdk.models.texml.accounts.AccountRetrieveRecordingsJsonResponse;

AccountRetrieveRecordingsJsonResponse response = client.texml().accounts().retrieveRecordingsJson("account_sid");
```

## 获取特定录制的详细信息

根据录制 ID 获取该录制的详细信息。

`GET /texml/Accounts/{account_sid}/Recordings/{recording_sid}.json`

```java
import com.telnyx.sdk.models.texml.accounts.TexmlGetCallRecordingResponseBody;
import com.telnyx.sdk.models.texml.accounts.recordings.json.JsonRetrieveRecordingSidJsonParams;

JsonRetrieveRecordingSidJsonParams params = JsonRetrieveRecordingSidJsonParams.builder()
    .accountSid("account_sid")
    .recordingSid("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .build();
TexmlGetCallRecordingResponseBody texmlGetCallRecordingResponseBody = client.texml().accounts().recordings().json().retrieveRecordingSidJson(params);
```

## 删除特定录制

删除根据录制 ID 标识的录制资源。

`DELETE /texml/Accounts/{account_sid}/Recordings/{recording_sid}.json`

```java
import com.telnyx.sdk.models.texml.accounts.recordings.json.JsonDeleteRecordingSidJsonParams;

JsonDeleteRecordingSidJsonParams params = JsonDeleteRecordingSidJsonParams.builder()
    .accountSid("account_sid")
    .recordingSid("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .build();
client.texml().accounts().recordings().json().deleteRecordingSidJson(params);
```

## 获取特定通话的录制记录

根据通话 ID 获取该通话的录制记录。

`GET /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings.json`

```java
import com.telnyx.sdk.models.texml.accounts.calls.recordingsjson.RecordingsJsonRetrieveRecordingsJsonParams;
import com.telnyx.sdk.models.texml.accounts.calls.recordingsjson.RecordingsJsonRetrieveRecordingsJsonResponse;

RecordingsJsonRetrieveRecordingsJsonParams params = RecordingsJsonRetrieveRecordingsJsonParams.builder()
    .accountSid("account_sid")
    .callSid("call_sid")
    .build();
RecordingsJsonRetrieveRecordingsJsonResponse response = client.texml().accounts().calls().recordingsJson().retrieveRecordingsJson(params);
```

## 为特定通话请求开始录制

根据通话 ID 启动录制功能。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings.json`

```java
import com.telnyx.sdk.models.texml.accounts.calls.recordingsjson.RecordingsJsonRecordingsJsonParams;
import com.telnyx.sdk.models.texml.accounts.calls.recordingsjson.RecordingsJsonRecordingsJsonResponse;

RecordingsJsonRecordingsJsonParams params = RecordingsJsonRecordingsJsonParams.builder()
    .accountSid("account_sid")
    .callSid("call_sid")
    .build();
RecordingsJsonRecordingsJsonResponse response = client.texml().accounts().calls().recordingsJson().recordingsJson(params);
```

## 更新特定通话的录制记录

更新特定通话的录制资源。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings/{recording_sid}.json`

```java
import com.telnyx.sdk.models.texml.accounts.calls.recordings.RecordingRecordingSidJsonParams;
import com.telnyx.sdk.models.texml.accounts.calls.recordings.RecordingRecordingSidJsonResponse;

RecordingRecordingSidJsonParams params = RecordingRecordingSidJsonParams.builder()
    .accountSid("account_sid")
    .callSid("call_sid")
    .recordingSid("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .build();
RecordingRecordingSidJsonResponse response = client.texml().accounts().calls().recordings().recordingSidJson(params);
```

## 列出会议录制记录

列出所有会议录制记录。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Recordings`

```java
import com.telnyx.sdk.models.texml.accounts.conferences.ConferenceRetrieveRecordingsParams;
import com.telnyx.sdk.models.texml.accounts.conferences.ConferenceRetrieveRecordingsResponse;

ConferenceRetrieveRecordingsParams params = ConferenceRetrieveRecordingsParams.builder()
    .accountSid("account_sid")
    .conferenceSid("conference_sid")
    .build();
ConferenceRetrieveRecordingsResponse response = client.texml().accounts().conferences().retrieveRecordings(params);
```

## 获取特定会议的录制记录

根据会议 ID 获取该会议的录制记录。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Recordings.json`

```java
import com.telnyx.sdk.models.texml.accounts.conferences.ConferenceRetrieveRecordingsJsonParams;
import com.telnyx.sdk.models.texml.accounts.conferences.ConferenceRetrieveRecordingsJsonResponse;

ConferenceRetrieveRecordingsJsonParams params = ConferenceRetrieveRecordingsJsonParams.builder()
    .accountSid("account_sid")
    .conferenceSid("conference_sid")
    .build();
ConferenceRetrieveRecordingsJsonResponse response = client.texml().accounts().conferences().retrieveRecordingsJson(params);
```

## 创建 TeXML 密钥

创建一个 TeXML 密钥，该密钥可在使用 Mustache 模板时作为动态参数使用。

`POST /texml/secrets` — 必需参数：`name`, `value`

```java
import com.telnyx.sdk.models.texml.TexmlSecretsParams;
import com.telnyx.sdk.models.texml.TexmlSecretsResponse;

TexmlSecretsParams params = TexmlSecretsParams.builder()
    .name("My Secret Name")
    .value("My Secret Value")
    .build();
TexmlSecretsResponse response = client.texml().secrets(params);
```

## 为特定通话请求启动 SIPREC 会话

根据通话 ID 启动 SIPREC 会话。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Siprec.json`

```java
import com.telnyx.sdk.models.texml.accounts.calls.CallSiprecJsonParams;
import com.telnyx.sdk.models.texml.accounts.calls.CallSiprecJsonResponse;

CallSiprecJsonParams params = CallSiprecJsonParams.builder()
    .accountSid("account_sid")
    .callSid("call_sid")
    .build();
CallSiprecJsonResponse response = client.texml().accounts().calls().siprecJson(params);
```

## 更新特定通话的 SIPREC 会话

更新特定通话的 SIPREC 会话信息。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Siprec/{siprec_sid}.json`

```java
import com.telnyx.sdk.models.texml.accounts.calls.siprec.SiprecSiprecSidJsonParams;
import com.telnyx.sdk.models.texml.accounts.calls.siprec.SiprecSiprecSidJsonResponse;

SiprecSiprecSidJsonParams params = SiprecSiprecSidJsonParams.builder()
    .accountSid("account_sid")
    .callSid("call_sid")
    .siprecSid("siprec_sid")
    .build();
SiprecSiprecSidJsonResponse response = client.texml().accounts().calls().siprec().siprecSidJson(params);
```

## 为特定通话启动媒体流

为特定通话启动媒体流。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Streams.json`

```java
import com.telnyx.sdk.models.texml.accounts.calls.CallStreamsJsonParams;
import com.telnyx.sdk.models.texml.accounts.calls.CallStreamsJsonResponse;

CallStreamsJsonParams params = CallStreamsJsonParams.builder()
    .accountSid("account_sid")
    .callSid("call_sid")
    .build();
CallStreamsJsonResponse response = client.texml().accounts().calls().streamsJson(params);
```

## 更新特定通话的媒体流信息

更新特定通话的媒体流资源。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Streams/{streaming_sid}.json`

```java
import com.telnyx.sdk.models.texml.accounts.calls.streams.StreamStreamingSidJsonParams;
import com.telnyx.sdk.models.texml.accounts.calls.streams.StreamStreamingSidJsonResponse;

StreamStreamingSidJsonParams params = StreamStreamingSidJsonParams.builder()
    .accountSid("account_sid")
    .callSid("call_sid")
    .streamingSid("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .build();
StreamStreamingSidJsonResponse response = client.texml().accounts().calls().streams().streamingSidJson(params);
```

## 获取所有录制资源的转录文本

返回账户的所有录制资源的转录文本。

`GET /texml/Accounts/{account_sid}/Transcriptions.json`

```java
import com.telnyx.sdk.models.texml.accounts.AccountRetrieveTranscriptionsJsonParams;
import com.telnyx.sdk.models.texml.accounts.AccountRetrieveTranscriptionsJsonResponse;

AccountRetrieveTranscriptionsJsonResponse response = client.texml().accounts().retrieveTranscriptionsJson("account_sid");
```

## 获取特定录制的转录文本

根据转录文本 ID 获取该录制的转录文本。

`GET /texml/Accounts/{account_sid}/Transcriptions/{recording_transcription_sid}.json`

```java
import com.telnyx.sdk.models.texml.accounts.transcriptions.json.JsonRetrieveRecordingTranscriptionSidJsonParams;
import com.telnyx.sdk.models.texml.accounts.transcriptions.json.JsonRetrieveRecordingTranscriptionSidJsonResponse;

JsonRetrieveRecordingTranscriptionSidJsonParams params = JsonRetrieveRecordingTranscriptionSidJsonParams.builder()
    .accountSid("account_sid")
    .recordingTranscriptionSid("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .build();
JsonRetrieveRecordingTranscriptionSidJsonResponse response = client.texml().accounts().transcriptions().json().retrieveRecordingTranscriptionSidJson(params);
```

## 删除录制转录文本

永久删除特定录制的转录文本。

`DELETE /texml/Accounts/{account_sid}/Transcriptions/{recording_transcription_sid}.json`

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL：
所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `TexmlCallAnsweredWebhook` | TeXML 通话已接听。当 TeXML 通话被接听时发送此 Webhook |
| `TexmlCallCompletedWebhook` | TeXML 通话已完成。当 TeXML 通话完成后发送此 Webhook |
| `TexmlCallInitiatedWebhook` | TeXML 通话已发起。当 TeXML 通话开始时发送此 Webhook |
| `TexmlCallRingingWebhook` | TeXML 通话正在振铃。当 TeXML 通话正在振铃时发送此 Webhook |
| `TexmlCallAmdWebhook` | TeXML 通话中的自动应答机检测（AMD）完成时发送此 Webhook |
| `TexmlCallDtmfWebhook` | TeXML 通话中接收到 DTMF 数字时发送此 Webhook |
| `TexmlGatherWebhook` | TeXML 收集操作完成时发送此 Webhook（发送到指定的动作 URL） |
| `TexmlHttpRequestWebhook` | TeXML HTTP 请求响应时发送此 Webhook |
| `TexmlAiGatherWebhook` | AI 收集操作完成并生成转录结果时发送此 Webhook |
| `TexmlConferenceJoinWebhook` | 参与者加入会议时发送此 Webhook |
| `TexmlConferenceLeaveWebhook` | 参与者离开会议时发送此 Webhook |
| `TexmlConferenceSpeakerWebhook` | 参与者在会议中开始或停止发言时发送此 Webhook |
| `TexmlConferenceEndWebhook` | 会议结束时发送此 Webhook |
| `TexmlConferenceStartWebhook` | 会议开始时发送此 Webhook |
| `TexmlQueueWebhook` | 队列状态事件发生时发送此 Webhook（由 `enqueue` 命令触发） |
| `TexmlRecordingCompletedWebhook` | 通话中的录制完成时发送此 Webhook（由 `recordingStatusCallbackEvent` 触发） |
| `TexmlRecordingInProgressWebhook` | 通话中的录制开始时发送此 Webhook（由 `recordingStatusCallbackEvent` 触发） |
| `TexmlSiprecWebhook` | SIPREC 会话状态更新时发送此 Webhook |
| `TexmlStreamWebhook` | 媒体流状态更新时发送此 Webhook |
| `TexmlTranscriptionWebhook` | 录制转录完成时发送此 Webhook |
```
```