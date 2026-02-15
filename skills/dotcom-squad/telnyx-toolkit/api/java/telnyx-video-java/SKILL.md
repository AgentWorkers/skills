---
name: telnyx-video-java
description: >-
  Create and manage video rooms for real-time video communication and
  conferencing. This skill provides Java SDK examples.
metadata:
  author: telnyx
  product: video
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Video - Java

## 安装

```text
// See https://github.com/team-telnyx/telnyx-java for Maven/Gradle setup
```

## 设置

```java
import com.telnyx.sdk.client.TelnyxClient;
import com.telnyx.sdk.client.okhttp.TelnyxOkHttpClient;

TelnyxClient client = TelnyxOkHttpClient.fromEnv();
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 查看房间组成列表。

`GET /room_compositions`

```java
import com.telnyx.sdk.models.roomcompositions.RoomCompositionListPage;
import com.telnyx.sdk.models.roomcompositions.RoomCompositionListParams;

RoomCompositionListPage page = client.roomCompositions().list();
```

## 创建房间组成。

异步创建房间组成。

`POST /room_compositions`

```java
import com.telnyx.sdk.models.roomcompositions.RoomCompositionCreateParams;
import com.telnyx.sdk.models.roomcompositions.RoomCompositionCreateResponse;

RoomCompositionCreateResponse roomComposition = client.roomCompositions().create();
```

## 查看房间组成。

`GET /room_compositions/{room_composition_id}`

```java
import com.telnyx.sdk.models.roomcompositions.RoomCompositionRetrieveParams;
import com.telnyx.sdk.models.roomcompositions.RoomCompositionRetrieveResponse;

RoomCompositionRetrieveResponse roomComposition = client.roomCompositions().retrieve("5219b3af-87c6-4c08-9b58-5a533d893e21");
```

## 删除房间组成。

同步删除房间组成。

`DELETE /room_compositions/{room_composition_id}`

```java
import com.telnyx.sdk.models.roomcompositions.RoomCompositionDeleteParams;

client.roomCompositions().delete("5219b3af-87c6-4c08-9b58-5a533d893e21");
```

## 查看房间参与者列表。

`GET /room_participants`

```java
import com.telnyx.sdk.models.roomparticipants.RoomParticipantListPage;
import com.telnyx.sdk.models.roomparticipants.RoomParticipantListParams;

RoomParticipantListPage page = client.roomParticipants().list();
```

## 查看房间参与者。

`GET /room_participants/{room_participant_id}`

```java
import com.telnyx.sdk.models.roomparticipants.RoomParticipantRetrieveParams;
import com.telnyx.sdk.models.roomparticipants.RoomParticipantRetrieveResponse;

RoomParticipantRetrieveResponse roomParticipant = client.roomParticipants().retrieve("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0");
```

## 查看房间录制列表。

`GET /room_recordings`

```java
import com.telnyx.sdk.models.roomrecordings.RoomRecordingListPage;
import com.telnyx.sdk.models.roomrecordings.RoomRecordingListParams;

RoomRecordingListPage page = client.roomRecordings().list();
```

## 批量删除多个房间录制。

`DELETE /room_recordings`

```java
import com.telnyx.sdk.models.roomrecordings.RoomRecordingDeleteBulkParams;
import com.telnyx.sdk.models.roomrecordings.RoomRecordingDeleteBulkResponse;

RoomRecordingDeleteBulkResponse response = client.roomRecordings().deleteBulk();
```

## 查看房间录制。

`GET /room_recordings/{room_recording_id}`

```java
import com.telnyx.sdk.models.roomrecordings.RoomRecordingRetrieveParams;
import com.telnyx.sdk.models.roomrecordings.RoomRecordingRetrieveResponse;

RoomRecordingRetrieveResponse roomRecording = client.roomRecordings().retrieve("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0");
```

## 删除房间录制。

同步删除房间录制。

`DELETE /room_recordings/{room_recording_id}`

```java
import com.telnyx.sdk.models.roomrecordings.RoomRecordingDeleteParams;

client.roomRecordings().delete("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0");
```

## 查看房间会话列表。

`GET /room_sessions`

```java
import com.telnyx.sdk.models.rooms.sessions.SessionList0Page;
import com.telnyx.sdk.models.rooms.sessions.SessionList0Params;

SessionList0Page page = client.rooms().sessions().list0();
```

## 查看房间会话。

`GET /room_sessions/{room_session_id}`

```java
import com.telnyx.sdk.models.rooms.sessions.SessionRetrieveParams;
import com.telnyx.sdk.models.rooms.sessions.SessionRetrieveResponse;

SessionRetrieveResponse session = client.rooms().sessions().retrieve("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0");
```

## 结束房间会话。

注意：这也会将当前在房间中的所有参与者踢出。

`POST /room_sessions/{room_session_id}/actions/end`

```java
import com.telnyx.sdk.models.rooms.sessions.actions.ActionEndParams;
import com.telnyx.sdk.models.rooms.sessions.actions.ActionEndResponse;

ActionEndResponse response = client.rooms().sessions().actions().end("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0");
```

## 将参与者从房间会话中踢出。

`POST /room_sessions/{room_session_id}/actions/kick`

```java
import com.telnyx.sdk.models.rooms.sessions.actions.ActionKickParams;
import com.telnyx.sdk.models.rooms.sessions.actions.ActionKickResponse;
import com.telnyx.sdk.models.rooms.sessions.actions.ActionsParticipantsRequest;

ActionKickParams params = ActionKickParams.builder()
    .roomSessionId("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")
    .actionsParticipantsRequest(ActionsParticipantsRequest.builder().build())
    .build();
