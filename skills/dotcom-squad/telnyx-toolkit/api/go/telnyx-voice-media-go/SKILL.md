---
name: telnyx-voice-media-go
description: >-
  Play audio files, use text-to-speech, and record calls. Use when building IVR
  systems, playing announcements, or recording conversations. This skill
  provides Go SDK examples.
metadata:
  author: telnyx
  product: voice-media
  language: go
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Voice Media - Go

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

## 播放音频文件

在通话中播放音频文件。

`POST /calls/{call_control_id}/actions/playback_start`

```go
	response, err := client.Calls.Actions.StartPlayback(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStartPlaybackParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 停止音频播放

停止通话中的音频播放。

`POST /calls/{call_control_id}/actions/playback_stop`

```go
	response, err := client.Calls.Actions.StopPlayback(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStopPlaybackParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 暂停录音

暂停通话的录音。

`POST /calls/{call_control_id}/actions/record_PAUSE`

```go
	response, err := client.Calls.Actions.PauseRecording(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionPauseRecordingParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 恢复录音

恢复通话的录音。

`POST /calls/{call_control_id}/actions/record.resume`

```go
	response, err := client.Calls.Actions.ResumeRecording(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionResumeRecordingParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 开始录音

开始通话的录音。

`POST /calls/{call_control_id}/actions/record_start` — 必需参数：`format`, `channels`

```go
	response, err := client.Calls.Actions.StartRecording(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStartRecordingParams{
			Channels: telnyx.CallActionStartRecordingParamsChannelsSingle,
			Format:   telnyx.CallActionStartRecordingParamsFormatWav,
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 停止录音

停止通话的录音。

`POST /calls/{call_control_id}/actions/record_stop`

```go
	response, err := client.Calls.Actions.StopRecording(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStopRecordingParams{
			StopRecordingRequest: telnyx.StopRecordingRequestParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 将文本转换为语音并在通话中播放

将文本转换为语音并在通话中播放。

`POST /calls/{call_control_id}/actions/speak` — 必需参数：`payload`, `voice`

```go
	response, err := client.Calls.Actions.Speak(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionSpeakParams{
			Payload: "Say this on the call",
			Voice:   "female",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

---

## Webhook

以下 webhook 事件会被发送到您配置的 webhook URL：
所有 webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 头部信息以进行验证（兼容标准 Webhook）。

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