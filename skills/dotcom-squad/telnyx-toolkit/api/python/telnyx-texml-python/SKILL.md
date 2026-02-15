---
name: telnyx-texml-python
description: >-
  Build voice applications using TeXML markup language (TwiML-compatible).
  Manage applications, calls, conferences, recordings, queues, and streams. This
  skill provides Python SDK examples.
metadata:
  author: telnyx
  product: texml
  language: python
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 本文档由 Telnyx OpenAPI 规范自动生成，请勿修改。 -->

# Telnyx Texml - Python

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

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出所有 TeXML 应用程序

返回您的所有 TeXML 应用程序列表。

`GET /texml_applications`

```python
page = client.texml_applications.list()
page = page.data[0]
print(page.id)
```

## 创建一个 TeXML 应用程序

创建一个新的 TeXML 应用程序。

`POST /texml_applications` — 必需参数：`friendly_name`、`voice_url`

```python
texml_application = client.texml_applications.create(
    friendly_name="call-router",
    voice_url="https://example.com",
)
print(texml_application.data)
```

## 获取 TeXML 应用程序详情

获取现有 TeXML 应用程序的详细信息。

`GET /texml_applications/{id}`

```python
texml_application = client.texml_applications.retrieve(
    "1293384261075731499",
)
print(texml_application.data)
```

## 更新 TeXML 应用程序

更新现有 TeXML 应用程序的设置。

`PATCH /texml_applications/{id}` — 必需参数：`friendly_name`、`voice_url`

```python
texml_application = client.texml_applications.update(
    id="1293384261075731499",
    friendly_name="call-router",
    voice_url="https://example.com",
)
print(texml_application.data)
```

## 删除 TeXML 应用程序

删除一个 TeXML 应用程序。

`DELETE /texml_applications/{id}`

```python
texml_application = client.texml_applications.delete(
    "1293384261075731499",
)
print(texml_application.data)
```

## 获取多个通话记录

获取某个账户的所有通话记录。

`GET /texml/Accounts/{account_sid}/Calls`

```python
response = client.texml.accounts.calls.retrieve_calls(
    account_sid="account_sid",
)
print(response.calls)
```

## 发起出站通话

发起一个出站 TeXML 通话。

`POST /texml/Accounts/{account_sid}/Calls` — 必需参数：`To`、`From`、`ApplicationSid`

```python
response = client.texml.accounts.calls.calls(
    account_sid="account_sid",
    application_sid="example-app-sid",
    from_="+13120001234",
    to="+13121230000",
)
print(response.from_)
```

## 获取特定通话记录

根据通话 ID 获取相应的通话记录。

`GET /texml/Accounts/{account_sid}/Calls/{call_sid}`

```python
call = client.texml.accounts.calls.retrieve(
    call_sid="call_sid",
    account_sid="account_sid",
)
print(call.account_sid)
```

## 更新通话记录

更新特定通话的记录信息。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}`

```python
call = client.texml.accounts.calls.update(
    call_sid="call_sid",
    account_sid="account_sid",
)
print(call.account_sid)
```

## 列出会议参与者

列出会议中的参与者。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants`

```python
response = client.texml.accounts.conferences.participants.retrieve_participants(
    conference_sid="conference_sid",
    account_sid="account_sid",
)
print(response.end)
```

## 添加新的会议参与者

添加新的会议参与者。

`POST /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants`

```python
response = client.texml.accounts.conferences.participants.participants(
    conference_sid="conference_sid",
    account_sid="account_sid",
)
print(response.account_sid)
```

## 获取会议参与者信息

获取特定会议参与者的信息。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label}`

```python
participant = client.texml.accounts.conferences.participants.retrieve(
    call_sid_or_participant_label="call_sid_or_participant_label",
    account_sid="account_sid",
    conference_sid="conference_sid",
)
print(participant.account_sid)
```

## 更新会议参与者信息

更新会议参与者的信息。

`POST /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label}`

```python
participant = client.texml.accounts.conferences.participants.update(
    call_sid_or_participant_label="call_sid_or_participant_label",
    account_sid="account_sid",
    conference_sid="conference_sid",
)
print(participant.account_sid)
```

## 删除会议参与者

删除会议参与者。

`DELETE /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label}`

```python
client.texml.accounts.conferences.participants.delete(
    call_sid_or_participant_label="call_sid_or_participant_label",
    account_sid="account_sid",
    conference_sid="conference_sid",
)
```

## 列出会议资源

列出所有会议资源。

`GET /texml/Accounts/{account_sid}/Conferences`

```python
response = client.texml.accounts.conferences.retrieve_conferences(
    account_sid="account_sid",
)
print(response.conferences)
```

## 获取会议资源信息

获取特定会议的资源信息。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}`