ActionKickResponse response = client.rooms().sessions().actions().kick(params);
```

## 静音房间会话中的参与者。

`POST /room_sessions/{room_session_id}/actions/mute`

```java
import com.telnyx.sdk.models.rooms.sessions.actions.ActionMuteParams;
import com.telnyx.sdk.models.rooms.sessions.actions.ActionMuteResponse;
import com.telnyx.sdk.models.rooms.sessions.actions.ActionsParticipantsRequest;

ActionMuteParams params = ActionMuteParams.builder()
    .roomSessionId("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")
    .actionsParticipantsRequest(ActionsParticipantsRequest.builder().build())
    .build();
ActionMuteResponse response = client.rooms().sessions().actions().mute(params);
```

## 恢复房间会话中参与者的音量。

`POST /room_sessions/{room_session_id}/actions/unmute`

```java
import com.telnyx.sdk.models.rooms.sessions.actions.ActionUnmuteParams;
import com.telnyx.sdk.models.rooms.sessions.actions.ActionUnmuteResponse;
import com.telnyx.sdk.models.rooms.sessions.actions.ActionsParticipantsRequest;

ActionUnmuteParams params = ActionUnmuteParams.builder()
    .roomSessionId("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")
    .actionsParticipantsRequest(ActionsParticipantsRequest.builder().build())
    .build();
ActionUnmuteResponse response = client.rooms().sessions().actions().unmute(params);
```

## 查看房间参与者列表。

`GET /room_sessions/{room_session_id}/participants`

```java
import com.telnyx.sdk.models.rooms.sessions.SessionRetrieveParticipantsPage;
import com.telnyx.sdk.models.rooms.sessions.SessionRetrieveParticipantsParams;

SessionRetrieveParticipantsPage page = client.rooms().sessions().retrieveParticipants("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0");
```

## 查看房间列表。

`GET /rooms`

```java
import com.telnyx.sdk.models.rooms.RoomListPage;
import com.telnyx.sdk.models.rooms.RoomListParams;

RoomListPage page = client.rooms().list();
```

## 创建房间。

同步创建房间。

`POST /rooms`

```java
import com.telnyx.sdk.models.rooms.RoomCreateParams;
import com.telnyx.sdk.models.rooms.RoomCreateResponse;

RoomCreateResponse room = client.rooms().create();
```

## 查看房间信息。

`GET /rooms/{room_id}`

```java
import com.telnyx.sdk.models.rooms.RoomRetrieveParams;
import com.telnyx.sdk.models.rooms.RoomRetrieveResponse;

RoomRetrieveResponse room = client.rooms().retrieve("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0");
```

## 更新房间信息。

同步更新房间信息。

`PATCH /rooms/{room_id}`

```java
import com.telnyx.sdk.models.rooms.RoomUpdateParams;
import com.telnyx.sdk.models.rooms.RoomUpdateResponse;

RoomUpdateResponse room = client.rooms().update("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0");
```

## 删除房间。

同步删除房间。

`DELETE /rooms/{room_id}`

```java
import com.telnyx.sdk.models.rooms.RoomDeleteParams;

client.rooms().delete("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0");
```

## 创建客户端令牌以加入房间。

同步创建客户端令牌以加入房间。

`POST /rooms/{room_id}/actions/generate_join_client_token`

```java
import com.telnyx.sdk.models.rooms.actions.ActionGenerateJoinClientTokenParams;
import com.telnyx.sdk.models.rooms.actions.ActionGenerateJoinClientTokenResponse;

ActionGenerateJoinClientTokenResponse response = client.rooms().actions().generateJoinClientToken("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0");
```

## 刷新客户端令牌以加入房间。

同步刷新客户端令牌以加入房间。

`POST /rooms/{room_id}/actions/refresh_client_token` — 需要参数：`refresh_token`

```java
import com.telnyx.sdk.models.rooms.actions.ActionRefreshClientTokenParams;
import com.telnyx.sdk.models.rooms.actions.ActionRefreshClientTokenResponse;

ActionRefreshClientTokenParams params = ActionRefreshClientTokenParams.builder()
    .roomId("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")
    .refreshToken("eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ0ZWxueXhfdGVsZXBob255IiwiZXhwIjoxNTkwMDEwMTQzLCJpYXQiOjE1ODc1OTA5NDMsImlzcyI6InRlbG55eF90ZWxlcGhvbnkiLCJqdGkiOiJiOGM3NDgzNy1kODllLTRhNjUtOWNmMi0zNGM3YTZmYTYwYzgiLCJuYmYiOjE1ODc1OTA5NDIsInN1YiI6IjVjN2FjN2QwLWRiNjUtNGYxMS05OGUxLWVlYzBkMWQ1YzZhZSIsInRlbF90b2tlbiI6InJqX1pra1pVT1pNeFpPZk9tTHBFVUIzc2lVN3U2UmpaRmVNOXMtZ2JfeENSNTZXRktGQUppTXlGMlQ2Q0JSbWxoX1N5MGlfbGZ5VDlBSThzRWlmOE1USUlzenl6U2xfYURuRzQ4YU81MHlhSEd1UlNZYlViU1ltOVdJaVEwZz09IiwidHlwIjoiYWNjZXNzIn0.gNEwzTow5MLLPLQENytca7pUN79PmPj6FyqZWW06ZeEmesxYpwKh0xRtA0TzLh6CDYIRHrI8seofOO0YFGDhpQ")
    .build();
ActionRefreshClientTokenResponse response = client.rooms().actions().refreshClientToken(params);
```

## 查看房间会话列表。

`GET /rooms/{room_id}/sessions`

```java
import com.telnyx.sdk.models.rooms.sessions.SessionList1Page;
import com.telnyx.sdk.models.rooms.sessions.SessionList1Params;

SessionList1Page page = client.rooms().sessions().list1("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0");
```