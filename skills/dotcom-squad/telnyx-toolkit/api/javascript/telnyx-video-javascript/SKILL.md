---
name: telnyx-video-javascript
description: >-
  Create and manage video rooms for real-time video communication and
  conferencing. This skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: video
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Video - JavaScript

## 安装

```bash
npm install telnyx
```

## 设置

```javascript
import Telnyx from 'telnyx';

const client = new Telnyx({
  apiKey: process.env['TELNYX_API_KEY'], // This is the default and can be omitted
});
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 查看房间组合列表

`GET /room_compositions`

```javascript
// Automatically fetches more pages as needed.
for await (const roomComposition of client.roomCompositions.list()) {
  console.log(roomComposition.id);
}
```

## 创建房间组合

异步创建房间组合。

`POST /room_compositions`

```javascript
const roomComposition = await client.roomCompositions.create();

console.log(roomComposition.data);
```

## 查看房间组合信息

`GET /room_compositions/{room_composition_id}`

```javascript
const roomComposition = await client.roomCompositions.retrieve(
  '5219b3af-87c6-4c08-9b58-5a533d893e21',
);

console.log(roomComposition.data);
```

## 删除房间组合

同步删除房间组合。

`DELETE /room_compositions/{room_composition_id}`

```javascript
await client.roomCompositions.delete('5219b3af-87c6-4c08-9b58-5a533d893e21');
```

## 查看房间参与者列表

`GET /room_participants`

```javascript
// Automatically fetches more pages as needed.
for await (const roomParticipant of client.roomParticipants.list()) {
  console.log(roomParticipant.id);
}
```

## 查看房间参与者信息

`GET /room_participants/{room_participant_id}`

```javascript
const roomParticipant = await client.roomParticipants.retrieve(
  '0ccc7b54-4df3-4bca-a65a-3da1ecc777f0',
);

console.log(roomParticipant.data);
```

## 查看房间录制列表

`GET /room_recordings`

```javascript
// Automatically fetches more pages as needed.
for await (const roomRecordingListResponse of client.roomRecordings.list()) {
  console.log(roomRecordingListResponse.id);
}
```

## 批量删除房间录制文件

`DELETE /room_recordings`

```javascript
const response = await client.roomRecordings.deleteBulk();

console.log(response.data);
```

## 查看房间录制文件信息

`GET /room_recordings/{room_recording_id}`

```javascript
const roomRecording = await client.roomRecordings.retrieve('0ccc7b54-4df3-4bca-a65a-3da1ecc777f0');

console.log(roomRecording.data);
```

## 删除房间录制文件

同步删除房间录制文件。

`DELETE /room_recordings/{room_recording_id}`

```javascript
await client.roomRecordings.delete('0ccc7b54-4df3-4bca-a65a-3da1ecc777f0');
```

## 查看房间会话列表

`GET /room_sessions`

```javascript
// Automatically fetches more pages as needed.
for await (const roomSession of client.rooms.sessions.list0()) {
  console.log(roomSession.id);
}
```

## 查看房间会话信息

`GET /room_sessions/{room_session_id}`

```javascript
const session = await client.rooms.sessions.retrieve('0ccc7b54-4df3-4bca-a65a-3da1ecc777f0');

console.log(session.data);
```

## 结束房间会话

注意：此操作会同时将当前在房间中的所有参与者踢出。

`POST /room_sessions/{room_session_id}/actions/end`

```javascript
const response = await client.rooms.sessions.actions.end('0ccc7b54-4df3-4bca-a65a-3da1ecc777f0');

console.log(response.data);
```

## 将参与者从房间会话中踢出

`POST /room_sessions/{room_session_id}/actions/kick`

```javascript
const response = await client.rooms.sessions.actions.kick('0ccc7b54-4df3-4bca-a65a-3da1ecc777f0');

console.log(response.data);
```

## 静音房间中的参与者

`POST /room_sessions/{room_session_id}/actions/mute`

```javascript
const response = await client.rooms.sessions.actions.mute('0ccc7b54-4df3-4bca-a65a-3da1ecc777f0');

