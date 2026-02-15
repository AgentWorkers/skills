---
name: telnyx-voice-streaming-go
description: >-
  Stream call audio in real-time, fork media to external destinations, and
  transcribe speech live. Use for real-time analytics and AI integrations. This
  skill provides Go SDK examples.
metadata:
  author: telnyx
  product: voice-streaming
  language: go
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 语音流媒体 - Go

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

以下所有示例均假设 `client` 已按照上述方式初始化完成。

## 启动分叉流媒体

`POST /calls/{call_control_id}/actions/fork_start`  
（用于将通话中的媒体内容实时传输到指定目标。）

```go
	response, err := client.Calls.Actions.StartForking(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStartForkingParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 停止分叉流媒体

`POST /calls/{call_control_id}/actions/fork_stop`  
（用于停止分叉流媒体功能。）

```go
	response, err := client.Calls.Actions.StopForking(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStopForkingParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 启动流媒体传输

`POST /calls/{call_control_id}/actions/streaming_start`  
（用于将通话中的媒体内容以接近实时的方式传输到指定的 WebSocket 地址或 Dialogflow 连接。）

```go
	response, err := client.Calls.Actions.StartStreaming(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStartStreamingParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 停止流媒体传输

`POST /calls/{call_control_id}/actions/streaming_stop`  
（用于停止向 WebSocket 的媒体传输。）

```go
	response, err := client.Calls.Actions.StopStreaming(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStopStreamingParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 启动实时转录

`POST /calls/{call_control_id}/actions/transcription_start`  
（用于启动实时转录功能。）

```go
	response, err := client.Calls.Actions.StartTranscription(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStartTranscriptionParams{
			TranscriptionStartRequest: telnyx.TranscriptionStartRequestParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 停止实时转录

`POST /calls/{call_control_id}/actions/transcription_stop`  
（用于停止实时转录功能。）

```go
	response, err := client.Calls.Actions.StopTranscription(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStopTranscriptionParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL：
所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callForkStarted` | 分叉流媒体功能已启动 |
| `callForkStopped` | 分叉流媒体功能已停止 |
| `callStreamingStarted` | 流媒体传输已启动 |
| `callStreamingStopped` | 流媒体传输已停止 |
| `callStreamingFailed` | 流媒体传输失败 |
| `transcription` | 实时转录功能已启动 |
| `transcriptionStopped` | 实时转录功能已停止 |
```
```