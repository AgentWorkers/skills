---
name: telnyx-texml-ruby
description: >-
  Build voice applications using TeXML markup language (TwiML-compatible).
  Manage applications, calls, conferences, recordings, queues, and streams. This
  skill provides Ruby SDK examples.
metadata:
  author: telnyx
  product: texml
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Texml - Ruby

## 安装

```bash
gem install telnyx
```

## 设置

```ruby
require "telnyx"

client = Telnyx::Client.new(
  api_key: ENV["TELNYX_API_KEY"], # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出所有 TeXML 应用程序

返回您的所有 TeXML 应用程序列表。

`GET /texml_applications`

```ruby
page = client.texml_applications.list

puts(page)
```

## 创建 TeXML 应用程序

创建一个新的 TeXML 应用程序。

`POST /texml_applications` — 必需参数：`friendly_name`, `voice_url`

```ruby
texml_application = client.texml_applications.create(friendly_name: "call-router", voice_url: "https://example.com")

puts(texml_application)
```

## 获取 TeXML 应用程序详情

获取现有 TeXML 应用程序的详细信息。

`GET /texml_applications/{id}`

```ruby
texml_application = client.texml_applications.retrieve("1293384261075731499")

puts(texml_application)
```

## 更新 TeXML 应用程序

更新现有 TeXML 应用程序的设置。

`PATCH /texml_applications/{id}` — 必需参数：`friendly_name`, `voice_url`

```ruby
texml_application = client.texml_applications.update(
  "1293384261075731499",
  friendly_name: "call-router",
  voice_url: "https://example.com"
)

puts(texml_application)
```

## 删除 TeXML 应用程序

删除一个 TeXML 应用程序。

`DELETE /texml_applications/{id}`

```ruby
texml_application = client.texml_applications.delete("1293384261075731499")

puts(texml_application)
```

## 获取多个通话资源

获取账户的所有通话资源。

`GET /texml/Accounts/{account_sid}/Calls`

```ruby
response = client.texml.accounts.calls.retrieve_calls("account_sid")

puts(response)
```

## 发起出站通话

发起一个出站 TeXML 通话。

`POST /texml/Accounts/{account_sid}/Calls` — 必需参数：`To`, `From`, `ApplicationSid`

```ruby
response = client.texml.accounts.calls.calls(
  "account_sid",
  application_sid: "example-app-sid",
  from: "+13120001234",
  to: "+13121230000"
)

puts(response)
```

## 获取特定通话的详细信息

根据通话 ID 获取该通话的详细信息。

`GET /texml/Accounts/{account_sid}/Calls/{call_sid}`

```ruby
call = client.texml.accounts.calls.retrieve("call_sid", account_sid: "account_sid")

puts(call)
```

## 更新通话信息

更新特定通话的详细信息。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}`

```ruby
call = client.texml.accounts.calls.update("call_sid", account_sid: "account_sid")

puts(call)
```

## 列出会议参与者

列出会议参与者。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants`

```ruby
response = client.texml.accounts.conferences.participants.retrieve_participants(
  "conference_sid",
  account_sid: "account_sid"
)

puts(response)
```

## 添加新的会议参与者

添加一个新的会议参与者。

`POST /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants`

```ruby
response = client.texml.accounts.conferences.participants.participants("conference_sid", account_sid: "account_sid")

puts(response)
```

## 获取会议参与者信息

获取特定会议参与者的信息。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label}`

```ruby
participant = client.texml.accounts.conferences.participants.retrieve(
  "call_sid_or_participant_label",
  account_sid: "account_sid",
  conference_sid: "conference_sid"
)

puts(participant)
```

## 更新会议参与者信息

更新特定会议参与者的信息。

`POST /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label}`

```ruby
participant = client.texml.accounts.conferences.participants.update(
  "call_sid_or_participant_label",
  account_sid: "account_sid",
  conference_sid: "conference_sid"
)

puts(participant)
```

## 删除会议参与者

