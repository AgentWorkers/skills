---
name: telnyx-voice-conferencing-go
description: >-
  Create and manage conference calls, queues, and multi-party sessions. Use when
  building call centers or conferencing applications. This skill provides Go SDK
  examples.
metadata:
  author: telnyx
  product: voice-conferencing
  language: go
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 语音会议 - Go

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

## 将呼叫放入队列

将呼叫放入队列中。

`POST /calls/{call_control_id}/actions/enqueue` — 必需参数：`queue_name`

```go
	response, err := client.Calls.Actions.Enqueue(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionEnqueueParams{
			QueueName: "support",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 从队列中移除呼叫

从队列中移除呼叫。

`POST /calls/{call_control_id}/actions/leave_queue`

```go
	response, err := client.Calls.Actions.LeaveQueue(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionLeaveQueueParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出会议

列出所有会议。

`GET /conferences`

```go
	page, err := client.Conferences.List(context.TODO(), telnyx.ConferenceListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建会议

使用 `call_control_id` 和会议名称从现有的通话中创建会议。

`POST /conferences` — 必需参数：`call_control_id`, `name`

```go
	conference, err := client.Conferences.New(context.TODO(), telnyx.ConferenceNewParams{
		CallControlID: "v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg",
		Name:          "Business",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", conference.Data)
```

## 获取会议信息

获取现有会议的信息。

`GET /conferences/{id}`

```go
	conference, err := client.Conferences.Get(
		context.TODO(),
		"id",
		telnyx.ConferenceGetParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", conference.Data)
```

## 暂停会议参与者的发言

暂停会议中参与者的发言。

`POST /conferences/{id}/actions/hold`

```go
	response, err := client.Conferences.Actions.Hold(
		context.TODO(),
		"id",
		telnyx.ConferenceActionHoldParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 加入会议

加入现有的通话以参与会议。

`POST /conferences/{id}/actions/join` — 必需参数：`call_control_id`

```go
	response, err := client.Conferences.Actions.Join(
		context.TODO(),
		"id",
		telnyx.ConferenceActionJoinParams{
			CallControlID: "v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 退出会议

将通话从会议中移除并恢复到待处理状态。

`POST /conferences/{id}/actions/leave` — 必需参数：`call_control_id`

```go
	response, err := client.Conferences.Actions.Leave(
		context.TODO(),
		"id",
		telnyx.ConferenceActionLeaveParams{
			CallControlID: "c46e06d7-b78f-4b13-96b6-c576af9640ff",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 静音会议参与者

静音会议中的所有参与者。

`POST /conferences/{id}/actions/mute`

```go
	response, err := client.Conferences.Actions.Mute(
		context.TODO(),
		"id",
		telnyx.ConferenceActionMuteParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 播放音频给会议参与者

向会议中的所有或部分参与者播放音频。

`POST /conferences/{id}/actions/play`

```go
	response, err := client.Conferences.Actions.Play(
		context.TODO(),
		"id",
		telnyx.ConferenceActionPlayParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 暂停会议录制

暂停会议录制。

`POST /conferences/{id}/actions/record_PAUSE`

```go
	response, err := client.Conferences.Actions.RecordPause(
		context.TODO(),
		"id",
		telnyx.ConferenceActionRecordPauseParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 恢复会议录制

恢复会议录制。

`POST /conferences/{id}/actions/record_resume`

```go
	response, err := client.Conferences.Actions.RecordResume(
		context.TODO(),
		"id",
		telnyx.ConferenceActionRecordResumeParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 开始会议录制

开始会议录制。

`POST /conferences/{id}/actions/record_start` — 必需参数：`format`

```go
	response, err := client.Conferences.Actions.RecordStart(
		context.TODO(),
		"id",
		telnyx.ConferenceActionRecordStartParams{
			Format: telnyx.ConferenceActionRecordStartParamsFormatWav,
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 停止会议录制

停止会议录制。

`POST /conferences/{id}/actions/record_stop`

```go
	response, err := client.Conferences.Actions.RecordStop(
		context.TODO(),
		"id",
		telnyx.ConferenceActionRecordStopParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 向会议参与者朗读文本

将文本转换为语音并播放给所有或部分参与者。

`POST /conferences/{id}/actions/speak` — 必需参数：`payload`, `voice`

```go
	response, err := client.Conferences.Actions.Speak(
		context.TODO(),
		"id",
		telnyx.ConferenceActionSpeakParams{
			Payload: "Say this to participants",
			Voice:   "female",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 停止向会议参与者播放音频

停止向会议中的所有或部分参与者播放音频。

`POST /conferences/{id}/actions/stop`

```go
	response, err := client.Conferences.Actions.Stop(
		context.TODO(),
		"id",
		telnyx.ConferenceActionStopParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 恢复会议参与者的发言权限

恢复会议中参与者的发言权限。

`POST /conferences/{id}/actions/unhold` — 必需参数：`call_control_ids`

```go
	response, err := client.Conferences.Actions.Unhold(
		context.TODO(),
		"id",
		telnyx.ConferenceActionUnholdParams{
			CallControlIDs: []string{"v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg"},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 解除会议参与者的静音状态

取消会议中参与者的静音状态。

`POST /conferences/{id}/actions/unmute`

```go
	response, err := client.Conferences.Actions.Unmute(
		context.TODO(),
		"id",
		telnyx.ConferenceActionUnmuteParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 更新会议参与者信息

更新会议参与者的角色。

`POST /conferences/{id}/actions/update` — 必需参数：`call_control_id`, `supervisor_role`

```go
	action, err := client.Conferences.Actions.Update(
		context.TODO(),
		"id",
		telnyx.ConferenceActionUpdateParams{
			UpdateConference: telnyx.UpdateConferenceParam{
				CallControlID:  "v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg",
				SupervisorRole: telnyx.UpdateConferenceSupervisorRoleWhisper,
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", action.Data)
```

## 列出会议参与者

列出会议的所有参与者。

`GET /conferences/{conference_id}/participants`

```go
	page, err := client.Conferences.ListParticipants(
		context.TODO(),
		"conference_id",
		telnyx.ConferenceListParticipantsParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

---

## Webhook

以下 Webhook 事件会发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callEnqueued` | 呼叫被放入队列 |
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