```python
conference = client.texml.accounts.conferences.retrieve(
    conference_sid="conference_sid",
    account_sid="account_sid",
)
print(conference.account_sid)
```

## 更新会议资源

更新会议资源信息。

`POST /texml/Accounts/{account_sid}/Conferences/{conference_sid}`

```python
conference = client.texml.accounts.conferences.update(
    conference_sid="conference_sid",
    account_sid="account_sid",
)
print(conference.account_sid)
```

## 列出队列资源

列出所有队列资源。

`GET /texml/Accounts/{account_sid}/Queues`

```python
page = client.texml.accounts.queues.list(
    account_sid="account_sid",
)
page = page.queues[0]
print(page.account_sid)
```

## 创建新的队列

创建一个新的队列资源。

`POST /texml/Accounts/{account_sid}/Queues`

```python
queue = client.texml.accounts.queues.create(
    account_sid="account_sid",
)
print(queue.account_sid)
```

## 获取队列资源信息

获取特定队列的资源信息。

`GET /texml/Accounts/{account_sid}/Queues/{queue_sid}`

```python
queue = client.texml.accounts.queues.retrieve(
    queue_sid="queue_sid",
    account_sid="account_sid",
)
print(queue.account_sid)
```

## 更新队列资源

更新队列资源信息。

`POST /texml/Accounts/{account_sid}/Queues/{queue_sid}`

```python
queue = client.texml.accounts.queues.update(
    queue_sid="queue_sid",
    account_sid="account_sid",
)
print(queue.account_sid)
```

## 删除队列资源

删除队列资源。

`DELETE /texml/Accounts/{account_sid}/Queues/{queue_sid}`

```python
client.texml.accounts.queues.delete(
    queue_sid="queue_sid",
    account_sid="account_sid",
)
```

## 获取多个录音资源

获取某个账户的所有录音资源。

`GET /texml/Accounts/{account_sid}/Recordings.json`

```python
response = client.texml.accounts.retrieve_recordings_json(
    account_sid="account_sid",
)
print(response.end)
```

## 获取特定录音资源

根据录音 ID 获取相应的录音资源。

`GET /texml/Accounts/{account_sid}/Recordings/{recording_sid}.json`

```python
texml_get_call_recording_response_body = client.texml.accounts.recordings.json.retrieve_recording_sid_json(
    recording_sid="6a09cdc3-8948-47f0-aa62-74ac943d6c58",
    account_sid="account_sid",
)
print(texml_get_call_recording_response_body.account_sid)
```

## 删除录音资源

根据录音 ID 删除相应的录音资源。

`DELETE /texml/Accounts/{account_sid}/Recordings/{recording_sid}.json`

```python
client.texml.accounts.recordings.json.delete_recording_sid_json(
    recording_sid="6a09cdc3-8948-47f0-aa62-74ac943d6c58",
    account_sid="account_sid",
)
```

## 获取通话录音

根据通话 ID 获取相应的通话录音记录。

`GET /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings.json`

```python
response = client.texml.accounts.calls.recordings_json.retrieve_recordings_json(
    call_sid="call_sid",
    account_sid="account_sid",
)
print(response.end)
```

## 为通话请求录音

根据通话 ID 启动录音。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings.json`

```python
response = client.texml.accounts.calls.recordings_json.recordings_json(
    call_sid="call_sid",
    account_sid="account_sid",
)
print(response.account_sid)
```

## 更新通话录音

更新特定通话的录音信息。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings/{recording_sid}.json`

```python
response = client.texml.accounts.calls.recordings.recording_sid_json(
    recording_sid="6a09cdc3-8948-47f0-aa62-74ac943d6c58",
    account_sid="account_sid",
    call_sid="call_sid",
)
print(response.account_sid)
```

## 列出会议录音

列出所有会议录音。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Recordings`

```python
response = client.texml.accounts.conferences.retrieve_recordings(
    conference_sid="conference_sid",
    account_sid="account_sid",
)
print(response.end)
```

## 获取会议录音记录

根据会议 ID 获取相应的会议录音记录。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Recordings.json`

```python
response = client.texml.accounts.conferences.retrieve_recordings_json(
    conference_sid="conference_sid",
    account_sid="account_sid",
)
print(response.end)
```

