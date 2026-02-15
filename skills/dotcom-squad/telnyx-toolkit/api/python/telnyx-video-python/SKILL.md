---
name: telnyx-video-python
description: >-
  Create and manage video rooms for real-time video communication and
  conferencing. This skill provides Python SDK examples.
metadata:
  author: telnyx
  product: video
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Video - Python

## 安装

```bash
pip install telnyx
```

## 设置

```python
import os
from telnyx import Telnyx

client = Telnyx(
    api_key=os.environ.get("TELNYX_API_KEY"),  # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 查看房间组合列表

`GET /room_compositions`

```python
page = client.room_compositions.list()
page = page.data[0]
print(page.id)
```

## 创建房间组合

异步创建房间组合。

`POST /room_compositions`

```python
room_composition = client.room_compositions.create()
print(room_composition.data)
```

## 查看房间组合信息

`GET /room_compositions/{room_composition_id}`

```python
room_composition = client.room_compositions.retrieve(
    "5219b3af-87c6-4c08-9b58-5a533d893e21",
)
print(room_composition.data)
```

## 删除房间组合

同步删除房间组合。

`DELETE /room_compositions/{room_composition_id}`

```python
client.room_compositions.delete(
    "5219b3af-87c6-4c08-9b58-5a533d893e21",
)
```

## 查看房间参与者列表

`GET /room_participants`

```python
page = client.room_participants.list()
page = page.data[0]
print(page.id)
```

## 查看房间参与者信息

`GET /room_participants/{room_participant_id}`

```python
room_participant = client.room_participants.retrieve(
    "0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
)
print(room_participant.data)
```

## 查看房间录制列表

`GET /room_recordings`

```python
page = client.room_recordings.list()
page = page.data[0]
print(page.id)
```

## 批量删除房间录制文件

`DELETE /room_recordings`

```python
response = client.room_recordings.delete_bulk()
print(response.data)
```

## 查看房间录制文件信息

`GET /room_recordings/{room_recording_id}`

```python
room_recording = client.room_recordings.retrieve(
    "0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
)
print(room_recording.data)
```

## 删除房间录制文件

同步删除房间录制文件。

`DELETE /room_recordings/{room_recording_id}`

```python
client.room_recordings.delete(
    "0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
)
```

## 查看房间会话列表

`GET /room_sessions`

```python
page = client.rooms.sessions.list_0()
page = page.data[0]
print(page.id)
```

## 查看房间会话信息

`GET /room_sessions/{room_session_id}`

```python
session = client.rooms.sessions.retrieve(
    room_session_id="0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
)
print(session.data)
```

## 结束房间会话

注意：此操作也会将当前在房间中的所有参与者踢出。

`POST /room_sessions/{room_session_id}/actions/end`

```python
response = client.rooms.sessions.actions.end(
    "0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
)
print(response.data)
```

## 将参与者从房间会话中踢出

`POST /room_sessions/{room_session_id}/actions/kick`

```python
response = client.rooms.sessions.actions.kick(
    room_session_id="0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
)
print(response.data)
```

## 静音房间中的参与者

`POST /room_sessions/{room_session_id}/actions/mute`

```python
response = client.rooms.sessions.actions.mute(
    room_session_id="0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
)
print(response.data)
```

## 恢复房间中参与者的发言权

`POST /room_sessions/{room_session_id}/actions/unmute`

```python
response = client.rooms.sessions.actions.unmute(
    room_session_id="0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
)
print(response.data)
```

## 查看房间参与者列表

`GET /room_sessions/{room_session_id}/participants`

```python
page = client.rooms.sessions.retrieve_participants(
    room_session_id="0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
)
page = page.data[0]
print(page.id)
```

## 查看房间列表

`GET /rooms`

```python
page = client.rooms.list()
page = page.data[0]
print(page.id)
```

## 创建房间

同步创建房间。

`POST /rooms`

```python
room = client.rooms.create()
print(room.data)
```

## 查看房间信息

`GET /rooms/{room_id}`

```python
room = client.rooms.retrieve(
    room_id="0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
)
print(room.data)
```

## 更新房间信息

同步更新房间信息。

`PATCH /rooms/{room_id}`

```python
room = client.rooms.update(
    room_id="0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
)
print(room.data)
```

## 删除房间

同步删除房间。

`DELETE /rooms/{room_id}`

```python
client.rooms.delete(
    "0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
)
```

## 创建客户端令牌以加入房间

同步生成客户端令牌以加入房间。

`POST /rooms/{room_id}/actions/generate_join_client_token`

```python
response = client.rooms.actions.generate_join_client_token(
    room_id="0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
)
print(response.data)
```

## 刷新客户端令牌以加入房间

同步刷新客户端令牌以加入房间。

`POST /rooms/{room_id}/actions/refresh_client_token` — 需要参数：`refresh_token`

```python
response = client.rooms.actions.refresh_client_token(
    room_id="0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
    refresh_token="eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ0ZWxueXhfdGVsZXBob255IiwiZXhwIjoxNTkwMDEwMTQzLCJpYXQiOjE1ODc1OTA5NDMsImlzcyI6InRlbG55eF90ZWxlcGhvbnkiLCJqdGkiOiJiOGM3NDgzNy1kODllLTRhNjUtOWNmMi0zNGM3YTZmYTYwYzgiLCJuYmYiOjE1ODc1OTA5NDIsInN1YiI6IjVjN2FjN2QwLWRiNjUtNGYxMS05OGUxLWVlYzBkMWQ1YzZhZSIsInRlbF90b2tlbiI6InJqX1pra1pVT1pNeFpPZk9tTHBFVUIzc2lVN3U2UmpaRmVNOXMtZ2JfeENSNTZXRktGQUppTXlGMlQ2Q0JSbWxoX1N5MGlfbGZ5VDlBSThzRWlmOE1USUlzenl6U2xfYURuRzQ4YU81MHlhSEd1UlNZYlViU1ltOVdJaVEwZz09IiwidHlwIjoiYWNjZXNzIn0.gNEwzTow5MLLPLQENytca7pUN79PmPj6FyqZWW06ZeEmesxYpwKh0xRtA0TzLh6CDYIRHrI8seofOO0YFGDhpQ",
)
print(response.data)
```

## 查看房间会话列表

`GET /rooms/{room_id}/sessions`

```python
page = client.rooms.sessions.list_1(
    room_id="0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
)
page = page.data[0]
print(page.id)
```