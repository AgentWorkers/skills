---
name: telnyx-voice-gather-go
description: >-
  Collect DTMF input and speech from callers using standard gather or AI-powered
  gather. Build interactive voice menus and AI voice assistants. This skill
  provides Go SDK examples.
metadata:
  author: telnyx
  product: voice-gather
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 本文档由 Telnyx OpenAPI 规范自动生成，请勿修改。 -->

# Telnyx 语音采集 - Go

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

以下所有示例均假设 `client` 已按上述方式初始化。

## 向 AI 助手添加消息

向 AI 助手发起的通话中添加消息。

`POST /calls/{call_control_id}/actions/ai_assistant_add_messages`

```go
	response, err := client.Calls.Actions.AddAIAssistantMessages(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionAddAIAssistantMessagesParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 启动 AI 助手

在通话中启动 AI 助手。

`POST /calls/{call_control_id}/actions/ai_assistant_start`

```go
	response, err := client.Calls.Actions.StartAIAssistant(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStartAIAssistantParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 停止 AI 助手

在通话中停止 AI 助手。

`POST /calls/{call_control_id}/actions/ai_assistant_stop`

```go
	response, err := client.Calls.Actions.StopAIAssistant(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStopAIAssistantParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 停止数据采集

停止当前的数据采集操作。

`POST /calls/{call_control_id}/actions/gather_stop`

```go
	response, err := client.Calls.Actions.StopGather(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStopGatherParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 使用 AI 进行数据采集

使用语音助手收集请求负载中定义的参数。

`POST /calls/{call_control_id}/actions/gather_using_ai` — 必需参数：`parameters`

```go
	response, err := client.Calls.Actions.GatherUsingAI(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionGatherUsingAIParams{
			Parameters: map[string]any{
				"properties": "bar",
				"required":   "bar",
				"type":       "bar",
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 使用音频进行数据采集

在通话中播放音频文件，直到收集到所需的 DTMF 信号以构建交互式菜单。

`POST /calls/{call_control_id}/actions/gather_using_audio`

```go
	response, err := client.Calls.Actions.GatherUsingAudio(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionGatherUsingAudioParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 使用文本转语音功能进行数据采集

将文本转换为语音并在通话中播放，直到收集到所需的 DTMF 信号以构建交互式菜单。

`POST /calls/{call_control_id}/actions/gather_using_speak` — 必需参数：`voice`, `payload`

```go
	response, err := client.Calls.Actions.GatherUsingSpeak(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionGatherUsingSpeakParams{
			Payload: "say this on call",
			Voice:   "male",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 数据采集

收集 DTMF 信号以构建交互式菜单。

`POST /calls/{call_control_id}/actions/gather`

```go
	response, err := client.Calls.Actions.Gather(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionGatherParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

---

## Webhook

以下 webhook 事件会被发送到您配置的 webhook URL：
所有 webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头，用于验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callGatherEnded` | 通话数据采集结束 |
| `CallAIGatherEnded` | 通话中 AI 数据采集结束 |
| `CallAIGatherMessageHistoryUpdated` | 通话中 AI 数据采集消息历史更新 |
| `CallAIGatherPartialResults` | 通话中 AI 数据采集部分结果 |
| `CallConversationEnded` | 通话结束 |
| `callPlaybackStarted` | 通话播放开始 |
| `callPlaybackEnded` | 通话播放结束 |
| `callDtmfReceived` | 通话中接收到 DTMF 信号 |