console.log(response.data);
```

## 恢复房间中参与者的麦克风权限

`POST /room_sessions/{room_session_id}/actions/unmute`

```javascript
const response = await client.rooms.sessions.actions.unmute('0ccc7b54-4df3-4bca-a65a-3da1ecc777f0');

console.log(response.data);
```

## 查看房间参与者列表

`GET /room_sessions/{room_session_id}/participants`

```javascript
// Automatically fetches more pages as needed.
for await (const roomParticipant of client.rooms.sessions.retrieveParticipants(
  '0ccc7b54-4df3-4bca-a65a-3da1ecc777f0',
)) {
  console.log(roomParticipant.id);
}
```

## 查看房间列表

`GET /rooms`

```javascript
// Automatically fetches more pages as needed.
for await (const room of client.rooms.list()) {
  console.log(room.id);
}
```

## 创建房间

同步创建房间。

`POST /rooms`

```javascript
const room = await client.rooms.create();

console.log(room.data);
```

## 查看房间信息

`GET /rooms/{room_id}`

```javascript
const room = await client.rooms.retrieve('0ccc7b54-4df3-4bca-a65a-3da1ecc777f0');

console.log(room.data);
```

## 更新房间信息

同步更新房间信息。

`PATCH /rooms/{room_id}`

```javascript
const room = await client.rooms.update('0ccc7b54-4df3-4bca-a65a-3da1ecc777f0');

console.log(room.data);
```

## 删除房间

同步删除房间。

`DELETE /rooms/{room_id}`

```javascript
await client.rooms.delete('0ccc7b54-4df3-4bca-a65a-3da1ecc777f0');
```

## 创建客户端令牌以加入房间

同步生成客户端令牌以加入房间。

`POST /rooms/{room_id}/actions/generate_join_client_token`

```javascript
const response = await client.rooms.actions.generateJoinClientToken(
  '0ccc7b54-4df3-4bca-a65a-3da1ecc777f0',
);

console.log(response.data);
```

## 刷新客户端令牌以加入房间

同步刷新客户端令牌以加入房间。

`POST /rooms/{room_id}/actions/refresh_client_token` — 需要参数：`refresh_token`

```javascript
const response = await client.rooms.actions.refreshClientToken(
  '0ccc7b54-4df3-4bca-a65a-3da1ecc777f0',
  {
    refresh_token:
      'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ0ZWxueXhfdGVsZXBob255IiwiZXhwIjoxNTkwMDEwMTQzLCJpYXQiOjE1ODc1OTA5NDMsImlzcyI6InRlbG55eF90ZWxlcGhvbnkiLCJqdGkiOiJiOGM3NDgzNy1kODllLTRhNjUtOWNmMi0zNGM3YTZmYTYwYzgiLCJuYmYiOjE1ODc1OTA5NDIsInN1YiI6IjVjN2FjN2QwLWRiNjUtNGYxMS05OGUxLWVlYzBkMWQ1YzZhZSIsInRlbF90b2tlbiI6InJqX1pra1pVT1pNeFpPZk9tTHBFVUIzc2lVN3U2UmpaRmVNOXMtZ2JfeENSNTZXRktGQUppTXlGMlQ2Q0JSbWxoX1N5MGlfbGZ5VDlBSThzRWlmOE1USUlzenl6U2xfYURuRzQ4YU81MHlhSEd1UlNZYlViU1ltOVdJaVEwZz09IiwidHlwIjoiYWNjZXNzIn0.gNEwzTow5MLLPLQENytca7pUN79PmPj6FyqZWW06ZeEmesxYpwKh0xRtA0TzLh6CDYIRHrI8seofOO0YFGDhpQ',
  },
);

console.log(response.data);
```

## 查看房间会话列表

`GET /rooms/{room_id}/sessions`

```javascript
// Automatically fetches more pages as needed.
for await (const roomSession of client.rooms.sessions.list1(
  '0ccc7b54-4df3-4bca-a65a-3da1ecc777f0',
)) {
  console.log(roomSession.id);
}
```