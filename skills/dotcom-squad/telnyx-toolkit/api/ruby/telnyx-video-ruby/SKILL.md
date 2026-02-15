---
name: telnyx-video-ruby
description: >-
  Create and manage video rooms for real-time video communication and
  conferencing. This skill provides Ruby SDK examples.
metadata:
  author: telnyx
  product: video
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Video - Ruby

## 安装

```bash
gem install telnyx
```

## 设置

```ruby
require "telnyx"

client = Telnyx::Client.new(
  api_key: ENV["TELNYX_API_KEY"], # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已经按照上述方式初始化。

## 查看房间组合列表。

`GET /room_compositions`

```ruby
page = client.room_compositions.list

puts(page)
```

## 创建房间组合。

异步创建房间组合。

`POST /room_compositions`

```ruby
room_composition = client.room_compositions.create

puts(room_composition)
```

## 查看房间组合信息。

`GET /room_compositions/{room_composition_id}`

```ruby
room_composition = client.room_compositions.retrieve("5219b3af-87c6-4c08-9b58-5a533d893e21")

puts(room_composition)
```

## 删除房间组合。

同步删除房间组合。

`DELETE /room_compositions/{room_composition_id}`

```ruby
result = client.room_compositions.delete("5219b3af-87c6-4c08-9b58-5a533d893e21")

puts(result)
```

## 查看房间参与者列表。

`GET /room_participants`

```ruby
page = client.room_participants.list

puts(page)
```

## 查看特定房间参与者信息。

`GET /room_participants/{room_participant_id}`

```ruby
room_participant = client.room_participants.retrieve("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")

puts(room_participant)
```

## 查看房间录制列表。

`GET /room_recordings`

```ruby
page = client.room_recordings.list

puts(page)
```

## 批量删除房间录制文件。

`DELETE /room_recordings`

```ruby
response = client.room_recordings.delete_bulk

puts(response)
```

## 查看特定房间录制文件信息。

`GET /room_recordings/{room_recording_id}`

```ruby
room_recording = client.room_recordings.retrieve("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")

puts(room_recording)
```

## 删除房间录制文件。

同步删除房间录制文件。

`DELETE /room_recordings/{room_recording_id}`

```ruby
result = client.room_recordings.delete("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")

puts(result)
```

## 查看房间会话列表。

`GET /room_sessions`

```ruby
page = client.rooms.sessions.list_0

puts(page)
```

## 查看特定房间会话信息。

`GET /room_sessions/{room_session_id}`

```ruby
session = client.rooms.sessions.retrieve("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")

puts(session)
```

## 结束房间会话。

注意：此操作也会将当前在房间中的所有参与者踢出。

`POST /room_sessions/{room_session_id}/actions/end`

```ruby
response = client.rooms.sessions.actions.end_("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")

puts(response)
```

## 将参与者从房间会话中踢出。

`POST /room_sessions/{room_session_id}/actions/kick`

```ruby
response = client.rooms.sessions.actions.kick("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")

puts(response)
```

## 将房间中的参与者静音。

`POST /room_sessions/{room_session_id}/actions/mute`

```ruby
response = client.rooms.sessions.actions.mute("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")

puts(response)
```

## 取消房间中参与者的静音状态。

`POST /room_sessions/{room_session_id}/actions/unmute`

```ruby
response = client.rooms.sessions.actions.unmute("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")

puts(response)
```

## 查看房间参与者列表。

`GET /room_sessions/{room_session_id}/participants`

```ruby
page = client.rooms.sessions.retrieve_participants("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")

puts(page)
```

## 查看房间列表。

`GET /rooms`

```ruby
page = client.rooms.list

puts(page)
```

## 创建新房间。

同步创建房间。

`POST /rooms`

```ruby
room = client.rooms.create

puts(room)
```

## 查看房间信息。

`GET /rooms/{room_id}`

```ruby
room = client.rooms.retrieve("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")

puts(room)
```

## 更新房间信息。

同步更新房间信息。

`PATCH /rooms/{room_id}`

```ruby
room = client.rooms.update("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")

puts(room)
```

## 删除房间。

同步删除房间。

`DELETE /rooms/{room_id}`

```ruby
result = client.rooms.delete("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")

puts(result)
```

## 创建客户端令牌以加入房间。

同步生成客户端令牌以加入房间。

`POST /rooms/{room_id}/actions/generate_join_client_token`

```ruby
response = client.rooms.actions.generate_join_client_token("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")

puts(response)
```

## 刷新客户端令牌以重新加入房间。

同步刷新客户端令牌以重新加入房间。

`POST /rooms/{room_id}/actions/refresh_client_token` — 需要参数：`refresh_token`

```ruby
response = client.rooms.actions.refresh_client_token(
  "0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
  refresh_token: "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ0ZWxueXhfdGVsZXBob255IiwiZXhwIjoxNTkwMDEwMTQzLCJpYXQiOjE1ODc1OTA5NDMsImlzcyI6InRlbG55eF90ZWxlcGhvbnkiLCJqdGkiOiJiOGM3NDgzNy1kODllLTRhNjUtOWNmMi0zNGM3YTZmYTYwYzgiLCJuYmYiOjE1ODc1OTA5NDIsInN1YiI6IjVjN2FjN2QwLWRiNjUtNGYxMS05OGUxLWVlYzBkMWQ1YzZhZSIsInRlbF90b2tlbiI6InJqX1pra1pVT1pNeFpPZk9tTHBFVUIzc2lVN3U2UmpaRmVNOXMtZ2JfeENSNTZXRktGQUppTXlGMlQ2Q0JSbWxoX1N5MGlfbGZ5VDlBSThzRWlmOE1USUlzenl6U2xfYURuRzQ4YU81MHlhSEd1UlNZYlViU1ltOVdJaVEwZz09IiwidHlwIjoiYWNjZXNzIn0.gNEwzTow5MLLPLQENytca7pUN79PmPj6FyqZWW06ZeEmesxYpwKh0xRtA0TzLh6CDYIRHrI8seofOO0YFGDhpQ"
)

puts(response)
```

## 查看房间会话列表。

`GET /rooms/{room_id}/sessions`

```ruby
page = client.rooms.sessions.list_1("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")

puts(page)
```