删除特定的会议参与者。

`DELETE /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label}`

```ruby
result = client.texml.accounts.conferences.participants.delete(
  "call_sid_or_participant_label",
  account_sid: "account_sid",
  conference_sid: "conference_sid"
)

puts(result)
```

## 列出会议资源

列出所有会议资源。

`GET /texml/Accounts/{account_sid}/Conferences`

```ruby
response = client.texml.accounts.conferences.retrieve_conferences("account_sid")

puts(response)
```

## 获取特定会议资源

获取特定会议的资源信息。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}`

```ruby
conference = client.texml.accounts.conferences.retrieve("conference_sid", account_sid: "account_sid")

puts(conference)
```

## 更新会议资源

更新特定会议的资源信息。

`POST /texml/Accounts/{account_sid}/Conferences/{conference_sid}`

```ruby
conference = client.texml.accounts.conferences.update("conference_sid", account_sid: "account_sid")

puts(conference)
```

## 列出队列资源

列出所有队列资源。

`GET /texml/Accounts/{account_sid}/Queues`

```ruby
page = client.texml.accounts.queues.list("account_sid")

puts(page)
```

## 创建新的队列

创建一个新的队列资源。

`POST /texml/Accounts/{account_sid}/Queues`

```ruby
queue = client.texml.accounts.queues.create("account_sid")

puts(queue)
```

## 获取队列资源

获取特定队列的资源信息。

`GET /texml/Accounts/{account_sid}/Queues/{queue_sid}`

```ruby
queue = client.texml.accounts.queues.retrieve("queue_sid", account_sid: "account_sid")

puts(queue)
```

## 更新队列资源

更新特定队列的资源信息。

`POST /texml/Accounts/{account_sid}/Queues/{queue_sid}`

```ruby
queue = client.texml.accounts.queues.update("queue_sid", account_sid: "account_sid")

puts(queue)
```

## 删除队列资源

删除特定的队列资源。

`DELETE /texml/Accounts/{account_sid}/Queues/{queue_sid}`

```ruby
result = client.texml.accounts.queues.delete("queue_sid", account_sid: "account_sid")

puts(result)
```

## 获取账户的所有录音资源

获取账户的所有录音资源。

`GET /texml/Accounts/{account_sid}/Recordings.json`

```ruby
response = client.texml.accounts.retrieve_recordings_json("account_sid")

puts(response)
```

## 获取特定录音资源

根据录音 ID 获取相应的录音资源。

`GET /texml/Accounts/{account_sid}/Recordings/{recording_sid}.json`

```ruby
texml_get_call_recording_response_body = client.texml.accounts.recordings.json.retrieve_recording_sid_json(
  "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
  account_sid: "account_sid"
)

puts(texml_get_call_recording_response_body)
```

## 删除特定录音资源

根据录音 ID 删除相应的录音资源。

`DELETE /texml/Accounts/{account_sid}/Recordings/{recording_sid}.json`

```ruby
result = client.texml.accounts.recordings.json.delete_recording_sid_json(
  "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
  account_sid: "account_sid"
)

puts(result)
```

## 获取特定通话的录音资源

根据通话 ID 获取该通话的录音资源。

`GET /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings.json`

```ruby
response = client.texml.accounts.calls.recordings_json.retrieve_recordings_json(
  "call_sid",
  account_sid: "account_sid"
)

puts(response)
```

## 为特定通话请求录音

根据通话 ID 启动录音。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings.json`

```ruby
response = client.texml.accounts.calls.recordings_json.recordings_json("call_sid", account_sid: "account_sid")

puts(response)
```

## 更新特定通话的录音资源

更新特定通话的录音信息。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings/{recording_sid}.json`

```ruby
response = client.texml.accounts.calls.recordings.recording_sid_json(
  "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
  account_sid: "account_sid",
  call_sid: "call_sid"
)

puts(response)
```

## 列出会议录音

列出所有会议录音。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Recordings`

