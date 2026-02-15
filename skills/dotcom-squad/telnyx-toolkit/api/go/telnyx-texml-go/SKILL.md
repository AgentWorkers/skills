---
name: telnyx-texml-go
description: >-
  Build voice applications using TeXML markup language (TwiML-compatible).
  Manage applications, calls, conferences, recordings, queues, and streams. This
  skill provides Go SDK examples.
metadata:
  author: telnyx
  product: texml
  language: go
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Texml - Go

## 安装

```bash
go get github.com/team-telnyx/telnyx-go
```

## 设置

```go
import (
  "context"
  "fmt"
  "os"

  "github.com/team-telnyx/telnyx-go"
  "github.com/team-telnyx/telnyx-go/option"
)

client := telnyx.NewClient(
  option.WithAPIKey(os.Getenv("TELNYX_API_KEY")),
)
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出所有 TeXML 应用程序

返回您的所有 TeXML 应用程序列表。

`GET /texml_applications`

```go
	page, err := client.TexmlApplications.List(context.TODO(), telnyx.TexmlApplicationListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建 TeXML 应用程序

创建一个新的 TeXML 应用程序。

`POST /texml_applications` — 必需参数：`friendly_name`、`voice_url`

```go
	texmlApplication, err := client.TexmlApplications.New(context.TODO(), telnyx.TexmlApplicationNewParams{
		FriendlyName: "call-router",
		VoiceURL:     "https://example.com",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", texmlApplication.Data)
```

## 获取 TeXML 应用程序信息

检索现有 TeXML 应用程序的详细信息。

`GET /texml_applications/{id}`

```go
	texmlApplication, err := client.TexmlApplications.Get(context.TODO(), "1293384261075731499")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", texmlApplication.Data)
```

## 更新 TeXML 应用程序

更新现有 TeXML 应用程序的设置。

`PATCH /texml_applications/{id}` — 必需参数：`friendly_name`、`voice_url`

```go
	texmlApplication, err := client.TexmlApplications.Update(
		context.TODO(),
		"1293384261075731499",
		telnyx.TexmlApplicationUpdateParams{
			FriendlyName: "call-router",
			VoiceURL:     "https://example.com",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", texmlApplication.Data)
```

## 删除 TeXML 应用程序

删除一个 TeXML 应用程序。

`DELETE /texml_applications/{id}`

```go
	texmlApplication, err := client.TexmlApplications.Delete(context.TODO(), "1293384261075731499")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", texmlApplication.Data)
```

## 获取多个通话资源

获取某个账户的所有通话资源。

`GET /texml/Accounts/{account_sid}/Calls`

```go
	response, err := client.Texml.Accounts.Calls.GetCalls(
		context.TODO(),
		"account_sid",
		telnyx.TexmlAccountCallGetCallsParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Calls)
```

## 发起出站通话

发起一个出站 TeXML 通话。

`POST /texml/Accounts/{account_sid}/Calls` — 必需参数：`To`、`From`、`ApplicationSid`

```go
	response, err := client.Texml.Accounts.Calls.Calls(
		context.TODO(),
		"account_sid",
		telnyx.TexmlAccountCallCallsParams{
			ApplicationSid: "example-app-sid",
			From:           "+13120001234",
			To:             "+13121230000",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.From)
```

## 获取特定通话信息

根据通话 ID 获取通话详情。

`GET /texml/Accounts/{account_sid}/Calls/{call_sid}`

```go
	call, err := client.Texml.Accounts.Calls.Get(
		context.TODO(),
		"call_sid",
		telnyx.TexmlAccountCallGetParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", call.AccountSid)
```

## 更新通话信息

更新特定通话的详细信息。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}`

```go
	call, err := client.Texml.Accounts.Calls.Update(
		context.TODO(),
		"call_sid",
		telnyx.TexmlAccountCallUpdateParams{
			AccountSid: "account_sid",
			UpdateCall: telnyx.UpdateCallParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", call.AccountSid)
```

## 列出会议参与者

列出会议参与者信息。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants`

```go
	response, err := client.Texml.Accounts.Conferences.Participants.GetParticipants(
		context.TODO(),
		"conference_sid",
		telnyx.TexmlAccountConferenceParticipantGetParticipantsParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.End)
```

## 拨打电话给会议参与者

拨打电话给会议中的参与者。

`POST /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants`

```go
	response, err := client.Texml.Accounts.Conferences.Participants.Participants(
		context.TODO(),
		"conference_sid",
		telnyx.TexmlAccountConferenceParticipantParticipantsParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.AccountSid)
```

## 获取会议参与者信息

获取会议参与者的详细信息。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label}`

```go
	participant, err := client.Texml.Accounts.Conferences.Participants.Get(
		context.TODO(),
		"call_sid_or_participant_label",
		telnyx.TexmlAccountConferenceParticipantGetParams{
			AccountSid:    "account_sid",
			ConferenceSid: "conference_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", participant.AccountSid)
```

## 更新会议参与者信息

更新会议参与者的信息。

`POST /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label}`

```go
	participant, err := client.Texml.Accounts.Conferences.Participants.Update(
		context.TODO(),
		"call_sid_or_participant_label",
		telnyx.TexmlAccountConferenceParticipantUpdateParams{
			AccountSid:    "account_sid",
			ConferenceSid: "conference_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", participant.AccountSid)
```

## 删除会议参与者

删除会议参与者。

`DELETE /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label}`

```go
	err := client.Texml.Accounts.Conferences.Participants.Delete(
		context.TODO(),
		"call_sid_or_participant_label",
		telnyx.TexmlAccountConferenceParticipantDeleteParams{
			AccountSid:    "account_sid",
			ConferenceSid: "conference_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
```

## 列出会议资源

列出所有会议资源。

`GET /texml/Accounts/{account_sid}/Conferences`

```go
	response, err := client.Texml.Accounts.Conferences.GetConferences(
		context.TODO(),
		"account_sid",
		telnyx.TexmlAccountConferenceGetConferencesParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Conferences)
```

## 获取会议资源信息

获取特定会议的详细信息。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}`

```go
	conference, err := client.Texml.Accounts.Conferences.Get(
		context.TODO(),
		"conference_sid",
		telnyx.TexmlAccountConferenceGetParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", conference.AccountSid)
```

## 更新会议资源

更新会议资源的详细信息。

`POST /texml/Accounts/{account_sid}/Conferences/{conference_sid}`

```go
	conference, err := client.Texml.Accounts.Conferences.Update(
		context.TODO(),
		"conference_sid",
		telnyx.TexmlAccountConferenceUpdateParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", conference.AccountSid)
```

## 列出队列资源

列出所有队列资源。

`GET /texml/Accounts/{account_sid}/Queues`

```go
	page, err := client.Texml.Accounts.Queues.List(
		context.TODO(),
		"account_sid",
		telnyx.TexmlAccountQueueListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建新队列

创建一个新的队列资源。

`POST /texml/Accounts/{account_sid}/Queues`

```go
	queue, err := client.Texml.Accounts.Queues.New(
		context.TODO(),
		"account_sid",
		telnyx.TexmlAccountQueueNewParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", queue.AccountSid)
```

## 获取队列资源信息

获取特定队列的详细信息。

`GET /texml/Accounts/{account_sid}/Queues/{queue_sid}`

```go
	queue, err := client.Texml.Accounts.Queues.Get(
		context.TODO(),
		"queue_sid",
		telnyx.TexmlAccountQueueGetParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", queue.AccountSid)
```

## 更新队列资源

更新队列的详细信息。

`POST /texml/Accounts/{account_sid}/Queues/{queue_sid}`

```go
	queue, err := client.Texml.Accounts.Queues.Update(
		context.TODO(),
		"queue_sid",
		telnyx.TexmlAccountQueueUpdateParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", queue.AccountSid)
```

## 删除队列资源

删除队列资源。

`DELETE /texml/Accounts/{account_sid}/Queues/{queue_sid}`

```go
	err := client.Texml.Accounts.Queues.Delete(
		context.TODO(),
		"queue_sid",
		telnyx.TexmlAccountQueueDeleteParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
```

## 获取多个录音资源

获取某个账户的所有录音资源。

`GET /texml/Accounts/{account_sid}/Recordings.json`

```go
	response, err := client.Texml.Accounts.GetRecordingsJson(
		context.TODO(),
		"account_sid",
		telnyx.TexmlAccountGetRecordingsJsonParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.End)
```

## 获取特定录音资源

根据录音 ID 获取录音资源。

`GET /texml/Accounts/{account_sid}/Recordings/{recording_sid}.json`

```go
	texmlGetCallRecordingResponseBody, err := client.Texml.Accounts.Recordings.Json.GetRecordingSidJson(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.TexmlAccountRecordingJsonGetRecordingSidJsonParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", texmlGetCallRecordingResponseBody.AccountSid)
```

## 删除录音资源

根据录音 ID 删除录音资源。

`DELETE /texml/Accounts/{account_sid}/Recordings/{recording_sid}.json`

```go
	err := client.Texml.Accounts.Recordings.Json.DeleteRecordingSidJson(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.TexmlAccountRecordingJsonDeleteRecordingSidJsonParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
```

## 获取通话录音

根据通话 ID 获取通话的录音资源。

`GET /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings.json`

```go
	response, err := client.Texml.Accounts.Calls.RecordingsJson.GetRecordingsJson(
		context.TODO(),
		"call_sid",
		telnyx.TexmlAccountCallRecordingsJsonGetRecordingsJsonParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.End)
```

## 为通话请求录音

根据通话 ID 启动录音。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings.json`

```go
	response, err := client.Texml.Accounts.Calls.RecordingsJson.RecordingsJson(
		context.TODO(),
		"call_sid",
		telnyx.TexmlAccountCallRecordingsJsonRecordingsJsonParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.AccountSid)
```

## 更新通话录音

更新特定通话的录音资源。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings/{recording_sid}.json`

```go
	response, err := client.Texml.Accounts.Calls.Recordings.RecordingSidJson(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.TexmlAccountCallRecordingRecordingSidJsonParams{
			AccountSid: "account_sid",
			CallSid:    "call_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.AccountSid)
```

## 列出会议录音

列出所有会议录音。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Recordings`

```go
	response, err := client.Texml.Accounts.Conferences.GetRecordings(
		context.TODO(),
		"conference_sid",
		telnyx.TexmlAccountConferenceGetRecordingsParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.End)
```

## 获取会议录音资源

根据会议 ID 获取会议录音资源。

`GET /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Recordings.json`

```go
	response, err := client.Texml.Accounts.Conferences.GetRecordingsJson(
		context.TODO(),
		"conference_sid",
		telnyx.TexmlAccountConferenceGetRecordingsJsonParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.End)
```

## 创建 TeXML 密钥

创建一个 TeXML 密钥，该密钥可在使用 Mustache 模板时作为动态参数使用。

`POST /texml/secrets` — 必需参数：`name`、`value`

```go
	response, err := client.Texml.Secrets(context.TODO(), telnyx.TexmlSecretsParams{
		Name:  "My Secret Name",
		Value: "My Secret Value",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 为通话请求 SIPREC 会话

根据通话 ID 启动 SIPREC 会话。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Siprec.json`

```go
	response, err := client.Texml.Accounts.Calls.SiprecJson(
		context.TODO(),
		"call_sid",
		telnyx.TexmlAccountCallSiprecJsonParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.AccountSid)
```

## 更新通话的 SIPREC 会话

更新特定通话的 SIPREC 会话信息。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Siprec/{siprec_sid}.json`

```go
	response, err := client.Texml.Accounts.Calls.Siprec.SiprecSidJson(
		context.TODO(),
		"siprec_sid",
		telnyx.TexmlAccountCallSiprecSiprecSidJsonParams{
			AccountSid: "account_sid",
			CallSid:    "call_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.AccountSid)
```

## 从通话中开始流媒体传输

开始将媒体流传输到指定的 WebSocket 地址。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Streams.json`

```go
	response, err := client.Texml.Accounts.Calls.StreamsJson(
		context.TODO(),
		"call_sid",
		telnyx.TexmlAccountCallStreamsJsonParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.AccountSid)
```

## 更新通话中的流媒体资源

更新特定通话的流媒体资源。

`POST /texml/Accounts/{account_sid}/Calls/{call_sid}/Streams/{streaming_sid}.json`

```go
	response, err := client.Texml.Accounts.Calls.Streams.StreamingSidJson(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.TexmlAccountCallStreamStreamingSidJsonParams{
			AccountSid: "account_sid",
			CallSid:    "call_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.AccountSid)
```

## 获取会议录音转录文本

获取所有会议的录音转录文本。

`GET /texml/Accounts/{account_sid}/Transcriptions.json`

```go
	response, err := client.Texml.Accounts.GetTranscriptionsJson(
		context.TODO(),
		"account_sid",
		telnyx.TexmlAccountGetTranscriptionsJsonParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.End)
```

## 获取特定录音的转录文本

根据转录文本 ID 获取其详细信息。

`GET /texml/Accounts/{account_sid}/Transcriptions/{recording_transcription_sid}.json`

```go
	response, err := client.Texml.Accounts.Transcriptions.Json.GetRecordingTranscriptionSidJson(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.TexmlAccountTranscriptionJsonGetRecordingTranscriptionSidJsonParams{
			AccountSid: "account_sid",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.AccountSid)
```

## 删除录音转录文本

永久删除录音转录文本。

`DELETE /texml/Accounts/{account_sid}/Transcriptions/{recording_transcription_sid}.json`

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook 地址。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `TexmlCallAnsweredWebhook` | TeXML 通话已接听。当 TeXML 通话被接听时触发此 Webhook |
| `TexmlCallCompletedWebhook` | TeXML 通话已完成。当 TeXML 通话结束时触发此 Webhook |
| `TexmlCallInitiatedWebhook` | TeXML 通话已发起。当 TeXML 通话开始时触发此 Webhook |
| `TexmlCallRingingWebhook` | TeXML 通话正在振铃。当 TeXML 通话开始振铃时触发此 Webhook |
| `TexmlCallAmdWebhook` | TeXML 通话中的自动应答机检测（AMD）完成时触发此 Webhook |
| `TexmlCallDtmfWebhook` | TeXML 通话中接收到 DTMF 数字时触发此 Webhook |
| `TexmlGatherWebhook` | TeXML 采集操作完成时触发此 Webhook（发送到指定的动作 URL） |
| `TexmlHttpRequestWebhook` | TeXML HTTP 请求响应时触发此 Webhook |
| `TexmlAiGatherWebhook` | AI 采集完成并生成转录结果时触发此 Webhook |
| `TexmlConferenceJoinWebhook` | 会议参与者加入时触发此 Webhook |
| `TexmlConferenceLeaveWebhook` | 会议参与者离开时触发此 Webhook |
| `TexmlConferenceSpeakerWebhook` | 会议参与者开始或停止发言时触发此 Webhook |
| `TexmlConferenceEndWebhook` | 会议结束时触发此 Webhook |
| `TexmlConferenceStartWebhook` | 会议开始时触发此 Webhook |
| `TexmlQueueWebhook` | 队列状态事件触发时触发此 Webhook（由 `Enqueue` 命令的 `waitUrl` 触发） |
| `TexmlRecordingCompletedWebhook` | 通话中的录音完成时触发此 Webhook（由 `recordingStatusCallbackEvent` 触发） |
| `TexmlRecordingInProgressWebhook` | 通话中的录音开始时触发此 Webhook（由 `recordingStatusCallbackEvent` 触发） |
| `TexmlSiprecWebhook` | SIPREC 会话状态更新时触发此 Webhook |
| `TexmlStreamWebhook` | 流媒体传输状态更新时触发此 Webhook |
| `TexmlTranscriptionWebhook` | 录音转录完成时触发此 Webhook |
```
```