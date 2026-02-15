---
name: telnyx-video-go
description: >-
  Create and manage video rooms for real-time video communication and
  conferencing. This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: video
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Video - Go

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

## 查看房间组合列表

`GET /room_compositions`

```go
	page, err := client.RoomCompositions.List(context.TODO(), telnyx.RoomCompositionListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建房间组合

异步创建房间组合。

`POST /room_compositions`

```go
	roomComposition, err := client.RoomCompositions.New(context.TODO(), telnyx.RoomCompositionNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", roomComposition.Data)
```

## 查看房间组合信息

`GET /room_compositions/{room_composition_id}`

```go
	roomComposition, err := client.RoomCompositions.Get(context.TODO(), "5219b3af-87c6-4c08-9b58-5a533d893e21")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", roomComposition.Data)
```

## 删除房间组合

同步删除房间组合。

`DELETE /room_compositions/{room_composition_id}`

```go
	err := client.RoomCompositions.Delete(context.TODO(), "5219b3af-87c6-4c08-9b58-5a533d893e21")
	if err != nil {
		panic(err.Error())
	}
```

## 查看房间参与者列表

`GET /room_participants`

```go
	page, err := client.RoomParticipants.List(context.TODO(), telnyx.RoomParticipantListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 查看房间参与者信息

`GET /room_participants/{room_participant_id}`

```go
	roomParticipant, err := client.RoomParticipants.Get(context.TODO(), "0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", roomParticipant.Data)
```

## 查看房间录像列表

`GET /room_recordings`

```go
	page, err := client.RoomRecordings.List(context.TODO(), telnyx.RoomRecordingListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 批量删除房间录像

`DELETE /room_recordings`

```go
	response, err := client.RoomRecordings.DeleteBulk(context.TODO(), telnyx.RoomRecordingDeleteBulkParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 查看房间录像信息

`GET /room_recordings/{room_recording_id}`

```go
	roomRecording, err := client.RoomRecordings.Get(context.TODO(), "0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", roomRecording.Data)
```

## 删除房间录像

同步删除房间录像。

`DELETE /room_recordings/{room_recording_id}`

```go
	err := client.RoomRecordings.Delete(context.TODO(), "0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")
	if err != nil {
		panic(err.Error())
	}
```

## 查看房间会话列表

`GET /room_sessions`

```go
	page, err := client.Rooms.Sessions.List0(context.TODO(), telnyx.RoomSessionList0Params{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 查看房间会话信息

`GET /room_sessions/{room_session_id}`

```go
	session, err := client.Rooms.Sessions.Get(
		context.TODO(),
		"0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
		telnyx.RoomSessionGetParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", session.Data)
```

## 结束房间会话

注意：此操作也会将当前在房间中的所有参与者踢出。

`POST /room_sessions/{room_session_id}/actions/end`

```go
	response, err := client.Rooms.Sessions.Actions.End(context.TODO(), "0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 将参与者踢出房间会话

`POST /room_sessions/{room_session_id}/actions/kick`

```go
	response, err := client.Rooms.Sessions.Actions.Kick(
		context.TODO(),
		"0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
		telnyx.RoomSessionActionKickParams{
			ActionsParticipantsRequest: telnyx.ActionsParticipantsRequestParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 将房间中的参与者静音

`POST /room_sessions/{room_session_id}/actions/mute`

```go
	response, err := client.Rooms.Sessions.Actions.Mute(
		context.TODO(),
		"0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
		telnyx.RoomSessionActionMuteParams{
			ActionsParticipantsRequest: telnyx.ActionsParticipantsRequestParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 解除房间中参与者的静音

`POST /room_sessions/{room_session_id}/actions/unmute`

```go
	response, err := client.Rooms.Sessions.Actions.Unmute(
		context.TODO(),
		"0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
		telnyx.RoomSessionActionUnmuteParams{
			ActionsParticipantsRequest: telnyx.ActionsParticipantsRequestParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 查看房间参与者列表

`GET /room_sessions/{room_session_id}/participants`

```go
	page, err := client.Rooms.Sessions.GetParticipants(
		context.TODO(),
		"0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
		telnyx.RoomSessionGetParticipantsParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 查看房间列表

`GET /rooms`

```go
	page, err := client.Rooms.List(context.TODO(), telnyx.RoomListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建房间

同步创建房间。

`POST /rooms`

```go
	room, err := client.Rooms.New(context.TODO(), telnyx.RoomNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", room.Data)
```

## 查看房间信息

`GET /rooms/{room_id}`

```go
	room, err := client.Rooms.Get(
		context.TODO(),
		"0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
		telnyx.RoomGetParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", room.Data)
```

## 更新房间信息

同步更新房间信息。

`PATCH /rooms/{room_id}`

```go
	room, err := client.Rooms.Update(
		context.TODO(),
		"0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
		telnyx.RoomUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", room.Data)
```

## 删除房间

同步删除房间。

`DELETE /rooms/{room_id}`

```go
	err := client.Rooms.Delete(context.TODO(), "0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")
	if err != nil {
		panic(err.Error())
	}
```

## 创建客户端令牌以加入房间

同步创建客户端令牌以加入房间。

`POST /rooms/{room_id}/actions/generate_join_client_token`

```go
	response, err := client.Rooms.Actions.GenerateJoinClientToken(
		context.TODO(),
		"0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
		telnyx.RoomActionGenerateJoinClientTokenParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 刷新客户端令牌以加入房间

同步刷新客户端令牌以加入房间。

`POST /rooms/{room_id}/actions/refresh_client_token` — 需要参数：`refresh_token`

```go
	response, err := client.Rooms.Actions.RefreshClientToken(
		context.TODO(),
		"0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
		telnyx.RoomActionRefreshClientTokenParams{
			RefreshToken: "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ0ZWxueXhfdGVsZXBob255IiwiZXhwIjoxNTkwMDEwMTQzLCJpYXQiOjE1ODc1OTA5NDMsImlzcyI6InRlbG55eF90ZWxlcGhvbnkiLCJqdGkiOiJiOGM3NDgzNy1kODllLTRhNjUtOWNmMi0zNGM3YTZmYTYwYzgiLCJuYmYiOjE1ODc1OTA5NDIsInN1YiI6IjVjN2FjN2QwLWRiNjUtNGYxMS05OGUxLWVlYzBkMWQ1YzZhZSIsInRlbF90b2tlbiI6InJqX1pra1pVT1pNeFpPZk9tTHBFVUIzc2lVN3U2UmpaRmVNOXMtZ2JfeENSNTZXRktGQUppTXlGMlQ2Q0JSbWxoX1N5MGlfbGZ5VDlBSThzRWlmOE1USUlzenl6U2xfYURuRzQ4YU81MHlhSEd1UlNZYlViU1ltOVdJaVEwZz09IiwidHlwIjoiYWNjZXNzIn0.gNEwzTow5MLLPLQENytca7pUN79PmPj6FyqZWW06ZeEmesxYpwKh0xRtA0TzLh6CDYIRHrI8seofOO0YFGDhpQ",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 查看房间会话列表

`GET /rooms/{room_id}/sessions`

```go
	page, err := client.Rooms.Sessions.List1(
		context.TODO(),
		"0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
		telnyx.RoomSessionList1Params{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```