---
name: telnyx-voice-advanced-go
description: >-
  Advanced call control features including DTMF sending, SIPREC recording, noise
  suppression, client state, and supervisor controls. This skill provides Go SDK
  examples.
metadata:
  author: telnyx
  product: voice-advanced
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Voice Advanced - Go

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

以下所有示例均假设 `client` 已经按照上述方式初始化。

## 更新客户端状态

更新客户端状态

`PUT /calls/{call_control_id}/actions/client_state_update` — 必需参数：`client_state`

```go
	response, err := client.Calls.Actions.UpdateClientState(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionUpdateClientStateParams{
			ClientState: "aGF2ZSBhIG5pY2UgZGF5ID1d",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## SIP 转接呼叫

在呼叫控制过程中发起 SIP 转接。

`POST /calls/{call_control_id}/actions/refer` — 必需参数：`sip_address`

```go
	response, err := client.Calls.Actions.Refer(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionReferParams{
			SipAddress: "sip:username@sip.non-telnyx-address.com",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 发送 DTMF 音调

从当前通话链路发送 DTMF 音调。

`POST /calls/{call_control_id}/actions/send_dtmf` — 必需参数：`digits`

```go
	response, err := client.Calls.Actions.SendDtmf(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionSendDtmfParams{
			Digits: "1www2WABCDw9",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 启动 SIPREC 会话

启动在 SIPREC 连接器 SRS 中配置的 SIPREC 会话。

`POST /calls/{call_control_id}/actions/siprec_start`

```go
	response, err := client.Calls.Actions.StartSiprec(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStartSiprecParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 停止 SIPREC 会话

停止 SIPREC 会话。

`POST /calls/{call_control_id}/actions/siprec_stop`

```go
	response, err := client.Calls.Actions.StopSiprec(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStopSiprecParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 噪音抑制（测试版）

启动噪声抑制功能。

`POST /calls/{call_control_id}/actions/suppression_start`

```go
	response, err := client.Calls.Actions.StartNoiseSuppression(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStartNoiseSuppressionParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 停止噪声抑制（测试版）

停止噪声抑制功能。

`POST /calls/{call_control_id}/actions/suppression_stop`

```go
	response, err := client.Calls.Actions.StopNoiseSuppression(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionStopNoiseSuppressionParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 切换监督者角色

切换桥接呼叫的监督者角色。

`POST /calls/{call_control_id}/actions/switch_supervisor_role` — 必需参数：`role`

```go
	response, err := client.Calls.Actions.SwitchSupervisorRole(
		context.TODO(),
		"call_control_id",
		telnyx.CallActionSwitchSupervisorRoleParams{
			Role: telnyx.CallActionSwitchSupervisorRoleParamsRoleBarge,
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callReferStarted` | 转接呼叫开始 |
| `callReferCompleted` | 转接呼叫完成 |
| `callReferFailed` | 转接呼叫失败 |
| `callSiprecStarted` | SIPREC 会话开始 |
| `callSiprecStopped` | SIPREC 会话停止 |
| `callSiprecFailed` | SIPREC 会话失败 |