## 创建 TeXML 密钥

创建一个 TeXML 密钥，该密钥可在使用 Mustache 模板时作为动态参数使用。

`POST /texml/secrets` — 必需参数：`name`、`value`

```python
response = client.texml.secrets(
    name="My Secret Name",
    value="My Secret Value",
)
print(response.data)
```

## 为通话请求 SIPREC 会话

根据通话 ID 启动 SIPREC 会话。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Siprec.json`

```python
response = client.texml.accounts.calls.siprec_json(
    call_sid="call_sid",
    account_sid="account_sid",
)
print(response.account_sid)
```

## 更新通话的 SIPREC 会话

更新特定通话的 SIPREC 会话信息。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Siprec/{siprec_sid}.json`

```python
response = client.texml.accounts.calls.siprec.siprec_sid_json(
    siprec_sid="siprec_sid",
    account_sid="account_sid",
    call_sid="call_sid",
)
print(response.account_sid)
```

## 为通话启动媒体流

为特定通话启动媒体流。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Streams.json`

```python
response = client.texml.accounts.calls.streams_json(
    call_sid="call_sid",
    account_sid="account_sid",
)
print(response.account_sid)
```

## 更新通话中的媒体流

更新特定通话的媒体流信息。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Streams/{streaming_sid}.json`

```python
response = client.texml.accounts.calls.streams.streaming_sid_json(
    streaming_sid="6a09cdc3-8948-47f0-aa62-74ac943d6c58",
    account_sid="account_sid",
    call_sid="call_sid",
)
print(response.account_sid)
```

## 获取录音转录结果

获取所有录音的转录结果。

`GET /texml/Accounts/{account_sid}/Transcriptions.json`

```python
response = client.texml.accounts.retrieve_transcriptions_json(
    account_sid="account_sid",
)
print(response.end)
```

## 获取特定录音的转录结果

根据转录 ID 获取相应的转录结果。

`GET /texml/Accounts/{account_sid}/Transcriptions/{recording_transcription_sid}.json`

```python
response = client.texml.accounts.transcriptions.json.retrieve_recording_transcription_sid_json(
    recording_transcription_sid="6a09cdc3-8948-47f0-aa62-74ac943d6c58",
    account_sid="account_sid",
)
print(response.account_sid)
```

## 删除录音转录结果

永久删除特定的录音转录结果。

`DELETE /texml/Accounts/{account_sid}/Transcriptions/{recording_transcription_sid}.json`

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 头部信息以用于验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `TexmlCallAnsweredWebhook` | TeXML 通话已接听。当 TeXML 通话被接听时触发 |
| `TexmlCallCompletedWebhook` | TeXML 通话已完成。当 TeXML 通话结束时触发 |
| `TexmlCallInitiatedWebhook` | TeXML 通话已发起。当 TeXML 通话开始时触发 |
| `TexmlCallRingingWebhook` | TeXML 通话正在振铃。当 TeXML 通话开始振铃时触发 |
| `TexmlCallAmdWebhook` | TeXML 通话中的自动应答机制（AMD）完成时触发 |
| `TexmlCallDtmfWebhook` | TeXML 通话中接收到 DTMF 数字时触发 |
| `TexmlGatherWebhook` | TeXML 数据收集任务完成时触发（发送到指定的动作 URL） |
| `TexmlHttpRequestWebhook` | TeXML HTTP 请求响应时触发 |
| `TexmlAiGatherWebhook` | AI 数据收集任务完成并生成转录结果时触发 |
| `TexmlConferenceJoinWebhook` | 会议参与者加入时触发 |
| `TexmlConferenceLeaveWebhook` | 会议参与者离开时触发 |
| `TexmlConferenceSpeakerWebhook` | 会议参与者开始或停止发言时触发 |
| `TexmlConferenceEndWebhook` | 会议结束时触发 |
| `TexmlConferenceStartWebhook` | 会议开始时触发 |
| `TexmlQueueWebhook` | 队列状态变化时触发（由 `Enqueue` 命令触发） |
| `TexmlRecordingCompletedWebhook` | 通话中的录音完成时触发 |
| `TexmlRecordingInProgressWebhook` | 通话中的录音开始时触发 |
| `TexmlSiprecWebhook` | SIPREC 会话状态更新时触发 |
| `TexmlStreamWebhook` | 媒体流状态更新时触发 |
| `TexmlTranscriptionWebhook` | 录音转录完成时触发 |
```
```