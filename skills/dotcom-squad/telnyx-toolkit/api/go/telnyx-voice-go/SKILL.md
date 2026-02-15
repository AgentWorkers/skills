---
name: telnyx-voice-go
description: >-
  Make and receive calls, transfer, bridge, and manage call lifecycle with Call
  Control. Includes application management and call events. This skill provides
  Go SDK examples.
metadata:
  author: telnyx
  product: voice
  language: go
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Voice - Go

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

## 接听来电

接听传入的电话。

`POST /calls/{call_control_id}/actions/answer`

```go
	response, err := client.Calls.Actions.Answer(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionAnswerParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 桥接通话

将两个通话控制请求进行桥接。

`POST /calls/{call_control_id}/actions/bridge` — 必需参数：`call_control_id`

```go
	response, err := client.Calls.Actions.Bridge(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionBridgeParams{
			CallControlIDToBridgeWith: "v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 拨打电话

从指定的连接拨打一个号码或 SIP URI。

`POST /calls` — 必需参数：`connection_id`, `to`, `from`

```go
	response, err := client.Calls.Dial(context.TODO(), telnyx.CallDialParams{
		ConnectionID: "7267xxxxxxxxxxxxxx",
		From:         "+18005550101",
		To: telnyx.CallDialParamsToUnion{
			OfString: telnyx.String("+18005550100"),
		},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 挂断电话

挂断通话。

`POST /calls/{call_control_id}/actions/hangup`

```go
	response, err := client.Calls.Actions.Hangup(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionHangupParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 转接电话

将通话转接到新的目的地。

`POST /calls/{call_control_id}/actions/transfer` — 必需参数：`to`

```go
	response, err := client.Calls.Actions.Transfer(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionTransferParams{
			To: "+18005550100",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出指定连接的所有活动通话

列出指定连接的所有活动通话。

`GET /connections/{connection_id}/active_calls`

```go
	page, err := client.Connections.ListActiveCalls(
		context.TODO(),
		"1293384261075731461",
		telnyx.ConnectionListActiveCallsParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 列出通话控制应用程序

返回通话控制应用程序的列表。

`GET /call_control_applications`

```go
	page, err := client.CallControlApplications.List(context.TODO(), telnyx.CallControlApplicationListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建通话控制应用程序

创建一个新的通话控制应用程序。

`POST /call_control_applications` — 必需参数：`application_name`, `webhook_event_url`

```go
	callControlApplication, err := client.CallControlApplications.New(context.TODO(), telnyx.CallControlApplicationNewParams{
		ApplicationName: "call-router",
		WebhookEventURL: "https://example.com",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", callControlApplication.Data)
```

## 获取通话控制应用程序的详细信息

获取现有通话控制应用程序的详细信息。

`GET /call_control_applications/{id}`

```go
	callControlApplication, err := client.CallControlApplications.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", callControlApplication.Data)
```

## 更新通话控制应用程序

更新现有通话控制应用程序的设置。

`PATCH /call_control_applications/{id}` — 必需参数：`application_name`, `webhook_event_url`

```go
	callControlApplication, err := client.CallControlApplications.Update(
		context.TODO(),
		"id",
		telnyx.CallControlApplicationUpdateParams{
			ApplicationName: "call-router",
			WebhookEventURL: "https://example.com",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", callControlApplication.Data)
```

## 删除通话控制应用程序

删除通话控制应用程序。

`DELETE /call_control_applications/{id}`

```go
	callControlApplication, err := client.CallControlApplications.Delete(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", callControlApplication.Data)
```

## 列出通话事件

根据指定的过滤参数筛选通话事件。

`GET /call_events`

```go
	page, err := client.CallEvents.List(context.TODO(), telnyx.CallEventListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callAnswered` | 电话已接听 |
| `callStreamingStarted` | 通话流开始 |
| `callStreamingStopped` | 通话流停止 |
| `callStreamingFailed` | 通话流失败 |
| `callBridged` | 通话被桥接 |
| `callInitiated` | 通话开始 |
| `callHangup` | 电话挂断 |
| `callRecordingSaved` | 通话录音保存 |
| `callMachineDetectionEnded` | 机器检测结束 |
| `callMachineGreetingEnded` | 机器问候结束 |
| `callMachinePremiumDetectionEnded` | 机器高级检测结束 |
| `callMachinePremiumGreetingEnded` | 机器高级问候结束 |
```
```