```ruby
response = client.texml.accounts.conferences.retrieve_recordings("conference_sid", account_sid: "account_sid")

puts(response)
```

## 获取特定会议的录音资源

根据会议 ID 获取该会议的录音资源。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Recordings.json`

```ruby
response = client.texml.accounts.conferences.retrieve_recordings_json("conference_sid", account_sid: "account_sid")

puts(response)
```

## 创建 TeXML 密钥

创建一个 TeXML 密钥，该密钥可在使用 Mustache 模板时作为动态参数使用。

`POST /texml/secrets` — 必需参数：`name`, `value`

```ruby
response = client.texml.secrets(name: "My Secret Name", value: "My Secret Value")

puts(response)
```

## 为特定通话请求 SIPREC 会话

根据通话 ID 启动 SIPREC 会话。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Siprec.json`

```ruby
response = client.texml.accounts.calls.siprec_json("call_sid", account_sid: "account_sid")

puts(response)
```

## 更新特定通话的 SIPREC 会话

更新特定通话的 SIPREC 会话信息。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Siprec/{siprec_sid}.json`

```ruby
response = client.texml.accounts.calls.siprec.siprec_sid_json(
  "siprec_sid",
  account_sid: "account_sid",
  call_sid: "call_sid"
)

puts(response)
```

## 为特定通话开始媒体流

开始向指定 WebSocket 地址传输媒体流。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Streams.json`

```ruby
response = client.texml.accounts.calls.streams_json("call_sid", account_sid: "account_sid")

puts(response)
```

## 更新特定通话的媒体流信息

更新特定通话的媒体流资源。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Streams/{streaming_sid}.json`

```ruby
response = client.texml.accounts.calls.streams.streaming_sid_json(
  "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
  account_sid: "account_sid",
  call_sid: "call_sid"
)

puts(response)
```

## 获取所有录音的转录信息

获取账户的所有录音转录文件。

`GET /texml/Accounts/{account_sid}/Transcriptions.json`

```ruby
response = client.texml.accounts.retrieve_transcriptions_json("account_sid")

puts(response)
```

## 获取特定录音的转录文件

根据转录文件 ID 获取相应的转录文件。

`GET /texml/Accounts/{account_sid}/Transcriptions/{recording_transcription_sid}.json`

```ruby
response = client.texml.accounts.transcriptions.json.retrieve_recording_transcription_sid_json(
  "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
  account_sid: "account_sid"
)

puts(response)
```

## 删除录音转录文件

永久删除特定的录音转录文件。

`DELETE /texml/Accounts/{account_sid}/Transcriptions/{recording_transcription_sid}.json`

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL：
所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 头部信息，用于验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `TexmlCallAnsweredWebhook` | TeXML 通话已接听。当 TeXML 通话被接听时发送此 Webhook |
| `TexmlCallCompletedWebhook` | TeXML 通话已完成。当 TeXML 通话结束时发送此 Webhook |
| `TexmlCallInitiatedWebhook` | TeXML 通话已发起。当 TeXML 通话开始时发送此 Webhook |
| `TexmlCallRingingWebhook` | TeXML 通话正在拨号中。当 TeXML 通话正在拨号时发送此 Webhook |
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
| `TexmlQueueWebhook` | 队列状态事件发生时发送此 Webhook（由 `Enqueue` 命令触发） |
| `TexmlRecordingCompletedWebhook` | TeXML 通话中的录音完成时发送此 Webhook（由 `recordingStatusCallbackEvent` 触发） |
| `TexmlRecordingInProgressWebhook` | 通话中的录音开始时发送此 Webhook（由 `recordingStatusCallbackEvent` 触发） |
| `TexmlSiprecWebhook` | SIPREC 会话状态更新时发送此 Webhook |
| `TexmlStreamWebhook` | 媒体流状态更新时发送此 Webhook |
| `TexmlTranscriptionWebhook` | 录音转录完成时发送此 Webhook |
```
```